// Núcleo DTCG sin dependencias: carga, recorre, resuelve alias, valida y convierte a CSS.
// Referencia: Design Tokens Format Module 2025.10 (designtokens.org).
// Acepta además los formatos "legados" (hex en cadena, "16px") con advertencia,
// para poder importar sistemas hechos con Style Dictionary sin romperlos.
import { readFileSync, existsSync } from 'node:fs';

export const TIPOS = [
  'color', 'dimension', 'fontFamily', 'fontWeight', 'duration', 'cubicBezier', 'number',
  'strokeStyle', 'border', 'transition', 'shadow', 'gradient', 'typography',
];
const ALIAS = /^\{([^{}]+)\}$/;
const ALIAS_G = /\{([^{}]+)\}/g;
const EXT_FLUIDO = 'com.gorr.fluido';
const EXT_CRUDO = 'com.gorr.css-crudo';

// ---------- carga ----------
export function fusionar(a, b) {
  for (const [k, v] of Object.entries(b)) {
    if (v && typeof v === 'object' && !Array.isArray(v) && a[k] && typeof a[k] === 'object' && !('$value' in v)) fusionar(a[k], v);
    else a[k] = v;
  }
  return a;
}
export function cargar(archivos) {
  const arbol = {};
  for (const f of archivos) {
    if (!existsSync(f)) throw new Error(`no existe ${f}`);
    fusionar(arbol, JSON.parse(readFileSync(f, 'utf8')));
  }
  return arbol;
}

// ---------- recorrido: devuelve Map ruta -> {ruta, $value, $type, $extensions, $description} ----------
export function aplanar(arbol) {
  const mapa = new Map();
  const rec = (nodo, ruta, tipoHeredado) => {
    const tipo = nodo.$type ?? tipoHeredado;
    if ('$value' in nodo) {
      mapa.set(ruta.join('.'), { ruta, $value: nodo.$value, $type: tipo, $extensions: nodo.$extensions, $description: nodo.$description });
      return;
    }
    for (const [k, v] of Object.entries(nodo)) {
      if (k.startsWith('$') || !v || typeof v !== 'object') continue;
      rec(v, [...ruta, k], tipo);
    }
  };
  rec(arbol, [], undefined);
  return mapa;
}

// ---------- alias ----------
export function resolver(mapa, valor, pila = []) {
  if (typeof valor === 'string') {
    const m = valor.match(ALIAS);
    if (m) {
      const ref = m[1];
      if (pila.includes(ref)) throw new Error(`alias circular: ${[...pila, ref].join(' → ')}`);
      const t = mapa.get(ref);
      if (!t) throw new Error(`alias roto: {${ref}}`);
      return resolver(mapa, t.$value, [...pila, ref]);
    }
    // alias incrustado en una cadena (formato legado, no DTCG)
    if (ALIAS_G.test(valor)) {
      ALIAS_G.lastIndex = 0;
      return valor.replace(ALIAS_G, (_, ref) => {
        const t = mapa.get(ref);
        if (!t) throw new Error(`alias roto: {${ref}}`);
        return valorCss(resolver(mapa, t.$value, [...pila, ref]), t.$type);
      });
    }
    return valor;
  }
  if (Array.isArray(valor)) return valor.map((v) => resolver(mapa, v, pila));
  if (valor && typeof valor === 'object') {
    const o = {};
    for (const [k, v] of Object.entries(valor)) o[k] = resolver(mapa, v, pila);
    return o;
  }
  return valor;
}
// Sustituye cada alias por {__var: nombre} para emitir CSS que referencia en vez de copiar valores.
export function conReferencias(valor, nombrar) {
  if (typeof valor === 'string' && ALIAS.test(valor)) return { __var: nombrar(valor.match(ALIAS)[1].split('.')) };
  if (Array.isArray(valor)) return valor.map((v) => conReferencias(v, nombrar));
  if (valor && typeof valor === 'object') return Object.fromEntries(Object.entries(valor).map(([k, v]) => [k, conReferencias(v, nombrar)]));
  return valor;
}
export const esAlias = (v) => typeof v === 'string' && ALIAS.test(v);
export const refDe = (v) => v.match(ALIAS)[1];

// ---------- conversión a CSS ----------
const num = (n, d = 4) => String(Math.round(n * 10 ** d) / 10 ** d);
const refVar = (v) => (v && typeof v === 'object' && v.__var ? `var(--${v.__var})` : null);
export function dimCss(v) {
  if (refVar(v)) return refVar(v);
  if (typeof v === 'string') return v;
  if (typeof v === 'number') return v === 0 ? '0' : `${v}px`;
  return v.value === 0 ? '0' : `${num(v.value)}${v.unit}`;
}
export function colorCss(v) {
  if (refVar(v)) return refVar(v);
  if (typeof v === 'string') return v;
  if (v.hex && (v.alpha === undefined || v.alpha === 1)) return v.hex;
  const c = v.components.map((x) => (x === 'none' ? 'none' : num(x, 5)));
  const a = v.alpha !== undefined && v.alpha !== 1 ? ` / ${num(v.alpha, 3)}` : '';
  if (v.colorSpace === 'srgb') return `color(srgb ${c.join(' ')}${a})`;
  return `${v.colorSpace}(${c.join(' ')}${a})`;
}
export function valorCss(v, tipo, ext) {
  if (refVar(v)) return refVar(v);
  if (ext?.[EXT_CRUDO]) return ext[EXT_CRUDO];
  if (ext?.[EXT_FLUIDO]) return clampFluido(ext[EXT_FLUIDO]);
  switch (tipo) {
    case 'color': return colorCss(v);
    case 'dimension': return dimCss(v);
    case 'duration': return typeof v === 'string' ? v : `${v.value}${v.unit}`;
    case 'fontFamily': return Array.isArray(v) ? v.map((f) => (/[\s-]/.test(f) && !/^[a-z-]+$/.test(f) ? `"${f}"` : f)).join(', ') : v;
    case 'cubicBezier': return Array.isArray(v) ? `cubic-bezier(${v.join(', ')})` : v;
    case 'shadow': {
      if (typeof v === 'string') return v;
      const capas = Array.isArray(v) ? v : [v];
      return capas.map((s) => [s.inset ? 'inset' : '', dimCss(s.offsetX), dimCss(s.offsetY), dimCss(s.blur), dimCss(s.spread), colorCss(s.color)].filter(Boolean).join(' ')).join(', ');
    }
    case 'border': return typeof v === 'string' ? v : `${dimCss(v.width)} ${typeof v.style === 'string' ? v.style : 'solid'} ${colorCss(v.color)}`;
    default: return typeof v === 'object' ? JSON.stringify(v) : String(v);
  }
}
export function clampFluido(f) {
  // f = {min:{value,unit:'rem'}, max:{...}, vwMin, vwMax, raiz}
  const raiz = f.raiz ?? 16;
  const aPx = (d) => (d.unit === 'rem' ? d.value * raiz : d.value);
  const minPx = aPx(f.min), maxPx = aPx(f.max);
  const pendiente = (maxPx - minPx) / (f.vwMax - f.vwMin);
  const interseccion = minPx - pendiente * f.vwMin;
  const d = f.decimales ?? 4;
  const r = (px) => `${(px / raiz).toFixed(d)}rem`;
  const [lo, hi] = minPx <= maxPx ? [minPx, maxPx] : [maxPx, minPx];
  return `clamp(${r(lo)}, ${(interseccion / raiz).toFixed(d)}rem + ${(pendiente * 100).toFixed(d)}vw, ${r(hi)})`;
}

// ---------- validación ----------
// Devuelve { errores:[], avisos:[] }. Error = rompe el contrato DTCG o el sistema. Aviso = legado o mala práctica.
export function validar(mapa, { capasSinLiterales = [] } = {}) {
  const errores = [], avisos = [];
  const E = (r, m) => errores.push(`${r}: ${m}`);
  const A = (r, m) => avisos.push(`${r}: ${m}`);
  const esDim = (v) => v && typeof v === 'object' && typeof v.value === 'number' && ['px', 'rem'].includes(v.unit);

  for (const [r, t] of mapa) {
    const v = t.$value;
    if (!t.$type) { E(r, 'sin $type (ni propio ni heredado)'); continue; }
    if (!TIPOS.includes(t.$type)) { E(r, `$type desconocido «${t.$type}»`); continue; }
    if (r.split('.').some((s) => /[{}.]/.test(s) || s.startsWith('$'))) E(r, 'nombre con caracteres reservados');

    // alias: que exista, que no sea circular y que el tipo coincida
    if (esAlias(v)) {
      const ref = refDe(v), dest = mapa.get(ref);
      if (!dest) { E(r, `alias roto {${ref}}`); continue; }
      try { resolver(mapa, v); } catch (e) { E(r, e.message); continue; }
      if (dest.$type && dest.$type !== t.$type) E(r, `alias de tipo ${t.$type} apunta a ${dest.$type}`);
      continue;
    }
    if (capasSinLiterales.some((c) => r.startsWith(c + '.')) && t.$type === 'color' && !t.$extensions?.[EXT_CRUDO])
      E(r, 'valor literal en la capa semántica: debe ser alias a un primitivo');

    if (typeof v === 'string' && ALIAS_G.test(v)) { ALIAS_G.lastIndex = 0; A(r, 'alias incrustado en cadena (legado); DTCG pide valor compuesto'); try { resolver(mapa, v); } catch (e) { E(r, e.message); } continue; }
    if (capasSinLiterales.some((c) => r.startsWith(c + '.')) && ['shadow', 'border', 'gradient'].includes(t.$type)) {
      const piezas = (Array.isArray(v) ? v : [v]).map((x) => x?.color).filter(Boolean);
      if (piezas.some((p) => !esAlias(p))) E(r, 'color literal dentro de un valor compuesto de la capa semántica: debe ser alias');
    }
    if (v && typeof v === 'object') { try { resolver(mapa, v); } catch (e) { E(r, e.message); continue; } }
    if (t.$extensions?.[EXT_CRUDO]) { A(r, 'valor CSS crudo en $extensions: no es portable a otras plataformas'); continue; }

    switch (t.$type) {
      case 'color':
        if (typeof v === 'string') { /^#([0-9a-f]{6}|[0-9a-f]{8})$/i.test(v) ? A(r, 'color como cadena hex (legado 2023); 2025.10 pide {colorSpace, components}') : E(r, `color inválido «${v}»`); }
        else if (!v || typeof v.colorSpace !== 'string' || !Array.isArray(v.components)) E(r, 'color sin colorSpace/components');
        break;
      case 'dimension':
        if (typeof v === 'string') { /^-?\d*\.?\d+(px|rem)$|^0$/.test(v) ? A(r, `dimensión como cadena «${v}» (legado)`) : E(r, `dimensión inválida «${v}»`); }
        else if (!esDim(v)) E(r, 'dimensión debe ser {value:number, unit:"px"|"rem"}');
        break;
      case 'fontFamily': if (!(typeof v === 'string' || (Array.isArray(v) && v.every((x) => typeof x === 'string')))) E(r, 'fontFamily inválida'); break;
      case 'fontWeight': if (!(typeof v === 'number' && v >= 1 && v <= 1000) && typeof v !== 'string') E(r, 'fontWeight fuera de 1–1000'); break;
      case 'number': if (typeof v !== 'number') E(r, 'number debe ser numérico'); break;
      case 'duration': if (typeof v === 'string') A(r, 'duración como cadena (legado)'); else if (!(v && typeof v.value === 'number' && ['ms', 's'].includes(v.unit))) E(r, 'duración inválida'); break;
      case 'cubicBezier': if (!(Array.isArray(v) && v.length === 4 && v[0] >= 0 && v[0] <= 1 && v[2] >= 0 && v[2] <= 1)) E(r, 'cubicBezier inválido'); break;
      case 'shadow': if (typeof v === 'string') A(r, 'sombra como cadena CSS (legado)'); break;
      default: break;
    }
    if (t.$extensions?.[EXT_FLUIDO]) {
      const f = t.$extensions[EXT_FLUIDO];
      if (!esDim(f.min) || !esDim(f.max) || !(f.vwMax > f.vwMin)) E(r, 'extensión fluida incompleta');
    }
  }
  return { errores, avisos };
}

export const EXT = { FLUIDO: EXT_FLUIDO, CRUDO: EXT_CRUDO };
