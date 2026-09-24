# {{nombre}} · Identidad visual

Fase 3. Lo que las herramientas generan (color, escala tipográfica, espacio) está en `../marca.config.json`. Lo que decide un diseñador (logo, familias tipográficas, iconografía, imagen) se registra aquí, **cada decisión con el problema que resuelve**.

## Tabla de decisiones
| Decisión visual | Problema o fila del posicionamiento que responde |
|---|---|
| | |

Si una decisión no tiene fila, es estética, no de marca: se revisa o se quita.

## Logo
- Archivos en `logo/`: SVG con `fill="currentColor"` (marca, logotipo, bloqueos horizontal y vertical) + PNG de respaldo.
- Área de protección y tamaño mínimo:
- Usos incorrectos (máximo cinco, con imagen):
- Licencia de la tipografía del logotipo:
- Si se vectoriza desde un PNG: comparar por rasterización contra el original y anotar el % de coincidencia.

## Color
Generado por `npm run paleta`. Aquí solo se decide:
- Matiz y croma de cada familia (`h`, `cmax` o `semilla`) y su `porque` en `marca.config.json`.
- Qué significa cada familia. Una familia no se usa fuera de su significado.
- Objetivos de contraste (por defecto 1.5 → 11:1).

Si el cliente necesita una escala lista rápido, Radix Colors (MIT) es una alternativa; para contrastar con Adobe Leonardo, usar `reportes/leonardo-entrada.json` en leonardocolor.io.

## Tipografía
- Familias (`tipo.familias`), con licencia verificada. Preferir fuentes OFL autoalojadas: sin dependencia de Google Fonts en tiempo de ejecución.
- Escala: Utopia (`tipo.min`, `tipo.max`, `vwMin`, `vwMax`). Ajustar en utopia.fyi/type/calculator y copiar los parámetros.
- Datos (cifras, códigos, fechas): monoespaciada o cifras tabulares.

## Iconografía
Librería elegida (licencia) y reglas de trazo y tamaño.

## Imagen y composición
Fotografía, ilustración, retícula. Solo lo que el cliente va a producir de verdad.

## Compuerta de salida
- [ ] Cada fila de la tabla de decisiones tiene problema asociado.
- [ ] `npm run contraste -- {{id}}`: 0 fallos WCAG 2.2 en todos los temas.
- [ ] Pares bajo Lc 60 en texto de cuerpo: revisados y justificados.
- [ ] Licencias de fuentes, iconos e imágenes anotadas.
