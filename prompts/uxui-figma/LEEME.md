# Prompt UX/UI de Kino en Figma

Versión 1.2 · 28 sep 2026. La 1.1 depuró el prompt y remitió a las fuentes. La 1.2 corrige lo que encontró la revisión del 28 sep: una compuerta de voz y un script de auditoría que podían dar 0 errores sin revisar nada, dos contradicciones con `decisiones.md` (llamada de portería y verde de acción, ahora D-UX-01 y D-UX-02) y lo que había cambiado en la API. La 1.1 está en `_obsoleto/uxui-figma-1.1/`; la 1.0 no llegó al repositorio. Cuatro archivos:

- `prompt.md` · el prompt, listo para pegar.
- `evals.md` · criterios de éxito, 21 casos de prueba, rúbrica y prompt del juez, umbrales y qué ajustar.
- `auditoria-uxui.js` · script de solo lectura que el agente corre con `use_figma` en cada página de pantallas.
- `probar-auditoria.mjs` · prueba el script con un Figma simulado, sin conector: `node prompts/uxui-figma/probar-auditoria.mjs`. Se corre cada vez que cambia el script.

## 1. Decisión de arquitectura

**Un agente con herramientas, en una sola sesión, que avanza por siete fases con paradas humanas.** El trabajo necesita herramientas (el servidor MCP de Figma para leer la librería y construir, el repositorio para leer fuentes y correr la compuerta de voz) y el conocimiento vive en archivos que cambian (decisiones del 27 sep, tokens), así que el agente lee las fuentes en vez de recibirlas pegadas: es una recuperación dirigida sobre el repositorio, sin índice vectorial, porque las fuentes son pocas y tienen nombre.

Se descartó una cadena de prompts separados porque cada fase depende de lo que Nico decidió en la parada anterior y del estado del archivo de Figma; partir la sesión obligaría a reconstruir ese contexto cada vez. Se descartó un solo prompt sin fases porque el volumen (unas 65 pantallas más sus variantes) degrada la calidad y porque el proyecto exige que nada quede aprobado sin respuesta explícita. Las fases dan los cortes naturales: arquitectura, componentes, residente, demás superficies, prototipo, auditoría.

Decisiones tomadas con Nico para este prompt: todo el ecosistema (residente, visita, portería, administración); archivo nuevo «Kino · App» que consume la librería publicada `BO7UnDO9iE0aG6yUpNj0bc` sin tocarla; la app del residente es una PWA mobile-first.

## 2. Cómo se usa

1. Abre Claude Code en la raíz del repositorio `kino` (rama propia, por ejemplo `uxui/fase-1`), con el conector de Figma activo y la cuenta que ve la librería.
2. Confirma que la librería «Kino · Sistema de marca» está **publicada** en el equipo de Figma (en el archivo de la librería: panel Assets → Publish). Sin eso, el archivo nuevo no puede usar sus componentes y el agente se detiene en la Fase 0 (caso C18). El 28 sep no lo estaba: `search_design_system` no encontró «Botón de acción».
3. Pega el contenido de `prompt.md` como primer mensaje. El agente arranca con `<plan>` para la Fase 0.
4. En cada PARADA responde con aprobadas, cambios o la opción elegida (A/B). Las respuestas van a `decisiones.md`.
5. En la Fase 6 corre la rúbrica con el prompt del juez de `evals.md` y califica tú 4 de las 12 capturas para medir el acuerdo.

**Modelo:** el más capaz disponible en la sesión (familia Claude Opus; verifica el nombre vigente en https://docs.claude.com/en/docs/about-claude/models en vez de fijarlo aquí), con razonamiento extendido activado. El trabajo es de juicio de diseño y de muchas llamadas de herramienta encadenadas; un modelo rápido ahorra poco y equivoca más.

**Parámetros:** en los modelos actuales (Opus 4.7 en adelante, Opus 5 y 5.5, Sonnet 5) la API rechaza `temperature` con un error 400, y el razonamiento es adaptativo. Lo que se ajusta es el esfuerzo (`output_config.effort`): `high` o `xhigh` para el agente que diseña. `max_tokens` alto y con streaming, porque el informe de cada fase y las llamadas a `use_figma` son largos. El juez de `evals.md` corre aparte, con un modelo distinto del que diseñó (por ejemplo `claude-sonnet-5` si diseñó un Opus), para que nadie califique su propio trabajo. Su consistencia se mide con el acuerdo con Nico (`evals.md` §2), no con la temperatura.

**Prefill:** ni Claude Code ni la API aceptan que la respuesta empiece por un texto puesto de antemano: en los modelos actuales, un turno de asistente al final devuelve error 400. Por eso el prompt termina con «Empieza tu respuesta con `<plan>`».

## 3. Herramientas que usa el agente

No se definen herramientas nuevas: son las del servidor MCP de Figma y las del entorno. El prompt dice cuándo usar cada una.

| Herramienta | Para qué | Cuándo no |
|---|---|---|
| `whoami`, `get_libraries` | Comprobar cuenta y que la librería esté publicada | · |
| `search_design_system`, `get_variable_defs` | Encontrar componentes, variables y estilos antes de dibujar. Responde una consulta por llamada | Nunca se salta: dibujar algo que ya existe es un fallo |
| `create_new_file` | Crear «Kino · App» una sola vez | Para rehacer: lo reemplazado va a «99 · Descartes» |
| `use_figma` | Construir y auditar, una página por llamada, en serie | Nunca sobre `BO7UnDO9iE0aG6yUpNj0bc` |
| `get_screenshot` | Comparar cada pantalla con su ficha; capturas para el juez | · |
| `get_metadata` | Ubicar nodos y enlaces para los informes | · |
| `upload_assets` | Logo y símbolo en SVG desde `branding/sistema/marca/` si la librería no los trae | Fotos de personas, nunca |
| `generate_diagram` (FigJam) | Opcional para los flujos de la Fase 1 si se prefiere FigJam | Si ya están en la página 02 |
| Bash local | Leer fuentes, `npm run voz`, `npm run ciclo` | · |

Si una llamada falla o vuelve vacía: el agente lo dice en el informe, no reintenta en bucle (dos intentos como máximo) y no busca una vía alterna que rompa una regla.

## 4. Qué vigilar al correrlo

- **Volumen.** Son unas 65 pantallas más sus variantes. Si la sesión se vuelve lenta o el contexto se llena, cierra en una PARADA y abre una sesión nueva con `prompt.md` más una línea: «Retoma desde la Fase N; lee `avances.md` y `decisiones.md`». Por eso cada fase escribe en esos dos archivos.
- **Plataforma.** Nico eligió PWA, pero el repositorio tiene `paquetes/kino-motion-nativo/` (`PaseKino`, worklets), que sugiere una app nativa en algún momento. Si el equipo decide nativo, lo que cambia es la Fase 3 (navegación, hojas, zonas seguras); la arquitectura y los componentes se conservan.
- **Pendientes bloqueantes del MAESTRO.** Si Manuel confirma que HikCentral no acepta una credencial temporal sin crear una persona, el Pase sin cuenta cambia y con él V-L-01 y el paso de WhatsApp de R-P-02. El prompt lo deja marcado; no hace falta rehacer el resto.
- **Una verificación en 0 puede no haber mirado nada.** `voz.mjs` descarta en silencio una ruta que no existe y termina en 0 errores, y la auditoría devuelve `marcos: 0` si no encuentra pantallas con el nombre esperado. Revisa siempre que la voz diga «1 textos» y que `marcos` coincida con el inventario.
- **La compuerta de voz es un filtro, no un juez.** Atrapa 40 de 42 frases problemáticas. Un texto que pasa la compuerta todavía puede sonar genérico; eso lo mide la dimensión Voz de la rúbrica.
- **El script no ve todo.** No detecta un estado sin palabra dibujado a mano ni una jerarquía débil. Esos casos quedan para el juez y para Nico.
- **Coste.** El 80 % de las llamadas son `use_figma` y `get_screenshot`, más una llamada a `search_design_system` por cada componente que se busca. Pedir capturas solo de las pantallas P0 y de las que cambiaron baja el coste sin perder control.
