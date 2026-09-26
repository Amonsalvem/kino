"""Construye las escenas 3D de Kino por etapas, una por proceso. Guarda el .blend entre etapas.

    python construir.py <id> <etapa> [--reducido]

id:     pase-3d-objeto · pase-3d-latir · conjunto-noche-lector-confirma
etapa:  escena · modelado · materiales · animacion · verificacion · render · exportar

Se corre con bpy 4.2 como módulo de Python (pip install bpy==4.2.0, Python 3.11). El .blend queda en
blender/<id>[.reducido].blend y el render en //render/<id>[.reducido]/ (junto al .blend).
"""
import json
import sys
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
INTERACTIVO_WEB = {'pase-3d-objeto'}
ETAPAS = ('escena', 'modelado', 'materiales', 'animacion', 'verificacion', 'render', 'exportar')


def nombre(id_, reducido):
    return id_ + ('.reducido' if reducido else '')


def tramos_render(id_, reducido):
    """Rangos a renderizar: por clip en pase-3d-objeto; el rango de la escena en los demás."""
    sc = bpy.context.scene
    if id_ == 'pase-3d-objeto':
        return {clip: pase.rango(clip) for clip in pase.CLIPS if not (reducido and clip == 'latir')} | (
            {'latir': (pase.CLIPS['latir'][0],) * 2} if reducido else {})
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
    if etapa == 'verificacion':
        destino = AQUI / 'verificacion' / nombre(id_, reducido)
        destino.mkdir(parents=True, exist_ok=True)
        sc.render.resolution_percentage = 50
        for clip, (a, b) in tramos_render(id_, reducido).items():
            for f in sorted({a, (a + b) // 2, b}):
                sc.frame_set(f)
                sc.render.filepath = str(destino / f'{clip + "-" if clip else ""}f{f:04d}.png')
                bpy.ops.render.render(write_still=True)
                print('✓ miniatura', sc.render.filepath)
    elif etapa == 'render':
        for clip, (a, b) in tramos_render(id_, reducido).items():
            sc.frame_start, sc.frame_end = a, b
            sub = f'{nombre(id_, reducido)}/{clip}/' if clip else f'{nombre(id_, reducido)}/'
            sc.render.filepath = f'//render/{sub}'
            bpy.ops.render.render(animation=True)
            print(f'✓ render {sub} frames {a}–{b}')
    elif etapa == 'exportar':
        if id_ not in INTERACTIVO_WEB or reducido:
            print('— sin GLB: el recurso no es interactivo en web')
            return
        # glTF no anima materiales: cada pieza lleva su token en extras y clips.json dice qué se ve en cada estado.
        for ob in bpy.data.objects:
            if ob.name in pase.TOKEN_PIEZA:
                ob['kino_token'] = pase.TOKEN_PIEZA[ob.name]
        glb = AQUI / 'glb' / f'{id_}.sin-draco.glb'
        glb.parent.mkdir(exist_ok=True)
        sc.frame_start, sc.frame_end = 1, pase.rango('revocar')[1]
        bpy.ops.export_scene.gltf(filepath=str(glb), export_format='GLB', export_animations=True,
                                  export_animation_mode='SCENE', export_force_sampling=True, export_apply=True,
                                  export_cameras=False, export_lights=False, export_extras=True)
        clips = {c: {'desde': pase.rango(c)[0], 'hasta': pase.rango(c)[1], 'estado_inicial': pase.ESTADOS_CLIP[c][0],
                     'estado_final': pase.ESTADOS_CLIP[c][1], 'duracion': pase.CLIPS[c][1],
                     'curva': pase.CURVA_CLIP[c]} for c in pase.CLIPS}
        datos = {'fps': k.FPS, 'clips': clips, 'piezas_por_estado': pase.PIEZAS_POR_ESTADO,
                 'color_por_estado': pase.COLOR_POR_ESTADO, 'tokens': {t: k.TOKENS['color'][t] for t in pase.tokens_usados()}}
        (AQUI / 'glb' / f'{id_}.clips.json').write_text(json.dumps(datos, ensure_ascii=False, indent=1) + '\n')
        print('✓ GLB', glb)


if __name__ == '__main__':
    main()
