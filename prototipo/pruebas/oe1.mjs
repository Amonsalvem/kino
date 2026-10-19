// Mide OE1 sobre el prototipo: toques reales y tiempo estimado con el modelo KLM (Card, Moran y Newell, 1980)
// para las dos formas de crear un Pase de visita. KLM predice el tiempo de alguien que ya conoce la interfaz;
// no reemplaza una prueba con personas.
// Operadores: M = 1,35 s (decidir), P = 1,1 s (llevar el dedo al objetivo), B = 0,2 s (tocar y soltar),
// K = 0,28 s por carácter (persona promedio). R = espera medida de la interfaz.
// Uso: node pruebas/oe1.mjs  → imprime la tabla y guarda build/oe1.json
import {createRequire} from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const req = createRequire(import.meta.url);
const raiz = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const pw = req(path.join(raiz, 'gorr-brand-system/node_modules/playwright'));
const archivo = path.resolve(raiz, 'prototipo/build/kino-prototipo.html');
const cands = fs.existsSync('/opt/pw-browsers') ? fs.readdirSync('/opt/pw-browsers').filter((d) => /^chromium-\d+$/.test(d)).map((d) => `/opt/pw-browsers/${d}/chrome-linux/chrome`) : [];
const nav = await pw.chromium.launch({executablePath: cands.find(fs.existsSync)});
const M = 1.35, P = 1.1, B = 0.2, K = 0.28;

const tarea = async (nombre, pasos) => {
	const p = await nav.newPage({viewport: {width: 470, height: 940}});
	await p.goto(`file://${archivo}?actor=residente&solo=1`);
	const R = p.locator('.app--residente');
	await R.getByRole('button', {name: 'Enviar código'}).click();
	await R.locator('.notificacion').click();
	await R.getByText('Tus Pases').waitFor({timeout: 6000});
	let toques = 0, caracteres = 0, espera = 0;
	const tocar = async (loc) => {
		toques++;
		await loc.click();
	};
	const escribir = async (loc, texto) => {
		toques++;
		await loc.click();
		await loc.fill(texto);
		caracteres += texto.replace(/\s/g, '').length;
	};
	const esperar = async (f) => {
		const t0 = Date.now();
		await f();
		espera += (Date.now() - t0) / 1000;
	};
	await pasos(R, {tocar, escribir, esperar});
	await p.close();
	// Un M antes de cada toque (decidir qué tocar), P + B por toque, K por carácter.
	const klm = toques * (M + P + B) + caracteres * K + espera;
	return {nombre, toques, caracteres, espera: +espera.toFixed(2), segundos: +klm.toFixed(1)};
};

const filas = [];
filas.push(
	await tarea('Volver a invitar (visita reciente)', async (R, {tocar, esperar}) => {
		await tocar(R.locator('.reciente', {hasText: 'Andrés'}));
		await tocar(R.locator('.hoja__pie .accion'));
		await esperar(() => R.getByText('Pase creado').waitFor());
		await tocar(R.getByRole('button', {name: /Enviar por WhatsApp/}));
	}),
);
filas.push(
	await tarea('Visita nueva', async (R, {tocar, escribir, esperar}) => {
		await tocar(R.getByRole('button', {name: /Crear Pase/}).first());
		await escribir(R.locator('.hoja input').nth(0), 'Sofía Herrera');
		await escribir(R.locator('.hoja input').nth(1), '3125550148');
		await tocar(R.locator('.hoja__pie .accion'));
		await esperar(() => R.getByText('Pase creado').waitFor());
		await tocar(R.getByRole('button', {name: /Enviar por WhatsApp/}));
	}),
);
await nav.close();

let falla = false;
for (const f of filas) {
	const cumple = f.segundos < 30 && (f.nombre.startsWith('Volver') ? f.toques <= 3 : true);
	if (!cumple) falla = true;
	console.log(`${cumple ? 'ok ' : 'MAL'}  ${f.nombre}: ${f.toques} toques, ${f.caracteres} caracteres, ${f.segundos} s (KLM)`);
}
fs.writeFileSync(path.join(raiz, 'prototipo/build/oe1.json'), JSON.stringify(filas, null, 1));
process.exit(falla ? 1 : 0);
