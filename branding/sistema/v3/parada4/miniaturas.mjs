// Miniaturas JPEG de las piezas del Pase para la lámina de la Parada 4.
// Uso: node miniaturas.mjs (después de python3 ../pase/construir.py).
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
const req = createRequire(import.meta.url);
let pw; try { pw = req('playwright'); } catch { pw = req(path.join(execSync('npm root -g').toString().trim(), 'playwright')); }
const aqui = path.dirname(new URL(import.meta.url).pathname);
const dir = path.join(aqui, '../pase/build'); const sal = path.join(aqui, 'miniaturas'); fs.mkdirSync(sal, { recursive: true });
const cands = fs.existsSync('/opt/pw-browsers') ? fs.readdirSync('/opt/pw-browsers').filter(d => /^chromium-\d+$/.test(d)).map(d => `/opt/pw-browsers/${d}/chrome-linux/chrome`) : [];
const nav = await pw.chromium.launch(cands.find(fs.existsSync) ? { executablePath: cands.find(fs.existsSync) } : {});
const piezas = [
  ['imagen-visita', '.pieza-pase', 1080, 1350, 0.5, 'dark'],
  ['pase-vivo', '.pase-vivo', 400, 900, 1.5, 'dark'],
  ['pase-vivo-vencido', '.pase-vivo', 400, 900, 1.5, 'dark'],
  ['porteria', '.vista-porteria', 1280, 800, 0.75, 'dark'],
  ['pdf', '.pase-pdf', 816, 1056, 0.75, 'light'],
  ['senal-entrada', '.senal-entrada', 1800, 1200, 0.4, 'dark'],
];
for (const [n, sel, w, h, esc, esquema] of piezas) {
  const p = await nav.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: esc, colorScheme: esquema });
  await p.goto('file://' + path.join(dir, n + '.html')); await p.waitForTimeout(900);
  await (await p.$(sel)).screenshot({ path: path.join(sal, n + '.jpg'), type: 'jpeg', quality: 80 });
  console.log(n, fs.statSync(path.join(sal, n + '.jpg')).size); await p.close();
}
await nav.close();
