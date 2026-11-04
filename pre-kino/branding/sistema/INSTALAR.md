# Instalar

**Esto se ejecuta en Terminal.app, no en el shell de Cowork.** El entorno donde trabaja el agente no tiene salida a internet: recibe `403` de la política de egreso al llegar a `registry.npmjs.org`, `cdn.jsdelivr.net`, `raw.githubusercontent.com` y `fonts.googleapis.com`. Tu terminal normal no pasa por ese proxy. `instalar.sh` lo comprueba antes de hacer nada y se detiene si está del lado equivocado.

```bash
cd ~/Library/Mobile\ Documents/com~apple~CloudDocs/Documents/montesereno/projects/kino/branding/sistema
bash instalar.sh
```

## Los tres scripts

| Script | Qué hace | Pide algo |
|---|---|---|
| `instalar.sh` | Requisitos, dependencias, construcción de tokens, verificación de contraste e iconos | No |
| `instalar-fuentes.sh` | Autoaloja Archivo y JetBrains Mono, y reescribe el `@import` | No |
| `instalar-figma-mcp.sh` | Registra los MCP de Figma en Claude Code | El token de Figma |

Córrelos en ese orden y por separado. Los dos últimos son opcionales.

### Qué hace `instalar.sh`, paso por paso

1. **Requisitos.** Node 20 o superior (Style Dictionary 5 no corre por debajo), npm, python3, y salida real a npm. Si algo falta, se detiene y dice cómo instalarlo.
2. **Dependencias.** `style-dictionary`, `colorjs.io` e `iconoir`, los tres en `@latest`. No fijo versiones porque no las pude confirmar sin red: el script instala, resuelve y **escribe en `versiones.txt` lo que quedó**.
3. **Compatibilidad.** Dos comprobaciones que evitan un fallo silencioso:
   - `construir-tokens.mjs` está escrito para la API de Style Dictionary 5 (ESM, `registerTransform` con `transform`). Si npm resuelve una 3 o una 4, el build saldría mal sin avisar. El script corta y dice qué habría que cambiar.
   - color.js se prueba contra valores conocidos —blanco sobre negro debe dar 21:1 y Lc 106— antes de confiar en sus cifras. Si su API cambió, corta.
4. **Construcción.** Guarda el `kino-brand.css` actual como `.antes`, reconstruye desde los tokens y compara los nombres de variable de una versión a la otra. Si cambian, avisa con el `diff` exacto que hay que mirar.
5. **Contraste.** 19 pares en dos temas. Sale con código 1 si alguno falla, así que sirve tal cual como paso de CI.
6. **Iconos.** Encuentra la carpeta de SVG dentro de `node_modules/iconoir` en vez de adivinar la ruta, y copia diez a `iconos/`.

## De las diez herramientas, cuáles hacen falta

| Herramienta | ¿Necesaria? | Por qué |
|---|---|---|
| **Style Dictionary** | Sí, es el eje | Convierte `tokens/*.json` en el CSS que consumen deck, documentos y app. Sin esto cada superficie copia valores a mano |
| **color.js** | Sí | Verifica los contrastes en cada build. Es el paso que impide que un cambio de color rompa la accesibilidad sin que nadie se entere |
| **Iconoir** | Sí | Es el set elegido y hoy no está en el sistema |
| **Figma Console MCP** | Sí, si trabajan en Figma | Extrae contexto real en vez de transcribir specs a mano |
| **Claude Talk to Figma** | Opcional | Añade escritura sobre el canvas y funciona con cuentas gratuitas |
| **Adobe Leonardo** | Una sola vez | La paleta ya está generada con el mismo algoritmo. Sirve para contrastar valores, no para el día a día |
| **Fluid Type Scale Calculator** | No se instala | Es una web. La escala ya está en `typescale.json` |
| **Design Tokens (plugin de Figma)** | Solo si los tokens nacen en Figma | Hoy nacen en código. Instálalo el día que se invierta esa dirección |
| **Open Props** | No | Aporta escalas base; las de Kino son pocas y derivadas. Duplica vocabulario |
| **Radix Colors** | No | Entrega escalas listas; las de Kino heredan los matices de la Propuesta 1 |

## Leonardo, si quieren contrastar la paleta

```bash
npm install --no-save @adobe/leonardo-contrast-colors
```

El motor propio (`motor/color.py`) implementa su misma idea: búsqueda binaria sobre la luminosidad en OKLCh hasta alcanzar el contraste objetivo, con recorte de chroma al gamut sRGB. Lo esperable es que coincidan salvo redondeo. Si no coinciden, gana Leonardo y hay que regenerar con `npm run paleta`.

## El token de Figma

`instalar-figma-mcp.sh` lo pide por teclado, no lo muestra en pantalla y no lo escribe en ningún archivo del repositorio: queda solo en la configuración de usuario de Claude Code. Créalo en Settings → Security → Personal access tokens, con lectura en contenido de archivo, versiones, variables y comentarios.

## Qué está probado y qué no

| | Estado |
|---|---|
| Paleta, contrastes y escala tipográfica | Verificados: 36 pares, 0 fallos, con el motor propio |
| Cadena de Python (`npm run paleta`) | Corre de punta a punta desde esta carpeta |
| Vectorización del logo | Verificada por rasterización contra el PNG: 98 % de coincidencia |
| `tokens/*.json` como fuente DTCG | Estructura correcta, referencias resueltas, sin literales sueltos en la capa semántica |
| `instalar.sh` pasos 1 a 6 | **Ejecutados** en tu máquina el 19 sep. 0 fallos |
| `instalar-fuentes.sh` | **Ejecutado.** 12 archivos woff2 en `fonts/`, con los ejes variables intactos (`font-stretch: 62% 125%`, `font-weight: 100 900`). Cero referencias remotas |
| `instalar-figma-mcp.sh` | **Sin ejecutar.** Solo sintaxis (`bash -n`) |
| Versiones de npm | Resueltas: style-dictionary 5.5.4, colorjs.io 0.7.1, iconoir 7.12.1. Ver `versiones.txt` |
| Comandos de los MCP de Figma | Copiados de los README de cada repositorio, sin probar |

Las dos pasadas encontraron cuatro defectos, los cuatro de la implementación y ya corregidos:

1. El orden de argumentos de `contrast()` en color.js: el receptor es el fondo, y APCA no es simétrico.
2. Style Dictionary 5 no acepta `source` por plataforma, así que los archivos de tema no se cargaban.
3. `capa-componentes.css` referenciaba sombras que ningún token definía.
4. `ensamblar.mjs` dejaba el `@import` de las tipografías en mitad del archivo, donde el navegador lo descarta. Las fuentes nunca habían cargado.

Los defectos 3 y 4 comparten la misma forma: no rompen nada, no fallan ningún test y degradan en silencio. Por eso ahora `npm run verificar` incluye `verificar-css.mjs`.
