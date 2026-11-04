# Piloto Kino · gorr-brand-system (22 sep 2026)

Kino es el primer cliente que pasa por la cadena completa. **Adoptado el 22 sep 2026:** `kino/branding/sistema/` ya construye sus tokens con esta cadena (ver «Adopción» abajo). La fuente de verdad de la marca Kino es ahora esta carpeta.

## Resultado

`npm run ciclo -- kino`: las 9 etapas pasan.

| Fase | Etapa | Resultado |
|---|---|---|
| 3 | paleta | 118 colores: los 100 de Kino, 14 del objetivo 9:1 agregado y 4 fijos. Reproduce el motor Python de Kino: de los 100 comunes, 42 idénticos y 58 con 1/255 de diferencia en un canal (redondeo). |
| 3 | tipo | 8 pasos, `clamp()` idénticos a `typescale.json` de Kino. |
| 4 | validar | 169 tokens por tema, 0 errores, 1 aviso (`radio.arco`). |
| 4 | contraste | 38 pares, 0 fallos WCAG 2.2. Los dos pares que quedaban bajo Lc 60 se corrigieron y ahora se exigen con `apcaMin: 60`. |
| 2 | voz | Texto visible final del deck del 22 sep: 0 errores. |
| 2 | calibrar-voz | 21 de 42 frases del barrido de muletillas atrapadas, 0 falsos positivos. |
| 5 | skill | `skill/kino-marca/SKILL.md` generada desde las fuentes. |
| 5 | evals | Corridas con subagentes (redactor y juez separados): **12 de 15 (80 %)** en la tercera ronda. Ver `evals/INFORME-2026-09-22.md`. |

## Hallazgos que el sistema de Kino no había detectado

### 1. Literales en la capa semántica (corregido en el piloto)
`sistema-de-marca-kino.md` dice: «Un hex suelto en `tokens/tema/` es un error de revisión». Había cinco, y ninguna de las dos verificaciones de Kino los detecta:

| Token | Tema | Literal | Ahora |
|---|---|---|---|
| `semantico.superficie.elevada` | claro | `#FFFFFF` | `{primitivo.color.fijo.blanco}` |
| `semantico.estado.sin-confirmar.fondo` | ambos | `#00000000` | `{primitivo.color.fijo.transparente}` |
| `semantico.relieve.membrana` (sombra) | oscuro | `#000000` | `{primitivo.color.fijo.negro}` |
| `semantico.relieve.membrana` (sombra) | claro | `#ffffff`, `#0b201a` | `fijo.blanco`, `fijo.sombra-claro` |

`#0B201A` no existe en ninguna escala: es un color que solo vive en esa sombra. Queda como `fijo.sombra-claro` para no cambiar el aspecto; vale la pena decidir si debería ser un paso de `sustrato`.

### 2. Dos textos que pasan WCAG 2 y se leen flojo según APCA (corregido)
| Tema | Par | WCAG 2.2 | APCA |
|---|---|---|---|
| oscuro | texto del estado `vencido` sobre su fondo | 5,86:1 | Lc −47,7 |
| oscuro | texto sobre acento (botón que otorga un permiso) | 7,71:1 | Lc 55,5 |

APCA pide Lc 60 para texto de cuerpo. `vencido` se apaga a propósito (H1/H5), pero la regla 2 exige que el estado lleve palabra, y esa palabra tiene que leerse.

**Decisión del equipo (22 sep): subir un paso ambos.** Se agregó el objetivo 9:1 a la paleta (`d90`/`l90` en cada familia) y en el tema oscuro:

| Token | Antes | Ahora | WCAG | APCA |
|---|---|---|---|---|
| `acento.base` | `biolum.d70` | `biolum.d90` | 9,91:1 | Lc 67,3 |
| `estado.vencido.texto` | `sustrato.800` | `sustrato.d90` | 8,02:1 | Lc −62,9 |

El acento del tema oscuro queda un poco más claro. `borde.foco` sigue en `d70`.

> Nota del 24 sep: el 23 sep el equipo volvió el acento a `#00BB83` (biolum d70). La Parada 3 del sistema de marca propone usar `#00D595` (d90) solo en el botón Crear Pase. Ver `decisiones.md` X4.

### 3. Formatos anteriores a DTCG 2025.10
Los tokens de Kino usan el formato que acepta Style Dictionary (hex en cadena, `"16px"`, sombras como cadena CSS con alias incrustados, `clamp()` como dimensión). La migración a 2025.10 fue automática con `importar.mjs`. `radio.arco` (`999px 999px 4px 4px`) no tiene forma DTCG: queda como CSS crudo con aviso. Propuesta: componerlo en `capa-componentes.css` a partir de `radio.pleno` y `radio.s`.

## Identidad verbal
`voz.json` reúne:
- El vocabulario del proyecto: Pase ≠ cuenta, acceso previsto, colaboradores, el lector permite el ingreso.
- Las decisiones tomadas convertidas en términos prohibidos: contraseña, aprobación de ingreso, Arcana, seguridad total, todo queda registrado.
- Los patrones del barrido del 22 sep.
- La sección `hechos`, con lo que el producto hace y lo que todavía no está confirmado.

**Perfil de tono aprobado por el equipo el 22 sep:** formalidad 2, humor 1, respeto 1, entusiasmo 2.

## Adopción en kino/branding/sistema (22 sep)
- `construir-tokens.mjs` corre `ciclo.mjs kino` y copia `primitivos.css`, `tema-oscuro.css` y `tema-claro.css` a `build/`. `ensamblar.mjs` y `capa-componentes.css` no cambiaron.
- `npm run verificar` = `verificar-css.mjs` + `contraste.mjs` de esta cadena (38 pares, 0 fallos).
- **Paridad verificada** contra el build anterior:
  - Los 37 tokens semánticos de cada tema existen con el mismo nombre.
  - Ninguna variable desapareció. Las nuevas son las 14 `*-d90`/`*-l90` y las 4 `--kino-fijo-*`.
  - Cambios de valor: los dos que decidió el equipo, los literales que pasaron a alias y 60 primitivos con 1/255 de diferencia.
- `kino-brand.css`: 191 variables definidas, 0 huérfanas.
- Respaldo del sistema anterior (Style Dictionary, tokens en formato legado, `pares.json`, `verificar-contraste.mjs`) en `_obsoleto/style-dictionary-2026-09-22/`.
- Ningún deck enlaza `kino-brand.css`: los decks traen su propia capa de marca. La adopción no cambia ningún deck publicado.

### Riesgo encontrado: iCloud expulsa `node_modules`
La carpeta del proyecto vive en iCloud Drive con «Optimizar almacenamiento». iCloud había dejado los archivos de `colorjs.io` en `branding/sistema/node_modules` solo en la nube, así que `verificar-contraste.mjs` fallaba con `Resource deadlock avoided`, sin que nadie hubiera cambiado nada. Por eso la verificación pasó a la copia de colorjs.io que trae `gorr-brand-system`. Arreglo de fondo, recomendado: sacar `node_modules` de iCloud renombrándolo a `node_modules.nosync` con un enlace simbólico, o mover los repos fuera de iCloud Drive.

## Qué falta
1. **Decidir la unidad de los cupos** (por casa, por residente o por conjunto). Lo destapó la eval del caso 4; es una decisión de producto.
2. Correr las evals con promptfoo cuando haya red, idealmente con un juez de otro proveedor.
3. Terrazzo y Adobe Leonardo real: bloqueados por la política de red (npm y leonardocolor.io devuelven 403 o no conectan, en la nube y en el Mac). `reportes/leonardo-entrada.json` y `terrazzo.config.mjs` quedan listos.
4. `radio.arco`: sigue como CSS crudo. Se puede componer en `capa-componentes.css`.
5. `fijo.sombra-claro` (`#0B201A`): se mantiene; revisar si debe ser un paso de `sustrato`.
