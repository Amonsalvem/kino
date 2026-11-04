// Segunda auditoría (solo lectura): tamaños dentro del auto-layout.
// - texto de ancho fijo dentro de un padre vertical que no abraza su contenido (debería llenar);
// - frames de ancho fijo dentro de un padre vertical (deberían llenar);
// - filas horizontales con tarjetas de alto distinto (deberían estirarse al alto de la fila);
// - marcos de primer nivel que se solapan en el lienzo.
const PAGINA = '__PAGINA__';
const p = await figma.getNodeByIdAsync(PAGINA); await figma.setCurrentPageAsync(p);
const enInst = n => { let q = n.parent; while (q && q.type !== 'PAGE') { if (q.type === 'INSTANCE' || q.type === 'COMPONENT' || q.type === 'COMPONENT_SET') return true; q = q.parent; } return false; };
let txtFijo = 0, frameFijo = 0; const filas = [];
for (const f of p.findAllWithCriteria({ types: ['FRAME'] })) {
  if (enInst(f) || f.layoutMode === 'NONE') continue;
  const kids = f.children.filter(c => c.visible !== false && c.layoutPositioning !== 'ABSOLUTE');
  if (f.layoutMode === 'VERTICAL' && f.layoutSizingHorizontal !== 'HUG') for (const c of kids) {
    if (c.layoutSizingHorizontal !== 'FIXED') continue;
    if (c.type === 'TEXT') txtFijo++; else if (c.type === 'FRAME' && c.layoutMode !== 'NONE') frameFijo++;
  }
  if (f.layoutMode === 'HORIZONTAL' && kids.length >= 2 && kids.every(c => c.type === 'FRAME')) {
    const hs = kids.map(c => Math.round(c.height)); if (Math.max(...hs) - Math.min(...hs) > 2 && f.layoutWrap !== 'WRAP') filas.push(`${f.id} ${f.name} [${hs.join(',')}]`);
  }
}
const tops = p.children.filter(n => n.visible !== false).map(n => ({ id: n.id, n: n.name, x: Math.round(n.x), y: Math.round(n.y), w: Math.round(n.width), h: Math.round(n.height) }));
const solapes = [];
for (let i = 0; i < tops.length; i++) for (let j = i + 1; j < tops.length; j++) { const a = tops[i], b = tops[j]; if (a.x < b.x + b.w && b.x < a.x + a.w && a.y < b.y + b.h && b.y < a.y + a.h) solapes.push(a.n + ' × ' + b.n); }
return { pagina: p.name, txtFijo, frameFijo, filasDesiguales: filas.slice(0, 12), nFilas: filas.length, tops, solapes };
