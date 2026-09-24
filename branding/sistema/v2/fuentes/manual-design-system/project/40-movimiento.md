# Movimiento

En Kino el movimiento no decora: dice qué le pasó a un pase. Hay cinco verbos, y cada uno tiene una curva y una duración que no se usan para otra cosa. Si dos cosas distintas se mueven igual, el usuario deja de poder leerlas.

## Los cinco verbos

| Verbo | Qué significa | Duración | Curva | Qué se mueve |
|---|---|---|---|---|
| `aparecer` | Algo nuevo llega: un pase emitido, una fila nueva en la traza | `crecer` 420 ms | `crecer` | Sube 18 px y escala de 0,94 a 1 |
| `confirmar` | El lector respondió: `sin-confirmar` pasa a `vigente` | `corto` × 1,75 ≈ 420 ms | rebote corto | El chip escala de 0,85 a 1 y el punto late tres ciclos |
| `caducar` | La vigencia se agotó sola | `decaer` × 1,6 ≈ 1 440 ms | `decaer` | La barra de vigencia se vacía; la tarjeta baja a 62 % |
| `revocar` | Alguien cortó el pase | `corto` 240 ms | `revocar` | Sacudida seca de 6 px y el estado pasa a `negado` con el motivo |
| `cascada` | Los elementos de una vista entran en orden | `tarjeta` 820 ms | `crecer` | Cada ítem sube 26 px, con 90 ms entre uno y otro (máximo 520 ms en total) |

Caducar es seis veces más lento que revocar a propósito: vencer es natural, cortar es una decisión. Se distinguen sin leer.

## Tokens

Viven en `tokens/40-movimiento.tokens.json` (DTCG 2025.10) y llegan a CSS como `--kino-movimiento-*`.

| Familia | Tokens |
|---|---|
| Duración | `instante` 120 · `corto` 240 · `crecer` 420 · `tarjeta` 820 · `decaer` 900 · `trazo` 950 · `cortina` 1 600 · `latir` 1 800 (ms) |
| Curva | `crecer` (.16, .84, .30, 1) · `decaer` (.62, .03, .86, .34) · `latir` (.45, 0, .55, 1) · `cortina` (.76, 0, .24, 1) · `revocar` (.4, 0, 1, 1) |
| Escalonado | `tarjetas` 90 ms · `filas` 55 ms |
| Distancia | `subida` 26 px · `desenfoque` 6 px |

## Implementación

`kino-movimiento.js` expone `window.KinoMovimiento` con los cinco verbos más `cortina`, `filas` y `registrarEnMotor`. Lee los valores de las variables CSS: el script no tiene números propios. Si la página carga el motor de Motion Playground (`window.__motion`), los tokens de Kino se registran en él y `M.animate('crecer')` usa la misma curva.

```js
KinoMovimiento.aparecer(tarjeta);
KinoMovimiento.confirmar(chip);                       // sin-confirmar → vigente
KinoMovimiento.caducar({ barra, chip, tarjeta });     // lento
KinoMovimiento.revocar({ chip, tarjeta, texto: 'Negado · revocado por el residente' });
```

## Reglas

- Solo `transform`, `opacity` y `filter`. Nada que obligue a recalcular el layout.
- El punto de `vigente` es lo único que se anima sin que nadie lo pida. Todo lo demás se mueve porque algo cambió.
- Con `prefers-reduced-motion: reduce` cada verbo salta a su estado final. La información es la misma; solo falta el tránsito.
- La cortina y la aurora son del deck, la web y la bienvenida. En la aplicación de trabajo no se usan.
- Ninguna animación bloquea la acción: el botón responde antes de que termine el tránsito.
