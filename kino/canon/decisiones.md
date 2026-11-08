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

## D-004 · Identidad visual trabajada en Grok como candidata · PROPUESTA

Se propone conservar esta identidad como referencia hasta que Alejandro compare la marca nueva en Figma. No se da por vigente. Fuentes: conversación oct-nov 2026 resumida en el inventario externo de Kino Ops; D-001, D-002 y `kino/marca/README.md`.

| Opción | Alcance | Costo |
|---|---|---|
| A | Adoptar la paleta, Poppins y el candado de arco trabajados en Grok | Requiere validar las piezas y su respuesta al diagnóstico en Figma |
| B (recomendada) | Partir de cero en Figma; mantener el trabajo de Grok como referencia | Requiere nueva construcción y comparación antes de aplicar una identidad |
| C | Heredar solo lo verbal, opción A de D-002, sin esta estética | Requiere aprobar D-002 y diseñar lo visual |

La recomendación espera la comparación y aprobación de Alejandro; no autoriza empezar cambios visuales. Lista de piezas, herencia no demostrada y referencias: `kino/marca/revision/2026-11-identidad-trabajada-en-grok.md`. Clave de Figma de marca nueva: por definir, según `kino/marca/README.md`.

**Trazabilidad y HikCentral.** Esta propuesta trata identidad visual; no cambia autor, motivo, vigencia ni autoridad del Pase. No incorpora una integración ni prueba la sincronización del Pase temporal; sin fuente de implementación nueva. D-002 permanece en PROPUESTA.

**Pregunta aparte.** El canon mantiene identidad propia sin marca blanca en `kino/canon/proyecto.md`. El inventario externo registra un pedido de Nico sobre versiones marca blanca del 21 oct 2026. Se consulta a Alejandro; no se modifica esa decisión de producto.
