# Prompt para traer a Kino el trabajo hecho en Grok

Nico pega el bloque de abajo, completo, en **cada** conversación de Grok donde trabajó algo de Kino (marca, producto, investigación, entregas, código u otro tema). Grok hace el inventario de lo que hay en esa conversación, lo reparte en las carpetas del repositorio y entrega un PR por área. Lo abre el issue [#15](https://github.com/Amonsalvem/kino/issues/15).

**Por qué así.** El repositorio es público, así que Grok lee las reglas desde `raw.githubusercontent.com`. Grok en grok.com no escribe en GitHub: entrega archivos y Nico los sube. Si se usa Grok Build con acceso al repositorio, Grok mismo abre las ramas y los PR en borrador, nunca integra a `main` (`AGENTS.md` §1). Grok no ve otras conversaciones, por eso el prompt va en cada una.

```text
Vas a trabajar como agente del repositorio de Kino: https://github.com/Amonsalvem/kino
En esta conversación trabajé (Nico) cosas de Kino. Tu tarea es encontrar todo lo que hicimos aquí, sea del tema que sea, y entregarlo en la forma que exige el repositorio para que yo o Alejandro lo subamos a GitHub.

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

PASO 4. QUÉ ME ENTREGAS
Repasa toda esta conversación, de principio a fin, y entrégame en este orden:

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

B. Archivos. Uno por bloque de código, con su ruta completa en la línea anterior al bloque, por ejemplo:
   Ruta: kino/producto/flujos/pase-visita.md
   y el contenido completo dentro del bloque. Markdown para documentos, JSON para tokens, SVG como texto si tienes el vector, TypeScript para código. Si una pieza es una imagen o un archivo que no puedes entregar como texto, lista la ruta y el nombre para que yo lo exporte y lo suba.
   Si creas una subcarpeta prevista en el README de su carpeta, entrega también ese README.md actualizado.

C. Decisiones. Las entradas nuevas para kino/canon/decisiones.md, con el formato de ese archivo: D-### consecutivo desde el siguiente libre, estado PROPUESTA, al menos dos alternativas en tabla con su costo, una recomendada y sus fuentes. Si hubo trabajo de marca, agrega la lista de herencia para D-002: qué se tomó de pre-kino, pieza por pieza, con la ruta de origen, o «nada». No cambies el estado de ninguna decisión: eso lo hace Alejandro.

D. Un pull request por área (regla «una rama y un PR por tarea»), cada uno listo para pegar:
   - Rama: area/tema, por ejemplo marca/identidad-grok o producto/flujo-pase-visita
   - Título que empiece con el área: «Marca: ...», «Producto: ...»
   - Cuerpo con las secciones de la plantilla: «Qué cambia», «Por qué», «Decisiones», «Cómo se verificó» y «Uso de IA». En «Qué cambia» escribe «Parte de #15» y, en el último PR que te pida, «Cierra #15».
   - «Uso de IA» con la tabla de registro-ia: herramienta Grok (y el modelo, si lo sabes), pidió nico, prompts «resumen» (Nico todavía no aceptó el registro de prompts: no copies sus mensajes, solo una línea por pedido en tus palabras), qué hizo la IA, qué hizo la persona, y una nota de práctica.
   - Las entradas de decisiones.md van en el PR del área a la que pertenecen.

E. Lo que falta por verificar: datos sin fuente, contradicciones con el canon, piezas que dependen de Figma u otra herramienta, y preguntas para Alejandro (máximo cinco, ordenadas por impacto).

Antes de entregar, revisa todo tu texto contra el paso 3 y corrige lo que no cumpla.

PASO 5. CÓMO SE SUBE (explícamelo al final, en pasos cortos)
Si no tienes acceso de escritura al repositorio, dame los pasos para subir cada PR desde github.com: crear la rama, «Add file» > «Create new file» o «Upload files» en cada carpeta, y abrir el PR en borrador con su cuerpo del punto D. Si GitHub no me deja crear ramas, le paso los archivos a Alejandro.
Si sí tienes acceso de escritura (Grok Build u otra integración con GitHub), crea tú las ramas y los PR en borrador. Nunca escribas en main ni integres un PR: eso lo hace Alejandro.
```

## Después de pegarlo

- Revisa el inventario (punto A) antes de subir: si Grok olvidó algo de la conversación, pídeselo antes de crear los PR.
- Si trabajaste en varias conversaciones, repite el prompt en cada una y sube sus PR por separado.
- Cada PR corre el chequeo de texto de GitHub. Si falla, el error dice la línea; corrígela en GitHub y vuelve a guardar.
