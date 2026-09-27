# Documento maestro — Kino

**Punto de entrada del proyecto. Toda entrega parte de aquí.**

Última actualización: 21 de septiembre de 2026 · Equipo: Nicolás Ramírez Acosta y Alejandro Monsalve Marín · Cliente-aliado: Manuel Arango

---

## 0. Cómo se usa este documento

1. **Antes** de producir cualquier entrega —académica o de producto— se lee este documento completo. Es lo que da continuidad: cada entrega hereda de la anterior en vez de empezar de cero.
2. **Al cerrar** una entrega se actualizan las secciones 3 a 7 y se agrega una línea en la bitácora del final.
3. Nada entra aquí sin **fuente y fecha**. Si un dato no tiene de dónde salió, no es un hecho: es un supuesto, y va en la columna que corresponde.
4. Una afirmación que se cae **no se borra**: pasa a §5 con lo que la refutó. Ese registro es el que evita volver a construir encima de algo ya descartado.
5. Un documento anterior con una premisa refutada **no queda inservible**. Se tacha la premisa y se hereda el resto. Ese fue el error de septiembre y es la razón de existir de este archivo.

**Dónde vive.** La copia canónica es el documento del proyecto de Claude «Kino» (`claude/documento-maestro-kino.md`), porque es lo que toda sesión lee automáticamente. La copia de la carpeta (`kino/MAESTRO-KINO.md`) es un espejo para el equipo. Si divergen, manda la del proyecto.

---

## 1. El encargo

| | |
|---|---|
| **Qué es Kino** | Plataforma de control de acceso para conjuntos cerrados. Antes se llamaba Arcana |
| **Estado** | MVP en producción en Monte Sereno, El Retiro, con dos comunidades: Refugio Campestre y Villas Campestres |
| **Quién compra** | La administración del conjunto. Manuel es desarrollador y aliado, no comprador |
| **Modelo** | B2B, marca blanca, suscripción. Monte Sereno es el piloto, no el destino |
| **Alcance** | De diseño a implementación, con libertad para replantear arquitectura, stack e identidad |
| **Restricción firme** | Convivir con la infraestructura instalada: cámaras térmicas, reconocimiento facial, LPR y talanquera, sobre HikCentral |
| **Horizonte académico** | Línea LE005, EAFIT. Entrega segunda semana de noviembre de 2026 |
| **Horizonte real** | El producto sigue después y lo sostiene el equipo. Ante un empate, gana lo que se sostiene en el tiempo |

---

## 2. La problemática y la pregunta

Esto es lo estable del proyecto. Si una entrega no se puede amarrar a esta sección, algo está mal en la entrega.

**Encuadre:** el recorrido del invitado, de la invitación a la portería. No es «arreglar la función de invitados» ni «rediseñar el producto entero»: es un hilo que atraviesa a todos los actores y se mantiene concreto y medible. *(Origen: brief v0.1, nota de encuadre, 4 sep 2026.)*

**Causa de fondo:** un desajuste entre conocimiento y autoridad para decidir quién entra. *(Origen: brief v0.1 §02. Confirmada y precisada por la inspección de sep 2026.)*

> El recorrido del invitado está roto de punta a punta porque el conocimiento y la autoridad para decidir quién entra están repartidos entre actores distintos. El residente, único que sabe a quién espera y por cuánto tiempo, no tiene dónde expresarlo, y la autoridad que de hecho ejerce —habilitar una placa— es involuntaria, ilimitada y no deja constancia. La administración conserva una autoridad nominal que no ejerce sobre ningún ingreso. Y como no existe el permiso temporal para una persona, dejar entrar a alguien obliga a convertirlo en usuario permanente.

**Pregunta guía v1**

> ¿Cómo podríamos lograr que, en un conjunto cerrado como Monte Sereno, la decisión sobre quién entra la tome quien conoce al visitante, sin que la comunidad pierda control, trazabilidad ni protección de los datos de quienes ingresan?

Versión corta, para decidir en el día a día: **¿cómo reunir conocimiento y autoridad para decidir quién entra?**

**Los cuatro retos**

- **R1.** Reconocer y acotar la autoridad de quien conoce al visitante.
- **R2.** Dejar constancia de quién autorizó a quién, por qué y hasta cuándo.
- **R3.** Dejar entrar sin convertir a nadie en usuario, también cuando el ingreso es recurrente.
- **R4.** Operar sobre el hardware instalado y proteger los datos de quien entra.

**Diferenciación**, para no volver a discutirla: integración con el hardware que el conjunto ya tiene, invitado sin cuenta y marca blanca. **No** la autonomía del residente, que los competidores ya ofrecen. El competidor diario a vencer es la llamada a portería.

---

## 3. Hechos vigentes

Prevalecen sobre cualquier documento anterior. Jerarquía de evidencia: inspección directa > entrevistas del 2 de septiembre > brief y documentos académicos.

| # | Hecho | Evidencia | Fecha | Grado |
|---|---|---|---|---|
| F1 | Ningún rol puede anunciar una visita, autorizar un ingreso en el momento ni fijar hasta cuándo entra una persona | Inspección, menús de los cuatro paneles; `matriz-capacidades.csv` | 14–16 sep 2026 | Observado |
| F2 | El residente ya concede acceso físico al registrar una placa: queda «Permitido» y se sincroniza, bajo un texto que dice que lo controla la administración | Inspección, prueba ejecutada con la placa TST001 | 16 sep 2026 | Observado, con prueba |
| F3 | La vigencia existe para los vehículos («Válido Desde / Hasta», ventanas de un año) y está oculta para su dueño | Inspección, portal de portería y panel de super admin | 14–16 sep 2026 | Observado |
| F4 | El invitado es un miembro permanente con rol «Visitante» y cuenta, sin fecha ni vigencia | Inspección, ficha de la propiedad 346 | 15 sep 2026 | Observado |
| F5 | Los 711 errores de HikCentral son todos `add_person` por el campo correo, sin resolver desde agosto | Inspección, `/super-admin/hikcentral-errors` | 16 sep 2026 | Observado |
| F6 | Refugio Campestre tiene el hardware instalado y 0 de 312 personas y 1 de 44 vehículos sincronizados: integración caída | Inspección + confirmación del equipo | 16 sep 2026 | Observado + confirmado |
| F7 | Simetría invertida: el portero ve de los residentes la vigencia y la sincronización que ellos no ven de sí mismos, más su cédula, teléfono y correo | Inspección, `/guard/2/users` y `/guard/2/vehicles` | 15 sep 2026 | Observado |
| F8 | Existe una sola cola de aprobación en el sistema, `sso-registration-requests`, anidada bajo Users. Aprueba **cuentas**, no ingresos: 4 solicitudes, todas aprobadas, una con rol Visitor | Captura del panel de super administrador | 21 sep 2026 | Observado |
| F9 | Hay un único Access Level en todo el sistema, binario, sin horarios, con 0 personas asignadas y sin sincronizar desde el 15 de mayo | Inspección, `/super-admin/access-levels` | 16 sep 2026 | Observado |
| F10 | Cero contratistas registrados y cero zonas comunes configuradas en Refugio, con las funciones construidas en los dos extremos | Inspección, paneles de administrador | 16 sep 2026 | Observado |
| F11 | Los colaboradores son el ingreso más frecuente del conjunto | Entrevistas del 2 sep + caracterización con el cliente | 2 sep 2026 | Declarado |

**Discrepancia abierta:** el panel de super administrador reporta 893 usuarios y los escritorios de comunidad suman 1.200 (312 + 888). Sin explicación. No usar una cifra sin decir cuál panel la da.

---

## 4. Decisiones tomadas

No se reabren salvo que el equipo lo pida o aparezca evidencia que las contradiga. Si aparece, se señala aparte y se registra en §5.

| Decisión | Razón | Fecha |
|---|---|---|
| El residente aprueba a sus propios invitados y colaboradores; la administración deja de ser un paso del ingreso | F1, F2: la autoridad ya la ejerce, falta reconocerla y acotarla | sep 2026 |
| La administración fija límites —cupos, duración, franjas— en vez de aprobar caso a caso | Le da un control verificable, que hoy no tiene | sep 2026 |
| El invitado sin cuenta se verifica con QR, placa o código de un solo uso; los tres conviven | F4, F5 y la Resolución SIC 52185: no puede depender de una sola vía | sep 2026 |
| Ingreso a la app con código por WhatsApp, sin contraseña. Teléfono obligatorio y único; el cambio de número pasa por administración | Baja la barrera de entrada; el correo es el campo que rompe la sincronización | sep 2026 |
| El registro no lo aprueba el administrador: se valida contra la cédula ya existente en la base de datos | Reemplaza un paso humano que hoy sí existe (F8), no construye uno nuevo | sep 2026, revisada 21 sep |
| Los arquetipos se construyen desde la evidencia de esta fase. No se usan los del trabajo 2026-1 | No tienen respaldo en la investigación propia y ponen al vigilante como usuario primario | 21 sep 2026 |
| Los arquetipos no llevan nombre, edad ni biografía inventados | Con cinco entrevistas sin citas documentadas, una persona con nombre propio sería ficción con apariencia de dato | 21 sep 2026 |

---

## 5. Afirmaciones derogadas

Se conservan a propósito. Si algo de esto reaparece en un documento nuevo, es señal de que se partió de una fuente vieja.

| Lo que se afirmó | Dónde | Qué lo refutó |
|---|---|---|
| «El Super Administrador aprueba a mano cada ingreso» | Brief v0.1 §01, §02, §04; documentos académicos de agosto y septiembre | Inspección: no existe bandeja ni cola de aprobación de ingresos en ninguno de los cuatro paneles (F1) |
| «El residente no tiene autonomía sobre sus invitados» | Brief v0.1 §02 | Ya concede acceso físico al registrar una placa (F2). El problema es que no lo sabe y no puede acotarlo |
| «El cuello de botella es el tiempo del Super Administrador» | Brief v0.1 §02, §04, §08 | No hay tiempo de aprobación que liberar. El argumento económico se reconstruyó sobre F6 y la norma |
| «Liberar tiempo de aprobación manual es argumento de compra» | Brief v0.1 §08 | Los argumentos que resisten: infraestructura pagada y sin operar, riesgo legal con fecha, y permisos que nadie puede rastrear |
| «El vigilante autoriza el ingreso» | Documentos de agosto | El ingreso lo permite un lector en la puerta. El vigilante supervisa |
| «La integración con hardware es una fortaleza del producto actual» | Brief v0.1 §07 | Lo es en Villas y está caída en Refugio, que es la comunidad del piloto (F6) |
| Arquetipos Valeria Gómez y Carlos Ramírez | Documentos de agosto, trabajo 2026-1 | Sin respaldo en la evidencia de esta fase |
| Cifras «8.800 copropiedades del Valle de Aburrá» y «1.080 copropiedades» | Documentos anteriores | Sin fuente verificable. Reemplazadas por las de Fedelonjas 2026 |
| Métrica «% de accesos que exigen al Super Administrador» | Brief v0.1 §08 | El baseline es cero. Reemplazada en el brief v0.2 |

---

## 6. Entregables producidos

En orden. Cada uno dice qué hereda y qué agrega, para que el siguiente sepa de dónde partir.

| Fecha | Entregable | Qué hereda | Qué agrega |
|---|---|---|---|
| ago 2026 | Documento conceptual IxD y Biblia integradora E1 | Encargo del cliente | Primer encuadre. Contiene afirmaciones de §5 |
| 2 sep 2026 | Prueba con cinco residentes de Monte Sereno | — | Única evidencia de usuario del proyecto. **Citas textuales pendientes de documentar** |
| 4 sep 2026 | Brief Kino v0.1 | Auditoría del equipo + prueba con residentes | Encuadre, usuarios, ambición, negocio, benchmark, dirección creativa, riesgos |
| 14–16 sep 2026 | Inspección directa por rol | Brief v0.1 | 59 observaciones sobre cinco roles, matriz de capacidades, y la corrección del mecanismo |
| 19 sep 2026 | Sistema de marca Kino | Dirección creativa del brief | Paleta, tipografías, tokens, verificación de contraste |
| 21 sep 2026 | Reporte de inspección por rol | Inspección | Lectura sujeto por sujeto, anexo de seguridad para el cliente |
| 21 sep 2026 | Tres guías del curso diligenciadas | Brief + inspección + entorno | Cuestionario depurado, PESTEL con fuentes, hallazgos, pregunta guía, experiencia deseada |
| 21 sep 2026 | Documento unificado de diagnóstico | Las tres guías | Arquetipos y veinte insights por arquetipo |
| 21 sep 2026 | **Brief Kino v0.2** | Brief v0.1 | Corrige el mecanismo conservando el encuadre. Métrica nueva con baseline real |

Los entregables viven en `enfasis/servicios_y_ experiencias_interactivas/entregas/` y en `enfasis/ixd/Entregas/`.

---

## 7. Pendientes

**Bloqueantes**, en orden. Cada uno detiene una decisión de diseño concreta.

| # | Pregunta | Quién responde | Qué bloquea |
|---|---|---|---|
| 1 | ¿HikCentral admite una credencial temporal sin crear una persona? | Manuel | Todo el invitado sin cuenta (R3). Si no la admite, cualquier pase reintroduce el correo obligatorio y con él los 711 errores |
| 2 | ¿Por qué está caída la sincronización de Refugio? | Manuel | Decide si el piloto sigue en Refugio o pasa a Villas |
| 3 | ¿Qué reglas de autorización tiene escritas el conjunto y quién responde por ellas? | Administración | El contenido de los límites (R1) |
| 4 | ¿Qué necesitaría la administración para confiar en una autorización hecha por un residente? | Administración | La forma del acuerdo que hace viable R1 |
| 5 | ¿Qué dispara aprobar una solicitud de registro? ¿Crea la persona en HikCentral? | Manuel | La relación entre F8 y F5 |

**Abiertos**

- Citas textuales de los cinco residentes del 2 de septiembre y de qué comunidad son. Único eslabón de evidencia sin respaldo escrito.
- Baseline del dolor: volumen de ingresos por tipo, con registros del sistema.
- Consentimiento biométrico actual y vía no biométrica ofrecida hoy.
- Comportamiento del sistema sin conexión en portería.
- Costo de la infraestructura instalada en Refugio.
- Discrepancia 893 contra 1.200 usuarios.

**Operativo:** borrar la placa de prueba `TST001` (id 799, Refugio Campestre), que quedó sincronizada con el sistema físico de acceso.

---

## 8. Fuentes externas verificadas

| Dato | Fuente | Consultada |
|---|---|---|
| 47,88% de la vivienda urbana del país en propiedad horizontal, ~6,7M unidades, 61,7% en Medellín; arriendo 40,8%; servicios de PH +13,42% anual a mayo 2026 contra 5,84% de inflación | Fedelonjas, vía [Portafolio](https://www.portafolio.co/mis-finanzas/vivienda/casi-la-mitad-de-viviendas-urbanas-en-colombia-estan-concentradas-en-conjuntos-cerrados-o-edificios-497094), 28 jun 2026 | 21 sep 2026 |
| Resolución 52185 del 28 de agosto de 2025: no se puede exigir biometría para el ingreso; vías alternativas no invasivas; autorización previa, expresa, informada y cualificada | [SIC, comunicado oficial](https://sedeelectronica.sic.gov.co/comunicado/la-superintendencia-de-industria-y-comercio-ordena-un-conjunto-residencial-habilitar-mecanismos-de-ingreso-que-no-impliquen-el-tratamiento) | 21 sep 2026 |
| 51,3% de los contratos de trabajo doméstico por días en 1S-2026 (42,8% en 2025); ~704.000 ocupados a marzo 2026; informalidad >87% | GEIH-DANE y Symplifica, vía [Infobae](https://www.infobae.com/colombia/2026/09/09/el-trabajo-domestico-cambia-de-ritmo-en-colombia-crecen-los-contratos-por-dias-y-la-informalidad-supera-el-87/), 9 sep 2026 | 21 sep 2026 |
| Neivor: autogestión de visitas por QR, integración con los sistemas de acceso del condominio, sincronización de cartera morosa con acceso vehicular | [Neivor, página de producto](https://landing.neivor.com/control-de-acceso-visitantes) | 21 sep 2026 |
| Ley 1581 de 2012, protección de datos personales; Ley 675 de 2001, propiedad horizontal | Normativa colombiana | — |

---

## 9. Bitácora de este documento

| Fecha | Qué cambió | Por qué |
|---|---|---|
| 21 sep 2026 | Creación. Se consolidan encargo, problemática, hechos, decisiones, derogados, entregables, pendientes y fuentes | Las entregas se estaban produciendo sin heredar de las anteriores, y el resultado era información dispersa sin hilo conductor |
