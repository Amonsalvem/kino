Parada 4 · segunda vuelta · 25 sep 2026
Sistema de marca · versión 1.1.0 en revisión
Tu respuesta, aplicada. Faltan dos aprobaciones
Figma se revisó entera con atención al auto-layout y al espaciado, y el sitio ahora usa la identidad que describe. Tres preguntas; las dos primeras liberan el artefacto oficial.
Abrir el sitio vista previa 1.1.0
Abrir Figma BO7UnDO9…
Parada 4 primera vuelta
Rama marca/fase-4
El artefacto oficial «Kino · Sistema de marca» sigue sin republicarse. Se republica cuando respondas las preguntas 1 y 2.
Lo que necesito de ti
Tres preguntas
1
Figma · versión 1.1.0
¿Apruebas la librería de Figma con el auto-layout y el espaciado revisados?
Sí
Marco la librería como aprobada, y con la pregunta 2 aprobada republico el artefacto oficial.
Sí, con cambios
Dime la página y qué ves. Los scripts de auditoría se vuelven a correr después de cada cambio.
Abre cualquier página desde la tabla de Figma más abajo. Prueba a cambiar el ancho de un marco: el contenido debe acomodarse solo.
2
F4-P4 · Identidad en el sitio
¿La identidad aplicada al sitio queda así?
A · Así
Aurora en la portada y en la apertura de cada sección, índigo en enlaces y rótulos, gota en el índice.
B · Más sobria
Aurora solo en la portada. Las aperturas de sección van en superficie elevada, con el número en contorno.
En los dos casos el cuerpo de las secciones queda igual: el color de la marca aparece en lo que significa algo.
3
Un texto para la administración
El detector marcó «HikCentral rechazó el registro porque falta el correo. Los Pases no deben crear personas.» porque la segunda frase suena a regla interna. ¿Lo reescribo?
A · Reescribir
«HikCentral rechazó el registro porque falta el correo. Agréguelo en la ficha de la persona y vuelva a sincronizar.»
B · Dejarlo
Queda como se aprobó en la Parada 2.
La versión A no promete nada nuevo: solo dice qué hacer con el error de hoy.
Primera vuelta
Qué hice con cada respuesta
Tu respuesta
Qué cambió
Dónde
1
Todo aprobado salvo Figma y lo que se exporta de ella
Tokens, sitio y piezas del Pase quedan como 1.0.0 aprobada. Figma se revisó entera: ver abajo.
decisiones.md · Registro de cambios
2
Aviso de llegada: A
El inventario marca el aviso «requiere el evento del lector». Pendiente nuevo: confirmar que HikCentral entregue ese evento.
F4-P2 · verbal.py · Gobernanza
3
Llamada desde el Pase vivo: A
El Pase vivo vencido ya no tiene botón. Dice «Pídele uno nuevo a Carolina o pide en portería que la llamen.» Piezas regeneradas.
F4-P1 · pase.py · entregables
4
Vencido y Usado: B
Usado, Vencido y Revocado llevan el ícono del estado en el chip, en código y en Figma. Las tarjetas de Pase lo heredan.
F4-P3 · capa-componentes.css · Estado
5
Detector de IA: B
Cuarto ciclo: 1 señal, 0 en el microcopy. Pasa.
evaluaciones.md
+
El sitio se lee monótono
La identidad aprobada, aplicada al propio sitio. Espera tu revisión.
F4-P4 · identidad.css
F4-P4 · pregunta 2
El sitio con la identidad de Kino
Cada recurso va donde ya significa algo. La aurora es la imagen aprobada para portadas (X7). El índigo es la familia de la profundidad y los enlaces. La gota es la marca. El verde del botón queda para crear un Pase, y el arco, para el Pase.
Portada
Aurora (X7), el logo en su versión principal y el Pase real, que es la pieza que más se usa.
Antes
Después
Apertura de sección
Aurora con el número de sección en contorno. Qué es, para qué sirve y cuándo se usa, en tres tarjetas. La gota marca la sección activa.
Antes
Después
Tema claro
La apertura conserva la aurora en oscuro local; el cuerpo va en claro. Los rótulos de subsección, en índigo.
Antes
Después
Chips de estado
Usado, Vencido y Revocado con su ícono (F4-P3). Enlaces en índigo, Lc 80 o más.
Antes
Después
En el teléfono
La portada apila el titular y el Pase.
Antes
Después
En 360 px: 0 px de desborde y 0 errores de consola en los dos temas (scripts/capturar.mjs).
Token nuevo para esto:
--kino-texto-enlace (índigo a84 en oscuro, l90 en claro), medido en las cuatro superficies de los dos temas: 120 mediciones WCAG y APCA sin fallos. La capa vive aparte, en
sitio/identidad.css.
Pregunta 1
Figma: auto-layout y espaciado
Auditoría automática en las 14 páginas, corrección con un script que se puede volver a correr, y revisión a ojo de cada página que cambió.
Qué se midió
Antes
Después
Cómo
Textos de ancho fijo dentro del auto-layout
111
0
Llenan su contenedor, con ancho máximo igual al que tenían.
Filas de tarjetas con alto desigual
7
0
La más alta abraza su contenido; las demás llenan ese alto.
Espacios y paddings sin variable
38
0
Léeme pasa de 80 a 72 y de 1200 a 1188, como las demás páginas.
Hijos que se salen de su contenedor
4
0
Botón de «Lista de Pases», retículas, chips del registro, texto de Elevación.
Separación entre marcos del lienzo
40 a 100
72
La misma en todas las páginas.
Pinturas sin variable
0
0
Se mantiene.
Variables distintas de DTCG
0
0
271 variables en los dos modos, más 3 sombras como estilos de efecto.
También: variable
texto/enlace; ícono de estado en Usado, Vencido y Revocado; vectores de íconos que escalan con su instancia; pantallas de teléfono con alto automático y mínimo de 780; tejido celular con su superficie y su radio; registro de cambios con 1.0.0 aprobada y 1.1.0 en revisión.
Léeme
Plataforma
Voz y UX writing
Logo
Color
Tipografía
Iconografía
Imagen
Estructura
Motion
Componentes
Pantallas
Aplicaciones
Registro de cambios
Fase 5 · 10 de 10
Verificación
Detector de IA, cuarto ciclo: 1 señal, ninguna sección con más de una, 0 en el microcopy. Pasa. La señal es el titular «43 carros permitidos en la app, uno en la puerta»; queda porque la cifra es el hallazgo (observado en la inspección).
#
Comprobación
Resultado
1
Términos prohibidos, palabras vetadas, exclamaciones y rayas en el texto visible
Pasa
2
npm run voz -- kino sobre el texto visible y los textos de la app
Pasa
3
Límites de largo de UX writing (botón ≤ 3, estado ≤ 20, WhatsApp ≤ 45)
Pasa
4
Tú con residente y visita, usted con la administración, sin mezclar
Pasa
5
APCA en todos los pares texto y fondo (Lc 75 · 60 · 45 · 30)
Pasa
6
Diff entre tokens DTCG, kino-brand.css y variables de Figma
Pasa
7
Componentes sin ligar a variables (CSS y Figma)
Pasa
8
Decisiones sin justificación de la plataforma
Pasa
9
Enlaces y anclas rotas
Pasa
10
Cobertura de la definición de terminado
Pasa
Al aprobar
Lo que sigue
Aplicar tus respuestas a las preguntas 2 y 3, reconstruir y volver a verificar.
Republicar el artefacto oficial leyéndolo primero, con la función de descarga del visor para que el centro de descargas funcione.
Integrar la rama
marca/fase-4 a
main: lo haces tú.
Fuentes:
decisiones.md (F4-P1 a F4-P4),
verificacion/informe.md,
verificacion/evaluaciones.md,
figma/LEEME.md,
figma/variables-figma.json.
Generada con
branding/sistema/v3/parada4b/construir.py.