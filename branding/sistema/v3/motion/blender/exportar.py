"""GLB del Pase (pase-3d-objeto) para el visor web.

glTF no anima materiales. En vez de que el visor reconstruya los colores, el GLB lleva un material por estado para
cada pieza (KHR_materials_variants): «sin-confirmar», «vigente», «por-vencer», «vencido», «usado», «revocado». Cada
variante trae el color horneado del token y la opacidad de la pieza en ese estado. Las marcas son unlit (salen con el
hex exacto) y la tarjeta es PBR (laca y sheen). Las transformaciones (subida, escala de entrada, asentamiento, barra,
corte, tachado, subida de la nota) van como animación.

Pasos: Blender escribe glb/pase-3d-objeto.base.glb y glb/pase-3d-objeto.estados.json; variantes.mjs (gltf-transform)
crea las variantes y comprime con Draco en glb/pase-3d-objeto.glb.
"""
import json
import math
import subprocess
from pathlib import Path

import bpy

import kino3d as k
import pase

AQUI = Path(__file__).resolve().parent
GLB = AQUI / 'glb'


def estados():
    """Por estado y pieza: color (hex del token) y opacidad. Sale de pase.valor(), lo mismo que anima Blender."""
    ob = bpy.data.objects
    out = {}
    for e in pase.ESTADOS:
        piezas = {}
        raiz = pase.valor(e, 'root.opacidad')
        for o in ob:
            if o.type not in ('MESH', 'FONT') or o.name == 'tarjeta' or not o.active_material:
                continue
            nodos = o.active_material.node_tree.nodes
            if 'local' not in nodos:
                continue
            n = o.name
            if n == 'brillo':
                alfa = 0.0  # el latido lo hace el visor con curva/latir
            elif o.parent and o.parent.name.startswith('chip-'):
                alfa = pase.valor(e, o.parent.name)
            elif n == 'quien':
                alfa = 1.0
            else:
                alfa = pase.valor(e, n)
            token = token_de(o, e)
            piezas[n] = {'token': token, 'hex': k.hexa(token), 'alfa': round(alfa * raiz, 4)}
        base = pase.valor(e, 'tarjeta.color')
        piezas['tarjeta'] = {'token': base[0], 'hex': k.hexa(base[0]), 'alfa': raiz, 'pbr': True}
        piezas['resplandor'] = {'token': k.RESPLANDOR_HALO['color'], 'hex': k.hexa(k.RESPLANDOR_HALO['color']),
                                'alfa': pase.valor(e, 'resplandor')}
        out[e] = piezas
    return out


def token_de(o, e):
    n = o.name
    if n == 'borde':
        return pase.valor(e, 'borde.color')
    if n == 'barra':
        return pase.valor(e, 'barra.color')
    # El resto tiene un solo token: el que Blender le puso a su material (se lee del nombre del grupo o de la tabla).
    if n.startswith('chip-'):
        est, parte = n[5:].rsplit('-', 1)
        return f'estado/{est}/{"texto" if parte == "texto" else "fondo" if parte == "fondo" else "borde"}'
    return {'borde-sin': 'estado/sin-confirmar/borde', 'quien': 'texto/primario', 'tachado': 'estado/usado/texto',
            'brillo': 'estado/vigente/texto', 'nota-confirmo': 'estado/vigente/texto', 'nota-revoco': 'estado/revocado/texto',
            'pista': 'superficie/elevada', 'corte': 'estado/revocado/texto'}.get(n, 'texto/secundario')


def halo_png(ruta, margen_px=48):
    """Textura del resplandor: el token resplandor/vigente (halo blur 28, spread −8) sobre la silueta de la tarjeta."""
    import numpy as np
    from PIL import Image
    w, h = 360 + 2 * margen_px, 132 + 2 * margen_px
    esc = 2
    ys, xs = np.mgrid[0:h * esc, 0:w * esc] / esc
    x, y = xs - w / 2, ys - h / 2
    r = k.FORMA['radio']['tarjeta'] + k.RESPLANDOR_HALO['spread']
    ax, ay = 180 + k.RESPLANDOR_HALO['spread'] - r, 66 + k.RESPLANDOR_HALO['spread'] - r
    dx, dy = np.maximum(np.abs(x) - ax, 0), np.maximum(np.abs(y) - ay, 0)
    d = np.hypot(dx, dy) - r  # distancia con signo a la silueta reducida
    sigma = k.RESPLANDOR_HALO['blur'] / 2
    from math import erf, sqrt
    a = 0.5 * (1 - np.vectorize(erf)(d / (sigma * sqrt(2))))
    # Solo fuera de la tarjeta (box-shadow queda debajo del elemento opaco).
    ra = k.FORMA['radio']['tarjeta']
    dt = np.hypot(np.maximum(np.abs(x) - (180 - ra), 0), np.maximum(np.abs(y) - (66 - ra), 0)) - ra
    a = np.where(dt < 0, 0, a)
    rgba = np.zeros((h * esc, w * esc, 4), np.uint8)
    rgba[..., :3] = [int(k.hexa(k.RESPLANDOR_HALO['color'])[i:i + 2], 16) for i in (1, 3, 5)]
    rgba[..., 3] = (a * 255).clip(0, 255).astype(np.uint8)
    Image.fromarray(rgba).save(ruta)
    return margen_px


def glb(id_, reducido):
    if id_ != 'pase-3d-objeto' or reducido:
        print('— sin GLB: solo pase-3d-objeto es interactivo en web')
        return
    sc = bpy.context.scene
    GLB.mkdir(exist_ok=True)
    # Membrana en PBR: los mismos valores que el material de Blender (rugosidad, laca, sheen con su token).
    pbr = {'rugosidad': 0.42, 'laca': 0.35, 'laca_rugosidad': 0.14, 'sheen_token': 'sustrato/d70',
           'sheen_hex': k.hexa('sustrato/d70'), 'sheen_rugosidad': 0.35}
    datos = {'fps': k.FPS, 'estados': estados(), 'pbr_tarjeta': pbr, 'clips': {}, 'tokens_motion': {
        'curva': k.MOTION['curva'], 'verbo': k.MOTION['verbo'], 'latir': k.frames('latir/duracion'),
        'latir_ciclos': k.MOTION['latirCiclos']}}
    for c in pase.CLIPS:
        a, b = pase.rango(c)
        ev, ini, fin = pase.CLIPS[c]
        datos['clips'][c] = {'desde': a, 'hasta': b, 'estado_inicial': ini or 'sin-confirmar', 'estado_final': fin,
                             'curva': k.curva(pase.curva_clip(c)), 'nombre_curva': pase.curva_clip(c),
                             'evento': ev, 'deja': next((t.get('deja') for t in k.PARTITURA['transiciones'] if t['evento'] == ev), None)}
    # Resplandor: plano con la textura del token, detrás de la tarjeta.
    margen = halo_png(GLB / 'resplandor.png')
    mw, mh = (360 + 2 * margen) * k.PX, (132 + 2 * margen) * k.PX
    me = bpy.data.meshes.new('resplandor')
    y = pase.GROSOR / 2 + 0.004
    me.from_pydata([(-mw / 2, y, -mh / 2), (mw / 2, y, -mh / 2), (mw / 2, y, mh / 2), (-mw / 2, y, mh / 2)], [], [(0, 1, 2, 3)])
    uv = me.uv_layers.new(name='UVMap')
    for i, (u, v) in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))):
        uv.data[i].uv = (u, v)
    o = bpy.data.objects.new('resplandor', me)
    sc.collection.objects.link(o)
    o.parent = bpy.data.objects['root']
    # Materiales de exportación: uno simple por pieza (variantes.mjs los reemplaza por los de cada estado).
    for ob in list(bpy.data.objects):
        if ob.type in ('MESH', 'FONT'):
            m = bpy.data.materials.new(f'm-{ob.name}')
            ob.data.materials.clear()
            ob.data.materials.append(m)
        ob['kino_pieza'] = ob.name
    for ob in bpy.data.objects:
        if ob.type == 'FONT':
            ob.hide_render = False
    # Las claves de hide_render no van al GLB; la visibilidad la dan las variantes.
    sc.frame_start, sc.frame_end = 1, pase.rango('revocar')[1]
    base = GLB / f'{id_}.base.glb'
    bpy.ops.export_scene.gltf(filepath=str(base), export_format='GLB', export_animations=True,
                              export_animation_mode='SCENE', export_force_sampling=True, export_apply=True,
                              export_cameras=False, export_lights=False, export_extras=True,
                              export_def_bones=False, export_optimize_animation_size=True,
                              export_yup=True, export_texcoords=True, export_normals=True)
    (GLB / f'{id_}.estados.json').write_text(json.dumps(datos, ensure_ascii=False, indent=1) + '\n')
    print('✓ GLB base', base)
    r = subprocess.run(['node', str(AQUI / 'variantes.mjs')], cwd=AQUI, capture_output=True, text=True)
    print(r.stdout, r.stderr)
