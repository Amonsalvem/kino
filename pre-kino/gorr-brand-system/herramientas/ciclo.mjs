// Corre la cadena completa de un cliente, en orden, y se detiene en la primera compuerta que falle.
//   npm run ciclo -- <cliente> [--sin-paleta] [--sin-tipo]
// --sin-paleta / --sin-tipo: no regenerar esos primitivos (p. ej. si se ajustaron a mano o se importaron).
import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { join } from 'node:path';
import { cliente, RAIZ } from './lib/cliente.mjs';

const id = process.argv[2];
const c = cliente(id);
const banderas = new Set(process.argv.slice(3));
const pasos = [
  { h: 'paleta', fase: '3 visual', si: () => c.cfg.color && !banderas.has('--sin-paleta') },
  { h: 'tipo', fase: '3 visual', si: () => c.cfg.tipo && !banderas.has('--sin-tipo') },
  { h: 'validar', fase: '4 código', compuerta: 'tokens DTCG válidos' },
  { h: 'construir', fase: '4 código' },
  { h: 'contraste', fase: '4 código', compuerta: 'contraste WCAG 2.2 y APCA', si: () => existsSync(c.p('pares.json')) },
  { h: 'voz', fase: '2 verbal', compuerta: 'voz sin errores', si: () => existsSync(c.p('voz.json')) },
  { h: 'calibrar-voz', fase: '2 verbal', compuerta: 'voz sin falsos positivos', si: () => existsSync(c.p('pruebas', 'voz-antes.md')) },
  { h: 'skill', fase: '5 IA' },
  { h: 'evals', fase: '5 IA', si: () => existsSync(c.p('voz.json')) },
];
const resumen = [];
for (const p of pasos) {
  if (p.si && !p.si()) { resumen.push([p.h, p.fase, 'omitido']); continue; }
  console.log(`\n── ${p.fase} · ${p.h} ${'─'.repeat(Math.max(0, 50 - p.h.length))}`);
  const r = spawnSync(process.execPath, [join(RAIZ, 'herramientas', `${p.h}.mjs`), id, ...(p.h === 'voz' ? ['--resumen'] : [])], { stdio: 'inherit' });
  if (r.status !== 0) {
    resumen.push([p.h, p.fase, `FALLA${p.compuerta ? ` (compuerta: ${p.compuerta})` : ''}`]);
    break;
  }
  resumen.push([p.h, p.fase, p.compuerta ? `ok · ${p.compuerta}` : 'ok']);
}
console.log(`\n══ ${c.cfg.cliente.nombre} ══`);
for (const [h, f, e] of resumen) console.log(`  ${f.padEnd(9)} ${h.padEnd(13)} ${e}`);
const falla = resumen.some(([, , e]) => e.startsWith('FALLA'));
console.log(falla ? '\nSe detuvo en una compuerta. Corregir y volver a correr.' : '\nCadena completa. Pendiente fuera de la cadena: correr evals con red (ver README).');
process.exit(falla ? 1 : 0);
