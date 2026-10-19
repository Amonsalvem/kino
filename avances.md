# Avances · Sistema de marca Kino

Bitácora del encargo «de borrador a sistema completo». Si una sesión nueva empieza, lee este archivo y retoma desde **Siguiente paso**.

## Estado actual

**PARADA 4 cerrada e integrada** (25 sep). La 1.2.0 está aprobada, el artefacto oficial la tiene (versión 5) y `marca/fase-4` se integró a `main` (PR https://github.com/Amonsalvem/kino/pull/1, commit 5c756bb). **1.2.1 aprobada** (F4-P7 A, sitio responsive), publicada en el oficial (versión 6) e integrada a `main` (PR https://github.com/Amonsalvem/kino/pull/2, commit de8ba70).

| # | Departamento | Estado | Nota |
|---|---|---|---|
| 1 | Plataforma | Aprobada (Parada 1) | |
| 2 | Verbal | Aprobada (Parada 2) | Aviso de llegada: requisito del evento del lector (F4-P2) |
| 3 | Logo | Aprobado (1.0.0) | SVG reconstruidos desde PNG (98 %) |
| 4 | Color | Aprobado (1.0.0) | 7 familias, 9 estados, 112 mediciones sin fallos |
| 5 | Tipografía | Aprobado (1.0.0) | Archivo al 112 %, JetBrains Mono |
| 6 | Iconografía | Aprobado (1.0.0) | 37 íconos |
| 7 | Imagen | Aprobado (1.0.0) | Aurora y tejido celular |
| 8 | Estructura | Aprobado (1.0.0) | Retículas, espacio, radios, elevación, quiebres |
| 9 | Motion | Aprobado (1.0.0) | 13 animaciones, motor en vivo |
| 10 | Producto | Aprobado (1.2.0): pantallas con la jerarquía del Pase (F4-P5) | Componentes, 5 pantallas, WCAG |
| 11 | Aplicaciones | Aprobado (1.0.0) | 15 piezas; Pase vivo vencido sin botón (F4-P1) |
| 12 | Gobernanza | Aprobado (1.0.0) | Registro, revisión, 17 pendientes, descargas |
| — | Sitio | 1.2.1 aprobado (responsive) y publicado en el oficial | `Kino_Sistema_de_marca.html` · vista previa 1.2.0 https://claude.ai/artifact/W5U4Nw4AeZMpM7QZ4gsXcH |
| — | Figma | 1.2.0 aprobada | 271 variables iguales a DTCG; componente nuevo Pase en lista; pantallas 1.1.0 en su sección |

## Fase 0 · Diagnóstico (cerrada)
- `auditoria.md`: 90 elementos; 10 completos, 39 superficiales, 41 faltan.
- Hallazgos transversales principales:
  - el tema oscuro falla APCA;
  - el texto visible menciona la «entrega 2»;
  - la diferenciación está afirmada de más (Neivor sí anuncia integración);
  - Figma no espeja los tokens (51 frente a 118 primitivos).
- Faltan el deck del 4 sep y el Anexo de sustentación: no están en la carpeta.

## Fase 1 · Plataforma y arquitectura

<plan>
Según la auditoría, en Plataforma faltaba:
- problema con evidencia;
- necesidades de cada actor;
- mapa de alternativas;
- posicionamiento con prueba;
- promesa;
- personalidad con somos / no somos;
- valores con comportamiento;
- arquitectura de nombres;
- manifiesto.
En arquitectura faltaba:
- las dos puertas;
- anclas por subsección;
- la búsqueda;
- el espejo de Figma.
</plan>

**Construido**
- `branding/sistema/v3/sitio/`: fuentes del sitio (`contenido/`, `sitio.css`, `sitio.js`, `construir.py`, `secciones.py`).
- `branding/sistema/v3/sitio/build/kino-sistema-de-marca.html`: el sitio armado.
- `gorr-brand-system/clientes/kino/01-estrategia/posicionamiento.md`: Dunford, 10 pasos.
- `decisiones.md` con 13 propuestas y la reorganización de Figma ejecutada.
- Figma: páginas Léeme y Plataforma construidas.

**Evaluación contra la definición de terminado (ronda 1)**

| Elemento | Estado | Nota |
|---|---|---|
| Problema con evidencia y fuente | Cumple | 5 hallazgos con grado y fuente, más 3 datos de entorno |
| Qué necesita cada actor | Cumple | Faltan las citas de las entrevistas [PENDIENTE] |
| Mapa de alternativas | Cumple | Mapa de 2 ejes y tabla con grado |
| Posicionamiento con prueba | Cumple con reserva | La prueba de «sin cuenta» está pendiente y se muestra así |
| Promesa | Cumple | Ejemplo que la cumple y ejemplo que la rompe |
| Personalidad | Cumple | 3 rasgos, somos / no somos, ejemplos correcto e incorrecto |
| Valores | Cumple | 5, cada uno con conducta y el hallazgo al que responde |
| Arquitectura de nombres | Cumple | Árbol y 4 pares correcto / incorrecto |
| Manifiesto | Cumple | — |

**Reglas**

| Regla | Resultado |
|---|---|
| Revisión local de la regla 10 | 0 hallazgos: sin rayas, exclamaciones ni léxico vacío; «permiso» solo fuera del texto visible |
| Corrector de muletillas | Aplicado; se quitaron 14 enumeraciones de tres |
| `npm run voz -- kino` | 0 errores, 2 avisos (DANE y GEIH leídos como mayúsculas de énfasis: son siglas; se agregan a las excepciones en la Fase 2) |
| APCA del sitio | Todo texto menor de 24 px va en texto-primario (Lc 102). Los bordes con información van en texto-tenue (Lc 49 ≥ 30) |

## Enlaces
- Parada 1 (lámina): https://claude.ai/artifact/EuPrHetctevY4PGiVAohiM · copia en `kino/parada-1.html`
- Parada 4 (lámina): https://claude.ai/artifact/DBF7w1VTGPtJ9oQwdz4tXa · copia en `kino/parada-4.html`
- Parada 4b (segunda vuelta): https://claude.ai/artifact/Bn6AaiChNchG5dhx7BjtQ1 · copia en `kino/parada-4b.html`
- Parada 4c (tercera vuelta, 1.2.0): https://claude.ai/artifact/NXuGd6VQc7k6Fqqi9pciZZ · copia en `kino/parada-4c.html`
- Vista previa del sitio 1.2.0: https://claude.ai/artifact/W5U4Nw4AeZMpM7QZ4gsXcH
- Artefacto oficial (1.2.1, versión 6): https://claude.ai/artifact/K8R2PRduS6SHBKYU31Bo6L
- PR de la Fase 4 (integrado): https://github.com/Amonsalvem/kino/pull/1
- PR de la 1.2.1 (integrado): https://github.com/Amonsalvem/kino/pull/2
- Vista previa del sitio 1.2.1: https://claude.ai/artifact/TKafvu7bHfjeKPSYaaKd7S
- Vista previa del sitio 1.1.0: https://claude.ai/artifact/NnuVUWwUdgk34VHkj3H5Rd
- Vista previa del sitio 1.0.0: https://claude.ai/artifact/AJey2DjrB4K8oo92fn6pfg
- Vista previa del sitio v3: https://claude.ai/artifact/NGW6EEiRghDxq4uFzvsjBa
- Figma: https://www.figma.com/design/BO7UnDO9iE0aG6yUpNj0bc

## Siguiente paso
1. Sin trabajo pendiente del sistema de marca: la 1.2.1 está aprobada, publicada e integrada.
2. Lo siguiente, si hace falta, arranca como versión 1.3.0, en una rama nueva desde `main` y con su propia parada.

## Fase 2 · Verbal (23 sep)
- Fuente única: `branding/sistema/v3/sitio/verbal.py`. Genera la sección 02, `guia-de-contenido.md`, `ux-writing.md` y la verificación de largo.
- 14 patrones nuevos en `02-verbal/patrones-nuevos.json`:
  - atrapan 11 de 11 frases de IA de prueba;
  - 0 hallazgos sobre los textos nuevos.
- voz.json fusionado: 28 patrones nuevos. Calibración 40/42 (antes 21/42) con 0 falsos positivos. `npm run voz -- kino` da 0 hallazgos sobre el sitio, los textos de la app y las muestras.
- Parada 2: https://claude.ai/artifact/JZmNsBpL9zizPj29yxE8x9 · vista previa del sitio v3, versión 2.

## Fase 3 · Identidad visual (exploración, 23 sep)
- Lámina `parada-3.html` con 8 decisiones de fondo. Cada una tiene 2 alternativas aplicadas a la imagen del Pase, el mensaje de WhatsApp y la señal de portería. La forma del Pase se aplica a la imagen, el Pase vivo y el PDF.
- Paleta oscura reajustada: todos los pares pasan APCA (`fase3/oscuro-ajustado.json`, calculada con `paleta.py`).
- Revisión de voz sobre la lámina: 0 errores (1 aviso: la sigla OLED).
- Siguiente paso: respuesta de Nico. Después, la Fase 4 construye los tokens DTCG, `kino-brand.css`, el resto de departamentos, el sitio y la librería de Figma.

- 24 sep · La carpeta pasa a repositorio git (commit inicial 8bfa679) con CLAUDE.md, docs/proyecto y .claude/skills, para trabajar también desde sesiones de Claude Code en la nube.

## Parada 3 · respuesta (24 sep)
- Nico aprueba X1 a X10 como se propusieron y responde la pregunta 5 (X11: portería puede llamar al residente desde Kino).
- Siguiente paso: la Fase 4, en la rama `marca/fase-4`. Guía de arranque en `SESION-NUBE.md`.

## Fase 4 y Fase 5 · 24 sep (sesión en la nube, rama `marca/fase-4`)

**Informe de verificación de la Fase 5** (`branding/sistema/v3/verificacion/`: `fase5.py`, `informe.md`, `evaluaciones.md`)

| # | Comprobación | Resultado |
|---|---|---|
| 1 | Términos prohibidos, «permiso», exclamaciones y rayas en el texto visible | PASA · 0 |
| 2 | `npm run voz -- kino` sobre el texto visible y los textos de la app | PASA · 0 hallazgos |
| 3 | Límites de largo de UX writing | PASA · 46 de 46 |
| 4 | Tú y usted por audiencia, sin mezclar | PASA · 0 mezclas |
| 5 | APCA en todos los pares | PASA · 112 mediciones en los dos temas, 0 fallos |
| 6 | Diff entre DTCG, `kino-brand.css` y Figma | Ver el bloque 6 |
| 7 | Componentes sin ligar a variables | PASA en CSS; Figma, ver el bloque 6 |
| 8 | Decisiones sin justificación de la plataforma | PASA después de agregar la línea de justificación a P07, P09, P14 y V6 |
| 9 | Enlaces y anclas rotas | PASA · 46 anclas, 0 rotas |
| 10 | Cobertura de la definición de terminado | PASA · 81 de 81 elementos con su ancla |

**Evaluaciones independientes (subagentes)**
- Lector frío: 8 de 8 con cita. Claridad media de 3,9 en el ciclo 1 y 4,25 en el ciclo 2: **PASA**.
- Detector de IA: 17, 12 y 8 señales en los ciclos 1, 2 y 3. En el ciclo 3 quedan Motion (3) y Plataforma (2) por encima del máximo de 1, y 1 microcopy débil: **FALLA**.
  - Las 8 señales del ciclo 3 se corrigieron, pero el límite de 3 ciclos no permite volver a medir. Queda sin verificar y se reporta así.
  - Detalle en `evaluaciones.md`.

**Bloque 6 · Figma (25 sep)**
- 270 variables en cinco colecciones, iguales a DTCG en los dos modos, más 3 sombras como estilos de efecto (`branding/sistema/v3/figma/variables-figma.json`).
- 0 pinturas sin variable en 14 páginas. Con eso las comprobaciones 6 y 7 pasan y el informe queda en 10 de 10.
- Páginas llenas: guía de Componentes, Registro de cambios, Léeme con el estado de la versión, Plataforma sin la etiqueta de propuesta.

**Bloque 7 · Parada 4 (25 sep)**
- `parada-4.html` publicada: https://claude.ai/artifact/DBF7w1VTGPtJ9oQwdz4tXa. Generador en `branding/sistema/v3/parada4/`; compuerta de voz: 0 hallazgos.
- Vista previa del sitio 1.0.0: https://claude.ai/artifact/AJey2DjrB4K8oo92fn6pfg. Dentro del visor, el centro de descargas no baja archivos; al republicar el oficial hay que declarar la capacidad de descargas.
- Propuestas nuevas en `decisiones.md`: F4-P1 (llamada desde el Pase vivo) y F4-P2 (aviso de llegada).
- Defecto corregido: los PNG y el PDF del Pase se habían generado sin Archivo ni JetBrains Mono, porque Google Fonts no responde en el entorno. Las fuentes van incrustadas (`fuentes_incrustadas()` en `deptos/comun.py`) y las entregas se regeneraron. El PDF sigue en una página.

## Parada 4 · respuesta y segunda vuelta (25 sep)
- **Respuesta de Nico:** 1.0.0 aprobada salvo Figma y lo que se exporta de ella («especial atención en el auto-layout y spacing»); F4-P2 A; F4-P1 A; Vencido y Usado B; detector B. Pedido nuevo: aplicar la identidad al propio sitio.
- **Aplicado:**
  - Pase vivo vencido sin botón; aviso de llegada marcado como requisito; ícono de estado en Usado, Vencido y Revocado (F4-P3);
  - las tres observaciones del lector frío;
  - `sitio/identidad.css` (F4-P4): aurora en portada y aperturas, índigo en enlaces y rótulos, gota en el índice, relieve de membrana. Token nuevo `texto-enlace`: 120 mediciones sin fallos.
- **Figma:** 111 textos a «llenar», 7 filas del mismo alto, 38 espacios ligados, 0 desbordes, 72 entre marcos. Detalle en `branding/sistema/v3/figma/LEEME.md`.
- **Verificación:** 10 de 10. Detector de IA, ciclo 4: 1 señal, 0 en el microcopy, **PASA**.
- **Lámina:** `parada-4b.html` · https://claude.ai/artifact/Bn6AaiChNchG5dhx7BjtQ1. El artefacto oficial sigue sin republicarse.

## Parada 4b · respuesta y tercera vuelta (25 sep)
- **Respuesta de Nico:** aprueba Figma; F4-P4 A. Pide que las pantallas tomen la jerarquía de las piezas del Pase («toda la información igual se vuelve compleja de leer»). No entendió la pregunta de HikCentral: la visita no debía pedir correo.
- **Aplicado:**
  - 1.1.0 aprobada en `decisiones.md`, en Gobernanza, en el Registro de cambios de Figma y en el Léeme; artefacto oficial republicado (versión 4, con descargas);
  - título de `parada-4b.html` legible en tema claro;
  - F4-P5: cinco niveles (manda, vigencia, rótulo, grupo, acción) en Lista, Crear Pase, Detalle, Acceso por código y Límites. En el sitio (`deptos/d10_producto.py`, `deptos.css`) y en Figma (página Pantallas, componente Pase en lista). Las pantallas de la 1.1.0 quedan en `_obsoleto/d10_producto-2026-09-25.py` y en una sección de la página Pantallas;
  - «Entrar» pasa al botón secundario (X4); los rótulos pequeños, a texto secundario;
  - F4-P6: la fila de HikCentral explicada en la lámina, con dos opciones.
- **Verificación:** 10 de 10; 132 mediciones de contraste sin fallos (6 pares nuevos); voz 0; Figma 0 hallazgos de layout en Pantallas y Componentes; lámina sin desborde en 360, 768 y 1440 px.
- **Lámina:** `parada-4c.html` · https://claude.ai/artifact/NXuGd6VQc7k6Fqqi9pciZZ. Vista previa 1.2.0: https://claude.ai/artifact/W5U4Nw4AeZMpM7QZ4gsXcH.

## Parada 4c · respuesta (25 sep)
- **Respuesta de Nico:** F4-P5 A (lista en «Ahora» y «Próximos»); F4-P6 A (mensaje genérico de alta fallida).
- **Aplicado:** 1.2.0 aprobada en `decisiones.md`, Gobernanza, Registro de cambios de Figma (fila 100:206 en Vigente) y Léeme; la sección de pantallas 1.1.0 queda como «anteriores». Fase 5: 10 de 10; voz 0.
- **Artefacto oficial republicado** con la 1.2.0 (versión 5), leyéndolo primero; conserva la capacidad de descargas.
- **PR:** https://github.com/Amonsalvem/kino/pull/1, con la descripción corregida. Integrado a `main` por pedido de Nico (commit 5c756bb).

## 1.2.1 · Sitio responsive (25 sep)
- **Pedido de Nico:** «Hazlo completamente responsive», sobre el sitio.
- **Auditoría:** `scripts/auditar-responsive.mjs`, 16 secciones en 11 anchos (320 a 1920 px). Antes: tablas con 704 px de mínimo, matriz de 1500 px, mapa y árbol ilegibles en el teléfono, dos secciones con desborde a 320 px, textos de 10 px.
- **Construido:** `sitio/responsive.css`; tablas que se apilan como fichas (cada celda con `data-t`, que añade `construir.py`); matriz en fichas; mapa y árbol en HTML en pantallas angostas; columnas con `minmax(min(100%, …), 1fr)`; textos de al menos 11 px.
- **Verificación:** 176 vistas sin desborde; `verificar.py` y voz sin hallazgos; Fase 5 10 de 10; capturas en los dos temas sin errores.
- **Respuesta de Nico (25 sep):** F4-P7 A. 1.2.1 aprobada en `decisiones.md`, Gobernanza, Figma (fila 105:18) y el Léeme; oficial republicado (versión 6), leyéndolo primero.
- **Integración:** PR https://github.com/Amonsalvem/kino/pull/2 integrado a `main` por pedido de Nico (commit de8ba70).

## Motion · fuentes Lottie y Remotion (26 sep)
- **Pedido:** Prompt 2B. Lottie JSON fuente con colores como slots de tema, un wrapper `@remotion/lottie` para los mp4_preview y composiciones Remotion con salida ProRes 4444. La codificación final la hace el pipeline.
- **Construido en `branding/sistema/v3/motion/`:** `tokens.py` (DTCG a frames a 60 fps, curvas y colores); 16 recursos Lottie, cada uno completo y reducido, con 30 slots de color y temas dotLottie oscuro y claro; 4 composiciones Remotion (hero, hero móvil, revocado, turno de Portería), cada una con variante reducida y póster.
- **Bloqueados:** `flujo-trazo`, `loader-espera-lector` y `onboarding-3-lector-confirma` (`trazo` no tiene curva); el desplazamiento de `control-presionar` (no hay token de magnitud).
- **Verificación:** tipos sin errores; fotogramas revisados; ProRes 4444 con alfa y H.264 renderizados de punta a punta; voz 0.
- **Pendiente de Nico:** las preguntas del inventario de motion. Ninguna pieza está aprobada.

## Sistema de motion · @kino/motion 0.1 (26 sep)
- **Pedido de Nico:** libertad total en motion; dejar a un lado el hero y crear los componentes y herramientas para construir la web y la app con excelencia.
- **Construido en `paquetes/kino-motion/`:**
  - Tokens: los de marca más resortes físicos (tacto, hoja, pase, firme), `curva/salir` y reglas de coreografía. Salen como TS, CSS (resortes en `linear()`) y JSON portable.
  - Núcleo sin DOM: curvas, resortes analíticos, coreografía, máquina de estados del Pase (estado derivado de los hechos) y política de movimiento reducido.
  - Runtime web: `animar()` interrumpible, física de gestos, FLIP, View Transitions y 9 Web Components (pase, estado, vigencia, lista, acción, hoja, aviso, espera del lector, número).
  - Herramientas: inspector, `lint-motion`, Lab y pruebas de navegador.
- **Verificación:** 23 pruebas unitarias, lint 0 hallazgos, 14 pruebas en navegador (390 y 1280 px, claro y oscuro).
- **Lab:** https://claude.ai/artifact/NoNiKp5nbr3sM9bcsoCzTY
- **Pendiente de Nico:** stack de la web y la app; aprobar los tokens nuevos.

## Adaptador React Native · @kino/motion-nativo 0.1 (26 sep)
- **Pedido de Nico:** el adaptador de React Native con Reanimated.
- **Construido en `paquetes/kino-motion-nativo/`:** configuraciones de Reanimated desde los tokens (los resortes con los mismos parámetros físicos que la web); el plan de cada transición del Pase a partir de la partitura del núcleo; hooks (`usePaseMotion`, `useVigencia`, `usePresion`, `useHoja` con gesto, `useEntrada`, `useNumeroAnimado`); animaciones de disposición y componentes de referencia (`PaseKino`, `BotonKino`, `HojaKino`, `EsperaLectorKino`, `NumeroKino`).
- **Núcleo:** quedó sin DOM (lo que dependía del navegador pasó a `src/web`) y los tokens traen los colores de marca por tema para la app.
- **Verificación:** tipos sin errores contra RN 0.76 y Reanimated 3.16; 9 pruebas unitarias; arnés web con react-native-web y 9 pruebas en Chromium (estados, estado honesto, hoja lanzada con el puntero); lint-motion 0. El paquete web sigue en verde.
- **Pendiente:** probarlo en un simulador o dispositivo; decidir el stack.

## Motion 3D · segunda versión de las escenas (26–27 sep)
- **Pedido de Nico:** las tres escenas de Blender se veían mediocres; subirlas a nivel profesional, con libertad total en motion.
- **Construido en `branding/sistema/v3/motion/blender/`:** tokens y partitura de `@kino/motion` (`partitura.mjs`), resortes analíticos horneados, curva de tono propia con marcas de estado exactas (AOV), sombra y resplandor como los tokens `relieve/membrana` y `resplandor/vigente`. Pase con chip, dato, evidencia, barra, corte y tachado en siete clips; portería con lector, talanquera, marquesina, muros, vegetación, niebla y aurora, con la talanquera que sube solo tras la confirmación. La versión 1 queda en `_obsoleto/v1-2026-09-26/`.
- **GLB:** 471 KB con Draco, 41 piezas × 6 estados (`KHR_materials_variants`); visor nuevo probado en Chromium sin errores de consola.
- **Verificado:** 11 de 13 mediciones de color con el hex exacto (ΔE 0); el indicador de la portería queda a ΔE 0,9–1,1 aun con la cámara quieta, porque la niebla volumétrica le suma luz. Loop del Pase en reposo cerrado (diferencia máxima 1/255).
- **Costo:** EEVEE Next en CPU de 4 núcleos, sin GPU. Pase 28 s por frame, Pase en reposo 16,6 s, portería 49,3 s. Detalle en `blender/tiempos/`.
- **Defecto corregido en el camino:** en avisar, caducar y usar volvía el chip del estado anterior al final del clip (la última clave de un tramo interpolaba hacia el clip siguiente). Se corrigió y se re-renderizaron los tres.
- **Lámina:** https://claude.ai/artifact/8MzyYi7R99Cs5egeBFysvb
- **Reducidos:** Pase (fundidos en lugar de subida, escala y líneas; latido quieto) y portería (cámara quieta, talanquera por fundido, sin latido). La portería reducida calculó 97 de 260 frames: los tramos quietos se copian.
- **Galería republicada** (versión 4, con los 36 videos 3D nuevos): https://claude.ai/artifact/EiPApRKP6NNECfu5i5rKNV
- **Pendiente de Nico:** M3D-1 a M3D-7 en `decisiones.md`. Nada está aprobado.
- **Respuesta de Nico (27 sep):** M3D-1 A, M3D-2 A y M3D-3 A, aprobadas tal como se construyeron; no cambia ningún render. M3D-4 a M3D-7 siguen PROPUESTA.
- **Segunda respuesta de Nico (27 sep):** M3D-4 A, M3D-5 A, M3D-6 A y M3D-7 A. Las siete decisiones de motion 3D quedan aprobadas.
  - **Aplicado en `@kino/motion` y `@kino/motion-nativo`:** tarjeta en membrana, pista de la barra en elevada, fundido a través de chip, dato y nota con la regla común `nucleo/textos.ts`.
  - **Verificación:** web con 26 pruebas unitarias, `lint-motion` sin hallazgos y 18 pruebas en navegador (entre ellas, el fundido del chip a 1280 y 390 px); app con tipos sin errores, pruebas unitarias y 11 pruebas en el arnés web.
  - **Remotion y Lottie (27 sep):** tarjeta en membrana y pista en elevada; 14 recursos Lottie regenerados, 28 previews y los masters de hero, hero móvil y revocado re-renderizados (≈12 min de render y 5 de codificación). Galería republicada (versión 5).
  - **Pendiente:** M3D-5 en Remotion y Lottie (fundido a través con capas separadas) y las piezas del Pase del sitio, que esperan una versión nueva.

## Entrega 3 · prototipo, estrategia y Biblia (19 oct)
- **Pedido de Nico:** la entrega 3 para dos materias (Diseño para la interacción y Estrategia de servicio), con el formato de la entrega 2 y letra legible a distancia; QA del prototipo de Figma, exploración biopunk y prototipo que se use al darle play; brief con SOSTAC, SMART, KPI, horizonte de empresa y lista de mercado, siguiendo `Plan_estrategico.pdf` e `Indicadores_2.pdf`.
- **Construido:**
  - `entrega-3/qa-prototipo.md`: QA de «Kino · App» por ocho especialidades, con nodo y severidad.
  - `prototipo/`: app en código con cuatro actores y un solo estado, 17 interacciones implementadas y 3 planeadas, reloj acelerable y capa biopunk (E3-1).
  - `entrega-3/kino_entrega_3.html`: deck de 38 láminas con el prototipo adentro.
  - `entrega-3/estrategia.md`: la estrategia completa, con fuentes.
  - `entrega-3/Kino_Biblia_E3.docx`: plantilla Diex con 16 apartados llenos y el protocolo de validación 6.1.
- **Figma «Kino · App»:**
  - «{cupo}» reemplazado por 5 en 22 textos de pantalla.
  - «[PENDIENTE: unidad del cupo]» resuelto en las 3 pantallas de Límites.
  - Las 22 reacciones pasan a Smart Animate (curva crecer, 420 ms).
  - Página nueva «15 Prototipo navegable».
- **Verificación:**
  - e2e del prototipo: 15 de 15.
  - Deck a 1920×1080: ningún texto visible bajo 24 px, sin desborde a 1920, 1280 y 390 px.
  - Compuerta de voz: 0 errores en el deck, la estrategia y el QA. Los avisos son siglas (KPI, SMART).
- **Publicado:**
  - Deck: https://claude.ai/artifact/VqbNFqTNrLpK16JzfjBMr2
  - Prototipo: https://claude.ai/artifact/GbcN5QxL9P9r3F7eGfEGuk
- **Validación con usuarios:** no se inventaron participantes. Se hizo una evaluación por inspección con los arquetipos y quedó listo el protocolo para 5 residentes (27 oct – 7 nov).
- **Pendiente de Nico:**
  - E3-1 a E3-3.
  - Grupo y fecha de entrega en la portada de la Biblia.
  - Correr la prueba con residentes.
  - Las cinco preguntas de `estrategia.md` §11.

## Entrega 3 · barrido, portería y E3-2 (19 oct)
- **Pedido de Nico:** E3-1 A, E3-3 aprobada; E3-2 sin límite de visitas y con Pases largos (familiares que se quedan meses); mejorar la animación de aprobado y rechazado en portería; barrido de diagramación antes de seguir; lista de decisiones pendientes.
- **Barrido:** `prototipo/pruebas/barrido.mjs` sobre 23 pantallas. De 39 hallazgos medidos y 18 vistos en capturas a 0 de diagramación. Detalle: `entrega-3/barrido-diagramacion.md`.
- **Portería:** panel con retícula y coreografía nueva para entra y no entra.
- **E3-2:** sin cupo ni duración máxima; estadías de varias entradas; la administración fija solo franjas. Biblia, deck, estrategia y Figma actualizados; las variantes de cupo pasaron a «99 Descartes».
- **Decisiones nuevas PROPUESTA:** E3-4 (franjas en estadías), E3-5 (umbral de estadía), E3-6 (una sola entrada).
- **Verificación:** e2e 16 de 16; deck sin desborde y sin texto bajo 24 px.

## Entrega 3 · deck como un solo relato (19 oct)
- **Pedido de Nico:** no separar las materias; un relato que integre Interacción y Estrategia sin dejar ningún requerimiento.
- **Hilo:** una tarde de Carolina (Casa 14, Villas Campestres). 2:00 p. m. espera a su hermano; 2:01 crea el Pase; 2:02 le llega a Andrés; 3:04 entra; 6:10 Laura llega con el Pase vencido. Marta (colaboradora) y la mamá que se queda dos meses cubren A2 y E3-2. El cierre vuelve a las 3:04 con el aviso.
- **Cinco actos:** La tarde (problema, evidencia, diagnóstico, situación, tiempo) · El Pase (solución, objetivo y meta, implicaciones) · En uso (QA, prototipo por escena, biopunk, inventario, validación, Biblia) · El plan (SMART atados a una escena, conexión, SOSTAC, estrategias, tácticas, acción, KPI) · Después (1 año, horizonte, lista de mercado, fichas, preguntas abiertas).
- La escena es construida y se marca así; cada hecho que la sostiene es observado (reporte de inspección por rol).
- **Verificación:** 35 láminas sin desborde ni texto bajo 24 px; voz sin errores en láminas ni notas.

## Respuestas de Nico a las decisiones pendientes (19 oct)
- E3-4 A, E3-5 A, E3-6 B y los cuatro supuestos de E3-2 confirmados (`decisiones.md`).
- **E3-6 en el prototipo:** la visita entra y sale dentro de su vigencia; la segunda lectura entra; la visita ve «Puedes salir y volver hasta las…». El rechazo de prueba pasa a Juan Pablo, que llega antes de su hora. e2e 17 de 17.
- **HikCentral (Manuel vía Nico):** la vigencia por persona o visitante llega hasta 2037 o 2099. Cierra la pregunta 1 de `estrategia.md` §11; queda probar el alta por OpenAPI.
- **Biblia:** grupo «Diseño para la interacción», 2026-2. 6.1 rehecha como evaluación por inspección con los perfiles del estudio de mercado de iAgency (2024) y los arquetipos: 11 hallazgos, 6 resueltos, 3 planeados (Pase de evento, Pase familiar, editar recurrente), 1 pendiente (número extranjero).
- No se registraron participantes ni resultados de una prueba que no ocurrió.

## Motion e ilustración desde procesos reales (19 oct)
- **Pedido de Nico:** la espiral del lector no tenía que ver con la estética; investigar y crear las animaciones e ilustraciones de Kino.
- **Investigación:** tres frentes. Las guías de motion y la evidencia (Apple, Carbon, Material 3, WCAG, NN/g, Heer y Robertson, Phosphor); la biología documentada para cada estado del Pase; y el inventario de lo que la marca ya decidió. Síntesis en `entrega-3/motion-e-ilustracion.md` (PROPUESTA E3-8).
- **Construido en el prototipo:**
  - el veredicto de portería se lee en el primer cuadro;
  - la diana de la sinapsis reemplaza a la espiral;
  - el rechazo se contrae en lugar de sacudirse;
  - la talanquera pivota en el borde del poste;
  - Sin confirmar queda quieto;
  - al confirmarse hay un destello y tres latidos;
  - el brillo se fatiga en Por vencer;
  - el Pase nuevo germina;
  - el micelio, la membrana y la quitina dejan de moverse;
  - la red de Physarum muestra la sincronización en administración;
  - cuatro ilustraciones de una sola familia;
  - el movimiento reducido pasa a fundidos y la talanquera no gira.
- **OE1 (E3-7):** se mide con `prototipo/pruebas/oe1.mjs`: 3 toques y 8 s; visita nueva, 19,4 s (KLM).
- **Verificación:** e2e 17 de 17; barrido sin cortes; deck de 36 láminas sin desborde; fotogramas en `prototipo/build/fotogramas/`.

## Motion a nivel profesional · segunda pasada (19 oct)
- **Pedido de Nico:** el motion, las ilustraciones, los diagramas y las transiciones seguían viéndose amateur; encontrar la causa y resolverla.
- **Diagnóstico (7 causas):** un límite de 180 KB que no existía y dejó sin usar la escena 3D aprobada; cortes secos sin elemento compartido; gráficos de primitivas sin dirección de arte; brillo neón en todo; animaciones de una sola propiedad; E3-8 corregida de más contra F7; y un proceso sin cuadros clave ni revisión en video.
- **Decisiones de Nico:** videos 3D ya renderizados como archivos de apoyo (sin three.js) y empezar por los momentos héroe.
- **Construido:**
  - el build copia los videos y pósters a `prototipo/build/assets/` (unos 1,9 MB);
  - portería con la escena nocturna 3D: reposo, lectura, luz del lector, talanquera; rechazo desaturado con contracción;
  - crear: el botón crece y toma la forma del arco del Pase; la hoja se arrastra con física;
  - tarjeta → detalle y Pase creado → detalle con elemento compartido; al volver no se repite la cascada;
  - visita: la imagen del chat crece hasta el Pase vivo, que se inclina con reflejo y sombra;
  - inicio con la aurora oficial y brillo solo en el Pase vigente;
  - administración con la red Kino → HikCentral que fluye solo mientras sincroniza, y transición entre secciones.
- **Revisión:** `prototipo/pruebas/video.mjs` graba cada momento; comparación en `entrega-3/antes-despues/` y la lámina https://claude.ai/artifact/RYzKtmq3ZTzgfK5LEhBFbC.
- **Verificación:** e2e 17 de 17; OE1 3 toques y 8 s; barrido sin cortes.
- **Falta:** visto bueno de Nico; aprobar la corrección de E3-8; llevar el nivel al resto de la app.

## Motion · tercera pasada: el resto de la app (19 oct)
- **Pedido de Nico:** «Aprobado, lleva el mismo nivel al resto de la app». Queda aprobada la corrección de E3-8.
- **Criterio común:** toda entrada tiene salida; las listas tienen identidad y viajan con FLIP; el texto que cambia se funde; las cifras se cuentan; el contenido que cambia de forma releva al anterior sin saltar de alto.
- **Piezas nuevas** (`prototipo/src/componentes.tsx`, `movimiento.ts`): `usePresencia`, `Fundir`, `Digitos`, `Cifra`, `useFlip`, `useIndicador` y `Relevo`.
- **Errores corregidos:** la cicatriz del revocado quedaba pegada tras Deshacer; listas sin `key` animaban la fila equivocada; la instrucción del Pase vivo nunca entraba; «usado» no se tachaba en el detalle; la tarjeta vencida recuperaba la opacidad.
- **Sexto momento, el ciclo del Pase:** el borde punteado se cierra al confirmarse; el brillo y el color se apagan con transición al acercarse el vencimiento; la vida se vacía al vencer; el revocado corta, deja cicatriz y el velo entra; Deshacer retrae la cicatriz; extender destella la cuenta.
- **Por actor:** ingreso con relevo de pasos y salida de la notificación; pestañas con indicador, botón flotante que brota y se encoge, lista que se reacomoda al cambiar un Pase de grupo; hoja con indicadores y altura que se desliza; detalle con modos fundidos y cuenta por dígito; visita que vuelve al chat con el Pase encogiéndose hasta la imagen; portería con teclado como hoja, llegadas y bitácora con FLIP y latidos de llamada que se detienen a los 3; administración con menú indicador, cifras contadas y alerta que sale; escenario con indicador de actor, cascada de dispositivos y panel de notas que entra y sale.
- **Verificación:** e2e 18 de 18, también con `KINO_REDUCIDO=1`; OE1 3 toques y 8 s; barrido sin cortes; videos nuevos `estados`, `ingreso`, `pestanas`, `portero`, `franjas` y `escenario`.

## Deck de la entrega 3 en 15 láminas (19 oct)
- **Pedido de Nico:** quitar los subtítulos sobre los títulos; hacer la parte de Estrategia de Servicio simple y específica; acortar y contar rápido con diagramas y animación; portada con «Kino» grande, las dos materias, EAFIT y los autores.
- **Hecho:** `entrega-3/kino_entrega_3.html` pasa de 36 a 15 láminas, sin subtítulos encima de los títulos. El anterior queda en `entrega-3/_obsoleto/kino_entrega_3-36-laminas.html`.
- **Estrategia de Servicio, una lámina por pieza del curso:** objetivo general con meta en tres cifras; los 5 SMART en cinco columnas (acción, métrica, usuario, contexto, tiempo); una estrategia y una táctica por objetivo con quién y cuándo; línea de tiempo de 6 hitos; un KPI GQM por objetivo con fórmula, meta, etapa y frecuencia; seis fichas de producto. El detalle completo sigue en `estrategia.md` y en la Biblia.
- **Visual:** diagramas en HTML que se animan al entrar a cada lámina (flujo del Pase, brecha conocimiento–autoridad, embudo de validación, árbol estrategia–táctica, línea de tiempo), cifras contadas, videos del prototipo y el prototipo en vivo. Con movimiento reducido todo queda en su cuadro final.
- **Verificación:** `entrega-3/verificar.mjs` sin desborde ni errores en 1920, 1280 y 390 px y sin texto menor de 24 px; compuerta de voz sin errores.

## Biblia E3 en versión corta (19 oct)
- **Pedido de Nico:** el mismo barrido del deck aplicado a la Biblia.
- **Hecho:** `entrega-3/biblia/contenido.py` reescrito: de unos 27.600 a 15.700 caracteres (−43 %). Una idea por apartado, en tabla o figura. La versión larga quedó en `entrega-3/_obsoleto/biblia-contenido-larga.py` y `Kino_Biblia_E3-larga.docx`.
- **Portada:** el nombre del proyecto es «Kino». El campo Grupo sigue en «Diseño para la interacción», como pidió Nico.
- **Estrategia de Servicio:** 3.1 con los 5 SMART en columnas (acción, métrica, usuario, contexto, tiempo); 3.3 con una estrategia y una táctica por objetivo (quién y cuándo), el plan de acción y las 6 fichas; 3.4 con un KPI GQM por objetivo.
- **Figuras:** 5 diagramas del deck insertados (`construir_biblia.py` admite `('img', archivo, pie)`): brecha conocimiento–autoridad (1.1), insights (2.3), plan de acción (3.3), flujo del Pase (5.1) y validación (6.1).
- **Verificación:** la Biblia abre en LibreOffice (21 páginas con la plantilla); compuerta de voz sin errores.

## estrategia.md en versión corta (19 oct)
- **Pedido de Nico:** el mismo barrido del deck y la Biblia sobre `entrega-3/estrategia.md`.
- **Hecho:** de 30.400 a 21.100 caracteres (−31 %). Toda la prosa pasó a tablas; los SMART van en cinco columnas (acción, métrica, usuario, contexto, tiempo) con su punto de partida; las 6 fichas, en una tabla; dos diagramas Mermaid (conexión de los objetivos y gantt del plan de acción). Se conservan todas las piezas a las que remiten el deck y la Biblia (12 KPI con el principal marcado ★, 12 tácticas, horizonte, lista de mercado y fichas) y la numeración de los apartados. La versión larga quedó en `entrega-3/_obsoleto/estrategia-larga.md`.

## Textos del prototipo, mismo barrido (19 oct)
- Sin rótulos encima de los títulos: bienvenida («Hola, Carolina» con casa y comunidad debajo), portería en reposo y leyendo, panel de notas del escenario.
- Textos más cortos y concretos en ingreso, Avisos, Mi casa, hoja de crear, portería, administración, escenario y en las respuestas del inventario de interacciones (`modelo.ts`).
- Los rótulos de dato encima de su valor se mantienen: son regla aprobada de la marca (decisiones.md, Parada 3).
- Verificación: e2e 18 de 18, OE1 sin cambios, barrido sin cortes y compuerta de voz sin hallazgos.

## Deck: personajes, tablero de KPI y despedida (19 oct)
- **Personajes (PROPUESTA E3-9):** residente y administración en 2D vectorial, cartoon plano, animados con CSS en la lámina 2. Archivos en `entrega-3/personajes/`.
- **Tablero de seguimiento:** lámina nueva (14) con un panel por objetivo contra su meta. OE1 con datos medidos; OE2 a OE4 con datos de ejemplo marcados como tales; OE5 como plan.
- **Despedida:** última lámina sin texto. La aurora amanece, sube el bloque del logo, cae la gota, hay ondas y tres latidos. El sonido se sintetiza en el navegador: acorde grave, soplo, golpe de la gota y dos notas de «confirmado». Se repite tocando la lámina.
- **Notas del presentador** con el guion de las láminas 8, 9 y 17 (antes 15).
- **Verificación:** `verificar.mjs` sin desborde ni errores en 17 láminas; compuerta de voz sin errores.

## Biblia: SOSTAC explícito (19 oct)
- Subtítulos en 3.1 a 3.4 que dicen qué pieza de la guía se muestra: mapa SOSTAC con el apartado de cada letra, objetivo general, SMART, preguntas orientadoras, estrategias y tácticas, ejes estratégicos del curso, plan de acción, fichas de producto, KPI GQM, etapas de los KPI y tablero de seguimiento (figura nueva).

## estrategia.md: SOSTAC explícito (19 oct)
- Mapa SOSTAC al inicio con la sección de cada letra; cada encabezado dice qué pieza de la guía es (SOSTAC · S/O/S/T/A/C · …).
- Agregados: preguntas orientadoras SMART por objetivo, tabla de los cuatro ejes estratégicos, paso a paso GQM y función del KPI según la guía, etapas con el KPI que cubre cada una, explicación de «ingresos en minuta» y tablero de seguimiento. Fichas como «Descripción de productos». Numeración §0–§11 conservada.

## Prototipo: SOSTAC en el panel de notas (19 oct)
- Cada interacción muestra en el panel del escenario su lugar en el plan: SOSTAC · O (objetivo), S (estrategia y eje), T (táctica) y C (KPI). La lista de cobertura marca el objetivo de cada una. Fuente: `SOSTAC` en `prototipo/src/modelo.ts`, alineada con `estrategia.md`.
- Las pantallas de la app no llevan rótulos académicos: son el producto.
- e2e 18 de 18.

## Figma «Kino · App»: SOSTAC en las fichas (19 oct)
- Cada «Ficha · X» de las páginas 04 a 10 lleva debajo una tarjeta «SOSTAC · Estrategia de servicio» con cuatro líneas: O (objetivo), S (estrategia y eje), T (táctica) y C (KPI y etapa). Usa la misma fuente y el mismo color de la ficha, con borde punteado.
- 62 tarjetas: 04 → 8, 05 → 13, 06 → 10, 07 → 7, 08 → 7, 09 → 10, 10 → 7. Las pantallas P2 (R-X-01, R-X-02, P-E-06, P-E-07, A-09) dicen «P2: fuera del plan actual». A-08 apunta al horizonte E5.
- Mapa fuente: la misma tabla `SOSTAC` de `prototipo/src/modelo.ts` y `entrega-3/estrategia.md`. El script es idempotente: no duplica tarjetas si se vuelve a correr.

## Deck: barrido de muletillas y generalidades (19 oct)
- 16 frases genéricas cambiadas por el dato concreto. Insights de los arquetipos con el hecho observado (placa «Permitido», cuenta permanente por una tarde, sin acceso por días, alta sin aprobación); títulos de las láminas 4, 7, 9 y 18 sin metáforas («objeto vivo», «capa de autorización», «seis letras»); preguntas GQM de OE2, OE4 y OE5 medibles; F4 nombra la sincronización con HikCentral.
- `verificar.mjs` sin desborde ni errores en 19 láminas. Compuerta de voz: un error que se deja a propósito, «experiencia» en el nombre literal del eje 3 de la guía del curso.

## Biblia: barrido de muletillas y generalidades (19 oct)
- 22 frases cambiadas por el dato concreto, alineadas con el deck: insights de A1 a A4 con el hecho observado (1.3, 2.1, 2.3), conclusión de 2.2, visión sin «capa de autorización» (1.2), 1.1 sin la fórmula «es un problema de…», emoción buscada concreta (2.4), modelo mental del sistema con «da de alta» en lugar de «aprueba» (5.1, hecho vigente), relevancia de OE2 y OE5, «en lugar de» de la administración (3.2), F4 y las preguntas GQM de OE2, OE4 y OE5.
- Figura `arquetipos.png` capturada de nuevo desde la lámina 4.
- Compuerta de voz: los errores restantes son texto fijo de la plantilla Diex y el nombre literal del eje 3.

## estrategia.md: barrido de muletillas y generalidades (19 oct)
- 22 frases cambiadas por el dato concreto, alineadas con el deck y la Biblia: diferencia sin la fórmula «no es X, es Y» (§0), insights de A1 a A4 con el hecho observado (§1.2), conclusión del journey (§1.3), objetivo académico verificable (§2), relevancia de OE2 y OE5 (§3), las 8 preguntas GQM vagas de §7 vueltas medibles, visión sin «capa de autorización» (§9), S de empresa con cifras en lugar de «mercado grande y en crecimiento» (§9.3), F4 y F5 (§10), «salud» por «estado» de la sincronización.
- Numeración §0–§11 sin cambios. Compuerta de voz: un error que se deja a propósito, el nombre literal del eje 3.

## Personajes 3D terminados (19 oct)
- Render completo de residente y administración (45 cuadros cada uno, 15 fps). Videos VP9 con transparencia y póster en `entrega-3/personajes/`; `codificar.sh` en `branding/sistema/v3/motion/blender/` los rearma.
- Lámina 2 revisada; `verificar.mjs` sin desborde ni errores en 19 láminas. Deck republicado con los dos personajes.

## Prototipo: barrido de muletillas y generalidades (19 oct)
- Revisados ~560 textos. Las pantallas ya estaban en lenguaje concreto; cambiaron 5: el objetivo de I-13 e I-19 («Kino dice la verdad en la puerta» → «98 % de Pases confirmados en < 60 s»), el de I-17 («cómo lo perciben» → OE2 con su meta), I-18 («vive en la pantalla bloqueada» → «aparece») y la nota de Administración («se confirma en segundos» → «queda vigente cuando el lector lo confirma», sin prometer un tiempo).
- Tipos, build y e2e completos sin fallas. Prototipo y deck republicados.

## Objetivo general reescrito desde Kino (19 oct)
- Pedido de Nico: que parta de «Kino», proyecte el año y diga la posición. Nuevo: «Kino, en octubre de 2027, es el control de acceso de los conjuntos del Oriente antioqueño que ya tienen lector Hikvision: el residente da y revoca los Pases y la administración fija las franjas.» Más una línea de posición: autoriza sobre el lector que el conjunto ya pagó, sin cambiarlo, y la visita entra sin crear cuenta.
- Aplicado en el deck (lámina 10 y su guion), la Biblia (3.1) y `estrategia.md` (§2 y diagrama). `verificar.mjs` sin fallas.

## Lámina 13: tácticas explícitas (19 oct)
- Cada táctica separa el **qué** (nombre en negrita) del **cómo** (rótulo «Cómo» y el paso concreto con su cifra: 3 toques, semana 1, 711 altas, 10 conjuntos). Columnas reajustadas para que el eje quepa en una línea. Misma redacción en la Biblia 3.3.
- `verificar.mjs` sin fallas; compuerta de voz igual que antes (solo el nombre literal del eje 3).

## Objetivo general: investigación y reescritura (19 oct)
- Investigación en `entrega-3/investigacion-objetivo-general.md`: guía del curso, metodología de objetivos (verbo + unidad + contexto), OKR (significativo, concreto, sin cifras), posicionamiento (Moore) y SOSTAC. De ahí salen 8 criterios.
- Nuevo objetivo general: «Posicionar a Kino, a octubre de 2027, como el control de acceso con el que el residente decide quién entra a su casa, dentro de los límites de la administración y sobre el lector que el conjunto ya tiene.» El espacio (Oriente antioqueño) pasa a la meta. Se quita la línea «Posición» aparte: ya va dentro de la frase.
- Aplicado en el deck (lámina 10 y guion), la Biblia (3.1) y `estrategia.md` (§2 y diagrama). `verificar.mjs` sin fallas. Pendiente de aprobación de Nico.

## Objetivo general desde el boceto de Nico (19 oct)
- Boceto: «posicionar a Kino, a octubre 2027, como el aliado estratégico líder en software de seguridad de las propiedades horizontales». Versión final: «Posicionar a Kino, a octubre de 2027, como el aliado de la propiedad horizontal en control de acceso: el residente decide quién entra, la administración pone los límites y funciona con el lector que el conjunto ya tiene.»
- Cambios frente al boceto y su porqué en `entrega-3/investigacion-objetivo-general.md` §5: se quitan «estratégico» y «líder» (este último no se puede comprobar; queda la ruta para medirlo si el equipo lo quiere) y «seguridad» pasa a «control de acceso».
- Deck (lámina 10 y guion), Biblia 3.1 y `estrategia.md` §2. `verificar.mjs` sin fallas. Pendiente de aprobación de Nico.
