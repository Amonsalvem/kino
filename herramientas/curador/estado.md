# Estado del curador

Memoria del curador entre corridas. El curador lo reescribe cada semana. Última corrida: 16 nov 2026 (`informes/2026-11-16.md`).

## Inventario

| Pieza | Tipo | Qué hace | Quién la usa | Estado |
|---|---|---|---|---|
| `corrector-muletillas` | Skill | Revisa el texto antes de subirlo | Toda IA, en cada commit con texto | Vigente |
| `registro-ia` | Skill | Llena «Uso de IA» del PR y el perfil de cada persona | Toda IA, en cada PR o issue | Vigente |
| `mentor` | Skill | Enseña GitHub y su rol a Alejandro mientras trabaja | Claude, en sesiones con Alejandro | Vigente; evaluar retiro desde el 30 dic 2026 |
| `preparar-entorno.sh` | Hook `SessionStart` | Revisa node, python, git y Chromium | Claude Code | Vigente |
| `registrar-prompt.py` | Hook `UserPromptSubmit` | Guarda los prompts en `registro-ia/` con consentimiento | Claude Code | Vigente, sin efecto en la nube hasta definir `KINO_PERSONA` |
| `prompt-grok.md` | Prompt | Conecta Grok al repositorio | Nico | Vigente; el PR #29 lo cambia y sigue abierto |
| Curador semanal | Agente en GitHub Actions | Este agente | GitHub, cada lunes | Vigente (corridas: 9 y 16 nov 2026) |

Actions sin IA (solo lectura para el curador): «Revisar texto», «Resumen de PR», «Aprobar decisiones».

## Pendientes

- Alejandro: decidir si el workflow del curador fija `--permission-mode` tras `claude-code-action` v1.0.273 (12 nov 2026).
- Alejandro: definir `KINO_PERSONA` en sesiones en la nube (segunda semana).
- `personas/nico.md` no existe; lo decide Alejandro con Nico.
- Número libre para la próxima decisión: D-016, salvo que un PR nuevo agregue otra (D-015 está en el PR #35).
- `mentor`: evaluar su retiro desde el 30 dic 2026 (8 semanas desde el PR #12).
- Sin fecha en la fuente, comparar la semana siguiente: Claude Code 2.1.318 a 2.1.325 (CHANGELOG); cambios del borrador de MCP (`_meta`, OAuth Client ID Metadata Document); retiro de `grok-imagine-image-quality`.
- Sin acceso el 16 nov 2026: `x.ai/news` y `x.ai/changelog/build` (403). Reintentar; si sigue igual, proponer quitar el changelog de Grok Build de la tabla o buscar otra fuente primaria.
- Medir la longitud de las descripciones de las skills contra el tope de 1024 caracteres de agentskills.io.

## Fuentes que vigilar

Las de `prompt.md` §3.3. El curador agrega aquí una fuente nueva cuando le sirvió dos semanas seguidas. Candidata: `github.com/anthropics/claude-code-action/releases` ya está en la tabla y es la que más afecta al curador.
