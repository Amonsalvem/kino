"""Utilidades comunes para las escenas 3D de Kino en Blender (bpy 4.2), versión 2.

Fuentes (aquí no se escribe ningún milisegundo, curva, resorte ni hex a mano):
- Motion: partitura.json, que `node partitura.mjs` vuelca de @kino/motion (paquetes/kino-motion): duraciones, curvas,
  resortes físicos, escala, latir y la partitura del Pase. Es lo mismo que usa la web.
- Color: ../tokens.motion.json (tema oscuro, sale de los DTCG). Semánticos y primitivos. hex → lineal.

Easing: cada tramo es un par de claves con handles bezier libres en las proporciones exactas del cubic-bezier del token.
Resortes: se resuelven de forma analítica (misma fórmula que src/nucleo/resorte.ts) y se hornean, una clave por frame.
Escala: 1 px del sistema = 0,01 unidades de Blender.

Gestión de color (ver README): transformada de vista Standard y una curva de tono propia en el compositor, que
comprime las luces de la escena. Las marcas de estado (bordes, chip, barra, texto, indicador) escriben la AOV «marca»
y pasan sin curva: salen con el hex exacto de su token. El resplandor sale solo de la AOV «brillo», que escriben las
piezas activas (vigente) con su color de token: nada brilla antes de que el lector confirme.
"""
import json
import math
from pathlib import Path

import bpy

AQUI = Path(__file__).resolve().parent
_T = json.loads((AQUI.parent / 'tokens.motion.json').read_text())['oscuro']
COLOR = _T['color']
PRIMITIVO = _T['primitivo']
FORMA = {'radio': _T['radio'], 'espacio': _T['espacio'], 'linea': _T['linea']}
PARTITURA = json.loads((AQUI / 'partitura.json').read_text())
_DTCG = json.loads((AQUI.parents[4] / 'gorr-brand-system/clientes/kino/tokens/tema/oscuro.tokens.json').read_text())
# relieve/membrana del tema oscuro: [borde de luz interior, sombra]. La sombra se aplica en el compositor.
RELIEVE_SOMBRA = None  # se define tras _sombra_token
MOTION = PARTITURA['tokens']
FPS = MOTION['fps']
PX = 0.01
SUBIDA = MOTION['distancia']['subida'] * PX


# Tokens de motion ---------------------------------------------------------------------------------
def _resolver(nombre):
    """'aparecer/duracion' → 'duracion/tarjeta'; 'duracion/corto' queda igual."""
    return MOTION['verbo'].get(nombre, nombre)


def ms(nombre):
    familia, clave = _resolver(nombre).split('/')
    return MOTION[familia][clave]


def frames(nombre):
    """Frames a 60 fps de un token de duración (redondeo al frame más cercano, como tokens.py)."""
    return round(ms(nombre) * FPS / 1000)


def curva(nombre):
    return MOTION['curva'][_resolver(nombre).split('/')[1]]


def bezier(nombre):
    x1, y1, x2, y2 = curva(nombre)

    def b(u, a, c):
        return 3 * (1 - u) ** 2 * u * a + 3 * (1 - u) * u * u * c + u ** 3

    def f(t):
        if t <= 0:
            return 0.0
        if t >= 1:
            return 1.0
        lo, hi = 0.0, 1.0
        for _ in range(40):
            u = (lo + hi) / 2
            if b(u, x1, x2) < t:
                lo = u
            else:
                hi = u
        return b((lo + hi) / 2, y1, y2)
    return f


class Resorte:
    """Resorte amortiguado analítico. Mismos parámetros que Reanimated, SwiftUI y Compose (rigidez, amortiguación, masa)."""

    def __init__(self, nombre, v0=0.0):
        p = MOTION['resorte'][nombre]
        k, c, m = p['rigidez'], p['amortiguacion'], p['masa']
        self.nombre = nombre
        self.w0 = math.sqrt(k / m)
        self.zeta = c / (2 * math.sqrt(k * m))
        self.asentamiento = p['asentamientoMs'] / 1000
        self.x0, self.dx0 = 1.0, -v0

    def desplazamiento(self, t):
        w0, z, x0, dx0 = self.w0, self.zeta, self.x0, self.dx0
        if z < 1:
            wd = w0 * math.sqrt(1 - z * z)
            B = (dx0 + z * w0 * x0) / wd
            return math.exp(-z * w0 * t) * (x0 * math.cos(wd * t) + B * math.sin(wd * t))
        if z == 1:
            return math.exp(-w0 * t) * (x0 + (dx0 + w0 * x0) * t)
        s = math.sqrt(z * z - 1)
        r1, r2 = -w0 * (z - s), -w0 * (z + s)
        Bc = (dx0 - r1 * x0) / (r2 - r1)
        return (x0 - Bc) * math.exp(r1 * t) + Bc * math.exp(r2 * t)

    def avance(self, t):
        return 1 - self.desplazamiento(t)

    def aceleracion(self, t, h=1e-3):
        return (self.avance(t + h) - 2 * self.avance(t) + self.avance(max(t - h, 0))) / (h * h)

    def frames(self):
        return math.ceil(self.asentamiento * FPS)


# Color --------------------------------------------------------------------------------------------
def hex_lineal(hexa):
    h = hexa.lstrip('#')

    def canal(c):
        c = int(c, 16) / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return (canal(h[0:2]), canal(h[2:4]), canal(h[4:6]), 1.0)


def hexa(token):
    if token in COLOR:
        return COLOR[token][:7]
    if token in PRIMITIVO:
        return PRIMITIVO[token][:7]
    raise KeyError(f'color sin token: {token}')


def color(token):
    return hex_lineal(hexa(token))


def rgb(token):
    return color(token)[:3]


# Escena -------------------------------------------------------------------------------------------
def vaciar():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def configurar(escena, ancho, alto, inicio, fin, transparente, muestras=16):
    escena.render.fps, escena.render.fps_base = FPS, 1
    escena.render.resolution_x, escena.render.resolution_y = ancho, alto
    escena.render.resolution_percentage = 100
    escena.frame_start, escena.frame_end = inicio, fin
    escena.render.engine = 'BLENDER_EEVEE_NEXT'
    ev = escena.eevee
    ev.taa_render_samples = muestras
    ev.use_shadows = True
    ev.shadow_ray_count, ev.shadow_step_count = 2, 8
    ev.use_raytracing = True
    ev.ray_tracing_method = 'SCREEN'
    ev.ray_tracing_options.resolution_scale = '2'
    ev.use_gtao = True
    ev.gtao_distance = 0.6
    escena.render.film_transparent = transparente
    escena.render.filter_size = 1.2
    im = escena.render.image_settings
    im.file_format, im.color_mode, im.color_depth, im.compression = 'PNG', 'RGBA', '8', 15
    # Standard: los hex de marca salen exactos. La compresión de luces la hace la curva de tono del compositor.
    escena.view_settings.view_transform = 'Standard'
    escena.view_settings.look = 'None'
    escena.view_settings.exposure = 0.0
    escena.view_settings.gamma = 1.0
    escena.sequencer_colorspace_settings.name = 'sRGB'


def escalar_compositor(escena):
    """Las distancias en px del compositor (erosión) siguen al porcentaje de resolución (miniaturas al 50 %)."""
    f = escena.render.resolution_percentage / 100
    for n in escena.node_tree.nodes:
        if n.bl_idname == 'CompositorNodeDilateErode' and 'base' in n:
            n.distance = round(n['base'] * f)


def aovs(escena):
    vl = escena.view_layers[0]
    for nombre, tipo in (('marca', 'VALUE'), ('brillo', 'COLOR')):
        if nombre not in vl.aovs:
            a = vl.aovs.add()
            a.name, a.type = nombre, tipo
    return vl


def _sombra_token(grupo, nombre, capa):
    t = _DTCG['semantico'][grupo][nombre]['$value'][capa]
    d = {c: t[c]['value'] for c in ('offsetX', 'offsetY', 'blur', 'spread')}
    d['color'] = t['color'].strip('{}').replace('primitivo.color.', '').replace('.', '/')
    return d


RELIEVE_SOMBRA = _sombra_token('relieve', 'membrana', 1)
RESPLANDOR_ANILLO = _sombra_token('resplandor', 'vigente', 0)
RESPLANDOR_HALO = _sombra_token('resplandor', 'vigente', 1)


def compositor(escena, brillo=(0.006, 0.02), fuerza_brillo=(1.0, 0.6), destello=0.0, transparente=True, caja=None):
    """Curva de tono, marcas exactas y los tokens de sombra de la marca.

    brillo: radios (fracción del ancho) del halo de la AOV brillo (el punto que late, el indicador del lector).
    destello: glare de las luces prácticas neutras de la escena (farolas, ventanas); 0 lo apaga.
    caja: px de render por px del sistema. Si se da, se aplican bajo la imagen, como box-shadow, los tokens
      relieve/membrana (sombra) y resplandor/vigente (anillo y halo), con la silueta del alfa. La fuerza del
      resplandor es el nodo «resplandor» (0 = no hay Pase vigente), que se anima desde la escena.
    El blur CSS se traduce a un filtro gaussiano de tamaño 1,5 × blur (σ ≈ blur / 2, como en CSS).
    """
    aovs(escena)
    escena.use_nodes = True
    nt = escena.node_tree
    nt.nodes.clear()
    N, L = nt.nodes, nt.links
    ancho, alto = escena.render.resolution_x, escena.render.resolution_y
    capas = N.new('CompositorNodeRLayers')
    salida = N.new('CompositorNodeComposite')
    salida.use_alpha = True
    visor = N.new('CompositorNodeViewer')

    def val(x):
        return x if not isinstance(x, (int, float)) else None

    def mat(op, a, b=None, clamp=False):
        n = N.new('CompositorNodeMath')
        n.operation = op
        n.use_clamp = clamp
        for i, x in enumerate((a, b)):
            if x is None:
                continue
            if isinstance(x, (int, float)):
                n.inputs[i].default_value = x
            else:
                L.new(x, n.inputs[i])
        return n.outputs[0]

    def separar(s):
        n = N.new('CompositorNodeSeparateColor')
        L.new(s, n.inputs[0])
        return n.outputs

    def lum(r, g, b):
        return mat('ADD', mat('ADD', mat('MULTIPLY', r, 0.2126), mat('MULTIPLY', g, 0.7152)), mat('MULTIPLY', b, 0.0722))

    def desenfocar(s, px, tipo='GAUSS'):
        bl = N.new('CompositorNodeBlur')
        bl.filter_type = tipo
        bl.use_relative = True
        bl.aspect_correction = 'NONE'
        bl.factor_x = bl.factor_y = 100 * px / ancho
        L.new(s, bl.inputs[0])
        return bl.outputs[0]

    def dilatar(s, px):
        n = N.new('CompositorNodeDilateErode')
        n.mode = 'DISTANCE'
        n.distance = round(px)
        n['base'] = n.distance
        L.new(s, n.inputs[0])
        return n.outputs[0]

    # 1. Curva de tono: Reinhard extendido sobre la luminancia (conserva el tono) y paso suave al blanco arriba.
    r, g, b, a = separar(capas.outputs['Image'])
    l = lum(r, g, b)
    ton = mat('DIVIDE', mat('MULTIPLY', l, mat('ADD', mat('DIVIDE', l, 36.0), 1.0)), mat('ADD', l, 1.0))
    esc = mat('DIVIDE', ton, mat('MAXIMUM', l, 1e-5))
    blanco = mat('MULTIPLY', mat('POWER', mat('DIVIDE', mat('SUBTRACT', ton, 0.55), 0.45, clamp=True), 2.0), 0.6)
    comb = N.new('CompositorNodeCombineColor')
    for i, c in enumerate((r, g, b)):
        c2 = mat('MULTIPLY', c, esc)
        L.new(mat('ADD', c2, mat('MULTIPLY', mat('SUBTRACT', ton, c2), blanco)), comb.inputs[i])
    L.new(a, comb.inputs[3])
    # 2. Marcas exactas: donde la AOV marca vale 1 se usa la imagen sin curva (Standard: el hex del token).
    exacta = N.new('CompositorNodeMixRGB')
    L.new(capas.outputs['marca'], exacta.inputs[0])
    L.new(comb.outputs[0], exacta.inputs[1])
    L.new(capas.outputs['Image'], exacta.inputs[2])
    imagen = exacta.outputs[0]
    # 3. Destello neutro de las luces prácticas.
    if destello > 0:
        gl = N.new('CompositorNodeGlare')
        gl.glare_type, gl.quality, gl.threshold, gl.size, gl.mix = 'FOG_GLOW', 'HIGH', 0.9, 8, -1 + destello
        L.new(imagen, gl.inputs[0])
        imagen = gl.outputs[0]
    # 4. Brillo de lo activo (AOV brillo): halo encima, fuera del núcleo de cada marca.
    halo = None
    for radio, fuerza in zip(brillo, fuerza_brillo):
        h = N.new('CompositorNodeMixRGB')
        h.blend_type = 'MULTIPLY'
        L.new(desenfocar(capas.outputs['brillo'], radio * ancho, 'FAST_GAUSS'), h.inputs[1])
        h.inputs[2].default_value = (fuerza, fuerza, fuerza, 1)
        if halo is not None:
            s = N.new('CompositorNodeMixRGB')
            s.blend_type = 'ADD'
            L.new(halo, s.inputs[1])
            L.new(h.outputs[0], s.inputs[2])
            h = s
        halo = h.outputs[0]
    ir, ig, ib, ia = separar(imagen)
    hr, hg, hb, _ = separar(halo)
    fuera = mat('SUBTRACT', 1.0, capas.outputs['marca'], clamp=True)
    arriba = [mat('ADD', c, mat('MULTIPLY', h, fuera)) for c, h in zip((ir, ig, ib), (hr, hg, hb))]
    alfa = ia
    if transparente:
        alfa = mat('ADD', ia, mat('MULTIPLY', mat('SUBTRACT', 1.0, ia, clamp=True),
                                  mat('MINIMUM', mat('MULTIPLY', lum(hr, hg, hb), 1.6), 1.0)))
    # 5. Bajo la imagen (box-shadow): relieve/membrana y resplandor/vigente con la silueta del alfa.
    if caja:
        rs, an, hl = RELIEVE_SOMBRA, RESPLANDOR_ANILLO, RESPLANDOR_HALO
        sil = a
        sombra = desenfocar(dilatar(sil, rs['spread'] * caja), 1.5 * rs['blur'] * caja)
        tr = N.new('CompositorNodeTranslate')
        tr.use_relative = True
        L.new(sombra, tr.inputs[0])
        tr.inputs['X'].default_value = rs['offsetX'] * caja / ancho
        tr.inputs['Y'].default_value = -rs['offsetY'] * caja / alto
        sombra = tr.outputs[0]
        fuerza = N.new('CompositorNodeValue')
        fuerza.name = fuerza.label = 'resplandor'
        fuerza.outputs[0].default_value = 0.0
        anillo = mat('MULTIPLY', mat('SUBTRACT', dilatar(sil, an['spread'] * caja), sil, clamp=True), fuerza.outputs[0])
        glow = mat('MULTIPLY', desenfocar(dilatar(sil, hl['spread'] * caja), 1.5 * hl['blur'] * caja), fuerza.outputs[0])
        ca, ch, cs = rgb(an['color']), rgb(hl['color']), rgb(rs['color'])
        # Capa de abajo (premultiplicada): halo encima de la sombra y el anillo encima de los dos.
        ab_a = mat('ADD', glow, mat('MULTIPLY', sombra, mat('SUBTRACT', 1.0, glow, clamp=True)))
        ab_a = mat('ADD', anillo, mat('MULTIPLY', ab_a, mat('SUBTRACT', 1.0, anillo, clamp=True)))
        abajo = []
        for i in range(3):
            v = mat('ADD', mat('MULTIPLY', glow, ch[i]), mat('MULTIPLY', mat('MULTIPLY', sombra, mat('SUBTRACT', 1.0, glow, clamp=True)), cs[i]))
            abajo.append(mat('ADD', mat('MULTIPLY', anillo, ca[i]), mat('MULTIPLY', v, mat('SUBTRACT', 1.0, anillo, clamp=True))))
        resto = mat('SUBTRACT', 1.0, alfa, clamp=True)
        arriba = [mat('ADD', c, mat('MULTIPLY', d, resto)) for c, d in zip(arriba, abajo)]
        alfa = mat('ADD', alfa, mat('MULTIPLY', ab_a, resto))
    fin = N.new('CompositorNodeCombineColor')
    for i, c in enumerate(arriba):
        L.new(c, fin.inputs[i])
    if transparente:
        L.new(alfa, fin.inputs[3])
    else:
        fin.inputs[3].default_value = 1.0
    L.new(fin.outputs[0], salida.inputs['Image'])
    L.new(fin.outputs[0], visor.inputs['Image'])


def resplandor(escena):
    """Socket animable de la fuerza de resplandor/vigente en el compositor."""
    return escena.node_tree.nodes['resplandor'].outputs[0]


# Materiales ---------------------------------------------------------------------------------------
def _nuevo(nombre):
    m = bpy.data.materials.get(nombre) or bpy.data.materials.new(nombre)
    m.use_nodes = True
    m.node_tree.nodes.clear()
    m.surface_render_method = 'DITHERED'
    return m


def driver_opacidad(nt, objeto='root', prop='opacidad'):
    """Nodo Value que lee root['opacidad'] (la opacidad de la tarjeta entera, como el elemento .tarjeta de la web)."""
    v = nt.nodes.new('ShaderNodeValue')
    v.name = v.label = 'raiz'
    d = v.outputs[0].driver_add('default_value').driver
    var = d.variables.new()
    var.name, var.type = 'op', 'SINGLE_PROP'
    var.targets[0].id = bpy.data.objects[objeto]
    var.targets[0].data_path = f'["{prop}"]'
    d.expression = 'op'
    return v.outputs[0]


def marca(nombre, token, brillo=0.0, raiz=True):
    """Marca plana de estado: emisión 1 del token (sale con su hex exacto), AOV marca = 1 y AOV brillo = color × brillo.

    Nodos animables: «color» (Color), «local» (opacidad propia) y «brillo» (fuerza del resplandor)."""
    m = _nuevo(nombre)
    nt = m.node_tree
    N, L = nt.nodes, nt.links
    out = N.new('ShaderNodeOutputMaterial')
    em = N.new('ShaderNodeEmission')
    em.name = 'emision'
    rgbn = N.new('ShaderNodeRGB')
    rgbn.name = 'color'
    rgbn.outputs[0].default_value = color(token)
    L.new(rgbn.outputs[0], em.inputs['Color'])
    em.inputs['Strength'].default_value = 1.0
    tr = N.new('ShaderNodeBsdfTransparent')
    mix = N.new('ShaderNodeMixShader')
    local = N.new('ShaderNodeValue')
    local.name = 'local'
    local.outputs[0].default_value = 1.0
    alfa = local.outputs[0]
    if raiz:
        mu = N.new('ShaderNodeMath')
        mu.operation = 'MULTIPLY'
        L.new(driver_opacidad(nt), mu.inputs[0])
        L.new(local.outputs[0], mu.inputs[1])
        alfa = mu.outputs[0]
    L.new(alfa, mix.inputs['Fac'])
    L.new(tr.outputs[0], mix.inputs[1])
    L.new(em.outputs[0], mix.inputs[2])
    L.new(mix.outputs[0], out.inputs['Surface'])
    aov_m = N.new('ShaderNodeOutputAOV')
    aov_m.aov_name = 'marca'
    aov_m.inputs['Value'].default_value = 1.0
    b = N.new('ShaderNodeValue')
    b.name = 'brillo'
    b.outputs[0].default_value = brillo
    mb = N.new('ShaderNodeVectorMath')
    mb.operation = 'SCALE'
    L.new(rgbn.outputs[0], mb.inputs[0])
    L.new(b.outputs[0], mb.inputs['Scale'])
    aov_b = N.new('ShaderNodeOutputAOV')
    aov_b.aov_name = 'brillo'
    L.new(mb.outputs[0], aov_b.inputs['Color'])
    return m


def nodo(m, nombre):
    return m.node_tree.nodes[nombre]


def principled(nombre, token, rugosidad=0.5, metalico=0.0, **extra):
    m = _nuevo(nombre)
    nt = m.node_tree
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    p = nt.nodes.new('ShaderNodeBsdfPrincipled')
    p.name = 'bsdf'
    p.inputs['Base Color'].default_value = color(token)
    p.inputs['Roughness'].default_value = rugosidad
    p.inputs['Metallic'].default_value = metalico
    for k, v in extra.items():
        p.inputs[k].default_value = color(v) if isinstance(v, str) else v
    nt.links.new(p.outputs[0], out.inputs['Surface'])
    return m, p


def ruido(nt, escala, detalle=6.0, rugosidad=0.55, coord=None, dim='3D'):
    n = nt.nodes.new('ShaderNodeTexNoise')
    n.noise_dimensions = dim
    n.inputs['Scale'].default_value = escala
    n.inputs['Detail'].default_value = detalle
    n.inputs['Roughness'].default_value = rugosidad
    if coord is not None:
        nt.links.new(coord, n.inputs['Vector'])
    return n


def rampa(nt, entrada, puntos):
    """ColorRamp con (posición, color o valor)."""
    cr = nt.nodes.new('ShaderNodeValToRGB')
    el = cr.color_ramp.elements
    while len(el) > len(puntos):
        el.remove(el[-1])
    while len(el) < len(puntos):
        el.new(0.5)
    for e, (pos, val) in zip(el, puntos):
        e.position = pos
        e.color = color(val) if isinstance(val, str) else (val, val, val, 1) if isinstance(val, (int, float)) else val
    nt.links.new(entrada, cr.inputs[0])
    return cr.outputs[0]


def microvariacion(m, p, tono_a, tono_b, escala=40.0, rug=(0.35, 0.5), bump=0.02, escala_bump=180.0):
    """Sustrato con microvariación procedural: color entre dos tokens, rugosidad variable y un relieve fino."""
    nt = m.node_tree
    tc = nt.nodes.new('ShaderNodeTexCoord')
    n = ruido(nt, escala, coord=tc.outputs['Object'])
    base = rampa(nt, n.outputs['Fac'], [(0.3, tono_a), (0.7, tono_b)])
    base.node.name = 'rampa-base'
    nt.links.new(base, p.inputs['Base Color'])
    nt.links.new(rampa(nt, n.outputs['Fac'], [(0.25, rug[0]), (0.75, rug[1])]), p.inputs['Roughness'])
    if bump:
        nf = ruido(nt, escala_bump, detalle=4, coord=tc.outputs['Object'])
        bu = nt.nodes.new('ShaderNodeBump')
        bu.inputs['Strength'].default_value = bump
        nt.links.new(nf.outputs['Fac'], bu.inputs['Height'])
        nt.links.new(bu.outputs[0], p.inputs['Normal'])
    return n


def captura_sombra(nombre, fuerza=0.85, token='superficie/abismo'):
    """Plano que solo muestra la sombra (EEVEE: Shader to RGB). Traduce el relieve de membrana a 3D en fondos transparentes."""
    m = _nuevo(nombre)
    nt = m.node_tree
    N, L = nt.nodes, nt.links
    out = N.new('ShaderNodeOutputMaterial')
    dif = N.new('ShaderNodeBsdfDiffuse')
    dif.inputs['Color'].default_value = (1, 1, 1, 1)
    s2r = N.new('ShaderNodeShaderToRGB')
    L.new(dif.outputs[0], s2r.inputs[0])
    bw = N.new('ShaderNodeRGBToBW')
    L.new(s2r.outputs[0], bw.inputs[0])
    # 1 − luz recibida: sombra; se normaliza con la luz que llega sin obstáculo (≈ 1 tras el mapeo).
    mp = N.new('ShaderNodeMapRange')
    mp.inputs['From Min'].default_value = 0.0
    mp.inputs['From Max'].default_value = 1.0
    mp.inputs['To Min'].default_value = fuerza
    mp.inputs['To Max'].default_value = 0.0
    L.new(bw.outputs[0], mp.inputs['Value'])
    mu = N.new('ShaderNodeMath')
    mu.operation = 'MULTIPLY'
    L.new(mp.outputs[0], mu.inputs[0])
    L.new(driver_opacidad(nt), mu.inputs[1])
    em = N.new('ShaderNodeEmission')
    em.inputs['Color'].default_value = color(token)
    tr = N.new('ShaderNodeBsdfTransparent')
    mix = N.new('ShaderNodeMixShader')
    L.new(mu.outputs[0], mix.inputs['Fac'])
    L.new(tr.outputs[0], mix.inputs[1])
    L.new(em.outputs[0], mix.inputs[2])
    L.new(mix.outputs[0], out.inputs['Surface'])
    return m, mp


# Luces --------------------------------------------------------------------------------------------
def luz(nombre, tipo, token, energia, pos, mirar=None, tam=1.0, **extra):
    li = bpy.data.lights.new(nombre, tipo)
    li.color = rgb(token)
    li.energy = energia
    if tipo == 'AREA':
        li.shape = extra.pop('forma', 'RECTANGLE')
        li.size, li.size_y = tam, extra.pop('tam_y', tam)
    elif tipo in ('POINT', 'SPOT'):
        li.shadow_soft_size = tam
    for k, v in extra.items():
        setattr(li, k, v)
    ob = bpy.data.objects.new(nombre, li)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = pos
    if mirar is not None:
        apuntar(ob, mirar)
    return ob


def apuntar(ob, destino):
    if isinstance(destino, bpy.types.Object):
        c = ob.constraints.new('TRACK_TO')
        c.target, c.track_axis, c.up_axis = destino, 'TRACK_NEGATIVE_Z', 'UP_Y'
    else:
        from mathutils import Vector
        d = Vector(destino) - Vector(ob.location)
        ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()


# Animación ----------------------------------------------------------------------------------------
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
    for kk in (k0, k1):
        kk.interpolation = 'BEZIER'
        kk.handle_left_type = kk.handle_right_type = 'FREE'
    dt, dv = t1 - t0, v1 - v0
    k0.handle_right = (t0 + x1 * dt, v0 + y1 * dv)
    k1.handle_left = (t0 + x2 * dt, v0 + y2 * dv)
    # El valor final se sostiene hasta la clave siguiente (no interpola hacia el estado del clip que viene).
    k1.interpolation = 'CONSTANT'
    fc.update()


def fijar(dueno, ruta, indice, t, v):
    """Clave constante: deja un valor fijo desde t (inicio de cada clip)."""
    _poner(dueno, ruta, indice, v)
    dueno.keyframe_insert(ruta, index=indice, frame=t)
    fc = _fcurva(dueno, ruta, indice)
    for kk in fc.keyframe_points:
        if kk.co.x == t:
            kk.interpolation = 'CONSTANT'
    fc.update()


def hornear(dueno, ruta, indice, t0, n, funcion, final=None):
    """Una clave lineal por frame: funcion(i) para i = 0 … n. Para resortes y movimientos derivados (inercia)."""
    for i in range(n + 1):
        _poner(dueno, ruta, indice, funcion(i))
        dueno.keyframe_insert(ruta, index=indice, frame=t0 + i)
    fc = _fcurva(dueno, ruta, indice)
    for kk in fc.keyframe_points:
        if t0 <= kk.co.x <= t0 + n:
            kk.interpolation = 'LINEAR'
    if final is not None:
        fijar(dueno, ruta, indice, t0 + n + 1, final)
    fc.update()


def resorte(dueno, ruta, indice, t0, v0, v1, nombre):
    """Lleva un valor de v0 a v1 con un resorte del sistema, horneado frame a frame. Devuelve el frame final."""
    r = Resorte(nombre)
    n = r.frames()
    hornear(dueno, ruta, indice, t0, n, lambda i: v0 + (v1 - v0) * r.avance(i / FPS))
    fijar(dueno, ruta, indice, t0 + n, v1)
    return t0 + n


def _poner(dueno, ruta, indice, v):
    if ruta.startswith('['):
        dueno[ruta[2:-2]] = v
        return
    actual = getattr(dueno, ruta)
    if indice >= 0 and hasattr(actual, '__len__'):
        actual[indice] = v
    else:
        setattr(dueno, ruta, v)


def _fcurva(dueno, ruta, indice):
    if isinstance(dueno, bpy.types.ID):
        accion = dueno.animation_data.action
        ruta_completa = ruta
    else:  # sockets, elementos de rampa: la curva vive en el árbol de nodos
        accion = dueno.id_data.animation_data.action
        ruta_completa = dueno.path_from_id(ruta)
    idx = max(indice, 0)
    return next(f for f in accion.fcurves if f.data_path == ruta_completa and f.array_index == idx)


def tramos_encadenados(dueno, ruta, indice, puntos, nombre_curva):
    for (t0, v0), (t1, v1) in zip(puntos, puntos[1:]):
        tramo(dueno, ruta, indice, t0, t1, v0, v1, nombre_curva)


def tramo_color(socket, t0, t1, desde, hasta, nombre_curva):
    for i, (a, b) in enumerate(zip(rgb(desde), rgb(hasta))):
        tramo(socket, 'default_value', i, t0, t1, a, b, nombre_curva)


def fijar_color(socket, t, token):
    for i, c in enumerate(rgb(token)):
        fijar(socket, 'default_value', i, t, c)


# Archivo ------------------------------------------------------------------------------------------
def guardar(ruta):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(ruta), compress=True)


def abrir(ruta):
    bpy.ops.wm.open_mainfile(filepath=str(ruta))
