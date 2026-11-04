// Une la salida de gorr-brand-system (build/*.css) con la capa de componentes en kino-brand.css.
import { readFileSync, writeFileSync } from 'node:fs';

const leer = (p) => readFileSync(p, 'utf8').trim();
const sinSelector = (css) =>
  css.slice(css.indexOf('{') + 1, css.lastIndexOf('}')).trim();

const claro = leer('build/tema-claro.css');

// Un @import solo es válido antes de cualquier otra regla. capa-componentes.css va al
// final del ensamblado, así que sus @import hay que subirlos al principio o el
// navegador los descarta en silencio y las tipografías nunca cargan.
const IMPORT = /^[ \t]*@import[^;]+;[ \t]*$/gm;
const imports = [];
const sacarImports = (css) =>
  css.replace(IMPORT, (m) => { imports.push(m.trim()); return ''; }).replace(/\n{3,}/g, '\n\n');

const componentes = sacarImports(leer('capa-componentes.css'));

const salida = [
  '/* Kino — capa de marca. Generado: no editar a mano.',
  '   Fuente: tokens/*.json  ·  Construcción: npm run tokens */',
  ...imports,
  '',
  leer('build/primitivos.css'),
  '',
  leer('build/tema-oscuro.css'),
  '',
  claro,
  '',
  '@media (prefers-color-scheme: light) {',
  '  :root:not([data-tema="oscuro"]) {',
  sinSelector(claro).split('\n').map((l) => '    ' + l.trim()).join('\n'),
  '  }',
  '}',
  '',
  componentes,
  '',
].join('\n');

writeFileSync('kino-brand.css', salida);
console.log(`kino-brand.css · ${salida.length} bytes`);
