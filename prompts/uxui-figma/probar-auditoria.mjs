// Prueba de auditoria-uxui.js con un Figma simulado, sin conector: pantallas en secciones, arco, verdes, oculto y página vacía.
// Uso: node prompts/uxui-figma/probar-auditoria.mjs [ruta del script]  (por omisión, el auditoria-uxui.js de esta carpeta)
import { readFileSync } from 'node:fs';
const src = readFileSync(process.argv[2] || new URL('./auditoria-uxui.js', import.meta.url), 'utf8');
let id = 0;
function N(type, name, props = {}, children = []) {
  const n = { id: String(++id), type, name, visible: true, children, fills: [], strokes: [], boundVariables: {}, width: 100, height: 100, ...props };
  for (const c of children) c.parent = n;
  n.findAll = f => { const out = []; (function w(x) { for (const c of x.children || []) { if (f(c)) out.push(c); w(c); } })(n); return out; };
  n.findOne = f => n.findAll(f)[0] || null;
  return n;
}
const MIXED = Symbol('mixed');
const comps = {};
const inst = (comp, texto, props = {}) => { const i = N('INSTANCE', comp, props, [N('TEXT', 'label', { characters: texto, textStyleId: 's', fontName: { family: 'Archivo' } })]); comps[i.id] = comp; return i; };
const txt = (s, props = {}) => N('TEXT', 't', { characters: s, textStyleId: 's', fontName: { family: 'Archivo' }, ...props });
const pant = (name, kids, modos = { c: 'm' }) => N('FRAME', name, { explicitVariableModes: modos, fills: [{ type: 'SOLID' }], boundVariables: { fills: [{ id: 'base' }] } }, kids);
const arco = name => N('FRAME', name, { topLeftRadius: 999, topRightRadius: 999, bottomLeftRadius: 16, bottomRightRadius: 16 });
function pagina(children) { const p = N('PAGE', 'Página', {}, children); return p; }
async function correr(p) {
  globalThis.figma = { mixed: MIXED, getNodeByIdAsync: async () => p, setCurrentPageAsync: async () => {},
    variables: { getVariableByIdAsync: async i => ({ name: i === 'verde' ? 'accion/fondo' : 'superficie/base' }) } };
  for (const x of p.findAll(() => true)) if (x.type === 'INSTANCE') x.getMainComponentAsync = async () => ({ name: comps[x.id], parent: null });
  const f = new (Object.getPrototypeOf(async function () {}).constructor)(src);
  return f();
}
// Caso 1: pantallas dentro de una sección, arco en Crear Pase (mal) y en Ventana del QR (bien), verde en Guardar límites, oculto con «Permitido».
const p1 = pagina([N('SECTION', 'Pases', {}, [
  pant('R-P-02 · Crear Pase · Vacío · Oscuro', [arco('Tarjeta'), inst('Botón de acción', 'Crear Pase', { height: 56, width: 328 })]),
  pant('R-P-08 · Detalle · Vigente · 320 · Oscuro', [N('FRAME', 'Ventana del QR', {}, [arco('Marco')]), N('FRAME', 'x', { visible: false }, [txt('Permitido')])]),
  N('FRAME', 'Ficha · R-P-02'),
]), pant('A-03 · Límites · Lleno · Claro', [inst('Botón de acción', 'Guardar límites', { height: 48, width: 200 }), inst('Botón de acción', 'Crear Pase')], {})]);
console.log(JSON.stringify(await correr(p1), null, 1));
// Caso 2: página sin pantallas con nombre válido.
console.log(JSON.stringify(await correr(pagina([N('SECTION', 's', {}, [N('FRAME', 'Pantalla 1')])])), null, 1));
