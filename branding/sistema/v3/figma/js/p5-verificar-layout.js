// Verificación final de una página (solo lectura): une p5-auditoria-layout.js y p5-auditoria-tamanos.js.
const PAGINA = '__PAGINA__';
const p = await figma.getNodeByIdAsync(PAGINA); await figma.setCurrentPageAsync(p);
const dentroInst = n => { let q = n.parent; while (q && q.type !== 'PAGE') { if (q.type === 'INSTANCE') return true; q = q.parent; } return false; };
const ilus = n => { let q = n; while (q && q.type !== 'PAGE') { if (/^(Icono|Logo)\//.test(q.name) || /QR|Aurora|Células|Tejido|Retícula|Tamaños|Íconos de app|Gota|Bloque|Símbolo|Vector|Mapa|Curva|Resplandor/i.test(q.name)) return true; q = q.parent; } return false; };
const r = { sinAuto: [], sueltos: [], fuera: [], txtFijo: [], filas: [] };
for (const f of p.findAllWithCriteria({ types: ['FRAME', 'COMPONENT', 'COMPONENT_SET'] })) {
  if (dentroInst(f) || ilus(f)) continue;
  const kids = f.children.filter(c => c.visible !== false);
  if (f.layoutMode === 'NONE') { if (kids.length >= 2 && kids.some(c => ['TEXT', 'FRAME', 'INSTANCE'].includes(c.type))) r.sinAuto.push(f.id + ' ' + f.name); }
  else {
    for (const k of ['itemSpacing', 'paddingTop', 'paddingBottom', 'paddingLeft', 'paddingRight', 'counterAxisSpacing']) {
      if (k === 'counterAxisSpacing' && f.layoutWrap !== 'WRAP') continue;
      if (f[k] && !(f.boundVariables && f.boundVariables[k])) r.sueltos.push(`${f.id} ${f.name} ${k}`);
    }
    if (f.type === 'FRAME' && f.layoutMode === 'VERTICAL' && f.layoutSizingHorizontal !== 'HUG')
      for (const t of kids) if (t.type === 'TEXT' && t.layoutSizingHorizontal === 'FIXED' && t.textAutoResize === 'HEIGHT') r.txtFijo.push(t.id);
    const fk = kids.filter(c => c.layoutPositioning !== 'ABSOLUTE');
    if (f.type === 'FRAME' && f.layoutMode === 'HORIZONTAL' && f.layoutWrap !== 'WRAP' && fk.length >= 2 && fk.every(c => c.type === 'FRAME' && c.layoutMode !== 'NONE')) {
      const hs = fk.map(c => c.height); if (Math.max(...hs) - Math.min(...hs) > 2) r.filas.push(f.id + ' ' + f.name);
    }
  }
  if (f.clipsContent !== false || f.layoutMode === 'NONE') for (const c of kids) {
    if (ilus(c)) continue;
    if (c.x < -1 || c.y < -1 || c.x + c.width > f.width + 1 || c.y + c.height > f.height + 1) r.fuera.push(`${c.id} ${c.name} en ${f.name}`);
  }
}
const tops = p.children.filter(n => n.visible !== false); let solapes = 0;
for (let i = 0; i < tops.length; i++) for (let j = i + 1; j < tops.length; j++) { const a = tops[i], b = tops[j]; if (a.x < b.x + b.width && b.x < a.x + a.width && a.y < b.y + b.height && b.y < a.y + a.height) solapes++; }
return { pagina: p.name, sinAuto: r.sinAuto.length, sueltos: r.sueltos.length, fuera: r.fuera.length, txtFijo: r.txtFijo.length, filas: r.filas.length, solapes, ej: [...r.sinAuto, ...r.sueltos, ...r.fuera, ...r.filas].slice(0, 8) };
