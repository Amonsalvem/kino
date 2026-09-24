#!/usr/bin/env python3
"""Fuente única del departamento Verbal.
Genera:
  contenido/02-verbal.html          sección del sitio
  build/guia-de-contenido.md        → gorr-brand-system/clientes/kino/02-verbal/guia-de-contenido.md
  build/ux-writing.md               inventario antes → después → por qué, con conteo de palabras
  build/muestras-ux.md              textos «después», uno por línea, para npm run voz
  build/verbal-verificacion.json    límites de largo y tratamiento por audiencia
Tratamiento con la administración y mayúscula de «Pase»: PROPUESTA de la Parada 2.
"""
import html, json, re, pathlib
R = pathlib.Path(__file__).parent
e = html.escape
def palabras(t):
    t = re.sub(r'\{[^}]+\}', 'X', t)
    return len([w for w in re.split(r'\s+', t.strip()) if re.search(r'[\wÁÉÍÓÚáéíóúñÑ0-9]', w)])

# ───────────────────────── Perfil NN/g ─────────────────────────
PERFIL = [
 ("Formalidad", 2, "formal", "casual", "Frases completas y sin jerga. Con el residente y la visita, tuteo y oraciones cortas.", "Andrés entra hoy de 2:00 a 6:00 p. m."),
 ("Humor", 1, "serio", "divertido", "Hablamos de quién entra a la casa de alguien. Ningún estado, error o aviso lleva chiste.", "El lector no leyó la placa KMN 305. Muestra el QR."),
 ("Respeto", 1, "respetuoso", "irreverente", "Describimos lo que pasó, nunca a quién se le olvidó.", "El número 300 555 0142 no tiene WhatsApp. Revísalo o copia el código."),
 ("Entusiasmo", 2, "sobrio", "entusiasta", "Confirmamos con el dato en vez de celebrar.", "Enviado. Vale hasta las 6:00 p. m."),
]

# ───────────────────────── Tono por contexto ─────────────────────────
TONO = [
 ("App del residente", "tú", "Directo y breve. El dato primero: nombre, hora, placa.", "Andrés recibió el Pase. Vale hoy de 2:00 a 6:00 p. m.", "¡Genial! Tu invitado ya puede ingresar sin problemas."),
 ("WhatsApp a la visita", "tú", "Quien lo recibe no conoce Kino. Primero quién le da el Pase; después qué hacer en la entrada.", "Hola, Andrés. Carolina Ruiz, de la Casa 14, te dio un Pase para hoy de 2:00 a 6:00 p. m.", "Estimado usuario, ha sido registrado en nuestra plataforma de seguridad."),
 ("Portería", "impersonal", "Frases de lectura en un segundo, en la vista de portería y en la señalética de la entrada. Verbo y objeto.", "Pase vigente · Andrés Gómez · KMN 305", "Usuario autorizado por el sistema de control."),
 ("Comercial", "usted (propuesta)", "Para la administración y el consejo. Cifras con denominador y fuente.", "Hoy su conjunto no sabe quién autorizó cada ingreso. Con Kino, cada Pase tiene autor y hora de salida.", "Transforme la seguridad de su conjunto con una solución innovadora."),
 ("Soporte", "el de la audiencia", "Qué pasó, qué hacer y en cuánto tiempo. Sin disculpas en cadena.", "El lector de Refugio Campestre no responde desde las 7:40 a. m. Los Pases nuevos quedan sin confirmar.", "Lamentamos mucho las molestias ocasionadas. Estamos trabajando para solucionarlo."),
 ("Redes", "tú", "Una idea por pieza, con un caso concreto. Nada de promesas absolutas.", "La señora del aseo entra lunes y jueves. Su Pase se repite esos días y vence solo.", "La seguridad total para tu hogar está a un clic."),
]

# ───────────────────────── Vocabulario ─────────────────────────
USAR = [
 ("Pase", "Lo que recibe una visita o un colaborador para entrar. Autor, motivo, vigencia y modo."),
 ("cuenta", "Lo que tiene el residente para usar la app."),
 ("visita", "Quien entra una vez o de vez en cuando. En la interfaz se prefiere a «visitante»."),
 ("colaborador", "Quien entra con regularidad a trabajar: aseo, jardinería, técnicos."),
 ("acceso previsto", "Pase preparado antes de que llegue la persona."),
 ("otorgar", "Crear un Pase. Solo el residente otorga."),
 ("revocar", "Cortar un Pase antes de que venza. Siempre con autor."),
 ("vencer", "Terminar la vigencia sin que nadie intervenga."),
 ("vigente", "Pase activo que el lector confirmó."),
 ("sin confirmar", "Pase enviado que el lector todavía no reconoce."),
 ("usado", "Código de un solo uso que ya sirvió para entrar."),
 ("lector", "El equipo de la entrada que reconoce placa, QR, código o rostro."),
 ("entrada", "El punto físico por donde se ingresa al conjunto."),
 ("límites", "Cupos, duración y franjas que fija la administración."),
 ("cupo", "Cuántos Pases pueden estar activos a la vez. Unidad [PENDIENTE]."),
 ("franja", "Horario en que un Pase se puede usar."),
 ("constancia", "La ficha que queda de cada Pase."),
 ("casa", "La unidad del residente. «Apartamento» si el conjunto lo usa así; es un dato del conjunto."),
 ("administración", "Quien compra Kino y fija los límites."),
 ("portería", "El equipo de vigilancia. Supervisa la entrada."),
]
NO_MEZCLAR = [
 ("Pase", "cuenta", "El Pase es de la visita o el colaborador y vence. La cuenta es del residente."),
 ("vencer", "revocar", "Vencer ocurre solo; revocar lo decide alguien y queda su nombre."),
 ("lector", "portería", "El lector deja entrar; portería supervisa. Nunca «el vigilante autorizó»."),
 ("visita", "colaborador", "Son tipos de Pase distintos, con el mismo peso en la interfaz."),
 ("sin confirmar", "pendiente", "No hay nada pendiente de aprobación: el lector aún no responde."),
]
EVITAR = [
 ("permiso", "Pase", "El objeto se llama Pase (decisión F3)."),
 ("usuario (para la visita)", "visita o el nombre de la persona", "La visita no tiene cuenta."),
 ("invitado", "visita", "No todos los que entran son invitados: un técnico entra a trabajar."),
 ("autorizar / aprobar (administración)", "fijar límites", "La administración no aprueba ingresos."),
 ("acceso concedido / permitido", "vigente, con la hora", "Afirma algo que la puerta tal vez no confirmó."),
 ("empleada doméstica", "colaborador, o su nombre", "Término de rol que reduce a la persona."),
 ("guardia / celador", "portería", "Nombra una función del conjunto, no un cargo."),
 ("contraseña", "código por WhatsApp", "El ingreso a la app es con un código que llega por WhatsApp."),
 ("seguridad total / 100 % seguro", "lo que Kino registra, con cifra", "Promesa que ningún sistema cumple."),
 ("¡Listo! / ¡Éxito!", "el dato que confirma", "Celebrar no dice qué pasó."),
 ("Arcana", "Kino", "Nombre anterior."),
 ("marca blanca", "Kino", "Kino tiene identidad propia (decisión F4)."),
]

# ───────────────────────── Guía de estilo ─────────────────────────
ESTILO = [
 ("Horas en texto", "9:00 p. m. · 7:30 a. m.", "21:00 · 9pm · 9 PM", "Con dos puntos, minutos siempre, «a. m.» y «p. m.» con espacio y puntos. Es como se lee la hora en Colombia."),
 ("Horas en datos", "21:00 (mono, en tablas, constancia y exportes)", "9:00 p. m. en una columna", "En columnas de datos, 24 horas en JetBrains Mono para que las cifras alineen."),
 ("Rangos de hora", "de 2:00 a 6:00 p. m.", "2-6pm · 14:00-18:00 en un mensaje", "«de… a…» en texto; guion corto solo en datos (14:00–18:00)."),
 ("Fechas en la app", "lun 29 sep · hoy · mañana", "29/09/2026 · Monday", "Día abreviado y fecha. «Hoy» y «mañana» siempre acompañados de la hora."),
 ("Fechas en mensajes", "el lunes 29 de septiembre", "el 29/09", "En WhatsApp y correo, completa y sin año si es el año en curso."),
 ("Fechas en exportes", "2026-09-29", "29 sep", "ISO 8601 en archivos y registros."),
 ("Números", "1.200 personas · 47,88 %", "1,200 · 47.88%", "Punto de miles, coma decimal, espacio antes de %. Cifras con denominador: 0 de 312."),
 ("Placas", "KMN 305", "kmn-305 · KMN305", "Mayúsculas, un espacio, en mono. Así la compara el residente con lo que lee el lector."),
 ("Códigos", "4817 · 482 913", "4-8-1-7", "Grupos de tres cuando pasan de cuatro cifras. Siempre en mono."),
 ("Teléfonos", "300 555 0142", "+573005550142", "Grupos 3-3-4. El indicativo solo si el número es de otro país."),
 ("Mayúsculas", "Crear Pase · Registrar vehículo", "Registrar Vehículo · CREAR PASE", "Tipo oración. «Pase» y «Kino» con mayúscula; nada en mayúsculas sostenidas salvo placas y siglas."),
 ("Puntuación", "Enviado. Vale hasta las 6:00 p. m.", "¡Enviado!", "Sin exclamaciones. Signo de apertura en preguntas. Botones sin punto."),
 ("Siglas", "QR, LPR, SIC", "Q.R. · L.P.R.", "Sin puntos. La primera vez en un documento, desarrollada: lectura de placas (LPR)."),
 ("Lenguaje inclusivo", "quien viene · la persona · el equipo de portería", "l@s visitantes · lxs · les", "Se nombra a la persona o se usa un colectivo. Sin arroba, x ni e."),
 ("El conjunto", "Refugio Campestre · Casa 14", "el logo del conjunto", "El conjunto es un dato en texto o chip, en ese orden: conjunto · unidad."),
]

# ───────────────────────── UX writing ─────────────────────────
# (grupo, momento, tipo, antes, despues, error, por_que, limite)   limite: boton=3, estado=20, wa=45
UX = [
 ("Residente","Crear un Pase · botón","boton","No existe. Hoy solo «Registrar Vehículo» o, en administración, «Crear Usuario»","Crear Pase",None,"Verbo y objeto. Es el único botón con color de acento.",3),
 ("Residente","Crear un Pase · pregunta de la pantalla","estado","No existe","¿Quién viene?",None,"La pregunta que el residente sí sabe responder.",20),
 ("Residente","Crear un Pase · campo de WhatsApp","estado","No existe","Ahí le llega el Pase. No necesita instalar nada ni crear cuenta.","Ese número tiene 9 cifras. Un celular en Colombia tiene 10.","Dice para qué es el dato y qué no le pedimos a la visita.",20),
 ("Residente","Elegir tipo · visita","estado","Visitante (rol de persona asociada)","Visita: entra una vez, en la franja que elijas.",None,"Deja de ser un rol permanente; es un tipo de Pase.",20),
 ("Residente","Elegir tipo · colaborador","estado","app.domestic_employee (clave sin traducir)","Colaborador: entra los días que elijas y el Pase se repite.",None,"El ingreso más frecuente con el mismo peso que la visita.",20),
 ("Residente","Confirmación de envío","estado","No existe","Enviado. Andrés recibió el Pase por WhatsApp. Vale hoy de 2:00 a 6:00 p. m.","No pudimos enviar el WhatsApp al 300 555 0142. Revisa el número o copia el código 4817.","Confirma con dato, dice cuándo vence y, si falla, da otra vía.",20),
 ("Residente","Pase sin confirmar","estado","Permitido (sin que la puerta lo sepa)","Enviado al lector. Queda sin confirmar hasta que la entrada responda.","El lector no responde desde las 7:40 a. m. La administración ya tiene el aviso.","Estado honesto: nada se da por hecho antes de que el lector lo confirme.",20),
 ("Residente","Pase usado","estado","Ultimo acceso: Sin accesos recientes","Usado. Andrés entró a las 3:12 p. m. con el código 4817.",None,"Nombre, hora y modo: lo que el residente necesita para saber quién entró.",20),
 ("Residente","Pase vencido","estado","No existe: la visita quedaba inscrita sin fecha","Vencido a las 6:00 p. m. Andrés ya no puede entrar con este Pase.",None,"Cierra el ciclo que antes no existía.",20),
 ("Residente","Pase vencido · botón","boton","No existe","Crear otro Pase",None,"Repite el flujo con los datos de antes.",3),
 ("Residente","Cupo agotado","estado","No existe","Tienes {cupo} Pases activos, el tope que fijó la administración. Revoca uno o espera a que venza.",None,"Dice el tope, quién lo fijó y las dos salidas. Unidad del cupo [PENDIENTE].",20),
 ("Residente","Franja agotada","estado","No existe","Las visitas entran de 6:00 a. m. a 10:00 p. m. Elige una hora en esa franja.",None,"La regla primero y después qué hacer.",20),
 ("Residente","Aviso de llegada","estado","No existe","Andrés entró a las 3:12 p. m. con la placa KMN 305.",None,"El aviso llega cuando el lector confirma, no cuando la visita dice que llegó.",20),
 ("Visitante","WhatsApp con el Pase","wa","No existe: la visita debía crear cuenta y esperar aprobación","Carolina Ruiz, de la Casa 14, te dio un Pase para hoy de 2:00 a 6:00 p. m. Muéstralo en la entrada: {enlace}",None,"Una sola acción. El Pase va como imagen con la identidad de Kino: QR, código, placa y vigencia. El enlace abre el Pase vivo, que dice si sigue vigente.",45),
 ("Visitante","En la entrada · QR","estado","No existe","Acerca el QR al lector y espera la luz verde.",None,"Una instrucción física. «Luz verde» depende del lector instalado [PENDIENTE: confirmar el modelo].",20),
 ("Visitante","En la entrada · placa","estado","No existe","Avanza despacio hasta la talanquera. La cámara lee la placa KMN 305.",None,"Dice qué hacer y qué va a pasar.",20),
 ("Visitante","En la entrada · código","estado","No existe","Dile a portería el código 4817. Sirve una sola vez.",None,"Vía que no exige datos personales ni biometría (SIC). Cómo se digita el código en la entrada: [PENDIENTE].",20),
 ("Visitante","Placa no leída","estado","No existe","El lector no leyó la placa KMN 305. Muestra el QR o di el código 4817.",None,"Qué pasó y dos salidas, sin culpar a nadie.",20),
 ("Visitante","Pase fuera de horario","estado","No existe","Tu Pase vale de 2:00 a 6:00 p. m. y son las 7:10 p. m. Pídele uno nuevo a Carolina.",None,"La hora exacta y la persona que puede resolverlo.",20),
 ("Acceso a la cuenta","Código por WhatsApp · mensaje","wa","Continuar con Google · Recordarme","Tu código para entrar a Kino es 482 913. Vence en 10 minutos. Si no lo pediste, ignora este mensaje.",None,"Decisión tomada: ingreso con código por WhatsApp. Vigencia del código [PENDIENTE: confirmar con producto].",45),
 ("Acceso a la cuenta","Código por WhatsApp · pantalla","estado","Recordarme","Te enviamos un código por WhatsApp al 300 *** 0142.","Ese código no coincide. Revisa el último mensaje de Kino.","Muestra a dónde llegó sin exponer el número completo.",20),
 ("Acceso a la cuenta","Código por WhatsApp · botón","boton","Continuar con Google","Recibir código",None,"Nombra lo que va a pasar.",3),
 ("Acceso a la cuenta","Validación por cédula","estado","No existe: una persona aprobaba la solicitud a mano","Escribe tu cédula. La comparamos con el registro de Refugio Campestre.",None,"Dice con qué se compara el dato. Reemplaza la aprobación manual.",20),
 ("Acceso a la cuenta","Cédula no encontrada","estado","No tienes propiedades asociadas","Esa cédula no está en el registro de Refugio Campestre. La administración puede agregarla.",None,"Qué pasó y quién lo resuelve, sin sugerir que el residente se equivocó.",20),
 ("Acceso a la cuenta","Cédula no encontrada · botón","boton","No existe","Escribir a administración",None,"El siguiente paso tiene nombre.",3),
 ("Administración","Fijar límites · título","estado","No existe: un único nivel de acceso, binario, sin horarios","Límites del conjunto",None,"Nombra el control que la administración sí ejerce.",20),
 ("Administración","Fijar límites · ayuda","estado","No existe","Aplican a los Pases nuevos. Los activos conservan su vigencia.",None,"Dice el alcance del cambio. Regla de producto [PENDIENTE: confirmar].",20),
 ("Administración","Fijar límites · botón","boton","No existe","Guardar límites",None,"Verbo y objeto.",3),
 ("Administración","Fijar límites · confirmación","estado","No existe","Límites guardados. Rigen desde hoy a las 4:32 p. m.",None,"Hora exacta para la constancia.",20),
 ("Administración","Resumen de actividad","estado","Permitido · app.vehicles_synced","Esta semana: 214 Pases otorgados, 187 usados y 3 rechazados en la entrada.",None,"Cifras con denominador (ejemplo). Reemplaza un estado que no decía nada.",20),
 ("Administración","Integración caída","estado","No existe: la app mostraba 43 carros permitidos y el lector conocía 1","0 de 312 personas reconocidas por el lector. Los Pases nuevos quedan sin confirmar.",None,"El hallazgo de Refugio convertido en aviso visible.",20),
 ("General","Estado vacío · lista de Pases","estado","No se encontraron registros","No tienes Pases activos. Crea uno cuando esperes a alguien.",None,"Dice qué falta y cuándo se usa.",20),
 ("General","Carga · envío","estado","No existe","Enviando el Pase a Andrés…",None,"Nombra lo que está pasando.",20),
 ("General","Sin conexión","estado","No existe","Sin conexión. El Pase no se envió; lo que escribiste sigue aquí.",None,"Qué pasó y que no se perdió nada.",20),
 ("General","Sin conexión · botón","boton","No existe","Reintentar",None,"Una palabra.",3),
 ("General","Error del servidor","estado","Incorrect request parameter. [email parameter error]","No pudimos crear el Pase: el servidor no respondió. Intenta en un minuto.",None,"Qué pasó y qué hacer, en español.",20),
]

# 36 textos actuales de la app (muestras-voz.md §a) → propuesta
ACTUALES = [
 ("Recordarme","Se elimina","Con el código por WhatsApp no queda nada que recordar."),
 ("Continuar con Google","Recibir código","El ingreso es con código por WhatsApp."),
 ("Perfil incompleto","Falta tu WhatsApp","Dice qué falta."),
 ("…para que administración y portería puedan contactarte","Tu WhatsApp sirve para entrar a Kino y para avisarte cuando alguien llega.","Dice para qué es el dato."),
 ("No tienes propiedades asociadas","Tu cédula no está ligada a ninguna casa. La administración puede hacerlo.","Qué pasó y quién lo resuelve."),
 ("Sin propiedades asignadas","(se une al anterior)","Dos textos para el mismo estado."),
 ("Rol: Residente","Casa 14 · Refugio Campestre","El residente se reconoce por su casa, no por su rol."),
 ("Registrar Vehículo","Agregar vehículo","Tipo oración."),
 ("Será registrado automáticamente en todas tus comunidades","Esta placa abre la talanquera en Refugio Campestre y Villas Campestres.","Dice el efecto real: la placa da acceso físico."),
 ("Crear Reserva","Reservar","Un verbo basta."),
 ("Sólo se muestran horarios disponibles según la zona, la fecha y las reservas existentes","Ves solo las horas libres de esa zona.","Más corto y sin tilde en «solo»."),
 ("Residente / Propietario","Propietario · Casa 14","Un dato, no dos roles."),
 ("1 propiedad asociada. 118 - Sin zona registrada - Activo - Rol: Propietario - Personas asociadas: 4","Casa 118 · 4 personas con cuenta","Los datos que el residente usa, sin guiones de registro."),
 ("1 vehiculo registrado. 1 activo para ingreso.","1 vehículo. Abre la talanquera hasta el 12 ago 2027.","Muestra la vigencia que hoy solo ve portería."),
 ("Ultimo acceso: Sin accesos recientes","Último ingreso: ninguno registrado","Tildes y un término del glosario."),
 ("Paquetes pendientes · Proximas reservas · Ultimos accesos · Mis propiedades · Mis Vehiculos","Paquetes · Reservas · Ingresos · Mi casa · Vehículos","Tildes y menos palabras."),
 ("Visitante (rol de persona asociada)","Visita (tipo de Pase)","La visita deja de ser un rol permanente."),
 ("app.domestic_employee","Colaborador","Clave sin traducir."),
 ("empleada domestica","Colaborador · aseo","Término de la marca, con la tarea."),
 ("Estado de Acceso","Lector","La columna dice si el lector lo reconoce."),
 ("El estado de acceso es controlado por los administradores","Esta placa abre la talanquera desde que la registraste.","Decía lo contrario de lo que pasaba (prueba TST001)."),
 ("confirmada / pendiente","Confirmada · Por confirmar","Tipo oración; «por confirmar» no sugiere una aprobación."),
 ("Permitido","Vigente · Sin confirmar","Separa lo que el lector confirmó de lo que no."),
 ("app.vehicles_synced","Vehículos reconocidos por el lector","Clave sin traducir."),
 ("Crear Usuario","Agregar residente","Las visitas ya no son usuarios."),
 ("No se encontraron registros","Aún no hay zonas comunes. Agrega la primera para que se pueda reservar.","Qué falta y para qué."),
 ("Crear Zona comun","Agregar zona común","Tilde y tipo oración."),
 ("Crear Contratista","Agregar colaborador","Término de la marca."),
 ("Estado de Sincronizacion","Lector","Una palabra que portería entiende."),
 ("Valido Desde / Valido Hasta","Vale desde · Vale hasta","Tildes y verbo."),
 ("Crear paquete","Registrar paquete","El paquete ya existe; se registra."),
 ("Autorizado","Entró","Un evento, dicho como hecho."),
 ("Sin propiedad vinculada","Sin casa asociada","Término del glosario."),
 ("General Access Level","Acceso general","En español."),
 ("Allowed · Sync Status · Valid Until · Synced · Pending","Vigente · Lector · Vale hasta · Reconocido · Sin confirmar","En español y con los estados de la marca."),
 ("Incorrect request parameter. [email parameter error]","HikCentral rechazó el registro porque falta el correo. Los Pases no deben crear personas.","Qué pasó y cuál es la regla que lo evita."),
]

# ───────────────────────── Plantillas de WhatsApp ─────────────────────────
WA = [
 ("Pase de visita", "residente → visita · imagen del Pase + enlace", "{residente}, de la {unidad}, te dio un Pase para {dia} de {desde} a {hasta}. Muéstralo en la entrada: {enlace}",
  "Carolina Ruiz, de la Casa 14, te dio un Pase para hoy de 2:00 a 6:00 p. m. Muéstralo en la entrada: kino.co/p/7Hq2"),
 ("Pase de colaborador", "residente → colaborador · imagen del Pase + enlace", "{residente}, de la {unidad}, te dio un Pase de colaborador: {dias}, de {desde} a {hasta}. Muéstralo en la entrada: {enlace}",
  "Carolina Ruiz, de la Casa 14, te dio un Pase de colaborador: lunes y jueves, de 7:00 a. m. a 5:00 p. m. Muéstralo en la entrada: kino.co/p/9Xc4"),
 ("Pase revocado", "sistema → visita", "{visita}, {residente} cortó tu Pase para {conjunto}. Ya no sirve para entrar. Si fue un error, escríbele a {residente}.",
  "Andrés, Carolina Ruiz cortó tu Pase para Refugio Campestre. Ya no sirve para entrar. Si fue un error, escríbele a Carolina."),
 ("Llegada", "sistema → residente", "{visita} entró a las {hora} con {modo}.",
  "Andrés entró a las 3:12 p. m. con la placa KMN 305."),
 ("Código de acceso", "sistema → residente", "Tu código para entrar a Kino es {codigo}. Vence en {minutos} minutos. Si no lo pediste, ignora este mensaje.",
  "Tu código para entrar a Kino es 482 913. Vence en 10 minutos. Si no lo pediste, ignora este mensaje."),
 ("Pase por vencer", "sistema → residente", "El Pase de {visita} vence a las {hasta}. Si necesita más tiempo, extiéndelo desde la app.",
  "El Pase de Andrés vence a las 6:00 p. m. Si necesita más tiempo, extiéndelo desde la app."),
]

# ───────────────────────── Decisiones de la Parada 2 ─────────────────────────
TRATO = [
 ("usted", True, "En Antioquia el usted es la forma cotidiana de respeto con un cliente y con alguien mayor. La administración paga y responde ante un consejo.", [
   "Su conjunto tiene 312 residentes registrados y 0 reconocidos por el lector. Kino le muestra ese dato cada mañana.",
   "Usted fija los límites una vez. Los residentes otorgan Pases dentro de ellos."]),
 ("tú", False, "Una sola voz en todo Kino. Puede sonar informal en una propuesta comercial o en un aviso de integración caída.", [
   "Tu conjunto tiene 312 residentes registrados y 0 reconocidos por el lector. Kino te muestra ese dato cada mañana.",
   "Tú fijas los límites una vez. Los residentes otorgan Pases dentro de ellos."]),
]
MAYUS = [
 ("Pase", True, "Distingue el objeto de Kino del «pase» genérico («pase adelante») y lo vuelve buscable en un mensaje. Es el nombre de un producto, como «Pase de abordar».", ["Andrés recibió el Pase.", "Crea un Pase de colaborador."]),
 ("pase", False, "Sigue la norma de la RAE para sustantivos comunes y se lee más liviano en una conversación.", ["Andrés recibió el pase.", "Crea un pase de colaborador."]),
]
HORAS = [
 ("12 horas en texto, 24 en datos", True, "Así se dice la hora en Colombia; los datos alinean en mono.", ["Vale hasta las 9:00 p. m.", "Constancia: 21:00 · KMN 305 · usado"]),
 ("24 horas en todo", False, "Sin ambigüedad y más corto, pero se lee como un registro técnico en un WhatsApp.", ["Vale hasta las 21:00.", "Constancia: 21:00 · KMN 305 · usado"]),
]

# ───────────────────────── Salidas ─────────────────────────
def chip(t, k): return f'<span class="chip-cont">{e(t)}</span>'
out = []
out.append('''<section class="vista" id="verbal" data-titulo="Voz y UX writing" data-num="02" data-grupo="Fundamentos" hidden>
  <header class="abre">
    <p class="ojo">02 · Fundamentos</p>
    <h1>Voz y UX writing</h1>
    <dl class="lector">
      <div><dt>Qué es</dt><dd>Cómo habla Kino con el residente, con la visita, con portería y con la administración.</dd></div>
      <div><dt>Para qué sirve</dt><dd>Para escribir cualquier texto de la app, un WhatsApp o una propuesta sin que cada persona lo resuelva a su manera.</dd></div>
      <div><dt>Cuándo se usa</dt><dd>Cada vez que un texto va a llegarle a alguien fuera del equipo. Antes de publicar, pásalo por <code>npm run voz -- kino</code>.</dd></div>
    </dl>
  </header>''')
# Perfil
fil = ''.join(f'''<div class="dim"><div class="dim-cab"><h3>{e(n)}</h3><span class="dim-val">{v} de 5</span></div>
  <div class="escala" role="img" aria-label="{e(n)}: {v} de 5, de {e(a)} a {e(b)}"><span>{e(a)}</span><ol>{"".join(f'<li{" class=on" if i==v else ""}></li>' for i in range(1,6))}</ol><span>{e(b)}</span></div>
  <p>{e(nota)}</p><p class="si">{e(ej)}</p></div>''' for n,v,a,b,nota,ej in PERFIL)
out.append(f'''  <article class="sub" id="verbal.perfil" data-titulo="Perfil de tono">
    <h2>Perfil de tono</h2>
    <p class="lede">Las cuatro dimensiones de Nielsen Norman Group, de 1 a 5. Cada valor se reconoce en una frase.</p>
    <div class="perfil">{fil}</div>
    <p class="traza">Responde a: personalidad Exacto, Franco y Discreto (plataforma)</p>
  </article>''')
# Tono
filas = ''.join(f'<tr><th scope="row">{e(c)}<small>{e(t)}</small></th><td>{e(r)}</td><td><p class="si">{e(si)}</p></td><td><p class="no">{e(no)}</p></td></tr>' for c,t,r,si,no in TONO)
out.append(f'''  <article class="sub" id="verbal.tono" data-titulo="Tono por contexto">
    <h2>El mismo Kino en seis lugares</h2>
    <p class="lede">La voz no cambia. Cambia cuánto sabe quien lee y cuánto tiempo tiene.</p>
    <div class="tabla-envoltura" role="region" aria-label="Tono por contexto" tabindex="0"><table class="tabla"><thead><tr><th scope="col">Contexto</th><th scope="col">Cómo suena</th><th scope="col">Así</th><th scope="col">Así no</th></tr></thead><tbody>{filas}</tbody></table></div>
  </article>''')
# Tratamiento, mayúscula, horas (Parada 2)
def opciones(titulo, id_, lede, ops):
    cards = ''.join(f'''<div class="op{" rec" if rec else ""}"><p class="op-et">{e(n)}{" · propuesta" if rec else ""}</p><p>{e(por)}</p>{"".join(f'<p class="si">{e(x)}</p>' for x in ej)}</div>''' for n,rec,por,ej in ops)
    return f'''  <article class="sub" id="verbal.{id_}" data-titulo="{e(titulo)}">
    <h2>{e(titulo)}</h2>
    <p class="lede">{e(lede)}</p>
    <div class="opciones">{cards}</div>
  </article>'''
out.append(opciones("Tratamiento con la administración","tratamiento","Con el residente y la visita, tú. Con la administración se propone usted; se decide en la revisión de esta sección.",TRATO))
out.append(opciones("«Pase» con mayúscula","mayuscula","Una sola forma en todas las piezas.",MAYUS))
out.append(opciones("Horas","horas","Un formato por contexto, nunca dos en la misma pieza.",HORAS))
# Vocabulario
u = ''.join(f'<li><dt>{e(a)}</dt><dd>{e(b)}</dd></li>' for a,b in USAR)
nm = ''.join(f'<tr><td>{e(a)}</td><td>{e(b)}</td><td>{e(c)}</td></tr>' for a,b,c in NO_MEZCLAR)
ev = ''.join(f'<tr><td><span class="tachado">{e(a)}</span></td><td>{e(b)}</td><td>{e(c)}</td></tr>' for a,b,c in EVITAR)
out.append(f'''  <article class="sub" id="verbal.vocabulario" data-titulo="Vocabulario">
    <h2>Vocabulario</h2>
    <p class="lede">{len(USAR)} términos para usar, {len(NO_MEZCLAR)} pares que no se mezclan y {len(EVITAR)} que se evitan. Las definiciones completas están en el <a href="#glosario">glosario</a>.</p>
    <h3 class="sub-h">Usar</h3>
    <dl class="vocab">{u}</dl>
    <h3 class="sub-h">No mezclar</h3>
    <div class="tabla-envoltura"><table class="tabla"><thead><tr><th scope="col">Término</th><th scope="col">No es</th><th scope="col">Diferencia</th></tr></thead><tbody>{nm}</tbody></table></div>
    <h3 class="sub-h">Evitar</h3>
    <div class="tabla-envoltura"><table class="tabla"><thead><tr><th scope="col">Evitar</th><th scope="col">Usar</th><th scope="col">Por qué</th></tr></thead><tbody>{ev}</tbody></table></div>
  </article>''')
# Estilo
es = ''.join(f'<tr><th scope="row">{e(a)}</th><td><p class="si">{e(b)}</p></td><td><p class="no">{e(c)}</p></td><td>{e(d)}</td></tr>' for a,b,c,d in ESTILO)
out.append(f'''  <article class="sub" id="verbal.estilo" data-titulo="Guía de estilo">
    <h2>Guía de estilo</h2>
    <p class="lede">Números, horas, fechas, placas, mayúsculas, puntuación, siglas y lenguaje inclusivo.</p>
    <div class="tabla-envoltura"><table class="tabla"><thead><tr><th scope="col">Qué</th><th scope="col">Así</th><th scope="col">Así no</th><th scope="col">Regla</th></tr></thead><tbody>{es}</tbody></table></div>
  </article>''')
# UX writing
grupos = []
for g in ["Residente","Visitante","Acceso a la cuenta","Administración","General"]:
    rows = ''.join(f'''<tr><th scope="row">{e(m)}<small>{e({"boton":"botón","estado":"mensaje","wa":"WhatsApp"}[t])} · máx. {lim} palabras · {palabras(d)}</small></th><td class="antes">{e(a)}</td><td><p class="si">{e(d)}</p>{f'<p class="err"><span>Error</span> {e(err)}</p>' if err else ""}</td><td>{e(p)}</td></tr>''' for gg,m,t,a,d,err,p,lim in UX if gg==g)
    grupos.append(f'<h3 class="sub-h">{e(g)}</h3><div class="tabla-envoltura"><table class="tabla ux"><thead><tr><th scope="col">Momento</th><th scope="col">Antes</th><th scope="col">Después</th><th scope="col">Por qué</th></tr></thead><tbody>{rows}</tbody></table></div>')
out.append(f'''  <article class="sub" id="verbal.ux" data-titulo="Textos de la app">
    <h2>Textos de la app</h2>
    <p class="lede">Cada momento del recorrido con su texto final, su error cuando aplica y su límite: botones de 3 palabras o menos, mensajes de 20 o menos, WhatsApp de 45 o menos.</p>
    {"".join(grupos)}
  </article>''')
act = ''.join(f'<tr><td class="antes">{e(a)}</td><td><p class="si">{e(b)}</p></td><td>{e(c)}</td></tr>' for a,b,c in ACTUALES)
out.append(f'''  <article class="sub" id="verbal.actuales" data-titulo="Los 36 textos actuales">
    <h2>Los 36 textos de la app actual</h2>
    <p class="lede">Copiados tal cual de la inspección de septiembre de 2026, con sus tildes faltantes, y la versión que los reemplaza.</p>
    <div class="tabla-envoltura"><table class="tabla"><thead><tr><th scope="col">Antes</th><th scope="col">Después</th><th scope="col">Por qué</th></tr></thead><tbody>{act}</tbody></table></div>
  </article>''')
# WhatsApp
wa = ''.join(f'''<div class="wa"><p class="wa-rot">{e(n)} <small>{e(q)} · {palabras(ej)} palabras</small></p>
  <div class="wa-burbuja"><p>{e(ej)}</p><span class="wa-hora">3:04 p. m.</span></div>
  <details><summary>Plantilla</summary><code class="plantilla">{e(pl)}</code></details></div>''' for n,q,pl,ej in WA)
out.append(f'''  <article class="sub" id="verbal.whatsapp" data-titulo="Plantillas de WhatsApp">
    <h2>Plantillas de WhatsApp</h2>
    <p class="lede">Seis mensajes cortos. El texto dice quién y cuándo; el Pase llega como imagen, con la identidad de Kino, y el enlace abre su versión viva. Las variables van entre llaves.</p>
    <div class="was">{wa}</div>
    <p class="pie-fuente">[PENDIENTE] No hay mensajes reales de portería ni de WhatsApp del conjunto para comparar. El dominio del enlace (kino.co) es de ejemplo.</p>
  </article>''')
out.append('</section>')
(R/'contenido/02-verbal.html').write_text('\n'.join(out), encoding='utf8')

# Verificación de largo y muestras para npm run voz
ver = []
for gg,m,t,a,d,err,p,lim in UX:
    for txt in [d]+([err] if err else []):
        ver.append({"momento": f"{gg} · {m}", "texto": txt, "palabras": palabras(txt), "limite": lim, "pasa": palabras(txt) <= lim})
for n,q,pl,ej in WA:
    ver.append({"momento": f"WhatsApp · {n}", "texto": ej, "palabras": palabras(ej), "limite": 45, "pasa": palabras(ej) <= 45})
(R/'build').mkdir(exist_ok=True)
json.dump(ver, open(R/'build/verbal-verificacion.json','w'), ensure_ascii=False, indent=1)
muestras = [v["texto"] for v in ver] + [b for a,b,c in ACTUALES] + [x[3] for x in TONO] + [x[5] for x in PERFIL]
(R/'build/muestras-ux.md').write_text('\n'.join(muestras)+'\n', encoding='utf8')
# Inventario en markdown
md = ["# Inventario de UX writing · Kino","","Formato: antes → después → por qué. Límites: botón ≤ 3 palabras, mensaje ≤ 20, WhatsApp ≤ 45. Tratamiento: tú con residente y visita. Estado: PROPUESTA (Parada 2).",""]
for g in ["Residente","Visitante","Acceso a la cuenta","Administración","General"]:
    md += [f"## {g}","","| Momento | Antes | Después | Error | Palabras | Por qué |","|---|---|---|---|---|---|"]
    md += [f"| {m} | {a} | {d} | {err or '—'} | {palabras(d)}/{lim} | {p} |" for gg,m,t,a,d,err,p,lim in UX if gg==g]
    md.append("")
md += ["## Los 36 textos actuales","","| Antes | Después | Por qué |","|---|---|---|"] + [f"| {a} | {b} | {c} |" for a,b,c in ACTUALES] + [""]
md += ["## Plantillas de WhatsApp",""] + sum([[f"### {n} ({q})","",f"- Plantilla: `{pl}`",f"- Ejemplo ({palabras(ej)} palabras): {ej}",""] for n,q,pl,ej in WA],[])
(R/'build/ux-writing.md').write_text('\n'.join(md), encoding='utf8')
# Guía de contenido
g = ["# Kino · Guía de contenido","","Si algo aquí contradice `voz.json`, manda `voz.json`. Estado: PROPUESTA (Parada 2).","","## Perfil de tono (aprobado)",""]
g += [f"- **{n} {v}/5** ({a} ↔ {b}). {nota} Ej.: «{ej}»" for n,v,a,b,nota,ej in PERFIL]
g += ["","## Tono por contexto","","| Contexto | Trato | Cómo suena | Así | Así no |","|---|---|---|---|---|"] + [f"| {c} | {t} | {r} | {si} | {no} |" for c,t,r,si,no in TONO]
g += ["","## Vocabulario","","### Usar",""] + [f"- **{a}**: {b}" for a,b in USAR] + ["","### No mezclar",""] + [f"- **{a}** ≠ **{b}**: {c}" for a,b,c in NO_MEZCLAR] + ["","### Evitar",""] + [f"- ~~{a}~~ → {b}. {c}" for a,b,c in EVITAR]
g += ["","## Estilo","","| Qué | Así | Así no | Regla |","|---|---|---|---|"] + [f"| {a} | {b} | {c} | {d} |" for a,b,c,d in ESTILO]
g += ["","## Decisiones abiertas (Parada 2)",""]
for t,ops in [("Tratamiento con la administración",TRATO),("Mayúscula de Pase",MAYUS),("Horas",HORAS)]:
    g += [f"### {t}",""] + [f"- **{n}**{' (propuesta)' if r else ''}: {p} Ej.: " + " / ".join(f"«{x}»" for x in ej) for n,r,p,ej in ops] + [""]
g += ["El inventario completo de textos está en `ux-writing.md`."]
(R/'build/guia-de-contenido.md').write_text('\n'.join(g), encoding='utf8')
malos = [v for v in ver if not v["pasa"]]
print("momentos", len(UX), "textos", len(ver), "fuera de límite", len(malos))
for m in malos: print(" ", m["momento"], m["palabras"], "/", m["limite"], "·", m["texto"])
print("usar", len(USAR), "no mezclar", len(NO_MEZCLAR), "evitar", len(EVITAR), "total", len(USAR)+len(NO_MEZCLAR)+len(EVITAR))
