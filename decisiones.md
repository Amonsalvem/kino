# Decisiones · Sistema de marca Kino

Registro único de decisiones de marca. Cada una dice qué se propuso, qué alternativas se consideraron, por qué y en qué estado está.

**Estados**
- **APROBADA**: decidida.
- **PROPUESTA**: lo construido sobre ella se rehace si cambia.
- **REVERTIDA**: se deshizo.
- **HEREDADA**: viene del borrador del 23 sep. No está entre las decisiones firmes del encargo, así que se trata como propuesta y se revisa en su parada.

Última actualización: 25 sep 2026, respuesta de Nico a la Parada 4.

---

## Decisiones firmes del encargo (APROBADAS)

| # | Decisión | Fuente |
|---|---|---|
| F1 | El logo se conserva: bloque cuadrado con arco interior y gota, más el logotipo «KINO». Puede recolorearse | Encargo de Nico, 23 sep |
| F2 | Dirección estética: biopunk | Encargo |
| F3 | El objeto que recibe el invitado o colaborador se llama «Pase», nunca «permiso» | Encargo |
| F4 | Kino tiene identidad propia y no es marca blanca. Un conjunto aparece solo como dato, en texto o chip, sin logo ni colores | Encargo |
| F5 | Perfil de tono NN/g: formalidad 2, humor 1, respeto 1, entusiasmo 2 | Encargo; `voz.json` |
| F6 | Tuteo en la app, con residente y visitante. Con la administración queda abierto hasta la Parada 2 | Encargo |
| F7 | El motion no se sacrifica. Se optimiza con GPU, carga diferida y pausa fuera de pantalla. Reduced-motion es un modo alternativo | Encargo |
| F8 | Nada existente se borra. En Figma, el contenido actual pasa a «Referencias» | Encargo, regla 13 |

## Heredadas del borrador (se revisan en su parada)

| # | Decisión | Se revisa en | Nota |
|---|---|---|---|
| H1 | Tema oscuro canónico; el claro es el segundo | Parada 3 · Nico autorizó reajustar los pasos del oscuro para pasar APCA (23 sep) | Choca con la regla APCA 5: en oscuro fallan el texto secundario (Lc 71,8), el tenue (49,2), los textos de estado (62,9 a 71,8) y los bordes (23 a 24). Ver `auditoria.md` §2.1 |
| H2 | Acento `#00BB83` y regla de tamaño sobre acento (18 px en 700) | Parada 3 | — |
| H3 | El acento significa otorgar: botón que da el Pase, Pase recién emitido y la marca | Parada 3 | El chip de evidencia «Prueba» del borrador lo usaba. En el sitio nuevo ya no |
| H4 | El color solo nombra hechos confirmados; sin-confirmar va sin relleno y con borde discontinuo | Parada 3 | Coincide con el valor «Estado honesto» (P07) |
| H5 | Archivo y JetBrains Mono, las dos OFL | Parada 3 | — |
| H6 | Verbos de movimiento: crecer, decaer, revocar, latir y cascada, con 17 tokens | Parada 3 | — |

---

## Parada 1 · Plataforma y arquitectura

### P01 · Formato del sitio: una sección por vez · APROBADA (Nico, 23 sep: «todo lo demás es aprobado»)
- **Qué:** un solo HTML con rutas por ancla (`#plataforma.problema`). Muestra una sección a la vez; las demás no pintan ni animan.
- **Alternativas:**
  - (b) una página larga con todo el contenido;
  - (c) láminas, como el borrador.
- **Por qué:**
  - cumple el ancla profunda por subsección y las ≤ 2 interacciones;
  - al no pintar lo que no se ve, el motion completo de la sección activa no compite con el resto (F7);
  - (b) pesa y obliga a pausar a mano;
  - (c) sirve para presentar, pero no deja enlazar una regla.
- **Justificación de plataforma:** el valor «Constancia» exige poder citar una regla con enlace.

### P02 · Dos puertas desde el inicio · APROBADA (Nico, 23 sep: «todo lo demás es aprobado»)
- **Qué:**
  - «Conocer Kino» es un recorrido de 5 paradas;
  - «Usar la marca» es el mapa de las 12 secciones.
- **Alternativas:**
  - (b) dos sitios separados;
  - (c) una sola entrada con filtros por perfil.
- **Por qué:** una sola fuente con dos órdenes de lectura. (b) duplica contenido y se desincroniza.
- **Justificación:** dos compradores distintos, la administración (audiencia A) y quien produce piezas (audiencia B).

### P03 · Índice en cuatro grupos · APROBADA (Nico, 23 sep: «todo lo demás es aprobado»)
- **Qué:** Fundamentos (01–02), Identidad (03–09), Aplicación (10–11), Operación (12), más Consulta (glosario).
- **Alternativa:** una lista plana de 12.
- **Por qué:** los grupos siguen el orden de construcción de una pieza: por qué, cómo suena, cómo se ve y dónde se aplica.

### P04 · Posicionamiento · APROBADA (Nico, 23 sep: opción A)
- **Propuesta (A):** «Para la administración de un conjunto cerrado que ya tiene lectores de placa, rostro y talanquera, Kino es el sistema de acceso donde el residente le entrega un Pase con hora de vencimiento a quien espera, dentro de los límites que fija la administración, y el lector instalado lo aplica sin crearle una cuenta a la visita.»
- **Alternativas:**
  - (B), centrada en el residente: «Kino le devuelve al residente la decisión de quién entra a su casa». Se descarta porque Neivor ya vende autonomía del residente (P12 de la auditoría).
  - (C), centrada en la constancia: «Kino es el registro de quién autorizó cada ingreso y hasta cuándo». Es fuerte ante el consejo, pero no nombra el hardware ni la visita sin cuenta.
- **Por qué A:**
  - habla a quien compra;
  - se apoya en la prueba más fuerte que hay (Villas: 887/888 y 757/757 sincronizados);
  - nombra los tres rasgos que las alternativas no reúnen.
- **Riesgo:** «sin cuenta» no tiene prueba técnica todavía (bloqueante 1 del maestro). Se muestra marcado como pendiente.

### P05 · Promesa · APROBADA (Nico, 23 sep: «todo lo demás es aprobado»)
- **Qué:** «Cada persona que entra lleva un Pase con el nombre de quien se lo dio y la hora en que vence. Kino dice "vigente" solo cuando la puerta lo confirmó.»
- **Alternativa:** una versión corta, «Cada ingreso con autor y hora de salida».
- **Por qué:** la larga incluye el estado honesto, que responde a los 43 carros permitidos que la puerta no conocía. La corta queda para piezas de espacio reducido.

### P06 · Personalidad: Exacto, Franco, Discreto · APROBADA (Nico, 23 sep)
- **Alternativa:** Exacto, Sereno, Cercano.
- **Por qué:**
  - «Franco» responde a la app que afirmaba «Permitido» sin confirmación;
  - «Discreto» responde a las 312 cédulas a la vista y a la SIC;
  - «Sereno» y «Cercano» no apuntan a ningún hallazgo.

### P07 · Valores con comportamiento · APROBADA (Nico, 23 sep: «todo lo demás es aprobado»)
- **Qué:** cinco valores, cada uno con la conducta que lo prueba:
  - Decide quien conoce;
  - Topes a la vista;
  - Constancia;
  - Datos mínimos;
  - Estado honesto.
- **Alternativa:** tres valores abstractos (confianza, cercanía, control). Se descarta: ninguno se verifica mirando el producto.
- **Justificación de plataforma:** cada valor responde a un hallazgo de la inspección (P01 a P15 en `auditoria.md`) y se comprueba mirando una pantalla. (Línea agregada el 24 sep para la comprobación 8 de la Fase 5; no cambia la decisión.)

### P08 · Arquitectura de nombres monolítica · APROBADA (Nico, 23 sep: «todo lo demás es aprobado»)
- **Qué:**
  - superficies: Kino, Kino Administración, Kino Portería;
  - objetos: Pase, Cuenta, Acceso previsto, Límites, Constancia;
  - modos: QR, Placa, Código.
- **Alternativas:**
  - (b) submarcas: Kino Casa, Kino Puerta, Kino Pass;
  - (c) nombres descriptivos sin Kino.
- **Por qué:**
  - una marca pequeña no sostiene submarcas;
  - (b) mete inglés y nombres que hay que aprender;
  - (c) pierde la marca en portería, donde la ven visitantes de todos los conjuntos.

### P09 · Manifiesto · APROBADA (Nico, 23 sep: «todo lo demás es aprobado»)
- **Qué:** cinco párrafos cortos anclados en una casa (la 14) y dos ingresos concretos.
- **Alternativa:** un manifiesto en primera persona plural («Creemos que…»). Se descarta por la regla 10 (arranques prohibidos).
- **Justificación de plataforma:** la promesa (P05) contada con un caso: cada frase tiene un objeto, una hora o una casa, como pide la regla 9. (Línea agregada el 24 sep.)

### P10 · El problema se cuenta con datos del conjunto piloto · APROBADA (Nico, 23 sep: se puede nombrar Monte Sereno y mostrar fallas con cifras)
- **Qué:** el sitio nombra Monte Sereno y muestra las cifras de la inspección: la placa inventada, 711 errores, 312 cédulas y 0/312 sincronizados.
- **Alternativas:**
  - (b) anonimizar como «un conjunto en Antioquia»;
  - (c) contar el problema solo con cifras del entorno.
- **Por qué:** es la única evidencia propia.
- **Costo:** expone en público fallas de un sistema en operación que hoy es el MVP. **Pregunta 2 de la Parada 1.**

### P11 · Estados de un Pase · REEMPLAZADA por V5, que es la versión aprobada (Nico, 23 sep: «todo lo demás es aprobado») (se cierra en la Parada 3)
- **Qué:**
  - agregar **usado**, para el código de un solo uso;
  - «pendiente» se escribe «sin confirmar»;
  - «rechazado» reemplaza a «negado» en el texto visible.
- **Alternativa:** mantener «pendiente» como estado propio.
- **Por qué:** «pendiente» sugiere una aprobación que el producto no tiene. H2 del diagnóstico: no hay cola de aprobación de ingresos.

### P12 · Tema del sitio · APROBADA (Nico, 23 sep: «todo lo demás es aprobado»)
- **Qué:** el sitio abre en oscuro aunque el sistema operativo esté en claro, y el claro se elige con un botón.
- **Alternativa:** seguir el tema del sistema operativo.
- **Por qué:** H1 (oscuro canónico). Depende de la Parada 3.

### P13 · Tratamiento en el sitio de marca · APROBADA (Nico, 23 sep: «todo lo demás es aprobado»)
- **Qué:** tuteo, de persona del equipo a persona del equipo (regla 8).
- **Alternativa:** impersonal («se usa», «se recomienda»).
- **Por qué:** la regla 8 pide explicar como alguien del equipo; el impersonal alarga las frases.

### P14 · Figma reorganizado en 15 páginas · APROBADA por el encargo (ejecutada el 23 sep)
- **Qué:**
  - se crearon 15 páginas espejo;
  - el contenido de las 8 páginas anteriores pasó a «Referencias», cada página en su propia sección «Ref · …»;
  - se quitaron las páginas que quedaron vacías.
- **Qué no cambió:** ningún nodo, variable ni estilo se borró.
- **Cómo revertir:** mover cada sección de vuelta a una página nueva.
- **Por qué:** el encargo pide que la librería espeje la arquitectura del sitio (sección <figma>) y que nada se borre (regla 13). (Línea agregada el 24 sep.)

### Estado tras las respuestas del 23 sep
- Aprobadas: P04 (A), P06, P10; permiso para reajustar los pasos del tema oscuro en la Parada 3.
- **Sin respuesta**: pregunta 5 (P01, formato de una sección por vez y modo presentación). Sigue PROPUESTA y se vuelve a preguntar en la Parada 2.
- P02, P03, P05, P07, P08, P09, P11, P12 y P13 no se preguntaron una por una. Siguen PROPUESTA; la Fase 2 se construye sobre ellas y se rehace lo que cambie.

---

## Parada 2 · Verbal

### V1 · Tratamiento con la administración: usted · APROBADA (Nico, 23 sep)
- **Alternativa:** tú en todo Kino.
- **Por qué usted:** en Antioquia es la forma cotidiana de respeto con un cliente. La administración paga y responde ante un consejo.
- **Costo:** Kino habla de dos maneras. La regla evita que se mezclen:
  - tú con el residente y la visita;
  - usted con la administración, en el panel, los correos y lo comercial.

### V2 · «Pase» con mayúscula · APROBADA (Nico, 23 sep)
- **Alternativa:** «pase» en minúscula, como pide la RAE para sustantivos comunes.
- **Por qué:** distingue el objeto de Kino del «pase» genérico y lo vuelve reconocible en un WhatsApp de alguien que no conoce Kino.

### V3 · Horas: 12 h en texto, 24 h en datos · APROBADA (Nico, 23 sep)
- **Alternativa:** 24 h en todo.
- **Por qué:** «9:00 p. m.» es como se dice la hora en Colombia. En tablas y constancias, «21:00» en mono alinea las cifras.

### V4 · «Visita» en la interfaz · APROBADA (Nico, 23 sep)
- **Alternativas:**
  - «invitado»;
  - «visitante».
- **Por qué:** un técnico no es un invitado. «Visita» es el tipo de Pase y se lee natural en «¿Quién viene?».

### V5 · Nombres de estado · APROBADA (Nico, 23 sep) (el color se decide en la Parada 3)
- **Estados de un Pase:**
  - Previsto
  - Sin confirmar
  - Vigente
  - Por vencer
  - Usado
  - Vencido
  - Revocado
- **Evento en la entrada:** Rechazado, con su motivo.
- **Alternativa:** los seis del borrador (vigente, por vencer, vencido, negado, sin confirmar, identidad).
- **Por qué:**
  - «usado» cierra el código de un solo uso;
  - «revocado» y «vencido» se separan, porque uno tiene autor y el otro no;
  - «previsto» nombra el acceso previsto;
  - «negado» pasa a ser un evento de la entrada;
  - «identidad» marca un dato, no un estado del Pase.

### V6 · Patrones nuevos en voz.json · APROBADA (Nico, 23 sep)
- **Qué:** 28 patrones nuevos, 10 de gravedad error. Salen de la regla 10 y de calibrar contra las 42 frases.
- **Resultado:**
  - calibración 40 de 42 (antes 21), con 0 falsos positivos;
  - 11 de 11 frases de IA de prueba atrapadas;
  - 0 hallazgos sobre el sitio, los textos de la app y las muestras.
- **Por qué:** la regla 10 del encargo exige que esos patrones no aparezcan; la calibración contra las 42 frases mide que el filtro los atrape sin marcar textos correctos. (Línea agregada el 24 sep.)
- **Descartados por dar falsos positivos:** «invitado», «lo que sí» y la triple negación. «Invitado» vuelve si se aprueba V4 y se corrigen las frases de referencia.
- **Otros ajustes:**
  - «permiso» sube a error;
  - DANE, GEIH, OTP, ISO, RAE, COP y PENDIENTE pasan a las siglas permitidas.

### Estado tras la respuesta del 23 sep (noche)
- Nico: «todo lo demás es aprobado».
  - Quedan APROBADAS las propuestas de la Parada 1 y V1 a V6.
  - P01 se aprueba como una sección por vez, sin modo presentación. Si se quiere proyectar, se pide aparte.
- Pregunta 4 de la Parada 2 (cómo se ingresa el código en la entrada): es un dato, no una decisión. Queda el texto «Dile a portería el código» y [PENDIENTE: confirmar si el lector tiene teclado].

## Nueva dirección · 23 sep

### V7 · El Pase se entrega con la identidad de Kino y con poca carga · APROBADA (Nico, 23 sep: «imagen más enlace»)
- **Pedido de Nico:**
  - menos carga cognitiva al interactuar con el usuario;
  - que el Pase entregado (QR o código) tenga la estética de Kino, por ejemplo en PDF.
- **Propuesta:**
  - el WhatsApp lleva una sola frase (quién, cuándo y «muéstralo en la entrada»);
  - el Pase llega como **imagen** de cabecera con la identidad de Kino: QR, código, placa, vigencia y quién lo otorgó;
  - un enlace abre el **Pase vivo**, que dice si sigue vigente;
  - el PDF queda como descarga opcional desde el Pase vivo, para imprimir o para quien no usa WhatsApp.
- **Alternativas:**
  - (b) el PDF como adjunto principal;
  - (c) solo el enlace.
- **Por qué no el PDF como principal:**
  - hay que tocarlo, esperar a que abra y hacer zoom para mostrar el QR;
  - un PDF no cambia cuando el Pase vence o se revoca, y choca con el valor «Estado honesto»;
  - WhatsApp muestra la imagen en la conversación sin abrir nada.
- **Por qué no solo el enlace:** depende de datos móviles en la entrada.
- **Efecto:** las plantillas de visita y colaborador bajan de 41 y 42 palabras a 23 y 28. El diseño del Pase (imagen, página viva y PDF) entra a la exploración de la Parada 3.

---

## Parada 3 · Identidad visual (propuestas, 23 sep)

Lámina: `kino/parada-3.html`. Fuentes: `branding/sistema/v3/fase3/`. Contraste medido con la fórmula APCA-W3 0.1.9, que reproduce los valores de `reportes/contraste.json`.

| # | Elemento | Propuesta (A) | Alternativa (B) | Responde a |
|---|---|---|---|---|
| X1 | Forma del Pase | Portal: el QR dentro del arco del logo; imagen, Pase vivo y PDF en claro | Boleto con talón | V7; reconocimiento de marca por quien no conoce Kino |
| X2 | Logo | Bloque en hueso y gota en #00BB83 | Marca completa en acento | H3: el acento significa otorgar |
| X3 | Color | Oscuro reajustado (texto secundario #CEDBD6, tenue #A5C7B8, borde #6E8E81, estados con texto Lc ≥ 75 y borde Lc ≥ 30) | Claro canónico | Regla APCA 5; H1 |
| X4 | Acento de acción | #00BB83 para la marca y #00D595 para el botón Crear Pase (texto Lc 67) | #00D595 en todo | Regla APCA 5: #00BB83 da Lc 55 con texto oscuro |
| X5 | Tipografía | Archivo al 112 % en titulares y JetBrains Mono con cero barrado | Archivo al 100 % | Exacto: placa y código legibles |
| X6 | Iconografía | Trazo 1,7 con puntas redondas | Trazo 2 con puntas rectas | Curvas del logo |
| X7 | Imagen | Aurora bioluminiscente en pantalla; tejido celular solo en impresos grandes; sin fotos de personas | Tejido celular en todo | Discreto; el QR necesita un fondo liso |
| X8 | Estructura | Radio 14 y arco solo en lo que es un Pase | Radio 4, sin arco | El arco significa «esto es un Pase» |
| X9 | Motion | Crecer (820 ms, cascada de 90 ms); cortina solo en presentaciones | Cortina | Verbo «aparecer» del sistema de movimiento |
| X10 | Estados | 7 estados y el evento Rechazado, con los colores de la tabla de la lámina | — | V5 |

Estado: **todas APROBADA (A)** · respuesta de Nico a la Parada 3, 24 sep:

1. X1 Portal como forma del Pase: aprobado.
2. X4 dos verdes (#00BB83 marca, #00D595 botón Crear Pase): aprobado.
3. X3 oscuro reajustado como tema principal: aprobado. El PDF del Pase va en claro.
4. X2, X5, X6, X7, X8 y X9 en bloque: aprobado. X10 queda aprobada con ellas.
5. Pase vencido en la entrada: ver X11.

### X11 · Pase vencido en la entrada · APROBADA (24 sep)
- **Dato de operación (dicho por Nico):** portería puede llamar al residente desde Kino.
- **Efecto:** la señal de portería y el Pase vivo en estado vencido ofrecen «Llamar al residente». El texto puede prometer esa llamada.
- **Por verificar en producto:** la inspección no registró un botón de llamada en la vista del portero. Si la función no existe hoy, es un requisito de producto que el sistema de marca da por hecho y hay que construir.
- **Trazabilidad:** la llamada no autoriza el ingreso. Si el residente quiere dejar entrar a la persona, crea un Pase nuevo o extiende el vencido. Así cada ingreso sigue teniendo un Pase con autor, y HikCentral recibe el alta con su vigencia.

---

## Parada 4 · Sistema completo (propuestas, 25 sep)

Lámina: `kino/parada-4.html` (https://claude.ai/artifact/DBF7w1VTGPtJ9oQwdz4tXa).

### F4-P1 · Llamada desde el Pase vivo vencido · APROBADA (Nico, 25 sep: opción A)
- **Qué está construido:** el Pase vivo en estado Vencido, que ve la visita, muestra el botón «Llamar al residente», igual que la vista de portería (X11).
- **El problema:**
  - X11 aprobó la llamada desde portería.
  - En el Pase vivo el botón lo toca la visita. Si abre una llamada normal, la visita ve el número del residente: un dato personal expuesto a alguien sin cuenta.
  - La inspección no registró ninguna función de llamada.
- **Propuesta (A):** quitar el botón del Pase vivo. El aviso queda: «Tu Pase valía de 2:00 a 6:00 p. m. y son las 7:10 p. m. Pídele uno nuevo a Carolina o pide en portería que la llamen.» La llamada queda solo en portería.
- **Alternativa (B):** mantener el botón con llamada enmascarada. Kino conecta a la visita con el residente sin mostrar el número. Es una función nueva de producto, con un proveedor de telefonía por elegir y un costo por llamada.
- **Por qué A:**
  - no promete una función que no existe (regla «Prometedores» de la voz);
  - no expone el número;
  - el camino sigue siendo el mismo: el residente crea un Pase nuevo.
- **Trazabilidad y HikCentral:** ninguna de las dos autoriza el ingreso. En las dos, entrar exige un Pase nuevo o extendido, con autor, que se sincroniza a HikCentral con su vigencia. B además obliga a guardar un registro de cada llamada: quién llamó, a quién y cuándo.
- **Si se aprueba A:** cambian `sitio/deptos/pase.py` (función `vivo`) y `pase/construir.py`, y se rehacen `pase-vivo-vencido.png` y la sección Aplicaciones del sitio.

### F4-P2 · Aviso de llegada al residente · APROBADA (Nico, 25 sep: opción A)
- **El conflicto:**
  - El inventario de UX writing de la Parada 2 incluye el estado «Aviso de llegada»: «Andrés entró a las 3:12 p. m. con la placa KMN 305.»
  - El campo de WhatsApp dice «Tu WhatsApp sirve para entrar a Kino y para avisarte cuando alguien llega.»
  - `voz.json → hechos` lista «Avisos automáticos cuando el lector confirma una placa» como **no confirmado**, así que la regla de voz prohíbe prometerlo.
  - Observado en la inspección: el aviso no existe hoy.
- **Propuesta (A):** tratar el aviso como requisito de producto y conservar los dos textos, marcados en el inventario con «requiere el evento del lector». Pasa a «confirmado» en `voz.json` cuando exista, y ningún texto sale a producción antes.
- **Alternativa (B):** quitar la promesa hasta que el producto la tenga. El campo dice «Tu WhatsApp sirve para entrar a Kino.» y el estado «Aviso de llegada» sale del inventario.
- **Por qué A:** el aviso responde al núcleo del diagnóstico. El residente otorga el Pase pero hoy no sabe si la persona entró; el aviso le da ese conocimiento sin pasar por portería.
- **Trazabilidad y HikCentral:**
  - El aviso sale del evento de paso del lector, ligado al Pase. Por verificar: que HikCentral entregue ese evento a Kino.
  - Con la integración caída, como en Refugio Campestre, no hay evento. El Pase sigue «Sin confirmar» y no se envía aviso, lo que es coherente con «Estado honesto».

### F4-P3 · Ícono de estado en el chip de Usado, Vencido y Revocado · APROBADA (Nico, 25 sep: opción B)
- **Origen:** el lector frío notó que Vencido y Usado solo se distinguían por el tono del texto y la palabra.
- **Decisión:** en esos tres estados, el punto del chip se cambia por el ícono del estado (`usado`, `vencido`, `revocado`, trazo 1,7). Los otros estados conservan el punto.
- **Alternativa descartada:** (A) dejar solo la palabra.
- **Efecto:** cambia el componente Estado en código (`capa-componentes.css`, `deptos/comun.py → chip`) y en Figma. No cambia el color ni los tokens.

### F4-P4 · La identidad de marca aplicada al propio sitio · APROBADA (Nico, 25 sep: opción A)
- **Pedido de Nico (25 sep):** el sitio se lee monótono porque usa dos colores. Aprovechar la identidad ya aprobada dentro del mismo documento.
- **Propuesta:**
  - aurora (X7) en la portada y en la apertura de cada sección;
  - índigo en enlaces y en la navegación, que es lo que la familia significa (profundidad y enlaces);
  - la gota del logo marca la sección activa del índice y numera las secciones;
  - capas de superficie (abismo, elevada, membrana) para separar bloques, con el relieve de membrana;
  - los estados, el ámbar y el violeta siguen solo en lo que significan.
- **Por qué:** el sitio es la primera pieza de Kino que ve una administración o un aliado. Si se lee monótono, contradice la identidad que describe. Aplica recursos ya aprobados en su uso aprobado: X7 pone la aurora en portadas y la familia índigo significa profundidad y enlaces.
- **Qué no cambia:** el verde #00D595 sigue solo en el botón que crea un Pase; el arco sigue solo en el Pase; todo texto nuevo sobre aurora se mide con APCA.
- **Resultado:** aprobada tal como se construyó (aurora en portada y en cada apertura).

### Estado tras la respuesta del 25 sep
1. **Versión 1.0.0:** aprobados los tokens, el sitio y las piezas del Pase. **La librería de Figma y lo que se exporta de ella no se aprueba**: se revisa el auto-layout y el espaciado de todas las páginas.
2. F4-P2: opción A.
3. F4-P1: opción A.
4. Vencido y Usado: opción B, ver F4-P3.
5. Detector de IA: opción B, se autoriza un cuarto ciclo.
6. Pedido nuevo: F4-P4.
7. El artefacto oficial sigue sin republicarse: la Parada 4 no queda cerrada mientras Figma y F4-P4 esperan revisión.

### F4-P5 · Pantallas con la jerarquía del Pase · APROBADA (Nico, 25 sep: opción A)
- **Pedido de Nico (25 sep, al aprobar Figma):** las pantallas cargan mucho: toda la información tiene el mismo peso y se vuelve difícil de leer. La distribución, el color y la jerarquía de las piezas del Pase funcionan; aplicarlas a las pantallas.
- **Qué se toma del Pase:**
  - un dato manda por pantalla (el nombre, o el código) en Archivo grande;
  - rótulos cortos en JetBrains Mono, mayúsculas pequeñas, encima de su valor;
  - la vigencia en el color de su estado, en monoespaciada;
  - datos agrupados en bloques con aire entre ellos, en vez de una columna pareja;
  - la monoespaciada solo para datos (hora, placa, código, teléfono), no para nombres;
  - una sola acción principal por pantalla.
- **Qué se quita:** textos que repiten lo obvio (por ejemplo «otorgó Carolina Ruiz» en la lista de la propia Carolina) y ayudas que se pueden decir en una línea.
- **Por qué:** responde a la personalidad «Exacto» (P06) y al valor «Topes a la vista»: el dato que decide un ingreso se lee primero. La aurora solo va en la pantalla de inicio, como fija X7.
- **Propuesta (A, construida en el sitio y en Figma):** cinco niveles, iguales en las cinco pantallas.

  | Nivel | Qué lleva | Cómo se ve |
  |---|---|---|
  | 1 · Manda | El nombre, el código o el límite | Archivo 800 ancho, lo más grande de la pantalla |
  | 2 · Vigencia | Cuándo vale el Pase | Mono en el color de su estado; en Crear Pase, en texto primario porque aún no hay estado |
  | 3 · Rótulo | Placa, Código, Vigencia | Mono pequeño en mayúsculas, texto secundario, encima del valor |
  | 4 · Grupo | Lo que se decide junto | Superficie elevada, radio 14 |
  | 5 · Acción | Una principal, abajo | Verde solo si crea un Pase; revocar va en texto |

  - **Lista (inicio):** aurora arriba con «Tus Pases» y el conteo. Los Pases se agrupan en «Ahora» y «Próximos» en vez de pestañas. Cada tarjeta lleva el tipo como rótulo, sin «Visita» repetido debajo del nombre.
  - **Crear Pase:** nombre y WhatsApp en un bloque; vigencia y placa en otro. El día se elige con tres opciones (Hoy, Mañana, Otro día) y la franja de la administración va en una nota con reloj.
  - **Detalle:** sin «Otorgó Carolina Ruiz · Casa 14», porque es la app de Carolina. Placa y código en grande. «Lo que pasó» como línea de tiempo: los hechos que el lector confirmó llevan punto verde. Extender es el botón; «Revocar Pase» va en texto carmín.
  - **Acceso por código:** el número enmascarado va en mono como dato. El error va en una línea con ícono, sin bloque rojo. «Entrar» pasa al botón secundario, porque X4 reserva el verde de acción para crear un Pase (la 1.1.0 lo tenía en verde).
  - **Límites:** cada límite en su tarjeta con el valor en grande. El resumen de la semana va en cifras, y las rechazadas en su color.
- **Alternativa (B):** la misma jerarquía, pero la lista conserva las pestañas «Activos / Anteriores» de la 1.1.0 en vez de los grupos «Ahora / Próximos».
- **Contraste:** 6 pares nuevos en `pares.json` (vigencia de cada estado sobre la tarjeta, Revocar y el error de código sobre base). 132 mediciones, 0 fallos. Los rótulos pequeños pasan de texto tenue a secundario: el tenue solo está medido para 24 px o más (Lc 65 en oscuro).
- **Anterior:** `_obsoleto/d10_producto-2026-09-25.py` (sitio) y la sección «Pantallas 1.1.0 (anterior)» en la página Pantallas de Figma.
- **Resultado:** aprobada tal como se construyó, con la lista agrupada en «Ahora» y «Próximos» (lámina `parada-4c.html`, https://claude.ai/artifact/NXuGd6VQc7k6Fqqi9pciZZ).

### F4-P6 · Mensaje de alta fallida en HikCentral · APROBADA (Nico, 25 sep: opción A)
- **Qué es la fila:** el inventario de la Parada 2 traduce cada texto que hoy muestra el sistema. Uno es el error que ve el super administrador: «Incorrect request parameter. [email parameter error]», 711 veces (observado, `inspeccion/diagnostico-inspeccion.md`).
- **Lo que Nico señaló (25 sep):** con el Pase, la visita no se registra como persona ni necesita correo, así que ese error no es el problema que Kino resuelve.
- **Lo que dice la inspección:** los 711 errores son `add_person` de todas las personas, no solo de visitas. En Refugio, 0 de 312 usuarios están sincronizados, residentes incluidos.
- **Efecto del diseño actual:** la visita entra con un Pase y no crea una persona. El residente entra con código por WhatsApp y el correo deja de ser obligatorio (inferido de la decisión del ingreso sin contraseña). Con eso, el error del correo desaparece para todos.
- **Propuesta (A, construida):** la fila deja de hablar del correo y queda como el mensaje genérico de un alta que HikCentral no acepta: «HikCentral no aceptó el alta de Carolina Ruiz. Hasta que se corrija, el lector no la reconoce.» Sirve para cualquier falla de sincronización, que sigue siendo posible (Refugio es el caso).
- **Alternativa (B):** quitar la fila del inventario, porque Kino no debería producir ese error.
- **Por qué A:** la integración caída de Refugio muestra que las altas pueden fallar por otras causas. La administración necesita un mensaje que diga a quién afecta y qué pasa en la puerta. Tampoco promete que Kino reintente solo, porque eso no está confirmado.
- **Resultado:** la fila queda como mensaje genérico de alta fallida, tal como se construyó en `sitio/verbal.py`.

### Estado tras la respuesta del 25 sep (segunda vuelta)
1. Librería de Figma: **APROBADA**. Pedido: pantallas con la jerarquía del Pase (F4-P5).
2. F4-P4: **APROBADA** (A).
3. La fila del error de HikCentral se explica y se corrige como F4-P6.
4. Con 1 y 2 aprobadas, la versión 1.1.0 queda aprobada y se republica el artefacto oficial. F4-P5 y F4-P6 van en la 1.2.0.

### F4-P7 · Sitio responsive de 320 a 1920 px · APROBADA (Nico, 25 sep: opción A)
- **Pedido de Nico (25 sep):** «Hazlo completamente responsive», sobre el sitio «Kino · Sistema de marca».
- **Lo que encontró la auditoría** (`scripts/auditar-responsive.mjs`, 16 secciones en 11 anchos):
  - las tablas tenían un ancho mínimo de 704 px y se desplazaban de lado en el teléfono y hasta en 1024 px;
  - la matriz de componentes pedía 1500 px;
  - el mapa de alternativas y el árbol de nombres son SVG de 760 y 820 px: en el teléfono el texto quedaba en 6 px o se desplazaba;
  - la conversación de WhatsApp y el código de Motion se salían a 320 px;
  - columnas con mínimos más anchos que la pantalla y textos de 10 px.
- **Propuesta (A, construida en `sitio/responsive.css`):**
  - las tablas se leen como tabla cuando caben y como fichas cuando el contenedor mide 42rem o menos: cada fila es una ficha y cada celda lleva el nombre de su columna; en 26rem o menos, el nombre va encima del valor;
  - la matriz de componentes pasa a una ficha por componente, con los estados en retícula;
  - en pantallas de 40rem o menos (46rem para el árbol), el mapa y el árbol se muestran en HTML con el mismo contenido: cuatro cuadrantes y una lista por niveles;
  - ninguna columna pide más ancho que el disponible; los rótulos y chips bajan a 11 px como mínimo.
- **Alternativa (B):** conservar las tablas y los SVG como en la 1.2.0, con desplazamiento lateral dentro de su caja.
- **Resultado medido:** 176 vistas sin desborde de página. Quedan a propósito el caso de tipografía «un renglón que no termina» y el texto de las piezas del Pase, que son imágenes a escala.
- **Por qué A:** la administración y el equipo leen el sistema desde el teléfono; una tabla que se desplaza de lado esconde columnas enteras.
- **Resultado:** aprobada tal como se construyó (vista previa 1.2.1, https://claude.ai/artifact/TKafvu7bHfjeKPSYaaKd7S). La versión 1.2.1 queda aprobada y se republica el artefacto oficial.

### Estado tras la respuesta del 25 sep (tercera vuelta)
1. F4-P5: **APROBADA** (A). Pantallas con la jerarquía del Pase y lista en «Ahora» y «Próximos».
2. F4-P6: **APROBADA** (A). Mensaje genérico de alta fallida en HikCentral.
3. Con las dos, la versión 1.2.0 queda aprobada y se republica el artefacto oficial.

### Estado tras la respuesta del 25 sep (1.2.1)
1. F4-P7: **APROBADA** (A). Sitio responsive de 320 a 1920 px.
2. La versión 1.2.1 queda aprobada y se republica el artefacto oficial.

## Motion · curva de trazo (26 sep)
- **Decisión de Nico:** `trazo` usa `duracion/trazo` con `curva/crecer`. Se aplica a `flujo-trazo`, `loader-espera-lector` y `onboarding-3-lector-confirma`. Estado: decidida para el borrador del inventario de motion; el inventario completo sigue sin aprobar.

## Motion 3D · segunda versión de las escenas (26 sep)
Pedido de Nico: subir las tres escenas de Blender a nivel profesional; libertad total en motion. Lámina de revisión: ver `avances.md`. Todas quedan en **PROPUESTA**; la opción A es la construida en `branding/sistema/v3/motion/blender/`.

### M3D-1 · Gestión de color de las escenas · APROBADA (Nico, 27 sep: opción A)
- **A (construida):** vista Standard y curva de tono propia en el compositor para la escena; las marcas de estado (bordes, chip, textos, barra, indicador) escriben la AOV `marca` y pasan sin curva. Medido con `blender/medir.py`: vigente borde, texto y fondo y texto primario salen con ΔE 0.
- **B:** AgX para todo. Más cinematográfico, pero desatura los verdes de estado: `#00EAA5` deja de salir como `#00EAA5`.
- **Por qué A:** estado honesto y colores solo de tokens; el color de un estado es información.

### M3D-2 · Tiempo de la talanquera · APROBADA (Nico, 27 sep: opción A)
- **A (construida):** `resorte/firme` (494 ms, sin rebote). El brazo se flexiona un poco por su inercia y se asienta.
- **B:** token nuevo de mecánica, de 1 a 1,5 s, más cercano a una barrera real.
- **Regla que se cumple en las dos:** la talanquera sube solo después de que el lector confirma.

### M3D-3 · Cámara de la portería · APROBADA (Nico, 27 sep: opción A)
- **A (construida):** llega con `duracion/cortina` y `curva/crecer`, espera la confirmación y avanza al 60 % de ese tiempo (`coreografia/salida-factor`) con `curva/salir`. Faros de un vehículo que no se ve (sin placa ni personas).
- **B:** cámara fija, como en la versión 1 y como la variante reducida.
- **Falta:** no hay token de cámara; A reutiliza tokens que existen.

### M3D-4 · Base de la tarjeta del Pase · APROBADA (Nico, 27 sep: opción A)
- **A (construida en 3D):** `superficie/membrana`, como el recurso Membrana. Implica cambiar `<kino-pase>` en la web, que hoy usa `superficie/elevada`.
- **B:** `superficie/elevada` en los dos. Se cambia el 3D.

### M3D-5 · Textos que cambian con el estado · APROBADA (Nico, 27 sep: opción A)
- **A (construida en 3D):** fundido a través: el texto que sale se va en la primera mitad del verbo y el nuevo llega en la segunda. Se llevaría a `<kino-pase>` y `<kino-estado>`.
- **B:** cambio de golpe, como la web hoy; solo los colores tienen transición.
- **Por qué se propone:** en 3D un fundido cruzado encima los dos textos a mitad de la transición.

### M3D-6 · Aurora en la portería · APROBADA (Nico, 27 sep: opción A)
- **A (construida):** índigo y violeta con un rastro de `biolum/d15`; el único verde de la escena es el indicador confirmado.
- **B:** aurora completa, verde e índigo, como en las portadas (X7).

### M3D-7 · Arco Portal en 3D · APROBADA (Nico, 27 sep: opción A)
- **A (construida):** sin arco. Las escenas muestran la tarjeta de la lista; el arco es del Pase vivo con el QR (X1, X8).
- **B:** sumar una escena del Pase vivo, en claro, con el arco y el QR sobre fondo liso (nunca aurora detrás del QR).

### Estado tras la respuesta del 27 sep (motion 3D)
1. M3D-1: **APROBADA** (A). Vista Standard con curva de tono propia; las marcas de estado salen con el hex de su token.
2. M3D-2: **APROBADA** (A). La talanquera sube con `resorte/firme`, solo después de la confirmación del lector.
3. M3D-3: **APROBADA** (A). La cámara de la portería llega con `duracion/cortina` y `curva/crecer`, espera la confirmación y avanza al 60 % con `curva/salir`; faros sin mostrar el vehículo.
4. M3D-4 a M3D-7: sin respuesta. Siguen PROPUESTA.

### Estado tras la segunda respuesta del 27 sep (motion 3D)
1. M3D-4: **APROBADA** (A). La tarjeta del Pase es `superficie/membrana`. Aplicado en `<kino-pase>` (web) y `PaseKino` (app); la pista de la barra pasa a `superficie/elevada` para verse sobre la membrana.
2. M3D-5: **APROBADA** (A). Los textos que cambian con el estado (chip, dato, nota) se funden a través. La regla vive en el núcleo (`nucleo/textos.ts`) y la usan la web (`fundirTexto`) y la app (`useTextoFundido`).
3. M3D-6: **APROBADA** (A). Sin cambios: la aurora de noche ya es índigo y violeta.
4. M3D-7: **APROBADA** (A). Sin cambios: no hay escena del Pase vivo con arco.
5. Las siete decisiones de motion 3D quedan aprobadas.
- **M3D-4 en Remotion y Lottie (27 sep):** `piezas.tsx` y `generar.py` pasan la tarjeta a membrana y la pista a elevada; heroes, revocado y 28 previews re-renderizados. Las piezas del Pase del sitio oficial (1.2.1) no cambian sin una versión nueva.
- **Queda fuera:** M3D-5 en Remotion y Lottie. Las dos cambian de estado con un fundido cruzado de la tarjeta entera; llevar ahí el fundido a través exige separar fondo y textos en capas.

## Entrega 3 · prototipo navegable (19 oct 2026)

### E3-1 · Exploración biopunk en el prototipo · APROBADA (opción A, Nico, 19 oct)
- **Qué es:** una capa de tema (`prototipo/src/estilos.css`, bloque «Exploración biopunk»). Desde la aprobación va encendida por defecto; la tecla B la apaga para comparar. No toca ningún token aprobado.
- **Rasgos:** el Pase vigente late como tejido; el vencido se marchita (pierde saturación y se deforma); el revocado cicatriza (el corte punteado); el lector reconoce con una sinapsis; el borde del Portal es una quitina iridiscente; micelio vivo de fondo. *El movimiento de estos rasgos lo reemplaza E3-8 si se aprueba.*
- **Por qué:** hoy no existe el acceso temporal para una persona, así que el estado tiene que verse vivo (H1/H5). Cada rasgo nombra un hecho del Pase; ninguno decora.
- **Decidido:** A, adoptar la capa en la app. Pendiente: llevar la capa a tokens y a la librería de Figma con una versión nueva del sistema.

### E3-2 · Vigencia y franjas del Pase · APROBADA con cambio (Nico, 19 oct)
- **Lo que dijo Nico:** sin límite de visitas; Pases con rangos de tiempo amplios a comodidad del residente, porque hay familiares que se quedan meses.
- **Cambia una decisión tomada.** «La administración fija límites (cupos, duración, franjas)» pasa a «la administración fija solo franjas». Se quitan el cupo por casa y la duración máxima. Se señala aquí porque toca una de las decisiones tomadas del proyecto.
- **Quedó así en el prototipo:**
  1. Sin cupo por casa ni duración máxima.
  2. Tres vigencias al crear: Unas horas, Un día y Se queda (3 días, 1 semana, 1 mes, 3 meses o una fecha).
  3. «Estadía» es todo Pase de visita de más de 20 h: entra y sale las veces que quiera hasta su fecha de salida.
  4. ~~La visita de unas horas o de un día queda Usada al entrar~~. Reemplazado por E3-6: toda visita entra y sale mientras su Pase esté vigente.
  5. Extender no tiene tope: +1 h, +1 día o +1 semana; en estadía, +1 semana o +1 mes. Un Pase de un día ya usado no se extiende: se crea otro.
  6. La administración fija dos franjas (visitas de un día y colaboradores) y ve qué Pases activos quedarían fuera; los activos conservan su vigencia.
  7. Portería digita el código en su pantalla; no se asume teclado en el lector. **Confirmado por Nico, 19 oct.**
  8. La vigencia del código es la del Pase. **Confirmado.**
  9. La administración no revoca Pases. **Confirmado.**
  10. El Pase de colaborador se repite sin fecha de fin hasta que el residente lo revoque. **Confirmado.**
- **Efecto en HikCentral:** cada Pase es una persona temporal con «Válido desde / hasta»; una estadía de meses es la misma persona con una ventana larga. **Manuel (19 oct, vía Nico):** al configurar el acceso de una persona o visitante, HikCentral acepta una vigencia de varias décadas, por lo general hasta 2037 o 2099. Ninguna estadía choca con ese tope. Con E3-6 ya no hace falta dar de baja la persona después del primer evento.
- **Efecto en la trazabilidad:** no cambia. Cada Pase guarda autor, casa, motivo y vigencia; sin tope, la constancia es lo que le responde al consejo.
- **Variantes de Figma:** las de cupo agotado (R-P-01, R-P-05) se movieron a «99 Descartes», sin borrarlas.

### E3-3 · Revocar con mantener presionado y deshacer · APROBADA (Nico, 19 oct)
- Reemplaza el diálogo de confirmación de R-P-10. Mantener 0,8 s revoca al instante; «Deshacer» dura 5 s; la baja en HikCentral sale cuando vence el deshacer.
- **Por qué:** el diálogo protege de un toque accidental que el gesto ya evita y deja sin arreglo el arrepentimiento, que es el error común.

### E3-4 · ¿Las franjas aplican a las estadías? · APROBADA (A, Nico, 19 oct)
- **Supuesto del prototipo:** no. Un familiar que se queda un mes entra y sale a cualquier hora.
- **Opciones:** A, no aplican (supuesto actual); B, aplican también a las estadías; C, la administración decide por conjunto.

### E3-5 · Desde cuándo un Pase es estadía · APROBADA (A, Nico, 19 oct)
- **Supuesto del prototipo:** más de 20 h. Por debajo es una visita de unas horas o de un día, que sí respeta la franja (E3-4).
- **Opciones:** A, más de 20 h; B, desde 2 días; C, lo marca el residente con «Se queda», sin umbral de horas.

### E3-6 · La visita de unas horas o de un día entra una sola vez · APROBADA (B, Nico, 19 oct)
- **Supuesto del prototipo:** sí; queda Usada al entrar. Si sale a la tienda, el residente crea otro Pase.
- **Opciones:** A, una sola entrada; B, entra y sale dentro de su vigencia, como la estadía.
- **Efecto en HikCentral:** A pide dar de baja la persona después del primer evento; B solo usa «Válido hasta».
- **Decidido:** B. «No, le dura el tiempo establecido»: la visita entra y sale dentro de su vigencia, igual que la estadía. El estado Usado deja de aplicar a las visitas; la traza guarda cada entrada.
- **Efecto en la trazabilidad:** cada lectura queda en la traza del Pase y en la bitácora de portería, con hora y modo. Antes la segunda lectura quedaba como rechazo; ahora queda como entrada.

### E3-7 · OE1 se mide en el prototipo · APROBADA (B, Nico, 19 oct)
- **Antes:** 90 % de 5 residentes crea un Pase en menos de 30 s y 3 toques, en una prueba con personas antes del 9 nov.
- **Ahora:** en el prototipo, crear y enviar un Pase toma 3 toques o menos con una visita reciente y menos de 30 s estimados con KLM con una visita nueva, verificado por `prototipo/pruebas/oe1.mjs`.
- **Medido el 19 oct:** 3 toques y 8 s; visita nueva, 5 toques y 19,4 s.
- **Lo que no mide:** KLM predice a alguien que ya conoce la interfaz; no mide si un residente la entiende la primera vez. La satisfacción (SUS) pasa a OE2, con residentes, en el piloto.

### E3-8 · Motion e ilustración desde procesos reales · PROPUESTA
- **Pedido de Nico (19 oct):** la espiral del lector «no tiene nada que ver con la estética»; investigar y crear las animaciones e ilustraciones que debe tener Kino.
- **Qué propone:** `entrega-3/motion-e-ilustracion.md`. Cada movimiento sale de un proceso documentado:
  - el lector reconoce como en la sinapsis inmunológica;
  - el encendido al confirmarse es bioluminiscente;
  - por vencer es la fatiga de la luz;
  - no entra es la contracción de la *Mimosa*;
  - la integración es la red de *Physarum*.
- **Reglas** (Apple HIG, Carbon, Material 3, WCAG 2.2):
  - el veredicto se lee en el primer cuadro;
  - nada gira;
  - nada se mueve si no cambia un dato;
  - los latidos son 3;
  - reducido es fundido.
- **Ilustraciones:** una familia con el arco y la gota del logo, solo en primer uso, estados vacíos y el diagrama de integración.
- **Ya está en el prototipo.** Corrige cinco contradicciones con la marca:
  - latidos infinitos;
  - spinner en la espera;
  - reducido que apagaba todo;
  - fondos en movimiento;
  - la nota de confirmación sin el movimiento que pide la partitura.
- **Falta:** aprobarla; llevar `destello` y la curva de sístole a `@kino/motion`; pasar las ilustraciones a Figma.
- **Corrección (19 oct, segunda pasada) · APROBADA por Nico el 19 oct** («Aprobado, lleva el mismo nivel al resto de la app»). Nico vio el resultado todavía amateur. Diagnóstico y cambios en `entrega-3/motion-e-ilustracion.md` § «Segunda pasada». Lo que cambia de E3-8:
  - **Regla 6 acotada.** «Nada se mueve si no cambia un dato» vale para portería y para los estados del Pase. La vida ambiental de la marca (aurora del inicio, decisiones.md X7) se mantiene y se pausa a los 5 s, como pide F7 («el motion no se sacrifica»).
  - **Portería con la escena 3D aprobada** (M3D, portería nocturna) en lugar de la talanquera dibujada. Reposa en un cuadro fijo y solo avanza con una lectura; el veredicto sigue en el primer cuadro.
  - **Continuidad espacial:** elemento compartido entre tarjeta, Pase creado y detalle; el botón de crear crece y toma la forma del arco; la burbuja de la visita crece hasta el Pase vivo.
  - **Jerarquía de brillo:** solo el Pase vigente brilla; por vencer en ámbar que se apaga; las demás tarjetas sin neón.
  - **El Pase como objeto:** inclinación con el dedo o el giroscopio, reflejo y sombra.
  - **Revisión en video** de cada momento (`prototipo/pruebas/video.mjs`).
- **Lámina de revisión:** https://claude.ai/artifact/RYzKtmq3ZTzgfK5LEhBFbC (`entrega-3/antes-despues.html`).
- **Falta (además de lo anterior):** el visto bueno de Nico a los cinco momentos antes de llevar el mismo nivel al resto de la app; el momento de confirmar, vencer y revocar sobre el Pase.
- **Tercera pasada (19 oct):** el mismo criterio llevado al resto de la app (ingreso, pestañas, hoja, detalle, ciclo del Pase, visita, portería, administración y escenario). Detalle en `entrega-3/motion-e-ilustracion.md` § «Tercera pasada». Nada de esto cambia tokens aprobados.

### E3-9 · Personajes del residente y la administración · APROBADA (19 oct, Nico)
- **Pedido de Nico (19 oct):** un personaje con la estética de Kino para cada usuario.
- **Qué propone:** `entrega-3/personajes/` (README y dos SVG). 2D vectorial, cartoon plano, animado con CSS; ya están en la lámina 2 del deck.
- **Choque que hay que decidir:** la familia de ilustraciones de E3-8 dice «sin personas». Propuesta: personajes solo en presentaciones y onboarding, nunca en pantallas de operación.
- **Falta:** aprobarla; decidir si se suman la visita, el colaborador y portería.
- **Respuesta de Nico (19 oct):** «Aprobado E3-9, personajes solo en presentaciones y onboarding; pero rehace los personajes, están nefastos. hazlos en 3d con estética biopunk». Se rehicieron en 3D (Blender, `branding/sistema/v3/motion/blender/personajes.py`); la versión 2D quedó en `entrega-3/personajes/_obsoleto-2d/`.

### E3-10 · Objetivo general del plan estratégico · APROBADA (19 oct, Nico)
- **Pedido de Nico (19 oct):** boceto «posicionar a Kino, a octubre 2027, como el aliado estratégico lider en software de seguridad de las propiedades horizontales»; después: «Líder en Antioquia, deja de lado esto: "el residente decide quién entra, la administración pone los límites y funciona con el lector que el conjunto ya tiene"; extrapolar la seguridad de software de las propiedades horizontales y sus involucrados»; y luego: «Has que todo sea coherente. Y realiza un test de calidad al objetivo y púlelo».
- **Redacción aplicada:** «Posicionar a Kino, a octubre de 2027, como el software de seguridad líder en Antioquia para la propiedad horizontal: el aliado que reúne a residentes, visitas, colaboradores, portería y administración en la decisión de quién entra.» El test de calidad está en `entrega-3/investigacion-objetivo-general.md` §7: pasa 11 de 11 pruebas.
- **Coherencia aplicada:** meta general con «primero en participación en Antioquia» y 4 conjuntos como piso; OE5 en Antioquia, empezando por el Oriente; censo de copropiedades en el plan (abril a junio de 2027); KPI de participación en GQM y en la etapa de conversión. Cambios en el deck (láminas 10, 11, 14, 15 y 18), la Biblia (3.1, 3.3 y 3.4) y `estrategia.md` (§2, §3, §6, §7, §8 y §11).
- **Riesgo abierto:** si el censo muestra que 4 conjuntos no alcanzan para ser primeros, hay que subir la meta o acotar la región.
- **Respuesta de Nico (19 oct):** «Sí, aplica la visión y deja el objetivo así». El objetivo general queda en el ingreso; la ambición del portafolio va en la visión (`estrategia.md` §9, E6, lámina 18): «Kino empieza por quién entra y crece hacia los demás problemas de seguridad de la propiedad horizontal que descubra con sus clientes, sobre el hardware que cada conjunto ya tiene.»
