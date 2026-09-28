// Kino · App · auditoría de reglas de marca y producto en una página de pantallas (solo lectura). Versión 1.2 · 28 sep 2026.
// Se corre con use_figma, una llamada por página, reemplazando __PAGINA__ por el id de la página.
// Complementa branding/sistema/v3/figma/js/p5-verificar-layout.js (auto-layout, espacios, desbordes), que se corre también.
// Mismo contrato que los scripts p5: await de nivel superior y `return` del resultado. Salida corta (< 20 kB).
// 1.2: entra en las secciones de Figma y falla si no encuentra pantallas; el arco ya no se exime por el nombre de la pantalla;
// revisa qué dice cada botón verde; revisa el marco de la pantalla y su modo; salta lo oculto; acepta variantes de ancho.
const PAGINA = '__PAGINA__';
const p = await figma.getNodeByIdAsync(PAGINA); await figma.setCurrentPageAsync(p);

// <ID> · <Pantalla> · <Estado> · [<ancho> · ]<Oscuro|Claro>. El ancho solo en variantes de reflujo (320, 430).
const RX_MARCO = /^([RVPAS](?:-[A-Z])?-\d{2}) · .+ · (?:(\d{3,4}) · )?(Oscuro|Claro)$/;
const NO_PANTALLA = /^Ficha · |^Nota · |^Sección/;
const VERDE_OK = /^(Crear Pase|Crear otro Pase|Enviando…)$/; // Únicos textos con accion/fondo (D-UX-02); «Enviando…» es el estado de carga del mismo botón. Extender, Entrar y Guardar límites son secundarios.
const ES_PASE = /Ventana del QR|Pase vivo|Imagen del Pase|Portal/i; // Lo único que lleva arco (X1, X8).
const SUPERFICIE_PASE = /^V-[LID]-/; // Pase vivo, imagen y PDF: la pantalla entera es un Pase.
const EVITAR = /\b(permiso|permisos|invitad[oa]s?|acceso concedido|permitido|empleada|guardia|celador|contraseñas?|seguridad total|100 ?% segur|arcana|marca blanca|pendiente de aprobación|aprobad[oa]s?|autorizad[oa]s?|usuario visitante)\b|¡|!/i;
const HORA_MAL = /\b\d{1,2}(:\d{2})?\s?(am|pm|AM|PM)\b|\bp\.m\.|\ba\.m\.|\d{1,2}:\d{2}\s?-\s?\d{1,2}:\d{2}\s?(a|p)\./; // bien: «2:00 p. m.», «de 2:00 a 6:00 p. m.»
const PLACA = /\b[A-Z]{3}[- \u00A0]?\d{2}[0-9A-Z]\b/g;
const PLACA_BIEN = /^[A-Z]{3}[ \u00A0]\d{2}[0-9A-Z]$/; // El espacio puede ser de no separación: la placa no se parte en dos líneas.
const DATO_PERSONAL = /c[ée]dula|\bC\.?C\.?\s?\d|\b\d{1,3}(\.\d{3}){2,3}\b|\b3\d{2} \d{3} \d{4}\b|@/i;

const varCache = new Map();
async function nombreVar(id) { if (!varCache.has(id)) { const v = await figma.variables.getVariableByIdAsync(id); varCache.set(id, v ? v.name : '?'); } return varCache.get(id); }
async function nombreComp(inst) { const m = await inst.getMainComponentAsync(); if (!m) return ''; return m.parent && m.parent.type === 'COMPONENT_SET' ? m.parent.name : m.name; }
const dentroDe = (n, rx, tope) => { let q = n.parent; while (q && q !== tope && q.type !== 'PAGE') { if (rx.test(q.name)) return true; q = q.parent; } return false; };
const dentroInst = n => { let q = n.parent; while (q && q.type !== 'PAGE') { if (q.type === 'INSTANCE') return true; q = q.parent; } return false; };
const oculto = (n, tope) => { let q = n; while (q && q !== tope) { if (q.visible === false) return true; q = q.parent; } return false; };
// Mismo filtro de ilustraciones que p5-verificar-layout.js.
const RX_ILUS = /QR|Aurora|Células|Tejido|Retícula|Tamaños|Íconos de app|Gota|Bloque|Símbolo|Vector|Mapa|Curva|Resplandor|Imagen del Pase|Ilustración/i;
const ilus = n => { let q = n; while (q && q.type !== 'PAGE') { if (/^(Icono|Logo)\//.test(q.name) || RX_ILUS.test(q.name)) return true; q = q.parent; } return false; };

// Pantallas y fichas: en la página o dentro de secciones (a cualquier profundidad de secciones).
const pantallas = [], fichas = new Set(), otros = [];
(function recorrer(nodos) {
  for (const n of nodos) {
    if (n.type === 'SECTION') { recorrer(n.children); continue; }
    if (n.type !== 'FRAME') continue;
    if (/^Ficha · /.test(n.name)) { fichas.add(n.name.slice('Ficha · '.length).split(' · ')[0]); continue; }
    if (NO_PANTALLA.test(n.name)) continue;
    if (RX_MARCO.test(n.name)) pantallas.push(n); else otros.push(n.name);
  }
})(p.children);

const r = { marcos: 0, nombreMal: otros, sinFicha: [], sinModo: [], pinturaSuelta: [], textoSinEstilo: [], verdes: [], verdeMal: [], arco: [], evitar: [], hora: [], placa: [], boton: [], tactil: [], datoPersonal: [] };

for (const m of pantallas) {
  const [, id, , ] = m.name.match(RX_MARCO);
  r.marcos++;
  if (!fichas.has(id) && !m.findOne(n => n.name.startsWith('Ficha · '))) r.sinFicha.push(id);
  if (!m.explicitVariableModes || !Object.keys(m.explicitVariableModes).length) r.sinModo.push(m.name);
  const superficie = id[0];
  let verdes = 0;

  for (const n of [m, ...m.findAll(() => true)]) {
    if (oculto(n, m.parent)) continue;
    const enInst = dentroInst(n);
    // Pinturas sin variable (fuera de instancias de librería e ilustraciones). Incluye el fondo del marco de la pantalla.
    if (!enInst && !ilus(n) && n.type !== 'INSTANCE') {
      for (const prop of ['fills', 'strokes']) {
        const ps = n[prop]; if (!Array.isArray(ps)) continue;
        ps.forEach((pt, i) => { if (pt.visible !== false && pt.type === 'SOLID') {
          const bv = n.boundVariables && n.boundVariables[prop] && n.boundVariables[prop][i];
          const estilo = prop === 'fills' ? n.fillStyleId : n.strokeStyleId;
          if (!bv && !estilo) r.pinturaSuelta.push(`${id} ${n.name} ${prop}`);
        } });
      }
    }
    // Verde de acción: cada Botón de acción cuenta y su texto debe otorgar un Pase. Un relleno suelto en accion/fondo también cuenta.
    if (n.type === 'INSTANCE') {
      const c = await nombreComp(n);
      const t = /Botón/i.test(c) ? n.findOne(x => x.type === 'TEXT' && x.visible !== false) : null;
      if (/Botón de acción/i.test(c)) { verdes++; if (!t || !VERDE_OK.test(t.characters.trim())) r.verdeMal.push(`${id} «${t ? t.characters : '?'}»`); }
      if (superficie === 'R' && /Botón|Campo|Selector|Chip de filtro/i.test(c) && Math.min(n.height, n.width) < 48) r.tactil.push(`${id} ${c} ${Math.round(n.width)}×${Math.round(n.height)}`);
      if (t && t.characters.trim().split(/\s+/).length > 3) r.boton.push(`${id} «${t.characters}»`);
    } else if (!enInst && Array.isArray(n.fills)) {
      const bv = n.boundVariables && n.boundVariables.fills;
      if (bv) for (const a of bv) if (a && /accion\/fondo/.test(await nombreVar(a.id))) { verdes++; r.verdeMal.push(`${id} relleno suelto en ${n.name}: usa la instancia de Botón de acción`); }
    }
    // Arco (radio pleno arriba, no abajo) solo en lo que es un Pase. Se exime por el nombre del nodo o de un grupo interno, nunca por el de la pantalla.
    if (!enInst && n !== m && 'topLeftRadius' in n && n.topLeftRadius >= 999 && n.topRightRadius >= 999 && n.bottomLeftRadius < 999
        && !SUPERFICIE_PASE.test(id) && !ES_PASE.test(n.name) && !dentroDe(n, ES_PASE, m)) r.arco.push(`${id} ${n.name}`);
    // Texto
    if (n.type === 'TEXT') {
      const s = n.characters;
      if (!enInst && !n.textStyleId && !(n.boundVariables && n.boundVariables.fontSize)) r.textoSinEstilo.push(`${id} «${s.slice(0, 30)}»`);
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
const alerta = r.marcos === 0 ? 'Sin pantallas: ningún marco con el nombre <ID> · <Pantalla> · <Estado> · <Oscuro|Claro>. La auditoría no revisó nada; no cuenta como aprobada.' : undefined;
return { pagina: p.name, alerta, totales: cuenta(r), ejemplos: Object.fromEntries(Object.entries(r).filter(([, v]) => Array.isArray(v) && v.length).map(([k, v]) => [k, v.slice(0, 5)])) };
