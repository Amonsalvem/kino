"""conjunto-noche-lector-confirma: vía de acceso y portería de un conjunto genérico, de noche.

Sin personas, sin vehículos y sin placas. Cámara fija. La talanquera queda quieta (pregunta pendiente del inventario).
Lo único que cambia: el indicador del lector pasa de estado/sin-confirmar/borde a estado/vigente/borde con
«aparecer» (aparecer/duracion, aparecer/curva). Frames 1 … 1 + aparecer/duracion.
"""
import math

import bpy

import kino3d as k


def escena(modo, reducido):
    k.vaciar()
    sc = bpy.context.scene
    k.configurar(sc, 1920, 1080, 1, 1 + k.dur('aparecer/duracion'), transparente=False)
    sc['kino_recurso'] = 'conjunto-noche-lector-confirma' + ('.reducido' if reducido else '')


def caja(nombre, centro, tam, bisel=0.04):
    bpy.ops.mesh.primitive_cube_add(size=1, location=centro)
    ob = bpy.context.active_object
    ob.name = nombre
    ob.scale = tam
    bpy.ops.object.transform_apply(scale=True)
    b = ob.modifiers.new('bisel', 'BEVEL')
    b.width, b.segments = bisel, 3
    return ob


def modelado(modo, reducido):
    bpy.ops.mesh.primitive_plane_add(size=80, location=(0, 20, 0))
    bpy.context.active_object.name = 'suelo'
    caja('via', (0, 18, 0.01), (5, 60, 0.02), bisel=0.005)
    # Muros del conjunto a los lados de la vía, con una sección espejada.
    muro = caja('muro', (5.5, 16, 0.9), (4, 0.3, 1.8))
    esp = muro.modifiers.new('espejo', 'MIRROR')
    esp.use_axis = (True, False, False)
    esp.mirror_object = None
    caja('porteria', (5.2, 11.5, 1.35), (2.6, 2.6, 2.7))
    caja('techo', (5.2, 11.5, 2.8), (3.2, 3.2, 0.2))
    bpy.ops.mesh.primitive_plane_add(size=1, location=(3.89, 11.5, 1.55), rotation=(0, math.radians(90), 0))
    ventana = bpy.context.active_object
    ventana.name = 'ventana'
    ventana.scale = (0.7, 1.6, 1)
    # Talanquera: poste y brazo abajo, cruzando la vía.
    caja('poste', (2.9, 10, 0.55), (0.35, 0.35, 1.1))
    caja('brazo', (0.35, 10, 1.0), (5.0, 0.1, 0.1), bisel=0.02)
    # Lector en su pedestal, antes de la talanquera, con el indicador de frente a la vía.
    caja('lector', (2.7, 8.2, 0.7), (0.3, 0.3, 1.4))
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.02, location=(2.54, 8.2, 1.2), rotation=(0, math.radians(90), 0))
    ind = bpy.context.active_object
    ind.name = 'indicador'
    sub = ind.modifiers.new('suave', 'SUBSURF')
    sub.levels = sub.render_levels = 1

    cam = bpy.data.objects.new('camara', bpy.data.cameras.new('camara'))
    bpy.context.scene.collection.objects.link(cam)
    cam.data.lens = 35
    cam.location = (-0.8, 1.2, 1.55)
    cam.rotation_euler = (math.radians(87), 0, math.radians(-24))
    bpy.context.scene.camera = cam
    luna = bpy.data.objects.new('luna', bpy.data.lights.new('luna', 'SUN'))
    luna.data.energy = 1.4
    luna.data.color = k.color('texto/secundario')[:3]
    luna.rotation_euler = (math.radians(55), 0, math.radians(35))
    bpy.context.scene.collection.objects.link(luna)
    farol = bpy.data.objects.new('luz-porteria', bpy.data.lights.new('luz-porteria', 'AREA'))
    farol.data.energy, farol.data.size = 120, 1.2
    farol.data.color = k.color('texto/primario')[:3]
    farol.location = (3.5, 9.4, 2.5)
    farol.rotation_euler = (math.radians(180), 0, 0)
    bpy.context.scene.collection.objects.link(farol)
    mundo = bpy.data.worlds.new('noche')
    mundo.use_nodes = True
    mundo.node_tree.nodes['Background'].inputs['Color'].default_value = k.color('superficie/abismo')
    bpy.context.scene.world = mundo


def materiales(modo, reducido):
    tabla = {'suelo': 'superficie/base', 'via': 'superficie/elevada', 'muro': 'superficie/elevada', 'porteria': 'superficie/membrana',
             'techo': 'superficie/elevada', 'poste': 'superficie/membrana', 'brazo': 'texto/tenue', 'lector': 'superficie/membrana'}
    for nombre, token in tabla.items():
        bpy.data.objects[nombre].data.materials.append(k.material(nombre, token, rugosidad=0.7))
    bpy.data.objects['ventana'].data.materials.append(
        k.material('ventana', 'superficie/membrana', token_emision='texto/tenue', emision=0.4))
    bpy.data.objects['indicador'].data.materials.append(
        k.material('indicador', 'estado/sin-confirmar/borde', token_emision='estado/sin-confirmar/borde', emision=1.0))
    # Emisión 1: el indicador sale con el hex del token. Con más fuerza el verde satura hacia cian (prohibido).


def animacion(modo, reducido):
    # Completo y reducido son iguales: el cambio es de color, sin desplazamiento (ficha del inventario).
    s, f = 1, 1 + k.dur('aparecer/duracion')
    m = bpy.data.materials['indicador']
    for entrada in ('Base Color', 'Emission Color'):
        sock = k.entrada(m, entrada)
        for i, (a, b) in enumerate(zip(k.color('estado/sin-confirmar/borde')[:3], k.color('estado/vigente/borde')[:3])):
            k.tramo(sock, 'default_value', i, s, f, a, b, 'aparecer/curva')
