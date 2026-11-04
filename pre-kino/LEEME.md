# Pre-kino

Archivo de la etapa anterior de Kino, hasta el 4 nov 2026 (decisión D-001 en `../kino/canon/decisiones.md`). Tenía una identidad de marca distinta y sirvió como base informativa para el Kino nuevo.

## Cómo se usa

- **Solo lectura.** No se edita, no se reorganiza y no se le agrega trabajo nuevo. Las únicas excepciones son este `LEEME.md` y los avisos para agentes (`AGENTS.md`, `CLAUDE.md`).
- **La evidencia sigue vigente.** La inspección, las entrevistas y el diagnóstico son la base del Kino nuevo y conservan su jerarquía.
- **La marca no.** Logo, paleta, tipografía, voz, motion y sitio 1.2.1 son referencia. Lo que se quiera conservar se hereda con una decisión en el canon.
- **Rutas.** El árbol interno es el mismo que tenía la raíz del repositorio antes del 4 nov. Las rutas que citan los documentos de aquí son relativas a `pre-kino/`: donde un documento dice `inspeccion/`, hoy es `pre-kino/inspeccion/`.
- **Historia.** Todo se movió con `git mv`. `git log --follow pre-kino/<archivo>` muestra la historia completa.

## Índice

### Evidencia y diagnóstico (vigente como base)

| Ruta | Qué es |
|---|---|
| `inspeccion/` | Inspección directa por rol de la app en producción (14 a 16 sep 2026). La evidencia de mayor rango |
| `docs/proyecto/diagnostico-consolidado-v1.md` | Diagnóstico consolidado y pregunta guía v1 |
| `docs/proyecto/arquetipos-e-insights.md` | Arquetipos e insights |
| `docs/proyecto/reporte-inspeccion-por-rol.md` | Reporte sujeto por sujeto de la inspección |
| `docs/proyecto/incongruencias-2026-09-21.md` | Incongruencias entre carpetas contra los hechos vigentes |
| `MAESTRO-KINO.md` | Documento maestro: encargo, problemática, pregunta guía, retos, hechos y supuestos |
| `muestras-voz.md` | Mensajes reales anonimizados, reunidos para calibrar la voz |

### Instrucciones y traspasos de sesiones

| Ruta | Qué es |
|---|---|
| `CLAUDE-original.md` | Instrucciones de Claude Code hasta el 4 nov. Las vigentes están en `../CLAUDE.md` y `../kino/canon/proyecto.md` |
| `instrucciones-proyecto-kino.md`, `proyecto-claude-kino.md` | Copias anteriores de las instrucciones del proyecto de claude.ai |
| `SESION-NUBE.md` | Arranque de la sesión en la nube para la Fase 4 del sistema de marca |
| `TRASPASO-SISTEMA-DE-MARCA.md` | Traspaso del sistema de marca 1.2.1: estado, enlaces, Figma, cómo se reconstruye |

### Sistema de marca anterior (referencia)

| Ruta | Qué es |
|---|---|
| `encargo-sistema-de-marca.md` | Encargo original de Nico (23 sep) |
| `decisiones.md` | Decisiones de marca P, V, X y F4 con su estado |
| `avances.md` | Bitácora del sistema de marca por fase y departamento |
| `auditoria.md` | Auditoría del borrador: 90 elementos y hechos P1 a P15 |
| `registro-muletillas-2026-09-22.md` | Barrido de muletillas del deck del 22 sep |
| `gorr-brand-system/` | Cadena de tokens DTCG, contraste APCA, compuerta de voz y evals. Cliente `kino` |
| `branding/sistema/v3/` | Sitio 1.2.1, láminas de paradas, piezas del Pase, Figma, verificación y motion 3D |
| `branding/sistema/v2/`, `motor/`, `_obsoleto/` | Versiones previas del sistema |
| `paquetes/kino-motion/`, `paquetes/kino-motion-nativo/` | Motion en web y React Native (borrador 0.1) |
| `skills/` | Skills de Claude de la marca anterior (`gorr-*`, `kino-marca`). Inertes: no se cargan desde aquí |
| `Kino_Sistema_de_marca.html` | Sitio del sistema de marca armado (1.2.1) |
| `parada-1.html` a `parada-4c.html` | Láminas de revisión de cada parada |
| `sistema-de-marca-kino.md`, `TRASPASO-BRANDING-2026-09-23.md`, `decisiones-marca-2026-09-23.md` | Documentos ya históricos antes del 4 nov |

### Entregas académicas y decks

| Ruta | Qué es |
|---|---|
| `Kino_Deck_diagnostico_2026-09-19.html` y `.pdf` | Deck de diagnóstico del 19 sep |
| `Kino_Deck_diagnostico_2026-09-21.html` | Deck de diagnóstico del 21 sep |
| `Kino_Deck_flujos_y_mapa_2026-09-22.html` | Deck de flujos y mapa, base de la estética de decks |
| `kino_entrega_2.html` | Entrega 2 |
| `Claude outputs/` | Documentos Word del diagnóstico (G1 a G3, brief, documento unificado), capturas y scripts sueltos |
| `docs/proyecto/estetica-movimiento-decks.md`, `motor-deck-kino.md` | Cómo se armaban los decks |

### Otros

| Ruta | Qué es |
|---|---|
| `scripts/preparar-entorno.sh` | Hook de inicio anterior: instalaba dependencias y construía el sitio |
| `scripts/auditar-responsive.mjs` | Auditoría responsive del sitio 1.2.1 |
| `_obsoleto/` | Lo que ya estaba reemplazado antes del 4 nov |

`capturar.mjs` salió de aquí: hoy es `../herramientas/capturar.mjs`.

## Reconstruir algo para consultarlo

Funciona desde aquí, porque las rutas internas no cambiaron:

```bash
cd pre-kino/branding/sistema/v3/sitio
python3 verbal.py && python3 secciones.py && python3 construir.py && python3 verificar.py
```

Lo que eso regenere no se sube: `git checkout -- pre-kino` deja el archivo como estaba.

## Enlaces externos de esta etapa

| Qué | Dónde |
|---|---|
| Artefacto oficial «Kino · Sistema de marca» 1.2.1 | https://claude.ai/artifact/K8R2PRduS6SHBKYU31Bo6L |
| Figma de la marca anterior | https://www.figma.com/design/BO7UnDO9iE0aG6yUpNj0bc |
| Láminas de paradas y vistas previas | `TRASPASO-SISTEMA-DE-MARCA.md` §3 |
