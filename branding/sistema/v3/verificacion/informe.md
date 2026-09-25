| # | Comprobación | Resultado | Detalle |
|---|---|---|---|
| 1 | Términos prohibidos, «permiso», exclamaciones y rayas en el texto visible | PASA | 0 términos, 0 exclamaciones, 0 rayas |
| 2 | npm run voz -- kino sobre el texto visible y los textos de la app | PASA | 0 hallazgos · 0 errores |
| 3 | Límites de largo de UX writing (botón ≤ 3, estado ≤ 20, WhatsApp ≤ 45) | PASA | 46 de 46 dentro del límite |
| 4 | Tú con residente y visita, usted con la administración, sin mezclar | PASA | app con usted: 0 · administración con tú: 0 · piezas para administración con tú: 0 |
| 5 | APCA en todos los pares texto y fondo (Lc 75 · 60 · 45 · 30) | PASA | 120 mediciones, 0 fallos, 0 sin mínimo APCA |
| 6 | Diff entre tokens DTCG, kino-brand.css y variables de Figma | FALLA | DTCG 274 · kino-brand.css: 0 faltan · Figma: 270 variables y 3 estilos de efecto, 1 tokens sin variable, 0 valores distintos (color en los dos modos, números y cadenas) · --kino-texto-enlace |
| 7 | Componentes sin ligar a variables (CSS y Figma) | PASA | capa-componentes.css: 0 valores sueltos · Figma: 0 nodos con color sin variable |
| 8 | Decisiones sin justificación de la plataforma | PASA | decisiones.md: 29 con detalle, 0 sin «Por qué» · tabla X: 0 sin «Responde a» · departamentos sin traza: 0 |
| 9 | Enlaces y anclas rotas | PASA | 48 anclas internas, 0 rotas · 6 enlaces externos |
| 10 | Cobertura de la definición de terminado | PASA | 81 elementos · 81 con su ancla en el sitio · 0 [PENDIENTE] con motivo · 0 faltan |
