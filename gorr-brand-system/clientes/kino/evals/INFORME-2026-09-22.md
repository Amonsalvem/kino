# Evals de voz · Kino · 22 sep 2026

**Resultado: 12 de 15 (80 %) en la tercera ronda. Llega justo al umbral.** Caso por caso: los casos 1 a 3 pasan 3 de 3; el 4 (explicar a la administración el cambio de rol) pasa 1 de 3 y el 5 (estado vacío) pasa 2 de 3.

## Cómo se corrió
promptfoo necesita red y no había acceso a npm, así que la suite se corrió con subagentes, respetando la separación entre quien escribe y quien juzga:

| Rol | Qué ve | Qué no ve |
|---|---|---|
| Redactor (un agente nuevo por ronda) | `skill/kino-marca/SKILL.md` y los 5 casos de `voz.json` | rúbrica, corridas anteriores |
| Juez (un agente nuevo por ronda) | `evals/rubrica.md`, las 15 salidas, los casos | quién escribió, corridas anteriores |
| Compuerta determinista | `voz.mjs` sobre las 15 salidas | — |

Una salida pasa si la aprueban **el juez y la compuerta**. 5 casos × 3 versiones = 15 salidas por ronda. Todo está en `corrida-2026-09-22*/` (`salidas.json`, `juicio.json`, `compuerta.json`, `resultado.json`).

## Las tres rondas

| Ronda | Pasan | Qué falló | Qué se cambió después |
|---|---|---|---|
| 1 | 11/15 (73 %) | El texto inventa funciones: «Te avisamos cuando el lector la confirme», «Muéstralo o escríbelo en el lector», «Todo queda registrado». La compuerta dio un falso positivo: «deja de aprobar ingresos» (negación legítima). | Se agregó a «no somos»: no describir funciones que el producto no tenga confirmadas. Se prohibió «todo queda registrado» y «trazabilidad completa». Se corrigió el patrón para aceptar la negación y las placas (ABC-123). |
| 2 | 10/15 (67 %) | Bajó. La sugerencia de reemplazo que agregamos («decir qué queda registrado: quién, cuándo, vigencia») empujó al redactor a afirmar un registro que ningún caso confirma. | Se agregó a `voz.json` la sección `hechos`: lo que el producto hace (confirmado por las decisiones tomadas) y lo que no está confirmado. La skill y la rúbrica la leen. |
| 3 | **12/15 (80 %)** | 4v1 da por hecho que los cupos son «por casa». 4v3 no explica por qué cambia el rol. 5v2 tiene un sujeto ambiguo («Entra con QR…» se lee como una orden al residente). | — |

En las 45 salidas, las cuatro dimensiones de tono quedaron dentro de ±1 del perfil aprobado. El tono se sostiene; lo que falla es afirmar de más.

## Lo que la prueba encontró sobre el producto
En la ronda 3 el caso 4 falla por una pregunta de negocio que no está decidida: **¿los cupos que fija la administración son por casa, por residente o por conjunto?** Las decisiones tomadas dicen «cupos, duración y franjas», sin la unidad. Mientras no se decida, cualquier texto dirigido a la administración va a tener que rodearla. Se decide en producto, no en la voz.

## Límites de esta medición
- **n = 15 por ronda.** Una salida mueve el resultado 6,7 puntos, así que 80 % y 73 % no son distinguibles estadísticamente. El número sirve para detectar tendencias y patrones de falla, no como garantía.
- **El juez es un modelo.** Salió estricto (cuenta como falla cualquier afirmación fuera de los hechos), que es lo que se busca, pero algunos juicios son discutibles. Ejemplo: 5v2 falla por ambigüedad del sujeto.
- **Redactor y juez son la misma familia de modelo.** Con promptfoo y red se puede usar otro proveedor como juez (`evals/promptfooconfig.yaml`).

## Siguiente
1. Decidir la unidad de los cupos y agregarla a `voz.json → hechos.confirmado`.
2. Volver a correr cuando haya red: `cd clientes/kino/evals && npx promptfoo@latest eval`. Esa corrida usa la misma rúbrica y la misma compuerta.
