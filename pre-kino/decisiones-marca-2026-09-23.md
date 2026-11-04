> **Documento histórico (23 sep 2026, tarde). No es la referencia vigente.** Lo reemplazan `claude/traspaso-sistema-de-marca.md`, `claude/decisiones-sistema-de-marca.md` y `claude/avances-sistema-de-marca.md`, que mandan donde difieran. Se conserva por trazabilidad. Varias cosas de aquí ya cambiaron:
> - el tratamiento con la administración es usted;
> - el sitio muestra una sección a la vez, no láminas;
> - el texto sobre el acento se propone resolver con #00D595 y no con tamaño;
> - los estados del Pase son siete más el evento Rechazado;
> - la calibración de voz está en 40/42.

# Decisiones de marca · 23 sep 2026

Tomadas por el equipo. Reemplazan lo que diga lo contrario en `claude/sistema-de-marca-kino.md` y en las instrucciones del proyecto.

**Etapa (aclarado por el equipo el 23 sep):** apenas se está creando la base de todo lo que compone la marca Kino. Lo construido hasta hoy (deck, manual, Figma, rotulado «v2») es un primer borrador de trabajo, no un sistema cerrado.

1. **Kino deja de ser marca blanca.** La identidad visual se potencia porque Kino es la marca. Se elimina la capa tenant (`kino-tenant-marca`, `kino-tenant-radio`). El conjunto (p. ej. Refugio Campestre) aparece solo como dato: texto o chip, sin logo ni colores propios.
2. **`kino_entrega_2.html` es la referencia, no la base.** («Kino · Quién decide quién entra», 29 láminas). Llamarla «base» fue una hipérbole: se tomó porque era lo más avanzado que había en cuanto a marca. De ella se partió para el lenguaje de evidencia, la gramática de flujo, el objeto pase, las matrices, los chips de evidencia y la navegación con progreso, y el primer design system y sistema de movimiento salieron de ahí, sobre el motor de `Motion_Playground_1.html` (`gorr-brand-system/vendor/motion/`). Nada de eso es canon: se puede replantear.
3. **«Pase» reemplaza a «permiso»** como nombre del objeto que recibe el invitado o colaborador (autor, motivo, vigencia, modo). «Cuenta» sigue siendo del residente, y pase y cuenta no se mezclan.
4. **El acento vuelve a `#00BB83`** (biolum d70, el de la entrega 2). El texto sobre el acento es oscuro (`#00140C`, 7,63:1 WCAG) y, como APCA le da Lc 55,1, va a 18 px o más en peso 700 (21 px en 600). Se resuelve con tamaño, no cambiando el color.
5. **Entregables de esta etapa:** un deck HTML de marca con el motor de movimiento, un manual como activo interno navegable y una librería de componentes y variables en Figma.
6. **Los motion graphics no se sacrifican** al optimizar rendimiento o navegación.

## Estado de los entregables (23 sep, tarde)

| Entregable | Dónde | Qué tiene |
|---|---|---|
| Deck de marca | Artifact «Kino Sistema de Marca» (https://claude.ai/artifact/K8R2PRduS6SHBKYU31Bo6L) y `kino/Kino_Sistema_de_marca_2026-09-23.html` | 28 láminas sobre el shell y el motor tomados de la entrega 2; navegación lámina por lámina |
| Implementación | `kino/branding/sistema/v2/` | `kino-sistema.css`, `kino-movimiento.js` (5 verbos: aparecer, confirmar, caducar, revocar, cascada), `paginar.js`; fuentes para reconstruir en `v2/fuentes/` |
| Manual interno | Artifact «Kino» tipo Design System (https://claude.ai/artifact/224KDZ6KbmV8PFeXG2BbPD), versión 11 | README, 10 la membrana, 20 aplicación, 30 verificación, 40 movimiento; componentes Estado, Pase, Vigencia, Tarjeta, Evidencia, Flujo, Tabla, Movimiento, Dato, Marca |
| Librería Figma | «Kino — Sistema de marca v2», equipo de Alejandro (https://www.figma.com/design/BO7UnDO9iE0aG6yUpNj0bc) | 113 variables, 12 estilos de texto, 6 efectos, componentes Estado, Pase/Boleto, Pase/Fila, Flujo/Nodo, Evidencia, Tarjeta, Marca |

## Herramientas

Activadas el 23 sep con `activar-herramientas.sh` en la Terminal del Mac: Terrazzo 2.7.1, Leonardo 1.1.0, apca-w3 0.1.9, utopia-core 1.6.0, promptfoo 0.123.1, colorjs 0.7.1, iconoir 7.12.1, skill DTCG de dgtlntv y anthropics/skills. Resultados: 38/38 pares pasan; Leonardo reproduce la paleta con ΔE OK medio 0,019; 6/6 archivos DTCG válidos. Terrazzo y promptfoo se corren desde la Terminal del Mac.

## Pendiente del equipo
- Actualizar las instrucciones del proyecto: regla 6 (marca blanca), regla 5 (quitar «marca blanca» de la diferenciación) y vocabulario («permiso» → «pase»). Claude no puede editarlas.
- Correr Terrazzo y promptfoo en el Mac y dejar su salida en `reportes/`.
- No tenemos: el vectorial original del logo, la licencia de Arkit ExtraBold ni la decisión de tú/usted con la administración.

Traspaso para el chat siguiente: `claude/traspaso-branding-2026-09-23.md`.
