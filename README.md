# Kino

Plataforma de control de acceso para conjuntos cerrados. Este repositorio es el centro de trabajo de Kino: aquí conviven el producto, la marca, la investigación, el código y todas las IA y herramientas que trabajan en él.

## Mapa

| Carpeta | Qué hay | Quién escribe |
|---|---|---|
| [`kino/`](kino/) | El Kino nuevo: canon, investigación, marca, producto, código y entregas | Todos, siguiendo [`AGENTS.md`](AGENTS.md) |
| [`kino/canon/`](kino/canon/) | La verdad vigente: hechos, decisiones y vocabulario. Manda sobre todo lo demás | Solo con aprobación de Nico o Alejandro |
| [`coordinacion/`](coordinacion/) | Cómo se reparten y se pasan el trabajo personas e IA: tablero, bitácora, traspasos | Todo agente, al empezar y al terminar |
| [`herramientas/`](herramientas/) | Scripts compartidos que no dependen de ninguna marca | Todos |
| [`pre-kino/`](pre-kino/) | Archivo de la etapa anterior (identidad de marca anterior, diagnóstico, decks, sistema de marca 1.2.1). Base informativa, solo lectura | Nadie, salvo su índice y sus avisos |

## Por dónde empezar

| Si eres | Lee |
|---|---|
| Persona del equipo | Este archivo, [`kino/README.md`](kino/README.md) y [`coordinacion/tablero.md`](coordinacion/tablero.md) |
| Una IA o herramienta | [`AGENTS.md`](AGENTS.md). Claude Code lo carga solo desde [`CLAUDE.md`](CLAUDE.md) |
| Quien busca algo de antes | [`pre-kino/LEEME.md`](pre-kino/LEEME.md), con el índice de todo lo archivado |

## Reglas que no cambian

1. **El canon manda.** Si un archivo dice algo distinto de [`kino/canon/`](kino/canon/), gana el canon.
2. **Pre-kino no se edita.** Se lee, se cita y se hereda por decisión explícita. Su identidad de marca no se aplica a lo nuevo.
3. **Nada se borra.** Lo que se reemplaza se mueve a `_obsoleto/` dentro de su carpeta, con fecha.
4. **Una rama por tarea, un PR por rama.** Nico o Alejandro integran a `main`.
5. **Todo en español**: archivos, commits, PR y texto visible.

El detalle está en [`CONVENCIONES.md`](CONVENCIONES.md).

## Equipo

Nicolás Ramírez Acosta y Alejandro Monsalve Marín. Cliente y aliado: Manuel Arango. Piloto en producción: Monte Sereno, El Retiro.
