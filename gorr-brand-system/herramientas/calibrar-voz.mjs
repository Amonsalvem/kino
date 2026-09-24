// Calibra la compuerta verbal con pares reales antes/después (pruebas/voz-antes.md y voz-despues.md,
// una frase por línea, alineadas). Mide cuántas frases "antes" atrapa (cobertura) y cuántas "después"
// marca por error (falsos positivos). Falla si hay falsos positivos: una compuerta que acusa texto
// limpio se termina ignorando.
import { readFileSync, existsSync } from 'node:fs';
import { cliente, escribir } from './lib/cliente.mjs';
import { reglas, revisar } from './voz.mjs';

const c = cliente(process.argv[2]);
const [fa, fd] = [c.p('pruebas', 'voz-antes.md'), c.p('pruebas', 'voz-despues.md')];
if (!existsSync(fa) || !existsSync(fd)) { console.log('calibrar-voz · sin pruebas/voz-antes.md y voz-despues.md: se omite.'); process.exit(0); }
const rs = reglas(JSON.parse(readFileSync(c.p('voz.json'), 'utf8')));
const lineas = (f) => readFileSync(f, 'utf8').split('\n').filter((l) => l.trim() && !l.startsWith('#'));
const antes = lineas(fa), despues = lineas(fd);
const atrapadas = antes.filter((l) => revisar(l, rs).length).length;
const falsos = despues.map((l) => [l, revisar(l, rs)]).filter(([, h]) => h.length);
const r = { frases: antes.length, cobertura: atrapadas, coberturaPct: Math.round((100 * atrapadas) / antes.length), falsosPositivos: falsos.length };
escribir(c.p('reportes', 'calibracion-voz.json'), r);
console.log(`calibrar-voz · ${atrapadas}/${antes.length} frases problemáticas atrapadas (${r.coberturaPct} %) · ${falsos.length} falsos positivos`);
for (const [l, h] of falsos) console.log(`  FALSO POSITIVO [${h.map((x) => x.id).join(', ')}] ${l.slice(0, 90)}`);
console.log('  El resto (tríadas por inercia, énfasis como «real», redundancias) no tiene forma de regex: lo juzga la rúbrica de evals/.');
process.exit(falsos.length ? 1 : 0);
