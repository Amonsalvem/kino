# Flujo

La gramática de los lienzos de recorrido: nueve formas con un significado fijo. Viene de las láminas 13 a 23 de la entrega 2 y es la forma en que Kino muestra cómo se mueve una persona por el sistema.

## Las formas

| Forma | Significa | Especificación |
|---|---|---|
| Inicio y fin | El segundo 0 y el punto donde termina | Píldora, `rx` = alto/2, membrana |
| Paso o pantalla | Una pantalla real o un acto del mundo | Rectángulo `rx` 4, elevada |
| Decisión | Bifurcación; debajo va la evidencia | Rombo ámbar (`--pv-*`) |
| Camino alterno | Por donde suele pasar el volumen hoy | Trazo 6 · 5 |
| Estado del sistema | Lo que el producto afirma | Punteado 6 · 4, sin relleno |
| Meta lograda | Llega a donde tenía que llegar | Píldora vigente |
| Meta no lograda | Termina fuera o con costo | Píldora negado |
| Otorgar | El acto que crea el pase | Rectángulo acento. Lo único con acento |
| Pregunta abierta | Depende de una respuesta pendiente | Punteado violeta con «?» |

## Reglas

- Debajo de cada caja va, en mono de 10–11 px, de dónde sale lo que afirma: pantalla, prueba o fuente.
- El lienzo va en `.lienzo` con `data-zoom`: clic para ampliar.
- En decks, los elementos entran de izquierda a derecha según su x y los trazos se dibujan (`data-traza`). Lo punteado solo se funde.
- En teléfono, el lienzo se desliza de lado; la página nunca.
