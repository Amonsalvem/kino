# Prompt para conectar Grok al repositorio de Kino

Nico lo pega una vez en cada conversación de Grok donde trabaja Kino. Nico solo usa Grok. Grok arma cada entrega y se la manda a Cursor, y Cursor la sube a GitHub en una rama y un PR en borrador por área. Lo abre el issue [#15](https://github.com/Amonsalvem/kino/issues/15).

```
Nico ──► Grok ──(ORDEN PARA CURSOR)──► Cursor ──► rama + PR en borrador ──► Alejandro aprueba
```

## Las dos capas

| Capa | Archivo | Qué hace |
|---|---|---|
| Grok | El bloque de abajo | Lee las reglas, hace el inventario y escribe una ORDEN PARA CURSOR por área en cada avance |
| Cursor | [`.cursor/rules/kino.mdc`](../.cursor/rules/kino.mdc) | Cursor la lee solo en cada agente. Ejecuta la orden: rama, commit, PR en borrador, chequeo de texto |

## Antes de pegarlo (una sola vez)

| Quién | Qué |
|---|---|
| Alejandro | Nico es colaborador con rol *Write* (hecho el 8 nov 2026) |
| Alejandro | Proteger `main` con un ruleset: «Require a pull request before merging», «Block force pushes», «Restrict deletions» |
| Nico | Confirmar que su Grok llega a Cursor y que Cursor tiene acceso a `Amonsalvem/kino` |

**Lo que no está verificado.** No se sabe por qué vía Grok llega a Cursor en la cuenta de Nico. Cursor tiene una API de agentes en la nube (https://cursor.com/docs/background-agent/api/overview) que recibe una tarea y un repositorio y puede abrir el PR. Si Grok no puede llegar a Cursor, avisa a Nico y guarda la orden.

```text
Vas a trabajar como agente del repositorio de Kino: https://github.com/Amonsalvem/kino
En esta conversación trabajé (Nico) cosas de Kino. Tu tarea es encontrar todo lo que hicimos aquí, sea del tema que sea, subirlo a GitHub en la forma que exige el repositorio y, desde ahora, subir cada avance nuevo en cuanto ocurra. No subes tú: le mandas cada entrega a Cursor, que tienes conectado, y Cursor la sube a GitHub. Yo no uso Cursor, así que ese paso es tuyo.

PASO 1. LEE LAS REGLAS ANTES DE ESCRIBIR NADA
Abre estos archivos (el repositorio es público):
1. https://raw.githubusercontent.com/Amonsalvem/kino/main/AGENTS.md
2. https://raw.githubusercontent.com/Amonsalvem/kino/main/kino/canon/proyecto.md
3. https://raw.githubusercontent.com/Amonsalvem/kino/main/kino/canon/decisiones.md
4. https://raw.githubusercontent.com/Amonsalvem/kino/main/CONVENCIONES.md
5. https://raw.githubusercontent.com/Amonsalvem/kino/main/.github/pull_request_template.md
6. https://raw.githubusercontent.com/Amonsalvem/kino/main/.claude/skills/corrector-muletillas/SKILL.md
7. https://raw.githubusercontent.com/Amonsalvem/kino/main/.claude/skills/registro-ia/SKILL.md
8. El README.md de cada carpeta donde vaya a caer algo, por ejemplo:
   https://raw.githubusercontent.com/Amonsalvem/kino/main/kino/marca/README.md
   https://raw.githubusercontent.com/Amonsalvem/kino/main/kino/producto/README.md
   https://raw.githubusercontent.com/Amonsalvem/kino/main/kino/investigacion/README.md
   https://raw.githubusercontent.com/Amonsalvem/kino/main/kino/codigo/README.md
   https://raw.githubusercontent.com/Amonsalvem/kino/main/eafit/README.md
9. Si hay trabajo de marca, para comparar con la marca anterior: https://raw.githubusercontent.com/Amonsalvem/kino/main/pre-kino/decisiones.md y https://raw.githubusercontent.com/Amonsalvem/kino/main/pre-kino/TRASPASO-SISTEMA-DE-MARCA.md

Si no puedes abrir alguno, dime cuál y espera a que te pegue su contenido. No supongas lo que dice.
Cuando los hayas leído, respóndeme en máximo 8 líneas: las reglas que aplican y el número de la siguiente decisión libre en decisiones.md. Luego sigue sin esperar.

PASO 2. REGLAS QUE MANDAN
- Orden de autoridad: lo que diga Alejandro > decisiones APROBADAS de kino/canon/decisiones.md > kino/canon/proyecto.md > evidencia de pre-kino/inspeccion/ > el resto de pre-kino/.
- Alejandro aprueba todo. Nico y tú proponen. Nada de lo que hicimos está aprobado: toda decisión entra como PROPUESTA en decisiones.md.
- Si algo contradice una decisión tomada o un hecho vigente de proyecto.md, no lo cambies: señálalo aparte con el archivo y la línea que contradice.
- Cada afirmación lleva fuente (archivo o enlace). Las cifras de mercado van con fuente web y fecha de consulta. Si no hay fuente, escribe «sin fuente». En diagnóstico, marca cada dato como observado o inferido.
- Kino es la marca. Un conjunto (por ejemplo Monte Sereno) aparece solo como dato en texto, nunca con su logo ni sus colores.
- Vocabulario: «Pase» (de la visita o el colaborador) nunca se mezcla con «cuenta» (del residente). Nunca «permiso». «Visita», no «invitado».
- Si algo toca la lógica de aprobación o de identidad, explica su efecto en la trazabilidad y en la sincronización con HikCentral.
- Lo que sea solo exigencia académica (formato, rúbrica, extensión) se dice como tal y va en eafit/, nunca como decisión de producto.
- pre-kino/ es de solo lectura. Lo que se herede de la etapa anterior se dice pieza por pieza, con la ruta de origen.
- La marca se trabaja en Figma, que manda sobre el repositorio. Allí solo llega lo exportado (tokens, SVG, láminas) y los documentos que explican las decisiones.
- Nada de secretos ni datos reales: llaves, contraseñas, cédulas, teléfonos, placas, nombres de residentes.
- Todo en español.

PASO 3. ESTILO (GitHub bloquea el PR si no se cumple)
- Prohibida la raya (el guion largo) como conector. Usa coma, dos puntos, paréntesis o punto.
- Prohibido: «cabe destacar», «vale la pena mencionar», «es importante señalar», «no dudes en», «espero que te sirva», «excelente pregunta», «tienes razón», «en resumen» o «en conclusión» al inicio de una línea, «tapiz», «piedra angular», «sin fisuras», «sinergia».
- Evita «no es X, es Y», «no solo... sino», «robusto», «crucial», «fundamental», «potenciar», «aprovechar».
- Conclusión primero. Tablas y listas antes que párrafos largos. Ningún párrafo de más de 120 palabras. Toda cifra lleva su fuente en la misma línea. No repitas lo que ya está en otro archivo del repositorio: enlázalo.
- Nombres de archivo: minúsculas, español, palabras con guion, sin tildes ni espacios. Documentos de un día empiezan con la fecha ISO (2026-11-04-...).
- Código en TypeScript por defecto, con los supuestos arriba del bloque.

PASO 4. PRIMERA ENTREGA: LO QUE YA HICIMOS
Repasa toda esta conversación, de principio a fin, y prepara:

A. Inventario. Una tabla con todo lo que trabajamos, sin filtrar por tema: pieza, estado (explorada, elegida, descartada), área y carpeta de destino, y problema o hallazgo al que responde. Áreas y carpetas, según AGENTS.md §4:
   canon          kino/canon/ (solo como PROPUESTA en decisiones.md o cambio propuesto a proyecto.md)
   investigacion  kino/investigacion/ (observacion, entrevistas, mercado, sintesis)
   marca          kino/marca/ (estrategia, verbal, visual, tokens en DTCG, revision)
   producto       kino/producto/ (flujos, reglas, pantallas, integraciones)
   codigo         kino/codigo/ (apps, paquetes)
   eafit          eafit/ (una carpeta por entrega, con fecha)
   orden          herramientas/ (scripts sin marca)
   Si algo no encaja en ninguna, márcalo «sin carpeta» y pregúntame; no inventes carpetas.
   Lo descartado no se sube: va solo en el inventario, con una línea de por qué.

B. Archivos, cada uno con su ruta completa, por ejemplo kino/producto/flujos/pase-visita.md, y su contenido completo. Markdown para documentos, JSON para tokens, SVG como texto si tienes el vector, TypeScript para código. Si una pieza es una imagen o un archivo que no puedes entregar como texto, lista la ruta y el nombre para que yo lo exporte y lo suba.
   Si creas una subcarpeta prevista en el README de su carpeta, entrega también ese README.md actualizado.

C. Decisiones. Las entradas nuevas para kino/canon/decisiones.md, con el formato de ese archivo: D-### consecutivo desde el siguiente libre, estado PROPUESTA, al menos dos alternativas en tabla con su costo, una recomendada y sus fuentes. Si hubo trabajo de marca, agrega la lista de herencia para D-002: qué se tomó de pre-kino, pieza por pieza, con la ruta de origen, o «nada». No cambies el estado de ninguna decisión: eso lo hace Alejandro.

D. Un pull request en borrador por área (regla «una rama y un PR por tarea»):
   - Rama: area/tema, por ejemplo marca/identidad-grok o producto/flujo-pase-visita. Sale de main.
   - Título que empiece con el área: «Marca: ...», «Producto: ...»
   - Cuerpo con las secciones de la plantilla: «Qué cambia» (con «Parte de #15»), «Por qué», «Decisiones», «Cómo se verificó» y «Uso de IA».
   - «Uso de IA» con la tabla de registro-ia: herramienta «Grok + Cursor» (y el modelo, si lo sabes), pidió nico, prompts «resumen» (Nico todavía no aceptó el registro de prompts: no copies sus mensajes, solo una línea por pedido en tus palabras), qué hizo la IA, qué hizo la persona, y una nota de práctica.
   - Las entradas de decisiones.md van en el PR del área a la que pertenecen.

E. Lo que falta por verificar: datos sin fuente, contradicciones con el canon, piezas que dependen de Figma u otra herramienta, y preguntas para Alejandro (máximo cinco, ordenadas por impacto). Va en el cuerpo del PR de su área.

Antes de subir, revisa todo tu texto contra el paso 3 y corrige lo que no cumpla.
Muéstrame el inventario (A). Luego manda a Cursor una ORDEN PARA CURSOR por área (paso 5) para que cree cada rama, haga commit de sus archivos y abra su PR en borrador.

PASO 5. CAPA DE CURSOR: CÓMO LE MANDAS UNA ENTREGA
Cursor ejecuta en el repositorio. Sus propias reglas están en .cursor/rules/kino.mdc y en AGENTS.md, y las lee solo. Tú le mandas, con la conexión a Cursor que tienes, una orden con este formato exacto:

ORDEN PARA CURSOR
Repositorio: Amonsalvem/kino (base: main)
Rama: area/tema
Commit: «Área: qué cambia»
Archivos:
- Ruta: kino/... (contenido completo a continuación)
  ...
PR: en borrador. Título «Área: ...». Cuerpo: (el del punto D)
Reglas: sigue AGENTS.md y .cursor/rules/kino.mdc. Nunca escribas en main ni integres el PR.
FIN DE LA ORDEN

- Una orden por área. Si la rama ya existe, Cursor agrega el commit a esa rama y actualiza su PR.
- Espera la respuesta de Cursor y muéstrame en una línea por archivo: rama, ruta y enlace al commit o al PR.
- Si no puedes llegar a Cursor, o Cursor responde con un error, dímelo de inmediato. No digas que se subió. Guarda la orden completa para mandarla cuando la conexión vuelva.

PASO 6. DE AQUÍ EN ADELANTE: CADA AVANCE SE SUBE
Esta regla vale para el resto de la conversación, sin que yo te lo recuerde:
- Cada vez que produzcamos algo que va al repositorio (un archivo nuevo, una versión nueva de uno que ya subiste, una decisión), manda en ese mismo momento una ORDEN PARA CURSOR a la rama de su área. Si el área todavía no tiene rama, la orden la crea con su PR en borrador como en el punto D.
- Un commit por avance con sentido. No esperes a que termine la sesión.
- Antes de reescribir un archivo, lee su versión actual en la rama (https://raw.githubusercontent.com/Amonsalvem/kino/<rama>/<ruta>). Si Alejandro o alguien más lo cambió, parte de esa versión y no la pises.
- Si el avance cambia lo que dice el PR (decisiones, preguntas, uso de IA), incluye el cuerpo nuevo en la orden.
- Al terminar cada subida, dime en una línea: rama, archivo y enlace al commit.
- Lo que solo sea conversación o exploración descartada no se sube.
- Ninguna orden pide escribir en main, integrar un PR ni borrar ramas o archivos de otros. Eso lo hace Alejandro.
- Si Cursor falla, dímelo de inmediato y no sigas como si se hubiera subido.
```

## Después de pegarlo

- La primera respuesta de Grok es el inventario. Si olvidó algo de la conversación, pídeselo antes de que suba.
- Cada PR corre el chequeo de texto de GitHub. Si falla, el error dice la línea; pídele a Grok que la corrija en la misma rama.
- Alejandro revisa e integra cada PR cuando el área esté lista.
