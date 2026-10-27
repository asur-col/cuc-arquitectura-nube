# CAMBIOS DE CONTENIDO — rama `arq-normalizacion` (U1+U2, 2026-10-26)

Para aprobación de Rodolfo. Todo el cambio está en **45 slides con ícono añadido** y los
**4 ajustes concretos** de abajo. No se quitó contenido de ninguna diapositiva, no cambió el
número de slides (S02/S03/S04 59, S08 55), no cambió la voz, y las duraciones se movieron 0,00 s
(los dos audios re-grabados cambiaron una palabra).

## 1. Muros de texto (tarea 3 del plan)

Criterio medido con el `innerText` del navegador: slide **sin** imagen real y con **>60 palabras
visibles**. Antes → después (mismo criterio): **S02 11→0 · S03 12→0 · S04 12→0 · S08 10→0**.
Cada slide recibió un ícono real de `assets/iconos/` en un hueco libre localizado por píxeles
(comprobado: 0 píxeles cambian fuera de la caja del ícono).

| Deck | Slide | Antes | Después |
|---|---|---|---|
| S02 | 6 | — | ícono `aws/general/users.png` (Usuarios y responsabilidades) insertado en hueco libre (70,295, caja 120×120 px) |
| S02 | 12 | — | ícono `aws/management/trusted-advisor-checklist.png` (Lista de chequeo de decisión) insertado en hueco libre (155,180, caja 150×150 px) |
| S02 | 13 | — | ícono `aws/cost/cost-explorer.png` (Explorador de costos) insertado en hueco libre (1145,180, caja 80×80 px) |
| S02 | 28 | — | ícono `aws/general/ssl-padlock.png` (Candado: dependencia del proveedor) insertado en hueco libre (1125,530, caja 100×100 px) |
| S02 | 48 | — | ícono `aws/security/identity-and-access-management-iam-permissions.png` (Permisos IAM) insertado en hueco libre (565,180, caja 120×120 px) |
| S02 | 49 | — | ícono `aws/security/identity-and-access-management-iam.png` (IAM: Effect y Action) insertado en hueco libre (1125,525, caja 100×100 px) |
| S02 | 50 | — | ícono `aws/management/service-catalog.png` (Catálogo de recursos (ARN)) insertado en hueco libre (1080,180, caja 150×150 px) |
| S02 | 52 | — | ícono `aws/general/generic-firewall.png` (Firewall: el Deny gana) insertado en hueco libre (1080,180, caja 150×150 px) |
| S02 | 53 | — | ícono `aws/management/management-console.png` (Práctica en la consola) insertado en hueco libre (825,185, caja 120×120 px) |
| S02 | 54 | — | ícono `aws/security/identity-and-access-management-iam-access-analyzer.png` (Analizador de accesos) insertado en hueco libre (1120,530, caja 100×100 px) |
| S02 | 57 | — | ícono `aws/security/identity-and-access-management-iam-role.png` (Rol de IAM) insertado en hueco libre (1010,50, caja 80×80 px) |
| S03 | 1 | — | ícono `aws/storage/storage.png` (Almacenamiento en la nube) insertado en hueco libre (1080,245, caja 150×150 px) |
| S03 | 8 | — | ícono `aws/storage/elastic-file-system-efs.png` (Archivos en red (NAS)) insertado en hueco libre (1130,530, caja 100×100 px) |
| S03 | 9 | — | ícono `aws/storage/multiple-volumes-resource.png` (Varios discos como uno (RAID)) insertado en hueco libre (510,445, caja 120×120 px) |
| S03 | 11 | — | ícono `aws/management/cloudwatch.png` (Métricas: IOPS, throughput, latencia) insertado en hueco libre (1100,195, caja 120×120 px) |
| S03 | 13 | — | ícono `aws/storage/simple-storage-service-s3.png` (Amazon S3) insertado en hueco libre (385,180, caja 120×120 px) |
| S03 | 33 | — | ícono `aws/management/personal-health-dashboard.png` (Panel de salud y durabilidad) insertado en hueco libre (1150,180, caja 80×80 px) |
| S03 | 37 | — | ícono `aws/storage/elastic-block-store-ebs-snapshot.png` (Copias entre zonas) insertado en hueco libre (945,180, caja 80×80 px) |
| S03 | 42 | — | ícono `aws/storage/s3-glacier.png` (Clases de almacenamiento) insertado en hueco libre (1070,180, caja 150×150 px) |
| S03 | 43 | — | ícono `aws/management/cloudwatch-event-time-based.png` (Reglas por tiempo (ciclo de vida)) insertado en hueco libre (580,345, caja 120×120 px) |
| S03 | 48 | — | ícono `aws/storage/simple-storage-service-s3-bucket.png` (Bucket de S3) insertado en hueco libre (1010,50, caja 80×80 px) |
| S03 | 50 | — | ícono `aws/storage/simple-storage-service-s3-bucket-with-objects.png` (Sitio estático en el bucket) insertado en hueco libre (665,185, caja 100×100 px) |
| S03 | 52 | — | ícono `aws/security/identity-and-access-management-iam-permissions.png` (Política del bucket) insertado en hueco libre (585,180, caja 120×120 px) |
| S04 | 1 | — | ícono `aws/network/vpc.png` (Redes en la nube) insertado en hueco libre (1080,180, caja 150×150 px) |
| S04 | 4 | — | ícono `aws/general/internet-alt1.png` (Direcciones de Internet) insertado en hueco libre (1125,415, caja 80×80 px) |
| S04 | 5 | — | ícono `aws/devtools/command-line-interface.png` (Cálculo de direcciones) insertado en hueco libre (1080,410, caja 120×120 px) |
| S04 | 6 | — | ícono `generic/network/subnet.png` (Subred) insertado en hueco libre (150,510, caja 80×80 px) |
| S04 | 7 | — | ícono `aws/network/public-subnet.png` (Subred pública) insertado en hueco libre (1080,180, caja 150×150 px) |
| S04 | 8 | — | ícono `aws/network/private-subnet.png` (Subred privada) insertado en hueco libre (1080,365, caja 120×120 px) |
| S04 | 9 | — | ícono `aws/general/generic-office-building.png` (Corporación Industrial del Caribe) insertado en hueco libre (485,180, caja 80×80 px) |
| S04 | 14 | — | ícono `aws/network/direct-connect.png` (Conexión dedicada) insertado en hueco libre (55,205, caja 150×150 px) |
| S04 | 19 | — | ícono `aws/network/route-table.png` (Tabla de rutas) insertado en hueco libre (1080,180, caja 150×150 px) |
| S04 | 20 | — | ícono `aws/network/vpc-router.png` (Enrutamiento) insertado en hueco libre (1080,180, caja 150×150 px) |
| S04 | 37 | — | ícono `aws/compute/ec2-elastic-ip-address.png` (IP elástica) insertado en hueco libre (1115,205, caja 100×100 px) |
| S04 | 40 | — | ícono `aws/network/site-to-site-vpn.png` (Interconexión de redes) insertado en hueco libre (1080,180, caja 150×150 px) |
| S08 | 18 | — | ícono `aws/database/rds.png` (Bases de datos administradas) insertado en hueco libre (1080,180, caja 150×150 px) |
| S08 | 19 | — | ícono `aws/database/aurora.png` (Conmutación Multi-AZ) insertado en hueco libre (1150,320, caja 80×80 px) |
| S08 | 21 | — | ícono `aws/database/rds-instance.png` (Instancia de base de datos) insertado en hueco libre (1085,180, caja 120×120 px) |
| S08 | 22 | — | ícono `aws/database/database-migration-service.png` (Replicación de datos) insertado en hueco libre (1080,420, caja 150×150 px) |
| S08 | 27 | — | ícono `aws/management/cloudwatch-alarm.png` (Tiempos: RTO y RPO) insertado en hueco libre (1020,195, caja 120×120 px) |
| S08 | 35 | — | ícono `aws/storage/backup.png` (Respaldo) insertado en hueco libre (810,480, caja 120×120 px) |
| S08 | 42 | — | ícono `aws/management/trusted-advisor-checklist.png` (Síntesis de la parte) insertado en hueco libre (295,350, caja 80×80 px) |
| S08 | 45 | — | ícono `aws/migration/datasync.png` (Mover los datos) insertado en hueco libre (1080,420, caja 150×150 px) |
| S08 | 48 | — | ícono `aws/management/systems-manager-maintenance-windows.png` (Ventana de mantenimiento) insertado en hueco libre (1150,320, caja 80×80 px) |
| S08 | 50 | — | ícono `aws/storage/cloudendure-disaster-recovery.png` (Recuperación: plan de reversa) insertado en hueco libre (295,510, caja 120×120 px) |

## 2. Defectos concretos y guion↔audio

| Deck | Slide | Antes | Después |
|---|---|---|---|
| S02 | 42 | etiqueta «3 · Ana inicia sesión» (y su subtexto «contraseña + MFA, una sola vez») centrada sobre la línea de vida del portal (x=440) | misma etiqueta movida al carril central (x=620), sin tapar ninguna línea de vida (x=440/800) |
| S03 | 15 | ícono de switch gris (`generic/network/switch.png`, trazos finos y poco legibles) | ícono `onprem/network/cisco-switch-l2.png` (más tinta y contraste), misma posición y tamaño |
| S04 | 2 | el audio decía «Cuatro partes» | audio re-grabado con el texto del deck («Tres partes»); voz es-CO-GonzaloNeural, rate +20 % (el de la parte), volume +0 % |
| S10 | 55 | el audio decía «la parte cuatro:» (p3, slide 16) | audio re-grabado con el texto del deck («la última parte:»); rate +15 %, volume +0 % |

## 3. Cobertura conceptual (tarea 5)

Auditoría del patrón REQ-045 sobre 30 conceptos clave (virtualización, hipervisor, IaaS/PaaS/SaaS,
región, zona de disponibilidad, bucket, CIDR, VPC, instancia, AMI, Multi-AZ, réplica de lectura,
snapshot, RTO/RPO, Auto Scaling, plantilla, pila, idempotencia, deriva…): **0 conceptos usados sin
lámina introductoria previa** (método: primera mención en texto visible + búsqueda de lámina con
criterio de definición en o antes de la semana de uso; `auditar_conceptos.py`). No hubo nada
crítico que corregir, así que este punto no genera cambios.

## 4. Verificación

- Píxeles: 45/45 íconos con **0 cambios fuera de su caja**; S02-42 y S03-15 con cambios confinados
  a las zonas esperadas (`verificar_dif_iconos.py`, `verificar_defectos.py`).
- Playwright: 4 decks con **0 imágenes rotas** (`chequear_decks_icons.js`).
- Videos re-codificados de las partes afectadas con el mismo audio (Δ 0,00 s) y el audio nuevo en
  S04 p1 (slide 2) y S10 p3 (slide 16); logo NCC 0,99 y pie «n / 59»·«n / 55» en 2 fotogramas por
  video (`verificar_regenerados.py`).
