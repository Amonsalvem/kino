"""conjunto-noche-lector-confirma (versión 2): la entrada de un conjunto genérico, de noche.

Sin personas, sin vehículos a la vista, sin placas, sin monitores ni logos. La cámara va a la altura de quien conduce
y llega a la portería. El lector lee, confirma y solo entonces la talanquera sube y la vía se abre.

Tiempos (60 fps, todo de @kino/motion):
  llegada     1 → +duracion/cortina, curva/crecer (frena al llegar al lector)
  lectura     barrido neutro sobre la ventana del lector: responder (duracion/corto, curva/crecer)
  confirmar   indicador estado/sin-confirmar/borde → estado/vigente/borde con aparecer; brillo y luz práctica verde
              solo desde aquí; luego late (curva/latir)
  talanquera  sube con resorte/firme (sin rebote) al terminar confirmar; el brazo se flexiona por su inercia
  salida      la cámara avanza hacia la vía abierta: 60 % de la llegada (coreografia/salida-factor), curva/salir
Reducido: cámara quieta en el plano final de la llegada, barrido → fundido, brazo abajo → brazo arriba por fundido con
la misma duración, sin latido. Colores: solo tokens (primitivos para sustratos y luces, semánticos para estados).
"""
import math
import random

import bpy

import kino3d as k

# Línea de tiempo --------------------------------------------------------------------------------
LLEGADA = (1, 1 + k.frames('duracion/cortina'))
LECTURA = (LLEGADA[1], LLEGADA[1] + k.frames('responder/duracion'))
CONFIRMA = (LECTURA[1], LECTURA[1] + k.frames('aparecer/duracion'))
TALANQUERA = (CONFIRMA[1], CONFIRMA[1] + k.Resorte('firme').frames())
SALIDA = (TALANQUERA[1], TALANQUERA[1] + round(k.frames('duracion/cortina') * k.MOTION['coreografia']['salidaFactor']))
FIN = SALIDA[1] + 12

CAM_INICIO, CAM_LLEGA, CAM_SALE = (0.95, -10.5, 1.24), (0.85, 0.2, 1.2), (0.95, 1.05, 1.2)
MIRA_INICIO, MIRA_LLEGA, MIRA_SALE = (0.2, 9.0, 1.3), (-0.35, 7.0, 1.12), (0.5, 14.0, 1.3)
LECTOR = (-0.95, 4.4)
PIVOTE = (-0.78, 6.9, 0.98)
BRAZO = 4.45
rnd = random.Random(7)


def escena(modo, reducido):
    k.vaciar()
    sc = bpy.context.scene
    k.configurar(sc, 1920, 1080, 1, FIN, transparente=False, muestras=16)
    sc['kino_recurso'] = 'conjunto-noche-lector-confirma' + ('.reducido' if reducido else '')
    ev = sc.eevee
    ev.volumetric_start, ev.volumetric_end = 0.5, 70
    ev.volumetric_tile_size = '8'
    ev.volumetric_samples = 48
    ev.volumetric_light_clamp = 8
    ev.use_volumetric_shadows = True
    ev.volumetric_shadow_samples = 8
    sc.render.use_motion_blur = not reducido
    sc.render.motion_blur_shutter = 0.5
    k.compositor(sc, brillo=(0.004, 0.018), fuerza_brillo=(1.3, 0.8), destello=0.22, transparente=False)


# Geometría --------------------------------------------------------------------------------------
def caja(nombre, centro, tam, mat, bisel=0.02, segmentos=3, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=centro, rotation=rot)
    ob = bpy.context.active_object
    ob.name = nombre
    ob.scale = tam
    bpy.ops.object.transform_apply(scale=True)
    if bisel:
        b = ob.modifiers.new('bisel', 'BEVEL')
        b.width, b.segments, b.harden_normals = bisel, segmentos, True
        b.limit_method = 'ANGLE'
    for p in ob.data.polygons:
        p.use_smooth = True
    asignar(ob, mat)
    return ob


def cilindro(nombre, centro, radio, alto, mat, rot=(0, 0, 0), lados=24, bisel=0.004):
    bpy.ops.mesh.primitive_cylinder_add(radius=radio, depth=alto, location=centro, rotation=rot, vertices=lados)
    ob = bpy.context.active_object
    ob.name = nombre
    if bisel:
        b = ob.modifiers.new('bisel', 'BEVEL')
        b.width, b.segments, b.harden_normals, b.limit_method = bisel, 2, True, 'ANGLE'
    for p in ob.data.polygons:
        p.use_smooth = True
    asignar(ob, mat)
    return ob


def arbusto(nombre, centro, tam, mat, semilla):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4, radius=1, location=centro)
    ob = bpy.context.active_object
    ob.name = nombre
    ob.scale = tam
    tex = bpy.data.textures.get('follaje') or bpy.data.textures.new('follaje', 'VORONOI')
    tex.noise_scale = 0.35
    d = ob.modifiers.new('hojas', 'DISPLACE')
    d.texture, d.strength, d.mid_level = tex, 0.22, 0.6
    d.texture_coords = 'GLOBAL'
    t2 = bpy.data.textures.get('masa') or bpy.data.textures.new('masa', 'CLOUDS')
    t2.noise_scale = 0.9
    d2 = ob.modifiers.new('masa', 'DISPLACE')
    d2.texture, d2.strength = t2, 0.35
    d2.texture_coords = 'GLOBAL'
    ob.location.x += semilla * 0.001
    for p in ob.data.polygons:
        p.use_smooth = True
    asignar(ob, mat)
    return ob


def asignar(ob, mat):
    if mat:
        ob.data.materials.append(bpy.data.materials.get(mat) or bpy.data.materials.new(mat))


def plano(nombre, centro, tam, mat):
    bpy.ops.mesh.primitive_plane_add(size=1, location=centro)
    ob = bpy.context.active_object
    ob.name = nombre
    ob.scale = (tam[0], tam[1], 1)
    bpy.ops.object.transform_apply(scale=True)
    asignar(ob, mat)
    return ob


def tornillo(nombre, centro, rot, mat='acero', r=0.009):
    return cilindro(nombre, centro, r, 0.006, mat, rot=rot, lados=6, bisel=0.0015)


# Etapas -----------------------------------------------------------------------------------------
def modelado(modo, reducido):
    sc = bpy.context.scene
    via()
    isla()
    lector()
    talanquera('brazo', 0.0)
    if reducido:
        talanquera_arriba_reducido()
    salida_talanquera()
    porteria()
    marquesina()
    muros_y_vegetacion()
    interior()
    camara()
    luces()
    mundo()


def via():
    plano('suelo', (0, 20, -0.02), (160, 160), 'cesped')
    plano('asfalto', (-2.5, 14, 0.0), (15, 72), 'asfalto')
    # Línea de pare y bordes de carril (pintura vial gastada), reductor de velocidad antes del lector.
    caja('pare', (1.5, 3.3, 0.004), (3.8, 0.3, 0.008), 'pintura', bisel=0)
    for x in (3.55,):
        for i in range(10):
            caja(f'linea-{i}', (x, -18 + i * 3.2, 0.004), (0.12, 1.8, 0.008), 'pintura', bisel=0)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=4.0, location=(1.5, -2.6, -0.42), rotation=(0, math.radians(90), 0), vertices=48)
    r = bpy.context.active_object
    r.name = 'reductor'
    r.scale = (1, 1, 0.9)
    for p in r.data.polygons:
        p.use_smooth = True
    asignar(r, 'reductor')
    # Andén derecho con bordillo en segmentos.
    caja('anden-der', (5.0, -6, 0.08), (2.8, 26, 0.16), 'concreto', bisel=0.01)
    for i in range(26):
        caja(f'bordillo-der-{i}', (3.64, -18.5 + i * 1.0, 0.09), (0.16, 0.985, 0.18), 'bordillo', bisel=0.02)


def isla():
    # Isla central de la portería, con bordillo en segmentos y una tapa de concreto.
    caja('isla', (-2.55, 7.5, 0.1), (4.1, 13.0, 0.2), 'concreto', bisel=0.015)
    for i in range(13):
        caja(f'bordillo-isla-{i}', (-0.47, 1.5 + i * 1.0, 0.11), (0.16, 0.985, 0.22), 'bordillo', bisel=0.02)
    caja('nariz-isla', (-2.55, 0.92, 0.11), (4.1, 0.2, 0.22), 'bordillo', bisel=0.03)


def lector():
    """Pedestal del lector: cuerpo biselado, capota, placa frontal con ventana de lectura, indicador y tornillería."""
    x, y = LECTOR
    ang = math.radians(-28)  # mira hacia el carril que llega
    raiz = bpy.data.objects.new('lector', None)
    bpy.context.scene.collection.objects.link(raiz)
    raiz.location = (x, y, 0.2)
    raiz.rotation_euler = (0, 0, ang)
    piezas = [
        caja('lector-base', (0, 0, 0.012), (0.44, 0.36, 0.024), 'acero-oscuro', bisel=0.006),
        caja('lector-cuerpo', (0, 0, 0.64), (0.26, 0.2, 1.24), 'metal', bisel=0.025, segmentos=4),
        caja('lector-capota', (0, -0.035, 1.3), (0.32, 0.3, 0.05), 'metal', bisel=0.02, segmentos=4, rot=(math.radians(-8), 0, 0)),
        caja('lector-placa', (0, -0.103, 0.98), (0.21, 0.012, 0.44), 'metal-claro', bisel=0.006),
        caja('lector-ventana', (0, -0.111, 1.08), (0.15, 0.006, 0.12), 'vidrio-negro', bisel=0.004),
        caja('lector-junta-a', (0, -0.1, 0.72), (0.26, 0.004, 0.006), 'junta', bisel=0),
        caja('lector-junta-b', (0, -0.1, 0.3), (0.26, 0.004, 0.006), 'junta', bisel=0),
    ]
    for i, (dx, dz) in enumerate(((-0.085, 1.18), (0.085, 1.18), (-0.085, 0.78), (0.085, 0.78))):
        piezas.append(tornillo(f'lector-tornillo-{i}', (dx, -0.11, dz), (math.radians(90), 0, 0)))
    for i, (dx, dy) in enumerate(((-0.18, -0.14), (0.18, -0.14), (-0.18, 0.14), (0.18, 0.14))):
        piezas.append(tornillo(f'lector-perno-{i}', (dx, dy, 0.027), (0, 0, 0), r=0.012))
    # Indicador: anillo y punto (marcas de estado), bajo la ventana. El barrido de lectura pasa sobre la ventana.
    piezas += indicador((0, -0.1135, 0.9))
    b = caja('barrido', (0, -0.1155, 1.08), (0.15, 0.002, 0.012), 'barrido', bisel=0)
    b.visible_shadow = False
    piezas.append(b)
    for ob in piezas:
        ob.parent = raiz


def indicador(c):
    import pase
    x, y, z = c
    anillo = pase.anillo('indicador', x, z, 0.03, 0.009, 0, lados=48)
    punto = pase.disco('indicador-punto', x, z, 0.011, 0, lados=32)
    for ob in (anillo, punto):
        ob.location.y = y
        ob.visible_shadow = False
    return [anillo, punto]


def talanquera(nombre, angulo):
    """Gabinete con puerta, rejillas, tapa y buje; el brazo gira en el pivote (eje Y)."""
    if not bpy.data.objects.get('gabinete'):
        x, y = PIVOTE[0] - 0.22, PIVOTE[1]
        caja('gabinete', (x, y, 0.2 + 0.5), (0.34, 0.4, 1.0), 'metal', bisel=0.02, segmentos=4)
        caja('gabinete-tapa', (x, y, 1.22), (0.38, 0.44, 0.04), 'metal-claro', bisel=0.012)
        caja('gabinete-puerta', (x - 0.172, y, 0.7), (0.004, 0.32, 0.78), 'junta', bisel=0)
        for i in range(6):
            caja(f'rejilla-{i}', (x, y - 0.202, 0.42 + i * 0.05), (0.22, 0.012, 0.018), 'acero-oscuro', bisel=0.003,
                 rot=(math.radians(35), 0, 0))
        cilindro('buje', (PIVOTE[0] - 0.02, y, PIVOTE[2]), 0.085, 0.07, 'acero', rot=(0, math.radians(90), 0), lados=32)
        for i, (dy, dz) in enumerate(((-0.14, 0.34), (0.14, 0.34), (-0.14, 1.06), (0.14, 1.06))):
            tornillo(f'gabinete-tornillo-{i}', (x + 0.172, y + dy, dz), (0, math.radians(90), 0))
    piv = bpy.data.objects.new(f'{nombre}-pivote', None)
    bpy.context.scene.collection.objects.link(piv)
    piv.location = PIVOTE
    piv.rotation_euler = (0, -angulo, 0)
    L = BRAZO
    brazo = caja(nombre, (L / 2 + 0.03, 0, 0), (L, 0.055, 0.095), 'brazo', bisel=0.022, segmentos=4)
    tapa = caja(f'{nombre}-punta', (L + 0.05, 0, 0), (0.05, 0.065, 0.105), 'caucho', bisel=0.015)
    falda = caja(f'{nombre}-falda', (L / 2 + 0.03, 0, -0.07), (L * 0.96, 0.012, 0.05), 'caucho', bisel=0.004)
    for ob in (brazo, tapa, falda):
        ob.parent = piv
    # Flexión por inercia: SimpleDeform BEND alrededor de un eje paralelo a Y en el pivote.
    eje = bpy.data.objects.new(f'{nombre}-eje', None)
    bpy.context.scene.collection.objects.link(eje)
    eje.parent = piv
    eje.rotation_euler = (math.radians(90), 0, 0)
    for ob in (brazo, falda):
        sd = ob.modifiers.new('flexion', 'SIMPLE_DEFORM')
        sd.deform_method, sd.origin, sd.deform_axis = 'BEND', eje, 'Z'
        sd.angle = 0.0
    return piv


def talanquera_arriba_reducido():
    talanquera('brazo-arriba', math.radians(86))


def salida_talanquera():
    """Carril de salida (quieto): otro gabinete sencillo con el brazo abajo, más lejos."""
    caja('gab-salida', (-4.35, 7.6, 0.7), (0.34, 0.4, 1.0), 'metal', bisel=0.02)
    caja('brazo-salida', (-6.55, 7.6, 0.98), (4.2, 0.055, 0.095), 'brazo', bisel=0.02)


def porteria():
    x0, x1, y0, y1, h = -4.3, -1.4, 8.4, 12.2, 2.9
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    caja('porteria-zocalo', (cx, cy, 0.35), (x1 - x0 + 0.06, y1 - y0 + 0.06, 0.3), 'concreto', bisel=0.01)
    caja('porteria-muro', (cx, cy, 0.2 + h / 2), (x1 - x0, y1 - y0, h), 'muro', bisel=0.015)
    # Banda de ventanas hacia el carril de entrada, con parteluces; luz interior tenue (sin pantallas).
    caja('porteria-vidrio', (x1 + 0.005, cy, 1.75), (0.02, y1 - y0 - 0.6, 1.1), 'vidrio', bisel=0)
    for i in range(5):
        caja(f'parteluz-{i}', (x1 + 0.02, y0 + 0.3 + i * (y1 - y0 - 0.6) / 4, 1.75), (0.05, 0.06, 1.16), 'acero-oscuro', bisel=0.006)
    caja('porteria-travesano', (x1 + 0.02, cy, 1.95), (0.05, y1 - y0 - 0.6, 0.05), 'acero-oscuro', bisel=0.006)
    caja('porteria-travesano-frente', (cx, y0 - 0.02, 1.95), (x1 - x0 - 0.9, 0.05, 0.05), 'acero-oscuro', bisel=0.006)
    caja('porteria-alfeizar', (x1 + 0.05, cy, 1.17), (0.12, y1 - y0 - 0.5, 0.05), 'concreto', bisel=0.008)
    caja('porteria-vidrio-frente', (cx, y0 - 0.005, 1.75), (x1 - x0 - 0.9, 0.02, 1.1), 'vidrio', bisel=0)
    for i in range(8):
        caja(f'porteria-junta-{i}', (x1 + 0.004, cy, 0.5 + i * 0.36), (0.004, y1 - y0, 0.008), 'junta', bisel=0) if i < 2 else None
    caja('porteria-cubierta', (cx, cy, h + 0.28), (x1 - x0 + 0.8, y1 - y0 + 0.8, 0.16), 'concreto', bisel=0.02)
    caja('porteria-imposta', (cx, cy, h + 0.18), (x1 - x0 + 0.84, y1 - y0 + 0.84, 0.05), 'metal', bisel=0.01)
    k.luz('porteria-interior', 'AREA', 'hueso/d70', 25, (cx, cy, h - 0.1), (cx, cy, 0), tam=2.0)


def marquesina():
    """Cubierta sobre los carriles con luminarias: la luz clave de la entrada."""
    caja('marquesina', (-2.3, 7.9, 4.75), (14.2, 4.6, 0.32), 'concreto', bisel=0.03)
    caja('marquesina-borde', (-2.3, 5.58, 4.75), (14.3, 0.08, 0.4), 'metal', bisel=0.01)
    for i, x in enumerate((-9.2, -4.45, 4.55)):
        caja(f'columna-{i}', (x, 7.9, 2.4), (0.34, 0.34, 4.8), 'concreto', bisel=0.02)
    for i, (x, y) in enumerate(((1.5, 6.7), (1.5, 9.1), (-6.6, 7.9))):
        cilindro(f'luminaria-{i}', (x, y, 4.58), 0.16, 0.03, 'luminaria', lados=32, bisel=0.002)
        k.luz(f'foco-{i}', 'SPOT', 'hueso/100', 900, (x, y, 4.54), (x, y, 0), tam=0.12,
              spot_size=math.radians(78), spot_blend=0.45, volume_factor=1.2)


def muros_y_vegetacion():
    """Muros del conjunto con pilastras, remate y apliques; seto al frente; árboles detrás."""
    for lado, (xa, xb) in (('der', (4.8, 26.0)), ('izq', (-9.4, -30.0))):
        paso = 3.0 if xb > xa else -3.0
        largo = abs(xb - xa)
        cx = (xa + xb) / 2
        caja(f'muro-{lado}', (cx, 6.9, 1.15), (largo, 0.26, 2.3), 'muro', bisel=0.01)
        caja(f'remate-{lado}', (cx, 6.9, 2.33), (largo, 0.36, 0.07), 'concreto', bisel=0.01)
        n = int(largo / 3)
        for i in range(n + 1):
            x = xa + i * paso
            caja(f'pilastra-{lado}-{i}', (x, 6.88, 1.3), (0.46, 0.4, 2.6), 'muro', bisel=0.015)
            caja(f'capitel-{lado}-{i}', (x, 6.88, 2.64), (0.56, 0.5, 0.08), 'concreto', bisel=0.012)
            if i % 2 == 0:
                caja(f'aplique-{lado}-{i}', (x, 6.64, 2.0), (0.14, 0.08, 0.2), 'luminaria', bisel=0.01)
                k.luz(f'aplique-luz-{lado}-{i}', 'SPOT', 'hueso/100', 45, (x, 6.56, 1.95), (x, 6.2, 0.0), tam=0.05,
                      spot_size=math.radians(110), spot_blend=0.9, volume_factor=0.6)
        for i in range(int(largo / 1.3)):
            x = xa + (i + 0.5) * (1.3 if xb > xa else -1.3)
            arbusto(f'seto-{lado}-{i}', (x, 6.35, 0.5), (0.75, 0.45, 0.55 + rnd.random() * 0.12), 'follaje', i)
        for i in range(int(largo / 5)):
            x = xa + (i + 0.4) * (5 if xb > xa else -5) + rnd.uniform(-1, 1)
            arbol(f'arbol-{lado}-{i}', (x, 9.5 + rnd.uniform(0, 3), 0))


def arbol(nombre, base, alto=None):
    alto = alto or rnd.uniform(4.2, 6.5)
    cilindro(f'{nombre}-tronco', (base[0], base[1], alto * 0.3), 0.12, alto * 0.6, 'corteza', lados=10, bisel=0)
    for j in range(3):
        c = (base[0] + rnd.uniform(-0.6, 0.6), base[1] + rnd.uniform(-0.6, 0.6), alto * (0.65 + 0.12 * j))
        arbusto(f'{nombre}-copa-{j}', c, (1.5 - 0.25 * j, 1.5 - 0.25 * j, 1.2 - 0.2 * j), 'follaje-alto', j)


def interior():
    """La vía sigue dentro del conjunto: faroles, casas con ventanas encendidas y árboles, perdidos en la niebla."""
    for i in range(6):
        y = 16 + i * 9
        for lado, x in (('d', 5.0), ('i', -2.0)):
            if (i + (lado == 'i')) % 2:
                continue
            cilindro(f'poste-{lado}{i}', (x, y, 2.6), 0.06, 5.2, 'acero-oscuro', lados=12)
            caja(f'farol-{lado}{i}', (x - 0.35 if lado == 'd' else x + 0.35, y, 5.15), (0.8, 0.22, 0.1), 'metal', bisel=0.02)
            k.luz(f'farol-luz-{lado}{i}', 'SPOT', 'hueso/100', 500, (x - 0.5 if lado == 'd' else x + 0.5, y, 5.05),
                  (x - 0.8 if lado == 'd' else x + 0.8, y, 0), tam=0.1, spot_size=math.radians(95), spot_blend=0.6, volume_factor=1.0)
    for i in range(10):
        lado = 1 if i % 2 else -1
        x = lado * (9 + rnd.uniform(0, 4)) + 1.5
        y = 18 + i * 6.5
        w, d, h = rnd.uniform(6, 8), rnd.uniform(6, 8), rnd.uniform(3, 5.8)
        caja(f'casa-{i}', (x, y, h / 2), (w, d, h), 'muro', bisel=0.03)
        bpy.ops.mesh.primitive_cylinder_add(radius=w * 0.62, depth=d + 0.4, vertices=3, location=(x, y, h + w * 0.2),
                                            rotation=(math.radians(90), 0, math.radians(90)))
        t = bpy.context.active_object
        t.name = f'techo-{i}'
        t.scale = (0.55, 1, 1)
        asignar(t, 'techo')
        for j in range(rnd.randint(1, 3)):
            fx = x - lado * (w / 2 + 0.01)
            caja(f'ventana-{i}-{j}', (fx, y + rnd.uniform(-d / 3, d / 3), rnd.uniform(1.2, h - 1.0)),
                 (0.02, rnd.uniform(0.8, 1.6), rnd.uniform(0.7, 1.1)), 'ventana-casa' if rnd.random() > 0.35 else 'vidrio', bisel=0)
        arbol(f'arbol-int-{i}', (x - lado * (w / 2 + 2.2), y + rnd.uniform(-2, 2), 0))


def camara():
    sc = bpy.context.scene
    mira = bpy.data.objects.new('mira', None)
    sc.collection.objects.link(mira)
    mira.location = MIRA_INICIO
    cam = bpy.data.objects.new('camara', bpy.data.cameras.new('camara'))
    sc.collection.objects.link(cam)
    cam.data.lens = 28
    cam.data.sensor_width = 36
    cam.data.dof.use_dof = True
    cam.data.dof.focus_object = bpy.data.objects['lector']
    cam.data.dof.aperture_fstop = 3.2
    cam.data.dof.aperture_blades = 6
    cam.location = CAM_INICIO
    k.apuntar(cam, mira)
    sc.camera = cam
    # Faros del vehículo que llega (no se ve): luz motivada, neutra, que viaja con la cámara.
    for i, dx in enumerate((-0.75, 0.75)):
        f = k.luz(f'faro-{i}', 'SPOT', 'texto/primario', 260, (dx, -0.4, -0.55), tam=0.06,
                  spot_size=math.radians(42), spot_blend=0.35, volume_factor=0.5)
        f.parent = cam
        f.rotation_euler = (math.radians(-6), 0, 0)


def luces():
    # Luna: relleno frío (índigo de la aurora), sin sombras duras.
    luna = k.luz('luna', 'SUN', 'indigo/d70', 0.35, (0, 0, 30))
    luna.rotation_euler = (math.radians(52), 0, math.radians(-140))
    luna.data.angle = math.radians(6)
    # Luz práctica del indicador: verde de estado, apagada hasta que el lector confirma.
    x, y = LECTOR
    ang = math.radians(-28)
    px, py = x + 0.12 * math.sin(-ang) * -1, y - 0.12 * math.cos(ang)
    k.luz('indicador-luz', 'POINT', 'estado/vigente/borde', 0.0, (px, py, 1.12), tam=0.03)


def mundo():
    """Cielo: abismo arriba, bruma de sustrato en el horizonte y la aurora (índigo y violeta; el verde queda para lo
    activo). Niebla volumétrica neutra en todo el espacio."""
    sc = bpy.context.scene
    w = bpy.data.worlds.new('noche')
    w.use_nodes = True
    nt = w.node_tree
    N, L = nt.nodes, nt.links
    fondo = N['Background']
    tc = N.new('ShaderNodeTexCoord')
    sepv = N.new('ShaderNodeSeparateXYZ')
    L.new(tc.outputs['Generated'], sepv.inputs[0])
    horiz = k.rampa(nt, sepv.outputs['Z'], [(0.0, 'sustrato/200'), (0.08, 'sustrato/200'), (0.3, 'sustrato/100')])
    # Aurora: bandas de ruido estiradas sobre la dirección de vista, con máscara de altura.
    mp = N.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (1.2, 4.5, 1.0)
    L.new(tc.outputs['Generated'], mp.inputs['Vector'])
    ondas = N.new('ShaderNodeTexWave')
    ondas.wave_type, ondas.bands_direction = 'BANDS', 'X'
    ondas.inputs['Scale'].default_value = 1.4
    ondas.inputs['Distortion'].default_value = 6.0
    ondas.inputs['Detail'].default_value = 3.0
    L.new(mp.outputs[0], ondas.inputs['Vector'])
    color_aurora = k.rampa(nt, ondas.outputs['Fac'], [(0.1, 'sustrato/100'), (0.45, 'indigo/d15'), (0.7, 'violeta/d15'), (0.9, 'biolum/d15')])
    alto = k.rampa(nt, sepv.outputs['Z'], [(0.1, 0.0), (0.28, 1.0), (0.62, 0.0)])
    mezcla = N.new('ShaderNodeMix')
    mezcla.data_type = 'RGBA'
    mezcla.blend_type = 'SCREEN'
    L.new(alto, mezcla.inputs['Factor'])
    L.new(horiz, mezcla.inputs['A'])
    L.new(color_aurora, mezcla.inputs['B'])
    L.new(mezcla.outputs['Result'], fondo.inputs['Color'])
    fondo.inputs['Strength'].default_value = 0.9
    vol = N.new('ShaderNodeVolumePrincipled')
    vol.inputs['Color'].default_value = k.color('sustrato/d70')
    vol.inputs['Density'].default_value = 0.016
    vol.inputs['Anisotropy'].default_value = 0.35
    L.new(vol.outputs[0], N['World Output'].inputs['Volume'])
    sc.world = w


# Materiales -------------------------------------------------------------------------------------
def materiales(modo, reducido):
    def pb(nombre, token, rug, met=0.0, **extra):
        m, p = k.principled(nombre, token, rugosidad=rug, metalico=met, **extra)
        return m, p

    m, p = pb('asfalto', 'hueso/l90', 0.75)
    nt = m.node_tree
    tc = nt.nodes.new('ShaderNodeTexCoord')
    grano = k.ruido(nt, 60, detalle=8, coord=tc.outputs['Object'])
    charcos = k.ruido(nt, 0.35, detalle=3, coord=tc.outputs['Object'])
    nt.links.new(k.rampa(nt, grano.outputs['Fac'], [(0.35, 'sustrato/200'), (0.65, 'hueso/l90')]), p.inputs['Base Color'])
    rug = k.rampa(nt, charcos.outputs['Fac'], [(0.6, 0.3), (0.66, 0.82)])
    nt.links.new(rug, p.inputs['Roughness'])
    bu = nt.nodes.new('ShaderNodeBump')
    bu.inputs['Strength'].default_value = 0.25
    bu.inputs['Distance'].default_value = 0.02
    nt.links.new(grano.outputs['Fac'], bu.inputs['Height'])
    nt.links.new(bu.outputs[0], p.inputs['Normal'])

    m, p = pb('pintura', 'hueso/500', 0.6)
    nt = m.node_tree
    gasto = k.ruido(nt, 18, detalle=6)
    nt.links.new(k.rampa(nt, gasto.outputs['Fac'], [(0.42, 'hueso/l90'), (0.52, 'hueso/500')]), p.inputs['Base Color'])
    m, p = pb('reductor', 'hueso/200', 0.55)
    nt = m.node_tree
    tc = nt.nodes.new('ShaderNodeTexCoord')
    sepv = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['Object'], sepv.inputs[0])
    franjas = nt.nodes.new('ShaderNodeMath')
    franjas.operation = 'PINGPONG'
    franjas.inputs[1].default_value = 0.25
    nt.links.new(sepv.outputs['Z'], franjas.inputs[0])
    nt.links.new(k.rampa(nt, franjas.outputs[0], [(0.124, 'sustrato/100'), (0.126, 'hueso/300')]), p.inputs['Base Color'])

    for nombre, a, b, rug, esc in (('concreto', 'hueso/l70', 'hueso/d32', (0.6, 0.85), 3.0),
                                   ('bordillo', 'hueso/d45', 'hueso/l70', (0.55, 0.8), 6.0),
                                   ('muro', 'sustrato/300', 'sustrato/d15', (0.7, 0.9), 1.5),
                                   ('techo', 'sustrato/100', 'sustrato/300', (0.6, 0.8), 2.0),
                                   ('cesped', 'sustrato/300', 'sustrato/l70', (0.8, 0.95), 0.8)):
        m, p = pb(nombre, a, 0.7)
        k.microvariacion(m, p, a, b, escala=esc, rug=rug, bump=0.08, escala_bump=40)
    m, p = pb('metal', 'sustrato/400', 0.32, met=0.35, **{'Coat Weight': 0.3, 'Coat Roughness': 0.2})
    k.microvariacion(m, p, 'sustrato/400', 'sustrato/d15', escala=8, rug=(0.28, 0.4), bump=0.01, escala_bump=300)
    pb('metal-claro', 'sustrato/500', 0.3, met=0.4, **{'Coat Weight': 0.4, 'Coat Roughness': 0.15})
    pb('acero', 'hueso/600', 0.28, met=1.0)
    pb('acero-oscuro', 'hueso/d23', 0.4, met=0.8)
    pb('junta', 'sustrato/100', 0.8)
    pb('caucho', 'sustrato/100', 0.85)
    pb('corteza', 'hueso/d15', 0.9)
    pb('vidrio-negro', 'sustrato/100', 0.04, **{'Coat Weight': 1.0, 'Coat Roughness': 0.02})
    # Vidrio oscuro con un resplandor interior muy bajo: no debe leerse como pantalla (la marca prohíbe monitores).
    m, p = pb('vidrio', 'sustrato/100', 0.12, **{'Coat Weight': 0.25, 'Coat Roughness': 0.08,
                                                  'Emission Color': 'sustrato/d45', 'Emission Strength': 0.08})
    m, p = pb('brazo', 'hueso/200', 0.35, **{'Coat Weight': 0.5, 'Coat Roughness': 0.1})
    nt = m.node_tree
    tc = nt.nodes.new('ShaderNodeTexCoord')
    sepv = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['Object'], sepv.inputs[0])
    fr = nt.nodes.new('ShaderNodeMath')
    fr.operation = 'PINGPONG'
    fr.inputs[1].default_value = 0.3
    nt.links.new(sepv.outputs['X'], fr.inputs[0])
    nt.links.new(k.rampa(nt, fr.outputs[0], [(0.149, 'hueso/200'), (0.151, 'sustrato/500')]), p.inputs['Base Color'])
    for nombre, a, b in (('follaje', 'sustrato/l70', 'sustrato/300'), ('follaje-alto', 'sustrato/l90', 'sustrato/200')):
        m, p = pb(nombre, a, 0.75, **{'Subsurface Weight': 0.15, 'Subsurface Scale': 0.05, 'Sheen Weight': 0.3})
        k.microvariacion(m, p, a, b, escala=6, rug=(0.6, 0.9), bump=0.3, escala_bump=25)
    pb('luminaria', 'hueso/300', 0.3, **{'Emission Color': 'hueso/100', 'Emission Strength': 12.0})
    pb('ventana-casa', 'hueso/300', 0.3, **{'Emission Color': 'hueso/d70', 'Emission Strength': 1.1})
    # Marcas de estado: el indicador sale con el hex exacto de su token; el barrido de lectura es neutro.
    for nombre in ('indicador', 'indicador-punto'):
        mm = k.marca(nombre, 'estado/sin-confirmar/borde', raiz=False)
        bpy.data.objects[nombre].data.materials.append(mm)
    mm = k.marca('barrido', 'texto/tenue', raiz=False)
    k.nodo(mm, 'local').outputs[0].default_value = 0.0
    bpy.data.objects['barrido'].data.materials.append(mm)
    for ob in bpy.data.objects:
        if ob.type == 'MESH' and not ob.data.materials:
            print('sin material:', ob.name)


# Animación --------------------------------------------------------------------------------------
def animacion(modo, reducido):
    sc = bpy.context.scene
    cam, mira = bpy.data.objects['camara'], bpy.data.objects['mira']
    # Cámara: llega frenando (crecer), espera la confirmación y avanza cuando la vía se abre (salir).
    if reducido:
        cam.location, mira.location = CAM_LLEGA, MIRA_LLEGA
        for i in range(3):
            k.fijar(cam, 'location', i, 1, CAM_LLEGA[i])
            k.fijar(mira, 'location', i, 1, MIRA_LLEGA[i])
    else:
        for i in range(3):
            k.tramo(cam, 'location', i, LLEGADA[0], LLEGADA[1], CAM_INICIO[i], CAM_LLEGA[i], 'curva/crecer')
            k.tramo(mira, 'location', i, LLEGADA[0], LLEGADA[1], MIRA_INICIO[i], MIRA_LLEGA[i], 'curva/crecer')
            k.tramo(cam, 'location', i, SALIDA[0], SALIDA[1], CAM_LLEGA[i], CAM_SALE[i], 'curva/salir')
            k.tramo(mira, 'location', i, SALIDA[0], SALIDA[1], MIRA_LLEGA[i], MIRA_SALE[i], 'curva/salir')
    # Lectura: el barrido cruza la ventana (reducido: aparece y se va por fundido, misma duración).
    barrido = bpy.data.objects['barrido']
    loc = k.nodo(bpy.data.materials['barrido'], 'local').outputs[0]
    s, f = LECTURA
    m = (s + f) // 2
    k.fijar(loc, 'default_value', -1, 1, 0.0)
    k.tramos_encadenados(loc, 'default_value', -1, [(s, 0.0), (m, 1.0), (f, 0.0)], 'responder/curva')
    if not reducido:
        k.tramo(barrido, 'location', 2, s, f, 1.14, 1.02, 'responder/curva')
    # Confirmar: sin confirmar → vigente. Color del indicador, brillo (AOV) y luz práctica verde, solo desde aquí.
    s, f = CONFIRMA
    for nombre in ('indicador', 'indicador-punto'):
        mm = bpy.data.materials[nombre]
        sock = k.nodo(mm, 'color').outputs[0]
        k.fijar_color(sock, 1, 'estado/sin-confirmar/borde')
        k.tramo_color(sock, s, f, 'estado/sin-confirmar/borde', 'estado/vigente/borde', 'aparecer/curva')
        b = k.nodo(mm, 'brillo').outputs[0]
        k.fijar(b, 'default_value', -1, 1, 0.0)
        k.tramo(b, 'default_value', -1, s, f, 0.0, 1.0, 'aparecer/curva')
    luz = bpy.data.objects['indicador-luz'].data
    k.fijar(luz, 'energy', -1, 1, 0.0)
    k.tramo(luz, 'energy', -1, s, f, 0.0, 1.6, 'aparecer/curva')
    # Latir: el brillo del indicador respira con curva/latir desde que queda vigente (reducido: quieto).
    if not reducido:
        n = k.frames('latir/duracion')
        e = k.bezier('latir/curva')

        def pulso(i):
            u = e((i % n) / n)
            return 1.0 + 0.6 * (2 * u if u < 0.5 else 2 - 2 * u)
        total = FIN - f
        for nombre in ('indicador', 'indicador-punto'):
            k.hornear(k.nodo(bpy.data.materials[nombre], 'brillo').outputs[0], 'default_value', -1, f, total, pulso)
        k.hornear(luz, 'energy', -1, f, total, lambda i: 1.6 * pulso(i))
    # Talanquera: solo después de confirmar. resorte/firme (llega sin pasarse); el brazo se flexiona por inercia.
    s, _ = TALANQUERA
    piv = bpy.data.objects['brazo-pivote']
    arriba = math.radians(86)
    r = k.Resorte('firme')
    n = r.frames()
    if reducido:
        # Fundido cruzado entre el brazo abajo y el brazo arriba, con el avance del resorte como curva.
        abajo_obs = [o for o in bpy.data.objects if o.parent == piv]
        arriba_obs = [o for o in bpy.data.objects if o.parent == bpy.data.objects['brazo-arriba-pivote']]
        for grupo_, desde, hasta in ((abajo_obs, 1.0, 0.0), (arriba_obs, 0.0, 1.0)):
            for ob in grupo_:
                if ob.type != 'MESH':
                    continue
                mat = fundible(ob)
                a = k.nodo(mat, 'alfa-fundido').outputs[0]
                k.fijar(a, 'default_value', -1, 1, desde)
                k.hornear(a, 'default_value', -1, s, n, lambda i, d=desde, h=hasta: d + (h - d) * r.avance(i / k.FPS))
                k.fijar(a, 'default_value', -1, s + n + 1, hasta)
                # Oculto cuando su alfa es 0 (EEVEE deja rastro de lo tramado con alfa 0).
                claves = ((1, False), (s + n + 1, True)) if hasta == 0 else ((1, True), (s, False))
                for fr, oculto in claves:
                    ob.hide_render = oculto
                    ob.keyframe_insert('hide_render', frame=fr)
    else:
        k.fijar(piv, 'rotation_euler', 1, 1, 0.0)
        k.hornear(piv, 'rotation_euler', 1, s, n, lambda i: -arriba * r.avance(i / k.FPS))
        k.fijar(piv, 'rotation_euler', 1, s + n + 1, -arriba)
        # Flexión: proporcional a la aceleración angular (el extremo se queda atrás al arrancar y alcanza al frenar).
        for nombre in ('brazo', 'brazo-falda'):
            sd = bpy.data.objects[nombre].modifiers['flexion']
            k.fijar(sd, 'angle', -1, 1, 0.0)
            k.hornear(sd, 'angle', -1, s, n + 6, lambda i: -0.00022 * arriba * r.aceleracion(i / k.FPS))
            k.fijar(sd, 'angle', -1, s + n + 7, 0.0)


def fundible(ob):
    """Copia del material de la pieza con un factor de fundido (para el reducido del brazo)."""
    base = ob.active_material
    m = base.copy()
    m.name = f'{base.name}-fundido-{ob.name}'
    nt = m.node_tree
    out = nt.nodes['Material Output']
    enlace = out.inputs['Surface'].links[0]
    shader = enlace.from_socket
    nt.links.remove(enlace)
    tr = nt.nodes.new('ShaderNodeBsdfTransparent')
    mix = nt.nodes.new('ShaderNodeMixShader')
    v = nt.nodes.new('ShaderNodeValue')
    v.name = 'alfa-fundido'
    nt.links.new(v.outputs[0], mix.inputs['Fac'])
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(shader, mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs['Surface'])
    m.use_transparent_shadow = True
    ob.material_slots[0].material = m
    return m
