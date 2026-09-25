from .comun import *  # noqa: F401,F403
from . import d03_logo, d06_iconografia

PEND = [
    ('Vector original del logo', 'No existe. Los SVG son reconstrucciones desde los PNG de 1543 × 1425 px, con 98 % de coincidencia. Las medidas del logo son derivadas.'),
    ('Licencia de Arkit ExtraBold', 'Sin información. La fuente vive solo dentro de los contornos del logotipo.'),
    ('Mensajes reales de portería y WhatsApp', 'No hay ninguno en los archivos. Las plantillas se escribieron sin referencia de uso real.'),
    ('Credencial temporal en HikCentral', 'Falta confirmar que acepte una credencial sin crear una persona. Es la prueba del Pase sin cuenta.'),
    ('Unidad del cupo', 'Por casa, por residente o por conjunto. Decisión de producto; los ejemplos dicen «a la vez».'),
    ('Teclado del lector', 'No se sabe si el lector tiene teclado para el código. El texto dice «Dile a portería el código».'),
    ('Llamada de portería al residente', 'Nico confirmó que portería puede llamar desde Kino (X11). La inspección no registró el botón: si no existe, es un requisito de producto.'),
    ('Evento de paso del lector', 'El aviso de llegada (F4-P2) es requisito de producto: falta confirmar que HikCentral le entregue a Kino el evento de paso. Ningún texto del aviso sale antes.'),
    ('Citas de las entrevistas con residentes', 'Las cinco entrevistas no tienen citas escritas. Las necesidades por actor se apoyan en la inspección.'),
    ('Integración real de las apps de visitas', 'Neivor anuncia integración sin nombrar marcas de hardware. Falta verificar.'),
    ('Prueba física del logo y de color', 'Tamaños mínimos impresos y CMYK sin prueba en papel.'),
    ('Equivalencias Pantone', 'Sin guía física para comparar.'),
    ('Prueba con usuarios daltónicos', 'Los estados se revisaron solo por simulación.'),
    ('Mockups físicos en 3D', 'No hubo herramienta 3D disponible. Señal, adhesivo, papelería y credencial están en 2D.'),
    ('Datos de contacto', 'Correo, teléfono y dominio definitivos. Los ejemplos usan kino.co.'),
    ('Canal de solicitudes', 'Dónde se piden activos y cambios: correo o canal del equipo, por definir.'),
]

CAMBIOS = [
    ('1.2.1', '25 sep 2026', 'Propuesta', 'Sitio responsive de 320 a 1920 px: tablas apiladas como fichas, mapa y árbol en HTML para el teléfono, columnas que caben y textos de al menos 11 px. Espera revisión.'),
    ('1.2.0', '25 sep 2026', 'Aprobada', 'Pantallas con la jerarquía del Pase (un dato manda, vigencia en el color de su estado, rótulos, bloques y una acción) y mensaje genérico de alta fallida en HikCentral.'),
    ('1.1.0', '25 sep 2026', 'Aprobada', 'La identidad aplicada al propio sitio, ícono en los chips de Usado, Vencido y Revocado, llamada solo desde portería, librería de Figma con auto-layout y espaciado revisados.'),
    ('1.0.0', '24 sep 2026', 'Aprobada', 'Tokens con la paleta aprobada, departamentos 03 a 12, piezas del Pase y verificación. La librería de Figma se aprobó en la 1.1.0.'),
    ('0.3', '24 sep 2026', 'Aprobada', 'Identidad visual: forma Portal, dos verdes, oscuro reajustado, Archivo al 112 %, trazo 1,7, aurora, radio 14 y arco, crecer, estados. Llamada de portería en vencido.'),
    ('0.2', '23 sep 2026', 'Aprobada', 'Voz: usted con la administración, «Pase» con mayúscula, horas, «Visita», nombres de estado, patrones de voz, imagen más enlace.'),
    ('0.1', '23 sep 2026', 'Aprobada', 'Plataforma y arquitectura: posicionamiento, promesa, personalidad, valores, nombres y manifiesto.'),
    ('0.0', '23 sep 2026', 'Borrador', 'Borrador del sistema. Copia guardada con su fecha.'),
]

REVISION = [
    '¿Cada estado lleva palabra además de color?',
    '¿El verde #00D595 aparece solo en el botón que crea o entrega un Pase?',
    '¿El conjunto aparece solo como dato, sin logo ni colores?',
    '¿Los textos pasan <code>npm run voz -- kino</code> sin errores?',
    '¿Todo par texto y fondo nuevo está en <code>pares.json</code> y pasa APCA?',
    '¿Ningún hex, tamaño ni duración está escrito a mano en el código?',
    '¿El arco aparece solo en lo que es un Pase?',
    '¿Placas, códigos y horas en datos van en JetBrains Mono?',
    '¿Tú con residente y visita, usted con la administración, sin mezclar en una pieza?',
    '¿El texto evita las palabras de la lista <a href="#verbal">Evitar</a> de Verbal?',
    '¿Las cifras tienen denominador y fuente?',
    '¿El logo respeta su área de protección y su tamaño mínimo?',
]


def _registro():
    """Códigos de decisión (F, H, P, V, X) leídos de decisiones.md, con su estado."""
    d = (R / '../../../../decisiones.md').read_text(encoding='utf8')
    filas = []
    for c, t in re.findall(r'^\| (F\d) \| ([^|]+) \|', d, flags=re.M):
        filas.append((c, t.strip(), 'Aprobada'))
    for c, t in re.findall(r'^\| (H\d) \| ([^|]+) \|', d, flags=re.M):
        filas.append((c, t.strip(), 'Revisada en la revisión 3'))
    for c, t, est in re.findall(r'^### ([PV]\d{1,2}) · (.+?) · (APROBADA|REEMPLAZADA|PROPUESTA|REVERTIDA)', d, flags=re.M):
        filas.append((c, t.strip(), est.capitalize()))
    for c, t, a in re.findall(r'^\| (X\d+) \| ([^|]+) \| ([^|]+) \|', d, flags=re.M):
        filas.append((c, f'{t.strip()}: {a.strip()}', 'Aprobada'))
    if '### X11' in d:
        filas.append(('X11', 'Pase vencido en la entrada: portería puede llamar al residente', 'Aprobada'))
    for c, t, est in re.findall(r'^### (F4-P\d) · (.+?) · (APROBADA|PROPUESTA)', d, flags=re.M):
        filas.append((c, t.strip(), est.capitalize()))
    # En el texto visible, las palabras que la voz evita se reemplazan por su forma aprobada.
    limpiar = lambda t: t.replace(', nunca «permiso»', '').replace('el invitado', 'la visita').replace('invitado', 'visita')
    filas = [(c, limpiar(t), s) for c, t, s in filas]
    est = lambda s: chip('vigente' if s == 'Aprobada' else ('previsto' if s == 'Propuesta' else 'vencido'), s)
    return tabla(['Código', 'Decisión', 'Estado'], [[f'<span class="mono">{c}</span>', e(t), est(s)] for c, t, s in filas], 'Registro de decisiones')


def html_():
    pend_html = ''.join(f'<li><strong>{e(a)}</strong><span>{e(b)}</span></li>' for a, b in PEND)
    cambios = tabla(['Versión', 'Fecha', 'Estado', 'Qué cambió'], [[f'<span class="mono">{v}</span>', f'<span class="mono">{f}</span>', chip('vigente' if s == 'Aprobada' else ('previsto' if s == 'Propuesta' else 'vencido'), s), c] for v, f, s, c in CAMBIOS], 'Registro de cambios')
    rev = ''.join(f'<li><label><input type="checkbox"> {t}</label></li>' for t in REVISION)
    # Centro de descargas: reúne los archivos que ya están junto a cada regla.
    H = lambda n: hx(n)
    logos = [descarga(nombre, f'kino-{id_}.svg', re.sub(r'<path fill="#(000000|FFFFFF)" d="M 50.000[^"]*"/>', '', logo(forma, bloque=hb, gota=hg, hex_=True)))
             for id_, nombre, _f, forma, _b, _g, hb, hg, _u in d03_logo.VERSIONES]
    sprite = ('<svg xmlns="http://www.w3.org/2000/svg" style="display:none"><defs>'
              + ''.join(f'<symbol id="kino-{k}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="{d}"/></symbol>' for k, _, d in d06_iconografia.ICONOS)
              + '</defs></svg>')
    centro = (f'<div class="centro"><div><h3>Logo</h3>{descargas(*logos)}</div>'
              f'<div><h3>Íconos</h3>{descargas(descarga("Favicon", "kino-favicon.svg", d03_logo._favicon()), descarga("Ícono de app", "kino-icono-app.svg", d03_logo._icono_app()), descarga("Sprite de íconos", "kino-iconos.svg", sprite))}</div>'
              f'<div><h3>Código</h3>{descargas(descarga("Tokens DTCG resueltos", "kino-tokens.resuelto.json", (GBS / "build/tokens.resuelto.json").read_text(encoding="utf8"), "application/json"), descarga("Tokens en CSS", "kino-tokens.css", TOKENS_CSS, "text/css"), descarga("Capa de marca", "kino-brand.css", (R / "../../kino-brand.css").read_text(encoding="utf8"), "text/css"))}</div>'
              f'<div><h3>Fuentes</h3><p><a href="https://fonts.google.com/specimen/Archivo" rel="noopener">Archivo</a> · <a href="https://fonts.google.com/specimen/JetBrains+Mono" rel="noopener">JetBrains Mono</a> (OFL 1.1)</p></div></div>')
    cuerpo = '\n'.join([
        sub('gobernanza.decide', 'Quién decide', 'El equipo de Kino decide sobre la marca',
            'Nico Ramírez y Alejandro Monsalve. Una propuesta de cambio llega con la fila de la plataforma a la que responde; sin esa fila no se discute.',
            tabla(['Qué', 'Quién decide', 'Cómo queda'], [
                ['Logo, color, tipografía, voz', 'El equipo de Kino', 'En el registro de decisiones con estado Aprobada'],
                ['Una pieza nueva con la marca', 'Quien la produce, con la lista de revisión', 'Revisa el equipo antes de publicar'],
                ['Datos de un conjunto en una pieza', 'La administración del conjunto', 'Solo nombre y unidad, como texto'],
                ['Tokens y código', 'El equipo de Kino', 'Cambio en los tokens del repositorio, con todas las compuertas en verde'],
            ], 'Quién decide cada cosa')
            + traza('F4: Kino tiene identidad propia. La administración de un conjunto no decide sobre la marca.')),
        sub('gobernanza.pedir', 'Cómo pedir activos', 'Tres datos y el equipo responde',
            'Para pedir un archivo o una pieza nueva, escribe qué pieza es, dónde se va a publicar y para cuándo. Si el archivo ya existe, está en el centro de descargas de abajo.',
            '<ol class="pasos-cortos"><li>Busca el archivo junto a su regla o en el centro de descargas.</li><li>Si no está, pide la pieza con qué, dónde y cuándo ' + pend('canal de solicitudes') + '.</li><li>Antes de publicar, pasa la lista de revisión.</li></ol>'),
        sub('gobernanza.versiones', 'Versiones', 'Número de versión con tres partes',
            'Mayor, menor y corrección, como en el software. El número está en la cabecera de <code>kino-tokens.css</code> y en este registro.',
            tabla(['Cambio', 'Ejemplo', 'Sube'], [
                ['Cambia lo que significa algo', 'El color de un estado, la forma del logo, un nombre', 'Mayor: 1.0.0 → 2.0.0'],
                ['Algo nuevo que no rompe lo anterior', 'Un componente, una pieza, un ícono', 'Menor: 1.0.0 → 1.1.0'],
                ['Corrección', 'Un texto, un paso de contraste, un error de dibujo', 'Corrección: 1.0.0 → 1.0.1'],
            ], 'Reglas de versión')),
        sub('gobernanza.cambios', 'Registro de cambios', 'Qué cambió y cuándo', '', cambios),
        sub('gobernanza.registro', 'Registro de decisiones', 'Qué significa cada código de decisión',
            'Las líneas «Responde a» de cada regla citan un código. F son las decisiones fijas del inicio; H, las heredadas del borrador; P, V y X, las aprobadas en las revisiones de plataforma, voz e identidad visual.',
            _registro()),
        sub('gobernanza.revision', 'Lista de revisión', 'Doce preguntas antes de publicar una pieza', '', f'<ul class="revision">{rev}</ul>'),
        sub('gobernanza.pendientes', 'Pendientes', 'Lo que falta y por qué no se puede resolver todavía', '', f'<ul class="pendientes">{pend_html}</ul>'),
        sub('gobernanza.descargas', 'Centro de descargas', 'Todos los archivos en un lugar',
            'Cada archivo también está junto a la regla que lo gobierna.', centro),
    ])
    return seccion('gobernanza', '12', 'Gobernanza', 'Operación',
                   'Quién decide sobre la marca y cómo se pide un archivo o un cambio.',
                   'Para que la marca siga siendo una sola cuando la usen personas fuera del equipo.',
                   'Antes de publicar una pieza o de proponer un cambio.', cuerpo)
