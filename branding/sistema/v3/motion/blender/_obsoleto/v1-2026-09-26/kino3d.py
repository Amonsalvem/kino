"""Utilidades comunes para las escenas 3D de Kino en Blender (bpy 4.2).

- Tokens: los lee de ../tokens.motion.json (tema oscuro), que sale de los DTCG del repositorio.
- Color: hex del token → RGB lineal (Blender trabaja en lineal).
- Easing: cada tramo es un par de claves con handles bezier libres que reproducen exactamente el cubic-bezier
  del token (x1, y1, x2, y2), porque una curva de Blender entre dos claves es el mismo bezier cúbico en (t, v).
- Escala: 1 px del sistema = 0,01 unidades de Blender (la tarjeta de 360 × 132 px mide 3,6 × 1,32).
"""
import json
from pathlib import Path

import bpy

AQUI = Path(__file__).resolve().parent
TOKENS = json.loads((AQUI.parent / 'tokens.motion.json').read_text())['oscuro']
FPS = TOKENS['fps']
PX = 0.01
SUBIDA = TOKENS['distancia']['subida'] * PX


# Tokens -------------------------------------------------------------------------
def _verbo(nombre):
    return TOKENS['verbo'].get(nombre, nombre)


def dur(nombre):
    familia, clave = _verbo(nombre).split('/')
    return TOKENS[familia][clave]['frames']


def curva(nombre):
    return TOKENS['curva'][_verbo(nombre).split('/')[1]]


def hex_lineal(hexa):
    h = hexa.lstrip('#')
    def canal(c):
        c = int(c, 16) / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return (canal(h[0:2]), canal(h[2:4]), canal(h[4:6]), 1.0)


def color(token):
    if token not in TOKENS['color']:
        raise KeyError(f'color sin token: {token}')
    return hex_lineal(TOKENS['color'][token][:7])


# Escena -------------------------------------------------------------------------
def vaciar():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def configurar(escena, ancho, alto, inicio, fin, transparente):
    escena.render.fps = FPS
    escena.render.fps_base = 1
    escena.render.resolution_x, escena.render.resolution_y = ancho, alto
    escena.render.resolution_percentage = 100
    escena.frame_start, escena.frame_end = inicio, fin
    escena.render.engine = 'BLENDER_EEVEE_NEXT'
    escena.eevee.taa_render_samples = 16
    escena.render.film_transparent = transparente
    escena.render.image_settings.file_format = 'PNG'
    escena.render.image_settings.color_mode = 'RGBA'
    escena.render.image_settings.color_depth = '8'
    escena.view_settings.view_transform = 'Standard'  # los hex de marca deben salir iguales, sin tone mapping
    escena.view_settings.look = 'None'


# Materiales ---------------------------------------------------------------------
def material(nombre, token_base, rugosidad=0.5, token_emision=None, emision=0.0, alfa=1.0):
    """Principled BSDF con color de token. La emisión, si existe, también es un token."""
    m = bpy.data.materials.get(nombre) or bpy.data.materials.new(nombre)
    m.use_nodes = True
    bsdf = m.node_tree.nodes['Principled BSDF']
    bsdf.inputs['Base Color'].default_value = color(token_base)
    bsdf.inputs['Roughness'].default_value = rugosidad
    if token_emision:
        bsdf.inputs['Emission Color'].default_value = color(token_emision)
        bsdf.inputs['Emission Strength'].default_value = emision
    bsdf.inputs['Alpha'].default_value = alfa
    m.surface_render_method = 'BLENDED'
    m.use_transparency_overlap = True
    return m


def entrada(m, nombre):
    return m.node_tree.nodes['Principled BSDF'].inputs[nombre]


# Animación ----------------------------------------------------------------------
def tramo(dueno, ruta, indice, t0, t1, v0, v1, nombre_curva):
    """Dos claves en t0 y t1 con el easing exacto del token. dueno: objeto, socket o dato con keyframe_insert."""
    x1, y1, x2, y2 = curva(nombre_curva)
    _poner(dueno, ruta, indice, v0)
    dueno.keyframe_insert(ruta, index=indice, frame=t0)
    _poner(dueno, ruta, indice, v1)
    dueno.keyframe_insert(ruta, index=indice, frame=t1)
    fc = _fcurva(dueno, ruta, indice)
    k0 = next(k for k in fc.keyframe_points if k.co.x == t0)
    k1 = next(k for k in fc.keyframe_points if k.co.x == t1)
    for k in (k0, k1):
        k.interpolation = 'BEZIER'
        k.handle_left_type = k.handle_right_type = 'FREE'
    dt, dv = t1 - t0, v1 - v0
    k0.handle_right = (t0 + x1 * dt, v0 + y1 * dv)
    k1.handle_left = (t0 + x2 * dt, v0 + y2 * dv)
    fc.update()


def fijar(dueno, ruta, indice, t, v):
    """Clave constante: deja un valor fijo desde t (inicio de cada clip)."""
    _poner(dueno, ruta, indice, v)
    dueno.keyframe_insert(ruta, index=indice, frame=t)
    fc = _fcurva(dueno, ruta, indice)
    for k in fc.keyframe_points:
        if k.co.x == t:
            k.interpolation = 'CONSTANT'
    fc.update()


def _poner(dueno, ruta, indice, v):
    actual = getattr(dueno, ruta)
    if indice >= 0 and hasattr(actual, '__len__'):
        actual[indice] = v
    else:
        setattr(dueno, ruta, v)


def _fcurva(dueno, ruta, indice):
    if isinstance(dueno, bpy.types.NodeSocket):
        arbol = dueno.id_data
        accion = arbol.animation_data.action
        ruta_completa = dueno.path_from_id(ruta)
    else:
        accion = dueno.animation_data.action
        ruta_completa = ruta
    idx = max(indice, 0)
    return next(f for f in accion.fcurves if f.data_path == ruta_completa and f.array_index == idx)


def tramos_encadenados(dueno, ruta, indice, puntos, nombre_curva):
    """Varios tramos seguidos con la misma curva: puntos = [(t, v), ...]."""
    for (t0, v0), (t1, v1) in zip(puntos, puntos[1:]):
        tramo(dueno, ruta, indice, t0, t1, v0, v1, nombre_curva)


def guardar(ruta):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(ruta))


def abrir(ruta):
    bpy.ops.wm.open_mainfile(filepath=str(ruta))
