# Avances · Sistema de marca Kino

Bitácora del encargo «de borrador a sistema completo». Si una sesión nueva empieza, lee este archivo y retoma desde **Siguiente paso**.

## Estado actual

**PARADA 4, tercera vuelta, pendiente** (25 sep). La 1.1.0 está aprobada (Figma y F4-P4 A) y el artefacto oficial la tiene. La 1.2.0 propone pantallas con la jerarquía del Pase (F4-P5) y el mensaje de alta fallida en HikCentral (F4-P6). Lámina: `parada-4c.html` · https://claude.ai/artifact/NXuGd6VQc7k6Fqqi9pciZZ

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
| 10 | Producto | Aprobado (1.1.0); pantallas con la jerarquía del Pase en revisión (F4-P5) | Componentes, 5 pantallas, WCAG |
| 11 | Aplicaciones | Aprobado (1.0.0) | 15 piezas; Pase vivo vencido sin botón (F4-P1) |
| 12 | Gobernanza | Aprobado (1.0.0) | Registro, revisión, 17 pendientes, descargas |
| — | Sitio | 1.1.0 aprobado y publicado en el oficial; 1.2.0 en revisión | `Kino_Sistema_de_marca.html` · vista previa 1.2.0 https://claude.ai/artifact/W5U4Nw4AeZMpM7QZ4gsXcH |
| — | Figma | 1.1.0 aprobada; pantallas 1.2.0 en revisión | 271 variables iguales a DTCG; componente nuevo Pase en lista; pantallas 1.1.0 en su sección |

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
- Artefacto oficial (1.1.0, versión 4): https://claude.ai/artifact/K8R2PRduS6SHBKYU31Bo6L
- Vista previa del sitio 1.1.0: https://claude.ai/artifact/NnuVUWwUdgk34VHkj3H5Rd
- Vista previa del sitio 1.0.0: https://claude.ai/artifact/AJey2DjrB4K8oo92fn6pfg
- Vista previa del sitio v3: https://claude.ai/artifact/NGW6EEiRghDxq4uFzvsjBa
- Figma: https://www.figma.com/design/BO7UnDO9iE0aG6yUpNj0bc

## Siguiente paso
1. Nico responde las dos preguntas de `parada-4c.html`: F4-P5 (A con grupos Ahora y Próximos, o B con pestañas) y F4-P6 (A mensaje genérico o B quitar la fila).
2. Al aprobar la 1.2.0: aplicar la respuesta, reconstruir, verificar y republicar el artefacto oficial leyéndolo primero (ver §9 del traspaso).

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
