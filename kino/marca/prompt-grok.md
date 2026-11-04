# Prompt para traer a Kino el trabajo de marca hecho en Grok

Nico pega el bloque de abajo, completo, en la conversación de Grok donde trabajó la identidad. Grok lee las reglas del repositorio y entrega el trabajo listo para subir. Lo abre el issue [#15](https://github.com/Amonsalvem/kino/issues/15).

**Por qué así.** El repositorio es público, así que Grok puede leer las reglas desde `raw.githubusercontent.com`. Grok en grok.com no escribe en GitHub: entrega archivos y Nico los sube. Si se usa Grok Build con acceso al repositorio, Grok mismo abre la rama y el PR en borrador, nunca integra a `main` (`AGENTS.md` §1).

```text
Vas a trabajar como agente del repositorio de Kino: https://github.com/Amonsalvem/kino
En esta conversación trabajamos la identidad de marca nueva de Kino. Tu tarea es entregar ese trabajo en la forma que exige el repositorio, para que yo (Nico) o Alejandro lo subamos a GitHub.

PASO 1. LEE LAS REGLAS ANTES DE ESCRIBIR NADA
Abre estos archivos (el repositorio es público):
1. https://raw.githubusercontent.com/Amonsalvem/kino/main/AGENTS.md
2. https://raw.githubusercontent.com/Amonsalvem/kino/main/kino/canon/proyecto.md
3. https://raw.githubusercontent.com/Amonsalvem/kino/main/kino/canon/decisiones.md
4. https://raw.githubusercontent.com/Amonsalvem/kino/main/kino/marca/README.md
5. https://raw.githubusercontent.com/Amonsalvem/kino/main/CONVENCIONES.md
6. https://raw.githubusercontent.com/Amonsalvem/kino/main/.github/pull_request_template.md
7. https://raw.githubusercontent.com/Amonsalvem/kino/main/.claude/skills/corrector-muletillas/SKILL.md
8. https://raw.githubusercontent.com/Amonsalvem/kino/main/.claude/skills/registro-ia/SKILL.md
9. Para comparar con la marca anterior: https://raw.githubusercontent.com/Amonsalvem/kino/main/pre-kino/decisiones.md y https://raw.githubusercontent.com/Amonsalvem/kino/main/pre-kino/TRASPASO-SISTEMA-DE-MARCA.md

Si no puedes abrir alguno, dime cuál y espera a que te pegue su contenido. No supongas lo que dice.
Cuando los hayas leído, respóndeme en máximo 8 líneas: las reglas que aplican a este trabajo y el número de la siguiente decisión libre en decisiones.md. Luego sigue con el paso 2 sin esperar.

PASO 2. REGLAS QUE MANDAN EN ESTE TRABAJO
- Orden de autoridad: lo que diga Alejandro > decisiones APROBADAS de kino/canon/decisiones.md > kino/canon/proyecto.md > evidencia de pre-kino/inspeccion/ > el resto de pre-kino/.
- Alejandro aprueba todo. Nico y tú proponen. Nada de esta identidad está aprobado: cada decisión de marca entra como PROPUESTA.
- La fuente de la marca es Figma. En el repositorio solo va lo que se exporta (tokens, SVG, láminas) y los documentos que explican las decisiones.
- Toda decisión visual o verbal responde a un problema del diagnóstico. Cita el hallazgo o archivo de donde sale. Si no tiene fuente, escribe «sin fuente».
- Kino es la marca. Un conjunto (por ejemplo Monte Sereno) aparece solo como dato en texto, nunca con su logo ni sus colores.
- Vocabulario: «Pase» (de la visita o el colaborador) nunca se mezcla con «cuenta» (del residente). Nunca «permiso». «Visita», no «invitado».
- pre-kino/ es de solo lectura. Lo que se herede de la marca anterior se dice pieza por pieza, con la ruta del archivo de origen (lo pide D-002).
- Nada de secretos ni datos reales: llaves, contraseñas, cédulas, teléfonos, placas.
- Todo en español.

PASO 3. ESTILO (GitHub bloquea el PR si no se cumple)
- Prohibida la raya (el guion largo) como conector. Usa coma, dos puntos, paréntesis o punto.
- Prohibido: «cabe destacar», «vale la pena mencionar», «es importante señalar», «no dudes en», «espero que te sirva», «excelente pregunta», «tienes razón», «en resumen» o «en conclusión» al inicio de una línea, «tapiz», «piedra angular», «sin fisuras», «sinergia».
- Evita «no es X, es Y», «no solo... sino», «robusto», «crucial», «fundamental», «potenciar», «aprovechar».
- Conclusión primero. Tablas y listas antes que párrafos largos. Ningún párrafo de más de 120 palabras. Toda cifra lleva su fuente en la misma línea.
- Nombres de archivo: minúsculas, español, palabras con guion, sin tildes ni espacios. Documentos de un día empiezan con la fecha ISO (2026-11-04-...).

PASO 4. QUÉ ME ENTREGAS
Repasa todo lo que hicimos en esta conversación y entrégame, en este orden:

A. Inventario. Tabla con: pieza (logo, paleta, tipografía, voz, etc.), estado (explorada, elegida por Nico, descartada), carpeta de destino y problema del diagnóstico al que responde. Destinos posibles, según kino/marca/README.md:
   kino/marca/estrategia/  posicionamiento, promesa, personalidad
   kino/marca/verbal/      voz, tono, vocabulario, UX writing
   kino/marca/visual/      logo, color, tipografía, iconografía, imagen, motion
   kino/marca/tokens/      tokens en formato DTCG (JSON), como los exportaría Figma
   kino/marca/revision/    láminas de revisión, con fecha en el nombre
   Lo descartado no se sube: va solo en el inventario, con una línea de por qué.

B. Archivos. Uno por bloque de código, con su ruta completa como primera línea fuera del bloque, por ejemplo:
   Ruta: kino/marca/visual/color.md
   y el contenido completo dentro del bloque. Markdown para documentos, JSON DTCG para tokens, SVG como texto si tienes el vector. Si una pieza es una imagen que no puedes entregar como texto, lista su ruta y nombre de archivo para que yo la exporte y la suba.
   Incluye también el kino/marca/README.md actualizado: estado, carpetas creadas y la clave del archivo de Figma si te la di (si no, deja «por definir»).

C. Decisiones. Las entradas nuevas para kino/canon/decisiones.md, con el formato que usa ese archivo: identificador D-### consecutivo desde el siguiente libre, estado PROPUESTA, al menos dos alternativas en tabla con su costo, una recomendada y sus fuentes. Agrega además la lista de herencia para D-002: qué se tomó de pre-kino, pieza por pieza, con la ruta de origen, o «nada» si es el caso. No cambies el estado de D-002: eso lo hace Alejandro.

D. Pull request, listo para pegar:
   - Rama: marca/identidad-grok
   - Título: «Marca: identidad nueva trabajada en Grok»
   - Cuerpo con las secciones de la plantilla: «Qué cambia», «Cierra #15», «Por qué», «Decisiones», «Cómo se verificó» y «Uso de IA».
   - «Uso de IA» en la tabla de registro-ia: herramienta Grok (y el modelo, si lo sabes), pidió nico, prompts «resumen» (Nico todavía no aceptó el registro de prompts, así que no copies sus mensajes: solo una línea por pedido, en tus palabras), qué hizo la IA, qué hizo la persona, y una nota de práctica.

E. Lo que falta por verificar: datos sin fuente, piezas que dependen de Figma, preguntas para Alejandro (máximo cinco, ordenadas por impacto).

Antes de entregar, revisa todo tu texto contra el paso 3 y corrige lo que no cumpla.

PASO 5. CÓMO SE SUBE (explícamelo al final, en pasos cortos)
Si no tienes acceso de escritura al repositorio, dame los pasos para subirlo desde github.com: crear la rama marca/identidad-grok, «Add file» > «Create new file» o «Upload files» en cada carpeta, y abrir el PR en borrador con el cuerpo del punto D. Si GitHub no me deja crear la rama, le paso los archivos a Alejandro.
Si sí tienes acceso de escritura (Grok Build u otra integración con GitHub), crea tú la rama y el PR en borrador. Nunca escribas en main ni integres el PR: eso lo hace Alejandro.
```

## Después de pegarlo

- Revisa el inventario (punto A) antes de subir: si Grok olvidó algo de la conversación, pídeselo antes de crear el PR.
- El PR corre el chequeo de texto de GitHub. Si falla, el error dice la línea; corrígela en GitHub y vuelve a guardar.
