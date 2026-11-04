// Fase 3/4 · Compuerta de legibilidad. Recorre pares.json en cada tema.
// WCAG 2.2 (razón) es la COMPUERTA: es el estándar exigible hoy.
// APCA (Lc, base de WCAG 3) se reporta siempre y bloquea solo si el par declara "apcaMin".
// Razón: APCA predice mejor la legibilidad en temas oscuros, pero aún no es norma.
import Color from 'colorjs.io';
import { readFileSync, existsSync } from 'node:fs';
import { cliente, escribir, salir } from './lib/cliente.mjs';

const c = cliente(process.argv[2]);
const archivoPares = c.p('pares.json');
if (!existsSync(archivoPares)) salir('Falta pares.json: declara qué texto va sobre qué fondo y con qué mínimo.');
const resuelto = JSON.parse(readFileSync(c.p('build', 'tokens.resuelto.json'), 'utf8'));
const pares = JSON.parse(readFileSync(archivoPares, 'utf8'));

let fallos = 0; const filas = [];
for (const [tema, vars] of Object.entries(resuelto.temas)) {
  const buscar = (n) => vars[n] ?? resuelto.primitivos[n] ?? salir(`token ausente en ${tema}: ${n}`);
  for (const p of pares) {
    // color.js: contrast(fondo, frente). APCA no es simétrico: el orden importa.
    const bg = new Color(buscar(p.bg)), fg = new Color(buscar(p.fg));
    const wcag = Math.round(bg.contrast(fg, 'WCAG21') * 100) / 100;
    const lc = Math.round(bg.contrast(fg, 'APCA') * 10) / 10;
    const pasaW = wcag >= p.min, pasaA = p.apcaMin === undefined || Math.abs(lc) >= p.apcaMin;
    if (!pasaW || !pasaA) fallos++;
    filas.push({ tema, que: p.que, wcag, apcaLc: lc, min: p.min, apcaMin: p.apcaMin, pasa: pasaW && pasaA });
    console.log(`${pasaW && pasaA ? 'ok   ' : 'FALLA'} ${tema.padEnd(7)} ${p.que.padEnd(40)} ${String(wcag).padStart(6)}:1 (min ${p.min})  Lc ${String(lc).padStart(6)}${p.apcaMin ? ` (min ${p.apcaMin})` : ''}`);
  }
}
// Avisos APCA sin bloquear: texto de cuerpo por debajo de Lc 60 suele leerse mal aunque pase WCAG 2.
const flojos = filas.filter((f) => f.min >= 4.5 && Math.abs(f.apcaLc) < 60);
escribir(c.p('reportes', 'contraste.json'), filas);
console.log(`\ncontraste · ${filas.length} pares · ${fallos} fallos${flojos.length ? ` · ${flojos.length} pasan WCAG 2 pero quedan bajo Lc 60 (revisar para texto de cuerpo)` : ''}`);
process.exit(fallos ? 1 : 0);
