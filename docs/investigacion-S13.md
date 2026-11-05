# Investigación Técnica: Semana 13 · OpenStack II: Arquitectura Interna, Redes de Producción y Alta Disponibilidad

Este documento recopila las fuentes técnicas primarias y documentación oficial utilizadas para el diseño de los contenidos teóricos de la Semana 13 de Arquitectura en la Nube (2026-2).

---

## 1. Ciclo de Vida del Aprovisionamiento y Orquestación Nova / Placement
- **Fuente**: OpenStack Nova Architecture Documentation
  - **URL**: https://docs.openstack.org/nova/latest/user/architecture.html
  - **Cita**: El flujo de creación de instancias coordina `nova-api`, `nova-conductor`, `placement-api`, `glance-api`, `neutron-server` y `cinder-api` a través de colas de mensajes RPC en RabbitMQ y persistencia de estado en MariaDB.
- **Fuente**: OpenStack Placement API Documentation
  - **URL**: https://docs.openstack.org/placement/latest/
  - **Cita**: Placement rastrea el inventario de Resource Providers (CPU, RAM, DISK) y rasgos (traits) para resolver consultas complejas de hipervisores disponibles sin sobrecargar las bases de datos de Nova.

---

## 2. Redes Avanzadas en Producción: Provider Networks y OVN
- **Fuente**: OpenStack Neutron OVN Architecture Guide
  - **URL**: https://docs.openstack.org/neutron/latest/admin/ovn/index.html
  - **Cita**: Open Virtual Network (OVN) reemplaza los tradicionales agentes Python L2/L3 de OVS por bases de datos distribuidas (OVN Northbound y Southbound) y demonios `ovn-controller` en cada hipervisor, permitiendo enrutamiento distribuido (DVR) y eliminación de cuellos de botella en nodos de red centrales.
- **Fuente**: OpenStack Neutron Networking Concepts
  - **URL**: https://docs.openstack.org/neutron/latest/admin/intro-basic-networking.html
  - **Cita**: Comparativa técnica entre redes de proveedor (conectadas directamente a interfaces físicas L2 / VLAN sin traducción de direcciones) y redes de autoservicio o proyecto (basadas en overlays VXLAN/Geneve con aislamiento L3).

---

## 3. Almacenamiento Unificado Ceph y Persistencia Cinder/Glance
- **Fuente**: Ceph Block Device & OpenStack Integration Guide
  - **URL**: https://docs.ceph.com/en/latest/rbd/rbd-openstack/
  - **Cita**: La integración de Ceph RADOS Block Device (RBD) permite a Cinder, Glance y Nova compartir un mismo cluster distribuido. Nova y Glance pueden clonar imágenes a volúmenes mediante Copy-on-Write (CoW) en milisegundos sin tráfico de red entre nodos de cómputo.
- **Fuente**: OpenStack Cinder Storage Drivers
  - **URL**: https://docs.openstack.org/cinder/latest/reference/support-matrix.html
  - **Cita**: Arquitectura de Cinder Volume, Cinder Scheduler y Cinder Backup para el desacoplamiento de bloques elásticos.

---

## 4. Alta Disponibilidad (HA) del Plano de Control
- **Fuente**: OpenStack High Availability Guide
  - **URL**: https://docs.openstack.org/ha-guide/
  - **Cita**: Estrategias de resiliencia mediante clúster MariaDB Galera (replicación síncrona multi-master certificada por quórum), RabbitMQ con colas Quorum/Mirrored, y balanceo de carga mediante HAProxy y Keepalived para proporcionar una VIP unificada de acceso a las APIs.
- **Fuente**: Pacemaker & Corosync Cluster Engine
  - **URL**: https://clusterlabs.org/pacemaker/doc/
  - **Cita**: Gestión de servicios con estado (stateful), fencing mediante STONITH y migración automática de recursos en caso de fallo de hardware en nodos controladores.

---

## 5. Herramientas de Despliegue en Producción y TCO
- **Fuente**: Kolla-Ansible Production Deployment Guide
  - **URL**: https://docs.openstack.org/kolla-ansible/latest/
  - **Cita**: Kolla encapsula cada servicio de OpenStack en contenedores Docker y utiliza Ansible para orquestar despliegues, parches y actualizaciones canary sin tiempo de inactividad, a diferencia de DevStack que es exclusivamente un entorno de desarrollo volátil en un solo nodo.
- **Fuente**: OpenInfra Foundation User Survey & Case Studies
  - **URL**: https://www.openstack.org/user-stories/
  - **Cita**: Análisis de retorno de inversión (ROI) y costo total de propiedad (TCO): las nubes privadas son óptimas financieramente cuando se operan cargas de cómputo y almacenamiento intensivo 24/7 con tasas de utilización sostenida mayores al 70%, evitando los elevados cargos de transferencia de datos de salida (egress) de las nubes públicas.
