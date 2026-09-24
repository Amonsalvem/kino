from .comun import *  # noqa: F401,F403
from . import pase
from .d10_producto import _lista
from .d07_imagen import AURORA, celulas


def _app(n, titulo, pieza, texto, por='', medida=''):
    m = f'<span class="mono nota">{medida}</span>' if medida else ''
    return (f'<figure class="aplicacion" id="aplicaciones.{n}"><div class="ap-lienzo">{pieza}</div>'
            f'<figcaption><h3>{titulo}</h3>{m}<p>{texto}</p>{traza(por) if por else ""}</figcaption></figure>')


def _adhesivo():
    return (f'<div class="adhesivo en-oscuro"><div class="ad-logo">{logo("vertical", etiqueta="Kino")}</div>'
            f'<div class="ad-txt"><p class="ad-t">Avanza despacio</p><p>La cámara lee tu placa y la talanquera abre si tu Pase está vigente.</p></div></div>')


def _diapositiva():
    return (f'<div class="diapo en-oscuro" style="background:{AURORA}"><div class="in"><div class="dp-cab">{logo("horizontal", etiqueta="Kino")}<span class="kino-etiqueta">Para administraciones</span></div>'
            '<p class="dp-t">Su conjunto no registra quién autorizó cada ingreso.</p>'
            '<div class="dp-cifras"><div><b class="cifra">0<small>/312</small></b><span>personas reconocidas por el lector en una comunidad con el equipo instalado</span></div>'
            '<div><b class="cifra">711</b><span>errores de sincronización, todos por el campo correo</span></div></div>'
            '<p class="dp-fuente kino-dato">Inspección en Monte Sereno, sep 2026</p></div></div>')


def _una_pagina():
    return (f'<div class="hoja en-claro"><div class="in"><div class="hj-cab">{logo("horizontal", etiqueta="Kino")}<span class="kino-etiqueta">Kino para administraciones</span></div>'
            '<p class="hj-t">Cada ingreso con un Pase que tiene autor y hora de salida</p>'
            '<div class="hj-cols"><div><h4>Qué hace</h4><p>El residente le da un Pase a quien espera. La visita entra con QR, placa o código, sin crear cuenta. El lector que ya tiene el conjunto lo aplica.</p></div>'
            '<div><h4>Qué hace usted</h4><p>Fija los límites una vez: cuántos Pases a la vez, cuánto duran y en qué franja. Ya no aprueba ingresos uno por uno.</p></div>'
            '<div><h4>Qué necesita el conjunto</h4><p>Lectores de placa, rostro o QR sobre HikCentral. Kino se conecta a ellos.</p></div></div>'
            '<div class="hj-cifra"><b class="cifra">887 de 888</b><span>personas sincronizadas con el lector en Villas Campestres, Monte Sereno</span></div>'
            '<p class="hj-pie kino-dato">kino.co · ' + pend('datos de contacto') + '</p></div></div>')


def _redes():
    post = (f'<div class="red post en-oscuro" style="background:{AURORA}"><div class="in"><p class="rd-t">La señora del aseo entra lunes y jueves.</p>'
            f'<p>Su Pase se repite esos días y vence solo.</p><div class="rd-pie">{logo("horizontal", etiqueta="Kino")}</div></div></div>')
    historia = (f'<div class="red historia en-oscuro"><div class="in"><div class="rd-celulas">{celulas(180, 320, 30, 9)}</div><div class="rd-sobre">{pase.imagen("vigente", clase="mini")}'
                f'<p class="rd-t">El Pase llega por WhatsApp.</p><p>Sin instalar nada.</p></div></div></div>')
    return f'<div class="redes">{post}{historia}</div>'


def _correo():
    return ('<div class="correo en-claro"><div class="co-cab"><p><b>De</b> Kino &lt;resumen@kino.co&gt;</p><p><b>Asunto</b> Refugio Campestre · semana del 22 al 28 de septiembre</p></div>'
            f'<div class="co-cuerpo">{logo("horizontal", etiqueta="Kino")}<p>Buenos días. Este es el resumen de la semana en Refugio Campestre.</p>'
            '<ul class="co-cifras"><li><b class="cifra">214</b> Pases otorgados</li><li><b class="cifra">187</b> usados</li><li><b class="cifra">3</b> rechazados en la entrada</li></ul>'
            '<p>Los tres rechazos fueron Pases vencidos. Puede ver el detalle de cada uno en Kino Administración.</p>'
            '<p class="nota">Cifras de ejemplo.</p></div></div>')


def _papeleria():
    return (f'<div class="papeleria"><div class="membrete en-claro"><div class="in"><div class="mb-cab">{logo("horizontal", etiqueta="Kino")}</div>'
            '<p class="mb-fecha kino-dato">Medellín, 29 de septiembre de 2026</p><span class="mb-linea"></span><span class="mb-linea"></span><span class="mb-linea corta"></span>'
            f'<p class="mb-pie kino-dato">kino.co</p></div></div>'
            f'<div class="tarjeta-pres en-oscuro"><div>{logo("simbolo", etiqueta="Kino")}</div><div><p class="tp-n">Nombre Apellido</p><p class="kino-etiqueta">Equipo Kino</p>'
            '<p class="kino-dato">300 000 0000 · nombre@kino.co</p></div></div></div>')


def _credencial():
    return (f'<div class="credencial en-oscuro"><div class="cr-cab">{logo("horizontal", etiqueta="Kino")}</div><div class="cr-iniciales" aria-hidden="true">NA</div>'
            '<p class="cr-n">Nombre Apellido</p><p class="kino-etiqueta">Instalación y soporte</p>'
            '<p class="cr-dato kino-dato">Vigente hasta 2026-12-31</p><span class="kino-estado" data-estado="vigente">Vigente</span></div>')


def _bienvenida():
    return (f'<div class="hoja carta en-claro"><div class="in"><div class="hj-cab">{logo("horizontal", etiqueta="Kino")}<span class="chip-dato">Refugio Campestre</span></div>'
            '<p class="hj-t">Desde el lunes, las visitas entran con un Pase</p>'
            '<p>Cuando esperes a alguien, créale un Pase en Kino con su nombre, su WhatsApp y la hora. Le llega por WhatsApp y lo muestra en la entrada. No tiene que instalar nada.</p>'
            '<ol class="bv-pasos"><li><b>Entra a Kino</b> con el código que te llega por WhatsApp.</li><li><b>Crea el Pase</b>: visita o colaborador.</li><li><b>Tu visita lo muestra en la entrada</b>: QR, placa o código.</li></ol>'
            '<p>La administración fijó estos límites: 5 Pases activos a la vez y visitas de 6:00 a. m. a 10:00 p. m.</p>'
            '<p class="hj-pie">Administración de Refugio Campestre · con Kino</p></div></div>')


def html_():
    apps = ''.join([
        _app('app', 'App móvil', f'<div class="solo-movil">{_lista()}</div>', 'La lista de Pases de la Casa 14 con cuatro estados distintos.', 'Decide quien conoce.', '360 × 780 px'),
        _app('whatsapp', 'Mensaje de WhatsApp con el Pase', pase.whatsapp(), 'Una frase, la imagen del Pase y el enlace al Pase vivo.', 'V7: imagen más enlace; el PDF es opcional.', 'Mensaje de 23 palabras'),
        _app('pase-qr', 'Pase QR (imagen)', f'<div class="dos">{pase.imagen("vigente")}{pase.imagen("vigente", "Colaborador")}</div>', 'La imagen que se ve en el chat sin abrir nada. El QR vive en el arco del logo, sobre blanco.', 'X1: forma Portal.', '1080 × 1350 px'),
        _app('pase-vivo', 'Pase vivo', f'<div class="dos">{pase.vivo("vigente")}{pase.vivo("vencido")}</div>', 'La página del enlace. Dice si el Pase sigue sirviendo; en vencido ofrece llamar a quien lo dio.', 'Estado honesto y X11.', '360 px'),
        _app('pdf', 'PDF del Pase', pase.pdf(), 'Para imprimir o para quien no usa WhatsApp. Siempre en claro.', 'X3: el PDF va en claro.', 'Carta, 216 × 279 mm'),
        _app('senal', 'Señalética de la entrada', pase.senal(), 'Tres formas de entrar, leídas a dos metros. Abajo, qué pasa si el Pase venció.', 'X11 y el valor Decide quien conoce.', '60 × 40 cm'),
        _app('porteria', 'Vista de portería', pase.porteria(), 'Nombre, placa y estado. La cédula no aparece. En un rechazo, el turno puede llamar al residente.', 'Discreto y X11: la llamada no abre la entrada.', '1280 px'),
        _app('adhesivo', 'Adhesivo de talanquera', _adhesivo(), 'En el brazo o el poste de la talanquera, para quien entra en carro.', '', '20 × 10 cm, vinilo'),
        _app('presentacion', 'Presentación comercial', _diapositiva(), 'Para el consejo de administración: el problema con cifras propias y su fuente.', 'P10: el problema se cuenta con datos del conjunto piloto.', '1920 × 1080 px'),
        _app('una-pagina', 'Documento de una página', _una_pagina(), 'Lo que se deja después de la reunión con una administración. Trato de usted.', 'V1: usted con la administración.', 'Carta'),
        _app('redes', 'Plantillas de redes', _redes(), 'Una idea por pieza, con un caso concreto.', '', '1080 × 1080 y 1080 × 1920 px'),
        _app('correo', 'Correo a la administración', _correo(), 'Resumen semanal con cifras que tienen denominador.', 'Topes a la vista.', '600 px de ancho'),
        _app('papeleria', 'Papelería', _papeleria(), 'Hoja membretada y tarjeta de presentación.', '', 'Carta · 90 × 55 mm'),
        _app('credencial', 'Credencial', _credencial(), 'Para el equipo de Kino que instala y da soporte en un conjunto. Sin foto: iniciales y vigencia.', 'Datos mínimos.', '85,6 × 54 mm'),
        _app('bienvenida', 'Carta de bienvenida al conjunto', _bienvenida(), 'La recibe cada residente el día que el conjunto empieza con Kino. Trato de tú.', 'Tú con el residente (V1).', 'Carta'),
    ])
    cuerpo = '\n'.join([
        sub('aplicaciones.piezas', 'Piezas', 'Quince piezas con su medida y su uso',
            'Datos de ejemplo en todas. Las piezas físicas (señal, adhesivo, papelería, credencial) están en 2D: no hubo herramienta 3D disponible para los mockups ' + pend('mockups físicos en 3D') + '.',
            f'<div class="aplicaciones">{apps}</div>'),
        sub('aplicaciones.plantillas', 'Plantillas', 'Dónde están las plantillas para duplicar',
            'Las plantillas editables viven en la página «Aplicaciones / Plantillas» de la librería de Figma, ligadas a las variables. En código, las piezas del Pase salen de <code>deptos/pase.py</code>.',
            '<p><a class="descarga" href="https://www.figma.com/design/BO7UnDO9iE0aG6yUpNj0bc" rel="noopener">Abrir la librería de Figma</a></p>'),
    ])
    return seccion('aplicaciones', '11', 'Aplicaciones', 'Aplicación',
                   'Quince piezas con la marca aplicada, del Pase a la papelería.',
                   'Para duplicar una pieza aprobada y cambiar solo los datos.',
                   'Al producir una pieza nueva para un conjunto o para un aliado.', cuerpo)
