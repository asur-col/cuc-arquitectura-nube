# Fuentes de recursos: piloto visual Unidad 3 (Arquitectura en la Nube)

Recursos nuevos o usados en las diapositivas rediseñadas (rama `arq-piloto-u3`). Licencias verificadas en la API de Wikimedia Commons (`extmetadata`) el 2026-11-05.

## Fotos (assets/fotos/)

| Archivo local | Diapositiva | Autor | Licencia | Página del archivo | Modificación |
|---|---|---|---|---|---|
| `nvidia-h100-nvlink-geekerwan-002.png` | S15 diap. 5 | Geekerwan (极客湾) | CC BY 3.0 (https://creativecommons.org/licenses/by/3.0) | https://commons.wikimedia.org/wiki/File:NVIDIA_H100_(%E6%9E%81%E5%AE%A2%E6%B9%BEGeekerwan)_002.png | Ninguna en el archivo. En la diapositiva: recorte `slice` (≈20 % del ancho) y pie «4 tarjetas H100 apiladas». La descripción de Commons dice «Here you can see 4 stacked cards» y no menciona conectores NVLink, por eso se retiró ese rótulo (verificado 2026-11-05) |
| `coolit-rack-refrigeracion-liquida.jpg` | S15 diap. 10 | Barbara Massolin (CoolIT) | CC BY-SA 3.0 (https://creativecommons.org/licenses/by-sa/3.0) | https://commons.wikimedia.org/wiki/File:%C2%A9_CoolIT_Rack_DCLC_AHx_Liquid_Cooling_Solution.jpg | Ninguna (600×394 original) |

## Íconos (assets/iconos/, ya existentes en el repositorio)

Se usan sin modificar. Origen declarado en el commit `ea9e664` (2026-10-04): librería multi-nube de `mingrammer/diagrams` (https://github.com/mingrammer/diagrams). Verificado el 2026-11-05:

- **Código de la librería**: MIT, https://github.com/mingrammer/diagrams/blob/master/LICENSE. El README no declara una licencia propia para los íconos ni para los logos de terceros.
- **OpenStack** (`openstack/compute/nova.png`, `networking/neutron.png`, `storage/cinder.png`): **no es una licencia abierta, sino una política de marca**. Los logos son marcas de la OpenStack Foundation d/b/a OpenInfra Foundation (https://www.openstack.org/brand/). Su política (https://www.openstack.org/brand/openstack-trademark-policy/) tiene una regla para individuos que actúan a título personal, que incluye «educational materials like a slide deck presented at a conference», y otra para organizaciones, con condiciones distintas. CUC es una organización. **Sin confirmar: falta la decisión de CUC/docente sobre si este uso encaja en la política antes de publicar.**
- **On-prem** (`onprem/...`: servidor, switch, cliente, usuario, PostgreSQL, MySQL, MariaDB, GitHub, Git): **sin confirmar**. No encontré en el repo ni en la librería una licencia por archivo; las marcas de PostgreSQL, MySQL, MariaDB, GitHub y Git pertenecen a sus titulares.
- **Kubernetes** (`k8s/k8s.png`): no verificado en este piloto.

- OpenStack: `openstack/compute/nova.png`, `openstack/networking/neutron.png`, `openstack/storage/cinder.png`
- Genéricos y on-prem: `onprem/compute/server.png`, `onprem/network/cisco-switch-l2.png`, `onprem/client/client.png`, `onprem/client/user.png`, `onprem/database/{postgresql,mysql,mariadb}.png`, `onprem/vcs/{github,git}.png`
- Kubernetes: `k8s/k8s.png`

## Diapositivas afectadas

- S13 diap. 6 (Nova Scheduler): íconos OpenStack y servidores on-prem.
- S13 diap. 25 (IP flotante): usuario, switch, Nova.
- S15 diap. 5 (NVLink frente a PCIe): foto H100 + diagramas propios.
- S15 diap. 10 (refrigeración): foto CoolIT + gráfica propia de kW por rack.
- S15 diap. 27 (KV-Cache): diagrama propio de memoria por usuario.
- S16 diap. 36 (MCP): íconos de clientes y fuentes (PostgreSQL, MySQL, MariaDB, Kubernetes, GitHub, Git).

## Cifras de S15 sin fuente en el repositorio (no editadas)

- Diap. 10: «Aire: PUE ≈ 1,5» y «Líquido: PUE ≈ 1,15»: no aparecen en `docs/cifras-S15.md` ni en el guion.
- Diap. 10: «40 a más de 100 kW»: el guion dice «más de cuarenta kilovatios»; el 100 no tiene fuente.
- Diap. 5: «en modelos de 70 mil a 405 mil millones de parámetros»: no aparece en fuentes ni en el guion.

La cifra «10,2 kW» (un DGX H100) sí quedó respaldada en `docs/cifras-S15.md`, sección 1.3.
