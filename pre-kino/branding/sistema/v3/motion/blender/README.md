# Escenas 3D de Kino (Blender, bpy) · versión 2

Decisiones M3D-1 a M3D-7 aprobadas (Nico, 27 sep: opción A). La versión 1 está en `_obsoleto/v1-2026-09-26/` y sus videos en
`../entregables/_obsoleto/v1-2026-09-26/`.

Todo se construye por código, sin assets descargados. Las únicas fuentes externas son Archivo y JetBrains Mono, que
se toman de `branding/sistema/fonts` y se convierten a TTF con el corte de la web (Archivo 700, JetBrains Mono 400).

| Recurso | Tamaño | Frames (60 fps) | Fondo |
|---|---|---|---|
| `pase-3d-objeto` | 1920 × 1080 | 7 clips: aparecer, confirmar, latir, avisar, caducar, usar, revocar (ver `pase.inicios()`) | transparente |
| `pase-3d-latir` | 1080 × 1080 | 1–109 en loop (el 109 es igual al 1) | transparente |
| `conjunto-noche-lector-confirma` | 1920 × 1080 | 1–260 | opaco |

```bash
# bpy 4.2 como módulo (Python 3.11). EEVEE sin GPU necesita EGL de Mesa:
#   apt-get install libegl1 libgl1-mesa-dri libegl-mesa0 libgles2
python3.11 -m venv .venv && .venv/bin/pip install bpy==4.2.0 fonttools brotli pillow
(cd ../../../../../paquetes/kino-motion && npm install && npm run build)
node partitura.mjs                 # tokens y partitura de @kino/motion → partitura.json
npm install                        # gltf-transform y draco para el GLB
./etapas.sh pase-3d-objeto escena modelado materiales animacion      # y --reducido
.venv/bin/python construir.py pase-3d-objeto verificacion            # miniaturas al 50 % (--frames=, --escala=)
.venv/bin/python construir.py pase-3d-objeto render                  # PNG RGBA; anota tiempos/<id>.json
.venv/bin/python construir.py pase-3d-objeto exportar                # GLB con variantes y Draco
.venv/bin/python medir.py render/…/0049.png estado/vigente/borde     # ¿sale el hex del token?
FFMPEG=… python3 ../codificar.py                                     # ProRes 4444, VP9/HEVC con alfa, H.264
```

## Fuentes de verdad

- **Motion:** `partitura.json` sale de `paquetes/kino-motion/dist/nucleo.js`: duraciones, curvas, resortes, escala de
  entrada, ciclos de latir y la partitura de cada transición (`TRANSICIONES`). El 3D anima las mismas partes con el
  mismo verbo que `<kino-pase>`. Aquí no hay milisegundos ni curvas escritos a mano.
- **Resortes:** `kino3d.Resorte` es la misma solución analítica de `src/nucleo/resorte.ts`. Verificado contra
  `tokens.json`: ζ y rebote coinciden (tacto 2,98 %, hoja 0,03 %, pase 1,11 %, firme 0 %). Se hornean una clave por
  frame.
- **Latir:** como en la web, `curva/latir` se aplica a la iteración entera y la opacidad sube y baja lineal sobre ese
  tiempo.
- **Color:** hex de token → lineal. Semánticos para estados y texto; primitivos (sustrato, hueso, índigo, violeta,
  biolum) para superficies de escena y luces. Sombra y resplandor son los tokens `relieve/membrana` y
  `resplandor/vigente` leídos del DTCG.

## Gestión de color (M3D-1 A, aprobada el 27 sep)

- Transformada de vista **Standard**, sin look. AgX o Filmic desaturan los verdes de estado y no dejan que un
  `#00EAA5` salga como `#00EAA5`.
- La compresión de luces la hace una **curva de tono propia en el compositor** (Reinhard extendido sobre la
  luminancia, con paso suave al blanco), aplicada a todo menos a las marcas de estado.
- Las marcas (bordes, chip, textos, barra, corte, indicador del lector) escriben la AOV `marca` y pasan sin curva.
  Resultado medido con `medir.py`: `estado/vigente/borde`, `estado/vigente/texto`, `estado/vigente/fondo` y
  `texto/primario` salen con ΔE 0 respecto a su hex.
- El brillo sale de la AOV `brillo`, que solo escriben las piezas activas (el punto que late, el indicador del lector
  confirmado). El resplandor del Pase es `resplandor/vigente` aplicado como `box-shadow` en el compositor y su fuerza
  vale 0 en cualquier estado que no sea vigente.

## Motor y costo

EEVEE Next en CPU (Mesa llvmpipe, 4 núcleos). Cycles con OpenImageDenoise se evaluó con la misma escena de prueba a
16 muestras: 41 s por frame contra 21 s de EEVEE con volumétrica, a calidad comparable. Se quedó EEVEE.

En el Pase se quitaron la profundidad de campo (20 s por frame, la tarjeta es casi plana) y el trazado de rayos en
pantalla (solo reflejaba un mundo oscuro), y se renderiza solo la región del Pase (`use_border`, sin recorte).

## Desviaciones

| Punto | Qué se hizo | Motivo |
|---|---|---|
| Alfa 0 en EEVEE Next | Además del fundido, cada marca se oculta del render (`hide_render`) en los frames en que su opacidad efectiva es 0 | Una superficie tramada con alfa 0 deja glifos fantasma |
| Textos que cambian (M3D-5 A) | Fundido a través: el que sale se va en la primera mitad del verbo y el que entra llega en la segunda | En la web el texto cambia de golpe; en 3D, un fundido cruzado encima los dos |
| Chip | Un grupo por estado (fondo, borde, punto, texto) que se funde | El texto del chip cambia con el estado |
| Tarjeta (M3D-4 A) | Color base `superficie/membrana`, igual que la web desde el 27 sep | El recurso Membrana de la marca: «el fondo de todo lo que se toca»; la pista de la barra usa elevada para contrastar |
| Talanquera | `resorte/firme` (494 ms) | Llega sin pasarse; no hay token de mecánica. Aprobada (M3D-2 A, 27 sep) |
| Llegada de la cámara | `duracion/cortina` con `curva/crecer`; la salida dura el 60 % (`coreografia/salida-factor`) con `curva/salir` | No hay token de cámara. Aprobada (M3D-3 A, 27 sep) |
| Aurora de noche | Índigo y violeta, con apenas `biolum/d15` | El verde queda para lo activo (el indicador) |
| Rig | Sin armature: Empties y un SimpleDeform para la flexión del brazo | Nada se deforma como personaje; la marca prohíbe personajes |
