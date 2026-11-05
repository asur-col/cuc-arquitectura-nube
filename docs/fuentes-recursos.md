# Fuentes de recursos: piloto visual Unidad 3 (Arquitectura en la Nube)

Recursos nuevos o usados en las diapositivas rediseñadas (rama `arq-piloto-u3`). Licencias verificadas en la API de Wikimedia Commons (`extmetadata`) el 2026-11-05.

## Fotos (assets/fotos/)

| Archivo local | Diapositiva | Autor | Licencia | Página del archivo | Modificación |
|---|---|---|---|---|---|
| `nvidia-h100-nvlink-geekerwan-002.png` | S15 diap. 5 | Geekerwan (极客湾) | CC BY 3.0 (https://creativecommons.org/licenses/by/3.0) | https://commons.wikimedia.org/wiki/File:NVIDIA_H100_(%E6%9E%81%E5%AE%A2%E6%B9%BEGeekerwan)_002.png | Ninguna en el archivo. En la diapositiva: recorte `slice` (≈20 % del ancho) y pie «4 tarjetas H100 apiladas». La descripción de Commons dice «Here you can see 4 stacked cards» y no menciona conectores NVLink, por eso se retiró ese rótulo (verificado 2026-11-05) |
| `coolit-rack-refrigeracion-liquida.jpg` | S15 diap. 10 | Barbara Massolin (CoolIT) | CC BY-SA 3.0 (https://creativecommons.org/licenses/by-sa/3.0) | https://commons.wikimedia.org/wiki/File:%C2%A9_CoolIT_Rack_DCLC_AHx_Liquid_Cooling_Solution.jpg | Ninguna (600×394 original) |
| `cern-sala-servidores-02.jpg` | S13 diap. 13 (caso de dimensionamiento: hipervisores físicos) | Florian Hirzinger (CERN) | CC BY-SA 3.0 (https://creativecommons.org/licenses/by-sa/3.0) | https://commons.wikimedia.org/wiki/File:CERN_Server_02.jpg | Recorte `slice` a ≈460×118 px en la diapositiva. Título, autor y licencia confirmados por la API de Commons el 2026-11-05; el archivo local está redimensionado, por eso su SHA-1 no coincide con el original |

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

- S13 diap. 2–5, 7–15, 17–24, 26–30, 32–45 y 47–60: rediseño con íconos oficiales de `assets/iconos/` (sin modificar) y diagramas propios. Diap. 6 y 25 sin cambios (diseño piloto aprobado).
- S13 diap. 13: foto `cern-sala-servidores-02.jpg` (ver tabla de fotos).
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

## Segunda pasada S13 (2026-11-05)

### Fotos nuevas (assets/fotos/), licencias verificadas en la API de Wikimedia Commons

| Archivo local | Diapositiva | Autor (Commons) | Licencia | Página del archivo |
|---|---|---|---|---|
| `noirlab-sala-servidores-racks.jpg` | S13 diap. 47 (producción) | NOIRLab/NSF/AURA, T. Slovinský | CC BY 4.0 (https://creativecommons.org/licenses/by/4.0) | https://commons.wikimedia.org/wiki/File:NOIRLab_HQ_Server_Racks_(6V6A0395-CC).jpg |
| `switches-rack-patch-panels.jpg` | S13 diap. 49 (segmentación) | Dsimic | CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0) | https://commons.wikimedia.org/wiki/File:19-inch_rackmount_Ethernet_switches_and_patch_panels.jpg |
| `rubin-sala-computo-cumbre.jpg` | S13 diap. 53 (criterios de nube privada) | Rubin Observatory/NSF/AURA | CC BY 4.0 (https://creativecommons.org/licenses/by/4.0) | https://commons.wikimedia.org/wiki/File:Summit_Computer_Room_Installation_(rubin-2018-05-02-110524).jpg |
| `wikimedia-servidores-racks.jpg` | S13 diap. 37 (topología de control, ilustración) | Victorgrigas | CC BY-SA 3.0 (https://creativecommons.org/licenses/by-sa/3.0) | https://commons.wikimedia.org/wiki/File:Wikimedia_Foundation_Servers-8055_13.jpg |
| `amravati-racks-datacenter.jpg` | S13 diap. 60 (práctica guiada) | PiDatacenters | CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0) | https://commons.wikimedia.org/wiki/File:Racks_Amravati_Data_Center.jpg |

Descargadas desde los thumbnails de 1280 px de Commons (sin modificar salvo redimensión). La foto CERN de S13 diap. 13 se mantiene.

### Cifras de S13: qué se quitó y qué quedó respaldado

| Cifra original | Diapositiva | Decisión | Fuente / motivo |
|---|---|---|---|
| 70 % de utilización | 53 | Quitada: «utilización sostenida alta» | Cita sin verificar en investigacion-S13.md (openstack.org/user-stories); no se pudo confirmar el número |
| 75 % de uso (alerta de disco) | 55 | Quitada | Sin fuente |
| 25 / 100 Gbps | 36, 58 | Quitadas; «bonds LACP» sin velocidad | Sin fuente verificable |
| 10.0.0.100 (IP virtual) | 40 | Quitada: «IP virtual (VIP)» | Dato de ejemplo sin respaldo |
| 50 GB y Ubuntu 24.04 | 35 | Quitados: «Ubuntu (LTS)» y «clonación casi instantánea» | Sin fuente |
| cpu_allocation_ratio = 4.0, ram_allocation_ratio = 1.0, «3:1 a 4:1» | 55 | **Corregida** con los valores por defecto documentados: CPU 16.0, RAM 1.5, disco 1.0 | https://docs.openstack.org/nova/latest/admin/scheduling.html (sección de allocation ratios, verificada el 2026-11-05) |
| max_attempts = 3 (reintentos del scheduler) | 10 | Conservada | https://docs.openstack.org/nova/latest/configuration/config.html: `max_attempts`, default 3 (verificada el 2026-11-05) |
| 3:1 de sobresuscripción y 768 vCPU sobre 256 núcleos | 13, 58 | Conservadas como caso ilustrativo (aritmética del caso: 4×64 núcleos, 3:1) | Caso ilustrativo declarado en la diapositiva |

Nota: la URL del pie de diap. 55 pasó de `admin/configuration/schedulers.html` (301) a `admin/scheduling.html`.

Cifras de S15 (PUE 1,5 / 1,15; >100 kW; 70–405 mil millones de parámetros) **no se tocaron**: S14–S16 están fuera del alcance de esta pasada y siguen pendientes de respaldo.

## Piloto S14 (2026-11-05): Modelos, tokens e inferencia

Rediseño del deck S14 con el estándar aprobado en S13. Las licencias de las fotos se volvieron a verificar en la API de Wikimedia Commons (`extmetadata`) el 2026-11-05.

### Fotos (assets/fotos/)

| Archivo local | Diapositiva | Autor (Commons) | Licencia | Página del archivo | Modificación |
|---|---|---|---|---|---|
| `nvidia-h100-nvlink-geekerwan-002.png` | S14 diap. 41 (instancias GPU) | Geekerwan (极客湾) | CC BY 3.0 (https://creativecommons.org/licenses/by/3.0) | https://commons.wikimedia.org/wiki/File:NVIDIA_H100_(%E6%9E%81%E5%AE%A2%E6%B9%BEGeekerwan)_002.png | Recorte `xMaxYMid slice` a la zona de las tarjetas. La imagen trae impreso un precio («约300,000元»), que queda fuera del recorte |
| `noirlab-sala-servidores-racks.jpg` | S14 diap. 50 (servidor dedicado) | NOIRLab/NSF/AURA, T. Slovinský | CC BY 4.0 (https://creativecommons.org/licenses/by/4.0) | https://commons.wikimedia.org/wiki/File:NOIRLab_HQ_Server_Racks_(6V6A0395-CC).jpg | Recorte `slice` |
| `coolit-rack-refrigeracion-liquida.jpg` | S14 diap. 51 (servidor dedicado: costos y mantenimiento) | Barbara Massolin (CoolIT) | CC BY-SA 3.0 (https://creativecommons.org/licenses/by-sa/3.0) | https://commons.wikimedia.org/wiki/File:%C2%A9_CoolIT_Rack_DCLC_AHx_Liquid_Cooling_Solution.jpg | Recorte `slice` |
| `cern-sala-servidores-02.jpg` | S14 diap. 52 (inferencia local) | Florian Hirzinger (CERN) | CC BY-SA 3.0 (https://creativecommons.org/licenses/by-sa/3.0) | https://commons.wikimedia.org/wiki/File:CERN_Server_02.jpg | Recorte `slice` |

### Cifras de S14: decisión sobre cada cifra

| Cifra (versión anterior) | Diap. | Decisión | Fuente / motivo |
|---|---|---|---|
| Precios Nova Micro, Lite y Pro; Haiku, Sonnet y Opus 5.5 | 26, 25, 27, 28 | Respaldadas | Tarifas de Bedrock us-east-1, consulta 2026-11-05 (`docs/fuentes/precios-bedrock-us-east-1.txt` de `_arq-material`). Las tarifas de Claude están en `$/1M`; Nova está en otra unidad en el archivo, y se usaron los valores aprobados por el docente |
| Claude 3.5 Sonnet a $3 / $15 | 26 | Quitada | No aparece en el archivo de precios |
| Sobrecosto de tokenización de +75 % y de 25–50 % | 19 | Quitadas | Conteo ilustrativo no medido con un tokenizador real. El diagrama queda como ejemplo rotulado |
| Vocabulario de 200.000 tokens y «GPT-6» | 20 | Quitadas | Sin fuente en el repositorio. Se conservan 32.000 (Llama 2) y 128.256 (Llama 3), de las model cards de Meta |
| Contexto de 1 a 2 millones de tokens en 2026 | 22 | Quitada | Sin fuente. Se conserva el par 2.048 (GPT-3, arXiv:2005.14165) y 200.000 (Claude 3.5 Sonnet, documentación de modelos). La URL de esta última está en `docs/cifras-S14.md` y **su verificación en vivo queda pendiente** |
| «≈ 98 veces más contexto» | 22 | Respaldada (cálculo) | 200.000 ÷ 2.048 |
| N = 100.000 → 10¹⁰ pares | 23 | Respaldada (cálculo) | N² con N = 100.000 |
| Descuento de caché de 90 % a 95 % y TTFT −80 % | 24 | Respaldada parcialmente | 95 % = 1 − 0.10/2.00 (cálculo con tarifas). La reducción del TTFT (−80 %) se quitó: sin fuente |
| Mínimo de 1.024 tokens para caché | 28 | Quitada | No aparece en el archivo de tarifas |
| Escritura 125 % de la tarifa base | 24 | Respaldada (cálculo) | $2.50 / $2.00 |
| Ahorro de 52 % frente a Sonnet 5.5 | 27 | Respaldada (cálculo) | 120.40 ÷ 250.00 = 0.48 |
| Ahorro de 83 % con caché | 28 | Respaldada (cálculo) | 34.00 ÷ 200.00 = 0.17 |
| «3x a 5x» de salida frente a entrada | 25 | Respaldada (cálculo) | Razón salida/entrada en el archivo: 4 a 5 para Nova, Haiku, Sonnet y Opus |
| Cold start de 2 a 5 min y cooldown de 300 s | 42 | Quitadas (cualitativo: «minutos») | Sin fuente verificada en esta sesión |
| Latencia de 8 s y de 400 tokens sin streaming | 39 | Quitadas (cualitativo) | Ejemplo sin fuente |
| VRAM vacía de más de 60 % y «2 a 4 veces» de batching | 35, 36 | Quitadas | Sin fuente |
| Legacy de Claude 3.5 Sonnet y Llama 3.3 con fechas de retiro | 12 | Quitadas (cualitativo) | Fechas sin verificar en vivo; la diapositiva solo dice «en estado Legacy» con la URL del ciclo de vida |
| 1 token ≈ 4 caracteres en inglés y ≈ 3 en español | 17 | Quitada | Sin fuente |
| g5.xlarge a $1.006 / h; $734 al mes | 41, 50, 51, 54 | Respaldadas | $1.006 × 730 h = $734.38. `docs/investigacion-S14.md` registra $1.0061/h y $734.45/mes |
| g6e.xlarge a $1.861 / h y p5.48xlarge a $55.04 / h | 41 | Respaldadas por la lista de precios aprobada | **No están en el archivo local de tarifas; verificación en vivo pendiente** |
| g5.12xlarge a $5.672 / h y g6.xlarge a $0.805 / h | 41 | Quitadas | No verificadas |
| Punto de equilibrio de 183 M tokens / mes | 54 | Reemplazada por 191 M | Cálculo: $734.38 ÷ (0.005 $ / 1 300 tokens por petición) = 191 M. Supuesto: 1 000 entrada + 300 salida por petición con tarifas de Sonnet 5.5 |
| Reparto 80/20 entre modelos | 27 | Respaldado como supuesto de arquitectura | Rotulado como supuesto, no como dato de mercado |
| Reducción de costo de más de 60 % con el enrutador | 55 | Quitada | Sin fuente. Sí aparece la cifra calculada de 52 % en la diapositiva 27 |
| Puerto 11434 de Ollama | 52 | Respaldada (verificación pendiente) | Documentación de Ollama (github.com/ollama/ollama) |
| Artículo 26 de la Ley 1581 de 2012 | 53 | Respaldada | Ley 1581 de 2012, art. 26 (texto del Gestor Normativo) |
| Listado de países «adecuados» de la SIC | 53 | Quitado | El listado no se verificó. La diapositiva dice que hay que verificarlo |
