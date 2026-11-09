# Estado del curador

Memoria del curador entre corridas. El curador lo reescribe cada semana. Última corrida: 9 nov 2026 (`informes/2026-11-09.md`).

## Inventario

| Pieza | Tipo | Qué hace | Quién la usa | Estado |
|---|---|---|---|---|
| `corrector-muletillas` | Skill | Revisa el texto antes de subirlo | Toda IA, en cada commit con texto | Vigente |
| `registro-ia` | Skill | Llena «Uso de IA» del PR y el perfil de cada persona | Toda IA, en cada PR o issue | Vigente |
| `mentor` | Skill | Enseña GitHub y su rol a Alejandro mientras trabaja | Claude, en sesiones con Alejandro | Vigente |
| `preparar-entorno.sh` | Hook `SessionStart` | Revisa node, python, git y Chromium | Claude Code | Vigente |
| `registrar-prompt.py` | Hook `UserPromptSubmit` | Guarda los prompts en `registro-ia/` con consentimiento | Claude Code | Vigente |
| `prompt-grok.md` | Prompt | Conecta Grok al repositorio | Nico | Vigente |
| Curador semanal | Agente en GitHub Actions | Este agente | GitHub, cada lunes | Vigente (primera corrida 9 nov 2026) |

Actions sin IA (solo lectura para el curador): «Revisar texto», «Resumen de PR», «Aprobar decisiones».

## Pendientes

- Consultar las fuentes que faltaron el 9 nov 2026: docs.x.ai, Figma MCP, modelcontextprotocol.io, agentskills.io, github.blog/changelog.
- Confirmar las fechas de Claude Code 2.1.312 a 2.1.319: el changelog no las trae.
- `personas/nico.md` no existe; lo decide Alejandro con Nico.
- `KINO_PERSONA` sin definir en sesiones en la nube.
- Antes de proponer una decisión, contar D-009 (PR #28) y los demás PR abiertos para el número libre.
- `mentor`: evaluar su retiro desde el 30 dic 2026 (8 semanas desde el PR #12).

## Fuentes que vigilar

Las de `prompt.md` §3.3. El curador agrega aquí una fuente nueva cuando le sirvió dos semanas seguidas.
