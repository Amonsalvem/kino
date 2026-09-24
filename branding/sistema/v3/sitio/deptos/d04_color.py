from .comun import *  # noqa: F401,F403

FAMILIAS = [
    ('sustrato', 'Superficies del tema oscuro'), ('hueso', 'Texto y tema claro'),
    ('biolum', 'Marca, acción de otorgar y Vigente'), ('ambar', 'Por vencer'),
    ('carmin', 'Revocado y Rechazado'), ('violeta', 'Dato personal'), ('indigo', 'Previsto y enlaces'),
]


def _orden(k):
    m = re.match(r'([dla]?)(\d+)', k)
    return ({'': 0, 'd': 1, 'l': 2, 'a': 3}[m.group(1)], int(m.group(2)))


def _sobre(hexf):
    """Texto legible sobre una muestra: el que da más Lc."""
    a, b = PRIM['kino-sustrato-100'], PRIM['kino-hueso-100']
    return 'var(--kino-sustrato-100)' if abs(lc(a, hexf)) >= abs(lc(b, hexf)) else 'var(--kino-hueso-100)'


def _primitivos():
    out = []
    for fam, sig in FAMILIAS:
        pasos = sorted([k.split('-', 2)[2] for k in PRIM if k.startswith(f'kino-{fam}-')], key=_orden)
        celdas = ''.join(
            f'<li style="background:var(--kino-{fam}-{p});color:{_sobre(PRIM[f"kino-{fam}-{p}"])}"><b>{p}</b><span class="mono">{PRIM[f"kino-{fam}-{p}"]}</span></li>'
            for p in pasos)
        out.append(f'<div class="fam"><h3>{fam}<small>{sig}</small></h3><ol class="muestras">{celdas}</ol></div>')
    return ''.join(out)


ROLES = [
    ('superficie-abismo', 'Fondo más profundo: índice, cabeceras de tabla.'), ('superficie-base', 'Fondo de la app y del sitio.'),
    ('superficie-elevada', 'Tarjetas sobre la base.'), ('superficie-membrana', 'Controles, campos, el Pase.'),
    ('superficie-inversa', 'Bloques de contraste invertido.'),
    ('texto-primario', 'Todo texto de menos de 24 px.'), ('texto-secundario', 'Textos de apoyo en 16 px o más.'),
    ('texto-tenue', 'Solo desde 24 px: cifras grandes, rótulos de fondo.'), ('texto-inverso', 'Texto sobre la superficie inversa.'),
    ('borde-tenue', 'Separa sin informar.'), ('borde-definido', 'Borde que informa: campos, chips, tarjetas seleccionadas.'),
    ('borde-foco', 'Anillo de foco del teclado.'),
    ('acento-base', 'Verde de marca: logo, gota, nodo «Otorgar». Nunca de fondo bajo texto.'),
    ('accion-fondo', 'Botón que crea o entrega un Pase.'), ('accion-texto', 'Texto sobre ese botón.'),
    ('marca-bloque', 'Bloque del logo.'), ('marca-gota', 'Gota del logo.'),
]


def _sw(var, tema):
    h = hx('kino-' + var, tema)
    return f'<span class="sw" style="background:{h}"></span><span class="mono">{h}</span>'


def _roles():
    filas = [[f'<code>--kino-{v}</code>', _sw(v, 'oscuro'), _sw(v, 'claro'), u] for v, u in ROLES]
    return tabla(['Variable', 'Oscuro', 'Claro', 'Uso'], filas, 'Roles semánticos de color')


def _mini(tema):
    t = 'oscuro' if tema == 'en-oscuro' else 'claro'
    return f'''<div class="{tema} mini-tema">
  <p class="ojo">Tema {t}</p>
  <div class="kino-pase" data-estado="vigente">
    <div class="kino-pase__cabeza"><p class="kino-pase__quien">Andrés Gómez</p>{chip('vigente', 'Vigente')}</div>
    <p class="kino-pase__autor">Otorgó Carolina Ruiz · Casa 14</p>
    <span class="kino-vigencia" style="--kino-vida:.62"><i></i></span>
    <p class="kino-pase__pie"><span class="kino-dato">KMN 305</span><span class="kino-dato">hasta 6:00 p. m.</span></p>
  </div>
  <p class="mt-texto">Texto primario. <span class="secundario">Texto secundario.</span></p>
  <button class="kino-accion" type="button" tabindex="-1">Crear Pase</button>
</div>'''


def _estados():
    chips = lambda: ''.join(chip(k, n) for k, n, _ in ESTADOS)
    filas = []
    for k, n, d in ESTADOS:
        fo, fc = hx(f'kino-estado-{k}-fondo'), hx(f'kino-estado-{k}-fondo', 'claro')
        to, tc = hx(f'kino-estado-{k}-texto'), hx(f'kino-estado-{k}-texto', 'claro')
        bo = hx(f'kino-estado-{k}-borde')
        bgo = hx('kino-superficie-base') if k == 'sin-confirmar' else fo
        bgc = hx('kino-superficie-base', 'claro') if k == 'sin-confirmar' else fc
        filas.append([chip(k, n), e(d), f'<span class="mono">{to}</span> sobre <span class="mono">{"transparente" if k == "sin-confirmar" else fo}</span>',
                      f'<b class="mono">{abs(lc(to, bgo))}</b>', f'<span class="mono">{abs(lc(bo, hx("kino-superficie-base")))}</span>',
                      f'<b class="mono">{abs(lc(tc, bgc))}</b>'])
    return (f'<div class="estados-dos"><div class="en-oscuro fila-chips">{chips()}</div><div class="en-claro fila-chips">{chips()}</div></div>'
            + tabla(['Estado', 'Qué dice', 'Texto sobre fondo (oscuro)', 'Lc texto', 'Lc borde', 'Lc texto (claro)'], filas, 'Colores de los estados')
            + casos(caso(f'<div class="pase-linea">{chip("vigente", "Vigente")}<span class="kino-dato">hasta 6:00 p. m.</span></div>', 'Palabra, color y hora.'),
                    caso('<div class="pase-linea"><span class="solo-color" aria-hidden="true"></span><span class="kino-dato">6:00 p. m.</span></div>', 'Un punto verde sin palabra: quien no distingue el verde no sabe nada.', False),
                    caso(f'<div class="pase-linea">{chip("sin-confirmar", "Sin confirmar")}<span class="kino-dato">KMN 305</span></div>', 'El lector no respondió: borde discontinuo y sin relleno.'),
                    caso('<div class="pase-linea"><span class="kino-estado ej-mal" data-estado="vigente">Permitido</span><span class="kino-dato">KMN 305</span></div>', 'Verde sobre algo que la puerta no confirmó.', False))
            + traza('V5 y X10 (nombres y colores), H4 (el color solo nombra hechos confirmados) y el valor «Estado honesto».'))


def _datos():
    cat = [('indigo', 'd70'), ('biolum', 'd70'), ('ambar', 'd70'), ('violeta', 'd70'), ('sustrato', 'd90')]
    catc = [('indigo', 'l45'), ('biolum', 'l45'), ('ambar', 'l45'), ('violeta', 'l45'), ('sustrato', 'l70')]
    li = lambda lst: ''.join(f'<li><span class="sw" style="background:var(--kino-{f}-{p})"></span><span class="mono">{f}.{p}</span><span class="mono">{PRIM[f"kino-{f}-{p}"]}</span></li>' for f, p in lst)
    seq = ''.join(f'<span style="background:var(--kino-biolum-{p})"></span>' for p in ('d15', 'd23', 'd32', 'd45', 'd70', 'd90', 'd110'))
    dias = [('lun', 38), ('mar', 31), ('mié', 34), ('jue', 41), ('vie', 46), ('sáb', 22), ('dom', 18)]
    mx = 50
    barras = ''.join(f'<g transform="translate({40 + i * 52} 0)"><rect class="barra" x="0" y="{170 - v / mx * 150:.0f}" width="32" height="{v / mx * 150:.0f}" rx="3"/>'
                     f'<text class="eje" x="16" y="188" text-anchor="middle">{d}</text><text class="val" x="16" y="{164 - v / mx * 150:.0f}" text-anchor="middle">{v}</text></g>' for i, (d, v) in enumerate(dias))
    graf = (f'<svg class="grafico" viewBox="0 0 420 196" width="420" height="196" style="aspect-ratio:420/196" role="img" aria-label="Pases otorgados por día, ejemplo: de 18 el domingo a 46 el viernes">'
            f'<line class="base" x1="30" y1="170" x2="410" y2="170"/>{barras}</svg>')
    apil = [('usado', 187), ('vencido', 21), ('revocado', 3), ('rechazado', 3)]
    tot = sum(v for _, v in apil)
    x = 0
    segs = ''
    for k, v in apil:
        w = v / tot * 380
        segs += f'<rect x="{20 + x:.1f}" y="20" width="{w:.1f}" height="28" style="fill:var(--kino-estado-{k}-fondo);stroke:var(--kino-estado-{k}-borde)"/>'
        x += w
    ley = ''.join(f'<li>{chip(k, k.capitalize())}<span class="mono">{v} de {tot}</span></li>' for k, v in apil)
    apilado = (f'<svg class="grafico" viewBox="0 0 420 64" width="420" height="64" style="aspect-ratio:420/64" role="img" aria-label="Destino de 214 Pases, ejemplo">{segs}</svg><ul class="leyenda">{ley}</ul>')
    return (f'<div class="datos-paletas"><div><h3>Categorías (oscuro)</h3><ol class="lista-sw">{li(cat)}</ol></div>'
            f'<div><h3>Categorías (claro)</h3><ol class="lista-sw">{li(catc)}</ol></div>'
            f'<div><h3>Secuencia</h3><div class="secuencia">{seq}</div><p class="nota">Una sola familia, de menos a más. Para cantidades de una misma cosa.</p></div></div>'
            + casos(caso(graf, 'Una serie, un color de la secuencia. Cifras en mono sobre cada barra. <span class="nota">(Datos de ejemplo.)</span>'),
                    caso(apilado, 'Cuando la serie es un estado, usa el color del estado y su palabra en la leyenda. <span class="nota">(Ejemplo.)</span>'))
            + '<ul class="reglas-cortas"><li>El carmín no va en gráficos salvo para Rechazado.</li><li>Máximo cinco categorías; la sexta se agrupa en «Otras».</li><li>Toda marca de dato pasa Lc 30 sobre su fondo; toda cifra, Lc 75.</li></ul>'
            + traza('Topes a la vista: la administración lee cifras con denominador.'))


def _proporciones():
    p = [('sustrato', 'var(--kino-sustrato-200)', 60, 'Superficies'), ('hueso', 'var(--kino-hueso-100)', 25, 'Texto'),
         ('neutros de apoyo', 'var(--kino-sustrato-500)', 10, 'Bordes y membranas'), ('biolum', 'var(--kino-biolum-d70)', 4, 'Marca y acción'),
         ('estados', 'linear-gradient(90deg,var(--kino-ambar-d70),var(--kino-carmin-d70),var(--kino-violeta-d70),var(--kino-indigo-d70))', 1, 'Solo donde hay un estado')]
    barra = ''.join(f'<span style="flex:{v};background:{c}" title="{n} {v} %"></span>' for n, c, v, _ in p)
    ley = ''.join(f'<li><span class="sw" style="background:{c}"></span><b class="mono">{v} %</b> {n}<small>{u}</small></li>' for n, c, v, u in p)
    return (f'<div class="proporcion">{barra}</div><ul class="leyenda-prop">{ley}</ul>'
            + casos(caso(f'<div class="en-oscuro mini-prop"><p>Casa 14</p><button class="kino-accion" type="button" tabindex="-1">Crear Pase</button></div>', 'Un solo verde en pantalla: el botón que otorga.'),
                    caso('<div class="en-oscuro mini-prop mal-verde"><p>Casa 14</p><button class="kino-accion" type="button" tabindex="-1">Crear Pase</button><button class="kino-accion" type="button" tabindex="-1">Ver historial</button></div>', 'Verde en todo: el botón que otorga deja de destacarse.', False))
            + traza('H3: el acento significa otorgar. Si aparece en todo, no significa nada.'))


def _apca():
    por = {}
    for f in CONTRASTE:
        por.setdefault(f['que'], {})[f['tema']] = f
    filas = []
    for que, t in por.items():
        o, c = t['oscuro'], t['claro']
        ok = o['pasa'] and c['pasa']
        filas.append([e(que), f'<span class="mono">{abs(o["apcaLc"])}</span> <small class="mono">{o["wcag"]}:1</small>',
                      f'<span class="mono">{abs(c["apcaLc"])}</span> <small class="mono">{c["wcag"]}:1</small>',
                      f'<span class="mono">Lc {o.get("apcaMin", "")} · {o["min"]}:1</span>', chip('vigente', 'Pasa') if ok else chip('rechazado', 'Falla')])
    return ('<p>Cada par que aparece en una pieza está en <code>pares.json</code> y se mide en los dos temas cada vez que cambian los tokens. La compuerta es doble: APCA (Lc) y WCAG 2.2 (razón).</p>'
            + tabla(['Par', 'Oscuro', 'Claro', 'Mínimo', 'Resultado'], filas, 'Contraste APCA de todos los pares', 'apca')
            + f'<p class="nota">{len(CONTRASTE)} mediciones · {sum(1 for f in CONTRASTE if not f["pasa"])} fallos. Mínimos de la plataforma: Lc 75 cuerpo, 60 texto grande, 45 titulares, 30 elementos no textuales.</p>'
            + descargas(descarga('Informe de contraste', 'kino-contraste.json', json.dumps(CONTRASTE, ensure_ascii=False, indent=1), 'application/json')))


# Machado, Oliveira y Fernandes (2009), severidad 1, sobre RGB lineal.
MATRICES = {
    'Protanopía': [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
    'Deuteranopía': [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]],
    'Tritanopía': [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]],
}


def simular(h, m):
    h = h.lstrip('#')
    lin = [(lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)(int(h[i:i + 2], 16) / 255) for i in (0, 2, 4)]
    out = [max(0, min(1, sum(m[r][k] * lin[k] for k in range(3)))) for r in range(3)]
    enc = lambda c: 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
    return '#' + ''.join(f'{round(enc(c) * 255):02X}' for c in out)


def _daltonismo():
    filas = []
    for k, n, _ in ESTADOS:
        f, t = hx(f'kino-estado-{k}-fondo'), hx(f'kino-estado-{k}-texto')
        if k == 'sin-confirmar':
            f = hx('kino-superficie-base')
        celdas = [f'<span class="chip-sim" style="background:{f};color:{t};border-color:{t}">{n}</span>']
        for m in MATRICES.values():
            fs, ts = simular(f, m), simular(t, m)
            celdas.append(f'<span class="chip-sim" style="background:{fs};color:{ts};border-color:{ts}">{n}</span> <small class="mono">Lc {abs(lc(ts, fs))}</small>')
        filas.append(celdas)
    return ('<p>Los nueve estados en el tema oscuro, simulados con las matrices de Machado (2009). Con protanopía y deuteranopía, Vigente, Por vencer y Rechazado se acercan en tono: por eso cada estado lleva palabra y el punto cambia de forma (lleno, discontinuo o cuadrado).</p>'
            + tabla(['Visión típica', *MATRICES.keys()], filas, 'Simulación de daltonismo de los estados')
            + '<p class="nota">La simulación no reemplaza una prueba con personas daltónicas ' + pend('prueba con usuarios daltónicos') + '.</p>')


def _cmyk(h):
    r, g_, b = [int(h.lstrip('#')[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    k = 1 - max(r, g_, b)
    if k >= 1:
        return 0, 0, 0, 100
    return tuple(round(100 * v) for v in ((1 - r - k) / (1 - k), (1 - g_ - k) / (1 - k), (1 - b - k) / (1 - k), k))


def _impresion():
    cl = [('Sustrato', 'kino-sustrato-200'), ('Hueso', 'kino-hueso-100'), ('Verde de marca', 'kino-biolum-d70'), ('Verde sobre claro', 'kino-biolum-l70'),
          ('Ámbar', 'kino-ambar-d70'), ('Carmín', 'kino-carmin-d45'), ('Violeta', 'kino-violeta-d45'), ('Índigo', 'kino-indigo-d45')]
    filas = []
    for n, v in cl:
        h = PRIM[v]
        rgb = ' '.join(str(int(h[i:i + 2], 16)) for i in (1, 3, 5))
        c = _cmyk(h)
        filas.append([f'<span class="sw" style="background:var(--{v})"></span>{n}', f'<span class="mono">{h}</span>', f'<span class="mono">{rgb}</span>', f'<span class="mono">{c[0]} {c[1]} {c[2]} {c[3]}</span>'])
    return (tabla(['Color', 'Hex', 'RGB', 'CMYK aproximado'], filas, 'Valores para impresión')
            + '<p class="nota">Los CMYK salen de una conversión directa, sin perfil de color. Son un punto de partida para la imprenta; antes de un tiraje se pide una prueba física. El Pantone equivalente está ' + pend('equivalencias Pantone') + '.</p>')


def html_():
    tokens_json = (GBS / 'build/tokens.resuelto.json').read_text(encoding='utf8')
    cuerpo = '\n'.join([
        sub('color.primitivos', 'Primitivos', 'Siete familias, cada una con un significado',
            'Los pasos <b>100 a 800</b> ordenan los neutros por luminosidad. <b>d45</b> quiere decir «4,5:1 sobre el fondo oscuro» y <b>l45</b>, lo mismo sobre el claro. Los pasos <b>a</b> son los fijados por APCA en el tema oscuro reajustado: <b>a84</b> da al menos Lc 84 sobre la base.',
            _primitivos() + descargas(descarga('Tokens DTCG resueltos', 'kino-tokens.resuelto.json', tokens_json, 'application/json'),
                                      descarga('Tokens en CSS', 'kino-tokens.css', TOKENS_CSS, 'text/css'))
            + traza('Regla 6 del encargo: una sola fuente de verdad, los tokens DTCG del cliente kino.')),
        sub('color.roles', 'Roles', 'En código se usa el rol, nunca el hex',
            'Cada rol apunta a un primitivo distinto en cada tema. Si mañana cambia un paso, cambian todas las piezas.',
            _roles() + casos(caso('<code class="bloque-cod">color: var(--kino-texto-secundario);</code>', 'El rol dice para qué es el color.'),
                             caso('<code class="bloque-cod">color: #CEDBD6;</code>', 'Un hex suelto no se entera cuando la paleta cambia.', False))),
        sub('color.temas', 'Temas', 'Oscuro para la app y la entrada, claro para el papel',
            'El oscuro reajustado es el canónico. El claro se usa en el PDF del Pase, la papelería y quien lo elija en la app.',
            f'<div class="temas-dos">{_mini("en-oscuro")}{_mini("en-claro")}</div>'
            + traza('X3: oscuro reajustado para pasar APCA. Se lee mejor de noche en la entrada; el PDF va en claro porque se imprime.')),
        sub('color.estados', 'Estados', 'Siete estados del Pase, un evento y un dato',
            'Todo texto de estado pasa Lc 75, así sirve en chips de 13 px. Todo borde pasa Lc 30. ' + g('sin-confirmar', 'Sin confirmar') + ' va sin relleno y ' + g('rechazado', 'Rechazado') + ' es un evento de la entrada, no un estado del Pase.',
            _estados()),
        sub('color.datos', 'Datos y gráficos', 'Colores para contar cifras', '', _datos()),
        sub('color.proporciones', 'Proporciones', 'Mucho sustrato, poco verde', 'Una pantalla típica de Kino, medida por área.', _proporciones()),
        sub('color.contraste', 'Contraste APCA', 'Todos los pares, medidos en los dos temas', '', _apca()),
        sub('color.daltonismo', 'Daltonismo', 'Qué ve alguien que no distingue rojo y verde', '', _daltonismo()),
        sub('color.impresion', 'Impresión', 'Valores aproximados para imprenta', '', _impresion()),
    ])
    return seccion('color', '04', 'Color', 'Identidad',
                   'La paleta y lo que significa cada color, incluidos los estados de un Pase.',
                   'Para que un color signifique siempre lo mismo: vigente, por vencer, usado, vencido o rechazado.',
                   'Al elegir el color de cualquier texto, fondo, borde o gráfico.', cuerpo)
