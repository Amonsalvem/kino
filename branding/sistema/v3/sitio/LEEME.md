# Sitio «Kino · Sistema de marca»

Fuentes del sitio del sistema de marca. Se arma en un solo HTML con Python 3, sin dependencias externas.

## Cómo se construye

Desde esta carpeta:

```bash
python3 verbal.py && python3 secciones.py && python3 construir.py
python3 verificar.py
```

| Script | Qué hace |
|---|---|
| `verbal.py` | Fuente del departamento 2. Genera `contenido/02-verbal.html` y, en `build/`, `guia-de-contenido.md`, `ux-writing.md`, `muestras-ux.md` y `verbal-verificacion.json` |
| `secciones.py` | Genera los departamentos 03 a 12 y el glosario en `contenido/` |
| `construir.py` | Arma el sitio y escribe `texto-visible.md` |
| `verificar.py` | Cuenta rayas, palabras vetadas por el vocabulario, mezclas de tú y usted y textos fuera de límite. Necesita `build/verbal-verificacion.json`, que sale de `verbal.py` |
| `probar.mjs` | Busca los patrones de `patrones-nuevos.json` en los archivos que recibe (`node probar.mjs <archivos>`). Lee ese JSON de la carpeta desde donde se corre; el archivo vive en `gorr-brand-system/clientes/kino/02-verbal/`. <!-- TODO: completar por el equipo: desde qué carpeta se corre --> |

## Salidas

- `build/kino-sistema-de-marca.html`: el sitio completo.
- `build/artefacto.html`: el cuerpo sin doctype, para publicar como artefacto.
- `../../../../Kino_Sistema_de_marca.html`: copia del sitio en la raíz del repositorio.
- `texto-visible.md`: el texto que ve el lector, sin los ejemplos incorrectos.

`build/` está en el `.gitignore` de `branding/sistema/`.

## De dónde salen los tokens

`construir.py` lee `gorr-brand-system/clientes/kino/build/kino-tokens.css` y los temas claro y oscuro de esa misma carpeta. Si no existen, usa la copia local `kino-tokens.css`. Para regenerarlos: `cd gorr-brand-system && npm run ciclo -- kino`.

## Después de construir

Pasa la compuerta de voz sobre el texto visible:

```bash
cd ../../../../gorr-brand-system && npm run voz -- kino ../branding/sistema/v3/sitio/texto-visible.md
```

Más contexto en [`TRASPASO-SISTEMA-DE-MARCA.md`](../../../../TRASPASO-SISTEMA-DE-MARCA.md), §5.
