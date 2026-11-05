# Fuentes de recursos: piloto visual Unidad 3 (Arquitectura en la Nube)

Recursos nuevos o usados en las diapositivas rediseñadas (rama `arq-piloto-u3`). Licencias verificadas en la API de Wikimedia Commons (`extmetadata`) el 2026-11-05.

## Fotos (assets/fotos/)

| Archivo local | Diapositiva | Autor | Licencia | Página del archivo | Modificación |
|---|---|---|---|---|---|
| `nvidia-h100-nvlink-geekerwan-002.png` | S15 diap. 5 | Geekerwan (极客湾) | CC BY 3.0 (https://creativecommons.org/licenses/by/3.0) | https://commons.wikimedia.org/wiki/File:NVIDIA_H100_(%E6%9E%81%E5%AE%A2%E6%B9%BEGeekerwan)_002.png | Ninguna en el archivo. En la diapositiva: recorte `slice` de 440 × 330 u (≈37 % del ancho del lienzo, foto grande) y pie «Tarjetas H100 apiladas». La descripción de Commons dice «Here you can see 4 stacked cards» y no menciona conectores NVLink, por eso se retiró ese rótulo (verificado 2026-11-05) |
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

## Piloto S15 (2026-11-05): GPU, cuantización y despliegue

Rediseño del deck S15 con el estándar de S13 y S14. Los guiones no cambiaron (idénticos a HEAD). Las licencias de las fotos son las ya registradas en las secciones S13 y S14 de este archivo; no se volvieron a consultar en la API en esta pasada.

### Fotos (assets/fotos/)

| Archivo local | Diapositiva | Autor (Commons) | Licencia | Estado frente a S14 | Modificación |
|---|---|---|---|---|---|
| `nvidia-h100-nvlink-geekerwan-002-recorte.png` (derivada de `nvidia-h100-nvlink-geekerwan-002.png`) | S15 diap. 5 | Geekerwan (极客湾) | CC BY 3.0 (https://creativecommons.org/licenses/by/3.0) | Reutilizada | Recorte sin estirar a las cuatro tarjetas (píxeles 440–960 × 60–274 de la original, 520 × 214); se oculta el precio impreso «约300,000元». La original no se modificó |
| `coolit-rack-refrigeracion-liquida.jpg` | S15 diap. 10 | Barbara Massolin (CoolIT) | CC BY-SA 3.0 (https://creativecommons.org/licenses/by-sa/3.0) | Reutilizada | `slice` |
| `switches-rack-patch-panels.jpg` | S15 diap. 8 (redes EFA) | Dsimic | CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0) | **Nueva** | `slice` |
| `rubin-sala-computo-cumbre.jpg` | S15 diap. 41 (nube privada OpenStack) | Rubin Observatory/NSF/AURA | CC BY 4.0 (https://creativecommons.org/licenses/by/4.0) | **Nueva** | `slice` |
| `amravati-racks-datacenter.jpg` | S15 diap. 44 (caso self-hosted) | PiDatacenters | CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0) | **Nueva** | `slice` |
| `noirlab-sala-servidores-racks.jpg` | S15 diap. 50 (seguridad y ZDR) | NOIRLab/NSF/AURA, T. Slovinský | CC BY 4.0 (https://creativecommons.org/licenses/by/4.0) | Reutilizada | `slice` |

Son seis fotos: tres nuevas frente a S14 (la regla pedía al menos dos). Las URL de las páginas de archivo están en la tabla de S13 y S14.

### Íconos

Los íconos de `assets/iconos/` se usan sin modificar. Marcas: solo para el servicio que representan (AWS, Bedrock, EC2, PrivateLink, KMS, SQS, Budgets, VPC, CloudWatch, IAM; Azure no se usa como marca de otro servicio). Íconos de OpenStack (Nova, Cinder, Neutron, Octavia): la nota de política de marca de S13 sigue sin decisión de CUC; el uso es el mismo de S13.

### Cifras de S15: decisión sobre cada cifra

| Cifra (versión anterior) | Diap. | Decisión | Fuente / motivo |
|---|---|---|---|
| «Aire: PUE ≈ 1,5» y «Líquido: PUE ≈ 1,15» | 10 | **Quitadas**; se muestra el PUE medio mundial de 1,54 | Uptime Institute, Global Data Center Survey 2025 (1,54, según cobertura secundaria; el informe primario no se abrió) |
| «más de 100 kW por rack», «40 a más de 100 kW» | 10 | **Quitadas** | Las fuentes consultadas dan límites del aire entre 30 y 50 kW con criterios distintos; no hay una cifra homogénea |
| «Límite del aire: 10 a 15 kW por rack» | 10 | **Quitada** (cualitativa) | Misma razón |
| 1 servidor DGX H100 (8 GPU, máx.): 10,2 kW; 4 servidores ≈ 41 kW | 10 | **Respaldada** | NVIDIA, DGX H100 (10,2 kW máx.); 4 × 10,2 = 40,8 (cálculo propio) |
| «70 mil a 405 mil millones de parámetros» | 5, 25, 38 | **Respaldada** como «Llama 3.1: 70B y 405B» | Meta, Llama 3.1 model card (tamaños 8B, 70B y 405B, verificado en vivo) |
| «> 3 TB/s en A100/H100» | 15 | **Corregida**: H100 SXM 3,35 TB/s; A100 SXM 2,04 TB/s (PCIe 1,94) | NVIDIA, páginas de A100 y H100 (verificado en vivo) |
| «600 a 900 GB/s» (GDDR6, A10G) | 3 | **Corregida**: A10G 600 GB/s | NVIDIA, A10 (cifra ya registrada en `docs/cifras-S15.md` §1.1; no reverificada en vivo) |
| «50 a 100 GB/s» (DDR5 del host), «> 10 TB/s» (SRAM), «512 GB a 2 TB», «50 a 256 MB», «80 a 141 GB» | 3 | **Quitadas** (cualitativas) | Sin fuente |
| «16 veces» (Tensor Core frente a unidades tradicionales) | 4 | **Quitada** | Sin fuente |
| FP8 frente a FP16: «duplica» | 4 | **Respaldada** | NVIDIA, H100: FP8 3 958 TFLOPS frente a FP16 1 979 TFLOPS, ambos con sparsity (verificado en vivo) |
| «Hasta 50 %» de ahorro en Inf2 | 6 | **Quitada** | Sin fuente en el repositorio |
| g5.xlarge $1,006 / h | 7, 54 | **Respaldada** | AWS Price List, us-east-1 (ya registrada en S14; consulta 2026-11-05) |
| p5.48xlarge $55,04 / h | 7 | **Quitada** | Pendiente de verificar en vivo (igual que S14) |
| «Latencia sub-microsegundo» y «unos pocos microsegundos» (EFA) | 8 | **Quitadas** (cualitativas) | Sin fuente |
| «Pérdida menor al 1 %» (passthrough) | 11 | **Quitada** | Sin fuente; el texto dice que se valida en laboratorio |
| «30 % a 55 %» de MFU en inferencia | 12 | **Quitada**; se explica que el MFU de decodificación es bajo | Sin fuente en el repositorio; la longitud de la barra del MFU real es ilustrativa |
| «Cada 5 a 10 s» (DCGM) | 13 | **Quitada** | Sin fuente |
| «1 a 2 GB» reservados para CUDA | 17 | **Quitada** | Sin fuente |
| «> 3,5 GB/s» y «40 GB en < 15 s» (Cinder) | 41 | **Quitadas** | Sin fuente |
| Precios p4de.24xlarge «$15 a $20 / h» y g5.12xlarge «$5,60 / h»; ahorro «> 65 %» | 29 | **Quitados** | No verificados; la comparación queda en memoria: 140 GB frente a 35 GB, 320 GB frente a 48 GB (cálculo propio) |
| «PPL sube < 0,2» y «retiene > 98 % del benchmark» | 23 | **Quitadas**; el umbral se declara como criterio del equipo | Sin fuente en el repositorio |
| «> 99 % de retención» (GPTQ) y «128 a 512 secuencias» de calibración | 20 | **Quitadas** | Sin fuente verificada en esta pasada |
| «100 veces» (activaciones salientes) | 21 | **Quitada**; se conserva «1 %» | Lin et al. (2023), arXiv:2306.00978 |
| «2 GB de caché por usuario» (32 000 tokens) | 27 | **Corregida**: 4 GB por sesión en FP16 y 2 GB en FP8; dos sesiones frente a cuatro | Cálculo propio: 2 × 32 capas × 8 cabezas KV × 128 × 2 bytes × 32 000 = 4,2 × 10⁹ bytes. Configuración de Llama 3 8B: 32 capas, 8 KV, dimensión 128 (Dubey et al. 2024, arXiv:2407.21783, verificado en vivo) |
| «8x de ahorro» (GQA) | 26 | **Quitada** la cifra; se explica la relación general | El factor depende del número de consultas por par K/V |
| «Hasta 2,5x menor latencia» (TensorRT-LLM) | 28 | **Quitada** | Sin fuente verificada |
| «Más de 2 000 tokens/s» con 4 nodos A10G (caso) | 44 | **Rotulada como supuesto** de diseño | Caso ilustrativo |
| TTFT < 800 ms, TPOT < 40 ms, 1 500 tokens/s por nodo | 39 | **Rotuladas como objetivos de ejemplo** (1 500 tokens/s quitado) | Supuestos de diseño, no medidos |
| «Reducción de costo de más del 70 %» con el enrutador | 57 | **Quitada**; 70 % y 30 % del tráfico quedan como supuesto | Sin fuente |
| «Circular Externa 007 (2025)» | 58 | **Corregida** a «de 2018» | Denominación de la circular; **verificar la fecha en la fuente** (no abierta en vivo) |
| Códigos XID 31, 45 y 79 con causas distintas a las del catálogo | 13, 42 | **Corregidos** | NVIDIA, catálogo de errores XID (verificado en vivo): 31 = GPU memory page fault; 45 = preemptive cleanup, due to previous errors; 79 = GPU has fallen off the bus |
| Límite de rack «ventiladores» en la diap. 10 | 10 | Descripción cualitativa | Sin cifra única |
| Tarifa de Bedrock, caché 90 % | 48, 53 | **Respaldadas** | `_arq-material/docs/fuentes/precios-bedrock-us-east-1.txt`: Haiku 5.5 $0,10 / $0,50, caché $0,01; Sonnet 5.5 $2 / $10, caché $0,10; Nova Micro $0,035 / $0,14 y Nova Lite $0,06 / $0,24 (Nova en la unidad por 1 000 tokens del archivo) |
| 183 M tokens/mes de punto de equilibrio | 54 | **Respaldada** (cálculo) | $734,4 ÷ $4,00 por millón (mezcla 3:1 con Sonnet 5.5) |
| ~12 000 M tokens/mes con Nova Micro | 54 | **Respaldada** (cálculo) | $734,4 ÷ $0,06125 (mezcla 3:1 con Nova Micro) |
| «SLA 99,9 %» de Bedrock | 55 | Mantenida con la cita de documentación oficial | Pendiente de verificar en vivo |

### Diapositivas afectadas

- S15 diap. 2–15, 17–30, 32–45 y 47–60: rediseño con diagramas propios del mecanismo e íconos de `assets/iconos/`.
- Diap. 45: el título pasó de «Decálogo» a «Cuatro reglas de operación» (la diapositiva muestra cuatro reglas).
- Portadas 1, 16, 31 y 46: sin cambios de contenido; la portada 46 agrega «TCO = costo total de propiedad» al pie de siglas.

## Piloto S16 (2026-11-05): Capacidades de los modelos y repaso de la Unidad 3

Rediseño del deck S16 con el estándar de S15 v3 (diagramas con íconos reales, máximo 25 palabras por diapositiva, fotos grandes con crédito). Los guiones `<aside class="guion">` no se tocaron.

### Fotos (assets/fotos/, ya registradas en S13/S14; reutilizadas)

| Archivo local | Diapositiva | Autor (Commons) | Licencia |
|---|---|---|---|
| `wikimedia-servidores-racks.jpg` | S16 diap. 12 (banda superior) | Victorgrigas | CC BY-SA 3.0 |
| `switches-rack-patch-panels.jpg` | S16 diap. 49 | Dsimic | CC BY-SA 4.0 |
| `noirlab-sala-servidores-racks.jpg` | S16 diap. 50 | NOIRLab/NSF/AURA, T. Slovinský | CC BY 4.0 |
| `nvidia-h100-nvlink-geekerwan-002-recorte.png` | S16 diap. 51 | Geekerwan | CC BY 3.0 |

### Íconos

Íconos oficiales de `assets/iconos/` (AWS, Kubernetes, OpenStack, marcas de software). Cada marca se usa solo para su servicio o proyecto; los conceptos genéricos usan íconos genéricos de `aws/general`, `generic/` y `onprem/`.

### Cifras de S16: decisión sobre cada cifra

| Cifra (versión anterior) | Diap. | Decisión | Fuente / motivo |
|---|---|---|---|
| Modelo 32B con razonamiento supera a 405B | 3 | Quitada del diagrama (barras ilustrativas, sin cifras) | Sin fuente en el repositorio; el guion conserva la afirmación y queda pendiente de respaldo docente |
| 0,5–1,2 s y 8–45 s de latencia; 8 veces más costo | 9 | Latencias quitadas; se conserva el cálculo del costo | Costo: 1 000 × $2/M + 400 × $10/M = $0,006; 1 000 × $2/M + 4 500 × $10/M = $0,047 (≈ 8 veces). Tarifas de `precios-bedrock-us-east-1.txt` |
| 3x a 10x de tokens de pensamiento | 8 | Quitada | Sin fuente; el diagrama usa solo las etiquetas |
| budget_tokens 1 024 / 4 096 / 16 384+ con latencias < 5 s, 10–20 s, > 45 s | 10 | Se conservan los valores; latencias quitadas | Mínimo de 1 024 verificado en la documentación de Anthropic (platform.claude.com, extended thinking, consulta 2026-11-05). Esa página indica que `budget_tokens` está deprecado en modelos 4.7 y posteriores (usar thinking adaptativo con effort) |
| SWE-bench: «40 % a 55 %»; HumanEval «> 90 %» | 18 | Quitadas (cualitativo: «benchmark saturado») | Sin verificar en esta sesión |
| Firecracker: arranque de 5–10 ms; < 10 ms; ~5 MB | 23, 24 | Quitadas | No verificadas; el guion dice 5–10 ms, la cifra del paper NSDI 2020 que se revisará es distinta (pendiente para el docente) |
| PagedAttention: 60–80 % de desperdicio y < 4 % | 53 | Quitadas (cualitativo: «desperdicio alto» / «casi cero desperdicio») | El abstract de Kwon et al. (arXiv:2309.06180) confirma «2-4×» de rendimiento y «near-zero waste»; los porcentajes no aparecen en el abstract |
| 2–4 veces de rendimiento (vLLM) | 53 | Respaldada | Abstract de arXiv:2309.06180 (verificado 2026-11-05) |
| AWQ: 1 % de pesos salientes | 52 | Respaldada | Abstract de arXiv:2306.00978 («Protecting only 1% salient weights»; verificado 2026-11-05) |
| 3x de reducción de VRAM (70B: 140 GB → 40 GB) | 52 | Quitada | Cálculo aproximado sin fuente |
| Ahorro de 80 % de tokens de salida | 30, 40 | Quitadas (cualitativo) | Sin fuente |
| Éxito de invocación > 98 % | 35 | Quitada | Sin fuente |
| 15–50 ms de búsqueda vectorial | 39 | Quitada | Sin fuente |
| Punto de equilibrio de 183 M tokens / mes | 55 | Reemplazada por 191 M | $734 ÷ $0,005 por petición × 1 300 tokens = 191 M tokens/mes; coherente con S14 y S15 |
| Ruteo 20 % / 80 % | 15 | Quitada (cualitativo: «solo consultas complejas») | Sin fuente |
| Precios de Bedrock | 8, 9, 54 | Respaldadas | Solo de `precios-bedrock-us-east-1.txt`: Nova Micro $0,035/$0,14; Haiku 5.5 $0,10/$0,50; Sonnet 5.5 $2/$10; Opus 5.5 $4/$20 por millón |
| GPT-6.1 Sol (guion, diap. 17) | 17 | No aparece en la diapositiva; el guion lo menciona | Sin fuente verificable; pendiente para el docente |
| H100: 3,35 TB/s; NVLink 900 GB/s | 51 | Respaldadas | NVIDIA H100 (nvidia.com/en-us/data-center/h100) |
| CPU DDR5 «200 a 300 GB/s» | 51 | Quitada (cualitativo: «ancho de banda bajo») | Sin fuente |
| Ley 1581 de 2012 | 56 | Respaldada | Ley Estatutaria 1581 de 2012; SIC (sic.gov.co) |
