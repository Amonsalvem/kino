// Fase 2 · Compuerta verbal determinista. Revisa textos contra voz.json: términos a evitar y patrones
// prohibidos (muletillas, estructuras). No juzga el tono —eso lo hace la rúbrica LLM de evals/—;
// atrapa lo que se puede atrapar sin modelo, gratis y en cada build.
//   node herramientas/voz.mjs <cliente> [archivo|carpeta …]     (por defecto: clientes/<id>/muestras)
// Sale con 1 si hay hallazgos de gravedad "error".
import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, relative } from 'node:path';
import { pathToFileURL } from 'node:url';
import { cliente, escribir, salir } from './lib/cliente.mjs';

export function reglas(voz) {
  const r = [];
  for (const e of voz.vocabulario?.evitar ?? [])
    r.push({ id: `evitar:${e.termino}`, re: new RegExp(e.patron ?? `(?<![\\p{L}])${e.termino.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(?![\\p{L}])`, 'giu'), porque: e.porque + (e.usar ? ` → usar «${e.usar}»` : ''), gravedad: e.gravedad ?? 'error' });
  for (const p of voz.patrones ?? []) r.push({ id: p.id, re: new RegExp(p.regex, (p.flags ?? '').replace('g', '') + 'gu'), porque: p.porque, gravedad: p.gravedad ?? 'aviso' });
  return r;
}
export function revisar(texto, rs) {
  const hallazgos = [];
  texto.split('\n').forEach((linea, i) => {
    for (const r of rs) for (const m of linea.matchAll(r.re)) hallazgos.push({ linea: i + 1, id: r.id, gravedad: r.gravedad, fragmento: m[0].slice(0, 60), porque: r.porque });
  });
  return hallazgos;
}

const esCli = process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href;
if (esCli) {
  const c = cliente(process.argv[2]);
  const archivoVoz = c.p('voz.json');
  if (!existsSync(archivoVoz)) salir('Falta voz.json (fase 2).');
  const voz = JSON.parse(readFileSync(archivoVoz, 'utf8'));
  const rs = reglas(voz);
  const objetivos = process.argv.slice(3).filter((a) => !a.startsWith('--'));
  const listar = (p) => (statSync(p).isDirectory() ? readdirSync(p).flatMap((f) => listar(join(p, f))) : /\.(md|txt|html)$/.test(p) ? [p] : []);
  const archivos = (objetivos.length ? objetivos : [c.p('muestras')]).filter(existsSync).flatMap(listar);
  if (!archivos.length) { console.log('voz · no hay textos que revisar (clientes/<id>/muestras/).'); process.exit(0); }
  let errores = 0, total = 0; const informe = {};
  for (const f of archivos) {
    const h = revisar(readFileSync(f, 'utf8'), rs);
    informe[relative(c.dir, f)] = h; total += h.length; errores += h.filter((x) => x.gravedad === 'error').length;
    console.log(`voz · ${relative(c.dir, f)} · ${h.length} hallazgos`);
    if (!process.argv.includes('--resumen')) for (const x of h) console.log(`  ${x.gravedad === 'error' ? 'ERROR' : 'aviso'} l${x.linea} [${x.id}] «${x.fragmento}» — ${x.porque}`);
  }
  escribir(c.p('reportes', 'voz.json'), informe);
  console.log(`\nvoz · ${archivos.length} textos · ${total} hallazgos · ${errores} errores`);
  process.exit(errores ? 1 : 0);
}
