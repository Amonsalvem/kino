# Arquetipos e insights — Kino, 21 de septiembre de 2026

Construidos desde cero con la evidencia de esta fase. **No se usan los arquetipos del trabajo 2026-1** (Valeria Gómez y Carlos Ramírez): no tienen respaldo en la investigación propia y ponen al vigilante como usuario primario, que es justo lo que la inspección desmiente. Decisión del equipo, 21 de septiembre.

Tampoco se les inventó nombre, edad ni biografía. Con cinco entrevistas sin citas documentadas, una persona con nombre propio sería una ficción con apariencia de dato. Cada arquetipo se define por su **posición frente al sistema**, que es lo que la evidencia sí permite afirmar.

## Los cuatro arquetipos

| Arquetipo | Qué lo define frente al sistema | Evidencia |
|---|---|---|
| **A1. El residente que recibe** — propietario o arrendatario que vive en el conjunto; usuario primario | Es el único que sabe a quién espera y por cuánto tiempo, y el único que no puede expresarlo. Ya abre la puerta cuando registra una placa, sin saberlo | Sujetos 1 y 2 de la inspección (33 obs.); prueba TST001; entrevistas del 2 sep (citas pendientes) |
| **A2. El colaborador recurrente** — empleada, jardinero, técnico; entra por días | Vínculo intermitente y repetido; el sistema solo sabe representar permanencia. Es el ingreso más frecuente y el que menos existe en el producto | Rol `app.domestic_employee` observado; 0 contratistas registrados; GEIH-DANE y Symplifica 2026 |
| **A3. El visitante ocasional** — va una vez | Entrega datos de por vida para una visita de una tarde. Es el actor con menos interés en el sistema y al que más se le pide | Ficha de la propiedad 346 con 2 «Visitante» permanentes; cola `sso-registration-requests` con 1 Visitor aprobado; SIC 52185 |
| **A4. La administración y la portería** — quien compra y quien opera | Responde ante el consejo por ingresos que no puede rastrear, y paga infraestructura que en Refugio no opera. El portero ve todo y no puede cambiar nada | Sujetos 3, 4 y 5 (26 obs.); 1 super admin para 893 usuarios; 441 trabajos fallidos |

Los veinte insights (cinco por arquetipo), cada uno con hecho observado, insight formulado, fuente y oportunidad, están en el §6 del documento unificado: `enfasis/servicios_y_ experiencias_interactivas/entregas/Kino_Documento_unificado_diagnostico_2026-09-21.docx`.

## Los cuatro insights que más mueven el diseño

1. **A1.** Los residentes ya deciden quién entra pero creen que no, porque el producto les niega en pantalla la autoridad que les dio en la base de datos. → Nombrar y acotar, no traspasar.
2. **A2.** El dato que más cuesta pedirle al colaborador (el correo) es exactamente el que rompe la sincronización con la puerta. → Una decisión resuelve fricción y falla técnica.
3. **A3.** La vía que menos datos personales exige (la placa por LPR) es la única que hoy no crea persona en HikCentral. → El vehículo del visitante como primer canal del pase.
4. **A4.** La administración cree conservar un control que no ejerce. → El argumento de venta no es «suelte el control», es «hoy no lo tiene».

## Entregables del 21 de septiembre

Tres guías del curso diligenciadas sobre las plantillas oficiales en blanco, más un documento unificado. Están en `enfasis/servicios_y_ experiencias_interactivas/entregas/`:

- `Kino_G1_cliente_y_entorno_v2_2026-09-21.docx`
- `Kino_G2_consolidacion_y_pregunta_guia_v2_2026-09-21.docx`
- `Kino_G3_experiencia_deseada_v2_2026-09-21.docx`
- `Kino_Documento_unificado_diagnostico_2026-09-21.docx`

## Regla de redacción acordada el 21 de septiembre

**Se sigue usando la inspección del 14 al 16 de septiembre como fuente. La información de las guías del 16 de septiembre no se usa, y los documentos tampoco mencionan que existieron.** Nada de notas de versión, erratas, comparaciones «antes y después» ni referencias al brief anterior: cada documento se sostiene por sí solo sobre la evidencia. Los cuatro entregables ya están escritos así.

Donde el contraste aportaba algo al razonamiento —por ejemplo distinguir el problema real del que parece a primera vista— se conserva la idea, pero formulada como lectura superficial frente a lo que muestra la evidencia, sin fechar ninguna versión anterior.

## Entorno verificado con fuente el 21 de septiembre

- **PH**: 47,88% de la vivienda urbana del país, ~6,7M unidades; Medellín 61,7%; arriendo 40,8%; servicios de PH +13,42% anual a mayo 2026 contra 5,84% de inflación. Fedelonjas vía [Portafolio, 28 jun 2026](https://www.portafolio.co/mis-finanzas/vivienda/casi-la-mitad-de-viviendas-urbanas-en-colombia-estan-concentradas-en-conjuntos-cerrados-o-edificios-497094).
- **Biometría**: Resolución 52185 del 28 de agosto de 2025; autorización previa, expresa, informada y cualificada; obligación de ofrecer vías no invasivas; hay que advertir que la persona no está obligada a autorizar. [SIC, comunicado oficial](https://sedeelectronica.sic.gov.co/comunicado/la-superintendencia-de-industria-y-comercio-ordena-un-conjunto-residencial-habilitar-mecanismos-de-ingreso-que-no-impliquen-el-tratamiento).
- **Trabajo doméstico**: 51,3% de los contratos por días en 1S-2026 (42,8% en 2025); ~704.000 ocupados a marzo 2026; informalidad >87%. GEIH-DANE y Symplifica vía [Infobae, 9 sep 2026](https://www.infobae.com/colombia/2026/09/09/el-trabajo-domestico-cambia-de-ritmo-en-colombia-crecen-los-contratos-por-dias-y-la-informalidad-supera-el-87/).
- **Neivor**: vende autogestión de visitas por QR, integración con los sistemas de acceso del condominio y sincronización de cartera morosa con el acceso vehicular. Su página pública no especifica si el visitante necesita cuenta. [Página de producto](https://landing.neivor.com/control-de-acceso-visitantes), consultada el 21 sep 2026. Confirma la regla 5: la autonomía del residente no diferencia.

## Discrepancia anotada, sin resolver

El panel de super administrador reporta **893 usuarios** en todo el sistema, mientras los escritorios de comunidad suman **1.200** (312 en Refugio + 888 en Villas). La diferencia no está explicada. Queda anotada en el documento unificado §1 y conviene resolverla antes de sustentar.
