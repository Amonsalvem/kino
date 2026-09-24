from .comun import *  # noqa: F401,F403

JERARQUIA = [
    ('Display', 'kino-display', 'texto-6', 'Archivo 800 al 112 %', 'Lc 45', 'Un Pase con autor.'),
    ('Título 1', 'kino-titulo t1', 'texto-5', 'Archivo 700 al 112 %', 'Lc 45', 'Pases de la Casa 14'),
    ('Título 2', 'kino-titulo t2', 'texto-3', 'Archivo 700 al 112 %', 'Lc 60', '¿Quién viene?'),
    ('Título 3', 'kino-titulo t3', 'texto-1', 'Archivo 700', 'Lc 60', 'Límites del conjunto'),
    ('Cuerpo', 'kino-texto', 'texto-0', 'Archivo 400', 'Lc 75', 'Ahí le llega el Pase. No necesita instalar nada ni crear cuenta.'),
    ('Pequeño', 'kino-texto pq', 'texto-n1', 'Archivo 400', 'Lc 75', 'Otorgó Carolina Ruiz · Casa 14'),
    ('Dato', 'kino-dato', 'texto-0', 'JetBrains Mono 500', 'Lc 75', '2:00 – 6:00 p. m. · 4817'),
    ('Placa', 'kino-placa', 'texto-3', 'JetBrains Mono 700', 'Lc 60', 'KMN 305'),
    ('Etiqueta', 'kino-etiqueta', 'texto-n1', 'JetBrains Mono 500, mayúsculas', 'Lc 75', 'Vence hoy'),
]


def html_():
    esc = ''.join(f'<tr><th scope="row" class="mono">texto-{("n" + str(-t["paso"])) if t["paso"] < 0 else t["paso"]}</th>'
                  f'<td class="mono">{t["minPx"]} → {t["maxPx"]} px</td><td><span class="esc-muestra" style="font-size:var(--kino-texto-{("n" + str(-t["paso"])) if t["paso"] < 0 else t["paso"]})">Pase</span></td>'
                  f'<td><code>{t["clamp"]}</code></td></tr>' for t in TIPO)
    escala = (f'<div class="tabla-envoltura" role="region" aria-label="Escala tipográfica" tabindex="0"><table class="tabla"><thead><tr><th scope="col">Token</th>'
              f'<th scope="col">360 → 1440 px</th><th scope="col">Muestra</th><th scope="col">CSS</th></tr></thead><tbody>{esc}</tbody></table></div>')
    jer = ''.join(f'<div class="jer"><p class="jer-rot mono">{n}<small>{tk} · {f} · mínimo {m}</small></p><p class="{c}">{e(ej)}</p></div>' for n, c, tk, f, m, ej in JERARQUIA)
    cuerpo = '\n'.join([
        sub('tipografia.familias', 'Familias', 'Archivo para leer, JetBrains Mono para comparar',
            'Dos familias libres (OFL 1.1). Archivo es variable en ancho: los titulares van al 112 %. JetBrains Mono tiene el cero barrado, que separa la O de la placa del 0 del código.',
            '<div class="familias"><div class="familia"><p class="fam-nombre" style="font-family:var(--kino-fuente-display);font-weight:800;font-stretch:112%">Archivo</p>'
            '<p class="fam-abc" style="font-family:var(--kino-fuente-texto)">Aa Bb Cc Ññ Áá 0123456789</p><p>Textos, titulares y botones. Pesos 400, 500, 700 y 800. Ancho 100 % en texto y 112 % en titulares.</p></div>'
            '<div class="familia"><p class="fam-nombre kino-dato" style="font-size:var(--kino-texto-5)">JetBrains Mono</p>'
            '<p class="fam-abc kino-dato">KMN 305 · O0 · 482 913 · 21:00</p><p>Placas, códigos, horas en datos, rótulos y cifras. Pesos 500 y 700, con cifras tabulares y cero barrado.</p></div></div>'
            + casos(caso('<span class="kino-placa">OOK 040</span>', 'Con cero barrado, la O y el 0 no se confunden.'),
                    caso('<span class="placa-sin" style="font-family:var(--kino-fuente-texto);font-size:var(--kino-texto-3);font-weight:700">OOK 040</span>', 'En Archivo, la placa se lee de dos maneras.', False))
            + traza('Exacto: el residente compara la placa y el código con lo que lee el lector (X5).')),
        sub('tipografia.escala', 'Escala', 'Ocho tamaños que crecen con la pantalla',
            'Escala con el método Utopia: 16 px con razón 1,2 en un teléfono de 360 px y 18 px con razón 1,26 en una pantalla de 1440 px. Entre los dos, <code>clamp()</code>.',
            escala + traza('Regla 6: los tamaños salen de tokens; ninguno se escribe a mano.')),
        sub('tipografia.jerarquias', 'Jerarquías', 'Nueve niveles y el contraste mínimo de cada uno', '', f'<div class="jerarquia">{jer}</div>'),
        sub('tipografia.reglas', 'Interlineado, tracking y columna', 'Medidas que no se tocan pieza por pieza', '',
            tabla(['Qué', 'Valor', 'Token'], [
                ['Interlineado de display', '1,04', '<code>--kino-interlinea-display</code>'],
                ['Interlineado de títulos', '1,16', '<code>--kino-interlinea-titulo</code>'],
                ['Interlineado de texto', '1,6', '<code>--kino-interlinea-texto</code>'],
                ['Tracking de display', '−0,02 em', '<code>--kino-tracking-display</code>'],
                ['Tracking de datos · placas · etiquetas', '0,04 · 0,06 · 0,08 em', '<code>--kino-tracking-*</code>'],
                ['Columna de texto', '62 caracteres (42 en tarjetas)', '<code>--kino-columna-texto</code>'],
              ], 'Reglas de interlineado, tracking y columna')
            + casos(caso('<p class="kino-texto col-bien">Carolina Ruiz, de la Casa 14, te dio un Pase para hoy de 2:00 a 6:00 p. m. Muéstralo en la entrada.</p>', 'Columna de 42 caracteres en una tarjeta: el ojo vuelve al inicio sin perderse.'),
                    caso('<p class="col-mal ej-mal">CAROLINA RUIZ, DE LA CASA 14, TE DIO UN PASE PARA HOY DE 2:00 A 6:00 P. M.</p>', 'Mayúsculas sostenidas, sin tracking y en un renglón que no termina.', False))),
        sub('tipografia.cifras', 'Cifras tabulares', 'Las horas se alinean en columna', 'En tablas, constancias y la vista de portería, las cifras ocupan el mismo ancho.',
            casos(caso('<ol class="horas kino-dato"><li>07:05</li><li>11:40</li><li>21:00</li></ol>', 'Mono con cifras tabulares: los dos puntos caen en la misma línea.'),
                  caso('<ol class="horas prop"><li>07:05</li><li>11:40</li><li>21:00</li></ol>', 'Cifras proporcionales: la columna se mueve.', False))
            + traza('V3: 24 h en datos, en mono, para que las cifras alineen.')),
        sub('tipografia.licencias', 'Licencias', 'Qué se puede instalar y qué no', '',
            tabla(['Fuente', 'Licencia', 'Dónde vive', 'Uso'], [
                ['Archivo', 'SIL Open Font License 1.1', 'Autoalojada en <code>branding/sistema/fonts/</code> y Google Fonts', 'Libre, también comercial. Se puede incrustar en PDF.'],
                ['JetBrains Mono', 'SIL Open Font License 1.1', 'Igual que Archivo', 'Libre, también comercial.'],
                ['Arkit ExtraBold', 'Sin información', 'Solo dentro de los contornos del logotipo', 'No se instala ni se usa para escribir ' + pend('licencia de Arkit ExtraBold') + '.'],
              ], 'Licencias tipográficas')),
    ])
    return seccion('tipografia', '05', 'Tipografía', 'Identidad',
                   'Las dos familias tipográficas y cómo se escriben placas y códigos.',
                   'Para que una placa y un código de un solo uso se lean igual en la app y en portería.',
                   'Al componer texto para pantalla o para impresión.', cuerpo)
