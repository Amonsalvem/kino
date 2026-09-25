
const COL = "Tipografía", MODOS = ["Valor"], VARS = [["texto/0","FLOAT",{"Valor":{"num":16}},""],["texto/1","FLOAT",{"Valor":{"num":19.2}},""],["texto/2","FLOAT",{"Valor":{"num":23.04}},""],["texto/3","FLOAT",{"Valor":{"num":27.65}},""],["texto/4","FLOAT",{"Valor":{"num":33.18}},""],["texto/5","FLOAT",{"Valor":{"num":39.81}},""],["texto/6","FLOAT",{"Valor":{"num":47.78}},""],["texto/n1","FLOAT",{"Valor":{"num":13.33}},""],["fuente/display","STRING",{"Valor":{"str":"Archivo"}},""],["fuente/texto","STRING",{"Valor":{"str":"Archivo"}},""],["fuente/dato","STRING",{"Valor":{"str":"JetBrains Mono"}},""],["ancho/titular","FLOAT",{"Valor":{"num":112}},""],["ancho/texto","FLOAT",{"Valor":{"num":100}},""],["peso/texto","FLOAT",{"Valor":{"num":400}},""],["peso/medio","FLOAT",{"Valor":{"num":500}},""],["peso/titulo","FLOAT",{"Valor":{"num":700}},""],["peso/display","FLOAT",{"Valor":{"num":800}},""],["interlinea/display","FLOAT",{"Valor":{"num":1.04}},""],["interlinea/titulo","FLOAT",{"Valor":{"num":1.16}},""],["interlinea/texto","FLOAT",{"Valor":{"num":1.6}},""],["interlinea/dato","FLOAT",{"Valor":{"num":1.3}},""],["tracking/display","FLOAT",{"Valor":{"num":-0.02}},""],["tracking/texto","FLOAT",{"Valor":{"num":0}},""],["tracking/dato","FLOAT",{"Valor":{"num":0.04}},""],["tracking/placa","FLOAT",{"Valor":{"num":0.06}},""],["tracking/etiqueta","FLOAT",{"Valor":{"num":0.08}},""],["columna/texto","FLOAT",{"Valor":{"num":62}},""],["columna/corta","FLOAT",{"Valor":{"num":42}},""]];
const cols = await figma.variables.getLocalVariableCollectionsAsync();
let c = cols.find(x => x.name === COL);
const creada = !c;
if (!c) { c = figma.variables.createVariableCollection(COL); c.renameMode(c.modes[0].modeId, MODOS[0]); }
for (const m of MODOS) if (!c.modes.find(x => x.name === m)) c.addMode(m);
const modo = n => c.modes.find(x => x.name === n).modeId;
const todas = await figma.variables.getLocalVariablesAsync();
const porCol = {}; for (const col of cols.concat(creada ? [c] : [])) porCol[col.id] = col.name;
const buscar = (col, nombre) => todas.find(v => v.name === nombre && porCol[v.variableCollectionId] === col) || nuevas[col + '|' + nombre];
const nuevas = {};
const scopes = (n, t) => {
  if (COL === 'Primitivos' || COL === 'Movimiento' || COL === 'Tipografía') return [];
  if (t === 'FLOAT') { if (/radio/.test(n)) return ['CORNER_RADIUS']; if (/^espacio/.test(n)) return ['GAP', 'WIDTH_HEIGHT']; if (/linea|trazo/.test(n)) return ['STROKE_FLOAT']; return []; }
  if (/^texto|\/texto$/.test(n)) return ['TEXT_FILL'];
  if (/borde|foco/.test(n)) return ['STROKE_COLOR'];
  return ['FRAME_FILL', 'SHAPE_FILL'];
};
let creadas = 0, actualizadas = 0;
for (const [n, t] of VARS.map(v => [v[0], v[1]])) {
  let v = buscar(COL, n);
  if (!v) { v = figma.variables.createVariable(n, c, t); v.scopes = scopes(n, t); nuevas[COL + '|' + n] = v; creadas++; }
}
const errores = [];
for (const [n, t, vals, desc] of VARS) {
  const v = buscar(COL, n);
  if (desc && v.description !== desc) v.description = desc;
  for (const [m, val] of Object.entries(vals)) {
    let x;
    if (val.alias) { const d = buscar(val.coleccion, val.alias); if (!d) { errores.push(n + ' → ' + val.alias); continue; } x = figma.variables.createVariableAlias(d); }
    else if (val.rgba) x = { r: val.rgba[0], g: val.rgba[1], b: val.rgba[2], a: val.rgba[3] };
    else if ('num' in val) x = val.num; else x = val.str;
    v.setValueForMode(modo(m), x); actualizadas++;
  }
}
return { coleccion: COL, id: c.id, modos: c.modes.map(m => m.name), variables: c.variableIds.length, creadas, valores: actualizadas, errores };
