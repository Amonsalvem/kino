// Video de revisión de motion: graba cada momento héroe a velocidad real (Playwright recordVideo) y arma una
// tira de fotogramas con ffmpeg para revisarlo cuadro a cuadro.
// Uso: node pruebas/video.mjs [momento…]
// Momentos héroe: porteria, crear, detalle, visita, admin. Resto de la app: estados, ingreso, pestanas, portero, franjas, escenario.
import {createRequire} from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';

const req = createRequire(import.meta.url);
const raiz = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const pw = req(path.join(raiz, 'gorr-brand-system/node_modules/playwright'));
// KINO_HTML y KINO_VIDEOS permiten grabar otra versión (por ejemplo, la anterior) para comparar.
const archivo = path.resolve(process.env.KINO_HTML || path.join(raiz, 'prototipo/build/kino-prototipo.html'));
const salida = path.resolve(process.env.KINO_VIDEOS || path.join(raiz, 'prototipo/build/videos'));
fs.mkdirSync(salida, {recursive: true});
const cands = fs.readdirSync('/opt/pw-browsers').filter((d) => /^chromium-\d+$/.test(d)).map((d) => `/opt/pw-browsers/${d}/chrome-linux/chrome`);
const nav = await pw.chromium.launch({executablePath: cands.find(fs.existsSync), args: ['--autoplay-policy=no-user-gesture-required']});

const telefono = {w: 470, h: 940};
const entrar = async (p) => {
	const R = p.locator('.app--residente');
	await R.getByRole('button', {name: 'Enviar código'}).click();
	await R.locator('.notificacion').click();
	await R.getByText('Tus Pases').waitFor({timeout: 6000});
	await p.waitForTimeout(900);
	return R;
};

const MOMENTOS = {
	porteria: {actor: 'porteria', w: 1080, h: 760, async correr(p) {
		const T = p.locator('.app--porteria');
		await p.waitForTimeout(800);
		await T.locator('.llegada', {hasText: 'Andrés'}).first().click();
		await p.waitForTimeout(5600);
		await T.locator('.llegada', {hasText: 'Juan Pablo'}).first().click();
		await p.waitForTimeout(3200);
	}},
	crear: {actor: 'residente', ...telefono, async correr(p) {
		const R = await entrar(p);
		await R.locator('.reciente', {hasText: 'Laura'}).click();
		await p.waitForTimeout(900);
		await R.locator('.hoja__pie .accion').click();
		await p.waitForTimeout(4200);
	}},
	detalle: {actor: 'residente', ...telefono, async correr(p) {
		const R = await entrar(p);
		await R.locator('.tarjeta').first().click();
		await p.waitForTimeout(1600);
		await R.getByRole('button', {name: 'Volver'}).click();
		await p.waitForTimeout(1400);
		await R.getByRole('button', {name: /Avisos/}).click();
		await p.waitForTimeout(700);
		await R.getByRole('button', {name: /Pases/}).first().click();
		await p.waitForTimeout(900);
	}},
	visita: {actor: 'visita', ...telefono, async correr(p) {
		const V = p.locator('.app--visita');
		await p.waitForTimeout(900);
		await V.locator('.burbuja--pase').click();
		await p.waitForTimeout(1500);
		await p.mouse.move(235, 400, {steps: 10});
		await p.mouse.move(330, 560, {steps: 20});
		await p.mouse.move(140, 520, {steps: 20});
		await p.waitForTimeout(800);
	}},
	admin: {actor: 'administracion', w: 1280, h: 800, async correr(p) {
		const A = p.locator('.app--admin');
		await p.waitForTimeout(600);
		await A.getByRole('button', {name: 'Lector e integración'}).click();
		await p.waitForTimeout(900);
		await A.getByRole('button', {name: /Reintentar/}).click();
		await p.waitForTimeout(6000);
	}},
	// El ciclo del Pase sobre el detalle: sin confirmar → vigente, extender, revocar y deshacer.
	estados: {actor: 'residente', ...telefono, async correr(p) {
		const R = await entrar(p);
		await R.locator('.reciente', {hasText: 'Laura'}).click();
		await p.waitForTimeout(700);
		await R.locator('.hoja__pie .accion').click();
		await p.waitForTimeout(900);
		await R.getByRole('button', {name: 'Ver el Pase'}).click();
		await p.waitForTimeout(3200);
		await R.getByRole('button', {name: '+1 h'}).click();
		await p.waitForTimeout(1200);
		const b = await R.locator('.mantener').boundingBox();
		await p.mouse.move(b.x + b.width / 2, b.y + b.height / 2);
		await p.mouse.down();
		await p.waitForTimeout(1000);
		await p.mouse.up();
		await p.waitForTimeout(1600);
		await R.getByRole('button', {name: /Deshacer/}).click();
		await p.waitForTimeout(1600);
	}},
	ingreso: {actor: 'residente', ...telefono, async correr(p) {
		const R = p.locator('.app--residente');
		await p.waitForTimeout(700);
		await R.getByRole('button', {name: 'Enviar código'}).click();
		await p.waitForTimeout(1500);
		await R.locator('.notificacion').click();
		await R.getByText('Tus Pases').waitFor({timeout: 6000});
		await p.waitForTimeout(1600);
	}},
	pestanas: {actor: 'residente', ...telefono, async correr(p) {
		const R = await entrar(p);
		await R.getByRole('button', {name: /Avisos/}).click();
		await p.waitForTimeout(900);
		await R.getByRole('button', {name: /Mi casa/}).click();
		await p.waitForTimeout(900);
		await R.getByRole('button', {name: /Pases/}).first().click();
		await p.waitForTimeout(900);
		await R.getByRole('button', {name: /Crear Pase/}).first().click();
		await p.waitForTimeout(700);
		await R.getByRole('tab', {name: 'Colaborador'}).click();
		await p.waitForTimeout(900);
		await R.getByRole('tab', {name: 'Visita'}).click();
		await p.waitForTimeout(500);
		await R.getByRole('radio', {name: 'Se queda'}).click();
		await p.waitForTimeout(1200);
	}},
	portero: {actor: 'porteria', w: 1080, h: 760, async correr(p) {
		const T = p.locator('.app--porteria');
		await p.waitForTimeout(600);
		await T.getByRole('button', {name: 'Digitar código'}).click();
		await p.waitForTimeout(800);
		await T.getByRole('button', {name: 'Digitar placa'}).click();
		await p.waitForTimeout(800);
		await T.getByRole('button', {name: 'Digitar placa'}).click();
		await p.waitForTimeout(600);
		await T.locator('.llegada', {hasText: 'Juan Pablo'}).first().click();
		await p.waitForTimeout(2200);
		await T.getByRole('button', {name: /Llamar a/}).click();
		await p.waitForTimeout(3600);
	}},
	franjas: {actor: 'administracion', w: 1280, h: 800, async correr(p) {
		const A = p.locator('.app--admin');
		await p.waitForTimeout(500);
		await A.getByRole('button', {name: 'Franjas'}).click();
		await p.waitForTimeout(800);
		for (let i = 0; i < 3; i++) {
			await A.getByRole('button', {name: 'Más: Desde'}).first().click();
			await p.waitForTimeout(350);
		}
		await p.waitForTimeout(600);
		await A.getByRole('button', {name: 'Guardar franjas'}).click();
		await p.waitForTimeout(1200);
		await A.getByRole('button', {name: 'Resumen'}).click();
		await p.waitForTimeout(1200);
	}},
	escenario: {actor: 'todos', w: 1600, h: 900, async correr(p) {
		await p.waitForTimeout(900);
		await p.getByRole('button', {name: 'Residente', exact: true}).click();
		await p.waitForTimeout(1200);
		await p.getByRole('button', {name: 'Portería', exact: true}).click();
		await p.waitForTimeout(1200);
		await p.getByRole('button', {name: 'Notas'}).click();
		await p.waitForTimeout(900);
		await p.getByRole('button', {name: 'Notas'}).click();
		await p.waitForTimeout(900);
	}, url: '?actor=todos'},
};

const pedidos = process.argv.slice(2).length ? process.argv.slice(2) : Object.keys(MOMENTOS);
for (const nombre of pedidos) {
	const m = MOMENTOS[nombre];
	const ctx = await nav.newContext({viewport: {width: m.w, height: m.h}, recordVideo: {dir: salida, size: {width: m.w, height: m.h}}});
	const p = await ctx.newPage();
	await p.goto(`file://${archivo}${m.url ?? `?actor=${m.actor}&solo=1`}`);
	await m.correr(p);
	const v = p.video();
	await ctx.close();
	const destino = path.join(salida, `${nombre}.webm`);
	fs.renameSync(await v.path(), destino);
	const tira = path.join(salida, `${nombre}-tira.png`);
	execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', destino, '-vf', `fps=5,scale=${m.w > 600 ? 360 : 180}:-1,drawtext=text='%{pts\\:hms}':x=4:y=4:fontsize=12:fontcolor=white,tile=8x6`, '-frames:v', '1', tira]);
	console.log(`ok ${nombre} → ${path.relative(raiz, destino)} · ${path.relative(raiz, tira)}`);
}
await nav.close();
