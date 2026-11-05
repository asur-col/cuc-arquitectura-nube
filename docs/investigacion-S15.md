# Investigación Técnica — Semana 15: IA en la Nube II: GPU, Cuantización y Modelos Gestionados frente a Auto-Alojados

**Curso**: Arquitectura en la Nube (2026-2)  
**Institución**: Universidad de la Costa (CUC)  
**Profesor**: Ing. Rodolfo José Cañas Cervantes  
**Fecha de consulta**: 2026-11-04  

---

## 1. Arquitectura de Hardware, Aceleradores y Memoria para IA

### 1.1 Microarquitectura de GPUs de Centro de Datos y Tensor Cores
- **NVIDIA Hopper Architecture Whitepaper**:
  - URL: `https://resources.nvidia.com/en-us-tensor-core/gtc22-whitepaper-hopper`
  - *Detalles técnicos*: Arquitectura SXM5 con núcleos Tensor Core de 4.ª generación. Soporte nativo para formato Transformer Engine con precisión adaptativa FP8 (E4M3 y E5M2), duplicando el rendimiento respecto a FP16 con mínima degradación de precisión. Rendimiento de hasta 2,000 TFLOPS en FP8 Tensor Core.
- **Roofline Model para Modelos de Lenguaje**:
  - URL: `https://arxiv.org/abs/2009.06899`
  - *Detalles técnicos*: Clasificación de las fases de inferencia en LLMs: fase de prefill (procesamiento del prompt) compute-bound dominada por multiplicación matricial GEMM; fase de decode (generación autorregresiva token por token) memory-bound dominada por el ancho de banda de la memoria VRAM (GEMV de batch pequeño).
- **Memoria de Alto Ancho de Banda (HBM3 / HBM3e)**:
  - URL: `https://www.nvidia.com/en-us/data-center/h100/`
  - *Detalles técnicos*: H100 cuenta con 80 GB HBM3 entregando 3.35 TB/s de ancho de banda. Interconexión NVLink de 4.ª generación con 900 GB/s bidireccionales por GPU, superando el límite de 64 GB/s del bus PCIe 5.0 x16.

### 1.2 Familias Cloud de Instancias Aceleradas (AWS)
- **AWS EC2 Accelerated Computing Instances**:
  - URL: `https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/accelerated-computing-instances.html`
  - *Instancias p5.48xlarge*: 8x NVIDIA H100 (80GB HBM3 cada una, 640GB total), 192 vCPUs, 2048 GB RAM, 3200 Gbps de ancho de banda de red agregado mediante 32x Elastic Fabric Adapter (EFA) con libfabric GPUDirect RDMA.
  - *Instancias g5.12xlarge / g5.48xlarge*: NVIDIA A10G (24GB GDDR6), optimizadas para inferencia económica de modelos medianos (7B a 13B parámetros).
  - *Aceleradores propietarios*: AWS Inferentia2 (inf2) y Trainium (trn1), arquitectura NeuronCore optimizada para modelos Transformer.

---

## 2. Técnicas de Compresión, Cuantización y Optimización de Modelos

### 2.1 Requerimientos de Memoria VRAM para Inferencia
- **Fórmula de Memoria para LLMs**:
  - Memoria de pesos: \( M_{\text{pesos}} \approx P \times B \) bytes, donde \( P \) es el número de parámetros y \( B \) los bytes por parámetro (FP16: 2 bytes; INT8: 1 byte; INT4: 0.5 bytes).
  - Memoria de KV-Cache: \( M_{\text{KV}} = 2 \times L \times H_{\text{kv}} \times D \times B_{\text{kv}} \times S \times N \), donde \( L \) es número de capas, \( H_{\text{kv}} \) cabezas clave-valor, \( D \) dimensión por cabeza, \( S \) longitud de contexto y \( N \) batch size.

### 2.2 Algoritmos de Cuantización de Pesos
- **GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers**:
  - URL: `https://arxiv.org/abs/2210.17323`
  - *Mecanismo*: Basado en la matriz Hessiana inversa (segunda derivada del error) para compensar secuencialmente el error cuadrático en los pesos adyacentes al cuantizar a 4 bits.
- **AWQ: Activation-aware Weight Quantization**:
  - URL: `https://arxiv.org/abs/2306.00978`
  - *Mecanismo*: Observa que no todos los pesos son igualmente importantes; protege el 1% de pesos salientes que corresponden a activaciones de gran magnitud, cuantizando el 99% restante a 4 bits sin pérdida perceptible en benchmarks MMLU.
- **Formato GGUF y Llama.cpp**:
  - URL: `https://github.com/ggerganov/llama.cpp/blob/master/docs/gguf.md`
  - *Mecanismo*: Archivo unificado de metadatos y tensores alineados para ejecución en CPU con extensiones AVX-512/ARM Neon y descarga selectiva de capas a GPU (cuantizaciones k-quants: Q4_K_M, Q5_K_M).

---

## 3. Motores de Inferencia de Alto Rendimiento Auto-Alojados (Self-Hosted)

### 3.1 PagedAttention y Servidor vLLM
- **vLLM: Efficient Memory Management for Large Language Model Serving with PagedAttention**:
  - URL: `https://arxiv.org/abs/2309.06180`
  - URL Documentación: `https://docs.vllm.ai/en/latest/`
  - *Innovación*: Trata la memoria KV-Cache de las GPUs como la memoria virtual paginada de un sistema operativo, eliminando la fragmentación externa e interna (que desperdiciaba del 60% al 80% de VRAM en motores clásicos).
- **Continuous Batching (In-Flight Batching)**:
  - *Principio*: En lugar de esperar a que termine la generación de todas las secuencias de un batch estático para insertar nuevas peticiones, el scheduler itera a nivel de tokens, admitiendo nuevas solicitudes tan pronto como una secuencia alcanza el token de fin (`<eos>`).
- **Triton Inference Server y Hugging Face TGI**:
  - URL: `https://developer.nvidia.com/triton-inference-server`
  - URL: `https://huggingface.co/docs/text-generation-inference`
  - *Características*: Servidores optimizados para producción con métricas Prometheus nativas, paralelismo tensorial (Tensor Parallelism) con NCCL y compatibilidad con OpenAI API specs.

---

## 4. Servicios Gestionados frente a Auto-Alojados: Análisis TCO y Arquitectura

### 4.1 Panorama de Servicios Gestionados
- **AWS Bedrock Pricing**:
  - URL: `https://aws.amazon.com/bedrock/pricing/`
  - Facturación bajo demanda por millón de tokens de entrada y salida:
    - Claude 3.5 Sonnet: $3.00 / 1M tokens entrada; $15.00 / 1M tokens salida.
    - Claude 3 Haiku: $0.25 / 1M tokens entrada; $1.25 / 1M tokens salida.
    - Llama 3 70B en Bedrock: $0.72 / 1M tokens entrada; $0.72 / 1M tokens salida.
- **Costos de Instancias de GPU Dedicadas (AWS EC2 On-Demand)**:
  - g5.12xlarge (4x A10G, 96GB VRAM): ~$5.67 / hora (~$4,082 / mes continuo).
  - p4de.24xlarge (8x A100 80GB, 640GB VRAM): ~$40.96 / hora (~$29,491 / mes continuo).

### 4.2 Punto de Equilibrio Económico (Break-Even Analysis)
- Si una organización genera más de 50 millones de tokens diarios con un modelo de 70B parámetros, el costo en APIs gestionadas supera los $6,000 USD/mes, justificando económicamente el auto-alojamiento en una instancia de 4x A10G o en servidores físicos on-premise con GPUs L40S.
- Si el volumen es bajo (<5 millones de tokens/día) o impredecible con picos repentinos, el servicio gestionado Serverless minimiza el TCO evitando el desperdicio de horas de GPU ociosa.

---

## 5. Caso Ilustrativo de Negocio
- **Entidad**: Corporación Industrial del Caribe (Barranquilla) — Caso ilustrativo empresarial, no es una empresa real.
- **Escenario**: Plataforma de mantenimiento predictivo y asistente operativo para operadores de planta química en la zona industrial de Mamonal / Vía 40.
- **Decisión arquitectónica**:
  - Tareas operativas de planta y análisis de telemetría interna: Servidor local vLLM con modelo Llama 3 8B cuantizado en AWQ INT4 ejecutando sobre GPU NVIDIA RTX 6000 Ada en nodo de cómputo OpenStack propio (latencia < 20 ms, soberanía absoluta de datos).
  - Consultas ejecutivas complejas y síntesis de reportes regulatorios: Ruteo mediante AWS Bedrock con Claude 3.5 Sonnet vía VPC Endpoint con Zero Data Retention (ZDR).
