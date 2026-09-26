"""Genera el Lottie JSON fuente de los recursos «lottie» del inventario de motion de Kino.

    python3 generar.py            # escribe fuente/<id>.json, fuente/<id>.reducido.json, temas/ y manifiesto.json

Reglas que cumple el código:
- Duraciones, curvas, escalonados y distancias salen de tokens.py (DTCG del repositorio). Aquí no hay milisegundos.
- Cada color es un slot de tema (propiedad con «sid» y entrada en «slots»). El id del slot es el token semántico con
  guiones: estado/vigente/borde → estado-vigente-borde. temas/oscuro.json y temas/claro.json traen los valores.
- Los textos también son slots (tipo texto): el pipeline puede cambiar nombre, hora o casa sin tocar la animación.
- Cambiar de estado es un fundido cruzado entre dos capas con colores fijos: así cada color sigue siendo un slot.
- La variante reducida cambia desplazamientos por fundidos con la misma duración y el mismo orden; el latido se detiene.
- Lo que entra subiendo lleva distancia/subida de margen bajo la pieza para que el lienzo no lo recorte.

Los recursos bloqueados (flujo-trazo, loader-espera-lector, onboarding-3-lector-confirma) no se generan: su curva no
está definida en el sistema. Ver BLOQUEADOS al final.
"""
import json
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))
import tokens as tk  # noqa: E402

T = tk.cargar('oscuro')
T_CLARO = tk.cargar('claro')
FPS = T['fps']
F = lambda nombre: tk.resolver_duracion(T, nombre)  # noqa: E731
C = lambda nombre: tk.resolver_curva(T, nombre)  # noqa: E731
SUBIDA = T['distancia']['subida']
R_TARJETA, R_CONTROL, R_CHIP = T['radio']['tarjeta'], T['radio']['control'], T['radio']['chip']
LINEA = T['linea']['fino']
ESP = T['espacio']

FUENTES = {
    'Archivo-Regular': ('Archivo', 'Regular', 'https://fonts.googleapis.com/css2?family=Archivo:wght@400&display=block'),
    'Archivo-Bold': ('Archivo', 'Bold', 'https://fonts.googleapis.com/css2?family=Archivo:wght@700&display=block'),
    'JetBrainsMono-Regular': ('JetBrains Mono', 'Regular', 'https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400&display=block'),
}
# Ancho medio de un carácter en em, solo para maquetar chips y tachados (no es un valor de movimiento).
ANCHO_EM = {'Archivo-Bold': 0.56, 'Archivo-Regular': 0.52, 'JetBrainsMono-Regular': 0.6}


def rgba(hexa):
    h = hexa.lstrip('#')
    a = int(h[6:8], 16) / 255 if len(h) == 8 else 1
    return [round(int(h[i:i + 2], 16) / 255, 4) for i in (0, 2, 4)] + [round(a, 4)]


def sid(token):
    return token.replace('/', '-')


class Lienzo:
    """Una animación Lottie en construcción."""

    def __init__(self, id_, ancho, alto, op, loop=False):
        self.id, self.w, self.h, self.op, self.loop = id_, ancho, alto, op, loop
        self.slots, self.assets, self.capas, self.textos = {}, [], [], []
        self._ind = 0

    # Propiedades -----------------------------------------------------------
    def color(self, token):
        if token not in T['color']:
            raise KeyError(f'color sin token: {token}')
        k = rgba(T['color'][token])
        self.slots[sid(token)] = {'p': {'a': 0, 'k': k}}
        return {'a': 0, 'k': k, 'sid': sid(token)}

    # Capas -----------------------------------------------------------------
    def ind(self):
        self._ind += 1
        return self._ind


def fijo(v):
    return {'a': 0, 'k': v}


def kf(t0, t1, v0, v1, curva):
    """Dos claves con la curva del token (cubic-bezier x1 y1 x2 y2)."""
    x1, y1, x2, y2 = curva
    n = len(v0)
    return {'a': 1, 'k': [{'t': t0, 's': v0, 'o': {'x': [x1] * n, 'y': [y1] * n}, 'i': {'x': [x2] * n, 'y': [y2] * n}},
                          {'t': t1, 's': v1}]}


def kfs(tramos):
    """Varios tramos encadenados: [(t0, t1, v0, v1, curva), ...]."""
    k = []
    for i, (t0, t1, v0, v1, curva) in enumerate(tramos):
        x1, y1, x2, y2 = curva
        n = len(v0)
        k.append({'t': t0, 's': v0, 'o': {'x': [x1] * n, 'y': [y1] * n}, 'i': {'x': [x2] * n, 'y': [y2] * n}})
        if i == len(tramos) - 1:
            k.append({'t': t1, 's': v1})
    return {'a': 1, 'k': k}


def ks(p=(0, 0), o=None, pos=None, s=None, a=(0, 0)):
    return {'o': o or fijo(100), 'r': fijo(0), 'p': pos or fijo([p[0], p[1], 0]), 'a': fijo([a[0], a[1], 0]),
            's': s or fijo([100, 100, 100])}


def capa_base(lz, nm, tipo, op, ks_, **extra):
    c = {'ddd': 0, 'ind': lz.ind(), 'ty': tipo, 'nm': nm, 'sr': 1, 'ks': ks_, 'ao': 0, 'ip': 0, 'op': op, 'st': 0, 'bm': 0}
    c.update(extra)
    return c


# Formas -----------------------------------------------------------------------
def rect(lz, x, y, w, h, r, relleno=None, borde=None, discontinuo=False, grosor=None):
    it = [{'ty': 'rc', 'd': 1, 'nm': 'rect', 's': fijo([w, h]), 'p': fijo([x + w / 2, y + h / 2]), 'r': fijo(r)}]
    if borde:
        st = {'ty': 'st', 'nm': 'borde', 'c': lz.color(borde), 'o': fijo(100), 'w': fijo(grosor or LINEA), 'lc': 2, 'lj': 2}
        if discontinuo:
            st['d'] = [{'n': 'd', 'nm': 'trazo', 'v': fijo(ESP['2xs'])}, {'n': 'g', 'nm': 'hueco', 'v': fijo(ESP['2xs'])}]
        it.append(st)
    if relleno and not transparente(relleno):
        it.append({'ty': 'fl', 'nm': 'relleno', 'c': lz.color(relleno), 'o': fijo(100), 'r': 1})
    it.append(tr())
    return {'ty': 'gr', 'nm': 'grupo', 'it': it}


def transparente(token):
    # Lottie ignora el alfa del color de relleno: un token transparente se dibuja sin relleno.
    return rgba(T['color'][token])[3] == 0


def circulo(lz, cx, cy, d, relleno=None, borde=None, discontinuo=False):
    it = [{'ty': 'el', 'd': 1, 'nm': 'punto', 's': fijo([d, d]), 'p': fijo([cx, cy])}]
    if borde:
        st = {'ty': 'st', 'nm': 'borde', 'c': lz.color(borde), 'o': fijo(100), 'w': fijo(LINEA), 'lc': 2, 'lj': 2}
        if discontinuo:
            st['d'] = [{'n': 'd', 'nm': 'trazo', 'v': fijo(ESP['3xs'])}, {'n': 'g', 'nm': 'hueco', 'v': fijo(ESP['3xs'])}]
        it.append(st)
    if relleno:
        it.append({'ty': 'fl', 'nm': 'relleno', 'c': lz.color(relleno), 'o': fijo(100), 'r': 1})
    it.append(tr())
    return {'ty': 'gr', 'nm': 'punto', 'it': it}


def linea(lz, x0, y0, x1, y1, token, grosor, recorte=None):
    it = [{'ty': 'sh', 'nm': 'linea', 'ks': fijo({'c': False, 'v': [[x0, y0], [x1, y1]], 'i': [[0, 0], [0, 0]], 'o': [[0, 0], [0, 0]]})},
          {'ty': 'st', 'nm': 'trazo', 'c': lz.color(token), 'o': fijo(100), 'w': fijo(grosor), 'lc': 2, 'lj': 2}]
    if recorte:
        it.append({'ty': 'tm', 'nm': 'recorte', 's': fijo(0), 'e': recorte, 'o': fijo(0), 'm': 1})
    it.append(tr())
    return {'ty': 'gr', 'nm': 'linea', 'it': it}


def tr():
    return {'ty': 'tr', 'p': fijo([0, 0]), 'a': fijo([0, 0]), 's': fijo([100, 100]), 'r': fijo(0), 'o': fijo(100)}


def formas(lz, nm, grupos, op, **kw):
    return capa_base(lz, nm, 4, op, ks(**kw), shapes=grupos)


def texto(lz, nm, cadena, x, y, fuente, tam, token, op, just=0, **kw):
    doc = {'s': tam, 'f': fuente, 't': cadena, 'j': just, 'tr': 0, 'lh': round(tam * 1.3, 2), 'ls': 0,
           'fc': rgba(T['color'][token])[:3]}
    clave = f'texto-{lz.id}-{len(lz.textos) + 1}'
    lz.textos.append({'slot': clave, 'texto': cadena, 'color': token})
    lz.slots[clave] = {'p': {'k': [{'s': doc, 't': 0}]}}
    lz.slots[sid(token)] = {'p': {'a': 0, 'k': rgba(T['color'][token])}}
    d = {'k': [{'s': doc, 't': 0}], 'sid': clave}
    return capa_base(lz, nm, 5, op, ks(p=(x, y), **kw),
                     t={'d': d, 'p': {}, 'm': {'g': 1, 'a': fijo([0, 0])}, 'a': []})


def ancho_texto(cadena, fuente, tam):
    return len(cadena) * tam * ANCHO_EM[fuente]


def precomp(lz, id_, capas, w, h):
    lz.assets.append({'id': id_, 'nm': id_, 'layers': capas, 'w': w, 'h': h})
    return id_


def capa_precomp(lz, nm, ref, w, h, op, **kw):
    return capa_base(lz, nm, 0, op, ks(**kw), refId=ref, w=w, h=h)


# Piezas de marca ---------------------------------------------------------------
ESTADOS = {
    'previsto': 'Previsto', 'sin-confirmar': 'Sin confirmar', 'vigente': 'Vigente', 'por-vencer': 'Por vencer',
    'usado': 'Usado', 'vencido': 'Vencido', 'revocado': 'Revocado', 'rechazado': 'Rechazado',
}


def chip(lz, estado, x_der, y, op, prefijo='chip'):
    """Chip de estado alineado a la derecha en x_der. Devuelve capas (texto arriba, forma abajo)."""
    etiqueta, tam = ESTADOS[estado], 13
    alto = ESP['l'] + ESP['3xs']
    punto = ESP['xs'] - ESP['3xs']
    w = ancho_texto(etiqueta, 'Archivo-Bold', tam) + ESP['s'] * 2 + punto + ESP['2xs'] + ESP['3xs']
    x = x_der - w
    discontinuo = estado == 'sin-confirmar'
    fondo = f'estado/{estado}/fondo'
    grupos = [circulo(lz, x + ESP['s'] + punto / 2, y + alto / 2, punto,
                      relleno=None if discontinuo else f'estado/{estado}/borde',
                      borde=f'estado/{estado}/borde' if discontinuo else None, discontinuo=discontinuo),
              rect(lz, x, y, w, alto, R_CHIP, relleno=fondo, borde=f'estado/{estado}/borde', discontinuo=discontinuo)]
    return [texto(lz, f'{prefijo}-{estado}-texto', etiqueta, x + ESP['s'] + punto + ESP['2xs'] + ESP['3xs'], y + alto / 2 + tam * 0.36,
                  'Archivo-Bold', tam, f'estado/{estado}/texto', op),
            formas(lz, f'{prefijo}-{estado}', grupos, op)], (x + ESP['s'] + punto / 2, y + alto / 2)


def tarjeta(lz, id_, estado, quien, dato, op, w=360, h=132, evidencia=None, barra=None, borde_estado=True,
            relleno='superficie/elevada', con_chip=True, fuente_quien='Archivo-Bold'):
    """Precomp de una tarjeta de Pase. dato y evidencia en JetBrains Mono."""
    capas = []
    compacta = h < 100  # filas de tabla: menos aire, mismo orden
    pad = ESP['m'] if compacta else ESP['m'] + ESP['2xs']
    if con_chip:
        cc, _ = chip(lz, estado, w - pad, pad - ESP['3xs'], op)
        capas += cc
    capas.append(texto(lz, 'quien', quien, pad, pad + 17, fuente_quien, 17, 'texto/primario', op))
    if dato:
        capas.append(texto(lz, 'dato', dato, pad, pad + 17 + (ESP['l'] if compacta else ESP['l'] + ESP['2xs']),
                           'JetBrainsMono-Regular', 13, 'texto/secundario', op))
    if evidencia:
        capas.append(texto(lz, 'evidencia', evidencia, pad, pad + 17 + ESP['2xl'], 'JetBrainsMono-Regular', 12, f'estado/{estado}/texto', op))
    if barra is not None:
        capas.append(formas(lz, 'vigencia', [rect(lz, pad, h - pad, (w - 2 * pad) * barra, ESP['2xs'], ESP['3xs'], relleno=f'estado/{estado}/borde'),
                                             rect(lz, pad, h - pad, w - 2 * pad, ESP['2xs'], ESP['3xs'], relleno='superficie/membrana')], op))
    borde = f'estado/{estado}/borde' if borde_estado else 'borde/tenue'
    capas.append(formas(lz, 'tarjeta', [rect(lz, LINEA / 2, LINEA / 2, w - LINEA, h - LINEA, R_TARJETA, relleno=relleno, borde=borde,
                                             discontinuo=estado == 'sin-confirmar')], op))
    return precomp(lz, id_, capas, w, h)


def boton(lz, id_, etiqueta, token_fondo, op, w=320, h=56):
    capas = [texto(lz, 'etiqueta', etiqueta, w / 2, h / 2 + 16 * 0.36, 'Archivo-Bold', 16, 'accion/texto', op, just=2),
             formas(lz, 'boton', [rect(lz, 0, 0, w, h, R_CONTROL, relleno=token_fondo)], op)]
    return precomp(lz, id_, capas, w, h)


# Movimientos por verbo ---------------------------------------------------------
def entrada(t0, verbo_dur, verbo_curva, x, y, reducido, subir=True):
    """crecer / aparecer: sube distancia/subida y funde. Reducido: solo funde."""
    d = F(verbo_dur)
    c = C(verbo_curva)
    o = kf(t0, t0 + d, [0], [100], c)
    if reducido or not subir:
        return {'p': (x, y), 'o': o}
    return {'o': o, 'pos': kf(t0, t0 + d, [x, y + SUBIDA, 0], [x, y, 0], c)}


def fundido(t0, verbo_dur, verbo_curva, desde, hasta):
    d = F(verbo_dur)
    return kf(t0, t0 + d, [desde], [hasta], C(verbo_curva))


# Recursos -----------------------------------------------------------------------
DATO = 'Casa 14 · hoy 4:00–6:00 p. m.'
ENVIADO = 'Enviado 3:41 p. m.'
EVIDENCIA = 'Confirmó Lector Portería · 3:58 p. m.'


def pase_aparecer(r):
    op = F('aparecer/duracion')
    lz = Lienzo('pase-aparecer', 360, 132 + SUBIDA, op)
    ref = tarjeta(lz, 'tarjeta-previsto', 'previsto', 'Andrés Gómez', DATO, op)
    lz.capas = [capa_precomp(lz, 'pase', ref, 360, 132, op, **entrada(0, 'aparecer/duracion', 'aparecer/curva', 0, 0, r))]
    return lz


def pase_cascada(r):
    esc = F('aparecer/escalonado')
    filas = [('vigente', 'Andrés Gómez', DATO), ('previsto', 'Luz Marina', 'Casa 3 · mañana 8:00 a. m.–12:00 m.'),
             ('sin-confirmar', 'Técnico del gas', 'Casa 22 · enviado 3:41 p. m.'), ('vencido', 'Diana Arango', 'Casa 9 · venció 2:00 p. m.')]
    h, gap = 132, ESP['xs'] + ESP['3xs']
    op = esc * (len(filas) - 1) + F('aparecer/duracion')
    lz = Lienzo('pase-cascada', 360, h * 4 + gap * 3 + SUBIDA, op)
    for i, (est, quien, dato) in enumerate(filas):
        ref = tarjeta(lz, f'tarjeta-{est}', est, quien, dato, op, evidencia=EVIDENCIA if est == 'vigente' else None)
        lz.capas.append(capa_precomp(lz, f'pase-{i + 1}', ref, 360, h, op,
                                     **entrada(i * esc, 'aparecer/duracion', 'aparecer/curva', 0, i * (h + gap), r)))
    return lz


def pase_latir(r):
    op = 1 if r else F('latir/duracion')
    lz = Lienzo('pase-latir', 24, 24, op, loop=not r)
    d = ESP['xs'] + ESP['3xs']
    base = formas(lz, 'punto', [circulo(lz, 12, 12, d, relleno='estado/vigente/borde')], op)
    if r:
        lz.capas = [base]
        return lz
    mitad = F('latir/duracion') // 2
    c = C('latir/curva')
    brillo = formas(lz, 'brillo', [circulo(lz, 12, 12, d, relleno='estado/vigente/texto')], op,
                    o=kfs([(0, mitad, [0], [100], c), (mitad, op, [100], [0], c)]))
    lz.capas = [brillo, base]
    return lz


def pase_caducar(r):
    op = F('caducar/duracion')
    lz = Lienzo('pase-caducar', 360, 8, op)
    c = C('caducar/curva')
    if r:
        barra = formas(lz, 'barra', [rect(lz, 0, 0, 360, 8, ESP['2xs'], relleno='estado/vigente/borde')], op,
                       o=kf(0, op, [100], [0], c))
    else:
        barra = formas(lz, 'barra', [rect(lz, 0, 0, 360, 8, ESP['2xs'], relleno='estado/vigente/borde')], op,
                       s=kf(0, op, [100, 100, 100], [0, 100, 100], c))
    borde_a = formas(lz, 'borde-vigente', [rect(lz, 0.5, 0.5, 359, 7, ESP['2xs'], borde='estado/vigente/borde')], op,
                     o=kf(0, op, [100], [0], c))
    borde_b = formas(lz, 'borde-vencido', [rect(lz, 0.5, 0.5, 359, 7, ESP['2xs'], borde='estado/vencido/borde')], op,
                     o=kf(0, op, [0], [100], c))
    pista = formas(lz, 'pista', [rect(lz, 0, 0, 360, 8, ESP['2xs'], relleno='superficie/membrana')], op)
    lz.capas = [borde_b, borde_a, barra, pista]
    return lz


def cruce(lz, op, t0, verbo, a, b, w=360, h=132):
    """Fundido cruzado entre dos precomps con el verbo dado."""
    d, c = F(f'{verbo}/duracion'), C(f'{verbo}/curva')
    ca = capa_precomp(lz, 'antes', a, w, h, op, o=kf(t0, t0 + d, [100], [0], c))
    cb = capa_precomp(lz, 'despues', b, w, h, op, o=kf(t0, t0 + d, [0], [100], c))
    return [cb, ca]


def pase_confirmar(r):
    op = F('aparecer/duracion')
    lz = Lienzo('pase-confirmar', 360, 132, op)
    a = tarjeta(lz, 'tarjeta-sin-confirmar', 'sin-confirmar', 'Andrés Gómez', ENVIADO, op)
    b = tarjeta(lz, 'tarjeta-vigente', 'vigente', 'Andrés Gómez', DATO, op, evidencia=EVIDENCIA)
    capas = cruce(lz, op, 0, 'aparecer', a, b)
    if not r:
        # El borde discontinuo se cierra: el hueco del trazo va a cero con la misma curva.
        for asset in lz.assets:
            if asset['id'] == 'tarjeta-sin-confirmar':
                for capa in asset['layers']:
                    for g in capa.get('shapes', []):
                        for it in g['it']:
                            if it.get('ty') == 'st' and 'd' in it:
                                hueco = it['d'][1]['v']['k']
                                it['d'][1]['v'] = kf(0, op, [hueco], [0], C('aparecer/curva'))
    lz.capas = capas
    return lz


def pase_por_vencer(r):
    op = F('responder/duracion')
    lz = Lienzo('pase-por-vencer', 360, 132, op)
    a = tarjeta(lz, 'tarjeta-vigente', 'vigente', 'Andrés Gómez', 'Casa 14 · vence 6:00 p. m.', op)
    b = tarjeta(lz, 'tarjeta-por-vencer', 'por-vencer', 'Andrés Gómez', 'Casa 14 · vence 6:00 p. m.', op)
    lz.capas = cruce(lz, op, 0, 'responder', a, b)
    return lz


def pase_revocar(r):
    op = F('revocar/duracion')
    lz = Lienzo('pase-revocar', 360, 132, op)
    a = tarjeta(lz, 'tarjeta-vigente', 'vigente', 'Andrés Gómez', DATO, op)
    b = tarjeta(lz, 'tarjeta-revocado', 'revocado', 'Andrés Gómez', DATO, op, relleno='superficie/base',
                evidencia='Revocó Carolina Ruiz · 4:10 p. m.')
    capas = cruce(lz, op, 0, 'revocar', a, b)
    if not r:
        corte = formas(lz, 'corte', [linea(lz, 0, 66, 360, 66, 'estado/revocado/texto', LINEA * 2,
                                           recorte=kf(0, op, [0], [100], C('revocar/curva')))], op)
        capas = [corte] + capas
    lz.capas = capas
    return lz


def pase_usar(r):
    op = F('responder/duracion')
    lz = Lienzo('pase-usar', 360, 132, op)
    codigo = '4817'
    a = tarjeta(lz, 'tarjeta-vigente', 'vigente', codigo, 'Código de un solo uso · Casa 14', op, fuente_quien='JetBrainsMono-Regular')
    b = tarjeta(lz, 'tarjeta-usado', 'usado', codigo, 'Usado 4:22 p. m. · Casa 14', op, fuente_quien='JetBrainsMono-Regular')
    capas = cruce(lz, op, 0, 'responder', a, b)
    pad = ESP['m'] + ESP['2xs']
    x1 = pad + ancho_texto(codigo, 'JetBrainsMono-Regular', 17)
    y = pad + 17 * 0.64
    c = C('responder/curva')
    if r:
        tachado = formas(lz, 'tachado', [linea(lz, pad, y, x1, y, 'estado/usado/texto', LINEA * 2)], op, o=kf(0, op, [0], [100], c))
    else:
        tachado = formas(lz, 'tachado', [linea(lz, pad, y, x1, y, 'estado/usado/texto', LINEA * 2, recorte=kf(0, op, [0], [100], c))], op)
    lz.capas = [tachado] + capas
    return lz


def fila_evento(lz, id_, estado, placa, detalle, motivo, op, w=480, h=96, fondo=None):
    pad = ESP['m']
    capas = []
    cc, _ = chip(lz, estado, w - pad, pad, op)
    capas += cc
    capas.append(texto(lz, 'placa', placa, pad, pad + 18, 'JetBrainsMono-Regular', 18, 'texto/primario', op))
    capas.append(texto(lz, 'detalle', detalle, pad, pad + 18 + ESP['l'], 'JetBrainsMono-Regular', 12, 'texto/secundario', op))
    if motivo:
        capas.append(texto(lz, 'motivo', motivo, pad, pad + 18 + ESP['l'] * 2, 'Archivo-Regular', 13, f'estado/{estado}/texto', op))
    capas.append(formas(lz, 'fila', [rect(lz, LINEA / 2, LINEA / 2, w - LINEA, h - LINEA, R_CONTROL,
                                          relleno=fondo or f'estado/{estado}/fondo', borde=f'estado/{estado}/borde')], op))
    return precomp(lz, id_, capas, w, h)


def entrada_rechazar(r):
    op = F('duracion/crecer')
    lz = Lienzo('entrada-rechazar', 480, 96 + SUBIDA, op)
    ref = fila_evento(lz, 'evento-rechazado', 'rechazado', 'KMN 305', 'Casa 14 · 6:12 p. m.', 'Pase vencido a las 6:00 p. m.', op)
    fila = capa_precomp(lz, 'evento', ref, 480, 96, op, **entrada(0, 'duracion/crecer', 'curva/crecer', 0, 0, r))
    if r:
        lz.capas = [fila]
        return lz
    destello = formas(lz, 'destello', [rect(lz, 0, 0, 480, 96, R_CONTROL, borde='estado/rechazado/borde', grosor=T['linea']['foco'])], op,
                      o=kf(0, op, [100], [0], C('curva/crecer')), pos=kf(0, op, [0, SUBIDA, 0], [0, 0, 0], C('curva/crecer')))
    lz.capas = [destello, fila]
    return lz


def burbuja(lz, id_, op, w=320, h=104):
    pad = ESP['m']
    capas = [texto(lz, 'mensaje-1', 'Carolina Ruiz, de la Casa 14, te dio', pad, pad + 15, 'Archivo-Regular', 15, 'texto/primario', op),
             texto(lz, 'mensaje-2', 'un Pase para hoy.', pad, pad + 15 + 21, 'Archivo-Regular', 15, 'texto/primario', op),
             texto(lz, 'mensaje-3', 'Vigencia 4:00–6:00 p. m.', pad, pad + 15 + 21 * 2 + ESP['2xs'], 'JetBrainsMono-Regular', 13, 'texto/secundario', op),
             formas(lz, 'burbuja', [rect(lz, 0, 0, w, h, R_TARJETA, relleno='superficie/membrana')], op)]
    return precomp(lz, id_, capas, w, h)


def enviar_capas(lz, op, r, dy=0):
    """pase-enviar: la tarjeta sube y se funde en la burbuja; debajo queda sin confirmar con la hora de envío."""
    d, c = F('aparecer/duracion'), C('aparecer/curva')
    t = tarjeta(lz, 'tarjeta-previsto', 'previsto', 'Andrés Gómez', DATO, op)
    b = burbuja(lz, 'burbuja', op)
    y_t, y_b = dy + 54, dy + 20
    sal = {'o': kf(0, d, [100], [0], c)}
    if not r:
        sal['pos'] = kf(0, d, [0, y_t, 0], [0, y_t - SUBIDA, 0], c)
    else:
        sal['p'] = (0, y_t)
    capa_t = capa_precomp(lz, 'pase', t, 360, 132, op, **sal)
    capa_b = capa_precomp(lz, 'mensaje', b, 320, 104, op, **entrada(0, 'aparecer/duracion', 'aparecer/curva', 20, y_b, r))
    cc, _ = chip(lz, 'sin-confirmar', 20 + 118, 0, op, prefijo='estado')
    estado = precomp(lz, 'estado-envio', cc + [texto(lz, 'enviado', ENVIADO, 118 + 20 + ESP['s'], 18, 'JetBrainsMono-Regular', 13, 'texto/tenue', op)], 320, 28)
    capa_e = capa_precomp(lz, 'estado', estado, 320, 28, op, p=(20 - 20, y_b + 104 + ESP['m']), o=kf(0, d, [0], [100], c))
    return [capa_e, capa_b, capa_t]


def pase_enviar(r):
    op = F('aparecer/duracion')
    lz = Lienzo('pase-enviar', 360, 240, op)
    lz.capas = enviar_capas(lz, op, r)
    return lz


def control_presionar(r):
    # El botón pasa de accion/fondo a accion/fondo-activo. La app reproduce el tramo al tocar y en reversa al soltar.
    # El desplazamiento «baja levemente» no se genera: el sistema no tiene token para su magnitud (ver BLOQUEADOS).
    op = F('responder/duracion')
    lz = Lienzo('control-presionar', 320, 56, op)
    a = boton(lz, 'boton-reposo', 'Crear Pase', 'accion/fondo', op)
    b = boton(lz, 'boton-activo', 'Crear Pase', 'accion/fondo-activo', op)
    lz.capas = cruce(lz, op, 0, 'responder', a, b, 320, 56)
    return lz


def presentacion_cortina(r):
    op = F('duracion/cortina')
    lz = Lienzo('presentacion-cortina', 1920, 1080, op)
    c = C('curva/cortina')
    izq = rect(lz, 0, 0, 960, 1080, 0, relleno='superficie/abismo')
    der = rect(lz, 960, 0, 960, 1080, 0, relleno='superficie/abismo')
    if r:
        lz.capas = [formas(lz, 'hojas', [izq, der], op, o=kf(0, op, [100], [0], c))]
    else:
        lz.capas = [formas(lz, 'hoja-izquierda', [izq], op, pos=kf(0, op, [0, 0, 0], [-960, 0, 0], c)),
                    formas(lz, 'hoja-derecha', [der], op, pos=kf(0, op, [0, 0, 0], [960, 0, 0], c))]
    return lz


def onboarding_1_crear(r):
    dr, da = F('responder/duracion'), F('aparecer/duracion')
    op = dr + da
    lz = Lienzo('onboarding-1-crear', 360, 480, op)
    cr = C('responder/curva')
    a = boton(lz, 'boton-reposo', 'Crear Pase', 'accion/fondo', op)
    b = boton(lz, 'boton-activo', 'Crear Pase', 'accion/fondo-activo', op)
    y_boton = 480 - 56 - ESP['l']
    # Tocar (0 → responder) y soltar (responder → 2 × responder): el mismo tramo de ida y vuelta.
    boton_b = capa_precomp(lz, 'boton-activo', b, 320, 56, op, p=(20, y_boton),
                           o=kfs([(0, dr, [0], [100], cr), (dr, 2 * dr, [100], [0], cr)]))
    boton_a = capa_precomp(lz, 'boton-reposo', a, 320, 56, op, p=(20, y_boton))
    t = tarjeta(lz, 'tarjeta-previsto', 'previsto', 'Andrés Gómez', DATO, op)
    pase = capa_precomp(lz, 'pase', t, 360, 132, op, **entrada(dr, 'aparecer/duracion', 'aparecer/curva', 0, 120, r))
    lz.capas = [pase, boton_b, boton_a]
    return lz


def onboarding_2_entregar(r):
    op = F('aparecer/duracion')
    lz = Lienzo('onboarding-2-entregar', 360, 480, op)
    lz.capas = enviar_capas(lz, op, r, dy=100)
    return lz


def loader_sincronizacion_lote(r):
    filas = [('Andrés Gómez', 'Casa 14'), ('Luz Marina', 'Casa 3'), ('Técnico del gas', 'Casa 22'),
             ('Diana Arango', 'Casa 9'), ('Jardinería', 'Casa 31')]
    esc, d = F('escalonado/filas'), F('aparecer/duracion')
    op = esc * (len(filas) - 1) + d
    w, h = 960, 480
    lz = Lienzo('loader-sincronizacion-lote', w, h, op)
    alto, gap, y0 = 72, ESP['xs'], 80
    # Contador exacto: cambia cuando cada fila termina de confirmarse.
    doc = lambda n: {'s': 15, 'f': 'JetBrainsMono-Regular', 't': f'{n} de {len(filas)} confirmados por el lector', 'j': 0, 'tr': 0,  # noqa: E731
                     'lh': 19.5, 'ls': 0, 'fc': rgba(T['color']['texto/secundario'])[:3]}
    claves = [{'s': doc(0), 't': 0}] + [{'s': doc(i + 1), 't': i * esc + d} for i in range(len(filas))]
    lz.slots['texto-loader-sincronizacion-lote-contador'] = {'p': {'k': claves}}
    lz.textos.append({'slot': 'texto-loader-sincronizacion-lote-contador', 'texto': doc(0)['t'], 'color': 'texto/secundario'})
    contador = capa_base(lz, 'contador', 5, op, ks(p=(ESP['l'], 56)),
                         t={'d': {'k': claves, 'sid': 'texto-loader-sincronizacion-lote-contador'}, 'p': {}, 'm': {'g': 1, 'a': fijo([0, 0])}, 'a': []})
    titulo = texto(lz, 'titulo', 'Envío al lector de Portería', ESP['l'], 32, 'Archivo-Bold', 20, 'texto/primario', op)
    capas = [titulo, contador]
    for i, (quien, casa) in enumerate(filas):
        a = tarjeta(lz, f'fila-{i}-sin-confirmar', 'sin-confirmar', quien, f'{casa} · enviado 3:41 p. m.', op, w=w - 2 * ESP['l'], h=alto)
        b = tarjeta(lz, f'fila-{i}-vigente', 'vigente', quien, f'{casa} · confirmado', op, w=w - 2 * ESP['l'], h=alto)
        y = y0 + i * (alto + gap)
        t0 = i * esc
        ca = capa_precomp(lz, f'fila-{i + 1}-antes', a, w - 2 * ESP['l'], alto, op, p=(ESP['l'], y), o=kf(t0, t0 + d, [100], [0], C('aparecer/curva')))
        cb = capa_precomp(lz, f'fila-{i + 1}-despues', b, w - 2 * ESP['l'], alto, op, p=(ESP['l'], y), o=kf(t0, t0 + d, [0], [100], C('aparecer/curva')))
        capas += [cb, ca]
    lz.capas = capas
    return lz


def vacio_primer_pase(r):
    op = F('aparecer/duracion')
    lz = Lienzo('vacio-primer-pase', 360, 480, op)
    c = C('aparecer/curva')
    vacio = texto(lz, 'vacio', 'Aún no hay Pases en la Casa 14.', 180, 200, 'Archivo-Regular', 15, 'texto/secundario', op, just=2,
                  o=kf(0, op, [100], [0], c))
    t = tarjeta(lz, 'tarjeta-previsto', 'previsto', 'Andrés Gómez', DATO, op)
    pase = capa_precomp(lz, 'pase', t, 360, 132, op, **entrada(0, 'aparecer/duracion', 'aparecer/curva', 0, 120, r))
    b = boton(lz, 'boton', 'Crear Pase', 'accion/fondo', op)
    boton_ = capa_precomp(lz, 'boton', b, 320, 56, op, p=(20, 480 - 56 - ESP['l']))
    lz.capas = [pase, vacio, boton_]
    return lz


RECURSOS = {
    'pase-aparecer': pase_aparecer, 'pase-cascada': pase_cascada, 'pase-latir': pase_latir, 'pase-caducar': pase_caducar,
    'pase-confirmar': pase_confirmar, 'pase-por-vencer': pase_por_vencer, 'pase-revocar': pase_revocar, 'pase-usar': pase_usar,
    'entrada-rechazar': entrada_rechazar, 'pase-enviar': pase_enviar, 'control-presionar': control_presionar,
    'presentacion-cortina': presentacion_cortina, 'onboarding-1-crear': onboarding_1_crear,
    'onboarding-2-entregar': onboarding_2_entregar, 'loader-sincronizacion-lote': loader_sincronizacion_lote,
    'vacio-primer-pase': vacio_primer_pase,
}

BLOQUEADOS = {
    'flujo-trazo': 'El sistema define duracion/trazo pero ningún verbo le asigna curva.',
    'loader-espera-lector': 'Usa flujo-trazo: misma curva sin definir.',
    'onboarding-3-lector-confirma': 'Usa flujo-trazo: misma curva sin definir.',
    'control-presionar (desplazamiento)': 'La spec dice «baja levemente», pero el sistema no tiene token para esa magnitud. Se entrega solo el cambio de color.',
}


def cerrar(lz):
    """En Lottie op es exclusivo: sin un frame más, el último frame visible no llega al valor final de la clave.
    Las piezas en loop no lo llevan (su último frame empalma con el primero)."""
    if lz.loop:
        return lz
    viejo, lz.op = lz.op, lz.op + 1
    for capa in lz.capas + [c for a in lz.assets for c in a['layers']]:
        if capa['op'] == viejo:
            capa['op'] = lz.op
    return lz


def a_json(lz):
    fuentes = [{'fName': k, 'fFamily': f, 'fStyle': s, 'ascent': 75, 'fPath': u, 'origin': 1} for k, (f, s, u) in FUENTES.items()]
    return {'v': '5.12.0', 'fr': FPS, 'ip': 0, 'op': lz.op, 'w': lz.w, 'h': lz.h, 'nm': lz.id, 'ddd': 0,
            'assets': lz.assets, 'fonts': {'list': fuentes}, 'layers': lz.capas, 'slots': lz.slots,
            'meta': {'g': 'Kino · branding/sistema/v3/motion/lottie/generar.py', 'd': f'{lz.id}; tema oscuro por defecto'}}


def tema_dotlottie(tokens_tema, slots):
    reglas = []
    for s in sorted(slots):
        if s.startswith('texto-'):
            continue
        token = next(k for k in tokens_tema['color'] if sid(k) == s)
        reglas.append({'id': s, 'type': 'Color', 'value': rgba(tokens_tema['color'][token])})
    return {'rules': reglas}


def main():
    fuente, temas = AQUI / 'fuente', AQUI / 'temas'
    fuente.mkdir(exist_ok=True)
    temas.mkdir(exist_ok=True)
    manifiesto, todos_slots, textos = [], set(), []
    for id_, fn in RECURSOS.items():
        for reducido in (False, True):
            lz = cerrar(fn(reducido))
            nombre = f'{id_}.reducido.json' if reducido else f'{id_}.json'
            (fuente / nombre).write_text(json.dumps(a_json(lz), ensure_ascii=False, separators=(',', ':')))
            todos_slots |= set(lz.slots)
            if not reducido:
                textos += [t['texto'] for t in lz.textos]
            manifiesto.append({'id': id_, 'reducido': reducido, 'archivo': f'fuente/{nombre}', 'fps': FPS, 'op': lz.op,
                               'ancho': lz.w, 'alto': lz.h, 'loop': lz.loop,
                               'slots_color': sorted(s for s in lz.slots if not s.startswith('texto-')),
                               'slots_texto': [t['slot'] for t in lz.textos]})
    for nombre, tema in (('oscuro', T), ('claro', T_CLARO)):
        (temas / f'{nombre}.json').write_text(json.dumps(tema_dotlottie(tema, todos_slots), ensure_ascii=False, indent=1) + '\n')
    (AQUI / 'manifiesto.json').write_text(json.dumps({'fps': FPS, 'recursos': manifiesto, 'bloqueados': BLOQUEADOS},
                                                     ensure_ascii=False, indent=1) + '\n')
    (AQUI / 'texto-visible.md').write_text('\n'.join(sorted(set(textos))) + '\n')
    print(f'{len(manifiesto)} archivos Lottie ({len(RECURSOS)} recursos × completo y reducido), '
          f'{len([s for s in todos_slots if not s.startswith("texto-")])} slots de color')


if __name__ == '__main__':
    main()
