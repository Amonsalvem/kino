"""Piezas comunes de los departamentos 03 a 12.
Todo valor visual sale de los tokens DTCG del cliente kino (gorr-brand-system). En el HTML del sitio
se usan variables --kino-*; los archivos descargables (SVG, PNG, JSON) llevan el hex resuelto."""
import html, json, pathlib, re, sys, urllib.parse

R = pathlib.Path(__file__).resolve().parent.parent          # branding/sistema/v3/sitio
GBS = R / '../../../../gorr-brand-system/clientes/kino'
sys.path.insert(0, str(R / '../fase3'))
from apca import lc, wcag  # noqa: E402  APCA-W3 0.1.9, reproduce reportes/contraste.json

e = html.escape
RES = json.loads((GBS / 'build/tokens.resuelto.json').read_text(encoding='utf8'))
PRIM = RES['primitivos']
OSC, CLA = RES['temas']['oscuro'], RES['temas']['claro']
CONTRASTE = json.loads((GBS / 'reportes/contraste.json').read_text(encoding='utf8'))
TIPO = json.loads((GBS / 'reportes/tipo.json').read_text(encoding='utf8'))
TOKENS_CSS = (GBS / 'build/kino-tokens.css').read_text(encoding='utf8')


def hx(nombre, tema='oscuro'):
    """Hex de una variable (sin «--»), buscando en el tema y luego en los primitivos."""
    t = OSC if tema == 'oscuro' else CLA
    return t.get(nombre) or PRIM[nombre]


# ───────────── Logo (reconstrucción desde PNG, ver Gobernanza) ─────────────
BLOQUE = ('M 3.483 0 H 96.517 A 3.483 3.483 0 0 1 100.000 3.483 V 101.824 H 0 V 3.483 A 3.483 3.483 0 0 1 3.483 0 Z '
          'M 18.242 86.567 V 46.766 A 31.675 31.675 0 0 1 81.592 46.766 V 86.567 Z')
GOTA = 'M 50.000 35.987 A 16.169 17.579 0 0 1 66.169 53.566 L 50.000 66.667 L 33.831 53.566 A 16.169 17.579 0 0 1 50.000 35.987 Z'
PALABRA = (R / '../fase3/wordmark.txt').read_text(encoding='utf8').strip()
VB = {'simbolo': '0 0 100 101.824', 'horizontal': '0 0 267.960 101.824', 'vertical': '0 0 100 140.023'}
PROP = {'simbolo': (100, 101.824), 'horizontal': (267.96, 101.824), 'vertical': (100, 140.023)}


def logo(forma='horizontal', bloque='var(--kino-marca-bloque)', gota='var(--kino-marca-gota)', palabra=None,
         clase='logo', etiqueta='Kino', attrs='', hex_=False):
    """SVG del logo. Con hex_=True los colores van como atributos (archivo descargable)."""
    palabra = palabra or bloque
    w, h = PROP[forma]
    pint = (lambda c: f'fill="{c}"') if hex_ else (lambda c: f'style="fill:{c}"')
    partes = [f'<path {pint(bloque)} fill-rule="evenodd" d="{BLOQUE}"/>', f'<path {pint(gota)} d="{GOTA}"/>']
    if forma == 'horizontal':
        partes.append(f'<g transform="translate(126.000 25.681) scale(1.4196)"><path {pint(palabra)} fill-rule="evenodd" d="{PALABRA}"/></g>')
    elif forma == 'vertical':
        partes.append(f'<g transform="translate(0 105.970)"><path {pint(palabra)} fill-rule="evenodd" d="{PALABRA}"/></g>')
    rol = f'role="img" aria-label="{e(etiqueta)}"' if etiqueta else 'aria-hidden="true"'
    tam = f'width="{w:g}" height="{h:g}"'
    cls = f' class="{clase}"' if clase and not hex_ else ''
    ns = ' xmlns="http://www.w3.org/2000/svg"' if hex_ else ''
    return f'<svg{ns}{cls} viewBox="{VB[forma]}" {tam} style="aspect-ratio:{w:g}/{h:g}" {rol} {attrs}>{"".join(partes)}</svg>'


def data_uri(texto, tipo='image/svg+xml'):
    return f'data:{tipo};charset=utf-8,' + urllib.parse.quote(texto, safe='')


def descarga(etiqueta, archivo, contenido, tipo='image/svg+xml', png=None):
    """Enlace de descarga junto a la regla que lo gobierna. png=(ancho, alto) agrega la versión PNG (la arma sitio.js)."""
    uri = data_uri(contenido, tipo)
    ext = archivo.rsplit('.', 1)[-1].upper()
    a = f'<a class="descarga" href="{uri}" download="{e(archivo)}"><svg class="ic" aria-hidden="true"><use href="#i-bajar"/></svg>{e(etiqueta)} <small>{ext}</small></a>'
    if png:
        a += (f'<button class="descarga" type="button" data-png="{e(archivo.rsplit(".", 1)[0])}.png" data-ancho="{png[0]}" data-alto="{png[1]}" data-src="{uri}">'
              f'<svg class="ic" aria-hidden="true"><use href="#i-bajar"/></svg>{e(etiqueta)} <small>PNG {png[0]} px</small></button>')
    return a


def descargas(*items):
    return f'<div class="descargas">{"".join(items)}</div>'


# ───────────── Estructura de sección ─────────────
def seccion(id_, num, titulo, grupo, que, para, cuando, cuerpo):
    return f'''<section class="vista" id="{id_}" data-titulo="{e(titulo)}" data-num="{num}" data-grupo="{e(grupo)}" hidden>
  <header class="abre">
    <p class="ojo">{num} · {e(grupo)}</p>
    <h1>{e(titulo)}</h1>
    <dl class="lector">
      <div><dt>Qué es</dt><dd>{que}</dd></div>
      <div><dt>Para qué sirve</dt><dd>{para}</dd></div>
      <div><dt>Cuándo se usa</dt><dd>{cuando}</dd></div>
    </dl>
  </header>
{cuerpo}
</section>'''


def sub(id_, titulo, h2, lede, cuerpo):
    l = f'<p class="lede">{lede}</p>' if lede else ''
    return f'''  <article class="sub" id="{id_}" data-titulo="{e(titulo)}">
    <h2>{h2}</h2>
    {l}
    {cuerpo}
  </article>'''


def traza(texto):
    """Regla 3 del encargo: qué rasgo de la plataforma justifica la decisión."""
    return f'<p class="traza">Responde a: {texto}</p>'


def caso(viz, texto, bien=True, clase=''):
    rot = 'Así' if bien else 'Así no'
    return (f'<figure class="caso {"bien" if bien else "mal"} {clase}"><div class="caso-viz">{viz}</div>'
            f'<figcaption><p class="caso-rot">{rot}</p><p>{texto}</p></figcaption></figure>')


def casos(*cs):
    return f'<div class="casos">{"".join(cs)}</div>'


def regla(titulo, texto, cuerpo='', por=''):
    return (f'<div class="regla"><h3>{titulo}</h3>{f"<p>{texto}</p>" if texto else ""}{cuerpo}'
            f'{traza(por) if por else ""}</div>')


def tabla(cab, filas, etiqueta, clase=''):
    th = ''.join(f'<th scope="col">{c}</th>' for c in cab)
    tr = ''.join('<tr>' + ''.join((f'<th scope="row">{c}</th>' if i == 0 else f'<td>{c}</td>') for i, c in enumerate(f)) + '</tr>' for f in filas)
    return (f'<div class="tabla-envoltura" role="region" aria-label="{e(etiqueta)}" tabindex="0">'
            f'<table class="tabla {clase}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>')


def g(termino, texto=None):
    """Enlace al glosario."""
    return f'<a class="g" href="#glosario.{termino}">{texto or termino}</a>'


def pend(texto):
    return f'<a class="pend" href="#gobernanza.pendientes">[pendiente: {texto}]</a>'


def chip(estado, texto):
    return f'<span class="kino-estado" data-estado="{estado}">{e(texto)}</span>'


ESTADOS = [
    ('previsto', 'Previsto', 'Pase creado para una franja futura.'),
    ('sin-confirmar', 'Sin confirmar', 'Enviado; el lector aún no responde.'),
    ('vigente', 'Vigente', 'El lector lo confirmó y está en su franja.'),
    ('por-vencer', 'Por vencer', 'Entró en la ventana de aviso.'),
    ('usado', 'Usado', 'Código de un solo uso que ya sirvió.'),
    ('vencido', 'Vencido', 'Terminó solo, a su hora.'),
    ('revocado', 'Revocado', 'Alguien lo cortó; queda su nombre.'),
    ('rechazado', 'Rechazado', 'Evento en la entrada, con motivo.'),
    ('identidad', 'Dato personal', 'Cédula, rostro o teléfono a la vista.'),
]


def qr(semilla=7, n=25, clase='qr'):
    """QR de muestra (no codifica nada): patrón determinista con los tres buscadores."""
    s = semilla
    def r():
        nonlocal s
        s = (s * 16807) % 2147483647
        return s / 2147483647
    m = [[r() > .5 for _ in range(n)] for _ in range(n)]
    celdas = []
    def buscador(x, y):
        for i in range(7):
            for j in range(7):
                borde = i in (0, 6) or j in (0, 6)
                centro = 2 <= i <= 4 and 2 <= j <= 4
                m[y + i][x + j] = borde or centro
        for i in range(-1, 8):
            for j in range(-1, 8):
                if 0 <= y + i < n and 0 <= x + j < n and (i in (-1, 7) or j in (-1, 7)):
                    m[y + i][x + j] = False
    for x, y in ((0, 0), (n - 7, 0), (0, n - 7)):
        buscador(x, y)
    for y in range(n):
        for x in range(n):
            if m[y][x]:
                celdas.append(f'M{x} {y}h1v1h-1z')
    return (f'<svg class="{clase}" viewBox="-2 -2 {n + 4} {n + 4}" width="{n + 4}" height="{n + 4}" style="aspect-ratio:1" role="img" aria-label="Código QR de muestra">'
            f'<rect x="-2" y="-2" width="{n + 4}" height="{n + 4}" style="fill:var(--kino-fijo-blanco)"/><path style="fill:var(--kino-sustrato-100)" d="{"".join(celdas)}"/></svg>')
