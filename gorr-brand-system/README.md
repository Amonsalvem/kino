# gorr-brand-system

Sistema de GORR para producir una marca completa —estrategia, voz, identidad visual, marca en código y marca para IA— con compuertas verificables entre fases. El método está en **[PLAYBOOK.md](PLAYBOOK.md)**; esto es cómo se usa.

## Empezar

```bash
node -v                                   # >= 20
npm install                               # única dependencia: colorjs.io
npm run prueba                            # la plantilla pasa sus propias compuertas
npm run nuevo -- acme "Acme Café"         # crea clientes/acme desde plantilla/
npm run ciclo -- acme                     # paleta → tipo → validar → construir → contraste → voz → skill → evals
```

Sin red: si ya existe otra carpeta con `node_modules/colorjs.io` (p. ej. `kino/branding/sistema`), copiarla a `node_modules/` funciona igual.

## Estructura

```
PLAYBOOK.md              el método: fases, entregables, compuertas
herramientas/            la cadena (Node, sin dependencias salvo colorjs.io)
  lib/dtcg.mjs             núcleo DTCG 2025.10: carga, alias, validación, emisión CSS
  paleta.mjs               color por objetivo de contraste (método Leonardo, OKLCH)
  tipo.mjs                 escala fluida de tipo y espacio (Utopia)
  importar.mjs             migra tokens legados (Style Dictionary) a DTCG 2025.10
  validar.mjs              compuerta DTCG + «ningún literal en la capa semántica»
  construir.mjs            tokens → CSS por referencia, un bloque por tema
  contraste.mjs            compuerta WCAG 2.2 + informe APCA
  voz.mjs                  compuerta verbal determinista (voz.json)
  calibrar-voz.mjs         mide la compuerta verbal con pares antes/después reales
  skill.mjs                empaqueta la marca como Agent Skill
  evals.mjs                genera la suite promptfoo (términos + voz + rúbrica NN/g)
  ciclo.mjs                corre todo en orden y se detiene en la primera compuerta
plantilla/               lo que copia `npm run nuevo`
clientes/<id>/           un cliente = una carpeta
  marca.config.json        parámetros de color, tipo, temas, reglas
  voz.json                 identidad verbal medible
  pares.json               qué texto va sobre qué fondo, con su mínimo
  tokens/                  fuente DTCG (10-, 20- generados; tema/ a mano)
  build/                   CSS generado (no editar)
  skill/<id>-marca/        skill generada (no editar)
  evals/                   suite promptfoo generada
  reportes/                paleta, contraste, voz, calibración
skills/                  skills de Claude que operan este playbook
terrazzo.config.mjs      salida multiplataforma (no verificada, ver abajo)
```

## Correr las evals (requiere red y `ANTHROPIC_API_KEY`)

```bash
cd clientes/<id>/evals
npx promptfoo@latest eval
npx promptfoo@latest view
```
Revisar el proveedor en `marca.config.json → evals.proveedor` antes de correr.

## Estado de cada recurso del informe

| # | Recurso | Cómo entra | Estado |
|---|---|---|---|
| 1 | DTCG 2025.10 | formato de todos los tokens; `lib/dtcg.mjs` valida los 13 tipos | **usado y probado** |
| 2 | Anthropic Agent Skills | `skill.mjs` genera la skill de cada cliente; `skills/` opera el playbook | **usado y probado** (formato) |
| 3 | Dunford | `plantilla/01-estrategia/posicionamiento.md` | plantilla |
| 4 | Utopia | `tipo.mjs` implementa la fórmula; reproduce la calculadora (16/1.2 → 18/1.25, 320–1240 px da `clamp(1rem, 0.9565rem + 0.2174vw, 1.125rem)`) | **usado y probado** |
| 5 | Leonardo | `paleta.mjs` aplica el método (paso por razón de contraste); exporta la entrada para Leonardo real | método propio; Leonardo **sin correr** (sin red) |
| 6 | NN/g 4 dimensiones | `voz.json → perfil`, rúbrica de evals | **usado** |
| 7 | APCA | `contraste.mjs` vía colorjs.io, informe y `apcaMin` opcional | **usado y probado** |
| 8 | Terrazzo | `terrazzo.config.mjs` para salidas nativas | **no verificado** (sin red al crearlo); el CSS lo emite `construir.mjs` |
| 9 | promptfoo | `evals.mjs` genera config, rúbrica y aserción JS | config generada; sin correr con promptfoo. La misma rúbrica y compuerta se corrieron con subagentes (Kino: 12/15) |
| 10 | Mailchimp Content Style Guide | estructura de `guia-de-contenido.md` (licencia NC: solo estructura) | plantilla |
| 11 | Play Bigger | `categoria.md` con test de aplicabilidad | plantilla |
| 12 | Agent skill DTCG (dgtlntv) | no incorporado: `validar.mjs` cubre la validación sin depender de él | descartado por redundante |

## Deuda declarada
- **Emisor CSS propio en vez de Terrazzo.** Se escribió porque no había acceso a npm y porque para web basta: ~60 líneas, sin dependencias. Si un cliente necesita iOS/Android, se activa Terrazzo y se verifica su config. Costo de mantener el emisor: bajo mientras solo sea CSS.
- **Extensiones propias** `com.gorr.fluido` y `com.gorr.css-crudo`: DTCG no tiene tipo fluido. Otras herramientas ignoran la extensión y usan `$value` (el mínimo), que es válido.
- **Proveedor de evals** fijado por nombre de modelo: revisar al correr.
