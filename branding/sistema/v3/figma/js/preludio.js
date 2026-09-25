// Preludio común: variables, estilos y ayudas para ligar todo a tokens (ningún valor suelto).
const cols = await figma.variables.getLocalVariableCollectionsAsync();
const COL = Object.fromEntries(cols.map(c => [c.name, c]));
const ALL = await figma.variables.getLocalVariablesAsync();
const V = (col, n) => { const v = ALL.find(x => x.variableCollectionId === COL[col].id && x.name === n); if (!v) throw new Error('falta variable ' + col + '/' + n); return v; };
const C = n => V('Color', n), E = n => V('Espacio y radio', n), P = n => V('Primitivos', 'color/' + n);
const pintura = v => figma.variables.setBoundVariableForPaint({ type: 'SOLID', color: { r: 0, g: 0, b: 0 } }, 'color', v);
const fill = (n, v) => { n.fills = v ? [pintura(v)] : []; return n; };
const borde = (n, v, w = 'linea/fino', dash) => { n.strokes = [pintura(v)]; n.setBoundVariable('strokeWeight', E(w)); if (dash) n.dashPattern = dash; return n; };
const radio = (n, r) => { for (const k of ['topLeftRadius', 'topRightRadius', 'bottomLeftRadius', 'bottomRightRadius']) n.setBoundVariable(k, E(r)); return n; };
const radioPortal = n => { n.setBoundVariable('topLeftRadius', E('radio/pleno')); n.setBoundVariable('topRightRadius', E('radio/pleno')); n.setBoundVariable('bottomLeftRadius', E('radio/l')); n.setBoundVariable('bottomRightRadius', E('radio/l')); return n; };
const pad = (n, y, x) => { n.setBoundVariable('paddingTop', E('espacio/' + y)); n.setBoundVariable('paddingBottom', E('espacio/' + y)); n.setBoundVariable('paddingLeft', E('espacio/' + x)); n.setBoundVariable('paddingRight', E('espacio/' + x)); return n; };
const gap = (n, g) => { n.setBoundVariable('itemSpacing', E('espacio/' + g)); return n; };
const TS = Object.fromEntries((await figma.getLocalTextStylesAsync()).map(s => [s.name, s]));
for (const s of Object.values(TS)) await figma.loadFontAsync(s.fontName);
const txt = async (s, estilo, colorVar, ancho) => {
  const t = figma.createText(); await t.setTextStyleIdAsync(TS[estilo].id); t.characters = s; fill(t, colorVar);
  if (ancho) { t.resize(ancho, t.height); t.textAutoResize = 'HEIGHT'; } return t; };
const auto = (dir, nombre, g, py, px) => { const f = figma.createAutoLayout(dir, { name: nombre }); f.fills = []; if (g) gap(f, g); if (py) pad(f, py, px || py); return f; };
const modoColor = (n, m) => n.setExplicitVariableModeForCollection(COL['Color'], COL['Color'].modes.find(x => x.name === m).modeId);
const pagina = async (id) => { const p = await figma.getNodeByIdAsync(id); await figma.setCurrentPageAsync(p); return p; };
const hoja = (p, nombre, x = 0, y = 0) => {
  let f = p.children.find(n => n.name === nombre);
  if (f) f.remove();
  f = figma.createAutoLayout('VERTICAL', { name: nombre }); p.appendChild(f); f.x = x; f.y = y;
  f.resize(1188, 100); f.counterAxisSizingMode = 'FIXED'; f.primaryAxisSizingMode = 'AUTO';
  fill(f, C('superficie/base')); pad(f, '3xl', '3xl'); gap(f, 'xl'); modoColor(f, 'Oscuro'); return f; };
const cabeza = async (f, ojo, titulo, lede) => {
  f.appendChild(await txt(ojo, 'Dato/etiqueta', C('texto/secundario')));
  f.appendChild(await txt(titulo, 'Display/display-2', C('texto/primario'), 1044));
  if (lede) f.appendChild(await txt(lede, 'Texto/cuerpo', C('texto/secundario'), 900)); };
const seccion = async (f, titulo, lede) => {
  const s = auto('VERTICAL', titulo, 'm'); f.appendChild(s); s.layoutSizingHorizontal = 'FILL';
  s.appendChild(await txt(titulo, 'Título/titulo-2', C('texto/primario'), 1044));
  if (lede) s.appendChild(await txt(lede, 'Texto/cuerpo-s', C('texto/secundario'), 900));
  return s; };
