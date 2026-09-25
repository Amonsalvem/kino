# Traspaso · Sistema de marca Kino

Última actualización: 23 sep 2026, noche. Este archivo sirve para que otra sesión de Claude retome el trabajo exactamente donde quedó. Manda sobre el historial de cualquier chat anterior.

## 1. Cómo arrancar una sesión nueva

1. Abre una tarea nueva en Claude (Cowork) **dentro del proyecto «Kino»** y conecta la carpeta `…/iCloud Drive/Documents/montesereno/projects/kino`.
2. Pega este mensaje como primero:

> Continuamos el sistema de marca de Kino. Lee, en este orden:
> 1. `kino/TRASPASO-SISTEMA-DE-MARCA.md`;
> 2. `kino/encargo-sistema-de-marca.md`, el encargo completo, que sigue vigente;
> 3. `kino/avances.md`;
> 4. `kino/decisiones.md`.
>
> La Parada 3 está aprobada. Sigue la Fase 4 (ver §9).

Con eso basta. Si la carpeta no está conectada, las copias de `avances` y `decisiones` también están en el proyecto como `claude/avances-sistema-de-marca.md` y `claude/decisiones-sistema-de-marca.md`.

## 2. Dónde estamos

| Fase | Estado |
|---|---|
| 0 · Auditoría | Cerrada: `auditoria.md` |
| 1 · Plataforma y arquitectura | Aprobada (Parada 1) |
| 2 · Verbal | Aprobada (Parada 2) |
| V7 · Pase entregado como imagen más enlace | Aprobada |
| 3 · Identidad visual | Aprobada (Parada 3, 24 sep): X1 a X11 |
| 4 · Construcción | 1.2.0 aprobada el 25 sep (F4-P5 A, F4-P6 A); oficial republicado (versión 5). Falta integrar a `main` |
| 5 · Verificación y evaluaciones | 10 de 10. Lector frío PASA; detector de IA PASA en el ciclo 4 |

**Sin preguntas abiertas.** La Parada 4c se respondió el 25 sep: F4-P5 A y F4-P6 A. El PR https://github.com/Amonsalvem/kino/pull/1 espera que Nico lo integre.

Las respuestas a las Paradas 4, 4b y 4c (25 sep) están en `decisiones.md`, «Estado tras la respuesta del 25 sep», «(segunda vuelta)» y «(tercera vuelta)».

## 3. Enlaces

| Qué | Enlace |
|---|---|
| Parada 1 (lámina) | https://claude.ai/artifact/EuPrHetctevY4PGiVAohiM |
| Parada 2 (lámina) | https://claude.ai/artifact/JZmNsBpL9zizPj29yxE8x9 |
| Parada 3 (lámina) | https://claude.ai/artifact/788FzxvYPNk3557owP4Mms |
| Parada 4 (lámina) | https://claude.ai/artifact/DBF7w1VTGPtJ9oQwdz4tXa · copia en `parada-4.html` |
| Parada 4b (segunda vuelta) | https://claude.ai/artifact/Bn6AaiChNchG5dhx7BjtQ1 · copia en `parada-4b.html` |
| Parada 4c (tercera vuelta, 1.2.0) | https://claude.ai/artifact/NXuGd6VQc7k6Fqqi9pciZZ · copia en `parada-4c.html` |
| Vista previa del sitio 1.2.0 | https://claude.ai/artifact/W5U4Nw4AeZMpM7QZ4gsXcH |
| Vista previa del sitio 1.1.0 | https://claude.ai/artifact/NnuVUWwUdgk34VHkj3H5Rd |
| Vista previa del sitio 1.0.0 | https://claude.ai/artifact/AJey2DjrB4K8oo92fn6pfg (copia de `Kino_Sistema_de_marca.html`) |
| Vista previa del sitio v3 (Paradas 1 y 2) | https://claude.ai/artifact/NGW6EEiRghDxq4uFzvsjBa |
| Artefacto oficial «Kino · Sistema de marca» | https://claude.ai/artifact/K8R2PRduS6SHBKYU31Bo6L (1.2.0, versión 5, con la capacidad de descargas) |
| Figma | https://www.figma.com/design/BO7UnDO9iE0aG6yUpNj0bc |

Los artefactos se publicaron desde otra sesión. Una sesión nueva no puede republicarlos por ruta de archivo:
- para actualizar uno, hay que leerlo primero con Artifact `read` y publicar pasando su `url`;
- una lámina nueva de parada se publica como artefacto nuevo.

## 4. Archivos (todos bajo `kino/`)

| Ruta | Qué es |
|---|---|
| `encargo-sistema-de-marca.md` | El encargo original, textual |
| `avances.md` | Bitácora por fase y departamento |
| `decisiones.md` | Todas las decisiones con su estado: F (firmes), H (heredadas), P (Parada 1), V (Parada 2), X (Parada 3) |
| `auditoria.md` | Matriz de 90 elementos y los hechos P1–P15 que sostienen la plataforma |
| `parada-1.html`, `parada-2.html`, `parada-3.html` | Copias locales de las láminas |
| `gorr-brand-system/clientes/kino/01-estrategia/posicionamiento.md` | Posicionamiento con el método Dunford (aprobado, opción A) |
| `gorr-brand-system/clientes/kino/voz.json` | Voz: 42 patrones, calibración 40/42 con 0 falsos positivos |
| `gorr-brand-system/clientes/kino/02-verbal/` | `guia-de-contenido.md`, `ux-writing.md` y `patrones-nuevos.json` |
| `branding/sistema/v3/sitio/` | Fuentes del sitio nuevo (ver §5) |
| `branding/sistema/v3/sitio/build/kino-sistema-de-marca.html` | El sitio armado |
| `branding/sistema/v3/fase3/` | Exploración de la Parada 3: `explorar.src.html`, `build.py`, `apca.py`, `paleta.py`, `oscuro-ajustado.json` |

**Fuentes del sitio (`v3/sitio/`)**

| Archivo | Qué hace |
|---|---|
| `construir.py` | Arma el HTML. Toma los tokens de `gorr-brand-system/clientes/kino/build/kino-tokens.css` y, si no existe, de la copia local |
| `contenido/00-inicio.html` | Inicio con las dos puertas, «Conocer Kino» y «Usar la marca» |
| `contenido/01-plataforma.html` | Departamento 1 completo, escrito a mano |
| `verbal.py` | Fuente única del departamento 2. Genera `contenido/02-verbal.html`, `build/guia-de-contenido.md`, `build/ux-writing.md`, `build/muestras-ux.md` y `build/verbal-verificacion.json` |
| `secciones.py` | Genera los departamentos 03 a 12, hoy en construcción, y el glosario (32 términos), en `contenido/02-12.html` |
| `sitio.css`, `sitio.js` | Estilo y navegación: rutas por ancla `#seccion.subseccion`, búsqueda, índice, tema claro u oscuro |
| `verificar.py`, `probar.mjs` | Comprobaciones locales: rayas, «permiso», mezclas de tú y usted, largo de textos, patrones |
| `texto-visible.md` | Lo genera `construir.py`. Excluye los ejemplos incorrectos (`.no`, `.antes`) y es la entrada de `npm run voz` |

## 5. Cómo se reconstruye y se verifica

**Sitio**, desde la carpeta `branding/sistema/v3/sitio`:
```bash
python3 verbal.py && python3 secciones.py && python3 construir.py
```

**Compuertas de voz**, desde `gorr-brand-system`:
```bash
npm run calibrar-voz -- kino    # esperado: 40/42 · 0 falsos positivos
node herramientas/voz.mjs kino ../branding/sistema/v3/sitio/texto-visible.md ../branding/sistema/v3/sitio/build/muestras-ux.md   # esperado: 0 hallazgos
```

**Lámina de la Parada 3**: `cd branding/sistema/v3/fase3 && python3 build.py`. Lee los tokens y el sprite de `../sitio/`.

**APCA**: `apca.py` implementa APCA-W3 0.1.9 y reproduce `reportes/contraste.json`. `paleta.py` recalcula la paleta oscura ajustada.

## 6. Lo que la sesión anterior aprendió (evita tropiezos)

**La conexión con el Mac se cae seguido.**
- Trabaja en el contenedor y copia a la carpeta con `device_commit_files`.
- Antes de depender de una herramienta del Mac, copia al contenedor lo que necesites con `device_stage_files`: `herramientas/*.mjs`, `lib/cliente.mjs`, `voz.json`, `pruebas/`. Crea también un `marca.config.json` mínimo.
- Si la conexión falla dos veces, sigue en el contenedor y sincroniza después.

**En el contenedor, npm no instala paquetes** (colorjs y apca-w3 dan 403).
- Usa `apca.py` para el contraste.
- Playwright y Chromium sí están, en `/opt/pw-browsers/chromium`. Enlaza `node_modules` a `~/.npm-global/lib/node_modules`.

**Figma**
- Carga la skill `figma-use` antes de cada `use_figma`.
- Cambia de página una sola vez por llamada. Para mover nodos entre páginas, usa `loadAsync` sobre la página destino.
- Fuentes disponibles: Archivo (Regular a Black) y JetBrains Mono.

**Artefactos**
- El HTML se publica sin doctype; `construir.py` genera `build/artefacto.html` para eso.
- En los SVG hay que fijar `width`, `height` y `aspect-ratio`. En Chrome, el mapa y el logo se cortaban sin eso.

**Texto visible**
- Nada académico: ni curso, ni fase, ni entrega, ni fechas de entrega.
- No usar «permiso» ni «contraseña», ni siquiera para explicar.
- Horas con espacio duro: `construir.py` ya lo aplica a horas, placas y códigos.

**Cómo le gusta trabajar a Nico**
- Todo en español.
- Paradas con lámina visual, alternativas con una recomendada y máximo 5 preguntas ordenadas por impacto.
- Pide baja carga cognitiva para el usuario final.
- Aprueba en bloque («todo lo demás es aprobado»). Lo que no aprueba de forma explícita sigue en PROPUESTA.

## 7. Decisiones clave vigentes (detalle en `decisiones.md`)

**Firmes**
- Logo conservado.
- Dirección biopunk.
- «Pase», nunca «permiso».
- Kino con identidad propia; el conjunto es solo un dato.
- Perfil NN/g 2-1-1-2.
- Motion intacto.

**Aprobadas**
- Posicionamiento A: la administración, el hardware instalado y el Pase sin cuenta.
- Personalidad: Exacto, Franco, Discreto.
- Cinco valores con su comportamiento.
- Nombres: Kino, Kino Administración, Kino Portería.
- Se puede nombrar a Monte Sereno con cifras.
- El sitio muestra una sección a la vez.
- Tratamiento: usted con la administración, tú con residente y visita.
- «Pase» con mayúscula.
- Horas: 12 h en texto y 24 h en datos.
- «Visita» en vez de «invitado».
- Estados:
  - del Pase: Previsto, Sin confirmar, Vigente, Por vencer, Usado, Vencido, Revocado;
  - evento en la entrada: Rechazado.
- Patrones de voz nuevos.
- V7: imagen del Pase más enlace al Pase vivo; PDF opcional; WhatsApp de 23 a 28 palabras.

**Propuestas (Parada 3)**: X1 a X10.
- Forma Portal.
- Gota en acento.
- Oscuro reajustado.
- Acento de acción #00D595.
- Archivo al 112 %.
- Trazo 1,7.
- Aurora.
- Radio 14 y arco.
- Motion «crecer».
- Paleta de estados.

## 8. Pendientes (no bloquean)

- Vector original del logo y licencia de Arkit ExtraBold.
- Mensajes reales de portería o WhatsApp.
- Citas de las 5 entrevistas con residentes.
- Confirmar con Manuel si HikCentral acepta una credencial temporal sin crear persona. Es la prueba del Pase sin cuenta.
- Unidad de los cupos: por casa, por residente o por conjunto.
- Si el lector tiene teclado para el código.
- Confirmar que portería puede llamar al residente desde Kino (X11): la inspección no registró esa función.
- El deck de diagnóstico del 4 sep y el Anexo de sustentación no están en la carpeta.

## 9. Siguiente trabajo, en orden

**1. Parada 3 cerrada** el 24 sep: X1 a X11 aprobadas en `decisiones.md`.

**2. Fase 4 y Fase 5 construidas** (24 y 25 sep, rama `marca/fase-4`, un commit por bloque):
- Bloque 1 · tokens: paleta aprobada, 203 primitivos y 70 semánticos por tema, 112 mediciones WCAG y APCA sin fallos.
- Bloque 2 · departamentos 03 a 12 en el sitio (`branding/sistema/v3/sitio/deptos/`).
- Bloque 3 · piezas del Pase (`branding/sistema/v3/pase/`): imagen, Pase vivo, PDF, señal de la entrada y portería. Las fuentes van incrustadas desde el 25 sep; antes los PNG y el PDF salían con una fuente de reemplazo.
- Bloque 4 · sitio definitivo `Kino_Sistema_de_marca.html` con el Motion Playground; el borrador está en `_obsoleto/`.
- Bloque 5 · verificación (`branding/sistema/v3/verificacion/`): 10 de 10 PASA; lector frío PASA; detector de IA FALLA con las 8 señales del ciclo 3 corregidas y sin volver a medir.
- Bloque 6 · Figma: 270 variables iguales a DTCG en los dos modos, más 3 sombras como estilos de efecto; componentes con todos sus estados; 15 páginas. Scripts y exportación en `branding/sistema/v3/figma/` (ver su `LEEME.md`).
- Bloque 7 · `parada-4.html` publicada; propuestas F4-P1 y F4-P2 en `decisiones.md`.

**3. Parada 4 respondida el 25 sep; segunda vuelta respondida el mismo día.**
- Hecho: F4-P1 y F4-P2 (A), F4-P3 (íconos en chips), las tres observaciones del lector frío, detector ciclo 4 (pasa), Figma revisada, F4-P4 aplicada al sitio.
- Al recibir la respuesta a `parada-4b.html`:
  1. Anotar en `decisiones.md` el estado de F4-P4 y de la librería de Figma. Si F4-P4 es B: en `sitio/identidad.css`, la aurora solo en `.portada`; `.abre` en superficie elevada.
  2. Pregunta 3 (A): cambiar el texto en `sitio/verbal.py` (fila «Incorrect request parameter»).
  3. Pasar 1.1.0 a «Aprobada» en `d12_gobernanza.py` (CAMBIOS), en Figma (Registro de cambios 69:2, fila v1.1.0) y en el Léeme (texto 22:143).
  4. Reconstruir (`secciones.py`, `construir.py`), correr `fase5.py ../figma/variables-figma.json` y la compuerta de voz.
  5. Republicar el artefacto oficial `K8R2PRduS6SHBKYU31Bo6L`: leerlo con Artifact `read`, publicar `Kino_Sistema_de_marca.html` con su `url` y declarar la capacidad de descargas.
  6. Nico integra `marca/fase-4` a `main`.
- Hecho tras la respuesta a la 4b: pasos 1 a 5 (Figma aprobada, F4-P4 A, 1.1.0 aprobada, oficial republicado como versión 4).

**4. Tercera vuelta (1.2.0) respondida el 25 sep: F4-P5 A, F4-P6 A.** Pasos 1 a 3 hechos; queda el 4. Construido: pantallas con la jerarquía del Pase (F4-P5) en el sitio y en Figma, y la fila de HikCentral explicada (F4-P6). Al recibir la respuesta a `parada-4c.html`:
  1. Anotar F4-P5 y F4-P6 en `decisiones.md`. Si F4-P5 es B: en `deptos/d10_producto.py` (`_lista`), volver a las pestañas «Activos / Anteriores» en lugar de los grupos, y lo mismo en Figma (98:95). Si F4-P6 es B: quitar la fila en `sitio/verbal.py`.
  2. Pasar 1.2.0 a «Aprobada» en `d12_gobernanza.py`, en Figma (Registro de cambios, fila v1.2.0 100:206) y en el Léeme (22:143).
  3. Reconstruir, correr `fase5.py` y la compuerta de voz, y republicar el oficial leyéndolo primero, con `capabilities: {downloads: true}`.
  4. Nico integra `marca/fase-4` a `main`.

## 10. Estado de Figma

- **Archivo**: `BO7UnDO9iE0aG6yUpNj0bc`, en la cuenta de Alejandro. En una sesión en la nube, el conector de Figma escribe con `use_figma`; la red no deja bajar las capturas al repositorio.
- **Páginas** (15, todas llenas): Léeme, Plataforma, Voz y UX writing, Logo, Color, Tipografía, Iconografía, Imagen, Estructura, Motion (specs), Componentes, Pantallas, Aplicaciones / Plantillas, Registro de cambios, Referencias.
- **Variables**: Primitivos 128, Color 52 (Oscuro y Claro, con `texto/enlace`), Espacio y radio 35, Movimiento 28, Tipografía 28 (1440 px y 360 px). Code syntax `var(--kino-*)` y alcances en todas. Las 4 colecciones anteriores quedaron dentro de estas; no se borró ninguna variable.
- **Componentes** (página Componentes): guía (71:38), íconos (56:2), logo (56:114), Botón de acción, Botón secundario, Campo, Selector de tipo (57:3), Estado, Tarjeta de Pase y Pase en lista (96:100, 1.2.0) en 58:2.
- **Pantallas** (22:65): Lista 98:95, Crear 98:160, Detalle 99:143, Acceso por código 99:187, Límites 99:217 (1.2.0, aprobada). Las de la 1.1.0, en la sección 98:94 (anteriores).
- **Verificación**: `branding/sistema/v3/figma/exportar_variables.py`, 0 diferencias y 0 pinturas sin variable (25 sep). Auto-layout y espaciado: `figma/js/p5-verificar-layout.js`, 0 hallazgos en 14 páginas.

## Repositorio (24 sep)

La carpeta `kino` es un repositorio git (rama `main`). El historial vive en `.git.nosync` para que iCloud no lo sincronice a medias; `.git` es un enlace simbólico a esa carpeta. `CLAUDE.md` lleva las instrucciones del proyecto para sesiones de Claude Code (nube o terminal) y `docs/proyecto/` las copias de los documentos de conocimiento de claude.ai. Si un documento cambia en claude.ai, se actualiza también aquí. `branding/sistema/**/build/` no se versiona: se regenera con `construir.py`.
