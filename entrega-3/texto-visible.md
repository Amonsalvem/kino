Kino · Entrega 3
La tarde
El Pase
En uso
El plan
Después
1 / 35

Kino · Entrega 3 · Diseño para la interacción y Estrategia de servicio · EAFIT LE005

¿Quién decide quién entra?

El residente sabe a quién espera. El sistema del conjunto no tiene dónde guardarlo.

Nico Ramírez · Alejandro Monsalve
Monte Sereno, El Retiro · oct 2026

Escenario · arquetipos A1 y A3 · cada paso, observado en la inspección

Martes · 2:00 p. m.

Carolina está en la oficina. Su hermano Andrés llega a las 3.
Hoy puede

llamar a portería o mandar un WhatsApp que nadie registra.

O puede

registrar la placa de Andrés: la puerta abre y la pantalla le dice que eso lo controla la administración.

Andrés

necesita una cuenta permanente, con correo, para una visita de una tarde.

Evidencia · observado en la inspección del 14 al 16 de sep 2026

Detrás de esa tarde hay un sistema que solo crea personas permanentes
0/312

usuarios sincronizados en Refugio Campestre, con el hardware instalado

711

errores de alta en HikCentral, todos por el campo correo

0

maneras de dar un ingreso temporal a una persona

Diagnóstico · entregas 1 y 2

Carolina tiene el conocimiento. La autoridad está en la administración, que no sabe a quién espera.

¿Cómo reunir conocimiento y autoridad para decidir quién entra?

En los cuatro recorridos de la entrega 2 falta el mismo objeto: algo que diga quién entra, para cuándo y hasta cuándo.

SOSTAC · S · Situación

Casi la mitad de la vivienda urbana de Colombia vive en propiedad horizontal
47,88 %

de la vivienda urbana del país

61,7 %

en Medellín

13,42 %

subieron los servicios de PH, contra 5,84 % de inflación

6,8 %

crecimiento anual del control de acceso global, 2024–2032

Fedelonjas vía Portafolio, jun 2026 · IMARC

El tiempo

Dos plazos: la sustentación y el producto
Académico
9 nov 2026

Prototipo probado con 5 residentes y sustentación.

Producto
Ene–mar 2027

Piloto pagado en Villas y Refugio.

Producto
Oct 2027

4 conjuntos con pago. Fin de este plan.

La solución

Carolina le da a Andrés un Pase

Con autor, motivo, vigencia y modo. Lo otorga el residente por el tiempo que decida, dentro de las franjas del conjunto. Andrés entra sin cuenta.

QR
Placa
Código de un solo uso

Lo que diferencia a Kino: integración probada con el hardware instalado, Pase sin cuenta y autoridad del residente dentro de las franjas.

Objetivo general · meta general

Reunir conocimiento y autoridad para decidir quién entra

Que el residente otorgue, acote y revoque el ingreso de sus visitas y colaboradores, sobre el hardware que el conjunto ya tiene y sin crear personas permanentes.

Meta general · octubre de 2027
4 conjuntos con pago, 95 % de los Pases confirmados por el lector en menos de 60 s, y ningún ingreso que exija dar de alta a una persona permanente

Lo que implica la mejora

Para que el Pase de Andrés exista cambian seis frentes
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

QA del prototipo de Figma «Kino · App»

226

pantallas diseñadas, en oscuro y claro, con ficha cada una

22

reacciones en todo el archivo, todas «al clic, ir a»

0

interacciones que crucen de un actor a otro

En Figma, lo que hacía Carolina no le llegaba a Andrés ni a portería. Por eso el prototipo se construyó en código.

QA por especialidad · 31 hallazgos · severidad de Nielsen

Los cuatro hallazgos que más cambiaron el prototipo
Interacción · sev. 4

Ningún estado depende del tiempo: Por vencer era una pantalla aparte.

Identidad · sev. 3

El residente nunca ve su Pase como objeto: el arco solo existía para la visita.

Escritura · sev. 3

«3 de {cupo} Pases activos» y «[PENDIENTE]» visibles en pantallas aprobadas.

Integración · sev. 3

La pantalla de integración caída no nombraba la causa: 711 errores por el campo correo.

Prototipo en vivo · el mismo de Reto

La tarde de Carolina, en las cuatro pantallas
Carolina crea y envía
Andrés abre el Pase sin cuenta
Portería lo lee
A Carolina le llega el aviso

2:01 p. m.

Carolina crea el Pase en 3 toques
I-01

Código por WhatsApp
Llega el código y se llena solo

I-03

Volver a invitar
Tocar a Andrés abre la hoja ya llena

I-05

Vigencia a tu medida
Unas horas, un día o una estadía de meses

I-06

Nacimiento del Pase
El botón se vuelve el arco del Pase

2:01 p. m. · 3 s después

El Pase queda vigente cuando el lector lo confirma
I-07

Espera del lector
Borde punteado hasta que HikCentral responde

I-02

Pase vivo en la lista
La barra se consume con el tiempo

I-14

Extender
+1 h, +1 día o +1 semana, sin tope

I-13

Mantener para revocar
Anillo de 0,8 s y deshacer por 5 s

Sin confirmar
Vigente
Por vencer
Rechazado

2:02 p. m.

A Andrés le llega el Pase por WhatsApp
I-08

Compartir por WhatsApp
Imagen con QR, código y enlace

I-09

Pase vivo en el navegador
QR, placa o código en el mismo arco; cambia solo si Carolina lo extiende o lo revoca

3:04 p. m.

El lector lee la placa de Andrés
I-10

Lectura
La talanquera sube y portería ve por qué entró

I-11

Aviso de llegada
«Andrés entró por Portería principal»

I-12

6:10 p. m. · Laura llega tarde
«Venció a las 6:00 p. m.» y «Llamar a Carolina»

Los ingresos que más se repiten · arquetipos A2 y A1 · decisión E3-2

Marta entra cada día. La mamá de Carolina se queda dos meses.
Colaborador recurrente
Marta Ospina · aseo y cocina

Lunes a viernes, 7 a. m. a 5 p. m., hasta que Carolina lo revoque. Se crea una vez.

Estadía
Rosa Ruiz · se queda

«Se queda»: de 3 días a 3 meses o hasta una fecha. Entra y sale sin pedir nada.

Sin tope de visitas ni de duración. Los colaboradores son el ingreso más frecuente, y el 51,3 % del trabajo doméstico se contrata por días.

Administración · arquetipo A4

La administración fija franjas
I-15

Vista previa
Antes de guardar, ve qué Pase quedaría fuera

I-16

Integración y arreglo
Refugio: reintentar con teléfono

Identidad del Pase · dirección biopunk Aprobada · E3-1

El Pase se ve vivo porque hoy el acceso temporal no existe
Late

mientras está vigente
La vigencia se ve sin leerla

Se marchita

al vencer
Se agota a la vista

Cicatriza

al revocarse
Revocado tiene autor; queda la marca

La tecla B la apaga para comparar con la marca base.

Inventario de interacciones

17

implementadas y probadas de punta a punta en Chromium

3

planeadas: Pase en la billetera, háptica por estado, rostro como cuarto modo

16/16

pruebas del recorrido automático

Cada interacción tiene disparador, respuesta, regla y efecto en HikCentral, visibles en el panel derecho del prototipo.

Validación · Biblia 6.1

Evaluación por inspección con los cuatro arquetipos
Arquetipo y contexto	Dónde se traba	Sev.	Qué cambió
A3 · visita en la puerta sin señal	La imagen del WhatsApp no traía un QR real	3	La imagen lleva QR y código
A1 · residente con una mano	Elegir una hora lejana exige muchos toques	2	«Unas horas», «Un día», «Se queda»
A4 · portería en hora pico	Una lectura tapa la anterior	2	Bitácora con la última resaltada
A1 · familiar que se queda un mes	Solo había Pases de horas	3	«Se queda»: de 3 días a 3 meses, entra y sale

Prueba con cinco residentes de Monte Sereno: 27 oct al 7 nov, con protocolo, SEQ y SUS.

Avances de la Biblia · documento integrador Diex

Lo que la Biblia ya tiene
Apartado	Clase	Entrega	Estado
1.1–1.5 Contexto del reto	IxD · SD	E1	Completo
2.1–2.4 Usuario y diseño emocional	SD · UX	E1–E2	Completo
4.3 · 5.1 Requerimientos y modelo conceptual	UX · IxD	E2	Completo
3.1–3.3 SMART, propuesta de valor, estrategia	SD	E3	Nuevo hoy
5.2 Representación visual · 6.1 Validación	IxD · UX	E3	Nuevo hoy
3.4–3.7 · 4.1–4.2 · 6.2–7.2	Todas	E4–Final	Previsto

SOSTAC · O · Objetivos específicos SMART · cada uno mide una escena de la tarde

#	Escena	Objetivo	Meta	Cuándo
OE1	Carolina crea el Pase	Residentes de Monte Sereno crean un Pase de visita en el prototipo	90 % · <30 s · ≤3 toques	9 nov 2026
OE2	Las casas lo usan	Casas de Villas Campestres crean al menos un Pase	60 % de las casas	8 semanas de piloto
OE3	Marta entra sin llamada	Ingresos de colaboradores recurrentes con Pase	80 %	Ene–mar 2027
OE4	El lector confirma	Pases confirmados por el lector; Refugio sincronizado	98 % <60 s · ≥95 %	31 mar 2027
OE5	La administración renueva	Monte Sereno renueva y 2 conjuntos nuevos firman piloto pagado	4 conjuntos	31 oct 2027

Conexión de los objetivos específicos con el plan general

OE4 primero, OE5 al final
Objetivo general: reunir conocimiento y autoridad
 ├─ OE1 crear un Pase en 30 s ...... Producto    → valida la propuesta
 ├─ OE2 adopción del residente .......... Servicio    → el residente usa su autoridad
 ├─ OE3 colaborador sin llamada ......... Producto    → el ingreso de mayor volumen
 ├─ OE4 integración confirmada .......... Tecnología  → el Pase existe en la puerta
 └─ OE5 renovación y conjuntos nuevos ... Negocio     → la meta general

OE4 es la condición técnica de todos. OE2 y OE3 son la evidencia que vende OE5.

Plan estratégico SOSTAC

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

SOSTAC · S · Estrategia · nombradas con sustantivo

Estrategia	Objetivo	Eje estratégico
Simplificación del otorgamiento	OE1	Interactividad y personalización
Validación con residentes reales	OE1	Soporte y acompañamiento
Acompañamiento de la adopción	OE2	Soporte y acompañamiento
Diversificación de los canales del Pase	OE2	Omnicanalidad y accesibilidad
Recurrencia del colaborador	OE3	Automatización y gestión
Integración confiable con HikCentral	OE4	Automatización y gestión
Transparencia del estado	OE4	Automatización y gestión
Penetración por los instaladores	OE5	Omnicanalidad y accesibilidad
Fidelización con evidencia	OE5	Automatización y gestión

SOSTAC · T · Tácticas

Qué	Cómo	Quién	Cuándo
Volver a invitar	4 personas recientes a un toque	Equipo	Prototipo · hecho
Prueba con 5 residentes	6 tareas, SEQ y SUS	Equipo y admón.	27 oct – 7 nov
Alta con teléfono	Reintentar las 711 sin correo	Equipo y Manuel	Nov – dic 2026
Pase por WhatsApp	Plantilla de utilidad con imagen y enlace	Equipo	Dic 2026
Día de lanzamiento	Puesto en la entrada: primer Pase con cada residente	Equipo y admón.	Ene 2027
Reporte semanal	Entradas, rechazos con motivo, salud del lector	Equipo	Feb 2027
Aliados instaladores	Ficha comercial para instaladores Hikvision	Equipo	Abr – jun 2027

SOSTAC · A · Plan de acción

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

SOSTAC · C · Control · KPI de uso y adopción · método GQM

Pregunta	KPI	Meta	Etapa
¿Crear un Pase es más rápido que llamar?	Tiempo para crear	< 30 s	Comportamiento
¿Se entiende sin ayuda?	Éxito de la tarea	≥ 90 %	Satisfacción
¿Cómo lo perciben?	SUS	≥ 80	Satisfacción
¿Las casas usan su autoridad?	Casas con ≥1 Pase	≥ 60 %	Conversión
¿Vuelven a usarlo?	Retención a 2 semanas	≥ 50 %	Compromiso
¿El colaborador entra sin llamada?	Ingresos con Pase	≥ 80 %	Comportamiento

OE1 · OE2 · OE3

SOSTAC · C · Control · KPI de confianza y negocio

Pregunta	KPI	Meta	Etapa
¿El Pase existe en la puerta?	Confirmados en <60 s	≥ 98 %	Confianza
¿Refugio volvió a operar?	Sincronización	≥ 95 %	Confianza
¿Kino dice la verdad?	Vigente en Kino, rechazado en la puerta	≤ 0,5 %	Confianza
¿Los rechazos se explican?	Rechazos con motivo	100 %	Confianza
¿La administración ve valor?	NPS de la administración	≥ 30	Satisfacción
¿Crece la base?	Conjuntos con pago	4	Conversión

OE4 · OE5 · revisión semanal, mensual y trimestral

Kino como empresa · a 1 año, octubre de 2027

La tarde de Carolina, en cuatro conjuntos
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
Objetivo de empresa	Estrategia	KPI	Año
40 conjuntos en Antioquia	Replicación con instaladores	Conjuntos con pago	2028
Segundo y tercer fabricante	Independencia del fabricante	Conectores en producción	2028–29
Punto de equilibrio	Eficiencia en la implementación	Días hasta el primer Pase	2029
250 conjuntos con Bogotá	Expansión	Ingreso recurrente mensual	2030

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

Otorga, acota y revoca. PWA con @kino/motion.

F2 · OE2
Pase vivo

La visita entra sin cuenta, con QR, placa o código.

F3 · OE3 OE4
Kino Portería

El porqué de cada lectura, legible desde 3 m.

F4 · OE4 OE5
Kino Administración

Franjas con vista previa y salud de la integración.

F5 · OE4
Conector HikCentral

Persona temporal con vigencia y cola de reintentos.

F6 · OE2
Kit de implementación

Un conjunto nuevo opera en menos de 10 días.

Martes · 3:04 p. m.

«Andrés entró por Portería principal»

Lo que falta verificar antes del piloto

¿HikCentral admite una persona temporal con vigencia? Manuel
¿Cuántas casas tiene Villas Campestres? El sistema reporta 888 usuarios
¿Qué precio por casa acepta una administración?
¿Por qué el sistema dice 893 usuarios y las comunidades suman 1.200?
¿Cuántas copropiedades del Oriente tienen hardware Hikvision?

Prototipo, QA, estrategia y Biblia: carpeta entrega-3/ del repositorio.