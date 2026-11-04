# Escenas 3D de Kino (Blender, bpy)

Los tres recursos `blender` del inventario de motion, construidos solo por código: no hay assets descargados. La
única fuente externa es JetBrains Mono, que se toma de `branding/sistema/fonts` y se convierte a TTF.

| Recurso | Tamaño | Frames (60 fps) | Fondo | Salida |
|---|---|---|---|---|
| `pase-3d-objeto` | 1920 × 1080 | 5 clips: aparecer 1–50, confirmar 60–109, latir 120–228, caducar 240–294, revocar 300–314 | transparente | `render/pase-3d-objeto/<clip>/`, `glb/` |
| `pase-3d-latir` | 1080 × 1080 | 1–109, en loop: el 109 es igual al 1 | transparente | `render/pase-3d-latir/` |
| `conjunto-noche-lector-confirma` | 1920 × 1080 | 1–50 | opaco | `render/conjunto-noche-lector-confirma/` |

Cada recurso tiene su variante `.reducido`. El render es una secuencia PNG RGBA hecha con EEVEE. La codificación a
ProRes 4444, HEVC y VP9 la hace el pipeline.

```bash
# bpy 4.2 como módulo (Python 3.11). EEVEE sin GPU necesita EGL de Mesa:
#   apt-get install libegl1 libgl1-mesa-dri libegl-mesa0 libgles2
python3.11 -m venv .venv && .venv/bin/pip install bpy==4.2.0 fonttools brotli
for e in escena modelado materiales animacion verificacion render exportar; do
  .venv/bin/python construir.py pase-3d-objeto $e            # y --reducido
done
# Draco: el exportador glTF del módulo bpy no trae la librería. Se comprime después:
npx @gltf-transform/cli@4 draco glb/pase-3d-objeto.sin-draco.glb glb/pase-3d-objeto.glb
```

## Cómo se cumple el sistema

- **Tokens:** duraciones, curvas, distancia y colores salen de `../tokens.motion.json`. Aquí no hay milisegundos,
  curvas ni hex escritos a mano.
- **Color:** el hex del token se pasa a lineal. Con `view_transform = Standard` las marcas planas (emisión 1) salen
  con su hex exacto.
- **Easing:** cada tramo es un par de claves con handles bezier libres, en las proporciones exactas del cubic-bezier
  del token. Verificado: la opacidad en el frame 25 de «aparecer» vale 0,9371 en Blender y en el `cubic-bezier`
  de `curva/crecer`.
- **Escala:** 1 px = 0,01 u. La tarjeta mide 3,6 × 1,32; `distancia/subida` equivale a 0,26 u. Esto responde la
  pregunta 10 del inventario.
- **Estado honesto:** el Pase entra en «sin confirmar». El borde continuo, el punto verde, la barra y el brillo solo
  aparecen desde el clip «confirmar».

## GLB (solo `pase-3d-objeto`, interactivo en web)

- `glb/pase-3d-objeto.glb` (Draco) lleva las transformaciones: la subida del `root`, la escala de la `barra` y la del
  `corte`.
- glTF no anima materiales. Cada pieza lleva su token en `extras.kino_token`, y `glb/pase-3d-objeto.clips.json` da,
  por clip, el rango, el estado inicial y final, la duración y la curva por nombre de token. También da las piezas
  visibles y los colores de cada estado. El visor aplica fundidos y colores con esos tokens.
- Movimiento reducido en el visor: con `prefers-reduced-motion`, no reproduce las transformaciones (subida, escala) y
  aplica solo los fundidos. El latido queda como punto fijo.

## Desviaciones de la spec

| Punto | Qué se hizo | Motivo |
|---|---|---|
| Rig | Sin armature. Solo un Empty `root`, que es el control de la subida y de la opacidad | Nada se deforma. Los nombres pedidos (spine, head, arm…) son de personaje y la marca prohíbe personas y personajes |
| Membrana translúcida | La tarjeta es opaca y solo funde al aparecer (tramado) | Si es translúcida, EEVEE ordena por origen de objeto y la tarjeta tapa la barra y el punto |
| Emisión del indicador de noche | Fuerza 1 | Con más fuerza, el verde vigente satura hacia el cian, que la marca prohíbe |
| Variante reducida de la noche | Igual a la completa | La ficha la define así: el cambio es de color, sin desplazamiento |
| `pase-3d-objeto`, clip latir reducido | Un solo frame (120) | El latido se detiene; el punto queda fijo |
| Herramientas | `execute_blender_code` y `render_thumbnail_to_path` no existen en la sesión | Se reemplazaron por `construir.py` (una etapa por proceso) y la etapa `verificacion` (miniaturas al 50 %) |
