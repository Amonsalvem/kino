# Herramientas

Scripts compartidos que no dependen de ninguna marca. Si una herramienta solo sirve para una carpeta, vive en esa carpeta.

| Script | Qué hace | Uso |
|---|---|---|
| `preparar-entorno.sh` | Comprueba node, python, git y Chromium. Lo corre el hook de inicio de Claude Code | `bash herramientas/preparar-entorno.sh` |
| `revisar-pr.sh` | Resume un PR: cuenta lo que solo se movió (no hace falta leerlo) y lista lo que cambió de verdad, con líneas agregadas y quitadas | `bash herramientas/revisar-pr.sh [base] [rama]` |
| `capturar.mjs` | Capturas de un HTML a 360, 768 y 1440 px, en oscuro y claro, con chequeo de desborde horizontal y errores de consola | `node herramientas/capturar.mjs <archivo.html> [carpeta-salida]` |

**Requisitos.** Node 20 o más. `capturar.mjs` usa Playwright (local o global) y el Chromium de `/opt/pw-browsers` si existe. Las capturas salen en `capturas/`, que no se versiona.

**Herramientas de pre-kino.** La cadena de tokens, contraste y voz (`pre-kino/gorr-brand-system/`) y la auditoría responsive del sitio anterior (`pre-kino/scripts/auditar-responsive.mjs`) siguen allí. Si la marca nueva las necesita, se traen aquí en un PR propio.
