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
- **Proyecto de claude.ai.** Si cambia un documento de conocimiento del proyecto, la copia de aquí se actualiza en el mismo PR. `kino/canon/proyecto.md` es el espejo de las instrucciones del proyecto.
- Si necesitas algo que no está aquí, dilo y no lo supongas.

## Skills

- `.claude/skills/corrector-muletillas`: úsala antes de entregar texto visible o documentos.
- Las skills de la marca anterior (`gorr-*`, `kino-marca`) están archivadas en `pre-kino/skills/` y no se cargan. No las uses para trabajo nuevo.
- Cuando la marca nueva tenga su skill, va en `.claude/skills/` y se anota aquí.

## Paradas

Nada de marca ni de producto se da por aprobado sin respuesta explícita del equipo. Cuando una decisión es del equipo, preséntala con alternativas y una recomendada, déjala como PROPUESTA en `kino/canon/decisiones.md` y sigue con lo que no dependa de ella.
