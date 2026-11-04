// Capturas antes y después de la identidad aplicada al sitio (F4-P4), en JPEG, para la lámina.
// Uso: node capturar.mjs <antes.html> <despues.html>  (con las fuentes incrustadas; ver construir.py)
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
const req = createRequire(import.meta.url);
const pw = req('/home/user/kino/gorr-brand-system/node_modules/playwright');
const aqui = path.dirname(new URL(import.meta.url).pathname);
const [antes, despues] = process.argv.slice(2);
const d = fs.readdirSync('/opt/pw-browsers').find(x => /^chromium-\d+$/.test(x));
const nav = await pw.chromium.launch({ executablePath: `/opt/pw-browsers/${d}/chrome-linux/chrome` });
const vistas = [['inicio', 1440, 820, 'oscuro'], ['plataforma', 1440, 820, 'oscuro'], ['plataforma', 1440, 820, 'claro'], ['color.estados', 1440, 820, 'oscuro'], ['inicio', 390, 820, 'oscuro']];
for (const [cual, archivo] of [['antes', antes], ['despues', despues]]) for (const [h, w, alto, tema] of vistas) {
  const p = await nav.newPage({ viewport: { width: w, height: alto }, deviceScaleFactor: w < 500 ? 1 : 0.7 });
  await p.addInitScript(t => { try { localStorage.setItem('kino-tema', t); } catch (e) {} }, tema);
  await p.goto('file://' + archivo + '#' + h); await p.waitForTimeout(1600);
  const n = `${cual}-${h.replace('.', '_')}-${w}-${tema}.jpg`;
  await p.screenshot({ path: path.join(aqui, 'capturas', n), type: 'jpeg', quality: 78 });
  console.log(n, fs.statSync(path.join(aqui, 'capturas', n)).size); await p.close();
}
await nav.close();
