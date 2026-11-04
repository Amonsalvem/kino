// animar(): Web Animations con tokens, interrumpible y con modo reducido.
import {cssBezier} from '../nucleo/curvas';
import {reducirKeyframes} from './reducido-web';
import {curvaDe, ms, TOKENS, type NombreCurva, type NombreDuracion, type NombreResorte} from '../nucleo/tokens';
import {esReducido, registrar} from './entorno';

export type Opciones = {
	/** Token de duración o verbo ('aparecer/duracion'). Se ignora si hay resorte. */
	duracion?: NombreDuracion;
	/** Duración derivada de un token (por ejemplo, salida()). Tiene prioridad sobre duracion. */
	duracionMs?: number;
	/** Token de curva o verbo ('aparecer/curva'). */
	curva?: NombreCurva;
	/** Resorte del sistema: la duración es la de asentamiento y la curva, su linear(). */
	resorte?: NombreResorte;
	/** Milisegundos antes de empezar (normalmente de escalonar()). */
	retraso?: number;
	iteraciones?: number;
	/** Nombre del canal: una animación nueva en el mismo canal interrumpe la anterior desde donde iba. */
	canal?: string;
	/** Empieza desde el valor actual: se usa solo el último keyframe. */
	desdeActual?: boolean;
	/** Texto para el inspector. */
	etiqueta?: string;
	/** Fuerza el modo (por defecto, esReducido()). */
	reducido?: boolean;
};

const CANAL = Symbol('kino-canal');
type ConCanal = Element & {[CANAL]?: Map<string, Animation>};

/** Parámetros de tiempo de unas opciones, en ms y como easing CSS. */
export function tiempoDe(o: Opciones): {duracion: number; easing: string; tokens: string} {
	if (o.resorte) {
		const r = TOKENS.resorte[o.resorte];
		return {duracion: r.asentamientoMs, easing: r.linear, tokens: `resorte/${o.resorte}`};
	}
	const duracion = o.duracionMs ?? ms(o.duracion ?? 'duracion/corto');
	const curva = o.curva ?? 'curva/crecer';
	const nombre = o.duracionMs !== undefined ? `${o.duracionMs} ms derivados` : o.duracion ?? 'duracion/corto';
	return {duracion, easing: cssBezier(curvaDe(curva)), tokens: `${nombre} · ${curva}`};
}

export function animar(el: Element, frames: Keyframe[], o: Opciones = {}): Animation | null {
	const reducido = o.reducido ?? esReducido();
	const {duracion, easing, tokens} = tiempoDe(o);
	let kf = reducido ? reducirKeyframes(frames) : frames;
	const loop = (o.iteraciones ?? 1) > 1 || o.iteraciones === Infinity;
	const canal = o.canal ? ((el as ConCanal)[CANAL] ??= new Map()) : null;
	const previa = o.canal ? canal!.get(o.canal) : undefined;
	if (previa && previa.playState === 'running') {
		// Interrumpir: fija el valor actual como estilo y cancela; la nueva parte desde ahí.
		try {
			previa.commitStyles();
		} catch {
			/* el elemento no está renderizado */
		}
		previa.cancel();
	}
	if (!kf.length || (reducido && loop)) {
		// Nada que animar en este modo: se aplica el estado final.
		const fin = frames[frames.length - 1];
		if (fin && !loop) aplicarEstilo(el, reducido ? reducirKeyframes([fin])[0] ?? {} : fin);
		registrar(null, {etiqueta: o.etiqueta ?? 'sin animación', elemento: el, duracion: 0, tokens, reducido});
		return null;
	}
	if (o.desdeActual) kf = kf.slice(-1);
	const a = el.animate(kf, {duration: duracion, easing, delay: o.retraso ?? 0, iterations: o.iteraciones ?? 1, fill: 'both'});
	canal?.set(o.canal!, a);
	// Al terminar, el valor final queda como estilo y la animación se libera (no se acumulan efectos «fill»).
	if (!loop) {
		a.addEventListener('finish', () => {
			try {
				a.commitStyles();
			} catch {
				/* sin render */
			}
			a.cancel();
		});
	}
	registrar(a, {etiqueta: o.etiqueta ?? '', elemento: el, duracion: duracion + (o.retraso ?? 0), tokens, reducido});
	return a;
}

function aplicarEstilo(el: Element, f: Keyframe) {
	const s = (el as HTMLElement).style;
	if (!s) return;
	for (const [k, v] of Object.entries(f)) if (!['offset', 'easing', 'composite'].includes(k) && v != null) s.setProperty(k.replace(/[A-Z]/g, (m) => '-' + m.toLowerCase()), String(v));
}

/** Espera a que termine una animación (o resuelve de inmediato si no hubo). */
export const terminada = (a: Animation | null) => (a ? a.finished.then(() => undefined, () => undefined) : Promise.resolve());
