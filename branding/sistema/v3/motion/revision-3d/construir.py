"""Lámina de revisión de las escenas 3D (versión 2 frente a la versión 1).

    ../blender/.venv/bin/python construir.py        # necesita Pillow y los renders de ../blender/render

Escribe revision-3d/lamina.html (imágenes incrustadas como JPEG) y copia a revision-3d/archivos/ los videos cortos que
la lámina reproduce. Colores y tipos: tokens de Kino (tema oscuro). Todo el texto visible está en TEXTO y en las tablas.
"""
import base64
import html
import io
import json
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

AQUI = Path(__file__).resolve().parent
MOTION = AQUI.parent
BL = MOTION / 'blender'
V1 = BL / '_obsoleto/v1-2026-09-26/verificacion'
R = BL / 'render'
T = json.loads((MOTION / 'tokens.motion.json').read_text())['oscuro']
C = T['color']
sys.path.insert(0, str(BL))
import bpy  # noqa: E402,F401  (bmesh, que usa pase.py, solo existe tras importar bpy)


def jpeg(ruta, fondo=None, ancho=1280, recorte=None):
    im = Image.open(ruta).convert('RGBA')
    if recorte:
        w, h = im.size
        im = im.crop(tuple(int(v * s) for v, s in zip(recorte, (w, h, w, h))))
    base = Image.new('RGBA', im.size, fondo or C['superficie/base'])
    im = Image.alpha_composite(base, im).convert('RGB')
    if im.width > ancho:
        im = im.resize((ancho, round(im.height * ancho / im.width)), Image.LANCZOS)
    b = io.BytesIO()
    im.save(b, 'JPEG', quality=84, optimize=True, progressive=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()


def cuadro(id_, clip, f):
    return R / id_ / clip / f'{f:04d}.png' if clip else R / id_ / f'{f:04d}.png'


def comparador(antes, despues, alt, ratio='16 / 9'):
    return (f'<div class="comparador" style="--r:{ratio}"><img src="{antes}" alt="Versión 1: {html.escape(alt)}">'
            f'<div class="despues"><img src="{despues}" alt="Versión 2: {html.escape(alt)}"></div>'
            f'<input type="range" min="0" max="100" value="50" aria-label="Deslizar entre versión 1 y versión 2: {html.escape(alt)}">'
            '<span class="rot izq">Versión 1</span><span class="rot der">Versión 2</span></div>')


def tabla(cabeza, filas, clase=''):
    th = ''.join(f'<th scope="col">{h}</th>' for h in cabeza)
    tr = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in f) + '</tr>' for f in filas)
    return f'<div class="tabla {clase}"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def tiempos():
    filas, total_s, total_f = [], 0.0, 0
    nombres = {'pase-3d-objeto': 'Pase 3D, 7 clips', 'pase-3d-latir': 'Pase en reposo',
               'conjunto-noche-lector-confirma': 'Portería de noche'}
    for id_ in nombres:
        for red in ('', '.reducido'):
            ruta = BL / 'tiempos' / f'{id_}{red}.json'
            if not ruta.exists():
                continue
            d = json.loads(ruta.read_text())
            frames = sum(v['frames'] for v in d.values())
            calc = sum(v.get('calculados', v['frames']) for v in d.values())
            seg = sum(v['segundos'] for v in d.values())
            v0 = next(iter(d.values()))
            total_s += seg
            total_f += calc
            filas.append([nombres[id_] + (' · reducido' if red else ''), f'{v0["resolucion"][0]} × {v0["resolucion"][1]}',
                          str(v0['muestras']), f'{frames}', f'{calc}', f'{seg / max(calc, 1):.1f} s', f'{seg / 60:.0f} min'])
    return filas, total_s, total_f


def _noche(f):
    red = R / f'conjunto-noche-lector-confirma.reducido/{f:04d}.png'
    return red if red.exists() else R / f'conjunto-noche-lector-confirma/{f:04d}.png'


def medir():
    import medir as m
    casos = [
        ('Pase vigente (latir, frame 55)', R / 'pase-3d-latir/0055.png',
         ['estado/vigente/borde', 'estado/vigente/texto', 'estado/vigente/fondo', 'texto/primario', 'texto/secundario']),
        ('Pase sin confirmar (aparecer, último frame)', cuadro('pase-3d-objeto', 'aparecer', 50),
         ['estado/sin-confirmar/borde', 'estado/sin-confirmar/texto', 'texto/primario']),
        ('Pase por vencer (avisar, último frame)', None, ['estado/por-vencer/borde', 'estado/por-vencer/texto', 'estado/por-vencer/fondo']),
        ('Portería reducida: indicador antes de la lectura', _noche(100), ['estado/sin-confirmar/borde']),
        ('Portería reducida: indicador confirmado', _noche(200), ['estado/vigente/borde']),
    ]
    import pase
    s, f = pase.rango('avisar')
    casos[2] = (casos[2][0], cuadro('pase-3d-objeto', 'avisar', f), casos[2][2])
    filas, crudo = [], {}
    for nombre, ruta, toks in casos:
        if not ruta or not Path(ruta).exists():
            continue
        res = m.medir(ruta, toks)
        crudo[nombre] = res
        for t, r in res.items():
            filas.append([nombre, f'<code>{t}</code>', f'<span class="muestra" style="background:{r["hex"]}"></span><code>{r["hex"]}</code>',
                          f'{r["pixeles_exactos"]:,}'.replace(',', '.'), f'{r["delta_e_min"]}',
                          '<b class="si">exacto</b>' if r['exacto'] else '<b class="no">no</b>'])
    (AQUI / 'mediciones.json').write_text(json.dumps(crudo, ensure_ascii=False, indent=1) + '\n')
    return filas


def videos():
    """Videos cortos para la lámina (H.264 sobre superficie/base): la portería y el Pase que se confirma."""
    ff = shutil.which('ffmpeg') or str(next(Path('/tmp').glob('**/ffmpeg-master-latest-linux64-gpl/bin/ffmpeg'), 'ffmpeg'))
    destino = AQUI / 'archivos'
    destino.mkdir(exist_ok=True)
    out = {}
    fondo = C['superficie/base'].lstrip('#')
    for nombre, carpeta, ancho in (('porteria', R / 'conjunto-noche-lector-confirma', 1280),
                                  ('porteria-reducido', R / 'conjunto-noche-lector-confirma.reducido', 1280),
                                  ('pase-confirmar', R / 'pase-3d-objeto/confirmar', 1280)):
        pngs = sorted(carpeta.glob('[0-9][0-9][0-9][0-9].png'))
        if not pngs:
            continue
        mp4 = destino / f'{nombre}.mp4'
        alto = ancho * 9 // 16
        subprocess.run([ff, '-hide_banner', '-loglevel', 'error', '-y', '-f', 'lavfi', '-i', f'color=c=0x{fondo}:s={ancho}x{alto}:r=60',
                        '-framerate', '60', '-start_number', pngs[0].stem, '-i', str(carpeta / '%04d.png'),
                        '-filter_complex', f'[1]scale={ancho}:-2[v];[0][v]overlay=shortest=1,format=yuv420p',
                        '-c:v', 'libx264', '-crf', '22', '-movflags', '+faststart', str(mp4)], check=True)
        out[nombre] = f'archivos/{nombre}.mp4'
    return out


def main():
    import pase
    ini = pase.inicios()
    fin = {c: pase.rango(c)[1] for c in pase.CLIPS}
    rec = (0.14, 0.2, 0.86, 0.8)
    # Antes y después: los mismos momentos de cada escena.
    comp_pase = [
        ('Aparecer (sin confirmar)', V1 / 'pase-3d-objeto/aparecer-f0050.png', cuadro('pase-3d-objeto', 'aparecer', fin['aparecer'])),
        ('Confirmar (vigente)', V1 / 'pase-3d-objeto/confirmar-f0109.png', cuadro('pase-3d-objeto', 'confirmar', fin['confirmar'])),
        ('Revocar', V1 / 'pase-3d-objeto/revocar-f0314.png', cuadro('pase-3d-objeto', 'revocar', fin['revocar'])),
    ]
    comp = ''.join(comparador(jpeg(a, recorte=rec), jpeg(b, recorte=rec), t, '43 / 27') + f'<p class="pie">{t}</p>'
                   for t, a, b in comp_pase if Path(a).exists() and Path(b).exists())
    latir = comparador(jpeg(V1 / 'pase-3d-latir/f0055.png', ancho=900), jpeg(R / 'pase-3d-latir/0055.png', ancho=900), 'Pase en reposo', '1 / 1')
    noche = comparador(jpeg(V1 / 'conjunto-noche-lector-confirma/f0050.png'), jpeg(R / 'conjunto-noche-lector-confirma/0200.png'),
                       'Portería con el lector confirmado')
    # Tira de los siete clips del Pase (último frame de cada uno).
    tira = ''.join(f'<figure><img src="{jpeg(cuadro("pase-3d-objeto", c, fin[c] if c != "latir" else ini[c] + 54), recorte=rec, ancho=640)}" '
                   f'alt="Pase al final de {c}"><figcaption>{c}</figcaption></figure>'
                   for c in pase.CLIPS if cuadro('pase-3d-objeto', c, fin[c] if c != 'latir' else ini[c] + 54).exists())
    import noche as n
    momentos = [('Llega', 1), ('El lector lee', n.LECTURA[0] + 7), ('Confirma', n.CONFIRMA[1]),
                ('La talanquera sube', n.TALANQUERA[1]), ('Entra', n.FIN)]
    tira_noche = ''.join(f'<figure><img src="{jpeg(cuadro("conjunto-noche-lector-confirma", "", f), ancho=640)}" alt="Portería: {t}">'
                         f'<figcaption>{t} · frame {f}</figcaption></figure>'
                         for t, f in momentos if cuadro('conjunto-noche-lector-confirma', '', f).exists())
    filas_t, total_s, total_f = tiempos()
    filas_m = medir()
    vids = videos()
    v = lambda k, d: (f'<figure class="video"><video src="{vids[k]}" muted playsinline loop controls preload="metadata"></video>'  # noqa: E731
                      f'<figcaption>{d}</figcaption></figure>') if k in vids else ''
    pagina = (AQUI / 'plantilla.html').read_text()
    for k, val in {
        '{{C}}': ''.join(f'--{k.replace("/", "-")}:{v};' for k, v in C.items() if len(v) == 7),
        '{{COMP_PASE}}': comp, '{{LATIR}}': latir, '{{NOCHE}}': noche, '{{TIRA}}': tira, '{{TIRA_NOCHE}}': tira_noche,
        '{{VIDEO_PORTERIA}}': v('porteria', 'Portería de noche, completa (260 frames a 60 fps).') + v('porteria-reducido', 'Movimiento reducido: cámara quieta, la talanquera cambia por fundido y no hay latido.'),
        '{{VIDEO_PASE}}': v('pase-confirmar', 'Confirmar: el borde se cierra, el chip pasa a vigente, llega la evidencia y aparece el resplandor.'),
        '{{TABLA_TIEMPOS}}': tabla(['Pieza', 'Tamaño', 'Muestras', 'Frames', 'Calculados', 'Por frame', 'Total'], filas_t, 'num'),
        '{{TOTAL_TIEMPO}}': f'{total_s / 3600:.1f} h para {total_f} frames calculados',
        '{{TABLA_COLOR}}': tabla(['Dónde', 'Token', 'Hex', 'Píxeles con el hex (±1)', 'ΔE mínimo', 'Resultado'], filas_m, 'num'),
    }.items():
        pagina = pagina.replace(k, val)
    (AQUI / 'lamina.html').write_text(pagina)
    print(f'✓ lamina.html · {len(pagina) / 1e6:.1f} MB · videos: {", ".join(vids) or "ninguno"}')


if __name__ == '__main__':
    main()
