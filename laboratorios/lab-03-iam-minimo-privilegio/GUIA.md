# Lab 3 — IAM, roles y mínimo privilegio

**Resumen:** Crea un rol de EC2 con una política de solo lectura sobre el bucket del sitio, un instance profile que lo use y un usuario auditor con una denegación explícita.

**Asignatura:** Arquitectura en la Nube HEP · **Semana:** 3
**Duración estimada:** 75–90 min · **Entrega:** individual, en la plataforma
**Estación:** nube AWS simulada con `floci` (sin cuenta de AWS y sin Internet)

---

## 1. Qué vas a aprender

- distinguir **usuario**, **rol**, **política** e **instance profile**;
- escribir una **política de confianza** para que un servicio asuma un rol;
- aplicar **mínimo privilegio**: solo las acciones y los recursos necesarios;
- usar un **Deny explícito** para blindar una operación destructiva;
- leer políticas IAM con la CLI y comprobar que no haya comodines.

El laboratorio trabaja sobre el bucket `sitio-hep` del Lab 1. Si en esta
estación el bucket no existe todavía, no importa: las políticas se escriben
sobre su **ARN** y el verificador revisa el documento declarado.

---

## 2. El entorno

`floci` emula la API de IAM en `http://127.0.0.1:4566`. Credenciales dummy:

```bash
source /etc/profile.d/lab-aws.sh
```

| Recurso | Nombre / valor |
|---|---|
| Rol | `rol-app-hep` |
| Confianza | `ec2.amazonaws.com` · `sts:AssumeRole` |
| Política inline del rol | `politica-leer-sitio` |
| Permisos | `s3:GetObject` en `arn:aws:s3:::sitio-hep/*` · `s3:ListBucket` en `arn:aws:s3:::sitio-hep` |
| Instance profile | `perfil-app-hep` |
| Usuario auditor | `auditor-hep` |
| Allow del auditor | `s3:ListAllMyBuckets` |
| Deny del auditor | `s3:DeleteObject` |

Trabaja en `~/lab-03` (hay una hoja de apuntes). No hace falta crear
instancias ni buckets para este laboratorio.

> **Importante:** floci guarda y devuelve las políticas, pero **no evalúa
> permisos** cuando llamas a S3 (la aplicación de políticas está desactivada).
> En AWS real sí se evalúan. Por eso el laboratorio se califica sobre la
> política declarada: es el mismo documento que usarías en producción.

---

## 3. Paso 1 — La política de confianza y el rol

Un rol no tiene contraseña: lo **asume** un servicio o usuario de confianza.
La política de confianza dice quién puede asumirlo.

```bash
cat > confianza.json <<'JSON'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {"Service": "ec2.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }
  ]
}
JSON

aws iam create-role \
  --role-name rol-app-hep \
  --assume-role-policy-document file://confianza.json
```

Comprueba que la confianza quedó bien:

```bash
aws iam get-role --role-name rol-app-hep \
  --query 'Role.AssumeRolePolicyDocument' --output json
```

**Criterio 1:** `rol-app-hep` existe y confía en `ec2.amazonaws.com` con
`sts:AssumeRole`, sin `Principal: "*"`.

---

## 4. Paso 2 — La política de solo lectura

La política permite leer el sitio y listar el bucket. Nada más: ni borrar, ni
subir, ni tocar otro bucket.

```bash
cat > politica-leer-sitio.json <<'JSON'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject"],
      "Resource": "arn:aws:s3:::sitio-hep/*"
    },
    {
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": "arn:aws:s3:::sitio-hep"
    }
  ]
}
JSON

aws iam put-role-policy \
  --role-name rol-app-hep \
  --policy-name politica-leer-sitio \
  --policy-document file://politica-leer-sitio.json
```

Fíjate en la diferencia de recursos:

- `GetObject` actúa sobre **objetos** → `arn:aws:s3:::sitio-hep/*`;
- `ListBucket` actúa sobre el **bucket** → `arn:aws:s3:::sitio-hep`.

Cambiar esos ARN es el error más común: la política queda sintácticamente
válida pero no permite lo que se pide.

**Criterio 2:** `politica-leer-sitio` permite exactamente
`GetObject` sobre los objetos y `ListBucket` sobre el bucket, y ningún otro
par acción/recurso.

---

## 5. Paso 3 — Sin comodines

Revisa todas las políticas del rol:

```bash
aws iam list-role-policies --role-name rol-app-hep
aws iam list-attached-role-policies --role-name rol-app-hep

aws iam get-role-policy \
  --role-name rol-app-hep \
  --policy-name politica-leer-sitio \
  --query 'PolicyDocument' --output json
```

No debe aparecer:

- `"Action": "*"` ni acciones terminadas en `:*` (`s3:*`, `iam:*`…);
- `"Resource": "*"`;
- `NotAction` / `NotResource`, que es otra forma de decir «todo menos…».

**Criterio 3:** ninguna política del rol (inline o adjunta) usa comodines.

---

## 6. Paso 4 — El instance profile

Una instancia EC2 no recibe un rol directamente: recibe un **instance
profile**, que es el envoltorio del rol.

```bash
aws iam create-instance-profile --instance-profile-name perfil-app-hep

aws iam add-role-to-instance-profile \
  --instance-profile-name perfil-app-hep \
  --role-name rol-app-hep
```

Comprueba la relación:

```bash
aws iam get-instance-profile --instance-profile-name perfil-app-hep \
  --query 'InstanceProfile.Roles[].RoleName' --output text
```

**Criterio 4:** `perfil-app-hep` existe y contiene `rol-app-hep`.

---

## 7. Paso 5 — El usuario auditor y el Deny explícito

El auditor solo necesita **ver** qué buckets hay. Para que no pueda borrar
objetos ni por error, se agrega un `Deny` explícito. En IAM, un `Deny`
explícito **siempre gana**, incluso sobre un `Allow` de otro lado.

```bash
aws iam create-user --user-name auditor-hep

cat > politica-auditor.json <<'JSON'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:ListAllMyBuckets"],
      "Resource": "*"
    },
    {
      "Effect": "Deny",
      "Action": ["s3:DeleteObject"],
      "Resource": "arn:aws:s3:::sitio-hep/*"
    }
  ]
}
JSON

aws iam put-user-policy \
  --user-name auditor-hep \
  --policy-name politica-auditor \
  --policy-document file://politica-auditor.json
```

El `Resource: "*"` del `Allow` es correcto aquí: `ListAllMyBuckets` no actúa
sobre un bucket concreto. El criterio de «sin comodines» se aplica al rol, no
al usuario auditor; aun así, el `Deny` sí está acotado a los objetos del sitio.

**Criterio 5:** `auditor-hep` tiene un `Allow` de `s3:ListAllMyBuckets` y un
`Deny` explícito de `s3:DeleteObject`.

---

## 8. Paso 6 — Autocontrol

```bash
revisar
```

Debe terminar en **5 de 5**. Si algo falla, el detalle indica el recurso o la
acción exacta que no coincide.

---

## 9. Criterios de evaluación

| # | Criterio | Qué se comprueba | Peso |
|---|---|---|---|
| 1 | `rol_confianza` | `rol-app-hep` confía en EC2 con `sts:AssumeRole` | 1,0 |
| 2 | `politica_bucket` | `politica-leer-sitio`: solo GetObject y ListBucket | 1,0 |
| 3 | `sin_comodines` | políticas del rol sin `*`, `:*` ni `NotAction` | 1,0 |
| 4 | `instance_profile` | `perfil-app-hep` contiene `rol-app-hep` | 1,0 |
| 5 | `usuario_auditor` | Allow de listar + Deny explícito de borrar | 1,0 |

---

## 10. Problemas frecuentes

| Síntoma | Causa | Solución |
|---|---|---|
| `MalformedPolicyDocument` | JSON inválido o comillas sin escapar | valida el archivo con `python3 -m json.tool` |
| El rol no confía en EC2 | `Principal` mal escrito o falta `sts:AssumeRole` | revisa `get-role` |
| `politica_bucket` en rojo | ARN de bucket y de objetos intercambiados | `GetObject` → `/*`; `ListBucket` → bucket |
| `sin_comodines` en rojo | quedó un `s3:*` o un `Resource: "*"` | acota acción y recurso |
| El perfil no tiene rol | faltó `add-role-to-instance-profile` | agrégalo y repite |
| `usuario_auditor` en rojo | el `Deny` no es explícito o la acción está mal | usa `Effect: "Deny"` y `s3:DeleteObject` |

No reinicies la nube ni la estación. Si `floci` no responde:
`curl -s http://127.0.0.1:4566/` y avisa al docente si persiste.

---

## 11. Para ir más allá (opcional)

- Crea un **grupo** `auditores` con la política del auditor y agrega el usuario;
  compara cuántas políticas quedan en el usuario.
- Añade una **condición** (`Condition`) que exija MFA para borrar objetos.
- Diseña una política que permita `s3:PutObject` solo bajo el prefijo
  `entregas/` y explica por qué el prefijo debe terminar en `/*`.
- Lee la documentación de IAM sobre **permissions boundaries** y describe un
  caso donde te sirvan.

---

## 12. Entrega

El servidor evalúa las políticas declaradas en tu cuenta. Antes de cerrar,
ejecuta `revisar` y comprueba **5 de 5**.
