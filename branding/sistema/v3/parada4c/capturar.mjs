// Capturas antes (1.1.0) y después (1.2.0) de cada pantalla, en JPEG, para la lámina de la 1.2.0.
// Uso: node capturar.mjs <antes.html> <despues.html>  (sitios con las fuentes incrustadas; ver construir.py)
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
const req = createRequire(import.meta.url);
const pw = req('/home/user/kino/gorr-brand-system/node_modules/playwright');
const aqui = path.dirname(new URL(import.meta.url).pathname);
const [antes, despues] = process.argv.slice(2);
const d = fs.readdirSync('/opt/pw-browsers').find(x => /^chromium-\d+$/.test(x));
const nav = await pw.chromium.launch({ executablePath: `/opt/pw-browsers/${d}/chrome-linux/chrome` });
const PANTALLAS = [['lista', 'Lista de Pases'], ['crear', 'Crear Pase'], ['detalle', 'Detalle de Pase'], ['codigo', 'Acceso por código']];
fs.mkdirSync(path.join(aqui, 'capturas'), { recursive: true });
for (const [cual, archivo] of [['antes', antes], ['despues', despues]]) {
  const p = await nav.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
  await p.addInitScript(() => { try { localStorage.setItem('kino-tema', 'oscuro'); } catch (e) {} });
  await p.goto('file://' + archivo + '#producto.pantallas'); await p.waitForTimeout(1500);
  for (const [n, cap] of PANTALLAS) {
    const fig = p.locator('#producto\\.pantallas figure.movil').filter({ has: p.locator('figcaption', { hasText: cap }) }).first();
    const f = path.join(aqui, 'capturas', `${cual}-${n}.jpg`);
    await fig.locator('.movil-pantalla').screenshot({ path: f, type: 'jpeg', quality: 80 });
    console.log(path.basename(f), fs.statSync(f).size);
  }
  const f = path.join(aqui, 'capturas', `${cual}-limites.jpg`);
  await p.locator('#producto\\.pantallas .escritorio-pantalla').first().screenshot({ path: f, type: 'jpeg', quality: 80 });
  console.log(path.basename(f), fs.statSync(f).size);
  await p.close();
}
await nav.close();
