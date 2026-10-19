# QA del prototipo · Kino · App (Figma `wXZ10ygSOp8RXINwg0ZvJw`)

Revisión del 19 oct 2026, hecha sobre el archivo en vivo con lectura por API (páginas, nodos, reacciones y textos) y capturas de las pantallas clave. Cada hallazgo trae el nodo o la página de donde sale. La severidad sigue la escala de Nielsen: 0 = no es problema, 4 = catástrofe.

## Conclusión

El archivo está muy bien armado como **especificación**. Tiene 226 pantallas en oscuro y claro, cada una con su ficha, y la auditoría del 28 sep encontró 0 hallazgos de marca y 0 de layout (`14 Auditoría`). Como **prototipo** es débil:

- Solo hay 22 reacciones en todo el archivo y 5 flujos lineales de clic en clic (`11 Prototipos`).
- No hay Smart Animate, gestos, estados que dependan del tiempo, ni interacciones que crucen actores.

En la sustentación, el profesor de Interacción va a ver pantallas y no interacciones. La parte visual es correcta pero genérica: tarjetas en lista, botones y formularios que podrían ser de cualquier app. La identidad del Pase (el arco Portal) aparece solo en la vista de la visita. El residente, que es quien otorga, nunca ve su propio Pase como objeto.

| Especialidad | Hallazgos | Severidad máxima |
|---|---|---|
| Investigación / estrategia UX | 3 | 3 |
| Arquitectura de información | 3 | 2 |
| Interacción | 6 | 4 |
| UI visual e identidad | 5 | 3 |
| UX writing y contenido | 4 | 3 |
| Accesibilidad | 3 | 2 |
| Motion | 3 | 3 |
| Ingeniería e integración | 4 | 3 |

## 1. Investigación / estrategia UX

| # | Hallazgo | Evidencia | Sev. | Qué cambia |
|---|---|---|---|---|
| I-1 | Cada flujo responde a un hallazgo del diagnóstico. F-11 «Integración caída» sale directo del caso de Refugio Campestre (0 de 312 usuarios sincronizados). | `02 Flujos` F-01 a F-11 | 0 | Se conserva |
| I-2 | Las pantallas muestran a Refugio Campestre como si su integración funcionara (Pases vigentes confirmados por el lector). Hoy esa integración está caída. En la demo, el ejemplo contradice el hecho que mejor sostiene el diagnóstico. | `R-P-01 · Lleno` (19:41), `P-E-01` (51:2) | 3 | El recorrido principal ocurre en un conjunto con lector en línea. Refugio aparece en Administración con la integración caída y su arreglo |
| I-3 | El colaborador tiene la misma prioridad que la visita (decisión tomada), pero solo aparece como segunda pestaña de Crear Pase. Nada lo acelera, aunque es el ingreso más frecuente. | `R-P-03` (22:1033) | 3 | Un Pase de colaborador se crea una vez y queda recurrente; la lista lo muestra como «Hoy le toca» |

## 2. Arquitectura de información

| # | Hallazgo | Evidencia | Sev. | Qué cambia |
|---|---|---|---|---|
| A-1 | La barra inferior tiene Pases, Avisos y Mi casa, pero Avisos y Mi casa no tienen ninguna reacción. En Present la navegación no existe. | `06 Residente`, conteo de reacciones: 0 | 2 | La navegación entre pestañas funciona |
| A-2 | «Ver Pases anteriores» no lleva a ninguna parte. | `R-P-01` (19:41) | 2 | Abre el historial |
| A-3 | Portería no puede pasar de «Esperados hoy» al detalle de un Pase. | `P-E-01` (51:2) | 2 | Tocar un esperado lo abre en el panel principal |

## 3. Interacción

| # | Hallazgo | Evidencia | Sev. | Qué cambia |
|---|---|---|---|---|
| X-1 | Hay 22 reacciones en total (10 en la página 05, 4 en la 07, 4 en la 08, 4 en la 09) y todas son «al clic, ir a» o «después de un tiempo, ir a». El prototipo no se puede usar: solo se recorre. | Conteo por página con la API | 4 | Prototipo en código con estado real: lo que hace un actor le cambia la pantalla a otro |
| X-2 | El estado del Pase no depende del tiempo. La barra de vigencia es un rectángulo fijo y «Por vencer» es otra pantalla, no algo que ocurre. | `R-P-08 · Por vencer` (25:2336) | 3 | La vigencia corre con un reloj; Por vencer y Vencido llegan solos |
| X-3 | Revocar pide confirmación con un diálogo y no se puede deshacer. Un diálogo protege de un error que el residente casi nunca comete y deja sin arreglo el que sí comete. | `R-P-10 · Confirmación` (25:2771) | 3 | Mantener presionado para revocar y deshacer durante 5 s |
| X-4 | Crear un Pase de alguien que ya vino exige escribir todo de nuevo. «Crear otro Pase» (R-P-13) existe, pero no se llega a él desde la lista. | `R-P-13` (26:2845) | 3 | La persona reciente queda a un toque: un toque precarga y otro crea |
| X-5 | Los límites de la administración aparecen como error después de tocar «Crear Pase». | `R-P-05 · Cupo agotado` (22:1319) | 3 | El cupo y la franja se ven antes de crear; el botón explica por qué no deja |
| X-6 | Ninguna interacción cruza actores. La lectura en portería no llega al residente ni a la visita. | `11 Prototipos`: cada flujo vive en una página | 4 | Un solo estado compartido: el lector confirma, el residente recibe el aviso y el Pase de la visita cambia |

## 4. UI visual e identidad

| # | Hallazgo | Evidencia | Sev. | Qué cambia |
|---|---|---|---|---|
| U-1 | El Pase del residente es una fila de lista sin arco ni QR. El objeto que define a Kino (X1 Portal, X8 «el arco significa esto es un Pase») solo existe para la visita. | `R-P-01`, `R-P-08` (25:2287) | 3 | El detalle abre el Pase vivo con su arco y su estado |
| U-2 | El detalle es un formulario de lectura (dato, dato, línea de tiempo) sin jerarquía de objeto. | `R-P-08 · Vigente` (25:2287) | 2 | Arriba el Pase, abajo la constancia |
| U-3 | Límites en 1440 px usa un tercio de la pantalla, y los controles −/+ no muestran qué efecto tiene el cambio. | `A-03 · Reposo` (59:345) | 2 | Una vista previa que dice cuántos Pases activos quedarían fuera |
| U-4 | En portería, la tarjeta principal ocupa el 55 % del ancho con tres líneas de dato y deja mucho espacio vacío. | `P-E-01` (51:2) | 2 | El resultado de la lectura ocupa la tarjeta (sí / no, con el motivo) y se lee desde 3 m |
| U-5 | La aurora es lo único orgánico del sistema y vive solo en la cabecera. El concepto biopunk aprobado en el encargo («dirección biopunk») no llega a la interacción. | `Aurora · cabecera`, `decisiones.md` F2 | 3 | Exploración biopunk (PROPUESTA): el Pase como tejido vivo que late, se marchita y cicatriza |

## 5. UX writing y contenido

| # | Hallazgo | Evidencia | Sev. | Qué cambia |
|---|---|---|---|---|
| W-1 | Variables sin resolver en la pantalla: «3 de {cupo} Pases activos.», «Tienes {cupo} Pases activos…». | `I19:109;14:298` y otras 8 instancias en la página 05; `06` «{cupo} Pases activos» | 3 | Se usa el número real |
| W-2 | «[PENDIENTE: unidad del cupo]» visible en la pantalla de Límites. | `A-03 · Reposo` (59:345) | 3 | Se decide un supuesto (cupo por casa) y se declara |
| W-3 | Las fichas acumulan 76 marcas [PENDIENTE] en las páginas 04 a 09. Son decisiones de producto abiertas, no texto de la pantalla. | Búsqueda por página | 2 | Se listan como supuestos del prototipo, abajo |
| W-4 | En portería, «Diana Arango · RECHAZADO» no dice el motivo en la fila. | `P-E-01` tabla | 2 | Cada rechazo lleva su motivo (V5) |

## 6. Accesibilidad

| # | Hallazgo | Evidencia | Sev. | Qué cambia |
|---|---|---|---|---|
| C-1 | Ningún texto baja de 12 px y los estados llevan palabra además de color. | Búsqueda de fontSize < 12: 0 | 0 | Se conserva |
| C-2 | «Revocar Pase» es un enlace rosado de 14 px sin área de toque visible. | `R-P-08` (25:2287) | 2 | Acción de 48 px de alto con mantener presionado |
| C-3 | No hay variante con movimiento reducido. | `12 Motion` | 2 | El prototipo respeta `prefers-reduced-motion` |

## 7. Motion

| # | Hallazgo | Evidencia | Sev. | Qué cambia |
|---|---|---|---|---|
| M-1 | Las transiciones son instantáneas y no usan la partitura del Pase (`paquetes/kino-motion/src/nucleo/pase.ts`). | Reacciones sin `transition` | 3 | Cada cambio de estado usa su verbo (aparecer, responder, caducar, revocar) |
| M-2 | El latido de «vigente» (M3D aprobado) no existe en la app. | `12 Motion` | 2 | El Pase vigente late a 1800 ms |
| M-3 | No hay espera del lector entre «Enviado» y «Confirmado»: el estado honesto se ve como un salto. | `R-P-06` (22:1603) | 2 | Un indicador de espera mientras el lector confirma |

## 8. Ingeniería e integración (regla 7)

| # | Hallazgo | Evidencia | Sev. | Qué cambia |
|---|---|---|---|---|
| E-1 | El estado honesto está bien modelado: Enviado no es Vigente hasta que el lector confirma. | `11 Prototipos` flujo 1 | 0 | Se conserva |
| E-2 | Integración caída (A-07) muestra el problema, pero no dice la causa conocida: 711 errores `add_person` por el campo correo. | `A-07 · Integración caída` (61:976) | 3 | El panel nombra la causa y propone dar el alta con teléfono |
| E-3 | Portería muestra «Vigente» para una visita que ya entró, cuando debería verse «Entró» o «Usado». | `P-E-01` fila 15:12 | 2 | Después de la lectura, el Pase de visita pasa a Usado |
| E-4 | No se ve qué pasa en el lector si la administración cambia un límite. | `A-03 · Guardado` | 2 | «Aplica a los Pases nuevos»: los activos conservan su vigencia (ya está en el texto) y la vista previa lo muestra |

## Supuestos del prototipo navegable (los [PENDIENTE] que hubo que resolver para que se pueda usar)

Son supuestos, no decisiones. Van a `decisiones.md` como PROPUESTA.

| [PENDIENTE] | Supuesto | Por qué |
|---|---|---|
| Unidad del cupo | Por casa: 5 Pases de visita activos al mismo tiempo | Es la que la administración puede controlar sin conocer a cada residente |
| Si QR y placa cierran el Pase de visita | Sí: después de entrar, queda Usado | Un Pase de visita es para una llegada; si sale y vuelve, se crea otro |
| Si el lector tiene teclado para el código | No: portería digita el código en su pantalla | No está confirmado que el lector lo acepte (voz.json, «noConfirmado») |
| Vigencia del código | La misma del Pase | Un solo reloj por Pase |
| Si la administración puede revocar | No en esta versión | Mantiene la regla «solo el residente otorga» |
| Renovación del colaborador | Recurrente sin fecha de fin; el residente lo revoca | Es el caso de la empleada fija |
