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
> Estamos en la Parada 3, pendiente de mi respuesta. Mis respuestas: [pega aquí tus respuestas a las 5 preguntas de la Parada 3, o «vuelve a presentarme la Parada 3»].

Con eso basta. Si la carpeta no está conectada, las copias de `avances` y `decisiones` también están en el proyecto como `claude/avances-sistema-de-marca.md` y `claude/decisiones-sistema-de-marca.md`.

## 2. Dónde estamos

| Fase | Estado |
|---|---|
| 0 · Auditoría | Cerrada: `auditoria.md` |
| 1 · Plataforma y arquitectura | Aprobada (Parada 1) |
| 2 · Verbal | Aprobada (Parada 2) |
| V7 · Pase entregado como imagen más enlace | Aprobada |
| 3 · Identidad visual | **Parada 3 presentada, esperando respuesta de Nico** |
| 4 · Construcción | No iniciada |
| 5 · Verificación y evaluaciones | No iniciada |

**Preguntas abiertas de la Parada 3, en orden de impacto**
1. ¿La forma del Pase es «Portal», con el QR dentro del arco del logo?
2. ¿Dos verdes: #00BB83 para la marca y #00D595 para el botón Crear Pase?
3. ¿El tema oscuro reajustado queda como canónico?
4. ¿Se aprueban en bloque las opciones A de logo, tipografía, iconografía, imagen, estructura y motion?
5. ¿Portería puede llamar al residente desde Kino cuando alguien llega con el Pase vencido? Es un dato, no una decisión.

## 3. Enlaces

| Qué | Enlace |
|---|---|
| Parada 1 (lámina) | https://claude.ai/artifact/EuPrHetctevY4PGiVAohiM |
| Parada 2 (lámina) | https://claude.ai/artifact/JZmNsBpL9zizPj29yxE8x9 |
| Parada 3 (lámina) | https://claude.ai/artifact/788FzxvYPNk3557owP4Mms |
| Vista previa del sitio v3 | https://claude.ai/artifact/NGW6EEiRghDxq4uFzvsjBa |
| Artefacto oficial del borrador | https://claude.ai/artifact/K8R2PRduS6SHBKYU31Bo6L (**no se toca hasta aprobar la Parada 4**) |
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
- Qué pasa en la entrada con un Pase vencido.
- El deck de diagnóstico del 4 sep y el Anexo de sustentación no están en la carpeta.
- Instrucciones del proyecto: todavía dicen «marca blanca» y «permiso». Solo el equipo puede editarlas; mandan `decisiones.md` y el encargo.

## 9. Siguiente trabajo, en orden

**1. Cerrar la Parada 3** con las respuestas de Nico y marcar X1 a X10 en `decisiones.md`.

**2. Fase 4, construir sin parar:**
- Llevar la paleta aprobada a `gorr-brand-system/clientes/kino`:
  - `marca.config.json` y `tokens/tema/*.tokens.json`: acción #00D595 y los 7 estados más el evento;
  - correr `npm run construir` en `branding/sistema` y `npm run contraste`.
  - Usa la skill `gorr-identidad-en-codigo` y regenera `kino-brand.css`.
- Escribir los departamentos 03 a 12 en el sitio, reemplazando los apartados «en construcción» de `secciones.py` con contenido de verdad.
- El sitio definitivo:
  - guardar copia fechada del borrador `Kino_Sistema_de_marca_2026-09-23.html`;
  - integrar el Motion Playground (`gorr-brand-system/vendor/motion/`).
- Figma:
  - sincronizar las variables con DTCG (hoy 51 contra 118 primitivos, 34 contra 37 semánticos, 12 contra 17 de movimiento, sin colección de tipografía);
  - llenar las 13 páginas vacías y construir los componentes con todos sus estados y las plantillas.

**3. Fase 5**
- Las 10 comprobaciones del encargo.
- Dos evaluaciones en subagentes: lector frío y detector de IA.
- Parada 4.
- Solo con aprobación, republicar K8R2PRduS6SHBKYU31Bo6L.

## 10. Estado de Figma

- **Páginas**: Léeme, Plataforma, Voz y UX writing, Logo, Color, Tipografía, Iconografía, Imagen, Estructura, Motion (specs), Componentes, Pantallas, Aplicaciones / Plantillas, Registro de cambios, Referencias.
- **Referencias**: guarda en secciones «Ref · …» todo el contenido anterior.
- **Construidas**: solo Léeme (nodo 22:94) y Plataforma (nodo 22:144).
- **Variables**: las 4 colecciones originales siguen intactas.
