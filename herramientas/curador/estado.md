# Estado del curador

Memoria del curador entre corridas. El curador lo reescribe cada semana. Última corrida: ninguna (archivo inicial, 9 nov 2026).

## Inventario

| Pieza | Tipo | Qué hace | Quién la usa | Estado |
|---|---|---|---|---|
| `corrector-muletillas` | Skill | Revisa el texto antes de subirlo | Toda IA, en cada commit con texto | Vigente |
| `registro-ia` | Skill | Llena «Uso de IA» del PR y el perfil de cada persona | Toda IA, en cada PR o issue | Vigente |
| `mentor` | Skill | Enseña GitHub y su rol a Alejandro mientras trabaja | Claude, en sesiones con Alejandro | Vigente |
| `preparar-entorno.sh` | Hook `SessionStart` | Revisa node, python, git y Chromium | Claude Code | Vigente |
| `registrar-prompt.py` | Hook `UserPromptSubmit` | Guarda los prompts en `registro-ia/` con consentimiento | Claude Code | Vigente |
| `prompt-grok.md` | Prompt | Conecta Grok al repositorio | Nico | Vigente |
| Curador semanal | Agente en GitHub Actions | Este agente | GitHub, cada lunes | Nuevo |

Actions sin IA (solo lectura para el curador): «Revisar texto», «Resumen de PR», «Aprobar decisiones».

## Pendientes

Ninguno.

## Fuentes que vigilar

Las de `prompt.md` §3.3. El curador agrega aquí una fuente nueva cuando le sirvió dos semanas seguidas.
