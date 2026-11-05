# Respaldo de Cifras Técnicas: Semana 14 · IA en la Nube I

Este documento audita y respalda cada número, tarifa y cifra técnica visible en las diapositivas y guiones de la Semana 14.
Las tarifas corresponden a precios oficiales publicados por Amazon Web Services (consultados en noviembre de 2026) o metodologías de dimensionamiento algebraico rotuladas formalmente como ejemplos pedagógicos.

---

## 1. Tarifas Oficiales de Amazon Bedrock (Noviembre 2026)
- **Precios por 1 Millón de Tokens Bajo Demanda (US East N. Virginia)**:
  - *Fuente oficial*: AWS Amazon Bedrock Pricing
  - *URL*: https://aws.amazon.com/bedrock/pricing/
  - *Fecha de consulta*: Noviembre de 2026
  - *Cifras oficiales verificadas*:
    - **Amazon Nova Micro**: Entrada \$0.035 USD / Salida \$0.140 USD (Diapositiva 26).
    - **Amazon Nova Lite**: Entrada \$0.060 USD / Salida \$0.240 USD (Diapositiva 26).
    - **Amazon Nova Pro**: Entrada \$0.800 USD / Salida \$3.200 USD (Diapositiva 26).
    - **Anthropic Claude 3.5 Haiku**: Entrada \$0.800 USD / Salida \$4.000 USD (Diapositiva 26).
    - **Anthropic Claude 3.5 Sonnet**: Entrada \$3.000 USD / Salida \$15.000 USD (Diapositiva 26).
    - **Anthropic Claude 3 Haiku (modelo histórico)**: Entrada \$0.250 USD / Salida \$1.250 USD (Diapositiva 26).
- **Descuentos Oficiales en Bedrock**:
  - **Prompt Caching (90 % de descuento en lectura de caché)**: En Claude 3.5 Sonnet, la lectura de tokens cacheados cuesta \$0.300 USD por millón (frente a \$3.00 USD estándar).
    - *URL*: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-cache.html
  - **Batch Inference (50 % de descuento)**: Procesamiento asíncrono por lotes con 50% de reducción en tokens de entrada y salida.
    - *URL*: https://docs.aws.amazon.com/bedrock/latest/userguide/batch-inference.html

---

## 2. Parámetros Técnicos de Hardware y Memoria VRAM
- **2 bytes por parámetro en precisión FP16 / BF16** (Diapositiva 12):
  - *Fuente*: NVIDIA Deep Learning Performance Documentation
  - *URL*: https://docs.nvidia.com/deeplearning/performance/dl-performance-gpu-background/index.html
  - *Comprobación*: FP16 utiliza 16 bits = 2 bytes por peso sináptico estático.
- **Memoria VRAM de Instancias EC2 G5 (NVIDIA A10G 24GB)** (Diapositivas 12, 50):
  - *Fuente*: AWS EC2 G5 Instance Specifications
  - *URL*: https://aws.amazon.com/ec2/instance-types/g5/
  - *Comprobación*: Instancia `g5.xlarge` dispone de 1 GPU NVIDIA A10G con 24 GB de memoria VRAM y 4 vCPUs.
  - *Tarifa de referencia*: ~$1.00 USD/hora bajo demanda (~$730 USD/mes continuo): https://aws.amazon.com/ec2/pricing/on-demand/

---

## 3. Ventanas de Contexto y Vocabularios de Modelos
- **Vocabularios BPE**:
  - Llama 2: 32.000 tokens (Diapositiva 20): https://llama.meta.com/
  - Llama 3: 128.256 tokens (~128k) (Diapositiva 20): https://llama.meta.com/docs/model-cards-and-prompt-formats/meta-llama-3/
  - Claude 3.5 Sonnet: > 150.000 tokens (Diapositiva 20): https://docs.anthropic.com/en/docs/about-claude/models
- **Ventanas de Contexto**:
  - 2.048 tokens (GPT-3, 2020) (Diapositiva 22): https://arxiv.org/abs/2005.14165
  - 8k - 32k tokens (2023) (Diapositiva 22): https://arxiv.org/abs/2307.09288
  - 128k - 200k tokens (Claude 3.5 / Llama 3, 2024-2026) (Diapositiva 22): https://aws.amazon.com/bedrock/
  - 1M - 2M+ tokens (Modelos Long-Context 2026) (Diapositiva 22): https://aws.amazon.com/bedrock/

---

## 4. Ejemplos Pedagógicos y Metodología FinOps (Sin Cifras Inventadas)
- **Simulación FinOps de 50.000 peticiones mensuales** (Diapositiva 27):
  - *Estado*: Rotulado formalmente como *"Ejemplo para el cálculo, no es tarifa real"*.
  - *Desglose metodológico*: 50M tokens de entrada + 15M tokens de salida; cálculo explícito con tarifas oficiales de Nova Pro (\$88.00 USD/mes) frente a Claude 3.5 Sonnet (\$375.00 USD/mes).
- **Punto de Equilibrio Servidor Dedicado vs API Serverless** (Diapositiva 54):
  - *Estado*: Rotulado formalmente como *"Ejemplo para el cálculo, no es tarifa real"*.
  - *Fórmula*: \( \text{Tokens de Cruce} = \frac{\text{Costo Fijo Mensual GPU (\$730)}}{\text{Costo Mixto por Token API}} \).
- **Topología Híbrida de Referencia** (Diapositiva 56):
  - *Estado*: Rotulado formalmente como *"Caso ilustrativo de arquitectura, no es una empresa real"*.
