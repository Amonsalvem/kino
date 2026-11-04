// Verifica con color.js cada par declarado en pares.json, en los dos temas.
// Falla con código 1 si algún par no alcanza su mínimo: sirve como paso de CI.
import Color from 'colorjs.io';
import { readFileSync } from 'node:fs';

const vars = (archivo) => {
  const css = readFileSync(archivo, 'utf8');
  const m = {};
  for (const [, k, v] of css.matchAll(/--(kino-[\w-]+)\s*:\s*([^;]+);/g)) m[k] = v.trim();
  return m;
};

const primitivos = vars('build/primitivos.css');
const pares = JSON.parse(readFileSync('pares.json', 'utf8'));

const resolver = (mapa, nombre, visto = 0) => {
  let v = mapa[nombre] ?? primitivos[nombre];
  if (!v) throw new Error(`token ausente: ${nombre}`);
  const ref = v.match(/^var\(--([\w-]+)\)$/);
  if (ref) {
    if (visto > 16) throw new Error(`referencia circular en ${nombre}`);
    return resolver(mapa, ref[1], visto + 1);
  }
  return v;
};

let fallos = 0;
for (const tema of ['oscuro', 'claro']) {
  const mapa = { ...primitivos, ...vars(`build/tema-${tema}.css`) };
  for (const p of pares) {
    const fg = new Color(resolver(mapa, p.fg));
    const bg = new Color(resolver(mapa, p.bg));
    // color.js: contrast(fondo, frente). APCA no es simétrico, el orden importa.
    const wcag = Math.round(bg.contrast(fg, 'WCAG21') * 100) / 100;
    const apca = Math.round(bg.contrast(fg, 'APCA') * 10) / 10;
    const pasa = wcag >= p.min;
    if (!pasa) fallos++;
    console.log(
      `${pasa ? 'ok  ' : 'FALLA'} ${tema.padEnd(7)} ${p.que.padEnd(38)} ${String(wcag).padStart(6)}:1  Lc ${String(apca).padStart(6)}  min ${p.min}`
    );
  }
}
console.log(`\n${pares.length * 2} pares · ${fallos} fallos`);
process.exit(fallos ? 1 : 0);
