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
