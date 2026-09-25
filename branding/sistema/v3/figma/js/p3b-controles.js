const p = await pagina('22:64');
for (const n of ['Controles']) { const f = p.children.find(x => x.name === n); if (f) f.remove(); }
// Estilo de texto para controles: Archivo Bold al tamaño texto/0.
let est = TS['Control/botón'];
if (!est) { est = figma.createTextStyle(); est.name = 'Control/botón'; }
await figma.loadFontAsync({ family: 'Archivo', style: 'Bold' });
est.fontName = { family: 'Archivo', style: 'Bold' }; est.setBoundVariable('fontSize', V('Tipografía', 'texto/0')); est.setBoundVariable('fontFamily', V('Tipografía', 'fuente/texto'));
est.lineHeight = { unit: 'PERCENT', value: 120 }; est.description = 'Texto de botones y selectores. Archivo Bold, tamaño texto/0.'; TS['Control/botón'] = est;
const cont = auto('VERTICAL', 'Controles', '2xl', 'xl', 'xl'); p.appendChild(cont); fill(cont, C('superficie/base')); modoColor(cont, 'Oscuro'); radio(cont, 'radio/l');
const logo = p.children.find(n => n.name === 'Logo'); cont.x = 0; cont.y = logo.y + logo.height + 48;
const grilla = (set, cols) => { set.layoutMode = 'HORIZONTAL'; set.layoutWrap = 'WRAP'; gap(set, 'l'); set.setBoundVariable('counterAxisSpacing', E('espacio/l')); pad(set, 'l', 'l'); set.fills = []; borde(set, C('borde/tenue'), 'linea/fino', [4, 4]); radio(set, 'radio/l'); set.resize(cols, 100); set.primaryAxisSizingMode = 'FIXED'; set.counterAxisSizingMode = 'AUTO'; };
const conTexto = (set, nombre, def) => { const k = set.addComponentProperty(nombre, 'TEXT', def); for (const c of set.children) { const t = c.findOne(x => x.type === 'TEXT' && x.name === nombre); if (t) t.componentPropertyReferences = { characters: k }; } };
const bloque = async (titulo, desc) => { const s = auto('VERTICAL', titulo, 's'); cont.appendChild(s); s.appendChild(await txt(titulo, 'Título/titulo-2', C('texto/primario'))); s.appendChild(await txt(desc, 'Texto/cuerpo-s', C('texto/secundario'), 900)); return s; };
// ── Botón de acción ──
const botones = [];
for (const e of ['Reposo', 'Hover', 'Foco', 'Deshabilitado', 'Carga']) {
  const b = figma.createComponent(); b.name = 'Estado=' + e; b.layoutMode = 'HORIZONTAL'; b.primaryAxisSizingMode = 'AUTO'; b.counterAxisSizingMode = 'AUTO';
  b.counterAxisAlignItems = 'CENTER'; pad(b, 's', 'l'); gap(b, 'xs'); radio(b, 'forma/radio/control'); b.setBoundVariable('minHeight', E('espacio/2xl'));
  fill(b, C(e === 'Hover' ? 'accion/fondo-activo' : e === 'Deshabilitado' ? 'superficie/membrana' : 'accion/fondo'));
  if (e === 'Foco') borde(b, C('borde/foco'), 'linea/foco');
  if (e === 'Carga') { const r = figma.createEllipse(); r.name = 'Carga'; r.resize(16, 16); r.fills = []; borde(r, C('accion/texto'), 'linea/foco'); r.arcData = { startingAngle: 0, endingAngle: 4.7, innerRadius: 0.8 }; fill(r, C('accion/texto')); r.strokes = []; b.appendChild(r); }
  const t = await txt(e === 'Carga' ? 'Enviando…' : 'Crear Pase', 'Control/botón', C(e === 'Deshabilitado' ? 'texto/secundario' : 'accion/texto')); t.name = 'Texto'; b.appendChild(t);
  botones.push(b);
}
const sb = figma.combineAsVariants(botones, cont); sb.name = 'Botón de acción'; grilla(sb, 1124); conTexto(sb, 'Texto', 'Crear Pase');
sb.description = 'El botón que crea o entrega un Pase. Uno por pantalla. Fondo accion/fondo (#00D595 en oscuro, X4). Texto de 3 palabras o menos.';
const s1 = await bloque('Botón de acción', 'Crea o entrega un Pase. Es el único verde de la pantalla. El estado Error no existe en un botón.'); s1.appendChild(sb);
// ── Botón secundario ──
const sec = [];
for (const e of ['Reposo', 'Hover', 'Foco', 'Deshabilitado']) {
  const b = figma.createComponent(); b.name = 'Estado=' + e; b.layoutMode = 'HORIZONTAL'; b.primaryAxisSizingMode = 'AUTO'; b.counterAxisSizingMode = 'AUTO'; b.counterAxisAlignItems = 'CENTER';
  pad(b, 's', 'l'); gap(b, 'xs'); radio(b, 'forma/radio/control'); b.setBoundVariable('minHeight', E('espacio/2xl'));
  fill(b, e === 'Hover' ? C('superficie/membrana') : null); borde(b, C(e === 'Foco' ? 'borde/foco' : 'borde/definido'), e === 'Foco' ? 'linea/foco' : 'linea/fino');
  if (e === 'Deshabilitado') b.opacity = 0.55;
  const t = await txt('Extender', 'Control/botón', C('texto/primario')); t.name = 'Texto'; b.appendChild(t); sec.push(b);
}
const ss = figma.combineAsVariants(sec, cont); ss.name = 'Botón secundario'; grilla(ss, 1124); conTexto(ss, 'Texto', 'Extender');
ss.description = 'Acciones que no otorgan: extender, revocar, cancelar, guardar límites.';
const s2 = await bloque('Botón secundario', 'Para lo que no crea un Pase. Nunca en verde.'); s2.appendChild(ss);
// ── Campo ──
const campos = [];
for (const e of ['Reposo', 'Hover', 'Foco', 'Deshabilitado', 'Error']) {
  const c = figma.createComponent(); c.name = 'Estado=' + e; c.layoutMode = 'VERTICAL'; c.primaryAxisSizingMode = 'AUTO'; c.counterAxisSizingMode = 'FIXED'; c.resize(280, 100); gap(c, '2xs'); c.fills = [];
  const et = await txt('WhatsApp de la visita', 'Texto/menor', C('texto/primario')); et.name = 'Etiqueta'; c.appendChild(et);
  const caja = figma.createAutoLayout('HORIZONTAL', { name: 'Caja' }); c.appendChild(caja); caja.layoutSizingHorizontal = 'FILL'; caja.counterAxisAlignItems = 'CENTER';
  pad(caja, 'xs', 's'); radio(caja, 'forma/radio/control'); caja.setBoundVariable('minHeight', E('espacio/2xl')); fill(caja, C(e === 'Deshabilitado' ? 'superficie/elevada' : 'superficie/base'));
  borde(caja, C(e === 'Foco' ? 'borde/foco' : e === 'Error' ? 'estado/rechazado/borde' : e === 'Hover' ? 'texto/secundario' : 'borde/definido'), e === 'Foco' ? 'linea/foco' : 'linea/fino');
  const val = await txt(e === 'Error' ? '300 555 014' : '300 555 0142', 'Dato/dato', C('texto/primario')); val.name = 'Valor'; caja.appendChild(val);
  if (e === 'Error') { const er = auto('HORIZONTAL', 'Error', null, '2xs', 'xs'); c.appendChild(er); er.layoutSizingHorizontal = 'FILL'; fill(er, C('estado/rechazado/fondo')); radio(er, 'forma/radio/chip');
    const m = await txt('Ese número tiene 9 cifras. Un celular en Colombia tiene 10.', 'Texto/menor', C('estado/rechazado/texto')); m.name = 'Ayuda'; er.appendChild(m); m.layoutSizingHorizontal = 'FILL'; }
  else { const a = await txt('Ahí le llega el Pase.', 'Texto/menor', C('texto/secundario')); a.name = 'Ayuda'; c.appendChild(a); a.layoutSizingHorizontal = 'FILL'; }
  if (e === 'Deshabilitado') c.opacity = 0.55;
  campos.push(c);
}
const sc = figma.combineAsVariants(campos, cont); sc.name = 'Campo'; grilla(sc, 1124); conTexto(sc, 'Etiqueta', 'WhatsApp de la visita'); conTexto(sc, 'Valor', '300 555 0142');
sc.description = 'Campo con etiqueta, caja y ayuda. El error dice qué pasó y qué hacer, debajo del campo.';
const s3 = await bloque('Campo', 'El error va en texto, debajo de la caja, con el fondo del evento Rechazado. El estado Carga no aplica.'); s3.appendChild(sc);
// ── Selector de tipo ──
const sels = [];
for (const e of ['Reposo', 'Hover', 'Foco', 'Deshabilitado']) for (const sel of ['Visita', 'Colaborador']) {
  const s = figma.createComponent(); s.name = `Estado=${e}, Selección=${sel}`; s.layoutMode = 'HORIZONTAL'; s.primaryAxisSizingMode = 'AUTO'; s.counterAxisSizingMode = 'AUTO';
  pad(s, '3xs', '3xs'); gap(s, '3xs'); radio(s, 'forma/radio/control'); fill(s, C('superficie/base')); borde(s, C(e === 'Foco' ? 'borde/foco' : 'borde/definido'), e === 'Foco' ? 'linea/foco' : 'linea/fino');
  for (const op of ['Visita', 'Colaborador']) {
    const o = auto('HORIZONTAL', op, null, 'xs', 'l'); s.appendChild(o); radio(o, 'forma/radio/chip'); o.counterAxisAlignItems = 'CENTER';
    const on = op === sel; fill(o, on ? C('superficie/inversa') : (e === 'Hover' ? C('superficie/membrana') : null));
    const t = await txt(op, 'Control/botón', C(on ? 'texto/inverso' : 'texto/primario')); o.appendChild(t);
  }
  if (e === 'Deshabilitado') s.opacity = 0.55;
  sels.push(s);
}
const sss = figma.combineAsVariants(sels, cont); sss.name = 'Selector de tipo'; grilla(sss, 1124);
sss.description = 'Visita y Colaborador con el mismo peso. Se mueve con las flechas del teclado.';
const s4 = await bloque('Selector de tipo', 'Visita y Colaborador pesan lo mismo: el colaborador es el ingreso más frecuente.'); s4.appendChild(sss);
return { contenedor: cont.id, sets: [sb.id, ss.id, sc.id, sss.id], variantes: [sb.children.length, ss.children.length, sc.children.length, sss.children.length] };
