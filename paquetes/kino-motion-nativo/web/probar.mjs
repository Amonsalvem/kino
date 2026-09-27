// Pruebas del adaptador en navegador (react-native-web + Reanimated + Gesture Handler).
//   npm run web && node web/probar.mjs
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
const raiz = path.join(path.dirname(new URL(import.meta.url).pathname), 'dist');
const tipos = {'.html': 'text/html', '.js': 'text/javascript', '.map': 'application/json'};
const servidor = http
	.createServer((q, r) => {
		const f = path.join(raiz, q.url === '/' ? 'index.html' : q.url.split('?')[0]);
		if (!fs.existsSync(f)) return r.writeHead(404).end();
		r.writeHead(200, {'content-type': tipos[path.extname(f)] ?? 'application/octet-stream'}).end(fs.readFileSync(f));
	})
	.listen(0);
const url = `http://localhost:${servidor.address().port}/`;
const cands = fs.existsSync('/opt/pw-browsers') ? fs.readdirSync('/opt/pw-browsers').filter((d) => /^chromium-\d+$/.test(d)).map((d) => `/opt/pw-browsers/${d}/chrome-linux/chrome`) : [];
const nav = await pw.chromium.launch(cands[0] ? {executablePath: cands[0]} : {});
let fallas = 0;
const ok = (c, m) => {
	console.log(`${c ? '✓' : '✗'} ${m}`);
	if (!c) fallas++;
};
const p = await (await nav.newContext({viewport: {width: 430, height: 1100}, colorScheme: 'dark'})).newPage();
const errores = [];
await p.route('https://fonts.googleapis.com/**', (r) => r.fulfill({status: 200, contentType: 'text/css', body: ''})); // la sandbox no alcanza Google Fonts
p.on('pageerror', (e) => errores.push(e.message));
p.on('console', (m) => m.type() === 'error' && !/findDOMNode|404/.test(m.text()) && errores.push(m.text()));
await p.goto(url);
await p.waitForTimeout(2000);
const etiqueta = (id) => p.evaluate((i) => document.querySelector(`[data-testid="${i}"]`)?.getAttribute('aria-label') ?? '', id);
const click = (t) => p.getByText(t, {exact: true}).first().click();

ok((await etiqueta('pase-vivo')).includes('Previsto'), 'el Pase empieza previsto');
await click('Enviar al lector');
await p.waitForTimeout(400);
ok((await etiqueta('pase-vivo')).includes('Sin confirmar'), 'enviar → sin confirmar');
await click('El lector confirma');
// M3D-5: el texto del chip se funde a través (misma regla que la web). Muestras cada 40 ms del texto del chip.
const chip = () => p.evaluate(() => {
	const raiz = document.querySelector('[data-testid="pase-vivo"]');
	const t = [...raiz.querySelectorAll('*')].find((n) => n.children.length === 0 && ['Sin confirmar', 'Vigente'].includes(n.textContent));
	return t ? {texto: t.textContent, opacidad: Number(getComputedStyle(t).opacity)} : {texto: '', opacidad: 0};
});
const muestras = [];
for (let i = 0; i < 12; i++) { muestras.push(await chip()); await p.waitForTimeout(40); }
const viejo = muestras.filter((m) => m.texto === 'Sin confirmar').map((m) => m.opacidad);
ok(muestras.every((m) => ['Sin confirmar', 'Vigente'].includes(m.texto)) && viejo.every((o, i) => i === 0 || o <= viejo[i - 1] + 1e-3) && viejo.length < muestras.length,
	`el chip se funde a través (${muestras.map((m) => `${m.texto[0]}${m.opacidad.toFixed(2)}`).join(' ')})`);
await p.waitForTimeout(700);
const vig = await etiqueta('pase-vivo');
ok(vig.includes('Vigente') && vig.includes('Confirmó Lector Portería'), 'confirmar → vigente, con la evidencia del lector');
const final = await chip();
ok(final.texto === 'Vigente' && final.opacidad > 0.99, `al terminar el chip dice «Vigente» (${final.texto}, ${final.opacidad})`);
await click('Revocar');
await p.waitForTimeout(400);
ok((await etiqueta('pase-vivo')).includes('Revocó Carolina Ruiz'), 'revocar → revocado, con autor');
ok((await etiqueta('pase-honesto')).includes('Sin confirmar'), '«vigente» sin evidencia se muestra «sin confirmar»');
// Hoja: se abre y se cierra lanzándola hacia abajo desde el asa.
await click('Ver el Pase de Andrés');
await p.waitForTimeout(900);
const asa = p.getByLabel('Arrastra para cerrar');
ok(await asa.isVisible(), 'la hoja se abre');
const caja = await asa.boundingBox();
await p.mouse.move(caja.x + caja.width / 2, caja.y + caja.height / 2);
await p.mouse.down();
for (let i = 1; i <= 6; i++) await p.mouse.move(caja.x + caja.width / 2, caja.y + caja.height / 2 + i * 40, {steps: 2});
await p.mouse.up();
await p.waitForTimeout(1200);
ok(!(await asa.isVisible().catch(() => false)), 'lanzada hacia abajo, la hoja se cierra');
ok(!(await p.evaluate(() => document.documentElement.scrollWidth > innerWidth)), 'sin desborde horizontal en 430 px');
ok(errores.length === 0, `sin errores ${errores.join(' | ')}`);
await nav.close();
servidor.close();
console.log(fallas ? `\n${fallas} fallas` : '\ntodo en orden');
process.exit(fallas ? 1 : 0);
