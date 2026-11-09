## Qué cambia

Área: orden. Registro de los archivos de Figma que cambiaron desde el último PR integrado: índice en `kino/figma/README.md`, una ficha por archivo y su miniatura. Este PR se actualiza solo cada día mientras siga abierto.

## Por qué

D-003: la marca se trabaja en Figma. Este registro deja ver a los agentes del repositorio qué existe en Figma y qué cambió, sin que Nico mande archivos.

## Decisiones

Ninguna. Un cambio en Figma no es una decisión aprobada: lo que deba decidirse va como PROPUESTA en `kino/canon/decisiones.md`.

## Cómo se verificó

La Action «Sincronizar Figma» leyó los proyectos con la API de Figma. Revisa las fichas y las miniaturas en la pestaña «Files changed».

## Uso de IA

Sin IA. Lo genera `herramientas/sincronizar-figma.py` con la API de Figma.
