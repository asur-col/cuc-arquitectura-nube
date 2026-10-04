"""Utilidades compartidas por las herramientas del curso."""
import re, html as H
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PPM = 150  # palabras por minuto aprox. de la voz sintética


def limpiar(s):
    return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()


def diapositivas(path):
    """Lista de dicts {n, parte, cover, titulo, guion} en el orden del HTML."""
    src = Path(path).read_text(encoding='utf-8')
    body = src[src.find('<div id="stage">'):]
    out = []
    for i, (cls, attrs, inner) in enumerate(
            re.findall(r'<section class="slide([^"]*)"([^>]*)>(.*?)</section>', body, re.S), 1):
        p = re.search(r'data-parte="(\d)"', attrs)
        g = re.search(r'<aside class="guion">(.*?)</aside>', inner, re.S)
        vis = re.sub(r'<aside class="guion">.*?</aside>', '', inner, flags=re.S)
        h = re.search(r'<h[12][^>]*>(.*?)</h[12]>', vis, re.S)
        out.append(dict(n=i, parte=int(p.group(1)) if p else 1, cover='cover' in cls,
                        titulo=limpiar(h.group(1)) if h else '', guion=limpiar(g.group(1)) if g else ''))
    return out


def lanzar_chromium(pw):
    exe = Path('/opt/pw-browsers/chromium')
    return pw.chromium.launch(executable_path=str(exe)) if exe.exists() else pw.chromium.launch()


OCULTAR_UI = '#nav,#progress{display:none!important} #stage{box-shadow:none!important;transform:none!important}'
