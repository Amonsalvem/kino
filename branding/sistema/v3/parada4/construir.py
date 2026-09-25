#!/usr/bin/env python3
"""Lámina de la Parada 4 (sistema completo). Escribe kino/parada-4.html.
Lee los datos de las fuentes: informe de la Fase 5, pendientes de Gobernanza, tokens resueltos y decisiones.md.
Uso: node miniaturas.mjs && python3 construir.py"""
import base64, json, pathlib, re, sys
R = pathlib.Path(__file__).resolve().parent
S = R / '../sitio'
sys.path.insert(0, str(S))
from deptos.comun import logo, chip, e  # noqa: E402
from deptos import d12_gobernanza as gob, d09_motion as mot, d06_iconografia as ico  # noqa: E402

RAIZ = R / '../../../..'
K = RAIZ / 'gorr-brand-system/clientes/kino'
resu = json.loads((K / 'build/tokens.resuelto.json').read_text(encoding='utf8'))
informe = json.loads((R / '../verificacion/informe.json').read_text(encoding='utf8'))
figma = json.loads((R / '../figma/variables-figma.json').read_text(encoding='utf8'))
pares = json.loads((K / 'pares.json').read_text(encoding='utf8'))
dec = (RAIZ / 'decisiones.md').read_text(encoding='utf8')

N_PRIM, N_SEM = len(resu['primitivos']), len(resu['temas']['oscuro'])
N_VAR = len({v['css'] for v in figma['variables']})
N_EF = len({x['css'] for x in figma.get('estilosDeEfecto', [])})
N_P = len(re.findall(r'^### P\d+ ', dec, re.M))
N_V = len(re.findall(r'^### V\d ', dec, re.M))
N_X = len(re.findall(r'^\| X\d+ \|', dec, re.M)) + ('### X11' in dec)
PASAN = sum(1 for c in informe if c['pasa'])

brand = (R / '../../kino-brand.css').read_text(encoding='utf8')
brand = re.sub(r"^@import[^;]+;\s*$", '', brand, flags=re.M)
comp = re.sub(r"^@import[^;]+;\s*$", '', (R / '../../capa-componentes.css').read_text(encoding='utf8'), flags=re.M)


def img(n):
    return 'data:image/jpeg;base64,' + base64.b64encode((R / 'miniaturas' / f'{n}.jpg').read_bytes()).decode()


SITIO = 'https://claude.ai/artifact/AJey2DjrB4K8oo92fn6pfg'
FIGMA = 'https://www.figma.com/design/BO7UnDO9iE0aG6yUpNj0bc'
RAMA = 'https://github.com/amonsalvem/kino/tree/marca/fase-4'

# ── Preguntas, ordenadas por impacto ──
PREGUNTAS = [
    ('Versión 1.0.0', '¿Apruebas la versión 1.0.0 como está: tokens, sitio, piezas del Pase y librería de Figma?',
     [('Sí', 'Marco 1.0.0 como vigente, quito la etiqueta «Propuesta» del sitio y de Figma, y republico el artefacto oficial «Kino · Sistema de marca» con su enlace de siempre.'),
      ('Sí, con cambios', 'Dime cuáles. Los hago, vuelvo a correr la verificación y te muestro solo lo que cambió.')],
     'Es la única respuesta que libera el artefacto oficial. Las otras cuatro se pueden contestar después sin frenar esta.'),
    ('F4-P2 · Aviso de llegada', 'El inventario de textos promete avisar al residente cuando alguien entra, pero el producto no tiene confirmado ese aviso. ¿Qué hacemos con esa promesa?',
     [('A · Requisito de producto (recomendada)', 'Los textos se quedan, marcados «requiere el evento del lector». Ninguno sale a producción antes de que el aviso exista. Responde al núcleo del diagnóstico: el residente otorga el Pase pero hoy no sabe si la persona entró.'),
      ('B · Quitar la promesa', 'El campo dice «Tu WhatsApp sirve para entrar a Kino.» y el estado «Aviso de llegada» sale del inventario hasta que el producto lo tenga.')],
     'Por verificar en los dos casos: que HikCentral le entregue a Kino el evento de paso del lector.'),
    ('F4-P1 · Llamada desde el Pase vivo', 'El Pase vivo vencido, que ve la visita, tiene el botón «Llamar al residente». X11 aprobó la llamada desde portería. ¿La visita también llama?',
     [('A · Quitar el botón (recomendada)', 'El aviso dice «Pídele uno nuevo a Carolina o pide en portería que la llamen.» La llamada queda solo en portería. No expone el número del residente ni promete una función que no existe.'),
      ('B · Llamada enmascarada', 'Kino conecta a la visita con el residente sin mostrar el número. Es una función nueva: proveedor de telefonía por elegir, costo por llamada y un registro de cada llamada.')],
     'Lo construido hoy es el botón. Si eliges A, cambian dos funciones y se rehace una imagen.'),
    ('Vencido y Usado', 'El lector frío notó que Vencido y Usado solo se distinguen por el tono del texto y la palabra. ¿Basta?',
     [('A · Basta con la palabra', 'Todo estado ya lleva palabra (regla 2). Los dos van en sustrato porque ninguno pide acción.'),
      ('B · Ícono en el chip', 'El punto del chip se cambia por el ícono del estado (Usado, Vencido, Revocado). Los íconos ya existen en la librería.')],
     'No cambia el color ni los tokens, solo el componente Estado.'),
    ('Detector de IA', 'El detector no pasó: 8 señales en el tercer ciclo. Las corregí, pero el límite de 3 ciclos no me deja volver a medir. ¿Cómo lo cerramos?',
     [('A · Aceptar el ciclo 3', 'Se aprueba con la última medición y las correcciones hechas, y se reporta así.'),
      ('B · Un cuarto ciclo', 'Autorizas una medición más antes de aprobar. Si quedan señales, las corrijo y te muestro el resultado.')],
     'El lector frío sí pasó: 8 de 8 con cita y claridad media de 4,25.'),
]

DEPTOS = [
    ('01', 'Plataforma', 'Aprobada', 'Parada 1: posicionamiento, promesa, personalidad, valores, nombres y manifiesto.'),
    ('02', 'Verbal', 'Aprobada', 'Parada 2: tono, vocabulario, 46 textos en límite, plantillas de WhatsApp.'),
    ('03', 'Logo', 'En revisión', 'Tres versiones con bloque hueso y gota verde. Los SVG se reconstruyeron desde PNG (98 % de coincidencia).'),
    ('04', 'Color', 'En revisión', f'Siete familias, nueve estados, {len(pares)} pares medidos en los dos temas, simulación de daltonismo, CMYK.'),
    ('05', 'Tipografía', 'En revisión', 'Archivo al 112 % en titulares, JetBrains Mono con cero barrado, escala de 8 pasos.'),
    ('06', 'Iconografía', 'En revisión', f'{len(ico.ICONOS)} íconos en retícula de 24, trazo 1,7 con puntas redondas.'),
    ('07', 'Imagen', 'En revisión', 'Aurora en pantalla, tejido celular solo en impresos grandes, sin fotos de personas.'),
    ('08', 'Estructura', 'En revisión', 'Cuatro retículas, diez pasos de espacio, radio 14 y arco solo en el Pase.'),
    ('09', 'Motion', 'En revisión', f'{len(mot.CATALOGO)} animaciones con su token, el motor en vivo y el modo de movimiento reducido.'),
    ('10', 'Producto', 'En revisión', 'Componentes con todos sus estados, cinco pantallas, criterios WCAG.'),
    ('11', 'Aplicaciones', 'En revisión', 'Quince piezas, del Pase a la papelería. Las físicas están en 2D.'),
    ('12', 'Gobernanza', 'En revisión', f'Quién decide, registro de decisiones, lista de revisión, {len(gob.PEND)} pendientes y descargas.'),
]

PIEZAS = [
    ('imagen-visita', 'Imagen del WhatsApp', '1080 × 1350. Llega en la conversación sin abrir nada.'),
    ('pase-vivo', 'Pase vivo', 'La página del enlace. Dice si el Pase sigue sirviendo.'),
    ('pase-vivo-vencido', 'Pase vivo vencido', 'Con el botón de la pregunta 3.'),
    ('pdf', 'PDF', 'Carta, en claro, una página. Descarga opcional.'),
    ('porteria', 'Portería', 'Rechazo por Pase vencido y la llamada de X11.'),
    ('senal-entrada', 'Señal de la entrada', '60 × 40 cm.'),
]

OBS_LECTOR = [
    ('Vencido y Usado se distinguen solo por el tono y la palabra.', 'Pregunta 4.'),
    ('El Pase se nombra antes de definirse en el recorrido «Conocer Kino».', 'Se corrige al aprobar: una línea de definición en la entrada del recorrido.'),
    ('Cuatro verdes: se aclaran en Color, no donde aparecen primero.', 'Se corrige al aprobar: nota en la primera aparición.'),
    ('La versión 1.0.0 figura «Propuesta».', 'Se resuelve con la pregunta 1.'),
    ('El centro de descargas está al final de Gobernanza.', 'Se corrige al aprobar: enlace desde el inicio del sitio.'),
]


def tabla(cab, filas, clase=''):
    th = ''.join(f'<th scope="col">{c}</th>' for c in cab)
    tr = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in f) + '</tr>' for f in filas)
    return f'<div class="tabla {clase}"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


est_chip = lambda s: chip({'Aprobada': 'vigente', 'En revisión': 'previsto'}.get(s, 'sin-confirmar'), s)
res_chip = lambda ok: chip('vigente', 'Pasa') if ok else chip('rechazado', 'Falla')

preguntas = ''.join(
    f'''<li class="preg" id="p{i}"><div class="preg-cab"><span class="preg-n">{i}</span><div><p class="ojo">{e(t)}</p><h3>{e(q)}</h3></div></div>
<div class="opciones">{''.join(f'<div class="op"><b>{e(a)}</b><p>{e(b)}</p></div>' for a, b in ops)}</div><p class="nota">{e(n)}</p></li>'''
    for i, (t, q, ops, n) in enumerate(PREGUNTAS, 1))

verif = tabla(['#', 'Comprobación', 'Resultado', 'Detalle'],
              [[f'<span class="mono">{c["n"]}</span>', e(c['comprobacion'].replace('«permiso», ', 'palabras vetadas, ')), res_chip(c['pasa']), e(c['detalle'])] for c in informe], 'verif')

deptos = tabla(['', 'Departamento', 'Estado', 'Qué tiene'],
               [[f'<span class="mono">{n}</span>', f'<b>{d}</b>', est_chip(s), e(t)] for n, d, s, t in DEPTOS])

piezas = ''.join(f'<figure class="pieza {"ancha" if n in ("porteria", "senal-entrada") else ""}"><div class="marco"><img src="{img(n)}" alt="{e(t)}"></div>'
                 f'<figcaption><b>{e(t)}</b><span>{e(d)}</span></figcaption></figure>' for n, t, d in PIEZAS)

pend = ''.join(f'<li><b>{e(a)}</b><span>{e(b)}</span></li>' for a, b in gob.PEND)
obs = ''.join(f'<li><span>{e(a)}</span><em>{e(b)}</em></li>' for a, b in OBS_LECTOR)

html = f'''<title>Kino · Parada 4</title>
<meta name="description" content="Revisión del sistema de marca Kino completo: qué se construyó, cómo se verificó y cinco preguntas.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&family=JetBrains+Mono:wght@400;500;700&display=swap">
<script>
/* El visor marca data-theme; los tokens de Kino leen data-tema. Sin marca, sigue la preferencia del sistema. */
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
a{{color:var(--kino-acento-fuerte);text-underline-offset:.2em}}
a:focus-visible,button:focus-visible{{outline:var(--kino-linea-foco) solid var(--kino-borde-foco);outline-offset:3px}}
h1,h2,h3{{margin:0;text-wrap:balance;font-family:var(--kino-fuente-display)}}
h1{{font-size:var(--kino-texto-5);font-stretch:112%;font-weight:800;line-height:1.02;letter-spacing:-.02em;max-inline-size:18ch}}
h2{{font-size:var(--kino-texto-3);font-stretch:112%;font-weight:750;line-height:1.1}}
h3{{font-size:var(--kino-texto-1);font-weight:700;line-height:1.25}}
p{{margin:0;max-inline-size:66ch}}
.ojo{{font-family:var(--kino-fuente-dato);font-size:var(--kino-texto-n1);letter-spacing:.08em;text-transform:uppercase;color:var(--kino-texto-tenue)}}
.lede{{color:var(--kino-texto-secundario);font-size:var(--kino-texto-1);line-height:1.45}}
.cabeza{{display:grid;gap:1.5rem;padding-block:2.5rem 0}}
.barra{{display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap;padding-block:1.25rem;border-block-end:1px solid var(--kino-borde-tenue)}}
.barra svg{{block-size:2rem;inline-size:auto}}
.barra .mono{{color:var(--kino-texto-tenue);font-size:var(--kino-texto-n1)}}
.enlaces{{display:flex;flex-wrap:wrap;gap:.75rem}}
.enlaces a{{display:inline-flex;align-items:center;gap:.5rem;padding:.55rem 1rem;border:1px solid var(--kino-borde-definido);border-radius:var(--kino-forma-radio-control);color:var(--kino-texto-primario);text-decoration:none;font-weight:600}}
.enlaces a:hover{{border-color:var(--kino-borde-foco)}}
.enlaces a small{{font-family:var(--kino-fuente-dato);color:var(--kino-texto-tenue);font-weight:400}}
.regla{{padding:1rem 1.25rem;border:1px dashed var(--kino-borde-definido);border-radius:var(--kino-forma-radio-tarjeta);color:var(--kino-texto-secundario);max-inline-size:none}}
section{{display:grid;gap:1.5rem;scroll-margin-top:1rem}}
.sec-cab{{display:grid;gap:.6rem}}
.cifras{{display:grid;grid-template-columns:repeat(auto-fit,minmax(11rem,1fr));gap:1rem}}
.cifra{{background:var(--kino-superficie-elevada);border:1px solid var(--kino-borde-tenue);border-radius:var(--kino-forma-radio-tarjeta);padding:1.25rem;display:grid;gap:.4rem;align-content:start}}
.cifra .n{{font-family:var(--kino-fuente-dato);font-size:var(--kino-texto-4);font-weight:700;line-height:1;font-variant-numeric:tabular-nums;color:var(--kino-texto-primario)}}
.cifra h3{{font-size:var(--kino-texto-0)}}
.cifra p{{color:var(--kino-texto-secundario);font-size:var(--kino-texto-n1)}}
.preguntas{{list-style:none;margin:0;padding:0;display:grid;gap:1.25rem;counter-reset:p}}
.preg{{border:1px solid var(--kino-borde-tenue);border-radius:var(--kino-forma-radio-tarjeta);padding:1.5rem;display:grid;gap:1.1rem;background:var(--kino-superficie-elevada)}}
.preg:first-child{{border-color:var(--kino-borde-foco);box-shadow:var(--kino-resplandor-vigente)}}
.preg-cab{{display:grid;grid-template-columns:auto 1fr;gap:1rem;align-items:start}}
.preg-n{{font-family:var(--kino-fuente-dato);font-weight:700;font-size:var(--kino-texto-2);line-height:1;color:var(--kino-acento-base);min-inline-size:1.5ch}}
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
.piezas{{display:grid;grid-template-columns:repeat(auto-fill,minmax(13rem,1fr));gap:1.25rem;align-items:start}}
.pieza{{margin:0;display:grid;gap:.6rem}}
.pieza.ancha{{grid-column:1/-1}}
.pieza .marco{{background:var(--kino-superficie-abismo);border:1px solid var(--kino-borde-tenue);border-radius:var(--kino-forma-radio-tarjeta);padding:.75rem;display:grid;place-items:center}}
.pieza img{{display:block;max-inline-size:100%;block-size:auto;border-radius:.4rem}}
.pieza:not(.ancha) img{{max-block-size:26rem}}
.pieza figcaption{{display:grid;gap:.15rem;font-size:var(--kino-texto-n1);color:var(--kino-texto-secundario)}}
.pieza figcaption b{{color:var(--kino-texto-primario)}}
.dos{{display:grid;grid-template-columns:repeat(auto-fit,minmax(20rem,1fr));gap:1.25rem}}
.caja{{border:1px solid var(--kino-borde-tenue);border-radius:var(--kino-forma-radio-tarjeta);padding:1.25rem;display:grid;gap:.9rem;align-content:start;background:var(--kino-superficie-elevada)}}
.caja .tabla{{border:0;border-radius:0}}
.caja table{{min-inline-size:0}}
.lista{{list-style:none;margin:0;padding:0;display:grid;gap:.7rem}}
.lista li{{display:grid;gap:.15rem;padding-block-end:.7rem;border-block-end:1px solid var(--kino-borde-tenue);font-size:var(--kino-texto-n1);color:var(--kino-texto-secundario)}}
.lista li:last-child{{border:0;padding:0}}
.lista b{{color:var(--kino-texto-primario)}}
.lista em{{font-style:normal;color:var(--kino-texto-tenue)}}
.pend{{columns:2 22rem;column-gap:2rem}}
.pend li{{break-inside:avoid;margin-block-end:.7rem}}
.cierre{{border-block-start:1px solid var(--kino-borde-tenue);padding-block-start:1.5rem;color:var(--kino-texto-tenue);font-size:var(--kino-texto-n1);display:grid;gap:.4rem}}
@media (max-width:40rem){{.preg{{padding:1.1rem}}.preg-cab{{grid-template-columns:1fr}}}}
</style>
<div class="hoja">
<header class="cabeza">
  <div class="barra">{logo('horizontal', etiqueta='Kino')}<span class="mono">Parada 4 · 25 sep 2026 · rama marca/fase-4</span></div>
  <p class="ojo">Sistema de marca · versión 1.0.0 en revisión</p>
  <h1>El sistema completo, listo para tu revisión</h1>
  <p class="lede">Tokens, sitio de doce departamentos, las piezas del Pase y la librería de Figma, con la verificación de la Fase 5. Abajo, cinco preguntas ordenadas por lo que desbloquean.</p>
  <div class="enlaces"><a href="{SITIO}" target="_blank" rel="noopener">Abrir el sitio <small>vista previa</small></a><a href="{FIGMA}" target="_blank" rel="noopener">Abrir Figma <small>BO7UnDO9…</small></a><a href="{RAMA}" target="_blank" rel="noopener">Ver la rama <small>marca/fase-4</small></a></div>
  <p class="regla">El artefacto oficial «Kino · Sistema de marca» no se toca hasta que respondas la pregunta 1. El silencio no cuenta como aprobación.</p>
</header>

<section id="preguntas" aria-labelledby="t-preg">
  <div class="sec-cab"><p class="ojo">Lo que necesito de ti</p><h2 id="t-preg">Cinco preguntas</h2></div>
  <ol class="preguntas">{preguntas}</ol>
</section>

<section id="construido" aria-labelledby="t-cons">
  <div class="sec-cab"><p class="ojo">Fase 4 · bloques 1 a 6</p><h2 id="t-cons">Qué se construyó</h2></div>
  <div class="cifras">
    <div class="cifra"><span class="n">{N_PRIM + N_SEM}</span><h3>Tokens DTCG</h3><p>{N_PRIM} primitivos y {N_SEM} semánticos por tema, oscuro y claro. <span class="mono">kino-brand.css</span> sale de ellos.</p></div>
    <div class="cifra"><span class="n">{2 * len(pares)}</span><h3>Mediciones de contraste</h3><p>{len(pares)} pares en los dos temas, con mínimo WCAG 2.2 y APCA. Cero fallos.</p></div>
    <div class="cifra"><span class="n">12</span><h3>Departamentos en el sitio</h3><p>Del 01 al 12, con glosario, descargas y el motor de movimiento en vivo.</p></div>
    <div class="cifra"><span class="n">6</span><h3>Piezas del Pase</h3><p>Imagen, Pase vivo, PDF, señal de la entrada y portería, en PNG y PDF.</p></div>
    <div class="cifra"><span class="n">{N_VAR}</span><h3>Variables de Figma</h3><p>Iguales a DTCG en los dos modos, más {N_EF} sombras como estilos de efecto. Seis juegos de componentes con todos sus estados.</p></div>
  </div>
</section>

<section id="piezas" aria-labelledby="t-piezas">
  <div class="sec-cab"><p class="ojo">Bloque 3 · forma Portal (X1)</p><h2 id="t-piezas">Las piezas del Pase</h2>
  <p class="lede">Datos de ejemplo. El QR vive dentro del arco del logo en todas.</p></div>
  <div class="piezas">{piezas}</div>
</section>

<section id="verificacion" aria-labelledby="t-verif">
  <div class="sec-cab"><p class="ojo">Fase 5 · {PASAN} de {len(informe)}</p><h2 id="t-verif">Verificación</h2>
  <p class="lede">Se corre con <span class="mono">verificacion/fase5.py</span>. La comprobación 6 compara 270 variables de Figma contra DTCG en los dos modos, además de los números y las sombras.</p></div>
  {verif}
</section>

<section id="evaluaciones" aria-labelledby="t-eval">
  <div class="sec-cab"><p class="ojo">Dos lectores que solo vieron el sitio</p><h2 id="t-eval">Evaluaciones independientes</h2></div>
  <div class="dos">
    <div class="caja"><h3>Lector frío {chip('vigente', 'Pasa')}</h3>
      {tabla(['Ciclo', 'Con cita', 'Claridad media'], [['1', '8 de 8', '3,9'], ['2', '8 de 8', '<b>4,25</b>']])}
      <p class="nota">Observaciones que siguen abiertas:</p><ul class="lista">{obs}</ul></div>
    <div class="caja"><h3>Detector de IA {chip('rechazado', 'Falla')}</h3>
      {tabla(['Ciclo', 'Señales', 'Secciones con más de 1'], [['1', '17', 'Plataforma, Imagen, Voz, Iconografía'], ['2', '12', 'Plataforma, Imagen'], ['3', '<b>8</b>', 'Motion, Plataforma']])}
      <p>Las 8 señales del ciclo 3 se corrigieron. El límite de 3 ciclos impide volver a medir, así que la condición queda sin verificar y se reporta como falla. Queda un patrón: titulares en dos mitades paralelas. Ver la pregunta 5.</p></div>
  </div>
</section>

<section id="departamentos" aria-labelledby="t-dep">
  <div class="sec-cab"><p class="ojo">Sitio definitivo · bloques 2 y 4</p><h2 id="t-dep">Estado por departamento</h2></div>
  {deptos}
</section>

<section id="decisiones" aria-labelledby="t-dec">
  <div class="sec-cab"><p class="ojo">decisiones.md</p><h2 id="t-dec">Decisiones</h2></div>
  <div class="dos">
    <div class="caja"><h3>Aprobadas</h3><ul class="lista">
      <li><b>Plataforma · {N_P}</b><span>P01 a P14. P11 quedó reemplazada por V5.</span></li>
      <li><b>Verbal · {N_V}</b><span>V1 a V7: usted con la administración, «Pase» con mayúscula, horas, «Visita», estados, patrones, imagen más enlace.</span></li>
      <li><b>Identidad visual · {N_X}</b><span>X1 a X11: Portal, logo, oscuro reajustado, dos verdes, tipografía, íconos, imagen, radio y arco, crecer, estados, llamada de portería.</span></li></ul></div>
    <div class="caja"><h3>Propuestas nuevas</h3><ul class="lista">
      <li><b>F4-P1 · Llamada desde el Pase vivo</b><span>Recomendada: quitar el botón y dejar la llamada solo en portería. Pregunta 3.</span></li>
      <li><b>F4-P2 · Aviso de llegada</b><span>Recomendada: tratarlo como requisito de producto y no publicarlo antes de que exista. Pregunta 2.</span></li>
      <li><b>Efecto en la trazabilidad</b><span>Ninguna de las dos autoriza un ingreso. Entrar siempre exige un Pase con autor, que llega a HikCentral con su vigencia.</span></li></ul></div>
  </div>
</section>

<section id="cambios" aria-labelledby="t-camb">
  <div class="sec-cab"><p class="ojo">Al preparar esta lámina</p><h2 id="t-camb">Un defecto corregido y una limitación</h2></div>
  <p>Las piezas del Pase en PNG y PDF se habían generado con una fuente de reemplazo: pedían Archivo y JetBrains Mono a Google Fonts, y el entorno donde se generan no tiene esa salida. Ahora las fuentes van incrustadas desde <span class="mono">branding/sistema/fonts/</span> y las cuatro entregas se volvieron a generar. El PDF sigue en una página.</p>
  <p>Una limitación de la vista previa: dentro del visor de artefactos, los botones del centro de descargas no bajan nada. En el archivo del repositorio sí funcionan. Al republicar el artefacto oficial, las descargas pasan por la función de descarga del visor.</p>
</section>

<section id="pendientes" aria-labelledby="t-pend">
  <div class="sec-cab"><p class="ojo">Gobernanza · {len(gob.PEND)}</p><h2 id="t-pend">Pendientes</h2>
  <p class="lede">Lo que el sistema no puede resolver con los archivos que hay. Cada uno aparece marcado en el sitio donde afecta.</p></div>
  <ul class="lista pend">{pend}</ul>
</section>

<footer class="cierre">
  <p>Fuentes: <span class="mono">verificacion/informe.md</span>, <span class="mono">verificacion/evaluaciones.md</span>, <span class="mono">figma/variables-figma.json</span>, <span class="mono">decisiones.md</span>, <span class="mono">avances.md</span>.</p>
  <p>Generada con <span class="mono">branding/sistema/v3/parada4/construir.py</span>.</p>
</footer>
</div>
'''
(RAIZ / 'parada-4.html').write_text(html, encoding='utf8')
# Texto visible para la compuerta de voz.
vis = re.sub(r'<(style|script|svg)[^>]*>.*?</\1>', ' ', html, flags=re.S)
vis = re.sub(r'<title>.*?</title>|<meta[^>]*>', ' ', vis)
vis = re.sub(r'<(li|p|h\d|td|th|b|figcaption|span|a|div)[^>]*>', '\n', vis)
vis = re.sub(r'<[^>]+>', '', vis)
vis = '\n'.join(l.strip() for l in vis.splitlines() if l.strip())
(R / 'texto-visible.md').write_text(vis, encoding='utf8')
print('ok parada-4.html', len(html.encode()) // 1024, 'KB ·', PASAN, 'de', len(informe), 'pasan')
