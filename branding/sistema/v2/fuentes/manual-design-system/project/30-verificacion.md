# Verificación

Todo par de color se verifica de forma programática en cada build. Las escalas no se eligieron a ojo: se generan resolviendo un contraste objetivo sobre el fondo de cada tema, y la paleta de registro está congelada en los valores de la entrega 2.

## Resultado (23 sep 2026)

38 pares verificados, 0 fallos. WCAG 2.2 es la condición obligatoria: 4.5:1 para texto y 3:1 para bordes, indicadores y elementos gráficos. APCA (`apca-w3`) se reporta en todos los pares. El texto sobre acento lleva además un tamaño mínimo calculado con `fontLookupAPCA`: en oscuro, 18 px en peso 700.

| Par | WCAG | APCA Lc | Mínimo |
|---|---|---|---|
| oscuro: texto primario sobre superficie base | 16,49:1 | -102,4 | 4.5:1 |
| oscuro: texto secundario sobre superficie base | 10,38:1 | -71,8 | 4.5:1 |
| oscuro: texto tenue sobre superficie base | 6,62:1 | -49,2 | 3.0:1 |
| oscuro: acento sobre superficie base | 6,98:1 | -52,3 | 3.0:1 |
| oscuro: texto sobre acento | 7,63:1 | 55,1 | 4.5:1 · 18 px a 700 |
| oscuro: borde definido sobre superficie base | 3,19:1 | -23,1 | 3.0:1 |
| oscuro: texto inverso sobre superficie inversa | 18,04:1 | 101,7 | 4.5:1 |
| oscuro: texto del estado vigente | 7,33:1 | -69,6 | 4.5:1 |
| oscuro: borde del estado vigente | 3,19:1 | -23,7 | 3.0:1 |
| oscuro: texto del estado por-vencer | 7,32:1 | -69 | 4.5:1 |
| oscuro: borde del estado por-vencer | 3,19:1 | -23,4 | 3.0:1 |
| oscuro: texto del estado vencido | 8,02:1 | -62,9 | 4.5:1 |
| oscuro: borde del estado vencido | 3,19:1 | -23,1 | 3.0:1 |
| oscuro: texto del estado negado | 7,31:1 | -67,2 | 4.5:1 |
| oscuro: borde del estado negado | 3,2:1 | -24,4 | 3.0:1 |
| oscuro: texto del estado sin-confirmar | 10,38:1 | -71,8 | 4.5:1 |
| oscuro: borde del estado sin-confirmar | 3,19:1 | -23,1 | 3.0:1 |
| oscuro: texto del estado identidad | 7,35:1 | -68,3 | 4.5:1 |
| oscuro: borde del estado identidad | 3,19:1 | -23,4 | 3.0:1 |
| claro: texto primario sobre superficie base | 18,04:1 | 101,7 | 4.5:1 |
| claro: texto secundario sobre superficie base | 12,47:1 | 95,7 | 4.5:1 |
| claro: texto tenue sobre superficie base | 6,49:1 | 79,9 | 3.0:1 |
| claro: acento sobre superficie base | 6,96:1 | 81,3 | 3.0:1 |
| claro: texto sobre acento | 6,96:1 | -85,8 | 4.5:1 · 14 px a 700 |
| claro: borde definido sobre superficie base | 3,19:1 | 57,5 | 3.0:1 |
| claro: texto inverso sobre superficie inversa | 18,04:1 | -103,3 | 4.5:1 |
| claro: texto del estado vigente | 6,96:1 | 81,3 | 4.5:1 |
| claro: borde del estado vigente | 3,19:1 | 56,7 | 3.0:1 |
| claro: texto del estado por-vencer | 6,97:1 | 81,6 | 4.5:1 |
| claro: borde del estado por-vencer | 3,22:1 | 57,4 | 3.0:1 |
| claro: texto del estado vencido | 5,46:1 | 68,6 | 4.5:1 |
| claro: borde del estado vencido | 3,19:1 | 57,5 | 3.0:1 |
| claro: texto del estado negado | 7,01:1 | 80,1 | 4.5:1 |
| claro: borde del estado negado | 3,2:1 | 56,7 | 3.0:1 |
| claro: texto del estado sin-confirmar | 9,53:1 | 89,6 | 4.5:1 |
| claro: borde del estado sin-confirmar | 3,19:1 | 57,5 | 3.0:1 |
| claro: texto del estado identidad | 7,02:1 | 81,6 | 4.5:1 |
| claro: borde del estado identidad | 3,21:1 | 57,4 | 3.0:1 |

El signo de Lc indica la polaridad: negativo es texto claro sobre fondo oscuro. El texto tenue (Lc 49) se limita a leyendas y metadatos de 14 px o más; no lleva información que el usuario necesite para actuar.

## Cambios desde la versión del 22 sep

| Qué | 22 sep | 23 sep | Por qué |
|---|---|---|---|
| Acento, tema oscuro | `biolum-d90` `#00D595` | `biolum-d70` `#00BB83` | Vuelve al de la entrega 2. Su texto (Lc 55,1) se resuelve con tamaño mínimo, no cambiando el color |
| Paleta | Regenerada (1/255 de diferencia) | Congelada en `legado/paleta-2026-09-19.json` | Lo que el equipo ya presentó es la paleta de registro |
| Tokens de conjunto | `kino-tenant-marca`, `kino-tenant-radio` | Eliminados | Kino es la marca; el conjunto es un dato |
| Movimiento | 3 curvas | 17 tokens (`40-movimiento.md`) | Sistema de movimiento v2 |

## Herramientas activadas

| Pieza | Herramienta | Resultado |
|---|---|---|
| Paleta por contraste | `paleta.mjs` (color.js) + **Adobe Leonardo** 1.1 real | 98 pasos comparados: ΔE OK medio 0,019, máximo 0,14. Las diferencias mayores están en los pasos extremos de `biolum` y `ambar` (`d90`–`d110`, `l15`), donde el croma choca con el borde del gamut sRGB y cada motor recorta distinto |
| Contraste | `contraste.mjs` + **apca-w3** (`fontLookupAPCA`) | 38 de 38 pasan; tamaño mínimo para texto sobre acento |
| Tipografía fluida | **utopia-core** | 360 → 1440 px, 16/1,2 → 18/1,26 |
| Tokens | DTCG 2025.10 + validador de **dgtlntv** (skill de W3C Design Tokens) | 6 de 6 archivos válidos |
| Build de tokens | **Terrazzo** | Corre desde la Terminal del Mac (`npm run terrazzo`): sus binarios nativos son de macOS |
| Evaluación de voz | **promptfoo** | Desde la Terminal del Mac (`npm run evals:promptfoo`, requiere `ANTHROPIC_API_KEY`) |
| Iconos | **Iconoir** 7 (MIT) | 9 iconos del recorrido |
| Movimiento | Motor de Motion Playground (`window.__motion`) + `kino-movimiento.js` | Los tokens se registran en el motor; WAAPI solo sobre transform, opacity y filter |

## Lo que falta por verificar

1. La licencia de Arkit ExtraBold, la familia del logotipo. Mientras no se confirme, las letras viven solo como contornos.
2. El archivo vectorial original del logo, si existe. La reconstrucción coincide 98 % (IoU), pero no es la fuente.
3. Cómo se ve la paleta en las pantallas de portería de HikCentral.
4. Si la administración de Monte Sereno tiene alguna restricción de marca que no esté en los archivos.
5. Las corridas de Terrazzo y promptfoo en el Mac, para dejar su salida en `reportes/`.
