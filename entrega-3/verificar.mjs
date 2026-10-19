// Verifica el deck de la entrega 3 para proyección: a 1920×1080 ningún texto visible baja de 24 px,
// no hay desborde horizontal ni errores de consola; también revisa 1280 y 390 px. Guarda capturas.
// Uso: node entrega-3/verificar.mjs [carpeta-capturas]
import {createRequire} from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const req = createRequire(import.meta.url);
const aqui = path.dirname(fileURLToPath(import.meta.url));
const pw = req(path.join(aqui, '../gorr-brand-system/node_modules/playwright'));
const salida = path.resolve(process.argv[2] || path.join(aqui, 'capturas'));
fs.mkdirSync(salida, {recursive: true});
// El artefacto se publica sin doctype (lo agrega la plataforma); aquí se envuelve igual para no medir en modo quirks.
const cuerpo = fs.readFileSync(path.join(aqui, 'kino_entrega_3.html'), 'utf8');
const tmp = path.join(aqui, '.verificar.html');
fs.writeFileSync(tmp, `<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>${cuerpo}</body></html>`);
const cands = fs.existsSync('/opt/pw-browsers') ? fs.readdirSync('/opt/pw-browsers').filter((d) => /^chromium-\d+$/.test(d)).map((d) => `/opt/pw-browsers/${d}/chrome-linux/chrome`) : [];
const nav = await pw.chromium.launch({executablePath: cands.find(fs.existsSync)});
let fallas = 0;
for (const [w, h] of [[1920, 1080], [1280, 720], [390, 844]]) {
	const p = await nav.newPage({viewport: {width: w, height: h}});
	const errores = [];
	p.on('pageerror', (e) => errores.push(e.message));
	await p.goto('file://' + tmp);
	await p.waitForTimeout(800);
	const r = await p.evaluate(() => {
		const chicos = [];
		const w = document.createTreeWalker(document.querySelector('#deck'), NodeFilter.SHOW_TEXT);
		while (w.nextNode()) {
			const n = w.currentNode;
			if (!n.textContent.trim()) continue;
			const el = n.parentElement;
			if (el.closest('.guion')) continue;
			const cs = getComputedStyle(el);
			if (cs.display === 'none' || cs.visibility === 'hidden') continue;
			const fs = parseFloat(cs.fontSize);
			if (fs < 23.5) chicos.push(`${fs.toFixed(1)}px «${n.textContent.trim().slice(0, 40)}»`);
		}
		const secs = [...document.querySelectorAll('#deck > section')];
		const altas = secs.map((s, i) => [i + 1, Math.round(s.getBoundingClientRect().height)]).filter(([, hh]) => hh > innerHeight + 2);
		return {chicos, desborde: document.documentElement.scrollWidth - innerWidth, secciones: secs.length, altas};
	});
	const legible = w !== 1920 || r.chicos.length === 0;
	const ok = legible && r.desborde <= 0 && !errores.length && (w === 390 || r.altas.length === 0);
	if (!ok) fallas++;
	console.log(`${ok ? 'ok ' : 'MAL'} ${w}×${h}: ${r.secciones} láminas · desborde ${r.desborde}px · errores ${errores.length}${w === 1920 ? ` · textos <24px: ${r.chicos.length}` : ''}${r.altas.length && w !== 390 ? ` · láminas más altas que la pantalla: ${r.altas.map((a) => a.join(':')).join(', ')}` : ''}`);
	if (w === 1920 && r.chicos.length) console.log('   ' + r.chicos.slice(0, 12).join('\n   '));
	if (w === 1920) {
		const secs = await p.$$('#deck > section');
		for (let i = 0; i < secs.length; i++) {
			await secs[i].scrollIntoViewIfNeeded();
			await p.waitForTimeout((await secs[i].$('iframe')) ? 2500 : i === secs.length - 1 ? 7600 : 1600);
			await p.screenshot({path: path.join(salida, `lamina-${String(i + 1).padStart(2, '0')}.png`)});
		}
	}
	await p.close();
}
await nav.close();
fs.unlinkSync(tmp);
process.exit(fallas ? 1 : 0);
