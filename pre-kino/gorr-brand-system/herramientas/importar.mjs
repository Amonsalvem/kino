// Importa tokens "legados" (p. ej. hechos para Style Dictionary) al formato DTCG 2025.10.
//   node herramientas/importar.mjs <cliente> <origen.json> <destino.tokens.json> [--excluir a.b,c.d]
// Convierte: hex → objeto de color · "16px" → {value,unit} · clamp() → extensión fluida ·
// sombra en cadena → capas DTCG · familia en cadena → lista · color literal en capa semántica →
// alias a primitivo.color.fijo.* si coincide con un color fijo de marca.config.json.
// Lo que no tiene forma DTCG (p. ej. un radio de cuatro valores) queda en $extensions["com.gorr.css-crudo"].
import Color from 'colorjs.io';
import { readFileSync } from 'node:fs';
import { cliente, escribir } from './lib/cliente.mjs';
import { EXT } from './lib/dtcg.mjs';

const [, , id, origen, destino, ...resto] = process.argv;
const c = cliente(id);
const excluir = (resto[resto.indexOf('--excluir') + 1] ?? '').split(',').filter(Boolean);
if (!resto.includes('--excluir')) excluir.length = 0;
const fijos = Object.fromEntries(Object.entries(c.cfg.color?.fijos ?? {}).map(([k, v]) => [v.toUpperCase(), k]));
const capas = c.cfg.capasSemanticas ?? [];
const t = c.cfg.tipo ?? {};
const notas = [];

const colorObj = (hex) => {
  const col = new Color(hex);
  const [L, C, H] = col.to('oklch').coords;
  const o = { colorSpace: 'oklch', components: [+L.toFixed(4), +(C || 0).toFixed(4), Number.isNaN(H) || H == null ? 0 : +H.toFixed(2)], hex: hex.slice(0, 7).toUpperCase() };
  if (col.alpha < 1) o.alpha = +(+col.alpha).toFixed(3);
  return o;
};
const dim = (s) => {
  if (s === '0') return { value: 0, unit: 'px' };
  const m = s.match(/^(-?\d*\.?\d+)(px|rem)$/);
  return m ? { value: +m[1], unit: m[2] } : null;
};
const colorPieza = (s) => (s.startsWith('{') ? s : colorObj(s));

function sombra(cadena) {
  const capasS = []; let prof = 0, buf = '';
  for (const ch of cadena) { if (ch === '(') prof++; if (ch === ')') prof--; if (ch === ',' && !prof) { capasS.push(buf); buf = ''; } else buf += ch; }
  capasS.push(buf);
  return capasS.map((capa) => {
    const piezas = capa.trim().split(/\s+/);
    const inset = piezas.includes('inset');
    const color = piezas.find((p) => p.startsWith('#') || p.startsWith('{') || /^[a-z]+\(/.test(p));
    const medidas = piezas.filter((p) => p !== 'inset' && p !== color).map(dim);
    if (!color || medidas.some((m) => !m)) throw new Error(`sombra no interpretable: ${capa}`);
    const [offsetX, offsetY, blur = { value: 0, unit: 'px' }, spread = { value: 0, unit: 'px' }] = medidas;
    return { color: colorPieza(color), offsetX, offsetY, blur, spread, ...(inset ? { inset: true } : {}) };
  });
}

function convertir(tok, ruta) {
  const v = tok.$value, tipo = tok.$type, r = ruta.join('.');
  if (typeof v !== 'string' || /^\{[^{}]+\}$/.test(v)) return tok;
  const out = { ...tok };
  if (tipo === 'color') {
    if (capas.includes(ruta[0]) && fijos[v.toUpperCase()]) { out.$value = `{primitivo.color.fijo.${fijos[v.toUpperCase()]}}`; notas.push(`${r}: literal ${v} → alias fijo.${fijos[v.toUpperCase()]}`); }
    else out.$value = colorObj(v);
  } else if (tipo === 'dimension') {
    const d = dim(v);
    const cl = v.match(/^clamp\(\s*(-?[\d.]+)rem\s*,.*,\s*(-?[\d.]+)rem\s*\)$/);
    if (d) out.$value = d;
    else if (cl && t.vwMin) {
      const min = { value: +cl[1], unit: 'rem' }, max = { value: +cl[2], unit: 'rem' };
      out.$value = min;
      out.$extensions = { ...tok.$extensions, [EXT.FLUIDO]: { min, max, vwMin: t.vwMin, vwMax: t.vwMax, raiz: t.raiz ?? 16, decimales: t.decimales ?? 4 } };
    } else {
      const primera = dim(v.split(/\s+/)[0]);
      out.$value = primera ?? { value: 0, unit: 'px' };
      out.$extensions = { ...tok.$extensions, [EXT.CRUDO]: v };
      notas.push(`${r}: «${v}» no tiene forma DTCG → css-crudo (revisar)`);
    }
  } else if (tipo === 'fontFamily') {
    out.$value = v.split(',').map((s) => s.trim().replace(/^["']|["']$/g, ''));
  } else if (tipo === 'shadow') {
    const capasDeSombra = sombra(v);
    if (capas.includes(ruta[0])) for (const s of capasDeSombra) {
      const hex = s.color.hex && !s.color.alpha ? s.color.hex : null;
      if (hex && fijos[hex]) { s.color = `{primitivo.color.fijo.${fijos[hex]}}`; notas.push(`${r}: literal ${hex} en sombra → alias fijo.${fijos[hex]}`); }
    }
    out.$value = capasDeSombra;
  }
  return out;
}

function recorrer(nodo, ruta) {
  if (excluir.some((e) => ruta.join('.') === e)) return undefined;
  if (nodo && typeof nodo === 'object' && '$value' in nodo) return convertir(nodo, ruta);
  const o = {};
  for (const [k, v] of Object.entries(nodo)) {
    if (k.startsWith('$')) { o[k] = v; continue; }
    const r = recorrer(v, [...ruta, k]);
    if (r !== undefined && !(typeof r === 'object' && Object.keys(r).length === 0)) o[k] = r;
  }
  return o;
}

const salida = recorrer(JSON.parse(readFileSync(origen, 'utf8')), []);
escribir(c.p(destino), salida);
console.log(`importado ${origen.split('/').slice(-2).join('/')} → ${destino}${excluir.length ? ` (excluidos: ${excluir.join(', ')})` : ''}`);
for (const n of notas) console.log('  · ' + n);
