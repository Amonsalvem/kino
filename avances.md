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
