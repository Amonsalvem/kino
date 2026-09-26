// Pruebas de navegador sobre el Lab (Playwright). npm run lab && node scripts/probar-lab.mjs
// Comprueba: sin errores de JS, estado honesto, movimiento reducido, cambio de pantalla y sin desborde en 390 px.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {execSync} from 'node:child_process';

const req = createRequire(import.meta.url);
let pw;
try {
	pw = req('playwright');
} catch {
	pw = req(path.join(execSync('npm root -g').toString().trim(), 'playwright'));
}
const html = fs.readFileSync('lab/dist/kino-motion-lab.html');
const servidor = http.createServer((_q, r) => r.writeHead(200, {'content-type': 'text/html; charset=utf-8'}).end(html)).listen(0);
const url = `http://localhost:${servidor.address().port}/`;
const cands = fs.existsSync('/opt/pw-browsers') ? fs.readdirSync('/opt/pw-browsers').filter((d) => /^chromium-\d+$/.test(d)).map((d) => `/opt/pw-browsers/${d}/chrome-linux/chrome`) : [];
const nav = await pw.chromium.launch(cands[0] ? {executablePath: cands[0]} : {});
let fallas = 0;
const ok = (cond, msg) => {
	console.log(`${cond ? '✓' : '✗'} ${msg}`);
	if (!cond) fallas++;
};

for (const [ancho, esquema] of [[1280, 'dark'], [390, 'light']]) {
	const p = await (await nav.newContext({viewport: {width: ancho, height: 900}, colorScheme: esquema})).newPage();
	await p.route('https://fonts.googleapis.com/**', (r) => r.fulfill({status: 200, contentType: 'text/css', body: ''}));
	const errores = [];
	p.on('pageerror', (e) => errores.push(e.message));
	await p.goto(url);
	await p.waitForTimeout(1200);
	ok(!(await p.evaluate(() => document.documentElement.scrollWidth > innerWidth)), `${ancho} px ${esquema}: sin desborde horizontal`);
	const ev = p.locator('#pase-eventos');
	ok(await ev.getByRole('button', {name: 'El lector confirma'}).isDisabled(), `${ancho} px: «confirmar» no se puede desde «previsto»`);
	await ev.getByRole('button', {name: 'Enviar al lector'}).click();
	await p.waitForTimeout(300);
	await ev.getByRole('button', {name: 'El lector confirma'}).click();
	await p.waitForTimeout(900);
	ok((await p.evaluate(() => document.querySelector('#pase-vivo').dataset.estado)) === 'vigente', `${ancho} px: enviar → confirmar deja el Pase vigente`);
	await p.click('#pase-forzar');
	await p.waitForTimeout(100);
	ok((await p.evaluate(() => document.querySelector('#pase-vivo').dataset.estado)) === 'sin-confirmar', `${ancho} px: «vigente» sin lector se muestra «sin confirmar»`);
	await p.evaluate(() => (document.documentElement.dataset.movimiento = 'reducido'));
	await p.click('#pase-reiniciar');
	await ev.getByRole('button', {name: 'Enviar al lector'}).click();
	await p.waitForTimeout(300);
	await ev.getByRole('button', {name: 'El lector confirma'}).click();
	await p.waitForTimeout(200);
	const pistas = await p.evaluate(() => [...document.querySelectorAll('#partitura .pista > span:first-child')].map((x) => x.textContent));
	ok(!pistas.some((t) => / (y|escala|escalaX)$/.test(t)), `${ancho} px: en reducido ninguna pista desplaza (${pistas.join(', ')})`);
	await p.evaluate(() => (document.documentElement.dataset.movimiento = 'completo'));
	await p.locator('#tel-pantalla kino-pase').first().click();
	await p.waitForTimeout(900);
	ok((await p.textContent('#tel-titulo')) === 'Detalle del Pase', `${ancho} px: la lista abre el detalle`);
	ok(errores.length === 0, `${ancho} px: sin errores de JS ${errores.join(' | ')}`);
}
await nav.close();
servidor.close();
console.log(fallas ? `\n${fallas} fallas` : '\ntodo en orden');
process.exit(fallas ? 1 : 0);
