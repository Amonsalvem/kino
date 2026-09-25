#!/usr/bin/env python3
"""Lámina de la segunda vuelta de la Parada 4. Escribe kino/parada-4b.html.
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

SITIO = 'https://claude.ai/artifact/NnuVUWwUdgk34VHkj3H5Rd'
P4 = 'https://claude.ai/artifact/DBF7w1VTGPtJ9oQwdz4tXa'
FIGMA = 'https://www.figma.com/design/BO7UnDO9iE0aG6yUpNj0bc'
RAMA = 'https://github.com/amonsalvem/kino/tree/marca/fase-4'
PAGINAS = [('Léeme', '22-54'), ('Plataforma', '22-55'), ('Voz y UX writing', '22-56'), ('Logo', '22-57'), ('Color', '22-58'),
           ('Tipografía', '22-59'), ('Iconografía', '22-60'), ('Imagen', '22-61'), ('Estructura', '22-62'), ('Motion', '22-63'),
           ('Componentes', '22-64'), ('Pantallas', '22-65'), ('Aplicaciones', '22-66'), ('Registro de cambios', '22-67')]


def img(n):
    return 'data:image/jpeg;base64,' + base64.b64encode((R / 'capturas' / f'{n}.jpg').read_bytes()).decode()


PREGUNTAS = [
    ('Figma · versión 1.1.0', '¿Apruebas la librería de Figma con el auto-layout y el espaciado revisados?',
     [('Sí', 'Marco la librería como aprobada, y con la pregunta 2 aprobada republico el artefacto oficial.'),
      ('Sí, con cambios', 'Dime la página y qué ves. Los scripts de auditoría se vuelven a correr después de cada cambio.')],
     'Abre cualquier página desde la tabla de Figma más abajo. Prueba a cambiar el ancho de un marco: el contenido debe acomodarse solo.'),
    ('F4-P4 · Identidad en el sitio', '¿La identidad aplicada al sitio queda así?',
     [('A · Así', 'Aurora en la portada y en la apertura de cada sección, índigo en enlaces y rótulos, gota en el índice.'),
      ('B · Más sobria', 'Aurora solo en la portada. Las aperturas de sección van en superficie elevada, con el número en contorno.')],
     'En los dos casos el cuerpo de las secciones queda igual: el color de la marca aparece en lo que significa algo.'),
    ('Un texto para la administración', 'El detector marcó «HikCentral rechazó el registro porque falta el correo. Los Pases no deben crear personas.» porque la segunda frase suena a regla interna. ¿Lo reescribo?',
     [('A · Reescribir', '«HikCentral rechazó el registro porque falta el correo. Agréguelo en la ficha de la persona y vuelva a sincronizar.»'),
      ('B · Dejarlo', 'Queda como se aprobó en la Parada 2.')],
     'La versión A no promete nada nuevo: solo dice qué hacer con el error de hoy.'),
]

RESPUESTAS = [
    ('1', 'Todo aprobado salvo Figma y lo que se exporta de ella', 'Tokens, sitio y piezas del Pase quedan como 1.0.0 aprobada. Figma se revisó entera: ver abajo.', 'decisiones.md · Registro de cambios'),
    ('2', 'Aviso de llegada: A', 'El inventario marca el aviso «requiere el evento del lector». Pendiente nuevo: confirmar que HikCentral entregue ese evento.', 'F4-P2 · verbal.py · Gobernanza'),
    ('3', 'Llamada desde el Pase vivo: A', 'El Pase vivo vencido ya no tiene botón. Dice «Pídele uno nuevo a Carolina o pide en portería que la llamen.» Piezas regeneradas.', 'F4-P1 · pase.py · entregables'),
    ('4', 'Vencido y Usado: B', 'Usado, Vencido y Revocado llevan el ícono del estado en el chip, en código y en Figma. Las tarjetas de Pase lo heredan.', 'F4-P3 · capa-componentes.css · Estado'),
    ('5', 'Detector de IA: B', 'Cuarto ciclo: 1 señal, 0 en el microcopy. Pasa.', 'evaluaciones.md'),
    ('+', 'El sitio se lee monótono', 'La identidad aprobada, aplicada al propio sitio. Espera tu revisión.', 'F4-P4 · identidad.css'),
]

COMPARA = [
    ('inicio-1440-oscuro', 'Portada', 'Aurora (X7), el logo en su versión principal y el Pase real, que es la pieza que más se usa.'),
    ('plataforma-1440-oscuro', 'Apertura de sección', 'Aurora con el número de sección en contorno. Qué es, para qué sirve y cuándo se usa, en tres tarjetas. La gota marca la sección activa.'),
    ('plataforma-1440-claro', 'Tema claro', 'La apertura conserva la aurora en oscuro local; el cuerpo va en claro. Los rótulos de subsección, en índigo.'),
    ('color_estados-1440-oscuro', 'Chips de estado', 'Usado, Vencido y Revocado con su ícono (F4-P3). Enlaces en índigo, Lc 80 o más.'),
]

FIGMA_FILAS = [
    ('Textos de ancho fijo dentro del auto-layout', '111', '0', 'Llenan su contenedor, con ancho máximo igual al que tenían.'),
    ('Filas de tarjetas con alto desigual', '7', '0', 'La más alta abraza su contenido; las demás llenan ese alto.'),
    ('Espacios y paddings sin variable', '38', '0', 'Léeme pasa de 80 a 72 y de 1200 a 1188, como las demás páginas.'),
    ('Hijos que se salen de su contenedor', '4', '0', 'Botón de «Lista de Pases», retículas, chips del registro, texto de Elevación.'),
    ('Separación entre marcos del lienzo', '40 a 100', '72', 'La misma en todas las páginas.'),
    ('Pinturas sin variable', '0', '0', 'Se mantiene.'),
    ('Variables distintas de DTCG', '0', '0', f'{N_VAR} variables en los dos modos, más 3 sombras como estilos de efecto.'),
]


def tabla(cab, filas, clase=''):
    th = ''.join(f'<th scope="col">{c}</th>' for c in cab)
    tr = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in f) + '</tr>' for f in filas)
    return f'<div class="tabla {clase}"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


preguntas = ''.join(
    f'''<li class="preg"><div class="preg-cab"><span class="preg-n">{i}</span><div><p class="ojo">{e(t)}</p><h3>{e(q)}</h3></div></div>
<div class="opciones">{''.join(f'<div class="op"><b>{e(a)}</b><p>{e(b)}</p></div>' for a, b in ops)}</div><p class="nota">{e(n)}</p></li>'''
    for i, (t, q, ops, n) in enumerate(PREGUNTAS, 1))

respuestas = tabla(['', 'Tu respuesta', 'Qué cambió', 'Dónde'], [[f'<span class="mono">{n}</span>', f'<b>{e(r)}</b>', e(q), f'<span class="mono">{e(d)}</span>'] for n, r, q, d in RESPUESTAS])

compara = ''.join(f'''<figure class="par"><figcaption><b>{e(t)}</b><span>{e(d)}</span></figcaption>
<div class="dos-img"><div><span class="rot">Antes</span><img src="{img('antes-' + n)}" alt="{e(t)}, antes"></div><div><span class="rot ahora">Después</span><img src="{img('despues-' + n)}" alt="{e(t)}, después"></div></div></figure>''' for n, t, d in COMPARA)

movil = f'''<div class="movil"><div><span class="rot">Antes</span><img src="{img('antes-inicio-390-oscuro')}" alt="Portada en el teléfono, antes"></div><div><span class="rot ahora">Después</span><img src="{img('despues-inicio-390-oscuro')}" alt="Portada en el teléfono, después"></div>
<p class="nota">En 360 px: 0 px de desborde y 0 errores de consola en los dos temas (scripts/capturar.mjs).</p></div>'''

figma_tabla = tabla(['Qué se midió', 'Antes', 'Después', 'Cómo'], [[e(a), f'<span class="mono">{b}</span>', f'<span class="mono">{c}</span>', e(d)] for a, b, c, d in FIGMA_FILAS])
figma_links = ''.join(f'<li><a href="{FIGMA}?node-id={nid}" target="_blank" rel="noopener">{e(n)}</a></li>' for n, nid in PAGINAS)

verif = tabla(['#', 'Comprobación', 'Resultado'], [[f'<span class="mono">{c["n"]}</span>', e(c['comprobacion'].replace('«permiso», ', 'palabras vetadas, ')), chip('vigente', 'Pasa') if c['pasa'] else chip('rechazado', 'Falla')] for c in informe])

html = f'''<title>Kino · Parada 4b</title>
<meta name="description" content="Segunda vuelta de la Parada 4 del sistema de marca Kino: Figma revisado, la identidad aplicada al sitio y tres preguntas.">
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
.movil{{display:grid;grid-template-columns:repeat(2,minmax(0,15rem));gap:1rem;align-items:start}}
.movil .nota{{grid-column:1/-1}}
.paginas{{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:.5rem}}
.paginas a{{display:inline-block;padding:.35rem .75rem;border:1px solid var(--kino-borde-definido);border-radius:var(--kino-forma-radio-control);text-decoration:none;font-size:var(--kino-texto-n1)}}
.paginas a:hover{{border-color:var(--kino-texto-enlace)}}
.pasos{{margin:0;padding-inline-start:1.3rem;display:grid;gap:.5rem;color:var(--kino-texto-secundario)}}
.pasos b{{color:var(--kino-texto-primario)}}
.cierre{{border-block-start:1px solid var(--kino-borde-tenue);padding-block-start:1.5rem;color:var(--kino-texto-tenue);font-size:var(--kino-texto-n1);display:grid;gap:.4rem}}
@media (max-width:40rem){{.preg{{padding:1.1rem}}.preg-cab{{grid-template-columns:1fr}}.movil{{grid-template-columns:1fr 1fr}}}}
</style>
<style>:root{{--s-aurora:{AURORA}}}
{oscuro_local}</style>
<div class="hoja">
<header class="cabeza en-oscuro">
  <div class="barra">{logo('horizontal', etiqueta='Kino')}<span class="mono">Parada 4 · segunda vuelta · 25 sep 2026</span></div>
  <p class="ojo">Sistema de marca · versión 1.1.0 en revisión</p>
  <h1>Tu respuesta, aplicada. Faltan dos aprobaciones</h1>
  <p class="lede">Figma se revisó entera con atención al auto-layout y al espaciado, y el sitio ahora usa la identidad que describe. Tres preguntas; las dos primeras liberan el artefacto oficial.</p>
  <div class="enlaces"><a href="{SITIO}" target="_blank" rel="noopener">Abrir el sitio <small>vista previa 1.1.0</small></a><a href="{FIGMA}" target="_blank" rel="noopener">Abrir Figma <small>BO7UnDO9…</small></a><a href="{P4}" target="_blank" rel="noopener">Parada 4 <small>primera vuelta</small></a><a href="{RAMA}" target="_blank" rel="noopener">Rama <small>marca/fase-4</small></a></div>
  <p class="regla">El artefacto oficial «Kino · Sistema de marca» sigue sin republicarse. Se republica cuando respondas las preguntas 1 y 2.</p>
</header>

<section aria-labelledby="t-preg">
  <div class="sec-cab"><p class="ojo">Lo que necesito de ti</p><h2 id="t-preg">Tres preguntas</h2></div>
  <ol class="preguntas">{preguntas}</ol>
</section>

<section aria-labelledby="t-resp">
  <div class="sec-cab"><p class="ojo">Primera vuelta</p><h2 id="t-resp">Qué hice con cada respuesta</h2></div>
  {respuestas}
</section>

<section aria-labelledby="t-sitio">
  <div class="sec-cab"><p class="ojo">F4-P4 · pregunta 2</p><h2 id="t-sitio">El sitio con la identidad de Kino</h2>
  <p class="lede">Cada recurso va donde ya significa algo. La aurora es la imagen aprobada para portadas (X7). El índigo es la familia de la profundidad y los enlaces. La gota es la marca. El verde del botón queda para crear un Pase, y el arco, para el Pase.</p></div>
  <div class="comparas">{compara}</div>
  <figure class="par"><figcaption><b>En el teléfono</b><span>La portada apila el titular y el Pase.</span></figcaption>{movil}</figure>
  <p class="nota">Token nuevo para esto: <span class="mono">--kino-texto-enlace</span> (índigo a84 en oscuro, l90 en claro), medido en las cuatro superficies de los dos temas: 120 mediciones WCAG y APCA sin fallos. La capa vive aparte, en <span class="mono">sitio/identidad.css</span>.</p>
</section>

<section aria-labelledby="t-figma">
  <div class="sec-cab"><p class="ojo">Pregunta 1</p><h2 id="t-figma">Figma: auto-layout y espaciado</h2>
  <p class="lede">Auditoría automática en las 14 páginas, corrección con un script que se puede volver a correr, y revisión a ojo de cada página que cambió.</p></div>
  {figma_tabla}
  <p class="nota">También: variable <span class="mono">texto/enlace</span>; ícono de estado en Usado, Vencido y Revocado; vectores de íconos que escalan con su instancia; pantallas de teléfono con alto automático y mínimo de 780; tejido celular con su superficie y su radio; registro de cambios con 1.0.0 aprobada y 1.1.0 en revisión.</p>
  <ul class="paginas">{figma_links}</ul>
</section>

<section aria-labelledby="t-verif">
  <div class="sec-cab"><p class="ojo">Fase 5 · {PASAN} de {len(informe)}</p><h2 id="t-verif">Verificación</h2>
  <p class="lede">Detector de IA, cuarto ciclo: 1 señal, ninguna sección con más de una, 0 en el microcopy. Pasa. La señal es el titular «43 carros permitidos en la app, uno en la puerta»; queda porque la cifra es el hallazgo (observado en la inspección).</p></div>
  {verif}
</section>

<section aria-labelledby="t-sigue">
  <div class="sec-cab"><p class="ojo">Al aprobar</p><h2 id="t-sigue">Lo que sigue</h2></div>
  <ol class="pasos">
    <li><b>Aplicar tus respuestas</b> a las preguntas 2 y 3, reconstruir y volver a verificar.</li>
    <li><b>Republicar el artefacto oficial</b> leyéndolo primero, con la función de descarga del visor para que el centro de descargas funcione.</li>
    <li><b>Integrar la rama</b> <span class="mono">marca/fase-4</span> a <span class="mono">main</span>: lo haces tú.</li>
  </ol>
</section>

<footer class="cierre">
  <p>Fuentes: <span class="mono">decisiones.md</span> (F4-P1 a F4-P4), <span class="mono">verificacion/informe.md</span>, <span class="mono">verificacion/evaluaciones.md</span>, <span class="mono">figma/LEEME.md</span>, <span class="mono">figma/variables-figma.json</span>.</p>
  <p>Generada con <span class="mono">branding/sistema/v3/parada4b/construir.py</span>.</p>
</footer>
</div>
'''
(RAIZ / 'parada-4b.html').write_text(html, encoding='utf8')
vis = re.sub(r'<(style|script|svg)[^>]*>.*?</\1>', ' ', html, flags=re.S)
vis = re.sub(r'<title>.*?</title>|<meta[^>]*>', ' ', vis)
vis = re.sub(r'<(li|p|h\d|td|th|b|figcaption|span|a|div)[^>]*>', '\n', vis)
vis = re.sub(r'<[^>]+>', '', vis)
(R / 'texto-visible.md').write_text('\n'.join(l.strip() for l in vis.splitlines() if l.strip()), encoding='utf8')
print('ok parada-4b.html', len(html.encode()) // 1024, 'KB')
