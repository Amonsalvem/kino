# Herramientas

Scripts compartidos que no dependen de ninguna marca. Si una herramienta solo sirve para una carpeta, vive en esa carpeta.

| Script | Qué hace | Uso |
|---|---|---|
| `preparar-entorno.sh` | Comprueba node, python, git y Chromium. Lo corre el hook de inicio de Claude Code | `bash herramientas/preparar-entorno.sh` |
| `revisar-texto.py` | Chequeo de muletillas, cifras sin fuente y textos largos. Lo corre GitHub en cada PR | `python3 herramientas/revisar-texto.py <archivos>` o `--todo` |
| `registrar-prompt.py` | Hook de Claude Code que guarda cada prompt en `registro-ia/`, con datos sensibles tapados y solo con consentimiento | Lo corre el hook; no se usa a mano |
| `prompt-grok.md` | Prompt que conecta una conversación de Grok al repositorio: sube lo hecho y cada avance nuevo, con las reglas de `AGENTS.md` | Nico lo pega en cada conversación de Grok (issue #15) |
| `capturar.mjs` | Capturas de un HTML a 360, 768 y 1440 px, en oscuro y claro, con chequeo de desborde horizontal y errores de consola | `node herramientas/capturar.mjs <archivo.html> [carpeta-salida]` |

**Requisitos.** Node 20 o más. `capturar.mjs` usa Playwright (local o global) y el Chromium de `/opt/pw-browsers` si existe. Las capturas salen en `capturas/`, que no se versiona.

**Herramientas de pre-kino.** La cadena de tokens, contraste y voz (`pre-kino/gorr-brand-system/`) y la auditoría responsive del sitio anterior (`pre-kino/scripts/auditar-responsive.mjs`) siguen allí. Si la marca nueva las necesita, se traen aquí en un PR propio.
