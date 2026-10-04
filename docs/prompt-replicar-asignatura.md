# Prompt para replicar este flujo en otra asignatura

Copia y pega en una sesión nueva de Claude Code abierta sobre el repo de la otra asignatura.
Reemplaza lo que está entre [corchetes].

---

Eres mi asistente para producir el material de la asignatura **[NOMBRE]** (Universidad de la Costa — CUC,
periodo [2026-2], Ing. Rodolfo Cañas Cervantes). El repo contiene las presentaciones por semana en HTML
(de ahí salen los PDF y los videos) y un `index.html` con el **calendario por semanas y fechas**: esos títulos
son oficiales y NO se cambian.

**Fase 1 — Análisis (entrega y espera mi aprobación):**
1. Analiza todo el repo: semanas publicadas, calendario, en qué semana vamos (compara con la fecha de hoy),
   conteo de diapositivas y de diapositivas con gráfico por semana, calidad visual y técnica.
2. Investiga el contenido temático de la asignatura contra referentes externos reconocidos
   ([certificación/curso de industria relevante, p. ej. AWS Academy / Cisco / Microsoft], ACM/IEEE CS2023,
   normas/estándares del área) y valida su calidad: alineación, brechas por semana, repeticiones, temas faltantes.
   Mantén los títulos del calendario; las mejoras van DENTRO de cada semana.
3. Anexa fuentes de gráficos, íconos, imágenes y notas con su licencia (qué se puede reutilizar y cómo citar).
4. Si te comparto presentaciones viejas (.pptx), extrae sus diagramas e ideas y mapea a qué semana aportan;
   los diagramas se **redibujan como SVG propio**, no se pegan imágenes con derechos.
5. Deja todo en `docs/` (analisis-tematico.md, fuentes-recursos.md) y un plan por oleadas.

**Fase 2 — Producción (cuando apruebe):**
- Estándar por semana: **1 hora = 4 partes de ~15 min** sobre la misma presentación (diapositiva divisoria
  "Parte X de 4" donde va cada corte de video), ~14 diapositivas de contenido por parte, casi todas con
  **gráfico/diagrama** (topologías, flujos, arquitecturas — me gustan mucho los gráficos de red),
  estilo institucional CUC (vino #A6192E / dorado #D4AF37), caso aplicado colombiano y cierre con el lab.
- Enfoque: concepto genérico de industria, ilustrado con ejemplos de cualquier proveedor/tecnología;
  la práctica se hace en [plataforma de labs].
- Cada diapositiva lleva su **guion de narración** (para video con voz sintética) y el guion marca los cortes.
- Mejora las semanas ya publicadas al estándar y crea las semanas restantes del calendario.
  Las semanas futuras quedan creadas pero **desactivadas** en `index.html` (sin enlace) hasta que yo las publique.
- Orquesta con subagentes (modelo Sonnet), uno por semana en paralelo; tú (modelo principal) auditas cada
  entrega: conteo de diapositivas/gráficos, capturas renderizadas sin desbordes, precisión técnica, duración.
- Genera PDF desde el HTML. Para videos: genéralos aquí si la red lo permite; si no, deja un script
  (`herramientas/`) que con un comando produzca los 4 MP4 por semana (captura de diapositivas + voz TTS + ffmpeg)
  y las instrucciones para correrlo en mi computador.
- Al final deja notas en `CLAUDE.md` (estándar, convenciones, cómo regenerar PDF/videos, estado por semana,
  pendientes) para que Claude local continúe. Commits por oleada en la rama de trabajo.
