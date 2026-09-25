// Auditoría de auto-layout y espaciado de una página (solo lectura). Reemplazar PAGINA por el id.
// Marca: frames con 2+ hijos sin auto-layout; gap, padding y separación de filas sin variable o fuera de la escala;
// hijos que se salen del contenedor; texto con alto fijo que se corta; hijos en posición absoluta dentro de auto-layout.
const PAGINA = '__PAGINA__';
const ESCALA = [0, 2, 4, 8, 12, 16, 24, 32, 48, 72, 112];
const p = await figma.getNodeByIdAsync(PAGINA); await figma.setCurrentPageAsync(p);
const esIlustracion = n => { let q = n; while (q && q.type !== 'PAGE') { if (/^(Icono|Logo)\//.test(q.name) || /QR|Aurora|Células|Ilustr|Vector|Símbolo|Gota|Bloque|Mapa|Diagrama|Curva/i.test(q.name)) return true; q = q.parent; } return false; };
const enInstancia = n => { let q = n.parent; while (q && q.type !== 'PAGE') { if (q.type === 'INSTANCE') return true; q = q.parent; } return false; };
const sinAuto = [], sueltos = [], fuera = [], cortes = [], absolutos = [];
const props = ['itemSpacing', 'paddingTop', 'paddingBottom', 'paddingLeft', 'paddingRight', 'counterAxisSpacing'];
const marcos = p.findAllWithCriteria({ types: ['FRAME', 'COMPONENT', 'COMPONENT_SET'] });
for (const f of marcos) {
  if (enInstancia(f) || esIlustracion(f)) continue;
  const hijos = f.children.filter(c => c.visible !== false);
  if (f.layoutMode === 'NONE') {
    if (hijos.length >= 2 && hijos.some(c => c.type === 'TEXT' || c.type === 'FRAME' || c.type === 'INSTANCE')) sinAuto.push(`${f.id} ${f.name} (${hijos.length})`);
  } else {
    for (const k of props) {
      if (k === 'counterAxisSpacing' && f.layoutWrap !== 'WRAP') continue;
      const v = f[k]; if (v == null || v === 0) continue;
      const lig = f.boundVariables && f.boundVariables[k];
      if (!lig) sueltos.push(`${f.id} ${f.name} ${k}=${Math.round(v * 10) / 10}${ESCALA.includes(Math.round(v)) ? '' : ' (fuera de escala)'}`);
    }
    for (const c of hijos) if (c.layoutPositioning === 'ABSOLUTE') absolutos.push(`${c.id} ${c.name} en ${f.name}`);
  }
  if (f.clipsContent !== false || f.layoutMode === 'NONE') for (const c of hijos) {
    if (c.layoutPositioning === 'ABSOLUTE' && esIlustracion(c)) continue;
    if (c.x < -1 || c.y < -1 || c.x + c.width > f.width + 1 || c.y + c.height > f.height + 1) fuera.push(`${c.id} ${c.name} en ${f.id} ${f.name}`);
  }
}
for (const t of p.findAllWithCriteria({ types: ['TEXT'] })) {
  if (enInstancia(t)) continue;
  if (t.textAutoResize === 'NONE' || t.textTruncation === 'ENDING') cortes.push(`${t.id} «${t.characters.slice(0, 40)}» ${t.textAutoResize}`);
  else if (t.width < 4) cortes.push(`${t.id} «${t.characters.slice(0, 40)}» ancho ${Math.round(t.width)}`);
}
const top = n => n.slice(0, 25);
return { pagina: p.name, marcos: marcos.length, sinAutoLayout: sinAuto.length, sueltos: sueltos.length, fuera: fuera.length, cortes: cortes.length, absolutos: absolutos.length,
  ej: { sinAuto: top(sinAuto), sueltos: top(sueltos), fuera: top(fuera), cortes: top(cortes), absolutos: top(absolutos) } };
