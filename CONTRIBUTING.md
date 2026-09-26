# Cómo se trabaja en este repositorio

Estas son las convenciones que el repositorio ya sigue. La fuente es [`CLAUDE.md`](CLAUDE.md) («Cómo se trabaja en este repositorio») y el historial de commits.

## Ramas y PR

- Cada trabajo va en una rama propia: `marca/fase-4` para el sistema de marca, `claude/<nombre>` para las sesiones de Claude en la nube.
- Se integra a `main` por PR. Nico integra.
- Los PR se han integrado con squash: el commit en `main` lleva el número del PR, por ejemplo `… (#4)`.

## Commits

- Un commit por paso con sentido.
- Mensaje en español, con el área al inicio: `Área: descripción` o `Área · descripción`. Ejemplos del historial: `Motion: adaptador de React Native con Reanimated`, `Parada 4c · lámina de la 1.2.0 publicada y bitácoras`, `Fase 4 · Bloque 7: Parada 4 publicada, propuestas y bitácoras`.

## Qué no se hace

- Nada existente se borra. Lo que se reemplaza se mueve a `_obsoleto/` (o al `_obsoleto/` de su carpeta), con una fila en su `LEEME.md` que dice qué era y qué lo reemplaza.
- Los documentos con aviso de «Documento histórico» no se editan como si fueran vigentes ni se usan como fuente de decisiones.

## Decisiones y paradas

- Nada del sistema de marca se da por aprobado sin una respuesta explícita de Nico. El silencio no es aprobación.
- Las decisiones van a [`decisiones.md`](decisiones.md) con su estado; el avance, a [`avances.md`](avances.md).

## Antes de abrir un PR

- Si el cambio toca texto visible de la marca, pasa la compuerta de voz: `cd gorr-brand-system && npm run voz -- kino <archivo>`. Para el sitio, sobre `branding/sistema/v3/sitio/texto-visible.md`.
- Si toca tokens: `cd gorr-brand-system && npm run ciclo -- kino`.
- Si toca el sitio: `cd branding/sistema/v3/sitio && python3 construir.py && python3 verificar.py`.
- Si toca un paquete de motion: `npm run verificar` en su carpeta.
- Actualiza `decisiones.md` y `avances.md` cuando corresponda.

<!-- TODO: completar por el equipo: responsables por carpeta y usuario de GitHub de cada uno (para CODEOWNERS). -->
