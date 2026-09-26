"""Construye las escenas 3D de Kino por etapas, una por proceso. Guarda el .blend entre etapas.

    python construir.py <id> <etapa> [--reducido] [--clip=<clip>] [--frames=a,b,c] [--escala=50]

id:     pase-3d-objeto · pase-3d-latir · conjunto-noche-lector-confirma
etapa:  escena · modelado · materiales · animacion · verificacion · render · exportar

Se corre con bpy 4.2 como módulo de Python (pip install bpy==4.2.0, Python 3.11) y EEVEE Next. El .blend queda en
blender/<id>[.reducido].blend y el render en blender/render/<id>[.reducido]/[<clip>/]NNNN.png. El render anota el
tiempo de cada frame en blender/tiempos/<id>[.reducido].json.
"""
import json
import sys
import time
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import bpy  # noqa: E402

import kino3d as k  # noqa: E402
import noche  # noqa: E402
import pase  # noqa: E402

RECURSOS = {
    'pase-3d-objeto': (pase, 'objeto'),
    'pase-3d-latir': (pase, 'latir'),
    'conjunto-noche-lector-confirma': (noche, None),
}
ETAPAS = ('escena', 'modelado', 'materiales', 'animacion', 'verificacion', 'render', 'exportar')


def nombre(id_, reducido):
    return id_ + ('.reducido' if reducido else '')


def opcion(clave, defecto=None):
    for a in sys.argv:
        if a.startswith(f'--{clave}='):
            return a.split('=', 1)[1]
    return defecto


def tramos_render(id_, reducido):
    """Rangos a renderizar: por clip en pase-3d-objeto; el rango de la escena en los demás.
    Reducido: el clip latir es un solo frame (el latido se detiene)."""
    sc = bpy.context.scene
    if id_ == 'pase-3d-objeto':
        out = {}
        for clip in pase.CLIPS:
            a, b = pase.rango(clip)
            out[clip] = (a, a) if (reducido and clip == 'latir') else (a, b)
        return out
    return {'': (sc.frame_start, sc.frame_end)}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    reducido = '--reducido' in sys.argv
    id_, etapa = args[0], args[1]
    if etapa not in ETAPAS:
        sys.exit(f'etapa desconocida: {etapa}. Usa una de: {", ".join(ETAPAS)}')
    modulo, modo = RECURSOS[id_]
    blend = AQUI / f'{nombre(id_, reducido)}.blend'
    if etapa == 'escena':
        modulo.escena(modo, reducido)
    else:
        k.abrir(blend)
    if etapa in ('modelado', 'materiales', 'animacion'):
        getattr(modulo, etapa)(modo, reducido)
    if etapa in ('escena', 'modelado', 'materiales', 'animacion'):
        k.guardar(blend)
        print(f'✓ {etapa} · {blend.name}')
        return
    sc = bpy.context.scene
    solo = opcion('clip')
    tramos = {c: r for c, r in tramos_render(id_, reducido).items() if not solo or c == solo}
    if etapa == 'verificacion':
        destino = AQUI / 'verificacion' / nombre(id_, reducido)
        destino.mkdir(parents=True, exist_ok=True)
        sc.render.resolution_percentage = int(opcion('escala', 50))
        k.escalar_compositor(sc)
        pedidos = opcion('frames')
        for clip, (a, b) in tramos.items():
            cuadros = [int(x) for x in pedidos.split(',')] if pedidos else sorted({a, (a + b) // 2, b})
            for f in cuadros:
                sc.frame_set(f)
                sc.render.filepath = str(destino / f'{clip + "-" if clip else ""}f{f:04d}.png')
                t0 = time.time()
                bpy.ops.render.render(write_still=True)
                print(f'✓ miniatura {sc.render.filepath} · {time.time() - t0:.1f} s')
    elif etapa == 'render':
        registro = AQUI / 'tiempos' / f'{nombre(id_, reducido)}.json'
        registro.parent.mkdir(exist_ok=True)
        datos = json.loads(registro.read_text()) if registro.exists() else {}
        quietos = modulo.tramos_quietos(reducido) if hasattr(modulo, 'tramos_quietos') else []
        for clip, (a, b) in tramos.items():
            sub = f'{nombre(id_, reducido)}/{clip}/' if clip else f'{nombre(id_, reducido)}/'
            carpeta = AQUI / 'render' / sub
            # Tramos quietos (idénticos por construcción: cámara y escena sin cambios) se renderizan una vez y se copian.
            segmentos, f = [], a
            while f <= b:
                q = next(((qa, qb) for qa, qb in quietos if qa <= f <= qb), None)
                if q:
                    segmentos.append(('quieto', f, min(q[1], b)))
                    f = min(q[1], b) + 1
                else:
                    fin = min([qa - 1 for qa, _ in quietos if qa > f] + [b])
                    segmentos.append(('render', f, fin))
                    f = fin + 1
            t0 = time.time()
            calculados = 0
            carpeta.mkdir(parents=True, exist_ok=True)
            sc.render.filepath = str(carpeta) + '/'
            for tipo, x, y in segmentos:
                # Reanudación: se saltan los frames que ya están escritos (el contenedor puede reiniciarse).
                hechos = {int(q.stem) for q in carpeta.glob('[0-9][0-9][0-9][0-9].png')}
                ultimo = x if tipo == 'quieto' else y
                faltan = [g for g in range(x, ultimo + 1) if g not in hechos]
                for c0 in faltan:
                    if c0 - 1 in faltan:
                        continue
                    c1 = c0
                    while c1 + 1 in faltan:
                        c1 += 1
                    sc.frame_start, sc.frame_end = c0, c1
                    bpy.ops.render.render(animation=True)
                    calculados += c1 - c0 + 1
                if tipo == 'quieto':
                    import shutil
                    for g in range(x + 1, y + 1):
                        shutil.copyfile(carpeta / f'{x:04d}.png', carpeta / f'{g:04d}.png')
            total = time.time() - t0
            n = b - a + 1
            datos[clip or 'escena'] = {'frames': n, 'calculados': calculados, 'segundos': round(total, 1),
                                       'por_frame_calculado': round(total / max(calculados, 1), 2),
                                       'resolucion': [sc.render.resolution_x, sc.render.resolution_y],
                                       'muestras': sc.eevee.taa_render_samples, 'motor': sc.render.engine}
            registro.write_text(json.dumps(datos, ensure_ascii=False, indent=1) + '\n')
            print(f'✓ render {sub} frames {a}–{b} · {calculados} calculados · {total:.0f} s · {total / max(calculados, 1):.1f} s/frame')
    elif etapa == 'exportar':
        import exportar
        exportar.glb(id_, reducido)


if __name__ == '__main__':
    main()
