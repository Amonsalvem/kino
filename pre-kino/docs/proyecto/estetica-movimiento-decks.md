# Estética de movimiento de los decks Kino (estándar desde el 22 sep 2026)

Base: `Kino_Deck_flujos_y_mapa_2026-09-22.html`. Todo deck nuevo parte de este archivo (su `<style>`, el `<div id="cortina">`, `#fondo`, `#velo` y el bloque del motor), no de cero.

## 1. Cortina de entrada
- Dos hojas color `--abismo` con borde en degradado de 22vh, más una costura de acento (`<b>`) que se extiende del centro a los bordes antes de abrir.
- Se anima con la Web Animations API nativa y solo `transform` (compositor). **No** con `M.animate`: ese va por requestAnimationFrame en el hilo principal, y la compilación del shader de la aurora, el partido de titulares y el pintado del documento se comían los cuadros. Por eso arrancaba y de golpe aparecía abierta.
- Espera a las fuentes y a tres cuadros (tope 1,2 s) para que la aurora ya haya dibujado detrás.
- Costura 420 ms → hojas 1600 ms con `cubic-bezier(.76,0,.24,1)`. La portada empieza a entrar al 42 % de la apertura.
- Seguro: `finally` + temporizador de 6 s la retiran siempre.

## 2. Fondo: aurora WebGL, fija
- `M.background.aurora({ …, dprMaximo: .5 })`. Media resolución: un campo sin bordes se ve igual y cuesta de 4 a 9 veces menos.
- **Sin vigilante de fps.** Antes, si los fps bajaban de 45, la aurora se cambiaba por el gradiente CSS a mitad de la presentación: el fondo pasaba de verde a índigo con un destello gris (visto en una grabación de pantalla el 22 sep). Decisión del equipo: el fondo inicial se mantiene. `vigilarFondo()` sigue definida pero no se llama.
- Paletas: oscuro `#006B4C · #2E2470 · #011F16` (menta profunda, índigo, base); claro `#6FDDB8 · #C4C2FF · #FFFFFF`.
- Velo `.55` en el oscuro y `.5` en el claro (antes `.86`/`.9`, que tapaban la aurora).
- Contraste en el peor caso (alfa a pleno, sin viñeta): `--tx3` = 4,65:1 en el oscuro y 5,28:1 en el claro. Si se sube la paleta o se baja el velo, hay que volver a medir.
- `motion/src/modules/background.ts` ya acepta `dprMaximo` (tsc limpio). El bundle del deck lleva el mismo cambio parcheado.

## 3. Entrada por ítem
- `coreografiar(sec, dentro)` sustituye a `entrarLamina`. Anima cada ítem, no el bloque: `.rej > *` (tarjetas, capturas), `ol/ul > li`, `thead`, `tbody > tr`, `.franja > *`. Solo el nivel exterior: una lista dentro de una tarjeta llega con su tarjeta.
- Tarjetas: subida de 26px, escala .965, 820 ms, escalonado de hasta 90 ms. Filas de tabla: entran desde la izquierda con 55 ms de escalonado. Texto suelto: subida con desenfoque de 6px.
- Diagramas SVG: después del recorte del lienzo, los elementos entran de izquierda a derecha según su x (en unos 950 ms). Los trazos se dibujan con `stroke-dashoffset`. Lo que ya trae `transform` como atributo solo se funde.
- Portada: el isotipo crece desde su base y después aparece el logotipo.
- `fill:'backwards'`: al terminar no queda estilo pegado. Imprimir ejecuta `finish()` sobre todo.
- `prefers-reduced-motion`: ni cortina, ni aurora, ni coreografía.

## 3b. Hover de tarjetas
- En la lámina activa, cada `.tj` tiene foco de luz (`M.spotlight`, radio 300) e inclinación hacia el puntero (`M.tilt`, 4°, perspectiva 1000, elevación 10). Las capturas se inclinan 7°; las tarjetas menos porque son anchas y llevan texto. Solo con puntero fino y sin «reducir movimiento».

## 3c. Recursos visuales (22 sep)
Regla: cada gráfico sale de un dato o afirmación que ya está en la lámina; nada decorativo sin respaldo.
- Íconos en línea (sprite `#i-*`, trazo `currentColor`) en actores, cifras, evidencia y chips.
- Encargo: cadena app → Kino → HikCentral → lectores → talanquera.
- Lugar: barras 312 frente a 888 y anillos 47,88 % / 61,7 %.
- Recorte: el hilo de los cuatro actores con la fuga al teléfono.
- Método: barras de observaciones por sujeto.
- Matriz: celdas con ícono (Nadie / No / Sí).
- Prueba: secuencia placa → «Permitido» → HikCentral → la puerta abre.
- Hallazgos: anillos de sincronización de H6 (0/312, 1/44) e íconos de evidencia.
- Problema: tabla quién sabe / quién decide.
- Leyenda: muestra de cada forma de los flujos.
- Transversal: cuatro carriles que se cortan en el mismo punto.
- Pase: boleto ilustrado que pasa de «sin confirmar» a «vigente» una vez.
- Estado: conteo por grupo. Abierto: chips de quién responde. Sigue: 5 de 10 posibilidades y alerta de la placa.
- Animación: `animarViz()` (barras, anillos, trazos, puntos) después de la cascada; todo por WAAPI y con `fill:'backwards'`.

## 3d. Responsive (22 sep)
- ≤1100 px (tablet): las parejas de columnas con gráfico (problema, pase) pasan a una; los anillos de H6 dejan de ir junto al titular.
- ≤900 px: la cadena del encargo, la secuencia de la prueba y los carriles de lo común pasan a vertical.
- ≤760 px (teléfono):
  - Las tablas se muestran como tarjetas. Un script copia el nombre de la columna en cada celda (`data-rot`), así que no hay que marcarlas a mano en decks nuevos.
  - La matriz de capacidades queda en una rejilla de 2×2 por capacidad.
  - Los flujos y el mapa se deslizan de lado (ancho 1050 y 1200 px) con la indicación «desliza para recorrer · toca para ampliar».
  - El hilo del recorrido tiene una versión vertical (`.hilo-movil`).
  - Márgenes de 16 px.
- Verificado a 390, 768, 1024 y 1440 px: sin desplazamiento horizontal de la página y sin errores. El escritorio queda igual que antes.

## 4. Texto
- Los titulares partidos por palabras dejaban la puntuación como pieza aparte y la línea podía cortarse antes del punto. Ahora la puntuación se une a la palabra anterior.
- Barrido de muletillas del 22 sep: registro en `kino/registro-muletillas-2026-09-22.md`.

## Pendiente
- Pasar la coreografía y la cortina a `engine/template.src.html` del plugin, para que los decks generados por el motor la traigan de fábrica.
- Probar en el equipo y el proyector de la sustentación que la aurora vaya fluida: ya no hay respaldo automático.
