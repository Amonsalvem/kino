# Marca

El logotipo de Kino: un bloque con un arco abierto y una gota que lo atraviesa. Es una puerta con memoria de lo que pasó por ella; por eso el sistema no usa candados ni escudos.

## Qué provee el consumidor

El SVG en línea (nunca `<img>`, porque la marca hereda color) y una altura. El ancho se calcula solo.

```html
<span class="kino-marca" style="block-size:40px">
  <svg viewBox="0 0 100 101.824" fill="currentColor" fill-rule="evenodd" role="img" aria-label="Kino">…</svg>
</span>
```

## Piezas

| Pieza | Cuándo | Archivo |
|---|---|---|
| Marca sola | Barras, avatares, sellos, cuando el nombre ya está dicho | `kino-mark.svg` |
| Bloqueo vertical | Portadas y láminas de apertura | `kino-lockup-vertical.svg` |
| Bloqueo horizontal | Encabezados y pies, de 28 a 48 px de alto | `kino-lockup-horizontal.svg` |
| Gota | Favicon, marcador de mapa, punto de una traza | `kino-drop.svg` |

## Reglas

- Colorea con `kino-acento-base` (`#00BB83` en oscuro) o con `kino-texto-primario`. Sobre `kino-superficie-inversa` usa `kino-texto-inverso`; sobre `kino-acento-base`, `kino-texto-sobre-acento`. El acento del tema oscuro sobre la superficie inversa queda por debajo de 3:1, el mínimo para elementos gráficos.
- **Aire mínimo: el ancho del arco interior**, 63 unidades de las 100 que mide el bloque de ancho (en píxeles, 0,63 × el ancho del bloque, o 0,62 × su alto). Una marca de 96 px de alto pide 60 px libres por cada lado; un bloqueo horizontal de 34 px, 21 px. Nada entra ahí, ni el nombre del conjunto ni el borde de un contenedor. Se mide desde el bloque, también en los bloqueos: el logotipo es parte de la pieza y el aire va por fuera del conjunto.
- Por qué el arco y no un módulo menor: la gota necesita aire para leerse como algo que pasa por el vano. Con menos espacio, la marca se lee como una insignia pegada al contenido, que es la lectura que la marca evita.
- Tamaño mínimo: 20 px de alto para la marca sola, 28 px para el bloqueo horizontal, 40 px para el vertical. Por debajo, usa la gota.
- En el bloqueo vertical el logotipo mide exactamente el ancho del bloque. Es la proporción del archivo original: no la ajustes a ojo.
- No rotes, no inclines, no apliques degradado, no pongas sombra proyectada. Si la marca necesita destacarse sobre una foto, va dentro de un bloque de `kino-superficie-inversa`.
- No reconstruyas el logotipo con una fuente: las letras están trazadas. La familia Arkit ExtraBold vive solo dentro de esos contornos y no se usa en ninguna otra parte del sistema.

## Kino es la marca

La marca de Kino encabeza toda pantalla y todo material. El nombre del conjunto va como dato, en `kino-texto-secundario`, nunca como logotipo en su lugar ni a su lado con el mismo peso. La gota es el marcador de un ingreso en la traza y significa lo mismo en todos los conjuntos.
