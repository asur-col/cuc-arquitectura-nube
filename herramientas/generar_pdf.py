#!/usr/bin/env python3
"""Genera el PDF (una diapositiva por página, 1280x720) a partir del HTML de la semana.

Uso: python3 herramientas/generar_pdf.py 2026-2-S09-....html [otro.html ...]
Salida: mismo nombre con extensión .pdf, junto al HTML.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from comun import lanzar_chromium, OCULTAR_UI

with sync_playwright() as pw:
    b = lanzar_chromium(pw)
    for h in sys.argv[1:]:
        pg = b.new_page(viewport={'width': 1280, 'height': 720})
        pg.goto(Path(h).resolve().as_uri())
        pg.add_style_tag(content=OCULTAR_UI)
        pg.wait_for_load_state('networkidle'); pg.wait_for_timeout(500)
        pg.emulate_media(media='print')
        out = Path(h).with_suffix('.pdf')
        pg.pdf(path=str(out), width='1280px', height='720px', print_background=True,
               margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'})
        print('PDF →', out)
        pg.close()
    b.close()
