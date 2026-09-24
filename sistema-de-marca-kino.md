> **Documento histórico (23 sep 2026, tarde). No es la referencia vigente.** Lo reemplazan `claude/traspaso-sistema-de-marca.md`, `claude/decisiones-sistema-de-marca.md` y `claude/avances-sistema-de-marca.md`, que mandan donde difieran. Se conserva por trazabilidad. Varias cosas de aquí ya cambiaron:
> - el tratamiento con la administración es usted;
> - el sitio muestra una sección a la vez, no láminas;
> - el texto sobre el acento se propone resolver con #00D595 y no con tamaño;
> - los estados del Pase son siete más el evento Rechazado;
> - la calibración de voz está en 40/42.

# Sistema de marca Kino — v2 (23 sep 2026)

Decisión de marca y dónde vive cada pieza. Reemplaza al tablero «Propuesta 1» como referencia operativa; la Propuesta 1 sigue siendo el origen del linaje, no la especificación.

**v2 (23 sep):** Kino deja de ser marca blanca; «pase» reemplaza a «permiso»; el acento vuelve a `#00BB83` con regla de tamaño APCA; la entrega 2 se toma como referencia (no como base); sistema de movimiento con 17 tokens y 5 verbos; deck de marca, manual v2 y librería de Figma. Detalle y enlaces en `claude/decisiones-marca-2026-09-23.md`, que manda sobre este archivo donde difieran.

**v1.1 (22 sep):** los tokens se construyen con gorr-brand-system (ver «La cadena») y el perfil de tono quedó aprobado.

## Decisiones del equipo

Tomadas por Nico y Alejandro, sin pasar por Manuel: **la marca es decisión del equipo**; Manuel aprueba producto y negocio.

1. **Dirección: biopunk, y manda sobre la Propuesta 1.** El logo se conserva y se recolorea; paleta y tipografía se replantean desde esa estética. (23 sep) La referencia más avanzada de esa dirección es la entrega 2 (aurora, cortina, crecer y decaer, boleto con talón); es punto de partida, no canon. La marca está en etapa de fundamentos.
2. **El tema canónico es el oscuro.** El claro («Laboratorio») es el segundo.
3. **El color solo nombra hechos confirmados.** Es la traducción visual de P15 (estados honestos): lo que el lector no confirmó se dibuja `sin-confirmar`, sin relleno y con borde discontinuo.
4. **(23 sep) Kino es la marca; el conjunto es un dato.** Se eliminó la capa tenant (`kino-tenant-marca`, `kino-tenant-radio`). Los seis estados son idénticos en todos los conjuntos, o la traza deja de ser comparable.
5. **(23 sep) Aire mínimo de la marca = ancho del arco interior** (0,63 × el ancho del bloque), también para los bloqueos, medido desde el bloque.
6. **(22 sep, ajustado 23 sep) Texto legible también según APCA.** `vencido` se exige con Lc ≥ 60. El texto sobre el acento `#00BB83` (Lc 55,1) se exige con tamaño mínimo: 18 px en 700, 21 px en 600.
7. **(22 sep) Perfil de tono aprobado** (NN/g): formalidad 2, humor 1, respeto 1, entusiasmo 2. Vive en `gorr-brand-system/clientes/kino/voz.json`.
8. **(22 sep) Se adopta gorr-brand-system** como cadena de construcción de la marca.
9. **(23 sep) «Pase»** es el objeto que recibe el invitado o colaborador; «cuenta» es del residente.
10. **(23 sep) El acento significa otorgar.** Solo el botón que da el pase, el boleto recién emitido y la marca.

## La tesis, anclada al diagnóstico

Kino es una **membrana**, no un muro. Cada decisión visual responde a un hallazgo de `claude/diagnostico-consolidado-v1.md`:

| Decisión visual | Hallazgo |
|---|---|
| Estados con vida (`vigente` late, `por-vencer` avisa, `vencido` se apaga) | H1 y H5: no existe pase temporal; el invitado es miembro permanente sin vigencia |
| `sin-confirmar` sin relleno, borde discontinuo | H3 y H6: una placa inventada queda «Permitido»; 0 de 312 sincronizados en Refugio |
| Componente `Pase` idéntico para residente y portero; datos personales truncados y marcados `identidad` | H8: simetría invertida |
| Familia `identidad` (violeta) para cédula, rostro y teléfono | R4 y la Res. 52185 de 2025 de la SIC |
| Monoespaciada con cero barrado y cifras tabulares para placas y códigos | El lector compara lo que ve con lo que escribió una persona |
| Arco abierto, sin candados ni escudos | El problema no es un cuello de botella, es ausencia de gobierno |
| Caducar lento, revocar seco (movimiento) | Vencer y cortar son hechos distintos y la traza debe distinguirlos |

## Linaje de la paleta

| Propuesta 1 | Pasa a ser | Significa |
|---|---|---|
| Carbón `#2C2D2F` | `sustrato` (sesgo verde) | Superficies |
| Menta `#B2E8DB` | `biolum` (chroma al límite del gamut) | Vigente, acción de otorgar |
| Morado `#7266CA` (intacto) | `identidad` | Dato personal o biométrico |
| Índigo `#00177D` | `indigo` | Profundidad, aurora |
| Hueso `#E1E8EE` (enfriado) | `hueso` | Tema claro |
| — | `ambar` (nueva) | Vigencia que se agota |
| — | `carmin` (nueva) | Rechazo |

La paleta de registro está congelada, por ahora, en los valores de la entrega 2 (`legado/paleta-2026-09-19.json`). Tipografía: **Archivo** (display y texto, eje de ancho 62–125) y **JetBrains Mono** (datos), ambas OFL 1.1. Arkit ExtraBold queda solo dentro de los contornos del logotipo.

## Dónde está cada cosa

- **Deck de marca (v2)**: «Kino Sistema de Marca» — https://claude.ai/artifact/K8R2PRduS6SHBKYU31Bo6L, copia en `kino/Kino_Sistema_de_marca_2026-09-23.html`. 28 láminas con el motor de movimiento.
- **Manual navegable (v2)**: artefacto «Kino» (Design System) — https://claude.ai/artifact/224KDZ6KbmV8PFeXG2BbPD, versión 11. Diez componentes y cinco guías (README, membrana, aplicación, verificación, movimiento).
- **Librería Figma**: «Kino — Sistema de marca v2» — https://www.figma.com/design/BO7UnDO9iE0aG6yUpNj0bc (equipo de Alejandro).
- **Implementación v2**: `kino/branding/sistema/v2/kino-sistema.css` y `kino-movimiento.js`.
- **Deck de diagnóstico**: https://claude.ai/artifact/VArWzzsnrcFFQrjCtRDFeZ (marca v1 aplicada).
- **Fuente de la marca**: `kino/gorr-brand-system/clientes/kino/` (`marca.config.json`, `voz.json`, `pares.json`, `tokens/` en DTCG 2025.10, la skill `kino-marca` y las evals de voz).
- **Capa v1**: `kino/branding/sistema/` (`kino-brand.css`, SVG de marca, tipografías, iconos).

Los artefactos son privados hasta que se compartan desde el menú Share de cada página.

## La cadena, y cómo se corre

```
gorr-brand-system/clientes/kino
  marca.config.json ─► paleta (congelada) · tipo ─► tokens/ (DTCG 2025.10) ─► validar ─► construir ─► contraste ─► voz ─► skill + evals
```

```bash
cd kino/branding/sistema
npm run construir          # cadena completa + 38 pares
cd ../../gorr-brand-system
npm run terrazzo           # solo en la Terminal del Mac (binarios de macOS)
npm run evals:promptfoo    # solo en el Mac, requiere ANTHROPIC_API_KEY
```

- La capa semántica es **referencia**, no valor: un literal hace fallar `validar`.
- Contraste: WCAG 2.2 obligatorio, APCA (apca-w3) como informe y tamaño mínimo con `fontLookupAPCA`.
- Herramientas activadas el 23 sep: Terrazzo, Leonardo, apca-w3, utopia-core, promptfoo, colorjs, iconoir, validador DTCG de dgtlntv. Versiones en `gorr-brand-system/versiones-herramientas.txt`.

## Verificación (23 sep)

38 pares, 0 fallos WCAG 2.2. Leonardo reproduce la paleta con ΔE OK medio 0,019 (máx. 0,14 en pasos extremos de `biolum` y `ambar`). 6 de 6 archivos DTCG válidos. Deck sin errores de página ni desborde horizontal a 390, 1024 y 1440 px. Logo vectorizado con 98 % de coincidencia (IoU) contra el PNG original.

## Lo que falta

1. La licencia de Arkit ExtraBold.
2. El archivo vectorial original del logo, si existe.
3. Correr Terrazzo y promptfoo en el Mac y guardar la salida en `reportes/`.
4. Actualizar las instrucciones del proyecto (reglas 5 y 6, vocabulario «permiso» → «pase»): solo el equipo puede editarlas.
5. Las plantillas de documento.
6. Decidir la unidad de los cupos (por casa, por residente o por conjunto): decisión de producto.
7. Ver la paleta en las pantallas de portería de HikCentral.
