# Decisiones · Kino

Registro único de decisiones del Kino nuevo: producto, marca, arquitectura y operación. Manda sobre cualquier otro archivo del repositorio.

**Cómo se escribe una entrada**

- Identificador `D-###`, consecutivo, nunca se reutiliza.
- Estado: PROPUESTA, APROBADA, DESCARTADA o REEMPLAZADA (ver `CONVENCIONES.md`).
- Una PROPUESTA trae al menos dos alternativas y una recomendada. Si toca aprobación o identidad, dice su efecto en la trazabilidad y en la sincronización con HikCentral.
- Una APROBADA cita quién aprobó, cuándo y con qué palabras.
- Lo que se hereda de pre-kino se aprueba aquí, con la ruta del archivo de origen.
- Las decisiones de producto que ya venían tomadas están en `proyecto.md`, bloque `<decisiones_tomadas>`, y siguen vigentes.

---

## D-001 · La etapa anterior pasa a ser pre-kino · APROBADA (Alejandro, 4 nov 2026)

**Qué se decidió.** Todo el trabajo hasta el 4 nov 2026 (identidad de marca anterior, sistema de marca 1.2.1, decks, láminas de paradas, motion, documentos de diagnóstico e inspección) se archiva en `pre-kino/` como base informativa. Kino arranca una identidad de marca nueva, más concisa.

**Palabras de origen.** «Toda esta etapa de kino, llamémosla pre-kino, puesto que era una identidad de marca diferente y sirvió como base informativa para el nuevo kino: nueva identidad de marca y más conciso y contundente con su información.»

**Efecto.**
- La marca de pre-kino (logo, paleta, tipografía, voz, motion, sitio) no se aplica a nada nuevo salvo herencia aprobada aquí.
- La evidencia de pre-kino (`pre-kino/inspeccion/`, `pre-kino/docs/proyecto/`) sigue siendo la base del diagnóstico y conserva su jerarquía.
- Las decisiones de producto de `proyecto.md` no cambian.

---

## D-002 · Qué se hereda de la marca de pre-kino · APROBADA (Alejandro, 8 nov 2026) · opción A

**Aprobación.** Alejandro en el chat del proyecto Kino (D-008), 8 nov 2026: «Opción A». Decidió antes de cargar la marca nueva en Figma.

La identidad nueva puede partir de cero o heredar piezas que ya probaron su valor. Esto no decide la estética, solo el punto de partida.

| Opción | Qué se hereda | Costo |
|---|---|---|
| A (recomendada) | Lo verbal que salió de la evidencia: vocabulario del Pase, estados del Pase y del evento Rechazado, tratamiento (usted con la administración, tú con residente y visita), reglas de horas. Lo visual empieza de cero | Se conserva lo que el producto ya usa y no se arrastra la estética anterior |
| B | Nada. Todo empieza de cero, incluido lo verbal | Hay que volver a validar estados y vocabulario que ya están en el producto y en el diagnóstico |
| C | Todo lo aprobado en pre-kino, ajustado | No responde al pedido de una identidad distinta |

**Fuentes.** `pre-kino/decisiones.md` (V1 a V7, X1 a X11), `pre-kino/TRASPASO-SISTEMA-DE-MARCA.md` §7.

**Cuándo se decide.** Cuando la identidad nueva esté cargada en Figma (Alejandro, 4 nov 2026). Entonces un agente compara la marca nueva con `pre-kino/` y lista qué se heredó, pieza por pieza y con su ruta de origen. Alejandro aprueba esa lista y la entrada pasa a APROBADA.

**Lista de herencia.** Herencia nueva demostrada: nada. Paleta: no demostrada; `pre-kino/decisiones.md`, X2 a X4, documenta otra. Poppins: nada; H5 y X5 documentan Archivo y JetBrains Mono. Arco y gota: similitud con F1, no transferencia probada; F1 conserva el cuadrado. Nombre KINO: coincidencia con F1 y P08, sin procedencia probada. Pase y visita: coincidencia con F3, V2 y V4; aquí rige `kino/canon/proyecto.md`. Estados, tratamiento y horas: adopción completa no demostrada frente a V1, V3 y V5. Señalética, tarjetas, motion, video y decks: no demostrado frente a `pre-kino/TRASPASO-SISTEMA-DE-MARCA.md`, apartados de enlaces y construcción. Comparación detallada: `kino/marca/revision/2026-11-identidad-trabajada-en-grok.md`.

---

## D-003 · Gobierno del repositorio · APROBADA (Alejandro, 4 nov 2026)

**Qué se decidió.**
- Alejandro aprueba todo, comentando o revisando el PR en GitHub. Nico propone.
- La IA puede hacer sin aprobación previa los cambios menores: orden, correcciones de texto, enlaces y código que no cambia comportamiento.
- Agentes del proyecto: Claude (Code, claude.ai, Cowork) y Grok. Viven en el repositorio (`AGENTS.md`, `.claude/skills/`), no en la cuenta de cada persona. Las skills de pre-kino y el plugin arcana se retiran.
- Las tareas van en GitHub Issues. Se retiran el tablero, la bitácora y los traspasos.
- La marca se trabaja en Figma, que manda sobre el repositorio.
- Las entregas académicas van en `eafit/` y se congelan al terminar la fase EAFIT.

**Palabras de origen.** «Yo apruebo todo, nico propone»; «Comentando el PR en Github»; «No hay nada imprescindible en esto».

**Pendiente.** Dónde vive el código del MVP en producción (lo desarrolló Manuel) y de quién es.

---

## D-004 · Identidad visual trabajada en Grok como candidata · APROBADA (Alejandro, 8 nov 2026) · opción B

**Aprobación.** [Comentario de Alejandro en el PR #20](https://github.com/Amonsalvem/kino/pull/20#issuecomment-6727546024).

Se propone conservar esta identidad como referencia hasta que Alejandro compare la marca nueva en Figma. No se da por vigente. Fuentes: conversación oct-nov 2026 resumida en el inventario externo de Kino Ops; D-001, D-002 y `kino/marca/README.md`.

| Opción | Alcance | Costo |
|---|---|---|
| A | Adoptar la paleta, Poppins y el candado de arco trabajados en Grok | Requiere validar las piezas y su respuesta al diagnóstico en Figma |
| B (recomendada) | Partir de cero en Figma; mantener el trabajo de Grok como referencia | Requiere nueva construcción y comparación antes de aplicar una identidad |
| C | Heredar solo lo verbal, opción A de D-002, sin esta estética | Requiere aprobar D-002 y diseñar lo visual |

La recomendación espera la comparación y aprobación de Alejandro; no autoriza empezar cambios visuales. Lista de piezas, herencia no demostrada y referencias: `kino/marca/revision/2026-11-identidad-trabajada-en-grok.md`. Clave de Figma de marca nueva: por definir, según `kino/marca/README.md`.

**Trazabilidad y HikCentral.** Esta propuesta trata identidad visual; no cambia autor, motivo, vigencia ni autoridad del Pase. No incorpora una integración ni prueba la sincronización del Pase temporal; sin fuente de implementación nueva. D-002 permanece en PROPUESTA.

**Pregunta aparte.** El canon mantiene identidad propia sin marca blanca en `kino/canon/proyecto.md`. El inventario externo registra un pedido de Nico sobre versiones marca blanca del 21 oct 2026. Se consulta a Alejandro; no se modifica esa decisión de producto.

---

## D-005 · Qué se cuenta en documentos comerciales sobre colaboradores y precios · APROBADA (Alejandro, 8 nov 2026) · opción A

**Aprobación.** [Comentario de Alejandro en el PR #19](https://github.com/Amonsalvem/kino/pull/19#discussion_r4507878973).

Se recomienda mantener el canon y tratar la omisión comercial como recorte de un documento de venta hasta que Alejandro decida. Nico pidió mencionar solo la alianza con HikCentral, decir el Pase de Kino y omitir contratistas o empleados, multi-conjunto, modelo y precios. Fuente: conversación del 3 nov 2026 resumida en el inventario de Kino Ops, fuera del repositorio, sin transcripción.

| Opción | Alcance | Costo |
|---|---|---|
| A (recomendada) | Conservar colaboradores y visita con la misma prioridad; limitar la omisión al documento comercial | Exige comprobar que el recorte no se lea como reducción del producto |
| B | Aplicar la omisión al producto | Contradice el canon y obliga a revisar reglas y recorridos; sin autorización |
| C | Mostrar todo el alcance del canon en documentos comerciales | No sigue el recorte comercial pedido por Nico |

La contradicción afecta la prioridad de colaboradores, explícita en `kino/canon/proyecto.md`. La omisión de precios no fija ni elimina un modelo comercial. No se cambia `proyecto.md` ni se aplica ninguna alternativa.

**Trazabilidad y HikCentral.** A conserva autor, motivo, vigencia y límites; el recorte narrativo no cambia quién autoriza ni la sincronización. B requeriría una evaluación de producto que no existe aquí. La mención comercial de la alianza no demuestra integración temporal del Pase; sin fuente de implementación. Fuentes: `kino/canon/proyecto.md` y `kino/producto/flujos/pase-visita.md`.

---

## D-006 · Cómo se describe el piloto · APROBADA (Alejandro, 8 nov 2026) · opción A

**Aprobación.** [Comentario de Alejandro en el PR #19](https://github.com/Amonsalvem/kino/pull/19#discussion_r4507881834).

Se recomienda distinguir uso actual de instalación con integración caída, sin presentar ambas comunidades como piloto activo. Nico indicó que la beta corre solo en Monte Sereno Villas Campestres, no en Refugio Campestre. Fuente: Nico, 20 oct 2026, según inventario de Kino Ops, sin transcripción y fuera del repositorio.

| Opción | Relato | Costo |
|---|---|---|
| A (recomendada) | Monte Sereno Villas Campestres como comunidad de uso actual declarado por Nico; Refugio Campestre como instalación con integración caída | Exige conservar la fecha y procedencia distinta de cada dato |
| B | Hablar solo de Monte Sereno Villas Campestres | Omite la instalación de Refugio y la contradicción con el contexto del canon |
| C | Hablar de ambas como piloto activo | Confunde hardware instalado con uso y sincronización comprobados |

El contexto de `kino/canon/proyecto.md` describe un MVP en las dos comunidades. Sus hechos vigentes registran en Refugio Campestre hardware instalado, 0 de 312 usuarios y 1 de 44 vehículos sincronizados; fuente: `kino/canon/proyecto.md`, inspección de sep 2026. Son datos históricos del canon, sin nueva comprobación operativa. La declaración posterior de Nico no basta para borrar ese registro.

**Trazabilidad y HikCentral.** Cambia solo el relato; no cambia la lógica de aprobación. A conserva visible el fallo de sincronización en Refugio; no convierte instalación en confirmación de ingresos ni acredita sincronización del Pase temporal. Se mantiene `proyecto.md` sin cambios.

---

## D-007 · Roles del equipo · APROBADA (Alejandro, 8 nov 2026) · opción A

**Aprobación.** [Comentario de Alejandro en el PR #22](https://github.com/Amonsalvem/kino/pull/22#issuecomment-6727546229).

Se recomienda registrar los roles como propuesta operativa, sin cambiar quién aprueba. Fuente: Nico, 4 nov 2026, según inventario de Kino Ops, fuera del repositorio y sin transcripción.

| Persona | Rol propuesto |
|---|---|
| Nico Ramírez | Responsable principal de marca y estrategia |
| Alejandro Monsalve | Responsable principal de parte técnica y lógica |
| Juan Esteban | Comercial |
| Manuel | Tech |
| Daniel | IoT |
| Henry | Marca |

| Opción | Alcance | Costo |
|---|---|---|
| A (recomendada) | Registrar estos roles como propuesta operativa | Hay que confirmarlos con Alejandro; no habilitan aprobaciones |
| B | Esperar la confirmación antes de registrarlos como equipo operativo | Las piezas siguen sin una atribución operativa confirmada |

D-003 sigue vigente: Alejandro aprueba y Nico propone. D-003 registra que Manuel desarrolló el código del MVP en producción y deja pendiente dónde vive y de quién es. Los roles no resuelven ese pendiente ni sustituyen el gobierno del repositorio. Fuente: `kino/canon/decisiones.md`, D-003. No se crea perfil de Nico.

**Trazabilidad y HikCentral.** La atribución de trabajo no cambia quién autoriza ingresos, el registro del Pase ni la sincronización con HikCentral. No se propone una función nueva.

---

## D-008 · Alejandro revisa e integra desde el chat del proyecto · APROBADA (Alejandro, 8 nov 2026)

**Qué se decidió.**
- Alejandro revisa los PR y toma las decisiones en el chat del proyecto Kino de Claude, sin entrar a GitHub.
- Claude le presenta la cola: cada PR resumido, la decisión que pide con sus opciones y una recomendada.
- Cuando Alejandro decide, Claude comenta en el PR con su cuenta «Apruebo D-00X, opción Y», y la Action «Aprobar decisiones» pasa la entrada a APROBADA.
- Claude integra un PR a `main` solo cuando Alejandro escribe en el chat «integra #N», un PR a la vez. Sin esa orden, nunca. Ajusta D-003, que sigue vigente en lo demás.

**Alternativa descartada.** Que Claude comente y Alejandro pulse *Merge* en GitHub: deja un paso fuera del chat.

**Palabras de origen.** «Prefiero que todo este flujo se realizado en mi claude, que sea meterme al project de kino y estén abiertos los PRs que debo revisar, las decisiones que tomar y realizar todo por medio de este chat». En la tarjeta de decisión del hilo «Revisar y aprobar PR desde el chat» eligió «Sí, solo con mi orden por PR».

**Trazabilidad.** Cada integración queda en GitHub con la cuenta de Alejandro, y el hilo del chat guarda la orden. No toca la lógica de ingresos ni la sincronización con HikCentral.

---

## D-009 · Marca blanca fuera del roadmap · APROBADA (Alejandro, 8 nov 2026) · opción A

**Aprobación.** [Comentario de Alejandro en el PR #28](https://github.com/Amonsalvem/kino/pull/28#issuecomment-6728910017).

El documento de roadmap de Nico con Grok (8 nov 2026) traía la fase 6 «KINO marca blanca» y el hito H4, «app de marca blanca de Monte Sereno», para jun 2027. El canon sostiene marca propia: `kino/canon/proyecto.md`, `<decisiones_tomadas>` y regla 6. D-004 dejó la pregunta abierta.

| Opción | Alcance | Costo |
|---|---|---|
| A (recomendada) | Marca propia, sin marca blanca. Salen la fase 6 y el H4. El conjunto aparece solo como dato en texto o chip | Se pierde una línea comercial que ofrecían los decks, el PDF y soykino.com; hay que retirarla de esos textos |
| B | Marca blanca como línea comercial aparte | Exige cambiar `proyecto.md` y mantener dos marcas |
| C | Decidir después del informe del piloto (H3) | El roadmap no la promete en la entrega; la pregunta sigue abierta |

**Respuesta de Alejandro.** En la tarjeta de decisión del hilo «Co-crear roadmap, estrategia y presupuesto de Kino» eligió «Marca propia, sin marca blanca» (8 nov 2026). Pasa a APROBADA con su comentario en el PR, según D-008.

**Trazabilidad y HikCentral.** No cambia autor, motivo, vigencia ni autoridad del Pase. No cambia la sincronización.

---

## D-010 · Modelo de ingresos · APROBADA (Alejandro, 8 nov 2026) · opción B

**Aprobación.** [Comentario de Alejandro en el PR #28](https://github.com/Amonsalvem/kino/pull/28#issuecomment-6729811673).

Alejandro pidió el modelo más rentable sin limitarse al cobro por unidad (chat del proyecto, 9 nov 2026). La comparación completa está en `eafit/2026-11-roadmap-estrategia/roadmap-estrategia-presupuesto.md`, apartado 2.7. Las cifras son ejemplos para comparar; el precio final se valida con administradores en la fase 4.

| Opción | Alcance | Costo |
|---|---|---|
| A | Cobro por unidad construida | Un conjunto pequeño casi no paga; deja valor sin cobrar |
| B (recomendada) | Piso por conjunto + cobro por unidad + implementación única; comisión de pagos desde la etapa 03 | Exige alianza con la pasarela para la comisión de pagos |
| C | Precio por valor, contra el costo de un puesto de vigilancia | Exige probar el ahorro en portería antes de venderlo |

**Trazabilidad y HikCentral.** No cambia autor, motivo, vigencia ni autoridad del Pase. No cambia la sincronización. La comisión de pagos toca datos financieros de residentes: exige la política de datos del Bloque 3 antes de operar.

---

## D-011 · El Pase se llama KEY · APROBADA (Alejandro, 9 nov 2026) · opción A

**Aprobación.** [Comentario de Alejandro en el PR #28](https://github.com/Amonsalvem/kino/pull/28#issuecomment-6739927904).

Alejandro pidió cambiar «Pase» por «KEY» en la entrega de EAFIT (comentario sobre el PDF, 9 nov 2026) y luego eligió que el cambio aplique a todo Kino (tarjeta en el chat del proyecto, 9 nov 2026).

| Opción | Alcance | Costo |
|---|---|---|
| A (recomendada) | «KEY» reemplaza a «Pase» en todo Kino: canon, producto, app y textos nuevos | Hay que actualizar el vocabulario de `proyecto.md`, `AGENTS.md` y los flujos de producto. Los archivos de pre-kino y los registros históricos conservan «Pase» |
| B | «KEY» solo en la entrega de EAFIT | El documento académico y el producto usan nombres distintos para lo mismo |

**Uso.** «KEY» en mayúsculas; plural «KEYs»; artículo masculino («el KEY», «un KEY»). La regla de fondo no cambia: el KEY (de la visita o el colaborador) no se mezcla con la cuenta (del residente). Nunca «permiso».

**Trazabilidad y HikCentral.** Cambia solo el nombre. No cambia autor, motivo, vigencia, modo ni autoridad. No cambia la sincronización.

---

## D-012 · Comisión de pagos desde el inicio · APROBADA (Alejandro, 9 nov 2026) · opción A

**Aprobación.** [Comentario de Alejandro en el PR #28](https://github.com/Amonsalvem/kino/pull/28#issuecomment-6740911654).

Cambia el momento de la comisión de pagos de D-010. Alejandro: «El D también se va implementar desde el inicio» (chat del proyecto, 9 nov 2026). También pidió que la app completa, con el módulo de pagos, quede lista en diciembre de 2026.

| Opción | Alcance | Costo |
|---|---|---|
| A (recomendada) | La comisión de pagos empieza con Villas Campestres y Refugio Campestre, en la app de diciembre de 2026 | El módulo de pagos y la alianza con la pasarela tienen que estar listos en diciembre, junto con el ingreso por WhatsApp y el KEY temporal |
| B | La comisión de pagos empieza en la etapa 03, como dice D-010 | Menos trabajo en diciembre; el ingreso por pagos llega más tarde |

**Regla.** El dinero de la cuota va de la pasarela a la cuenta del conjunto. KINO no recibe ni guarda el dinero del conjunto; recibe solo su margen.

**Monto.** $2.000 por cada pago de la cuota en la app. Lo aprobó Alejandro en el chat del proyecto el 9 nov 2026 («se aprueba la comisión de $2.000 por pago»). Quién asume la tarifa de la pasarela sigue por decidir.

**Trazabilidad y HikCentral.** No cambia autor, motivo, vigencia ni autoridad del KEY. No toca la sincronización. Toca datos financieros de los residentes: exige la política de datos y el contrato con la pasarela antes de cobrar.

## D-013 · Curador semanal de agentes y skills · APROBADA (Alejandro, 9 nov 2026) · opción A

**Aprobación.** [Comentario de Alejandro en el PR #30](https://github.com/Amonsalvem/kino/pull/30#discussion_r4513605107).

**Qué se propone.** Un agente que vive en GitHub y cada lunes revisa los agentes, las skills, los hooks y el estado del arte en IA. Crea, actualiza o retira skills y agentes según lo que Kino necesite, y abre un PR en borrador con un informe. Si el concepto de agente o skill cambia, propone la migración por etapas. Su única función es esa. Guía: `herramientas/curador/README.md`; instrucciones: `herramientas/curador/prompt.md`.

| Opción | Alcance | Costo |
|---|---|---|
| A (recomendada) | Action semanal con Claude Code. Cambia archivos solo en sus rutas (skills, agentes, hooks, `AGENTS.md`, `CLAUDE.md`, sus propios archivos) y agrega PROPUESTAS. Un guardián revierte lo demás. Abre un PR en borrador | Un PR por semana para revisar. Gasta del límite de Claude Pro |
| B | La misma Action, pero solo escribe un informe en un issue. Nadie cambia archivos hasta que una persona lo pida | Cada mejora necesita una sesión aparte. Las skills se desactualizan más rápido |
| C | Mensual en vez de semanal | Menos revisión. Las novedades llegan hasta 4 semanas tarde |

**Límites en todas las opciones.** El curador nunca integra, nunca aprueba decisiones y no toca `pre-kino/`, `.github/`, `kino/canon/proyecto.md`, código, marca ni producto. Integrar sigue la regla de D-008.

**Palabras de origen.** «Necesito que crees un agente experto/inspector/ y curador de agentes y skills. Que semanalmente a medida de lo que requiera Kino, haga una investigación del estado del arte en agentes y skills, integre lo que le convenga más a Kino.» (Alejandro, chat del proyecto, 9 nov 2026).

**Trazabilidad y HikCentral.** El curador trabaja sobre la forma de trabajar con IA, no sobre el producto. No toca la lógica de ingresos, el Pase ni la sincronización con HikCentral. Cada cambio queda en un PR con su informe y su corrida de Actions.

## D-014 · Precio: pago fijo por conjunto + cobro por casa · APROBADA (Alejandro, 9 nov 2026) · opción E

**Número.** Se propuso como D-013 y se renumeró a D-014 porque D-013 ya existía en `main` (curador semanal). El comentario de aprobación dice «D-013».

**Historia.** Alejandro aprobó primero la opción A en el [PR #28](https://github.com/Amonsalvem/kino/pull/28#issuecomment-6743415369). El 9 nov 2026, en el chat del proyecto, la cambió: «Prefiero el modelo de pago fijo, más cobro por casa, más la comisión de pago» y «Pago mínimo $1.200.000 + $16.000» (opción D). Después de ver que D dejaba a KINO más caro que Unita, eligió la opción E en la tarjeta del chat.

Precisa la parte de cobro mensual de D-010 (piso por conjunto + cobro por casa). Siguen igual la implementación única y la comisión de pagos de $2.000 (D-012).

| Opción | Precio al mes | Villas (100 casas) | Refugio (400 casas) | Costo |
|---|---|---|---|---|
| A | $16.000 por casa construida, mínimo $1.200.000 por conjunto | $1.600.000 | $6.400.000 | El «mínimo» se puede leer como una barrera de entrada |
| B | Pago fijo $1.000.000 + $8.000 por casa | $1.800.000 | $4.200.000 | Villas y Refugio apenas cubren el sostenimiento |
| C | Igual a Unita: $1.550.000 + $10.900 por casa | $2.640.000 | $5.910.000 | Se lee como copia del competidor |
| D | Pago fijo $1.200.000 + $16.000 por casa | $2.800.000 | $7.600.000 | Entre 6 % y 29 % más caro que Unita, con un diferencial todavía sin probar |
| **E (elegida)** | **Pago fijo $1.200.000 + $10.000 por casa** | **$2.200.000** | **$5.200.000** | **Menos ingreso que D: $225 M frente a $300 M en el escenario base a dic 2027** |

**Por qué.** KINO queda entre 12 % y 18 % más barato que Unita en todos los tamaños mientras la integración con el hardware no esté probada. Villas y Refugio juntos dejan $7,9 millones al mes y cubren el sostenimiento ($6,4 millones); con Monte Sereno Sagrada (70 casas, desde enero de 2027), los tres dejan $9,9 millones. Con una cuota de $600.000, KINO pesa entre el 2,2 % (Refugio) y el 3,7 % (Villas) de lo que paga cada casa. El precio de los conjuntos nuevos se revisa con el informe del piloto (H3).

**Trazabilidad y HikCentral.** No cambia el KEY, la autoridad del residente ni la sincronización.

---

## D-015 · Dónde vive Kino en GitHub y cómo entra el equipo · PROPUESTA

**Palabras de origen.** «Quiero que la plataforma donde conviva absolutamente todo lo de Kino, sea github» y «Quiero que todos convivamos en el Github, y allí, se reúna la información de todos» (Alejandro, chat del proyecto, 11 nov 2026).

**Problema.** El repositorio es de la cuenta personal de Alejandro y es público. Una cuenta personal da escritura a todo colaborador, sin roles. El código del MVP y los agentes de Manuel están fuera de GitHub (D-003, «Pendiente»). Ese código no puede ir a un repositorio público.

| Opción | Alcance | Costo |
|---|---|---|
| A (recomendada) | Organización de GitHub con dueño Alejandro. `kino` pasa a la organización y sigue público. El código y los agentes de Manuel van a `kino-app`, privado. Cuatro equipos con el acceso mínimo de cada rol (D-007). Detalle en [`ACCESOS.md`](../../ACCESOS.md) | Proteger `main` en `kino-app` pide el plan *Team*, con cobro por persona al mes. Hay que revisar Secrets y Actions después de transferir |
| B | Todo sigue en la cuenta de Alejandro. Cada persona entra como colaborador. El código va a un repositorio privado de la misma cuenta | Sin costo. Todo colaborador tiene escritura; Juan Esteban no puede entrar solo a leer. Más difícil de pasar a otra persona |
| C | Organización como en A, pero `kino` también pasa a privado | Grok deja de leer las reglas por enlace público (`herramientas/prompt-grok.md`). Más ajustes al flujo de Nico |

**Resuelve.** El pendiente de D-003: el código del MVP vive en `kino-app` y la organización es de Kino, con Alejandro como dueño.

**Trazabilidad y HikCentral.** No cambia el KEY, la autoridad del residente ni la lógica de ingresos. Las llaves de HikCentral pasan a los Secrets de `kino-app`: cada cambio de llave y cada despliegue quedan registrados en GitHub, con autor.
