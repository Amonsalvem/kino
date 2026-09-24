# Genera contenido/03-12.html: los departamentos 03 a 12 (deptos/) y el glosario.
# Cada departamento vive en su módulo; los valores visuales salen de los tokens DTCG del cliente kino.
import html, json, pathlib
from deptos import d03_logo, d04_color, d05_tipografia, d06_iconografia, d07_imagen, d08_estructura, d09_motion, d10_producto, d11_aplicaciones, d12_gobernanza
R = pathlib.Path(__file__).parent
e = html.escape
DEPTOS = [d03_logo, d04_color, d05_tipografia, d06_iconografia, d07_imagen, d08_estructura, d09_motion, d10_producto, d11_aplicaciones, d12_gobernanza]
GLOS = [
 ("pase","Pase","Lo que recibe un visitante o un colaborador para entrar. Lleva quién lo otorgó, a quién, el motivo, la vigencia y el modo. Vence solo."),
 ("cuenta","Cuenta","Lo que tiene un residente para usar la app. Una visita nunca tiene cuenta."),
 ("acceso-previsto","Acceso previsto","Un Pase que el residente prepara antes de que llegue la persona."),
 ("residente","Residente","Quien vive en el conjunto, propietario o arrendatario. Tiene cuenta."),
 ("visitante","Visitante","Quien entra una vez o de vez en cuando con un Pase y sin cuenta."),
 ("colaborador","Colaborador","Quien trabaja en una casa o en el conjunto y entra con regularidad: aseo, jardinería, técnicos. Tiene la misma prioridad que la visita."),
 ("administracion","Administración","Quien compra Kino. Fija los límites del conjunto y ve la constancia de cada Pase."),
 ("porteria","Portería","El equipo de vigilancia de la entrada. Supervisa; el ingreso lo permite el lector."),
 ("lector","Lector","El dispositivo de la entrada que lee la placa, el QR, el código o el rostro y deja pasar."),
 ("limites","Límites","Cupos, duración y franjas que fija la administración para todos los Pases del conjunto."),
 ("cupo","Cupo","Cuántos Pases pueden estar activos a la vez. La unidad está pendiente: por casa, por residente o por conjunto."),
 ("franja","Franja","El horario en el que un Pase se puede usar."),
 ("vigencia","Vigencia","Desde cuándo y hasta cuándo vale un Pase."),
 ("modo","Modo","Cómo se presenta el Pase en la entrada: QR, placa o código."),
 ("codigo","Código de un solo uso","Número que sirve para entrar una vez. Después queda usado."),
 ("otorgar","Otorgar","Crear un Pase. Es la única acción que lleva el color de acento."),
 ("sin-confirmar","Sin confirmar","Estado de un Pase que el lector todavía no reconoce."),
 ("constancia","Constancia","La ficha que queda de cada Pase: quién lo otorgó, a quién, para qué y hasta cuándo."),
 ("conjunto","Conjunto","La copropiedad donde opera Kino. Aparece como dato: «Refugio Campestre · Casa 14»."),
 ("hikcentral","HikCentral","La plataforma de Hikvision que administra los lectores y la talanquera. Kino se conecta a ella."),
 ("lpr","LPR","Lectura de placas por cámara, del inglés License Plate Recognition."),
 ("visita","Visita","Tipo de Pase para quien entra una vez o de vez en cuando. En la interfaz se prefiere a «visitante»."),
 ("vigente","Vigente","Estado de un Pase activo que el lector confirmó."),
 ("usado","Usado","Estado de un código de un solo uso que ya sirvió para entrar."),
 ("vencido","Vencido","Estado de un Pase cuya vigencia terminó sin que nadie interviniera."),
 ("revocado","Revocado","Estado de un Pase que alguien cortó antes de que venciera. Queda el nombre de quien lo hizo."),
 ("rechazado","Rechazado","Intento de entrada que el lector no aceptó, con su motivo: fuera de franja, Pase vencido o no reconocido."),
 ("revocar","Revocar","Cortar un Pase antes de su vencimiento."),
 ("entrada","Entrada","El punto físico por donde se ingresa al conjunto: peatonal o vehicular."),
 ("talanquera","Talanquera","La barrera vehicular de la entrada, que abre cuando el lector reconoce la placa."),
 ("casa","Casa","La unidad del residente dentro del conjunto. Si el conjunto usa «apartamento», se escribe así."),
 ("qr","QR","Código gráfico que la visita muestra en el lector desde su teléfono."),

 ("previsto","Previsto","Estado de un Pase creado para una franja futura. Es el acceso previsto antes de que empiece."),
 ("por-vencer","Por vencer","Estado de un Pase vigente que entró en la ventana de aviso antes de su hora de salida."),
 ("portal","Forma Portal","La forma del Pase: el QR dentro del arco del logo, abierto por arriba como una entrada."),
 ("pase-vivo","Pase vivo","La página que abre el enlace del WhatsApp. Dice si el Pase sigue sirviendo."),
 ("aurora","Aurora","El fondo de luz verde e índigo sobre sustrato. Nunca detrás de un QR."),
 ("membrana","Membrana","La superficie de lo que se toca: controles, tarjetas y el Pase."),
 ("apca","APCA","Método de contraste que mide la legibilidad en Lc. Kino exige Lc 75 en texto de cuerpo."),
 ("token","Token","Un valor de diseño con nombre (color, tamaño, duración). Los tokens de Kino están en formato DTCG."),
]

out = [d.html_() for d in DEPTOS]
g = "".join(f'<div class="termino" id="glosario.{k}" data-titulo="{e(t)}" data-glosario><dt>{e(t)}</dt><dd>{e(d)}</dd></div>' for k,t,d in sorted(GLOS, key=lambda x: x[1].lower()))
out.append(f'''<section class="vista" id="glosario" data-titulo="Glosario" data-grupo="Consulta" hidden>
  <header class="abre">
    <p class="ojo">Consulta</p>
    <h1>Glosario</h1>
    <p class="lede">Los términos propios de Kino, en el sentido exacto en que se usan en la app, en los textos y en el código.</p>
  </header>
  <dl class="glosario">{g}</dl>
</section>''')
(R / "contenido/03-12.html").write_text("\n".join(out), encoding="utf8")
json.dump({"deptos": [(d.__name__.split("_",1)[1], d.__name__[7:9]) for d in DEPTOS]}, open(R / "deptos.json", "w"), ensure_ascii=False)
print("ok", len(GLOS), "términos ·", sum(len(o) for o in out)//1024, "KB")
