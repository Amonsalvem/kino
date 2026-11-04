// Capturas del sitio o de una lámina en 360, 768 y 1440 px, con chequeo de desbordamiento horizontal.
// Uso: node herramientas/capturar.mjs <archivo.html> [carpeta-salida]
// Supuestos: playwright instalado (local o global) y Chromium en /opt/pw-browsers o descargado por playwright.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
const req = createRequire(import.meta.url);
let pw;
try { pw = req('playwright'); } catch { pw = req(path.join(execSync('npm root -g').toString().trim(), 'playwright')); }
if (!process.argv[2]) { console.error('Uso: node herramientas/capturar.mjs <archivo.html> [carpeta-salida]'); process.exit(2); }
const archivo = path.resolve(process.argv[2]);
const salida = path.resolve(process.argv[3] || 'capturas');
fs.mkdirSync(salida, { recursive: true });
const cands = fs.existsSync('/opt/pw-browsers') ? ['/opt/pw-browsers/chromium', ...fs.readdirSync('/opt/pw-browsers').filter(d => /^chromium-\d+$/.test(d)).flatMap(d => [`/opt/pw-browsers/${d}/chrome-linux64/chrome`, `/opt/pw-browsers/${d}/chrome-linux/chrome`])] : [];
const executablePath = cands.find(fs.existsSync);
const nav = await pw.chromium.launch(executablePath ? { executablePath } : {});
let fallas = 0;
for (const ancho of [360, 768, 1440]) {
  for (const tema of ['oscuro', 'claro']) {
    const p = await nav.newPage({ viewport: { width: ancho, height: 900 }, colorScheme: tema === 'oscuro' ? 'dark' : 'light' });
    const errores = [];
    p.on('pageerror', e => errores.push(e.message));
    p.on('console', m => m.type() === 'error' && errores.push(m.text()));
    await p.goto('file://' + archivo);
    await p.evaluate(t => document.documentElement.setAttribute('data-tema', t), tema);
    await p.waitForTimeout(1200);
    const desborde = await p.evaluate(() => document.documentElement.scrollWidth - innerWidth);
    const nombre = `${path.basename(archivo, '.html')}-${ancho}-${tema}.png`;
    await p.screenshot({ path: path.join(salida, nombre), fullPage: true });
    // Recursos externos bloqueados por la red del entorno (fuentes, CDN) se avisan, no fallan.
    const red = errores.filter(e => /net::ERR_/.test(e));
    const reales = errores.filter(e => !/net::ERR_/.test(e));
    const bien = desborde <= 0 && reales.length === 0;
    if (!bien) fallas++;
    console.log(`${bien ? 'ok ' : 'MAL'} ${ancho}px ${tema}: desborde ${desborde}px, errores ${reales.length}${reales.length ? ' · ' + reales[0] : ''}${red.length ? ` · aviso: ${red.length} recurso(s) externo(s) bloqueado(s) por la red` : ''}`);
    await p.close();
  }
}
await nav.close();
process.exit(fallas ? 1 : 0);
