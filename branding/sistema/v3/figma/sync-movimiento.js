
const COL = "Movimiento", MODOS = ["Valor"], VARS = [["duracion/instante","FLOAT",{"Valor":{"num":120}},"Hover, foco, cambio de color de un control."],["duracion/corto","FLOAT",{"Valor":{"num":240}},"Aparición de un chip o un estado."],["duracion/crecer","FLOAT",{"Valor":{"num":420}},"Lo que aparece: una tarjeta, un pase nuevo, la costura de la cortina."],["duracion/tarjeta","FLOAT",{"Valor":{"num":820}},"Entrada de un ítem de lámina (subida de 26 px, escala .965)."],["duracion/decaer","FLOAT",{"Valor":{"num":900}},"Lo que caduca. Más lento que revocar: caducar y ser revocado no se mueven igual."],["duracion/trazo","FLOAT",{"Valor":{"num":950}},"Dibujo de un diagrama de izquierda a derecha."],["duracion/cortina","FLOAT",{"Valor":{"num":1600}},"Apertura de las hojas de la cortina de entrada."],["duracion/latir","FLOAT",{"Valor":{"num":1800}},"Un ciclo del punto del estado vigente. Máximo tres ciclos (WCAG 2.2.2)."],["escalonado/tarjetas","FLOAT",{"Valor":{"num":90}},""],["escalonado/filas","FLOAT",{"Valor":{"num":55}},""],["curva/crecer","STRING",{"Valor":{"str":"cubic-bezier(0.16, 0.84, 0.3, 1)"}},"Sale rápido y se asienta: algo nuevo llega."],["curva/decaer","STRING",{"Valor":{"str":"cubic-bezier(0.62, 0.03, 0.86, 0.34)"}},"Empieza lento y cae: algo se apaga solo."],["curva/latir","STRING",{"Valor":{"str":"cubic-bezier(0.45, 0, 0.55, 1)"}},"Simétrica: respiración de lo que está vivo."],["curva/cortina","STRING",{"Valor":{"str":"cubic-bezier(0.76, 0, 0.24, 1)"}},"Apertura con peso: el telón."],["curva/revocar","STRING",{"Valor":{"str":"cubic-bezier(0.4, 0, 1, 1)"}},"Salida seca: alguien cortó el pase."],["curva/salir","STRING",{"Valor":{"str":"cubic-bezier(0.3, 0, 0.8, 0.15)"}},"Lo que se va: arranca lento y acelera fuera. No es revocar: nadie cortó nada."],["distancia/subida","FLOAT",{"Valor":{"num":26}},"Recorrido vertical de entrada de una tarjeta."],["distancia/desenfoque","FLOAT",{"Valor":{"num":6}},"Desenfoque inicial del texto suelto."],["resorte/tacto/rigidez","FLOAT",{"Valor":{"num":520}},""],["resorte/tacto/amortiguacion","FLOAT",{"Valor":{"num":34}},""],["resorte/tacto/masa","FLOAT",{"Valor":{"num":1}},""],["resorte/hoja/rigidez","FLOAT",{"Valor":{"num":260}},""],["resorte/hoja/amortiguacion","FLOAT",{"Valor":{"num":30}},""],["resorte/hoja/masa","FLOAT",{"Valor":{"num":1}},""],["resorte/pase/rigidez","FLOAT",{"Valor":{"num":180}},""],["resorte/pase/amortiguacion","FLOAT",{"Valor":{"num":22}},""],["resorte/pase/masa","FLOAT",{"Valor":{"num":1}},""],["resorte/firme/rigidez","FLOAT",{"Valor":{"num":400}},""],["resorte/firme/amortiguacion","FLOAT",{"Valor":{"num":40}},""],["resorte/firme/masa","FLOAT",{"Valor":{"num":1}},""],["coreografia/cascada-maximo","FLOAT",{"Valor":{"num":8}},"Elementos que entran escalonados; del noveno en adelante entran con el octavo."],["coreografia/cascada-tope","FLOAT",{"Valor":{"num":520}},"El escalonado total nunca pasa de este tiempo, aunque haya muchos elementos."],["coreografia/salida-factor","FLOAT",{"Valor":{"num":0.6}},"Salir dura el 60 % de entrar: lo que se va no debe hacer esperar."],["latir/ciclos","FLOAT",{"Valor":{"num":3}},"Ciclos del punto vigente antes de quedar quieto (WCAG 2.2.2). Vuelve a latir cuando el Pase cambia."],["escala/presion","FLOAT",{"Valor":{"num":0.97}},"Escala de un control mientras se presiona."],["escala/entrada","FLOAT",{"Valor":{"num":0.965}},"Escala inicial de una tarjeta que aparece."],["profundidad/sustrato","FLOAT",{"Valor":{"num":0}},""],["profundidad/membrana","FLOAT",{"Valor":{"num":1}},""],["profundidad/pase","FLOAT",{"Valor":{"num":2}},""],["profundidad/hoja","FLOAT",{"Valor":{"num":3}},""],["profundidad/aviso","FLOAT",{"Valor":{"num":4}},""],["aviso/visible","FLOAT",{"Valor":{"num":5400}},"Tiempo que un aviso queda en pantalla: tres ciclos de latir."],["aparecer/duracion","FLOAT",{"Valor":{"alias":"duracion/tarjeta","coleccion":"Movimiento"}},""],["aparecer/curva","STRING",{"Valor":{"alias":"curva/crecer","coleccion":"Movimiento"}},""],["aparecer/escalonado","FLOAT",{"Valor":{"alias":"escalonado/tarjetas","coleccion":"Movimiento"}},""],["responder/duracion","FLOAT",{"Valor":{"alias":"duracion/corto","coleccion":"Movimiento"}},""],["responder/curva","STRING",{"Valor":{"alias":"curva/crecer","coleccion":"Movimiento"}},""],["caducar/duracion","FLOAT",{"Valor":{"alias":"duracion/decaer","coleccion":"Movimiento"}},""],["caducar/curva","STRING",{"Valor":{"alias":"curva/decaer","coleccion":"Movimiento"}},""],["revocar/duracion","FLOAT",{"Valor":{"alias":"duracion/corto","coleccion":"Movimiento"}},""],["revocar/curva","STRING",{"Valor":{"alias":"curva/revocar","coleccion":"Movimiento"}},""],["latir/duracion","FLOAT",{"Valor":{"alias":"duracion/latir","coleccion":"Movimiento"}},""],["latir/curva","STRING",{"Valor":{"alias":"curva/latir","coleccion":"Movimiento"}},""],["salir/curva","STRING",{"Valor":{"alias":"curva/salir","coleccion":"Movimiento"}},""]];
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
