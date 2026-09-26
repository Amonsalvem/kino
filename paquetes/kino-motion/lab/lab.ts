// Kino Motion Lab: conecta la página con el sistema. Todo lo que se mueve pasa por el núcleo y el runtime web.
import {
	cssBezier, cssLinear, curvaDe, escalonar, eventosDesde, ms, reducirPistas, resolver, TOKENS, TRANSICIONES,
	type Estado, type Evento, type Resorte,
} from '../src/nucleo';
import {entrar, esReducido, montarInspector, obtenerVelocidad, registrar, transicionDeVista, type KinoAviso, type KinoHoja, type KinoLista, type KinoPase} from '../src/web';

const $ = <T extends HTMLElement = HTMLElement>(s: string) => document.querySelector(s) as T;
const min = (m: number) => new Date(Date.now() + m * 60_000).toISOString();
const horaCorta = (d = new Date()) => d.toLocaleTimeString('es-CO', {hour: 'numeric', minute: '2-digit'});

// Tema: el visor de artefactos usa data-theme; los tokens de Kino, data-tema.
const raiz = document.documentElement;
const tema = () => {
	const t = raiz.getAttribute('data-theme');
	if (t === 'light') raiz.dataset.tema = 'claro';
	else if (t === 'dark') raiz.dataset.tema = 'oscuro';
	else raiz.removeAttribute('data-tema');
};
new MutationObserver(tema).observe(raiz, {attributes: true, attributeFilter: ['data-theme']});
tema();
montarInspector();

// 01 · El Pase ------------------------------------------------------------------------------------------------
const pase = $<KinoPase>('#pase-vivo');
const NOMBRE_EVENTO: Record<Evento, string> = {enviar: 'Enviar al lector', confirmar: 'El lector confirma', avisar: 'Entra en aviso', caducar: 'Vence', usar: 'Se usa en la puerta', revocar: 'Revocar'};
function reiniciarPase() {
	for (const a of ['lector', 'confirmado', 'enviado', 'revoco', 'revocado', 'usado']) pase.removeAttribute(a);
	Object.entries({quien: 'Andrés Gómez', casa: 'Casa 14', desde: min(-20), hasta: min(100), estado: 'previsto'}).forEach(([k, v]) => pase.setAttribute(k, v));
	$('#pase-deja').textContent = '';
	botonesPase();
}
function botonesPase() {
	const cont = $('#pase-eventos');
	cont.innerHTML = '';
	const posibles = new Set(eventosDesde(pase.estadoHonesto));
	for (const ev of Object.keys(NOMBRE_EVENTO) as Evento[]) {
		const b = document.createElement('button');
		b.className = 'b';
		b.type = 'button';
		b.textContent = NOMBRE_EVENTO[ev];
		b.disabled = !posibles.has(ev);
		b.addEventListener('click', () => {
			pase.aplicar(ev, {lector: 'Lector Portería', autor: 'Carolina Ruiz'});
			botonesPase();
		});
		cont.append(b);
	}
}
pase.addEventListener('transicion', (e) => {
	const {evento, a, deja} = (e as CustomEvent).detail as {evento: Evento; a: Estado; deja: string};
	const t = TRANSICIONES.find((x) => x.evento === evento && x.a === a)!;
	const pistas = esReducido() ? reducirPistas(t.pistas) : t.pistas;
	const dur = ms(t.duracion);
	const p = $('#partitura');
	p.innerHTML = `<div class="titulo"><span>${evento} → ${a}${esReducido() ? ' · reducido' : ''}</span><span>${t.duracion} · ${t.curva} · ${dur} ms</span></div>`;
	for (const x of pistas) {
		const fila = document.createElement('div');
		fila.className = 'pista';
		fila.innerHTML = `<span></span><span class="carril"><span class="tramo"></span><span class="cabezal"></span></span>`;
		fila.children[0].textContent = `${x.parte} · ${x.propiedad}`;
		p.append(fila);
		// El cabezal marca el tiempo real de la transición (lineal a propósito: es un reloj).
		const a2 = fila.querySelector('.cabezal')!.animate([{left: '0%'}, {left: '100%'}], {duration: dur, easing: 'linear', fill: 'forwards'}); // motion-ok: reloj de la partitura
		a2.playbackRate = obtenerVelocidad(); // sigue la cámara lenta, pero no se registra: no es motion del sistema
	}
	if (t.late) p.insertAdjacentHTML('beforeend', `<div class="nota">Al terminar: el punto late ${TOKENS.latirCiclos} veces (latir/duracion · latir/curva) y se queda quieto.</div>`);
	$('#pase-deja').innerHTML = `<span class="deja">Deja en pantalla:</span> ${deja}`;
});
$('#pase-reiniciar').addEventListener('click', reiniciarPase);
$('#pase-forzar').addEventListener('click', () => {
	reiniciarPase();
	pase.setAttribute('estado', 'vigente');
	$('#pase-deja').innerHTML = '<span class="deja">El componente se negó:</span> sin la confirmación del lector no hay «vigente». Muestra «sin confirmar» y lo avisa en la consola.';
	botonesPase();
});
reiniciarPase();

// 02 · Lista --------------------------------------------------------------------------------------------------
const lista = $<KinoLista>('#lista-pases');
const PERSONAS = [
	{quien: 'Luz Marina', casa: 'Casa 3', estado: 'vigente', hasta: 70},
	{quien: 'Técnico del gas', casa: 'Casa 22', estado: 'sin-confirmar', hasta: 150},
	{quien: 'Diana Arango', casa: 'Casa 9', estado: 'por-vencer', hasta: 18},
	{quien: 'Jardinería', casa: 'Casa 31', estado: 'previsto', hasta: 300},
];
const EXTRA = ['Mateo Rincón', 'Paula Vélez', 'Domicilio', 'Samuel Ortiz', 'Valentina Ruiz'];
const nuevoPase = (d: {quien: string; casa: string; estado: string; hasta: number}) => {
	const el = document.createElement('kino-pase');
	Object.entries({quien: d.quien, casa: d.casa, estado: d.estado, desde: min(-30), hasta: min(d.hasta), enviado: min(-12)}).forEach(([k, v]) => el.setAttribute(k, String(v)));
	if (d.estado === 'vigente' || d.estado === 'por-vencer') {
		el.setAttribute('lector', 'Lector Portería');
		el.setAttribute('confirmado', min(-9));
	}
	return el;
};
PERSONAS.forEach((p) => lista.append(nuevoPase(p)));
lista.entrarTodo();
let extra = 0;
$('#l-agregar').addEventListener('click', () => lista.insertar(nuevoPase({quien: EXTRA[extra++ % EXTRA.length], casa: `Casa ${10 + extra}`, estado: 'previsto', hasta: 40 + extra * 25})));
$('#l-quitar').addEventListener('click', () => lista.firstElementChild && lista.quitar(lista.firstElementChild));
$('#l-ordenar').addEventListener('click', () => lista.ordenar((a, b) => Date.parse(a.getAttribute('hasta')!) - Date.parse(b.getAttribute('hasta')!)));
$('#l-entrar').addEventListener('click', () => lista.entrarTodo());

// 03 · Tocar --------------------------------------------------------------------------------------------------
const hoja = $<KinoHoja>('#hoja');
const paseHoja = $('#pase-hoja');
Object.entries({quien: 'Andrés Gómez', casa: 'Casa 14', estado: 'vigente', desde: min(-20), hasta: min(100), lector: 'Lector Portería', confirmado: min(-18)}).forEach(([k, v]) => paseHoja.setAttribute(k, v));
$('#abrir-hoja').addEventListener('click', () => hoja.abrir());
$('#cerrar-hoja').addEventListener('click', () => hoja.cerrar());
$('#aviso-btn').addEventListener('click', () => $<KinoAviso>('#avisos').mostrar(`Pase enviado a Andrés · ${horaCorta()}. Espera la confirmación del lector.`));
const conf = $('#conf');
$('#num-mas').addEventListener('click', () => conf.setAttribute('valor', String(Math.min(8, Number(conf.getAttribute('valor')) + 1))));
$('#num-reset').addEventListener('click', () => conf.setAttribute('valor', '3'));

// 04 · Espera -------------------------------------------------------------------------------------------------
const reiniciarEspera = () => {
	const vieja = $('#espera-vivo');
	const nueva = document.createElement('kino-espera-lector');
	nueva.id = 'espera-vivo';
	nueva.setAttribute('lector', 'Lector Portería');
	nueva.setAttribute('enviado', min(-2));
	vieja.replaceWith(nueva);
};
reiniciarEspera();
$('#e-confirmar').addEventListener('click', () => $('#espera-vivo').setAttribute('confirmado', new Date().toISOString()));
$('#e-reiniciar').addEventListener('click', reiniciarEspera);

// 05 · Pantallas ----------------------------------------------------------------------------------------------
const pantalla = $('#tel-pantalla');
const volver = $('#tel-volver');
const TEL = [
	{quien: 'Andrés Gómez', casa: 'Casa 14', estado: 'vigente', hasta: 100},
	{quien: 'Técnico del gas', casa: 'Casa 14', estado: 'sin-confirmar', hasta: 180},
	{quien: 'Empleada · Rosa', casa: 'Casa 14', estado: 'previsto', hasta: 480},
];
function vistaLista() {
	$('#tel-titulo').textContent = 'Pases de la Casa 14';
	volver.hidden = true;
	pantalla.innerHTML = '';
	TEL.forEach((d, i) => {
		const el = nuevoPase(d);
		el.style.viewTransitionName = `pase-${i}`;
		el.addEventListener('click', () => transicionDeVista(() => vistaDetalle(i), 'adelante'));
		pantalla.append(el);
	});
}
function vistaDetalle(i: number) {
	$('#tel-titulo').textContent = 'Detalle del Pase';
	volver.hidden = false;
	pantalla.innerHTML = '';
	const el = nuevoPase(TEL[i]);
	el.style.viewTransitionName = `pase-${i}`;
	const dl = document.createElement('div');
	dl.className = 'detalle';
	dl.innerHTML = `<dl><dt>Autor</dt><dd>Carolina Ruiz</dd><dt>Motivo</dt><dd>Visita</dd><dt>Modo</dt><dd>Placa KMN 305</dd><dt>Vence</dt><dd>${horaCorta(new Date(min(TEL[i].hasta)))}</dd></dl>`;
	pantalla.append(el, dl);
	entrar(dl, TOKENS.escalonado.tarjetas);
}
volver.addEventListener('click', () => transicionDeVista(vistaLista, 'atras'));
vistaLista();

// 06 · Resortes -----------------------------------------------------------------------------------------------
const lienzo = $<HTMLCanvasElement>('#res-canvas');
const k = $<HTMLInputElement>('#res-k');
const c = $<HTMLInputElement>('#res-c');
const m = $<HTMLInputElement>('#res-m');
let pestana = 'CSS';
const colorVar = (v: string) => getComputedStyle(raiz).getPropertyValue(v).trim() || '#888';
function presets() {
	const cont = $('#res-presets');
	for (const [nombre, r] of Object.entries(TOKENS.resorte)) {
		const b = document.createElement('button');
		b.className = 'b';
		b.type = 'button';
		b.textContent = `resorte/${nombre}`;
		b.addEventListener('click', () => {
			k.value = String(r.rigidez);
			c.value = String(r.amortiguacion);
			m.value = String(r.masa);
			resortes();
		});
		cont.append(b);
	}
	const tabs = $('#res-tabs');
	for (const t of ['CSS', 'Web', 'Reanimated', 'SwiftUI', 'Compose', 'Token']) {
		const b = document.createElement('button');
		b.className = 'b';
		b.type = 'button';
		b.textContent = t;
		b.addEventListener('click', () => {
			pestana = t;
			resortes();
		});
		tabs.append(b);
	}
	k.value = String(TOKENS.resorte.pase.rigidez);
	c.value = String(TOKENS.resorte.pase.amortiguacion);
	m.value = String(TOKENS.resorte.pase.masa);
}
function resortes() {
	const r: Resorte = {rigidez: +k.value, amortiguacion: +c.value, masa: +m.value};
	$('#res-k-o').textContent = k.value;
	$('#res-c-o').textContent = c.value;
	$('#res-m-o').textContent = m.value;
	const s = resolver(r);
	const ok = s.rebote <= 0.03;
	const v = $('#res-veredicto');
	v.dataset.ok = String(ok);
	const pct = (s.rebote * 100).toLocaleString('es-CO', {maximumFractionDigits: 1});
	v.textContent = ok
		? `Cumple la regla de marca: rebote de ${pct} %, se asienta en ${Math.round(s.asentamiento * 1000)} ms (ζ ${s.zeta.toFixed(2)}).`
		: `No cumple: rebota ${pct} % y el máximo es 3 %. Sube la amortiguación (ζ ${s.zeta.toFixed(2)}; hace falta 0,75 o más).`;
	document.querySelectorAll('#res-tabs .b').forEach((b) => b.setAttribute('aria-pressed', String(b.textContent === pestana)));
	const msA = Math.round(s.asentamiento * 1000);
	const lin = cssLinear(s.easing);
	const codigo: Record<string, string> = {
		CSS: `.pase {\n  transition: transform ${msA}ms ${lin.length > 160 ? lin.slice(0, 160) + '…)' : lin};\n}\n/* En el sistema: var(--kino-mov-resorte-<nombre>) y var(--kino-mov-resorte-<nombre>-duracion) */`,
		Web: `import {animar, animarResorte} from '@kino/motion';\n\n// Con un token:\nanimar(el, [{transform: 'none'}], {resorte: 'pase', desdeActual: true});\n\n// Desde un gesto (continúa la velocidad del dedo):\nanimarResorte({de: y, a: 0, velocidad: vy, resorte: 'hoja', alCambiar: (v) => pintar(v)});`,
		Reanimated: `import {withSpring} from 'react-native-reanimated';\n\noffset.value = withSpring(0, {\n  stiffness: ${r.rigidez},\n  damping: ${r.amortiguacion},\n  mass: ${r.masa},\n  velocity: gesto.velocityY,\n});`,
		SwiftUI: `withAnimation(.interpolatingSpring(\n  mass: ${r.masa},\n  stiffness: ${r.rigidez},\n  damping: ${r.amortiguacion},\n  initialVelocity: 0\n)) {\n  estado = .vigente\n}`,
		Compose: `animateFloatAsState(\n  targetValue = destino,\n  animationSpec = spring(\n    dampingRatio = ${s.zeta.toFixed(3)}f,\n    stiffness = ${(r.rigidez / r.masa).toFixed(1)}f\n  )\n)`,
		Token: JSON.stringify({'<nombre>': {$value: {rigidez: r.rigidez, amortiguacion: r.amortiguacion, masa: r.masa}, $description: `ζ ${s.zeta.toFixed(3)} · ${msA} ms · rebote ${pct} %`}}, null, 2),
	};
	$('#res-codigo').textContent = codigo[pestana];
	dibujar(s);
	$('#res-probar').dataset.easing = lin;
	$('#res-probar').dataset.ms = String(msA);
}
function dibujar(s: ReturnType<typeof resolver>) {
	const dpr = Math.min(devicePixelRatio || 1, 2);
	const W = lienzo.clientWidth || 720;
	const H = Math.round(W * 0.55);
	lienzo.width = W * dpr;
	lienzo.height = H * dpr;
	lienzo.style.height = `${H}px`;
	const g = lienzo.getContext('2d')!;
	g.scale(dpr, dpr);
	const pad = {l: 44, r: 14, t: 16, b: 30};
	const T = Math.max(s.asentamiento * 1.25, 0.3);
	const X = (t: number) => pad.l + (t / T) * (W - pad.l - pad.r);
	const Y = (v: number) => pad.t + (1 - v / 1.25) * (H - pad.t - pad.b);
	g.font = '11px JetBrains Mono, monospace';
	g.fillStyle = colorVar('--kino-texto-tenue');
	g.strokeStyle = colorVar('--kino-superficie-membrana');
	g.lineWidth = 1;
	for (const v of [0, 0.5, 1]) {
		g.beginPath();
		g.moveTo(pad.l, Y(v));
		g.lineTo(W - pad.r, Y(v));
		g.stroke();
		g.fillText(v.toFixed(1), 8, Y(v) + 4);
	}
	const paso = T > 1.2 ? 0.5 : 0.2;
	for (let t = 0; t <= T + 1e-9; t += paso) g.fillText(`${Math.round(t * 1000)}`, X(t) - 10, H - 10);
	// Límite de marca: 3 % de rebote
	g.setLineDash([4, 4]);
	g.strokeStyle = colorVar('--kino-estado-por-vencer-borde');
	g.beginPath();
	g.moveTo(pad.l, Y(1.03));
	g.lineTo(W - pad.r, Y(1.03));
	g.stroke();
	g.fillStyle = colorVar('--kino-estado-por-vencer-texto');
	g.fillText('máximo de marca · 3 %', W - pad.r - 150, Y(1.03) - 6);
	// Asentamiento
	g.strokeStyle = colorVar('--kino-texto-tenue');
	g.beginPath();
	g.moveTo(X(s.asentamiento), pad.t);
	g.lineTo(X(s.asentamiento), H - pad.b);
	g.stroke();
	g.setLineDash([]);
	g.fillStyle = colorVar('--kino-texto-secundario');
	g.fillText(`asienta · ${Math.round(s.asentamiento * 1000)} ms`, Math.min(X(s.asentamiento) + 6, W - 150), pad.t + 12);
	// Curva
	g.strokeStyle = colorVar('--kino-accion-fondo');
	g.lineWidth = 2.5;
	g.beginPath();
	for (let i = 0; i <= 300; i++) {
		const t = (i / 300) * T;
		const px = X(t);
		const py = Y(s.avance(t));
		if (i === 0) g.moveTo(px, py);
		else g.lineTo(px, py);
	}
	g.stroke();
}
presets();
for (const el of [k, c, m]) el.addEventListener('input', resortes);
addEventListener('resize', resortes);
resortes();
const correr = (caja: HTMLElement, easing: string, dur: number, etiqueta: string) => {
	const bola = caja.querySelector('.bola') as HTMLElement;
	const ancho = (caja.querySelector('.riel') as HTMLElement).clientWidth - 14;
	const a = bola.animate([{transform: 'translateX(0)'}, {transform: `translateX(${ancho}px)`}], {duration: dur, easing, fill: 'forwards'});
	registrar(a, {etiqueta, elemento: bola, duracion: dur, tokens: etiqueta, reducido: false});
};
$('#res-probar').addEventListener('click', (e) => {
	const caja = e.currentTarget as HTMLElement;
	correr(caja, caja.dataset.easing!, Number(caja.dataset.ms), 'resorte de prueba');
});

// 07 · Coreografía --------------------------------------------------------------------------------------------
const coreoN = $<HTMLInputElement>('#coreo-n');
function coreografia() {
	const n = +coreoN.value;
	$('#coreo-n-o').textContent = String(n);
	const r = escalonar(n);
	const dur = ms('aparecer/duracion');
	const total = Math.max(...r) + dur;
	const cont = $('#coreo');
	cont.innerHTML = '';
	r.forEach((retraso, i) => {
		const fila = document.createElement('div');
		fila.className = 'coreo-fila';
		fila.innerHTML = `<span>${i + 1}</span><span class="c"><span class="t"></span></span>`;
		const t = fila.querySelector('.t') as HTMLElement;
		t.style.left = `${(retraso / total) * 100}%`;
		t.style.width = `${(dur / total) * 100}%`;
		cont.append(fila);
		entrar(fila, retraso);
	});
	$('#coreo-total').textContent = `La última tarjeta empieza a los ${Math.max(...r)} ms; todo termina a los ${total} ms. Paso efectivo: ${n > 1 ? r[1] : 0} ms (token: ${TOKENS.escalonado.tarjetas} ms, tope ${TOKENS.coreografia.cascadaTopeMs} ms).`;
}
let espera = 0;
coreoN.addEventListener('input', () => {
	clearTimeout(espera);
	espera = window.setTimeout(coreografia, 180);
});
coreografia();

// 08 · Curvas y tokens ----------------------------------------------------------------------------------------
const USO: Record<string, [string, string]> = {
	crecer: ['aparecer/duracion', 'Algo llega: un Pase, una tarjeta.'],
	decaer: ['caducar/duracion', 'Algo se apaga solo: la vigencia.'],
	latir: ['latir/duracion', 'Lo que está vivo: el punto vigente.'],
	revocar: ['revocar/duracion', 'Alguien cortó el Pase.'],
	cortina: ['duracion/cortina', 'Abrir, en presentaciones.'],
	salir: ['aparecer/duracion', 'Lo que se va (60 % de entrar).'],
};
const cont = $('#curvas-lista');
for (const [nombre, valor] of Object.entries(TOKENS.curva)) {
	const [durTok, uso] = USO[nombre] ?? ['duracion/corto', ''];
	const d = nombre === 'salir' ? Math.round(ms('aparecer/duracion') * TOKENS.coreografia.salidaFactor) : ms(durTok as never);
	const caja = document.createElement('div');
	caja.className = 'curva';
	caja.innerHTML = `<h3>curva/${nombre}</h3><span class="nota">${cssBezier(valor as never)} · ${d} ms</span><span style="color:var(--kino-texto-secundario);font-size:14px">${uso}</span><div class="riel"><span class="bola"></span></div>`;
	caja.addEventListener('click', () => correr(caja, cssBezier(curvaDe(`curva/${nombre}` as never)), d, `curva/${nombre}`));
	cont.append(caja);
}
for (const [nombre, r] of Object.entries(TOKENS.resorte)) {
	const caja = document.createElement('div');
	caja.className = 'curva';
	caja.innerHTML = `<h3>resorte/${nombre}</h3><span class="nota">k ${r.rigidez} · c ${r.amortiguacion} · m ${r.masa} · ζ ${r.zeta} · ${r.asentamientoMs} ms</span><div class="riel"><span class="bola"></span></div>`;
	caja.addEventListener('click', () => correr(caja, r.linear, r.asentamientoMs, `resorte/${nombre}`));
	cont.append(caja);
}
const filas: string[] = [];
for (const [n, v] of Object.entries(TOKENS.duracion)) filas.push(`<tr><td><code>duracion/${n}</code></td><td class="dato">${v} ms</td><td class="dato">${Math.floor((v * 60) / 1000 + 0.5)} frames</td><td><code>--kino-mov-duracion-${n}</code></td></tr>`);
for (const [n, v] of Object.entries(TOKENS.escalonado)) filas.push(`<tr><td><code>escalonado/${n}</code></td><td class="dato">${v} ms</td><td class="dato">${Math.floor((v * 60) / 1000 + 0.5)} frames</td><td><code>--kino-mov-escalonado-${n}</code></td></tr>`);
for (const [n, r] of Object.entries(TOKENS.resorte)) filas.push(`<tr><td><code>resorte/${n}</code></td><td class="dato">${r.asentamientoMs} ms</td><td class="dato">rebote ${(r.rebote * 100).toFixed(1)} %</td><td><code>--kino-mov-resorte-${n}</code></td></tr>`);
for (const [v, d] of Object.entries(TOKENS.verbo)) filas.push(`<tr><td><code>${v}</code></td><td colspan="2">→ <code>${d}</code></td><td><code>--kino-mov-${v.replace('/', '-')}</code></td></tr>`);
$('#tabla-tokens').innerHTML = `<thead><tr><th>Token</th><th>Valor</th><th>A 60 fps</th><th>Variable CSS</th></tr></thead><tbody>${filas.join('')}</tbody>`;
