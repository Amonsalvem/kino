// Kino · App · auditoría de reglas de marca y producto en una página de pantallas (solo lectura).
// Se corre con use_figma, una llamada por página, reemplazando __PAGINA__ por el id de la página.
// Complementa branding/sistema/v3/figma/js/p5-verificar-layout.js (auto-layout, espacios, desbordes), que se corre también.
// Mismo contrato que los scripts p5: await de nivel superior y `return` del resultado. Salida corta (< 20 kB).
const PAGINA = '__PAGINA__';
const p = await figma.getNodeByIdAsync(PAGINA); await figma.setCurrentPageAsync(p);

const RX_MARCO = /^([RVPAS](?:-[A-Z])?-\d{2}) · .+ · (Oscuro|Claro)$/;
const EVITAR = /\b(permiso|permisos|invitad[oa]s?|acceso concedido|permitido|empleada|guardia|celador|contraseña|seguridad total|100 ?% segur|arcana|marca blanca|pendiente de aprobación|aprobad[oa]|autorizad[oa]|usuario visitante)\b|¡|!/i;
const HORA_MAL = /\b\d{1,2}(:\d{2})?\s?(am|pm|AM|PM)\b|\bp\.m\.|\ba\.m\.|\d{1,2}:\d{2}\s?-\s?\d{1,2}:\d{2}\s?(a|p)\./; // bien: «2:00 p. m.», «de 2:00 a 6:00 p. m.»
const PLACA = /\b[A-Z]{3}[- ]?\d{2}[0-9A-Z]\b/g;
const PLACA_BIEN = /^[A-Z]{3} \d{2}[0-9A-Z]$/;
const DATO_PERSONAL = /c[ée]dula|\bC\.?C\.?\s?\d|\b\d{1,3}(\.\d{3}){2,3}\b|\b3\d{2} \d{3} \d{4}\b|@/i;

const varCache = new Map();
async function nombreVar(id) { if (!varCache.has(id)) { const v = await figma.variables.getVariableByIdAsync(id); varCache.set(id, v ? v.name : '?'); } return varCache.get(id); }
async function nombreComp(inst) { const m = await inst.getMainComponentAsync(); if (!m) return ''; return m.parent && m.parent.type === 'COMPONENT_SET' ? m.parent.name : m.name; }
const dentroDe = (n, rx) => { let q = n.parent; while (q && q.type !== 'PAGE') { if (rx.test(q.name)) return true; q = q.parent; } return false; };
const dentroInst = n => { let q = n.parent; while (q && q.type !== 'PAGE') { if (q.type === 'INSTANCE') return true; q = q.parent; } return false; };
const ilus = n => dentroDe(n, /QR|Aurora|Tejido|Imagen del Pase|Ilustración|Logo\/|Icono\//i) || /QR|Aurora/i.test(n.name);

const r = { marcos: 0, nombreMal: [], sinFicha: [], pinturaSuelta: [], textoSinEstilo: [], verdes: [], arco: [], evitar: [], hora: [], placa: [], boton: [], tactil: [], datoPersonal: [] };
const ids = new Set(p.children.map(n => n.name));

for (const m of p.children) {
  if (m.type !== 'FRAME' || /^Ficha · |^Nota · |^Sección/.test(m.name)) continue;
  const k = m.name.match(RX_MARCO);
  if (!k) { r.nombreMal.push(m.name); continue; }
  r.marcos++;
  const id = k[1];
  if (!ids.has('Ficha · ' + id) && !m.findOne(n => n.name.startsWith('Ficha · '))) r.sinFicha.push(id);
  const superficie = id[0];
  let verdes = 0;

  for (const n of m.findAll(() => true)) {
    if (n.visible === false) continue;
    // Pinturas sin variable (fuera de instancias de librería e ilustraciones)
    if (!dentroInst(n) && !ilus(n) && n.type !== 'INSTANCE') {
      for (const prop of ['fills', 'strokes']) {
        const ps = n[prop]; if (!Array.isArray(ps)) continue;
        ps.forEach((pt, i) => { if (pt.visible !== false && pt.type === 'SOLID') {
          const bv = n.boundVariables && n.boundVariables[prop] && n.boundVariables[prop][i];
          const estilo = prop === 'fills' ? n.fillStyleId : n.strokeStyleId;
          if (!bv && !estilo) r.pinturaSuelta.push(`${id} ${n.name} ${prop}`);
        } });
      }
    }
    // Verde de acción: instancias de Botón de acción y rellenos ligados a accion/fondo
    if (n.type === 'INSTANCE') {
      const c = await nombreComp(n);
      if (/Botón de acción/i.test(c)) verdes++;
      if (superficie === 'R' && /Botón|Campo|Selector|Chip de filtro|Barra inferior/i.test(c) && n.height < 48 && !/Barra inferior/i.test(c)) r.tactil.push(`${id} ${c} ${Math.round(n.height)}px`);
      if (/Botón/i.test(c)) { const t = n.findOne(x => x.type === 'TEXT'); if (t && t.characters.trim().split(/\s+/).length > 3) r.boton.push(`${id} «${t.characters}»`); }
    } else if (!dentroInst(n) && Array.isArray(n.fills)) {
      const bv = n.boundVariables && n.boundVariables.fills;
      if (bv) for (const a of bv) if (a && /accion\/fondo/.test(await nombreVar(a.id))) verdes++;
    }
    // Arco (radio pleno arriba) solo en lo que es un Pase
    if ('topLeftRadius' in n && n.topLeftRadius >= 999 && n.topRightRadius >= 999 && n.bottomLeftRadius < 999 && !/Pase/i.test(n.name) && !dentroDe(n, /Pase/i)) r.arco.push(`${id} ${n.name}`);
    // Texto
    if (n.type === 'TEXT') {
      const s = n.characters;
      if (!dentroInst(n) && !n.textStyleId && !(n.boundVariables && n.boundVariables.fontSize)) r.textoSinEstilo.push(`${id} «${s.slice(0, 30)}»`);
      if (!/^Ficha · |Así no/.test(n.name) && !dentroDe(n, /Así no|^Ficha · /) && EVITAR.test(s)) r.evitar.push(`${id} «${s.slice(0, 50)}»`);
      if (HORA_MAL.test(s) && !dentroDe(n, /Así no/)) r.hora.push(`${id} «${s.slice(0, 40)}»`);
      const placas = s.match(PLACA) || [];
      const fam = n.fontName === figma.mixed ? 'mixta' : n.fontName.family;
      for (const pl of placas) if (!PLACA_BIEN.test(pl) || (s.trim() === pl && fam !== 'JetBrains Mono')) r.placa.push(`${id} «${pl}» ${fam}`);
      if ((superficie === 'P' || superficie === 'V') && DATO_PERSONAL.test(s) && !dentroDe(n, /^Ficha · /)) r.datoPersonal.push(`${id} «${s.slice(0, 40)}»`);
    }
  }
  if (verdes > 1) r.verdes.push(`${id}: ${verdes}`);
}

const cuenta = o => Object.fromEntries(Object.entries(o).map(([k, v]) => [k, Array.isArray(v) ? v.length : v]));
return { pagina: p.name, totales: cuenta(r), ejemplos: Object.fromEntries(Object.entries(r).filter(([, v]) => Array.isArray(v) && v.length).map(([k, v]) => [k, v.slice(0, 5)])) };
