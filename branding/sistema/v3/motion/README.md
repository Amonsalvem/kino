# Motion de Kino · fuentes de los recursos animados

Fuentes de los recursos de técnica `lottie` y `remotion` del inventario de motion (26 sep). Las escenas de Blender
no están aquí: este encargo no traía instrucciones para esa técnica.

Regla que se cumple en todo el directorio: **no hay milisegundos, curvas ni colores escritos a mano.** Todo sale de
`gorr-brand-system/clientes/kino/tokens` (DTCG) a través de `tokens.py`.

```bash
# 1. Tokens → frames a 60 fps, curvas y colores (escribe tokens.motion.json)
python3 tokens.py

# 2. Lottie JSON fuente (escribe lottie/fuente, lottie/temas, lottie/manifiesto.json, lottie/texto-visible.md)
python3 lottie/generar.py

# 3. Remotion (Node 20+)
cd remotion && npm install
npm run tipos
npm run estudio                         # revisar en el navegador
KINO_CHROMIUM=/ruta/headless_shell npm run previews   # mp4_preview (H.264) de cada Lottie
KINO_CHROMIUM=/ruta/headless_shell npm run masters    # ProRes 4444 con alfa + póster PNG
# Filtrar: node render-previews.mjs pase-latir   ·   node render-masters.mjs hero
```

En la nube, `KINO_CHROMIUM=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`, porque
Remotion no puede descargar su navegador (remotion.media no está en la lista de hosts permitidos).

## Qué hay

| Ruta | Qué es |
|---|---|
| `tokens.py`, `tokens.motion.json` | Tokens resueltos, temas oscuro y claro. Frames: corto 14, crecer 25, tarjeta 49, decaer 54, trazo 57, cortina 96, latir 108; escalonado de tarjetas 5, de filas 3 |
| `lottie/generar.py` | Genera los 16 recursos Lottie, cada uno completo y reducido |
| `lottie/fuente/<id>.json`, `<id>.reducido.json` | Lottie JSON fuente. El pipeline los empaqueta a `.lottie` |
| `lottie/temas/oscuro.json`, `claro.json` | Temas dotLottie: una regla `Color` por slot |
| `lottie/manifiesto.json` | Por archivo: fps, `op`, tamaño, loop, slots de color y de texto. Recursos bloqueados |
| `remotion/src/Hero.tsx` | `hero-ciclo-del-pase` (1920 × 1080) y `-movil` (1080 × 1350) |
| `remotion/src/Composiciones.tsx` | `composicion-revocado`, `composicion-turno-porteria` |
| `remotion/src/VistaLottie.tsx` | Wrapper `@remotion/lottie` de cada mp4_preview (`vista-<id>`) |
| `remotion/render-*.mjs` | Render de previews y maestros. La salida va a `remotion/salida/` (ignorada por git) |

## Slots de tema

- Cada color es una propiedad con `sid` y una entrada en `slots`. El id es el token semántico con guiones:
  `estado/vigente/borde` → `estado-vigente-borde`. Hay 30 slots de color en total.
- Lottie ignora el alfa del color de relleno. Por eso el relleno de `estado/sin-confirmar/fondo`, que es transparente,
  no se dibuja: no hay relleno ni slot.
- Los cambios de estado son un fundido cruzado entre dos capas con colores fijos, no una animación de color. Así
  cada color sigue siendo un slot que el tema puede cambiar.
- Los textos son slots de texto (`texto-<id>-<n>`); su color va dentro del documento de texto. Para cambiar un
  nombre, una casa o una hora no se toca la animación.
- **Pendiente de verificar en el pipeline:** el formato de las reglas de tema (`{"rules":[{"id","type":"Color","value"}]}`)
  contra la versión de dotLottie que se use. Las fuentes (Archivo, JetBrains Mono) deben empaquetarse desde
  `branding/sistema/fonts`, porque ThorVG no descarga las fuentes que declara el JSON.

## Decisiones de implementación que cambian el inventario

| Tema | Qué se hizo | Por qué |
|---|---|---|
| Frame final | Las piezas que no van en loop tienen `op` = duración + 1 | En Lottie, `op` es exclusivo: sin ese frame, el último valor de la clave no se ve. En Remotion, `revocado` y `turno` duran total + 1 |
| Alto del lienzo | `pase-aparecer`, `pase-cascada` y `entrada-rechazar` suman `distancia/subida` abajo (158, 584 y 122 px de alto) | Lo que entra subiendo no se recorta. El 0,0 de la pieza sigue arriba |
| Nombres de color | `acento/biolum/accion` → `accion/fondo`; `acento/biolum/fuerte` → `accion/fondo-activo`; `acento/biolum/brillo` → `estado/vigente/texto` (mismo hex) | Son los nombres reales de la colección semántica; resuelve la pregunta 12 del inventario |
| Pausas | Un ciclo de `duracion/latir`: espera y pausa del hero, separación entre lecturas del turno y reposo antes y después de cada mp4_preview | No hay token de pausa (pregunta 8 del inventario, sigue abierta) |
| Latido del hero | Dos ciclos | Se decide cuando se responda la pregunta 2 (bucle o máximo tres ciclos) |
| Contador de sincronización | Cambia cuando cada fila termina su confirmación | Una fila solo es vigente al final de `confirmar` |

## Bloqueos (spec contradictoria)

| Recurso | Contradicción |
|---|---|
| `flujo-trazo`, `loader-espera-lector`, `onboarding-3-lector-confirma` | Resuelto el 26 sep: Nico pidió `curva/crecer` para `trazo` |
| `control-presionar`, desplazamiento | «Baja levemente» no tiene token de magnitud. Se entrega solo el cambio de `accion/fondo` a `accion/fondo-activo`; la app lo reproduce hacia adelante al tocar y en reversa al soltar |

## Verificación (26 sep)

- `npm run tipos` sin errores.
- Fotogramas revisados a ojo: hero en cada tramo (la capa vigente vale 0 antes de `confirmar`), confirmar, cascada,
  enviar, revocar, usar, rechazar, loader de sincronización, vacío y cortina.
- Render de punta a punta: `composicion-revocado` en ProRes 4444 (perfil 4, `yuva444p12le`, 60 fps, 197 frames) con
  póster; `pase-confirmar` en H.264.
- Compuerta de voz sobre el texto visible: 0 hallazgos.
