// Prueba el visor del Pase 3D en Chromium: carga del GLB con variantes, cada clip visible, modo reducido y consola
// sin errores. three.js se sirve desde un paquete local (THREE_DIR = carpeta «package» de `npm pack three@0.169.0`),
// porque jsdelivr no es alcanzable desde la sandbox.
//
//   THREE_DIR=/ruta/three/package node probar-visor.mjs [carpeta-capturas]
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
import {execSync} from 'node:child_process';
const req = createRequire(import.meta.url);
let pw;
try { pw = req('playwright'); } catch { try { pw = req(path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../../../gorr-brand-system/node_modules/playwright')); } catch { pw = req(path.join(execSync('npm root -g').toString().trim(), 'playwright')); } }
const {chromium} = pw;

const AQUI = path.dirname(fileURLToPath(import.meta.url));
const THREE = process.env.THREE_DIR;
const salida = process.argv[2] || path.join(AQUI, 'capturas');
fs.mkdirSync(salida, {recursive: true});
const navegador = await chromium.launch({executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader']});
const pagina = await navegador.newPage({viewport: {width: 1280, height: 900}});
const errores = [];
// Los videos de la galería se codifican después del render: un archivo local que falta no es un error del visor.
const faltan = [];
pagina.on('requestfailed', (r) => { if (r.url().startsWith('file:') && r.url().includes('/entregables/')) faltan.push(r.url()); });
pagina.on('console', (m) => { if (m.type() === 'error' && !/ERR_FILE_NOT_FOUND/.test(m.text())) errores.push(m.text()); });
pagina.on('pageerror', (e) => errores.push(String(e)));
await pagina.route('https://cdn.jsdelivr.net/npm/three@0.169.0/**', (r) => {
	const rel = new URL(r.request().url()).pathname.replace('/npm/three@0.169.0/', '');
	r.fulfill({path: path.join(THREE, rel), contentType: 'text/javascript'});
});
await pagina.route('https://fonts.googleapis.com/**', (r) => r.fulfill({body: '', contentType: 'text/css'}));
await pagina.route('**/galeria/draco/**', (r) => r.fulfill({path: path.join(AQUI, 'draco', path.basename(new URL(r.request().url()).pathname))}));
await pagina.goto('file://' + path.join(AQUI, 'index.html').replace('/galeria/index.html', '/galeria/index.html'));
await pagina.waitForSelector('#visor-lienzo[data-listo="1"]', {timeout: 60000});
const variantes = await pagina.$eval('#visor-lienzo', (c) => c.dataset.variantes);
const piezas = await pagina.evaluate(() => window.kinoVisor.piezas());
const lienzo = await pagina.$('#visor-lienzo');
await lienzo.scrollIntoViewIfNeeded();
const resultado = {variantes: Number(variantes), piezas, clips: {}};
for (const reducido of [false, true]) {
	await pagina.evaluate((r) => { document.documentElement.dataset.reducido = r ? '1' : '0'; }, reducido);
	for (const clip of ['aparecer', 'confirmar', 'latir', 'avisar', 'caducar', 'usar', 'revocar']) {
		for (const p of [0.5, 1]) {
			await pagina.evaluate(([c, x]) => window.kinoVisor.fijar(c, x), [clip, p]);
			const nombre = `${clip}-${p}${reducido ? '-reducido' : ''}.png`;
			const buf = await lienzo.screenshot({path: path.join(salida, nombre)});
			// ¿Se ve algo? Cuenta píxeles no transparentes/no fondo en la captura.
			const txt = await pagina.$eval('#visor-estado', (e) => e.textContent);
			resultado.clips[`${clip}@${p}${reducido ? ' reducido' : ''}`] = {bytes: buf.length, estado: txt};
		}
	}
}
resultado.errores = errores;
resultado.videos_que_faltan = faltan.length;
console.log(JSON.stringify(resultado, null, 1));
await navegador.close();
process.exit(errores.length ? 1 : 0);
