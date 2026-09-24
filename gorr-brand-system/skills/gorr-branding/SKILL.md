---
name: gorr-branding
description: Conduce un proyecto de marca de GORR de punta a punta con el repo gorr-brand-system (brief, posicionamiento, voz, identidad visual, tokens DTCG, skill de marca y evals). Usar al iniciar, retomar o revisar el branding de un cliente.
---

# GORR · Branding de punta a punta

Operas el método de `PLAYBOOK.md` del repo `gorr-brand-system`. Tu trabajo es llevar al cliente de fase en fase sin saltarte compuertas y dejando cada decisión atada al problema que resuelve.

## 1. Ubicarte
1. Encuentra el repo (carpeta con `PLAYBOOK.md` y `herramientas/ciclo.mjs`). Si no existe, pídelo antes de seguir.
2. Si el cliente no existe: `npm run nuevo -- <id> "<Nombre>"`.
3. Determina la fase actual leyendo `clientes/<id>/`:

| Si falta o está en COMPLETAR… | Fase |
|---|---|
| `00-brief.md` | 0 |
| tabla final de `01-estrategia/posicionamiento.md` | 1 |
| `voz.json` con perfil «borrador» | 2 |
| `porque` en familias de `marca.config.json`, o `03-visual/identidad.md` | 3 |
| `npm run ciclo -- <id>` falla en validar/contraste | 4 |
| evals sin correr o bajo el umbral | 5 |
| `06-entrega/entrega.md` sin versión 1.0.0 | 6 |

Dile al equipo en una línea en qué fase está el cliente y qué compuerta falta.

## 2. Reglas de trabajo
- **Cada decisión responde a un problema.** Si una decisión verbal o visual no apunta a una fila del posicionamiento o a un hallazgo, dilo y propón quitarla o justificarla.
- **Observado vs. inferido.** En brief y posicionamiento, marca cada afirmación. No inventes datos del cliente; si falta uno, pregúntalo.
- **Fase 0 y 1 se trabajan con el cliente.** Para el brief usa la skill `constructor-de-brief`. No llenes el posicionamiento por tu cuenta: prepara las preguntas de cada paso de Dunford.
- **Categoría solo si aplica.** Abre `categoria.md` solo si las tres condiciones de su encabezado se cumplen.
- **Fase 2**: usa la skill `gorr-voz-de-marca`.
- **Fases 3 y 4**: usa la skill `gorr-identidad-en-codigo`.
- **Nunca edites archivos generados** (`build/`, `skill/`, `evals/`, `tokens/10-*`, `tokens/20-*`). Se cambian las fuentes y se corre `npm run ciclo -- <id>`.
- **Compuertas**: si `ciclo` falla, arregla la causa en la fuente; no bajes el mínimo de `pares.json` ni borres un patrón de `voz.json` para que pase sin decírselo al equipo.

## 3. Fase 5 · Marca para IA
1. `npm run ciclo -- <id>` genera `skill/<id>-marca/` y `evals/`.
2. Revisa que la skill generada se lea bien y que ninguna sección quede vacía.
3. Las evals requieren red y `ANTHROPIC_API_KEY`: `cd clientes/<id>/evals && npx promptfoo@latest eval`. Si no se pueden correr, dilo; no reportes un porcentaje que no mediste.
4. Umbral: ≥ 80 % de casos aprobados sin edición. Por debajo, ajusta `voz.json` o las reglas y vuelve a medir.

## 4. Fase 6 · Entrega
- Manual navegable como artefacto publicado, construido con `build/<id>-tokens.css` (nada de hex copiados).
- Registra la versión en `06-entrega/entrega.md` (semver: mayor = token renombrado o eliminado).
- La skill del cliente se entrega como carpeta para instalar en su Claude.

## 5. Al terminar cada sesión
Resume en tres líneas: fase actual, compuertas que pasan, lo que falta y quién lo tiene que decidir.
