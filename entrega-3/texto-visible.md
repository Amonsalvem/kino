Kino · Entrega 3
Kino · Entrega 3
Inicio
Interacción
Brief
SOSTAC
KPI
Horizonte
1 / 1
Diseño para la interacción · Estrategia de servicio · EAFIT LE005
El Pase
se usa
Prototipo con todas sus interacciones, avances de la Biblia y el plan para que Kino siga después de noviembre.
Nico Ramírez · Alejandro Monsalve
Monte Sereno, El Retiro · oct 2026
Presentamos dos materias en una: primero la interacción del prototipo, que es el mismo que llevamos a Reto; después el brief y la estrategia. Las teclas N y L muestran y ocultan estas notas y la barra.
Dónde estamos
Tres entregas, un solo hilo
Entrega 1 · ago–sep
Diagnóstico
Conocimiento y autoridad viven en actores distintos.
Entrega 2 · sep
Flujos y mapa
El objeto que falta en los cuatro recorridos: el Pase.
Entrega 3 · hoy
Prototipo y estrategia
El Pase funciona entre cuatro actores, con un plan de 12 meses.
El diagnóstico dijo que quien sabe quién entra no tiene cómo decirlo. La entrega 2 encontró el objeto que faltaba. Hoy lo mostramos funcionando y con un plan.
Parte 1 · Diseño para la interacción
Interacción
Biblia, QA del prototipo de Figma, el prototipo en vivo y cada interacción con su regla.
Avances de la Biblia · documento integrador Diex
Lo que la Biblia ya tiene
Apartado
Clase
Entrega
Estado
1.1–1.5 Contexto del reto
IxD · SD
E1
Completo
2.1–2.4 Usuario y diseño emocional
SD · UX
E1–E2
Completo
4.3 · 5.1 Requerimientos y modelo conceptual
UX · IxD
E2
Completo
3.1–3.3 SMART, propuesta de valor, estrategia
SD
E3
Nuevo hoy
5.2 Representación visual · 6.1 Validación
IxD · UX
E3
Nuevo hoy
3.4–3.7 · 4.1–4.2 · 6.2–7.2
Todas
E4–Final
Previsto
La Biblia va al día con la ruta del curso: lo de la entrega 3 queda escrito hoy y lo de las entregas 4 y 5 tiene su encabezado listo.
QA del prototipo de Figma «Kino · App»
226
pantallas diseñadas, en oscuro y claro, con ficha cada una
22
reacciones en todo el archivo: se recorre, no se usa
0
interacciones que crucen de un actor a otro
La especificación está completa. Al prototipo le faltaban tiempo, estado y consecuencias entre actores.
Contamos las reacciones con la API de Figma: 10 en residente, 4 en visita, 4 en portería, 4 en administración. Todas son «al clic, ir a». El hallazgo más grave: nada de lo que hace un actor le cambia la pantalla a otro.
QA por especialidad · 31 hallazgos · severidad de Nielsen
Lo genérico que quitamos
Interacción · sev. 4
Ningún estado depende del tiempo. Por vencer era otra pantalla, no algo que ocurre.
Identidad · sev. 3
El residente nunca ve su Pase como objeto: el arco solo existía para la visita.
Escritura · sev. 3
«3 de {cupo} Pases activos» y «[PENDIENTE]» visibles en pantallas aprobadas.
Integración · sev. 3
La pantalla de integración caída no nombraba la causa: 711 errores por el campo correo.
El QA completo está en entrega-3/qa-prototipo.md: ocho especialidades, cada hallazgo con su nodo de Figma. Aquí van los cuatro que más cambiaron el prototipo.
Prototipo en vivo · el mismo de Reto
Tócalo
Cuatro actores, un solo estado.
Residente crea y envía
Visita abre sin cuenta
Portería lee
Al residente le llega el aviso
Recorrido para la clase: entrar con WhatsApp, tocar Laura en «Volver a invitar», Crear Pase, ver cómo pasa de Sin confirmar a Vigente, Enviar por WhatsApp, abrir el enlace en el teléfono de la visita, leer su QR en portería. Para ver las notas de cada interacción, abrir prototipo.html en pantalla completa.
Residente · otorga y revoca
Crear un Pase en 3 toques
I-01
Código por WhatsApp
Llega el código y se llena solo
I-03
Volver a invitar
Un toque abre la hoja ya llena
I-05
Límites a la vista
El botón dice por qué no deja crear
I-06
Nacimiento del Pase
El botón se vuelve el arco del Pase
I-13
Mantener para revocar
Anillo de 0,8 s y deshacer por 5 s
El diálogo de confirmación para revocar protegía de un error raro y dejaba sin arreglo el común. Lo cambiamos por mantener presionado y deshacer: el gesto evita el toque accidental y el deshacer arregla el arrepentimiento.
Estado honesto · el Pase vive
Vigente solo si el lector confirmó
I-07
Espera del lector
Borde punteado hasta que HikCentral responde
I-02
Pase vivo en la lista
La barra se consume; vigente late a 1800 ms
I-14
Extender
+1 h o +2 h dentro del máximo del conjunto
I-17
Movimiento reducido
Fundidos en lugar de escalas y latidos
Sin confirmar
Vigente
Por vencer
Rechazado
Este es el hecho de Refugio Campestre convertido en interacción: 0 de 312 usuarios sincronizados. Si Kino mostrara vigente lo que la puerta no conoce, repetiría el error de la app actual.
Visita · sin cuenta
Entra con un enlace
I-08
Compartir por WhatsApp
Imagen con QR, código y enlace
I-09
Pase vivo en el navegador
QR, placa o código en el mismo arco
—
Cambia solo
Si lo revocan o lo extienden, el enlace lo muestra
La imagen del WhatsApp lleva el QR real y el código: si la visita llega sin señal, igual entra. Ese defecto lo encontró la evaluación por inspección y ya está corregido.
Portería · el lector decide
Se lee desde 3 metros
I-10
Lectura
QR, placa o código; la talanquera sube
I-12
Rechazo con motivo
«Venció a las 6:00 p. m.»
I-11
Aviso de llegada
Al residente le llega quién entró
Llamar al residente queda en la constancia, pero no abre la entrada. Si el residente quiere que entre, extiende el Pase y el lector vuelve a leer.
Administración · fija el marco
Límites con su consecuencia
I-15
Vista previa
Qué Pase quedaría por encima del tope
I-16
Integración y arreglo
Refugio: reintentar con teléfono
El cambio de límites cruza de actor: si la administración baja el cupo, el residente lo ve en su hoja de Crear Pase al instante. La sincronización de Refugio es una simulación del arreglo propuesto, no un dato.
Inventario de interacciones
17
implementadas y probadas de punta a punta en Chromium
3
planeadas: Pase en la billetera, háptica por estado, rostro como cuarto modo
15/15
pasos del recorrido automático sin errores
Cada interacción tiene disparador, respuesta, regla y efecto en HikCentral. El panel derecho del prototipo los muestra en vivo.
El rostro queda planeado y opcional por la Resolución 52185 de 2025 de la SIC: no se puede exigir biometría y siempre debe haber una vía no invasiva.
Exploración biopunk
Propuesta
El Pase como tejido
Late
mientras está vigente
Hoy no existe el acceso temporal: se tiene que ver vivo
Se marchita
al vencer
La vigencia se agota a la vista
Cicatriza
al revocarse
Revocado tiene autor; queda la marca
Sinapsis
cuando el lector reconoce
El estado honesto, en la puerta
Tecla B en el prototipo. No toca ningún token aprobado.
Cada rasgo nuevo responde a un problema del diagnóstico. Queda como propuesta en decisiones.md: la marca la decide el equipo.
Validación · Biblia 6.1
Evaluación por inspección con los cuatro arquetipos
Arquetipo y contexto
Dónde se traba
Sev.
Qué cambió
A3 · visita en la puerta sin señal
La imagen del WhatsApp no traía un QR real
3
La imagen lleva QR y código
A1 · residente con una mano
Elegir una hora lejana exige muchos toques
2
Atajos «Ya», «Esta tarde», «Mañana»
A4 · portería en hora pico
Una lectura tapa la anterior
2
Bitácora con la última resaltada
A1 · cupo lleno
El tope aparecía después de escribir el nombre
2
El tope se dice antes que todo
Prueba con cinco residentes de Monte Sereno: 27 oct al 7 nov, con protocolo, SEQ y SUS.
Esto es una evaluación por inspección: recorrimos cada tarea poniéndonos en el contexto de cada arquetipo del diagnóstico. La prueba con residentes reales va después y sus resultados entran a la Biblia.
Parte 2 · Estrategia de servicio
Brief
Problema y tiempo, la solución y lo que implica, objetivo y meta.
El problema
Quien sabe quién entra no tiene cómo decirlo
0/312
usuarios sincronizados en Refugio Campestre, con el hardware instalado
711
errores de alta en HikCentral por el campo correo
0
maneras de dar un ingreso temporal a una persona
Observado · inspección del 14 al 16 de sep 2026
El residente sabe a quién espera y no puede expresarlo; la administración tiene la autoridad nominal y no sabe a quién. El sistema solo sabe crear personas permanentes.
El tiempo
Cuatro semanas, y doce meses
Académico
9 nov 2026
Prototipo probado con 5 residentes y sustentación.
Producto
Ene–mar 2027
Piloto pagado en Villas y Refugio.
Producto
Oct 2027
4 conjuntos con pago. Fin de este plan.
Separamos lo que existe solo por la entrega (azul) de lo que es producto (verde). El producto sigue después de noviembre y lo sostenemos nosotros.
La solución
El Pase
Autor, motivo, vigencia y modo. Lo otorga el residente dentro de los límites de la administración. La visita entra sin cuenta.
QR
Placa
Código de un solo uso
La diferencia de Kino es la suma: integración probada con el hardware instalado, Pase sin cuenta y autoridad del residente acotada.
La autonomía del residente sola no nos diferencia: Neivor ya vende autogestión de visitas por QR. Lo que nadie junta es el hardware que el conjunto ya pagó, la visita sin cuenta y los límites.
Todo lo que implica la mejora
Seis frentes cambian a la vez
Producto
App del residente, Pase vivo, portería y administración.
Datos
Teléfono obligatorio y único; el correo deja de serlo.
Integración
Persona temporal con «Válido desde / hasta» en HikCentral.
Operación
Carga por cédula, capacitación de portería, señalética.
Legal
Ley 1581 y SIC 52185: la biometría nunca se exige.
Negocio
Suscripción que paga la administración del conjunto.
Quitar el correo arregla dos cosas con una decisión: la fricción del registro y los 711 errores de sincronización. Lo que falta confirmar con Manuel es si HikCentral admite una persona temporal sin crearla permanente.
Objetivo general · el qué
Reunir conocimiento y autoridad para decidir quién entra
Que el residente otorgue, acote y revoque el ingreso de sus visitas y colaboradores, sobre el hardware que el conjunto ya tiene y sin crear personas permanentes.
Meta general · octubre de 2027
4 conjuntos con pago, 95 % de los Pases confirmados por el lector en menos de 60 s, y ningún ingreso que exija dar de alta a una persona permanente
Los dos conjuntos nuevos son una meta propuesta por el equipo. La recalibramos cuando sepamos cuántas copropiedades del Oriente tienen hardware Hikvision.
Objetivos específicos SMART · acción + métrica + usuario + contexto + tiempo
#
Objetivo
Meta
Cuándo
OE1
Residentes de Monte Sereno crean un Pase de visita en el prototipo
90 % · <30 s · ≤3 toques
9 nov 2026
OE2
Casas de Villas Campestres crean al menos un Pase
60 % de las casas
8 semanas de piloto
OE3
Ingresos de colaboradores recurrentes con Pase y sin llamada
80 %
Ene–mar 2027
OE4
Pases confirmados por el lector; Refugio sincronizado
98 % <60 s · ≥95 %
31 mar 2027
OE5
Monte Sereno renueva y 2 conjuntos nuevos firman piloto pagado
4 conjuntos
31 oct 2027
Donde no existe medición, la meta es un supuesto y el punto de partida se mide en la semana 1 del piloto. OE1 ya es medible con el prototipo.
Conexión de los objetivos específicos con el plan general
Cada objetivo sostiene al siguiente
Objetivo general: reunir conocimiento y autoridad
├─
OE1
crear un Pase sin fricción ...... Producto    → valida la propuesta
├─
OE2
adopción del residente .......... Servicio    → el residente usa su autoridad
├─
OE3
colaborador sin llamada ......... Producto    → el ingreso de mayor volumen
├─
OE4
integración confirmada .......... Tecnología  → el Pase existe en la puerta
└─
OE5
renovación y conjuntos nuevos ... Negocio     → la meta general
OE4 es la condición técnica de todos. OE2 y OE3 son la evidencia que vende OE5.
Parte 3 · Plan estratégico
SOSTAC
Situación, objetivos, estrategia, tácticas, acción y control.
El plan en una lámina
S
Situación
Mercado grande; el manual es el competidor.
O
Objetivos
OE1 a OE5, SMART.
S
Estrategia
9 estrategias en 4 ejes.
T
Tácticas
Qué, cómo, quién, cuándo.
A
Acción
Oct 2026 a oct 2027.
C
Control
12 KPI con GQM.
S · Situación
El problema se repite en miles de conjuntos
47,88 %
de la vivienda urbana de Colombia en propiedad horizontal
61,7 %
en Medellín
13,42 %
subieron los servicios de PH, contra 5,84 % de inflación
6,8 %
crecimiento anual del control de acceso global, 2024–2032
Fedelonjas vía Portafolio, jun 2026 · IMARC
Competencia: el método manual (llamada, minuta, WhatsApp) es el más fuerte. Neivor y ComunidadFeliz nacen desde la administración y las finanzas; ZKTeco vende su hardware con su software. El hueco es la autorización encima del hardware instalado.
S · Estrategias · empiezan por sustantivo
Estrategia
Objetivo
Eje estratégico
Simplificación del otorgamiento
OE1
Interactividad y personalización
Validación con residentes reales
OE1
Soporte y acompañamiento
Acompañamiento de la adopción
OE2
Soporte y acompañamiento
Diversificación de los canales del Pase
OE2
Omnicanalidad y accesibilidad
Recurrencia del colaborador
OE3
Automatización y gestión
Integración confiable con HikCentral
OE4
Automatización y gestión
Transparencia del estado
OE4
Automatización y gestión
Penetración por los instaladores
OE5
Omnicanalidad y accesibilidad
Fidelización con evidencia
OE5
Automatización y gestión
T · Tácticas
Qué
Cómo
Quién
Cuándo
Volver a invitar
4 personas recientes a un toque
Equipo
Prototipo · hecho
Prueba con 5 residentes
6 tareas, SEQ y SUS
Equipo y admón.
27 oct – 7 nov
Alta con teléfono
Reintentar las 711 sin correo
Equipo y Manuel
Nov – dic 2026
Pase por WhatsApp
Plantilla de utilidad con imagen y enlace
Equipo
Dic 2026
Día de lanzamiento
Puesto en la entrada: primer Pase con cada residente
Equipo y admón.
Ene 2027
Reporte semanal
Entradas, rechazos con motivo, salud del lector
Equipo
Feb 2027
Aliados instaladores
Ficha comercial para instaladores Hikvision
Equipo
Abr – jun 2027
A · Plan de acción
De la sustentación al cuarto conjunto
Oct–nov 26
Sustentación
Prototipo y prueba
Nov–dic 26
Refugio
≥95 % sincronizado
Dic 26
Beta
Backend y WhatsApp
Ene–mar 27
Piloto
Mide OE2 a OE4
Abr–jun 27
Aliados
10 conjuntos contactados
Jul–oct 27
Meta
4 conjuntos
El primer bloque es académico; desde noviembre todo es producto. La dependencia crítica es la respuesta de Manuel sobre la credencial temporal en HikCentral.
C · Control
KPI
Método GQM: objetivo, pregunta, métrica. Cada KPI atado a un objetivo y a una etapa.
KPI · uso y adopción
Pregunta
KPI
Meta
Etapa
¿Crear un Pase es más rápido que llamar?
Tiempo para crear
< 30 s
Comportamiento
¿Se entiende sin ayuda?
Éxito de la tarea
≥ 90 %
Satisfacción
¿Cómo lo perciben?
SUS
≥ 80
Satisfacción
¿Las casas usan su autoridad?
Casas con ≥1 Pase
≥ 60 %
Conversión
¿Vuelven a usarlo?
Retención a 2 semanas
≥ 50 %
Compromiso
¿El colaborador entra sin llamada?
Ingresos con Pase
≥ 80 %
Comportamiento
OE1 · OE2 · OE3
KPI · confianza y negocio
Pregunta
KPI
Meta
Etapa
¿El Pase existe en la puerta?
Confirmados en <60 s
≥ 98 %
Confianza
¿Refugio volvió a operar?
Sincronización
≥ 95 %
Confianza
¿Kino dice la verdad?
Vigente en Kino, rechazado en la puerta
≤ 0,5 %
Confianza
¿Los rechazos se explican?
Rechazos con motivo
100 %
Confianza
¿La administración ve valor?
NPS de la administración
≥ 30
Satisfacción
¿Crece la base?
Conjuntos con pago
4
Conversión
OE4 · OE5 · revisión semanal, mensual y trimestral
Parte 4 · Kino como empresa
Horizonte
A un año y a cinco: objetivos, KPI, estrategias, tácticas y lo que hay que comprar.
Hacia dónde vamos en 1 año · octubre de 2027
4
conjuntos con pago
4
productos en producción conectados a HikCentral
1
caso documentado con KPI reales
SAS
constituida, con facturación electrónica y bases de datos ante la SIC
Horizonte de empresa · 3 a 5 años · ambición del equipo
La capa de autorización sobre cualquier lector
Objetivo de empresa
Estrategia
KPI
Año
40 conjuntos en Antioquia
Replicación con instaladores
Conjuntos con pago
2028
Segundo y tercer fabricante
Independencia del fabricante
Conectores en producción
2028–29
Punto de equilibrio
Eficiencia en la implementación
Días hasta el primer Pase
2029
250 conjuntos con Bogotá
Expansión
Ingreso recurrente mensual
2030
Bogotá: el 69 % de los predios está en propiedad horizontal según el Catastro Distrital 2025. Las cifras de conjuntos son ambición del equipo; las calibramos con el precio que acepte una administración.
Lista de mercado · lo que hay que comprar o contratar
WhatsApp Business
Por un proveedor oficial. ≈ US$0,0008 por mensaje de utilidad en Colombia, por confirmar con Meta.
HikCentral OpenAPI
Acceso y programa de socios de Hikvision. Por cotizar con Manuel.
Conector ZKTeco o Dahua
Para no depender de un fabricante. Horizonte 2028.
Tableta de portería
Android en modo kiosco, con soporte.
Facturación electrónica
Proveedor habilitado ante la DIAN y pasarela B2B.
Legal de datos
Registro de bases ante la SIC y política de la Ley 1581.
También: nube con región en Latinoamérica, billetera de Apple y Google, póliza de responsabilidad civil, kit de implementación y CRM comercial.
Fichas de producto
F1 · OE1 OE2 OE3
Kino Residente
Otorga, acota y revoca. PWA con
@kino/motion
.
F2 · OE2
Pase vivo
La visita entra sin cuenta, con QR, placa o código.
F3 · OE3 OE4
Kino Portería
El porqué de cada lectura, legible desde 3 m.
F4 · OE4 OE5
Kino Administración
Límites con vista previa y salud de la integración.
F5 · OE4
Conector HikCentral
Persona temporal con vigencia y cola de reintentos.
F6 · OE2
Kit de implementación
Un conjunto nuevo opera en menos de 10 días.
Cada ficha completa (propósito, interacciones, componentes, tecnologías y escenario de uso) está en entrega-3/estrategia.md §10 y en la Biblia.
Lo que falta verificar
Cinco preguntas antes del piloto
¿HikCentral admite una persona temporal con vigencia? Manuel
¿Cuántas casas tiene Villas Campestres? El sistema reporta 888 usuarios
¿Qué precio por casa acepta una administración?
¿Por qué el sistema dice 893 usuarios y las comunidades suman 1.200?
¿Cuántas copropiedades del Oriente tienen hardware Hikvision?
Prototipo, QA, estrategia y Biblia: carpeta
entrega-3/
del repositorio.
Fuentes: Fedelonjas vía Portafolio (28 jun 2026), Catastro Distrital vía Forbes, IMARC, SIC Resolución 52185 de 2025, GEIH-DANE y Symplifica vía Infobae, Meta y Leadsales para WhatsApp, Neivor. Todas enlazadas en estrategia.md.