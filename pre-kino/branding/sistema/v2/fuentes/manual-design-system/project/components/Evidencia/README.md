# Evidencia

El rótulo que dice qué tan segura es una afirmación y de dónde sale. Es la regla 1 del proyecto (jerarquía de evidencia) convertida en componente, y lo que hace que Kino hable como una investigación.

## Qué provee el consumidor

```html
<span class="evid" data-g="prueba">Prueba ejecutada</span>
<span class="fuente">inspección, sujeto 2 · 15 sep 2026</span>
```

| `data-g` | Significa | Forma |
|---|---|---|
| `observado` | Lo vimos en la pantalla o en el sistema | Punto lleno, verde vigente |
| `prueba` | Lo provocamos y registramos el resultado | Rombo, acento |
| `entorno` | Fuente externa citada | Punto, índigo |
| `inferido` | Conclusión nuestra | Punteado, ámbar |
| `abierto` | Depende de una respuesta que no tenemos | Punteado, violeta, «?» |

## Reglas

- Toda afirmación de diagnóstico lleva grado y fuente. Sin fuente no se publica.
- La forma cambia con el grado, no solo el color.
- `.fuente` va en mono, con el archivo o la referencia exacta y la fecha.
