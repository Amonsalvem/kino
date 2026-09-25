// Normaliza el auto-layout y el espaciado de una página. Se puede volver a correr sin daño.
// 1. Texto que envuelve (alto automático) dentro de un padre vertical de ancho fijo o que llena:
//    pasa a «llenar contenedor», con ancho máximo igual al que tenía (conserva la medida de lectura).
// 2. Filas horizontales de tarjetas con alto desigual: la más alta abraza su contenido y las demás llenan ese alto.
// 3. Espacio, padding y separación de filas sin variable: se ligan al paso de la escala con el mismo valor
//    (80 pasa a 72, el paso 3xl que usan las demás páginas).
// No toca instancias por dentro ni ilustraciones (íconos, logo, QR, aurora, retículas, tamaños).
const PAGINA = '__PAGINA__';
const p = await figma.getNodeByIdAsync(PAGINA); await figma.setCurrentPageAsync(p);
const cols = await figma.variables.getLocalVariableCollectionsAsync();
const col = cols.find(c => c.name === 'Espacio y radio');
const vars = (await figma.variables.getLocalVariablesAsync('FLOAT')).filter(v => v.variableCollectionId === col.id && v.name.startsWith('espacio/'));
const modo = col.modes[0].modeId;
const porValor = new Map(vars.map(v => [v.valuesByMode[modo], v]));
const ajustar = x => { const r = Math.round(x); if (porValor.has(r)) return r; if (r === 80) return 72; return [...porValor.keys()].reduce((a, b) => Math.abs(b - r) < Math.abs(a - r) ? b : a); };
const dentroInst = n => { let q = n.parent; while (q && q.type !== 'PAGE') { if (q.type === 'INSTANCE') return true; q = q.parent; } return false; };
const ilus = n => { let q = n; while (q && q.type !== 'PAGE') { if (/^(Icono|Logo)\//.test(q.name) || /QR|Aurora|Células|Tejido|Retícula|Tamaños|Íconos de app|Gota|Bloque/i.test(q.name)) return true; q = q.parent; } return false; };
const fuentes = new Set();
const cargar = async t => { for (const f of t.getRangeAllFontNames(0, t.characters.length)) { const k = f.family + '|' + f.style; if (!fuentes.has(k)) { await figma.loadFontAsync(f); fuentes.add(k); } } };
const res = { textos: 0, filas: 0, ligados: 0, ajustados: [], errores: [] };
const marcos = p.findAllWithCriteria({ types: ['FRAME', 'COMPONENT'] }).filter(f => !dentroInst(f) && f.layoutMode !== 'NONE');
for (const f of marcos) {
  try {
    // 3. espacios
    for (const k of ['itemSpacing', 'paddingTop', 'paddingBottom', 'paddingLeft', 'paddingRight', 'counterAxisSpacing']) {
      if (k === 'counterAxisSpacing' && f.layoutWrap !== 'WRAP') continue;
      const v = f[k]; if (!v || (f.boundVariables && f.boundVariables[k])) continue;
      const a = ajustar(v); if (a !== Math.round(v)) res.ajustados.push(`${f.name} ${k} ${Math.round(v * 10) / 10}→${a}`);
      f.setBoundVariable(k, porValor.get(a)); res.ligados++;
    }
    if (ilus(f)) continue;
    const kids = f.children.filter(c => c.visible !== false && c.layoutPositioning !== 'ABSOLUTE');
    // 1. textos
    if (f.layoutMode === 'VERTICAL' && f.layoutSizingHorizontal !== 'HUG') {
      const util = f.width - f.paddingLeft - f.paddingRight;
      for (const t of kids) {
        if (t.type !== 'TEXT' || t.layoutSizingHorizontal !== 'FIXED' || t.textAutoResize !== 'HEIGHT') continue;
        await cargar(t);
        const w = t.width; t.layoutSizingHorizontal = 'FILL';
        if (w < util - 1) t.maxWidth = Math.round(w);
        res.textos++;
      }
    }
    // 2. filas de tarjetas
    if (f.layoutMode === 'HORIZONTAL' && f.layoutWrap !== 'WRAP' && kids.length >= 2 && kids.every(c => (c.type === 'FRAME' || c.type === 'COMPONENT') && c.layoutMode !== 'NONE')) {
      const hs = kids.map(c => c.height);
      if (Math.max(...hs) - Math.min(...hs) > 2) {
        const alta = kids[hs.indexOf(Math.max(...hs))];
        f.layoutSizingVertical = 'HUG'; alta.layoutSizingVertical = 'HUG';
        for (const c of kids) if (c !== alta) c.layoutSizingVertical = 'FILL';
        res.filas++;
      }
    }
  } catch (e) { res.errores.push(`${f.id} ${f.name}: ${String(e).slice(0, 120)}`); }
}
return { pagina: p.name, ...res, ajustados: res.ajustados.slice(0, 20), errores: res.errores.slice(0, 10) };
