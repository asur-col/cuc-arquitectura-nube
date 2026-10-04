#!/usr/bin/env python3
"""Verifica una presentación semanal contra el estándar del curso.

Uso:
  python3 herramientas/verificar.py 2026-2-S09-....html            # reporte
  python3 herramientas/verificar.py archivo.html --capturas DIR     # + PNG por diapositiva y hoja de contacto

Revisa: 4 partes con portada, nº de diapositivas por parte, gráfico por diapositiva,
guion por diapositiva y duración estimada (~150 palabras/min), íconos inexistentes y
desbordes de contenido (render real con Chromium).
"""
import argparse, os, re, sys, html as H
from pathlib import Path

PPM = 150  # palabras por minuto de la voz sintética (aprox.)
REPO = Path(__file__).resolve().parent.parent


def texto(s):
    return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()


def analizar(path):
    src = Path(path).read_text(encoding='utf-8')
    body = src[src.find('<div id="stage">'):]
    secs = re.findall(r'<section class="slide([^"]*)"([^>]*)>(.*?)</section>', body, re.S)
    filas = []
    for i, (cls, attrs, inner) in enumerate(secs, 1):
        parte = re.search(r'data-parte="(\d)"', attrs)
        g = re.search(r'<aside class="guion">(.*?)</aside>', inner, re.S)
        sin_guion = re.sub(r'<aside class="guion">.*?</aside>', '', inner, flags=re.S)
        h = re.search(r'<h[12][^>]*>(.*?)</h[12]>', sin_guion, re.S)
        graf = len(re.findall(r'<svg|<img(?![^>]*logo)', sin_guion))
        filas.append(dict(n=i, cover='cover' in cls, parte=int(parte.group(1)) if parte else None,
                          titulo=texto(h.group(1)) if h else '?', graficos=graf,
                          palabras=len(texto(g.group(1)).split()) if g else 0))
    iconos = set(re.findall(r'href="(assets/iconos/[^"]+)"', src))
    faltan = [p for p in iconos if not (REPO / p).exists() and not (Path(os.environ.get('ICONOS_LIB', '/nonexistent')) / p.replace('assets/iconos/', '')).exists()]
    return filas, faltan


def reporte(path, filas, faltan):
    errores, avisos = [], []
    partes = {}
    for f in filas:
        partes.setdefault(f['parte'], []).append(f)
    if sorted(k for k in partes if k) != [1, 2, 3, 4]:
        errores.append(f"partes encontradas {sorted(k for k in partes if k)} — se esperan 1..4 (data-parte en cada section)")
    if None in partes:
        errores.append(f"{len(partes[None])} diapositivas sin data-parte")
    print(f"\n== {path}")
    total_min = 0
    for p in sorted(k for k in partes if k):
        fs = partes[p]
        cont = [f for f in fs if not f['cover']]
        conG = sum(1 for f in cont if f['graficos'])
        pal = sum(f['palabras'] for f in fs)
        mins = pal / PPM + len(fs) * 1.2 / 60  # + pausas entre diapositivas
        total_min += mins
        print(f"  Parte {p}: {len(fs)} diap. ({len(cont)} contenido, {conG} con gráfico) · guion {pal} palabras ≈ {mins:.1f} min")
        if not fs[0]['cover']:
            errores.append(f"Parte {p} no abre con portada (section class=\"slide cover\")")
        if len(cont) < 12:
            errores.append(f"Parte {p}: solo {len(cont)} diapositivas de contenido (mín. 12)")
        if cont and conG / len(cont) < 0.85:
            errores.append(f"Parte {p}: {conG}/{len(cont)} con gráfico (mín. 85%)")
        if not 12.5 <= mins <= 17.5:
            avisos.append(f"Parte {p}: duración estimada {mins:.1f} min (objetivo 13–17)")
    for f in filas:
        if f['palabras'] == 0:
            errores.append(f"Diap. {f['n']} '{f['titulo'][:40]}' sin guion")
        elif not f['cover'] and not 80 <= f['palabras'] <= 230:
            avisos.append(f"Diap. {f['n']} guion de {f['palabras']} palabras (rango 80–230)")
    for p in faltan:
        errores.append(f"ícono inexistente: {p}")
    print(f"  TOTAL: {len(filas)} diapositivas · ≈ {total_min:.0f} min de video")
    return errores, avisos


def render(path, capdir, filas):
    from playwright.sync_api import sync_playwright
    exe = '/opt/pw-browsers/chromium' if Path('/opt/pw-browsers/chromium').exists() else None
    problemas = []
    url = Path(path).resolve().as_uri()
    with sync_playwright() as pw:
        kw = {'executable_path': exe} if exe and Path(exe).is_file() else {}
        b = pw.chromium.launch(**kw)
        pg = b.new_page(viewport={'width': 1280, 'height': 720})
        pg.goto(url); pg.wait_for_timeout(800)
        n = pg.evaluate('document.querySelectorAll(".slide").length')
        if capdir:
            Path(capdir).mkdir(parents=True, exist_ok=True)
        for i in range(n):
            pg.evaluate(f'show({i})'); pg.wait_for_timeout(60)
            r = pg.evaluate('''() => {
              const s=document.querySelectorAll('.slide')[%d]; const sr=s.getBoundingClientRect();
              const foot=s.querySelector('.s-foot'); const lim=foot?foot.getBoundingClientRect().top:sr.bottom;
              let peor=0, quien='', fondo=0;
              s.querySelectorAll('.s-body *, .s-head *').forEach(e=>{ if(e.closest('.guion'))return;
                const b=e.getBoundingClientRect(); if(!b.width||!b.height) return;
                if(e.closest('.s-body')) fondo=Math.max(fondo,b.bottom);
                const d=Math.max(b.bottom-lim+2, b.right-sr.right+2);
                if(d>peor){peor=d; quien=e.tagName+'.'+e.className;} });
              const cover=s.classList.contains('cover');
              return {peor, quien, vacio: cover||!fondo ? 0 : lim-fondo};
            }''' % i)
            if r['peor'] > 4:
                problemas.append(f"Diap. {i+1}: contenido desborda {r['peor']:.0f}px ({r['quien'][:40]})")
            if r['vacio'] > 120:
                problemas.append(f"Diap. {i+1}: {r['vacio']:.0f}px vacíos bajo el contenido — el diagrama debe llenar el cuerpo")
            if capdir:
                pg.screenshot(path=f"{capdir}/{i+1:03d}.png")
        b.close()
    if capdir:
        from PIL import Image
        fs = sorted(Path(capdir).glob('[0-9][0-9][0-9].png'))
        c, w, h = 6, 320, 180
        m = Image.new('RGB', (c * w, ((len(fs) + c - 1) // c) * h), 'white')
        for k, f in enumerate(fs):
            im = Image.open(f).convert('RGB'); im.thumbnail((w, h)); m.paste(im, ((k % c) * w, (k // c) * h))
        m.save(f"{capdir}/hoja-contacto.png")
        print(f"  capturas en {capdir}/ (hoja-contacto.png)")
    return problemas


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('html', nargs='+')
    ap.add_argument('--capturas', help='directorio para PNG por diapositiva')
    ap.add_argument('--sin-render', action='store_true')
    a = ap.parse_args()
    malo = False
    for h in a.html:
        filas, faltan = analizar(h)
        err, av = reporte(h, filas, faltan)
        if not a.sin_render:
            err += render(h, a.capturas and (a.capturas if len(a.html) == 1 else f"{a.capturas}/{Path(h).stem}"), filas)
        for e in err: print('  ❌', e)
        for w in av: print('  ⚠️ ', w)
        if not err: print('  ✅ cumple el estándar')
        malo |= bool(err)
    sys.exit(1 if malo else 0)
