"""El Pase como objeto 3D: recursos pase-3d-objeto y pase-3d-latir.

Piezas (todas en el plano XZ, de frente a la cámara en -Y; 1 px = 0,01 u):
  root      Empty que sube distancia/subida en «aparecer» y lleva la propiedad «opacidad».
  tarjeta   rectángulo redondeado (radio tarjeta) + Solidify + Bevel, material membrana (opaco).
  borde-sin anillo discontinuo (estado/sin-confirmar/borde).  borde  anillo continuo cuyo color cambia de estado.
  punto     disco de estado.  brillo  disco encima con estado/vigente/texto que late.
  pista / barra   vigencia (la barra escala en X desde su extremo izquierdo).
  corte     línea de revocar (escala en X desde la izquierda).
  evidencia solo en pase-3d-latir: «Confirmó Lector Portería · 3:58 p. m.» en JetBrains Mono.

Clips de pase-3d-objeto (frame inicial s, duración del token d; se renderiza s … s + d):
  aparecer s=1, confirmar s=60, latir s=120, caducar s=240, revocar s=300.
"""
import math

import bmesh
import bpy

import kino3d as k

ANCHO, ALTO, GROSOR = 3.6, 1.32, 0.06
R = k.TOKENS['radio']['tarjeta'] * k.PX
PAD = (k.TOKENS['espacio']['m'] + k.TOKENS['espacio']['2xs']) * k.PX
LINEA = k.TOKENS['linea']['foco'] * k.PX * 0.6  # banda del borde: 1,2 px de la escala de la tarjeta
TRAZO, HUECO = k.TOKENS['espacio']['2xs'] * k.PX, k.TOKENS['espacio']['2xs'] * k.PX
Y_FRENTE = -GROSOR / 2

CLIPS = {
    'aparecer': (1, 'aparecer/duracion'),
    'confirmar': (60, 'aparecer/duracion'),
    'latir': (120, 'latir/duracion'),
    'caducar': (240, 'caducar/duracion'),
    'revocar': (300, 'revocar/duracion'),
}


# Para el visor web (glTF no anima materiales): estados de cada clip, piezas visibles y colores por estado.
ESTADOS_CLIP = {'aparecer': ('sin-confirmar', 'sin-confirmar'), 'confirmar': ('sin-confirmar', 'vigente'),
                'latir': ('vigente', 'vigente'), 'caducar': ('vigente', 'vencido'), 'revocar': ('vigente', 'revocado')}
CURVA_CLIP = {'aparecer': 'aparecer/curva', 'confirmar': 'aparecer/curva', 'latir': 'latir/curva',
              'caducar': 'caducar/curva', 'revocar': 'revocar/curva'}
PIEZAS_POR_ESTADO = {'sin-confirmar': ['tarjeta', 'borde-sin', 'punto'],
                     'vigente': ['tarjeta', 'borde', 'punto', 'brillo', 'pista', 'barra'],
                     'vencido': ['tarjeta', 'borde', 'punto', 'pista'],
                     'revocado': ['tarjeta', 'borde', 'punto', 'corte']}
COLOR_POR_ESTADO = {
    'sin-confirmar': {'punto': 'estado/sin-confirmar/borde', 'tarjeta': 'superficie/membrana'},
    'vigente': {'borde': 'estado/vigente/borde', 'punto': 'estado/vigente/borde', 'tarjeta': 'superficie/membrana'},
    'vencido': {'borde': 'estado/vencido/borde', 'punto': 'estado/vencido/borde', 'tarjeta': 'superficie/membrana'},
    'revocado': {'borde': 'estado/revocado/borde', 'punto': 'estado/revocado/borde', 'tarjeta': 'superficie/base'},
}
TOKEN_PIEZA = {'tarjeta': 'superficie/membrana', 'borde-sin': 'estado/sin-confirmar/borde', 'borde': 'estado/vigente/borde',
               'punto': 'estado/vigente/borde', 'brillo': 'estado/vigente/texto', 'pista': 'superficie/elevada',
               'barra': 'estado/vigente/borde', 'corte': 'estado/revocado/texto', 'evidencia': 'estado/vigente/texto'}


def tokens_usados():
    t = set(TOKEN_PIEZA.values())
    for c in COLOR_POR_ESTADO.values():
        t |= set(c.values())
    return sorted(t)


def rango(clip):
    s, token = CLIPS[clip]
    return s, s + k.dur(token)


# Geometría --------------------------------------------------------------------------
def perimetro(w, h, r, paso=0.01):
    """Puntos (x, z) del rectángulo redondeado, antihorario, espaciados ~paso."""
    esquinas = [(w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90), (-w / 2 + r, -h / 2 + r, 180), (w / 2 - r, -h / 2 + r, 270)]
    pts = []
    for i, (cx, cz, a0) in enumerate(esquinas):
        n = max(8, int(math.pi / 2 * r / paso))
        for j in range(n):
            a = math.radians(a0 + 90 * j / n)
            pts.append((cx + r * math.cos(a), cz + r * math.sin(a)))
        # tramo recto hasta la esquina siguiente
        ax = math.radians(a0 + 90)
        x0, z0 = cx + r * math.cos(ax), cz + r * math.sin(ax)
        nx, nz, na = esquinas[(i + 1) % 4]
        x1, z1 = nx + r * math.cos(math.radians(na)), nz + r * math.sin(math.radians(na))
        largo = math.hypot(x1 - x0, z1 - z0)
        m = max(1, int(largo / paso))
        for j in range(m):
            pts.append((x0 + (x1 - x0) * j / m, z0 + (z1 - z0) * j / m))
    return pts


def malla(nombre, verts, caras):
    me = bpy.data.meshes.new(nombre)
    me.from_pydata(verts, [], caras)
    me.update()
    ob = bpy.data.objects.new(nombre, me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def banda(nombre, pts, ancho, y, discontinua=False):
    """Banda plana a lo largo del perímetro, hacia adentro. Discontinua: trazo y hueco de espacio/2xs."""
    n = len(pts)
    verts, caras, largo = [], [], 0.0
    for i, (x, z) in enumerate(pts):
        xa, za = pts[i - 1]
        xb, zb = pts[(i + 1) % n]
        tx, tz = xb - xa, zb - za
        l = math.hypot(tx, tz) or 1
        nx, nz = -tz / l, tx / l  # normal hacia adentro en recorrido antihorario
        verts += [(x, y, z), (x + nx * ancho, y, z + nz * ancho)]
    for i in range(n):
        j = (i + 1) % n
        x0, z0 = pts[i]
        x1, z1 = pts[j]
        seg = math.hypot(x1 - x0, z1 - z0)
        medio = largo + seg / 2
        largo += seg
        if discontinua and int(medio / TRAZO) % 2:
            continue
        caras.append((2 * i, 2 * j, 2 * j + 1, 2 * i + 1))
    return malla(nombre, verts, caras)


def rect_plano(nombre, x0, z0, w, h, y):
    return malla(nombre, [(0, y, 0), (w, y, 0), (w, y, h), (0, y, h)], [(0, 1, 2, 3)]), (x0, z0)


def disco(nombre, cx, cz, r, y, lados=48):
    verts = [(cx, y, cz)] + [(cx + r * math.cos(2 * math.pi * i / lados), y, cz + r * math.sin(2 * math.pi * i / lados)) for i in range(lados)]
    caras = [(0, 1 + (i + 1) % lados, 1 + i) for i in range(lados)]
    return malla(nombre, verts, caras)


# Etapas ---------------------------------------------------------------------------------
def escena(modo, reducido):
    k.vaciar()
    sc = bpy.context.scene
    if modo == 'objeto':
        k.configurar(sc, 1920, 1080, 1, rango('revocar')[1], transparente=True)
    else:
        k.configurar(sc, 1080, 1080, 1, 1 if reducido else 1 + k.dur('latir/duracion'), transparente=True)
    sc['kino_recurso'] = f'pase-3d-{modo}' + ('.reducido' if reducido else '')


def modelado(modo, reducido):
    root = bpy.data.objects.new('root', None)
    bpy.context.scene.collection.objects.link(root)
    root['opacidad'] = 1.0
    root.id_properties_ui('opacidad').update(min=0.0, max=1.0)

    pts = perimetro(ANCHO, ALTO, R)
    bm = bmesh.new()
    vs = [bm.verts.new((x, 0, z)) for x, z in pts]
    bm.faces.new(vs)
    me = bpy.data.meshes.new('tarjeta')
    bm.to_mesh(me)
    bm.free()
    tarjeta = bpy.data.objects.new('tarjeta', me)
    bpy.context.scene.collection.objects.link(tarjeta)
    sol = tarjeta.modifiers.new('grosor', 'SOLIDIFY')
    sol.thickness, sol.offset = GROSOR, 0.0
    bev = tarjeta.modifiers.new('canto', 'BEVEL')
    bev.width, bev.segments, bev.limit_method = GROSOR / 4, 3, 'ANGLE'

    y = Y_FRENTE - 0.002
    piezas = [tarjeta, banda('borde-sin', pts, LINEA, y, discontinua=True), banda('borde', pts, LINEA, y)]
    cx, cz, rp = ANCHO / 2 - PAD - 0.06, ALTO / 2 - PAD - 0.06, k.TOKENS['espacio']['s'] * k.PX / 2
    piezas += [disco('punto', cx, cz, rp, y), disco('brillo', cx, cz, rp, y - 0.001)]
    wb = ANCHO - 2 * PAD
    hb = k.TOKENS['espacio']['2xs'] * k.PX
    pista, _ = rect_plano('pista', 0, 0, wb, hb, y)
    barra, _ = rect_plano('barra', 0, 0, wb, hb, y - 0.001)
    for ob in (pista, barra):
        ob.location = (-wb / 2, 0, -ALTO / 2 + PAD)
    corte, _ = rect_plano('corte', 0, 0, ANCHO, LINEA * 1.6, y - 0.002)
    corte.location = (-ANCHO / 2, 0, 0.02)
    piezas += [pista, barra, corte]
    if modo == 'latir':
        piezas.append(texto_evidencia(y))
    for ob in piezas:
        ob.parent = root

    # Cámara fija en tres cuartos y luz de la marca (texto/primario). No se mueven.
    cam = bpy.data.objects.new('camara', bpy.data.cameras.new('camara'))
    bpy.context.scene.collection.objects.link(cam)
    cam.data.lens = 50
    distancia = 7.2 if modo == 'objeto' else 6.2
    cam.location = (distancia * math.sin(math.radians(14)), -distancia * math.cos(math.radians(14)), 0.9)
    mirar = cam.constraints.new('TRACK_TO')
    mirar.target, mirar.track_axis, mirar.up_axis = root, 'TRACK_NEGATIVE_Z', 'UP_Y'
    bpy.context.scene.camera = cam
    for nombre, pos, energia, tam in (('clave', (-2.5, -4, 4), 900, 4), ('contra', (3, 3, 2.5), 250, 3)):
        luz = bpy.data.objects.new(nombre, bpy.data.lights.new(nombre, 'AREA'))
        luz.data.energy, luz.data.size = energia, tam
        luz.data.color = k.color('texto/primario')[:3]
        luz.location = pos
        bpy.context.scene.collection.objects.link(luz)
        c = luz.constraints.new('TRACK_TO')
        c.target, c.track_axis, c.up_axis = root, 'TRACK_NEGATIVE_Z', 'UP_Y'
    mundo = bpy.data.worlds.new('mundo')
    mundo.use_nodes = True
    mundo.node_tree.nodes['Background'].inputs['Color'].default_value = k.color('superficie/abismo')
    mundo.node_tree.nodes['Background'].inputs['Strength'].default_value = 1.0
    bpy.context.scene.world = mundo


def texto_evidencia(y):
    from fuentes import ttf
    cu = bpy.data.curves.new('evidencia', 'FONT')
    cu.body = 'Confirmó Lector Portería · 3:58 p. m.'
    cu.font = bpy.data.fonts.load(str(ttf('jetbrains-mono')))
    cu.size = 12 * k.PX * 1.4
    ob = bpy.data.objects.new('evidencia', cu)
    bpy.context.scene.collection.objects.link(ob)
    ob.rotation_euler = (math.radians(90), 0, 0)
    ob.location = (-ANCHO / 2 + PAD, y, -0.05)
    return ob


def material_plano(nombre, token):
    """Marca plana: emisión del token (sale con su hex exacto) mezclada con transparencia.
    alfa = root['opacidad'] × valor «local» del material (ambos animables)."""
    m = bpy.data.materials.new(nombre)
    m.use_nodes = True
    m.surface_render_method = 'BLENDED'
    nt = m.node_tree
    nt.nodes.clear()
    salida = nt.nodes.new('ShaderNodeOutputMaterial')
    mezcla = nt.nodes.new('ShaderNodeMixShader')
    transp = nt.nodes.new('ShaderNodeBsdfTransparent')
    em = nt.nodes.new('ShaderNodeEmission')
    em.name = 'color'
    em.inputs['Color'].default_value = k.color(token)
    em.inputs['Strength'].default_value = 1.0
    local = nt.nodes.new('ShaderNodeValue')
    local.name = 'local'
    local.outputs[0].default_value = 1.0
    raiz = nt.nodes.new('ShaderNodeValue')
    raiz.name = 'raiz'
    d = raiz.outputs[0].driver_add('default_value').driver
    v = d.variables.new()
    v.name, v.type = 'op', 'SINGLE_PROP'
    v.targets[0].id = bpy.data.objects['root']
    v.targets[0].data_path = '["opacidad"]'
    d.expression = 'op'
    mult = nt.nodes.new('ShaderNodeMath')
    mult.operation = 'MULTIPLY'
    nt.links.new(raiz.outputs[0], mult.inputs[0])
    nt.links.new(local.outputs[0], mult.inputs[1])
    nt.links.new(mult.outputs[0], mezcla.inputs['Fac'])
    nt.links.new(transp.outputs[0], mezcla.inputs[1])
    nt.links.new(em.outputs[0], mezcla.inputs[2])
    nt.links.new(mezcla.outputs[0], salida.inputs['Surface'])
    return m


def materiales(modo, reducido):
    tarjeta = k.material('tarjeta', 'superficie/membrana', rugosidad=0.35)
    bsdf = tarjeta.node_tree.nodes['Principled BSDF']
    raiz = tarjeta.node_tree.nodes.new('ShaderNodeValue')
    raiz.name = 'raiz'
    d = raiz.outputs[0].driver_add('default_value').driver
    v = d.variables.new()
    v.name, v.type = 'op', 'SINGLE_PROP'
    v.targets[0].id = bpy.data.objects['root']
    v.targets[0].data_path = '["opacidad"]'
    d.expression = 'op'
    tarjeta.node_tree.links.new(raiz.outputs[0], bsdf.inputs['Alpha'])
    # Opaca con fundido por tramado: si fuera translúcida, EEVEE la ordena por origen y tapa la barra y el punto.
    tarjeta.surface_render_method = 'DITHERED'
    bpy.data.objects['tarjeta'].data.materials.append(tarjeta)
    for nombre, token in TOKEN_PIEZA.items():
        if nombre == 'tarjeta':
            continue
        ob = bpy.data.objects.get(nombre)
        if ob:
            ob.data.materials.append(material_plano(nombre, token))


# Animación ------------------------------------------------------------------------------
def local(nombre):
    return bpy.data.materials[nombre].node_tree.nodes['local'].outputs[0]


def color_em(nombre):
    return bpy.data.materials[nombre].node_tree.nodes['color'].inputs['Color']


def base_tarjeta():
    return bpy.data.materials['tarjeta'].node_tree.nodes['Principled BSDF'].inputs['Base Color']


def fijar_color(socket, t, token):
    for i, c in enumerate(k.color(token)[:3]):
        k.fijar(socket, 'default_value', i, t, c)


def tramo_color(socket, t0, t1, desde, hasta, curva):
    for i, (a, b) in enumerate(zip(k.color(desde)[:3], k.color(hasta)[:3])):
        k.tramo(socket, 'default_value', i, t0, t1, a, b, curva)


def estado_fijo(t, estado):
    """Deja todas las piezas en un estado desde el frame t (inicio de un clip)."""
    root = bpy.data.objects['root']
    k.fijar(root, 'location', 2, t, 0.0)
    k.fijar(root, '["opacidad"]', -1, t, 1.0)
    sin = estado == 'sin-confirmar'
    k.fijar(local('borde-sin'), 'default_value', -1, t, 1.0 if sin else 0.0)
    k.fijar(local('borde'), 'default_value', -1, t, 0.0 if sin else 1.0)
    fijar_color(color_em('borde'), t, 'estado/vigente/borde')
    fijar_color(color_em('punto'), t, 'estado/sin-confirmar/borde' if sin else 'estado/vigente/borde')
    fijar_color(base_tarjeta(), t, 'superficie/membrana')
    k.fijar(local('brillo'), 'default_value', -1, t, 0.0)
    for n in ('pista', 'barra'):
        k.fijar(local(n), 'default_value', -1, t, 0.0 if sin else 1.0)
    k.fijar(bpy.data.objects['barra'], 'scale', 0, t, 1.0)
    k.fijar(local('corte'), 'default_value', -1, t, 0.0)
    k.fijar(bpy.data.objects['corte'], 'scale', 0, t, 0.0)


def animacion(modo, reducido):
    if modo == 'latir':
        return animacion_latir(reducido)
    root = bpy.data.objects['root']
    # aparecer: entra en sin confirmar (nunca vigente). Sube distancia/subida y funde; reducido: solo funde.
    s, f = rango('aparecer')
    estado_fijo(s, 'sin-confirmar')
    k.tramo(root, '["opacidad"]', -1, s, f, 0.0, 1.0, 'aparecer/curva')
    if not reducido:
        k.tramo(root, 'location', 2, s, f, -k.SUBIDA, 0.0, 'aparecer/curva')
    # confirmar: el lector responde. Borde discontinuo → continuo, punto y barra en vigente.
    s, f = rango('confirmar')
    estado_fijo(s, 'sin-confirmar')
    k.tramo(local('borde-sin'), 'default_value', -1, s, f, 1.0, 0.0, 'aparecer/curva')
    k.tramo(local('borde'), 'default_value', -1, s, f, 0.0, 1.0, 'aparecer/curva')
    tramo_color(color_em('punto'), s, f, 'estado/sin-confirmar/borde', 'estado/vigente/borde', 'aparecer/curva')
    for n in ('pista', 'barra'):
        k.tramo(local(n), 'default_value', -1, s, f, 0.0, 1.0, 'aparecer/curva')
    # latir: un ciclo; el último frame iguala al primero. Reducido: punto fijo.
    s, f = rango('latir')
    estado_fijo(s, 'vigente')
    if not reducido:
        m = s + k.dur('latir/duracion') // 2
        k.tramos_encadenados(local('brillo'), 'default_value', -1, [(s, 0.0), (m, 1.0), (f, 0.0)], 'latir/curva')
    # caducar: la barra se vacía; el borde y el punto pasan a vencido. Reducido: la barra funde.
    s, f = rango('caducar')
    estado_fijo(s, 'vigente')
    if reducido:
        k.tramo(local('barra'), 'default_value', -1, s, f, 1.0, 0.0, 'caducar/curva')
    else:
        k.tramo(bpy.data.objects['barra'], 'scale', 0, s, f, 1.0, 0.0, 'caducar/curva')
    tramo_color(color_em('borde'), s, f, 'estado/vigente/borde', 'estado/vencido/borde', 'caducar/curva')
    tramo_color(color_em('punto'), s, f, 'estado/vigente/borde', 'estado/vencido/borde', 'caducar/curva')
    # revocar: una línea cruza y apaga la tarjeta. Reducido: sin línea, mismo cambio de estado.
    s, f = rango('revocar')
    estado_fijo(s, 'vigente')
    if not reducido:
        k.fijar(local('corte'), 'default_value', -1, s, 1.0)
        k.tramo(bpy.data.objects['corte'], 'scale', 0, s, f, 0.0, 1.0, 'revocar/curva')
    tramo_color(color_em('borde'), s, f, 'estado/vigente/borde', 'estado/revocado/borde', 'revocar/curva')
    tramo_color(color_em('punto'), s, f, 'estado/vigente/borde', 'estado/revocado/borde', 'revocar/curva')
    tramo_color(base_tarjeta(), s, f, 'superficie/membrana', 'superficie/base', 'revocar/curva')
    k.tramo(local('barra'), 'default_value', -1, s, f, 1.0, 0.0, 'revocar/curva')
    k.tramo(local('pista'), 'default_value', -1, s, f, 1.0, 0.0, 'revocar/curva')


def animacion_latir(reducido):
    estado_fijo(1, 'vigente')
    if not reducido:
        s, d = 1, k.dur('latir/duracion')
        k.tramos_encadenados(local('brillo'), 'default_value', -1, [(s, 0.0), (s + d // 2, 1.0), (s + d, 0.0)], 'latir/curva')
