# Lab 4 — Cómputo con sitio dinámico

**Resumen:** Lanza una instancia EC2 con user-data que sirve una página generada, abre solo el puerto 80, publica el sitio y le asigna una dirección IP elástica.

**Asignatura:** Arquitectura en la Nube HEP · **Semana:** 4
**Duración estimada:** 75–90 min · **Entrega:** individual, en la plataforma
**Estación:** nube AWS simulada con `floci` (sin cuenta de AWS y sin Internet)

---

## 1. Qué vas a aprender

- lanzar una **instancia EC2** con una AMI y un tipo de instancia concretos;
- automatizar el arranque con **user-data** (el «primer boot» de la instancia);
- abrir **solo** el puerto necesario en un grupo de seguridad;
- comprobar que el servicio responde por su **puerto publicado**;
- asociar una **IP elástica** para que la dirección no cambie.

La instancia de este laboratorio es un contenedor real del motor local. floci
publica su puerto 80 en `127.0.0.1:30000+` para que puedas abrirlo desde la
terminal y desde la vista «Sitio web».

---

## 2. El entorno

`floci` emula la API de EC2 en `http://127.0.0.1:4566`. Credenciales dummy:

```bash
source /etc/profile.d/lab-aws.sh
```

| Recurso | Nombre / valor |
|---|---|
| VPC | `10.30.0.0/16` |
| Subred | `10.30.1.0/24` · `us-east-1a` |
| Grupo de seguridad | `sg-app` · TCP 80 desde `0.0.0.0/0` |
| Instancia | `web-hep` · `ami-hep-app` · `t3.micro` |
| User-data | script que crea la página y arranca `httpd` |
| IP elástica | `eip-hep` |

Trabaja en `~/lab-04` (hay una hoja de apuntes). La AMI del lab es BusyBox:
trae `sh`, `httpd`, `wget` y `nc`. **No hay Internet** dentro de la instancia,
así que no intentes instalar paquetes: todo se hace con esas herramientas.

---

## 3. Paso 1 — Red y grupo de seguridad

```bash
VPC=$(aws ec2 create-vpc --cidr-block 10.30.0.0/16 \
  --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=vpc-app-hep}]' \
  --query 'Vpc.VpcId' --output text)

SUB=$(aws ec2 create-subnet --vpc-id "$VPC" --cidr-block 10.30.1.0/24 \
  --availability-zone us-east-1a \
  --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=sub-app-hep}]' \
  --query 'Subnet.SubnetId' --output text)

SG=$(aws ec2 create-security-group --group-name sg-app \
  --description "web del laboratorio" --vpc-id "$VPC" \
  --query GroupId --output text)

aws ec2 authorize-security-group-ingress \
  --group-id "$SG" --protocol tcp --port 80 --cidr 0.0.0.0/0
```

**Criterio 3:** `sg-app` permite TCP 80 desde `0.0.0.0/0`. No abras SSH ni
otros puertos «por si acaso»: el mínimo privilegio también aplica a la red.

---

## 4. Paso 2 — El user-data

El user-data es un script que la instancia ejecuta al arrancar. En la AMI del
lab el servidor web es `httpd` de BusyBox.

```bash
cat > user-data.sh <<'SH'
#!/bin/sh
mkdir -p /www
cat > /www/index.html <<'HTML'
<!doctype html>
<html lang="es">
<head><meta charset="utf-8"><title>CaribeMart HEP</title></head>
<body>
  <h1>CaribeMart HEP</h1>
  <p>Sitio dinámico servido desde una instancia EC2.</p>
  <p>Laboratorio 4 — Arquitectura en la Nube.</p>
</body>
</html>
HTML
httpd -f -p 80 -h /www
SH
```

Dos detalles importantes:

- `httpd -f` lo deja en **primer plano**. Si el proceso termina, el contenedor
  de la instancia termina y el puerto deja de responder.
- el `<<'HTML'` entre comillas evita que la shell expanda variables dentro del
  HTML.

---

## 5. Paso 3 — Lanzar la instancia

```bash
IID=$(aws ec2 run-instances \
  --image-id ami-hep-app \
  --instance-type t3.micro \
  --subnet-id "$SUB" \
  --security-group-ids "$SG" \
  --user-data file://user-data.sh \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=web-hep}]' \
  --query 'Instances[0].InstanceId' --output text)
echo "$IID"

aws ec2 wait instance-running --instance-ids "$IID"
```

Comprueba el estado y el user-data guardado:

```bash
aws ec2 describe-instances --instance-ids "$IID" \
  --query 'Reservations[0].Instances[0].{Estado:State.Name,AMI:ImageId,Tipo:InstanceType}' \
  --output table

aws ec2 describe-instance-attribute --instance-id "$IID" \
  --attribute userData --query 'UserData.Value' --output text | base64 -d
```

La API devuelve el user-data en **base64**; al decodificarlo debe verse tu
script completo, con `httpd` y `CaribeMart`.

**Criterios 1 y 2:** instancia `web-hep` running con `ami-hep-app` y
`t3.micro`; user-data decodificable con servidor HTTP y la marca.

---

## 6. Paso 4 — Comprobar el sitio publicado

floci publica el puerto 80 de la instancia en un puerto `30xxx` del host de la
estación. El puerto cambia en cada arranque; se descubre con `docker ps`:

```bash
docker ps --format '{{.Names}} {{.Ports}}' | grep floci-aws-ec2-fwd
```

Busca la línea `floci-aws-ec2-fwd-<tu-instancia>-80` y el puerto
`0.0.0.0:30xxx->80/tcp`. Luego:

```bash
PORT=30xxx        # el que viste
curl -i "http://127.0.0.1:$PORT/"
```

Debe responder `HTTP/1.1 200 OK` y el HTML con `CaribeMart HEP`. También puedes
abrir la pestaña **Sitio web** del laboratorio: el proxy busca ese mismo puerto.

**Criterio 4:** el puerto publicado responde 200 y el cuerpo contiene
`CaribeMart HEP`.

---

## 7. Paso 5 — La IP elástica

Una IP elástica es una dirección pública que puedes mover entre instancias sin
que cambie. Así el sitio no depende de la IP efímera del arranque.

```bash
ALLOC=$(aws ec2 allocate-address --domain vpc \
  --tag-specifications 'ResourceType=elastic-ip,Tags=[{Key=Name,Value=eip-hep}]' \
  --query 'AllocationId' --output text)

aws ec2 associate-address --instance-id "$IID" --allocation-id "$ALLOC"

aws ec2 describe-addresses --filters Name=tag:Name,Values=eip-hep \
  --query 'Addresses[].{IP:PublicIp,Instancia:InstanceId}' --output table
```

**Criterio 5:** existe `eip-hep` y está asociada a `web-hep`.

> En AWS real, una instancia en una subred privada no sería alcanzable aunque
> tuviera EIP: haría falta una subred pública con ruta al Internet Gateway
> (Lab 2). floci publica el puerto localmente para que el laboratorio funcione
> sin salir a Internet; la diferencia se explica en clase.

---

## 8. Paso 6 — Autocontrol

```bash
revisar
```

Debe terminar en **5 de 5**. Si `http_200` falla, revisa el user-data y el
puerto publicado antes de tocar nada más.

---

## 9. Criterios de evaluación

| # | Criterio | Qué se comprueba | Peso |
|---|---|---|---|
| 1 | `instancia` | `web-hep` running, `ami-hep-app`, `t3.micro` | 1,0 |
| 2 | `user_data` | base64 decodificable, `httpd` y `CaribeMart` | 1,0 |
| 3 | `sg_app` | TCP 80 desde `0.0.0.0/0` | 1,0 |
| 4 | `http_200` | puerto publicado → 200 con `CaribeMart HEP` | 1,0 |
| 5 | `eip` | `eip-hep` asociada a la instancia | 1,0 |

---

## 10. Problemas frecuentes

| Síntoma | Causa | Solución |
|---|---|---|
| La instancia queda `pending` | el motor está creando el contenedor | espera con `aws ec2 wait instance-running` |
| `http_200` falla con 000 | `httpd` no arrancó o terminó | revisa el user-data; debe quedar en primer plano |
| La página responde 404 | `httpd` apunta a otra carpeta | usa `-h /www` y crea allí `index.html` |
| El puerto no aparece | la instancia no está running | `docker ps` y `describe-instances` |
| `allocate-address` falla | falta `--domain vpc` | agrégalo |
| `eip` en rojo | no asociaste la dirección | `associate-address --instance-id` |

No reinicies la nube ni la estación. Si `floci` no responde:
`curl -s http://127.0.0.1:4566/` y avisa al docente si persiste.

---

## 11. Para ir más allá (opcional)

- Añade una segunda instancia y un **Application Load Balancer** (lo verás en
  el Lab 6).
- Sirve una página distinta según la hora con un script en el user-data.
- Investiga qué es una **AMI** y por qué la del lab es distinta de las de AWS.
- Explica qué cambiaría si la instancia estuviera en una subred privada.

---

## 12. Entrega

El servidor evalúa la instancia, su user-data, el grupo y la EIP. Antes de
cerrar, ejecuta `revisar` y comprueba **5 de 5**.
