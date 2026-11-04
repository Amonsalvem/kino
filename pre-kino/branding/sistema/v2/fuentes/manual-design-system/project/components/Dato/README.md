# Dato

El tratamiento de las cifras que el sistema lee en la puerta: placas, códigos de un solo uso, horas de entrada, cédulas.

## Qué provee el consumidor

La clase y el contenido. Nada más.

```html
<span class="kino-placa">HTK 481</span>
<span class="kino-dato">19 sep · 14:32:07</span>
```

## Reglas

- `kino-placa` y `kino-dato` usan JetBrains Mono con `slashed-zero` y `tabular-nums`. En un sistema que compara lo que ve el lector de placas contra lo que escribió una persona, confundir `0` con `O` o `1` con `I` es un ingreso mal concedido.
- Los códigos de un solo uso se muestran con separación entre caracteres, para que se dicten por teléfono sin error.
- Todo dato personal —cédula, teléfono, correo, rostro— se muestra truncado y envuelto en el estado `identidad`. La versión completa se revela con una acción explícita que queda en la traza.
- Las horas se escriben en formato de 24 horas con segundos cuando son de la traza, y en lenguaje del residente («hasta el viernes a las 6:00 p. m.») cuando son de un pase que él mismo está creando.
- Nunca centres una columna de cifras: alineadas a la derecha, o a la izquierda si son códigos alfanuméricos.
