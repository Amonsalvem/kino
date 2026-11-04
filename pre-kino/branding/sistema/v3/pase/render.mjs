// Pasa las piezas del Pase a los formatos que se entregan: PNG de 1080 × 1350 para WhatsApp, PDF carta
// y PNG de la señal. Uso: node render.mjs (después de python3 construir.py).
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
const req = createRequire(import.meta.url);
let pw; try { pw = req('playwright'); } catch { pw = req(path.join(execSync('npm root -g').toString().trim(), 'playwright')); }
const dir = path.join(path.dirname(new URL(import.meta.url).pathname), 'build');
const cands = fs.existsSync('/opt/pw-browsers') ? fs.readdirSync('/opt/pw-browsers').filter(d => /^chromium-\d+$/.test(d)).map(d => `/opt/pw-browsers/${d}/chrome-linux/chrome`) : [];
const nav = await pw.chromium.launch(cands.find(fs.existsSync) ? { executablePath: cands.find(fs.existsSync) } : {});
const abrir = async (archivo, ancho, alto) => {
  const p = await nav.newPage({ viewport: { width: ancho, height: alto }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.join(dir, archivo)); await p.waitForTimeout(800); return p;
};
for (const n of ['visita', 'colaborador']) {
  const p = await abrir(`imagen-${n}.html`, 1080, 1350);
  await (await p.$('.pieza-pase')).screenshot({ path: path.join(dir, `pase-${n}.png`) });
  console.log(`pase-${n}.png`); await p.close();
}
{ const p = await abrir('pdf.html', 816, 1056); await p.pdf({ path: path.join(dir, 'pase.pdf'), format: 'Letter', printBackground: true }); console.log('pase.pdf'); await p.close(); }
{ const p = await abrir('senal-entrada.html', 1800, 1200); await (await p.$('.senal-entrada')).screenshot({ path: path.join(dir, 'senal-entrada.png') }); console.log('senal-entrada.png'); await p.close(); }
await nav.close();
