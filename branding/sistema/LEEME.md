# Sistema de marca Kino — capa aplicable

> **Desde el 22 sep 2026 los tokens se construyen con `gorr-brand-system`.** La fuente de verdad es `../../gorr-brand-system/clientes/kino/` (`marca.config.json`, `voz.json`, `tokens/` en DTCG 2025.10). `npm run construir` corre esa cadena, copia el CSS a `build/`, ensambla `kino-brand.css` y verifica variables y los 38 pares de contraste. Lo que se describe abajo sobre Style Dictionary, `tokens/`, `motor/` y `verificar-contraste.mjs` es el sistema anterior, respaldado en `_obsoleto/style-dictionary-2026-09-22/`. Detalle en `gorr-brand-system/clientes/kino/PILOTO.md`.


Los archivos que hacen que el deck, los documentos y la app hereden la marca sin copiar y pegar valores. El manual navegable vive como artefacto en Claude; esto es lo que se consume desde el código.

Para instalar las herramientas: **`INSTALAR.md`**.

## La cadena

```
motor/*.py  ──►  tokens/*.json  ──►  build/*.css  ──►  kino-brand.css
  Python          fuente DTCG       Style Dictionary    lo que se enlaza
```

El color se genera una vez en Python y se congela en `tokens/`. De ahí en adelante manda Style Dictionary. Solo hay que volver a Python si cambia un matiz de la paleta o un objetivo de contraste.

```bash
npm install
npm run construir     # compila los tokens y verifica los contrastes
npm run paleta        # solo si cambia la paleta: regenera tokens/ desde el motor
```

## Qué hay aquí

| Archivo | Qué es |
|---|---|
| `tokens/primitivo.json` | Las escalas generadas, con valor. 100 colores, espacio, radio, escala tipográfica y familias. |
| `tokens/tema/oscuro.json`, `tema/claro.json` | La capa semántica. Cada token es una **referencia** a un primitivo, nunca un hex suelto: cambiar un matiz cambia los dos temas a la vez. |
| `construir-tokens.mjs` | El build de Style Dictionary: un nombre `--kino-*` por token y **un build por tema**. Style Dictionary no acepta `source` por plataforma y los dos temas declaran los mismos nombres, así que no pueden compartir diccionario. |
| `capa-componentes.css` | Las clases `.kino-*` y lo que no es token: curvas de movimiento, eje variable de la tipografía y la capa tenant. Se edita a mano. |
| `ensamblar.mjs` | Une la salida de Style Dictionary con la capa de componentes en `kino-brand.css`, incluida la variante `prefers-color-scheme`. Sube los `@import` al principio: en CSS un `@import` fuera de la cabecera se descarta en silencio. |
| `verificar-contraste.mjs` | Recorre `pares.json` con color.js en los dos temas. Sale con código 1 si algo falla: sirve como paso de CI. |
| `verificar-css.mjs` | Busca variables `--kino-*` usadas y nunca definidas. Existe por un fallo real que no rompía nada y no fallaba ningún test. |
| `fonts/` | Archivo y JetBrains Mono autoalojadas (OFL 1.1), con sus `@font-face`. Sin dependencia de Google Fonts en tiempo de ejecución. |
| `iconos/` | Diez iconos de Iconoir para el recorrido del invitado. |
| `kino-brand.css` | El CSS ensamblado. Es lo que se enlaza en el deck y en la app. |
| `marca/*.svg` | Marca, logotipo, los dos bloqueos y la gota, con `fill="currentColor"`. |
| `palette.json`, `contraste.json`, `typescale.json` | Las escalas generadas, las 36 verificaciones y la escala fluida, con sus cifras. |
| `motor/*.py` | El generador de color: ciencia de color, paleta por contraste, capa semántica y salida DTCG. Sin dependencias externas. |

`kino-brand.css` lo produce Style Dictionary desde `tokens/`. La capa semántica sale por referencia, así que en el CSS un token semántico es `var(--kino-...)` y no un hex: cambiar un primitivo arrastra los dos temas y también las sombras.

## Cómo se usa en un deck o documento

```html
<link rel="stylesheet" href="kino-brand.css">
<body data-tema="oscuro">
  <h1 class="kino-display">La membrana</h1>
  <span class="kino-estado" data-estado="vigente">Vigente</span>
</body>
```

El tema oscuro es el canónico. `data-tema="claro"` lo cambia; sin atributo, sigue la preferencia del sistema.

## Las reglas que no se negocian

1. El color solo nombra hechos confirmados. Si el lector no confirmó, el estado es `sin-confirmar`: sin relleno y con borde discontinuo.
2. Todo estado lleva palabra además de color.
3. El acento es acción, no estado. `kino-acento-base` va en el botón que otorga un permiso y en nada más.
4. Un conjunto puede cambiar `kino-tenant-marca` y `kino-tenant-radio`. Los seis estados no se tocan: si cada conjunto los recolorea, la traza deja de ser comparable entre conjuntos.
5. Placas, códigos y horas van en `kino-dato` o `kino-placa`, con cero barrado y cifras tabulares.
6. Un token semántico nuevo se escribe como referencia a un primitivo. Un hex suelto en `tokens/tema/` es un error de revisión.
7. Toda variable que use `capa-componentes.css` tiene que existir en `tokens/`. `npm run verificar` lo comprueba.

## Lo que falta

- La licencia de Arkit ExtraBold. Mientras no se confirme, las letras del logotipo viven solo como contornos y no se usan en ninguna otra parte.
- El archivo vectorial original del logo, si existe. Estos SVG son una reconstrucción con 98 % de coincidencia contra el PNG.
- Los iconos de Iconoir: entran con `npm install`, falta copiarlos a `iconos/` y subirlos al sistema de marca.
- Autoalojar Archivo y JetBrains Mono: hoy entran por `@import` desde Google Fonts.
- Subir los diez iconos de `iconos/` al grupo `Icons` del manual.
- Los MCP de Figma, si el diseño pasa por ahí: `bash instalar-figma-mcp.sh`.
- Aplicar el sistema al deck y a las plantillas de documento.
