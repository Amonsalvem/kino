#!/usr/bin/env python3
"""Construye Kino_Marca.html: el deck del sistema de marca v2 sobre el shell de la entrega 2.
Reutiliza de kino_entrega_2.html: el script de cabecera, el sprite, la barra, el fondo, la cortina,
el visor, el motor de movimiento y el controlador de láminas. El contenido es nuevo y los datos
(colores, contraste, Leonardo) se leen de gorr-brand-system/clientes/kino."""
import re, json, html, sys, math

E2 = '/tmp/ke.html'
UP = '/mnt/user-data/uploads/kino/gorr-brand-system/clientes/kino'
TOK = '/home/claude/gbs/clientes/kino'
src = open(E2).read()
scripts = re.findall(r'<script([^>]*)>([\s\S]*?)</script>', src)
s_head, s_motor, s_ctrl = scripts[0][1], scripts[1][1], scripts[2][1]
# 24 sep: la información llega mientras la lámina llega, no después.
RITMO = [
  # Se conservan intactas las duraciones, curvas, escalonados y el desenfoque de la entrega 2.
  # Solo cambia CUÁNDO empieza la entrada: al arrancar el paso de lámina, no al terminar.
  ("const entradas = new WeakSet();", "const entradas = new WeakSet();\n  window.__kinoEntrar = (s) => { if (!abierto) return; entrar(s); enfocarLamina(s); };"),
  ("if (s.offsetTop - 220 <= y) act = i;", "if (s.offsetTop - innerHeight * .5 <= y) act = i;"),
]
for a, z in RITMO:
    assert a in s_ctrl, a
    s_ctrl = s_ctrl.replace(a, z)
fonts = re.search(r'(<link rel="preconnect"[\s\S]*?display=swap"[^>]*>)', src).group(1)
sprite = open('sprite.svg').read()
P = json.load(open('paths.json'))
res = json.load(open(f'{UP}/build/tokens.resuelto.json'))
prim = res['primitivos']; osc = res['temas']['oscuro']; cla = res['temas']['claro']
tokcss = open(f'{UP}/build/kino-tokens.css').read()
contr = json.load(open(f'{UP}/reportes/contraste.json'))
leo = json.load(open(f'{UP}/reportes/leonardo-comparacion.json'))
voz = json.load(open(f'{TOK}/voz.json'))
cfg = json.load(open(f'{TOK}/marca.config.json'))
mov = json.load(open(f'{TOK}/tokens/40-movimiento.tokens.json'))['primitivo']['movimiento']
css = open('kino-tokens-extra.css').read() if False else ''
CSS = tokcss + '\n' + open('alias.css').read() + '\n' + open('componentes-e2.css').read() + '\n' + open('v2.css').read() + '\n' + open('paginar.css').read()
open('kino-sistema.css', 'w').write(CSS)

e = html.escape
MARK = P['mark']; LOGO = P['logo']
DROP = 'M 16.169 0 A 16.169 17.579 0 0 1 32.338 17.579 L 16.169 30.680 L 0 17.579 A 16.169 17.579 0 0 1 16.169 0 Z'
def svg_mark(extra=''):
    return f'<svg viewBox="0 0 100 101.824" fill="currentColor" fill-rule="evenodd" aria-hidden="true" {extra}><path d="{MARK}"/></svg>'
def svg_h(extra=''):
    return (f'<svg viewBox="0 0 267.960 101.824" fill="currentColor" fill-rule="evenodd" aria-hidden="true" {extra}><path d="{MARK}"/>'
            f'<g transform="translate(126.000 25.681) scale(1.4196)"><path d="{LOGO}"/></g></svg>')
def svg_v(extra=''):
    return (f'<svg viewBox="0 0 100 140.023" fill="currentColor" fill-rule="evenodd" aria-hidden="true" {extra}><path d="{MARK}"/>'
            f'<g transform="translate(0 105.970)"><path d="{LOGO}"/></g></svg>')
def svg_drop(extra=''):
    return f'<svg viewBox="0 0 32.338 30.68" fill="currentColor" aria-hidden="true" {extra}><path d="{DROP}"/></svg>'
def ic(i, cls='ic'):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{i}"/></svg>'
def lum(hexv):
    h = hexv.lstrip('#')[:6]; r, g, b = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)
def tinta(hexv): return '#00140C' if lum(hexv) > .22 else '#EFFCF7'

secciones = []  # (id, nav, cap, clase, html)
def S(id, nav, cap, cuerpo, clase=''):
    secciones.append((id, nav, cap, clase, cuerpo))

# ── 01 Portada ──────────────────────────────────────────────────────────────
S('portada', 'Portada', '', f'''
<div class="marca-portada">{svg_h('role="img" aria-label="Kino"').replace('aria-hidden="true" ','')}</div>
<p class="autores">Sistema de marca &nbsp;·&nbsp; v2 &nbsp;·&nbsp; 23 sep 2026</p>''')

# ── 02 El pilar ──────────────────────────────────────────────────────────────
S('pilar', 'El pilar', 'Punto de partida', f'''
<p class="ojo">De dónde sale este sistema</p>
<h2 class="ancho">Kino habla como una investigación: afirma solo lo que puede mostrar</h2>
<p class="lede">La base es la entrega 2, «Quién decide quién entra». Sus 29 láminas ya tenían un idioma propio: superficies de sustrato, luz de biolum, rótulos en mono, diagramas de flujo con evidencia debajo de cada caja. Este sistema lo nombra, lo mide y lo vuelve reutilizable.</p>
<div class="rej r4">
<div class="tj">{ic('matraz','ic ic-tj')}<p class="rol">Idioma</p><h3>Lenguaje de evidencia</h3><p class="peq">Cada afirmación lleva su grado —observado, prueba, entorno, inferido— y su fuente en mono.</p></div>
<div class="tj">{ic('lista','ic ic-tj')}<p class="rol">Gramática</p><h3>Flujos que se leen</h3><p class="peq">Nueve formas con significado fijo: inicio, paso, decisión, alterno, estado, metas, otorgar y pregunta abierta.</p></div>
<div class="tj acento">{ic('codigo','ic ic-tj')}<p class="rol">Objeto</p><h3>El pase</h3><p class="peq">Autor, motivo, vigencia y modo. Es la unidad del producto y de la marca.</p></div>
<div class="tj">{ic('reloj','ic ic-tj')}<p class="rol">Tiempo</p><h3>Movimiento con sentido</h3><p class="peq">Crecer es aparecer, decaer es caducar, latir es estar vivo. Nada se mueve para decorar.</p></div>
</div>
<div class="franja"><p class="glosa">Tres decisiones del 23 sep ordenan el resto: Kino es la marca y deja de ser marca blanca; el objeto se llama <b>pase</b>; el acento vuelve a <span class="mono">#00BB83</span>, el de la entrega 2.</p>
<p class="pie">Fuente: claude/decisiones-marca-2026-09-23.md · kino_entrega_2.html</p></div>''')

# ── 03 La tesis ──────────────────────────────────────────────────────────────
S('tesis', 'La tesis', 'Concepto', f'''
<p class="ojo">La membrana</p>
<h2>Un muro no sabe quién pasó. Una membrana sí.</h2>
<div class="rej r2" style="align-items:start;gap:40px">
<div>
<p class="destacado">¿Cómo reunir conocimiento y autoridad para decidir quién entra? Quien conoce al visitante no tiene la autoridad, y quien la tiene no lo conoce. La marca dibuja la respuesta: una membrana selectiva que deja pasar lo que reconoce, y donde lo que pasa deja rastro.</p>
<p class="pie">Pregunta guía del proyecto · diagnóstico consolidado v1</p>
</div>
<div class="rej" style="gap:12px">
<div class="tj"><p class="rol">Metabolismo</p><h3>Lo que entra se procesa y se elimina</h3><p class="peq">Hoy el invitado queda como miembro permanente. El pase caduca solo.</p><span class="evid" data-g="observado">Observado · H4</span></div>
<div class="tj"><p class="rol">Bioluminiscencia</p><h3>Solo brilla lo confirmado</h3><p class="peq">La interfaz decía «Permitido» sin que la puerta confirmara. Aquí la luz es un hecho.</p><span class="evid" data-g="prueba">Prueba · H2</span></div>
<div class="tj"><p class="rol">Membrana</p><h3>Permeable, con reconocimiento</h3><p class="peq">El residente ya decide quién entra. Falta reconocerlo, acotarlo y dejar constancia.</p><span class="evid" data-g="inferido">Inferido · núcleo</span></div>
</div></div>''')

# ── 04 Principios ────────────────────────────────────────────────────────────
reglas = cfg['reglas']
S('principios', 'Principios', 'Reglas', f"""
<p class="ojo">Lo que no se negocia</p>
<h2 class="ancho">Nueve reglas, y cada una se puede verificar mirando una pieza</h2>
<div class="rej r2" style="gap:14px 44px">
<ol class="pasos">{''.join(f'<li><span style="font-size:17px;line-height:1.42">{e(r)}</span></li>' for r in reglas[:5])}</ol>
<ol class="pasos" style="counter-reset:p 5">{''.join(f'<li><span style="font-size:17px;line-height:1.42">{e(r)}</span></li>' for r in reglas[5:])}</ol>
</div>
<p class="pie">Fuente: gorr-brand-system/clientes/kino/marca.config.json → reglas. La skill kino-marca las carga en cada pieza que produce Claude.</p>""")

# ── 05 La marca ──────────────────────────────────────────────────────────────
S('marca', 'La marca', 'Identidad', f'''
<p class="ojo">El logotipo</p>
<h2 class="ancho">Un portal apoyado en el suelo, con algo que lo atraviesa</h2>
<div class="rej r2" style="gap:30px;align-items:stretch;margin-bottom:18px">
<div class="guia-marca" style="--h:120px"><div class="zona"><span class="kmarca">{svg_mark()}</span></div>
<span class="cota" style="top:10px;left:14px">aire mínimo = ancho del arco · 0,63 × el bloque</span>
<span class="cota" style="bottom:10px;right:14px">120 px → 74 px por lado</span></div>
<div class="rej" style="gap:10px">
<div class="tj"><p class="rol">El bloque</p><p class="peq">Esquinas superiores redondeadas, inferiores rectas: un portal que toca el suelo, no una insignia que flota.</p></div>
<div class="tj"><p class="rol">El arco</p><p class="peq">El vano, siempre abierto. Su ancho es la unidad de aire: nada entra ahí, ni el borde de un contenedor.</p></div>
<div class="tj acento"><p class="rol">La gota</p><p class="peq">Lo que pasa. Célula y marcador de mapa a la vez: en la traza, cada ingreso se marca con ella.</p></div>
</div></div>
<div class="piezas">
<div class="pieza" style="--h:74px"><div class="lugar">{svg_mark()}</div><h3>Marca</h3><p>Desde 20 px. Barras, avatares, sellos.</p></div>
<div class="pieza" style="--h:52px"><div class="lugar">{svg_h()}</div><h3>Bloqueo horizontal</h3><p>De 28 a 48 px de alto. Encabezados y pies.</p></div>
<div class="pieza" style="--h:96px"><div class="lugar">{svg_v()}</div><h3>Bloqueo vertical</h3><p>Desde 40 px. Portadas y aperturas.</p></div>
<div class="pieza" style="--h:44px"><div class="lugar" style="color:var(--ac-fuerte)">{svg_drop()}</div><h3>Gota</h3><p>Favicon, marcador de traza, marca de agua.</p></div>
</div>''')

# ── 06 Usos ──────────────────────────────────────────────────────────────────
S('usos', 'Usos del logo', 'Identidad', f'''
<p class="ojo">Usos</p>
<h2>Correcto e incorrecto</h2>
<div class="rej r4">
<div class="uso si"><div class="lugar">{svg_h()}</div><p>En <span class="mono">texto-primario</span> sobre la base. Es el uso por defecto.</p></div>
<div class="uso si"><div class="lugar" style="background:var(--ac);color:var(--kino-texto-sobre-acento)">{svg_h()}</div><p>Sobre el acento, en <span class="mono">texto-sobre-acento</span>.</p></div>
<div class="uso si"><div class="lugar" style="background:var(--inversa);color:var(--tx-inv)">{svg_h()}</div><p>Sobre la inversa, en <span class="mono">texto-inverso</span>.</p></div>
<div class="uso si"><div class="lugar" style="color:var(--ac)">{svg_mark()}</div><p>La marca sola en acento, sobre la base.</p></div>
<div class="uso no"><div class="lugar" style="background:var(--inversa);color:var(--ac)">{svg_h()}</div><p>Acento sobre la inversa: queda por debajo de 3:1.</p></div>
<div class="uso no"><div class="lugar">{svg_h('style="transform:rotate(-9deg)"')}</div><p>Rotar, inclinar o deformar.</p></div>
<div class="uso no"><div class="lugar">{svg_h('style="filter:drop-shadow(6px 8px 0 #000)"')}</div><p>Sombra proyectada o degradado.</p></div>
<div class="uso no"><div class="lugar" style="gap:12px;display:flex;justify-content:center;align-items:center"><span style="font-family:var(--mono);font-size:12px;border:1px solid var(--bd-def);padding:14px 10px;border-radius:4px">LOGO&nbsp;PH</span>{svg_mark('style="height:44px"')}</div><p>Logo del conjunto junto a la marca. El conjunto es un dato.</p></div>
</div>''')

# ── 07 Paleta ────────────────────────────────────────────────────────────────
fam_orden = ['sustrato', 'hueso', 'biolum', 'ambar', 'carmin', 'violeta', 'indigo']
signif = {**{k: v for k, v in cfg['color']['neutros'].items()}, **cfg['color']['familias']}
pasos_d = ['d15', 'd23', 'd32', 'd45', 'd70', 'd90', 'd110']
filas = []
for f in fam_orden:
    ks = ([str(i) for i in range(100, 900, 100)] if f in ('sustrato', 'hueso') else []) + pasos_d
    MARCA_AC = ' class="marca-ac"'
    tira = ''.join('<i style="background:%s;--c:%s" data-k="%s"%s title="%s-%s %s"></i>' % (prim["kino-"+f+"-"+k], tinta(prim["kino-"+f+"-"+k]), k, MARCA_AC if (f=="biolum" and k=="d70") else "", f, k, prim["kino-"+f+"-"+k]) for k in ks)
    s = signif[f]
    filas.append(f'<div class="familia"><div class="nom">{f}<small>{e(s["significa"])}</small></div><div class="tira">{tira}</div></div>')
S('paleta', 'Paleta', 'Color', f'''
<p class="ojo">Siete familias</p>
<h2 class="ancho">Cada paso es una promesa de contraste: d45 da 4,5:1 sobre el fondo</h2>
<div class="tj" style="padding:8px 20px">{''.join(filas)}</div>
<div class="franja"><p class="glosa">El recuadro marca el acento, <span class="mono">biolum-d70 #00BB83</span>. Los neutros van de 100 a 800 por luminosidad; las familias de color, de d15 a d110 por contraste sobre <span class="mono">sustrato-200</span>. La paleta de registro es la que se presentó: el generador solo completa pasos nuevos, como d90.</p>
<p class="pie">Fuente: tokens/10-primitivo-color.tokens.json · legado/paleta-2026-09-19.json</p></div>''', 'ancha')

# ── 08 Semántica ─────────────────────────────────────────────────────────────
grupos = [('Superficies', ['superficie-abismo', 'superficie-base', 'superficie-elevada', 'superficie-membrana', 'superficie-inversa']),
          ('Texto', ['texto-primario', 'texto-secundario', 'texto-tenue', 'texto-inverso', 'texto-sobre-acento']),
          ('Bordes y acento', ['borde-tenue', 'borde-definido', 'borde-foco', 'acento-base', 'acento-fuerte', 'acento-sordo'])]
def sw(n, tema):
    v = (osc if tema == 'oscuro' else cla)['kino-' + n]
    return f'<div class="s"><i style="background:{v}"></i><div><b>{n}</b><span>{v}</span></div></div>'
bloques = ''.join(f'<h3 style="margin:14px 0 8px">{g}</h3><div class="sem">{"".join(sw(n,"oscuro") for n in ns)}</div>' for g, ns in grupos)
S('semantica', 'Semántica', 'Color', f'''
<p class="ojo">Capa semántica · tema oscuro, canónico</p>
<h2 class="ancho">Los componentes usan roles, nunca un hex</h2>
{bloques}
<div class="franja"><p class="glosa">Cada rol es un alias a un primitivo. El tema claro, «Laboratorio», reasigna los mismos roles; el botón <span class="mono">tema</span> de la barra lo muestra en vivo. Un literal en esta capa hace fallar la verificación.</p>
<p class="pie">Fuente: tokens/tema/oscuro.tokens.json · validado contra el esquema oficial DTCG</p></div>''', 'ancha')

# ── 09 Estados ───────────────────────────────────────────────────────────────
est = [('vigente', 'Vigente', 'El lector de la puerta confirmó el pase. El único punto que late, tres ciclos.'),
       ('por-vencer', 'Vence en 40 min', 'Dentro de la ventana de aviso que fijó la administración. Dice cuánto queda.'),
       ('vencido', 'Vencido', 'Caducó solo. Sin color propio: un final no es un error.'),
       ('negado', 'Negado', 'Fuera de ventana o de límites, con motivo legible y autor.'),
       ('sin-confirmar', 'Sin confirmar', 'Solicitado y aún sin respuesta de la puerta. Sin relleno, borde punteado.'),
       ('identidad', 'Dato personal', 'Cédula, rostro o teléfono a la vista. La zona que regula la SIC.')]
S('estados', 'Estados', 'Color', f'''
<p class="ojo">El color nombra hechos</p>
<h2 class="ancho">Seis estados, iguales en todo Kino</h2>
<div class="rej r3" style="gap:12px 22px;margin-bottom:22px">{''.join(f'<div class="par-est"><span class="est" data-e="{k}">{t}</span><span class="peq">{d}</span></div>' for k,t,d in est)}</div>
<div class="rej r2">
<div class="destacado">Si el lector no confirmó, el estado es «sin confirmar», aunque la base de datos diga «Permitido». Ese es el hallazgo H2 convertido en regla visual.</div>
<div class="tj"><p class="rol">Reglas</p><ul class="lim"><li>Todo estado lleva palabra además de color.</li><li>El acento no es un estado: es la acción de otorgar.</li><li>No hay estados intermedios del tipo «pendiente de aprobación»: el sistema no tiene cola de aprobación.</li><li>Ningún par se distingue solo por matiz.</li></ul></div>
</div>''')

# ── 10 Contraste ─────────────────────────────────────────────────────────────
sel = ['texto primario sobre superficie base', 'texto secundario sobre superficie base', 'texto sobre acento', 'texto del estado vencido', 'borde definido sobre superficie base']
filas_c = []
for q in sel:
    for x in contr:
        if x['tema'] == 'oscuro' and x['que'] == q:
            fm = x.get('fuenteMinima')
            nota = f'700 → {fm["700"]:g} px · 600 → {fm["600"]:g} px' if fm else '—'
            filas_c.append(f'<tr><td>{e(q)}</td><td class="c">{x["wcag"]:.2f}:1</td><td class="c">{x["apcaLc"]:g}</td><td class="c">{x["min"]:g}:1</td><td class="c">{nota}</td></tr>')
todos = [v for f in leo.values() for v in f.values()]
media = sum(v['deltaEOK'] for v in todos) / len(todos)
S('contraste', 'Contraste', 'Color', f'''
<p class="ojo">Medido, no estimado</p>
<h2 class="ancho">38 pares, 0 fallos. Y una regla de tamaño para el botón</h2>
<table><thead><tr><th>Par (tema oscuro)</th><th>WCAG 2.2</th><th>APCA Lc</th><th>Mínimo</th><th>Letra mínima (APCA)</th></tr></thead>
<tbody>{''.join(filas_c)}</tbody></table>
<div class="rej r3" style="margin-top:22px">
<div class="tj acento"><span class="cifra">18 px · 700</span><p class="peq">El texto sobre el acento de la entrega 2 llega a Lc 55. Se resuelve con tamaño y peso mínimos (fontLookupAPCA), no subiendo el acento.</p></div>
<div class="tj"><span class="cifra">{len(todos)}</span><p class="peq">pasos comparados con Adobe Leonardo real. ΔE OK medio {media:.3f}: imperceptible. La mayor diferencia está en los pasos casi iguales al fondo.</p></div>
<div class="tj"><span class="cifra">7 / 7</span><p class="peq">archivos de tokens validados contra el esquema oficial DTCG 2025.10 (skill de tokens de dgtlntv).</p></div>
</div>
<p class="pie">Fuente: reportes/contraste.json · reportes/leonardo-comparacion.json · apca-w3 0.1.9 · @adobe/leonardo-contrast-colors 1.1.0</p>''')

# ── 11 Tipografía ────────────────────────────────────────────────────────────
S('tipografia', 'Tipografía', 'Tipo', f'''
<p class="ojo">Dos familias, dos trabajos</p>
<h2 class="ancho">Archivo dice. JetBrains Mono registra.</h2>
<div class="rej r2" style="gap:30px;align-items:start">
<div class="tj"><p class="rol">Archivo · ancho variable 62–125 %</p>
<div class="ancho-var"><span style="font-stretch:100%">Pase<small>100 %</small></span><span style="font-stretch:112%">Pase<small>112 % · titulares</small></span><span style="font-stretch:125%">Pase<small>125 %</small></span></div>
<p class="peq" style="margin-top:14px">Titulares en 800 al 112 %: anchos y firmes, como una afirmación. Texto corrido en 400.</p></div>
<div class="tj"><p class="rol">JetBrains Mono · cero barrado</p>
<div class="cero">HTK 480 · O0</div>
<p class="peq" style="margin-top:14px">Todo lo que el lector de la puerta también lee: placas, códigos, horas, cifras. También los rótulos del sistema. Una placa mal leída es un ingreso mal concedido.</p></div>
</div>
<div style="margin-top:18px">
<div class="espec"><div class="rot"><b>h1 · portada</b>800 · 112 % · 48–72 px</div><div style="font-weight:800;font-stretch:112%;font-size:clamp(2.2rem,1.8rem + 1.6vw,3.2rem);letter-spacing:-.02em;line-height:1">Quién decide quién entra</div></div>
<div class="espec"><div class="rot"><b>h2 · lámina</b>800 · 112 % · 33–45 px</div><div style="font-weight:800;font-stretch:112%;font-size:clamp(1.7rem,1.5rem + .9vw,2.4rem);letter-spacing:-.02em;line-height:1.1">El objeto que falta: el pase</div></div>
<div class="espec"><div class="rot"><b>lede</b>400 · 19–23 px</div><div class="lede" style="margin:0">Un pase con cuatro atributos obligatorios y una prohibición.</div></div>
<div class="espec"><div class="rot"><b>ojo · cap · pie</b>mono 500 · 13 px · +8 %</div><div><span class="ojo" style="margin:0 18px 0 0">Los flujos</span><span class="pie" style="margin:0">Fuente: inspección, 14–16 sep</span></div></div>
<div class="espec"><div class="rot"><b>cifra</b>mono 700 · 33–45 px</div><div class="mono" style="font-weight:700;font-size:clamp(2rem,1.8rem + 1vw,2.8rem);color:var(--ac-fuerte);letter-spacing:.02em">0 / 312</div></div>
</div>''')

# ── 12 Escala, espacio y retícula ────────────────────────────────────────────
tipo = json.load(open('/home/claude/gbs/clientes/kino/reportes/tipo.json'))
CEL = '<i style="height:16px;border-radius:3px;background:var(--ac-sordo);border:1px solid var(--ac);display:block"></i>'
REJILLAS = ''.join('<div style="display:grid;grid-template-columns:repeat(%d,1fr);gap:5px">%s</div>' % (n, CEL * n) for n in (2, 3, 4, 5))
S('escala', 'Escala y retícula', 'Tipo', f'''
<p class="ojo">Escala fluida (Utopia) y retícula</p>
<h2 class="ancho">Crece con la pantalla, sin saltos</h2>
<div class="rej r2" style="gap:30px;align-items:start">
<table><thead><tr><th>Paso</th><th>360 px</th><th>1440 px</th><th>clamp()</th></tr></thead><tbody>
{''.join(f'<tr><td class="k">{r["paso"]}</td><td class="c">{r["minPx"]:g}</td><td class="c">{r["maxPx"]:g}</td><td class="mono" style="font-size:12px">{r["clamp"]}</td></tr>' for r in tipo)}
</tbody></table>
<div class="rej" style="gap:12px">
<div class="tj"><p class="rol">Rejillas</p><div style="display:grid;gap:6px">
{REJILLAS}
</div><p class="peq" style="margin-top:10px"><span class="mono">.rej .r2–.r5</span>, canal de 14 px. Bajo 1100 px pasan a dos columnas; bajo 680 px, a una.</p></div>
<div class="tj"><p class="rol">Láminas</p><p class="peq"><span class="mono">section</span> hasta 1360 px · <span class="mono">.ancha</span> hasta 1680 px · <span class="mono">.plena</span> sin límite, para lienzos de flujo. Radio 6 px. Texto corrido hasta 62 caracteres.</p></div>
</div></div>''', 'ancha')

# ── 13 Iconos ────────────────────────────────────────────────────────────────
ICONOS_PLANTILLA = '<div class="tj" style="padding:14px;display:flex;flex-direction:column;align-items:center;gap:8px"><svg class="ic" style="width:30px;height:30px;color:var(--tx2)" aria-hidden="true"><use href="#i-%s"/></svg><span class="mono" style="font-size:11px;color:var(--tx3)">%s</span></div>'
iconos = ['casa','persona','personas','visitante','herramienta','edificio','telefono','carro','qr','codigo','talanquera','camara','servidor','reloj','chat','documento','lista','lupa','ojo','check','cruz','alta','sinfecha','sinpersona','vacio','matraz']
ICONOS = ''.join(ICONOS_PLANTILLA % (i, i) for i in iconos)
S('iconos', 'Iconos', 'Iconografía', f'''
<p class="ojo">Trazo de 1,7 · retícula 24</p>
<h2 class="ancho">Iconos que nombran actores, modos y hechos</h2>
<div class="rej" style="grid-template-columns:repeat(auto-fill,minmax(112px,1fr));gap:10px">
{ICONOS}
</div>
<div class="franja"><p class="glosa">El sprite propio cubre el recorrido; para lo demás, Iconoir (MIT, 1.383 iconos instalados) con el mismo trazo. El icono nunca reemplaza la palabra en un estado. <span class="mono">candado</span> y <span class="mono">escudo</span> existen solo para describir el sistema anterior: Kino no se ilustra con ellos.</p>
<p class="pie">Fuente: sprite de la entrega 2 · iconoir 7.12.1</p></div>''', 'ancha')

# ── 14 Anatomía de lámina ────────────────────────────────────────────────────
S('lamina', 'La lámina', 'Componentes', f'''
<p class="ojo">Anatomía</p>
<h2 class="ancho">Cada lámina se arma con las mismas piezas</h2>
<div class="anatomia">
<span class="marca-a" style="top:-11px;left:24px">cap · sección</span><span class="marca-a" style="top:-11px;right:24px">num · 04 / 29</span>
<div class="fila-a"><span class="cap" style="position:static">Los flujos</span><span class="num" style="position:static">04 / 29</span></div>
<p class="ojo">Ojo · qué es esto</p>
<h2 style="max-width:none">Titular: una afirmación, no un tema</h2>
<p class="lede">Lede: el contexto en una o dos frases. Nunca repite el titular.</p>
<div class="rej r3"><div class="tj"><h3>Tarjeta</h3><p class="peq">Membrana con relieve. Foco de luz e inclinación al pasar el puntero.</p></div><div class="tj acento"><h3>Tarjeta acento</h3><p class="peq">Solo para lo que otorga o lo que se propone.</p></div><div class="tj"><span class="cifra">0 / 312</span><p class="peq">Cifra con su denominador.</p></div></div>
<div class="franja"><p class="glosa">Glosa: la lectura de la lámina en una frase.</p><p class="pie">Pie · fuente de la afirmación</p></div>
</div>''')

# ── 15 Componentes ───────────────────────────────────────────────────────────
S('componentes', 'Componentes', 'Componentes', f'''
<p class="ojo">Piezas de información</p>
<h2 class="ancho">Cifras, medidores, chips y avisos</h2>
<div class="rej r4" style="margin-bottom:14px">
<div class="tj"><span class="cifra">312</span><p class="peq">personas registradas</p><div class="medidor"><i data-barra style="--v:0"></i></div><p class="medidor-pie">0 sincronizadas con la puerta</p></div>
<div class="tj"><span class="cifra">888</span><p class="peq">personas registradas</p><div class="medidor fuerte"><i data-barra style="--v:1"></i></div><p class="medidor-pie">comunidad vecina</p></div>
<div class="tj"><div class="anillos"><div class="anillo"><svg viewBox="0 0 36 36"><circle class="pista" cx="18" cy="18" r="15.9"/><circle class="arco" data-arco="47.9" cx="18" cy="18" r="15.9" pathLength="100" stroke-dasharray="47.9 100"/></svg><div><b>47,9 %</b><span>Colombia</span></div></div></div><p class="peq" style="margin-top:8px">Anillo: proporción de un todo.</p></div>
<div class="tj"><div class="puntos"><i class="si"></i><i class="si"></i><i class="si"></i><i class="si"></i><i class="si"></i><i></i><i></i><i></i><i></i><i></i></div><p class="puntos-pie">5 de 10 posibilidades</p><p class="peq" style="margin-top:8px">Puntos: avance contable.</p></div>
</div>
<div class="rej r3">
<div class="tj"><p class="rol">Chips</p><div style="display:flex;gap:8px;flex-wrap:wrap"><span class="chip-q">{ic('persona')}El cliente</span><span class="chip-q">{ic('edificio')}La administración</span><span class="chip-app">Permitido</span><span class="alerta-l">{ic('cruz')}Abre la puerta hoy</span></div></div>
<div class="aviso"><strong>Aviso.</strong> Una restricción o un riesgo que ordena lo demás. Ámbar, nunca rojo: rojo es negado.</div>
<div class="destacado">Destacado: la conclusión que sostiene la lámina.</div>
</div>
<div class="rej r2" style="margin-top:14px">
<div class="tj"><p class="rol">Pasos</p><ol class="pasos"><li><b>Mandar las preguntas</b><p class="peq" style="margin:0">Cuatro correos desbloquean cinco posibilidades.</p></li><li><b>Llevar a wireframe lo que no espera a nadie</b></li></ol></div>
<div class="tj"><p class="rol">Cadena</p><div class="cadena" style="margin-top:6px"><div class="eslabon">{ic('telefono')}<b>App</b></div><span class="conector"></span><div class="eslabon acento">{ic('lista')}<b>Kino</b></div><span class="conector"></span><div class="eslabon">{ic('servidor')}<b>HikCentral</b></div><span class="conector"></span><div class="eslabon">{ic('talanquera')}<b>Puerta</b></div></div></div>
</div>''', 'ancha')

# ── 16 Tablas y matriz ───────────────────────────────────────────────────────
S('tablas', 'Tablas y matriz', 'Componentes', f'''
<p class="ojo">Leerlas en vertical</p>
<h2 class="ancho">La matriz de capacidades dice quién puede qué</h2>
<table class="cap5"><thead><tr><th>Capacidad</th><th>Residente</th><th>Portero</th><th>Admin</th><th>Super admin</th></tr></thead><tbody>
<tr class="nadie"><td>Anunciar un visitante para una fecha</td><td class="c">{ic('cruz','ic')}Nadie</td><td class="c">{ic('cruz','ic')}Nadie</td><td class="c">{ic('cruz','ic')}Nadie</td><td class="c">{ic('cruz','ic')}Nadie</td></tr>
<tr><td>Dar de alta una persona</td><td class="c no">No</td><td class="c no">No</td><td class="c si">{ic('check','ic')}Sí</td><td class="c si">{ic('check','ic')}Sí</td></tr>
<tr><td>Ver la vigencia del pase</td><td class="c no">No</td><td class="c si">{ic('check','ic')}Sí</td><td class="c si">{ic('check','ic')}Sí</td><td class="c si">{ic('check','ic')}Sí</td></tr>
</tbody></table>
<div class="rej r2" style="margin-top:20px">
<div class="tj"><p class="rol">Reglas de tabla</p><ul class="lim"><li>Encabezados en mono, mayúsculas, tenues.</li><li>Cifras en mono, tabulares, alineadas; nunca centradas en columnas numéricas.</li><li>Una fila que nadie puede cumplir se tiñe de negado: es el hallazgo, no una fila más.</li><li>En teléfono, cada fila se vuelve tarjeta con el nombre de la columna en cada celda.</li></ul></div>
<div class="tj"><p class="rol">Por qué importa</p><p class="peq">La matriz de la entrega 2 mostró que tres capacidades no las tiene nadie. Esa lectura en vertical es el tipo de hallazgo que la marca tiene que hacer visible sin explicación.</p><span class="evid" data-g="observado">Observado · 4 paneles</span></div>
</div>''')

# ── 17 El pase ───────────────────────────────────────────────────────────────
def boleto(estado, texto, v=1, anim=False):
    extra = ' data-estado-boleto' if anim else ''
    return f'''<div class="boleto" role="img" aria-label="Pase en estado {texto}"><div class="cab"><b>PASE</b><span class="est" data-e="{estado}"{extra}>{texto}</span></div>
<dl><dt>Autor</dt><dd>Ana Ruiz · casa 14</dd><dt>Motivo</dt><dd>Trabajo doméstico</dd>
<dt>Vigencia</dt><dd><div class="ventana"><i data-barra style="left:{'18%' if v else '0'};right:{'30%' if v else '100%'}"></i></div><div class="ventana-pie"><span>lun 07:00</span><span>vie 17:00 · caduca solo</span></div></dd>
<dt>Modo</dt><dd><div class="modos"><span>{ic('carro')}placa</span><span>{ic('qr')}QR</span><span>{ic('codigo')}código</span></div></dd></dl>
<div class="pie-b">{ic('sinpersona')}No crea una persona en la puerta</div></div>'''
S('pase', 'El pase', 'Objeto', f'''
<p class="ojo">La unidad del sistema</p>
<h2 class="ancho">El pase: cuatro atributos y una prohibición</h2>
<div class="rej r2 pase-cab">
<div><p class="lede">Es lo que recibe un invitado o colaborador. No es una cuenta: caduca solo y no deja a nadie matriculado. En la marca es la pieza más reconocible, porque es la que el producto no tenía.</p>
<div class="rej r2" style="gap:10px"><div class="tj acento"><h3>Autor</h3><p class="peq">Quién lo otorgó.</p></div><div class="tj acento"><h3>Motivo</h3><p class="peq">Por qué entra.</p></div><div class="tj acento"><h3>Vigencia</h3><p class="peq">Desde y hasta. Caduca solo.</p></div><div class="tj acento"><h3>Modo</h3><p class="peq">Placa, QR o código.</p></div></div></div>
{boleto('sin-confirmar', 'Sin confirmar', anim=True)}
</div>
<div class="franja"><p class="glosa">La forma del boleto —muescas laterales, línea punteada bajo la cabecera, borde de acento— es exclusiva del pase. Nace «sin confirmar» y pasa a «vigente» cuando la puerta responde: la ilustración lo hace una vez, al entrar.</p>
<p class="pie">Fuente: kino_entrega_2, lámina 19 · decisiones-marca-2026-09-23</p></div>''')

# ── 18 Gramática de flujo ────────────────────────────────────────────────────
nod = [('Inicio y fin', '<rect x="2" y="8" width="116" height="36" rx="18" fill="var(--membrana)" stroke="var(--bd-def)" stroke-width="1.6"/>', 'El segundo 0 y el punto donde termina.', 'rx = alto/2 · membrana'),
       ('Paso o pantalla', '<rect x="2" y="8" width="116" height="36" rx="4" fill="var(--elevada)" stroke="var(--bd-def)" stroke-width="1.6"/>', 'Una pantalla real o un acto del mundo.', 'rx 4 · elevada'),
       ('Decisión', '<polygon points="60,4 118,26 60,48 2,26" fill="var(--pv-bg)" stroke="var(--pv-bd)" stroke-width="1.8"/>', 'Bifurcación. Debajo va la evidencia que dice por dónde sale.', 'rombo · ámbar'),
       ('Camino alterno', '<path d="M4 26 H104" stroke="var(--bd-def)" stroke-width="2" stroke-dasharray="6 5" fill="none"/><path d="M102 20 L116 26 L102 32 z" fill="var(--bd-def)"/>', 'La rama punteada. Hoy suele ser por donde pasa el volumen.', 'trazo 6 · 5'),
       ('Estado del sistema', '<rect x="2" y="8" width="116" height="36" rx="4" fill="none" stroke="var(--bd-def)" stroke-width="1.6" stroke-dasharray="6 4"/>', 'Lo que el producto afirma o deja de afirmar.', 'punteado 6 · 4'),
       ('Meta lograda', '<rect x="2" y="8" width="116" height="36" rx="18" fill="var(--v-bg)" stroke="var(--v-bd)" stroke-width="2"/>', 'Llega a donde tenía que llegar.', 'vigente'),
       ('Meta no lograda', '<rect x="2" y="8" width="116" height="36" rx="18" fill="var(--ng-bg)" stroke="var(--ng-bd)" stroke-width="2"/>', 'Termina fuera del sistema o con un costo indebido.', 'negado'),
       ('Otorgar', '<rect x="2" y="8" width="116" height="36" rx="4" fill="var(--ac-sordo)" stroke="var(--ac)" stroke-width="2"/>', 'El acto que crea el pase. Lo único con acento.', 'acento'),
       ('Pregunta abierta', '<rect x="2" y="8" width="116" height="36" rx="4" fill="none" stroke="var(--id-bd)" stroke-width="1.6" stroke-dasharray="7 5"/><text x="60" y="31" text-anchor="middle" font-family="var(--mono)" font-size="14" fill="var(--id-tx)">?</text>', 'Depende de una respuesta que aún no tenemos.', 'violeta punteado')]
ej = f'''<div class="lienzo" data-zoom><svg viewBox="0 0 1200 250" role="img" aria-label="Ejemplo: el residente otorga un pase y la puerta lo confirma">
<rect x="20" y="95" width="150" height="60" rx="30" fill="var(--membrana)" stroke="var(--bd-def)" stroke-width="1.6"/><text x="95" y="122" text-anchor="middle" font-family="var(--mono)" font-size="11" fill="var(--tx3)">ENTRADA</text><text x="95" y="140" text-anchor="middle" font-family="var(--sans)" font-weight="700" font-size="14" fill="var(--tx)">Sabe a quién espera</text>
<path d="M170 125 H225" stroke="var(--bd-def)" stroke-width="2" data-traza/><path d="M221 119 L231 125 L221 131z" fill="var(--bd-def)"/>
<rect x="232" y="95" width="170" height="60" rx="4" fill="var(--ac-sordo)" stroke="var(--ac)" stroke-width="2"/><text x="317" y="122" text-anchor="middle" font-family="var(--sans)" font-weight="700" font-size="15" fill="var(--ac-fuerte)">Otorga un pase</text><text x="317" y="141" text-anchor="middle" font-family="var(--mono)" font-size="11" fill="var(--tx3)">autor · motivo · vigencia</text>
<text x="317" y="178" text-anchor="middle" font-family="var(--mono)" font-size="10.5" fill="var(--tx3)">Posibilidad · P1 acceso previsto</text>
<path d="M402 125 H455" stroke="var(--bd-def)" stroke-width="2" data-traza/><path d="M451 119 L461 125 L451 131z" fill="var(--bd-def)"/>
<polygon points="555,70 650,125 555,180 460,125" fill="var(--pv-bg)" stroke="var(--pv-bd)" stroke-width="1.8"/><text x="555" y="121" text-anchor="middle" font-family="var(--sans)" font-weight="700" font-size="14" fill="var(--pv-tx)">¿Cabe en los</text><text x="555" y="139" text-anchor="middle" font-family="var(--sans)" font-weight="700" font-size="14" fill="var(--pv-tx)">límites?</text>
<path d="M650 125 H705" stroke="var(--bd-def)" stroke-width="2" data-traza/><path d="M701 119 L711 125 L701 131z" fill="var(--bd-def)"/><text x="678" y="116" text-anchor="middle" font-family="var(--mono)" font-size="10" fill="var(--tx3)">sí</text>
<rect x="712" y="95" width="180" height="60" rx="4" fill="none" stroke="var(--bd-def)" stroke-width="1.6" stroke-dasharray="6 4"/><text x="802" y="122" text-anchor="middle" font-family="var(--sans)" font-weight="700" font-size="14" fill="var(--tx2)">Sin confirmar</text><text x="802" y="140" text-anchor="middle" font-family="var(--mono)" font-size="11" fill="var(--tx3)">hasta que el lector responde</text>
<path d="M892 125 H945" stroke="var(--bd-def)" stroke-width="2" data-traza/><path d="M941 119 L951 125 L941 131z" fill="var(--bd-def)"/>
<rect x="952" y="95" width="220" height="60" rx="30" fill="var(--v-bg)" stroke="var(--v-bd)" stroke-width="2"/><text x="1062" y="122" text-anchor="middle" font-family="var(--mono)" font-size="11" fill="var(--v-tx)">SALIDA</text><text x="1062" y="140" text-anchor="middle" font-family="var(--sans)" font-weight="700" font-size="14" fill="var(--v-tx)">Entra dentro de su ventana</text>
<path d="M555 180 V215 H820" stroke="var(--bd-def)" stroke-width="2" stroke-dasharray="6 5" fill="none" data-traza/><text x="566" y="206" font-family="var(--mono)" font-size="10" fill="var(--tx3)">no · reformular</text>
<rect x="822" y="195" width="200" height="40" rx="4" fill="none" stroke="var(--id-bd)" stroke-width="1.6" stroke-dasharray="7 5"/><text x="922" y="220" text-anchor="middle" font-family="var(--sans)" font-weight="700" font-size="13" fill="var(--id-tx)">¿Qué unidad tiene el cupo?</text>
</svg><span class="lupa">clic para ampliar</span></div>'''
S('flujo', 'Gramática de flujo', 'Diagramas', f'''
<p class="ojo">Cómo se dibuja un recorrido</p>
<h2 class="ancho">Nueve formas, cada una con un significado fijo</h2>
<div class="nodos" style="margin-bottom:16px">{''.join(f'<div class="nodo-m"><svg viewBox="0 0 120 52" aria-hidden="true">{s}</svg><div><h3>{t}</h3><p>{d}</p><span class="spec">{sp}</span></div></div>' for t,s,d,sp in nod)}</div>
{ej}
<p class="pie">Debajo de cada caja, en mono, va de dónde sale lo que afirma. La pregunta abierta del ejemplo es real: la unidad de los cupos aún no está decidida.</p>''', 'ancha')

# ── 19 Evidencia ─────────────────────────────────────────────────────────────
S('evidencia', 'Evidencia', 'Idioma', f'''
<p class="ojo">El grado de cada afirmación</p>
<h2 class="ancho">Toda afirmación dice qué tan segura es y de dónde sale</h2>
<div class="rej r5" style="margin-bottom:18px">
<div class="tj"><span class="evid" data-g="observado">Observado</span><p class="peq" style="margin-top:10px">Lo vimos en la pantalla o en el sistema.</p></div>
<div class="tj"><span class="evid" data-g="prueba">Prueba</span><p class="peq" style="margin-top:10px">Lo provocamos y registramos el resultado.</p></div>
<div class="tj"><span class="evid" data-g="entorno">Entorno</span><p class="peq" style="margin-top:10px">Viene de una fuente externa citada.</p></div>
<div class="tj"><span class="evid" data-g="inferido">Inferido</span><p class="peq" style="margin-top:10px">Conclusión nuestra a partir de lo anterior.</p></div>
<div class="tj"><span class="evid" data-g="abierto">Abierto</span><p class="peq" style="margin-top:10px">Depende de una respuesta que no tenemos.</p></div>
</div>
<div class="rej r2">
<div class="tj"><h3>Una placa inventada quedó «Permitido» al instante</h3><p class="peq">Se sincronizó con el sistema físico de acceso: esa placa abre la puerta.</p><span class="evid" data-g="prueba">Prueba ejecutada</span><span class="fuente">inspección, sujeto 2 · 15 sep 2026</span></div>
<div class="tj"><h3>El 51,3 % de los contratos domésticos es por días</h3><p class="peq">El vínculo es intermitente; el sistema solo sabe representar permanencia.</p><span class="evid" data-g="entorno">Entorno</span><span class="fuente">DANE-GEIH vía Infobae · 9 sep 2026</span></div>
</div>
<p class="pie">El grado se escribe siempre: en láminas, documentos, tarjetas de hallazgo y en la voz del producto cuando describe lo que sabe y lo que no.</p>''', 'ancha')

# ── 20 Movimiento: principios ────────────────────────────────────────────────
dur = mov['duracion']; cur = mov['curva']
filas_m = ''.join(f'<tr><td class="k">{k}</td><td class="c">{v["$value"]["value"]} ms</td><td>{e(v.get("$description",""))}</td></tr>' for k, v in dur.items() if k != '$type')
S('movimiento', 'Movimiento', 'Motion', f'''
<p class="ojo">Sistema de movimiento</p>
<h2 class="ancho">Lo que se mueve significa algo</h2>
<div class="rej r2" style="gap:30px;align-items:start">
<div class="rej" style="gap:12px">
<div class="tj"><p class="rol">Crecer</p><h3>Aparecer</h3><p class="peq">Un pase nuevo, una tarjeta que entra. Sale rápido y se asienta.</p></div>
<div class="tj"><p class="rol">Decaer</p><h3>Caducar</h3><p class="peq">Lo que se apaga solo, sin que nadie lo decida. Lento al principio y después cae.</p></div>
<div class="tj"><p class="rol">Revocar</p><h3>Cortar</h3><p class="peq">Alguien cortó el pase. Seco y corto, para que no se confunda con caducar.</p></div>
<div class="tj acento"><p class="rol">Latir</p><h3>Estar vivo</h3><p class="peq">Solo el punto del estado vigente, tres ciclos y se queda quieto.</p></div>
</div>
<table><thead><tr><th>Duración</th><th>ms</th><th>Para qué</th></tr></thead><tbody>{filas_m}</tbody></table>
</div>
<p class="pie">Fuente: tokens/40-movimiento.tokens.json (DTCG) · motor: Motion Playground (un solo requestAnimationFrame)</p>''', 'ancha')

# ── 21 Curvas ────────────────────────────────────────────────────────────────
def curva_svg(p):
    x1, y1, x2, y2 = p; W, H = 120, 100
    X = lambda t: 10 + t * W; Y = lambda t: 110 - t * H
    return (f'<svg viewBox="0 0 140 120" aria-hidden="true"><path class="rej-c" d="M10 60 H130 M70 10 V110"/><path class="eje" d="M10 10 V110 H130"/>'
            f'<path class="mango" d="M{X(0)} {Y(0)} L{X(x1)} {Y(y1)} M{X(1)} {Y(1)} L{X(x2)} {Y(y2)}"/><circle class="pm" cx="{X(x1)}" cy="{Y(y1)}" r="3"/><circle class="pm" cx="{X(x2)}" cy="{Y(y2)}" r="3"/>'
            f'<path class="traza" data-traza d="M{X(0)} {Y(0)} C{X(x1)} {Y(y1)} {X(x2)} {Y(y2)} {X(1)} {Y(1)}"/></svg>')
dmap = {'crecer': 420, 'decaer': 900, 'latir': 1800, 'cortina': 1600, 'revocar': 240}
S('curvas', 'Curvas', 'Motion', f'''
<p class="ojo">Cinco curvas y ninguna más</p>
<h2 class="ancho">Toca una curva para verla correr</h2>
<div class="curvas">{''.join(f'<button class="curva {k}" data-curva="{",".join(str(x) for x in v["$value"])}" data-ms="{dmap[k]}" aria-label="Reproducir la curva {k}"><h3>{k}</h3>{curva_svg(v["$value"])}<div class="pista-c"><b></b></div><span class="val">cubic-bezier({", ".join(str(x) for x in v["$value"])})<br>{dmap[k]} ms</span></button>' for k, v in cur.items() if k != '$type')}</div>
<div class="franja"><p class="glosa">Caducar dura 900 ms y revocar 240: la diferencia de tiempo es la diferencia de significado. Con «reducir movimiento» activo, todo salta a su estado final sin transición.</p>
<p class="pie">Fuente: kino_entrega_2 · estetica-movimiento-decks.md</p></div>''', 'ancha')

# ── 22 Coreografía ───────────────────────────────────────────────────────────
T = 3200
carriles = [('Costura', 0, 420, 'costura'), ('Cortina', 420, 1600, ''), ('Aurora (detrás)', 0, 3200, 'fondo'), ('Portada', 1092, 1100, ''),
            ('Titular', 1300, 900, ''), ('Tarjetas ×4', 1500, 820 + 270, ''), ('Trazos SVG', 1800, 950, '')]
S('coreografia', 'Coreografía', 'Motion', f'''
<p class="ojo">Cómo entra una presentación</p>
<h2 class="ancho">La cortina se abre y cada ítem llega por su cuenta</h2>
<div class="tj" style="margin-bottom:16px"><div class="crono" style="--T:{T}">
{''.join(f'<span class="et">{n}</span><div class="carril"><i class="{c}" style="--a:{a};--d:{d}"></i></div>' for n,a,d,c in carriles)}
<div class="regla"><span>0 ms</span><span>800</span><span>1600</span><span>2400</span><span>3200</span></div></div></div>
<div class="rej r3">
<div class="escena"><p class="rol">Cascada de tarjetas</p><div class="escenario" data-demo="cascada">{''.join('<div class="tj" style="width:80px;height:70px;padding:0"></div>' for _ in range(4))}</div><button class="demo-rep" data-rep="cascada">▶ reproducir</button></div>
<div class="escena"><p class="rol">Filas de tabla</p><div class="escenario" data-demo="filas" style="flex-direction:column;align-items:stretch;gap:6px">{''.join('<div style="height:14px;border-radius:3px;background:var(--membrana);border:1px solid var(--bd-tenue)"></div>' for _ in range(5))}</div><button class="demo-rep" data-rep="filas">▶ reproducir</button></div>
<div class="escena"><p class="rol">Texto suelto</p><div class="escenario" data-demo="texto"><p class="lede" style="margin:0;text-align:center">Sube con desenfoque de 6 px.</p></div><button class="demo-rep" data-rep="texto">▶ reproducir</button></div>
</div>
<p class="pie">Solo transform y opacity (compositor). Tarjetas: subida de 26 px, escala .965, 820 ms, escalonado hasta 90 ms. Filas: desde la izquierda, 55 ms. SVG: de izquierda a derecha según su x.</p>''', 'ancha')

# ── 23 Estados en movimiento ─────────────────────────────────────────────────
S('ciclo', 'El pase en movimiento', 'Motion', f'''
<p class="ojo">Cuatro momentos del pase</p>
<h2 class="ancho">Otorgar, confirmar, caducar, revocar</h2>
<div class="rej r4">
<div class="escena"><p class="rol">Otorgar · crecer</p><div class="escenario" data-demo="otorgar"><div class="mini-pase" style="width:100%"><div class="f1"><b>Marta Q.</b><span class="est" data-e="sin-confirmar">Sin confirmar</span></div><div class="f2">lun–vie · 07:00–17:00</div></div></div><button class="demo-rep" data-rep="otorgar">▶ reproducir</button></div>
<div class="escena"><p class="rol">Confirmar · latir</p><div class="escenario" data-demo="confirmar"><div class="mini-pase" style="width:100%"><div class="f1"><b>Marta Q.</b><span class="est" data-e="sin-confirmar">Sin confirmar</span></div><div class="f2">el lector respondió</div></div></div><button class="demo-rep" data-rep="confirmar">▶ reproducir</button></div>
<div class="escena"><p class="rol">Caducar · decaer</p><div class="escenario" data-demo="caducar"><div class="mini-pase vivo" style="width:100%"><div class="f1"><b>Técnico de gas</b><span class="est" data-e="por-vencer">40 min</span></div><div class="ventana"><i style="left:0;right:60%"></i></div></div></div><button class="demo-rep" data-rep="caducar">▶ reproducir</button></div>
<div class="escena"><p class="rol">Revocar · corte</p><div class="escenario" data-demo="revocar"><div class="mini-pase vivo" style="width:100%"><div class="f1"><b>Placa HTK 481</b><span class="est" data-e="vigente">Vigente</span></div><div class="f2">revoca: Ana Ruiz</div></div></div><button class="demo-rep" data-rep="revocar">▶ reproducir</button></div>
</div>
<div class="franja"><p class="glosa">El estado cambia de palabra y de color al mismo tiempo, nunca solo de color. Caducar desvanece despacio; revocar corta en 240 ms y deja el motivo escrito.</p><p class="pie">Demostraciones con los tokens de movimiento; respetan «reducir movimiento».</p></div>''', 'ancha')

# ── 24 Interacción y fondo ───────────────────────────────────────────────────
S('interaccion', 'Interacción y fondo', 'Motion', f'''
<p class="ojo">Luz, puntero y fondo</p>
<h2 class="ancho">El fondo respira; las tarjetas responden a la mano</h2>
<div class="rej r3" style="margin-bottom:14px">
<div class="tj"><p class="rol">Aurora · WebGL</p><h3>Un campo, no una imagen</h3><p class="peq">Oscuro: menta profunda <span class="mono">#006B4C</span>, índigo <span class="mono">#2E2470</span>, base. Media resolución (0,5): de 4 a 9 veces más barato. Sin cambio automático a mitad de la presentación.</p></div>
<div class="tj"><p class="rol">Velo</p><h3>Existe por contraste</h3><p class="peq">Velo del color base al 55 % (oscuro) y 50 % (claro). Peor caso medido: texto tenue a 4,65:1 y 5,28:1. Si cambia la paleta, se vuelve a medir.</p></div>
<div class="tj"><p class="rol">Puntero</p><h3>Foco e inclinación</h3><p class="peq">Pasa el puntero por esta tarjeta: foco de luz de radio 300 e inclinación de 4°, perspectiva 1000. Solo con puntero fino y sin «reducir movimiento».</p></div>
</div>
<div class="rej r4">
<div class="tj"><span class="cifra">1</span><p class="peq">requestAnimationFrame para todo el motor.</p></div>
<div class="tj"><span class="cifra">3</span><p class="peq">ciclos de latido como máximo (WCAG 2.2.2).</p></div>
<div class="tj"><span class="cifra">6 s</span><p class="peq">tope de seguridad: la cortina se retira siempre.</p></div>
<div class="tj"><span class="cifra">0</span><p class="peq">animaciones con «reducir movimiento»: ni cortina, ni aurora, ni cascada.</p></div>
</div>''', 'ancha')

# ── 25 Voz ───────────────────────────────────────────────────────────────────
p = voz['perfil']
ON, OFF = '<i class="on"></i>', '<i></i>'
dims = ''.join('<div class="dim"><span>%s</span><div class="esc">%s</div><span>%s</span><p class="nota">%s</p></div>' % (p[d]["polos"][0], ''.join(ON if i+1 == p[d]["valor"] else OFF for i in range(5)), p[d]["polos"][1], e(p[d]["nota"])) for d in ['formalidad','humor','respeto','entusiasmo'])
S('voz', 'Voz', 'Verbal', f'''
<p class="ojo">Cómo habla Kino</p>
<h2 class="ancho">Exacto, honesto con el estado, breve</h2>
<div class="rej r2" style="gap:30px;align-items:start">
<div class="tj"><p class="rol">Perfil de tono · NN/g · aprobado 22 sep</p>{dims}</div>
<div class="rej" style="gap:12px">
<div class="dicho"><div class="mal"><b>No</b>¡Listo! Tu invitado ya tiene acceso.</div><div class="bien"><b>Sí</b>Pase enviado al lector. Vigente cuando la puerta confirme.</div></div>
<div class="dicho"><div class="mal"><b>No</b>El administrador debe aprobar el ingreso.</div><div class="bien"><b>Sí</b>La administración fija los límites; tú otorgas el pase.</div></div>
<div class="dicho"><div class="mal"><b>No</b>Crea una cuenta para tu visita.</div><div class="bien"><b>Sí</b>Sofía entra con un código de un solo uso. No necesita cuenta.</div></div>
<div class="tj"><p class="rol">Vocabulario</p><p class="peq"><b>pase</b> lo recibe el invitado · <b>cuenta</b> la tiene el residente · <b>acceso previsto</b> el pase preparado antes · <b>otorgar</b> el único acto con acento · <b>lector</b> lo que abre la puerta.</p></div>
</div></div>
<p class="pie">Fuente: gorr-brand-system/clientes/kino/voz.json · evals de voz 12/15 (80 %) · calibración 21/42, 0 falsos positivos</p>''', 'ancha')

# ── 26 Aplicaciones ──────────────────────────────────────────────────────────
S('aplicaciones', 'Aplicaciones', 'Producto', f'''
<p class="ojo">El sistema en el producto</p>
<h2 class="ancho">La misma pieza para el residente y para la portería</h2>
<div class="rej r3" style="align-items:center;gap:30px">
<div class="telefono"><div class="pant">
<div class="sup"><b>Kino<span>.</span></b><span>09:41</span></div>
<div class="tit">Accesos previstos</div><div class="conj">Refugio Campestre · casa 14</div>
<div class="lista">
<div class="mini-pase vivo"><div class="f1"><b>Marta Quintero</b><span class="est" data-e="vigente">Vigente</span></div><div class="f2">trabajo doméstico · lun–vie</div><div class="ventana"><i style="left:0;right:22%"></i></div></div>
<div class="mini-pase sc"><div class="f1"><b>Técnico de gas</b><span class="est" data-e="sin-confirmar">Sin confirmar</span></div><div class="f2">hoy · 14:00–16:00 · enviado al lector</div></div>
<div class="mini-pase"><div class="f1"><b>Placa HTK 481</b><span class="est" data-e="por-vencer">40 min</span></div><div class="f2">visita · entró 13:12</div><div class="ventana"><i style="left:0;right:86%;background:var(--pv-bd)"></i></div></div>
</div>
<div class="boton">Otorgar un pase</div>
</div></div>
<div class="rej" style="gap:12px">
<div class="tj"><p class="rol">El conjunto es un dato</p><p class="peq">«Refugio Campestre · casa 14» va en mono, como contexto. Sin logo ni colores del conjunto: Kino es la marca.</p></div>
<div class="tj acento"><p class="rol">Un solo acento por pantalla</p><p class="peq">El botón que otorga. Texto de 18 px en 700 para que se lea con la regla de APCA.</p></div>
<div class="tj"><p class="rol">Honesto con el estado</p><p class="peq">El técnico va punteado y sin relleno: el lector aún no confirmó.</p></div>
</div>
<div class="rej" style="gap:12px">
<div class="tj"><p class="rol">Deck</p><p class="peq">Este mismo shell: barra, cortina, aurora, coreografía. Cada lámina con su grado y su fuente.</p></div>
<div class="tj"><p class="rol">Documento</p><p class="peq">Cuerpo en Archivo, cifras en mono tabular, citas con borde de acento y el archivo de origen al final.</p></div>
<div class="tj"><p class="rol">Portería</p><p class="peq">El mismo pase, con los datos personales truncados y marcados como identidad.</p></div>
</div></div>''', 'ancha')

# ── 27 Gobierno ──────────────────────────────────────────────────────────────
S('gobierno', 'Gobierno', 'Mantenimiento', f'''
<p class="ojo">Dónde vive y cómo se cambia</p>
<h2 class="ancho">Un color se cambia en un solo lugar</h2>
<div class="cadena" style="margin-bottom:20px">
<div class="eslabon">{ic('documento')}<b>marca.config.json</b><span>matices, objetivos, reglas</span></div><span class="conector"></span>
<div class="eslabon">{ic('lista')}<b>tokens DTCG</b><span>validados con 2 validadores</span></div><span class="conector"></span>
<div class="eslabon acento">{ic('check')}<b>verificación</b><span>contraste, voz, variables</span></div><span class="conector"></span>
<div class="eslabon">{ic('codigo')}<b>kino-brand.css</b><span>la app, este deck</span></div><span class="conector"></span>
<div class="eslabon">{ic('matraz')}<b>skill kino-marca</b><span>Claude produce con la marca</span></div>
</div>
<div class="rej r2">
<div class="tj"><p class="rol">Herramientas activas · 23 sep</p><div class="versiones">
<div><b>Terrazzo</b><span>2.7.1</span></div><div><b>Leonardo</b><span>1.1.0</span></div><div><b>APCA</b><span>0.1.9</span></div>
<div><b>Utopia</b><span>1.6.0</span></div><div><b>promptfoo</b><span>0.123.1</span></div><div><b>color.js</b><span>0.7.1</span></div>
<div><b>Iconoir</b><span>7.12.1</span></div><div><b>DTCG skill</b><span>✓</span></div><div><b>Motion</b><span>✓</span></div></div></div>
<div class="tj"><p class="rol">Para cambiar algo</p><ol class="pasos"><li>Editar <span class="mono">clientes/kino/marca.config.json</span> o <span class="mono">voz.json</span>.</li><li><span class="mono">npm run construir</span> en <span class="mono">branding/sistema</span>.</li><li>Si algo no cumple, la cadena se detiene y dice qué.</li></ol></div>
</div>
<p class="pie">Fuente: gorr-brand-system · versiones-herramientas.txt</p>''', 'ancha')

# ── 28 Cierre ────────────────────────────────────────────────────────────────
S('cierre', 'Cierre', '', f'''
<div class="marca-portada">{svg_v('role="img" aria-label="Kino" style="width:min(18vw,190px)"').replace('aria-hidden="true" ','')}</div>
<p class="autores">Nicolás Ramírez &nbsp;·&nbsp; Alejandro Monsalve</p>
<p class="pie" style="text-align:center;margin:0">Lo abierto: la unidad de los cupos · la licencia de Arkit ExtraBold · la paleta en las pantallas de portería</p>''')

# ── Ensamblaje ───────────────────────────────────────────────────────────────
N = len(secciones)
nav = ''.join(f'<a href="#{id}" data-i="{i}">{e(n)}</a>' for i, (id, n, *_ ) in enumerate(secciones))
cuerpo = ''
for i, (id, n, cap, clase, h) in enumerate(secciones):
    capx = f'<span class="cap">{e(cap)}</span>' if cap else ''
    cuerpo += f'<section id="{id}"{f" class={chr(34)}{clase}{chr(34)}" if clase else ""}>{capx}<span class="num mono">{i+1:02d} / {N}</span><div class="interior">{h}</div></section>\n'

demos = open('kino-movimiento.js').read() + '\n' + open('demos.js').read()
paginar = open('paginar.js').read()
out = f'''<!doctype html>
<html lang="es" data-tema="oscuro"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kino · Sistema de marca</title>
<meta name="description" content="Sistema de marca de Kino v2: identidad, color, tipografía, componentes, gramática de flujo, el pase, movimiento y voz.">
{fonts}
<style>{CSS}</style>
<script>{s_head}</script>
</head><body>
{sprite}
<div class="barra"><div class="marca">Kino<span>.</span></div><nav>{nav}</nav><button id="tema">tema</button></div>
<div class="prog"></div>
<div id="fondo" aria-hidden="true"></div>
<div id="velo" aria-hidden="true"></div>
<div id="cortina" aria-hidden="true"><i></i><i></i><b></b></div>
<main>
{cuerpo}</main>
<div class="visor"><button class="cerrar">cerrar · esc</button><div class="lienzo-grande"></div></div>
<script>{s_motor}</script>
<script>{s_ctrl}</script>
<script>{demos}</script>
<script>{paginar}</script>
</body></html>'''
open('Kino_Sistema_de_marca_2026-09-23.html', 'w').write(out)
print('láminas', N, 'bytes', len(out))

# Versión para el Artifact: sin doctype/html/head/body, con el tema fijado antes del primer pintado.
tema = '<script>try{var g=localStorage.getItem("kino-tema");document.documentElement.dataset.tema=g||"oscuro";}catch(e){document.documentElement.dataset.tema="oscuro";}</script>'
art = out.split('<head>',1)[1]
art = art.replace('<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n','')
art = art.replace('<title>Kino · Sistema de marca</title>','<title>Kino Sistema de Marca</title>')
art = art.replace('</head><body>', tema)
art = art.replace('</body></html>','')
open('artifact/kino-sistema-de-marca.html','w').write(art)
print('artifact bytes', len(art))
