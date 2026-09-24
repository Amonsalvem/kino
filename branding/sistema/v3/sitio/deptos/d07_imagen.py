from .comun import *  # noqa: F401,F403
import random

AURORA = ('radial-gradient(120% 80% at 85% 0%,color-mix(in oklch,var(--kino-biolum-d23) 75%,transparent),transparent 60%),'
          'radial-gradient(90% 70% at 0% 100%,color-mix(in oklch,var(--kino-violeta-d15) 80%,transparent),transparent 65%),'
          'radial-gradient(60% 50% at 40% 60%,color-mix(in oklch,var(--kino-indigo-d15) 50%,transparent),transparent 70%),var(--kino-sustrato-100)')


def celulas(ancho=400, alto=260, n=60, semilla=4):
    random.seed(semilla)
    c = [f'<svg class="celulas" viewBox="0 0 {ancho} {alto}" width="{ancho}" height="{alto}" style="aspect-ratio:{ancho}/{alto}" aria-hidden="true" preserveAspectRatio="xMidYMid slice">'
         f'<rect width="{ancho}" height="{alto}" style="fill:var(--kino-sustrato-200)"/>']
    for _ in range(n):
        x, y, r = random.uniform(0, ancho), random.uniform(0, alto), random.uniform(14, 40)
        c.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" style="fill:var(--kino-sustrato-300);stroke:var(--kino-sustrato-500)" stroke-width="1.5"/>'
                 f'<circle cx="{x + r * .2:.0f}" cy="{y - r * .15:.0f}" r="{r * .18:.0f}" style="fill:var(--kino-sustrato-400)"/>')
    c.append('</svg>')
    return ''.join(c)


def html_():
    recursos = [
        ('Aurora', f'<div class="img-muestra" style="background:{AURORA}"></div>', 'Luz verde e índigo que sube desde una esquina, como la bioluminiscencia en agua oscura.', 'Fondos de pantalla de inicio, portadas, redes, presentación comercial.'),
        ('Tejido celular', f'<div class="img-muestra">{celulas()}</div>', 'Células en sustrato: el conjunto como un organismo con membrana.', 'Solo en impresos grandes: carta de bienvenida, señalética, papelería.'),
        ('Membrana', '<div class="img-muestra" style="background:var(--kino-superficie-membrana);box-shadow:var(--kino-relieve-membrana) inset"></div>', 'Superficie lisa con un borde de luz arriba.', 'Tarjetas, el Pase, controles. Es el fondo de todo lo que se toca.'),
        ('Resplandor', '<div class="img-muestra centro"><span class="resplandor-demo"></span></div>', 'Halo verde alrededor de lo que está vivo.', 'Solo en un Pase vigente. En nada más.'),
    ]
    rec = ''.join(f'<figure class="recurso">{v}<figcaption><h3>{n}</h3><p>{q}</p><p class="nota">Dónde: {d}</p></figcaption></figure>' for n, v, q, d in recursos)
    usos = tabla(['Pieza', 'Aurora', 'Tejido celular', 'Membrana', 'Fotografía'], [
        ['App del residente', 'Pantalla de inicio', 'No', 'Sí', 'No'],
        ['Imagen del Pase', 'Cabecera, nunca detrás del QR', 'No', 'Sí', 'No'],
        ['Vista de portería', 'No: se lee en un segundo', 'No', 'Sí', 'No'],
        ['Redes y presentación', 'Sí', 'Detalle', 'Sí', 'Espacios sin personas'],
        ['Señalética y papelería', 'Portadas', 'Sí', 'No', 'No'],
    ], 'Cuándo usar cada recurso')
    cuerpo = '\n'.join([
        sub('imagen.direccion', 'Dirección de arte', 'Biopunk: la luz de lo vivo sobre un fondo oscuro',
            'Kino se ve como un laboratorio de noche: superficies de sustrato, luz que sale de lo que está vivo y formas redondas. Nada de metal, neón magenta ni pantallas de vigilancia.',
            f'<div class="recursos">{rec}</div>'
            + traza('F2 (dirección biopunk) y X7: aurora en pantalla, tejido celular solo en impresos grandes.')),
        sub('imagen.si-no', 'Qué sí y qué no', 'Cuatro pares para decidir rápido', '',
            casos(caso(f'<div class="img-caso" style="background:{AURORA}"><p class="img-titular">Cada Pase con autor y hora de salida</p></div>', 'Aurora detrás de un titular, con el texto sobre la zona oscura.'),
                  caso(f'<div class="img-caso" style="background:{AURORA}"><div class="img-qr">{qr(3)}</div></div>', 'Aurora detrás de un QR: el lector necesita fondo liso.', False),
                  caso('<div class="img-caso img-espacio"><span class="img-porton"></span><span class="img-luz"></span></div>', 'Un espacio del conjunto de noche, sin personas, con la entrada iluminada.'),
                  caso('<div class="img-caso img-camaras"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-camara"/></svg><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-camara"/></svg><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-camara"/></svg><span>Monitores de vigilancia</span></div>', 'Imágenes de vigilancia: Kino no vende miedo.', False),
                  caso('<div class="img-caso img-sin-rostro"><svg class="kino-icono" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-visita"/></svg><span class="kino-dato">Andrés Gómez · KMN 305</span></div>', 'La persona se nombra con su dato, no con su cara.'),
                  caso('<div class="img-caso img-foto-mal"><span class="img-rostro"></span><span class="kino-dato">Andrés Gómez</span></div>', 'Foto de rostro de una visita en una pieza.', False),
                  caso(f'<div class="img-caso" style="background:{AURORA}"><span class="img-aurora-limpia"></span></div>', 'Verde e índigo en tonos del sustrato.'),
                  caso('<div class="img-caso img-neon"></div>', 'Neón magenta y cian: otra marca.', False))),
        sub('imagen.texturas', 'Texturas y fondos', 'Tres fondos y cómo se arman', 'Todos salen de tokens: la aurora son tres degradados radiales sobre sustrato 100; el tejido, círculos en sustrato 300 a 500.',
            tabla(['Fondo', 'Receta', 'Contraste del texto encima'], [
                ['Aurora', 'biolum d23 al 75 % arriba a la derecha · violeta d15 al 80 % abajo a la izquierda · índigo d15 al 50 % al centro, sobre sustrato 100', f'Texto primario: Lc {abs(lc(hx("kino-hueso-100"), hx("kino-biolum-d23")))} en la zona más clara'],
                ['Tejido celular', 'Círculos de 14 a 40 px en sustrato 300 con borde sustrato 500 y núcleo sustrato 400', f'Texto primario: Lc {abs(lc(hx("kino-hueso-100"), hx("kino-sustrato-400")))} sobre un núcleo'],
                ['Membrana', 'Superficie membrana con relieve interior de 1 px', f'Texto primario: Lc {abs(lc(hx("kino-hueso-100"), hx("kino-superficie-membrana")))}'],
            ], 'Recetas de fondos')),
        sub('imagen.personas', 'Personas y espacios', 'Sin fotos de personas; los espacios, de noche y sin gente',
            'Kino maneja datos de quién entra a una casa. Una foto de una persona en una pieza de Kino sugiere que Kino guarda caras. Los espacios se muestran vacíos, a la hora en que más se usa la entrada.',
            '<ul class="reglas-cortas"><li>Personas: por nombre, ícono o silueta sin rasgos.</li><li>Espacios: entradas, talanqueras y senderos del conjunto, de noche, sin placas legibles ni rostros.</li><li>Ninguna foto muestra el logo o el nombre de un conjunto real.</li><li>El rostro solo aparece como dato marcado en violeta en la vista que lo necesita, nunca en marketing.</li></ul>'
            + traza('Discreto y Datos mínimos: 312 cédulas a la vista de portería fue un hallazgo; la marca no repite el error.')),
        sub('imagen.cuando', 'Cuándo usar cada recurso', 'Qué fondo va en cada pieza', '', usos),
    ])
    return seccion('imagen', '07', 'Imagen', 'Identidad',
                   'La dirección de arte: texturas, fondos y cómo se muestran personas y espacios.',
                   'Para elegir o producir imágenes que se vean de Kino y no de un banco de fotos.',
                   'Al armar una presentación comercial, una publicación en redes o una pieza impresa.', cuerpo)
