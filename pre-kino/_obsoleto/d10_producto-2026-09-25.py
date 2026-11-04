from .comun import *  # noqa: F401,F403

ESTADOS_UI = ['Reposo', 'Hover', 'Foco', 'Deshabilitado', 'Error', 'Carga']
NA = '<span class="na">No aplica</span>'


def _boton(es):
    base = {'Reposo': '', 'Hover': ' es-hover', 'Foco': ' es-foco', 'Deshabilitado': '', 'Error': None, 'Carga': ' es-carga'}[es]
    if base is None:
        return NA
    dis = ' disabled' if es == 'Deshabilitado' else ''
    txt = '<span class="kino-carga" aria-hidden="true"></span>Enviando…' if es == 'Carga' else 'Crear Pase'
    return f'<button class="kino-accion{base}" type="button" tabindex="-1"{dis}>{txt}</button>'


def _secundario(es):
    if es in ('Error', 'Carga'):
        return NA
    cls = {'Reposo': '', 'Hover': ' es-hover', 'Foco': ' es-foco', 'Deshabilitado': ''}[es]
    dis = ' disabled' if es == 'Deshabilitado' else ''
    return f'<button class="kino-boton{cls}" type="button" tabindex="-1"{dis}>Extender</button>'


def _campo(es):
    if es == 'Carga':
        return NA
    cls = {'Reposo': '', 'Hover': ' es-hover', 'Foco': ' es-foco', 'Deshabilitado': ' es-deshabilitado', 'Error': ' es-error'}[es]
    val = '300 555 014' if es == 'Error' else '300 555 0142'
    ayuda = ('<p class="kino-campo__error">Ese número tiene 9 cifras. Un celular en Colombia tiene 10.</p>' if es == 'Error'
             else '<p class="kino-campo__ayuda">Ahí le llega el Pase.</p>')
    return f'<div class="kino-campo{cls}"><span class="kino-campo__rot">WhatsApp de la visita</span><span class="kino-campo__caja kino-dato">{val}</span>{ayuda}</div>'


def _selector(es):
    if es in ('Error', 'Carga'):
        return NA
    cls = {'Reposo': '', 'Hover': ' es-hover', 'Foco': ' es-foco', 'Deshabilitado': ' es-deshabilitado'}[es]
    return (f'<div class="kino-selector{cls}" role="radiogroup" aria-label="Tipo de Pase"><span class="kino-selector__op" aria-checked="true">Visita</span>'
            f'<span class="kino-selector__op" aria-checked="false">Colaborador</span></div>')


def _tarjeta(es):
    if es == 'Deshabilitado':
        return NA
    if es == 'Carga':
        return '<div class="kino-pase es-carga-pase" aria-hidden="true"><span></span><span></span></div>'
    cls = {'Reposo': '', 'Hover': ' es-hover', 'Foco': ' es-foco', 'Error': ''}[es]
    est, txt = ('sin-confirmar', 'Sin confirmar') if es == 'Error' else ('vigente', 'Vigente')
    extra = '<p class="kino-campo__error">El lector no responde desde las 7:40 a. m.</p>' if es == 'Error' else ''
    return (f'<div class="kino-pase{cls}" data-estado="{est}"><div class="kino-pase__cabeza"><p class="kino-pase__quien">Andrés Gómez</p>{chip(est, txt)}</div>'
            f'<p class="kino-pase__pie"><span class="kino-dato">hasta 6:00 p. m.</span></p>{extra}</div>')


COMPONENTES = [('Botón de acción', _boton), ('Botón secundario', _secundario), ('Campo', _campo), ('Selector de tipo', _selector), ('Tarjeta de Pase', _tarjeta)]


def movil(titulo, cuerpo, pie='', clase=''):
    return (f'<figure class="movil {clase}"><div class="movil-pantalla en-oscuro"><div class="movil-barra"><span class="mono">9:41</span></div>'
            f'<div class="movil-cuerpo">{cuerpo}</div>{f"<div class=movil-pie>{pie}</div>" if pie else ""}</div><figcaption>{titulo}</figcaption></figure>')


def _crear():
    c = ('<p class="app-atras"><svg class="ic" aria-hidden="true"><use href="#i-atras"/></svg>Casa 14</p><h3 class="app-h">¿Quién viene?</h3>'
         + _selector('Reposo')
         + '<div class="kino-campo"><span class="kino-campo__rot">Nombre</span><span class="kino-campo__caja">Andrés Gómez</span></div>'
         + '<div class="kino-campo"><span class="kino-campo__rot">WhatsApp</span><span class="kino-campo__caja kino-dato">300 555 0142</span><p class="kino-campo__ayuda">Ahí le llega el Pase. No necesita instalar nada ni crear cuenta.</p></div>'
         + '<div class="kino-campo"><span class="kino-campo__rot">Cuándo</span><span class="kino-campo__caja">Hoy · de 2:00 a 6:00 p. m.</span><p class="kino-campo__ayuda">Las visitas entran de 6:00 a. m. a 10:00 p. m.</p></div>'
         + '<div class="kino-campo"><span class="kino-campo__rot">Placa (opcional)</span><span class="kino-campo__caja kino-dato">KMN 305</span></div>')
    return movil('Crear Pase', c, '<button class="kino-accion ancho" type="button" tabindex="-1">Crear Pase</button>')


def _lista():
    pases = [('Andrés Gómez', 'Visita', 'vigente', 'Vigente', 'hasta 6:00 p. m.', .62), ('Diana Arango', 'Visita', 'por-vencer', 'Por vencer', 'hasta 4:30 p. m.', .12),
             ('Técnico del gas', 'Visita', 'sin-confirmar', 'Sin confirmar', 'de 3:00 a 5:00 p. m.', 1), ('Luz Marina', 'Colaborador', 'previsto', 'Previsto', 'lun y jue · 7:00 a. m.', 1)]
    c = '<h3 class="app-h">Pases de la Casa 14</h3><div class="app-pestanas"><span aria-current="true">Activos</span><span>Anteriores</span></div>'
    for n, t, s, st, h, v in pases:
        barra = f'<span class="kino-vigencia" style="--kino-vida:{v}"><i></i></span>' if s in ('vigente', 'por-vencer') else ''
        c += (f'<div class="kino-pase" data-estado="{s}"><div class="kino-pase__cabeza"><p class="kino-pase__quien">{n}</p>{chip(s, st)}</div>'
              f'<p class="kino-pase__autor">{t}</p>{barra}<p class="kino-pase__pie"><span class="kino-dato">{h}</span></p></div>')
    return movil('Lista de Pases', c, '<button class="kino-accion ancho" type="button" tabindex="-1">Crear Pase</button>')


def _detalle():
    c = (f'<p class="app-atras"><svg class="ic" aria-hidden="true"><use href="#i-atras"/></svg>Pases</p>'
         f'<div class="kino-pase" data-estado="vigente"><div class="kino-pase__portal">{qr(11)}</div>'
         f'<div class="kino-pase__cabeza"><p class="kino-pase__quien">Andrés Gómez</p>{chip("vigente", "Vigente")}</div>'
         '<span class="kino-vigencia" style="--kino-vida:.62"><i></i></span>'
         '<dl class="app-datos"><div><dt>Vale</dt><dd>hoy de 2:00 a 6:00 p. m.</dd></div><div><dt>Placa</dt><dd class="kino-dato">KMN 305</dd></div>'
         '<div><dt>Código</dt><dd class="kino-dato">4817</dd></div><div><dt>Otorgó</dt><dd>Carolina Ruiz · Casa 14</dd></div></dl></div>'
         '<ol class="constancia"><li><span class="kino-dato">13:58</span>Enviado por WhatsApp</li><li><span class="kino-dato">14:03</span>El lector lo confirmó</li><li><span class="kino-dato">15:12</span>Entró con la placa KMN 305</li></ol>')
    return movil('Detalle de Pase', c, '<div class="app-botones"><button class="kino-boton" type="button" tabindex="-1">Extender</button><button class="kino-boton" type="button" tabindex="-1">Revocar</button></div>')


def _codigo():
    c = ('<div class="app-logo">' + logo('horizontal', etiqueta='Kino') + '</div>'
         '<h3 class="app-h">Entra con tu WhatsApp</h3><p class="app-p">Te enviamos un código por WhatsApp al 300 *** 0142.</p>'
         '<div class="codigo-cajas kino-dato" aria-label="Código de seis cifras"><span>4</span><span>8</span><span>2</span><span>9</span><span>1</span><span class="cursor"></span></div>'
         '<p class="kino-campo__error">Ese código no coincide. Revisa el último mensaje de Kino.</p>'
         '<p class="app-p nota">El código se puede pegar desde WhatsApp.</p>')
    return movil('Acceso por código', c, '<button class="kino-accion ancho" type="button" tabindex="-1">Entrar</button>')


def _limites():
    filas = [('Pases activos al mismo tiempo', '5', 'por casa ' + pend('unidad del cupo')), ('Duración máxima de una visita', '12 h', ''),
             ('Franja de visitas', '6:00 a. m. – 10:00 p. m.', ''), ('Franja de colaboradores', '6:00 a. m. – 7:00 p. m.', '')]
    campos = ''.join(f'<div class="kino-campo"><span class="kino-campo__rot">{n}</span><span class="kino-campo__caja kino-dato">{v}</span>{f"<p class=kino-campo__ayuda>{a}</p>" if a else ""}</div>' for n, v, a in filas)
    return (f'<figure class="escritorio"><div class="escritorio-pantalla en-oscuro"><aside class="esc-lado">{logo("horizontal", etiqueta="Kino")}<p class="mono">Administración</p>'
            '<ul><li>Resumen</li><li aria-current="true">Límites</li><li>Residentes</li><li>Lector</li></ul><p class="chip-dato">Refugio Campestre</p></aside>'
            '<div class="esc-cuerpo"><h3 class="app-h">Límites del conjunto</h3><p class="app-p">Aplican a los Pases nuevos. Los activos conservan su vigencia.</p>'
            f'<div class="esc-campos">{campos}</div><div class="esc-acciones"><button class="kino-boton" type="button" tabindex="-1">Guardar límites</button>'
            '<p class="app-ok">Límites guardados. Rigen desde hoy a las 4:32 p. m.</p></div>'
            '<div class="esc-resumen"><p class="mono">Esta semana <span class="nota">(ejemplo)</span></p><p><b class="cifra">214</b> Pases otorgados · <b class="cifra">187</b> usados · <b class="cifra">3</b> rechazados en la entrada</p></div>'
            '</div></div><figcaption>Límites de la administración · Kino Administración, trato de usted</figcaption></figure>')


WCAG = [
    ('1.4.1 Uso del color', 'Todo estado lleva palabra; el punto cambia de forma.', 'Chip de estado'),
    ('1.4.3 y 1.4.11 Contraste', 'APCA Lc 75 cuerpo, 60 grande, 30 no textual, y además WCAG 4,5:1 y 3:1. 112 pares medidos.', 'Color · Contraste APCA'),
    ('1.4.10 Reflujo', 'Todo se lee a 320 px sin desplazamiento horizontal.', 'Retícula de teléfono'),
    ('1.4.12 Espaciado de texto', 'Interlineado 1,6 y columna de 62 caracteres; nada se corta si el usuario los agranda.', 'Tipografía'),
    ('2.1.1 Teclado', 'Todo control se alcanza con Tab; el selector de tipo se mueve con flechas.', 'Selector de tipo'),
    ('2.4.7 y 2.4.11 Foco visible y no oculto', 'Anillo de 2 px en borde-foco con separación de 2 px; la barra inferior no tapa el campo enfocado.', 'Todos los controles'),
    ('2.5.7 Arrastre', 'Revocar y extender son botones, nunca un gesto de deslizar.', 'Detalle de Pase'),
    ('2.5.8 Tamaño del objetivo', 'Mínimo 48 × 48 px en la app; 24 × 24 es el mínimo de la norma.', 'Botones y chips táctiles'),
    ('3.3.1 Identificación de errores', 'El error dice qué pasó y qué hacer, debajo del campo, en texto.', 'Campo · Error'),
    ('3.3.7 Entrada redundante', 'Crear otro Pase repite los datos del anterior.', 'Pase vencido · Crear otro Pase'),
    ('3.3.8 Autenticación accesible', 'Código por WhatsApp que se puede pegar; no hay que recordar ninguna clave.', 'Acceso por código'),
    ('4.1.3 Mensajes de estado', 'Enviado, Sin confirmar y los errores se anuncian con <code>aria-live</code>.', 'Confirmación de envío'),
]


def html_():
    cab = ''.join(f'<th scope="col">{s}</th>' for s in ESTADOS_UI)
    filas = ''.join(f'<tr><th scope="row">{n}</th>' + ''.join(f'<td>{f(s)}</td>' for s in ESTADOS_UI) + '</tr>' for n, f in COMPONENTES)
    matriz = (f'<div class="tabla-envoltura matriz-env" role="region" aria-label="Componentes y sus estados" tabindex="0"><table class="tabla matriz en-oscuro">'
              f'<thead><tr><th scope="col">Componente</th>{cab}</tr></thead><tbody>{filas}</tbody></table></div>')
    cuerpo = '\n'.join([
        sub('producto.componentes', 'Componentes', 'Cinco componentes en sus seis estados',
            'Cada componente sale de <code>kino-brand.css</code> y solo usa variables. «No aplica» quiere decir que ese estado no existe para ese componente.',
            matriz
            + casos(caso('<button class="kino-accion" type="button" tabindex="-1">Crear Pase</button>', 'Un botón de acción por pantalla, con verbo y objeto.'),
                    caso('<div class="dos-verdes"><button class="kino-accion" type="button" tabindex="-1">Crear Pase</button><button class="kino-accion" type="button" tabindex="-1">Cancelar</button></div>', 'Dos botones verdes compiten; «Cancelar» va como secundario.', False))
            + descargas(descarga('kino-brand.css', 'kino-brand.css', (R / '../../kino-brand.css').read_text(encoding='utf8'), 'text/css'))
            + traza('X4: #00D595 solo en el botón que crea o entrega un Pase.')),
        sub('producto.pantallas', 'Pantallas clave', 'Las cinco pantallas donde se decide un ingreso',
            'Textos finales del inventario de UX writing. Nombres, placas y códigos son de ejemplo.',
            f'<div class="pantallas">{_crear()}{_lista()}{_detalle()}{_codigo()}</div>{_limites()}'
            + traza('Decide quien conoce (el residente otorga) y Topes a la vista (la administración fija límites, no aprueba).')),
        sub('producto.accesibilidad', 'Accesibilidad', 'WCAG 2.2 AA, criterio por criterio',
            'Los criterios que más afectan a Kino y cómo los cumple cada pieza.',
            tabla(['Criterio', 'Cómo lo cumple Kino', 'Dónde se ve'], [[a, b, c] for a, b, c in WCAG], 'Accesibilidad WCAG 2.2 AA')),
    ])
    return seccion('producto', '10', 'Producto', 'Aplicación',
                   'Los componentes de la app y las pantallas clave, con todos sus estados.',
                   'Para construir la app con piezas que ya resuelven foco, error, carga y accesibilidad.',
                   'Al diseñar o programar una pantalla de Kino.', cuerpo)
