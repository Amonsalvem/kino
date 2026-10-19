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
