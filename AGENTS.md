# Guía para agentes

Reglas comunes para cualquier IA o herramienta que trabaje en este repositorio: Claude (Code, claude.ai, Cowork), Codex, Cursor, Copilot, Gemini, scripts automáticos. Es la fuente única: los archivos propios de cada herramienta (`CLAUDE.md`, por ejemplo) la importan y solo agregan lo que es exclusivo de esa herramienta.

## 1. Antes de trabajar

1. Lee [`kino/canon/proyecto.md`](kino/canon/proyecto.md) (qué es Kino, hechos vigentes, vocabulario) y [`kino/canon/decisiones.md`](kino/canon/decisiones.md).
2. Lee [`coordinacion/tablero.md`](coordinacion/tablero.md). Si otra persona o agente tiene tomada la carpeta o el archivo que vas a tocar, no lo toques: coordina primero (§4).
3. Si retomas trabajo, busca su traspaso en [`coordinacion/traspasos/`](coordinacion/traspasos/).
4. Anota tu tarea en el tablero antes de escribir el primer archivo.

## 2. Qué manda sobre qué

| Orden | Fuente | Para qué |
|---|---|---|
| 1 | Lo que Nico o Alejandro dicen en la sesión | Siempre gana |
| 2 | [`kino/canon/decisiones.md`](kino/canon/decisiones.md), entradas APROBADAS | Decisiones vigentes |
| 3 | [`kino/canon/proyecto.md`](kino/canon/proyecto.md) | Contexto, hechos y vocabulario |
| 4 | Evidencia: `pre-kino/inspeccion/` (observado) > entrevistas del 2 sep > brief y documentos académicos | Afirmaciones sobre el problema |
| 5 | Resto de `pre-kino/` | Información de contexto, nunca una decisión vigente |

La identidad de marca de pre-kino (logo, paleta, tipografía, voz, motion, sitio 1.2.1) **no se aplica** a nada nuevo. Si algo de ella se quiere conservar, se hereda con una entrada en `decisiones.md`.

## 3. Dónde va cada cosa

| Trabajo | Carpeta |
|---|---|
| Hechos, decisiones, vocabulario | `kino/canon/` (solo con aprobación) |
| Evidencia nueva: entrevistas, inspecciones, datos, mercado | `kino/investigacion/` |
| Identidad nueva: estrategia, voz, visual, tokens | `kino/marca/` |
| Flujos, reglas de negocio, pantallas, especificaciones | `kino/producto/` |
| Apps y paquetes | `kino/codigo/` |
| Entregables solo académicos (EAFIT) | `kino/entregas/` |
| Scripts reutilizables sin marca | `herramientas/` |
| Estado del trabajo entre agentes | `coordinacion/` |

Cada carpeta tiene un `README.md` con su estructura. Si lo que vas a crear no encaja en ninguna, pregunta antes de inventar una carpeta nueva.

## 4. Cómo se comunican los agentes

El repositorio es el canal. No hay memoria compartida fuera de él: lo que no queda escrito aquí, el siguiente agente no lo sabe.

- **Tablero** (`coordinacion/tablero.md`): una fila por tarea en curso, con agente, persona que la pidió, rama, carpetas que toca y estado. Se actualiza al empezar, al bloquearse y al terminar.
- **Traspaso** (`coordinacion/traspasos/AAAA-MM-DD-tema.md`): obligatorio si dejas trabajo sin terminar. Sigue la plantilla. Debe bastar para que otro agente retome sin preguntar.
- **Bitácora** (`coordinacion/bitacora.md`): una línea por PR integrado o decisión aprobada. Solo se agrega al final.
- **Decisiones** (`kino/canon/decisiones.md`): toda decisión nace como PROPUESTA con alternativas y una recomendada. Pasa a APROBADA solo con respuesta explícita de Nico o Alejandro, citada con fecha. El silencio no es aprobación. Una IA nunca aprueba.

Si dos agentes necesitan el mismo archivo, el primero en el tablero lo conserva y el segundo deja una nota en la fila del primero.

## 5. Reglas de trabajo

1. **Rama propia** por tarea (`area/tema`, ver [`CONVENCIONES.md`](CONVENCIONES.md)), un commit por paso con sentido, PR en borrador hacia `main`. No se escribe directo en `main`.
2. **Pre-kino es de solo lectura.** Se puede construir o correr lo que hay ahí para consultarlo, pero los cambios que eso genere no se suben.
3. **Nada se borra.** Lo reemplazado va a `_obsoleto/` en su misma carpeta, con fecha en el nombre.
4. **Cada afirmación con fuente.** Cita el archivo. Si un dato no está en el repositorio, dilo y no lo inventes. Cifras de mercado: con fuente web y fecha.
5. **Académico y producto se separan.** Si una exigencia es solo del entregable (formato, rúbrica, plantilla), dilo. Si una decisión compromete el producto, evalúala pensando en quién la mantiene.
6. **Vocabulario**: «Pase» (de la visita o el colaborador) nunca se mezcla con «cuenta» (del residente). Nunca «permiso». «Visita», no «invitado». Detalle en `kino/canon/proyecto.md`.
7. **Español** en archivos, commits, PR y texto visible. Sin muletillas de IA: revisa con la skill `corrector-muletillas` o equivalente.
8. **Secretos fuera.** Nada de llaves, contraseñas, cédulas, teléfonos ni placas reales en el repositorio.

## 6. Al terminar

1. Corre las verificaciones de lo que tocaste (las de cada carpeta están en su `README.md`).
2. Actualiza tu fila del tablero: terminada o bloqueada, con el enlace al PR.
3. Si dejas algo abierto, escribe el traspaso.
4. Si propusiste decisiones, quedan en `decisiones.md` como PROPUESTA y se mencionan en el PR.
