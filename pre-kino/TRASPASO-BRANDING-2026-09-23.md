> **Documento histórico (23 sep 2026, tarde). No es la referencia vigente.** Lo reemplazan `claude/traspaso-sistema-de-marca.md`, `claude/decisiones-sistema-de-marca.md` y `claude/avances-sistema-de-marca.md`, que mandan donde difieran. Se conserva por trazabilidad. Varias cosas de aquí ya cambiaron:
> - el tratamiento con la administración es usted;
> - el sitio muestra una sección a la vez, no láminas;
> - el texto sobre el acento se propone resolver con #00D595 y no con tamaño;
> - los estados del Pase son siete más el evento Rechazado;
> - la calibración de voz está en 40/42.

# Traspaso · branding de Kino · 23 sep 2026

Para continuar el desarrollo de marca en un chat nuevo. Este documento manda sobre el historial del chat anterior; `claude/decisiones-marca-2026-09-23.md` y `claude/sistema-de-marca-kino.md` tienen el detalle.

## 1. Estado en una línea

La marca v2 está construida y publicada: deck de marca paginado con motor de movimiento, manual interno (Design System) y librería de Figma. Kino es la marca (ya no es marca blanca). El objeto se llama «pase». El acento es `#00BB83`. Lo abierto es la voz: faltan muestras y decisiones (ver §6).

## 2. Decisiones vigentes (no reabrir sin que el equipo lo pida)

| # | Decisión | Fecha |
|---|---|---|
| 1 | Kino es la marca; el conjunto aparece solo como dato («Refugio Campestre · Casa 14»). Sin capa tenant | 23 sep |
| 2 | La base estética es `kino_entrega_2.html`: aurora, cortina, crecer/decaer, boleto con talón, evidencia, gramática de flujo | 23 sep |
| 3 | «Pase» reemplaza a «permiso» en interfaz, código y material. «Cuenta» es del residente. No se mezclan | 23 sep |
| 4 | Acento `#00BB83` (biolum d70). El texto sobre acento va a 18 px o más en 700 (APCA Lc 55,1) | 23 sep |
| 5 | El acento significa otorgar: solo el botón que da el pase, el boleto recién emitido y la marca | 23 sep |
| 6 | Tema oscuro canónico; claro («Laboratorio») es el segundo | 19 sep |
| 7 | El color solo nombra hechos que el lector confirmó (`sin-confirmar` sin relleno, borde discontinuo) | 19 sep |
| 8 | Perfil de tono NN/g: formalidad 2, humor 1, respeto 1, entusiasmo 2. Tuteo en la app | 22 sep |
| 9 | Los motion graphics no se sacrifican: duraciones, curvas, desenfoque y cascadas de la entrega 2 se conservan | 23 sep |
| 10 | El deck se navega lámina por lámina: un gesto de scroll = una lámina | 23 sep |

## 3. Dónde está cada cosa (rutas verificadas el 23 sep)

Carpeta raíz en el Mac de Alejandro: `…/iCloud Drive/Documents/montesereno/projects/kino/`.

| Pieza | Ruta o enlace |
|---|---|
| Deck de marca (28 láminas) | `kino/Kino_Sistema_de_marca_2026-09-23.html` · artefacto https://claude.ai/artifact/K8R2PRduS6SHBKYU31Bo6L (v3, compartido con enlace) |
| Manual interno (Design System) | artefacto «Kino» https://claude.ai/artifact/224KDZ6KbmV8PFeXG2BbPD (v11, privado) |
| Librería Figma | https://www.figma.com/design/BO7UnDO9iE0aG6yUpNj0bc (equipo de Alejandro). 113 variables, 12 estilos de texto, 6 efectos, componentes Estado, Pase/Boleto, Pase/Fila, Flujo/Nodo, Evidencia, Tarjeta, Marca |
| Entrega 2 (base estética) | `kino/kino_entrega_2.html` |
| Motor de movimiento | `kino/gorr-brand-system/vendor/motion/Motion_Playground_1.html` |
| Implementación v2 | `kino/branding/sistema/v2/` → `kino-sistema.css`, `kino-movimiento.js`, `paginar.js` |
| Fuentes para reconstruir el deck, el manual y Figma | `kino/branding/sistema/v2/fuentes/` (ver §4) |
| Fuente de verdad de la marca | `kino/gorr-brand-system/clientes/kino/` → `marca.config.json`, `tokens/` (DTCG 2025.10), `voz.json`, `pares.json`, `skill/kino-marca/`, `evals/`, `reportes/` |
| Capa v1 (anterior) | `kino/branding/sistema/kino-brand.css`, SVG en `kino/branding/sistema/marca/` |
| Logo (solo PNG) | `kino/branding/KINO PNG BL 2.png` y `KINO PNG WH 2.png` (1543 × 1425) |
| Muestras de voz | `kino/muestras-voz.md` |
| Registro de muletillas | `kino/registro-muletillas-2026-09-22.md` |

## 4. Cómo se reconstruye

**Tokens y contraste** (desde el Mac o la VM del dispositivo):

```bash
cd kino/branding/sistema && npm run construir        # cadena completa + 38 pares
cd ../../gorr-brand-system
npm run voz -- kino                                  # compuerta de voz
npm run calibrar-voz -- kino                         # 21/42 frases atrapadas
npm run terrazzo                                     # solo en la Terminal del Mac
npm run evals:promptfoo                              # solo en el Mac, con ANTHROPIC_API_KEY
```

**Deck de marca**: `v2/fuentes/fuente-deck/build.py` genera el HTML y la versión del artefacto. Es Python 3 y se corre desde esa carpeta. Antes hay que ajustar tres rutas al inicio del archivo, que apuntaban al contenedor del chat anterior:
- `E2` → `kino/kino_entrega_2.html`
- `UP` y `TOK` → `kino/gorr-brand-system/clientes/kino`

Se arma con: tokens (`build/kino-tokens.css`), `alias.css`, `componentes-e2.css`, `v2.css`, `paginar.css`, los scripts de la entrega 2 (el script de cabecera, el motor y el controlador, con dos ajustes en `RITMO`), `kino-movimiento.js`, `demos.js` y `paginar.js`. Para republicar el artefacto se usa su URL; la herramienta pide leer la versión viva primero.

**Manual**: `v2/fuentes/manual-design-system/project/` es la copia del proyecto del artefacto (README, 10–40, componentes, `tokens.json`, `bundle.css`). `manual.py` regenera las vistas previas de los componentes. Los logos y los iconos viven en el almacén de assets del artefacto, no en esta carpeta.

**Figma**: `v2/fuentes/figma/` → `figma-data.json` (valores), `fig1.js` (script que creó las variables) y `figma-ledger.json` (ids de colecciones y páginas). Antes de tocar el archivo hay que cargar la skill `figma-use`.

## 5. Verificación al cierre

- 38 de 38 pares de color pasan WCAG 2.2. APCA se reporta en todos.
- Leonardo reproduce la paleta con ΔE OK medio de 0,019.
- Los 6 archivos DTCG son válidos (validador de dgtlntv).
- El deck:
  - sin errores de página ni desborde horizontal a 390, 1024, 1280 y 1440 px;
  - un gesto de trackpad pasa una lámina (prueba repetida tres veces);
  - la coreografía arranca al 45 % del paso de lámina.

## 6. Pendientes

**Datos que no tenemos** (confirmado por el equipo el 23 sep):
- El logo vectorial original. Solo hay PNG; los SVG son reconstrucciones con 98 % de coincidencia.
- La licencia de Arkit ExtraBold.
- El tú o usted con la administración: ABIERTO.
- Para la voz: capturas de la app, mensajes reales de portería o WhatsApp, correcciones confirmadas del equipo y textos que el equipo considere bien escritos. Las secciones b, c y d de `muestras-voz.md` están vacías. La sección c tiene 42 candidatas del barrido del 22 sep, con autoría sin confirmar.
- `kino-tokens.json`, `kino-logo.svg` y `kino-marca.md` no existen; no se sabe si deberían existir.

**Trabajo abierto:**
1. Correr Terrazzo y promptfoo en el Mac y guardar la salida en `reportes/`.
2. Decidir la unidad de los cupos (por casa, por residente o por conjunto). Es una decisión de producto y bloquea textos para la administración.
3. Plantillas de documento.
4. Ver la paleta en las pantallas de portería de HikCentral.
5. Decidir si el chip de evidencia «Prueba ejecutada» sigue usando el acento, que choca con la decisión 5.
6. En Figma, los efectos del tema claro son estilos aparte (« · claro»), no variables por modo.
7. Actualizar las instrucciones del proyecto. Siguen diciendo «marca blanca» (reglas 5 y 6) y «permiso» en el vocabulario. Solo el equipo puede editarlas, y mientras tanto confunden a cualquier chat nuevo.

## 7. Para abrir el chat nuevo

Pega esto como primer mensaje:

> Continuamos el branding de Kino. Lee primero `claude/traspaso-branding-2026-09-23.md` y `claude/decisiones-marca-2026-09-23.md` del proyecto. Mandan sobre las instrucciones del proyecto donde difieran: Kino ya no es marca blanca y el objeto se llama «pase». Las fuentes de todo lo construido están en `kino/branding/sistema/v2/fuentes/`. No sacrifiques los motion graphics. Lo siguiente que quiero hacer es: [tarea].
