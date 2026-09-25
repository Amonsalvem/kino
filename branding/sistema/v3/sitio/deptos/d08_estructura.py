from .comun import *  # noqa: F401,F403

ESPACIOS = ['3xs', '2xs', 'xs', 's', 'm', 'l', 'xl', '2xl', '3xl', '4xl']


def _reticula(nombre, cols, ancho, alto, margen, medianil, nota):
    w_util = ancho - 2 * margen
    col = (w_util - (cols - 1) * medianil) / cols
    rects = ''.join(f'<rect x="{margen + i * (col + medianil):.1f}" y="{margen * .6:.1f}" width="{col:.1f}" height="{alto - margen * 1.2:.1f}"/>' for i in range(cols))
    return (f'<figure class="reticula"><svg viewBox="0 0 {ancho} {alto}" width="{ancho}" height="{alto}" style="aspect-ratio:{ancho}/{alto}" role="img" aria-label="Retícula {nombre}">'
            f'<rect class="ret-marco" width="{ancho}" height="{alto}" rx="6"/><g class="ret-col">{rects}</g></svg>'
            f'<figcaption><h3>{nombre}</h3><p class="mono">{cols} columnas · margen {margen} · medianil {medianil}</p><p>{nota}</p></figcaption></figure>')


def html_():
    esp = ''.join(f'<li><span class="mono">{k}</span><span class="barra-esp" style="inline-size:var(--kino-espacio-{k})"></span><span class="mono">{PRIM["kino-espacio-" + k]}</span></li>' for k in ESPACIOS)
    radios = [('nada', 'Tablas y bordes de pantalla'), ('xs', 'Marcas de texto, código en línea'), ('s', 'Chips de estado'),
              ('m', 'Controles: botones, campos, selectores'), ('l', 'Tarjetas, hojas, el Pase'), ('arco', 'Solo la ventana del QR y el Pase vivo')]
    rad = ''.join(f'<figure class="radio-m"><span style="border-radius:{"var(--kino-forma-radio-pase-arco) var(--kino-forma-radio-pase-arco) var(--kino-radio-l) var(--kino-radio-l)" if k == "arco" else f"var(--kino-radio-{k})"}"></span>'
                  f'<figcaption><b class="mono">{k} · {PRIM["kino-radio-" + k] if k != "arco" else "pleno arriba"}</b><small>{u}</small></figcaption></figure>' for k, u in radios)
    capas = [('abismo', 'Índice, cabeceras de tabla, lo que está detrás.'), ('base', 'Fondo de la app.'), ('elevada', 'Tarjetas y listas.'),
             ('membrana', 'Controles y el Pase, con relieve.')]
    elev = ''.join(f'<div class="capa" style="background:var(--kino-superficie-{k});{"box-shadow:var(--kino-relieve-membrana)" if k == "membrana" else ""}"><b>{k}</b><small>{u}</small></div>' for k, u in capas)
    cuerpo = '\n'.join([
        sub('estructura.reticulas', 'Retículas', 'Una retícula por formato',
            'Todas comparten el mismo medianil de 24 (el paso <code>espacio-l</code>), salvo el teléfono, que usa 16.',
            '<div class="reticulas">'
            + _reticula('Teléfono', 4, 180, 360, 16, 16, 'Desde 360 px. El Pase ocupa las cuatro columnas.')
            + _reticula('Web', 12, 480, 300, 32, 24, 'Contenedor máximo de 1152 px; lectura en 720 px.')
            + _reticula('Presentación 16:9', 12, 480, 270, 40, 24, 'Titulares en 8 columnas; datos en 4.')
            + _reticula('Carta (impresos)', 6, 216, 280, 20, 12, 'Margen de 20 mm a escala. El PDF del Pase usa esta.')
            + '</div>' + traza('Constancia: el Pase se ve igual en el teléfono, la hoja y la pantalla de portería.')),
        sub('estructura.espaciado', 'Espaciado', 'Diez pasos de espacio',
            'Dentro de una tarjeta, <code>s</code> o <code>m</code>; entre tarjetas, <code>l</code>; entre secciones, <code>2xl</code> o más.',
            f'<ul class="espacios">{esp}</ul>'
            + casos(caso('<div class="esp-demo bien"><div class="kino-pase"><p class="kino-pase__quien">Andrés Gómez</p><p class="kino-pase__autor">Otorgó Carolina · Casa 14</p></div><div class="kino-pase"><p class="kino-pase__quien">Luz Marina</p><p class="kino-pase__autor">Colaborador · lun y jue</p></div></div>', 'Poco espacio dentro, más espacio entre tarjetas.'),
                    caso('<div class="esp-demo mal"><div class="kino-pase"><p class="kino-pase__quien">Andrés Gómez</p><p class="kino-pase__autor">Otorgó Carolina · Casa 14</p></div><div class="kino-pase"><p class="kino-pase__quien">Luz Marina</p><p class="kino-pase__autor">Colaborador · lun y jue</p></div></div>', 'El mismo espacio dentro y fuera: no se sabe qué va con qué.', False))),
        sub('estructura.radios', 'Radios', 'Radio 14 en tarjetas, 8 en controles, el arco solo en el Pase',
            'El arco es la forma del vano del logo. Si aparece en cualquier botón, deja de significar «esto es un Pase».',
            f'<div class="radios">{rad}</div>'
            + casos(caso(f'<div class="arco-demo"><div class="kino-pase__portal">{qr(5)}</div></div>', 'Arco en la ventana del QR: es un Pase.'),
                    caso('<div class="arco-demo"><button class="kino-accion arco-mal" type="button" tabindex="-1">Guardar límites</button></div>', 'Arco en un botón: la forma pierde su significado.', False))
            + traza('X8: radio 14 y arco solo en lo que es un Pase.')),
        sub('estructura.elevacion', 'Elevación', 'Cuatro capas de superficie y un solo resplandor',
            'En el tema oscuro la altura se nota por luminosidad: lo que está más cerca es más claro. La sombra casi no se ve; el borde de luz arriba sí.',
            f'<div class="capas">{elev}<div class="capa vigente"><b>resplandor vigente</b><small>Solo un Pase vigente.</small></div></div>'
            + traza('Estado honesto: el resplandor es un estado, así que solo lo lleva el Pase que el lector confirmó.')),
        sub('estructura.quiebres', 'Puntos de quiebre', 'Cuatro anchos y qué cambia en cada uno', '',
            tabla(['Nombre', 'Desde', 'Token', 'Qué cambia'], [
                ['Compacto', '<span class="mono">360 px</span>', '', 'Una columna; el índice se esconde; botones de ancho completo.'],
                ['Medio', f'<span class="mono">{PRIM["kino-quiebre-medio"]}</span>', '<code>--kino-quiebre-medio</code>', 'Dos columnas de tarjetas; la lista de Pases muestra la placa.'],
                ['Amplio', f'<span class="mono">{PRIM["kino-quiebre-amplio"]}</span>', '<code>--kino-quiebre-amplio</code>', 'Índice fijo a la izquierda; detalle del Pase al lado de la lista.'],
                ['Extenso', f'<span class="mono">{PRIM["kino-quiebre-extenso"]}</span>', '<code>--kino-quiebre-extenso</code>', 'Tres columnas en portería y en el panel de administración.'],
            ], 'Puntos de quiebre')
            + '<p class="nota">Los puntos de quiebre viven en tokens, pero CSS no acepta variables dentro de <code>@media</code>: en código se escriben con el mismo valor y un comentario que nombra el token.</p>'),
    ])
    return seccion('estructura', '08', 'Estructura', 'Identidad',
                   'Retículas, espaciado, radios, elevación y puntos de quiebre.',
                   'Para que una pantalla de teléfono y una hoja carta compartan medidas.',
                   'Al maquetar cualquier pieza.', cuerpo)
