from .comun import *  # noqa: F401,F403
from . import motor

CURVAS = [('crecer', 'Aparecer. Arranca rápido y se asienta.'), ('decaer', 'Caducar. Empieza lento y se va.'),
          ('latir', 'Estar vivo. Simétrica, en bucle.'), ('revocar', 'Cortar. Acelera hasta el final, sin rebote.'),
          ('cortina', 'Abrir, solo en presentaciones.')]
DURACIONES = [('instante', 'Hover, foco, presión de un botón.'), ('corto', 'Un chip o un estado que cambia; revocar.'),
              ('crecer', 'Elementos pequeños que aparecen.'), ('tarjeta', 'Tarjetas y secciones que aparecen (X9).'),
              ('decaer', 'La barra de vigencia que baja.'), ('trazo', 'Una línea que se dibuja en un flujo.'),
              ('cortina', 'Transición entre láminas.'), ('latir', 'Un ciclo del latido de Vigente.')]

CATALOGO = [
    ('aparecer', 'Aparecer', 'Una tarjeta nueva crece desde abajo.', 'aparecer · 820 ms · crecer', 'Fundido de 240 ms'),
    ('cascada', 'Cascada', 'La lista de Pases entra una tarjeta tras otra, cada 90 ms.', 'escalonado · 90 ms', 'Fundido en el mismo orden'),
    ('latir', 'Latir', 'El punto de un Pase vigente respira mientras está en pantalla.', 'latir · 1800 ms', 'Punto fijo'),
    ('caducar', 'Caducar', 'La barra de vigencia baja cuando pasa el tiempo.', 'caducar · 900 ms · decaer', 'La barra salta sin animar'),
    ('confirmar', 'Confirmar', 'El lector responde: el borde discontinuo se cierra y aparece el relleno.', 'aparecer · 820 ms', 'Cambio de estado en 240 ms'),
    ('por-vencer', 'Por vencer', 'El chip pasa de verde a ámbar cuando entra la ventana de aviso.', 'responder · 240 ms', 'Igual: es un cambio de color'),
    ('revocar', 'Revocar', 'Una línea cruza la tarjeta y la apaga. Queda el nombre de quien revocó.', 'revocar · 240 ms', 'Sin la línea; cambia el estado'),
    ('usar', 'Usar', 'El código de un solo uso se tacha y pasa a Usado.', 'responder · 240 ms', 'Sin el tachado animado'),
    ('rechazar', 'Rechazar', 'En portería, el evento aparece con un borde que se enciende una vez.', 'crecer · 420 ms', 'Aparece sin encenderse'),
    ('enviar', 'Enviar', 'El Pase sube y se convierte en el mensaje de WhatsApp.', 'aparecer · 820 ms', 'Fundido cruzado'),
    ('presionar', 'Presionar', 'El botón Crear Pase baja un poco al tocarlo.', 'instante · 120 ms', 'Cambio de color sin escala'),
    ('trazo', 'Trazo', 'La línea de un flujo se dibuja de un paso al siguiente.', 'trazo · 950 ms', 'La línea aparece completa'),
    ('cortina', 'Cortina', 'En una presentación, la lámina siguiente entra como una cortina.', 'cortina · 1600 ms', 'Fundido de 240 ms'),
]


def _curva(nombre):
    v = PRIM[f'kino-movimiento-curva-{nombre}']
    x1, y1, x2, y2 = [float(n) for n in re.findall(r'-?\d*\.?\d+', v.split('(')[1])]
    P = lambda x, y: (10 + x * 100, 110 - y * 100)
    a, b, c, d = P(0, 0), P(x1, y1), P(x2, y2), P(1, 1)
    return (f'<svg class="curva" viewBox="0 0 120 120" width="120" height="120" style="aspect-ratio:1" role="img" aria-label="Curva {nombre}: {v}">'
            f'<rect x="10" y="10" width="100" height="100" class="c-marco"/><line x1="{a[0]}" y1="{a[1]}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" class="c-guia"/>'
            f'<line x1="{d[0]}" y1="{d[1]}" x2="{c[0]:.1f}" y2="{c[1]:.1f}" class="c-guia"/>'
            f'<path d="M{a[0]} {a[1]} C{b[0]:.1f} {b[1]:.1f} {c[0]:.1f} {c[1]:.1f} {d[0]} {d[1]}" class="c-linea"/></svg>')


def _escena(k):
    tarjeta = lambda n='Andrés Gómez', est='vigente', txt='Vigente': (f'<div class="kino-pase m-tarjeta" data-estado="{est}"><div class="kino-pase__cabeza"><p class="kino-pase__quien">{n}</p>{chip(est, txt)}</div>'
                                                                   f'<span class="kino-vigencia"><i></i></span></div>')
    if k == 'cascada':
        return '<div class="m-lista">' + ''.join(f'<div class="kino-pase m-fila" style="--i:{i}"><p class="kino-pase__quien">{n}</p></div>' for i, n in enumerate(['Andrés Gómez', 'Luz Marina', 'Técnico del gas', 'Diana Arango'])) + '</div>'
    if k == 'confirmar':
        return '<div class="kino-pase m-tarjeta m-confirma" data-estado="sin-confirmar"><div class="kino-pase__cabeza"><p class="kino-pase__quien">Andrés Gómez</p><span class="kino-estado m-a" data-estado="sin-confirmar">Sin confirmar</span><span class="kino-estado m-b" data-estado="vigente">Vigente</span></div></div>'
    if k == 'por-vencer':
        return '<div class="kino-pase m-tarjeta"><div class="kino-pase__cabeza"><p class="kino-pase__quien">Andrés Gómez</p><span class="kino-estado m-a" data-estado="vigente">Vigente</span><span class="kino-estado m-b" data-estado="por-vencer">Por vencer</span></div><p class="kino-pase__pie"><span class="kino-dato">vence 6:00 p. m.</span></p></div>'
    if k == 'revocar':
        return '<div class="kino-pase m-tarjeta m-revoca"><div class="kino-pase__cabeza"><p class="kino-pase__quien">Andrés Gómez</p><span class="kino-estado m-a" data-estado="vigente">Vigente</span><span class="kino-estado m-b" data-estado="revocado">Revocado</span></div><p class="kino-pase__autor m-b">Revocó Carolina Ruiz · 4:10 p. m.</p><span class="m-corte"></span></div>'
    if k == 'usar':
        return '<div class="kino-pase m-tarjeta"><div class="kino-pase__cabeza"><p class="kino-placa m-codigo">4817</p><span class="kino-estado m-a" data-estado="vigente">Vigente</span><span class="kino-estado m-b" data-estado="usado">Usado</span></div></div>'
    if k == 'rechazar':
        return '<div class="kino-pase m-tarjeta m-rechazo"><div class="kino-pase__cabeza"><p class="kino-placa">KMN 305</p><span class="kino-estado" data-estado="rechazado">Rechazado</span></div><p class="kino-pase__autor">Pase vencido a las 6:00 p. m.</p></div>'
    if k == 'enviar':
        return '<div class="m-envio"><div class="kino-pase m-tarjeta m-sale"><p class="kino-pase__quien">Pase para Andrés</p></div><div class="wa-burbuja m-llega"><p>Carolina Ruiz, de la Casa 14, te dio un Pase para hoy.</p></div></div>'
    if k == 'presionar':
        return '<button class="kino-accion m-presiona" type="button" tabindex="-1">Crear Pase</button>'
    if k == 'trazo':
        return ('<svg class="m-trazo" viewBox="0 0 300 60" width="300" height="60" style="aspect-ratio:5/1" aria-hidden="true">'
                '<circle cx="20" cy="30" r="8"/><circle cx="150" cy="30" r="8"/><circle cx="280" cy="30" r="8"/>'
                '<path d="M28 30H142 M158 30H272" pathLength="1"/></svg>')
    if k == 'cortina':
        return '<div class="m-lamina"><p>Lámina 1</p><div class="m-cortina"><p>Lámina 2</p></div></div>'
    if k == 'caducar':
        return tarjeta()
    return tarjeta()


def html_():
    dur = tabla(['Token', 'Valor', 'Para qué'], [[f'<code>duracion-{k}</code>', f'<span class="mono">{PRIM["kino-movimiento-duracion-" + k]}</span>', u] for k, u in DURACIONES]
                + [['<code>escalonado-tarjetas</code>', f'<span class="mono">{PRIM["kino-movimiento-escalonado-tarjetas"]}</span>', 'Entre tarjetas de una cascada.'],
                   ['<code>escalonado-filas</code>', f'<span class="mono">{PRIM["kino-movimiento-escalonado-filas"]}</span>', 'Entre filas de una tabla.']], 'Duraciones')
    curvas = ''.join(f'<figure class="curva-fig">{_curva(k)}<figcaption><b>{k}</b><span class="mono">{PRIM["kino-movimiento-curva-" + k]}</span><small>{u}</small></figcaption></figure>' for k, u in CURVAS)
    cat = ''.join(f'<figure class="demo m-{k}" data-demo><div class="demo-escena">{_escena(k)}</div>'
                  f'<figcaption><h3>{i + 1:02d} · {n}</h3><p>{q}</p><p class="mono nota">{t}</p><p class="nota">Reducido: {r}</p>'
                  f'<button class="boton-tenue" type="button" data-repetir>Repetir</button></figcaption></figure>' for i, (k, n, q, t, r) in enumerate(CATALOGO))
    cuerpo = '\n'.join([
        sub('motion.principios', 'Principios', 'Cada movimiento nombra un cambio del Pase',
            'Kino se mueve cuando algo cambia de verdad: un Pase aparece, el lector lo confirma, el tiempo pasa, alguien lo corta. Si nada cambió, nada se mueve.',
            tabla(['Verbo', 'Significa', 'Curva', 'Ejemplo'], [
                ['Crecer', 'Aparecer', '<code>crecer</code>', 'Un Pase nuevo en la lista.'],
                ['Decaer', 'Caducar', '<code>decaer</code>', 'La barra de vigencia.'],
                ['Latir', 'Estar vivo', '<code>latir</code>', 'El punto de Vigente.'],
                ['Revocar', 'Cortar', '<code>revocar</code>', 'Carolina revoca el Pase de Andrés.'],
                ['Cortina', 'Abrir', '<code>cortina</code>', 'Cambio de lámina en una presentación.'],
            ], 'Principios de movimiento')
            + '<ul class="reglas-cortas"><li>Nada se anima para decorar.</li><li>El movimiento no se recorta para ganar velocidad: se optimiza con transform y opacity, carga diferida y pausa fuera de pantalla.</li><li>Lo que está fuera de la pantalla no anima; en este sitio, las secciones ocultas no pintan.</li></ul>'
            + traza('H6 y F7: verbos de movimiento con significado; el motion no se sacrifica.')),
        sub('motion.tokens', 'Duraciones y curvas', 'Diecisiete tokens de movimiento', '',
            dur + f'<div class="curvas">{curvas}</div>'),
        sub('motion.coreografia', 'Coreografía', 'Primero lo que se lee, después lo que se toca',
            'En una pantalla nueva entra el título, luego las tarjetas en cascada de 90 ms y al final el botón de acción. Máximo ocho elementos en una cascada; del noveno en adelante entran juntos.',
            '<div class="demo m-coreo" data-demo><div class="demo-escena"><div class="coreo"><p class="coreo-t" style="--i:0">Pases de la Casa 14</p>'
            + ''.join(f'<div class="kino-pase coreo-f" style="--i:{i + 1}"><p class="kino-pase__quien">{n}</p>{chip(s, t)}</div>' for i, (n, s, t) in enumerate([('Andrés Gómez', 'vigente', 'Vigente'), ('Luz Marina', 'previsto', 'Previsto'), ('Técnico del gas', 'sin-confirmar', 'Sin confirmar')]))
            + '<button class="kino-accion coreo-b" style="--i:4" type="button" tabindex="-1">Crear Pase</button></div></div>'
            '<figcaption><button class="boton-tenue" type="button" data-repetir>Repetir</button></figcaption></figure>'),
        sub('motion.catalogo', 'Catálogo', f'{len(CATALOGO)} animaciones en vivo',
            'Cada una con su token y su versión en movimiento reducido. Pruébalas también con el botón de abajo.',
            '<p><button class="boton-tenue" type="button" data-mov-reducido aria-pressed="false">Ver en movimiento reducido</button></p>'
            f'<div class="catalogo">{cat}</div>'),
        sub('motion.motor', 'El motor', 'El motor que mueve todo esto', '', motor.sub_html()),
        sub('motion.logo', 'Movimiento del logo', 'El logo se anima una sola vez',
            'Al abrir la app y al empezar una presentación. La secuencia completa está en <a href="#logo.animacion">Logo · Animación</a>.', ''),
        sub('motion.reducido', 'Movimiento reducido', 'Un modo alternativo, no un recorte',
            'Si el sistema operativo pide menos movimiento, Kino cambia desplazamientos por fundidos con la misma duración de referencia y el mismo orden. El latido se detiene.',
            casos(caso('<div class="kino-pase m-tarjeta"><div class="kino-pase__cabeza"><p class="kino-pase__quien">Andrés Gómez</p>' + chip('vigente', 'Vigente') + '</div></div>', 'Movimiento completo para quien no pidió menos.'),
                  caso('<div class="kino-pase m-tarjeta sin-mov"><div class="kino-pase__cabeza"><p class="kino-pase__quien">Andrés Gómez</p>' + chip('vigente', 'Vigente') + '</div></div>', 'Apagar toda animación para todos «por rendimiento».', False))
            + traza('F7: prefers-reduced-motion se ofrece como modo alternativo.')),
    ])
    return seccion('motion', '09', 'Motion', 'Identidad',
                   'Cómo se mueve Kino y qué significa cada movimiento.',
                   'Para que otorgar, confirmar, vencer y revocar un Pase se distingan también por su ritmo.',
                   'Al animar una pantalla o el logo.', cuerpo)
