#!/usr/bin/env python3
"""Publica (o refresca) una semana en index.html.

Uso: python3 herramientas/publicar_semana.py 09        # activa la tarjeta pendiente de la semana 9
     python3 herramientas/publicar_semana.py 03        # semana ya publicada: rehace sus enlaces
                                                       # (p. ej. pasa de 1 video a 4 partes)

Enlaza HTML, PDF y los videos que EXISTAN en videos/ (<nombre>-parte1..4.mp4, o <nombre>.mp4).
Actualiza el contador "X de 15 publicadas".
"""
import re, sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sem = sys.argv[1].zfill(2)
idx = REPO / 'index.html'
s = idx.read_text(encoding='utf-8')

html = sorted(REPO.glob(f'2026-2-S{sem}-*.html'))
if not html:
    sys.exit(f'No existe 2026-2-S{sem}-*.html')
nombre = html[0].stem


def enlaces():
    L = [f'          <a class="go" href="{nombre}.html" target="_blank">Ver HTML →</a>']
    if (REPO / f'{nombre}.pdf').exists():
        L.append(f'          <a class="go" href="{nombre}.pdf" target="_blank">Ver PDF →</a>')
    partes = [p for p in range(1, 5) if (REPO / 'videos' / f'{nombre}-parte{p}.mp4').exists()]
    if partes:
        L += [f'          <a class="go" href="videos/{nombre}-parte{p}.mp4" target="_blank">Ver video Parte {p} →</a>' for p in partes]
    elif (REPO / 'videos' / f'{nombre}.mp4').exists():
        L.append(f'          <a class="go" href="videos/{nombre}.mp4" target="_blank">Ver video →</a>')
    return '        <div class="go-group">\n' + '\n'.join(L) + '\n        </div>'


# 1) tarjeta pendiente → publicada
pend = re.compile(r'      <!-- PENDIENTE:[^\n]*-->\n      <div class="week-card pending" data-semana="%s"[^>]*>(.*?)        <div class="go">Próximamente</div>\n      </div>\n' % sem, re.S)
m = pend.search(s)
if m:
    s = s[:m.start()] + '      <div class="week-card multi">' + m.group(1) + enlaces() + '\n      </div>\n' + s[m.end():]
    print(f'Semana {sem} publicada')
else:
    # 2) ya publicada → rehacer go-group
    g = re.compile(r'        <div class="go-group">\n(?:(?!</div>).)*?href="%s\.html".*?        </div>' % re.escape(nombre), re.S)
    if not g.search(s):
        sys.exit(f'No encontré la tarjeta de la semana {sem} en index.html')
    s = g.sub(enlaces(), s, count=1)
    print(f'Semana {sem}: enlaces actualizados')

n = len(re.findall(r'<div class="week-card multi">', s))
s = re.sub(r'<span class="count">\d+ de 15 publicadas</span>', f'<span class="count">{n} de 15 publicadas</span>', s)
idx.write_text(s, encoding='utf-8')
