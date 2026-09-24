from .comun import *  # noqa: F401,F403

# Grilla de 24, área viva de 20 (margen 2), trazo 1,7, puntas y uniones redondas, radio de esquina 1.
ICONOS = [
    # Objetos
    ('pase', 'Pase', 'M5 3h14a1 1 0 0 1 1 1v16a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z M8 17v-5a4 4 0 0 1 8 0v5z'),
    ('qr', 'QR', 'M4 4h5v5H4z M15 4h5v5h-5z M4 15h5v5H4z M15 15h2v2h-2z M19.5 19.5h.01 M15 20h.01 M20 15v1'),
    ('placa', 'Placa', 'M3 7h18a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V8a1 1 0 0 1 1-1z M6 12h3 M11 12h2 M15 12h3'),
    ('codigo', 'Código', 'M4 7h16a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V8a1 1 0 0 1 1-1z M7.5 12h.01 M10.5 12h.01 M13.5 12h.01 M16.5 12h.01'),
    ('talanquera', 'Talanquera', 'M5 8v12 M3 20h4 M5 9h15v4H5 M9.5 9l-2 4 M14 9l-2 4 M18.5 9l-2 4'),
    ('camara', 'Cámara', 'M4 7h11a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V8a1 1 0 0 1 1-1z M16 10.5l5-2.5v8l-5-2.5'),
    ('rostro', 'Rostro', 'M4 8V5a1 1 0 0 1 1-1h3 M16 4h3a1 1 0 0 1 1 1v3 M20 16v3a1 1 0 0 1-1 1h-3 M8 20H5a1 1 0 0 1-1-1v-3 M9 10v1 M15 10v1 M9.5 15a3.5 3.5 0 0 0 5 0'),
    ('lector', 'Lector', 'M7 3h10a1 1 0 0 1 1 1v16a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z M9 6h6v5H9z M12 16.5h.01'),
    ('mensaje', 'Mensaje', 'M5 5h14a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H10l-5 4V6a1 1 0 0 1 1-1z M9 10h6'),
    ('carro', 'Vehículo', 'M3 16v-4l2.5-5h13L21 12v4z M3 12h18 M7 19a1.5 1.5 0 0 0 0-3 M17 19a1.5 1.5 0 0 0 0-3 M7 19a1.5 1.5 0 0 1 0-3 M17 19a1.5 1.5 0 0 1 0-3'),
    ('limites', 'Límites', 'M4 7h9 M17 7h3 M4 17h3 M11 17h9 M15 5v4 M9 15v4'),
    ('constancia', 'Constancia', 'M6 3h8l4 4v14H6z M14 3v4h4 M9 14l2 2 4-4'),
    # Personas
    ('residente', 'Residente', 'M3 11l9-7 9 7 M5 9.5V20h14V9.5 M12 14.5a2 2 0 1 0 0-4 2 2 0 0 0 0 4z M8.5 20a3.5 3.5 0 0 1 7 0'),
    ('visita', 'Visita', 'M9 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6z M3 20a6 6 0 0 1 12 0 M16 12h5 M19 10l2 2-2 2'),
    ('colaborador', 'Colaborador', 'M9 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6z M3 20a6 6 0 0 1 10-4.5 M16 15h5v5h-5z M17.5 15v-1.5h2V15'),
    ('administracion', 'Administración', 'M4 21V5l8-2v18 M12 9l8 2v10 M3 21h18 M7 8h2 M7 12h2 M7 16h2 M15 13h2 M15 17h2'),
    ('porteria', 'Portería', 'M4 20V6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v14 M2 20h20 M7 8h10v5H7z M12 16v4'),
    # Estados
    ('previsto', 'Previsto', 'M4 6h16v14H4z M4 10h16 M8 4v4 M16 4v4 M9 15h6'),
    ('sin-confirmar', 'Sin confirmar', 'M12 3a9 9 0 0 1 4.5 1.2 M19.8 7.5A9 9 0 0 1 21 12 M19.8 16.5a9 9 0 0 1-3.3 3.3 M12 21a9 9 0 0 1-4.5-1.2 M4.2 16.5A9 9 0 0 1 3 12 M4.2 7.5a9 9 0 0 1 3.3-3.3'),
    ('vigente', 'Vigente', 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18z M8 12.5l2.7 2.7L16 10'),
    ('por-vencer', 'Por vencer', 'M7 3h10 M7 21h10 M8 3c0 4 8 5 8 9s-8 5-8 9 M16 3c0 4-8 5-8 9s8 5 8 9'),
    ('usado', 'Usado', 'M4 7h16v3a2 2 0 0 0 0 4v3H4v-3a2 2 0 0 0 0-4z M9 12l2 2 4-4'),
    ('vencido', 'Vencido', 'M21 12a9 9 0 1 1-3-6.7 M12 7v5h3'),
    ('revocado', 'Revocado', 'M6 3h12a1 1 0 0 1 1 1v16a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z M3 21L21 3'),
    ('rechazado', 'Rechazado', 'M20 4v16 M16 12H4 M8 8l-4 4 4 4'),
    ('identidad', 'Dato personal', 'M3 6h18v12H3z M8.5 12a2 2 0 1 0 0-4 2 2 0 0 0 0 4z M5.5 16a3 3 0 0 1 6 0 M14 9h4 M14 13h4'),
    # Navegación y acciones
    ('inicio', 'Inicio', 'M3 11l9-7 9 7 M5 10v10h14V10 M10 20v-6h4v6'),
    ('atras', 'Atrás', 'M15 5l-7 7 7 7'),
    ('flecha', 'Siguiente', 'M5 12h14 M13 6l6 6-6 6'),
    ('menu', 'Menú', 'M4 7h16 M4 12h16 M4 17h16'),
    ('buscar', 'Buscar', 'M11 17a6 6 0 1 0 0-12 6 6 0 0 0 0 12z M20 20l-4.5-4.5'),
    ('ajustes', 'Ajustes', 'M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6z M12 3v3 M12 18v3 M3 12h3 M18 12h3 M5.6 5.6l2.1 2.1 M16.3 16.3l2.1 2.1 M5.6 18.4l2.1-2.1 M16.3 7.7l2.1-2.1'),
    ('crear', 'Crear', 'M12 5v14 M5 12h14'),
    ('cerrar', 'Cerrar', 'M6 6l12 12 M18 6L6 18'),
    ('compartir', 'Compartir', 'M12 15V4 M8 8l4-4 4 4 M5 13v6a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-6'),
    ('bajar', 'Descargar', 'M12 4v11 M8 11l4 4 4-4 M5 20h14'),
    ('llamar', 'Llamar', 'M5 4h3.5l1.8 4.5-2.3 1.4a10 10 0 0 0 5.1 5.1l1.4-2.3L19 14.5V18a2 2 0 0 1-2 2A14 14 0 0 1 3 6a2 2 0 0 1 2-2z'),
]
GRUPOS = [('Objetos', 0, 12), ('Personas', 12, 17), ('Estados', 17, 26), ('Navegación y acciones', 26, len(ICONOS))]


def svg_icono(d, tam=24, hex_color=None):
    col = hex_color or 'currentColor'
    ns = 'xmlns="http://www.w3.org/2000/svg" ' if hex_color else ''
    return (f'<svg {ns}viewBox="0 0 24 24" width="{tam}" height="{tam}" fill="none" stroke="{col}" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round"><path d="{d}"/></svg>')


def simbolos():
    """Sprite de los íconos base para el sitio (se agregan como i-<id>)."""
    return ''.join(f'<symbol id="i-{k}" viewBox="0 0 24 24"><path d="{d}"/></symbol>' for k, _, d in ICONOS)


def html_():
    color = hx('kino-hueso-100')
    grupos = ''
    for nombre, a, b in GRUPOS:
        celdas = ''.join(
            f'<li><a class="icono-celda" href="{data_uri(svg_icono(d, 24, color))}" download="kino-icono-{k}.svg" title="Descargar {e(n)} en SVG">'
            f'<svg class="kino-icono" viewBox="0 0 24 24" aria-hidden="true"><path d="{d}"/></svg><span>{e(n)}</span></a></li>'
            for k, n, d in ICONOS[a:b])
        grupos += f'<h3 class="sub-h">{nombre}</h3><ul class="iconos">{celdas}</ul>'
    sprite = ('<svg xmlns="http://www.w3.org/2000/svg" style="display:none"><defs>'
              + ''.join(f'<symbol id="kino-{k}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="{d}"/></symbol>' for k, _, d in ICONOS)
              + '</defs></svg>')
    grid = ''.join(f'<line x1="{i}" y1="0" x2="{i}" y2="24"/><line x1="0" y1="{i}" x2="24" y2="{i}"/>' for i in range(25))
    anatomia = (f'<svg class="ic-anatomia" viewBox="-1 -1 26 26" width="312" height="312" style="aspect-ratio:1" role="img" aria-label="Ícono del Pase sobre la grilla de 24 con el área viva de 20">'
                f'<g class="ic-grilla">{grid}</g><rect class="ic-viva" x="2" y="2" width="20" height="20"/>'
                f'<path class="ic-trazo" d="{ICONOS[0][2]}"/></svg>')
    tam = ''.join(f'<figure><svg class="kino-icono" style="width:{t}px;height:{t}px" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-pase"/></svg><figcaption class="mono">{t}</figcaption></figure>' for t in (16, 20, 24, 32, 48))
    cuerpo = '\n'.join([
        sub('iconografia.grilla', 'Grilla y trazo', 'Veinticuatro unidades, trazo 1,7, puntas redondas',
            'Cada ícono se dibuja en una grilla de 24 con 2 de margen. El trazo es de 1,7 unidades con puntas y uniones redondas, como las curvas del logo.',
            f'<div class="ic-construye">{anatomia}<div>'
            + tabla(['Medida', 'Valor', 'Token'], [
                ['Grilla', '24 × 24', ''], ['Área viva', '20 × 20', ''],
                ['Trazo', '1,7', '<code>--kino-forma-trazo-icono</code>'], ['Puntas y uniones', 'redondas', ''],
                ['Radio de esquina', '1', ''], ['Tamaños', '16 · 20 · 24 · 32 · 48 px', ''],
              ], 'Medidas de los íconos')
            + f'<div class="ic-tamanos">{tam}</div></div></div>'
            + casos(caso(f'<svg class="kino-icono" style="width:48px;height:48px" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-talanquera"/></svg>', 'Trazo 1,7 con puntas redondas.'),
                    caso(f'<svg style="width:48px;height:48px;fill:none;stroke:currentColor;stroke-width:3;stroke-linecap:butt;stroke-linejoin:miter" viewBox="0 0 24 24" aria-hidden="true"><path d="{ICONOS[4][2]}"/></svg>', 'Trazo 3 con puntas rectas: otra familia de íconos.', False))
            + traza('X6: trazo 1,7 con puntas redondas, por las curvas del logo.')),
        sub('iconografia.base', 'Íconos base', f'{len(ICONOS)} íconos para empezar',
            'Toca un ícono para descargarlo en SVG. El sprite trae todos con <code>currentColor</code>, listos para <code>&lt;use&gt;</code>.',
            grupos + descargas(descarga('Sprite completo', 'kino-iconos.svg', sprite))
            + traza('Exacto: cada objeto del producto (Pase, placa, código, lector) tiene un ícono propio y uno solo.')),
        sub('iconografia.ilustracion', 'Ilustración', 'Membranas y portales, nunca candados',
            'Kino no se dibuja como una fortaleza. La ilustración usa el arco del logo, la membrana y la luz de la aurora. Los colores de estado solo aparecen cuando nombran un estado.',
            casos(caso('<div class="ilus-bien"><span class="ilus-arco"></span><svg class="kino-icono" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-visita"/></svg></div>', 'La visita cruza un arco: el Pase abre una entrada.'),
                  caso('<div class="ilus-mal"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-candado"/></svg><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-escudo"/></svg></div>', 'Candados y escudos prometen una seguridad que Kino no vende.', False),
                  caso('<div class="ilus-bien"><svg class="kino-icono" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-pase"/></svg><span class="kino-estado" data-estado="vigente">Vigente</span></div>', 'Verde solo junto a un estado Vigente.'),
                  caso('<div class="ilus-mal verde"><svg class="kino-icono" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-residente"/></svg><svg class="kino-icono" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-carro"/></svg></div>', 'Íconos pintados de verde por decoración.', False))
            + '<ul class="reglas-cortas"><li>Figuras de personas sin rostro ni rasgos: Kino no guarda fotos de visitas en la interfaz.</li><li>Relleno solo con superficie membrana; nunca degradados en el ícono.</li><li>Una ilustración explica un paso del Pase o no va.</li></ul>'
            + traza('Regla de marca 10: sin candados, escudos ni muros. Discreto: la persona no se retrata.')),
    ])
    return seccion('iconografia', '06', 'Iconografía e ilustración', 'Identidad',
                   'Los íconos de Kino y las reglas para dibujar uno nuevo.',
                   'Para dibujar un Pase o una talanquera con el mismo trazo en la app y en la señalética.',
                   'Al necesitar un ícono que todavía no está en la biblioteca.', cuerpo)
