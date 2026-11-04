# Coordinación

Cómo se reparten y se pasan el trabajo las personas y las IA de Kino. El repositorio es el único canal compartido: lo que no queda escrito aquí, el siguiente agente no lo sabe.

| Archivo | Para qué | Cuándo se toca |
|---|---|---|
| [`tablero.md`](tablero.md) | Trabajo en curso: quién hace qué, en qué rama, sobre qué carpetas | Al empezar, al bloquearse y al terminar una tarea |
| [`bitacora.md`](bitacora.md) | Lo que ya pasó: PR integrados y decisiones aprobadas | Al integrar un PR o aprobar una decisión. Solo se agrega al final |
| [`traspasos/`](traspasos/) | Estado de un trabajo que queda a medias, para que otro lo retome | Al dejar algo sin terminar |

## Protocolo

1. **Leer.** `AGENTS.md`, `kino/canon/` y este tablero.
2. **Tomar.** Agrega una fila al tablero con estado «en curso». Si una carpeta ya está tomada, escribe una nota en esa fila y espera, o pide al equipo que decida.
3. **Trabajar** en tu rama. Un commit por paso.
4. **Soltar.** Pasa la fila a «en revisión» con el enlace al PR, o a «bloqueada» con lo que falta y a quién.
5. **Traspasar** si no terminaste: `traspasos/AAAA-MM-DD-tema.md` desde la plantilla, enlazado en la fila.
6. **Cerrar.** Cuando el PR se integra, la fila sale del tablero y entra una línea a la bitácora.

## Identificar al agente

En el tablero y en los traspasos, el agente se nombra por herramienta y lugar: `Claude Code (nube)`, `Claude (Cowork)`, `Codex`, `Cursor`. Si hay varias sesiones de la misma herramienta, se agrega la rama.

## Conflictos

- Dos agentes no escriben a la vez en la misma carpeta. Gana la fila más antigua del tablero.
- Si un agente encuentra evidencia que contradice el canon, no corrige el canon: abre una PROPUESTA en `kino/canon/decisiones.md` y la señala en su PR.
- Si el tablero dice algo que el estado real de las ramas contradice (fila abandonada, PR cerrado), se pregunta al equipo antes de retomar.
