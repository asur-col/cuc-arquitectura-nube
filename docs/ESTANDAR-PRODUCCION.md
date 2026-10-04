# Estándar de producción — presentaciones semanales

Todo HTML semanal (`2026-2-SNN-arquitectura-nube-<tema>.html`, en la raíz del repo) cumple esto.
Plantilla: `plantillas/semana-base.html` (cópiala a la raíz con el nombre final; las rutas `assets/` son relativas a la raíz).

## 1. Estructura: 1 hora = 4 videos de ~15 min
- **4 partes**, cada una = un video. Cada `<section>` lleva `data-parte="1|2|3|4"`.
- Cada parte **abre con portada** (`<section class="slide cover" data-parte="N">`) con `<h1>` = subtema
  y `<h3>Parte N de 4 · Unidad U</h3>`. Solo la primera portada lleva además `active`.
- **13–14 diapositivas de contenido por parte** (≈ 56–60 en total con portadas).
- Pie: `Arquitectura en la Nube · Semana NN · Parte N de 4` y numeración **por parte** (`3 / 15`).
- Arco de cada parte: encuadre → desarrollo con diagramas → caso aplicado → cierre "Lo que queda de la Parte N".
- Parte 4 cierra la semana: caso integrador (Corporación Industrial del Caribe u otro colombiano),
  laboratorio de la semana si lo hay (calendario en `index.html`), "Semana NN en cuatro ideas" y adelanto de la próxima.

## 2. Gráficos (lo más importante)
- **≥ 85 % de las diapositivas de contenido con un diagrama SVG** (topología, flujo, arquitectura, línea de tiempo,
  comparación visual, gráfico de datos). Los diagramas de **red/arquitectura con íconos** son los preferidos.
- El diagrama **llena el cuerpo**: `<svg viewBox="0 0 1180 H" class="dgm">` con H ≈ 470–520 si va solo;
  si va con tarjetas/nota, ajusta para que no queden > 120 px vacíos sobre el pie. Nada se sale del área.
- Íconos: `<image href="assets/iconos/<proveedor>/<categoría>/<nombre>.png" .../>`. Lista completa en
  `assets/iconos/LISTA.txt` (AWS, Azure, GCP, Kubernetes, OpenStack, on-prem, genéricos). Usa solo rutas que existan.
  Los íconos no se recortan ni recolorean.
- Paleta: vino `#A6192E`, dorado `#D4AF37`, texto `#2A2A2A`, gris `#6b6b6b`/`#555`, tintes `#f9eef0`/`#fbf6e7`;
  para distinguir capas: verde subred pública `#eaf5ea/#3b8a3b`, azul subred privada `#eaf0fa/#2f5d9a`.
- Texto en SVG ≥ 11 px; títulos de cajas en negrita. Flechas con `<marker>` (ids únicos por diapositiva: `arrV9a`, etc.,
  para no chocar entre secciones).
- Cada diagrama tiene su **fuente** en `.s-foot .src` ("adaptado de …", ver `docs/fuentes-recursos.md`).
- **Enfoque multi-nube**: el concepto es genérico; ilustra con el proveedor que mejor lo explique (AWS, Azure, GCP,
  OpenStack). AWS es la plataforma de práctica: el concepto aterriza en su implementación AWS. Evita tablas largas de
  equivalencias de nombres entre proveedores.

## 3. Texto en pantalla
- Título = una idea (≤ 60 caracteres). Subtítulo = la conclusión en una línea.
- Poco texto: el detalle va en el guion. Máx. ~40 palabras visibles fuera del diagrama.
- Clases utilitarias disponibles: `.cols/.col`, `.card(.dark|.gold|.white)`, `.kpi .k`, `.note`, `.warn`, `.pill`,
  `.step`, `.lab-box`, `table.t`.

## 4. Guion de narración (video con voz sintética)
- Cada `<section>` (también portadas) lleva al final `<aside class="guion">…</aside>` (oculto en pantalla).
- **Contenido 120–180 palabras** (≈ 50–70 s); portada 50–90 palabras. Objetivo ≈ 2.000–2.300 palabras por parte ≈ 15 min.
- Estilo: clase hablada, español neutro con ejemplos colombianos, segunda persona ("fíjate en…"), recorre el diagrama
  en orden visual. Texto plano: sin viñetas, sin markdown, sin emojis, sin flechas ni símbolos raros; escribe
  "por ciento" en lugar de "%" cuando ayude a la lectura. Siglas en mayúscula (la voz las deletrea).
- La portada de cada parte presenta el subtema; la última diapositiva de cada parte cierra y anuncia la siguiente
  (eso marca el corte de video).

## 5. Precisión técnica
- Conceptos y nombres de servicios vigentes (2026). Nada inventado: si un dato es incierto, no lo pongas.
- Números de ejemplo coherentes (CIDR válidos, puertos correctos, precios marcados como "ilustrativos").

## 6. Verificación obligatoria antes de entregar
```bash
python3 herramientas/verificar.py ARCHIVO.html --capturas /tmp/cap-SNN
```
Debe terminar en "✅ cumple el estándar". Además mira `hoja-contacto.png` y varias capturas individuales.
Luego: `python3 herramientas/exportar_guion.py ARCHIVO.html` (crea `guiones/ARCHIVO.md`).

## 7. Herramientas
| Script | Qué hace |
|---|---|
| `herramientas/verificar.py` | Valida estructura, gráficos, guion, duración, íconos, desbordes y espacio vacío; capturas |
| `herramientas/exportar_guion.py` | Guion legible por partes en `guiones/` |
| `herramientas/generar_pdf.py` | PDF 1 diapositiva/página |
| `herramientas/generar_videos.py` | 4 MP4 por semana (capturas + voz edge-tts + ffmpeg) |
