# Tarjeta

La superficie de información de Kino: membrana con relieve (`.tj`). Encima van cifras, medidores, anillos y chips. Las piezas vienen de la entrega 2.

## Qué provee el consumidor

```html
<div class="tj"><span class="cifra">312</span><p class="peq">personas registradas</p>
  <div class="medidor"><i style="--v:0"></i></div><p class="medidor-pie">0 sincronizadas con la puerta</p></div>
```

| Pieza | Clase | Cuándo |
|---|---|---|
| Tarjeta | `.tj` · `.tj.acento` | Toda agrupación. Acento solo para lo que otorga o se propone |
| Cifra | `.cifra` | Una cifra con su denominador («0 / 312»), nunca sola |
| Medidor | `.medidor > i` con `--v` (0–1) | Proporción de una cifra |
| Anillo | `.anillo` | Proporción de un todo |
| Puntos | `.puntos > i.si` | Avance contable (5 de 10) |
| Chip | `.chip-q`, `.chip-app`, `.alerta-l` | Quién responde, lo que dice la app, una alerta |
| Aviso | `.aviso` | Restricción o riesgo. Ámbar |
| Destacado | `.destacado` | La conclusión de la vista |

## Reglas

- No todo es una tarjeta: la tabla, la glosa y el pie van sin caja.
- En decks, cada `.tj` recibe foco de luz e inclinación de 4° al pasar el puntero (solo puntero fino y sin «reducir movimiento»).
- Rojo solo significa negado. Un aviso es ámbar.
