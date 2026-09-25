Parada 4 · 25 sep 2026 · rama marca/fase-4
Sistema de marca · versión 1.0.0 en revisión
El sistema completo, listo para tu revisión
Tokens, sitio de doce departamentos, las piezas del Pase y la librería de Figma, con la verificación de la Fase 5. Abajo, cinco preguntas ordenadas por lo que desbloquean.
Abrir el sitio vista previa
Abrir Figma BO7UnDO9…
Ver la rama marca/fase-4
El artefacto oficial «Kino · Sistema de marca» no se toca hasta que respondas la pregunta 1. El silencio no cuenta como aprobación.
Lo que necesito de ti
Cinco preguntas
1
Versión 1.0.0
¿Apruebas la versión 1.0.0 como está: tokens, sitio, piezas del Pase y librería de Figma?
Sí
Marco 1.0.0 como vigente, quito la etiqueta «Propuesta» del sitio y de Figma, y republico el artefacto oficial «Kino · Sistema de marca» con su enlace de siempre.
Sí, con cambios
Dime cuáles. Los hago, vuelvo a correr la verificación y te muestro solo lo que cambió.
Es la única respuesta que libera el artefacto oficial. Las otras cuatro se pueden contestar después sin frenar esta.
2
F4-P2 · Aviso de llegada
El inventario de textos promete avisar al residente cuando alguien entra, pero el producto no tiene confirmado ese aviso. ¿Qué hacemos con esa promesa?
A · Requisito de producto (recomendada)
Los textos se quedan, marcados «requiere el evento del lector». Ninguno sale a producción antes de que el aviso exista. Responde al núcleo del diagnóstico: el residente otorga el Pase pero hoy no sabe si la persona entró.
B · Quitar la promesa
El campo dice «Tu WhatsApp sirve para entrar a Kino.» y el estado «Aviso de llegada» sale del inventario hasta que el producto lo tenga.
Por verificar en los dos casos: que HikCentral le entregue a Kino el evento de paso del lector.
3
F4-P1 · Llamada desde el Pase vivo
El Pase vivo vencido, que ve la visita, tiene el botón «Llamar al residente». X11 aprobó la llamada desde portería. ¿La visita también llama?
A · Quitar el botón (recomendada)
El aviso dice «Pídele uno nuevo a Carolina o pide en portería que la llamen.» La llamada queda solo en portería. No expone el número del residente ni promete una función que no existe.
B · Llamada enmascarada
Kino conecta a la visita con el residente sin mostrar el número. Es una función nueva: proveedor de telefonía por elegir, costo por llamada y un registro de cada llamada.
Lo construido hoy es el botón. Si eliges A, cambian dos funciones y se rehace una imagen.
4
Vencido y Usado
El lector frío notó que Vencido y Usado solo se distinguen por el tono del texto y la palabra. ¿Basta?
A · Basta con la palabra
Todo estado ya lleva palabra (regla 2). Los dos van en sustrato porque ninguno pide acción.
B · Ícono en el chip
El punto del chip se cambia por el ícono del estado (Usado, Vencido, Revocado). Los íconos ya existen en la librería.
No cambia el color ni los tokens, solo el componente Estado.
5
Detector de IA
El detector no pasó: 8 señales en el tercer ciclo. Las corregí, pero el límite de 3 ciclos no me deja volver a medir. ¿Cómo lo cerramos?
A · Aceptar el ciclo 3
Se aprueba con la última medición y las correcciones hechas, y se reporta así.
B · Un cuarto ciclo
Autorizas una medición más antes de aprobar. Si quedan señales, las corrijo y te muestro el resultado.
El lector frío sí pasó: 8 de 8 con cita y claridad media de 4,25.
Fase 4 · bloques 1 a 6
Qué se construyó
273
Tokens DTCG
203 primitivos y 70 semánticos por tema, oscuro y claro.
kino-brand.css sale de ellos.
112
Mediciones de contraste
56 pares en los dos temas, con mínimo WCAG 2.2 y APCA. Cero fallos.
12
Departamentos en el sitio
Del 01 al 12, con glosario, descargas y el motor de movimiento en vivo.
6
Piezas del Pase
Imagen, Pase vivo, PDF, señal de la entrada y portería, en PNG y PDF.
270
Variables de Figma
Iguales a DTCG en los dos modos, más 3 sombras como estilos de efecto. Seis juegos de componentes con todos sus estados.
Bloque 3 · forma Portal (X1)
Las piezas del Pase
Datos de ejemplo. El QR vive dentro del arco del logo en todas.
Imagen del WhatsApp
1080 × 1350. Llega en la conversación sin abrir nada.
Pase vivo
La página del enlace. Dice si el Pase sigue sirviendo.
Pase vivo vencido
Con el botón de la pregunta 3.
PDF
Carta, en claro, una página. Descarga opcional.
Portería
Rechazo por Pase vencido y la llamada de X11.
Señal de la entrada
60 × 40 cm.
Fase 5 · 10 de 10
Verificación
Se corre con
verificacion/fase5.py. La comprobación 6 compara 270 variables de Figma contra DTCG en los dos modos, además de los números y las sombras.
#
Comprobación
Resultado
Detalle
1
Términos prohibidos, palabras vetadas, exclamaciones y rayas en el texto visible
Pasa
0 términos, 0 exclamaciones, 0 rayas
2
npm run voz -- kino sobre el texto visible y los textos de la app
Pasa
0 hallazgos · 0 errores
3
Límites de largo de UX writing (botón ≤ 3, estado ≤ 20, WhatsApp ≤ 45)
Pasa
46 de 46 dentro del límite
4
Tú con residente y visita, usted con la administración, sin mezclar
Pasa
app con usted: 0 · administración con tú: 0 · piezas para administración con tú: 0
5
APCA en todos los pares texto y fondo (Lc 75 · 60 · 45 · 30)
Pasa
112 mediciones, 0 fallos, 0 sin mínimo APCA
6
Diff entre tokens DTCG, kino-brand.css y variables de Figma
Pasa
DTCG 273 · kino-brand.css: 0 faltan · Figma: 270 variables y 3 estilos de efecto, 0 tokens sin variable, 0 valores distintos (color en los dos modos, números y cadenas)
7
Componentes sin ligar a variables (CSS y Figma)
Pasa
capa-componentes.css: 0 valores sueltos · Figma: 0 nodos con color sin variable
8
Decisiones sin justificación de la plataforma
Pasa
decisiones.md: 26 con detalle, 0 sin «Por qué» · tabla X: 0 sin «Responde a» · departamentos sin traza: 0
9
Enlaces y anclas rotas
Pasa
46 anclas internas, 0 rotas · 6 enlaces externos
10
Cobertura de la definición de terminado
Pasa
81 elementos · 81 con su ancla en el sitio · 0 [PENDIENTE] con motivo · 0 faltan
Dos lectores que solo vieron el sitio
Evaluaciones independientes
Lector frío
Pasa
Ciclo
Con cita
Claridad media
1
8 de 8
3,9
2
8 de 8
4,25
Observaciones que siguen abiertas:
Vencido y Usado se distinguen solo por el tono y la palabra.Pregunta 4.
El Pase se nombra antes de definirse en el recorrido «Conocer Kino».Se corrige al aprobar: una línea de definición en la entrada del recorrido.
Cuatro verdes: se aclaran en Color, no donde aparecen primero.Se corrige al aprobar: nota en la primera aparición.
La versión 1.0.0 figura «Propuesta».Se resuelve con la pregunta 1.
El centro de descargas está al final de Gobernanza.Se corrige al aprobar: enlace desde el inicio del sitio.
Detector de IA
Falla
Ciclo
Señales
Secciones con más de 1
1
17
Plataforma, Imagen, Voz, Iconografía
2
12
Plataforma, Imagen
3
8
Motion, Plataforma
Las 8 señales del ciclo 3 se corrigieron. El límite de 3 ciclos impide volver a medir, así que la condición queda sin verificar y se reporta como falla. Queda un patrón: titulares en dos mitades paralelas. Ver la pregunta 5.
Sitio definitivo · bloques 2 y 4
Estado por departamento
Departamento
Estado
Qué tiene
01
Plataforma
Aprobada
Parada 1: posicionamiento, promesa, personalidad, valores, nombres y manifiesto.
02
Verbal
Aprobada
Parada 2: tono, vocabulario, 46 textos en límite, plantillas de WhatsApp.
03
Logo
En revisión
Tres versiones con bloque hueso y gota verde. Los SVG se reconstruyeron desde PNG (98 % de coincidencia).
04
Color
En revisión
Siete familias, nueve estados, 56 pares medidos en los dos temas, simulación de daltonismo, CMYK.
05
Tipografía
En revisión
Archivo al 112 % en titulares, JetBrains Mono con cero barrado, escala de 8 pasos.
06
Iconografía
En revisión
37 íconos en retícula de 24, trazo 1,7 con puntas redondas.
07
Imagen
En revisión
Aurora en pantalla, tejido celular solo en impresos grandes, sin fotos de personas.
08
Estructura
En revisión
Cuatro retículas, diez pasos de espacio, radio 14 y arco solo en el Pase.
09
Motion
En revisión
13 animaciones con su token, el motor en vivo y el modo de movimiento reducido.
10
Producto
En revisión
Componentes con todos sus estados, cinco pantallas, criterios WCAG.
11
Aplicaciones
En revisión
Quince piezas, del Pase a la papelería. Las físicas están en 2D.
12
Gobernanza
En revisión
Quién decide, registro de decisiones, lista de revisión, 17 pendientes y descargas.
decisiones.md
Decisiones
Aprobadas
Plataforma · 14
P01 a P14. P11 quedó reemplazada por V5.
Verbal · 7
V1 a V7: usted con la administración, «Pase» con mayúscula, horas, «Visita», estados, patrones, imagen más enlace.
Identidad visual · 11
X1 a X11: Portal, logo, oscuro reajustado, dos verdes, tipografía, íconos, imagen, radio y arco, crecer, estados, llamada de portería.
Propuestas nuevas
F4-P1 · Llamada desde el Pase vivo
Recomendada: quitar el botón y dejar la llamada solo en portería. Pregunta 3.
F4-P2 · Aviso de llegada
Recomendada: tratarlo como requisito de producto y no publicarlo antes de que exista. Pregunta 2.
Efecto en la trazabilidad
Ninguna de las dos autoriza un ingreso. Entrar siempre exige un Pase con autor, que llega a HikCentral con su vigencia.
Al preparar esta lámina
Un defecto corregido y una limitación
Las piezas del Pase en PNG y PDF se habían generado con una fuente de reemplazo: pedían Archivo y JetBrains Mono a Google Fonts, y el entorno donde se generan no tiene esa salida. Ahora las fuentes van incrustadas desde
branding/sistema/fonts/ y las cuatro entregas se volvieron a generar. El PDF sigue en una página.
Una limitación de la vista previa: dentro del visor de artefactos, los botones del centro de descargas no bajan nada. En el archivo del repositorio sí funcionan. Al republicar el artefacto oficial, las descargas pasan por la función de descarga del visor.
Gobernanza · 17
Pendientes
Lo que el sistema no puede resolver con los archivos que hay. Cada uno aparece marcado en el sitio donde afecta.
Vector original del logo
No existe. Los SVG son reconstrucciones desde los PNG de 1543 × 1425 px, con 98 % de coincidencia. Las medidas del logo son derivadas.
Licencia de Arkit ExtraBold
Sin información. La fuente vive solo dentro de los contornos del logotipo.
Mensajes reales de portería y WhatsApp
No hay ninguno en los archivos. Las plantillas se escribieron sin referencia de uso real.
Credencial temporal en HikCentral
Falta confirmar que acepte una credencial sin crear una persona. Es la prueba del Pase sin cuenta.
Unidad del cupo
Por casa, por residente o por conjunto. Decisión de producto; los ejemplos dicen «a la vez».
Teclado del lector
No se sabe si el lector tiene teclado para el código. El texto dice «Dile a portería el código».
Llamada de portería al residente
Nico confirmó que portería puede llamar desde Kino (X11). La inspección no registró el botón: si no existe, es un requisito de producto.
Llamada desde el Pase vivo
Falta decidir si la visita llama sin ver el número del residente. Ver decisiones, F4-P1.
Aviso de llegada
El inventario de textos lo incluye, pero el producto no lo tiene confirmado. Ver decisiones, F4-P2.
Citas de las entrevistas con residentes
Las cinco entrevistas no tienen citas escritas. Las necesidades por actor se apoyan en la inspección.
Integración real de las apps de visitas
Neivor anuncia integración sin nombrar marcas de hardware. Falta verificar.
Prueba física del logo y de color
Tamaños mínimos impresos y CMYK sin prueba en papel.
Equivalencias Pantone
Sin guía física para comparar.
Prueba con usuarios daltónicos
Los estados se revisaron solo por simulación.
Mockups físicos en 3D
No hubo herramienta 3D disponible. Señal, adhesivo, papelería y credencial están en 2D.
Datos de contacto
Correo, teléfono y dominio definitivos. Los ejemplos usan kino.co.
Canal de solicitudes
Dónde se piden activos y cambios: correo o canal del equipo, por definir.
Fuentes:
verificacion/informe.md,
verificacion/evaluaciones.md,
figma/variables-figma.json,
decisiones.md,
avances.md.
Generada con
branding/sistema/v3/parada4/construir.py.