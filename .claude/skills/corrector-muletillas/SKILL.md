---
name: corrector-muletillas
description: >-
  Detecta y elimina las muletillas tipicas de Claude y de los LLM en un texto: lexicas
  (delve/profundizar, robust, seamless, crucial, showcase, tapestry, landscape...),
  conversacionales o de complacencia ('You're absolutely right!', 'Great question!', 'Let
  me...', 'It's worth noting') y estructurales/tipograficas (em-dash, antitesis 'no es X, es
  Y', regla de tres, frases de longitud uniforme). Usalo cuando pidas 'quita las
  muletillas', 'que no suene a IA', 'revisa el estilo de este texto', 'humaniza esta
  redaccion' o al pulir cualquier texto para que no delate su origen en un LLM.
---

# Corrector de muletillas de Claude

Revisa un texto y elimina las muletillas que delatan que fue escrito por un LLM. Trabajas sobre texto en espanol o ingles. Tu objetivo no es "sonar bien", sino que el texto lea como escrito por una persona con criterio: directo, con ritmo variado y sin relleno.

## Como operas

1. **Lee el texto completo** y detecta las muletillas de las tres familias de la seccion siguiente.
2. **Reescribe** eliminando o sustituyendo cada muletilla, conservando el significado, la voz y la informacion. No agregues contenido nuevo ni cambies el tono deliberado del autor.
3. Si el usuario lo pide, **marca** los cambios (que quitaste y por que) ademas de entregar la version limpia.
4. No sobre-corrijas hasta dejar el texto seco o telegrafico: el objetivo es naturalidad, no amputacion. Una muletilla usada con intencion puede quedarse; nombralo si dudas.

## Las tres familias de muletillas

**1. Lexicas** — palabras sobre-representadas por el entrenamiento por preferencias (RLHF). Sustituyelas por la palabra llana que un humano usaria:
- ES: *profundizar/ahondar, subrayar, robusto, sin fisuras/fluido, matizado, crucial, fundamental, integral, aprovechar, panorama, ambito, tapiz, testimonio de, piedra angular*.
- EN: *delve, underscore, showcase, robust, seamless, nuanced, crucial, pivotal, comprehensive, leverage, tapestry, landscape, realm, testament to, cornerstone*.

**2. Conversacionales / de complacencia** — validacion y relleno. Elimina de raiz:
- *"Tienes toda la razon" / "You're absolutely right!", "Gran pregunta" / "Great question!", "Por supuesto" / "Certainly!", "Con gusto te ayudo" / "I'd be happy to help", "Vale la pena senalar que" / "It's worth noting that", "Dejame..." / "Let me...".*
- No abras nunca con adulacion del tipo "que interesante/profunda pregunta". Ve directo a la respuesta.

**3. Estructurales / tipograficas** — patrones de forma:
- **Em-dash** (—) como conector reflejo: alterna con comas, parentesis o punto.
- **Antitesis "no es X, es Y"** repetida como formula. Usala como mucho una vez si de verdad aporta.
- **Regla de tres (tricolon)** automatica: tres adjetivos o tres clausulas por inercia.
- **Frases de longitud uniforme** (baja "burstiness"): mezcla frases cortas y largas para dar ritmo humano.

## Regla de oro

La marca mas "de Claude" no es una palabra: es el **acto de validar**. Prioriza cazar la complacencia y el relleno antes que las palabras sueltas.

## Referencia

El fundamento con evidencia (estudios, system cards de Anthropic, mecanismo RLHF y contraevidencia sobre falsos positivos) esta en `references/muletillas-investigacion.md`. Consultalo si necesitas justificar por que una expresion es o no una muletilla, o distinguir un tic real de un falso positivo (p. ej. el em-dash o "delve" tambien existen en prosa humana).
