# Estado

La etiqueta que dice en qué punto de su vida está un pase. El diagnóstico de septiembre encontró que la app no tiene lenguaje de estado y que afirma cosas del mundo físico que el lector nunca confirmó; este componente es la respuesta.

## Qué provee el consumidor

Un `<span class="est">` con `data-e` y la palabra visible. La palabra es obligatoria: el color nunca viaja solo.

```html
<span class="est" data-e="por-vencer">Vence en 40 min</span>
```

## Los seis estados

| `data-e` | Significa | Regla |
|---|---|---|
| `vigente` | Pase vivo, sincronizado y confirmado por el lector | El único punto que late, tres ciclos (WCAG 2.2.2) |
| `por-vencer` | Dentro de la ventana de aviso que fijó la administración | El texto dice cuánto queda, no «pronto» |
| `vencido` | Caducó solo | Sin color propio: un final no es un error |
| `negado` | Fuera de ventana, de límites o revocado | Dice el motivo y quién lo revocó |
| `sin-confirmar` | La app no sabe todavía qué pasó en la puerta | Sin relleno, borde discontinuo |
| `identidad` | Dato personal o biométrico a la vista | Marca la zona regulada por la SIC |

## Reglas

- `sin-confirmar` no es un estado de carga: es la respuesta honesta mientras HikCentral no confirme.
- No se inventan estados intermedios («en revisión», «pendiente de aprobación»): el sistema no tiene cola de aprobación.
- Un estado nunca se distingue solo por matiz.
- El acento no es un estado. Es la acción de otorgar.
- Para reiniciar los tres latidos cuando una vista entra, quitar y volver a poner la clase `relatir` (lo hace `KinoMovimiento.confirmar`).
