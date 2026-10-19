// Puente entre los tokens de @kino/motion y la interfaz: variables CSS, resortes en linear() y animaciones WAAPI.
import {TOKENS} from '../../paquetes/kino-motion/src/tokens.generados';
import {cssBezier} from '../../paquetes/kino-motion/src/nucleo/curvas';

export const D = TOKENS.duracion;
export const C = Object.fromEntries(Object.entries(TOKENS.curva).map(([k, v]) => [k, cssBezier(v as unknown as [number, number, number, number])])) as Record<keyof typeof TOKENS.curva, string>;
export const R = Object.fromEntries(Object.entries(TOKENS.resorte).map(([k, v]) => [k, {linear: v.linear, ms: v.asentamientoMs}])) as Record<keyof typeof TOKENS.resorte, {linear: string; ms: number}>;

export function variablesCss(): string {
	const l: string[] = [];
	for (const [k, v] of Object.entries(D)) l.push(`--d-${k}:${v}ms`);
	for (const [k, v] of Object.entries(C)) l.push(`--c-${k}:${v}`);
	for (const [k, v] of Object.entries(R)) l.push(`--r-${k}:${v.linear};--r-${k}-ms:${v.ms}ms`);
	return `:root{${l.join(';')}}`;
}

export const reducido = () => document.documentElement.dataset.reducido === '1' || matchMedia('(prefers-reduced-motion: reduce)').matches;

/** Anima con WAAPI; con movimiento reducido cambia las escalas y desplazamientos por un fundido corto. */
export function animar(el: Element | null | undefined, frames: Keyframe[], opts: KeyframeAnimationOptions): Animation | undefined {
	if (!el) return;
	if (reducido()) {
		const op = frames.map((f) => ({opacity: f.opacity ?? 1}));
		return el.animate(op.length > 1 ? op : [{opacity: 0}, {opacity: 1}], {duration: Math.min(Number(opts.duration) || 200, D.corto), easing: 'linear', fill: opts.fill});
	}
	return el.animate(frames, opts);
}

export const resorte = (nombre: keyof typeof R) => ({duration: R[nombre].ms, easing: R[nombre].linear});

export function vibrar(patron: number | number[]) {
	try {
		navigator.vibrate?.(patron);
	} catch {
		/* sin háptica */
	}
}

// Continuidad espacial ---------------------------------------------------------------------------------
// Todo se mide en pantalla y se traduce a píxeles del dispositivo, que se dibuja escalado (Escala).
const escalaDe = (el: Element) => {
	const h = el as HTMLElement;
	return h.getBoundingClientRect().width / (h.offsetWidth || 1) || 1;
};

/**
 * Elemento compartido (FLIP): `el` nace donde estaba `desde` y viaja a su lugar con el resorte «pase».
 * Escala uniforme, alineada al centro, para que el contenido (el QR) nunca se deforme.
 */
export function volar(el: HTMLElement | null | undefined, desde: DOMRect | null | undefined, o: {resorte?: keyof typeof R; retraso?: number} = {}) {
	if (!el || !desde) return;
	const a = el.getBoundingClientRect();
	if (!a.width || !a.height) return;
	const k = escalaDe(el);
	const s = Math.min(desde.width / a.width, desde.height / a.height);
	const dx = (desde.left + desde.width / 2 - (a.left + a.width / 2)) / k;
	const dy = (desde.top + desde.height / 2 - (a.top + a.height / 2)) / k;
	const r = R[o.resorte ?? 'pase'];
	return animar(el, [{transform: `translate(${dx}px, ${dy}px) scale(${s})`}, {transform: 'none'}], {duration: r.ms, easing: r.linear, delay: o.retraso ?? 0, fill: 'backwards'});
}

/**
 * Transformación de contenedor (como Material): una forma nace con el tamaño, el radio y el color de `desde`
 * y se convierte en `hacia`; al terminar se funde y deja ver el elemento real. Devuelve cuándo terminó.
 */
export function morfar(desde: DOMRect, hacia: HTMLElement, o: {fondoDesde: string; fondoHacia: string; radioDesde: string; radioHacia: string; capa: HTMLElement}) {
	const k = escalaDe(o.capa);
	const c = o.capa.getBoundingClientRect();
	const b = hacia.getBoundingClientRect();
	const caja = (r: DOMRect) => ({left: `${(r.left - c.left) / k}px`, top: `${(r.top - c.top) / k}px`, width: `${r.width / k}px`, height: `${r.height / k}px`});
	if (reducido()) return Promise.resolve();
	const f = document.createElement('div');
	f.className = 'morfo';
	o.capa.appendChild(f);
	hacia.style.opacity = '0';
	const r = R.pase;
	const a = f.animate(
		[
			{...caja(desde), background: o.fondoDesde, borderRadius: o.radioDesde},
			{...caja(b), background: o.fondoHacia, borderRadius: o.radioHacia},
		],
		{duration: r.ms, easing: r.linear, fill: 'forwards'},
	);
	return a.finished.then(() => {
		hacia.style.opacity = '';
		hacia.animate([{opacity: 0}, {opacity: 1}], {duration: D.instante, easing: 'linear'});
		f.animate([{opacity: 1}, {opacity: 0}], {duration: D.instante, fill: 'forwards'}).finished.then(() => f.remove());
	});
}
