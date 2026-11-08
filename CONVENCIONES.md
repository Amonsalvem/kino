# Convenciones

## Nombres

| Qué | Regla | Ejemplo |
|---|---|---|
| Carpetas y archivos | Minúsculas, español, palabras con guion, sin espacios ni tildes | `flujo-pase-visita.md` |
| Documentos de un día | Fecha ISO al inicio | `2026-11-04-entrevista-portero.md` |
| Índice de cada carpeta | `README.md` | |

## Ramas

`area/tema`, en minúsculas y con guiones. Áreas: `canon`, `investigacion`, `marca`, `producto`, `codigo`, `eafit`, `orden`. Si una sesión en la nube recibe una rama asignada (`claude/...`), se usa esa y el área va en el título del PR.

## Commits

- En español, en presente y con el área al inicio: `Marca: paleta base desde Figma`.
- Un commit por paso con sentido. Los archivos se mueven con `git mv`, en un commit sin cambios de contenido.

## Issues y PR

- Toda tarea empieza como issue. El PR que la resuelve lo enlaza con `Cierra #N`.
- El PR va en borrador hasta que esté listo para revisar.
- Etiqueta `menor`: cambios que la IA puede hacer sin pedir permiso (ver `AGENTS.md` §1).
- Solo Alejandro integra a `main`.

## Cómo se revisa y aprueba un PR

La Action «Resumen de PR» (`herramientas/resumir-pr.py`) deja en cada PR un comentario con de qué trata, qué se hizo y qué observar, y mantiene el issue **Panel de PR** con todos los abiertos. No usa IA: lee la plantilla, los archivos y los chequeos.

| Color | Qué significa | Qué haces |
|---|---|---|
| 🔴 Corregir antes | Chequeo fallido, falta «Uso de IA», toca `pre-kino/` o hay un posible secreto | No lo leas. Comenta qué corregir y sigue con el siguiente |
| 🟠 Decisión tuya | Toca canon, decisiones, marca, producto o reglas del repositorio | Lee solo los archivos 🟠 y responde la decisión en un comentario de línea |
| 🟡 Lectura normal | Evidencia, entregas, scripts, PR grande o que mezcla áreas | Revisa commit por commit |
| 🟢 Rápido | Solo movidos o registro de IA | Mira la cuenta de movidos y aprueba |

**Una sesión, en lote:**

1. Abre el Panel de PR. Se refresca con cada PR y a las 7 a. m.
2. Primero los 🔴: un comentario por PR y listo. Después los 🟢 y 🟡. Los 🟠 al final, con tiempo.
3. En cada PR lee el comentario de resumen. Lo «solo movido» git ya comprobó que es idéntico: no se lee.
4. En la pestaña *Files changed* marca **Viewed** en cada archivo leído; si el autor agrega commits, GitHub te muestra solo lo nuevo.
5. Aprueba con *Review changes → Approve* o comenta *Request changes*. Una pregunta en la línea sirve más que un comentario general.
6. Mientras un PR está en borrador, se comenta. Cuando el autor lo pasa a *Ready for review*, CODEOWNERS te pide la revisión y aparece en [tus revisiones pendientes](https://github.com/pulls/review-requested).

**Quien abre el PR lo hace revisable:** un tema por PR, los movimientos en un commit sin cambios de contenido, la plantilla llena y menos de 40 archivos para leer.

## Estados de una decisión

| Estado | Significa |
|---|---|
| PROPUESTA | Escrita con alternativas y una recomendada. No se aplica |
| APROBADA | Alejandro la aprobó; se cita cuándo y dónde |
| DESCARTADA | Se dejó de lado; se dice por qué |

## Formatos

- Documentos en Markdown. Tablas y listas antes que párrafos largos.
- Código en TypeScript por defecto.
- Lo que se genera (`build/`, `node_modules/`, capturas) no se versiona.
