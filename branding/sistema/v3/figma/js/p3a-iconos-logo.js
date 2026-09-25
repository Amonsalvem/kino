// Preludio común: variables, estilos y ayudas para ligar todo a tokens (ningún valor suelto).
const cols = await figma.variables.getLocalVariableCollectionsAsync();
const COL = Object.fromEntries(cols.map(c => [c.name, c]));
const ALL = await figma.variables.getLocalVariablesAsync();
const V = (col, n) => { const v = ALL.find(x => x.variableCollectionId === COL[col].id && x.name === n); if (!v) throw new Error('falta variable ' + col + '/' + n); return v; };
const C = n => V('Color', n), E = n => V('Espacio y radio', n), P = n => V('Primitivos', 'color/' + n);
const pintura = v => figma.variables.setBoundVariableForPaint({ type: 'SOLID', color: { r: 0, g: 0, b: 0 } }, 'color', v);
const fill = (n, v) => { n.fills = v ? [pintura(v)] : []; return n; };
const borde = (n, v, w = 'linea/fino', dash) => { n.strokes = [pintura(v)]; n.setBoundVariable('strokeWeight', E(w)); if (dash) n.dashPattern = dash; return n; };
const radio = (n, r) => { for (const k of ['topLeftRadius', 'topRightRadius', 'bottomLeftRadius', 'bottomRightRadius']) n.setBoundVariable(k, E(r)); return n; };
const radioPortal = n => { n.setBoundVariable('topLeftRadius', E('radio/pleno')); n.setBoundVariable('topRightRadius', E('radio/pleno')); n.setBoundVariable('bottomLeftRadius', E('radio/l')); n.setBoundVariable('bottomRightRadius', E('radio/l')); return n; };
const pad = (n, y, x) => { n.setBoundVariable('paddingTop', E('espacio/' + y)); n.setBoundVariable('paddingBottom', E('espacio/' + y)); n.setBoundVariable('paddingLeft', E('espacio/' + x)); n.setBoundVariable('paddingRight', E('espacio/' + x)); return n; };
const gap = (n, g) => { n.setBoundVariable('itemSpacing', E('espacio/' + g)); return n; };
const TS = Object.fromEntries((await figma.getLocalTextStylesAsync()).map(s => [s.name, s]));
for (const s of Object.values(TS)) await figma.loadFontAsync(s.fontName);
const txt = async (s, estilo, colorVar, ancho) => {
  const t = figma.createText(); await t.setTextStyleIdAsync(TS[estilo].id); t.characters = s; fill(t, colorVar);
  if (ancho) { t.resize(ancho, t.height); t.textAutoResize = 'HEIGHT'; } return t; };
const auto = (dir, nombre, g, py, px) => { const f = figma.createAutoLayout(dir, { name: nombre }); f.fills = []; if (g) gap(f, g); if (py) pad(f, py, px || py); return f; };
const modoColor = (n, m) => n.setExplicitVariableModeForCollection(COL['Color'], COL['Color'].modes.find(x => x.name === m).modeId);
const pagina = async (id) => { const p = await figma.getNodeByIdAsync(id); await figma.setCurrentPageAsync(p); return p; };
const hoja = (p, nombre, x = 0, y = 0) => {
  let f = p.children.find(n => n.name === nombre);
  if (f) f.remove();
  f = figma.createAutoLayout('VERTICAL', { name: nombre }); p.appendChild(f); f.x = x; f.y = y;
  f.resize(1188, 100); f.counterAxisSizingMode = 'FIXED'; f.primaryAxisSizingMode = 'AUTO';
  fill(f, C('superficie/base')); pad(f, '3xl', '3xl'); gap(f, 'xl'); modoColor(f, 'Oscuro'); return f; };
const cabeza = async (f, ojo, titulo, lede) => {
  f.appendChild(await txt(ojo, 'Dato/etiqueta', C('texto/secundario')));
  f.appendChild(await txt(titulo, 'Display/display-2', C('texto/primario'), 1044));
  if (lede) f.appendChild(await txt(lede, 'Texto/cuerpo', C('texto/secundario'), 900)); };
const seccion = async (f, titulo, lede) => {
  const s = auto('VERTICAL', titulo, 'm'); f.appendChild(s); s.layoutSizingHorizontal = 'FILL';
  s.appendChild(await txt(titulo, 'Título/titulo-2', C('texto/primario'), 1044));
  if (lede) s.appendChild(await txt(lede, 'Texto/cuerpo-s', C('texto/secundario'), 900));
  return s; };

const ICONOS = [["pase","Pase","M5 3h14a1 1 0 0 1 1 1v16a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z M8 17v-5a4 4 0 0 1 8 0v5z"],["qr","QR","M4 4h5v5H4z M15 4h5v5h-5z M4 15h5v5H4z M15 15h2v2h-2z M19.5 19.5h.01 M15 20h.01 M20 15v1"],["placa","Placa","M3 7h18a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V8a1 1 0 0 1 1-1z M6 12h3 M11 12h2 M15 12h3"],["codigo","Código","M4 7h16a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V8a1 1 0 0 1 1-1z M7.5 12h.01 M10.5 12h.01 M13.5 12h.01 M16.5 12h.01"],["talanquera","Talanquera","M5 8v12 M3 20h4 M5 9h15v4H5 M9.5 9l-2 4 M14 9l-2 4 M18.5 9l-2 4"],["camara","Cámara","M4 7h11a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V8a1 1 0 0 1 1-1z M16 10.5l5-2.5v8l-5-2.5"],["rostro","Rostro","M4 8V5a1 1 0 0 1 1-1h3 M16 4h3a1 1 0 0 1 1 1v3 M20 16v3a1 1 0 0 1-1 1h-3 M8 20H5a1 1 0 0 1-1-1v-3 M9 10v1 M15 10v1 M9.5 15a3.5 3.5 0 0 0 5 0"],["lector","Lector","M7 3h10a1 1 0 0 1 1 1v16a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z M9 6h6v5H9z M12 16.5h.01"],["mensaje","Mensaje","M5 5h14a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H10l-5 4V6a1 1 0 0 1 1-1z M9 10h6"],["carro","Vehículo","M3 16v-4l2.5-5h13L21 12v4z M3 12h18 M7 19a1.5 1.5 0 0 0 0-3 M17 19a1.5 1.5 0 0 0 0-3 M7 19a1.5 1.5 0 0 1 0-3 M17 19a1.5 1.5 0 0 1 0-3"],["limites","Límites","M4 7h9 M17 7h3 M4 17h3 M11 17h9 M15 5v4 M9 15v4"],["constancia","Constancia","M6 3h8l4 4v14H6z M14 3v4h4 M9 14l2 2 4-4"],["residente","Residente","M3 11l9-7 9 7 M5 9.5V20h14V9.5 M12 14.5a2 2 0 1 0 0-4 2 2 0 0 0 0 4z M8.5 20a3.5 3.5 0 0 1 7 0"],["visita","Visita","M9 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6z M3 20a6 6 0 0 1 12 0 M16 12h5 M19 10l2 2-2 2"],["colaborador","Colaborador","M9 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6z M3 20a6 6 0 0 1 10-4.5 M16 15h5v5h-5z M17.5 15v-1.5h2V15"],["administracion","Administración","M4 21V5l8-2v18 M12 9l8 2v10 M3 21h18 M7 8h2 M7 12h2 M7 16h2 M15 13h2 M15 17h2"],["porteria","Portería","M4 20V6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v14 M2 20h20 M7 8h10v5H7z M12 16v4"],["previsto","Previsto","M4 6h16v14H4z M4 10h16 M8 4v4 M16 4v4 M9 15h6"],["sin-confirmar","Sin confirmar","M12 3a9 9 0 0 1 4.5 1.2 M19.8 7.5A9 9 0 0 1 21 12 M19.8 16.5a9 9 0 0 1-3.3 3.3 M12 21a9 9 0 0 1-4.5-1.2 M4.2 16.5A9 9 0 0 1 3 12 M4.2 7.5a9 9 0 0 1 3.3-3.3"],["vigente","Vigente","M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18z M8 12.5l2.7 2.7L16 10"],["por-vencer","Por vencer","M7 3h10 M7 21h10 M8 3c0 4 8 5 8 9s-8 5-8 9 M16 3c0 4-8 5-8 9s8 5 8 9"],["usado","Usado","M4 7h16v3a2 2 0 0 0 0 4v3H4v-3a2 2 0 0 0 0-4z M9 12l2 2 4-4"],["vencido","Vencido","M21 12a9 9 0 1 1-3-6.7 M12 7v5h3"],["revocado","Revocado","M6 3h12a1 1 0 0 1 1 1v16a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z M3 21L21 3"],["rechazado","Rechazado","M20 4v16 M16 12H4 M8 8l-4 4 4 4"],["identidad","Dato personal","M3 6h18v12H3z M8.5 12a2 2 0 1 0 0-4 2 2 0 0 0 0 4z M5.5 16a3 3 0 0 1 6 0 M14 9h4 M14 13h4"],["inicio","Inicio","M3 11l9-7 9 7 M5 10v10h14V10 M10 20v-6h4v6"],["atras","Atrás","M15 5l-7 7 7 7"],["flecha","Siguiente","M5 12h14 M13 6l6 6-6 6"],["menu","Menú","M4 7h16 M4 12h16 M4 17h16"],["buscar","Buscar","M11 17a6 6 0 1 0 0-12 6 6 0 0 0 0 12z M20 20l-4.5-4.5"],["ajustes","Ajustes","M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6z M12 3v3 M12 18v3 M3 12h3 M18 12h3 M5.6 5.6l2.1 2.1 M16.3 16.3l2.1 2.1 M5.6 18.4l2.1-2.1 M16.3 7.7l2.1-2.1"],["crear","Crear","M12 5v14 M5 12h14"],["cerrar","Cerrar","M6 6l12 12 M18 6L6 18"],["compartir","Compartir","M12 15V4 M8 8l4-4 4 4 M5 13v6a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-6"],["bajar","Descargar","M12 4v11 M8 11l4 4 4-4 M5 20h14"],["llamar","Llamar","M5 4h3.5l1.8 4.5-2.3 1.4a10 10 0 0 0 5.1 5.1l1.4-2.3L19 14.5V18a2 2 0 0 1-2 2A14 14 0 0 1 3 6a2 2 0 0 1 2-2z"]];
const BLOQUE = "M 3.483 0 H 96.517 A 3.483 3.483 0 0 1 100.000 3.483 V 101.824 H 0 V 3.483 A 3.483 3.483 0 0 1 3.483 0 Z M 18.242 86.567 V 46.766 A 31.675 31.675 0 0 1 81.592 46.766 V 86.567 Z", GOTA = "M 50.000 35.987 A 16.169 17.579 0 0 1 66.169 53.566 L 50.000 66.667 L 33.831 53.566 A 16.169 17.579 0 0 1 50.000 35.987 Z", PALABRA = "M 85.55 33.97 C 84.03 34.05 81.06 33.97 79.57 33.80 C 78.07 33.64 77.57 33.36 76.58 32.97 C 75.58 32.59 74.68 32.27 73.59 31.48 C 72.49 30.69 70.81 29.06 70.02 28.24 C 69.23 27.42 69.21 27.19 68.85 26.58 C 68.49 25.97 68.19 25.50 67.86 24.58 C 67.52 23.67 67.08 22.20 66.86 21.10 C 66.64 19.99 66.56 19.13 66.53 17.94 C 66.50 16.75 66.56 15.14 66.69 13.95 C 66.83 12.76 67.03 11.85 67.36 10.80 C 67.69 9.75 68.22 8.53 68.69 7.64 C 69.16 6.76 69.50 6.24 70.18 5.48 C 70.86 4.72 71.80 3.78 72.76 3.07 C 73.71 2.37 74.86 1.72 75.91 1.25 C 76.97 0.78 78.18 0.47 79.07 0.25 C 79.96 0.03 79.98 -0.06 81.23 -0.08 C 82.48 -0.11 85.13 -0.08 86.54 0.08 C 87.96 0.25 88.76 0.58 89.70 0.91 C 90.64 1.25 91.39 1.61 92.19 2.08 C 93.00 2.55 93.73 3.03 94.52 3.74 C 95.31 4.44 96.22 5.33 96.93 6.31 C 97.63 7.30 98.28 8.47 98.75 9.63 C 99.22 10.80 99.56 11.79 99.75 13.29 C 99.94 14.78 99.97 17.14 99.92 18.60 C 99.86 20.07 99.67 20.99 99.42 22.09 C 99.17 23.20 98.86 24.28 98.42 25.25 C 97.98 26.22 97.33 27.15 96.76 27.91 C 96.19 28.67 95.78 29.17 95.02 29.82 C 94.26 30.47 93.24 31.23 92.19 31.81 C 91.14 32.39 89.81 32.95 88.70 33.31 C 87.60 33.67 87.07 33.89 85.55 33.97 Z M 34.55 33.47 L 22.84 33.39 L 22.92 1.91 L 34.63 1.99 L 34.55 33.47 Z M 63.46 33.47 L 56.64 33.47 L 49.50 24.00 L 49.34 33.47 L 38.46 33.39 L 38.54 1.91 L 45.35 1.91 L 53.82 13.04 C 53.82 13.04 54.03 13.80 54.07 11.96 C 54.11 10.12 54.07 1.99 54.07 1.99 L 63.54 1.99 L 63.46 33.47 Z M 20.10 33.31 L -0.08 33.22 L 0.17 2.08 L 20.18 2.33 C 20.18 2.33 17.52 6.81 15.86 9.30 C 14.20 11.79 10.22 17.28 10.22 17.28 L 20.10 33.31 Z M 84.47 23.59 C 85.16 23.45 85.74 23.15 86.21 22.84 C 86.68 22.54 87.03 22.11 87.29 21.76 C 87.56 21.41 87.62 21.29 87.79 20.76 C 87.96 20.24 88.21 19.55 88.29 18.60 C 88.37 17.66 88.40 16.09 88.29 15.12 C 88.18 14.15 87.89 13.39 87.62 12.79 C 87.36 12.20 87.20 11.95 86.71 11.54 C 86.23 11.14 85.41 10.60 84.72 10.38 C 84.03 10.16 83.28 10.11 82.56 10.22 C 81.84 10.33 80.97 10.70 80.40 11.05 C 79.83 11.39 79.44 11.92 79.15 12.29 C 78.86 12.67 78.82 12.68 78.65 13.29 C 78.49 13.90 78.21 14.92 78.16 15.95 C 78.10 16.97 78.18 18.52 78.32 19.44 C 78.46 20.35 78.70 20.89 78.99 21.43 C 79.28 21.97 79.55 22.30 80.07 22.67 C 80.58 23.05 81.33 23.52 82.06 23.67 C 82.79 23.82 83.78 23.73 84.47 23.59 Z";
const p = await pagina('22:64');
// Marco de íconos y logo (componentes base). Se rehace si ya existe.
for (const n of ['Íconos', 'Logo']) { const f = p.children.find(x => x.name === n); if (f) f.remove(); }
const fi = auto('HORIZONTAL', 'Íconos', 'm', 'l', 'l'); p.appendChild(fi); fi.x = 0; fi.y = 0; fi.layoutWrap = 'WRAP'; fi.resize(1188, 100);
fi.counterAxisSizingMode = 'AUTO'; fi.primaryAxisSizingMode = 'FIXED'; fi.setBoundVariable('counterAxisSpacing', E('espacio/m'));
fill(fi, C('superficie/base')); modoColor(fi, 'Oscuro'); radio(fi, 'radio/l');
const ids = [];
for (const [k, n, d] of ICONOS) {
  const svg = figma.createNodeFromSvg(`<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="${d}"/></svg>`);
  const comp = figma.createComponent(); comp.name = 'Icono/' + k; comp.resize(24, 24); comp.fills = []; comp.clipsContent = false;
  for (const ch of [...svg.children]) comp.appendChild(ch);
  svg.remove();
  for (const v of comp.findAll(x => 'strokes' in x)) { if (v.strokes.length) { v.strokes = [pintura(C('texto/primario'))]; v.setBoundVariable('strokeWeight', E('trazo/icono')); } v.fills = []; }
  comp.description = n + '. Grilla 24, trazo 1,7 ligado a trazo/icono, puntas redondas (X6).';
  fi.appendChild(comp); ids.push(comp.id);
}
// Logo: bloque en marca/bloque y gota en marca/gota (X2).
const fl = auto('HORIZONTAL', 'Logo', 'xl', 'l', 'l'); p.appendChild(fl); fl.x = 0; fl.y = fi.height + 48;
fill(fl, C('superficie/base')); modoColor(fl, 'Oscuro'); radio(fl, 'radio/l');
const hacerLogo = (forma) => {
  const w = forma === 'Horizontal' ? 267.96 : 100, h = forma === 'Vertical' ? 140.023 : 101.824;
  const pal = forma === 'Horizontal' ? `<g transform="translate(126 25.681) scale(1.4196)"><path fill-rule="evenodd" d="${PALABRA}"/></g>` : forma === 'Vertical' ? `<g transform="translate(0 105.97)"><path fill-rule="evenodd" d="${PALABRA}"/></g>` : '';
  const svg = figma.createNodeFromSvg(`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><path fill-rule="evenodd" d="${BLOQUE}"/><path d="${GOTA}"/>${pal}</svg>`);
  const comp = figma.createComponent(); comp.name = 'Logo/' + forma; comp.resize(w, h); comp.fills = [];
  const hijos = svg.findAll(x => x.type === 'VECTOR');
  hijos.forEach((v, i) => { const x = v.absoluteTransform[0][2] - svg.absoluteTransform[0][2], y = v.absoluteTransform[1][2] - svg.absoluteTransform[1][2]; comp.appendChild(v); v.x = x; v.y = y; v.name = ['Bloque', 'Gota', 'KINO'][i]; fill(v, C(i === 1 ? 'marca/gota' : 'marca/bloque')); v.strokes = []; });
  svg.remove();
  comp.description = 'Logo ' + forma.toLowerCase() + '. Reconstrucción desde PNG (98 %). Colores ligados a marca/bloque y marca/gota (X2).';
  fl.appendChild(comp); return comp.id;
};
const logos = ['Horizontal', 'Símbolo', 'Vertical'].map(hacerLogo);
return { iconos: ids.length, primero: ids[0], logos, marcoIconos: fi.id, marcoLogo: fl.id };
