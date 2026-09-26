# Kino

Carpeta de trabajo de Kino, una plataforma de control de acceso para conjuntos cerrados. Aquí están el diagnóstico, el sistema de marca, el sistema de motion y los entregables del proyecto. El MVP en producción no vive en este repositorio.

Para entender en qué va el proyecto, empieza por:

| Documento | Para qué |
|---|---|
| [`TRASPASO-SISTEMA-DE-MARCA.md`](TRASPASO-SISTEMA-DE-MARCA.md) | Qué hay, dónde está y en qué fase va el sistema de marca |
| [`MAESTRO-KINO.md`](MAESTRO-KINO.md) | Documento maestro del proyecto |
| [`decisiones.md`](decisiones.md) | Decisiones con su estado |
| [`avances.md`](avances.md) | Bitácora de avance |
| [`inspeccion/`](inspeccion/) | Evidencia cruda de la inspección del sistema actual |
| [`docs/proyecto/`](docs/proyecto/) | Documentos de conocimiento del proyecto (diagnóstico, arquetipos, evals, motor de decks) |
| [`CLAUDE.md`](CLAUDE.md) | Instrucciones para trabajar con Claude en este repositorio |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Cómo se trabaja: ramas, commits, PR y bitácoras |

Los documentos con aviso de «Documento histórico» se conservan por trazabilidad y no son fuente de decisiones. Lo reemplazado está en [`_obsoleto/`](_obsoleto/).

## Proyectos

No hay herramienta de workspaces: cada proyecto Node tiene su propio `package.json` y `package-lock.json`, y se instala por separado. Los proyectos se enlazan con rutas relativas; casi todos leen los tokens de `gorr-brand-system/clientes/kino/build/`.

| Proyecto | Ruta | Stack | Documentación |
|---|---|---|---|
| gorr-brand-system: tokens, contraste y voz de la marca | [`gorr-brand-system/`](gorr-brand-system/) | Node ≥ 20 | [`README.md`](gorr-brand-system/README.md) |
| Sistema de marca, capa aplicable (CSS y tokens) | [`branding/sistema/`](branding/sistema/) | Node ≥ 20 | [`LEEME.md`](branding/sistema/LEEME.md), [`INSTALAR.md`](branding/sistema/INSTALAR.md) |
| Sitio «Kino · Sistema de marca» | [`branding/sistema/v3/sitio/`](branding/sistema/v3/sitio/) | Python 3 | [`LEEME.md`](branding/sistema/v3/sitio/LEEME.md) |
| Láminas de las paradas | `branding/sistema/v3/fase3/`, `parada4/`, `parada4b/`, `parada4c/` | Python 3 | <!-- TODO: completar por el equipo --> |
| Recursos animados (Lottie y Remotion) | [`branding/sistema/v3/motion/`](branding/sistema/v3/motion/) | Python 3, Node | [`README.md`](branding/sistema/v3/motion/README.md) |
| @kino/motion | [`paquetes/kino-motion/`](paquetes/kino-motion/) | TypeScript | [`README.md`](paquetes/kino-motion/README.md) |
| @kino/motion-nativo, adaptador para React Native | [`paquetes/kino-motion-nativo/`](paquetes/kino-motion-nativo/) | TypeScript, React Native | [`README.md`](paquetes/kino-motion-nativo/README.md) |
| Scripts de entorno y capturas | [`scripts/`](scripts/) | Bash, Node | Sección «Pruebas visuales» abajo |

## Requisitos

- Node 20 o superior (`engines` en `gorr-brand-system/package.json` y `branding/sistema/package.json`).
- Python 3, sin dependencias externas, para el sitio, las láminas y la galería de motion.
- Chromium con Playwright para las capturas (`scripts/capturar.mjs`).

## Cómo correr cada proyecto

**gorr-brand-system**, desde `gorr-brand-system/`:

```bash
npm install
npm run ciclo -- kino          # paleta, tipo, validar, contraste, voz y skill
npm run validar -- kino        # valida los tokens DTCG
npm run voz -- kino <archivo>  # compuerta de voz sobre un texto
npm run calibrar-voz -- kino   # calibración de la compuerta de voz
npm run prueba                 # prueba de humo de la plantilla
```

**Sistema de marca**, desde `branding/sistema/`:

```bash
npm install
npm run construir              # tokens y verificación de CSS y contraste
```

**Sitio**, desde `branding/sistema/v3/sitio/`:

```bash
python3 verbal.py && python3 secciones.py && python3 construir.py
python3 verificar.py
```

Más detalle en su [`LEEME.md`](branding/sistema/v3/sitio/LEEME.md).

**Láminas de las paradas**:

```bash
cd branding/sistema/v3/fase3 && python3 build.py           # Parada 3
cd branding/sistema/v3/parada4 && python3 construir.py     # Parada 4 (igual en parada4b y parada4c)
```

Las de la Parada 4 se escriben en la raíz (`parada-4.html`, `parada-4b.html`, `parada-4c.html`).

**@kino/motion**, desde `paquetes/kino-motion/`:

```bash
npm install
npm test                       # vitest
npm run verificar              # build, tipos, test, lint de motion y laboratorio
```

**@kino/motion-nativo**, desde `paquetes/kino-motion-nativo/`:

```bash
npm install --legacy-peer-deps
npm test
npm run verificar              # tipos, test, build web y prueba web
```

**Remotion**, desde `branding/sistema/v3/motion/remotion/`:

```bash
npm install
npm run tipos
npm run estudio
```

**Galería de motion**, desde `branding/sistema/v3/motion/galeria/`:

```bash
python3 construir.py
```

## Pruebas visuales

```bash
bash scripts/preparar-entorno.sh          # lo corre el hook SessionStart de .claude/settings.json
node scripts/capturar.mjs <archivo.html>  # 360, 768 y 1440 px, oscuro y claro
node scripts/auditar-responsive.mjs <archivo.html>
```
