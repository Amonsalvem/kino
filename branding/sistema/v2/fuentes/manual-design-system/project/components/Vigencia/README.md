# Vigencia

La barra que muestra cuánta vida le queda a un pase. El campo «Válido desde / hasta» ya existe en la base de datos para los vehículos y está oculto para el dueño; esta pieza lo hace visible.

## Qué provee el consumidor

Un `.ventana` con un `<i>` cuyo `left` y `right` marcan el tramo vigente. Encima, el tiempo restante en `kino-dato`.

```html
<div class="ventana"><i style="left:0;right:86%;background:var(--pv-bd)"></i></div>
```

## Reglas

- La barra nunca va sola: una barra al 14 % no dice si son 40 minutos o 4 días.
- El aviso de «por vencer» lo decide la regla del conjunto; el componente solo lo pinta (ámbar).
- Un pase sin vigencia no existe. Un dato heredado sin fecha de fin se muestra `sin-confirmar` y se pide la fecha.
- Se vacía con `decaer` (900 ms, lento): caducar y ser revocado no se mueven igual (`KinoMovimiento.caducar`).
