# Movimiento

`KinoMovimiento`: la capa semántica del sistema de movimiento. Cada verbo significa algo y no se usa para otra cosa. Los valores salen de los tokens `kino-movimiento-*`; el archivo es `branding/sistema/v2/kino-movimiento.js`.

## Qué provee el consumidor

Cargar el motor (Motion Playground) si se usa, y después `kino-movimiento.js`. Si el motor está, `KinoMovimiento.registrarEnMotor()` le pasa las curvas de Kino (`M.animate(el, …, {easing: 'crecer'})`).

```js
KinoMovimiento.aparecer(tarjeta);                       // crecer · 420 ms
KinoMovimiento.confirmar(chip);                         // sin-confirmar → vigente, tres latidos
KinoMovimiento.caducar({ barra, chip, tarjeta });       // decaer · 900 ms, lento a propósito
KinoMovimiento.revocar({ chip, tarjeta });              // corte · 240 ms, deja «Negado»
KinoMovimiento.cascada(contenedor);                     // ítems de una lámina, 90 ms entre sí
KinoMovimiento.cortina();                               // apertura del deck: costura 420 + hojas 1600
```

## Reglas

- Crecer es aparecer, decaer es caducar, latir es estar vivo, revocar es cortar. Nada se anima para decorar.
- Solo `transform`, `opacity` y `filter` (compositor). La cortina va por Web Animations, no por requestAnimationFrame.
- El latido se detiene a los tres ciclos (WCAG 2.2.2).
- Con «reducir movimiento», todo salta a su estado final sin transición.
