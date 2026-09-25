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

### F4-P5 · Pantallas con la jerarquía del Pase · PROPUESTA
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
- **Espera:** revisión de Nico en la lámina siguiente.

### F4-P6 · Mensaje de alta fallida en HikCentral · PROPUESTA
- **Qué es la fila:** el inventario de la Parada 2 traduce cada texto que hoy muestra el sistema. Uno es el error que ve el super administrador: «Incorrect request parameter. [email parameter error]», 711 veces (observado, `inspeccion/diagnostico-inspeccion.md`).
- **Lo que Nico señaló (25 sep):** con el Pase, la visita no se registra como persona ni necesita correo, así que ese error no es el problema que Kino resuelve.
- **Lo que dice la inspección:** los 711 errores son `add_person` de todas las personas, no solo de visitas. En Refugio, 0 de 312 usuarios están sincronizados, residentes incluidos.
- **Efecto del diseño actual:** la visita entra con un Pase y no crea una persona. El residente entra con código por WhatsApp y el correo deja de ser obligatorio (inferido de la decisión del ingreso sin contraseña). Con eso, el error del correo desaparece para todos.
- **Propuesta (A, construida):** la fila deja de hablar del correo y queda como el mensaje genérico de un alta que HikCentral no acepta: «HikCentral no aceptó el alta de Carolina Ruiz. Hasta que se corrija, el lector no la reconoce.» Sirve para cualquier falla de sincronización, que sigue siendo posible (Refugio es el caso).
- **Alternativa (B):** quitar la fila del inventario, porque Kino no debería producir ese error.
- **Por qué A:** la integración caída de Refugio muestra que las altas pueden fallar por otras causas. La administración necesita un mensaje que diga a quién afecta y qué pasa en la puerta. Tampoco promete que Kino reintente solo, porque eso no está confirmado.

### Estado tras la respuesta del 25 sep (segunda vuelta)
1. Librería de Figma: **APROBADA**. Pedido: pantallas con la jerarquía del Pase (F4-P5).
2. F4-P4: **APROBADA** (A).
3. La fila del error de HikCentral se explica y se corrige como F4-P6.
4. Con 1 y 2 aprobadas, la versión 1.1.0 queda aprobada y se republica el artefacto oficial. F4-P5 y F4-P6 van en la 1.2.0.

