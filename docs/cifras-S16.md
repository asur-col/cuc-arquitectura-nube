# Cifras y Fuentes Verificadas — Semana 16
Fecha de consulta: 04 de noviembre de 2026

## 1. Modelos de Razonamiento y Pruebas en Repositorios
- **SWE-bench Verified (Tasa de Resolución de Incidencias en Repositorios Reales)**:
  - Agentes avanzados con Claude 3.5 Sonnet / OpenAI o1: 40% a 55% de incidencias resueltas.
  - Tasa de benchmarks tradicionales sintéticos (HumanEval/MBPP): >90% (benchmark saturado).
  - Fuente: Princeton NLP SWE-bench Leaderboard y Paper oficial.
  - URL: https://www.swebench.com/
  - Fecha de consulta: 04 de noviembre de 2026

- **Firecracker MicroVM**:
  - Tiempo de arranque por microVM: < 10 ms (típicamente 5 ms).
  - Huella de memoria por instancia: ~5 MB.
  - Reducción de dispositivos y superficie de ataque frente a QEMU: >95%.
  - Fuente: AWS Open Source Firecracker Whitepaper y GitHub.
  - URL: https://firecracker-microvm.github.io/
  - Fecha de consulta: 04 de noviembre de 2026

## 2. Protocolo Model Context Protocol (MCP)
- **Especificación de MCP**:
  - Protocolo: JSON-RPC 2.0 estandarizado.
  - Primitivas del servidor: Resources (recursos pasivos), Tools (herramientas ejecutables), Prompts (plantillas).
  - Transportes estándar: STDIO (subproceso local seguro) y SSE (Server-Sent Events con HTTP POST para nube).
  - Fuente: Model Context Protocol Specification — Anthropic.
  - URL: https://modelcontextprotocol.io/
  - Fecha de consulta: 04 de noviembre de 2026

## 3. Infraestructura y Aceleración (Repaso Unidad 3)
- **NVIDIA H100 SXM**:
  - Memoria: 80 GB HBM3.
  - Ancho de banda de memoria: 3.35 TB/s.
  - Interconexión NVLink 4: 900 GB/s bidireccionales.
  - Fuente: NVIDIA H100 Architecture Whitepaper.
  - URL: https://www.nvidia.com/en-us/data-center/h100/
  - Fecha de consulta: 04 de noviembre de 2026

- **vLLM y PagedAttention**:
  - Desperdicio por fragmentación de KV Cache: < 4% (frente a 60%-80% en servidores tradicionales).
  - Incremento de rendimiento concurrente por GPU: 2x a 4x con batching continuo.
  - Fuente: Kwon et al., SOSP 2023.
  - URL: https://vllm.ai/
  - Fecha de consulta: 04 de noviembre de 2026

- **AWQ (Activation-aware Weight Quantization)**:
  - Porcentaje de pesos críticos salientes protegidos: ~1%.
  - Cuantización: Pesos a 4 bits (INT4), activaciones en FP16.
  - Reducción de VRAM: ~3x frente a FP16 (modelo 70B pasa de ~140 GB a ~40 GB).
  - Fuente: Lin et al., MLSys 2024.
  - URL: https://arxiv.org/abs/2306.00978
  - Fecha de consulta: 04 de noviembre de 2026

## 4. Tarifas Oficiales Amazon Bedrock (US-East N. Virginia)
- **Amazon Nova Micro**: $0.035 / 1M entrada, $0.140 / 1M salida.
- **Amazon Nova Lite**: $0.060 / 1M entrada, $0.240 / 1M salida.
- **Claude Haiku 5.5 (Activo)**: $0.100 / 1M entrada, $0.500 / 1M salida.
- **Claude Sonnet 5.5 (Activo)**: $2.000 / 1M entrada, $10.000 / 1M salida.
- **Claude 3.5 Sonnet (Histórico / Legacy)**: $3.000 / 1M entrada, $15.000 / 1M salida (Legacy 10-oct-2026, EOL 13-nov-2026).
- **Prompt Caching**: 90% de descuento en tokens leídos de caché ($0.20 / 1M en Claude Sonnet 5.5).
- Fuente: AWS Bedrock Official Pricing Page.
- URL: https://aws.amazon.com/bedrock/pricing/
- Fecha de consulta: 04 de noviembre de 2026

## 5. Marco Regulatorio Colombiano
- **Ley Estatutaria 1581 de 2012**:
  - Régimen General de Protección de Datos Personales en Colombia.
  - Principios rectores: Finalidad, Libertad, Seguridad, Confidencialidad.
  - Requisitos de transferencia internacional: Países con nivel adecuado o contrato de transmisión de datos (DPA).
  - Fuente: Superintendencia de Industria y Comercio (SIC).
  - URL: https://www.sic.gov.co/proteccion-de-datos-personales
  - Fecha de consulta: 04 de noviembre de 2026
