# {{nombre}} · Entrega y mantenimiento

Fase 6.

## Qué recibe el cliente
| Pieza | Formato | Dónde |
|---|---|---|
| Manual de marca navegable | Artefacto HTML publicado | enlace |
| Tokens | `build/{{id}}-tokens.css` + `tokens/*.tokens.json` (DTCG 2025.10) | repo |
| Logo | SVG + PNG | `03-visual/logo/` |
| Guía de contenido | documento | `02-verbal/` |
| Skill de marca | carpeta `skill/{{id}}-marca/` | se instala en Claude del cliente |
| Suite de evaluación | `evals/` | para su equipo o para nosotros como servicio |

## Versionado
- Los tokens siguen semver: **mayor** si se renombra o elimina un token; **menor** si se agrega; **parche** si cambia un valor sin cambiar el significado.
- Cada versión se anota abajo con fecha y motivo.

| Versión | Fecha | Qué cambió | Por qué |
|---|---|---|---|
| 1.0.0 | | Primera entrega | |

## Mantenimiento
- Cualquier cambio de color o tipo entra por `marca.config.json` y se reconstruye con `npm run ciclo -- {{id}}`. Nunca se edita un hex en el CSS.
- Si el cliente produce copy con IA: correr evals cada vez que cambie `voz.json` o el modelo.
