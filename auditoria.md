# Auditoría del borrador · Sistema de marca Kino

Fase 0. Compara el borrador contra la definición de terminado de 12 departamentos. Fecha: 23 sep 2026.

**Fuentes auditadas**
- Borrador del sitio: `kino/Kino_Sistema_de_marca_2026-09-23.html`, 28 láminas (se cita como «l.NN»).
- Librería de Figma `BO7UnDO9iE0aG6yUpNj0bc`, leída por API el 23 sep:
  - 8 páginas: Portada, Fundamentos, divisor, Estado, Pase, Flujo, Evidencia, Tarjeta.
  - 113 variables en 4 colecciones: Primitivos 51, Color 34 (Oscuro/Claro), Espacio y radio 16, Movimiento 12.
  - 12 estilos de texto, 6 de efecto, 0 estilos de color.
- Fuente de verdad: `gorr-brand-system/clientes/kino/`.
  - Tokens: 118 primitivos de color, 8 de tipo, 20 de medida, 17 de movimiento y 37 semánticos por tema.
  - `voz.json`, `reportes/contraste.json` (38 pares) y `reportes/calibracion-voz.json` (21/42, 0 falsos positivos).
- `kino/branding/sistema/`:
  - `kino-brand.css`;
  - 5 SVG de marca reconstruidos;
  - 10 iconos Iconoir.
- Investigación:
  - `MAESTRO-KINO.md` y `inspeccion/diagnostico-inspeccion.md`;
  - `claude/diagnostico-consolidado-v1.md` y `claude/arquetipos-e-insights.md` (proyecto);
  - `Kino_Deck_diagnostico_2026-09-21.html`;
  - `muestras-voz.md`.

**Fuentes que no están en la carpeta.** Ni `deck-kino-diagnostico-2026-09-04.html` ni el «Anexo de sustentación» aparecen en `kino/` (búsqueda por nombre y por contenido). En su lugar se usó el deck de diagnóstico del 21 sep, que es posterior y ya incorpora la inspección. Queda como [PENDIENTE: ubicar el deck del 4 sep y el Anexo].

Leyenda: **C** completo · **S** superficial · **F** falta.

---

## 1. Matriz departamento × elemento

### 1 · Plataforma

| Elemento | Estado | Evidencia |
|---|---|---|
| Problema con evidencia y fuente | S | l.03: aparece la pregunta guía, pero no hay una sección del problema. Los códigos de evidencia están mal asignados: «miembro permanente» se cita como H4 cuando es H5, y «Permitido» como H2 cuando es H3 |
| Qué necesita cada actor (5) | F | No existe. Insumo: `arquetipos-e-insights.md` (A1–A4) |
| Mapa de alternativas | F | No existe en el borrador. El deck del 21 sep afirma que ni Neivor ni ButterflyMX se integran con el hardware instalado, y la página de Neivor dice lo contrario (ver §3) |
| Posicionamiento en una frase con prueba | F | — |
| Promesa | F | — |
| Personalidad: 3 rasgos, somos / no somos | S | `voz.json` tiene «somos» (3) y «no somos» (4), pero describen la voz y no la personalidad. l.25 |
| Valores con comportamiento observable | F | Las 9 reglas de l.04 son reglas de uso, no valores |
| Arquitectura de nombres | S | Solo la pareja Pase / cuenta. No hay nombres para las superficies (app, administración, portería) ni para los modos |
| Manifiesto breve | S | l.03 «La membrana»: un concepto con tres metáforas, sin manifiesto |

### 2 · Verbal

| Elemento | Estado | Evidencia |
|---|---|---|
| Perfil NN/g, una frase por dimensión | S | l.25 y `voz.json`. Completo en estructura, pero l.25 dice «ni permisos» y contiene «El administrador debe aprobar el ingreso» como ejemplo del «No», que la compuerta marca como ERROR |
| Tono en 6 contextos con ejemplo | F | Solo distingue app y documentos |
| Vocabulario ≥ 20 entradas | S | 15 entradas: 6 para usar, 8 para evitar, 1 que no se mezcla |
| Glosario completo | F | — |
| Guía de estilo | F | El borrador mezcla «07:00–17:00» (l.23) con «6:00 p. m.» (l.25) |
| Inventario de UX writing | F | `muestras-voz.md` trae 36 textos actuales. Ninguno está reescrito |
| Plantillas de WhatsApp | F | No hay mensajes reales (`muestras-voz.md` §b vacía) |
| Calibración | S | 21/42 atrapadas, 0 falsos positivos |

### 3 · Logo

| Elemento | Estado | Evidencia |
|---|---|---|
| Construcción sobre grilla | S | l.05 nombra bloque, arco y gota, sin grilla. Las medidas salen de la reconstrucción (IoU 98 %) |
| Área de protección | C | 0,63 × el ancho del bloque (l.05). Derivada de la reconstrucción |
| Tamaño mínimo digital | S | Marca desde 20 px; bloqueo horizontal de 28 a 48 px; vertical desde 40 px |
| Tamaño mínimo impreso | F | — |
| Versiones (color, negro, blanco, símbolo, horizontal) | S | Hay SVG de marca, gota, logotipo y bloqueos horizontal y vertical, más PNG en negro y blanco. Falta una lámina de versiones y los archivos por color |
| Uso en ≥ 6 fondos | S | 3 fondos (l.06) |
| ≥ 8 usos incorrectos | S | 4 (l.06) |
| Convivencia con el conjunto (solo texto) | S | 1 ejemplo incorrecto; falta el correcto |
| Favicon e ícono de app | F | — |
| Animación del logo | F | — |

### 4 · Color

| Elemento | Estado | Evidencia |
|---|---|---|
| Primitivos con escalas | C | 7 familias y 118 tokens (l.07) |
| Roles semánticos | C | 37 por tema (l.08) |
| Temas claro y oscuro | C | Tokens y botón de tema |
| Estados: activo, usado, vencido, rechazado, pendiente | S | Existen vigente, por-vencer, vencido, negado, sin-confirmar e identidad. Falta **usado**. «Pendiente» choca con la regla de l.09 (no hay estados de aprobación): se propone mapearlo a sin-confirmar (ver Parada 1) |
| Paleta de datos y gráficos | F | — |
| Proporciones de uso | F | — |
| Tabla APCA completa | S | Los 38 pares reportan APCA, pero **contra los umbrales nuevos (regla 5) el tema oscuro falla en masa** (ver §2) |
| Simulación de daltonismo | F | — |
| Valores de impresión | F | — |

### 5 · Tipografía

| Elemento | Estado | Evidencia |
|---|---|---|
| Familia de texto y monoespaciada | C | Archivo y JetBrains Mono, esta con cero barrado para placas (l.11) |
| Escala fluida | C | Utopia, 8 pasos (l.12) |
| Jerarquías | S | h1, h2, lede, ojo y cifra. Faltan h3, cuerpo, botón, etiqueta y campo |
| Interlineado, tracking y largo de línea | S | 62 caracteres y +8 % en el ojo. Sin interlineado declarado |
| Cifras tabulares | C | l.11 y l.16 |
| Licencias | S | OFL anotada en `sistema-de-marca-kino.md`, no en el sitio. Arkit sin licencia |

### 6 · Iconografía e ilustración

| Elemento | Estado | Evidencia |
|---|---|---|
| Grilla, trazo, esquinas y tamaños | S | Retícula de 24 y trazo de 1,7 (l.13). Sin esquinas ni tamaños |
| ≥ 24 íconos base en SVG | S | 27 en el sprite de la entrega 2, embebidos y sin descarga. 10 de Iconoir en `iconos/`. Faltan Pase, navegación y estados propios |
| Reglas de ilustración | F | — |

### 7 · Imagen

| Elemento | Estado | Evidencia |
|---|---|---|
| Dirección de arte biopunk | F | La palabra «biopunk» no aparece en el sitio |
| Qué sí y qué no, con ejemplos | F | — |
| Texturas y fondos | S | Aurora WebGL y velo (l.24) |
| Personas y espacios | F | — |
| Cuándo usar cada recurso | F | — |

### 8 · Estructura

| Elemento | Estado | Evidencia |
|---|---|---|
| Retícula web | S | l.12 |
| Retícula móvil | F | — |
| Retícula de presentación | S | Láminas de 1360 y 1680 |
| Retícula de impresos | F | — |
| Espaciado | S | 20 tokens de medida sin lámina |
| Radios | S | 6 px |
| Elevación | S | Tokens de relieve y resplandor |
| Breakpoints | S | 1100 y 680, sin token |

### 9 · Motion

| Elemento | Estado | Evidencia |
|---|---|---|
| Principios | C | 5 verbos (l.20) |
| Tokens de duración y curvas | C | 17 tokens y 5 curvas (l.20–21) |
| Coreografía y cascadas | C | l.22 |
| Catálogo ≥ 10 con demo viva | S | 7 demos (l.22–23) |
| Motion del logo | F | — |
| Modo reduced-motion | S | Hoy salta al estado final. Falta un modo alternativo con fundidos que conserve el significado |

### 10 · Producto / UI

| Elemento | Estado | Evidencia |
|---|---|---|
| Componentes con todos sus estados | S | Figma: 4 conjuntos con 24 variantes, sin hover, foco, deshabilitado, error ni carga. El manual v11 tiene 10 componentes |
| Crear Pase | F | — |
| Lista de Pases | S | l.26 |
| Detalle de Pase | F | — |
| Límites de administración | F | — |
| Acceso por código | F | — |
| Reglas WCAG 2.2 AA | S | Solo 2.2.2 (latido) y contraste |

### 11 · Aplicaciones

| Elemento | Estado | Evidencia |
|---|---|---|
| App móvil | S | l.26 |
| Mensaje de WhatsApp con Pase | F | — |
| Pase QR | F | — |
| Señalética de portería | F | — |
| Adhesivo de talanquera | F | — |
| Presentación comercial | S | El propio shell del deck. Falta la plantilla comercial |
| Documento de una página | S | Descrito en texto (l.26) |
| Plantillas de redes | F | — |
| Correo | F | — |
| Papelería | F | — |
| Credencial | F | — |
| Carta de bienvenida | F | — |

### 12 · Gobernanza

| Elemento | Estado | Evidencia |
|---|---|---|
| Quién decide | S | Lo dice `sistema-de-marca-kino.md`, no el sitio |
| Cómo pedir activos | F | — |
| Versionado | S | Rótulo «v2». No existe `06-entrega/entrega.md` |
| Registro de cambios | S | Vive en `decisiones-marca-*.md`, fuera del sitio |
| Lista de revisión antes de publicar | F | — |
| Pendientes | S | Tres en l.28 |
| Centro de descargas | F | — |

### Navegación

| Requisito | Estado | Evidencia |
|---|---|---|
| Índice persistente con sección activa y progreso | S | Índice de láminas y contador |
| Dos puertas por audiencia | F | — |
| Cualquier sección en ≤ 2 interacciones | S | Sí para láminas; no hay subsecciones |
| Ancla profunda por subsección | F | — |
| Búsqueda sobre títulos y glosario | F | — |
| Teclado y foco visible | S | Flechas para pasar lámina |
| Anterior y siguiente | S | Paginación de lámina |
| 360 px, claro y oscuro | S | Verificado a 390 px, no a 360 |
| Descargas junto a la regla | F | — |

### Cuenta

| | C | S | F |
|---|---|---|---|
| Elementos de los 12 departamentos (90) | 10 | 39 | 41 |

Por departamento (C/S/F):

| Departamento | C/S/F |
|---|---|
| Plataforma | 0/4/5 |
| Verbal | 0/3/5 |
| Logo | 1/6/3 |
| Color | 3/2/4 |
| Tipografía | 3/3/0 |
| Iconografía | 0/2/1 |
| Imagen | 0/1/4 |
| Estructura | 0/6/2 |
| Motion | 3/2/1 |
| Producto | 0/3/4 |
| Aplicaciones | 0/3/9 |
| Gobernanza | 0/4/3 |

---

## 2. Hallazgos transversales

1. **El tema oscuro no pasa los umbrales APCA de la regla 5.** Datos de `reportes/contraste.json`, tema oscuro:

   | Rol | Lc | Umbral que alcanza |
   |---|---|---|
   | texto secundario | 71,8 | < 75: no sirve para cuerpo |
   | texto tenue | 49,2 | solo titulares |
   | texto de los estados | 62,9 a 71,8 | solo texto grande |
   | bordes | 23,1 a 24,4 | < 30: falla como elemento no textual |

   En el tema claro todo pasa, salvo el texto de vencido (68,6), que alcanza texto grande. Toca la decisión firme de tema oscuro canónico y se lleva a la Parada 3.
2. **El texto visible menciona el contexto académico y fechas internas**: «la entrega 2» (l.02, l.10, l.13, l.16, l.17), «diagnóstico consolidado v1» (l.03), «23 sep» (l.01, l.02). Choca con el contexto: el sistema se presenta como oficial y vigente.
3. **La compuerta de voz marca 2 errores y 8 avisos en el borrador** (`npm run voz -- kino` sobre el texto extraído):
   - error: «El administrador debe aprobar el ingreso» (l.25);
   - error: «Y» de arranque (l.09);
   - aviso: «permisos» (l.25);
   - aviso: polisíndeton «ni cortina, ni aurora, ni…» (l.24).
4. **Patrones prohibidos que la compuerta no atrapa hoy**:
   - antítesis: «Un muro no sabe quién pasó. Una membrana sí» (l.03), «El acento es acción, no estado» (l.04), «Cinco curvas y ninguna más» (l.21);
   - rayas: 6 en el texto.
   Son candidatos para subir la cobertura en la Fase 2.
5. **La diferenciación está afirmada de más.** El deck del 21 sep dice que «ninguno se integra con el hardware de acceso ya instalado». La página de Neivor, consultada el 23 sep, dice «Integra Neivor Access Control con los sistemas de acceso de tu condominio», sin nombrar marcas. Lo que sí se sostiene:
   - la integración con HikCentral probada en producción: Villas Campestres, 887 de 888 personas y 757 de 757 vehículos (`diagnostico-inspeccion.md` §3);
   - el Pase sin cuenta;
   - la autoridad acotada del residente.
   El posicionamiento se escribe sobre eso.
6. **La prueba de «sin cuenta» todavía no existe.** Que HikCentral acepte una credencial temporal sin crear una persona es el bloqueante 1 del `MAESTRO-KINO.md` §7. La marca puede prometer el Pase sin cuenta del lado del visitante; la prueba técnica queda [PENDIENTE].
7. **Figma no espeja los tokens.**

   | Grupo | DTCG | Figma |
   |---|---|---|
   | Primitivos de color | 118 | 51 |
   | Semánticos por tema | 37 | 34 |
   | Movimiento | 17 | 12 |
   | Tipografía | tokens | sin colección |

   Los efectos del tema claro son estilos aparte. Falla la regla 6 (una sola fuente de verdad).
8. **Estados.** La definición pide «activo, usado, vencido, rechazado, pendiente»; el sistema tiene vigente, por-vencer, vencido, negado, sin-confirmar e identidad. Falta **usado**, necesario para el código de un solo uso. «Pendiente» se mapea a «sin confirmar» para no reintroducir una cola de aprobación que el producto no tiene (H2).
9. **Las instrucciones del proyecto siguen diciendo «marca blanca» y «permiso».** Mandan las decisiones firmes de este encargo. El texto visible del sitio no puede heredar esos términos.

---

## 3. Hechos que sostienen la plataforma

Cada hecho lleva su grado. Ninguno se inventa; lo que falta queda en §4.

| # | Hecho | Grado | Fuente |
|---|---|---|---|
| P1 | Ningún rol puede anunciar una visita, autorizar un ingreso en el momento ni fijar hasta cuándo entra una persona | Observado | `MAESTRO-KINO.md` F1; `matriz-capacidades.csv` |
| P2 | Una placa inventada registrada por un residente quedó «Permitido» al instante y se sincronizó con el lector. La misma pantalla dice que el acceso lo controla la administración | Observado, con prueba | `diagnostico-inspeccion.md` §2.1 |
| P3 | El invitado queda como miembro permanente con rol «Visitante», sin fecha ni vigencia | Observado | `diagnostico-inspeccion.md` §2.3 |
| P4 | Los 711 errores de sincronización con HikCentral son `add_person` por el campo correo | Observado | `diagnostico-inspeccion.md` §2.4 |
| P5 | El portero ve cédula, teléfono y correo de los residentes, y la vigencia que ellos no ven de sí mismos | Observado | `diagnostico-inspeccion.md` §2.5 |
| P6 | Refugio Campestre: 0 de 312 personas y 1 de 44 vehículos sincronizados, con el hardware instalado | Observado y confirmado | `diagnostico-inspeccion.md` §3 |
| P7 | Villas Campestres: 887 de 888 personas y 757 de 757 vehículos sincronizados con HikCentral | Observado | `diagnostico-inspeccion.md` §3 |
| P8 | Los colaboradores son el ingreso más frecuente, y hay 0 contratistas registrados | Declarado y observado | `MAESTRO-KINO.md` F10, F11 |
| P9 | El 51,3 % de los contratos de trabajo doméstico en el 1S-2026 son por días | Entorno | GEIH-DANE y Symplifica vía Infobae, 9 sep 2026 |
| P10 | El 47,88 % de la vivienda urbana de Colombia está en propiedad horizontal; en Medellín, el 61,7 % | Entorno | Fedelonjas vía Portafolio, 28 jun 2026 |
| P11 | La SIC ordenó a un conjunto ofrecer vías de ingreso no biométricas (Res. 52185 del 28 ago 2025) | Entorno | SIC, comunicado oficial |
| P12 | Neivor vende autogestión de visitas por QR e integración declarada con los sistemas de acceso del condominio | Entorno | landing.neivor.com, consultada el 23 sep 2026 |
| P13 | ButterflyMX emite pases de visitante sin cuenta, también recurrentes | Entorno | butterflymx.com/blog/visitor-pass (deck del 21 sep, fuente s6) |
| P14 | El competidor diario es la llamada o el WhatsApp a portería | Inferido del recorrido | `MAESTRO-KINO.md` §2; deck del 21 sep, lámina de flujo |
| P15 | Los servicios de copropiedad subieron 13,42 % anual a mayo de 2026, contra 5,84 % de inflación | Entorno | Fedelonjas vía Portafolio y Corrillos |

## 4. Lo que falta de la investigación

- [PENDIENTE: el deck de diagnóstico del 4 sep y el Anexo de sustentación no están en la carpeta.]
- [PENDIENTE: citas textuales de los cinco residentes del 2 sep.] Sin ellas, las necesidades por actor se apoyan en la inspección y el entorno, no en voz de usuario.
- [PENDIENTE: confirmar con Manuel si HikCentral admite una credencial temporal sin crear persona.] Es la prueba técnica del Pase sin cuenta.
- [PENDIENTE: evidencia de cómo trabaja la portería fuera del sistema (minuta, llamadas).] El mapa de alternativas la cita como inferida.
- [PENDIENTE: verificar qué integra Neivor en la práctica (marcas de hardware, si el visitante necesita cuenta).]
