# CLAUDE.md — Arquitectura en la Nube (CUC, 2026-2)

Repositorio del material del curso **Arquitectura en la Nube** — Ing. Rodolfo Cañas Cervantes, Universidad de la Costa (CUC),
Ingeniería de Sistemas. Sitio estático (GitHub Pages) cuya portada es `index.html`.

## Qué hay aquí
| Ruta | Contenido |
|---|---|
| `index.html` | Portada: tarjetas por semana + **calendario oficial** (títulos y fechas NO se cambian) |
| `2026-2-SNN-arquitectura-nube-<tema>.html` | **Fuente de verdad** de cada semana (de aquí salen PDF y videos) |
| `2026-2-SNN-….pdf` | PDF generado desde el HTML |
| `videos/2026-2-SNN-…-parte{1..4}.mp4` | 4 videos de ~15 min por semana (voz sintética) |
| `guiones/2026-2-SNN-….md` | Guion narrado por parte/diapositiva (exportado del HTML) |
| `docs/ESTANDAR-PRODUCCION.md` | **Estándar obligatorio** de cada presentación — léelo antes de editar una semana |
| `docs/analisis-tematico.md` | Validación del temario vs AWS Academy Cloud Architecting y SAA-C03; brechas por semana |
| `docs/fuentes-recursos.md` | Fuentes de íconos, diagramas y notas con licencias |
| `docs/prompt-replicar-asignatura.md` | Prompt para repetir este flujo en otra asignatura |
| `plantillas/semana-base.html` | Plantilla de semana (CSS, navegación, diagrama modelo) |
| `assets/iconos/` | Íconos AWS/Azure/GCP/K8s/OpenStack/on-prem (lista en `LISTA.txt`) |
| `herramientas/` | Scripts (abajo) |
| `proyectos/`, `laboratorios/` | Proyecto de aula Corte 1, guía SSH, labs complementarios Azure (OneDrive) |

## Estándar en una línea
1 hora por semana = **4 partes de ~15 min** (cada parte = 1 video; abre con portada "Parte N de 4", `data-parte="N"`),
~14 diapositivas por parte, ≥85 % con **diagrama SVG** que llena el cuerpo (al docente le gustan los gráficos de red),
`<aside class="guion">` con la narración en cada diapositiva, estilo CUC vino `#A6192E` / dorado `#D4AF37`,
enfoque **multi-nube** (concepto genérico ilustrado con cualquier proveedor; práctica en AWS Academy).

## Comandos
```bash
pip install playwright edge-tts && python -m playwright install chromium   # una vez (+ ffmpeg en el PATH)

python3 herramientas/verificar.py 2026-2-S09-*.html --capturas /tmp/cap   # valida estándar + capturas
python3 herramientas/exportar_guion.py 2026-2-S09-*.html                  # guiones/…md
python3 herramientas/generar_pdf.py 2026-2-S09-*.html                     # PDF
python3 herramientas/generar_videos.py 2026-2-S09-*.html                  # 4 MP4 en videos/ (voz es-CO-GonzaloNeural)
python3 herramientas/generar_videos.py X.html --voz es-MX-JorgeNeural --velocidad +5%   # otra voz / ritmo
python3 herramientas/publicar_semana.py 09                                # activa la tarjeta en index.html
```
- Videos: `generar_videos.py` usa **edge-tts** (requiere Internet normal; no funciona en la nube de Claude Code porque
  el proxy bloquea WebSocket). Alternativa offline: `--motor piper --modelo-piper voz.onnx`.
  Si el docente usaba otra voz para los videos anteriores, pasarla con `--voz` (listar: `edge-tts --list-voices | grep es-`).
- Caché de audio/clips en `.cache-video/` (ignorada por git): editar un guion solo resintetiza esa diapositiva.
- Publicar una semana = generar PDF + videos y luego `publicar_semana.py NN`, commit y push.

## Estado y plan para continuar
**Lee `NOTAS-PRODUCCION.md`**: estado por semana, pendientes (S01 y S16 incompletas en `borradores/`), datos a contrastar con las guías de AWS Academy y pasos para generar PDF/videos en local. Los videos NO se generan en la nube.

## Convenciones
- Commits en español, descriptivos ("Publica S09 …", "Corrige …").
- No cambiar títulos ni fechas del calendario. No publicar semanas futuras sin orden del docente.
- Diagramas: SVG propio; íconos oficiales sin modificar; fuente citada en el pie (`.s-foot .src`).
- Caso transversal: "Corporación Industrial del Caribe" (manufactura, Barranquilla).
