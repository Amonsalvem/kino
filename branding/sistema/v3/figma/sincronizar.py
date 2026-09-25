#!/usr/bin/env python3
"""Escribe un script de use_figma por colección (sync-<col>.js) a partir de espec.json.
Cada script crea lo que falta, actualiza valores y alias, y no borra ninguna variable (regla 13)."""
import json, pathlib
R = pathlib.Path(__file__).resolve().parent
E = json.loads((R / 'espec.json').read_text(encoding='utf8'))['variables']
PLANTILLA = r'''
const COL = %(col)s, MODOS = %(modos)s, VARS = %(vars)s;
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
'''
for col in ['Primitivos', 'Espacio y radio', 'Movimiento', 'Tipografía', 'Color']:
    vs = [v for v in E if v['col'] == col]
    modos = ['Oscuro', 'Claro'] if col == 'Color' else ['Valor']
    data = [[v['nombre'], v['tipo'], v['modos'], v['desc'][:180]] for v in vs]
    js = PLANTILLA % {'col': json.dumps(col, ensure_ascii=False), 'modos': json.dumps(modos), 'vars': json.dumps(data, ensure_ascii=False, separators=(',', ':'))}
    f = R / f'sync-{col.split()[0].lower().replace("í","i")}.js'
    f.write_text(js, encoding='utf8'); print(f.name, len(js))
