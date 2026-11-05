# Documento de Investigaci??n S14: Inteligencia Artificial en la Nube I ??? Modelos, Tokens e Inferencia

**Asignatura**: Arquitectura en la Nube  
**Semana**: 14 (Periodo 2026-2) ?? Unidad 3  
**Docente**: Ing. Rodolfo Jos?? Ca??as Cervantes  
**Fecha de consulta y elaboraci??n**: Noviembre 2026  
**Fuentes primarias**: Documentaci??n oficial de AWS, OpenInfra, NIST, Hugging Face, vLLM y proveedores de modelos fundacionales.

---

## 1. Contexto Acad??mico y Objetivos de la Semana
Dentro de la Unidad 3 de Arquitectura en la Nube ("Data Center virtualizado y nuevas cargas de trabajo"), las cargas de Inteligencia Artificial Generativa y Modelos de Lenguaje Grande (LLMs) representan la evoluci??n m??s disruptiva en consumo de c??mputo, memoria y red en la nube moderna.

El objetivo de esta sesi??n es desmitificar el funcionamiento de los modelos de IA desde la perspectiva de la **arquitectura de sistemas en la nube**:
1. Comprender la naturaleza probabil??stica y autorregresiva de los modelos fundacionales basados en Transformer.
2. Analizar el rol de los tokens como unidad m??nima de procesamiento, memoria y facturaci??n en la nube.
3. Desglosar el flujo de una petici??n de inferencia en la nube desde el cliente hasta la memoria de la GPU (VRAM) y el streaming de salida.
4. Comparar arquitect??nicamente las opciones de despliegue: APIs gestionadas (Serverless/PaaS como Amazon Bedrock), infraestructura de c??mputo con aceleradores (IaaS con GPUs en Amazon EC2) y ejecuci??n local/privada (Ollama/vLLM on-premise), analizando m??tricas de latencia, soberan??a de datos y TCO.

---

## 2. Parte 1: Modelos Fundacionales y Arquitectura Transformer

### 2.1 Qu?? es un Modelo de Lenguaje (LLM)
Un Modelo de Lenguaje Grande (LLM) es una red neuronal profunda con cientos de miles de millones de par??metros entrenada para modelar la distribuci??n de probabilidad de secuencias de texto. A diferencia del software determinista tradicional (basado en l??gica booleana y ramas de ejecuci??n condicional), un LLM opera mediante aproximaciones estad??sticas de alto orden.

- **Arquitectura can??nica**: La inmensa mayor??a de los LLMs contempor??neos (familias GPT, Llama, Claude, Mistral, Gemini) se basan en la arquitectura **Transformer** propuesta por Vaswani et al. (2017), espec??ficamente en su variante **Decoder-Only** (decodificador autorregresivo).
- **Proceso autorregresivo**: La generaci??n ocurre paso a paso (token por token). Dado un prompt de entrada $x_1, x_2, \dots, x_t$, el modelo calcula la distribuci??n de probabilidad condicional para el siguiente elemento:
  $$P(x_{t+1} \mid x_1, x_2, \dots, x_t)$$
- Una vez seleccionado el token $x_{t+1}$, este se concatena a la secuencia de entrada y el proceso se repite sucesivamente hasta emitir un token especial de finalizaci??n (`<|endoftext|>` o `EOS`).

### 2.2 Inferencia vs Entrenamiento
Desde la perspectiva de dise??o de infraestructura cloud, es imperativo separar ambas fases:
1. **Entrenamiento (Training / Pre-training)**:
   - Carga masivamente distribuida en miles de GPUs (clusters H100/A100 interconectados por redes de ultra-bajo retardo como InfiniBand o AWS EFA con RoCEv2).
   - Requiere c??lculo de gradientes, paso adelante (forward pass) y propagaci??n hacia atr??s (backward pass) para actualizar los pesos.
   - Demanda semanas o meses de ejecuci??n continua con un consumo energ??tico y de c??mputo extremo.
2. **Inferencia (Serving / Generation)**:
   - Es la carga operativa del d??a a d??a en producci??n.
   - Ejecuta ??nicamente el **forward pass**: los pesos del modelo son est??ticos y de s??lo lectura.
   - El cuello de botella principal no es la potencia bruta de c??lculo matem??tico (FLOPS), sino el **ancho de banda de memoria** (Memory Bandwidth) de la GPU para transferir gigabytes de pesos y la memoria din??mica del **KV Cache** (Key-Value Cache) para mantener el contexto de los usuarios concurrentes.

---

## 3. Parte 2: Tokens, Vocabulario y Ventana de Contexto (Context Window)

### 3.1 Tokenizaci??n y Vocabulario (BPE)
Los modelos no leen caracteres ni palabras completas en texto plano; procesan n??meros enteros (*token IDs*) correspondientes a fragmentos l??xicos indexados en un vocabulario prefijado.
- Algoritmo est??ndar: **Byte-Pair Encoding (BPE)**.
- Tama??o de vocabulario:
  - GPT-4 / GPT-4o: ~100.000 a ~200.000 tokens (tokenizadores `cl100k_base` y `o200k_base`).
  - Llama 3 / 3.1: 128.256 tokens.
- **Factor de conversi??n palabra-token**:
  - En ingl??s t??cnico, 1 palabra ??? 1.3 tokens (o 1.000 tokens ??? 750 palabras).
  - En espa??ol y lenguas romances, debido a la morfolog??a flexiva y a una menor representaci??n relativa en los corpus de entrenamiento hist??ricos, las palabras suelen dividirse en m??s subpalabras (morfemas, terminaciones). T??picamente 1 palabra en espa??ol equivale a entre 1.4 y 1.7 tokens, lo que influye directamente en el consumo de cuota y costos de facturaci??n.

### 3.2 La Ventana de Contexto (Context Window)
La ventana de contexto es el b??fer m??ximo de tokens (entrada + salida acumulada) que el mecanismo de autoatenci??n (*self-attention*) puede procesar en una sola interacci??n.
- Hist??rico: GPT-3 (2.048 tokens), GPT-3.5 (4.096 y 16.384 tokens).
- Est??ndar 2024???2026: Llama 3.1 (128k tokens), Claude 3.5 Sonnet (200k tokens), Gemini 1.5 Pro (hasta 2 millones de tokens).
- **Desaf??o computacional de la atenci??n**: En el Transformer original, la atenci??n completa escala con complejidad cuadr??tica $O(N^2)$ en memoria y tiempo respecto a la longitud de la secuencia $N$. Para permitir contextos de 128k+ tokens sin agotar la memoria VRAM de la GPU, los sistemas modernos emplean algoritmos de atenci??n optimizada como **FlashAttention-2/3**, t??cnicas de RoPE (Rotary Position Embeddings) extendidas y gesti??n eficiente del **KV Cache**.

### 3.3 Modelo de Costos por Mill??n de Tokens
A diferencia de los servidores web tradicionales facturados por vCPU/hora, las APIs gestionadas de IA cobran por volumen de tokens procesados:
- **Tokens de Entrada (Prompt / Contexto)**: Procesados en paralelo durante la fase de *prefill*. Menor coste computacional por token generado.
- **Tokens de Salida (Completion / Generaci??n)**: Generados secuencialmente uno por uno. Mayor retenci??n de GPU y consumo de ancho de banda; t??picamente entre 3x y 5x m??s costosos que los de entrada.
- Referencias de precios consultadas en proveedores l??deres (noviembre 2026):
  - Amazon Bedrock (Anthropic Claude 3.5 Sonnet): ~$3.00 USD / mill??n de tokens de entrada; ~$15.00 USD / mill??n de tokens de salida.
  - Amazon Bedrock (Meta Llama 3.1 70B): ~$0.72 USD / mill??n de tokens de entrada; ~$0.72 USD / mill??n de tokens de salida.
  - OpenAI GPT-4o: ~$2.50 USD / mill??n de entrada; ~$10.00 USD / mill??n de salida.

---

## 4. Parte 3: El Pipeline de Inferencia en la Nube y Flujo de Petici??n

### 4.1 Ciclo de Vida de una Petici??n de Inferencia Cloud
1. **Cliente / Aplicaci??n Web**: Emite una solicitud HTTP POST con cabecera `Authorization: Bearer <token>` y cuerpo JSON conteniendo mensajes del usuario, temperatura y par??metros de decodificaci??n.
2. **Capa Perimetral (API Gateway / Ingress ALB)**:
   - Terminaci??n TLS/HTTPS.
   - Autenticaci??n, control de identidad (IAM / API Keys) y aplicaci??n de cuotas de velocidad (*rate limiting* / *throttling*).
3. **Servidor de Inferencia / Motor de Ejecuci??n (vLLM / Triton / TGI)**:
   - **Tokenizador**: Convierte el string recibido en un tensor de enteros `input_ids`.
   - **Planificador de Lotes Din??micos (Continuous Batching)**: En lugar de procesar peticiones en lotes est??ticos que deben esperar a que la respuesta m??s larga termine, el motor intercala nuevos tokens de entrada con tokens de salida de m??ltiples peticiones en cada ciclo de c??mputo.
   - **PagedAttention / KV Cache**: Almacena en la memoria VRAM de la GPU las matrices de clave (*Key*) y valor (*Value*) de los tokens ya procesados, fragmentando la memoria en bloques paginados (an??logo a la memoria virtual de un sistema operativo) para eliminar la fragmentaci??n interna y desperdicio de memoria.
4. **Ejecuci??n en Hardware Acelerador (GPU / TPU / Trainium / Inferentia)**:
   - Realiza la multiplicaci??n de matrices (GEMM) a trav??s de n??cleos especializados (NVIDIA Tensor Cores).
   - Genera el vector de *logits* no normalizados sobre el vocabulario completo.
   - Aplica muestreo: Temperatura (control de entrop??a), Top-P (muestreo de n??cleo) o Top-K para seleccionar el siguiente token ID.
5. **Respuesta en Streaming (Server-Sent Events - SSE)**:
   - En lugar de retener la conexi??n TCP hasta que se generen los 500 o 1.000 tokens de la respuesta completa (lo que provocar??a una experiencia de usuario bloqueante y riesgo de timeout HTTP de 30 o 60 segundos), el servidor emite cada token conforme se des-tokeniza mediante el est??ndar SSE (`Content-Type: text/event-stream; data: {"chunk": "..."}`).

### 4.2 M??tricas de Rendimiento en Inferencia
- **TTFT (Time to First Token)**: Tiempo transcurrido entre el env??o del prompt y la recepci??n del primer token. Mide la eficiencia de la fase de *prefill* y la cola del planificador.
- **TPOT (Time per Output Token)** o **Inter-Token Latency**: Tiempo promedio para emitir cada token subsiguiente (t??picamente 20???40 ms por token para velocidades legibles de 25???50 tokens/segundo).
- **Throughput Total**: Cantidad total de tokens generados por segundo en el cluster o instancia GPU para soportar concurrencia masiva.

---

## 5. Parte 4: Arquitectura de Despliegue ??? Nube Gestionada vs Auto-alojada vs Local

### 5.1 Los Tres Enfoques Arquitect??nicos
| Criterio | A) API Gestionada (Serverless / PaaS)<br>*(ej. Amazon Bedrock, Azure OpenAI)* | B) Instancia GPU Dedicada (IaaS)<br>*(ej. Amazon EC2 G5/G6 + vLLM)* | C) Inferencia Local / Privada<br>*(ej. Servidor On-Premise / Ollama)* |
|---|---|---|---|
| **Modelo Operativo** | Cero gesti??n de infraestructura. Pago por token consumido. | Gesti??n del SO Linux, drivers NVIDIA, Docker y motor vLLM. | Gesti??n de hardware f??sico, climatizaci??n, energ??a y mantenimiento. |
| **Escalabilidad** | El??stica e instant??nea bajo demanda del proveedor. | Auto Scaling Groups de EC2 basados en longitud de cola y uso de GPU. | R??gida; acotada a las tarjetas gr??ficas f??sicas instaladas. |
| **Soberan??a y Privacidad** | Datos viajan al endpoint del proveedor (requiere acuerdos DPA/BAA). | Datos permanecen 100% dentro de la VPC y subred privada de la empresa. | Datos nunca abandonan las instalaciones f??sicas locales. |
| **Latencia de Red** | Depende de la regi??n del proveedor (Internet / Direct Connect). | Co-ubicada en la misma VPC de la base de datos y microservicios. | Latencia LAN ultra-baja (<2ms) dentro de la red corporativa. |
| **Modelos Soportados** | Modelos comerciales de vanguardia (Claude, Nova, GPT) + open-weights seleccionados. | Cualquier modelo de pesos abiertos (Llama 3, Mistral, Qwen, DeepSeek). | Modelos abiertos cuantizados a 4 u 8 bits (GGUF, AWQ, GPTQ). |

### 5.2 An??lisis de Punto de Equilibrio y Costos Reales (TCO)
- **Instancia EC2 g5.xlarge** (1 GPU NVIDIA A10G con 24 GB VRAM, 4 vCPUs, 16 GB RAM):
  - Costo bajo demanda en `us-east-1`: **\$1.0061 USD / hora**.
  - Operaci??n 24/7 mensual: $\$1.0061 \times 730\text{ horas} \approx \mathbf{\$734.45\text{ USD / mes}}$ (m??s almacenamiento EBS y transferencia de datos).
  - Con un modelo Llama 3.1 8B optimizado en vLLM, puede procesar en promedio ~100 tokens/segundo en concurrencia moderada.
- **Comparaci??n con API Gestionada**:
  - Si una aplicaci??n corporativa procesa 500.000 tokens al d??a en una API de nivel intermedio (\$3/MTok entrada, \$15/MTok salida; promedio ponderado ~$6/MTok):
    $$\text{Costo API} = 0.5\text{ MTok/d??a} \times 30\text{ d??as} \times \$6 = \mathbf{\$90.00\text{ USD / mes}}.$$
    En este volumen bajo, la API gestionada es inmensamente m??s econ??mica (\$90 vs \$734) y no genera sobrecarga de mantenimiento.
  - Si la demanda escala a **10 millones de tokens al d??a** (atenci??n masiva de clientes):
    $$\text{Costo API} = 10\text{ MTok/d??a} \times 30\text{ d??as} \times \$6 = \mathbf{\$1,800.00\text{ USD / mes}}.$$
    Aqu??, la instancia dedicada EC2 G5 (\$734/mes) ya representa un ahorro significativo de m??s del 50%, justificando la complejidad operativa.

### 5.3 Caso Transversal: Corporaci??n Industrial del Caribe
La *Corporaci??n Industrial del Caribe* (empresa de manufactura y distribuci??n en Barranquilla, caso de estudio transversal de la asignatura) eval??a la adopci??n de IA para dos cargas de trabajo:
1. **Asistente de Consulta de Pol??ticas Corporativas y N??mina (Uso Interno)**: Volumen bajo (~50 consultas diarias, ~200k tokens/d??a), pero con informaci??n altamente confidencial de empleados. Decisi??n arquitect??nica: API de Amazon Bedrock con VPC Endpoint privado (PrivateLink) y pol??ticas de exclusi??n de reentrenamiento, o modelo Llama 3.1 en servidor interno on-premise con Ollama.
2. **Clasificador Automatizado de ??rdenes de Pedido y Despacho**: Procesamiento continuo 24/7 de albaranes y facturas de transporte. Decisi??n arquitect??nica: Instancia EC2 con GPU en la misma VPC de su sistema ERP para garantizar latencias predecibles de sub-segundo sin depender de cuotas de APIs p??blicas externas.

---

## 6. Fuentes Primarias Verificadas y Enlaces Oficiales

1. **Amazon Web Services ??? Amazon Bedrock User Guide**:
   - URL: https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html
   - Contenido: Arquitectura serverless, integraci??n con VPC Endpoints (PrivateLink) y aislamiento de datos de clientes sin reentrenamiento.
2. **Amazon Web Services ??? EC2 G5 Instance Specifications & Pricing**:
   - URL: https://aws.amazon.com/ec2/instance-types/g5/
   - Contenido: Especificaciones t??cnicas de NVIDIA A10G Tensor Core GPU (24 GB GDDR6), PCIe Gen 4 y modelos de precios bajo demanda y Savings Plans.
3. **vLLM Documentation ??? PagedAttention & Continuous Batching**:
   - URL: https://docs.vllm.ai/en/latest/
   - Contenido: Algoritmo de PagedAttention para mitigaci??n de fragmentaci??n en memoria de KV Cache y arquitectura de inferencia de alto rendimiento.
4. **Hugging Face Transformers ??? Tokenizer & Summary Guide**:
   - URL: https://huggingface.co/docs/transformers/tokenizer_summary
   - Contenido: Explicaci??n de Byte-Pair Encoding (BPE), WordPiece y SentencePiece; gesti??n de vocabularios de subpalabras.
5. **NIST ??? Artificial Intelligence Risk Management Framework (AI RMF 1.0)**:
   - URL: https://www.nist.gov/itl/ai-risk-management-framework
   - Contenido: Principios de gobernanza, seguridad, privacidad y confiabilidad en sistemas de inteligencia artificial empresariales.
6. **OpenAI ??? Platform Tokenizer & Pricing Documentation**:
   - URL: https://platform.openai.com/tokenizer
   - Contenido: Funcionamiento de tiktoken y estructura de costos por mill??n de tokens.
7. **Anthropic ??? Claude Models & Pricing Overview**:
   - URL: https://docs.anthropic.com/en/docs/build-with-claude/token-counting
   - Contenido: Conteo de tokens, ventanas de contexto extendidas (200k) y separaci??n de precios de entrada vs salida.

