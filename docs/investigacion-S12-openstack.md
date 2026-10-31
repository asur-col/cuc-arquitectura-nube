# Documento de Investigación S12: OpenStack y Arquitectura de Nube Privada

**Asignatura**: Arquitectura en la Nube  
**Semana**: 12 (Periodo 2026-2) · Unidad 3  
**Docente**: Ing. Rodolfo José Cañas Cervantes  
**Fecha de elaboración**: Octubre 2026  

---

## 1. Fundamentos y Misión de OpenStack
OpenStack es la plataforma de código abierto de referencia global para la construcción y operación de nubes de infraestructura como servicio (IaaS) tanto privadas como públicas y de telecomunicaciones (NFV). Fundado originalmente en 2010 por Rackspace Hosting y la NASA, el proyecto es gobernado en la actualidad por la **OpenInfra Foundation** (anteriormente OpenStack Foundation).

Su objetivo arquitectónico fundamental es abstraer y desacoplar los recursos físicos de un centro de datos (cómputo x86/ARM/GPU, redes L2/L3 e infraestructura de almacenamiento en bloque, objetos y ficheros) agrupándolos en *pools* lógicos compartidos que pueden ser aprovisionados dinámicamente mediante autoservicio por medio de APIs REST abiertas, SDKs, interfaz de línea de órdenes (OpenStack CLI) y una interfaz gráfica unificada basada en web (Horizon).

### Principios de Diseño
1. **Composición de Microservicios sin Estado**: Los procesos de control de OpenStack (por ejemplo `nova-api`, `neutron-server`, `cinder-api`, `glance-api`) no guardan estado en memoria local entre peticiones. Todo el estado persistente y los metadatos residen en una base de datos relacional transaccional compartida (típicamente MariaDB con replicación sincrónica Galera).
2. **Mensajería Asíncrona Distribuida (AMQP)**: La coordinación entre los componentes que atienden peticiones API y los agentes o demonios de bajo nivel que operan en los hipervisores y nodos de red se efectúa a través de colas de mensajes altamente confiables (RabbitMQ), garantizando tolerancia a latencias y desacoplamiento temporal.
3. **Control Plano / Datos Desacoplados**: El plano de control orquesta las operaciones sin interponerse en la ruta del tráfico de datos de las instancias de computación ni en el tráfico I/O de los volúmenes de almacenamiento.
4. **Extensibilidad basada en Drivers y Plugins**: Cada servicio expone una abstracción genérica que delega la ejecución en implementaciones concretas de hardware o software mediante plugins (e.g. hipervisores KVM/QEMU, Ironic para bare-metal, switches ML2 con OVS/OVN, backends de almacenamiento Ceph RBD, NetApp, PureStorage, etc.).

---

## 2. Cronología de Lanzamientos y Estado Tecnológico (2024–2026)
OpenStack mantiene un ciclo semestral predecible de versiones, identificado con nombres en orden alfabético:

- **2024.1 Caracal (abril 2024)**: Consolidación de soporte LTS; mejoras críticas en microversiones de Nova, estabilidad en Neutron con backend OVN por defecto, y fortalecimiento de Ironic para cargas bare-metal con aceleradores de inteligencia artificial.
- **2024.2 Dalmatian (octubre 2024)**: Optimización exhaustiva para cargas de IA/ML, soporte mejorado de particionado dinámico de GPUs (vGPU, NVIDIA MIG), integración nativa de Neutron OVN con enrutamiento BGP dinámico, mejoras en Skyline (nueva UI alternativa a Horizon).
- **2025.1 Epoxy (abril 2025)**: Maduración de la integración con Kubernetes (Magnum y Kuryr), refuerzo de políticas de seguridad criptográfica en Keystone y Barbican, soporte refinado para kernels modernos de Linux 6.x y contenedores Zun.
- **2025.2 F... (octubre 2025)** y **2026.1 G... (abril 2026)**: Enfoque continuo en soberanía del dato, despliegues *green-cloud* para eficiencia energética (telemetría con Prometheus y Ceilometer), y automatización de ciclo de vida con Kolla-Ansible y OpenStack-Ansible.

---

## 3. Catálogo de Servicios Principales y Mapeo de Arquitectura

| Servicio OpenStack | Nombre en Clave | Función Principal | Equivalente Conceptual en AWS | Icono Local en `assets/iconos/openstack/` |
|---|---|---|---|---|
| **Identidad y Catálogo** | **Keystone** | Autenticación, autorización RBAC, emisión de tokens Fernet, catálogo de endpoints de servicios | AWS IAM / AWS STS | `sharedservices/keystone.png` |
| **Cómputo** | **Nova** | Orquestación del ciclo de vida de VMs, scheduling, gestión de hipervisores KVM | Amazon EC2 | `compute/nova.png` |
| **Redes y Conectividad** | **Neutron** | Puertos virtuales, subredes, routers L3, Floating IPs, Security Groups, OVN/OVS | Amazon VPC | `networking/neutron.png` |
| **Imágenes de SO** | **Glance** | Registro, almacenamiento y entrega de plantillas de disco e imágenes de SO (QCOW2, RAW) | Amazon EC2 AMI | `sharedservices/glance.png` |
| **Almacenamiento en Bloque**| **Cinder** | Provisión y acoplamiento de volúmenes persistentes a VMs (Ceph RBD, LVM, iSCSI) | Amazon EBS | `storage/cinder.png` |
| **Almacenamiento de Objetos**| **Swift** | Repositorio distribuido de objetos con redundancia por software y API HTTP REST | Amazon S3 | `storage/swift.png` |
| **Portal Gráfico Web** | **Horizon** | Tablero de autoservicio para usuarios y consola de administración operativa | AWS Management Console | `frontend/horizon.png` |
| **Orquestación Declarativa**| **Heat** | Motor de plantillas declarativas HOT (Heat Orchestration Template) para infraestructura | AWS CloudFormation | `orchestration/heat.png` |
| **Contenedores como Servicio**| **Zun** | Gestión y ejecución de contenedores rápidos sin necesidad de gestionar VMs completas | AWS Fargate / ECS | `compute/zun.png` |
| **Balanceo de Carga** | **Octavia** | Provisión de equilibradores de carga de alta disponibilidad (Amphora VMs) | AWS Application Load Balancer | `networking/octavia.png` |
| **DNS Administrado** | **Designate** | Gestión multitenant de zonas DNS y resolución interna/externa de nombres | Amazon Route 53 | `networking/designate.png` |
| **Bare Metal** | **Ironic** | Aprovisionamiento físico de servidores sin capa de virtualización (ideal IA/HPC) | Amazon EC2 Bare Metal | `baremetal/ironic.png` |

---

## 4. Flujo Detallado de Aprovisionamiento de una Instancia (Boot VM Workflow)
Cuando un usuario o un pipeline de CI/CD solicita la creación de una máquina virtual (por ejemplo: `openstack server create --flavor m1.small --image ubuntu-24.04 --network private-net srv-web-01`), interactúan los siguientes componentes en secuencia coordinada:

1. **Autenticación (Horizon/CLI -> Keystone)**: El cliente envía sus credenciales al endpoint de Keystone. Keystone valida la identidad en la base de datos de usuarios o directorio LDAP/Active Directory y emite un token de seguridad con firma criptográfica (Fernet Token) junto al catálogo de servicios y endpoints autorizados.
2. **Recepción de la Petición (CLI -> Nova-API)**: El cliente invoca la API de Nova (`POST /v2.1/servers`) acompañando el token. `nova-api` contacta a Keystone para verificar la autenticidad y vigencia del token y los permisos RBAC sobre el proyecto (tenant).
3. **Persistencia Inicial y Conductor (`nova-api` -> MariaDB & RabbitMQ -> `nova-conductor`)**: `nova-api` escribe la entrada inicial de la instancia en la base de datos (estado `BUILDING`) y publica un mensaje en el bus de RabbitMQ hacia `nova-conductor`.
4. **Planificación y Selección de Nodo (`nova-conductor` -> `nova-scheduler`)**: `nova-conductor` solicita al `nova-scheduler` determinar el nodo de cómputo físico óptimo. El scheduler ejecuta un proceso de dos fases:
   - *Filtering*: Descarta hipervisores que no cumplan requisitos de RAM, vCPUs, almacenamiento, arquitectura de CPU o afinidad/anti-afinidad.
   - *Weighting*: Califica los candidatos restantes mediante funciones de peso para balancear la carga o consolidar servidores.
5. **Delegación al Hipervisor (`nova-scheduler` -> `nova-compute`)**: La decisión se publica en la cola específica del agente `nova-compute` residente en el nodo físico seleccionado.
6. **Reserva y Configuración de Red (`nova-compute` -> Neutron)**: `nova-compute` invoca la API de Neutron para asignar una dirección IP privada fija, crear el puerto virtual L2, asociar Security Groups y preparar el mapeo de interfaz virtual (VIF) en Open vSwitch o OVN.
7. **Obtención de la Imagen de Disco (`nova-compute` -> Glance)**: `nova-compute` solicita la imagen base a Glance. Si la imagen ya se encuentra en la caché local del nodo (`/var/lib/nova/instances/_base`), se reutiliza; de lo contrario, se descarga por streaming desde el backend de Glance (Ceph o Swift) y se crea un disco diferencial o clon instantáneo de copia en escritura (CoW).
8. **Enlace de Almacenamiento Persistente si aplica (`nova-compute` -> Cinder)**: Si la instancia incluye volúmenes Cinder, `cinder-api` y `cinder-volume` configuran el mapeo del dispositivo de bloque (vía iSCSI, Fibre Channel o Ceph RBD) y `nova-compute` lo conecta al hipervisor.
9. **Invocación del Hipervisor (`nova-compute` -> Libvirt/QEMU-KVM)**: `nova-compute` genera el archivo XML de definición de la máquina virtual con las asignaciones de vCPUs, memoria RAM, interfaces de red e inyección de metadatos/cloud-init (`user-data` y llaves SSH públicas) e instruye a `libvirt` para arrancar el dominio KVM.
10. **Actualización de Estado (`nova-compute` -> `nova-conductor` -> MariaDB)**: El hipervisor confirma el encendido exitoso, `nova-compute` actualiza el estado a `ACTIVE` mediante mensajería y la máquina queda lista y accesible para el usuario.

---

## 5. Modelos de Redes con Neutron y Open vSwitch / OVN
Neutron desacopla la topología lógica de red definida por el usuario de la infraestructura física subyacente:
- **Redes de Proveedor (Provider Networks)**: Conectadas directamente a la red física del centro de datos mediante interfaces en modo *Flat* (sin etiquetado) o *VLAN* (802.1Q). Suelen emplearse para acceso administrativo o servidores que requieren baja latencia sin sobrecarga de encapsulación.
- **Redes de Autoservicio (Self-service / Tenant Networks)**: Redes virtuales creadas por cada proyecto, completamente aisladas de los demás tenants. Utilizan túneles de superposición (Overlay Networks) con protocolos como **VXLAN** (Virtual Extensible LAN) o **Geneve** (estándar en OVN), permitiendo hasta 16 millones de identificadores de red sin riesgo de colisión de direcciones IP privadas (soporte de direcciones solapadas RFC 1918).
- **Enrutamiento L3 y Floating IPs**: Un router virtual de Neutron interconecta las subredes privadas con una red externa (Gateway). Realiza traducción de direcciones por puerto (SNAT / Masquerade) para permitir que las VMs salgan a Internet, y mapea direcciones públicas flotantes (Floating IPs mediante DNAT 1:1) para exponer servicios hacia el exterior.
- **Transición OVS a OVN**: Históricamente Neutron dependía de múltiples agentes de Python (`neutron-openvswitch-agent`, `neutron-dhcp-agent`, `neutron-l3-agent`). En las versiones modernas (Caracal, Dalmatian, Epoxy), el backend estándar es **OVN (Open Virtual Network)**, el cual centraliza el control lógico mediante bases de datos OpenFlow de alto rendimiento (`ovn-northd`), eliminando agentes pesados y reduciendo significativamente la latencia de conmutación.

---

## 6. Distribuciones y Métodos de Despliegue de OpenStack
El despliegue de OpenStack en producción requiere herramientas de automatización debido a su arquitectura distribuida:

1. **DevStack**: Guión Bash oficial de desarrollo y pruebas para entornos de laboratorio de un único nodo. Instala todos los servicios en código fuente desde Git sobre Ubuntu o CentOS. Es ideal para estudiantes, investigación y validación de APIs, pero no cuenta con alta disponibilidad ni persistencia adecuada para producción.
2. **MicroStack (Canonical / Ubuntu)**: Distribución empaquetada en contenedores Snap de Ubuntu que instala un OpenStack funcional y preconfigurado con una sola orden de terminal (`snap install microstack --classic`), reduciendo la barrera de entrada para pruebas locales.
3. **Kolla-Ansible**: Proyecto oficial que ejecuta cada servicio de OpenStack dentro de contenedores Docker o Podman y utiliza playbooks de Ansible para la orquestación, actualización sin paradas de servicio (*rolling upgrades*) y monitoreo. Es uno de los estándares más adoptados en centros de datos empresariales.
4. **OpenStack-Ansible (OSA)**: Despliega los servicios dentro de contenedores de sistema Linux Containers (LXC) sobre las máquinas físicas, permitiendo un rendimiento casi nativo y un aislamiento limpio de dependencias de sistema.
5. **OpenStack on OpenShift / Kubernetes (TripleO / Cloud-native)**: Orquestadores basados en operadores de Kubernetes que gestionan el plano de control de OpenStack como aplicaciones nativas de Kubernetes.

---

## 7. Casos Reales Verificables y Soberanía del Dato
- **CERN (Organización Europea para la Investigación Nuclear)**: Opera una de las nubes OpenStack privadas más grandes del planeta con más de 300.000 núcleos de CPU y miles de nodos de cómputo para procesar los terabytes por segundo generados por los detectores del Gran Colisionador de Hadrónes (LHC).
- **Operadores de Telecomunicaciones (AT&T, Verizon, Telefónica)**: Despliegan OpenStack como plataforma base para la virtualización de funciones de red (NFV) en redes 5G, enrutadores de borde y estaciones base descentralizadas.
- **Caso Nacional / Empresarial Colombiano — Corporación Industrial del Caribe (CIC, Barranquilla)**: Empresa del sector logístico y portuario en la costa norte de Colombia que requiere operar sistemas SCADA de control portuario, trazabilidad de contenedores y facturación electrónica. Por motivos de latencia de red hacia regiones públicas de nube (Miami/Virginia), costos en dólares por tráfico de salida de datos (egress) y normativas estrictas de soberanía y auditoría de datos (Ley 1581 de 2012 y regulación aduanera DIAN), implementa una nube privada OpenStack sobre hardware propio en su centro de datos local, manteniendo una arquitectura híbrida conectada a AWS para copias de seguridad de largo plazo y analítica de datos.

---

## 8. Referencias y Fuentes Oficiales Consultadas
- OpenStack Documentation: https://docs.openstack.org/
- OpenInfra Foundation Releases & Roadmaps: https://releases.openstack.org/ (Caracal, Dalmatian, Epoxy)
- OpenStack Architecture Design Guide: https://docs.openstack.org/arch-design/
- Material de Cátedra: Diapositivas de la asignatura `/home/cuc/11 OpenStack.pptx` (Ing. Rodolfo Cañas).
- Guía de Redes OVN y Neutron: https://docs.openstack.org/neutron/latest/admin/ovn/index.html
