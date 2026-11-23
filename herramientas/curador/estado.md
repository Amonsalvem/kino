# Estado del curador

Memoria del curador entre corridas. El curador lo reescribe cada semana. Última corrida: 23 nov 2026 (`informes/2026-11-23.md`). La del 16 nov sigue en el PR #36 sin integrar.

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

- Resolver el PR #36 (curador del 16 nov): choca con este `estado.md`.
- Alejandro decide si `curador-semanal.yml` fija `--permission-mode default` tras `claude-code-action` v1.0.273 (informe del 16 nov).
- `KINO_PERSONA` sin definir en sesiones en la nube (tercera semana).
- `personas/nico.md` no existe; lo decide Alejandro con Nico.
- Leer la sección «Uso de IA» de #37 y #38 para la retroalimentación.
- Claude Code: fechas de 2.1.326 a 2.1.331 tomadas de la página de releases (16 a 23 nov); el CHANGELOG no las trae.
- Grok Build: la fuente x.ai/build/changelog tiene fechas y versiones que no cuadran; comparar la semana siguiente. `x.ai/news` da 403 por `WebFetch`.
- Revisar desde el 30 nov 2026 si Kino agrega plugins (autoactualización de marketplaces gestionados en Claude Code 2.1.331).
- Número libre para una decisión: D-025 (D-024 está en #38).
- `mentor`: evaluar su retiro desde el 30 dic 2026 (8 semanas desde el PR #12).

## Fuentes que vigilar

Las de `prompt.md` §3.3. El curador agrega aquí una fuente nueva cuando le sirvió dos semanas seguidas.
