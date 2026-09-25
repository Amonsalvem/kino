#!/usr/bin/env python3
"""Lámina de la versión 1.2.0 (tercera vuelta de la Parada 4). Escribe kino/parada-4c.html.
Uso: node capturar.mjs <antes.html> <despues.html> && python3 construir.py"""
import base64, json, pathlib, re, sys
R = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(R / '../sitio'))
from deptos.comun import logo, chip, e  # noqa: E402
from deptos.d07_imagen import AURORA  # noqa: E402

RAIZ = R / '../../../..'
informe = json.loads((R / '../verificacion/informe.json').read_text(encoding='utf8'))
figma = json.loads((R / '../figma/variables-figma.json').read_text(encoding='utf8'))
brand = re.sub(r"^@import[^;]+;\s*$", '', (R / '../../kino-brand.css').read_text(encoding='utf8'), flags=re.M)
_b = RAIZ / 'gorr-brand-system/clientes/kino/build'
# La cabecera lleva aurora: tema oscuro local, también cuando el visor está en claro.
oscuro_local = re.sub(r'^[^{]+\{', '.en-oscuro{', (_b / 'tema-oscuro.css').read_text(encoding='utf8'), count=1)
comp = re.sub(r"^@import[^;]+;\s*$", '', (R / '../../capa-componentes.css').read_text(encoding='utf8'), flags=re.M)
PASAN = sum(1 for c in informe if c['pasa'])
N_VAR = len({v['css'] for v in figma['variables']})

SITIO = 'https://claude.ai/artifact/W5U4Nw4AeZMpM7QZ4gsXcH'
OFICIAL = 'https://claude.ai/artifact/K8R2PRduS6SHBKYU31Bo6L'
P4B = 'https://claude.ai/artifact/Bn6AaiChNchG5dhx7BjtQ1'
FIGMA = 'https://www.figma.com/design/BO7UnDO9iE0aG6yUpNj0bc'
RAMA = 'https://github.com/amonsalvem/kino/tree/marca/fase-4'
NODOS = [('Pantallas', '22-65'), ('Lista de Pases', '98-95'), ('Crear Pase', '98-160'), ('Detalle de Pase', '99-143'), ('Acceso por código', '99-187'),
         ('Límites', '99-217'), ('Pantallas 1.1.0', '98-94'), ('Pase en lista (componente)', '96-100'), ('Registro de cambios', '22-67')]


def img(n):
    return 'data:image/jpeg;base64,' + base64.b64encode((R / 'capturas' / f'{n}.jpg').read_bytes()).decode()


PREGUNTAS = [
    ('F4-P5 · Pantallas', '¿Las pantallas quedan con la jerarquía del Pase?',
     [('A · Así', 'Como se ven abajo. La lista agrupa los Pases en «Ahora» y «Próximos».'),
      ('B · Con pestañas', 'La misma jerarquía, pero la lista conserva las pestañas «Activos / Anteriores» de la 1.1.0.')],
     'En las dos, «Entrar» pasa al botón secundario: el verde de acción queda solo para crear un Pase (X4).'),
    ('F4-P6 · El mensaje de HikCentral', '¿Qué hago con la fila del error de HikCentral en el inventario de textos?',
     [('A · Mensaje genérico', '«HikCentral no aceptó el alta de Carolina Ruiz. Hasta que se corrija, el lector no la reconoce.» Sirve para cualquier alta que falle, por la causa que sea.'),
      ('B · Quitar la fila', 'Kino no debería producir el error del correo, así que la fila sale del inventario.')],
     'La explicación de la fila está justo debajo.'),
]

RESPUESTAS = [
    ('1', 'Apruebo Figma', 'La 1.1.0 queda aprobada y el artefacto oficial se republicó con ella, leyéndolo primero y con su misma URL.', 'decisiones.md · Registro de cambios'),
    ('1', 'Las pantallas cargan mucho', 'Pantallas nuevas en el sitio y en Figma con la jerarquía del Pase. Las de la 1.1.0 no se borraron.', 'F4-P5 · d10_producto.py · Pantallas'),
    ('2', 'Identidad en el sitio: A', 'Queda como estaba en la vista previa.', 'F4-P4 · identidad.css'),
    ('3', 'No se entiende la pregunta de HikCentral', 'Explicación abajo y pregunta nueva con dos opciones.', 'F4-P6 · verbal.py'),
    ('+', 'El título de la tarjeta no se lee', 'El titular de la lámina anterior heredaba el color del tema claro. Corregido y republicado.', 'parada-4b.html'),
]

NIVELES = [
    ('1 · Manda', 'Un dato por pantalla: el nombre, el código o el límite.', 'Archivo 800 ancho, lo más grande de la pantalla.'),
    ('2 · Vigencia', 'Cuándo vale el Pase.', 'Monoespaciada en el color de su estado. En Crear Pase, en texto primario porque todavía no hay estado.'),
    ('3 · Rótulo', 'Qué es cada valor: Placa, Código, Vigencia.', 'Mono pequeño en mayúsculas, encima de su valor.'),
    ('4 · Grupo', 'Lo que se decide junto.', 'Un bloque en superficie elevada con radio 14. Entre bloques hay más aire que dentro de ellos.'),
    ('5 · Acción', 'Una acción principal, abajo.', 'Verde solo si crea un Pase. Revocar va en texto.'),
]

PANTALLAS = [
    ('lista', 'Lista de Pases · inicio', 'Manda el nombre de cada persona. La aurora sube a la cabecera porque esta es la pantalla de inicio (X7).',
     'Las pestañas y la palabra «Visita» repetida debajo de cada nombre.', 'Ahora y Próximos. El tipo de Pase pasa a rótulo.'),
    ('crear', 'Crear Pase', 'Manda la pregunta. La franja se lee en una línea.',
     'Cuatro cajas iguales, una debajo de otra.', 'Persona (nombre y WhatsApp) y vigencia (día, franja y placa).'),
    ('detalle', 'Detalle de Pase', 'Manda el nombre. Placa y código, en grande.',
     '«Otorgó Carolina Ruiz · Casa 14»: es la app de Carolina.', '«Lo que pasó» como línea de tiempo: lo que el lector confirmó lleva punto verde.'),
    ('codigo', 'Acceso por código', 'Mandan las seis cifras. El número va en mono, como dato.',
     'El bloque rojo del error y el verde en «Entrar».', 'El error, en una línea con ícono y en el color de Rechazado.'),
]

VERIF = [
    ('Contraste', '132 mediciones WCAG y APCA, 0 fallos. 6 pares nuevos: la vigencia de cada estado sobre la tarjeta, Revocar y el error de código.'),
    ('Rótulos pequeños', 'Pasan de texto tenue a secundario. El tenue solo está medido para 24 px o más (Lc 65 en oscuro).'),
    ('Voz', '0 hallazgos en el texto visible del sitio y en el LEEME de Figma.'),
    ('Fase 5', f'{PASAN} de {len(informe)} comprobaciones pasan.'),
    ('Figma', 'Pantallas y Componentes: 0 marcos sin auto-layout, 0 espacios sin variable, 0 desbordes, 0 filas desiguales, 0 solapes y 0 pinturas sin variable en las pantallas nuevas.'),
]


def tabla(cab, filas, clase=''):
    th = ''.join(f'<th scope="col">{c}</th>' for c in cab)
    tr = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in f) + '</tr>' for f in filas)
    return f'<div class="tabla {clase}"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


preguntas = ''.join(
    f"""<li class="preg"><div class="preg-cab"><span class="preg-n">{i}</span><div><p class="ojo">{e(t)}</p><h3>{e(q)}</h3></div></div>
<div class="opciones">{''.join(f'<div class="op"><b>{e(a)}</b><p>{e(b)}</p></div>' for a, b in ops)}</div><p class="nota">{e(n)}</p></li>"""
    for i, (t, q, ops, n) in enumerate(PREGUNTAS, 1))

respuestas = tabla(['', 'Tu respuesta', 'Qué hice', 'Dónde'], [[f'<span class="mono">{n}</span>', f'<b>{e(r)}</b>', e(q), f'<span class="mono">{e(d)}</span>'] for n, r, q, d in RESPUESTAS])
niveles = tabla(['Nivel', 'Qué lleva', 'Cómo se ve'], [[f'<b>{e(a)}</b>', e(b), e(c)] for a, b, c in NIVELES])
pantallas = ''.join(f"""<figure class="par"><figcaption><b>{e(t)}</b><span>{e(m)}</span></figcaption>
<div class="tel"><div><span class="rot">1.1.0</span><img src="{img('antes-' + n)}" alt="{e(t)}, versión 1.1.0"></div><div><span class="rot ahora">1.2.0</span><img src="{img('despues-' + n)}" alt="{e(t)}, versión 1.2.0"></div>
<dl class="cambios"><div><dt>Sale</dt><dd>{e(q)}</dd></div><div><dt>Se agrupa</dt><dd>{e(g)}</dd></div></dl></div></figure>""" for n, t, m, q, g in PANTALLAS)
limites = f"""<figure class="par"><figcaption><b>Límites de la administración</b><span>Cada límite en su tarjeta con el valor en grande. El resumen de la semana, en cifras; las rechazadas, en su color.</span></figcaption>
<div class="dos-img"><div><span class="rot">1.1.0</span><img src="{img('antes-limites')}" alt="Límites, versión 1.1.0"></div><div><span class="rot ahora">1.2.0</span><img src="{img('despues-limites')}" alt="Límites, versión 1.2.0"></div></div></figure>"""
verif = tabla(['Qué', 'Resultado'], [[f'<b>{e(a)}</b>', e(b)] for a, b in VERIF])
figma_links = ''.join(f'<li><a href="{FIGMA}?node-id={nid}" target="_blank" rel="noopener">{e(n)}</a></li>' for n, nid in NODOS)
hik = tabla(['', 'Lo que dice la evidencia'], [
    ['<b>De dónde sale la fila</b>', 'El inventario de textos traduce cada mensaje que hoy muestra el sistema. Este es el error que ve el super administrador cuando HikCentral rechaza un alta: «Incorrect request parameter. [email parameter error]», 711 veces (observado, <span class="mono">inspeccion/diagnostico-inspeccion.md</span>).'],
    ['<b>A quién afecta</b>', 'A cualquier persona que el sistema actual da de alta en HikCentral, residentes incluidos. En Refugio Campestre hay 0 de 312 usuarios sincronizados (observado).'],
    ['<b>Qué cambia con Kino</b>', 'Como dices, la visita entra con un Pase y no se da de alta como persona. El residente entra con código por WhatsApp, así que el correo deja de ser obligatorio (inferido de esa decisión). Con las dos cosas, el error del correo desaparece para todos.'],
    ['<b>Qué queda</b>', 'Un residente o un colaborador sí se dan de alta en HikCentral, y un alta puede fallar por otra causa: Refugio tiene el hardware y la integración caída. Para ese caso la administración necesita un mensaje que diga a quién afecta y qué pasa en la puerta.'],
])

html = f'''<title>Kino · Parada 4c</title>
<meta name="description" content="Versión 1.2.0 del sistema de marca Kino: pantallas con la jerarquía del Pase y el mensaje de alta fallida en HikCentral, con dos preguntas.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&family=JetBrains+Mono:wght@400;500;700&display=swap">
<script>
(function(){{var r=document.documentElement;function s(){{var t=r.getAttribute('data-theme');if(t==='dark')r.setAttribute('data-tema','oscuro');else if(t==='light')r.setAttribute('data-tema','claro');else r.removeAttribute('data-tema');}}
s();try{{new MutationObserver(s).observe(r,{{attributes:true,attributeFilter:['data-theme']}});}}catch(_){{}}}})();
</script>
<style>{brand}
{comp}
:root{{color-scheme:dark}}
:root[data-tema="claro"]{{color-scheme:light}}
@media (prefers-color-scheme: light){{:root:not([data-tema="oscuro"]){{color-scheme:light}}}}
*,*::before,*::after{{box-sizing:border-box}}
body{{margin:0;background:var(--kino-superficie-base);color:var(--kino-texto-primario);font-family:var(--kino-fuente-texto);font-size:var(--kino-texto-0);line-height:1.55;padding-inline:max(16px,4vw);padding-block:0 4rem}}
.hoja{{max-inline-size:72rem;margin-inline:auto;display:grid;gap:4.5rem}}
.mono{{font-family:var(--kino-fuente-dato);font-feature-settings:"zero" 1;font-variant-numeric:tabular-nums}}
a{{color:var(--kino-texto-enlace);text-underline-offset:.2em}}
a:focus-visible{{outline:var(--kino-linea-foco) solid var(--kino-borde-foco);outline-offset:3px}}
h1,h2,h3{{margin:0;text-wrap:balance;font-family:var(--kino-fuente-display)}}
h1{{font-size:var(--kino-texto-5);font-stretch:112%;font-weight:800;line-height:1.02;letter-spacing:-.02em;max-inline-size:20ch}}
h2{{font-size:var(--kino-texto-3);font-stretch:112%;font-weight:750;line-height:1.1}}
h3{{font-size:var(--kino-texto-1);font-weight:700;line-height:1.25}}
p{{margin:0;max-inline-size:66ch}}
.ojo{{font-family:var(--kino-fuente-dato);font-size:var(--kino-texto-n1);letter-spacing:.08em;text-transform:uppercase;color:var(--kino-texto-enlace)}}
.lede{{color:var(--kino-texto-secundario);font-size:var(--kino-texto-1);line-height:1.45}}
.cabeza{{color:var(--kino-texto-primario);display:grid;gap:1.4rem;margin-top:2rem;padding:clamp(1.5rem,4vw,3.5rem);border-radius:var(--kino-forma-radio-tarjeta);background:var(--s-aurora);box-shadow:var(--kino-relieve-membrana)}}
.cabeza .ojo{{color:var(--kino-texto-secundario)}}
.barra{{display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap}}
.barra svg{{block-size:2rem;inline-size:auto}}
.barra .mono{{color:var(--kino-texto-secundario);font-size:var(--kino-texto-n1)}}
.enlaces{{display:flex;flex-wrap:wrap;gap:.75rem}}
.enlaces a{{display:inline-flex;align-items:center;gap:.5rem;padding:.55rem 1rem;border:1px solid var(--kino-borde-definido);border-radius:var(--kino-forma-radio-control);color:var(--kino-texto-primario);text-decoration:none;font-weight:600;background:color-mix(in oklch,var(--kino-superficie-abismo) 60%,transparent)}}
.enlaces a:hover{{border-color:var(--kino-borde-foco)}}
.enlaces a small{{font-family:var(--kino-fuente-dato);color:var(--kino-texto-secundario);font-weight:400}}
.regla{{padding:1rem 1.25rem;border:1px dashed var(--kino-borde-definido);border-radius:var(--kino-forma-radio-control);color:var(--kino-texto-secundario);max-inline-size:none;background:color-mix(in oklch,var(--kino-superficie-abismo) 60%,transparent)}}
section{{display:grid;gap:1.5rem}}
.sec-cab{{display:grid;gap:.6rem;padding-top:1.25rem;background:linear-gradient(var(--kino-texto-enlace),var(--kino-texto-enlace)) top left / 3rem 2px no-repeat}}
.preguntas{{list-style:none;margin:0;padding:0;display:grid;gap:1.25rem}}
.preg{{border:1px solid var(--kino-borde-tenue);border-radius:var(--kino-forma-radio-tarjeta);padding:1.5rem;display:grid;gap:1.1rem;background:var(--kino-superficie-elevada);box-shadow:var(--kino-relieve-membrana)}}
.preg-cab{{display:grid;grid-template-columns:auto 1fr;gap:1rem;align-items:start}}
.preg-n{{font-family:var(--kino-fuente-dato);font-weight:700;font-size:var(--kino-texto-2);line-height:1;color:var(--kino-marca-gota);min-inline-size:1.5ch}}
.preg h3{{margin-top:.35rem}}
.opciones{{display:grid;grid-template-columns:repeat(auto-fit,minmax(16rem,1fr));gap:.75rem}}
.op{{border:1px solid var(--kino-borde-definido);border-radius:var(--kino-forma-radio-control);padding:1rem;display:grid;gap:.4rem;align-content:start;background:var(--kino-superficie-base)}}
.op p{{color:var(--kino-texto-secundario);font-size:var(--kino-texto-n1)}}
.nota{{color:var(--kino-texto-tenue);font-size:var(--kino-texto-n1)}}
.tabla{{overflow-x:auto;border:1px solid var(--kino-borde-tenue);border-radius:var(--kino-forma-radio-tarjeta)}}
table{{border-collapse:collapse;inline-size:100%;min-inline-size:40rem;font-size:var(--kino-texto-n1)}}
th{{text-align:start;font-family:var(--kino-fuente-dato);font-weight:500;letter-spacing:.06em;text-transform:uppercase;color:var(--kino-texto-tenue);background:var(--kino-superficie-abismo);padding:.7rem 1rem}}
td{{padding:.75rem 1rem;border-block-start:1px solid var(--kino-borde-tenue);vertical-align:top;color:var(--kino-texto-secundario)}}
td b{{color:var(--kino-texto-primario)}}
td .kino-estado{{white-space:nowrap}}
.par{{margin:0;display:grid;gap:.8rem}}
.par figcaption{{display:grid;gap:.2rem}}
.par figcaption span{{color:var(--kino-texto-secundario);font-size:var(--kino-texto-n1)}}
.dos-img{{display:grid;grid-template-columns:repeat(auto-fit,minmax(18rem,1fr));gap:1rem}}
.dos-img>div,.movil>div{{position:relative;border:1px solid var(--kino-borde-tenue);border-radius:var(--kino-forma-radio-control);overflow:hidden;background:var(--kino-superficie-abismo)}}
.dos-img img,.movil img{{display:block;inline-size:100%;block-size:auto}}
.rot{{position:absolute;inset-block-start:.6rem;inset-inline-start:.6rem;font-family:var(--kino-fuente-dato);font-size:var(--kino-texto-n1);letter-spacing:.08em;text-transform:uppercase;padding:.2rem .55rem;border-radius:var(--kino-forma-radio-chip);background:var(--kino-superficie-abismo);color:var(--kino-texto-secundario);border:1px solid var(--kino-borde-definido)}}
.rot.ahora{{color:var(--kino-texto-enlace);border-color:var(--kino-texto-enlace)}}
.comparas{{display:grid;gap:2.5rem}}
.tel{{display:grid;grid-template-columns:repeat(2,minmax(0,15rem)) minmax(0,1fr);gap:1rem;align-items:start}}
.tel>div{{position:relative;border:1px solid var(--kino-borde-tenue);border-radius:var(--kino-forma-radio-control);overflow:hidden;background:var(--kino-superficie-abismo)}}
.tel img{{display:block;inline-size:100%;block-size:auto}}
.cambios{{margin:0;display:grid;gap:1rem;align-content:start}}
.cambios dt{{font-family:var(--kino-fuente-dato);font-size:var(--kino-texto-n1);letter-spacing:.08em;text-transform:uppercase;color:var(--kino-texto-secundario)}}
.cambios dd{{margin:.25rem 0 0}}
.movil .nota{{grid-column:1/-1}}
.paginas{{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:.5rem}}
.paginas a{{display:inline-block;padding:.35rem .75rem;border:1px solid var(--kino-borde-definido);border-radius:var(--kino-forma-radio-control);text-decoration:none;font-size:var(--kino-texto-n1)}}
.paginas a:hover{{border-color:var(--kino-texto-enlace)}}
.pasos{{margin:0;padding-inline-start:1.3rem;display:grid;gap:.5rem;color:var(--kino-texto-secundario)}}
.pasos b{{color:var(--kino-texto-primario)}}
.cierre{{border-block-start:1px solid var(--kino-borde-tenue);padding-block-start:1.5rem;color:var(--kino-texto-tenue);font-size:var(--kino-texto-n1);display:grid;gap:.4rem}}
@media (max-width:52rem){{.tel{{grid-template-columns:1fr 1fr}}.cambios{{grid-column:1/-1}}}}
@media (max-width:40rem){{.preg{{padding:1.1rem}}.preg-cab{{grid-template-columns:1fr}}}}
</style>
<style>:root{{--s-aurora:{AURORA}}}
{oscuro_local}</style>
<div class="hoja">
<header class="cabeza en-oscuro">
  <div class="barra">{logo('horizontal', etiqueta='Kino')}<span class="mono">Parada 4 · tercera vuelta · 25 sep 2026</span></div>
  <p class="ojo">Sistema de marca · versión 1.2.0 en revisión</p>
  <h1>Las pantallas, con la jerarquía del Pase</h1>
  <p class="lede">La 1.1.0 quedó aprobada y el artefacto oficial ya la tiene. Esta vuelta trae las cinco pantallas rehechas y la explicación de la fila de HikCentral. Dos preguntas.</p>
  <div class="enlaces"><a href="{SITIO}" target="_blank" rel="noopener">Abrir el sitio <small>vista previa 1.2.0</small></a><a href="{FIGMA}?node-id=22-65" target="_blank" rel="noopener">Abrir Figma <small>página Pantallas</small></a><a href="{OFICIAL}" target="_blank" rel="noopener">Artefacto oficial <small>1.1.0</small></a><a href="{RAMA}" target="_blank" rel="noopener">Rama <small>marca/fase-4</small></a></div>
  <p class="regla">El oficial se republica otra vez cuando apruebes la 1.2.0 (pregunta 1).</p>
</header>

<section aria-labelledby="t-preg">
  <div class="sec-cab"><p class="ojo">Lo que necesito de ti</p><h2 id="t-preg">Dos preguntas</h2></div>
  <ol class="preguntas">{preguntas}</ol>
</section>

<section aria-labelledby="t-resp">
  <div class="sec-cab"><p class="ojo">Segunda vuelta</p><h2 id="t-resp">Qué hice con cada respuesta</h2></div>
  {respuestas}
</section>

<section aria-labelledby="t-jer">
  <div class="sec-cab"><p class="ojo">F4-P5 · pregunta 1</p><h2 id="t-jer">Cinco niveles, iguales en todas las pantallas</h2>
  <p class="lede">Salen de la imagen del Pase y del Pase vivo, que es lo que dijiste que funcionaba: el nombre manda, la vigencia se lee en su color y cada dato tiene su rótulo encima.</p></div>
  {niveles}
</section>

<section aria-labelledby="t-pant">
  <div class="sec-cab"><p class="ojo">Antes y después</p><h2 id="t-pant">Pantalla por pantalla</h2>
  <p class="lede">A la izquierda, la 1.1.0 aprobada; a la derecha, la propuesta. Mismos datos de ejemplo.</p></div>
  <div class="comparas">{pantallas}{limites}</div>
  <p class="nota">En Figma, lo mismo con auto-layout y variables, más el componente nuevo «Pase en lista» con sus cuatro estados. Las pantallas de la 1.1.0 quedan en su propia sección de la página.</p>
  <ul class="paginas">{figma_links}</ul>
</section>

<section aria-labelledby="t-hik">
  <div class="sec-cab"><p class="ojo">F4-P6 · pregunta 2</p><h2 id="t-hik">La fila de HikCentral, explicada</h2>
  <p class="lede">Tienes razón en lo principal: con el Pase, a la visita no se le pide correo ni se registra. La fila no hablaba de la visita.</p></div>
  {hik}
</section>

<section aria-labelledby="t-verif">
  <div class="sec-cab"><p class="ojo">Verificación</p><h2 id="t-verif">Lo que se midió</h2></div>
  {verif}
</section>

<section aria-labelledby="t-sigue">
  <div class="sec-cab"><p class="ojo">Al aprobar</p><h2 id="t-sigue">Lo que sigue</h2></div>
  <ol class="pasos">
    <li><b>Aplicar tus respuestas</b> y volver a verificar.</li>
    <li><b>Republicar el artefacto oficial</b> con la 1.2.0, leyéndolo primero y con su misma URL.</li>
    <li><b>Integrar la rama</b> <span class="mono">marca/fase-4</span> a <span class="mono">main</span>: lo haces tú.</li>
  </ol>
</section>

<footer class="cierre">
  <p>Fuentes: <span class="mono">decisiones.md</span> (F4-P5 y F4-P6), <span class="mono">inspeccion/diagnostico-inspeccion.md</span>, <span class="mono">verificacion/informe.md</span>, <span class="mono">figma/LEEME.md</span>.</p>
  <p>Generada con <span class="mono">branding/sistema/v3/parada4c/construir.py</span>. Lámina anterior: <a href="{P4B}" target="_blank" rel="noopener">Parada 4b</a>.</p>
</footer>
</div>
'''
(RAIZ / 'parada-4c.html').write_text(html, encoding='utf8')
vis = re.sub(r'<(style|script|svg)[^>]*>.*?</\1>', ' ', html, flags=re.S)
vis = re.sub(r'<title>.*?</title>|<meta[^>]*>', ' ', vis)
vis = re.sub(r'<(li|p|h\d|td|th|b|figcaption|span|a|div)[^>]*>', '\n', vis)
vis = re.sub(r'<[^>]+>', '', vis)
(R / 'texto-visible.md').write_text('\n'.join(l.strip() for l in vis.splitlines() if l.strip()), encoding='utf8')
print('ok parada-4c.html', len(html.encode()) // 1024, 'KB')
