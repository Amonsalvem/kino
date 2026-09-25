// Auditoría de pinturas y exportación de variables (bloque 6).
// 1. Recorre todas las páginas salvo «Referencias» y cuenta rellenos y trazos SOLID sin variable ligada.
// 2. Exporta cada variable con su code syntax (--kino-*), colección, modo, tipo y valor resuelto.
//    La salida pasa de 20 kB: se pide en dos mitades (out.slice(0, 175) y out.slice(175)),
//    se guarda como export-parte-1.json y export-parte-2.json, y exportar_variables.py arma variables-figma.json.
// 3. Los estilos de efecto (sombras) se exportan aparte a export-efectos.json.
const cols = await figma.variables.getLocalVariableCollectionsAsync();
const ALL = await figma.variables.getLocalVariablesAsync();
const byId = Object.fromEntries(ALL.map(v => [v.id, v]));
const colOf = Object.fromEntries(cols.map(c => [c.id, c]));
const h = x => Math.round(x * 255).toString(16).padStart(2, '0');
const resolver = (v, modo) => { let cur = v; for (let i = 0; i < 10; i++) { const c = colOf[cur.variableCollectionId]; const m = c.modes.find(x => x.name === modo) || c.modes[0]; const val = cur.valuesByMode[m.modeId]; if (val && val.type === 'VARIABLE_ALIAS') { cur = byId[val.id]; continue; } return val; } };
const fmt = (val, tipo) => { if (tipo === 'COLOR' && val && typeof val === 'object') { if (val.a === 0) return 'transparente'; const b = ('#' + h(val.r) + h(val.g) + h(val.b)).toUpperCase(); return val.a !== undefined && val.a < 1 ? b + h(val.a).toUpperCase() : b; } return val; };
const out = [];
for (const v of ALL) { const c = colOf[v.variableCollectionId]; const css = ((v.codeSyntax && v.codeSyntax.WEB) || '').match(/--[\w-]+/)[0];
  for (const m of c.modes) out.push([css, c.name[0], m.name, v.resolvedType[0], fmt(resolver(v, m.name), v.resolvedType)]); }
const porPagina = {};
for (const pg of figma.root.children) {
  if (pg.name === 'Referencias') continue;
  await figma.setCurrentPageAsync(pg);
  const ok = arr => !Array.isArray(arr) || arr.every(p => p.type !== 'SOLID' || p.visible === false || (p.boundVariables && p.boundVariables.color));
  porPagina[pg.name] = pg.findAll(x => 'fills' in x && (!ok(x.fills) || !ok(x.strokes))).length;
}
return JSON.stringify({ total: out.length, porPagina, parte: out.slice(0, 175) });
