# Investigación Técnica — Semana 16: IA en la Nube III: Capacidades de los Modelos y Repaso de la Unidad 3

**Curso**: Arquitectura en la Nube (2026-2)  
**Institución**: Universidad de la Costa (CUC)  
**Profesor**: Ing. Rodolfo José Cañas Cervantes  
**Fecha de consulta**: 2026-11-04  

---

## 1. Razonamiento Avanzado, Planificación y Modelos Reflexivos

### 1.1 Escalado del Cómputo en Tiempo de Prueba (Test-Time Compute Scaling)
- **DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning**:
  - URL: `https://arxiv.org/abs/2501.12948`
  - URL Repositorio: `https://github.com/deepseek-ai/DeepSeek-R1`
  - *Mecanismo técnico*: Uso de aprendizaje por refuerzo puro a gran escala (GRPO - Group Relative Policy Optimization) sin supervisión inicial humana previa (R1-Zero). El modelo aprende de forma autónoma a generar tokens de pensamiento (`<think> ... </think>`), reflexionar sobre pasos previos, detectar inconsistencias matemáticas y retroceder (backtracking) para explorar rutas alternativas de solución.
- **OpenAI o1 System Card & Competitive Reasoning Evaluation**:
  - URL: `https://openai.com/index/openai-o1-system-card/`
  - *Detalles de arquitectura*: Introducción de tokens de razonamiento ocultos generados antes de la respuesta final. A mayor asignación de cómputo en inferencia (tiempo de prueba), el rendimiento en problemas complejos de olimpiadas matemáticas (AIME) y programación competitiva (Codeforces) escala siguiendo una ley de potencias similar a la del preentrenamiento.

---

## 2. Programación, Generación de Código y Sandboxing en la Nube

### 2.1 Modelos Especializados en Código y Benchmarks Rigurosos
- **Evaluating Large Language Models Trained on Code (HumanEval Benchmark)**:
  - URL: `https://arxiv.org/abs/2107.03374`
  - *Métrica*: Pass@k evaluando la exactitud funcional de programas generados mediante pruebas unitarias deterministas.
- **SWE-bench: Can Language Models Resolve Real-World GitHub Issues?**:
  - URL: `https://www.swebench.com/`
  - URL Artículo: `https://arxiv.org/abs/2310.06770`
  - *Metodología*: Benchmark de referencia para agentes de ingeniería de software. Evalúa la capacidad de modelos como Claude 3.5 Sonnet para clonar repositorios completos de Python, reproducir fallos a partir de issues de GitHub, modificar código existente y aprobar suites de pruebas sin regresiones.
- **Anthropic Claude 3.5 Sonnet Architecture & Code Execution**:
  - URL: `https://www.anthropic.com/news/claude-3-5-sonnet`
  - Consulta: 2026-11. Desempeño líder en SWE-bench Verified y HumanEval con razonamiento paso a paso y formateo de parches estructurados unificados (diffs).

### 2.2 Entornos Aislados de Ejecución de Código (Cloud Sandboxing)
- **AWS Firecracker MicroVMs for Serverless Execution**:
  - URL: `https://firecracker-microvm.github.io/`
  - *Detalles técnicos*: Micro-máquinas virtuales basadas en KVM de Linux con tiempo de arranque de ~5 ms y consumo de memoria base de ~5 MB por instancia. Permite a las plataformas de nube ejecutar de forma segura código arbitrario generado por modelos de IA en contenedores efímeros con aislamiento estricto de red y CPU.

---

## 3. Delegación, Sistemas Agénticos y Protocolos de Comunicación

### 3.1 Model Context Protocol (MCP)
- **Anthropic Model Context Protocol (MCP) Specification**:
  - URL: `https://modelcontextprotocol.io/`
  - URL Especificación: `https://spec.modelcontextprotocol.io/specification/`
  - *Arquitectura*: Protocolo abierto estándar cliente-servidor basado en JSON-RPC 2.0 que conecta modelos de lenguaje con fuentes de datos externas, herramientas locales y APIs de negocio de manera segura y desacoplada. Define primitivas estandarizadas: Resources (datos legibles), Prompts (plantillas reutilizables) y Tools (funciones ejecutables con esquema JSON-Schema).
- **Patrón ReAct: Synergizing Reasoning and Acting in Language Models**:
  - URL: `https://arxiv.org/abs/2210.03629`
  - *Flujo operativo*: Bucle iterativo de tres pasos: Pensamiento (Thought), Acción (Action vía API o herramienta) y Observación (Observation del entorno), permitiendo al agente corregir su trayectoria en función de la respuesta real de los sistemas cloud.

### 3.2 Memoria en Agentes: Corto Plazo, Episódica y Semántica
- **Arquitectura de Memoria para Agentes Autónomos**:
  - *Memoria de trabajo (Working Memory)*: Ventana de contexto inmediata del modelo (KV-Cache activo).
  - *Memoria episódica*: Registro cronológico de interacciones previas persistido en almacenes semiestructurados (DynamoDB o S3).
  - *Memoria semántica*: Base de conocimientos vectorial con embeddings vectoriales almacenados en PostgreSQL con extensión `pgvector` en AWS RDS o Amazon OpenSearch Service.

### 3.3 Ventanas Masivas de Contexto vs RAG
- **Needle In A Haystack (NIAH) Benchmark & Gemini Long Context**:
  - URL: `https://arxiv.org/abs/2403.05530`
  - *Hallazgos*: Aunque modelos modernos admiten hasta 2 millones de tokens de contexto, la latencia de prefill y el costo de inferencia aumentan linealmente con el tamaño del contexto. La arquitectura híbrida óptima combina RAG vectorial para recuperar fragmentos relevantes de alta precisión y una ventana moderada (16k - 64k tokens) para la síntesis analítica.

---

## 4. Repaso de la Unidad 3: Infraestructura, Cómputo y Operación en la Nube

### 4.1 Nube Privada y Servicios Base (OpenStack)
- **OpenStack Architecture & Service Flow**:
  - Keystone (Identidad y Tokens Fernet), Nova (Cómputo e Hipervisores KVM), Glance (Registro de Imágenes qcow2/raw), Neutron (Redes OVN y túneles Geneve), Cinder (Almacenamiento en bloque con backend Ceph RBD).
  - Alta disponibilidad con clústeres Pacemaker, Corosync, Galera MySQL y RabbitMQ Quorum Queues.

### 4.2 Inferencia y Despliegue de IA en la Nube
- **GPUs y Aceleradores**: Tensor Cores, memoria HBM3, interconexión NVLink vs PCIe 5.0, modelos de Roofline (Prefill compute-bound vs Decode memory-bound).
- **Cuantización**: AWQ e INT4 para reducción del 75 % de VRAM sin degradación perceptual.
- **Motores Auto-Alojados**: vLLM y PagedAttention para eliminar la fragmentación de memoria KV-Cache.
- **Servicios Gestionados**: AWS Bedrock Serverless, VPC Endpoints con PrivateLink, garantías Zero Data Retention (ZDR) y cumplimiento de la Ley 1581 de Colombia.

---

## 5. Caso Ilustrativo de Negocio
- **Entidad**: Corporación Industrial del Caribe (Barranquilla) — Caso ilustrativo empresarial, no es una empresa real.
- **Escenario**: Sistema autónomo de supervisión de incidentes de planta y auditoría técnica de infraestructura cloud.
- **Implementación**:
  - Agente de diagnóstico ejecutando con Claude 3.5 Sonnet / o1 mediante protocolo MCP conectado a Prometheus y OpenStack Nova API.
  - Generación de scripts de remediación ejecutados en sandboxes aislados de Firecracker.
  - Memoria semántica persistida en clúster PostgreSQL `pgvector` local.
