# Lab 6 — Alta disponibilidad, escalado e IaC

**Resumen:** Despliega con CloudFormation una red de dos zonas con ALB, y completa el despliegue con un launch template y un Auto Scaling Group que sirve la página desde dos instancias.

**Asignatura:** Arquitectura en la Nube HEP · **Semana:** 6
**Duración estimada:** 100–120 min · **Entrega:** individual, en la plataforma
**Estación:** nube AWS simulada con `floci` (sin cuenta de AWS y sin Internet)

---

## 1. Qué vas a aprender

- describir infraestructura como **código** con CloudFormation;
- repartir una aplicación en **dos zonas de disponibilidad**;
- configurar un **Application Load Balancer** con target group y listener;
- crear un **launch template** y un **Auto Scaling Group** (2/4/2);
- comprobar que las dos instancias del grupo sirven la página.

Este es el laboratorio de cierre: combina red (Lab 2), cómputo (Lab 4) y
automatización. La plantilla crea la red y el balanceador; el launch template y
el ASG se crean con la CLI porque el emulador **no crea
`AWS::EC2::LaunchTemplate` desde CloudFormation** (limitación documentada).

---

## 2. El entorno

`floci` emula las APIs de CloudFormation, EC2, ELBv2 y Auto Scaling en
`http://127.0.0.1:4566`. Credenciales dummy:

```bash
source /etc/profile.d/lab-aws.sh
```

| Recurso | Nombre / valor |
|---|---|
| Stack | `hep-ha` |
| VPC | `10.40.0.0/16` |
| Subredes | `10.40.1.0/24` (`us-east-1a`) · `10.40.2.0/24` (`us-east-1b`) |
| Balanceador | `alb-hep` · 2 AZ · listener HTTP:80 |
| Target group | `tg-hep` · HTTP:80 |
| Launch template | `lt-hep` · `ami-hep-app` · `t3.micro` |
| Auto Scaling Group | `asg-hep` · min 2 / max 4 / desired 2 |

Trabaja en `~/lab-06`. Allí está `plantilla-ha.json`, la plantilla base del
stack, y una hoja de apuntes.

> **Limitaciones del emulador:** el ALB se crea y se configura, pero **no
> enruta tráfico real** a las instancias (floci no vive dentro de la VPC). Las
> páginas se comprueban por el puerto publicado de cada instancia. El stack
> tampoco crea `AWS::EC2::LaunchTemplate`; por eso el LT y el ASG van por CLI.

---

## 3. Paso 1 — Leer la plantilla

```bash
cd ~/lab-06
cat plantilla-ha.json
```

La plantilla declara:

- `VPC`, `SubA`, `SubB` (dos zonas), `IGW`, `IGWAttach`, `RT`, `Ruta` y las
  asociaciones de subred;
- `SG` con TCP 80 desde `0.0.0.0/0`;
- `ALB` con las dos subredes y el grupo;
- `TG` HTTP:80 y `Listener` en el puerto 80 que reenvía al target group.

Los `Ref` son la clave: `{"Ref": "SubA"}` pasa el ID de la subred al ALB, y
`{"Ref": "TG"}` pasa el ARN del target group al listener. CloudFormation
calcula el orden de creación.

**Criterio 1:** el stack `hep-ha` termina en `CREATE_COMPLETE`.

---

## 4. Paso 2 — Crear el stack

```bash
aws cloudformation create-stack \
  --stack-name hep-ha \
  --template-body file://plantilla-ha.json

aws cloudformation wait stack-create-complete --stack-name hep-ha

aws cloudformation describe-stacks --stack-name hep-ha \
  --query 'Stacks[0].StackStatus' --output text
```

Inspecciona los recursos creados y sus IDs físicos:

```bash
aws cloudformation describe-stack-resources --stack-name hep-ha \
  --query 'StackResources[].{Logico:LogicalResourceId,Tipo:ResourceType,Estado:ResourceStatus,Fisico:PhysicalResourceId}' \
  --output table
```

Deben aparecer `VPC`, `SubA`, `SubB`, `IGW`, `RT`, `SG`, `ALB`, `TG` y
`Listener` en `CREATE_COMPLETE`. Guarda el ID del grupo:

```bash
SG=$(aws cloudformation describe-stack-resource --stack-name hep-ha \
  --logical-resource-id SG --query 'StackResourceDetail.PhysicalResourceId' \
  --output text)
echo "$SG"
```

---

## 5. Paso 3 — El launch template

El launch template es el «molde» de las instancias: AMI, tipo, grupo de
seguridad y user-data. El ASG lo usa para lanzar cada réplica.

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
  <p>Instancia del Auto Scaling Group.</p>
  <p>Laboratorio 6 — Alta disponibilidad.</p>
</body>
</html>
HTML
httpd -f -p 80 -h /www
SH

UD=$(base64 -w0 user-data.sh)
cat > lt-hep.json <<JSON
{"ImageId":"ami-hep-app","InstanceType":"t3.micro",
 "SecurityGroupIds":["$SG"],"UserData":"$UD"}
JSON

aws ec2 create-launch-template --launch-template-name lt-hep \
  --launch-template-data file://lt-hep.json
```

El campo `UserData` de un launch template va en **base64** (a diferencia de
`run-instances --user-data file://`, que codifica solo). Comprueba la versión:

```bash
LTID=$(aws ec2 describe-launch-templates --launch-template-names lt-hep \
  --query 'LaunchTemplates[0].LaunchTemplateId' --output text)

aws ec2 describe-launch-template-versions \
  --launch-template-id "$LTID" --versions '$Latest' \
  --query 'LaunchTemplateVersions[0].LaunchTemplateData'
```

**Criterio 3:** `lt-hep` usa `ami-hep-app` y su user-data decodifica con
`httpd` y `CaribeMart`.

---

## 6. Paso 4 — El Auto Scaling Group

```bash
SUBA=$(aws ec2 describe-subnets --filters Name=tag:Name,Values=sub-ha-a \
  --query 'Subnets[0].SubnetId' --output text)
SUBB=$(aws ec2 describe-subnets --filters Name=tag:Name,Values=sub-ha-b \
  --query 'Subnets[0].SubnetId' --output text)

TGARN=$(aws elbv2 describe-target-groups --names tg-hep \
  --query 'TargetGroups[0].TargetGroupArn' --output text)

aws autoscaling create-auto-scaling-group \
  --auto-scaling-group-name asg-hep \
  --launch-template LaunchTemplateId="$LTID",Version='$Latest' \
  --min-size 2 --max-size 4 --desired-capacity 2 \
  --vpc-zone-identifier "$SUBA,$SUBB" \
  --target-group-arns "$TGARN" \
  --tags Key=Name,Value=asg-hep,PropagateAtLaunch=true
```

- `--desired-capacity 2` lanza dos réplicas ahora;
- `--min-size 2` mantiene al menos dos aunque una falle;
- `--max-size 4` pone el techo del escalado;
- `--vpc-zone-identifier` reparte las instancias entre las dos subredes;
- `--target-group-arns` registra el grupo en el target group del ALB.

Espera a que el grupo tenga sus instancias:

```bash
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names asg-hep \
  --query 'AutoScalingGroups[0].{Min:MinSize,Max:MaxSize,Desired:DesiredCapacity,Instancias:Instances[].InstanceId}' \
  --output json
```

**Criterio 2:** `asg-hep` con min 2 / max 4 / desired 2 y al menos dos
instancias `running`.

---

## 7. Paso 5 — Comprobar el ALB y las dos páginas

Configuración del balanceador:

```bash
aws elbv2 describe-load-balancers --names alb-hep \
  --query 'LoadBalancers[0].{Estado:State.Code,Zonas:AvailabilityZones[].ZoneName,SG:SecurityGroups}' \
  --output json

aws elbv2 describe-listeners \
  --load-balancer-arn "$(aws elbv2 describe-load-balancers --names alb-hep \
    --query 'LoadBalancers[0].LoadBalancerArn' --output text)"

aws elbv2 describe-target-groups --names tg-hep \
  --query 'TargetGroups[0].{Protocolo:Protocol,Puerto:Port,ALB:LoadBalancerArns}' \
  --output json
```

Debe haber **dos zonas**, un listener en el puerto **80** y `tg-hep` en
**HTTP:80** asociado a `alb-hep`.

Para las páginas, usa el puerto publicado de cada instancia:

```bash
for IID in $(aws autoscaling describe-auto-scaling-groups \
  --auto-scaling-group-names asg-hep \
  --query 'AutoScalingGroups[0].Instances[].InstanceId' --output text); do
  ESTADO=$(aws ec2 describe-instances --instance-ids "$IID" \
    --query 'Reservations[0].Instances[0].State.Name' --output text)
  PUERTO=$(docker ps --format '{{.Names}} {{.Ports}}' \
    | sed -n "s/^floci-aws-ec2-fwd-$IID-80 .*0\.0\.0\.0:\([0-9]*\)->80.*/\1/p" \
    | head -1)
  echo "$IID $ESTADO puerto=$PUERTO"
  curl -s "http://127.0.0.1:$PUERTO/" | grep -o 'CaribeMart HEP'
done
```

Las dos deben estar `running` y devolver `CaribeMart HEP`. La pestaña
**Sitio web** del laboratorio muestra una de ellas.

**Criterios 4 y 5:** ALB en 2 AZ con listener y TG; al menos dos instancias
running responden 200 con la marca.

---

## 8. Paso 6 — Autocontrol

```bash
revisar
```

Debe terminar en **5 de 5**. Si `instancias_sirven` falla, espera unos segundos:
el ASG tarda en arrancar los contenedores.

---

## 9. Criterios de evaluación

| # | Criterio | Qué se comprueba | Peso |
|---|---|---|---|
| 1 | `stack` | `hep-ha` en `CREATE_COMPLETE` | 1,0 |
| 2 | `asg` | `asg-hep` min 2 / max 4 / desired 2 y ≥2 instancias | 1,0 |
| 3 | `launch_template` | `lt-hep` con `ami-hep-app` y user-data con la página | 1,0 |
| 4 | `alb` | 2 AZ, listener 80 y `tg-hep` HTTP/80 | 1,0 |
| 5 | `instancias_sirven` | ≥2 instancias running responden 200 con la marca | 1,0 |

---

## 10. Problemas frecuentes

| Síntoma | Causa | Solución |
|---|---|---|
| El stack queda en `ROLLBACK` | error en la plantilla o un tipo no soportado | revisa `describe-stack-events` |
| No aparece `lt-hep` | el LT no se creó o el nombre está mal | créalo con `create-launch-template` |
| El ASG tiene 0 instancias | launch template inexistente o subred mala | revisa `Instances` y los IDs |
| Una instancia no responde | `httpd` no arrancó | decodifica el user-data y revisa el script |
| `alb` en rojo | falta una AZ, el listener o el TG | revisa los tres `describe` |
| `instancias_sirven` en rojo | el ASG aún está arrancando | espera y vuelve a ejecutar `revisar` |

No reinicies la nube ni la estación. Si `floci` no responde:
`curl -s http://127.0.0.1:4566/` y avisa al docente si persiste.

---

## 11. Para ir más allá (opcional)

- Añade una política de **escalado por CPU** (target tracking) al ASG.
- Convierte el launch template y el ASG en recursos de CloudFormation y explica
  por qué en AWS real sí funcionaría (en floci no).
- Diseña un **health check** de `/salud` y explica qué hace el ALB cuando una
  instancia falla.
- Compara esta arquitectura con la del Lab 4: ¿qué se ganó y qué se pagó?

---

## 12. Entrega

El servidor evalúa el stack, el ASG, el launch template, el ALB y las dos
páginas. Antes de cerrar, ejecuta `revisar` y comprueba **5 de 5**.
