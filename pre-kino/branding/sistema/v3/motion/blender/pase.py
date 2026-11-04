"""El Pase como objeto 3D (versión 2): recursos pase-3d-objeto y pase-3d-latir.

Es la tarjeta de <kino-pase> (paquetes/kino-motion/src/web/componentes/pase.ts) llevada a 3D, con las mismas partes
de la partitura (tarjeta, borde, chip, punto, barra, corte, tachado, nota) y los mismos datos de muestra que las
composiciones Remotion. Medidas en px del sistema (1 px = 0,01 u), plano XZ, de frente a la cámara en −Y.

  root           Empty: sube, escala y se asienta al aparecer; lleva «opacidad» (la de .tarjeta en la web).
  tarjeta        membrana de 360 × 132 px, 6 px de grosor, canto biselado con perfil redondo.
  borde-sin      borde discontinuo (sin confirmar).  borde  borde continuo, color del estado; escribe el resplandor.
  chip-<estado>  grupo por estado: fondo, borde, punto y texto (Archivo 700, 13 px). Se funden al cambiar de estado.
  brillo         disco sobre el punto del chip vigente: late con latir.
  quien, tachado nombre (Archivo 700, 17 px) y la línea de «usar».
  dato-<estado>  casa y franja (JetBrains Mono 13 px), una por estado.
  nota-confirmo, nota-revoco   la evidencia (JetBrains Mono 12 px).
  pista, barra   vigencia (4 px). corte: la línea de revocar.
  La sombra es la del token relieve/membrana (0 12 px 32 px −20 px, negro), aplicada en el compositor.

Clips (partitura de @kino/motion; se renderiza s … s + d):
  aparecer · confirmar · latir · avisar · caducar · usar · revocar
"""
import math

import bmesh
import bpy

import kino3d as k

P = k.PX
ANCHO, ALTO, GROSOR = 360 * P, 132 * P, 6 * P
R = k.FORMA['radio']['tarjeta'] * P
R_CHIP = k.FORMA['radio']['chip'] * P
PAD = 20 * P
BISEL = 2.5 * P
LINEA = k.FORMA['linea']['fino'] * P * 1.25  # borde de 1 px (1,25 para que no se pierda al 50 % de la miniatura)
TRAZO = k.FORMA['espacio']['2xs'] * P
Y_FRENTE = -GROSOR / 2
EPS = 0.0015
Z_FILA1, Z_DATO, Z_NOTA, Z_BARRA = 33.5 * P, 3 * P, -24.5 * P, -44 * P

ESTADOS = ('sin-confirmar', 'vigente', 'por-vencer', 'vencido', 'usado', 'revocado')
TERMINALES = {'vencido', 'usado', 'revocado'}
ETIQUETA = k.PARTITURA['etiqueta']
QUIEN = 'Andrés Gómez'
DATO = {'sin-confirmar': 'Casa 14 · enviado 3:52 p. m.', 'vigente': 'Casa 14 · hoy 4:00–6:00 p. m.',
        'por-vencer': 'Casa 14 · vence 6:00 p. m.', 'vencido': 'Casa 14 · venció 6:00 p. m.',
        'usado': 'Casa 14 · entró 4:02 p. m.', 'revocado': 'Casa 14 · hoy 4:00–6:00 p. m.'}
NOTA = {'nota-confirmo': 'Confirmó Lector Portería · 3:58 p. m.', 'nota-revoco': 'Revocó Carolina Ruiz · 4:10 p. m.'}
VIGENCIA = {'vigente': 0.86, 'por-vencer': 0.1, 'vencido': 0.0, 'usado': 0.8, 'revocado': 0.86}
FACTOR_LATIR = 0.74  # la tarjeta ocupa ~72 % del cuadro de 1080
RESPLANDOR = 1.0  # fuerza de resplandor/vigente (el token completo); 0 en cualquier otro estado

# Clips: (evento de la partitura, estado inicial, estado final). aparecer y latir no son transiciones de estado.
CLIPS = {
    'aparecer': (None, None, 'sin-confirmar'),
    'confirmar': ('confirmar', 'sin-confirmar', 'vigente'),
    'latir': (None, 'vigente', 'vigente'),
    'avisar': ('avisar', 'vigente', 'por-vencer'),
    'caducar': ('caducar', 'vigente', 'vencido'),
    'usar': ('usar', 'vigente', 'usado'),
    'revocar': ('revocar', 'vigente', 'revocado'),
}
HUECO = 10  # frames entre clips en la línea de tiempo


def transicion(evento):
    return next(t for t in k.PARTITURA['transiciones'] if t['evento'] == evento)


def duracion_clip(clip):
    evento = CLIPS[clip][0]
    if clip == 'aparecer':
        return k.frames('aparecer/duracion')
    if clip == 'latir':
        return k.frames('latir/duracion')
    return k.frames(transicion(evento)['duracion'])


def curva_clip(clip):
    evento = CLIPS[clip][0]
    if clip == 'aparecer':
        return 'aparecer/curva'
    if clip == 'latir':
        return 'latir/curva'
    return transicion(evento)['curva']


def inicios():
    t, out = 1, {}
    for c in CLIPS:
        out[c] = t
        t += duracion_clip(c) + HUECO
    return out


def rango(clip):
    s = inicios()[clip]
    return s, s + duracion_clip(clip)


# Geometría ---------------------------------------------------------------------------------------
def perimetro(w, h, r, paso=0.008, cx=0.0, cz=0.0):
    """Puntos (x, z) del rectángulo redondeado, antihorario, espaciados ~paso."""
    r = min(r, w / 2, h / 2)
    esquinas = [(w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90), (-w / 2 + r, -h / 2 + r, 180), (w / 2 - r, -h / 2 + r, 270)]
    pts = []
    for i, (ex, ez, a0) in enumerate(esquinas):
        n = max(6, int(math.pi / 2 * r / paso))
        for j in range(n):
            a = math.radians(a0 + 90 * j / n)
            pts.append((cx + ex + r * math.cos(a), cz + ez + r * math.sin(a)))
        ax = math.radians(a0 + 90)
        x0, z0 = ex + r * math.cos(ax), ez + r * math.sin(ax)
        nx, nz, na = esquinas[(i + 1) % 4]
        x1, z1 = nx + r * math.cos(math.radians(na)), nz + r * math.sin(math.radians(na))
        m = max(1, int(math.hypot(x1 - x0, z1 - z0) / paso))
        for j in range(m):
            pts.append((cx + x0 + (x1 - x0) * j / m, cz + z0 + (z1 - z0) * j / m))
    return pts


def malla(nombre, verts, caras, padre=None):
    me = bpy.data.meshes.new(nombre)
    me.from_pydata(verts, [], caras)
    me.update()
    ob = bpy.data.objects.new(nombre, me)
    bpy.context.scene.collection.objects.link(ob)
    if padre:
        ob.parent = padre
    return ob


def banda(nombre, pts, ancho, y, discontinua=False, padre=None):
    """Banda plana a lo largo de un perímetro, hacia adentro. Discontinua: trazo y hueco de espacio/2xs."""
    n = len(pts)
    verts, caras, largo = [], [], 0.0
    for i, (x, z) in enumerate(pts):
        xa, za = pts[i - 1]
        xb, zb = pts[(i + 1) % n]
        tx, tz = xb - xa, zb - za
        l = math.hypot(tx, tz) or 1
        nx, nz = -tz / l, tx / l
        verts += [(x, y, z), (x + nx * ancho, y, z + nz * ancho)]
    for i in range(n):
        j = (i + 1) % n
        seg = math.hypot(pts[j][0] - pts[i][0], pts[j][1] - pts[i][1])
        medio = largo + seg / 2
        largo += seg
        if discontinua and int(medio / TRAZO) % 2:
            continue
        caras.append((2 * i, 2 * i + 1, 2 * j + 1, 2 * j))
    return malla(nombre, verts, caras, padre)


def relleno(nombre, pts, y, padre=None):
    cx = sum(p[0] for p in pts) / len(pts)
    cz = sum(p[1] for p in pts) / len(pts)
    verts = [(cx, y, cz)] + [(x, y, z) for x, z in pts]
    n = len(pts)
    caras = [(0, 1 + (i + 1) % n, 1 + i) for i in range(n)]
    return malla(nombre, verts, caras, padre)


def disco(nombre, cx, cz, r, y, padre=None, lados=40):
    return relleno(nombre, [(cx + r * math.cos(2 * math.pi * i / lados), cz + r * math.sin(2 * math.pi * i / lados)) for i in range(lados)], y, padre)


def anillo(nombre, cx, cz, r, ancho, y, padre=None, lados=40):
    pts = [(cx + r * math.cos(2 * math.pi * i / lados), cz + r * math.sin(2 * math.pi * i / lados)) for i in range(lados)]
    return banda(nombre, pts, ancho, y, padre=padre)


def rect(nombre, x0, z0, w, h, y, padre=None):
    """Rectángulo con el origen en su borde izquierdo (escala en X desde la izquierda, como transform-origin: left)."""
    ob = malla(nombre, [(0, y, -h / 2), (w, y, -h / 2), (w, y, h / 2), (0, y, h / 2)], [(0, 3, 2, 1)], padre)
    ob.location = (x0, 0, z0)
    return ob


def texto(nombre, cuerpo, familia, peso, tam_px, x, z, y, alinear='LEFT', padre=None):
    from fuentes import ttf
    cu = bpy.data.curves.new(nombre, 'FONT')
    cu.body = cuerpo
    ruta = str(ttf(familia, peso))
    fuente = next((f for f in bpy.data.fonts if f.filepath == ruta), None) or bpy.data.fonts.load(ruta)
    cu.font = fuente
    cu.size = tam_px * P
    cu.align_x, cu.align_y = alinear, 'CENTER'
    cu.extrude = 0.15 * P
    cu.resolution_u = 6
    ob = bpy.data.objects.new(nombre, cu)
    bpy.context.scene.collection.objects.link(ob)
    ob.rotation_euler = (math.radians(90), 0, 0)
    ob.location = (x, y, z)
    if padre:
        ob.parent = padre
    return ob


def grupo(nombre, padre, opacidad=1.0):
    g = bpy.data.objects.new(nombre, None)
    bpy.context.scene.collection.objects.link(g)
    g.parent = padre
    g['opacidad'] = opacidad
    g.id_properties_ui('opacidad').update(min=0.0, max=1.0)
    return g


def tarjeta_membrana(padre):
    pts = perimetro(ANCHO, ALTO, R, paso=0.02)
    bm = bmesh.new()
    vs = [bm.verts.new((x, GROSOR / 2, z)) for x, z in pts]
    cara = bm.faces.new(vs)
    ext = bmesh.ops.extrude_face_region(bm, geom=[cara])
    for v in ext['geom']:
        if isinstance(v, bmesh.types.BMVert):
            v.co.y -= GROSOR
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new('tarjeta')
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    ob = bpy.data.objects.new('tarjeta', me)
    bpy.context.scene.collection.objects.link(ob)
    ob.parent = padre
    bev = ob.modifiers.new('canto', 'BEVEL')
    bev.width, bev.segments, bev.profile = BISEL, 6, 0.62
    bev.limit_method, bev.angle_limit = 'ANGLE', math.radians(40)
    bev.harden_normals = True
    return ob


def ancho_texto(ob):
    bpy.context.view_layer.update()
    return ob.dimensions.x


# Etapas ------------------------------------------------------------------------------------------
def escena(modo, reducido):
    k.vaciar()
    sc = bpy.context.scene
    if modo == 'objeto':
        k.configurar(sc, 1920, 1080, 1, rango('revocar')[1], transparente=True, muestras=14)
        # Solo se calcula la región del Pase (con margen para la sombra y el resplandor); el resto queda transparente.
        sc.render.use_border, sc.render.use_crop_to_border = True, False
        sc.render.border_min_x, sc.render.border_max_x = 0.12, 0.88
        sc.render.border_min_y, sc.render.border_max_y = 0.14, 0.86
    else:
        k.configurar(sc, 1080, 1080, 1, 1 if reducido else 1 + k.frames('latir/duracion'), transparente=True, muestras=14)
    sc['kino_recurso'] = f'pase-3d-{modo}' + ('.reducido' if reducido else '')
    # Sin trazado de rayos en pantalla (solo reflejaría un mundo oscuro) y sombras más baratas: ~30 s por frame.
    sc.eevee.use_raytracing = False
    sc.eevee.shadow_ray_count, sc.eevee.shadow_step_count = 1, 6
    # px del sistema → px del render: la tarjeta (360 px) ocupa ~55 % de 1920 o ~72 % de 1080.
    escala_px = (0.55 * 1920 if modo == 'objeto' else 0.72 * 1080) / 360
    k.compositor(sc, brillo=(0.004, 0.012), fuerza_brillo=(1.0, 0.6), caja=escala_px)


def modelado(modo, reducido):
    sc = bpy.context.scene
    root = bpy.data.objects.new('root', None)
    sc.collection.objects.link(root)
    root['opacidad'] = 1.0
    root.id_properties_ui('opacidad').update(min=0.0, max=1.0)
    tarjeta_membrana(root)
    y = Y_FRENTE - EPS
    interior = perimetro(ANCHO - 2 * BISEL, ALTO - 2 * BISEL, R - BISEL)
    banda('borde-sin', interior, LINEA, y, discontinua=True, padre=root)
    banda('borde', interior, LINEA, y, padre=root)

    # Cabeza: nombre a la izquierda, chip a la derecha (padding 3 × 10 px, punto 6 px, gap 6 px, texto 13 px).
    x_izq, x_der = -ANCHO / 2 + PAD, ANCHO / 2 - PAD
    quien = texto('quien', QUIEN, 'archivo', 700, 17, x_izq, Z_FILA1, y, padre=root)
    w_quien = ancho_texto(quien)
    rect('tachado', x_izq, Z_FILA1 - 0.5 * P, w_quien, 2 * P, y - EPS, padre=root)
    alto_chip = (13 * 1.3 + 6 + 2) * P
    for e in ESTADOS:
        g = grupo(f'chip-{e}', root, 1.0 if e == 'sin-confirmar' else 0.0)
        t = texto(f'chip-{e}-texto', ETIQUETA[e], 'archivo', 700, 13, 0, Z_FILA1, y - EPS, alinear='RIGHT', padre=g)
        wt = ancho_texto(t)
        w = (10 + 6 + 6 + 10 + 2) * P + wt
        cx = x_der - w / 2
        t.location.x = x_der - (10 + 1) * P
        contorno = perimetro(w, alto_chip, R_CHIP, paso=0.004, cx=cx, cz=Z_FILA1)
        if not k.COLOR[f'estado/{e}/fondo'].endswith('00') or len(k.COLOR[f'estado/{e}/fondo']) == 7:
            relleno(f'chip-{e}-fondo', contorno, y, padre=g)
        banda(f'chip-{e}-borde', contorno, 1 * P, y - EPS, discontinua=(e == 'sin-confirmar'), padre=g)
        px = x_der - w + (10 + 1 + 3) * P
        if e == 'sin-confirmar':
            anillo(f'chip-{e}-punto', px, Z_FILA1, 3 * P, 1 * P, y - EPS, padre=g)
        elif e == 'revocado':
            relleno(f'chip-{e}-punto', perimetro(6 * P, 6 * P, 1 * P, paso=0.002, cx=px, cz=Z_FILA1), y - EPS, padre=g)
        else:
            disco(f'chip-{e}-punto', px, Z_FILA1, 3 * P, y - EPS, padre=g)
        if e == 'vigente':
            disco('brillo', px, Z_FILA1, 4 * P, y - 2 * EPS, padre=g)
    for e in ESTADOS:
        texto(f'dato-{e}', DATO[e], 'jetbrains-mono', 400, 13, x_izq, Z_DATO, y, padre=root)
    for n, cuerpo in NOTA.items():
        texto(n, cuerpo, 'jetbrains-mono', 400, 12, x_izq, Z_NOTA, y, padre=root)
    wb, hb = ANCHO - 2 * PAD, 4 * P
    rect('pista', x_izq, Z_BARRA, wb, hb, y, padre=root)
    rect('barra', x_izq, Z_BARRA, wb, hb, y - EPS, padre=root)
    rect('corte', -ANCHO / 2 + BISEL, 0.12 * ALTO / 2, ANCHO - 2 * BISEL, 2 * P, y - 3 * EPS, padre=root)

    # Cámara: 85 mm en tres cuartos, a la altura de la tarjeta y un poco por encima. Mira a un foco fijo.
    foco = bpy.data.objects.new('foco', None)
    sc.collection.objects.link(foco)
    cam = bpy.data.objects.new('camara', bpy.data.cameras.new('camara'))
    sc.collection.objects.link(cam)
    cam.data.lens = 85
    # Sin profundidad de campo: la tarjeta es casi plana y el DOF costaba 20 s por frame en CPU (ver README).
    cam.data.dof.use_dof = False
    sc.camera = cam
    camara_en(cam, 1.0 if modo == 'objeto' else FACTOR_LATIR)
    k.apuntar(cam, foco)
    # Luz por capas: clave (caja grande arriba a la izquierda), relleno índigo de la aurora, contraluz en tira
    # que dibuja el borde de luz superior de la membrana, y un bajo de rebote. Ninguna luz es verde.
    k.luz('clave', 'AREA', 'texto/primario', 1400, (-5.5, -7.5, 6.0), foco, tam=4.5, tam_y=3.0)
    k.luz('relleno', 'AREA', 'indigo/d32', 500, (7.5, -5.0, -0.8), foco, tam=6.0)
    k.luz('contra', 'AREA', 'texto/primario', 1600, (0.0, 2.2, 3.0), (0, 0, 0.6), tam=8.0, tam_y=0.4)
    k.luz('recorte', 'AREA', 'violeta/d45', 350, (6.0, 2.5, 1.5), foco, tam=2.0)
    mundo = bpy.data.worlds.new('mundo')
    mundo.use_nodes = True
    fondo = mundo.node_tree.nodes['Background']
    fondo.inputs['Color'].default_value = k.color('superficie/abismo')
    fondo.inputs['Strength'].default_value = 1.0
    sc.world = mundo


def camara_en(cam, factor):
    """factor 1: plano de «aparecer»; menor: más cerca (el empuje de «confirmar»)."""
    d = 15.6 * factor
    yaw, alto = math.radians(17), 1.25
    cam.location = (d * math.sin(yaw), -d * math.cos(yaw), alto * factor)


# Materiales ---------------------------------------------------------------------------------------
def token_estado(e, parte):
    return f'estado/{e}/{parte}'


def color_borde(e):
    return 'estado/vencido/borde' if e in TERMINALES else f'estado/{e}/borde'


def materiales(modo, reducido):
    ob = bpy.data.objects
    # Membrana: capa de laca (coat) que da el fresnel, sheen en el grazing, rugosidad con microvariación y relieve fino.
    m, p = k.principled('tarjeta', 'superficie/membrana', rugosidad=0.42,
                        **{'Coat Weight': 0.35, 'Coat Roughness': 0.14, 'Sheen Weight': 0.45, 'Sheen Roughness': 0.35,
                           'Sheen Tint': 'sustrato/d70', 'Subsurface Weight': 0.08, 'Subsurface Scale': 0.02,
                           'Specular IOR Level': 0.45})
    k.microvariacion(m, p, 'superficie/membrana', 'sustrato/d15', escala=2.2, rug=(0.38, 0.47), bump=0.004, escala_bump=70)
    m.node_tree.links.new(k.driver_opacidad(m.node_tree), p.inputs['Alpha'])
    ob['tarjeta'].data.materials.append(m)
    m.use_transparent_shadow = True

    def poner(nombre, token, grupo_=None, brillo=0.0):
        mm = k.marca(nombre, token, brillo=brillo)
        if grupo_:
            multiplicar_grupo(mm, grupo_)
        ob[nombre].data.materials.append(mm)
        ob[nombre].visible_shadow = False  # tinta sobre la membrana: no proyecta sombra
        return mm

    poner('borde-sin', 'estado/sin-confirmar/borde')
    poner('borde', 'estado/vigente/borde')
    poner('quien', 'texto/primario')
    poner('tachado', 'estado/usado/texto')
    for e in ESTADOS:
        g = f'chip-{e}'
        if ob.get(f'{g}-fondo'):
            poner(f'{g}-fondo', token_estado(e, 'fondo'), g)
        poner(f'{g}-borde', token_estado(e, 'borde'), g)
        poner(f'{g}-punto', token_estado(e, 'borde'), g)
        poner(f'{g}-texto', token_estado(e, 'texto'), g)
        poner(f'dato-{e}', 'texto/secundario')
    poner('brillo', 'estado/vigente/texto', 'chip-vigente')
    poner('nota-confirmo', 'estado/vigente/texto')
    poner('nota-revoco', 'estado/revocado/texto')
    poner('pista', 'superficie/elevada')
    poner('barra', 'estado/vigente/borde')
    poner('corte', 'estado/revocado/texto')


def multiplicar_grupo(m, grupo_):
    """alfa = root.opacidad × grupo.opacidad × local."""
    nt = m.node_tree
    mix = nt.nodes['Mix Shader']
    enlace = next(l for l in nt.links if l.to_socket == mix.inputs['Fac'])
    previo = enlace.from_socket
    nt.links.remove(enlace)
    mu = nt.nodes.new('ShaderNodeMath')
    mu.operation = 'MULTIPLY'
    nt.links.new(previo, mu.inputs[0])
    nt.links.new(k.driver_opacidad(nt, objeto=grupo_), mu.inputs[1])
    nt.links.new(mu.outputs[0], mix.inputs['Fac'])


# Estados ------------------------------------------------------------------------------------------
def canales():
    """Canales animables: nombre → (dueño, ruta, índice). El valor de cada estado lo da valor()."""
    ob, mat = bpy.data.objects, bpy.data.materials

    def local(n):
        return (k.nodo(mat[n], 'local').outputs[0], 'default_value', -1)
    c = {'root.opacidad': (ob['root'], '["opacidad"]', -1)}
    for e in ESTADOS:
        c[f'chip-{e}'] = (ob[f'chip-{e}'], '["opacidad"]', -1)
        c[f'dato-{e}'] = local(f'dato-{e}')
    for n in ('borde-sin', 'borde', 'nota-confirmo', 'nota-revoco', 'pista', 'barra', 'corte', 'tachado', 'brillo'):
        c[n] = local(n)
    c['resplandor'] = (k.resplandor(bpy.context.scene), 'default_value', -1)
    c['brillo.brillo'] = (k.nodo(mat['brillo'], 'brillo').outputs[0], 'default_value', -1)
    c['barra.escala'] = (ob['barra'], 'scale', 0)
    c['corte.escala'] = (ob['corte'], 'scale', 0)
    c['tachado.escala'] = (ob['tachado'], 'scale', 0)
    c['nota.z'] = None  # se anima aparte (subida)
    return c


COLORES = ('borde.color', 'barra.color', 'tarjeta.color')


def socket_color(nombre):
    mat = bpy.data.materials
    if nombre == 'borde.color':
        return k.nodo(mat['borde'], 'color').outputs[0]
    if nombre == 'barra.color':
        return k.nodo(mat['barra'], 'color').outputs[0]
    return None


def valor(e, canal):
    """Valor de un canal en un estado estable (lo que la web pinta en ese estado)."""
    vig = e in ('vigente', 'por-vencer')
    tabla = {
        'root.opacidad': 0.72 if e in TERMINALES else 1.0,
        'borde-sin': 1.0 if e == 'sin-confirmar' else 0.0,
        'borde': 0.0 if e == 'sin-confirmar' else 1.0,
        'nota-confirmo': 1.0 if vig else 0.0,
        'nota-revoco': 1.0 if e == 'revocado' else 0.0,
        'pista': 0.0 if e == 'sin-confirmar' else 1.0,
        'barra': 0.0 if e == 'sin-confirmar' else 1.0,
        'corte': 1.0 if e == 'revocado' else 0.0,
        'tachado': 1.0 if e == 'usado' else 0.0,
        'brillo': 0.0,
        'resplandor': RESPLANDOR if e == 'vigente' else 0.0,
        'brillo.brillo': 0.0,
        'barra.escala': VIGENCIA.get(e, 0.86),
        'corte.escala': 1.0 if e == 'revocado' else 0.0,
        'tachado.escala': 1.0 if e == 'usado' else 0.0,
        'borde.color': color_borde(e) if e != 'sin-confirmar' else 'estado/vigente/borde',
        'barra.color': 'estado/vigente/borde' if e == 'vigente' else 'estado/por-vencer/borde' if e == 'por-vencer' else 'estado/vencido/borde',
        'tarjeta.color': ('superficie/base', 'superficie/elevada') if e == 'revocado' else ('superficie/membrana', 'sustrato/d15'),
    }
    if canal.startswith('chip-'):
        return 1.0 if canal == f'chip-{e}' else 0.0
    if canal.startswith('dato-'):
        return 1.0 if canal == f'dato-{e}' else 0.0
    return tabla[canal]


def rampa_tarjeta():
    """La tarjeta cambia de base en «revocar» (superficie/base): se anima el color claro de su rampa."""
    return bpy.data.materials['tarjeta'].node_tree.nodes['rampa-base'].color_ramp.elements


def estado_fijo(t, e, camara_factor):
    for nombre, c in canales().items():
        if c:
            k.fijar(*c, t, valor(e, nombre))
    for nombre in ('borde.color', 'barra.color'):
        k.fijar_color(socket_color(nombre), t, valor(e, nombre))
    el = rampa_tarjeta()
    for j, tono in enumerate(valor(e, 'tarjeta.color')):
        for i, cc in enumerate(k.rgb(tono)):
            k.fijar(el[j], 'color', i, t, cc)
    root = bpy.data.objects['root']
    k.fijar(root, 'location', 2, t, 0.0)
    k.fijar(root, 'rotation_euler', 0, t, 0.0)
    for i in range(3):
        k.fijar(root, 'scale', i, t, 1.0)
    for n in NOTA:
        k.fijar(bpy.data.objects[n], 'location', 2, t, Z_NOTA)
    cam = bpy.data.objects['camara']
    camara_en(cam, camara_factor)
    for i in range(3):
        k.fijar(cam, 'location', i, t, cam.location[i])


def transicionar(s, f, a, b, nombre_curva, pistas, reducido):
    """Cambia de a a b entre s y f con la curva del verbo. Las pistas de la partitura deciden cómo:
    escalaX dibuja o vacía (en reducido, funde); y hace subir la nota (en reducido, solo funde)."""
    partes_escala = {p['parte'] for p in pistas if p['propiedad'] == 'escalaX'}
    nota_sube = any(p['parte'] == 'nota' and p['propiedad'] == 'y' for p in pistas)
    for nombre, c in canales().items():
        if not c:
            continue
        v0, v1 = valor(a, nombre), valor(b, nombre)
        parte = nombre.split('.')[0]
        if nombre.endswith('.escala') and parte in partes_escala and reducido:
            # Reducido: la línea no se dibuja ni la barra se vacía; aparecen o se van por fundido.
            k.fijar(*c, s, v1 if v1 > 0 else v0)
            op = canales()[parte]
            k.tramo(*op, s, f, 1.0 if v0 > 0 else 0.0, 1.0 if v1 > 0 else 0.0, nombre_curva)
            continue
        if nombre in [p for p in (('corte', 'tachado') if not reducido else ())] and v1 > v0:
            k.fijar(*c, s, 1.0)  # la línea es visible desde el inicio: lo que se anima es su escala
            continue
        if v0 != v1:
            if reducido and parte in partes_escala and nombre == parte:
                continue  # ya lo funde la rama anterior
            familia = nombre.split('-')[0]
            if familia in ('chip', 'dato', 'nota') and cambia_texto(a, b, familia):
                # Fundido a través: el texto que sale se va en la primera mitad y el que entra llega en la segunda.
                m = (s + f) // 2
                if v1 < v0:
                    k.tramo(*c, s, m, v0, v1, nombre_curva)
                else:
                    k.fijar(*c, s, v0)
                    k.tramo(*c, m, f, v0, v1, nombre_curva)
                continue
            k.tramo(*c, s, f, v0, v1, nombre_curva)
    for nombre in ('borde.color', 'barra.color'):
        if valor(a, nombre) != valor(b, nombre):
            k.tramo_color(socket_color(nombre), s, f, valor(a, nombre), valor(b, nombre), nombre_curva)
    if valor(a, 'tarjeta.color') != valor(b, 'tarjeta.color'):
        el = rampa_tarjeta()
        for j in range(2):
            for i, (x, y) in enumerate(zip(k.rgb(valor(a, 'tarjeta.color')[j]), k.rgb(valor(b, 'tarjeta.color')[j]))):
                k.tramo(el[j], 'color', i, s, f, x, y, nombre_curva)
    if nota_sube and not reducido:
        for n in NOTA:
            if valor(b, n) > valor(a, n):
                k.tramo(bpy.data.objects[n], 'location', 2, s, f, Z_NOTA - k.SUBIDA, Z_NOTA, nombre_curva)


def cambia_texto(a, b, familia):
    """True si en la transición un texto de la familia sale y otro entra (hay que no encimarlos)."""
    nombres = [n for n in canales() if n.split('-')[0] == familia and '.' not in n]
    sale = any(valor(a, n) > valor(b, n) for n in nombres)
    entra = any(valor(b, n) > valor(a, n) for n in nombres)
    return sale and entra


def latido(s, reducido, respira=True):
    """Un ciclo de latir: opacidad 0 → 1 → 0 sobre el tiempo con curva/latir (igual que kino-estado en la web).
    El halo del borde respira con el mismo ciclo. Reducido: el punto queda quieto."""
    if reducido:
        return
    n = k.frames('latir/duracion')
    e = k.bezier('latir/curva')

    def tri(i):
        u = e(i / n)
        return 2 * u if u < 0.5 else 2 - 2 * u
    c = canales()
    k.hornear(*c['brillo'], s, n, tri)
    k.hornear(*c['brillo.brillo'], s, n, lambda i: 2.2 * tri(i))
    if respira:
        k.hornear(*c['resplandor'], s, n, lambda i: RESPLANDOR * (1 + 0.18 * tri(i)))


def animacion(modo, reducido):
    if modo == 'latir':
        estado_fijo(1, 'vigente', FACTOR_LATIR)
        latido(1, reducido)
        ocultar_invisibles()
        return
    root = bpy.data.objects['root']
    cam = bpy.data.objects['camara']
    CERCA = 0.94
    for clip, (evento, a, b) in CLIPS.items():
        s, f = rango(clip)
        nombre_curva = curva_clip(clip)
        if clip == 'aparecer':
            # Entra como <kino-pase entrar>: funde, sube distancia/subida y escala desde escala/entrada, con curva/crecer.
            # Movimiento secundario: la membrana llega inclinada y se asienta con resorte/pase.
            estado_fijo(s, 'sin-confirmar', 1.0)
            k.tramo(root, '["opacidad"]', -1, s, f, 0.0, 1.0, nombre_curva)
            if not reducido:
                k.tramo(root, 'location', 2, s, f, -k.SUBIDA, 0.0, nombre_curva)
                e0 = k.MOTION['escala']['entrada']
                for i in range(3):
                    k.tramo(root, 'scale', i, s, f, e0, 1.0, nombre_curva)
                k.resorte(root, 'rotation_euler', 0, s, math.radians(9), 0.0, 'pase')
            continue
        if clip == 'latir':
            estado_fijo(s, 'vigente', CERCA)
            latido(s, reducido)
            continue
        t = transicion(evento)
        assert t['a'] == b and a in t['de'], (clip, t)
        estado_fijo(s, a, 1.0 if clip == 'confirmar' else CERCA)
        transicionar(s, f, a, b, nombre_curva, t['pistas'], reducido)
        if clip == 'confirmar' and not reducido:
            # Cámara motivada: al quedar vigente, el Pase gana atención. Se acerca con resorte/pase.
            lejos = tuple(cam.location)
            camara_en(cam, CERCA)
            cerca = tuple(cam.location)
            for i in range(3):
                k.resorte(cam, 'location', i, s, lejos[i], cerca[i], 'pase')
        if clip == 'confirmar' and reducido:
            camara_en(cam, CERCA)
            for i in range(3):
                k.fijar(cam, 'location', i, s, cam.location[i])
    ocultar_invisibles()


def ocultar_invisibles():
    """EEVEE Next deja rastro de una superficie tramada con alfa 0 (glifos fantasma). Cada marca se oculta del render
    en los frames en que su opacidad efectiva (root × grupo × local) es 0; el fundido sigue igual."""
    sc = bpy.context.scene
    marcas = [o for o in bpy.data.objects if o.type in ('MESH', 'FONT') and o.name != 'tarjeta' and o.active_material
              and 'local' in o.active_material.node_tree.nodes]
    previo = {}
    for f in range(sc.frame_start, sc.frame_end + 1):
        sc.frame_set(f)
        for o in marcas:
            alfa = o.active_material.node_tree.nodes['local'].outputs[0].default_value
            if o.parent and o.parent.name.startswith('chip-'):
                alfa *= o.parent['opacidad']
            if o.name in ('corte', 'tachado', 'barra') and o.scale.x < 1e-4:
                alfa = 0.0
            oculto = alfa < 0.002
            if previo.get(o.name) != oculto:
                o.hide_render = oculto
                o.keyframe_insert('hide_render', frame=f)
                previo[o.name] = oculto
