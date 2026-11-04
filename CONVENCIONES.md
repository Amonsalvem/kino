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

## Cómo se revisa un PR

Un PR grande casi nunca es grande de verdad: la mayoría de los archivos suelen estar solo movidos. Se revisa así:

1. **Lee la sección «Qué revisar» del PR.** El agente que lo abre pega ahí la salida de `bash herramientas/revisar-pr.sh`. Lo que el script cuenta como «movidos sin cambios» git ya comprobó que es idéntico: no se lee.
2. **Revisa commit por commit**, no la pestaña completa de archivos. Por regla, los movimientos van en su propio commit, sin cambios de contenido, y ese commit se aprueba con mirar la cuenta.
3. **Lee solo la lista «Para revisar»**, de arriba abajo. Si un archivo no se entiende sin abrir otro, el PR está mal partido: se pide que lo dividan.
4. **Aprueba o comenta en GitHub.** Una pregunta concreta en la línea es mejor que un comentario general.

Quien abre el PR lo hace revisable: un tema por PR, los movimientos separados del contenido y la salida del script en la descripción.

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
