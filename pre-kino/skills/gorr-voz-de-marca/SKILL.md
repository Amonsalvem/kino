---
name: gorr-voz-de-marca
description: Construye y calibra la identidad verbal medible de un cliente de GORR (voz.json con perfil NN/g, vocabulario, patrones prohibidos y casos de evaluación) y la guía de contenido. Usar en la fase 2 del playbook o al revisar copy contra la voz de un cliente.
---

# GORR · Voz de marca medible

La voz de un cliente vive en `clientes/<id>/voz.json`. Lo que está ahí se verifica (`npm run voz`, `npm run calibrar-voz`, evals); lo que solo está en prosa no. Tu objetivo es pasar la voz de adjetivos a reglas.

## Entradas
- `00-brief.md` y la tabla de `01-estrategia/posicionamiento.md`.
- Textos reales del cliente (web, correos, posts). Si no hay, pídelos: sin muestras no hay calibración.

## Pasos

### 1. Perfil de tono (NN/g, Kate Moran, «The Four Dimensions of Tone of Voice»)
Cuatro dimensiones, escala 1–5 (1 = primer polo): formal↔casual, serio↔divertido, respetuoso↔irreverente, sobrio↔entusiasta. Para cada una escribe una `nota` que diga cómo se nota el valor en una frase real del cliente. Marca `perfil.estado` como «propuesta» hasta que el cliente lo apruebe.

### 2. Somos / no somos
Tres rasgos máximo. Cada «no somos» es el exceso del rasgo correspondiente (claros → no cortantes).

### 3. Vocabulario
- `usar`: términos propios con su significado exacto.
- `noMezclar`: pares que no se intercambian (ej. «permiso» ≠ «cuenta»).
- `evitar`: término, qué usar en cambio, por qué, y `patron` (regex) si el término tiene variantes. `gravedad: "error"` solo para lo que nunca debe salir publicado.

### 4. Patrones
Regex para muletillas y estructuras que se detectan sin modelo. La plantilla trae los genéricos del español (antítesis «no es X, es Y», «Y» de arranque, «Es decir:», relleno, léxico de agencia, raya). Agrega los del cliente. Cada patrón lleva `porque`.

### 5. Calibrar
- Si existen correcciones previas del cliente, ponlas en `pruebas/voz-antes.md` y `pruebas/voz-despues.md` (una frase por línea, alineadas).
- `npm run calibrar-voz -- <id>`: la compuerta exige **0 falsos positivos**. Si un patrón acusa una frase corregida, afínalo o bájalo a `aviso`; no lo dejes gritando sobre texto limpio.
- Reporta la cobertura real (ej. «21 de 42»). Lo que el regex no alcanza (tríadas por inercia, énfasis vacío) queda para la rúbrica LLM.

### 6. Casos para evals
Tres a seis piezas de copy que el cliente produce de verdad, con datos concretos en `contexto`. Evita casos genéricos («escribe un post sobre la marca»).

### 7. Guía de contenido
Llena `02-verbal/guia-de-contenido.md` con ejemplos reales. Si contradice `voz.json`, manda `voz.json`. La estructura sigue a Mailchimp, pero su licencia es no comercial: no copies su texto.

## Revisar un texto contra la voz
1. `npm run voz -- <id> <archivo>`.
2. Luego lee el texto contra el perfil y los rasgos: eso el regex no lo mide.
3. Entrega la versión corregida y una tabla antes → después → por qué. Si la corrección revela un patrón nuevo, propón agregarlo a `voz.json`.

## Compuerta de la fase
- `npm run voz -- <id>` sin errores sobre `muestras/`.
- `npm run calibrar-voz -- <id>` con 0 falsos positivos (si hay pruebas).
- Perfil aprobado por el cliente.
