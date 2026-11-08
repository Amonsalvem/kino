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

## D-005 · Qué se cuenta en documentos comerciales sobre colaboradores y precios · PROPUESTA

Se recomienda mantener el canon y tratar la omisión comercial como recorte de un documento de venta hasta que Alejandro decida. Nico pidió mencionar solo la alianza con HikCentral, decir el Pase de Kino y omitir contratistas o empleados, multi-conjunto, modelo y precios. Fuente: conversación del 3 nov 2026 resumida en el inventario de Kino Ops, fuera del repositorio, sin transcripción.

| Opción | Alcance | Costo |
|---|---|---|
| A (recomendada) | Conservar colaboradores y visita con la misma prioridad; limitar la omisión al documento comercial | Exige comprobar que el recorte no se lea como reducción del producto |
| B | Aplicar la omisión al producto | Contradice el canon y obliga a revisar reglas y recorridos; sin autorización |
| C | Mostrar todo el alcance del canon en documentos comerciales | No sigue el recorte comercial pedido por Nico |

La contradicción afecta la prioridad de colaboradores, explícita en `kino/canon/proyecto.md`. La omisión de precios no fija ni elimina un modelo comercial. No se cambia `proyecto.md` ni se aplica ninguna alternativa.

**Trazabilidad y HikCentral.** A conserva autor, motivo, vigencia y límites; el recorte narrativo no cambia quién autoriza ni la sincronización. B requeriría una evaluación de producto que no existe aquí. La mención comercial de la alianza no demuestra integración temporal del Pase; sin fuente de implementación. Fuentes: `kino/canon/proyecto.md` y `kino/producto/flujos/pase-visita.md`.

## D-006 · Cómo se describe el piloto · PROPUESTA

Se recomienda distinguir uso actual de instalación con integración caída, sin presentar ambas comunidades como piloto activo. Nico indicó que la beta corre solo en Monte Sereno Villas Campestres, no en Refugio Campestre. Fuente: Nico, 20 oct 2026, según inventario de Kino Ops, sin transcripción y fuera del repositorio.

| Opción | Relato | Costo |
|---|---|---|
| A (recomendada) | Monte Sereno Villas Campestres como comunidad de uso actual declarado por Nico; Refugio Campestre como instalación con integración caída | Exige conservar la fecha y procedencia distinta de cada dato |
| B | Hablar solo de Monte Sereno Villas Campestres | Omite la instalación de Refugio y la contradicción con el contexto del canon |
| C | Hablar de ambas como piloto activo | Confunde hardware instalado con uso y sincronización comprobados |

El contexto de `kino/canon/proyecto.md` describe un MVP en las dos comunidades. Sus hechos vigentes registran en Refugio Campestre hardware instalado, 0 de 312 usuarios y 1 de 44 vehículos sincronizados; fuente: `kino/canon/proyecto.md`, inspección de sep 2026. Son datos históricos del canon, sin nueva comprobación operativa. La declaración posterior de Nico no basta para borrar ese registro.

**Trazabilidad y HikCentral.** Cambia solo el relato; no cambia la lógica de aprobación. A conserva visible el fallo de sincronización en Refugio; no convierte instalación en confirmación de ingresos ni acredita sincronización del Pase temporal. Se mantiene `proyecto.md` sin cambios.
