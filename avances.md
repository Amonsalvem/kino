# Avances · Sistema de marca Kino

Bitácora del encargo «de borrador a sistema completo». Si una sesión nueva empieza, lee este archivo y retoma desde **Siguiente paso**.

## Estado actual

**PARADA 3 pendiente de aprobación** (23 sep). Paradas 1 y 2 aprobadas; V7 (imagen más enlace) aprobada.

| # | Departamento | Estado | Ronda | Nota |
|---|---|---|---|---|
| 1 | Plataforma | Construido · PROPUESTA | 1 de 3 | Pendiente de aprobación. Ver evaluación abajo |
| 2 | Verbal | Construido · PROPUESTA | 1 de 3 | 36 momentos, 46 textos en límite, 37 entradas de vocabulario, 32 términos de glosario, 6 plantillas de WhatsApp. voz.json con 42 patrones; calibración 40/42, 0 falsos positivos; voz 0 hallazgos |
| 3 | Logo | No iniciado | — | |
| 4 | Color | No iniciado | — | Hallazgo APCA del tema oscuro, para la Parada 3 |
| 5 | Tipografía | No iniciado | — | |
| 6 | Iconografía | No iniciado | — | |
| 7 | Imagen | No iniciado | — | |
| 8 | Estructura | No iniciado | — | |
| 9 | Motion | No iniciado | — | |
| 10 | Producto | No iniciado | — | |
| 11 | Aplicaciones | No iniciado | — | |
| 12 | Gobernanza | Parcial | — | Quién decide y pendientes, ya en el sitio |
| — | Arquitectura del sitio | Construida · PROPUESTA | 1 | Índice, dos puertas, búsqueda, anclas, teclado, 360 px, claro y oscuro |
| — | Figma | 15 páginas espejo | 1 | Contenido anterior en «Referencias». Léeme y Plataforma construidas con variables |

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
- Vista previa del sitio v3: https://claude.ai/artifact/NGW6EEiRghDxq4uFzvsjBa (el artefacto oficial K8R2PRduS6SHBKYU31Bo6L no se toca hasta la Parada 4)
- Figma: https://www.figma.com/design/BO7UnDO9iE0aG6yUpNj0bc

## Siguiente paso
1. Nico responde las preguntas de la Parada 1 (`parada-1.html`).
2. Al aprobar:
   - marcar las decisiones P01 a P13 como APROBADA;
   - pasar a la Fase 2 (Verbal).

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
