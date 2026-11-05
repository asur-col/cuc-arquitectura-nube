# Respaldo de Cifras y Datos — Semana 15
**Asignatura**: Arquitectura en la Nube (2026-2)  
**Tema**: IA en la Nube II: GPU, Cuantización y Despliegue  
**Fecha de consulta y verificación oficial**: Noviembre de 2026  

---

## 1. Especificaciones de Hardware y Aceleradores GPU

### 1.1 Ancho de Banda y Capacidad de Memoria (Diapositivas 3, 4, 5, 15)
- **HBM3 en NVIDIA H100**: Ancho de banda de 3.35 TB/s, capacidad de 80 GB.
  - *Fuente*: NVIDIA H100 Tensor Core GPU Architecture Whitepaper (2024).
  - *URL*: `https://www.nvidia.com/en-us/data-center/h100/`
  - *Dato verificado*: HBM3 alcanza 3.35 TB/s en bus de 5120 bits.
- **PCIe Gen 5 x16**: Ancho de banda unidireccional de 64 GB/s (128 GB/s bidireccional).
  - *Fuente*: PCI-SIG PCIe 5.0 Specification.
  - *URL*: `https://pcisig.com/specifications/pciexpress/5.0`
- **NVLink 4**: Ancho de banda bidireccional de 900 GB/s por GPU en arquitectura Hopper.
  - *Fuente*: NVIDIA NVLink High-Speed Interconnect Specification.
  - *URL*: `https://www.nvidia.com/en-us/data-center/nvlink/`
- **NVIDIA A10G**: 24 GB GDDR6, 600 GB/s ancho de banda de memoria.
  - *Fuente*: NVIDIA A10G Tensor Core GPU Datasheet.
  - *URL*: `https://www.nvidia.com/en-us/data-center/products/a10-gpu/`

### 1.2 Catálogo y Tarifas de Instancias AWS EC2 (Diapositivas 7, 14, 29, 54)
Tarifas on-demand para región US East (N. Virginia), consultadas oficialmente en noviembre de 2026:
- **g5.xlarge**: 1x NVIDIA A10G (24 GB VRAM), 4 vCPUs, 16 GB RAM.
  - *Tarifa On-Demand*: ~$1.006 USD/hora (~$730 USD/mes de operación continua).
  - *URL*: `https://aws.amazon.com/ec2/instance-types/g5/`
- **g6.xlarge**: 1x NVIDIA L4 (24 GB VRAM), 4 vCPUs, 16 GB RAM.
  - *Tarifa On-Demand*: ~$0.804 USD/hora.
  - *URL*: `https://aws.amazon.com/ec2/instance-types/g6/`
- **g5.12xlarge**: 4x NVIDIA A10G (96 GB VRAM total), 48 vCPUs, 192 GB RAM.
  - *Tarifa On-Demand*: ~$5.672 USD/hora.
  - *URL*: `https://aws.amazon.com/ec2/pricing/on-demand/`
- **p4de.24xlarge**: 8x NVIDIA A100 (80 GB HBM2e, 640 GB total), 96 vCPUs, 1.152 GB RAM, 400 Gbps EFA.
  - *Tarifa On-Demand*: ~$40.96 USD/hora.
  - *URL*: `https://aws.amazon.com/ec2/instance-types/p4/`

---

## 2. Cuantización y Dimensionamiento de VRAM

### 2.1 Presupuesto de Memoria (Diapositivas 4, 17, 18, 29)
- **Fórmula de VRAM base**: `Bytes por Parámetro × Número de Parámetros`.
  - FP16 (16 bits) = 2 bytes/parámetro. Modelo 8B = 16 GB; Modelo 70B = 140 GB.
  - INT8 (8 bits) = 1 byte/parámetro. Modelo 8B = 8 GB; Modelo 70B = 70 GB.
  - INT4 (4 bits) = 0.5 bytes/parámetro. Modelo 8B = 4 GB; Modelo 70B = 35 a 40 GB (incluyendo metadatos de escala y punto cero).
  - *Fuente*: HuggingFace Model Memory Calculator Guide.
  - *URL*: `https://huggingface.co/docs/transformers/model_memory_anatomy`

### 2.2 Benchmarks de Algoritmos AWQ y GPTQ (Diapositivas 20, 21, 23, 30)
- **AWQ (Activation-aware Weight Quantization)**:
  - Protege el 1 % superior de canales de activación salientes.
  - Retención de precisión en MMLU > 99 % frente a FP16 original.
  - *Fuente*: Lin et al. — AWQ Paper (MLSys 2024).
  - *URL*: `https://arxiv.org/abs/2306.00978`
- **GPTQ (Accurate Post-Training Quantization)**:
  - Cuantización analítica por capas mediante compensación de residuos.
  - Retención de precisión > 98.5 % en Llama-2 y Llama-3.
  - *Fuente*: Frantar et al. — GPTQ Paper (ICLR 2023).
  - *URL*: `https://arxiv.org/abs/2210.17323`

---

## 3. Tarifas Oficiales de Amazon Bedrock (Noviembre 2026)

Tarifas on-demand por 1 Millón de tokens (1M tokens) en región US East (N. Virginia):
- **Amazon Nova Micro**:
  - Entrada (Input): $0.035 USD / 1M tokens.
  - Salida (Output): $0.140 USD / 1M tokens.
  - Inferencia por Lotes (Batch): 50 % de descuento ($0.0175 / $0.070).
  - *URL*: `https://aws.amazon.com/bedrock/pricing/`
- **Amazon Nova Lite**:
  - Entrada (Input): $0.060 USD / 1M tokens.
  - Salida (Output): $0.240 USD / 1M tokens.
  - Lectura de Prompt Cache: $0.015 USD / 1M tokens.
  - *URL*: `https://aws.amazon.com/bedrock/pricing/`
- **Claude Haiku 5.5 (Activo)**:
  - Entrada (Input): $0.100 USD / 1M tokens.
  - Salida (Output): $0.500 USD / 1M tokens.
  - Lectura de Prompt Cache: $0.010 USD / 1M tokens (90 % de descuento).
  - *URL*: `https://aws.amazon.com/bedrock/pricing/` (consulta: 2026-11-05)
- **Claude Sonnet 5.5 (Activo)**:
  - Entrada (Input): $2.000 USD / 1M tokens.
  - Salida (Output): $10.000 USD / 1M tokens.
  - Lectura de Prompt Cache: $0.200 USD / 1M tokens (90 % de descuento).
  - *URL*: `https://aws.amazon.com/bedrock/pricing/` (consulta: 2026-11-05)
- **Claude 3.5 Sonnet (Histórico / Legacy)**:
  - Entrada: $3.000 USD / 1M tokens | Salida: $15.000 USD / 1M tokens.
  - Estado: Legacy 10-oct-2026, EOL 13-nov-2026.
  - *URL*: `https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle.html` (consulta: 2026-11-05)
- **Claude 3 Haiku (Modelo Histórico)**:
  - Entrada (Input): $0.250 USD / 1M tokens.
  - Salida (Output): $1.250 USD / 1M tokens.
  - *Rotulado*: Modelo histórico previo al lanzamiento de Claude 3.5 Haiku.
  - *URL*: `https://aws.amazon.com/bedrock/pricing/`

---

## 4. Marco Regulatorio Colombiano (Diapositiva 58)
- **Ley Estatutaria 1581 de 2012**:
  - Régimen general de protección de datos personales en Colombia.
  - Artículo 26: Prohibición de transferencia internacional de datos personales a países sin niveles adecuados de seguridad.
  - Sanciones de la SIC: Multas de hasta 2.000 salarios mínimos legales mensuales vigentes (SMMLV).
  - *URL*: `https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=49981`
- **Circular Externa 007 de la Superintendencia Financiera de Colombia (SFC)**:
  - Requisitos de seguridad, gobernanza y gestión de riesgo operativo en cómputo en la nube para entidades vigiladas.
  - *URL*: `https://www.superfinanciera.gov.co/inicio/normativa/normativa-general/circulares-externas/circulares-externas-2018-10084534`

---

## 5. Casos Ilustrativos
- **Diapositivas 14, 29, 44**:
  - Rotuladas explícitamente: *"Caso ilustrativo de arquitectura, no es una empresa real"*.
  - Se eliminaron nombres ficticios ("Corporación Industrial del Caribe") y costos inventados en pesos colombianos.
  - Los cálculos muestran la metodología de dimensionamiento de hardware y fórmulas de cruce financiero basadas en tarifas reales de catálogo.
