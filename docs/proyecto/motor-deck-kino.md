# Motor del deck Kino — qué cambió y dónde vive

Fecha: 2026-09-21 · Reemplaza el parcheo a mano del HTML del deck.

## El diagnóstico que originó el cambio

La queja era «aún se percibe muy IA». La medición sobre el deck del 19 de septiembre
dice que el problema no es el lenguaje sino la forma:

| Medida | Antes | Después |
|---|---|---|
| Anchos de columna distintos en todo el deck | 2 | 7 |
| Márgenes izquierdos distintos | 2 | 4 |
| Cuota de la forma más repetida | 0.94 | 0.355 |
| Láminas con composición idéntica | 11 | 0 (las once se reparten en dos espejos) |

Treinta de treinta y una láminas abrían `kicker > head` y cerraban en `foot`, dentro
de una sola columna de 1000 px. Un deck con un solo ritmo se lee como hecho por una
máquina por buena que sea la prosa.

## Qué se construyó

Un **paquete de marca Kino dentro del plugin** `hanademi-decks` (v0.5.0), no un fork:

- `engine/src/layouts.ts` — la composición se **deriva**: del papel de la lámina en el
  argumento y luego de la forma de su contenido. Un `statement` con un párrafo se lee
  al lado de su aserción; con dos, el segundo baja a un riel al margen (y el riel
  alterna de lado entre láminas que comparten forma); con tres o más, columna. Tablas y
  gráficos van anchos con el titular en un riel; el dibujo sangra; la cita es una pausa;
  la decisión se ancla a la derecha. Doce formas.
- `engine/src/motion.ts` + capa CSS — tres curvas que **significan** cosas distintas:
  `crecer` lo que aparece, `decaer` lo que vence, `latir` lo que está vivo. Caducar y
  ser revocado no se mueven igual porque no son lo mismo.
- `engine/src/brands.ts` — un paquete de marca cambia **todos** los tokens, no los dos
  acentos que ajusta `deckType`. Con marca activa el motor suprime la inyección de
  acentos del tipo de deck y la auto-auditoría WCAG mide **la paleta de la marca**.
  Antes medía la paleta Probatorio: reportaba verde sobre colores que nadie veía.
- `engine/src/render.ts` — el tipo de lámina `diagrama` entra al motor. Antes existía
  solo como parche a mano en el HTML del deck, así que cualquier reconstrucción lo
  perdía (y lo perdió: las cuatro láminas de flujo salieron «Unknown slide type»).
- `engine/test/estilos.test.ts` — la hoja de marca se comprueba como dato: tokens
  usados pero no definidos, atajos de `animation` con dos funciones de tiempo, reglas
  que se salen del alcance de la marca, y animaciones infinitas.

## Dos defectos que solo aparecieron al renderizar

1. `animation: k-latir var(--kino-latir) ease-in-out 2` no corría. La variable ya trae
   duración **y** curva; añadir `ease-in-out` mete dos funciones de tiempo en el atajo y
   el navegador descarta la declaración entera, sin error.
2. El pulso original era `infinite`. Un elemento que se mueve solo más de cinco segundos
   sin forma de pausarlo incumple WCAG 2.2.2, y una proyección no tiene botón de pausa.
   Ahora son dos ciclos: 3,6 s.

Las dos están cubiertas por el test de estilos.

## Verificación

31 láminas, ES y EN, tema claro y oscuro: 0 errores de consola o de página, 0 láminas
vacías, 0 tipos desconocidos, 0 láminas que se salgan de 1080 px. Auto-auditoría:
18/18 automáticos en verde, incluido «la composición varía». `tsc --noEmit` limpio.

## Dónde está

- Plugin empaquetado: `work/agente-decks/hanademi-decks.plugin` (v0.5.0)
- Fuente desempaquetada: `work/agente-decks/hanademi-decks-src/`
- Deck: `kino/Kino_Deck_diagnostico_2026-09-21.html`

## Pendiente

- Correr el build oficial: `cd hanademi-decks-src/engine && npm install && npm run build`.
  Lo verificado aquí se construyó con `build-sin-red.mjs`, un arnés que existe porque el
  entorno del agente no tiene red para instalar esbuild. Manda `build.mjs`.
- `npx vitest run` para los tests nuevos (`layouts`, `estilos`), por la misma razón.
- En el póster expandido del flujo 4, el nodo fantasma «NO EXISTE» se superpone al
  subtítulo del encabezado. Hay que regenerarlo, pero `inspeccion/flujos/` ya no está en
  el disco (ver `inspeccion/_borrado-flujos-2026-09-21.md`).
- La composición está delimitada a `[data-brand="kino"]`. Un deck Probatorio recibe las
  clases pero conserva su marco: es deliberado, para no cambiar decks existentes.
