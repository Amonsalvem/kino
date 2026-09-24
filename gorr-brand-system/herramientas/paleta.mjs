// Fase 3 · Color. Genera la paleta primitiva por OBJETIVO DE CONTRASTE, al estilo de Adobe Leonardo:
// cada paso de una familia se resuelve para dar exactamente la razón WCAG pedida contra el fondo del tema.
// Diferencia con Leonardo: aquí el tono es constante en OKLCH (Leonardo interpola entre colores clave en CAM02).
// Por eso también se escribe reportes/leonardo-entrada.json, para contrastar con Leonardo real cuando haya red.
//
// Nombres: pasos neutros 100…800 por luminosidad; pasos por contraste d<razón×10> sobre el fondo oscuro
// y l<razón×10> sobre el claro. Ej.: d45 = 4.5:1 sobre el fondo oscuro.
import Color from 'colorjs.io';
import { cliente, escribir } from './lib/cliente.mjs';

const c = cliente(process.argv[2]);
const cfg = c.cfg.color;
if (!cfg) { console.log('marca.config.json sin sección "color": nada que generar.'); process.exit(0); }
const dtcg2025 = (cfg.formato ?? 'dtcg-2025') === 'dtcg-2025';

const oklch = (L, C, H) => new Color('oklch', [L, C, H]);
function croma(L, H, cmax) {
  if (oklch(L, cmax, H).inGamut('srgb')) return cmax;
  let lo = 0, hi = cmax;
  for (let i = 0; i < 30; i++) { const m = (lo + hi) / 2; oklch(L, m, H).inGamut('srgb') ? (lo = m) : (hi = m); }
  return lo;
}
function paso(L, H, cmax) {
  const C = croma(L, H, cmax);
  const col = oklch(L, C, H).to('srgb').toGamut();
  return { hex: col.toString({ format: 'hex', collapse: false }).toUpperCase(), L, C, H };
}
const razon = (bg, hex) => new Color(bg).contrast(new Color(hex), 'WCAG21');
const apca = (bg, hex) => new Color(bg).contrast(new Color(hex), 'APCA');

function resolverObjetivo(objetivo, bg, H, cmax, aclarar) {
  const Lbg = new Color(bg).to('oklch').coords[0];
  let lo = aclarar ? Lbg : 0, hi = aclarar ? 1 : Lbg;
  for (let i = 0; i < 40; i++) {
    const m = (lo + hi) / 2;
    const r = razon(bg, paso(m, H, cmax).hex);
    if (aclarar) (r < objetivo ? (lo = m) : (hi = m)); else (r < objetivo ? (hi = m) : (lo = m));
  }
  // redondear hacia el lado seguro: el hex final nunca queda por debajo del objetivo
  let L = aclarar ? hi : lo, p = paso(L, H, cmax), n = 0;
  while (razon(bg, p.hex) < objetivo && n++ < 200) { L += aclarar ? 0.001 : -0.001; p = paso(L, H, cmax); }
  return p;
}

function semilla(f) {
  if (f.h !== undefined) return { H: f.h, cmax: f.cmax };
  const o = new Color(f.semilla).to('oklch').coords;
  return { H: o[2], cmax: f.cmax ?? o[1] };
}

// Paleta congelada: si marca.config.json → color.congelar apunta a un palette.json heredado
// ({paleta:{familia:{paso:hex}}}), los pasos que existan ahí conservan su hex exacto. Es la paleta
// «de registro» (la que ya se presentó); el generador solo completa los pasos nuevos.
let congelada = null;
if (cfg.congelar) {
  const { readFileSync } = await import('node:fs');
  congelada = JSON.parse(readFileSync(c.p(cfg.congelar), 'utf8')).paleta;
}
const deRegistro = (fam, k, p) => {
  const hex = congelada?.[fam]?.[k];
  if (!hex) return p;
  const o = new Color(hex).to('oklch').coords;
  return { hex: hex.toUpperCase(), L: o[0], C: o[1] || 0, H: Number.isNaN(o[2]) || o[2] == null ? 0 : o[2], congelado: true };
};
const valor = (p) =>
  dtcg2025
    ? { colorSpace: 'oklch', components: [+p.L.toFixed(4), +p.C.toFixed(4), +p.H.toFixed(2)], hex: p.hex }
    : p.hex;

const color = {}, reporte = {}, leonardo = { fondos: {}, colores: [] };
for (const [fam, f] of Object.entries(cfg.neutros ?? {})) {
  const { H, cmax } = semilla(f);
  color[fam] = { $description: [f.significa, f.porque].filter(Boolean).join(' · ') || undefined };
  f.L.forEach((L, i) => { color[fam][(i + 1) * 100] = { $value: valor(deRegistro(fam, String((i + 1) * 100), paso(L, H, cmax))) }; });
}
const hexDe = (ref) => {
  const [fam, k] = ref.split('.');
  const v = color[fam]?.[k]?.$value;
  if (!v) throw new Error(`fondo ${ref} no existe entre los neutros`);
  return typeof v === 'string' ? v : v.hex;
};
const fondos = Object.fromEntries(Object.entries(cfg.fondos).map(([k, ref]) => [k, hexDe(ref)]));
leonardo.fondos = fondos;

const familias = { ...(cfg.objetivosEnNeutros ? cfg.neutros : {}), ...cfg.familias };
for (const [fam, f] of Object.entries(familias)) {
  const { H, cmax } = semilla(f);
  color[fam] ??= { $description: [f.significa, f.porque].filter(Boolean).join(' · ') || undefined };
  reporte[fam] = {};
  for (const [lado, bg] of Object.entries(fondos)) {
    const aclarar = new Color(bg).to('oklch').coords[0] < 0.5;
    for (const t of cfg.objetivos) {
      const k = `${lado}${Math.round(t * 10)}`;
      const p = deRegistro(fam, k, resolverObjetivo(t, bg, H, cmax, aclarar));
      color[fam][k] = { $value: valor(p) };
      reporte[fam][k] = { congelado: !!p.congelado, objetivo: t, wcag: +razon(bg, p.hex).toFixed(2), apcaLc: +apca(bg, p.hex).toFixed(1), L: +p.L.toFixed(3), C: +p.C.toFixed(3) };
    }
  }
  leonardo.colores.push({ name: fam, colorKeys: [paso(0.6, H, cmax).hex], ratios: cfg.objetivos, colorspace: 'OKLCH' });
}

// Colores fijos (transparente, negro de sombra…): existen para que la capa semántica nunca lleve literales.
if (cfg.fijos) {
  color.fijo = { $description: 'Colores fijos: la capa semántica los referencia en vez de escribir literales.' };
  for (const [k, hex] of Object.entries(cfg.fijos)) {
    const col = new Color(hex), [L, C, H] = col.to('oklch').coords;
    color.fijo[k] = { $value: dtcg2025
      ? { colorSpace: 'oklch', components: [+L.toFixed(4), +(C || 0).toFixed(4), Number.isNaN(H) || H == null ? 0 : +H.toFixed(2)], hex: hex.slice(0, 7).toUpperCase(), ...(col.alpha < 1 ? { alpha: +(+col.alpha).toFixed(3) } : {}) }
      : hex.toUpperCase() };
  }
}

const faltanRazones = Object.entries({ ...cfg.neutros, ...cfg.familias }).filter(([, f]) => !f.porque).map(([k]) => k);
escribir(c.p('tokens', '10-primitivo-color.tokens.json'), { primitivo: { color: { $type: 'color', ...color } } });
escribir(c.p('reportes', 'paleta.json'), { fondos, contraste: reporte });
escribir(c.p('reportes', 'leonardo-entrada.json'), leonardo);

console.log(`paleta · ${Object.keys(color).length} familias · ${Object.values(color).reduce((n, f) => n + Object.keys(f).filter((k) => k !== '$description').length, 0)} colores · formato ${dtcg2025 ? 'DTCG 2025.10' : 'hex legado'}`);
for (const [fam, r] of Object.entries(reporte))
  console.log(`  ${fam.padEnd(10)} ${Object.entries(r).map(([k, v]) => `${k} ${v.wcag}`).join('  ')}`);
if (faltanRazones.length) console.log(`\n  AVISO: familias sin "porque" (qué problema resuelven): ${faltanRazones.join(', ')}`);
