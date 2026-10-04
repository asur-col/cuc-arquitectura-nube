#!/usr/bin/env python3
"""Genera los 4 videos (uno por parte) de una semana: captura cada diapositiva,
sintetiza su guion (<aside class="guion">) con voz neuronal y arma el MP4 con ffmpeg.

Requisitos (una vez):
    pip install playwright edge-tts
    python -m playwright install chromium
    ffmpeg en el PATH

Uso:
    python3 herramientas/generar_videos.py 2026-2-S09-....html
    python3 herramientas/generar_videos.py 2026-2-S09-....html --partes 2,3 --voz es-CO-GonzaloNeural
    python3 herramientas/generar_videos.py X.html --motor piper --modelo-piper voz.onnx   # voz offline

Salida: videos/<nombre>-parte{1..4}.mp4 (1920x1080, 25 fps, AAC mono 24 kHz — mismo formato que los
videos ya publicados). Usa caché en .cache-video/ para no resintetizar audio sin cambios.
"""
import argparse, asyncio, hashlib, shutil, subprocess, sys
from pathlib import Path
from comun import diapositivas, lanzar_chromium, OCULTAR_UI, REPO

PAUSA = 0.9  # segundos de silencio al final de cada diapositiva


def sh(*cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def duracion(f):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


async def tts_edge(texto, voz, velocidad, out):
    import edge_tts
    await edge_tts.Communicate(texto, voz, rate=velocidad).save(str(out))


def tts(texto, out, a):
    if a.motor == 'edge':
        tmp = out.with_suffix('.mp3')
        asyncio.run(tts_edge(texto, a.voz, a.velocidad, tmp))
        sh('ffmpeg', '-y', '-i', str(tmp), '-ac', '1', '-ar', '24000', str(out)); tmp.unlink()
    else:
        p = subprocess.run([sys.executable, '-m', 'piper', '-m', a.modelo_piper, '-f', str(out)],
                           input=texto, text=True, capture_output=True)
        if p.returncode: raise RuntimeError(p.stderr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('html')
    ap.add_argument('--voz', default='es-CO-GonzaloNeural', help='voz de edge-tts (edge-tts --list-voices)')
    ap.add_argument('--velocidad', default='+0%', help='p. ej. +5%% o -5%%')
    ap.add_argument('--motor', choices=['edge', 'piper'], default='edge')
    ap.add_argument('--modelo-piper', help='ruta al .onnx de Piper (motor offline)')
    ap.add_argument('--partes', default='1,2,3,4')
    ap.add_argument('--salida', default=str(REPO / 'videos'))
    a = ap.parse_args()

    html = Path(a.html).resolve()
    ds = diapositivas(html)
    partes = [int(x) for x in a.partes.split(',')]
    cache = REPO / '.cache-video' / html.stem
    cache.mkdir(parents=True, exist_ok=True)

    # 1) capturas 1920x1080
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = lanzar_chromium(pw)
        pg = b.new_page(viewport={'width': 1280, 'height': 720}, device_scale_factor=1.5)
        pg.goto(html.as_uri()); pg.add_style_tag(content=OCULTAR_UI)
        pg.wait_for_load_state('networkidle'); pg.wait_for_timeout(600)
        for k, d in enumerate(ds):
            if d['parte'] in partes:
                pg.evaluate(f'show({k})'); pg.wait_for_timeout(120)
                pg.screenshot(path=str(cache / f"{d['n']:03d}.png"))
        b.close()

    # 2) audio por diapositiva + clip
    Path(a.salida).mkdir(parents=True, exist_ok=True)
    for p in partes:
        fs = [d for d in ds if d['parte'] == p]
        clips = []
        for d in fs:
            texto = d['guion'] or d['titulo'] or ' '
            hsh = hashlib.sha1(f"{a.motor}|{a.voz}|{a.velocidad}|{texto}".encode()).hexdigest()[:12]
            wav = cache / f"{d['n']:03d}-{hsh}.wav"
            if not wav.exists():
                print(f"  voz diap. {d['n']} …", flush=True)
                tts(texto, wav, a)
            dur = duracion(wav) + PAUSA
            clip = cache / f"{d['n']:03d}-{hsh}.mp4"
            if not clip.exists():
                sh('ffmpeg', '-y', '-loop', '1', '-framerate', '25', '-i', str(cache / f"{d['n']:03d}.png"),
                   '-i', str(wav), '-af', f'apad=pad_dur={PAUSA}', '-t', f'{dur:.3f}',
                   '-c:v', 'libx264', '-preset', 'medium', '-tune', 'stillimage', '-crf', '20', '-pix_fmt', 'yuv420p',
                   '-vf', 'scale=1920:1080', '-c:a', 'aac', '-b:a', '64k', '-ac', '1', '-ar', '24000', str(clip))
            clips.append(clip)
        lista = cache / f'parte{p}.txt'
        lista.write_text(''.join(f"file '{c}'\n" for c in clips))
        out = Path(a.salida) / f"{html.stem}-parte{p}.mp4"
        sh('ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', str(lista), '-c', 'copy', '-movflags', '+faststart', str(out))
        print(f"Parte {p} → {out}  ({duracion(out)/60:.1f} min)")


if __name__ == '__main__':
    if not shutil.which('ffmpeg'):
        sys.exit('Falta ffmpeg en el PATH')
    main()
