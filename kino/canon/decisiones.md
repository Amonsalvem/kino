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

## D-002 · Qué se hereda de la marca de pre-kino · PROPUESTA (4 nov 2026)

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

## D-011 · El Pase se llama KEY · PROPUESTA (9 nov 2026)

Alejandro pidió cambiar «Pase» por «KEY» en la entrega de EAFIT (comentario sobre el PDF, 9 nov 2026) y luego eligió que el cambio aplique a todo Kino (tarjeta en el chat del proyecto, 9 nov 2026).

| Opción | Alcance | Costo |
|---|---|---|
| A (recomendada) | «KEY» reemplaza a «Pase» en todo Kino: canon, producto, app y textos nuevos | Hay que actualizar el vocabulario de `proyecto.md`, `AGENTS.md` y los flujos de producto. Los archivos de pre-kino y los registros históricos conservan «Pase» |
| B | «KEY» solo en la entrega de EAFIT | El documento académico y el producto usan nombres distintos para lo mismo |

**Uso.** «KEY» en mayúsculas; plural «KEYs»; artículo masculino («el KEY», «un KEY»). La regla de fondo no cambia: el KEY (de la visita o el colaborador) no se mezcla con la cuenta (del residente). Nunca «permiso».

**Trazabilidad y HikCentral.** Cambia solo el nombre. No cambia autor, motivo, vigencia, modo ni autoridad. No cambia la sincronización.
