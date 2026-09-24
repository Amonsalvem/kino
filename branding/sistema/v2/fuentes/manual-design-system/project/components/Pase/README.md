# Pase

El objeto que recibe un invitado o colaborador: autor, motivo, vigencia y modo, con una prohibición (no crea una persona). Es la unidad del producto y la pieza más reconocible de la marca. Un pase no es una cuenta: la cuenta la tiene el residente.

## Qué provee el consumidor

Dos formas del mismo objeto. El **boleto** (`.boleto`) es la ilustración: presentaciones, onboarding, material de venta. La **tarjeta de lista** (`.mini-pase`) es la pieza de producto.

```html
<div class="mini-pase vivo">
  <div class="f1"><b>Marta Quintero</b><span class="est" data-e="vigente">Vigente</span></div>
  <div class="f2">trabajo doméstico · lun–vie · 07:00–17:00</div>
  <div class="ventana"><i style="left:0;right:22%"></i></div>
</div>
```

Variantes de la tarjeta: `.vivo` (vigente, lleva `kino-resplandor-vigente`), `.sc` (sin confirmar: sin relleno, borde punteado), sin clase (resto de estados).

## Reglas

- Los cuatro atributos son obligatorios. Sin autor no hay constancia; sin vigencia no hay pase.
- La forma del boleto (muescas laterales, punteado bajo la cabecera, borde de acento) es exclusiva del pase.
- El pase nace `sin-confirmar` y pasa a `vigente` cuando la puerta responde (`KinoMovimiento.confirmar`).
- El residente y la portería ven el mismo objeto. En portería, cédula y teléfono van truncados y con `identidad`.
- Solo la tarjeta vigente resplandece: si todo resplandece, nada resplandece.
