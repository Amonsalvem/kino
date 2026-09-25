from .comun import *  # noqa: F401,F403

H = lambda n: hx(n)            # hex en oscuro
HC = lambda n: hx(n, 'claro')  # hex en claro


def _grilla():
    lineas = ''.join(f'<line x1="{i}" y1="0" x2="{i}" y2="101.824"/><line x1="0" y1="{i}" x2="100" y2="{i}"/>' for i in range(0, 101, 10))
    return f'''<svg class="lg-grilla" viewBox="-14 -8 128 120" width="512" height="480" style="aspect-ratio:128/120" role="img" aria-labelledby="lg-t">
<title id="lg-t">Construcción del símbolo sobre una grilla de 100 unidades</title>
<g class="lg-lineas">{lineas}</g>
<path class="lg-bloque" fill-rule="evenodd" d="{BLOQUE}"/><path class="lg-gota" d="{GOTA}"/>
<circle class="lg-guia" cx="49.917" cy="46.766" r="31.675"/><ellipse class="lg-guia" cx="50" cy="53.566" rx="16.169" ry="17.579"/>
<line class="lg-cota" x1="18.242" y1="95" x2="81.592" y2="95"/><text class="lg-num" x="50" y="104" text-anchor="middle">vano 63,4</text>
<line class="lg-cota" x1="-6" y1="0" x2="-6" y2="101.824"/><text class="lg-num" x="-9" y="52" text-anchor="middle" transform="rotate(-90 -9 52)">alto 101,8</text>
<line class="lg-cota" x1="33.831" y1="30" x2="66.169" y2="30"/><text class="lg-num" x="50" y="27" text-anchor="middle">gota 32,3</text>
<text class="lg-num" x="97" y="-2" text-anchor="end">radio 3,5</text>
</svg>'''


def _proteccion(forma):
    w, h = PROP[forma]
    x = 32.3
    return (f'<svg class="lg-prot" viewBox="{-x} {-x} {w + 2 * x:.1f} {h + 2 * x:.1f}" width="{w + 2 * x:.0f}" height="{h + 2 * x:.0f}" '
            f'style="aspect-ratio:{w + 2 * x:.1f}/{h + 2 * x:.1f}" role="img" aria-label="Área de protección alrededor del logo {forma}">'
            f'<rect class="lg-zona" x="{-x}" y="{-x}" width="{w + 2 * x:.1f}" height="{h + 2 * x:.1f}"/>'
            f'<rect class="lg-borde" x="0" y="0" width="{w}" height="{h}"/>'
            f'<g>{logo(forma, etiqueta=None, clase=None)[logo(forma, etiqueta=None, clase=None).index(">") + 1:-6]}</g>'
            f'<path class="lg-gota-x" d="{GOTA}" transform="translate({-x - 33.831:.3f} {-x - 35.987:.3f})"/>'
            f'<text class="lg-num" x="{-x / 2:.1f}" y="{h / 2:.1f}" text-anchor="middle">x</text></svg>')


def _icono_app(tam=1024, radio=224):
    esc = tam * 0.49 / 100
    dx, dy = (tam - 100 * esc) / 2, (tam - 101.824 * esc) / 2
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {tam} {tam}" width="{tam}" height="{tam}">'
            f'<rect width="{tam}" height="{tam}" rx="{radio}" fill="{H("kino-superficie-base")}"/>'
            f'<g transform="translate({dx:.2f} {dy:.2f}) scale({esc:.4f})"><path fill="{H("kino-marca-bloque")}" fill-rule="evenodd" d="{BLOQUE}"/>'
            f'<path fill="{H("kino-marca-gota")}" d="{GOTA}"/></g></svg>')


def _favicon():
    # A 16 px la gota mide 5 px: se mantiene. Fondo de sustrato para leerse en pestañas claras y oscuras.
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">'
            f'<rect width="32" height="32" rx="7" fill="{H("kino-superficie-base")}"/>'
            f'<g transform="translate(4.5 4.4) scale(.23)"><path fill="{H("kino-marca-bloque")}" fill-rule="evenodd" d="{BLOQUE}"/>'
            f'<path fill="{H("kino-marca-gota")}" d="{GOTA}"/></g></svg>')


VERSIONES = [
    # (id, nombre, fondo css, forma, bloque css, gota css, palabra, hex bloque, hex gota, uso)
    ('color-oscuro', 'Color sobre oscuro (principal)', 'var(--kino-superficie-base)', 'horizontal', 'var(--kino-marca-bloque)', 'var(--kino-marca-gota)',
     H('kino-marca-bloque'), H('kino-marca-gota'), 'App, sitio, portería, redes. Es la versión por defecto.'),
    ('color-claro', 'Color sobre claro', 'var(--kino-hueso-100)', 'horizontal', 'var(--kino-sustrato-100)', 'var(--kino-biolum-l70)',
     HC('kino-marca-bloque'), HC('kino-marca-gota'), 'PDF del Pase, papelería, documentos para administraciones.'),
    ('negro', 'Una tinta, negro', 'var(--kino-fijo-blanco)', 'horizontal', 'var(--kino-fijo-negro)', 'var(--kino-fijo-negro)',
     '#000000', '#000000', 'Sello, grabado láser, impresión en una tinta. La gota queda hueca como el arco.'),
    ('blanco', 'Una tinta, blanco', 'var(--kino-sustrato-100)', 'horizontal', 'var(--kino-fijo-blanco)', 'var(--kino-fijo-blanco)',
     '#FFFFFF', '#FFFFFF', 'Sobre fotografía oscura, vinilo blanco, serigrafía.'),
    ('simbolo', 'Solo símbolo', 'var(--kino-superficie-base)', 'simbolo', 'var(--kino-marca-bloque)', 'var(--kino-marca-gota)',
     H('kino-marca-bloque'), H('kino-marca-gota'), 'Ícono de app, favicon, avatar, sello del Pase. Cuando «Kino» ya está escrito cerca.'),
    ('vertical', 'Vertical', 'var(--kino-superficie-base)', 'vertical', 'var(--kino-marca-bloque)', 'var(--kino-marca-gota)',
     H('kino-marca-bloque'), H('kino-marca-gota'), 'Espacios angostos: adhesivo de talanquera, credencial, portada de una página.'),
]


def _version(v):
    id_, nombre, fondo, forma, b, gt, hb, hg, uso = v
    una_tinta = id_ in ('negro', 'blanco')
    svg_vivo = logo(forma, bloque=b, gota=gt, etiqueta=f'Kino, versión {nombre.lower()}')
    svg_arch = logo(forma, bloque=hb, gota=hg, hex_=True)
    if una_tinta:  # en una tinta la gota no se pinta encima: queda el vano
        svg_vivo = re.sub(r'<path style="fill:[^"]*" d="M 50.000[^"]*"/>', '', svg_vivo)
        svg_arch = re.sub(r'<path fill="[^"]*" d="M 50.000[^"]*"/>', '', svg_arch)
    png = (1024, round(1024 * PROP[forma][1] / PROP[forma][0])) if forma != 'horizontal' else (1600, round(1600 * 101.824 / 267.96))
    return (f'<figure class="lg-version"><div class="lg-lienzo" style="background:{fondo}">{svg_vivo}</div>'
            f'<figcaption><h3>{nombre}</h3><p>{uso}</p>{descargas(descarga("Descargar", f"kino-{id_}.svg", svg_arch, png=png))}</figcaption></figure>')


FONDOS = [
    ('Sustrato', 'background:var(--kino-sustrato-200)', 'color'),
    ('Hueso', 'background:var(--kino-hueso-100)', 'claro'),
    ('Aurora', 'background:radial-gradient(120% 80% at 85% 0%,color-mix(in oklch,var(--kino-biolum-d23) 70%,transparent),transparent 60%),radial-gradient(90% 70% at 0% 100%,color-mix(in oklch,var(--kino-violeta-d15) 80%,transparent),transparent 65%),var(--kino-sustrato-100)', 'color'),
    ('Tejido celular (impreso)', 'background:var(--kino-sustrato-200);background-image:radial-gradient(circle at 30% 30%,var(--kino-sustrato-400) 0 18%,transparent 19%),radial-gradient(circle at 75% 65%,var(--kino-sustrato-300) 0 24%,transparent 25%);background-size:64px 64px,88px 88px', 'color'),
    ('Verde de marca', 'background:var(--kino-biolum-d70)', 'negro-sustrato'),
    ('Fotografía oscura', 'background:linear-gradient(160deg,var(--kino-sustrato-500),var(--kino-sustrato-100) 70%)', 'blanco'),
]


def _fondo(nombre, estilo, version):
    if version == 'claro':
        l = logo('horizontal', bloque='var(--kino-sustrato-100)', gota='var(--kino-biolum-l70)', etiqueta=None)
        cual = 'Color sobre claro'
    elif version == 'negro-sustrato':
        l = re.sub(r'<path style="fill:[^"]*" d="M 50.000[^"]*"/>', '', logo('horizontal', bloque='var(--kino-sustrato-100)', gota='var(--kino-sustrato-100)', etiqueta=None))
        cual = 'Una tinta en sustrato: la gota verde se perdería'
    elif version == 'blanco':
        l = re.sub(r'<path style="fill:[^"]*" d="M 50.000[^"]*"/>', '', logo('horizontal', bloque='var(--kino-fijo-blanco)', gota='var(--kino-fijo-blanco)', etiqueta=None))
        cual = 'Una tinta, blanco'
    else:
        l = logo('horizontal', etiqueta=None)
        cual = 'Color sobre oscuro'
    return f'<figure class="lg-fondo"><div class="lg-lienzo" style="{estilo}">{l}</div><figcaption><strong>{nombre}</strong><span>{cual}</span></figcaption></figure>'


def _mal(viz, texto):
    return f'<figure class="lg-mal"><div class="lg-lienzo">{viz}</div><figcaption><span class="x" aria-hidden="true">✕</span>{texto}</figcaption></figure>'


def html_():
    L = lambda **k: logo('horizontal', etiqueta=None, **k)
    S = lambda **k: logo('simbolo', etiqueta=None, **k)
    malos = ''.join([
        _mal(L(attrs='preserveAspectRatio="none"').replace('style="aspect-ratio:267.96/101.824"', 'style="aspect-ratio:267.96/60;width:100%;height:auto"'), 'Estirar o aplastar. El arco deja de ser un vano.'),
        _mal(f'<div style="transform:rotate(-12deg)">{L()}</div>', 'Rotar. El bloque se lee como una puerta caída.'),
        _mal(L(gota='var(--kino-carmin-d70)'), 'Cambiar el color de la gota. El carmín significa Rechazado.'),
        _mal(L(bloque='transparent', gota='transparent').replace('<path style="fill:transparent"', '<path style="fill:transparent;stroke:var(--kino-hueso-100);stroke-width:1.5"'), 'Dibujarlo solo con contorno.'),
        _mal(f'<div style="filter:drop-shadow(0 0 12px var(--kino-biolum-d110)) drop-shadow(4px 6px 0 var(--kino-carmin-d45))">{L()}</div>', 'Sombras, brillos o neón. El resplandor es del Pase vigente, no del logo.'),
        _mal(L().replace(f'd="{GOTA}"', f'transform="translate(0 -30)" d="{GOTA}"'), 'Sacar la gota del arco o moverla.'),
        _mal('<div class="lg-escrito">' + S() + '<span class="ej-mal">KINO</span></div>', 'Reescribir «KINO» con otra letra. El logotipo es un dibujo cerrado.'),
        _mal(f'<div class="lg-bajo">{L(bloque="var(--kino-sustrato-500)", gota="var(--kino-biolum-d23)")}</div>', 'Ponerlo con poco contraste. El bloque necesita Lc 45 o más sobre su fondo.'),
        _mal(f'<div class="lg-duo">{L()}<span class="lg-emblema" aria-hidden="true">RC</span></div>', 'Ponerlo junto al emblema de un conjunto.'),
    ])
    simb_hex = logo('simbolo', bloque=H('kino-marca-bloque'), gota=H('kino-marca-gota'), hex_=True)
    app = _icono_app()
    fav = _favicon()

    cuerpo = '\n'.join([
        sub('logo.construccion', 'Construcción', 'Un bloque con un vano y una gota que pasa por él',
            'El símbolo se dibuja sobre una grilla de 100 unidades de ancho. Las medidas vienen de la reconstrucción desde el PNG de 1543 × 1425 px (98 % de coincidencia); no existe un vector original ' + pend('vector original del logo') + '.',
            f'<div class="lg-construye">{_grilla()}<div>'
            + tabla(['Pieza', 'Medida', 'Qué significa'], [
                ['Bloque', '100 × 101,8, radio 3,5', 'El conjunto: un lugar con borde.'],
                ['Vano', 'Arco de radio 31,7 y 63,4 de ancho', 'La entrada. La misma curva cierra la ventana del QR en el ' + g('pase', 'Pase') + '.'],
                ['Gota', '32,3 × 30,7', 'Lo que pasa por la entrada: la persona con su Pase.'],
                ['Logotipo', 'Arkit ExtraBold en contornos, alto 48,3', 'Se usa como dibujo; la fuente no se instala ' + pend('licencia de Arkit ExtraBold') + '.'],
              ], 'Medidas del símbolo')
            + descargas(descarga('Símbolo', 'kino-simbolo.svg', simb_hex, png=(1024, 1043)))
            + traza('F1 (el logo se conserva) y X1: el arco del logo es la forma del Pase.') + '</div></div>'),
        sub('logo.proteccion', 'Área de protección', 'Alrededor, el ancho de una gota',
            'La unidad <b>x</b> es el ancho de la gota: 32 % del ancho del símbolo. Ningún texto, borde ni imagen entra en esa franja.',
            f'<div class="lg-protegido">{_proteccion("horizontal")}{_proteccion("simbolo")}</div>'
            + casos(
                caso(f'<div class="lg-caja-prot">{L()}<p class="lg-junto">Refugio Campestre · Casa 14</p></div>', 'El dato del conjunto queda fuera de la franja x.'),
                caso(f'<div class="lg-caja-pegado">{L()}<p class="lg-junto">Refugio Campestre · Casa 14</p></div>', 'El texto toca el logo y se lee como parte del nombre.', False))
            + traza('Discreto: la marca se ve entera o no se pone.')),
        sub('logo.tamanos', 'Tamaños mínimos', 'Hasta dónde se puede achicar',
            'Por debajo de estos tamaños la gota se funde con el bloque o el logotipo pierde las letras.',
            tabla(['Versión', 'Pantalla', 'Impreso', 'Qué se pierde debajo'], [
                ['Solo símbolo', '<span class="mono">16 px</span>', '<span class="mono">6 mm</span>', 'La gota baja de 5 px y deja de leerse.'],
                ['Horizontal', '<span class="mono">88 px</span> de ancho', '<span class="mono">24 mm</span> de ancho', 'La «O» se cierra y la «N» se empasta.'],
                ['Vertical', '<span class="mono">48 px</span> de ancho', '<span class="mono">14 mm</span> de ancho', 'El logotipo queda por debajo de 8 px de alto.'],
              ], 'Tamaños mínimos del logo')
            + '<div class="lg-tamanos">' + ''.join(f'<figure><div style="width:{t}px">{S()}</div><figcaption class="mono">{t} px</figcaption></figure>' for t in (16, 24, 32, 48, 64))
            + ''.join(f'<figure><div style="width:{t}px">{L()}</div><figcaption class="mono">{t} px</figcaption></figure>' for t in (88, 140)) + '</div>'
            + casos(caso(f'<div style="width:88px">{L()}</div>', 'Horizontal a 88 px, el mínimo.'),
                    caso(f'<div style="width:44px">{L()}</div>', 'Horizontal a 44 px: usa el símbolo solo.', False))
            + '<p class="nota">Medidas propuestas desde la reconstrucción. Se confirman con una prueba impresa ' + pend('prueba física del logo') + '.</p>'),
        sub('logo.versiones', 'Versiones', 'Seis versiones y cuándo va cada una',
            'Todas salen del mismo dibujo; solo cambia el color. Cada una se descarga desde su tarjeta.',
            '<p class="nota">La gota usa el verde de la marca, #00BB83. Kino tiene cuatro verdes y cada uno dice algo distinto: #00BB83 es la marca; #00D595, el botón que crea un Pase; #00EAA5, el borde de Vigente y ese botón al presionarlo; #2FF8B2, el texto de Vigente. Detalle en <a href="#color.roles">Color</a>.</p>'
            + '<div class="lg-versiones">' + ''.join(_version(v) for v in VERSIONES) + '</div>'
            + traza('X2: bloque en hueso y gota en #00BB83. El acento significa otorgar; en el logo marca lo que pasa por la entrada.')),
        sub('logo.fondos', 'Sobre fondos', 'Seis fondos y la versión que le toca a cada uno',
            'Sobre fondo oscuro va la versión principal: bloque en hueso #EFFCF7 y gota en verde #00BB83, con un mínimo de 88 px de ancho (16 px si va solo el símbolo). Sobre claro, bloque en sustrato y gota #006343. Si el fondo ya es verde o es una foto, una tinta.',
            '<div class="lg-fondos">' + ''.join(_fondo(*f) for f in FONDOS) + '</div>'
            + traza('Estado honesto aplicado a la marca: la gota verde nunca se pone donde no se distingue.')),
        sub('logo.incorrectos', 'Usos incorrectos', 'Nueve cosas que no se le hacen al logo', '',
            f'<div class="lg-malos">{malos}</div>'),
        sub('logo.conjunto', 'Con el nombre del conjunto', 'El conjunto es un dato, no una segunda marca',
            'Cuando una pieza es para un conjunto, su nombre va en texto o en chip, en el orden conjunto · unidad. Nunca su logo ni sus colores.',
            casos(
                caso(f'<div class="lg-con-conjunto">{L()}<span class="chip-dato">Refugio Campestre · Casa 14</span></div>', 'Logo de Kino y el conjunto en un chip de texto, con su área de protección.'),
                caso(f'<div class="lg-duo">{L()}<span class="lg-emblema" aria-hidden="true">RC</span><span class="lg-junto">Refugio Campestre</span></div>', 'El emblema del conjunto al lado convierte a Kino en marca blanca.', False))
            + traza('F4: Kino tiene identidad propia y sirve a cualquier conjunto.')),
        sub('logo.icono', 'Favicon e ícono de app', 'El símbolo sobre sustrato, en un cuadrado redondeado',
            'El fondo de sustrato hace que el ícono se lea igual en una pestaña clara, en una oscura y en la pantalla de inicio del teléfono.',
            f'<div class="lg-iconos"><figure><div class="lg-ic" style="width:16px">{fav}</div><figcaption class="mono">16</figcaption></figure>'
            f'<figure><div class="lg-ic" style="width:32px">{fav}</div><figcaption class="mono">32</figcaption></figure>'
            f'<figure><div class="lg-ic" style="width:64px">{app}</div><figcaption class="mono">64</figcaption></figure>'
            f'<figure><div class="lg-ic" style="width:120px">{app}</div><figcaption class="mono">180 (iOS)</figcaption></figure>'
            f'<figure class="lg-telefono"><div class="lg-inicio">' + ''.join(f'<span></span>' for _ in range(3)) + f'<i>{app}</i><span></span></div><figcaption>En la pantalla de inicio</figcaption></figure></div>'
            + descargas(descarga('Favicon', 'kino-favicon.svg', fav, png=(32, 32)), descarga('Ícono de app', 'kino-icono-app.svg', app, png=(1024, 1024)),
                        descarga('Apple touch', 'kino-apple-touch.svg', _icono_app(180, 40), png=(180, 180)))),
        sub('logo.animacion', 'Animación', 'El logo aparece como se abre una entrada',
            'El bloque crece, el vano se abre y la gota baja y late una vez. Dura 1,6 s y se usa al abrir la app y al empezar una presentación. Dentro de la app el logo no se anima.',
            f'<div class="demo lg-anim" data-demo><div class="lg-lienzo">{logo("simbolo", etiqueta="Kino", clase="lg-animado")}</div>'
            '<button class="boton-tenue" type="button" data-repetir>Repetir</button></div>'
            + tabla(['Tiempo', 'Qué pasa', 'Token'], [
                ['<span class="mono">0–820 ms</span>', 'El bloque crece desde abajo', '<code>movimiento.aparecer</code>'],
                ['<span class="mono">420–1240 ms</span>', 'La gota baja por el vano', '<code>curva.crecer</code>'],
                ['<span class="mono">1240–1600 ms</span>', 'La gota late una vez', '<code>movimiento.latir</code>'],
                ['Movimiento reducido', 'Fundido de 240 ms, sin desplazamiento', '<code>duracion.corto</code>'],
              ], 'Tiempos de la animación del logo')
            + traza('X9 (crecer es aparecer) y F7: el movimiento se conserva y el modo reducido es alternativo.')),
    ])
    return seccion('logo', '03', 'Logo', 'Identidad',
                   'El bloque con arco y gota, el logotipo «KINO» y sus versiones.',
                   'Para poner la marca en cualquier superficie sin deformarla ni dejarla ilegible.',
                   'Al poner la marca en una pantalla o mandar un archivo a imprenta.', cuerpo)
