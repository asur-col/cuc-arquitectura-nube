# Lab 5 — Base de datos administrada y respaldos

**Resumen:** Crea una base PostgreSQL administrada y privada, carga pedidos, genera un snapshot y restaura una instancia nueva comprobando que los datos sobreviven.

**Asignatura:** Arquitectura en la Nube HEP · **Semana:** 5
**Duración estimada:** 75–90 min · **Entrega:** individual, en la plataforma
**Estación:** nube AWS simulada con `floci` (sin cuenta de AWS y sin Internet)

---

## 1. Qué vas a aprender

- crear una **base de datos administrada** (RDS) sin instalar ni administrar el
  servidor;
- elegir motor, clase, almacenamiento y **retención de respaldos**;
- mantener la base **privada**, fuera del alcance de Internet;
- conectarte con `psql` y cargar datos;
- generar un **snapshot** y **restaurar** una instancia nueva;
- comprobar que los datos sobreviven a la restauración.

RDS en floci es un contenedor PostgreSQL real. El endpoint queda en
`127.0.0.1` y el puerto cambia con cada instancia (`7001`, `7002`, …); se
descubre con `describe-db-instances`.

---

## 2. El entorno

`floci` emula la API de RDS en `http://127.0.0.1:4566`. Credenciales dummy:

```bash
source /etc/profile.d/lab-aws.sh
```

| Recurso | Nombre / valor |
|---|---|
| Instancia | `db-hep` |
| Motor | `postgres` |
| Clase | `db.t3.micro` |
| Almacenamiento | 20 GiB |
| Pública | **no** |
| Retención de respaldos | 7 días |
| Usuario maestro | `admin` |
| Clave maestra | `ClaveLab123` |
| Base | `pedidos` |
| Snapshot | `snap-hep` |
| Restaurada | `db-hep-restaurada` |

Trabaja en `~/lab-05` (hay una hoja de apuntes). El cliente `psql` ya está
instalado en la estación; no hace falta instalar nada.

> La clave `ClaveLab123` es **dummy**, solo para esta nube local. En un
> laboratorio real se usaría un gestor de secretos, nunca texto plano en el
> repositorio.

---

## 3. Paso 1 — Crear la instancia RDS

```bash
aws rds create-db-instance \
  --db-instance-identifier db-hep \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --allocated-storage 20 \
  --master-username admin \
  --master-user-password 'ClaveLab123' \
  --db-name pedidos \
  --backup-retention-period 7 \
  --no-publicly-accessible \
  --tags Key=Name,Value=db-hep
```

`--no-publicly-accessible` deja la base sin dirección pública: solo se llega a
ella desde la red privada. Es el valor correcto para una base de producción.

Espera a que esté disponible y mira su endpoint:

```bash
aws rds wait db-instance-available --db-instance-identifier db-hep

aws rds describe-db-instances --db-instance-identifier db-hep \
  --query 'DBInstances[0].{Estado:DBInstanceStatus,Motor:Engine,Clase:DBInstanceClass,GiB:AllocatedStorage,Publica:PubliclyAccessible,Puerto:Endpoint.Port}'
```

**Criterios 1 y 2:** `db-hep` available, postgres, `db.t3.micro`, 20 GiB,
privada; retención ≥ 7 días.

---

## 4. Paso 2 — Conectarse y cargar pedidos

Toma el puerto del endpoint y conéctate con `psql`:

```bash
PUERTO=$(aws rds describe-db-instances --db-instance-identifier db-hep \
  --query 'DBInstances[0].Endpoint.Port' --output text)
echo "$PUERTO"

PGPASSWORD='ClaveLab123' psql -h 127.0.0.1 -p "$PUERTO" -U admin -d pedidos
```

Dentro de `psql`, crea la tabla y carga dos pedidos:

```sql
CREATE TABLE pedidos (
  id serial PRIMARY KEY,
  cliente text NOT NULL,
  total numeric(10,2) NOT NULL
);

INSERT INTO pedidos (cliente, total) VALUES
  ('Ana', 125000.00),
  ('Luis', 98000.50);

SELECT count(*) FROM pedidos;
\q
```

También puedes hacerlo sin entrar a la consola interactiva:

```bash
PGPASSWORD='ClaveLab123' psql -h 127.0.0.1 -p "$PUERTO" -U admin -d pedidos \
  -c 'SELECT * FROM pedidos;'
```

**Criterio 3:** `psql` conecta con `admin` a la base `pedidos` y la tabla tiene
al menos 2 filas.

---

## 5. Paso 3 — Crear el snapshot

Un snapshot es una copia consistente del almacenamiento en un instante.

```bash
aws rds create-db-snapshot \
  --db-instance-identifier db-hep \
  --db-snapshot-identifier snap-hep

aws rds wait db-snapshot-available --db-snapshot-identifier snap-hep

aws rds describe-db-snapshots --db-snapshot-identifier snap-hep \
  --query 'DBSnapshots[0].{ID:DBSnapshotIdentifier,Estado:Status,Instancia:DBInstanceIdentifier}'
```

**Criterio 4:** `snap-hep` está `available` y pertenece a `db-hep`.

---

## 6. Paso 4 — Restaurar en una instancia nueva

La restauración **no** modifica la original: crea una instancia nueva a partir
del snapshot.

```bash
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier db-hep-restaurada \
  --db-snapshot-identifier snap-hep

aws rds wait db-instance-available --db-instance-identifier db-hep-restaurada

PUERTO2=$(aws rds describe-db-instances --db-instance-identifier db-hep-restaurada \
  --query 'DBInstances[0].Endpoint.Port' --output text)
echo "$PUERTO2"

PGPASSWORD='ClaveLab123' psql -h 127.0.0.1 -p "$PUERTO2" -U admin -d pedidos \
  -c 'SELECT count(*) FROM pedidos;'
```

Debe devolver al menos **2**. Si la tabla no existe o está vacía, el snapshot
no contenía los datos: revisa que hayas creado el snapshot **después** de los
`INSERT`.

**Criterio 5:** `db-hep-restaurada` está available y conserva los pedidos.

> En floci, la instancia restaurada puede mostrar `PubliclyAccessible: true`
> por defecto aunque la original fuera privada. Es una limitación del emulador;
> el criterio de la copia solo exige que esté disponible y conserve los datos.

---

## 7. Paso 5 — Autocontrol

```bash
revisar
```

Debe terminar en **5 de 5**. Si `datos` o `restaurada` fallan, revisa el puerto
y la tabla antes de recrear la instancia.

---

## 8. Criterios de evaluación

| # | Criterio | Qué se comprueba | Peso |
|---|---|---|---|
| 1 | `instancia_rds` | `db-hep` available, postgres, 20 GiB, privada | 1,0 |
| 2 | `respaldos` | retención ≥ 7 días | 1,0 |
| 3 | `datos` | `pedidos` con ≥ 2 filas vía `psql` | 1,0 |
| 4 | `snapshot` | `snap-hep` available y de `db-hep` | 1,0 |
| 5 | `restaurada` | `db-hep-restaurada` available con los pedidos | 1,0 |

---

## 9. Problemas frecuentes

| Síntoma | Causa | Solución |
|---|---|---|
| `psql: connection refused` | puerto equivocado o base aún arrancando | relee `Endpoint.Port` y espera |
| `database "pedidos" does not exist` | se creó sin `--db-name` | recrea con `--db-name pedidos` |
| `datos` en rojo | tabla vacía o en otra base | ejecuta los `INSERT` en `pedidos` |
| El snapshot no está available | se consultó demasiado pronto | `aws rds wait db-snapshot-available` |
| La restaurada no tiene filas | snapshot creado antes de insertar | repite el orden: datos → snapshot → restore |
| `respaldos` en rojo | retención 0 o 1 | usa `--backup-retention-period 7` |

No reinicies la nube ni la estación. Si `floci` no responde:
`curl -s http://127.0.0.1:4566/` y avisa al docente si persiste.

---

## 10. Para ir más allá (opcional)

- Crea un **read replica** y explica para qué sirve.
- Programa una ventana de mantenimiento y una de respaldo.
- Investiga **Point-in-Time Recovery** y en qué se diferencia de un snapshot.
- Diseña el grupo de seguridad que solo permitiría el puerto 5432 desde la capa
  web (repasa el Lab 2).

---

## 11. Entrega

El servidor evalúa la instancia, la retención, los datos, el snapshot y la
restauración. Antes de cerrar, ejecuta `revisar` y comprueba **5 de 5**.
