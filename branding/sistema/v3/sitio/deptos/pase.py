"""Piezas del Pase con la forma Portal (X1): imagen para WhatsApp, Pase vivo, PDF en claro,
señal de la entrada y vista de portería con «Llamar al residente» (X11).
Datos de ejemplo: Andrés Gómez, KMN 305, 4817, Carolina Ruiz, Casa 14, Refugio Campestre."""
from .comun import *  # noqa: F401,F403

EJ = dict(visita='Andrés Gómez', residente='Carolina Ruiz', casa='Casa 14', conjunto='Refugio Campestre',
          placa='KMN 305', codigo='4817', franja='Hoy · de 2:00 a 6:00 p. m.', enlace='kino.co/p/7Hq2')


def _ic(k):
    return f'<svg class="kino-icono" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-{k}"/></svg>'


def imagen(estado='vigente', tipo='Visita', clase=''):
    """La imagen que llega por WhatsApp (1080 × 1350). Se lee sin abrir nada."""
    colab = tipo == 'Colaborador'
    franja = 'lun y jue · de 7:00 a. m. a 5:00 p. m.' if colab else EJ['franja']
    nombre = 'Luz Marina Restrepo' if colab else EJ['visita']
    return f'''<div class="pieza-pase {clase}" data-estado="{estado}"><div class="in">
  <div class="pp-cab">{logo('horizontal', etiqueta='Kino')}<span class="pp-tipo">Pase · {tipo.lower()}</span></div>
  <div class="pp-portal">{qr(7)}</div>
  <p class="pp-nombre">{nombre}</p>
  <p class="pp-franja">{franja}</p>
  <dl class="pp-datos"><div><dt>Placa</dt><dd class="kino-dato">{EJ['placa'] if not colab else 'Sin placa'}</dd></div><div><dt>Código</dt><dd class="kino-dato">{EJ['codigo']}</dd></div>
  <div class="pp-ancho"><dt>Otorgó</dt><dd>{EJ['residente']} · {EJ['casa']}</dd></div></dl>
  <p class="pp-pie"><span class="chip-dato">{EJ['conjunto']}</span><span>Muéstralo en la entrada</span></p>
</div></div>'''


def whatsapp(tipo='Visita'):
    colab = tipo == 'Colaborador'
    txt = (f'{EJ["residente"]}, de la {EJ["casa"]}, te dio un Pase de colaborador: lunes y jueves, de 7:00 a. m. a 5:00 p. m. Muéstralo en la entrada: '
           if colab else f'{EJ["residente"]}, de la {EJ["casa"]}, te dio un Pase para hoy de 2:00 a 6:00 p. m. Muéstralo en la entrada: ')
    return (f'<div class="wa-chat"><div class="wa-msg">{imagen("vigente", tipo, "en-chat")}'
            f'<p>{txt}<a href="#aplicaciones.pase-vivo">{EJ["enlace"] if not colab else "kino.co/p/9Xc4"}</a></p><span class="wa-t">1:58 p. m.</span></div></div>')


INSTRUCCIONES = [('qr', 'QR', 'Acerca el QR al lector y espera la luz verde.'),
                 ('placa', 'Placa', f'Avanza despacio hasta la talanquera. La cámara lee la placa {EJ["placa"]}.'),
                 ('codigo', 'Código', f'Dile a portería el código {EJ["codigo"]}. Sirve una sola vez.')]


def vivo(estado='vigente', tema='en-oscuro'):
    """El Pase vivo: la página que abre el enlace. Dice si el Pase sigue sirviendo."""
    venc = estado == 'vencido'
    chip_ = chip('vencido', 'Vencido') if venc else chip('vigente', 'Vigente')
    # F4-P1 (A): la visita no llama desde aquí; la llamada queda en portería (X11) y el número del residente no se expone.
    cuerpo_estado = ('<p class="pv-aviso">Tu Pase valía de 2:00 a 6:00 p. m. y son las 7:10 p. m. Pídele uno nuevo a Carolina o pide en portería que la llamen.</p>'
                     if venc else
                     '<span class="kino-vigencia" style="--kino-vida:.62"><i></i></span><p class="pv-queda kino-dato">Vence a las 6:00 p. m.</p>'
                     '<ul class="pv-modos">' + ''.join(f'<li>{_ic(k)}<b>{n}</b><span>{t}</span></li>' for k, n, t in INSTRUCCIONES) + '</ul>'
                     '<button class="kino-boton ancho" type="button" tabindex="-1">' + _ic('bajar') + 'Descargar PDF</button>')
    return f'''<div class="pase-vivo {tema}" data-estado="{estado}">
  <div class="pv-barra">{logo('horizontal', etiqueta='Kino')}<span class="kino-dato">{EJ['enlace']}</span></div>
  <div class="pv-cuerpo">
    <div class="pv-cabeza">{chip_}<span class="chip-dato">{EJ['conjunto']}</span></div>
    <div class="kino-pase__portal pv-portal">{qr(7)}</div>
    <p class="pv-nombre">{EJ['visita']}</p>
    <p class="pv-franja">{EJ['franja']} · otorgó {EJ['residente']}</p>
    {cuerpo_estado}
  </div>
</div>'''


def pdf():
    """PDF opcional, en claro y tamaño carta, para imprimir o para quien no usa WhatsApp."""
    return f'''<div class="pase-pdf en-claro"><div class="in">
  <div class="pdf-cab">{logo('horizontal', etiqueta='Kino')}<span class="kino-etiqueta">Pase · visita</span></div>
  <div class="pdf-cuerpo">
    <div class="kino-pase__portal pdf-portal">{qr(7)}</div>
    <div class="pdf-info">
      <p class="pdf-nombre">{EJ['visita']}</p>
      <p class="pdf-franja">Lunes 29 de septiembre · de 2:00 a 6:00 p. m.</p>
      <dl class="pp-datos"><div><dt>Placa</dt><dd class="kino-dato">{EJ['placa']}</dd></div><div><dt>Código</dt><dd class="kino-dato">{EJ['codigo']}</dd></div>
      <div class="pp-ancho"><dt>Otorgó</dt><dd>{EJ['residente']} · {EJ['casa']}</dd></div><div class="pp-ancho"><dt>Conjunto</dt><dd>{EJ['conjunto']}</dd></div></dl>
    </div>
  </div>
  <ul class="pdf-modos">{''.join(f'<li>{_ic(k)}<b>{n}</b><span>{t}</span></li>' for k, n, t in INSTRUCCIONES)}</ul>
  <p class="pdf-pie kino-dato">Emitido 2026-09-29 13:58 · {EJ['enlace']} · Vence solo a las 18:00. El lector confirma cada ingreso.</p>
</div></div>'''


def senal(tema='en-oscuro'):
    """Señal física en la entrada de visitas (60 × 40 cm)."""
    return f'''<div class="senal-entrada {tema}"><div class="in">
  <div class="se-cab">{logo('horizontal', etiqueta='Kino')}<span class="kino-etiqueta">{EJ['conjunto']}<br>Entrada de visitas</span></div>
  <p class="se-titulo">Muestra tu Pase<br>al lector</p>
  <ul class="se-modos"><li>{_ic('qr')}<b>QR</b><span>Acércalo al lector</span></li><li>{_ic('carro')}<b>Placa</b><span>Avanza despacio</span></li><li>{_ic('codigo')}<b>Código</b><span>Díselo a portería</span></li></ul>
  <p class="se-vencido">{_ic('vencido')}Si tu Pase venció, portería puede llamar a quien te lo dio.</p>
</div></div>'''


def porteria(estado='vencido', tema='en-oscuro'):
    """Kino Portería: lo que ve el turno cuando alguien llega. Nombre, placa y estado; nunca la cédula."""
    eventos = [('15:12', 'Andrés Gómez', 'KMN 305', 'vigente', 'Entró', 'Casa 14'),
               ('15:40', 'Técnico del gas', 'QR', 'sin-confirmar', 'Sin confirmar', 'Casa 22'),
               ('19:10', 'Diana Arango', 'JRT 118', 'rechazado', 'Rechazado', 'Casa 14')]
    filas = ''.join(f'<li class="po-fila"><span class="kino-dato">{h}</span><b>{n}</b><span class="kino-dato">{p}</span><span>{c}</span>{chip(s, t)}</li>' for h, n, p, s, t, c in eventos)
    return f'''<div class="vista-porteria {tema}">
  <div class="po-barra">{logo('horizontal', etiqueta='Kino')}<b>Portería</b><span class="chip-dato">{EJ['conjunto']} · Entrada principal</span></div>
  <div class="po-cuerpo">
    <div class="po-alerta kino-pase" data-estado="rechazado">
      <div class="kino-pase__cabeza"><p class="kino-pase__quien">Diana Arango</p>{chip('rechazado', 'Rechazado')}</div>
      <p class="po-motivo">Pase vencido a las 6:00 p. m. · placa <span class="kino-dato">JRT 118</span> · otorgó Carolina Ruiz, Casa 14</p>
      <div class="po-acciones"><button class="kino-boton" type="button" tabindex="-1">{_ic('llamar')}Llamar al residente</button></div>
      <p class="nota">La llamada no abre la entrada. Si Carolina quiere que Diana entre, le da un Pase nuevo desde su app.</p>
    </div>
    <ol class="po-lista">{filas}</ol>
  </div>
</div>'''
