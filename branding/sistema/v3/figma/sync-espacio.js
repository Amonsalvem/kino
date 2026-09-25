
const COL = "Espacio y radio", MODOS = ["Valor"], VARS = [["espacio/3xs","FLOAT",{"Valor":{"num":2}},""],["espacio/2xs","FLOAT",{"Valor":{"num":4}},""],["espacio/xs","FLOAT",{"Valor":{"num":8}},""],["espacio/s","FLOAT",{"Valor":{"num":12}},""],["espacio/m","FLOAT",{"Valor":{"num":16}},""],["espacio/l","FLOAT",{"Valor":{"num":24}},""],["espacio/xl","FLOAT",{"Valor":{"num":32}},""],["espacio/2xl","FLOAT",{"Valor":{"num":48}},""],["espacio/3xl","FLOAT",{"Valor":{"num":72}},""],["espacio/4xl","FLOAT",{"Valor":{"num":112}},""],["radio/nada","FLOAT",{"Valor":{"num":0}},""],["radio/xs","FLOAT",{"Valor":{"num":2}},""],["radio/s","FLOAT",{"Valor":{"num":4}},""],["radio/m","FLOAT",{"Valor":{"num":8}},""],["radio/l","FLOAT",{"Valor":{"num":14}},""],["radio/arco","FLOAT",{"Valor":{"num":999}},""],["radio/pleno","FLOAT",{"Valor":{"num":999}},""],["trazo/icono","FLOAT",{"Valor":{"num":1.7}},""],["linea/fino","FLOAT",{"Valor":{"num":1}},""],["linea/foco","FLOAT",{"Valor":{"num":2}},""],["quiebre/medio","FLOAT",{"Valor":{"num":600}},""],["quiebre/amplio","FLOAT",{"Valor":{"num":960}},""],["quiebre/extenso","FLOAT",{"Valor":{"num":1280}},""],["reticula/movil","FLOAT",{"Valor":{"num":4}},""],["reticula/tableta","FLOAT",{"Valor":{"num":8}},""],["reticula/web","FLOAT",{"Valor":{"num":12}},""],["reticula/presentacion","FLOAT",{"Valor":{"num":12}},""],["reticula/carta","FLOAT",{"Valor":{"num":6}},""],["contenedor/maximo","FLOAT",{"Valor":{"num":1152}},""],["contenedor/lectura","FLOAT",{"Valor":{"num":720}},""],["forma/radio/control","FLOAT",{"Valor":{"alias":"radio/m","coleccion":"Espacio y radio"}},""],["forma/radio/tarjeta","FLOAT",{"Valor":{"alias":"radio/l","coleccion":"Espacio y radio"}},""],["forma/radio/chip","FLOAT",{"Valor":{"alias":"radio/s","coleccion":"Espacio y radio"}},""],["forma/radio/pase-arco","FLOAT",{"Valor":{"alias":"radio/pleno","coleccion":"Espacio y radio"}},"Radio superior de la ventana del QR y del Pase vivo (forma Portal, X1)."],["forma/trazo/icono","FLOAT",{"Valor":{"alias":"trazo/icono","coleccion":"Espacio y radio"}},""]];
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
