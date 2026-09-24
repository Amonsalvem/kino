# Inventario de UX writing · Kino

Formato: antes → después → por qué. Límites: botón ≤ 3 palabras, mensaje ≤ 20, WhatsApp ≤ 45. Tratamiento: tú con residente y visita. Estado: PROPUESTA (Parada 2).

## Residente

| Momento | Antes | Después | Error | Palabras | Por qué |
|---|---|---|---|---|---|
| Crear un Pase · botón | No existe. Hoy solo «Registrar Vehículo» o, en administración, «Crear Usuario» | Crear Pase | — | 2/3 | Verbo y objeto. Es el único botón con color de acento. |
| Crear un Pase · pregunta de la pantalla | No existe | ¿Quién viene? | — | 2/20 | La pregunta que el residente sí sabe responder. |
| Crear un Pase · campo de WhatsApp | No existe | Ahí le llega el Pase. No necesita instalar nada ni crear cuenta. | Ese número tiene 9 cifras. Un celular en Colombia tiene 10. | 12/20 | Dice para qué es el dato y qué no le pedimos a la visita. |
| Elegir tipo · visita | Visitante (rol de persona asociada) | Visita: entra una vez, en la franja que elijas. | — | 9/20 | Deja de ser un rol permanente; es un tipo de Pase. |
| Elegir tipo · colaborador | app.domestic_employee (clave sin traducir) | Colaborador: entra los días que elijas y el Pase se repite. | — | 11/20 | El ingreso más frecuente con el mismo peso que la visita. |
| Confirmación de envío | No existe | Enviado. Andrés recibió el Pase por WhatsApp. Vale hoy de 2:00 a 6:00 p. m. | No pudimos enviar el WhatsApp al 300 555 0142. Revisa el número o copia el código 4817. | 15/20 | Confirma con dato, dice cuándo vence y, si falla, da otra vía. |
| Pase sin confirmar | Permitido (sin que la puerta lo sepa) | Enviado al lector. Queda sin confirmar hasta que la entrada responda. | El lector no responde desde las 7:40 a. m. La administración ya tiene el aviso. | 11/20 | Estado honesto: nada se da por hecho antes de que el lector lo confirme. |
| Pase usado | Ultimo acceso: Sin accesos recientes | Usado. Andrés entró a las 3:12 p. m. con el código 4817. | — | 12/20 | Nombre, hora y modo: lo que el residente necesita para saber quién entró. |
| Pase vencido | No existe: la visita quedaba inscrita sin fecha | Vencido a las 6:00 p. m. Andrés ya no puede entrar con este Pase. | — | 14/20 | Cierra el ciclo que antes no existía. |
| Pase vencido · botón | No existe | Crear otro Pase | — | 3/3 | Repite el flujo con los datos de antes. |
| Cupo agotado | No existe | Tienes {cupo} Pases activos, el tope que fijó la administración. Revoca uno o espera a que venza. | — | 17/20 | Dice el tope, quién lo fijó y las dos salidas. Unidad del cupo [PENDIENTE]. |
| Franja agotada | No existe | Las visitas entran de 6:00 a. m. a 10:00 p. m. Elige una hora en esa franja. | — | 17/20 | La regla primero y después qué hacer. |
| Aviso de llegada | No existe | Andrés entró a las 3:12 p. m. con la placa KMN 305. | — | 12/20 | El aviso llega cuando el lector confirma, no cuando la visita dice que llegó. |

## Visitante

| Momento | Antes | Después | Error | Palabras | Por qué |
|---|---|---|---|---|---|
| WhatsApp con el Pase | No existe: la visita debía crear cuenta y esperar aprobación | Carolina Ruiz, de la Casa 14, te dio un Pase para hoy de 2:00 a 6:00 p. m. Muéstralo en la entrada: {enlace} | — | 23/45 | Una sola acción. El Pase va como imagen con la identidad de Kino: QR, código, placa y vigencia. El enlace abre el Pase vivo, que dice si sigue vigente. |
| En la entrada · QR | No existe | Acerca el QR al lector y espera la luz verde. | — | 10/20 | Una instrucción física. «Luz verde» depende del lector instalado [PENDIENTE: confirmar el modelo]. |
| En la entrada · placa | No existe | Avanza despacio hasta la talanquera. La cámara lee la placa KMN 305. | — | 12/20 | Dice qué hacer y qué va a pasar. |
| En la entrada · código | No existe | Dile a portería el código 4817. Sirve una sola vez. | — | 10/20 | Vía que no exige datos personales ni biometría (SIC). Cómo se digita el código en la entrada: [PENDIENTE]. |
| Placa no leída | No existe | El lector no leyó la placa KMN 305. Muestra el QR o di el código 4817. | — | 16/20 | Qué pasó y dos salidas, sin culpar a nadie. |
| Pase fuera de horario | No existe | Tu Pase vale de 2:00 a 6:00 p. m. y son las 7:10 p. m. Pídele uno nuevo a Carolina. | — | 20/20 | La hora exacta y la persona que puede resolverlo. |

## Acceso a la cuenta

| Momento | Antes | Después | Error | Palabras | Por qué |
|---|---|---|---|---|---|
| Código por WhatsApp · mensaje | Continuar con Google · Recordarme | Tu código para entrar a Kino es 482 913. Vence en 10 minutos. Si no lo pediste, ignora este mensaje. | — | 20/45 | Decisión tomada: ingreso con código por WhatsApp. Vigencia del código [PENDIENTE: confirmar con producto]. |
| Código por WhatsApp · pantalla | Recordarme | Te enviamos un código por WhatsApp al 300 *** 0142. | Ese código no coincide. Revisa el último mensaje de Kino. | 9/20 | Muestra a dónde llegó sin exponer el número completo. |
| Código por WhatsApp · botón | Continuar con Google | Recibir código | — | 2/3 | Nombra lo que va a pasar. |
| Validación por cédula | No existe: una persona aprobaba la solicitud a mano | Escribe tu cédula. La comparamos con el registro de Refugio Campestre. | — | 11/20 | Dice con qué se compara el dato. Reemplaza la aprobación manual. |
| Cédula no encontrada | No tienes propiedades asociadas | Esa cédula no está en el registro de Refugio Campestre. La administración puede agregarla. | — | 14/20 | Qué pasó y quién lo resuelve, sin sugerir que el residente se equivocó. |
| Cédula no encontrada · botón | No existe | Escribir a administración | — | 3/3 | El siguiente paso tiene nombre. |

## Administración

| Momento | Antes | Después | Error | Palabras | Por qué |
|---|---|---|---|---|---|
| Fijar límites · título | No existe: un único nivel de acceso, binario, sin horarios | Límites del conjunto | — | 3/20 | Nombra el control que la administración sí ejerce. |
| Fijar límites · ayuda | No existe | Aplican a los Pases nuevos. Los activos conservan su vigencia. | — | 10/20 | Dice el alcance del cambio. Regla de producto [PENDIENTE: confirmar]. |
| Fijar límites · botón | No existe | Guardar límites | — | 2/3 | Verbo y objeto. |
| Fijar límites · confirmación | No existe | Límites guardados. Rigen desde hoy a las 4:32 p. m. | — | 10/20 | Hora exacta para la constancia. |
| Resumen de actividad | Permitido · app.vehicles_synced | Esta semana: 214 Pases otorgados, 187 usados y 3 rechazados en la entrada. | — | 13/20 | Cifras con denominador (ejemplo). Reemplaza un estado que no decía nada. |
| Integración caída | No existe: la app mostraba 43 carros permitidos y el lector conocía 1 | 0 de 312 personas reconocidas por el lector. Los Pases nuevos quedan sin confirmar. | — | 14/20 | El hallazgo de Refugio convertido en aviso visible. |

## General

| Momento | Antes | Después | Error | Palabras | Por qué |
|---|---|---|---|---|---|
| Estado vacío · lista de Pases | No se encontraron registros | No tienes Pases activos. Crea uno cuando esperes a alguien. | — | 10/20 | Dice qué falta y cuándo se usa. |
| Carga · envío | No existe | Enviando el Pase a Andrés… | — | 5/20 | Nombra lo que está pasando. |
| Sin conexión | No existe | Sin conexión. El Pase no se envió; lo que escribiste sigue aquí. | — | 12/20 | Qué pasó y que no se perdió nada. |
| Sin conexión · botón | No existe | Reintentar | — | 1/3 | Una palabra. |
| Error del servidor | Incorrect request parameter. [email parameter error] | No pudimos crear el Pase: el servidor no respondió. Intenta en un minuto. | — | 13/20 | Qué pasó y qué hacer, en español. |

## Los 36 textos actuales

| Antes | Después | Por qué |
|---|---|---|
| Recordarme | Se elimina | Con el código por WhatsApp no queda nada que recordar. |
| Continuar con Google | Recibir código | El ingreso es con código por WhatsApp. |
| Perfil incompleto | Falta tu WhatsApp | Dice qué falta. |
| …para que administración y portería puedan contactarte | Tu WhatsApp sirve para entrar a Kino y para avisarte cuando alguien llega. | Dice para qué es el dato. |
| No tienes propiedades asociadas | Tu cédula no está ligada a ninguna casa. La administración puede hacerlo. | Qué pasó y quién lo resuelve. |
| Sin propiedades asignadas | (se une al anterior) | Dos textos para el mismo estado. |
| Rol: Residente | Casa 14 · Refugio Campestre | El residente se reconoce por su casa, no por su rol. |
| Registrar Vehículo | Agregar vehículo | Tipo oración. |
| Será registrado automáticamente en todas tus comunidades | Esta placa abre la talanquera en Refugio Campestre y Villas Campestres. | Dice el efecto real: la placa da acceso físico. |
| Crear Reserva | Reservar | Un verbo basta. |
| Sólo se muestran horarios disponibles según la zona, la fecha y las reservas existentes | Ves solo las horas libres de esa zona. | Más corto y sin tilde en «solo». |
| Residente / Propietario | Propietario · Casa 14 | Un dato, no dos roles. |
| 1 propiedad asociada. 118 - Sin zona registrada - Activo - Rol: Propietario - Personas asociadas: 4 | Casa 118 · 4 personas con cuenta | Los datos que el residente usa, sin guiones de registro. |
| 1 vehiculo registrado. 1 activo para ingreso. | 1 vehículo. Abre la talanquera hasta el 12 ago 2027. | Muestra la vigencia que hoy solo ve portería. |
| Ultimo acceso: Sin accesos recientes | Último ingreso: ninguno registrado | Tildes y un término del glosario. |
| Paquetes pendientes · Proximas reservas · Ultimos accesos · Mis propiedades · Mis Vehiculos | Paquetes · Reservas · Ingresos · Mi casa · Vehículos | Tildes y menos palabras. |
| Visitante (rol de persona asociada) | Visita (tipo de Pase) | La visita deja de ser un rol permanente. |
| app.domestic_employee | Colaborador | Clave sin traducir. |
| empleada domestica | Colaborador · aseo | Término de la marca, con la tarea. |
| Estado de Acceso | Lector | La columna dice si el lector lo reconoce. |
| El estado de acceso es controlado por los administradores | Esta placa abre la talanquera desde que la registraste. | Decía lo contrario de lo que pasaba (prueba TST001). |
| confirmada / pendiente | Confirmada · Por confirmar | Tipo oración; «por confirmar» no sugiere una aprobación. |
| Permitido | Vigente · Sin confirmar | Separa lo que el lector confirmó de lo que no. |
| app.vehicles_synced | Vehículos reconocidos por el lector | Clave sin traducir. |
| Crear Usuario | Agregar residente | Las visitas ya no son usuarios. |
| No se encontraron registros | Aún no hay zonas comunes. Agrega la primera para que se pueda reservar. | Qué falta y para qué. |
| Crear Zona comun | Agregar zona común | Tilde y tipo oración. |
| Crear Contratista | Agregar colaborador | Término de la marca. |
| Estado de Sincronizacion | Lector | Una palabra que portería entiende. |
| Valido Desde / Valido Hasta | Vale desde · Vale hasta | Tildes y verbo. |
| Crear paquete | Registrar paquete | El paquete ya existe; se registra. |
| Autorizado | Entró | Un evento, dicho como hecho. |
| Sin propiedad vinculada | Sin casa asociada | Término del glosario. |
| General Access Level | Acceso general | En español. |
| Allowed · Sync Status · Valid Until · Synced · Pending | Vigente · Lector · Vale hasta · Reconocido · Sin confirmar | En español y con los estados de la marca. |
| Incorrect request parameter. [email parameter error] | HikCentral rechazó el registro porque falta el correo. Los Pases no deben crear personas. | Qué pasó y cuál es la regla que lo evita. |

## Plantillas de WhatsApp

### Pase de visita (residente → visita · imagen del Pase + enlace)

- Plantilla: `{residente}, de la {unidad}, te dio un Pase para {dia} de {desde} a {hasta}. Muéstralo en la entrada: {enlace}`
- Ejemplo (23 palabras): Carolina Ruiz, de la Casa 14, te dio un Pase para hoy de 2:00 a 6:00 p. m. Muéstralo en la entrada: kino.co/p/7Hq2

### Pase de colaborador (residente → colaborador · imagen del Pase + enlace)

- Plantilla: `{residente}, de la {unidad}, te dio un Pase de colaborador: {dias}, de {desde} a {hasta}. Muéstralo en la entrada: {enlace}`
- Ejemplo (28 palabras): Carolina Ruiz, de la Casa 14, te dio un Pase de colaborador: lunes y jueves, de 7:00 a. m. a 5:00 p. m. Muéstralo en la entrada: kino.co/p/9Xc4

### Pase revocado (sistema → visita)

- Plantilla: `{visita}, {residente} cortó tu Pase para {conjunto}. Ya no sirve para entrar. Si fue un error, escríbele a {residente}.`
- Ejemplo (21 palabras): Andrés, Carolina Ruiz cortó tu Pase para Refugio Campestre. Ya no sirve para entrar. Si fue un error, escríbele a Carolina.

### Llegada (sistema → residente)

- Plantilla: `{visita} entró a las {hora} con {modo}.`
- Ejemplo (12 palabras): Andrés entró a las 3:12 p. m. con la placa KMN 305.

### Código de acceso (sistema → residente)

- Plantilla: `Tu código para entrar a Kino es {codigo}. Vence en {minutos} minutos. Si no lo pediste, ignora este mensaje.`
- Ejemplo (20 palabras): Tu código para entrar a Kino es 482 913. Vence en 10 minutos. Si no lo pediste, ignora este mensaje.

### Pase por vencer (sistema → residente)

- Plantilla: `El Pase de {visita} vence a las {hasta}. Si necesita más tiempo, extiéndelo desde la app.`
- Ejemplo (18 palabras): El Pase de Andrés vence a las 6:00 p. m. Si necesita más tiempo, extiéndelo desde la app.
