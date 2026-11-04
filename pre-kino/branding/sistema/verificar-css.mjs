// Comprueba que ninguna variable --kino-* se use sin estar definida.
// Existe por un fallo real: capa-componentes.css referenciaba --kino-resplandor-vigente
// y --kino-relieve-membrana sin que ningún token las definiera. No rompía nada,
// no fallaba ningún test, y la tarjeta del Pase vigente salía sin resplandor.
import { readFileSync } from 'node:fs';

const css = readFileSync('kino-brand.css', 'utf8');

const definidas = new Set([...css.matchAll(/(--kino-[\w-]+)\s*:/g)].map((m) => m[1]));
const usadas = new Set([...css.matchAll(/var\((--kino-[\w-]+)/g)].map((m) => m[1]));

// Se fijan en el marcado, no en el CSS: no son un fallo.
const EN_LINEA = new Set(['--kino-vida']);

const huerfanas = [...usadas].filter((v) => !definidas.has(v) && !EN_LINEA.has(v)).sort();
const sinUsar = [...definidas].filter((v) => !usadas.has(v)).sort();

console.log(`${definidas.size} definidas · ${usadas.size} usadas`);
if (sinUsar.length) {
  console.log(`\n${sinUsar.length} definidas y no usadas en este archivo (normal: son la paleta para consumo externo)`);
}
if (huerfanas.length) {
  console.log('\nUSADAS SIN DEFINIR:');
  for (const v of huerfanas) console.log('  ' + v);
  process.exit(1);
}
console.log('\nninguna variable huérfana');
