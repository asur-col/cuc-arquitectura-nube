# Respaldo de Cifras Técnicas: Semana 13 · OpenStack II

Este documento audita y respalda cada número y cifra técnica visible en las diapositivas y guiones de la Semana 13.
Las cifras corresponden a especificaciones protocolarias, parámetros oficiales de configuración de OpenStack o dimensiones técnicas de dimensionamiento (rotuladas como caso ilustrativo de arquitectura sin cifras financieras ficticias).

---

## 1. Protocolos, Criptografía y Códigos de Respuesta HTTP
- **128 bits (AES-CBC) y HMAC en Tokens Fernet** (Diapositiva 3):
  - *Fuente*: OpenStack Keystone Fernet Tokens Documentation
  - *URL*: https://docs.openstack.org/keystone/latest/admin/identity-tokens.html
  - *Comprobación*: Keystone utiliza Fernet (cifrado simétrico AES-128 en modo CBC con autenticación HMAC SHA-256).
- **HTTP 202 Accepted** (Diapositivas 4, 11):
  - *Fuente*: OpenStack Nova API Reference (Servers Create)
  - *URL*: https://docs.openstack.org/api-ref/compute/
  - *Comprobación*: La respuesta estándar de `POST /servers` es `202 Accepted` con cabeceras de ubicación de la tarea.
- **HTTP 403 Forbidden por cuotas** (Diapositiva 56):
  - *Fuente*: OpenStack Keystone & Nova Quotas Documentation
  - *URL*: https://docs.openstack.org/nova/latest/user/quotas.html
  - *Comprobación*: Cuando una petición supera la cuota del proyecto, la API responde con error `403 Forbidden`.

---

## 2. Parámetros de Configuración y Alta Disponibilidad
- **3 reintentos (`max_attempts = 3`)** (Diapositiva 10):
  - *Fuente*: OpenStack Nova Configuration Guide (`scheduler.max_attempts`)
  - *URL*: https://docs.openstack.org/nova/latest/admin/configuration/schedulers.html
  - *Comprobación*: El valor por defecto de reintentos del planificador ante fallo de un hipervisor es 3.
- **Quórum de 3 Nodos en Galera, RabbitMQ y OVN** (Diapositivas 37, 38, 39, 40, 48, 58):
  - *Fuente*: OpenStack High Availability Guide (Control Plane HA)
  - *URL*: https://docs.openstack.org/ha-guide/
  - *Comprobación*: Se requiere un mínimo de 3 nodos para tolerar la caída de 1 nodo manteniendo la mayoría matemática (\( \lfloor 3/2 \rfloor + 1 = 2 \)).
- **MTU Jumbo 9000 bytes** (Diapositiva 49):
  - *Fuente*: OpenStack Neutron MTU Configuration Guide
  - *URL*: https://docs.openstack.org/neutron/latest/admin/config-mtu.html
  - *Comprobación*: Se recomienda configurar MTU 9000 (Jumbo Frames) en la red física subyacente para encapsulamiento Geneve/VXLAN (overhead de 50-60 bytes).
- **Ratios de Asignación: vCPU 4:1 o 3:1, RAM 1:1 estricto** (Diapositiva 55):
  - *Fuente*: OpenStack Nova Configuration Guide (`cpu_allocation_ratio`, `ram_allocation_ratio`)
  - *URL*: https://docs.openstack.org/nova/latest/admin/configuration/schedulers.html
  - *Comprobación*: Parámetros canónicos de Nova: `cpu_allocation_ratio` (por defecto 4.0 o 3.0 en despliegues estables) y `ram_allocation_ratio = 1.0` recomendado para producción para evitar invocación de OOM Killer.
- **Réplica Ceph 3x** (Diapositivas 33, 44, 58):
  - *Fuente*: Ceph Storage Architecture Documentation (Data Protection Pools)
  - *URL*: https://docs.ceph.com/en/latest/rados/operations/pools/
  - *Comprobación*: La directiva `size = 3, min_size = 2` es la configuración estándar de réplica triple para almacenamiento por bloques en Ceph.

---

## 3. Casos Ilustrativos de Dimensionamiento y Gobernanza (Sin Costos Ficticios)
- **Caso ilustrativo de dimensionamiento: 4 hipervisores, 256 núcleos, 2 TB RAM, 50 VMs** (Diapositiva 13):
  - *Estado*: Rotulado formalmente como *"Caso ilustrativo de dimensionamiento técnico, no es una empresa real"*.
  - *Objetivo*: Ejercicio pedagógico de consolidación de servidores virtuales bajo overcommit 3:1 y balanceo NUMA.
- **Topología de referencia de producción** (Diapositiva 58):
  - *Estado*: Rotulado formalmente como *"Caso ilustrativo de arquitectura, no es una empresa real"*.
  - *Objetivo*: Diagrama arquitectónico de 3 nodos controladores, N nodos de cómputo y clúster Ceph sobre interfaces agregadas 25 Gbps.
- **Cuotas de Keystone: Finanzas y Analítica** (Diapositiva 56):
  - *Estado*: Ejemplo pedagógico de aislamiento multitenant con cuotas representativas (vCPUs, RAM, redes, Floating IPs).
