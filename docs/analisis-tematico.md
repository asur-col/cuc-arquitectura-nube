# Análisis temático — Arquitectura en la Nube (2026-2)

> Validación del contenido de la asignatura contra referentes externos.
> Fecha: 4 oct 2026. Fuente de verdad de títulos y fechas: el **calendario de `index.html`**
> (no existe en el repo otro plan académico / microcurrículo).

## 1. Referentes usados

| Referente | Por qué sirve |
|---|---|
| **AWS Academy Cloud Architecting (ACA v3)** — 17 módulos, labs de desafío "Café" | Los labs evaluados del curso (10% c/u) son exactamente los challenge labs de ACA. El calendario sigue casi 1:1 sus módulos. |
| **AWS Certified Solutions Architect – Associate (SAA-C03)** | Certificación a la que ACA prepara. Dominios: Seguridad 30% · Resiliencia 26% · Alto rendimiento 24% · **Costo 20%**. |
| **NIST SP 800-145** | Definición estándar de nube (5 características, 3 modelos de servicio, 4 de despliegue). |
| **ACM/IEEE CS2023** | Pide virtualización (hipervisores, contenedores) y sistemas distribuidos como base conceptual. |

## 2. Mapa calendario ↔ referentes

| Sem | Tema (calendario) | Módulo ACA | Lab ACA (evaluado) | Dominio SAA-C03 | Estado material |
|---|---|---|---|---|---|
| 1 | Fundamentos, modelos de servicio, buenas prácticas, proveedores | M2 Introducing Cloud Architecting | — | todos | 13 diap., 5 con gráfico, video ~11 min |
| 2 | Modelos de despliegue + identidad y acceso | M3 Securing Access | — | Seguridad | 11 diap., **2** con gráfico |
| 3 | Almacenamiento: objetos, bloques, archivos | M4 Storage Layer (S3) | Sitio web estático | Rendimiento/Costo | 16 diap., 11 con gráfico |
| 4 | Redes: redes virtuales, subredes, grupos de seguridad | M7 Networking + M8 Connecting Networks | Red VPC | Seguridad/Resiliencia | 22 diap., 13 con gráfico (el mejor de U1) |
| 5 | Seguridad y cumplimiento | M9 (parte datos) + Well-Architected Security | — | Seguridad | 11 diap., 4 con gráfico |
| 6 | Repaso U1 — Parcial 1 | — | — | — | sin presentación (correcto) |
| 7 | Cómputo: instancias, tipos, escalado | M5 Compute Layer (EC2) | Sitio web dinámico | Rendimiento/Costo | ✅ estándar: 56 diap., 4 partes |
| 8 | BD administradas y backup | M6 Database Layer | Migración a RDS | Resiliencia | ✅ estándar: 56 diap., 4 partes |
| 9 | Identidad avanzada: roles, políticas, mínimo privilegio | M9 Securing User, Application & Data Access | — | Seguridad | ❌ **falta (semana en curso)** |
| 10 | Elasticidad, alta disponibilidad, monitorización | M10 Monitoring, Elasticity & HA | Entorno escalable/HA | Resiliencia | ❌ falta (inicia 12 oct) |
| 11 | IaC — repaso U2 | M11 Automating Your Architecture | Automatización (IaC) | Resiliencia | ❌ falta |
| 12 | Caché y distribución de contenido | M12 Caching Content | — | Rendimiento | ❌ falta |
| 13 | Arquitecturas desacopladas | M13 Building Decoupled Architectures | — | Resiliencia | ❌ falta |
| 14 | Serverless y microservicios | M14 Serverless & Microservices | Arquitectura serverless | Resiliencia/Costo | ❌ falta |
| 15 | Patrones de ingeniería de datos | M15 Data Engineering Patterns | — | Rendimiento | ❌ falta |
| 16–17 | DR + repaso general | M16 Planning for Disaster | — | Resiliencia | ❌ falta |

**Veredicto general:** la secuencia temática es **sólida y está bien alineada** con un estándar
reconocido (ACA ↔ SAA-C03): progresión por capas (identidad → storage → red → cómputo → datos),
luego resiliencia/automatización (U2) y patrones modernos (U3). No hace falta cambiar títulos.
Los problemas están en **la profundidad y la forma del material**, no en el temario.

## 3. Hallazgos de calidad

### 3.1 Duración y densidad (crítico)
- S01–S05 tienen 11–22 diapositivas → cubren 10–20 min, no 1 hora. Videos de ~11 min.
- S07/S08 (56 diap. en 4 partes, ~52 gráficos) son el estándar a replicar.

### 3.2 Gráficos (crítico)
- S02 (2 de 11) y S05 (4 de 11) son casi solo texto. S01 tiene 5 de 13.
- Faltan diagramas de topología (lo que mejor funciona en esta materia): flujos de autenticación,
  evaluación de políticas, topologías híbridas/VPN, defensa en profundidad sobre una VPC real, etc.

### 3.3 Brechas de contenido por semana (dentro del mismo título)
| Sem | Falta / debe reforzarse |
|---|---|
| 1 | **Well-Architected Framework** (el calendario dice "marco de buenas prácticas" y no hay diapositiva). Definición NIST (5 características). **Virtualización** (hipervisor tipo 1/2, vSwitch, almacenamiento definido por software) — base de todo el curso, hoy es 1 diapositiva. Infraestructura global (regiones/AZ/edge) con diagrama. La diapositiva "Temario semanal" **está desfasada** (muestra el orden previo al corrimiento de semanas). |
| 2 | Nube privada en concreto (OpenStack: Nova/Neutron/Cinder/Keystone). Usuario raíz y MFA, usuarios/grupos/roles con diagrama, lógica de evaluación de políticas (deny explícito > allow > deny implícito), multi-cuenta. |
| 3 | Durabilidad vs. disponibilidad (réplicas entre AZ/regiones), versionado, replicación, cifrado, **hosting de sitio estático** (es el lab). |
| 4 | Ya bueno. Reforzar M8: Transit Gateway (hub-and-spoke), endpoints privados (gateway/interface), DNS privado. |
| 5 | Gestión de claves (KMS, envelope encryption), secretos, WAF/DDoS, detección (GuardDuty-tipo), Ley 1581 con más casos. |
| 9 | Debe ir **más allá de S02/S05** para no repetir: roles y *assume role*, federación/SSO, Cognito (identidad de usuarios de apps), *permission boundaries*, organizaciones multi-cuenta y SCP, **gobernanza y costos** (etiquetado, presupuestos, calculadora/TCO). |
| 10 | Balanceadores (ALB/NLB), Auto Scaling, métricas/alarmas/logs, Route 53 health checks, diseño multi-AZ. |
| 11 | IaC declarativa (CloudFormation/Terraform), drift, + **CI/CD** como cierre de automatización. |
| 12 | Capas de caché (cliente, CDN, app, BD), CloudFront, ElastiCache, **DNS/Route 53** (políticas de enrutamiento). |
| 13 | Colas (SQS), pub/sub (SNS), eventos (EventBridge), patrones fan-out, idempotencia. |
| 14 | Lambda, API Gateway, Step Functions **y contenedores** (Docker, ECS/Fargate, EKS) — ACA M14 los incluye; es la única semana donde caben. |
| 15 | 5 V de los datos, ingesta batch vs. streaming (Kinesis), data lake en S3, Glue/Athena. |
| 16–17 | RPO/RTO, 4 estrategias de DR (backup-restore, pilot light, warm standby, multi-site), + repaso general. |

### 3.4 Transversal
- **Costo es el 20% de SAA-C03** y no tiene semana propia → incluir en cada semana una diapositiva
  "¿Cuánto cuesta?" y concentrar FinOps en S09.
- **Enfoque multi-nube** (decisión del docente): el concepto es genérico de industria y se puede
  ilustrar con arquitecturas de **cualquier proveedor** (AWS, Azure, GCP, OpenStack) — por eso las
  presentaciones antiguas de Azure son fuente válida. AWS es la plataforma de práctica (labs AWS Academy),
  así que cada concepto aterriza en su implementación AWS. Evitar tablas largas de equivalencias de
  nombres por proveedor; preferir un diagrama de un proveedor concreto que explique el concepto.
- Mantener el caso transversal **Corporación Industrial del Caribe** y ejemplos colombianos.

## 4. Estándar de producción (para cada semana)
- 1 hora = **4 partes de ~15 min**, cada parte abre con diapositiva divisoria "Parte X de 4".
- ~14 diapositivas de contenido por parte (≈ 56 + portada + 4 divisorias).
- ≥ 1 gráfico/diagrama (SVG propio, estilo CUC vino/dorado) en casi todas las diapositivas de contenido.
- Guion narrado por diapositiva (para video sintético) y marcas de corte.
- Plantilla de referencia: `2026-2-S07-arquitectura-nube-computo.html`.

Fuentes de imágenes, íconos y notas: ver [`fuentes-recursos.md`](fuentes-recursos.md).
