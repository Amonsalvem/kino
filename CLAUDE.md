# Claude en Kino

@AGENTS.md

Lo de arriba es común a todos los agentes. Lo de abajo solo aplica a Claude.

## Contexto del proyecto

@kino/canon/proyecto.md

## Herramientas según dónde corra la sesión

Una sesión en la nube ve este repositorio, no el Mac ni los documentos o la memoria del proyecto de claude.ai. Al empezar, revisa qué herramientas tienes y dilo en una línea.

- **Hook de inicio.** `.claude/settings.json` corre `herramientas/preparar-entorno.sh` y su informe entra al contexto. Si algo sale en `[FALTA]`, dilo antes de depender de eso.
- **Artefactos de claude.ai.** Las láminas de revisión se publican como artefactos nuevos. Los artefactos de pre-kino (entre ellos el oficial «Kino · Sistema de marca», `K8R2PRduS6SHBKYU31Bo6L`) son de la identidad anterior: no se republican con la marca nueva sin una decisión en `kino/canon/decisiones.md`.
- **Figma.** El archivo `BO7UnDO9iE0aG6yUpNj0bc` es el de la marca de pre-kino. Si la marca nueva usa otro archivo, su clave se anota en `kino/marca/README.md`. Carga la skill `figma-use` antes de `use_figma`. Si el conector no responde, detente y pide que lo conecten en claude.ai.
- **Proyecto «Kino» de Claude Code.** No tiene instrucciones propias: el contexto llega por este archivo. Su pestaña *Environment* es donde se define `KINO_PERSONA` para el registro de prompts.
- **Memoria personal.** El progreso de aprendizaje de Alejandro vive en su memoria personal de Claude, no en el repositorio (skill `mentor`).
- Si necesitas algo que no está aquí, dilo y no lo supongas.

## Hooks

- `SessionStart` corre `herramientas/preparar-entorno.sh`.
- `UserPromptSubmit` corre `herramientas/registrar-prompt.py`: guarda el prompt en `registro-ia/` si se sabe quién escribe (`KINO_PERSONA` o `git config kino.persona`) y esa persona dio consentimiento. Súbelo en el PR de la sesión.

## Paradas

Nada de marca ni de producto se da por aprobado sin respuesta explícita de Alejandro. Cuando una decisión es suya, preséntala con alternativas y una recomendada, déjala como PROPUESTA en `kino/canon/decisiones.md` y sigue con lo que no dependa de ella.
