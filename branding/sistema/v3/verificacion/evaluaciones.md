# Evaluaciones independientes · Fase 5 (24 sep 2026)

Dos subagentes que solo vieron el sitio construido (`sitio/build/kino-sistema-de-marca.html` y su `texto-visible.md`), sin el razonamiento de quien lo escribió. El detector leyó `muestras-detector.md`: los titulares, ledes, definiciones y leyendas de cada sección, más el microcopy de la app.

Condición de cierre del encargo:
- lector frío 8/8 con cita y claridad media ≥ 4;
- detector sin marcas en el microcopy y como máximo 1 señal por sección.

## Lector frío

| Ciclo | Respuestas con cita | Claridad media | Resultado |
|---|---|---|---|
| 1 | 8/8 | 3,9 | FALLA (media < 4) |
| 2 | 8/8 | 4,25 | PASA |

**Qué se corrigió entre el ciclo 1 y el 2**
- Color del Pase vencido: faltaba decir que Usado, Vencido y Revocado van en sustrato. Se agregó una frase y una columna «Familia» en `#color.estados`.
- Verbal decía «propuesta» en decisiones ya aprobadas (tratamiento, mayúscula, horas). Ahora dice «aprobada».
- Logo sobre oscuro: la regla con los dos colores y el tamaño mínimo quedó en una sola frase en `#logo.fondos`.
- Códigos internos (F4, X2, V5): cada uno enlaza ahora a un registro nuevo, `#gobernanza.registro`. Se quitaron las menciones al «encargo» y a las «instrucciones».
- El texto plano traía un manifiesto C2PA en base64 dentro del sprite: se quita al construir.
- El saludo del WhatsApp y el uso de «visitante» y «visita» se unificaron.

**Observaciones del ciclo 2 que siguen abiertas.** Se llevan a la Parada 4.
1. Vencido y Usado solo se distinguen por el tono del texto y la palabra.
2. El Pase se nombra antes de definirse en el recorrido «Conocer Kino».
3. Cuatro verdes: se aclaran en `#color.roles`, pero no donde aparecen primero.
4. La versión 1.0.0 figura «Propuesta»: el lector no sabe qué puede aplicar ya. Se resuelve con la aprobación de la Parada 4.
5. El centro de descargas está al final de Gobernanza.

## Detector de IA

| Ciclo | Señales | Microcopy marcado | Secciones con más de 1 | Resultado |
|---|---|---|---|---|
| 1 | 17 | 1 | Plataforma (5), Imagen (3), Voz (2), Iconografía (2) | FALLA |
| 2 | 12 | 0 | Plataforma (4), Imagen (2) | FALLA |
| 3 | 8 | 1 (débil) | Motion (3), Plataforma (2) | FALLA |
| 4 | 1 | 0 | ninguna | **PASA** |

**Qué se corrigió en cada ciclo**
- Antítesis «X, nunca Y».
- Tríadas por inercia.
- Titulares en espejo.
- Cierres que repiten la idea.
- «Lo vivo» sin objeto concreto.
- «Hoy su conjunto… Con Kino…».

**Después del ciclo 3** se corrigieron también las 8 señales:
- Plataforma, 2: «voz, color o forma» y el cierre de la tarjeta de portería.
- Motion, 3: los titulares «nombra un cambio» y «Primero lo que se lee…», y «Estar vivo».
- Tipografía, 1: el titular.
- Verbal, 1: el lector frío.
- El ejemplo comercial marcado como microcopy débil.

El encargo fija un máximo de 3 ciclos. Por eso esas correcciones no se volvieron a evaluar en la Fase 5, y la Parada 4 reportó el detector como FALLA.

**Ciclo 4 (25 sep, autorizado por Nico en la respuesta a la Parada 4).** Se corrió con la muestra regenerada desde el sitio con la identidad aplicada (F4-P4), con el mismo prompt.
- Resultado: 1 señal, 0 secciones con más de una, 0 microcopy marcado. **PASA**.
- La señal: el titular «43 carros permitidos en la app, uno en la puerta» (dos mitades paralelas). Se deja: la cifra es el hallazgo (observado en `inspeccion/diagnostico-inspeccion.md`: 44 registrados, 43 «permitidos», 1 en el sistema físico).
- Tendencia a vigilar: el contraste en dos mitades aparece una vez como señal y tres veces como caso límite (Plataforma, Color, Estructura).
- Observaciones que no son de voz, llevadas a la lámina de revisión:
  - «HikCentral rechazó el registro porque falta el correo. Los Pases no deben crear personas.» suena a regla interna.
  - «Confirmada · Por confirmar» convive con «Vigente · Sin confirmar»; son objetos distintos, pero conviene decidir la pareja a propósito.

**Patrón que el detector nombró y no se corrigió del todo.** Hay titulares en dos mitades paralelas, por ejemplo «Radio 14 en tarjetas, 8 en controles, el arco solo en el Pase». Cada uno lleva datos, pero juntos forman un tic. Se cambiaron tres; quedan varios.

## Cómo repetirlas

1. Reconstruir el sitio: `python3 ../sitio/construir.py`.
2. Regenerar la muestra del detector: `python3 muestras.py`.
3. Lanzar los dos subagentes con los prompts de este archivo.

## Prompts usados

**Lector frío.** «Eres un lector frío: nunca has visto la marca Kino. Tu única fuente es el sitio (`sitio/build/kino-sistema-de-marca.html` y `sitio/texto-visible.md`); no leas otros archivos. Responde 8 preguntas con respuesta, cita exacta y ancla: qué es Kino y para quién, qué problema resuelve, qué es un Pase, cómo va el logo sobre fondo oscuro y su tamaño mínimo, qué color marca un Pase vencido, cómo suena un WhatsApp de Kino, dónde se descargan los tokens, quién decide sobre la marca. Califica la claridad de 1 a 5, da la media y hasta 5 observaciones con ancla.»

**Detector de IA.** «Lee solo `verificacion/muestras-detector.md`. Por sección, marca los textos que suenan escritos por IA con una señal concreta (antítesis, tríadas por inercia, frases de largo uniforme, léxico vacío, cierres enfáticos, arranques publicitarios, abstracciones sin objeto, simetrías, dos puntos de revelación, la marca hablando de sí misma). No marques lo formal, técnico u operativo. Cita el fragmento y propone una reescritura. Aparte, el microcopy. Cierra con el total, las secciones con más de una señal y los patrones.»
