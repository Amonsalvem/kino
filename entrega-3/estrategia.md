# Kino · Estrategia de servicio y horizonte de empresa

Entrega 3 · 19 oct 2026 · Nico Ramírez y Alejandro Monsalve

Estructura de las guías del curso: `entrega-3/fuentes/Plan_estrategico.pdf` (diagnóstico, objetivo general, SMART, SOSTAC, estrategias, tácticas, ejes estratégicos, fichas de producto) e `Indicadores_2.pdf` (KPI con el método GQM).

**Convención.** **[A]** marca lo que existe solo por la entrega académica. **[P]** marca una decisión de producto que sigue después de noviembre. Cada cifra externa trae su fuente. Las metas que dependen de una medición que todavía no existe se escriben como **supuesto** y dicen cómo se mide el punto de partida.

---

## 0. Problema, tiempo y solución en una página

| | |
|---|---|
| **Problema** | En los conjuntos cerrados, quien sabe quién debe entrar (el residente) no tiene cómo decirlo, y quien tiene la autoridad (la administración) no sabe a quién dejar entrar. El sistema actual solo sabe crear personas permanentes. Por eso la visita necesita cuenta, el colaborador se registra como si viviera ahí y el residente abre la puerta sin saberlo cuando registra una placa. *Observado, inspección 14–16 sep 2026 (`docs/proyecto/reporte-inspeccion-por-rol.md`).* |
| **Dónde duele hoy** | Refugio Campestre tiene el hardware instalado y 0 de 312 usuarios y 1 de 44 vehículos sincronizados. Los 711 errores de HikCentral son `add_person` rechazado por el campo correo. *Observado (`MAESTRO-KINO.md` §3).* |
| **Tiempo** | **[A]** Sustentación del prototipo: segunda semana de noviembre de 2026 (≈ 4 semanas). **[P]** Piloto pagado en Monte Sereno: enero a marzo de 2027. **[P]** Horizonte de este plan: 12 meses, hasta octubre de 2027. |
| **Solución** | **El Pase**: un objeto con autor, motivo, vigencia y modo (QR, placa o código de un solo uso) que el residente otorga a sus visitas y colaboradores. La administración fija las franjas horarias; no pone tope de visitas ni de duración y no aprueba caso a caso (E3-2). Un Pase puede ser de horas, de un día o una estadía de semanas o meses. La visita no crea cuenta. Kino da de alta el Pase en el hardware que el conjunto ya tiene (HikCentral) y solo lo muestra vigente cuando el lector confirma. |
| **Diferencia** | La autonomía del residente sola no diferencia a Kino: Neivor ya vende autogestión de visitas por QR ([Neivor](https://landing.neivor.com/control-de-acceso-visitantes)). Kino junta la integración probada con el hardware instalado, el Pase sin cuenta para la visita y la autoridad del residente dentro de las franjas de la administración. |

### Todo lo que implica la mejora

| Frente | Qué cambia | Efecto en trazabilidad y en HikCentral (regla 7) |
|---|---|---|
| Producto · residente | App (PWA) con ingreso por código de WhatsApp, Pases vivos, crear en 3 toques, extender y revocar con deshacer | Cada Pase tiene autor y hora. Revocar da de baja en el lector cuando vence el deshacer |
| Producto · visita | Pase vivo en el navegador (imagen y enlace por WhatsApp), sin cuenta | Ya no se crea un usuario «Visitante» permanente |
| Producto · portería | Pantalla que dice por qué el lector dejó o no dejó entrar, y botón para llamar al residente | La llamada queda en la constancia. La llamada no abre la entrada |
| Producto · administración | Franjas, constancia y salud de la integración | La administración ve quién autorizó a quién; hoy no puede |
| Datos | El teléfono pasa a ser obligatorio y único; el correo deja de serlo | Quita la causa de los 711 errores `add_person` |
| Integración | Alta de persona temporal con «Válido desde / hasta» en HikCentral (por confirmar con Manuel, pendiente 1 del maestro) | Si HikCentral no admite credencial temporal, la placa por LPR es la vía que no crea persona |
| Operación | Implementación en sitio: carga de casas por cédula, capacitación de portería, señalética del QR | El registro se valida contra la cédula que ya está en la base, no lo aprueba la administración |
| Legal | Ley 1581 de 2012 y Resolución SIC 52185 de 2025: la biometría no se exige y siempre hay una vía no biométrica | El rostro queda como cuarto modo opcional y con autorización expresa |
| Negocio | Suscripción que paga la administración del conjunto (único comprador) | Sin dato |

---

## 1. Diagnóstico (S de SOSTAC, primera parte)

### 1.1 Problema: conclusiones del brief
1. El conocimiento y la autoridad para decidir quién entra viven en actores distintos. *Brief v0.2 §02.*
2. El super administrador no aprueba ingresos: no hay bandeja ni cola. Autorizar significa dar de alta a un usuario permanente. *Observado.*
3. El residente ya concede acceso físico al registrar una placa, mientras la pantalla le dice que lo controla la administración. *Observado.*
4. El correo obligatorio molesta al usuario y además rompe la sincronización con el lector. *Observado (711 errores).*

### 1.2 Público objetivo (arquetipos, `docs/proyecto/arquetipos-e-insights.md`)
| Arquetipo | Posición frente al sistema |
|---|---|
| A1 · El residente que recibe | Único que sabe a quién espera; ya abre la puerta sin saberlo |
| A2 · El colaborador recurrente | El ingreso más frecuente y el que menos existe en el producto. 51,3 % de los contratos de trabajo doméstico son por días en 1S-2026 ([Infobae, GEIH-DANE y Symplifica](https://www.infobae.com/colombia/2026/09/09/el-trabajo-domestico-cambia-de-ritmo-en-colombia-crecen-los-contratos-por-dias-y-la-informalidad-supera-el-87/)) |
| A3 · El visitante ocasional | Entrega datos de por vida para una visita de una tarde |
| A4 · Administración y portería | Quien compra y quien opera. Responde ante el consejo por ingresos que no puede rastrear |

### 1.3 Conclusiones del journey (entrega 2, `kino_entrega_2.html`)
- En cada uno de los cuatro recorridos, el momento crítico es la puerta, y ahí nadie tiene la información completa.
- El objeto que falta en todos los mapas es el mismo: **el Pase**.
- La simetría está invertida: el portero ve de los residentes lo que ellos no ven de sí mismos.

### 1.4 Insights que mueven la estrategia
1. **A1.** El residente ya decide quién entra, pero cree que no. → Nombrar y acotar la autoridad que ya ejerce.
2. **A2.** El dato que más cuesta pedir (el correo) es el que rompe la puerta. → Quitar el correo obligatorio resuelve la queja del registro y los 711 errores.
3. **A3.** La placa por LPR es la vía que exige menos datos personales. → El vehículo de la visita es el primer canal del Pase.
4. **A4.** La administración cree conservar un control que no ejerce. → El argumento de venta: hoy no tiene ese control, y con Kino lo ejerce por franjas y constancia.

### 1.5 Situación externa
| Dato | Fuente |
|---|---|
| 47,88 % de la vivienda urbana de Colombia está en propiedad horizontal (~6,7 M unidades); en Medellín, 61,7 % | Fedelonjas, vía [Portafolio, 28 jun 2026](https://www.portafolio.co/mis-finanzas/vivienda/casi-la-mitad-de-viviendas-urbanas-en-colombia-estan-concentradas-en-conjuntos-cerrados-o-edificios-497094) y [vivienda.com.co](https://vivienda.com.co/?p=3240) |
| Los servicios de propiedad horizontal subieron 13,42 % anual a mayo de 2026, contra 5,84 % de inflación | Fedelonjas, vía Portafolio (mismo enlace) |
| En Bogotá, el 69 % de los predios está en propiedad horizontal (2025) | Catastro Distrital, vía [Forbes Colombia](https://forbes.co/economia-y-finanzas/el-valor-de-los-inmuebles-de-bogota-supero-los-900-billones-con-un-alza-del-12-frente-al-2024-segun-el-catastro-distrital) |
| 74.521 copropiedades aseguradas a cierre de 2022, de ellas 63.388 residenciales (piso del universo, no el total) | Fasecolda, vía [El Tiempo](https://www.eltiempo.com/economia/sector-financiero/alerta-hay-bajo-aseguramiento-de-copropiedades-en-colombia-estan-las-razones-808115) |
| Mercado global de control de acceso: US$10.000 M en 2023, proyectado a US$18.300 M en 2032 (TACC 6,8 %) | [IMARC](https://www.imarcgroup.com/report/es/access-control-market) |
| No se puede exigir biometría para entrar a un conjunto; hay que ofrecer una vía no invasiva | [SIC, Resolución 52185 de 2025](https://sedeelectronica.sic.gov.co/comunicado/la-superintendencia-de-industria-y-comercio-ordena-un-conjunto-residencial-habilitar-mecanismos-de-ingreso-que-no-impliquen-el-tratamiento) |
| WhatsApp cobra por plantilla entregada desde julio de 2025; las de utilidad y autenticación en Colombia rondan US$0,0008 (fuente de terceros, por confirmar en la tarifa oficial de Meta) | [Meta, precios](https://developers.facebook.com/docs/whatsapp/pricing); [Leadsales](https://leadsales.io/blog/whatsapp-business-api-cuanto-cuesta/) |

**Competencia.**
- **El método manual** (llamada, minuta, WhatsApp) es el competidor más fuerte: es gratis y conocido. *Brief v0.2 §06.*
- **Neivor** vende autogestión de visitas por QR e integración con sistemas de acceso. No dice si la visita necesita cuenta.
- **ComunidadFeliz** reporta más de 6.900 conjuntos en diez países (dato del brief v0.2, por reconfirmar).
- **Portea** es una app de portería nacida en Medellín ([GetApp](https://www.getapp.co.uk/software/2104437/portea)).
- **ZKTeco** vende integración de hardware con su propio software ([caso en Bogotá](https://www.zkteco.com/en/case/Access_Control_Solution_with_Biometrics_for_a_Residential_Complex_in_Colombia)).

**Vacío de mercado.** No hay en la fuente una cifra oficial de cuántas copropiedades hay en Antioquia. La Cámara de Comercio de Medellín para Antioquia lleva su registro (Ley 675 de 2001). Conseguir ese número es la primera tarea de captación.

---

## 2. Objetivo general y meta general (O de SOSTAC)

**Objetivo general (el qué).**
- **[P]** Reunir el conocimiento y la autoridad para decidir quién entra a un conjunto: que el residente otorgue, acote y revoque el ingreso de sus visitas y colaboradores, dentro de las franjas de la administración, sobre el hardware que el conjunto ya tiene y sin crear personas permanentes.
- **[A]** Para la sustentación: demostrarlo en un prototipo que se puede usar de punta a punta.

**Meta general (a 12 meses, octubre de 2027) [P].** Kino opera en **4 conjuntos con pago**: Villas Campestres, Refugio Campestre y 2 conjuntos nuevos del Oriente antioqueño. El **95 % de sus Pases** queda confirmado por el lector en menos de 60 segundos, y **ningún ingreso** exige dar de alta a una persona permanente.

> *Supuesto declarado:* «2 conjuntos nuevos» es una meta propuesta por el equipo, no un dato del cliente. Se recalibra cuando se tenga el número de copropiedades del Oriente con hardware Hikvision instalado.

---

## 3. Objetivos específicos SMART

Fórmula del curso: **acción + métrica + usuario + contexto + tiempo**.

| # | Objetivo SMART | Usuario | Punto de partida | Por qué importa (R) |
|---|---|---|---|---|
| **OE1** | Lograr que el 90 % de 5 residentes de Monte Sereno cree un Pase de visita en **menos de 30 s y 3 toques o menos** en una prueba con el prototipo, **antes del 9 nov 2026** **[A+P]** | A1 | Hoy la tarea no existe: no hay cómo crear una visita con vigencia | Si crear un Pase es más lento que llamar a portería, nadie lo adopta (el manual es el competidor) |
| **OE2** | Lograr que el **60 % de las casas** de Villas Campestres cree al menos un Pase en las **primeras 8 semanas** del piloto (ene–feb 2027) **[P]** | A1 | 0 Pases; Villas tiene 888 usuarios (casas por confirmar) | Adopción del residente = valor para la administración |
| **OE3** | Lograr que el **80 % de los ingresos de colaboradores recurrentes** de Villas ocurra con un Pase y sin llamada a portería durante el **primer trimestre** del piloto (ene–mar 2027) **[P]** | A2 | Por medir en la semana 1 del piloto con la minuta de portería | Es el ingreso más frecuente |
| **OE4** | Lograr que el **98 % de los Pases** quede confirmado por el lector en **menos de 60 s**, y recuperar Refugio Campestre de 0/312 a **≥ 95 %** de usuarios sincronizados **antes del 31 mar 2027** **[P]** | A4 | Refugio: 0/312 usuarios, 1/44 vehículos, 711 errores | Sin integración, el lector no conoce el Pase |
| **OE5** | Lograr que la administración de Monte Sereno **renueve el contrato** y que **2 conjuntos nuevos** firmen piloto pagado **antes del 31 oct 2027** **[P]** | A4 (comprador) | 1 cliente (MVP) | Sostenibilidad del producto después de la universidad |

### Cómo se conecta cada objetivo específico con el plan general

```
Objetivo general: reunir conocimiento y autoridad
 ├─ OE1  crear un Pase en 30 s ───────────── Producto (residente)   → valida la propuesta antes de construir
 ├─ OE2  adopción del residente ───────────────── Servicio (implementación) → el residente usa su autoridad
 ├─ OE3  colaborador sin llamada ──────────────── Producto + Servicio      → el caso de mayor volumen
 ├─ OE4  integración confirmada ───────────────── Tecnología (HikCentral)  → el Pase existe en la puerta
 └─ OE5  renovación y nuevos conjuntos ─────────── Negocio                  → la meta general (4 conjuntos)
```
OE1 es la condición de OE2. OE2 y OE3 son la evidencia de valor que pide OE5. OE4 es la condición técnica de todos.

---

## 4. Estrategias (la segunda S de SOSTAC)

Regla del curso: cada estrategia empieza por un **sustantivo** y responde al **cómo**. Hay una o dos por objetivo, cada una ubicada en un eje estratégico del curso.

| Objetivo | Estrategia | Eje estratégico |
|---|---|---|
| OE1 | **Simplificación** del otorgamiento: el Pase se crea en una hoja, con la persona reciente a un toque y la franja visible antes de crear | 1 · Interactividad y personalización |
| OE1 | **Validación** iterativa con residentes reales antes de construir | 4 · Soporte y acompañamiento |
| OE2 | **Acompañamiento** de la adopción en el conjunto: el día de lanzamiento se acompaña en sitio y por WhatsApp | 4 · Soporte y acompañamiento |
| OE2 | **Diversificación** de los canales del Pase (QR, placa, código, imagen por WhatsApp): la visita usa el que tenga a mano | 2 · Omnicanalidad y accesibilidad |
| OE3 | **Recurrencia** del colaborador: un Pase con días y franja que se crea una vez y no vuelve a pedir nada | 3 · Automatización y gestión |
| OE4 | **Integración** confiable con HikCentral: alta con teléfono, confirmación del lector y monitoreo | 3 · Automatización y gestión |
| OE4 | **Transparencia** del estado: Kino nunca muestra vigente lo que el lector no confirmó | 3 · Automatización y gestión |
| OE5 | **Penetración** en conjuntos que ya tienen hardware Hikvision, a través de quien lo instaló | 2 · Omnicanalidad y accesibilidad |
| OE5 | **Fidelización** de la administración con evidencia: constancia y reporte semanal | 3 · Automatización y gestión |

---

## 5. Tácticas (T de SOSTAC)

Cada táctica responde qué se hará, cómo, quién y cuándo.

| Estrategia | Qué se hará | Cómo se implementará | Quién | Cuándo |
|---|---|---|---|---|
| Simplificación | «Volver a invitar» en la lista | Las 4 personas recientes, a un toque, abren la hoja ya llena | Equipo (diseño y front) | Prototipo, oct 2026 ✔ |
| Simplificación | Vigencia a tu medida | Unas horas, un día o «Se queda» (3 días a 3 meses); la franja se ve antes de crear | Equipo | Prototipo ✔ |
| Validación | Prueba de usabilidad con 5 residentes | Protocolo de la Biblia §6.1: 6 tareas, éxito, tiempo, SEQ y SUS | Equipo con la administración | 27 oct – 7 nov 2026 |
| Acompañamiento | Día de lanzamiento en portería | Un puesto en la entrada con QR al instructivo; se crea el primer Pase con cada residente que pase | Equipo y administración | Semana 1 del piloto, ene 2027 |
| Acompañamiento | Línea de ayuda por WhatsApp | Número de Kino con respuestas guardadas y un responsable por turno | Equipo | Desde el piloto |
| Diversificación | Pase por imagen y enlace | Plantilla de utilidad de WhatsApp Business con la imagen del Pase y el enlace al Pase vivo | Equipo (backend) | Dic 2026 |
| Recurrencia | Pase de colaborador con días y franja | Persona temporal en HikCentral con horario, o renovación diaria automática si no se admite | Equipo con Manuel | Dic 2026 – ene 2027 |
| Integración | Alta con teléfono en lugar de correo | Migrar las altas de Refugio quitando el correo y reintentar las 711 fallidas | Equipo con Manuel | Nov – dic 2026 |
| Integración | Monitor de sincronización | Panel de administración con usuarios y vehículos sincronizados y alerta si baja de 95 % | Equipo | Ene 2027 |
| Transparencia | Estado honesto | Vigente solo con la respuesta del lector; Sin confirmar con borde punteado | Equipo | Prototipo ✔, producción ene 2027 |
| Penetración | Alianza con integradores | Ficha comercial para instaladores Hikvision del Valle de Aburrá y el Oriente | Equipo | Abr – jun 2027 |
| Fidelización | Reporte semanal a la administración | Correo los lunes con entradas, rechazos con motivo y salud del lector | Equipo | Feb 2027 |

---

## 6. Plan de acción (A de SOSTAC)

| Periodo | Hito | Responsable | Entregable |
|---|---|---|---|
| 19 oct – 9 nov 2026 **[A]** | Prototipo navegable, pruebas con 5 residentes y sustentación | Nico y Alejandro | Deck, Biblia E3, prototipo |
| Nov – dic 2026 **[P]** | Confirmar con Manuel la credencial temporal (pendiente 1); arreglar Refugio | Equipo con Manuel | Refugio ≥ 95 % sincronizado |
| Dic 2026 **[P]** | Backend del Pase y WhatsApp Business | Equipo | Versión beta |
| Ene – mar 2027 **[P]** | Piloto pagado en Villas Campestres y Refugio | Equipo con la administración | Medición de OE2, OE3 y OE4 |
| Abr – jun 2027 **[P]** | Ficha comercial e integradores | Equipo | 10 conjuntos contactados |
| Jul – oct 2027 **[P]** | 2 conjuntos nuevos en piloto; renovación de Monte Sereno | Equipo | Meta general |

---

## 7. Control (C de SOSTAC): KPI con el método GQM

Paso a paso del curso: objetivo → variable → meta. Cada KPI está atado a un objetivo y a una etapa (captación, comportamiento, conversión, satisfacción, confianza, compromiso).

| Objetivo (G) | Pregunta (Q) | KPI (M) | Fórmula | Meta | Etapa | Fuente | Frecuencia |
|---|---|---|---|---|---|---|---|
| OE1 | ¿Crear un Pase es más rápido que llamar? | Tiempo para crear un Pase | Mediana de segundos desde «Crear Pase» hasta «Pase creado» | < 30 s | Comportamiento | Prueba de usabilidad; después, analítica | Por prueba; semanal |
| OE1 | ¿Se entiende sin ayuda? | Éxito de la tarea | Tareas completas sin ayuda ÷ intentos | ≥ 90 % | Satisfacción | Prueba de usabilidad | Por prueba |
| OE1 | ¿Cómo la perciben? | SUS | Escala de usabilidad de 10 ítems | ≥ 80 | Satisfacción | Cuestionario | Por prueba |
| OE2 | ¿Las casas activan su autoridad? | Activación de casas | Casas con ≥ 1 Pase ÷ casas con residente registrado | ≥ 60 % a 8 semanas | Captación → conversión | Base de Kino | Semanal |
| OE2 | ¿Vuelven a usarlo? | Retención de residentes | Residentes que crean Pase en 2 semanas distintas ÷ activados | ≥ 50 % | Compromiso | Base de Kino | Mensual |
| OE3 | ¿El colaborador entra sin llamada? | Ingresos de colaborador con Pase | Ingresos de colaborador por lector ÷ ingresos de colaborador (minuta) | ≥ 80 % | Comportamiento | HikCentral y minuta | Semanal |
| OE4 | ¿El Pase existe en la puerta? | Confirmación del lector | Pases confirmados en < 60 s ÷ Pases creados | ≥ 98 % | Confianza | Registros de Kino y HikCentral | Diaria |
| OE4 | ¿Refugio volvió a operar? | Sincronización | Usuarios sincronizados ÷ usuarios | ≥ 95 % | Confianza | HikCentral | Diaria |
| OE4 | ¿Kino dice la verdad? | Discrepancia app–puerta | Pases vigentes en Kino que el lector rechaza ÷ lecturas | ≤ 0,5 % | Confianza | Lecturas rechazadas «sin Pase» | Semanal |
| OE5 | ¿La administración ve valor? | NPS de la administración | Promotores − detractores | ≥ 30 | Satisfacción | Encuesta trimestral | Trimestral |
| OE5 | ¿Crece la base? | Conjuntos con pago | Conteo | 4 a oct 2027 | Conversión | Contratos | Mensual |
| OE5 | ¿Los rechazos tienen explicación? | Rechazos con motivo | Rechazos con motivo ÷ rechazos | 100 % | Confianza | Kino Portería | Semanal |

Las metas de OE2, OE3 y OE5 son supuestos del equipo y se ajustan con el punto de partida que se mida en la semana 1 del piloto. Donde no existe medición, la tabla lo dice.

---

## 8. Hacia dónde vamos en 1 año (octubre de 2027) [P]

- **Producto:** Kino Residente, Pase vivo, Kino Portería y Kino Administración en producción, conectados a HikCentral.
- **Clientes:** 4 conjuntos con pago, incluidas las dos comunidades de Monte Sereno.
- **Prueba:** un caso documentado con KPI reales (OE2 a OE4), que se usa para vender.
- **Empresa:** sociedad constituida (SAS), con facturación electrónica y bases de datos registradas ante la SIC.
- **Equipo:** Nico y Alejandro, más un integrador aliado.

---

## 9. Horizonte de Kino como empresa (3 a 5 años) [P]

**Visión.** Ser la capa de autorización entre las personas y el hardware de acceso de los conjuntos residenciales en Colombia, sin importar la marca del lector.

### 9.1 Objetivos de empresa
| # | Objetivo | Horizonte |
|---|---|---|
| E1 | 40 conjuntos con pago en Antioquia | 2028 |
| E2 | Conectores para un segundo y un tercer fabricante (ZKTeco, Dahua), además de HikCentral | 2028–2029 |
| E3 | 250 conjuntos en Antioquia y Bogotá | 2030 |
| E4 | Punto de equilibrio operativo con ingresos recurrentes | 2029 |
| E5 | Producto para personal del conjunto y contratistas de la administración (A-08) | 2029 |

> *Supuesto declarado:* las cifras E1 y E3 son ambición del equipo. Se calibran con dos datos que faltan: cuántas copropiedades del Valle de Aburrá y el Oriente tienen hardware Hikvision, y cuál es el precio que acepta una administración.

### 9.2 KPI de empresa
| KPI | Fórmula | Etapa |
|---|---|---|
| Ingreso recurrente mensual (MRR) | Suma de suscripciones activas | Conversión |
| Rotación de conjuntos | Conjuntos que cancelan ÷ conjuntos al inicio del periodo | Compromiso |
| Costo de adquisición por conjunto | Gasto comercial ÷ conjuntos nuevos | Captación |
| Tiempo de implementación | Días desde la firma hasta el primer Pase confirmado | Comportamiento |
| Cobertura de fabricantes | Conectores en producción | Confianza |
| Pases confirmados por el lector | Igual que OE4, a escala | Confianza |

### 9.3 Plan y estrategias unidas a los objetivos de empresa (SOSTAC de empresa)
| | Contenido |
|---|---|
| **S** | Mercado de propiedad horizontal grande y en crecimiento (§1.5). Competencia de software sin hardware (Neivor, ComunidadFeliz) y de hardware con software propio (ZKTeco). El hueco es la autorización encima del hardware que ya está instalado. |
| **O** | E1 a E5 |
| **S** | E1: **Replicación** del caso Monte Sereno con integradores. E2: **Independencia** del fabricante con una capa de conectores. E3: **Expansión** a Bogotá, donde el 69 % de los predios es propiedad horizontal. E4: **Eficiencia** en la implementación (meta: menos de 10 días). E5: **Ampliación** del Pase a todo el que entra por trabajo. |
| **T** | Programa de aliados instaladores con comisión; kit de implementación; conector ZKTeco con un cliente ancla; ficha para consejos de administración; plantilla de reglamento con franjas. |
| **A** | 2027: Monte Sereno y 2 conjuntos más. 2028: 40 conjuntos y segundo conector. 2029: equilibrio. 2030: Bogotá. |
| **C** | KPI de 9.2, revisados cada mes; NPS de la administración cada trimestre. |

### 9.4 Lista de mercado: productos adicionales que pide cada estrategia
| Producto o servicio | Para qué estrategia | Costo o referencia | Estado del dato |
|---|---|---|---|
| WhatsApp Business Platform, a través de un proveedor (BSP) | Diversificación, Acompañamiento | Plantillas de utilidad y autenticación ≈ US$0,0008 por mensaje en Colombia | Fuente de terceros; confirmar en la tarifa oficial de Meta |
| Acceso a HikCentral Professional OpenAPI y programa de socios de Hikvision | Integración | Por cotizar | Pendiente con Manuel |
| Conector ZKTeco o Dahua | Independencia del fabricante | Por cotizar | Horizonte 2028 |
| Lector QR compatible con HikCentral para conjuntos que solo tienen LPR | Diversificación | Por cotizar con el integrador | Sin dato |
| Tableta de portería (Android) con soporte y kiosco | Transparencia | Por cotizar | Sin dato |
| Nube con región en Latinoamérica, monitoreo de errores y respaldo | Integración | Por cotizar | Sin dato |
| Proveedor de facturación electrónica (DIAN) y pasarela de pago B2B | Fidelización | Por cotizar | Obligatorio para facturar en Colombia |
| Registro de bases de datos ante la SIC y política de tratamiento (Ley 1581) | Integración, Transparencia | Asesoría legal por cotizar | Obligatorio |
| Cuenta de Apple Developer y emisor de Google Wallet (Pase en la billetera, I-18) | Diversificación | Por confirmar en sus sitios | Horizonte 2027 |
| Póliza de responsabilidad civil y ciberseguridad | Fidelización | Por cotizar | Horizonte 2028 |
| Kit de implementación: señalética con QR, guía de portería, capacitación | Acompañamiento, Penetración | Producción propia | Sin dato |
| CRM comercial y página de producto | Penetración | Por cotizar | Sin dato |

---

## 10. Fichas de producto

Plantilla del curso: nombre · propósito dentro de la estrategia · elementos clave (interacciones, componentes, tecnologías) · escenario de uso.

### F1 · Kino Residente (app)
- **Propósito:** que el residente otorgue, acote y revoque Pases. Apunta a OE1, OE2 y OE3.
- **Interacciones:** código por WhatsApp con autollenado (I-01), Pase vivo que se consume (I-02), volver a invitar (I-03), hoja con gesto (I-04), vigencia a tu medida (I-05), nacimiento del Pase (I-06), mantener para revocar con deshacer (I-13), extender (I-14), aviso de llegada (I-11).
- **Componentes:** tarjeta del Pase con barra de vida, Portal (arco del logo con QR), hoja inferior, botón de mantener, banner.
- **Tecnologías:** PWA en TypeScript, `@kino/motion`, notificaciones push, API de Kino.
- **Escenario:** Carolina está en la oficina a las 2 p. m. y su hermano llega a las 3. Abre Kino, toca «Andrés» en recientes y luego «Crear Pase». Lo envía por WhatsApp. A las 3:04 le llega «Andrés entró por Portería principal».

### F2 · Pase vivo (web para la visita)
- **Propósito:** que la visita entre sin cuenta. Apunta a OE2 y a la estrategia de Diversificación.
- **Interacciones:** abrir desde el enlace (I-09); cambiar entre QR, placa y código; cuenta regresiva; el Pase cambia solo si lo revocan o lo extienden.
- **Componentes:** Portal en claro, chip de estado, instrucción de una línea.
- **Tecnologías:** página web estática con datos en vivo; imagen del Pase generada en el servidor.
- **Escenario:** Andrés llega en carro, abre el enlace del WhatsApp y el lector lee su placa. Si no la registró, acerca el QR.

### F3 · Kino Portería
- **Propósito:** que portería vea por qué entró o no entró cada persona. Apunta a OE3 y OE4.
- **Interacciones:** lectura con resultado legible desde 3 m (I-10), rechazo con motivo (I-12), llamar al residente sin abrir la entrada, bitácora del día.
- **Componentes:** panel de resultado, talanquera, lista de esperados, bitácora.
- **Tecnologías:** tableta Android en modo kiosco, eventos de HikCentral.
- **Escenario:** a las 6:10 p. m. llega Laura con un Pase que venció a las 6:00. La pantalla lo dice. El portero llama a Carolina, ella lo extiende y el lector deja entrar a Laura.

### F4 · Kino Administración
- **Propósito:** fijar el marco y cuidar la integración. Apunta a OE4 y OE5.
- **Interacciones:** franjas con vista previa (I-15), salud de la integración y reintento (I-16), resumen con rechazos y su motivo.
- **Componentes:** controles de franja, tarjeta de sincronización, cifras del día.
- **Tecnologías:** web, API de Kino, correo semanal.
- **Escenario:** el consejo pide que las visitas de un día no entren después de las 9 p. m. La administración mueve la franja y ve qué Pase quedaría por fuera; ningún Pase activo se corta.

### F5 · Conector Kino–HikCentral (servicio)
- **Propósito:** que el Pase exista en la puerta. Apunta a OE4.
- **Interacciones:** ninguna directa. Su efecto es el estado honesto (I-07).
- **Tecnologías:** HikCentral Professional OpenAPI; persona temporal con «Válido desde / hasta» (por confirmar); cola de reintentos.
- **Escenario:** se crea un Pase, el conector da el alta y el lector responde en 3 segundos. Si falla, el Pase sigue en Sin confirmar y la administración ve la causa.

### F6 · Kit de implementación (servicio)
- **Propósito:** que un conjunto nuevo opere en menos de 10 días. Apunta a OE2 y a E4.
- **Elementos:** carga de casas por cédula, capacitación de portería de 45 minutos, señalética con el QR del instructivo, día de lanzamiento.
- **Escenario:** el lunes se firma; el martes se carga la base; el jueves se capacita a los tres turnos de portería; el sábado es el lanzamiento en la entrada.

---

## 11. Supuestos y lo que falta verificar

1. Que HikCentral admite una persona temporal con vigencia (pendiente 1 del maestro). Si no la admite, el Pase de visita depende de la placa por LPR.
2. Cuántas casas hay en Villas Campestres. El sistema reporta 888 usuarios, no casas.
3. El precio de la suscripción. No hay dato del cliente. Se propone validar con la administración un precio por casa al mes.
4. La discrepancia de 893 contra 1.200 usuarios (maestro §7).
5. El número de copropiedades del Oriente antioqueño con hardware Hikvision.
