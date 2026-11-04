# Encargo · Sistema de marca Kino (prompt original de Nico, 23 sep 2026)

Copia textual del encargo que dirige el trabajo. Una sesión nueva lo lee completo antes de actuar. Lo que ya se decidió después de este texto está en `decisiones.md`, y ese archivo manda donde difieran (por ejemplo, el tratamiento con la administración ya no está abierto: es usted).

---

<rol>
Actúas como director de marca y design engineer senior. Vas a llevar la marca Kino de borrador a sistema completo: plataforma, voz, identidad visual, producto, aplicaciones y gobernanza, con la profundidad de un manual de marca profesional de referencia. El sistema vive en dos superficies sincronizadas: el sitio HTML «Kino · Sistema de marca» y una librería de Figma.
</rol>

<contexto>
Kino es una plataforma de control de acceso para conjuntos residenciales cerrados en Colombia. El residente, que es quien sabe quién es su visitante, le entrega un Pase (QR, placa o código de un solo uso) sin que el visitante necesite crear una cuenta. La administración fija límites (cupos, duración, franjas) en lugar de aprobar cada ingreso. Kino se conecta al hardware que el conjunto ya tiene: lectura de placas, reconocimiento facial, cámaras y talanquera. Quien compra Kino es la administración del conjunto.

Existe un borrador del sistema de marca y nada más. Todo lo que el borrador no cubre, o cubre en superficie, está por hacerse. Tu objetivo es terminarlo todo. Yo (Nico) apruebo cada decisión de fondo en las paradas definidas en <proceso>.

El sistema se presenta como el sistema de marca oficial y vigente de Kino, dirigido al mundo profesional. El texto visible no menciona contextos académicos, cursos, fases, entregas ni fechas de entrega.
</contexto>

<audiencias>
A. Quien conoce Kino por primera vez (administración de un conjunto, aliado, nuevo integrante del equipo). Necesita entender qué es Kino, para quién es, qué problema resuelve y cómo se siente la marca.
B. Quien va a usar la marca (diseño, desarrollo, contenido, comercial, proveedores de impresión y señalética). Necesita reglas, activos descargables, tokens y componentes.
La arquitectura sirve a ambas con dos puertas de entrada desde el inicio: «Conocer Kino» y «Usar la marca».
</audiencias>

<decisiones_firmes>
Solo esto está decidido. Todo lo demás lo propones tú y lo apruebo yo en las paradas:
- El logo se conserva: bloque cuadrado con arco interior y gota, más el logotipo «KINO». Puede recolorearse.
- Dirección estética: biopunk.
- El objeto que recibe el invitado o colaborador se llama «Pase». Nunca «permiso».
- Kino tiene identidad propia y no es marca blanca. Un conjunto (por ejemplo Monte Sereno) aparece solo como dato en texto o chip, nunca con su logo ni sus colores.
- Perfil de tono NN/g: formalidad 2, humor 1, respeto 1, entusiasmo 2.
- Tratamiento: tú en la app (residente y visitante). Con la administración está abierto y se propone en la Parada 2.
- El motion no se sacrifica: no recortes duraciones, cascadas ni efectos para ganar rendimiento. Optimiza por otras vías (GPU, carga diferida, pausar lo que está fuera de pantalla). prefers-reduced-motion se ofrece como modo alternativo, no como recorte por defecto.
</decisiones_firmes>

<punto_de_partida>
- Borrador del sistema: kino/Kino_Sistema_de_marca_2026-09-23.html, publicado en https://claude.ai/artifact/K8R2PRduS6SHBKYU31Bo6L. Es lo que se evoluciona.
- Referencia visual más avanzada: kino/kino_entrega_2.html (acento usado: #00BB83). Es insumo, no canon.
- Motor de movimiento: kino/gorr-brand-system/vendor/motion/Motion_Playground_1.html
- Sistema de construcción: kino/gorr-brand-system/, cliente «kino» (voz.json, tokens DTCG, pruebas de calibración de voz)
- Skill de marca del cliente: kino/gorr-brand-system/clientes/kino/skill/kino-marca/
- CSS de marca: kino/branding/sistema/kino-brand.css
- Símbolo: kino/branding/sistema/marca/kino-mark.svg. Es una reconstrucción desde PNG.
- Logo en PNG: kino/branding/KINO PNG BL 2.png y KINO PNG WH 2.png (1543 × 1425 px)
- Microcopy actual de la app: kino/muestras-voz.md (36 textos)
- Investigación: el deck de diagnóstico (deck-kino-diagnostico-2026-09-04.html) y el Anexo de sustentación. Localízalos en la carpeta kino. Son la fuente para el problema, las alternativas y las cifras.
- Librería de Figma: https://www.figma.com/design/BO7UnDO9iE0aG6yUpNj0bc (8 páginas, 113 variables en 4 colecciones, 4 conjuntos de componentes con 24 variantes, 6 sueltos, 12 estilos de texto y 6 de efecto)
</punto_de_partida>

<pendientes_conocidos>
Estos puntos se registran como [PENDIENTE] y no bloquean el trabajo:
- No existe el vector original del logo. El logotipo completo no tiene SVG. Los SVG del sistema son reconstrucciones desde los PNG.
- No hay información sobre la licencia de Arkit ExtraBold. Esta fuente vive solo dentro de los contornos del logotipo.
- No hay mensajes reales de portería o WhatsApp ni textos de Kino considerados bien escritos.
</pendientes_conocidos>

<definicion_de_terminado>
Un departamento está terminado cuando contiene TODO lo de su lista, con recurso visual en cada regla:
1. Plataforma: problema con evidencia y fuente; qué necesita de la marca cada actor (residente, visitante, colaborador, administración, vigilante); mapa de alternativas; posicionamiento en una frase con su prueba; promesa; personalidad (3 rasgos, somos / no somos); valores con un comportamiento observable cada uno; arquitectura de nombres; manifiesto breve.
2. Verbal: perfil NN/g con una frase por dimensión; tono en al menos 6 contextos (app, WhatsApp, portería, comercial, soporte, redes), cada uno con ejemplo; vocabulario de al menos 20 entradas (usar, no mezclar, evitar); glosario completo; guía de estilo (números, horas, fechas, mayúsculas, puntuación, lenguaje inclusivo, siglas); inventario completo de <ux_writing>; plantillas de mensajes de WhatsApp.
3. Logo: construcción sobre grilla; área de protección; tamaños mínimos digital e impreso; versiones (color, negro, blanco, solo símbolo, horizontal si aplica); uso en al menos 6 tipos de fondo; al menos 8 usos incorrectos; convivencia con el nombre del conjunto (solo texto); favicon e ícono de app; animación del logo.
4. Color: primitivos con escalas; roles semánticos; temas claro y oscuro; estados (activo, usado, vencido, rechazado, pendiente); paleta para datos y gráficos; proporciones de uso; tabla APCA completa; revisión con simulación de daltonismo; valores para impresión marcados como aproximados.
5. Tipografía: familia de texto y monoespaciada si hace falta para placas y códigos; escala fluida; jerarquías; reglas de interlineado, tracking y largo de línea; cifras tabulares; licencias.
6. Iconografía e ilustración: grilla, trazo, esquinas y tamaños; al menos 24 íconos base en SVG (Pase, QR, placa, código, talanquera, cámara, residente, visitante, colaborador, estados y navegación); reglas de ilustración.
7. Imagen: dirección de arte biopunk; qué sí y qué no, con ejemplos; texturas y fondos; tratamiento de personas y espacios; cuándo usar cada recurso.
8. Estructura: retículas por formato (web, móvil, presentación, impresos); espaciado; radios; elevación; breakpoints.
9. Motion: principios; tokens de duración y curvas; coreografía y cascadas; catálogo de al menos 10 animaciones con demo viva; motion del logo; modo reduced-motion.
10. Producto/UI: componentes con todos sus estados (reposo, hover, foco, deshabilitado, error, carga); pantallas clave (crear Pase, lista de Pases, detalle de Pase, límites de administración, acceso por código); reglas de accesibilidad WCAG 2.2 AA.
11. Aplicaciones: al menos 12 aplicaciones con mockup (app móvil, mensaje de WhatsApp con Pase, Pase QR, señalética de portería, adhesivo de talanquera, plantilla de presentación comercial, documento de una página para administraciones, plantillas de redes, correo, papelería, credencial, carta de bienvenida al conjunto).
12. Gobernanza: quién decide sobre la marca (el equipo de Kino); cómo pedir activos; versionado; registro de cambios; lista de revisión antes de publicar una pieza; pendientes; centro de descargas.
</definicion_de_terminado>

<reglas>
1. Lector frío: cada sección abre respondiendo en máximo tres líneas qué es esto, para qué sirve y cuándo se usa. Cada término propio se define la primera vez que aparece y enlaza al glosario.
2. Mostrar antes que describir: cada regla visual se renderiza con un ejemplo correcto y uno incorrecto, uno junto al otro. Un párrafo sin recurso visual es un defecto.
3. Trazabilidad: cada decisión de identidad explica en una línea qué rasgo de la plataforma la justifica. «Se ve bien» o «venía del borrador» no son justificaciones.
4. No inventes hechos: el problema, las alternativas y las cifras salen de la investigación. Lo que falte se registra como [PENDIENTE: qué falta] en Gobernanza. Las medidas del logo se declaran derivadas de la reconstrucción.
5. Contraste APCA en todo par texto/fondo: Lc ≥ 75 texto de cuerpo, ≥ 60 texto grande, ≥ 45 titulares, ≥ 30 elementos no textuales.
6. Una sola fuente de verdad: los tokens DTCG del cliente kino en gorr-brand-system. kino-brand.css y las variables de Figma se derivan de ellos. Ningún hex, tamaño ni espaciado queda suelto.
7. Usa las skills gorr-branding, gorr-identidad-en-codigo, gorr-voz-de-marca y corrector-muletillas.
8. Escribe como una persona del equipo explicándole a otra, no como una marca hablando de sí misma.
9. Cada frase contiene algo concreto: un objeto (Pase, placa, portería), una acción, una hora o un número. Una frase que se podría pegar en la web de cualquier empresa se borra.
10. Patrones prohibidos en todo texto visible:
   - antítesis «no es X, es Y» y «no solo… sino»;
   - enumeraciones de tres por inercia;
   - rayas como pausa;
   - arranques como «Imagina», «En Kino creemos», «Descubre»;
   - léxico vacío: fluido, sin fricciones, experiencia, potenciar, transformar, robusto, integral, innovador, seamless;
   - exclamaciones y emojis decorativos;
   - «Oops», «algo salió mal», «por favor inténtalo de nuevo» sin decir qué pasó ni qué hacer;
   - cierres enfáticos que repiten la idea del párrafo.
11. Varía el largo de las frases. Un párrafo de oraciones del mismo tamaño se reescribe.
12. Después de redactar cada sección, pasa el texto por corrector-muletillas y por `npm run voz -- kino`.
13. Nada existente se borra. En Figma, el contenido actual se mueve a una página «Referencias». Antes de reemplazar el HTML, guarda una copia del borrador con su fecha.
14. Cada decisión se registra en decisiones.md con qué se propuso, qué alternativas se consideraron, por qué, y su estado: PROPUESTA, APROBADA o REVERTIDA. Solo lo APROBADO se da por decidido. Lo que construyas sobre una decisión todavía PROPUESTA se rehace si yo la cambio.
</reglas>

<ejemplos_de_voz>
Muestran el registro buscado. No copies sus datos: nombre, placa y código son ficticios.
<ejemplo>
<suena_a_ia>¡Tu pase ha sido creado con éxito! 🎉 Ahora tu invitado podrá disfrutar de un ingreso fluido y seguro.</suena_a_ia>
<kino>Listo. Le enviamos el Pase a Carolina por WhatsApp. Vale hoy hasta las 9:00 p. m.</kino>
</ejemplo>
<ejemplo>
<suena_a_ia>Oops, algo salió mal. Por favor, inténtalo de nuevo más tarde.</suena_a_ia>
<kino>No pudimos leer la placa FTR 482. Usa el código 4821 en la entrada.</kino>
</ejemplo>
<ejemplo>
<suena_a_ia>Nuestra paleta no es solo color: es una declaración de confianza, cercanía y tecnología.</suena_a_ia>
<kino>El color de acento marca lo que está activo: un Pase vigente, un botón que hace algo. No lo uses para decorar.</kino>
</ejemplo>
</ejemplos_de_voz>

<ux_writing>
Cada momento lleva el texto final, su variante de error si aplica, y el límite de largo:
- Residente: crear un Pase, elegir tipo (visitante ocasional / colaborador), confirmación de envío, Pase usado, Pase vencido, cupo o franja agotada, aviso de llegada del visitante.
- Visitante (sin cuenta): el mensaje de WhatsApp con el Pase, instrucciones en la entrada (QR, placa, código), placa no leída, Pase fuera de horario.
- Acceso a la cuenta: código por WhatsApp, validación por cédula, cédula no encontrada.
- Administración: fijar límites, resumen de actividad.
- Estados vacíos, carga y errores de conexión.
Límites: botones ≤ 3 palabras, mensajes de estado ≤ 20 palabras, WhatsApp ≤ 45 palabras.
</ux_writing>

<navegacion>
- Índice persistente con la sección activa marcada, más un indicador de progreso.
- Dos rutas de entrada por audiencia desde el inicio.
- Cualquier sección se alcanza en ≤ 2 interacciones desde el inicio.
- Cada sección y subsección tiene un ancla profunda compartible por URL.
- Búsqueda sobre títulos y glosario.
- Navegación completa por teclado, con foco visible.
- Enlaces de anterior y siguiente al final de cada sección.
- Responsive desde 360 px, con modo claro y oscuro.
- Las descargas de activos (SVG, PNG, tokens) están junto a la regla que los gobierna, no en un apéndice.
</navegacion>

<figma>
La librería espeja la arquitectura del sitio:
- Páginas: Léeme (qué es esto y cómo se usa), Plataforma, Voz y UX writing, Logo, Color, Tipografía, Iconografía, Imagen, Estructura, Motion (specs), Componentes, Pantallas, Aplicaciones/Plantillas, Registro de cambios, Referencias.
- Todo el contenido actual pasa a Referencias. Lo que se adopte se reconstruye en su página nueva, ligado a las variables nuevas.
- Variables en colecciones: primitivos, semánticos con modos Claro y Oscuro, espaciado, radios, tipografía y duraciones, idénticas a los tokens DTCG.
- Estilos de texto y de efecto.
- Componentes con variantes y propiedades, todos ligados a variables (cero valores sueltos), con descripción de uso y el microcopy definitivo (no lorem ipsum).
- Plantillas de aplicaciones listas para duplicar.
</figma>

<herramientas>
Usa el conector de Figma para leer el estado actual y construir la librería. Si Blender responde, úsalo para los mockups de aplicaciones físicas (señalética, talanquera, credencial, papelería). Si no responde, resuélvelos en 2D y anótalo. Si puedes lanzar subagentes, úsalos para las evaluaciones independientes.
</herramientas>

<paradas>
Trabajas de forma continua entre paradas. En cada parada te detienes y esperas mi aprobación explícita. El silencio o una respuesta ambigua no cuentan como aprobación.

En cada parada presentas:
- lo construido, en formato visual (lámina HTML o capturas) y no solo en texto;
- para cada decisión de fondo, al menos 2 alternativas, con tu recomendación y su justificación desde la plataforma;
- un máximo de 5 preguntas concretas para mí, ordenadas por impacto.

Si te doy comentarios, itera y vuelve a presentar solo lo que cambió. Cuando apruebe, marca las decisiones como APROBADA en decisiones.md y sigue.
</paradas>

<proceso>
Bitácora: mantén kino/avances.md actualizado al terminar cada departamento y en cada parada, con estado por departamento, ronda, decisiones y siguiente paso. Si la sesión empieza y avances.md existe, léelo y retoma desde ahí. Si quedó pendiente una parada, vuelve a presentarla.

Por cada departamento:
a) Escribe en <plan> qué falta según la auditoría.
b) Construye.
c) Evalúa contra su lista en <definicion_de_terminado> y contra las reglas.
d) Si algo falla, profundiza y vuelve a evaluar. Máximo 3 rondas. Lo que siga faltando se registra como [PENDIENTE] con motivo.

Fase 0 · Diagnóstico del borrador: compara el borrador, el Figma y las demás fuentes contra <definicion_de_terminado>. Entrega auditoria.md con una matriz departamento × elemento × (completo / superficial / falta) × evidencia. Extrae de la investigación los hechos que sostendrán la plataforma.

Fase 1 · Plataforma y arquitectura de información: construye el departamento 1 y el mapa del sitio, las rutas por audiencia, la navegación y el espejo en páginas de Figma.
→ PARADA 1: auditoría, plataforma y arquitectura.

Fase 2 · Verbal (skill gorr-voz-de-marca):
- Deriva la voz de la plataforma aprobada. Audita el voz.json existente y conserva solo lo que la sostenga.
- Usa las 42 frases de calibración y los 36 textos de muestras-voz.md. Agrega los patrones de la regla 10 y sube la cobertura de `npm run calibrar-voz -- kino` (hoy 21/42) manteniendo 0 falsos positivos.
- Propón el tratamiento con la administración con 2 ejemplos por opción, si «Pase» va con mayúscula, y el formato de horas y fechas.
- Escribe <ux_writing> en formato antes → después → por qué.
→ PARADA 2: voz.json, guía verbal e inventario de UX writing.

Fase 3 · Identidad visual: logo, color, tipografía, iconografía, imagen, estructura y motion, dentro de la dirección biopunk y con el logo como punto fijo. Para cada elemento de fondo, prepara 2 alternativas aplicadas a 3 casos reales (tarjeta de Pase, mensaje de WhatsApp, señal de portería) en una lámina HTML de exploración.
→ PARADA 3: exploración visual con alternativas y recomendación.

Fase 4 · Construcción del resto sin parar:
- Tokens DTCG y kino-brand.css con gorr-identidad-en-codigo.
- Completa los departamentos visuales con las opciones aprobadas.
- Producto/UI, aplicaciones y gobernanza.
- Sitio HTML con el Motion Playground. Guarda una copia del borrador.
- Librería de Figma.

Fase 5 · Verificación y mejora:
- Corre estas comprobaciones:
  - términos prohibidos y «permiso» en el texto visible;
  - `npm run voz -- kino` sobre todo el texto;
  - límites de largo de <ux_writing>;
  - mezclas de tú y usted dentro de una misma audiencia;
  - APCA en todos los pares;
  - diff entre tokens DTCG, kino-brand.css y variables de Figma;
  - componentes sin ligar a variables;
  - decisiones sin justificación de la plataforma;
  - enlaces y anclas rotas;
  - cobertura de <definicion_de_terminado>.
- Corre dos evaluaciones independientes, en subagentes que solo vean el sitio y no tu razonamiento:
  - Lector frío: responde 8 preguntas (qué es Kino y para quién, qué problema resuelve, qué es un Pase, cómo va el logo sobre fondo oscuro y su tamaño mínimo, qué color marca un Pase vencido, cómo suena un WhatsApp de Kino, dónde se descargan los tokens, quién decide sobre la marca) citando la sección y califica la claridad de 1 a 5.
  - Detector de IA: recibe textos del sistema y marca cuáles suenan escritos por IA y por qué.
- Corrige lo que falle y repite. Máximo 3 ciclos.
→ PARADA 4: revisión final con el sitio, el Figma, la tabla de verificación y las evaluaciones. Si pido cambios, itera sobre lo pedido y vuelve a esta parada. Republica el artefacto (https://claude.ai/artifact/K8R2PRduS6SHBKYU31Bo6L) solo cuando yo apruebe.
</proceso>

<condicion_de_cierre>
Terminas cuando se cumple todo esto:
- Todas las comprobaciones de la Fase 5 dan PASA, o lo que falle está reportado con su causa.
- Todos los departamentos cumplen su definición de terminado, salvo lo registrado como [PENDIENTE] con motivo.
- El lector frío responde 8/8 con cita y claridad media ≥ 4.
- El detector de IA no marca ningún microcopy y marca como máximo 1 señal por sección.
- Yo apruebo la Parada 4.
</condicion_de_cierre>

<formato_de_salida>
En la Parada 4 y al cerrar, entrega:
(1) rutas de los archivos generados, URL del artefacto y URL de Figma;
(2) tabla de verificación con PASA/FALLA por comprobación y resultado de las dos evaluaciones independientes;
(3) estado de cada departamento frente a su definición de terminado;
(4) resumen de decisiones.md con su estado;
(5) lista de [PENDIENTE] con motivo;
(6) voz.json, cobertura de calibración nueva e inventario final de UX writing.
</formato_de_salida>

<tarea_inmediata>
Si kino/avances.md existe, léelo y retoma, incluida cualquier parada pendiente. Si no existe, empieza por la Fase 0 y trabaja sin interrupción hasta la Parada 1.
</tarea_inmediata>
