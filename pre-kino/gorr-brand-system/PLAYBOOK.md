# GORR · Playbook de branding

Cómo se produce una marca completa en GORR, de la primera entrevista al manual entregado. Cada fase tiene **un entregable, un método con dueño identificable, una herramienta y una compuerta**. No se pasa de fase sin cruzar la compuerta.

```
 0 BRIEF ──► 1 ESTRATEGIA ──► 2 VERBAL ──► 3 VISUAL ──► 4 MARCA EN CÓDIGO ──► 5 MARCA PARA IA ──► 6 ENTREGA
 problema     posicionamiento   voz.json     paleta/tipo    tokens DTCG → CSS      skill + evals        manual + versión
             (categoría*)       guía         logo           validar · contraste    rúbrica ≥ 80 %
                                              ▲                    │
                                              └── la compuerta de contraste devuelve a la fase 3
```
\* Solo si aplica (ver `plantilla/01-estrategia/categoria.md`).

## La regla que ordena todo
**Cada decisión de marca responde a un problema.** El posicionamiento (fase 1) es la lista de problemas y valores; toda decisión verbal (fase 2) y visual (fase 3) se registra con la fila que responde. Una decisión sin fila es estética y se revisa. Por eso `marca.config.json` exige un `porque` en cada familia de color y la skill generada lo muestra.

## Mapa de fases

| Fase | Entregable | Método (fuente) | Herramienta en este repo | Compuerta |
|---|---|---|---|---|
| 0 · Brief | `00-brief.md` | Discovery con el cliente | skill `constructor-de-brief` | Problema escrito sin soluciones; aprobado por el cliente |
| 1 · Estrategia | `01-estrategia/posicionamiento.md` | April Dunford, *Obviously Awesome* | plantilla de 10 pasos | Ventas del cliente lo explica con sus palabras; cada atributo tiene prueba |
| 1b · Categoría | `01-estrategia/categoria.md` | Play Bigger (Lochhead et al.) | plantilla con test de aplicabilidad | Solo si las 3 condiciones se cumplen |
| 2 · Verbal | `voz.json` + `02-verbal/guia-de-contenido.md` + `mensajes.md` | NN/g, *Four Dimensions of Tone of Voice*; estructura de Mailchimp Content Style Guide (CC BY-NC: solo estructura) | `npm run voz`, `npm run calibrar-voz` | 0 errores en muestras reales; 0 falsos positivos |
| 3 · Visual | `marca.config.json` (color, tipo) + `03-visual/identidad.md` + logo | Paleta por objetivo de contraste (método Adobe Leonardo); escala fluida Utopia; APCA | `npm run paleta`, `npm run tipo` | Cada decisión con su problema; licencias anotadas |
| 4 · Código | `tokens/*.tokens.json` → `build/<id>-tokens.css` | W3C DTCG Format Module 2025.10 | `npm run validar`, `construir`, `contraste` | 0 errores DTCG; 0 fallos WCAG 2.2 en todos los temas |
| 5 · IA | `skill/<id>-marca/` + `evals/` | Anthropic Agent Skills (estándar abierto); promptfoo | `npm run skill`, `npm run evals` | Copy generado pasa la rúbrica sin edición en ≥ 80 % de los casos |
| 6 · Entrega | manual navegable + `06-entrega/entrega.md` | semver para tokens | artefacto publicado | El cliente puede cambiar un color sin nosotros |

`npm run ciclo -- <cliente>` corre las fases 3 → 5 en orden y se detiene en la primera compuerta que falle.

## Fase por fase

### 0 · Brief
Entrevistar, no llenar. La skill `constructor-de-brief` hace las preguntas por bloques. Cada afirmación se marca **observada** o **inferida**. Si el cliente pide «un logo», la compuerta obliga a escribir el problema de negocio detrás.

### 1 · Estrategia
Posicionamiento con los 10 pasos de Dunford, en sesión con el cliente y con alguien de ventas presente. El orden importa: alternativas competitivas → atributos → valor → cliente ideal → categoría. El entregable es una tabla, no un eslogan. Diseño de categoría solo para empresas que de verdad crean mercado; a una pyme que necesita claridad le cuesta caro.

### 2 · Verbal
1. Perfil de tono con las 4 dimensiones de NN/g (formal↔casual, serio↔divertido, respetuoso↔irreverente, sobrio↔entusiasta), en escala 1–5, con una nota de cómo se nota cada valor en una frase real. Va en `voz.json → perfil`.
2. «Somos / no somos», vocabulario propio, términos a evitar y pares que no se mezclan.
3. **Patrones**: expresiones regulares para lo que se puede atrapar sin modelo (muletillas, antítesis de efecto, léxico de agencia, términos prohibidos). La plantilla trae los genéricos del español.
4. Calibrar con textos reales del cliente: si hay pares antes/después (una corrección de estilo previa), ponerlos en `pruebas/` y exigir **0 falsos positivos**. En el piloto Kino la compuerta atrapó 21 de 42 frases problemáticas sin acusar ninguna de las corregidas; el resto (tríadas por inercia, énfasis vacío) lo juzga la rúbrica LLM.
5. Guía de contenido: estructura tipo Mailchimp, texto propio.

### 3 · Visual
- **Color**: se declara matiz y croma máximo por familia (o una `semilla` hex) y el sistema resuelve cada paso para una razón de contraste exacta contra el fondo de cada tema (`d45` = 4.5:1 sobre el oscuro, `l45` sobre el claro). Accesible por construcción, no auditado después. Tono constante en OKLCH; para comparar con Adobe Leonardo real, `reportes/leonardo-entrada.json`.
- **Tipo y espacio**: Utopia (dos escalas modulares interpoladas con `clamp()`). Los parámetros se ajustan en utopia.fyi y se copian a `marca.config.json`.
- **Logo, familias, iconos, imagen**: decisiones de diseñador, registradas en `03-visual/identidad.md` con su problema.
- **Colores fijos** (blanco, negro de sombra, transparente) se declaran en `color.fijos` para que la capa semántica nunca lleve literales.

### 4 · Marca en código
Tres capas:
```
tokens/10-primitivo-color.tokens.json   ← generado (paleta)
tokens/20-primitivo-tipo.tokens.json    ← generado (tipo)
tokens/30-…tokens.json                  ← a mano o importado (radios, sombras base, fuentes)
tokens/tema/<tema>.tokens.json          ← capa semántica: SOLO alias a primitivos
```
- `validar`: contrato DTCG 2025.10 (13 tipos, alias rotos o circulares, tipos que no coinciden) y la regla de la casa: **ningún literal en la capa semántica**, tampoco dentro de sombras o bordes.
- `construir`: primitivos con valor; semánticos por referencia (`var(--…)`), así cambiar un matiz arrastra todos los temas; variante `prefers-color-scheme` automática.
- `contraste`: `pares.json` declara qué texto va sobre qué fondo. WCAG 2.2 es la compuerta (es el estándar exigible); APCA se reporta siempre y marca el texto de cuerpo bajo Lc 60. Un par puede exigir APCA con `apcaMin`.
- Sistemas heredados (p. ej. hechos para Style Dictionary) se migran con `npm run importar`.

### 5 · Marca para IA
- `skill`: genera `skill/<id>-marca/SKILL.md` desde las fuentes (reglas, color con significado, tokens, tipo, voz, vocabulario, patrones) + `references/`. Nunca se edita a mano. Se instala en el Claude del cliente o en el nuestro: todo documento, deck o HTML que produzca Claude sale con la marca.
- `evals`: genera la suite de promptfoo. Tres capas por caso: términos prohibidos, la compuerta de voz como aserción JS, y una rúbrica LLM con el perfil NN/g. La rúbrica vive en `evals/rubrica.md`, independiente de promptfoo, para poder cambiar de evaluador (promptfoo pasó a ser de OpenAI el 9 mar 2026).
- Umbral de producto: si el copy pasa sin edición en ≥ 80 % de los casos, se puede vender como servicio de contenido; si no, se ajusta la skill o la voz y se vuelve a medir.

### 6 · Entrega
Manual navegable (artefacto), tokens con semver, skill instalada, guía de contenido. El criterio de éxito de la entrega: el cliente cambia un color o agrega un término prohibido sin llamarnos, y la cadena le dice si rompió algo.

## Qué NO hace este sistema
- No diseña el logo ni elige tipografías: registra y verifica esas decisiones.
- No corre las evals sin red ni API key: las deja listas.
- No reemplaza el criterio: una compuerta verde dice que no hay errores detectables, no que la marca sea buena.
