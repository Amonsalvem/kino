Parada 4 · tercera vuelta · 25 sep 2026
Sistema de marca · versión 1.2.0 en revisión
Las pantallas, con la jerarquía del Pase
La 1.1.0 quedó aprobada y el artefacto oficial ya la tiene. Esta vuelta trae las cinco pantallas rehechas y la explicación de la fila de HikCentral. Dos preguntas.
Abrir el sitio vista previa 1.2.0
Abrir Figma página Pantallas
Artefacto oficial 1.1.0
Rama marca/fase-4
El oficial se republica otra vez cuando apruebes la 1.2.0 (pregunta 1).
Lo que necesito de ti
Dos preguntas
1
F4-P5 · Pantallas
¿Las pantallas quedan con la jerarquía del Pase?
A · Así
Como se ven abajo. La lista agrupa los Pases en «Ahora» y «Próximos».
B · Con pestañas
La misma jerarquía, pero la lista conserva las pestañas «Activos / Anteriores» de la 1.1.0.
En las dos, «Entrar» pasa al botón secundario: el verde de acción queda solo para crear un Pase (X4).
2
F4-P6 · El mensaje de HikCentral
¿Qué hago con la fila del error de HikCentral en el inventario de textos?
A · Mensaje genérico
«HikCentral no aceptó el alta de Carolina Ruiz. Hasta que se corrija, el lector no la reconoce.» Sirve para cualquier alta que falle, por la causa que sea.
B · Quitar la fila
Kino no debería producir el error del correo, así que la fila sale del inventario.
La explicación de la fila está justo debajo.
Segunda vuelta
Qué hice con cada respuesta
Tu respuesta
Qué hice
Dónde
1
Apruebo Figma
La 1.1.0 queda aprobada y el artefacto oficial se republicó con ella, leyéndolo primero y con su misma URL.
decisiones.md · Registro de cambios
1
Las pantallas cargan mucho
Pantallas nuevas en el sitio y en Figma con la jerarquía del Pase. Las de la 1.1.0 no se borraron.
F4-P5 · d10_producto.py · Pantallas
2
Identidad en el sitio: A
Queda como estaba en la vista previa.
F4-P4 · identidad.css
3
No se entiende la pregunta de HikCentral
Explicación abajo y pregunta nueva con dos opciones.
F4-P6 · verbal.py
+
El título de la tarjeta no se lee
El titular de la lámina anterior heredaba el color del tema claro. Corregido y republicado.
parada-4b.html
F4-P5 · pregunta 1
Cinco niveles, iguales en todas las pantallas
Salen de la imagen del Pase y del Pase vivo, que es lo que dijiste que funcionaba: el nombre manda, la vigencia se lee en su color y cada dato tiene su rótulo encima.
Nivel
Qué lleva
Cómo se ve
1 · Manda
Un dato por pantalla: el nombre, el código o el límite.
Archivo 800 ancho, lo más grande de la pantalla.
2 · Vigencia
Cuándo vale el Pase.
Monoespaciada en el color de su estado. En Crear Pase, en texto primario porque todavía no hay estado.
3 · Rótulo
Qué es cada valor: Placa, Código, Vigencia.
Mono pequeño en mayúsculas, encima de su valor.
4 · Grupo
Lo que se decide junto.
Un bloque en superficie elevada con radio 14. Entre bloques hay más aire que dentro de ellos.
5 · Acción
Una acción principal, abajo.
Verde solo si crea un Pase. Revocar va en texto.
Antes y después
Pantalla por pantalla
A la izquierda, la 1.1.0 aprobada; a la derecha, la propuesta. Mismos datos de ejemplo.
Lista de Pases · inicio
Manda el nombre de cada persona. La aurora sube a la cabecera porque esta es la pantalla de inicio (X7).
1.1.0
1.2.0
SaleLas pestañas y la palabra «Visita» repetida debajo de cada nombre.
Se agrupaAhora y Próximos. El tipo de Pase pasa a rótulo.
Crear Pase
Manda la pregunta. La franja se lee en una línea.
1.1.0
1.2.0
SaleCuatro cajas iguales, una debajo de otra.
Se agrupaPersona (nombre y WhatsApp) y vigencia (día, franja y placa).
Detalle de Pase
Manda el nombre. Placa y código, en grande.
1.1.0
1.2.0
Sale«Otorgó Carolina Ruiz · Casa 14»: es la app de Carolina.
Se agrupa«Lo que pasó» como línea de tiempo: lo que el lector confirmó lleva punto verde.
Acceso por código
Mandan las seis cifras. El número va en mono, como dato.
1.1.0
1.2.0
SaleEl bloque rojo del error y el verde en «Entrar».
Se agrupaEl error, en una línea con ícono y en el color de Rechazado.
Límites de la administración
Cada límite en su tarjeta con el valor en grande. El resumen de la semana, en cifras; las rechazadas, en su color.
1.1.0
1.2.0
En Figma, lo mismo con auto-layout y variables, más el componente nuevo «Pase en lista» con sus cuatro estados. Las pantallas de la 1.1.0 quedan en su propia sección de la página.
Pantallas
Lista de Pases
Crear Pase
Detalle de Pase
Acceso por código
Límites
Pantallas 1.1.0
Pase en lista (componente)
Registro de cambios
F4-P6 · pregunta 2
La fila de HikCentral, explicada
Tienes razón en lo principal: con el Pase, a la visita no se le pide correo ni se registra. La fila no hablaba de la visita.
Lo que dice la evidencia
De dónde sale la fila
El inventario de textos traduce cada mensaje que hoy muestra el sistema. Este es el error que ve el super administrador cuando HikCentral rechaza un alta: «Incorrect request parameter. [email parameter error]», 711 veces (observado,
inspeccion/diagnostico-inspeccion.md).
A quién afecta
A cualquier persona que el sistema actual da de alta en HikCentral, residentes incluidos. En Refugio Campestre hay 0 de 312 usuarios sincronizados (observado).
Qué cambia con Kino
Como dices, la visita entra con un Pase y no se da de alta como persona. El residente entra con código por WhatsApp, así que el correo deja de ser obligatorio (inferido de esa decisión). Con las dos cosas, el error del correo desaparece para todos.
Qué queda
Un residente o un colaborador sí se dan de alta en HikCentral, y un alta puede fallar por otra causa: Refugio tiene el hardware y la integración caída. Para ese caso la administración necesita un mensaje que diga a quién afecta y qué pasa en la puerta.
Verificación
Lo que se midió
Qué
Resultado
Contraste
132 mediciones WCAG y APCA, 0 fallos. 6 pares nuevos: la vigencia de cada estado sobre la tarjeta, Revocar y el error de código.
Rótulos pequeños
Pasan de texto tenue a secundario. El tenue solo está medido para 24 px o más (Lc 65 en oscuro).
Voz
0 hallazgos en el texto visible del sitio y en el LEEME de Figma.
Fase 5
10 de 10 comprobaciones pasan.
Figma
Pantallas y Componentes: 0 marcos sin auto-layout, 0 espacios sin variable, 0 desbordes, 0 filas desiguales, 0 solapes y 0 pinturas sin variable en las pantallas nuevas.
Al aprobar
Lo que sigue
Aplicar tus respuestas y volver a verificar.
Republicar el artefacto oficial con la 1.2.0, leyéndolo primero y con su misma URL.
Integrar la rama
marca/fase-4 a
main: lo haces tú.
Fuentes:
decisiones.md (F4-P5 y F4-P6),
inspeccion/diagnostico-inspeccion.md,
verificacion/informe.md,
figma/LEEME.md.
Generada con
branding/sistema/v3/parada4c/construir.py. Lámina anterior:
Parada 4b.