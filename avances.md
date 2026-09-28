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

## Prompt UX/UI en Figma · revisión y versión 1.2 (28 sep)
- **Pedido de Nico:** revisar `prompt.md`, `evals.md`, `LEEME.md` y `auditoria-uxui.js` (1.1) antes de usarlos, y aplicar los arreglos.
- **Hallazgos que bloqueaban:**
  - la librería `BO7UnDO9iE0aG6yUpNj0bc` no está publicada: `search_design_system` no encuentra «Botón de acción»;
  - la compuerta de voz, con la ruta de los evals, terminaba en 0 errores sin revisar nada (`voz.mjs` descarta rutas que no existen);
  - la auditoría no entraba en las secciones de Figma y eximía del arco toda pantalla con «Pase» en el nombre;
  - «R-A-07 Permiso de avisos» usaba la palabra prohibida.
- **Hecho en `prompts/uxui-figma/` (1.2):** ruta de voz corregida y comprobada; auditoría que entra en secciones, avisa si no ve pantallas, revisa qué dice el botón verde, el fondo y el modo del marco, y salta lo oculto; `probar-auditoria.mjs` con un Figma simulado (la 1.1 veía 1 de 3 pantallas); fuentes 05 a 07, 11 y 12 del sistema de marca; «marca blanca» del MAESTRO subordinada a F4; C14 sin cifras del conjunto en la app del residente; C21; LEEME sin `temperature` ni prefill, que la API actual rechaza. La 1.1 queda en `_obsoleto/uxui-figma-1.1/`.
- **Respuesta de Nico (28 sep):** D-UX-01 A y D-UX-02 A, aprobadas; librería publicada y comprobada con `search_design_system`. El prompt 1.2 queda listo para la Fase 0.
- **Fuera de este cambio:** el MAESTRO (§1 y §2) todavía dice «marca blanca», contra F4. Corregirlo toca el documento maestro y su copia canónica en el proyecto de claude.ai.

## UX/UI en Figma · Fases 0 y 1 (28 sep)
- **Archivo nuevo:** «Kino · App», https://www.figma.com/design/wXZ10ygSOp8RXINwg0ZvJw, en «Alejandro's team», con las 16 páginas del prompt 1.2. Consume la librería publicada por clave; la librería no se tocó.
- **Fase 0 · lo que trae la librería:** Botón de acción, Botón secundario, Campo, Selector de tipo, Estado (siete estados, Rechazado y Dato personal), Tarjeta de Pase, Pase en lista, íconos y logos; variables de color (Oscuro y Claro), tipografía (1440 y 360 px), espacio y radio; estilos de texto y de efecto. **Falta:** los 24 componentes de producto de la lista del prompt (barra superior e inferior, hoja inferior, diálogo, avisos, selectores de fecha, franja y días, fila de evento, línea de tiempo, tabla, etc.) y las variantes Usado, Vencido y Revocado de «Pase en lista».
- **Fase 0 · hallazgos:** la librería publica también componentes de la versión anterior («Estado» de seis estados, «Pase/Fila», «Pase/Boleto», «Tarjeta/Aviso»); la descripción de «Botón secundario» dice que sirve para revocar (F4-P5 dice botón de texto); la librería no aparece en `get_libraries` del archivo nuevo, pero sus componentes, variables y estilos se importan por clave sin problema.
- **Fase 1 · construido:** página 01 con el mapa de las cuatro superficies, la matriz rol × pantalla × acción × estado, el modelo de estados con diez transiciones (evento, quién, constancia y HikCentral) y la lámina de propuestas y pendientes; página 02 con once flujos (F-01 a F-11), cada uno con camino feliz (actor, paso, pantalla, regla y dato) y sus errores con salida.
- **Verificación:** `p5-verificar-layout.js` en 00, 01 y 02: 0 sin auto-layout, 0 espacios sueltos, 0 desbordes, 0 filas desiguales, 0 solapes. 0 pinturas sin variable y 0 textos sin estilo en 2.116 nodos. Voz: `textos/fase-1.md`, 1 texto revisado, 0 errores (los avisos son de la marca [TEXTO NUEVO]).
- **Propuestas:** D-UX-03 a D-UX-07 en `decisiones.md`.
- **Pendientes nuevos:** cierre del Pase de visita tras el primer ingreso por QR o placa; duración de Por vencer; vigencia y renovación del Pase de colaborador; umbral de integración caída; qué hace portería sin lector; rol del super administrador; quién otorga el Pase del personal del conjunto (A-08, choca con «solo el residente otorga»); ingreso de la administración (A-01); canal de «Escribir a administración»; registro de la llamada de portería.
- **Estado:** PARADA 1. Nada de la Fase 1 está aprobado.

## UX/UI en Figma · Fase 2 (28 sep)
- **Respuesta de Nico a la PARADA 1:** «Has todo lo que consideres óptimo y sigue adelante». D-UX-03 a D-UX-07 aprobadas por delegación; la limpieza de la librería queda como propuesta (D-UX-08).
- **Construido en la página 03 de «Kino · App»:** cinco láminas con 33 componentes o sets, cada uno con variantes, los dos temas y el par «Así / Así no»:
  - base: íconos reloj, calendario y copiar; Iniciales; Botón de texto; Chip de filtro; Esqueleto de carga;
  - navegación y acciones: Barra del teléfono, Barra superior, Barra inferior, Acción fija inferior, Hoja inferior, Diálogo, Aviso breve, Aviso de sistema;
  - entradas: Campo de código, Selector de fecha, Selector de franja horaria, Día y Selector de días, Control numérico, Buscador, Selector de modo;
  - listas y datos: Fila de lista, Fila de evento, Línea de tiempo de constancia, Estado vacío, Pase anterior, Cifra con denominador, Fila de tabla, Menú lateral, Barra de escritorio;
  - Pase: QR de maqueta, Ventana del QR (arco), Pase vivo en siete estados (en claro), Ficha de pantalla.
- **Verificación:** `p5-verificar-layout.js` en la página 03: 0 en todo después de corregir 7 desbordes y 2 filas desiguales. 0 pinturas sin variable y 0 textos sin estilo. Contraste: 12 pares nuevos en `pares.json`, 156 pares y 0 fallos. Voz: `textos/fase-2.md`, 0 errores.
- **Propuestas:** D-UX-08 (subir a la librería después de la Fase 3) y D-UX-09 (QR del Pase vivo solo mientras puede servir).
- **Estado:** PARADA 2 abierta; la Fase 3 sigue sobre las opciones A.

## UX/UI en Figma · Fase 3 (28 sep)
- **Construido en «Kino · App»**, cada pantalla en oscuro y claro, con su ficha y el nombre `<ID> · <Pantalla> · <Estado> · <Oscuro|Claro>`:
  - página 05 · Pases: R-P-01 a R-P-13 (Tus Pases, crear Pase paso a paso, detalle, extender, revocar, Pases anteriores) con sus estados, más variantes de reflujo a 320 y 430 px. Aurora local en la cabecera. 98 marcos;
  - página 04 · Acceso: entrada con WhatsApp, código, cédula contra el registro, casa, tratamiento de datos, avisos e instalación de la PWA. 32 marcos;
  - página 06 · Avisos, Mi casa y Cuenta: 21 marcos;
  - página 10 · Estados del sistema: sin conexión, error del servidor, lector caído, sesión vencida, versión nueva. 14 marcos.
- **Verificación:** `auditoria-uxui.js` 1.2 en 04, 05, 06 y 10: 165 marcos, 0 hallazgos (se corrigió «Sin contraseña.» en R-A-02, que nombraba lo que Kino no usa). `p5-verificar-layout.js`: 0 en las cuatro páginas. Espacios de no separación en 191 textos de horas y placas. Voz: `textos/fase-3.md`, 1 texto, 0 errores.
- **Pendientes nuevos:** texto legal de tratamiento de datos (Ley 1581 de 2012) por redactar con la administración, marcado en R-A-06; Reservas y Paquetes quedan como «Sección sin definir» en Mi casa.
- **Propuestas:** D-UX-10 (correcciones a la librería) y D-UX-11 (espacios de no separación).
- **Estado:** PARADA 3 abierta; la Fase 4 sigue bajo la delegación, sobre las opciones A.

## UX/UI en Figma · Fase 4 (28 sep)
- **Respuesta de Nico durante la fase:** «Apruebo todo lo que se realice en figma, no me vuelvas a solicitar permisos». D-UX-08 a D-UX-14 aprobadas; permisos del conector de Figma preaprobados en `.claude/settings.json`.
- **Construido en «Kino · App»:**
  - página 07 · Visita, 27 marcos:
    - V-L-01, Pase vivo, en 7 estados en QR y 4 en Placa y Código (claro);
    - V-L-02, Pase vivo de colaborador, con dos variantes de vigencia;
    - V-I-01, imagen del Pase (432 × 540, exporta a 1080 × 1350);
    - V-W-01 a V-W-03, WhatsApp en oscuro y claro;
    - V-D-01, PDF en tamaño carta;
  - página 08 · Portería a 1280 px, 17 marcos:
    - P-E-01 en oscuro y claro;
    - P-E-02 en reposo, llamando y no contestó;
    - P-E-03, buscar, con y sin resultados;
    - P-E-04, código, con y sin teclado, en cinco estados;
    - P-E-05, lector sin respuesta, con dos variantes;
    - P-E-06 y P-E-07 en P2;
  - página 09 · Administración a 1440 px y en usted, 17 marcos:
    - A-01, ingreso;
    - A-02, resumen, en oscuro y claro;
    - A-03, límites, en cuatro estados;
    - A-04, constancia;
    - A-05, constancia de un Pase, con dos variantes;
    - A-06, residentes con alta fallida;
    - A-07, lector caído y en orden;
    - A-08 y A-09, sin definir;
    - A-10, correo semanal;
  - página 03: la Ventana del QR con Modo (9 variantes) y el componente nuevo «Imagen del Pase» (Visita y Colaborador).
- **Verificación:**
  - `auditoria-uxui.js` en 07, 08 y 09: 61 marcos, 0 hallazgos.
  - `p5-verificar-layout.js`: 0 en las tres, después de ligar los espacios sueltos a `espacio/*` y de igualar 12 filas en portería.
  - Voz: `textos/fase-4.md`, 1 texto, 0 errores.
- **Pendientes nuevos:**
  - número y plantilla de WhatsApp aprobada por Meta;
  - si portería ve Pases de otros días;
  - cómo entra portería (turno o equipo);
  - si Kino puede ordenar a HikCentral abrir la talanquera;
  - exportar la constancia y cuánto tiempo se guarda;
  - reintento del alta fallida;
  - destinatarios y día del correo semanal.
- **Siguiente:** subir a la librería los componentes de D-UX-08 y D-UX-10 (Nico publica desde Assets); Fase 5 (prototipos, motion y handoff).

## UX/UI en Figma · Fase 5 (28 sep)
- **Prototipos:** cinco flujos sobre las pantallas originales, sin copias, cada uno con su punto de inicio en el panel Prototype de su página:
  - crear Pase hasta Vigente (05);
  - revocar (05);
  - Pase vivo desde el WhatsApp (07);
  - rechazo en portería (08);
  - fijar límites (09).
  Los estados que dependen del sistema avanzan solos: Enviando 1,2 s; confirmación del lector 2 s; Revocando 0,8 s; baja en el lector 3 s.
- **Página 11:** índice de los flujos (pasos y qué prueba cada uno).
- **Página 12:** once notas de movimiento, cada una con verbo, token de la sección 12, duración, alternativa reducida y pantallas. La navegación entre pantallas es un fundido de 240 ms; no es movimiento de marca.
- **Página 13:** accesibilidad de las pantallas P0 (orden de foco, encabezados, aria-live, notas) y lámina de handoff (nombres, modos, componentes, textos, pendientes, verificación).
- **Estado:** aprobada por la respuesta del 28 sep sobre lo hecho en Figma. Sigue la Fase 6.
