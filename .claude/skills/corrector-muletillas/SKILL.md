---
name: corrector-muletillas
description: Revisa y corrige el texto antes de subirlo al repositorio de Kino. Quita las muletillas de IA que de verdad aparecen en este repositorio, los datos sin fuente, las generalidades y la información de más. Úsala antes de cada commit con texto, al escribir un PR o un issue, o cuando pidan «quita las muletillas», «que no suene a IA» o «revisa este texto».
---

# Corrector de muletillas

Revisas texto en español antes de que entre al repositorio. El objetivo es que cada frase diga algo verificable y nada sobre. Gasta tokens solo donde haya un problema: no reescribas lo que ya está bien.

## Paso 1. Corre el chequeo

```bash
python3 herramientas/revisar-texto.py <archivos>          # archivos
python3 herramientas/revisar-texto.py --texto cuerpo.md   # cuerpo de un PR o issue
```

Es el mismo chequeo que corre GitHub en cada PR. Los ERROR bloquean la integración; los AVISO no.

## Paso 2. Corrige solo las líneas marcadas

- **ERROR**: corrígelo siempre. Edita la línea; no reescribas el párrafo.
- **AVISO**: decide. Si la palabra o la antítesis es la más precisa (por ejemplo, «clave» como contraseña, «estado honesto» como concepto de marca), déjala.
- Una cita textual de otra persona va en una línea con `>`. Si un patrón es legítimo y no es cita, agrega `<!-- muletillas: ok -->` al final de la línea y di por qué en el PR.

## Paso 3. Revisa lo que el script no ve

Lee el texto una vez buscando solo estas tres cosas:

| Problema | Señal | Corrección |
|---|---|---|
| Dato sin respaldo | Una afirmación sobre Kino, el mercado o un usuario sin archivo ni enlace | Cita la ruta o el enlace. Si no existe, escribe «sin fuente» o quítala |
| Generalidad | La frase serviría igual para cualquier producto («mejora la experiencia», «solución integral») | Cámbiala por el dato concreto de Kino o bórrala |
| Información de más | Repite lo que ya está en otro archivo, o explica algo que nadie pidió | Enlaza el archivo y borra la repetición |

## Lo que no hace falta revisar

Las listas largas de palabras de IA en inglés y los tics que no aparecen en este repositorio. La medición del 4 nov 2026 sobre 115 documentos mostró que «tapiz», «piedra angular» o «panorama» salen una vez o ninguna. Las muletillas reales fueron la raya (166 veces), «no solo… sino» y la antítesis «no es X, es Y».

Si cambia el estilo de lo que se escribe, la lista se actualiza midiendo de nuevo. La investigación de fondo está en `references/muletillas-investigacion.md`; ábrela solo si necesitas justificar un caso dudoso.
