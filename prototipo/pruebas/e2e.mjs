// Recorre el prototipo de punta a punta como lo haría alguien en la sustentación, y guarda capturas.
// Uso: node pruebas/e2e.mjs [carpeta-capturas]
import {createRequire} from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const req = createRequire(import.meta.url);
const raiz = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const pw = req(path.join(raiz, 'gorr-brand-system/node_modules/playwright'));
const archivo = path.resolve(raiz, 'prototipo/build/kino-prototipo.html');
const capturas = path.resolve(process.argv[2] || path.join(raiz, 'prototipo/build/capturas'));
fs.mkdirSync(capturas, {recursive: true});
const cands = fs.existsSync('/opt/pw-browsers') ? fs.readdirSync('/opt/pw-browsers').filter((d) => /^chromium-\d+$/.test(d)).map((d) => `/opt/pw-browsers/${d}/chrome-linux/chrome`) : [];
const nav = await pw.chromium.launch({executablePath: cands.find(fs.existsSync)});
const p = await nav.newPage({viewport: {width: 1920, height: 1080}});
const errores = [];
p.on('pageerror', (e) => errores.push(e.message));
p.on('console', (m) => m.type() === 'error' && !/net::ERR_/.test(m.text()) && errores.push(m.text()));

let fallas = 0;
const ok = async (nombre, f) => {
	try {
		await f();
		console.log(`ok   ${nombre}`);
	} catch (e) {
		fallas++;
		console.log(`MAL  ${nombre}: ${e.message.split('\n')[0]}`);
	}
};
const foto = (n) => p.screenshot({path: path.join(capturas, `${n}.png`)});

await p.goto(`file://${archivo}?actor=todos`);
const R = p.getByRole('region', {name: 'App del residente'});
const V = p.getByRole('region', {name: 'Teléfono de la visita'});
const T = p.getByRole('region', {name: 'Pantalla de portería'});
await foto('00-todos');

await ok('Ingreso por WhatsApp: el código se llena solo', async () => {
	await R.getByRole('button', {name: 'Enviar código'}).click();
	await R.locator('.notificacion').click();
	await R.getByText('Tus Pases').waitFor({timeout: 6000});
});
await foto('01-inicio');

await ok('Volver a invitar: Laura queda precargada', async () => {
	await R.locator('.reciente', {hasText: 'Laura'}).click();
	const v = await R.locator('.hoja input').first().inputValue();
	if (v !== 'Laura Mejía') throw new Error(`precarga: ${v}`);
});
await foto('02-crear');

await ok('Crear Pase: nace Sin confirmar y queda Vigente con el lector', async () => {
	await R.locator('.hoja__pie .accion').click();
	await R.getByText('Pase creado').waitFor();
	await R.locator('.creado .chip--sin-confirmar').waitFor({timeout: 1500});
	await R.locator('.creado .chip--vigente').waitFor({timeout: 5000});
});
await foto('03-creado');

await ok('Compartir: a la visita le llega el Pase', async () => {
	await R.getByRole('button', {name: /Enviar por WhatsApp/}).click();
	await V.getByText('Hola Laura').waitFor();
	await V.locator('.burbuja--pase').click();
	await V.locator('.pase-vivo .chip--vigente').waitFor();
});
await foto('04-visita');
await R.getByRole('button', {name: 'Ver el Pase'}).click();
await R.getByRole('button', {name: 'Volver'}).click();

await ok('Portería: el QR de Laura entra y la talanquera sube', async () => {
	await T.locator('.llegada', {hasText: 'Laura Mejía'}).first().click();
	await T.getByText('Puede entrar').waitFor({timeout: 3000});
});
await ok('El residente recibe el aviso de llegada', async () => {
	await R.locator('.banner', {hasText: 'Laura entró'}).waitFor({timeout: 3000});
});
await ok('El Pase de la visita pasa a Usado', async () => {
	await V.locator('.pase-vivo .chip--usado').waitFor({timeout: 3000});
});
await foto('05-entra');

await ok('Segunda lectura: rechazada con motivo', async () => {
	await p.waitForTimeout(400);
	await T.locator('.llegada', {hasText: 'Laura Mejía'}).first().click();
	await T.getByText('Es de una sola entrada').first().waitFor({timeout: 3000});
});
await ok('Llamar al residente no abre la entrada', async () => {
	await T.getByRole('button', {name: /Llamar a Carolina/}).click();
	await T.getByText('Llamando a Carolina Ruiz').waitFor();
	await T.getByText(/Carolina contestó/).waitFor({timeout: 5000});
});
await foto('06-rechazo');

await ok('Revocar con mantener presionado y deshacer', async () => {
	await R.locator('.banner').waitFor({state: 'detached', timeout: 8000}).catch(() => {});
	await R.locator('.tarjeta', {hasText: 'Andrés Gómez'}).click();
	const b = R.locator('.mantener');
	await b.waitFor();
	const caja = await b.boundingBox();
	await p.mouse.move(caja.x + caja.width / 2, caja.y + caja.height / 2);
	await p.mouse.down();
	await p.waitForTimeout(1000);
	await p.mouse.up();
	await R.getByText('Pase revocado').waitFor();
	await R.locator('.detalle .chip--revocado').first().waitFor();
	await foto('07-revocado');
	await R.getByRole('button', {name: /Deshacer/}).click();
	await R.locator('.detalle .chip--vigente').first().waitFor();
});

await ok('Revocar de verdad: el lector lo rechaza con quién y cuándo', async () => {
	const b = R.locator('.mantener');
	const caja = await b.boundingBox();
	await p.mouse.move(caja.x + caja.width / 2, caja.y + caja.height / 2);
	await p.mouse.down();
	await p.waitForTimeout(1000);
	await p.mouse.up();
	await p.waitForTimeout(5600);
	await T.locator('.llegada', {hasText: 'Andrés Gómez'}).first().click();
	await T.getByText(/Revocado por Carolina Ruiz/).first().waitFor({timeout: 3000});
});

await ok('Administración: bajar el cupo cambia lo que el residente puede crear', async () => {
	await p.getByRole('button', {name: 'Administración', exact: true}).click();
	const A = p.getByRole('region', {name: 'Administración'});
	await A.getByRole('button', {name: 'Límites'}).click();
	for (let i = 0; i < 4; i++) await A.getByRole('button', {name: 'Menos: Visitas activas por casa'}).click();
	await A.getByText('Qué pasaría con este cambio').waitFor();
	await foto('08-limites');
	await A.getByRole('button', {name: 'Guardar límites'}).click();
	await p.getByRole('button', {name: 'Residente', exact: true}).click();
	const R2 = p.getByRole('region', {name: 'App del residente'});
	if (await R2.getByRole('button', {name: 'Volver'}).isVisible()) await R2.getByRole('button', {name: 'Volver'}).click();
	await R2.getByRole('button', {name: /Crear Pase/}).click();
	await R2.locator('.hoja__pie', {hasText: /tope/}).waitFor({timeout: 3000});
	await foto('09-limite-residente');
});

await ok('Integración caída: reintentar con teléfono la recupera', async () => {
	await p.getByRole('button', {name: 'Administración', exact: true}).click();
	const A = p.getByRole('region', {name: 'Administración'});
	await A.getByRole('button', {name: 'Lector e integración'}).click();
	await foto('10-integracion-caida');
	await A.getByRole('button', {name: /Reintentar con teléfono/}).click();
	await A.getByText('312 de 312').waitFor({timeout: 8000});
});
await foto('11-integracion');

await ok('El reloj acelerado no rompe nada', async () => {
	await p.getByRole('button', {name: 'Todos a la vez'}).click();
	await p.getByRole('button', {name: '600×'}).click();
	await p.waitForTimeout(2500);
	await p.getByRole('button', {name: '1×'}).click();
});
await foto('12-tarde');

await ok('Sin errores de consola', async () => {
	if (errores.length) throw new Error(errores.join(' | '));
});

await nav.close();
console.log(fallas ? `${fallas} falla(s)` : 'Todo el recorrido pasó');
process.exit(fallas ? 1 : 0);
