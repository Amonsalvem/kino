# Datos de las secciones 02–12 y del glosario. Genera contenido/02-12.html.
# Las secciones 02–12 están en construcción: se muestra qué contienen y su lector frío.
import html, json
D = [
 ("logo","03","Logo","Identidad",
  "El bloque con arco y gota, el logotipo «KINO» y sus versiones.",
  "Para poner la marca en cualquier superficie sin deformarla ni dejarla ilegible.",
  "Al poner la marca en una pantalla o mandar un archivo a imprenta.",
  ["Construcción sobre grilla y área de protección","Tamaños mínimos en pantalla e impresos","Versiones en color, negro, blanco y solo símbolo","Uso sobre seis tipos de fondo","Ocho usos incorrectos","Convivencia con el nombre del conjunto","Favicon, ícono de app y animación"],(1,6,3)),
 ("color","04","Color","Identidad",
  "La paleta y lo que significa cada color, incluidos los estados de un Pase.",
  "Para que un color signifique siempre lo mismo: activo, por vencer, usado, vencido o rechazado.",
  "Al elegir el color de cualquier texto, fondo, borde o gráfico.",
  ["Escalas de cada familia","Roles para superficies, texto y bordes","Temas oscuro y claro","Estados de un Pase","Paleta para datos y gráficos","Proporciones de uso","Contraste APCA de cada par","Revisión con daltonismo","Valores aproximados para impresión"],(3,2,4)),
 ("tipografia","05","Tipografía","Identidad",
  "Las dos familias tipográficas y cómo se escriben placas y códigos.",
  "Para que una placa y un código de un solo uso se lean igual en la app y en portería.",
  "Al componer texto para pantalla o para impresión.",
  ["Familia de texto y monoespaciada","Escala que crece con el ancho de pantalla","Jerarquías","Interlineado, tracking y largo de línea","Cifras tabulares","Licencias"],(3,3,0)),
 ("iconografia","06","Iconografía e ilustración","Identidad",
  "Los íconos de Kino y las reglas para dibujar uno nuevo.",
  "Para dibujar un Pase o una talanquera con el mismo trazo en la app y en la señalética.",
  "Al necesitar un ícono que todavía no está en la biblioteca.",
  ["Grilla, trazo, esquinas y tamaños","24 íconos base en SVG","Reglas de ilustración"],(0,2,1)),
 ("imagen","07","Imagen","Identidad",
  "La dirección de arte: fotografía, texturas y fondos.",
  "Para elegir o producir imágenes que se vean de Kino y no de un banco de fotos.",
  "Al armar una presentación comercial o una publicación en redes.",
  ["Dirección de arte","Qué sí y qué no, con ejemplos","Texturas y fondos","Personas y espacios","Cuándo usar cada recurso"],(0,1,4)),
 ("estructura","08","Estructura","Identidad",
  "Retículas, espaciado, radios y elevación.",
  "Para que una pantalla de teléfono y una hoja carta compartan medidas.",
  "Al maquetar cualquier pieza.",
  ["Retículas para web, móvil, presentación e impresos","Espaciado","Radios","Elevación","Puntos de quiebre"],(0,6,2)),
 ("motion","09","Motion","Identidad",
  "Cómo se mueve Kino y qué significa cada movimiento.",
  "Para que otorgar, confirmar, vencer y revocar un Pase se distingan también por su ritmo.",
  "Al animar una pantalla o el logo.",
  ["Principios","Duraciones y curvas","Coreografía y cascadas","Catálogo con diez animaciones en vivo","Animación del logo","Modo de movimiento reducido"],(3,2,1)),
 ("producto","10","Producto","Aplicación",
  "Los componentes de la app y las pantallas clave, con todos sus estados.",
  "Para construir la app con piezas que ya resuelven foco, error, carga y accesibilidad.",
  "Al diseñar o programar una pantalla de Kino.",
  ["Componentes con reposo, hover, foco, deshabilitado, error y carga","Crear Pase","Lista de Pases","Detalle de Pase","Límites de la administración","Acceso por código","Accesibilidad WCAG 2.2 AA"],(0,3,4)),
 ("aplicaciones","11","Aplicaciones","Aplicación",
  "La marca puesta en doce piezas reales.",
  "Para partir de una plantilla aprobada en vez de una hoja en blanco.",
  "Al producir una pieza nueva para un conjunto o para un aliado.",
  ["App móvil","Mensaje de WhatsApp con Pase","Pase QR","Señalética de portería","Adhesivo de talanquera","Presentación comercial","Documento de una página","Plantillas de redes","Correo","Papelería","Credencial","Carta de bienvenida al conjunto"],(0,3,9)),
 ("gobernanza","12","Gobernanza","Operación",
  "Quién decide sobre la marca y cómo se pide un archivo o un cambio.",
  "Para que la marca siga siendo una sola cuando la usen personas fuera del equipo.",
  "Antes de publicar una pieza o de proponer un cambio.",
  ["Quién decide","Cómo pedir archivos","Versiones","Registro de cambios","Lista de revisión antes de publicar","Pendientes","Centro de descargas"],(0,4,3)),
]
PEND = [
 ("Vector original del logo","No existe. Los SVG del sistema son reconstrucciones desde los PNG de 1543 × 1425 px, con 98 % de coincidencia."),
 ("Licencia de Arkit ExtraBold","Sin información. La fuente vive solo dentro de los contornos del logotipo."),
 ("Mensajes reales de portería y WhatsApp","No hay ninguno en los archivos. Sin ellos, las plantillas se escriben sin referencia de uso real."),
 ("Credencial temporal en HikCentral","Falta confirmar que acepte una credencial sin crear una persona. Es la prueba del Pase sin cuenta."),
 ("Unidad de los cupos","Por casa, por residente o por conjunto. Decisión de producto; bloquea los textos de límites."),
 ("Citas de las entrevistas con residentes","Las cinco entrevistas no tienen citas escritas. Las necesidades por actor se apoyan en la inspección."),
 ("Integración real de las apps de visitas","Neivor anuncia integración sin nombrar marcas de hardware. Falta verificar."),
]
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
]
e = html.escape
out = []
for (id_,num,tit,grupo,que,para,cuando,items,(c,s,f)) in D:
    lis = "".join(f"<li>{e(x)}</li>" for x in items)
    extra = ""
    if id_ == "gobernanza":
        filas = "".join(f'<li><strong>{e(a)}</strong><span>{e(b)}</span></li>' for a,b in PEND)
        extra = f'''
  <article class="sub" id="gobernanza.decide" data-titulo="Quién decide">
    <h2>Quién decide</h2>
    <p>El equipo de Kino decide sobre la marca. Una propuesta de cambio llega con la fila de la plataforma a la que responde; sin esa fila no se discute.</p>
  </article>
  <article class="sub" id="gobernanza.pendientes" data-titulo="Pendientes">
    <h2>Pendientes</h2>
    <p class="lede">Lo que falta para cerrar el sistema y por qué no se puede resolver todavía.</p>
    <ul class="pendientes">{filas}</ul>
  </article>'''
    out.append(f'''<section class="vista" id="{id_}" data-titulo="{e(tit)}" data-num="{num}" data-grupo="{e(grupo)}" hidden>
  <header class="abre">
    <p class="ojo">{num} · {e(grupo)}</p>
    <h1>{e(tit)}</h1>
    <dl class="lector">
      <div><dt>Qué es</dt><dd>{e(que)}</dd></div>
      <div><dt>Para qué sirve</dt><dd>{e(para)}</dd></div>
      <div><dt>Cuándo se usa</dt><dd>{e(cuando)}</dd></div>
    </dl>
  </header>
  <div class="obra" role="note">
    <p class="obra-rot"><span class="est-demo" data-e="sin-confirmar">En construcción</span></p>
    <p>Esta sección va a contener:</p>
    <ul class="contiene">{lis}</ul>
  </div>{extra}
</section>''')
g = "".join(f'<div class="termino" id="glosario.{k}" data-titulo="{e(t)}" data-glosario><dt>{e(t)}</dt><dd>{e(d)}</dd></div>' for k,t,d in GLOS)
out.append(f'''<section class="vista" id="glosario" data-titulo="Glosario" data-grupo="Consulta" hidden>
  <header class="abre">
    <p class="ojo">Consulta</p>
    <h1>Glosario</h1>
    <p class="lede">Los términos propios de Kino, en el sentido exacto en que se usan en la app, en los textos y en el código.</p>
  </header>
  <dl class="glosario">{g}</dl>
</section>''')
open("contenido/02-12.html","w").write("\n".join(out))
json.dump({"deptos":[(d[0],d[1],d[2],d[3]) for d in D]}, open("deptos.json","w"), ensure_ascii=False)
print("ok", sum(len(d[7]) for d in D))
