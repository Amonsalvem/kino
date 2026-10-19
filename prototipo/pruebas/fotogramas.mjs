// Fotogramas de la coreografía de portería: entra y no entra, a 0, 120, 280, 480, 800, 1400 y 4600 ms.
// Uso: node pruebas/fotogramas.mjs [carpeta]
import {createRequire} from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const req = createRequire(import.meta.url);
const raiz = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const pw = req(path.join(raiz, 'gorr-brand-system/node_modules/playwright'));
const salida = path.resolve(process.argv[2] || path.join(raiz, 'prototipo/build/fotogramas'));
fs.mkdirSync(salida, {recursive: true});
const cands = fs.readdirSync('/opt/pw-browsers').filter((d) => /^chromium-\d+$/.test(d)).map((d) => `/opt/pw-browsers/${d}/chrome-linux/chrome`);
const nav = await pw.chromium.launch({executablePath: cands.find(fs.existsSync)});
const p = await nav.newPage({viewport: {width: 1080, height: 820}});
await p.goto(`file://${raiz}/prototipo/build/kino-prototipo.html?actor=porteria&solo=1`);
await p.waitForTimeout(600);
const panel = p.locator('.lector');
for (const [nombre, quien] of [['entra', 'Andrés Gómez'], ['no-entra', 'Juan Pablo']]) {
	await p.locator('.llegada', {hasText: quien}).first().click();
	await p.waitForTimeout(500);
	await panel.screenshot({path: path.join(salida, `${nombre}-leyendo.png`)});
	await p.waitForFunction(() => !document.querySelector('.lector--leyendo'));
	const t0 = Date.now();
	for (const ms of [0, 60, 120, 280, 480, 800, 1400, 4600]) {
		const espera = ms - (Date.now() - t0);
		if (espera > 0) await p.waitForTimeout(espera);
		await panel.screenshot({path: path.join(salida, `${nombre}-${String(ms).padStart(4, '0')}.png`)});
	}
}
await nav.close();
