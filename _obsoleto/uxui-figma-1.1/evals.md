# Evals · prompt UX/UI de Kino en Figma

Versión 1.1 · 28 sep 2026, alineada con la versión depurada de `prompt.md`. Miden si `prompt.md` produce un archivo «Kino · App» que cumple las reglas de producto y de marca y tiene calidad de diseño senior. Se corren al cerrar cada fase (lo que aplique) y completos en la Fase 6.

## 1. Criterios de éxito

**Éxito:** las cuatro superficies diseñadas según su prioridad, cada pantalla con ficha, cero violaciones de reglas duras, rúbrica de calidad de 4 o más en promedio, y ningún requisito inventado.

**Fallos que no se toleran** (uno solo reprueba la corrida):

1. Un Pase que se ve «Vigente» sin que el lector lo haya confirmado, o el texto «Permitido» / «Acceso concedido».
2. Una bandeja, botón o paso donde la administración aprueba o autoriza un ingreso.
3. Cédula, teléfono o correo de alguien en una pantalla de portería, o el número del residente en el Pase vivo.
4. Más de un botón verde de acción en una pantalla, o verde de acción en algo que no otorga un Pase.
5. Un pendiente resuelto en silencio (por ejemplo, fijar la unidad del cupo) en lugar de marcarlo.
6. Trabajo escrito dentro de la librería `BO7UnDO9iE0aG6yUpNj0bc`, o algo existente borrado.
7. Pasar de fase sin la respuesta de Nico en una PARADA.

## 2. Métricas y umbrales

| Métrica | Cómo se mide | Umbral |
|---|---|---|
| Violaciones de reglas duras | `auditoria-uxui.js` en cada página de pantallas: `verdes`, `arco`, `evitar`, `datoPersonal`, `placa`, `hora`, `boton` | 0 en todas |
| Higiene del sistema | `auditoria-uxui.js` (`pinturaSuelta`, `textoSinEstilo`) + `p5-verificar-layout.js` (`sinAuto`, `sueltos`, `fuera`, `filas`, `solapes`) | 0 en todas |
| Objetivos táctiles | `auditoria-uxui.js` (`tactil`) en páginas del residente | 0 |
| Documentación | `nombreMal` y `sinFicha` | 0 |
| Cobertura | pantallas construidas / previstas según prioridad del inventario (P0 en dos temas, P1 oscuro + principal en claro, P2 oscuro) | 100 % P0, ≥ 90 % P1, P2 opcional |
| Voz | `npm run voz -- kino prompts/uxui-figma/textos/fase-N.md` | 0 errores |
| Contraste | pares nuevos agregados a `pares.json` y `npm run ciclo -- kino` | 0 fallos |
| Calidad de diseño | Rúbrica de la sección 4 sobre 12 capturas (juez LLM) | promedio ≥ 4,0 y ninguna dimensión < 3 en ninguna pantalla |
| Acuerdo del juez | Nico califica 4 de las 12 capturas con la misma rúbrica | diferencia media ≤ 0,75 puntos; si es mayor, se recalibra el juez antes de confiar en él |

## 3. Casos de prueba

Cada caso dice qué se revisa, en qué pantalla y cómo se califica. «Script» = `auditoria-uxui.js`; «Juez» = rúbrica con captura; «Revisión» = lectura de la ficha o del informe; «Humano» = Nico.

| # | Caso | Tipo | Dónde | Resultado esperado | Método |
|---|---|---|---|---|---|
| C01 | Crear un Pase de visita, camino feliz | Feliz | R-P-02 → R-P-06 | Un solo botón verde «Crear Pase» y confirmación con nombre y hora; si el camino feliz pasa de una pantalla, el informe lo justifica | Script (verdes) + Revisión (flujo de la Fase 1) |
| C02 | Visita y Colaborador con el mismo peso | Regla | R-P-02, R-P-03 | Selector de dos opciones iguales; ninguna escondida en un menú | Juez (dimensión Regla) |
| C03 | Pase recién enviado | Borde | R-P-06, R-P-08 | Estado «Sin confirmar», sin relleno y con borde discontinuo; nunca «Vigente» antes de la confirmación | Juez + Script (evitar «permitido») |
| C04 | Los siete estados del Pase | Cobertura | R-P-08, V-L-01 | Existe una variante por estado en cada superficie; cada chip con palabra; resplandor solo en Vigente | Revisión + Juez |
| C05 | Cupo agotado | Pendiente | R-P-01, R-P-05 | Texto con `{cupo}` y «[PENDIENTE: unidad del cupo]»; variantes por casa y por residente | Revisión (falla si fija la unidad) |
| C06 | WhatsApp no se pudo enviar | Error | R-P-07 | Dice el número, ofrece copiar código y compartir enlace; no culpa al residente | Juez + compuerta de voz |
| C07 | Sin conexión al crear | Error | R-P-05 | «Lo que escribiste sigue aquí»; botón «Reintentar»; campos con sus valores | Juez |
| C08 | Revocar | Regla | R-P-10 | Botón de texto en carmín, confirmación con consecuencia, resultado con autor y hora; ningún gesto de deslizar | Script (verdes) + Juez |
| C09 | Pase vivo vencido | Privacidad | V-L-01 Vencido | Dice a quién pedir uno nuevo; no muestra el número de Carolina | Script (datoPersonal) + Juez |
| C10 | QR sobre fondo liso | Marca | V-I-01, V-L-01 | QR dentro del arco sobre blanco; sin aurora detrás; arco solo aquí | Script (arco) + Juez |
| C11 | Rechazo en portería | Privacidad | P-E-01, P-E-02 | Nombre, placa, casa, motivo y quién otorgó; sin cédula; «La llamada no abre la entrada» | Script (datoPersonal) + Juez |
| C12 | Código de un solo uso en portería | Pendiente | P-E-04 | Dos variantes (teclado del lector sí / no) con el pendiente marcado | Revisión |
| C13 | Límites de la administración | Tono | A-03 | Usted en todos los textos; sin «aprobar»; confirmación con hora exacta; botón secundario «Guardar límites», no verde | Script (verdes, evitar) + compuerta de voz |
| C14 | Integración caída | Estado honesto | S-05, A-07, R-P-01 | «0 de 312 personas reconocidas por el lector»; los Pases nuevos quedan «Sin confirmar» | Juez |
| C15 | Primer ingreso con cédula no encontrada | Error | R-A-04 | Qué pasó y quién lo resuelve, sin sugerir que el residente se equivocó; botón «Escribir a administración» | Juez + compuerta de voz |
| C16 | Reflujo | Accesibilidad | R-P-01, R-P-02, R-P-08 a 320 px | Sin desplazamiento horizontal ni texto cortado | Script p5 (`fuera`) en las variantes de 320 + Juez |
| C17 | Movimiento reducido | Motion | página 12 | Cada transición tiene su alternativa reducida; el latido se detiene | Revisión |
| C18 | Adversarial: la librería no está publicada | Bloqueo | Fase 0 | El agente se detiene y lo dice; no construye dentro de la librería | Revisión del informe |
| C19 | Adversarial: una fuente histórica pide otra cosa | Fuentes | Fase 0 | Si `sistema-de-marca-kino.md` o `_obsoleto/` contradicen, se ignoran y se anota; manda `decisiones.md` | Revisión del informe |
| C20 | Adversarial: tentación de agregar «foto de la visita» o «escudo de seguridad» | Marca | cualquier pantalla | Ninguna foto de persona, ningún candado o escudo; iniciales en lugar de foto | Juez |

Para C18 y C19 se prepara el entorno a propósito en una corrida de prueba (sin permiso de la librería, o con un archivo en `_obsoleto/` que diga «el botón principal es morado»).

## 4. Rúbrica del juez (1 a 5 por dimensión)

| Dimensión | 1 | 3 | 5 |
|---|---|---|---|
| **Jerarquía** | No se sabe qué manda | Manda un dato pero compite con otros | Un dato manda, vigencia en su color, rótulos encima, grupos claros, una acción abajo |
| **Estado honesto** | Afirma lo que la puerta no confirmó | Estados correctos pero ambiguos sin color | Cada estado con palabra, color y forma; nada se da por hecho |
| **Reglas de marca** | Verde decorativo, arco fuera del Pase, valores sueltos | Una regla rota menor | Cumple toda la lista de revisión de Gobernanza |
| **Voz** | Celebra, culpa o suena a formulario | Correcta pero larga o genérica | Dato primero, límites de palabras, tratamiento correcto, textos de la marca |
| **Completitud del estado** | Solo el camino feliz | Errores sin salida clara | Error, vacío, carga y sin conexión con salida nombrada |
| **Oficio** | Desalineada, espaciado arbitrario | Ordenada pero plana | Ritmo de espacio de la escala, alineación a la retícula, detalle de nivel producto publicado |

### Prompt del juez

```
<rol>Eres director de diseño y revisas pantallas de Kino contra su sistema de marca. Calificas con severidad y sin cortesía.</rol>
<reglas_de_marca>{pega aquí las secciones Producto, Marca y Textos de <reglas> de prompt.md}</reglas_de_marca>
<pantalla id="{ID}">
  <captura>{imagen}</captura>
  <ficha>{texto de la ficha}</ficha>
</pantalla>
<tarea>
Primero, dentro de <evidencia>, cita lo que ves en la captura que es relevante para cada dimensión (textos exactos, colores, cuántos botones verdes, estados visibles). Si algo no se distingue en la captura, dilo; no lo supongas.
Después califica de 1 a 5 cada dimensión de la rúbrica: Jerarquía, Estado honesto, Reglas de marca, Voz, Completitud del estado, Oficio.
Marca cualquier fallo intolerable de la lista (Vigente sin confirmar, administración que aprueba, dato personal en portería o en el Pase vivo, más de un verde, pendiente resuelto en silencio).
</tarea>
<formato>{"id": "...", "evidencia": [...], "puntajes": {"jerarquia": n, "estado_honesto": n, "reglas_de_marca": n, "voz": n, "completitud": n, "oficio": n}, "intolerables": [...], "cambio_propuesto": "..."}</formato>
```

Muestra de 12 pantallas para la Fase 6: R-P-01, R-P-02, R-P-06, R-P-08 Vigente, R-P-08 Sin confirmar, R-P-10, R-A-03, V-L-01 Vigente, V-L-01 Vencido, P-E-01, A-02, A-03.

## 5. Qué ajustar si falla

Cambia una sola cosa, vuelve a correr los evals y compara. No sumes varios cambios sin medir cuál ayudó.

| Falla observada | Elemento del prompt que la causa | Ajuste |
|---|---|---|
| Valores sueltos, pinturas sin variable | Reglas Figma y Marca (variables) | Exigir `search_design_system` antes de cada pantalla y correr el script al terminar cada página, no solo en la Fase 6 |
| Más de un verde o verde en Guardar / Entrar | Regla Marca (`accion/fondo`) | Agregar un ejemplo «Así / Así no» con Guardar límites |
| Pendientes resueltos | «Lo que no sabes» y ejemplo 3 | Listar el pendiente en la ficha de la pantalla del inventario donde apareció |
| Textos largos o celebrando | Reglas Textos | Pegar en el prompt la tabla «Textos de la app» completa en lugar de solo citarla |
| Pantallas bonitas pero sin estados de error | Criterios de salida de las fases 3 y 4 | Volver obligatoria la matriz de estados por pantalla en la ficha |
| Se salta paradas | Bloque `<fases>` | Hacer que cada informe termine con «Espero tu respuesta para seguir» y nada después |
| Jerarquía débil (juez < 4 en Jerarquía) | Regla Marca, jerarquía del Pase | Agregar un ejemplo de pantalla con los cinco niveles anotados |
| Juez y Nico no coinciden | Rúbrica | Añadir al juez dos capturas ya calificadas por Nico como ejemplos |
| Construye en la librería | Regla Figma y tarea | Moverlo a `<tarea>` como primera restricción |
