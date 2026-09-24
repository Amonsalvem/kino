// Kino — construye la capa de tokens con gorr-brand-system (desde el 22 sep 2026).
// La fuente de verdad es ../../gorr-brand-system/clientes/kino/ (marca.config.json, voz.json, tokens/ DTCG 2025.10).
// Este script corre la cadena completa (paleta → tipo → validar → construir → contraste → voz → skill → evals)
// y copia el CSS generado a build/, donde lo recoge ensamblar.mjs junto con capa-componentes.css.
// El build anterior con Style Dictionary quedó en _obsoleto/style-dictionary-2026-09-22/.
import { spawnSync } from 'node:child_process';
import { copyFileSync, mkdirSync } from 'node:fs';
import { resolve } from 'node:path';

const GBS = resolve('../../gorr-brand-system');
const r = spawnSync(process.execPath, [resolve(GBS, 'herramientas/ciclo.mjs'), 'kino'], { stdio: 'inherit' });
if (r.status !== 0) process.exit(r.status);
mkdirSync('build', { recursive: true });
for (const f of ['primitivos.css', 'tema-oscuro.css', 'tema-claro.css']) {
  copyFileSync(resolve(GBS, 'clientes/kino/build', f), `build/${f}`);
  console.log(`  build/${f}`);
}
