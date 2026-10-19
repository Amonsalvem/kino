// Barrido de diagramación: recorre cada pantalla del prototipo a tamaño real del dispositivo y mide
// texto que se desborda o se corta, hijos fuera de su contenedor, solapes entre hermanos, objetivos táctiles
// menores de 44 px, textos de menos de 12 px y separaciones fuera de la escala de espaciado (4, 8, 12, 16, 24, 32, 48).
// Uso: node pruebas/barrido.mjs [carpeta-capturas]  → imprime hallazgos y guarda una captura por pantalla.
import {createRequire} from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const req = createRequire(import.meta.url);
const raiz = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const pw = req(path.join(raiz, 'gorr-brand-system/node_modules/playwright'));
const archivo = path.resolve(raiz, 'prototipo/build/kino-prototipo.html');
const salida = path.resolve(process.argv[2] || path.join(raiz, 'prototipo/build/barrido'));
fs.mkdirSync(salida, {recursive: true});
const cands = fs.existsSync('/opt/pw-browsers') ? fs.readdirSync('/opt/pw-browsers').filter((d) => /^chromium-\d+$/.test(d)).map((d) => `/opt/pw-browsers/${d}/chrome-linux/chrome`) : [];
const nav = await pw.chromium.launch({executablePath: cands.find(fs.existsSync)});

const medir = () => {
	const raizApp = document.querySelector('.telefono__pantalla, .tableta, .portatil');
	// fijos que tapan contenido del scroll: el último elemento visible queda bajo la barra fija
	const tapa = [];
	const h = [];
	const vis = (el) => {
		const cs = getComputedStyle(el);
		const r = el.getBoundingClientRect();
		return cs.display !== 'none' && cs.visibility !== 'hidden' && +cs.opacity > 0.05 && r.width > 0 && r.height > 0;
	};
	const nombre = (el) => {
		const c = (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '') || el.tagName.toLowerCase();
		const t = (el.innerText || el.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' ').slice(0, 32);
		return `${c}${t ? ` «${t}»` : ''}`;
	};
	const todos = [...raizApp.querySelectorAll('*')].filter((el) => vis(el) && !el.closest('svg') && !el.closest('canvas'));
	// El dispositivo se dibuja escalado: todo se mide en píxeles del diseño, no de pantalla.
	const disp = raizApp.closest('.telefono, .tableta, .portatil') || raizApp;
	const k = disp.getBoundingClientRect().width / disp.offsetWidth || 1;
	const marco = raizApp.getBoundingClientRect();
	for (const el of todos) {
		const cs = getComputedStyle(el);
		const r = el.getBoundingClientRect();
		// texto cortado o desbordado
		const tieneTexto = [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim());
		if (tieneTexto && cs.overflow !== 'visible' && (el.scrollWidth > el.clientWidth + 1 || el.scrollHeight > el.clientHeight + 2) && !/scroll|auto/.test(cs.overflowY))
			h.push(['corte', nombre(el), `${el.scrollWidth}×${el.scrollHeight} en ${el.clientWidth}×${el.clientHeight}`]);
		if (tieneTexto && cs.whiteSpace === 'nowrap' && cs.textOverflow !== 'ellipsis' && el.scrollWidth > el.clientWidth + 1) h.push(['corte', nombre(el), `texto de ${el.scrollWidth} en ${el.clientWidth}`]);
		if (tieneTexto && parseFloat(cs.fontSize) < 12) h.push(['letra', nombre(el), `${cs.fontSize}`]);
		// fuera del dispositivo en horizontal
		if (r.right > marco.right + 1 || r.left < marco.left - 1) if (!el.closest('.recientes,.chips,.capa,.hoja,.sinapsis,.micelio,.escaner,.aurora,.membrana') && !el.matches('.aurora,.membrana')) h.push(['fuera', nombre(el), `x ${Math.round(r.left - marco.left)}..${Math.round(r.right - marco.left)} de ${Math.round(marco.width)}`]);
		// hijo que se sale de su padre con overflow visible y borde o fondo
		const p = el.parentElement;
		if (p && p !== raizApp && vis(p)) {
			const pr = p.getBoundingClientRect();
			const pcs = getComputedStyle(p);
			const caja = pcs.borderTopWidth !== '0px' || pcs.backgroundColor !== 'rgba(0, 0, 0, 0)';
			if (caja && pcs.overflow === 'visible' && (r.right > pr.right + 1 || r.bottom > pr.bottom + 1 || r.left < pr.left - 1) && cs.position !== 'absolute' && cs.position !== 'fixed')
				h.push(['se sale', nombre(el), `de ${nombre(p)}`]);
		}
		// objetivos táctiles
		if (el.matches('button,a,input,[role=tab]') && !el.closest('.notificacion') && (r.height / k < 44 || r.width / k < 44) && !el.matches('.enlace-chat'))
			h.push(['toque', nombre(el), `${Math.round(r.width / k)}×${Math.round(r.height / k)}`]);
	}
	// solapes entre hermanos en flujo
	for (const p of todos) {
		const hijos = [...p.children].filter((c) => vis(c) && c.tagName !== 'svg' && c.tagName !== 'COLGROUP' && !/absolute|fixed/.test(getComputedStyle(c).position));
		for (let i = 0; i < hijos.length; i++)
			for (let j = i + 1; j < hijos.length; j++) {
				const a = hijos[i].getBoundingClientRect();
				const b = hijos[j].getBoundingClientRect();
				const x = Math.min(a.right, b.right) - Math.max(a.left, b.left);
				const y = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
				if (x > 2 && y > 2) h.push(['solape', nombre(hijos[i]), `con ${nombre(hijos[j])} (${Math.round(x / k)}×${Math.round(y / k)})`]);
			}
		// separaciones de flex/grid fuera de escala
		const cs = getComputedStyle(p);
		if (/flex|grid/.test(cs.display)) {
			const g = parseFloat(cs.rowGap) || parseFloat(cs.columnGap) || 0;
			if (g && ![2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 28, 32, 48].includes(Math.round(g))) h.push(['espacio', nombre(p), `gap ${g}px`]);
		}
	}
	const unico = new Map();
	for (const x of h) unico.set(x.join('|'), x);
	return [...unico.values()];
};

const pantallas = [];
const abrir = async (actor, w, h) => {
	const p = await nav.newPage({viewport: {width: w, height: h}, deviceScaleFactor: 2});
	await p.goto(`file://${archivo}?actor=${actor}&solo=1`);
	await p.waitForTimeout(700);
	return p;
};
const registrar = async (p, id) => {
	await p.waitForTimeout(900);
	const hallazgos = await p.evaluate(medir);
	await p.screenshot({path: path.join(salida, `${id}.png`)});
	pantallas.push({id, hallazgos});
};

// Residente
{
	const p = await abrir('residente', 470, 940);
	const R = p.locator('.app--residente');
	await registrar(p, 'R-01-ingreso');
	await R.getByRole('button', {name: 'Enviar código'}).click();
	await registrar(p, 'R-02-codigo');
	await R.locator('.notificacion').click();
	await R.getByText('Tus Pases').waitFor({timeout: 6000});
	await registrar(p, 'R-03-inicio');
	await p.evaluate(() => document.querySelector('.pantalla__scroll').scrollTo(0, 9999));
	await registrar(p, 'R-04-inicio-abajo');
	await R.getByRole('button', {name: /Crear Pase/}).first().click();
	await registrar(p, 'R-05-crear-vacio');
	await R.locator('.reciente').first().waitFor({state: 'attached'}).catch(() => {});
	await p.keyboard.press('Escape');
	await R.locator('.capa__fondo').click({position: {x: 10, y: 10}}).catch(() => {});
	await p.waitForTimeout(500);
	await R.locator('.reciente').nth(1).click();
	await registrar(p, 'R-06-crear-lleno');
	await R.getByRole('tab', {name: 'Colaborador'}).click();
	await registrar(p, 'R-07-crear-colaborador');
	await R.getByRole('tab', {name: 'Visita'}).click();
	await R.locator('.hoja__pie .accion').click();
	await registrar(p, 'R-08-creado');
	await R.getByRole('button', {name: 'Ver el Pase'}).click();
	await registrar(p, 'R-09-detalle');
	await p.evaluate(() => document.querySelector('.detalle .pantalla__scroll').scrollTo(0, 9999));
	await registrar(p, 'R-10-detalle-abajo');
	await R.getByRole('button', {name: 'Volver'}).click();
	await R.getByRole('button', {name: /Avisos/}).click();
	await registrar(p, 'R-11-avisos');
	await R.getByRole('button', {name: /Mi casa/}).click();
	await registrar(p, 'R-12-mi-casa');
	await p.close();
}
// Visita
{
	const p = await abrir('visita', 470, 940);
	const V = p.locator('.app--visita');
	await registrar(p, 'V-01-chat');
	await V.locator('.burbuja--pase').click();
	await registrar(p, 'V-02-pase-vivo');
	await V.getByRole('tab', {name: /Código/}).click();
	await registrar(p, 'V-03-pase-codigo');
	await p.close();
}
// Portería
{
	const p = await abrir('porteria', 1280, 900);
	const T = p.locator('.app--porteria');
	await registrar(p, 'P-01-reposo');
	await T.locator('.llegada').first().click();
	await p.waitForTimeout(250);
	await registrar(p, 'P-02-leyendo');
	await T.getByText(/Puede entrar|No entra/).first().waitFor({timeout: 3000});
	await registrar(p, 'P-03-resultado');
	await T.locator('.llegada', {hasText: 'Andrés'}).first().click();
	await T.getByText(/No entra|Puede entrar/).first().waitFor({timeout: 3000});
	await p.waitForTimeout(400);
	await registrar(p, 'P-04-rechazo');
	await T.getByRole('button', {name: /Digitar código/}).click();
	await registrar(p, 'P-05-teclado');
	await p.close();
}
// Administración
{
	const p = await abrir('administracion', 1440, 940);
	const A = p.locator('.app--admin');
	await registrar(p, 'A-01-resumen');
	await A.getByRole('button', {name: 'Franjas'}).click();
	await registrar(p, 'A-02-limites');
	await A.getByRole('button', {name: 'Lector e integración'}).click();
	await registrar(p, 'A-03-lector');
	await p.close();
}
await nav.close();

let total = 0;
const porTipo = {};
for (const s of pantallas) {
	total += s.hallazgos.length;
	console.log(`\n${s.id} · ${s.hallazgos.length}`);
	for (const [t, n, d] of s.hallazgos) {
		porTipo[t] = (porTipo[t] || 0) + 1;
		console.log(`  ${t.padEnd(8)} ${n} · ${d}`);
	}
}
console.log(`\nTotal ${total} en ${pantallas.length} pantallas · ${JSON.stringify(porTipo)}`);
fs.writeFileSync(path.join(salida, 'barrido.json'), JSON.stringify(pantallas, null, 1));
