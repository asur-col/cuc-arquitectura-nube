#!/usr/bin/env python3
"""Exporta el guion de narración de una semana a guiones/<nombre>.md (lectura humana, cortes de video).

Uso: python3 herramientas/exportar_guion.py 2026-2-S09-....html [otro.html ...]
"""
import sys
from pathlib import Path
from comun import diapositivas, PPM, REPO

for h in sys.argv[1:]:
    ds = diapositivas(h)
    stem = Path(h).stem
    L = [f"# Guion — {stem}", "",
         "Texto que narra la voz sintética, diapositiva por diapositiva. Cada **Parte** es un video",
         "independiente (corte de video). Duración estimada a ~%d palabras/min." % PPM, ""]
    total = 0
    for p in sorted({d['parte'] for d in ds}):
        fs = [d for d in ds if d['parte'] == p]
        mins = sum(len(d['guion'].split()) for d in fs) / PPM
        total += mins
        L += [f"## ✂️ Parte {p} de 4 — video `videos/{stem}-parte{p}.mp4` (≈ {mins:.1f} min)", ""]
        for d in fs:
            seg = len(d['guion'].split()) / PPM * 60
            L += [f"### Diap. {d['n']} · {d['titulo'] or '(portada)'}  _(≈ {seg:.0f} s)_", "", d['guion'] or '_(sin guion)_', ""]
    L.insert(4, f"**Duración total estimada: {total:.0f} min**\n")
    out = REPO / 'guiones' / f"{stem}.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text('\n'.join(L), encoding='utf-8')
    print('Guion →', out.relative_to(REPO), f'({total:.0f} min)')
