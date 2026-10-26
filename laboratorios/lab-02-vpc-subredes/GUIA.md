# Lab 2 — VPC, subredes y grupos de seguridad

**Resumen:** Diseña una VPC de dos capas en dos zonas de disponibilidad, con salida a Internet solo para la capa pública y grupos de seguridad de mínimo privilegio.

**Asignatura:** Arquitectura en la Nube HEP · **Semana:** 2
**Duración estimada:** 75–90 min · **Entrega:** individual, en la plataforma
**Estación:** nube AWS simulada con `floci` (sin cuenta de AWS y sin Internet)

---

## 1. Qué vas a aprender

- diseñar una **VPC** con direccionamiento privado (RFC 1918);
- separar una **capa pública** y una **capa privada** en dos zonas de
  disponibilidad;
- dar salida a Internet solo a la capa pública con un **Internet Gateway** y
  una **tabla de rutas**;
- escribir **grupos de seguridad** de mínimo privilegio, con referencias entre
  grupos en vez de rangos abiertos.

La VPC de este laboratorio es fija: **`10.20.0.0/16`**. Los nombres y CIDR
también: el verificador los busca así.

---

## 2. El entorno

`floci` emula la API de EC2 en `http://127.0.0.1:4566`. Credenciales dummy:

```bash
source /etc/profile.d/lab-aws.sh
```

| Recurso | Nombre / valor |
|---|---|
| VPC | `10.20.0.0/16` |
| Subred pública A | `10.20.1.0/24` · `us-east-1a` |
| Subred pública B | `10.20.2.0/24` · `us-east-1b` |
| Subred privada A | `10.20.11.0/24` · `us-east-1a` |
| Subred privada B | `10.20.12.0/24` · `us-east-1b` |
| Internet Gateway | etiqueta `Name=igw-hep` |
| Tabla de rutas | etiqueta `Name=rt-publica` |
| Grupos | `sg-web`, `sg-db` |

Trabaja en `~/lab-02` (hay una hoja de apuntes). No hace falta crear instancias:
este laboratorio es de **red**.

---

## 3. Paso 1 — Crear la VPC y las cuatro subredes

```bash
VPC=$(aws ec2 create-vpc --cidr-block 10.20.0.0/16 \
  --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=vpc-hep}]' \
  --query 'Vpc.VpcId' --output text)
echo "$VPC"

aws ec2 create-subnet --vpc-id "$VPC" --cidr-block 10.20.1.0/24 \
  --availability-zone us-east-1a \
  --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=sub-pub-a}]'

aws ec2 create-subnet --vpc-id "$VPC" --cidr-block 10.20.2.0/24 \
  --availability-zone us-east-1b \
  --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=sub-pub-b}]'

aws ec2 create-subnet --vpc-id "$VPC" --cidr-block 10.20.11.0/24 \
  --availability-zone us-east-1a \
  --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=sub-priv-a}]'

aws ec2 create-subnet --vpc-id "$VPC" --cidr-block 10.20.12.0/24 \
  --availability-zone us-east-1b \
  --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=sub-priv-b}]'
```

Comprueba:

```bash
aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC" \
  --query 'Subnets[].{CIDR:CidrBlock,AZ:AvailabilityZone,IPPublica:MapPublicIpOnLaunch}' \
  --output table
```

**Criterio 1:** la VPC `10.20.0.0/16` y las 4 subredes con sus CIDR y AZ.

---

## 4. Paso 2 — Internet Gateway y tabla de rutas pública

```bash
IGW=$(aws ec2 create-internet-gateway \
  --tag-specifications 'ResourceType=internet-gateway,Tags=[{Key=Name,Value=igw-hep}]' \
  --query 'InternetGateway.InternetGatewayId' --output text)
aws ec2 attach-internet-gateway --vpc-id "$VPC" --internet-gateway-id "$IGW"

RT=$(aws ec2 create-route-table --vpc-id "$VPC" \
  --tag-specifications 'ResourceType=route-table,Tags=[{Key=Name,Value=rt-publica}]' \
  --query 'RouteTable.RouteTableId' --output text)

aws ec2 create-route --route-table-id "$RT" \
  --destination-cidr-block 0.0.0.0/0 --gateway-id "$IGW"

PUBA=$(aws ec2 describe-subnets --filters Name=cidr-block,Values=10.20.1.0/24 \
  --query 'Subnets[0].SubnetId' --output text)
PUBB=$(aws ec2 describe-subnets --filters Name=cidr-block,Values=10.20.2.0/24 \
  --query 'Subnets[0].SubnetId' --output text)

aws ec2 associate-route-table --subnet-id "$PUBA" --route-table-id "$RT"
aws ec2 associate-route-table --subnet-id "$PUBB" --route-table-id "$RT"
```

Las subredes privadas **no** se asocian a `rt-publica`: se quedan con la tabla
principal de la VPC, que solo tiene la ruta `local`. Esa es la diferencia entre
una capa con salida y una capa aislada.

**Criterio 2:** IGW adjunto y `rt-publica` con `0.0.0.0/0` → IGW, asociada a
las dos subredes públicas.

---

## 5. Paso 3 — Grupo `sg-web`

```bash
SG_WEB=$(aws ec2 create-security-group --group-name sg-web \
  --description "web publica" --vpc-id "$VPC" --query GroupId --output text)

aws ec2 authorize-security-group-ingress --group-id "$SG_WEB" --ip-permissions '[
 {"IpProtocol":"tcp","FromPort":80,"ToPort":80,"IpRanges":[{"CidrIp":"0.0.0.0/0","Description":"http"}]},
 {"IpProtocol":"tcp","FromPort":443,"ToPort":443,"IpRanges":[{"CidrIp":"0.0.0.0/0","Description":"https"}]},
 {"IpProtocol":"tcp","FromPort":22,"ToPort":22,"IpRanges":[{"CidrIp":"10.20.0.0/16","Description":"ssh interno"}]}
]'
```

**Criterio 3:** 80 y 443 desde `0.0.0.0/0`; 22 **solo** desde
`10.20.0.0/16`. Si abres SSH a Internet, el criterio falla.

---

## 6. Paso 4 — Grupo `sg-db`

La base de datos no se abre a Internet: solo acepta conexiones del grupo web.

```bash
SG_DB=$(aws ec2 create-security-group --group-name sg-db \
  --description "base de datos" --vpc-id "$VPC" --query GroupId --output text)

aws ec2 authorize-security-group-ingress --group-id "$SG_DB" --ip-permissions \
  "[{\"IpProtocol\":\"tcp\",\"FromPort\":5432,\"ToPort\":5432,
     \"UserIdGroupPairs\":[{\"GroupId\":\"$SG_WEB\",\"Description\":\"desde web\"}]}]"
```

Una regla con **origen en otro grupo** es más segura que una con un CIDR: si
mañana cambian las IP de la capa web, la regla sigue siendo correcta.

**Criterio 4:** `sg-db` permite 5432 solo desde `sg-web`, sin ningún
`0.0.0.0/0` ni `::/0`.

---

## 7. Paso 5 — Comprobar las subredes privadas

```bash
aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC" \
  --query 'Subnets[?MapPublicIpOnLaunch==`true`].CidrBlock' --output text

aws ec2 describe-route-tables --filters "Name=vpc-id,Values=$VPC" \
  --query 'RouteTables[].{ID:RouteTableId,Rutas:Routes[].DestinationCidrBlock,Asociaciones:Associations[].SubnetId}' \
  --output table
```

Debe ocurrir:

- las subredes privadas tienen `MapPublicIpOnLaunch = false`;
- su tabla de rutas no contiene `0.0.0.0/0`;
- la única tabla con `0.0.0.0/0` es `rt-publica`, asociada a las públicas.

**Criterio 5:** las privadas no auto-asignan IP pública y no tienen salida
`0.0.0.0/0`.

---

## 8. Paso 6 — Autocontrol

```bash
revisar
```

Debe terminar en **5 de 5**. El detalle de cada criterio te dice qué recurso
falta o qué regla está mal.

---

## 9. Criterios de evaluación

| # | Criterio | Qué se comprueba | Peso |
|---|---|---|---|
| 1 | `vpc_subredes` | VPC `10.20.0.0/16` y 4 subredes con CIDR/AZ exactos | 1,0 |
| 2 | `salida_publica` | IGW adjunto; `rt-publica` con `0.0.0.0/0` y 2 públicas | 1,0 |
| 3 | `sg_web` | 80/443 públicos; SSH solo desde `10.20.0.0/16` | 1,0 |
| 4 | `sg_db` | 5432 solo desde `sg-web`; sin `0.0.0.0/0` | 1,0 |
| 5 | `privadas_sin_salida` | privadas sin IP pública ni ruta `0.0.0.0/0` | 1,0 |

---

## 10. Problemas frecuentes

| Síntoma | Causa | Solución |
|---|---|---|
| `describe-subnets` vacío | `$VPC` vacío o de otra shell | vuelve a exportar `VPC` |
| `create-route` falla | el IGW no está adjunto | `attach-internet-gateway` primero |
| `associate-route-table` falla | la subred ya está en otra tabla | revisa `Associations` |
| `sg-db` falla | regla con `0.0.0.0/0` | elimínala y usa `sg-web` |
| `revisar` dice 4/5 | lee el detalle en rojo | corrige el recurso exacto |

No reinicies la nube ni la estación. Si `floci` no responde:
`curl -s http://127.0.0.1:4566/` y avisa al docente si persiste.

---

## 11. Para ir más allá (opcional)

- Añade una **subred privada de datos** en una tercera AZ (si la región la
  ofrece) y su tabla de rutas.
- Crea un **VPC Endpoint** de tipo Gateway para S3 y comprueba que la capa
  privada puede leer el bucket sin salir a Internet.
- Escribe una **Network ACL** que permita solo 80/443 de entrada a la capa
  pública y compara con el grupo de seguridad.

---

## 12. Entrega

El servidor evalúa el estado de tu VPC. Antes de cerrar, ejecuta `revisar` y
comprueba **5 de 5**.
