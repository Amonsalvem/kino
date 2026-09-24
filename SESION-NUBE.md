# Sesión en la nube · cómo arrancar

## Prompt para pegar al abrir la sesión

> Lee `CLAUDE.md`, `TRASPASO-SISTEMA-DE-MARCA.md` (§9), `encargo-sistema-de-marca.md` y `decisiones.md`. La Parada 3 está aprobada (X1 a X11). Antes de empezar, dime qué herramientas tienes: la de artefactos de claude.ai y el conector de Figma (archivo `BO7UnDO9iE0aG6yUpNj0bc`). Si alguna falta, dilo y sigue con el resto. Crea la rama `marca/fase-4` y construye la Fase 4 en el orden de abajo, con un commit y un push por bloque. Publica las láminas de revisión como artefactos nuevos. El artefacto oficial `K8R2PRduS6SHBKYU31Bo6L` se republica solo después de que yo apruebe la Parada 4 (regla del encargo); para republicarlo, léelo primero con la acción read y publica con su url. Si algo necesita una decisión mía, anótalo en `decisiones.md` como PROPUESTA con dos alternativas y sigue con lo que no dependa de ella. Al final deja la Parada 4 lista como `parada-4.html` y actualiza `avances.md` y el §9 del traspaso.

## Bloques de la Fase 4

| # | Bloque | Hecho cuando |
|---|---|---|
| 1 | Tokens: paleta aprobada en `gorr-brand-system/clientes/kino` (oscuro reajustado de `branding/sistema/v3/fase3/oscuro-ajustado.json`, acción #00D595, 7 estados y el evento Rechazado, radio 14, arco, trazo 1,7, motion crecer) | `npm run ciclo -- kino` en verde; `npm run contraste` sin fallos APCA; `kino-brand.css` regenerado |
| 2 | Departamentos 03 a 12 en el sitio: reemplazar los apartados «en construcción» de `secciones.py` | Cada departamento con reglas, ejemplos y lo que no se hace; `verificar.py` sin errores |
| 3 | Pase: imagen de WhatsApp, Pase vivo y PDF en claro con la forma Portal; señal de portería con «Llamar al residente» en vencido | Probado a 360, 768 y 1440 px con Playwright |
| 4 | Sitio definitivo: copia fechada del borrador `Kino_Sistema_de_marca_2026-09-23.html` en `_obsoleto/` y Motion Playground desde `gorr-brand-system/vendor/motion/` | Sin desplazamiento horizontal, reduced-motion respetado |
| 5 | Fase 5: términos prohibidos, «permiso», `npm run voz -- kino` sobre `texto-visible.md`, largos de UX writing, tú/usted por audiencia, APCA de todos los pares | Informe en `avances.md` |
| 6 | Figma: variables sincronizadas con DTCG (hoy 51 contra 118 primitivos, 34 contra 37 semánticos, 12 contra 17 de movimiento, sin colección de tipografía), 13 páginas vacías llenas, componentes con todos sus estados | Si el conector está; si no, queda para Cowork |
| 7 | `parada-4.html` con lo construido y las preguntas abiertas, publicada como artefacto | Lámina lista para revisar |

## Al volver a Cowork

1. En GitHub, fusiona `marca/fase-4` en `main` (pull request).
2. En GitHub Desktop: Fetch origin → Pull.
3. En Cowork: «Lee `TRASPASO-SISTEMA-DE-MARCA.md`, revisa `parada-4.html` y sincroniza Figma y el artefacto cuando apruebe».

Si cambias un documento en claude.ai, copia la versión nueva en `docs/proyecto/`.
