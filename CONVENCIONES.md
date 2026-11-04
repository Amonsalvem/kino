# Convenciones

## Nombres

| Qué | Regla | Ejemplo |
|---|---|---|
| Carpetas y archivos | Minúsculas, español, palabras con guion, sin espacios ni tildes | `flujo-pase-visita.md` |
| Documentos de un día | Fecha ISO al inicio | `2026-11-04-entrevista-portero.md` |
| Versiones reemplazadas | A `_obsoleto/` con la fecha en que se reemplazaron | `_obsoleto/paleta-2026-11-04.json` |
| Índice de cada carpeta | `README.md` | |
| Archivos de agentes | Los nombres que cada herramienta espera | `AGENTS.md`, `CLAUDE.md` |

## Ramas

`area/tema`, en minúsculas y con guiones. Las áreas son las carpetas de primer nivel de `kino/` más dos propias del repositorio:

| Área | Para |
|---|---|
| `canon/` | Cambios a hechos, decisiones o vocabulario |
| `investigacion/` | Evidencia nueva |
| `marca/` | Identidad nueva |
| `producto/` | Flujos, reglas, pantallas |
| `codigo/` | Apps y paquetes |
| `entregas/` | Entregables académicos |
| `orden/` | Estructura del repositorio, convenciones, herramientas |
| `coordinacion/` | Solo si el cambio es al protocolo, no al tablero del día |

Las sesiones de Claude en la nube pueden recibir una rama asignada (`claude/...`). En ese caso se usa esa y el área va en el título del PR.

## Commits

- En español, en presente y con el área al inicio: `Marca: paleta base en OKLCH`.
- Uno por paso con sentido. Un movimiento de archivos va en su propio commit, sin cambios de contenido, para que `git log --follow` siga la historia.
- Mover siempre con `git mv`.

## Pull requests

- En borrador hasta que esté listo para revisar.
- Usan la plantilla de `.github/pull_request_template.md`.
- Nico o Alejandro integran a `main`. Una IA nunca integra.

## Estados de una decisión

| Estado | Significa |
|---|---|
| PROPUESTA | Escrita con alternativas y una recomendada. No se aplica como vigente |
| APROBADA | Respuesta explícita del equipo, citada con quién y cuándo |
| DESCARTADA | Se dejó de lado; se dice por qué |
| REEMPLAZADA | La sustituye otra; se enlaza |

## Formatos

- Documentos en Markdown. Tablas y listas antes que párrafos largos.
- Código en TypeScript por defecto, con los supuestos declarados arriba del bloque.
- Datos en JSON o CSV; registros de observación en JSONL.
- Lo que se genera (`build/`, `node_modules/`, capturas) no se versiona.
