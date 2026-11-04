// Contrasta la paleta generada con Adobe Leonardo real (@adobe/leonardo-contrast-colors).
// Requiere haber corrido activar-herramientas.sh. Para cada familia y cada fondo, pide a Leonardo los
// mismos objetivos de contraste y mide la distancia perceptual (ΔE OK) con lo que produjo paleta.mjs.
//   node herramientas/leonardo.mjs <cliente>
import Color from 'colorjs.io';
import { readFileSync } from 'node:fs';
import { cliente, escribir, salir } from './lib/cliente.mjs';

let L;
try { L = await import('@adobe/leonardo-contrast-colors'); } catch { salir('Falta @adobe/leonardo-contrast-colors: correr activar-herramientas.sh en el Mac.'); }
const c = cliente(process.argv[2]);
const cfg = c.cfg.color;
const prim = JSON.parse(readFileSync(c.p('tokens', '10-primitivo-color.tokens.json'), 'utf8')).primitivo.color;
const hex = (v) => (typeof v === 'string' ? v : v.hex);
const [ladoOsc, refOsc] = Object.entries(cfg.fondos)[0];
const informe = {}; let peor = { de: 0 };
for (const [lado, ref] of Object.entries(cfg.fondos)) {
  const [fb, kb] = ref.split('.');
  const bgHex = hex(prim[fb][kb].$value);
  const fondo = new L.BackgroundColor({ name: 'fondo', colorKeys: [bgHex], ratios: [1] });
  const lightness = Math.round(new Color(bgHex).to('hsluv').coords[2]);
  for (const fam of Object.keys({ ...(cfg.objetivosEnNeutros ? cfg.neutros : {}), ...cfg.familias })) {
    const clave = hex(prim[fam][`${lado}45`].$value);
    const col = new L.Color({ name: fam, colorKeys: [clave], ratios: cfg.objetivos, colorspace: 'OKLCH', smooth: false });
    const tema = new L.Theme({ colors: [col], backgroundColor: fondo, lightness, output: 'HEX' });
    const salida = tema.contrastColors.find((x) => x.name === fam)?.values ?? [];
    informe[fam] ??= {};
    cfg.objetivos.forEach((t, i) => {
      const k = `${lado}${Math.round(t * 10)}`;
      const nuestro = hex(prim[fam][k].$value), leo = salida[i]?.value;
      if (!leo) return;
      const de = +new Color(nuestro).deltaE(new Color(leo), 'OK').toFixed(4);
      const r = +new Color(bgHex).contrast(new Color(leo), 'WCAG21').toFixed(2);
      informe[fam][k] = { kino: nuestro, leonardo: leo.toUpperCase(), deltaEOK: de, razonLeonardo: r };
      if (de > peor.de) peor = { de, fam, k, kino: nuestro, leo };
    });
  }
}
escribir(c.p('reportes', 'leonardo-comparacion.json'), informe);
const todos = Object.values(informe).flatMap((f) => Object.values(f));
const media = todos.reduce((a, x) => a + x.deltaEOK, 0) / todos.length;
console.log(`leonardo · ${todos.length} pasos comparados · ΔE OK medio ${media.toFixed(3)} · máximo ${peor.de} (${peor.fam} ${peor.k}: ${peor.kino} vs ${peor.leo})`);
console.log('  ΔE OK < 0.02 es imperceptible; 0.02–0.05 perceptible de cerca; > 0.05 distinto.');
