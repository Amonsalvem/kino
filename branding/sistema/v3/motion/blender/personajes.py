"""Personajes 3D de Kino (E3-9, aprobada el 19 oct): el residente y la administración, estética biopunk.

Uso: .venv/bin/python personajes.py residente|administracion [--frames=1-90] [--paso=1] [--escala=100] [--muestras=48]
Escribe render/personaje-<id>/####.png (RGBA). Solo presentaciones y onboarding (decisiones.md E3-9).

Lenguaje de forma (motion-e-ilustracion.md, biopunk E3-1):
- Cuerpo de metabolas: una membrana viva, translúcida, con venas bioluminiscentes que laten.
- Residente: membrana verde y brotes de micelio en la cabeza; sostiene un Pase (el arco, X8) que se enciende tres veces.
- Administración: membrana índigo bajo placas de quitina (estructura, el marco); sostiene una lámina de cristal con
  tres franjas que se fijan una tras otra y un anillo (el reloj de las franjas).
Color: primitivos y semánticos del tema oscuro (tokens.motion.json), hex → lineal. No hay hex escritos a mano.
"""
import json
import math
import sys
from pathlib import Path

import bpy

AQUI = Path(__file__).resolve().parent
T = json.loads((AQUI.parent / 'tokens.motion.json').read_text())['oscuro']
P, C = T['primitivo'], T['color']
FPS = 30
DUR = 90  # 3 s; después el personaje queda quieto en su último cuadro


def lin(h, a=1.0):
    h = h.lstrip('#')
    rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return (*[f(c) for c in rgb], a)


def args():
    o = {'frames': (1, DUR), 'escala': 100, 'muestras': 48, 'paso': 1}
    for a in sys.argv[2:]:
        if a.startswith('--frames='):
            x, y = a.split('=')[1].split('-')
            o['frames'] = (int(x), int(y))
        elif a.startswith('--escala='):
            o['escala'] = int(a.split('=')[1])
        elif a.startswith('--paso='):
            o['paso'] = int(a.split('=')[1])
        elif a.startswith('--muestras='):
            o['muestras'] = int(a.split('=')[1])
    return o


def limpiar():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s = bpy.context.scene
    s.render.fps = FPS
    s.frame_start, s.frame_end = 1, DUR
    return s


# Materiales ---------------------------------------------------------------------------------------------
def nodo(nt, tipo, **kw):
    n = nt.nodes.new(tipo)
    for k, v in kw.items():
        if k == 'loc':
            n.location = v
        else:
            setattr(n, k, v)
    return n


def membrana(nombre, base, sss, vena, fuerza_vena=4.0, escala_vena=3.2):
    """Membrana viva: translúcida, con venas (bordes de Voronoi) que emiten y laten con el valor `latido`."""
    m = bpy.data.materials.new(nombre)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes['Principled BSDF']
    bsdf.inputs['Base Color'].default_value = lin(base)
    bsdf.inputs['Subsurface Weight'].default_value = 0.55
    bsdf.inputs['Subsurface Radius'].default_value = (0.5, 1.0, 0.7)
    bsdf.inputs['Subsurface Scale'].default_value = 0.25
    bsdf.inputs['Roughness'].default_value = 0.32
    bsdf.inputs['Coat Weight'].default_value = 0.6
    bsdf.inputs['Coat Roughness'].default_value = 0.08
    bsdf.inputs['Emission Color'].default_value = lin(vena)
    coord = nodo(nt, 'ShaderNodeTexCoord', loc=(-900, 0))
    vor = nodo(nt, 'ShaderNodeTexVoronoi', loc=(-700, 0), feature='DISTANCE_TO_EDGE')
    vor.inputs['Scale'].default_value = escala_vena * 1.6
    torcer = nodo(nt, 'ShaderNodeTexNoise', loc=(-1100, -150))
    torcer.inputs['Scale'].default_value = 3.0
    nt.links.new(coord.outputs['Object'], torcer.inputs['Vector'])
    mezcla = nodo(nt, 'ShaderNodeVectorMath', loc=(-880, -100), operation='MULTIPLY_ADD')
    mezcla.inputs[1].default_value = (0.35, 0.35, 0.35)
    nt.links.new(torcer.outputs['Color'], mezcla.inputs[0])
    nt.links.new(coord.outputs['Object'], mezcla.inputs[2])
    nt.links.new(mezcla.outputs[0], vor.inputs['Vector'])
    rampa = nodo(nt, 'ShaderNodeValToRGB', loc=(-480, 0))
    rampa.color_ramp.elements[0].position = 0.0
    rampa.color_ramp.elements[0].color = (1, 1, 1, 1)
    rampa.color_ramp.elements[1].position = 0.022
    rampa.color_ramp.elements[1].color = (0, 0, 0, 1)
    nt.links.new(vor.outputs['Distance'], rampa.inputs['Fac'])
    ruido = nodo(nt, 'ShaderNodeTexNoise', loc=(-700, 260))
    ruido.inputs['Scale'].default_value = 1.6
    nt.links.new(coord.outputs['Object'], ruido.inputs['Vector'])
    mascara = nodo(nt, 'ShaderNodeValToRGB', loc=(-480, 260))
    mascara.color_ramp.elements[0].position = 0.42
    mascara.color_ramp.elements[1].position = 0.62
    nt.links.new(ruido.outputs['Fac'], mascara.inputs['Fac'])
    venas = nodo(nt, 'ShaderNodeMath', loc=(-300, 120), operation='MULTIPLY')
    nt.links.new(rampa.outputs['Color'], venas.inputs[0])
    nt.links.new(mascara.outputs['Color'], venas.inputs[1])
    # Borde de luz (fresnel): la membrana brilla en el contorno, como una célula bajo el microscopio.
    fres = nodo(nt, 'ShaderNodeLayerWeight', loc=(-480, -220))
    fres.inputs['Blend'].default_value = 0.35
    suma = nodo(nt, 'ShaderNodeMath', loc=(-250, -80), operation='ADD')
    nt.links.new(venas.outputs[0], suma.inputs[0])
    pot = nodo(nt, 'ShaderNodeMath', loc=(-370, -220), operation='MULTIPLY')
    pot.inputs[1].default_value = 0.45
    nt.links.new(fres.outputs['Facing'], pot.inputs[0])
    nt.links.new(pot.outputs[0], suma.inputs[1])
    latido = nodo(nt, 'ShaderNodeValue', loc=(-250, -260), label='latido')
    latido.name = 'latido'
    latido.outputs[0].default_value = fuerza_vena
    mul = nodo(nt, 'ShaderNodeMath', loc=(-80, -120), operation='MULTIPLY')
    nt.links.new(suma.outputs[0], mul.inputs[0])
    nt.links.new(latido.outputs[0], mul.inputs[1])
    nt.links.new(mul.outputs[0], bsdf.inputs['Emission Strength'])
    return m


def emisivo(nombre, color, fuerza=6.0):
    m = bpy.data.materials.new(nombre)
    m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = lin(color)
    b.inputs['Emission Color'].default_value = lin(color)
    b.inputs['Emission Strength'].default_value = fuerza
    b.inputs['Roughness'].default_value = 0.2
    return m


def quitina(nombre, color, borde):
    """Placa de quitina: dura, lacada, con el filo encendido."""
    m = bpy.data.materials.new(nombre)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = lin(color)
    b.inputs['Metallic'].default_value = 0.35
    b.inputs['Roughness'].default_value = 0.18
    b.inputs['Coat Weight'].default_value = 1.0
    b.inputs['Coat Roughness'].default_value = 0.03
    b.inputs['Emission Color'].default_value = lin(borde)
    fres = nodo(nt, 'ShaderNodeLayerWeight', loc=(-400, -200))
    fres.inputs['Blend'].default_value = 0.2
    mul = nodo(nt, 'ShaderNodeMath', loc=(-200, -200), operation='POWER')
    mul.inputs[1].default_value = 3.0
    nt.links.new(fres.outputs['Facing'], mul.inputs[0])
    k = nodo(nt, 'ShaderNodeMath', loc=(-60, -200), operation='MULTIPLY')
    k.inputs[1].default_value = 3.5
    nt.links.new(mul.outputs[0], k.inputs[0])
    nt.links.new(k.outputs[0], b.inputs['Emission Strength'])
    return m


def cristal(nombre, tinte):
    m = bpy.data.materials.new(nombre)
    m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = lin(tinte)
    b.inputs['Transmission Weight'].default_value = 1.0
    b.inputs['Roughness'].default_value = 0.12
    b.inputs['IOR'].default_value = 1.35
    b.inputs['Alpha'].default_value = 0.55
    m.blend_method = 'BLEND' if hasattr(m, 'blend_method') else m.blend_method
    m.surface_render_method = 'BLENDED'
    return m


# Geometría ----------------------------------------------------------------------------------------------
def metabolas(nombre, bolas, material, umbral=0.6):
    """bolas: (x, y, z, radio, (sx, sy, sz)). Se convierten en malla suave."""
    mb = bpy.data.metaballs.new(nombre)
    mb.resolution = 0.04
    mb.render_resolution = 0.025
    mb.threshold = umbral
    for x, y, z, r, s in bolas:
        e = mb.elements.new(type='ELLIPSOID')
        e.co = (x, y, z)
        e.radius = r
        e.size_x, e.size_y, e.size_z = s
    ob = bpy.data.objects.new(nombre, mb)
    bpy.context.collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.convert(target='MESH')
    ob = bpy.context.active_object
    bpy.ops.object.shade_smooth()
    ob.data.materials.append(material)
    return ob


def esfera(nombre, loc, escala, material, seg=48):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, location=loc)
    o = bpy.context.active_object
    o.name = nombre
    o.scale = escala
    bpy.ops.object.shade_smooth()
    o.data.materials.append(material)
    return o


def tallo(nombre, puntos, grosor, material):
    cu = bpy.data.curves.new(nombre, 'CURVE')
    cu.dimensions = '3D'
    cu.bevel_depth = grosor
    cu.bevel_resolution = 6
    sp = cu.splines.new('BEZIER')
    sp.bezier_points.add(len(puntos) - 1)
    for bp, p in zip(sp.bezier_points, puntos):
        bp.co = p
        bp.handle_left_type = bp.handle_right_type = 'AUTO'
    ob = bpy.data.objects.new(nombre, cu)
    bpy.context.collection.objects.link(ob)
    cu.materials.append(material)
    # Se adelgaza hacia la punta.
    for i, bp in enumerate(sp.bezier_points):
        bp.radius = 1.0 - 0.7 * i / max(1, len(puntos) - 1)
    return ob


def arco(nombre, ancho, alto, grosor, material):
    """El arco del logo (X8: solo en lo que es un Pase), extruido."""
    cu = bpy.data.curves.new(nombre, 'CURVE')
    cu.dimensions = '2D'
    cu.fill_mode = 'BOTH'
    cu.extrude = grosor
    cu.bevel_depth = grosor * 0.35
    r = ancho / 2
    sp = cu.splines.new('POLY')
    pts = [(-r, 0), (r, 0), (r, alto - r)]
    for i in range(1, 24):
        a = math.pi * i / 24
        pts.append((r * math.cos(a), alto - r + r * math.sin(a)))
    pts.append((-r, alto - r))
    sp.points.add(len(pts) - 1)
    for p, (x, y) in zip(sp.points, pts):
        p.co = (x, y, 0, 1)
    sp.use_cyclic_u = True
    ob = bpy.data.objects.new(nombre, cu)
    bpy.context.collection.objects.link(ob)
    cu.materials.append(material)
    ob.rotation_euler = (math.pi / 2, 0, 0)
    return ob


def caja(nombre, loc, dim, material, bisel=0.02):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.active_object
    o.name = nombre
    o.scale = [d / 2 for d in dim]
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    mod = o.modifiers.new('bisel', 'BEVEL')
    mod.width = bisel
    mod.segments = 4
    bpy.ops.object.shade_smooth()
    o.data.materials.append(material)
    return o


def clave(ob, ruta, cuadros_valores, indice=-1):
    for f, v in cuadros_valores:
        if indice < 0:
            setattr(ob, ruta, v)
            ob.keyframe_insert(ruta, frame=f)
        else:
            getattr(ob, ruta)[indice] = v
            ob.keyframe_insert(ruta, index=indice, frame=f)


def clave_valor(material, nombre, cuadros_valores):
    n = material.node_tree.nodes[nombre]
    for f, v in cuadros_valores:
        n.outputs[0].default_value = v
        n.outputs[0].keyframe_insert('default_value', frame=f)


def suavizar_claves():
    for a in bpy.data.actions:
        for fc in a.fcurves:
            for k in fc.keyframe_points:
                k.interpolation = 'BEZIER'
                k.easing = 'AUTO'


# Escena -------------------------------------------------------------------------------------------------
def escena(s, o, apuntar):
    s.render.engine = 'BLENDER_EEVEE_NEXT'
    s.eevee.taa_render_samples = o['muestras']
    s.eevee.use_raytracing = False
    s.eevee.use_shadows = True
    s.render.film_transparent = True
    s.render.resolution_x = s.render.resolution_y = 1080
    s.render.resolution_percentage = o['escala']
    s.render.image_settings.file_format = 'PNG'
    s.render.image_settings.color_mode = 'RGBA'
    s.view_settings.view_transform = 'Standard'
    s.view_settings.look = 'None'
    w = bpy.data.worlds.new('mundo')
    s.world = w
    w.use_nodes = True
    w.node_tree.nodes['Background'].inputs['Color'].default_value = lin(P['sustrato/100'])
    w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.6

    cam = bpy.data.objects.new('camara', bpy.data.cameras.new('camara'))
    s.collection.objects.link(cam)
    cam.data.lens = 70
    s.camera = cam
    objetivo = bpy.data.objects.new('objetivo', None)
    s.collection.objects.link(objetivo)
    objetivo.location = apuntar
    t = cam.constraints.new('TRACK_TO')
    t.target = objetivo
    # Órbita corta: la cámara llega de 12° a la derecha y se asienta de frente.
    for f, a in [(1, math.radians(14)), (DUR, math.radians(4))]:
        d = 7.4
        cam.location = (d * math.sin(a), -d * math.cos(a), apuntar[2] + 0.55)
        cam.keyframe_insert('location', frame=f)

    def luz(nombre, tipo, loc, color, energia, tam=2.0):
        l = bpy.data.objects.new(nombre, bpy.data.lights.new(nombre, tipo))
        s.collection.objects.link(l)
        l.location = loc
        l.data.color = lin(color)[:3]
        l.data.energy = energia
        if tipo == 'AREA':
            l.data.size = tam
        tt = l.constraints.new('TRACK_TO')
        tt.target = objetivo
        return l

    luz('clave', 'AREA', (-3.2, -3.6, 4.2), P['hueso/100'], 520, 3.0)
    luz('contra-verde', 'AREA', (3.4, 2.6, 3.2), P['biolum/d110'], 900, 2.0)
    luz('contra-violeta', 'AREA', (-3.6, 2.8, 2.0), P['indigo/d70'], 700, 2.0)
    luz('relleno', 'AREA', (0, -4.5, 0.6), P['sustrato/800'], 120, 4.0)

    # Compositor: resplandor (Glare, niebla) sobre lo que emite; respeta el alfa.
    s.use_nodes = True
    nt = s.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    rl = nt.nodes.new('CompositorNodeRLayers')
    gl = nt.nodes.new('CompositorNodeGlare')
    gl.glare_type = 'FOG_GLOW'
    gl.quality = 'HIGH'
    gl.threshold = 0.85
    gl.size = 8
    gl.mix = -0.35
    out = nt.nodes.new('CompositorNodeComposite')
    sa = nt.nodes.new('CompositorNodeSetAlpha')
    sa.mode = 'REPLACE_ALPHA'
    nt.links.new(rl.outputs['Image'], gl.inputs['Image'])
    nt.links.new(gl.outputs['Image'], sa.inputs['Image'])
    nt.links.new(rl.outputs['Alpha'], sa.inputs['Alpha'])
    nt.links.new(sa.outputs['Image'], out.inputs['Image'])


def sombra_contacto(material_color):
    bpy.ops.mesh.primitive_plane_add(size=6, location=(0, 0, 0))
    p = bpy.context.active_object
    p.is_shadow_catcher = True
    m = bpy.data.materials.new('suelo')
    m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = lin(material_color)
    b.inputs['Alpha'].default_value = 0.0
    m.surface_render_method = 'BLENDED'
    p.data.materials.append(m)
    # Charco de luz bajo el personaje: una elipse emisiva muy tenue (el suelo vivo del biopunk).
    halo = esfera('charco', (0, 0, 0.005), (0.75, 0.55, 0.008), emisivo('charco', material_color, 0.05))
    return p, halo


# Residente ----------------------------------------------------------------------------------------------
def brazo(nombre, puntos, grosor, material):
    o = tallo(nombre, puntos, grosor, material)
    for bp in o.data.splines[0].bezier_points:
        bp.radius = 1.0
    return o


def residente():
    from mathutils import Matrix
    piel = membrana('membrana-verde', P['biolum/d15'], P['biolum/d45'], C['estado/vigente/texto'], 3.0, 3.0)
    ojo = emisivo('ojo', P['hueso/100'], 3.0)
    brote = emisivo('brote', C['estado/vigente/texto'], 9.0)
    tallo_m = membrana('tallo', P['biolum/d23'], P['biolum/d45'], C['estado/vigente/texto'], 1.2, 6.0)
    cuerpo = metabolas('residente', [
        (0, 0, 0.5, 0.58, (1.05, 0.95, 0.72)),   # base
        (0, 0, 0.98, 0.5, (0.95, 0.85, 1.05)),   # torso
        (0, 0, 1.38, 0.36, (1.0, 0.9, 1.0)),     # cuello: une cabeza y torso en una sola membrana
        (0, 0, 1.78, 0.7, (1.0, 0.94, 0.9)),     # cabeza grande: proporción amable
    ], piel, 0.5)
    brazo('brazo-izq', [(-0.22, 0, 1.15), (-0.52, -0.05, 1.02), (-0.62, -0.12, 0.76)], 0.12, piel)
    brazo('brazo-der', [(0.22, -0.02, 1.18), (0.56, -0.1, 1.38), (0.66, -0.22, 1.64)], 0.12, piel)
    esfera('mano-izq', (-0.62, -0.13, 0.7), (0.13, 0.13, 0.13), piel)
    esfera('mano-der', (0.66, -0.24, 1.7), (0.13, 0.13, 0.13), piel)
    for x in (-0.24, 0.24):
        esfera(f'ojo{x}', (x, -0.6, 1.86), (0.07, 0.04, 0.1), ojo)
    boca = emisivo('boca', P['biolum/d110'], 2.0)
    s_ = tallo('sonrisa', [(-0.1, -0.64, 1.66), (0, -0.67, 1.61), (0.1, -0.64, 1.66)], 0.016, boca)
    for bp in s_.data.splines[0].bezier_points:
        bp.radius = 1.0
    # Brotes de micelio en la cabeza, con la punta encendida.
    for i, (dx, dy, h) in enumerate([(-0.22, 0.05, 0.5), (0.04, 0.14, 0.72), (0.3, -0.02, 0.45)]):
        tallo(f'tallo{i}', [(dx * 0.6, dy, 2.32), (dx, dy, 2.32 + h * 0.6), (dx * 1.5, dy - 0.05, 2.32 + h)], 0.03, tallo_m)
        esfera(f'brote{i}', (dx * 1.5, dy - 0.05, 2.32 + h), (0.06, 0.06, 0.06), brote)
    # Motas bioluminiscentes, como esporas en la membrana.
    for i, (x, z) in enumerate([(-0.4, 1.35), (-0.28, 1.25), (0.3, 1.0), (0.18, 0.62)]):
        esfera(f'mota{i}', (x, -0.46, z), (0.035, 0.035, 0.035), brote, 16)

    # El Pase en la mano: arco de hueso con QR y borde vigente (X8).
    pase_m = emisivo('pase', P['hueso/100'], 1.4)
    borde = emisivo('pase-borde', C['estado/vigente/borde'], 8.0)
    raiz = bpy.data.objects.new('pase', None)
    bpy.context.collection.objects.link(raiz)
    a = arco('pase-arco', 0.5, 0.62, 0.035, pase_m)
    a.parent = raiz
    b = arco('pase-borde', 0.56, 0.68, 0.02, borde)
    b.parent = raiz
    b.location = (0, 0.03, -0.03)
    qr = emisivo('qr', P['sustrato/100'], 0.0)
    import random
    random.seed(4)
    for i in range(6):
        for j in range(6):
            if random.random() < 0.5 or (i < 2 and j < 2) or (i > 3 and j < 2):
                c = caja(f'qr{i}{j}', (-0.15 + i * 0.06, -0.065, 0.1 + j * 0.06), (0.05, 0.01, 0.05), qr, 0.004)
                c.parent = raiz
    raiz.location = (0.7, -0.3, 1.74)
    raiz.rotation_euler = (0, math.radians(-10), math.radians(-14))

    # Animación: respira; el Pase sale de la mano y se enciende tres veces (confirmado, como en la partitura).
    clave(cuerpo, 'scale', [(1, 0.96), (14, 1.02), (26, 1.0)], 2)
    clave(raiz, 'location', [(1, 1.7), (22, 1.82), (DUR, 1.82)], 2)
    for k in range(3):
        clave(raiz, 'scale', [(1, 0.15), (22, 0.82), (32, 0.75)], k)
    nb = borde.node_tree.nodes['Principled BSDF'].inputs['Emission Strength']
    for f, v in [(1, 0), (34, 0), (40, 22), (50, 6), (56, 22), (66, 6), (72, 22), (82, 8), (DUR, 8)]:
        nb.default_value = v
        nb.keyframe_insert('default_value', frame=f)
    clave_valor(piel, 'latido', [(1, 1.2), (38, 1.2), (44, 4.5), (54, 2.6), (60, 4.5), (70, 2.6), (76, 4.5), (DUR, 3.0)])
    suavizar_claves()
    return (0.15, 0, 1.3), C['estado/vigente/fondo']


# Administración -----------------------------------------------------------------------------------------
def administracion():
    from mathutils import Matrix, Euler
    piel = membrana('membrana-indigo', P['indigo/d15'], P['indigo/d32'], P['indigo/d70'], 1.6, 2.6)
    placa = quitina('quitina', P['violeta/d32'], P['indigo/d110'])
    visor = emisivo('visor', P['indigo/d45'], 1.5)
    cuerpo = metabolas('administracion', [
        (0, 0, 0.5, 0.64, (1.15, 0.95, 0.72)),
        (0, 0, 1.0, 0.56, (1.12, 0.85, 1.0)),
        (0, 0, 1.4, 0.4, (1.05, 0.9, 1.0)),
        (0, 0, 1.8, 0.64, (1.0, 0.94, 0.9)),
    ], piel, 0.5)
    brazo('brazo-izq', [(-0.3, 0, 1.2), (-0.52, -0.4, 1.02), (-0.3, -0.66, 0.98)], 0.12, piel)
    brazo('brazo-der', [(0.3, 0, 1.2), (0.52, -0.4, 1.02), (0.32, -0.66, 0.98)], 0.12, piel)
    # Placas de quitina: hombros, pecho y corona. La estructura es el marco que fija la administración.
    for x in (-0.48, 0.48):
        h = esfera(f'hombro{x}', (x, -0.05, 1.36), (0.28, 0.26, 0.09), placa)
        h.rotation_euler = (0, math.radians(-30 if x < 0 else 30), 0)
    corona = esfera('corona', (0, 0.04, 2.16), (0.5, 0.44, 0.16), placa)
    corona.rotation_euler = (math.radians(-12), 0, 0)
    esfera('visor', (0, -0.6, 1.86), (0.3, 0.035, 0.05), visor)
    marco = quitina('marco-visor', P['violeta/d23'], P['indigo/d70'])
    bpy.ops.mesh.primitive_torus_add(major_radius=0.33, minor_radius=0.03, location=(0, -0.58, 1.86))
    anteojo = bpy.context.active_object
    anteojo.rotation_euler = (math.pi / 2, 0, 0)
    anteojo.scale = (1, 0.22, 1)
    anteojo.data.materials.append(marco)

    # Lámina de cristal sostenida frente al pecho, con tres franjas y el anillo del reloj.
    lam = caja('lamina', (0, -0.82, 1.02), (0.74, 0.025, 0.5), cristal('cristal', P['indigo/d70']), 0.03)
    lam.rotation_euler = (math.radians(-14), 0, 0)
    bpy.context.view_layer.update()
    base = lam.matrix_world.copy()
    franjas = []
    for i, (col, ancho) in enumerate([(P['ambar/d110'], 0.46), (P['indigo/d90'], 0.32), (C['estado/vigente/borde'], 0.4)]):
        f = caja(f'franja{i}', (0, 0, 0), (ancho, 0.02, 0.06), emisivo(f'franja{i}', col, 6.0), 0.025)
        f.matrix_world = base @ Matrix.Translation((-0.28 + ancho / 2, -0.03, 0.12 - i * 0.12))
        # El origen va al borde izquierdo para que la franja crezca de izquierda a derecha.
        f.data.transform(Matrix.Translation((ancho / 2, 0, 0)))
        f.location.x -= ancho / 2
        franjas.append(f)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.07, minor_radius=0.012)
    anillo = bpy.context.active_object
    anillo.matrix_world = base @ Matrix.Translation((0.25, -0.03, 0.13)) @ Euler((math.pi / 2, 0, 0)).to_matrix().to_4x4()
    anillo.data.materials.append(emisivo('anillo', P['indigo/d110'], 6))
    aguja = caja('aguja', (0, 0, 0), (0.01, 0.01, 0.055), emisivo('aguja', P['indigo/d110'], 6), 0.004)
    aguja.matrix_world = base @ Matrix.Translation((0.25, -0.035, 0.155))

    # Animación: respira; las franjas se fijan una tras otra; el visor se enciende.
    clave(cuerpo, 'scale', [(1, 0.97), (14, 1.015), (26, 1.0)], 2)
    for i, f in enumerate(franjas):
        ini = 26 + i * 9
        f.scale = (0.02, 1, 1)
        f.keyframe_insert('scale', frame=1)
        f.keyframe_insert('scale', frame=ini)
        f.scale = (1, 1, 1)
        f.keyframe_insert('scale', frame=ini + 14)
    nv = visor.node_tree.nodes['Principled BSDF'].inputs['Emission Strength']
    for f, val in [(1, 0.2), (14, 0.2), (22, 2.4), (32, 1.5)]:
        nv.default_value = val
        nv.keyframe_insert('default_value', frame=f)
    clave_valor(piel, 'latido', [(1, 0.8), (30, 0.8), (40, 2.2), (DUR, 1.6)])
    suavizar_claves()
    return (0, 0, 1.3), P['indigo/d15']


def main():
    cual = sys.argv[1]
    o = args()
    s = limpiar()
    apuntar, charco = {'residente': residente, 'administracion': administracion}[cual]()
    sombra_contacto(charco)
    escena(s, o, apuntar)
    salida = AQUI / 'render' / f'personaje-{cual}'
    salida.mkdir(parents=True, exist_ok=True)
    for f in range(o['frames'][0], o['frames'][1] + 1, o['paso']):
        s.frame_set(f)
        s.render.filepath = str(salida / f'{f:04d}.png')
        bpy.ops.render.render(write_still=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(AQUI / f'personaje-{cual}.blend'))
    print('ok', cual, o['frames'])


if __name__ == '__main__':
    main()
