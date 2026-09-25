// Auditoría responsive del sitio: cada sección en cada ancho (de 320 a 1920 px).
// Uso: node scripts/auditar-responsive.mjs <sitio.html> [anchos separados por coma] [salida.json]
// Reporta por sección y ancho: desborde de la página, elementos fuera de la pantalla, contenedores con desplazamiento
// lateral, contenido recortado, controles de menos de 24 px (WCAG 2.5.8) y texto de menos de 11 px.
// Esperados (no son errores): el encabezado oculto de las tablas apiladas (thead), el número decorativo de cada apertura
// (header.abre), el caso de tipografía «un renglón que no termina», los enlaces del glosario dentro de una línea de texto y el
// texto de las piezas del Pase en Inicio y Aplicaciones, que son imágenes de 1080 × 1350 mostradas a escala.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
const req = createRequire(import.meta.url);
let pw;
try { pw = req('playwright'); } catch { try { pw = req(path.resolve('gorr-brand-system/node_modules/playwright')); } catch { pw = req(path.join(execSync('npm root -g').toString().trim(), 'playwright')); } }
const archivo = path.resolve(process.argv[2] || 'branding/sistema/v3/sitio/build/kino-sistema-de-marca.html');
const anchos = (process.argv[3] || '320,360,390,430,600,768,900,1024,1280,1440,1920').split(',').map(Number);
const cands = fs.existsSync('/opt/pw-browsers') ? fs.readdirSync('/opt/pw-browsers').filter(d => /^chromium-\d+$/.test(d)).map(d => `/opt/pw-browsers/${d}/chrome-linux/chrome`) : [];
const executablePath = cands.find(fs.existsSync);
const nav = await pw.chromium.launch(executablePath ? { executablePath } : {});
const p = await nav.newPage({ viewport: { width: 1440, height: 900 } });
await p.goto('file://' + archivo); await p.waitForTimeout(800);
const secciones = await p.evaluate(() => [...document.querySelectorAll('main section[id], .seccion[id], section.seccion')].map(s => s.id).filter((v, i, a) => v && a.indexOf(v) === i && !v.includes('.')));
const out = {};
for (const w of anchos) {
  await p.setViewportSize({ width: w, height: 900 });
  for (const s of secciones) {
    await p.goto('file://' + archivo + '#' + s); await p.waitForTimeout(350);
    const r = await p.evaluate(() => {
      const vis = el => { const cs = getComputedStyle(el); if (cs.display === 'none' || cs.visibility === 'hidden') return false; const b = el.getBoundingClientRect(); return b.width > 0 && b.height > 0 && el.closest('[hidden]') === null; };
      const sel = el => el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '');
      const W = innerWidth, res = { desborde: document.documentElement.scrollWidth - W, fuera: [], scroll: [], recorte: [], tactil: [], diminuto: [] };
      const enScroll = el => { let q = el.parentElement; while (q && q !== document.body) { const o = getComputedStyle(q).overflowX; if (o === 'auto' || o === 'scroll' || o === 'hidden' || o === 'clip') return true; q = q.parentElement; } return false; };
      const act = document.querySelector('main section:not([hidden]), .seccion:not([hidden])') || document.body;
      for (const el of act.querySelectorAll('*')) {
        if (!vis(el)) continue;
        const b = el.getBoundingClientRect(), cs = getComputedStyle(el);
        if (b.right > W + 1 && !enScroll(el)) res.fuera.push(sel(el) + ' r=' + Math.round(b.right));
        if ((cs.overflowX === 'auto' || cs.overflowX === 'scroll') && el.scrollWidth > el.clientWidth + 1) res.scroll.push(sel(el) + ' ' + el.scrollWidth + '/' + el.clientWidth);
        if ((cs.overflowX === 'hidden' || cs.overflow === 'hidden') && el.scrollWidth > el.clientWidth + 2 && el.children.length + (el.textContent.trim() ? 1 : 0) > 0 && !el.closest('svg')) res.recorte.push(sel(el) + ' ' + el.scrollWidth + '/' + el.clientWidth);
        if (el.matches('a,button,input,select,textarea,[role=button],[tabindex="0"]') && !el.closest('p,li:not(.nav li),td,dd,figcaption') && (b.width < 24 || b.height < 24) && el.getAttribute('tabindex') !== '-1') res.tactil.push(sel(el) + ' ' + Math.round(b.width) + 'x' + Math.round(b.height));
        if (el.childNodes.length && [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && parseFloat(cs.fontSize) < 11 && !el.closest('svg')) res.diminuto.push(sel(el) + ' ' + cs.fontSize);
      }
      for (const k of ['fuera', 'scroll', 'recorte', 'tactil', 'diminuto']) res[k] = [...new Set(res[k])];
      return res;
    });
    out[`${w}:${s}`] = r;
  }
}
await nav.close();
fs.writeFileSync(process.argv[4] || 'auditoria-responsive.json', JSON.stringify(out, null, 1));
const resumen = {};
for (const [k, r] of Object.entries(out)) { const [w, s] = k.split(':'); for (const t of ['fuera', 'scroll', 'recorte', 'tactil', 'diminuto']) { if (r[t].length) { resumen[t] = resumen[t] || {}; resumen[t][s] = resumen[t][s] || {}; resumen[t][s][w] = r[t].length; } } if (r.desborde > 0) { resumen.desborde = resumen.desborde || {}; resumen.desborde[k] = r.desborde; } }
console.log(JSON.stringify({ secciones, resumen }, null, 0));
