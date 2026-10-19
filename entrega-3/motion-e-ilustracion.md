# Motion e ilustración de Kino · 19 oct 2026

Estado: **PROPUESTA** (decisiones.md E3-8). Desarrolla E3-1 (biopunk, aprobada) y no toca tokens aprobados.

## Por qué se rehízo
La animación del lector era una espiral de 14 trazos curvos con el mismo desfase. No correspondía a ningún proceso biológico ni a una regla de la marca: era forma orgánica sin mecanismo, lo que la investigación llama biomorfismo cosmético. El inventario del prototipo encontró además cinco contradicciones con la marca:
- latidos infinitos, cuando el token permite 3 ciclos (`latirCiclos: 3`, WCAG 2.2.2);
- un spinner en la espera del lector, que la regla 5 de `@kino/motion` prohíbe;
- un movimiento reducido que apagaba todo, cuando la regla 6 dice «reducido no es apagado»;
- fondos que se movían sin cambiar ningún dato: micelio, membrana y quitina giratoria;
- la nota de confirmación sin el movimiento que pide la partitura.

## Las reglas, con su fuente

| # | Regla | Fuente |
|---|---|---|
| 1 | El veredicto del lector se lee en el primer cuadro. El color y la palabra no esperan a ninguna animación; lo que se mueve después explica el cambio | Nielsen (0,1 s); Apple HIG Motion («don't make people wait»); Baudisch y otros, Phosphor (UIST 2006) |
| 2 | «Puede entrar» y «No entra» usan tres canales: color, ícono de forma distinta y palabra | WCAG 2.2 · 1.4.1; MIL-STD-1472 |
| 3 | Estado continuo y evento se mueven distinto. Vigente brilla quieto; el reconocimiento es un destello | Bioluminiscencia de hongos, continua (Oliveira y otros, 2015) frente al destello de *Noctiluca* (Nicol, 1958) |
| 4 | Nada destella más de 3 veces por segundo; los latidos son 3 y se detienen | WCAG 2.3.1 y 2.2.2; token `latirCiclos` |
| 5 | Nada gira de forma continua. Una espera de menos de 10 s lleva texto, no un spinner | Nielsen; regla 5 de `@kino/motion` |
| 6 | Nada se mueve si no cambia un dato | Apple HIG; Zawojski (2025) sobre la imagen tipo salvapantallas |
| 7 | En portería no hay rebote ni sacudida. Contracción rápida y recuperación lenta | Material 3 (resortes de efectos sin rebote); *Mimosa pudica*, cierre en menos de 1 s y recuperación en ~20 min |
| 8 | Lo frecuente se anima menos que lo ocasional. Crear un Pase puede tener un momento; cada lectura de portería es sobria | Apple HIG; NN/g, duración de la animación |
| 9 | Movimiento reducido: escala, giro y desplazamiento pasan a fundido de 240 ms o menos; los latidos se detienen; ninguna información vive solo en la animación | MDN `prefers-reduced-motion`; WCAG 2.3.3; Apple, Reduce Motion |
| 10 | Ilustración solo donde hay una necesidad real: primer uso, estado vacío y explicar la integración. Nunca en un rechazo ni en el veredicto | GOV.UK Design System, imágenes; Polaris; Carbon, estados vacíos; Primer |
| 11 | Se traslada el ritmo y la proporción del proceso, comprimidos en el tiempo; nunca gore literal ni biología disputada | Berry (WEHI); Iwasa; Karst y otros (2023) sobre la red micorrícica |

## Catálogo

| Momento | Proceso real | Cómo se ve en Kino | Tokens | Reemplaza |
|---|---|---|---|---|
| **El lector reconoce** (portería) | Sinapsis inmunológica: el linfocito se detiene en seco y los receptores migran al centro en anillos concéntricos | El barrido de la ventana se detiene. Tres anillos convergen hacia la ventana del lector y forman una diana que queda mientras la talanquera está arriba. Antes, un destello de 120 ms | `tarjeta` 820 ms + `crecer`, cascada de 90 ms | La espiral |
| **Puede entrar** | Destello por estímulo (*Noctiluca*: sube 43 ms, cae 80 ms) | El panel ya está verde en el primer cuadro. Un destello sale del punto de lectura y deja un brillo quieto | `instante` 120 ms | La ola de 820 ms que retrasaba el color |
| **No entra** | *Mimosa pudica*: cierre rápido, recuperación lenta | El panel ya está rojo. Se contrae un 1,5 % en 120 ms y se recupera en 900 ms. La luz roja late dos veces y se detiene | `instante` + `decaer` | La sacudida horizontal |
| **Sin confirmar** | Quorum sensing: la señal se acumula sin efecto visible hasta un umbral | Punto hueco quieto, borde punteado quieto, texto «Esperando al lector…». Nada gira | — | El punto que giraba y la barra que fluía |
| **Confirmado → Vigente** | Al cruzar el umbral la luz se enciende de golpe; latido asimétrico (sístole ⅓ del ciclo) | Destello de encendido, tres latidos con sístole corta y luego brillo quieto. La nota sube (partitura) | `latir` 1800 ms × 3 | El latido infinito |
| **Vigente** | Hongos luminiscentes: luz verde continua, sin parpadeo | Brillo quieto en el borde del Pase y del Portal | — | `respira`, `pulso-tejido` |
| **Por vencer** | Fatiga de la bioluminiscencia: misma forma, menos amplitud | El brillo baja en proporción al tiempo que queda; con 10 % de aviso restante apenas brilla | — (dato del reloj) | Brillo fijo |
| **Vencido** | Senescencia: el verde cae y aparecen los amarillos que estaban debajo | Se apaga con `decaer` y queda un tono cálido desaturado | `decaer` 900 ms | Igual, con tinte cálido |
| **Revocado** | Hemostasia: un corte, un cierre y una cicatriz que persiste | Corte seco y cicatriz punteada que queda. Igual que hoy: «caducar lento, revocar seco» | `corto` + `revocar` | — |
| **Crear un Pase** | Germinación: la espora se hincha pareja y luego crece por la punta, a pulsos | La tarjeta nueva se hincha de 0,94 a 1 y la barra de vigencia crece desde la izquierda en tres pulsos | `tarjeta` + `crecer` | El círculo con desenfoque |
| **Integración** (administración) | Red de *Physarum* (Tero y otros, 2010): los tubos se engrosan con el flujo y se secan sin él | Diagrama Kino → HikCentral con dos tubos, personas y vehículos. El grosor es la proporción sincronizada. Refugio: tubo seco, punteado. Al reintentar, el tubo engrosa con los contadores | transición del grosor | La barra sola |
| **Fondo** | — | Micelio quieto, dibujado una vez; membrana y quitina sin movimiento propio | — | Animación continua |

## Ilustraciones

Familia única, construida con la geometría del logo (el arco y la gota):
- trazo de 1,7 px con puntas redondas (X6);
- dos o tres colores, menos saturados que la interfaz;
- sin sombras, sin personas y sin candados, escudos ni muros;
- el arco solo cuando la ilustración muestra un Pase (X8).

| Dónde | Qué muestra | Por qué hace falta |
|---|---|---|
| Ingreso (primer uso) | La membrana: un borde orgánico con una abertura y la gota que pasa | Kino es una membrana, no un muro (marca); reemplaza al micelio animado |
| Tus Pases, sin Pases vivos | El arco vacío, con el borde punteado del Pase que todavía no existe | Primer uso y estado vacío (Polaris, Carbon) |
| Avisos, sin avisos | El arco con la gota en el umbral y el rastro punteado de la llegada | Explica qué va a llegar aquí |
| Chat de la visita, sin Pase | El arco punteado | Estado vacío de la visita |
| Lector e integración | La red Kino → HikCentral | Explicar dónde está caída la integración (GOV.UK: solo con necesidad real) |

**No llevan ilustración:** el rechazo, el veredicto de portería, los errores de sincronización y los diálogos. Ahí van el ícono y el texto con la acción (Primer).

## Lo que queda para Nico
1. Aprobar el catálogo (E3-8).
2. Llevar los tokens nuevos a `@kino/motion`: `instante` ya existe; faltan `destello` (43 + 80 ms) y la curva de sístole.
3. Pasar las ilustraciones a la librería de Figma.

## Fuentes
- Apple, Human Interface Guidelines: Motion y Accessibility.
- IBM Carbon: motion, coreografía, estados vacíos y pictogramas.
- Material 3: tokens de resorte (androidx). Fluent 2: duraciones.
- W3C, WCAG 2.2: 1.4.1, 2.2.2, 2.3.1, 2.3.3 y técnica C39. MDN: `prefers-reduced-motion`.
- Nielsen (1993), tiempos de respuesta. NN/g, duración y usabilidad de la animación.
- Heer y Robertson (2007), transiciones animadas. Baudisch y otros (2006), Phosphor.
- GOV.UK Design System, imágenes. Shopify Polaris, ilustraciones y estados vacíos. Primer, estados vacíos.
- Dustin y otros (1997, PNAS), sinapsis inmunológica.
- Nicol (1958) y Eckert (1967), destello de *Noctiluca*.
- Oliveira y otros (2015), bioluminiscencia de hongos.
- Tero y otros (2010, Science), red de *Physarum*.
- Literatura sobre *Mimosa pudica* (APS 2024) y germinación de hifas (PMC3563291).
- Karst y otros (2023), red micorrícica.
- Zawojski (2025), crítica de Refik Anadol.
