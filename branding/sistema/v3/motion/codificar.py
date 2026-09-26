"""Codifica los entregables de video de motion a partir de los renders.

    FFMPEG=/ruta/ffmpeg python3 codificar.py [filtro]

Entradas
  blender/render/<id>[.reducido]/[<clip>/]NNNN.png   secuencias PNG RGBA de Blender
  remotion/salida/masters/<id>.mov (+ .poster.png)   maestros ProRes 4444 de Remotion

Salidas en entregables/<id>/ (se ignoran en git, salvo lo liviano; ver README):
  blender  → <nombre>.master.mov (ProRes 4444 + alfa), <nombre>.hevc_app.mp4;
             con fondo transparente además <nombre>.alpha.webm (VP9) y <nombre>.alpha.mov (HEVC con alfa, hvc1)
  remotion → <id>.av1.webm, <id>.h264.mp4, <id>.poster.avif

Los comandos son los de Nico con dos ajustes: 60 fps (el sistema entero está a 60) y HEVC con alfa por libx265
(FFmpeg ≥ 7.1) en vez de hevc_videotoolbox, que solo existe en macOS. FFMPEG debe tener libx265 con yuva420p.
Las piezas en loop repiten el primer frame al final (regla del render); en web y app se quita esa repetición
para que el bucle no se trabe. El máster la conserva.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
FF = os.environ.get('FFMPEG', 'ffmpeg')
T = json.loads((AQUI / 'tokens.motion.json').read_text())['oscuro']
FPS = T['fps']
FONDO_APP = T['color']['superficie/abismo'].lstrip('#')
SALIDA = AQUI / 'entregables'
TRANSPARENTES = {'pase-3d-objeto', 'pase-3d-latir'}
EN_LOOP = {'pase-3d-latir', 'pase-3d-objeto/latir'}


def ff(*args):
    cmd = [FF, '-hide_banner', '-loglevel', 'error', '-y', *map(str, args)]
    print('·', ' '.join(cmd[4:])[:160])
    subprocess.run(cmd, check=True)


def secuencias():
    raiz = AQUI / 'blender' / 'render'
    for d in sorted(p for p in raiz.rglob('*') if p.is_dir()):
        pngs = sorted(d.glob('[0-9][0-9][0-9][0-9].png'))
        if pngs:
            yield d.relative_to(raiz), pngs


def blender(filtro):
    for rel, pngs in secuencias():
        partes = rel.parts
        base = partes[0]
        id_ = base.replace('.reducido', '')
        clip = partes[1] if len(partes) > 1 else ''
        nombre = base + (f'.{clip}' if clip else '')
        if filtro and filtro not in nombre:
            continue
        destino = SALIDA / id_
        destino.mkdir(parents=True, exist_ok=True)
        inicio = int(pngs[0].stem)
        n = len(pngs)
        patron = pngs[0].parent / '%04d.png'
        master = destino / f'{nombre}.master.mov'
        # Máster ProRes 4444 con alfa
        ff('-framerate', FPS, '-start_number', inicio, '-i', patron, '-c:v', 'prores_ks', '-profile:v', '4444',
           '-pix_fmt', 'yuva444p10le', master)
        loop = f'{id_}/{clip}' in EN_LOOP or (id_ in EN_LOOP and not clip)
        cuadros = ['-frames:v', n - 1] if loop and n > 1 else []
        # App: HEVC sobre superficie/abismo (la app no compone alfa)
        w, h = tamano(pngs[0])
        ff('-i', master, '-f', 'lavfi', '-i', f'color=c=0x{FONDO_APP}:s={w}x{h}:r={FPS}',
           '-filter_complex', '[1][0]overlay=shortest=1,format=yuv420p', *cuadros,
           '-c:v', 'libx265', '-crf', 22, '-tag:v', 'hvc1', '-movflags', '+faststart', destino / f'{nombre}.hevc_app.mp4')
        if id_ in TRANSPARENTES:
            # Web con transparencia (Chrome, Firefox, Edge)
            ff('-i', master, *cuadros, '-c:v', 'libvpx-vp9', '-pix_fmt', 'yuva420p', '-crf', 30, '-b:v', 0,
               destino / f'{nombre}.alpha.webm')
            # Web con transparencia (Safari): HEVC con capa alfa por libx265
            ff('-i', master, *cuadros, '-c:v', 'libx265', '-pix_fmt', 'yuva420p', '-crf', 24, '-tag:v', 'hvc1',
               '-movflags', '+faststart', destino / f'{nombre}.alpha.mov')


def remotion(filtro):
    for master in sorted((AQUI / 'remotion' / 'salida' / 'masters').glob('*.mov')):
        id_ = master.stem
        if filtro and filtro not in id_:
            continue
        destino = SALIDA / id_.replace('-reducido', '')
        destino.mkdir(parents=True, exist_ok=True)
        # Hero web: AV1 + respaldo H.264
        ff('-i', master, '-c:v', 'libsvtav1', '-crf', 35, '-pix_fmt', 'yuv420p', destino / f'{id_}.av1.webm')
        ff('-i', master, '-c:v', 'libx264', '-crf', 20, '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
           destino / f'{id_}.h264.mp4')
        poster = master.with_suffix('.poster.png')
        if poster.exists():
            ff('-i', poster, '-c:v', 'libaom-av1', '-still-picture', 1, '-crf', 28, '-pix_fmt', 'yuv420p',
               destino / f'{id_}.poster.avif')


def tamano(png):
    salida = subprocess.run([FF.replace('ffmpeg', 'ffprobe'), '-v', 'error', '-select_streams', 'v', '-show_entries',
                             'stream=width,height', '-of', 'csv=p=0', str(png)], capture_output=True, text=True, check=True)
    w, h = re.findall(r'\d+', salida.stdout)[:2]
    return int(w), int(h)


if __name__ == '__main__':
    filtro = sys.argv[1] if len(sys.argv) > 1 else ''
    blender(filtro)
    remotion(filtro)
