"""Motion Playground (gorr-brand-system/vendor/motion) integrado en la sección Motion.
Se guarda en base64 dentro del sitio y se monta en un iframe solo cuando alguien lo abre (carga diferida).
Al salir de la sección, sitio.js lo desmonta: su bucle de requestAnimationFrame no corre fuera de pantalla (F7).
Sus colores y fuentes se reemplazan por los tokens de Kino; el motor y sus demos no se tocan."""
import base64, re
from .comun import GBS, OSC, CLA, e

ORIGEN = GBS / '../../vendor/motion/Motion_Playground_1.html'


def _vars(t):
    return (f'--base:{t["kino-superficie-base"]};--sup:{t["kino-superficie-elevada"]};--linea:{t["kino-borde-tenue"]};'
            f'--linea2:{t["kino-borde-definido"]};--tx:{t["kino-texto-primario"]};--tx2:{t["kino-texto-secundario"]};'
            f'--tx3:{t["kino-texto-secundario"]};--ac:{t["kino-acento-base"]};--ac2:{t["kino-estado-previsto-texto"]};')


def pagina():
    s = ORIGEN.read_text(encoding='utf8')
    s = re.sub(r'<metadata>.*?</metadata>', '', s, flags=re.S)
    tema = ('<style>/* Kino: colores y fuentes desde los tokens DTCG */'
            f':root{{{_vars(OSC)}--sans:Archivo,system-ui,sans-serif;--mono:"JetBrains Mono",ui-monospace,monospace;--r:8px}}'
            f':root[data-tema="claro"]{{{_vars(CLA)}}}</style>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&family=JetBrains+Mono:wght@400;500;700&display=swap">')
    return s.replace('</head>', tema + '</head>', 1)


def carga():
    """Script inerte con la página del motor en base64."""
    b64 = base64.b64encode(pagina().encode('utf8')).decode('ascii')
    return f'<script type="application/octet-stream" id="motor-src">{b64}</script>'


def sub_html():
    return ('<p>El motor de movimiento del sistema: un solo reloj de <code>requestAnimationFrame</code>, curvas, muelles, escalonado y la política de movimiento reducido. '
            'Aquí corre con los colores de Kino. Sus textos de demostración son del motor, no de la marca.</p>'
            '<p><button class="descarga" type="button" data-motor aria-controls="motor"><svg class="ic" aria-hidden="true"><use href="#i-flecha"/></svg>Abrir el motor en vivo</button></p>'
            '<div id="motor" class="motor" hidden></div>'
            '<p class="nota">Se carga al abrirlo y se detiene al salir de esta sección. Archivo original: <code>gorr-brand-system/vendor/motion/Motion_Playground_1.html</code>.</p>')
