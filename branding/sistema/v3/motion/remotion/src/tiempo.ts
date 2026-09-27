// Línea de tiempo por pasos: cada paso dura lo que dice su token, uno tras otro.
import {interpolate} from 'remotion';
import {cambioDeTexto} from '../../../../../../paquetes/kino-motion/src/nucleo/textos';
import {curva, dur} from './tokens';

export type Paso = {id: string; duracion: string; veces?: number};
export type Tramo = {inicio: number; fin: number};

export const lineaDeTiempo = (pasos: Paso[]) => {
	const tramos: Record<string, Tramo> = {};
	let t = 0;
	for (const p of pasos) {
		const d = dur(p.duracion) * (p.veces ?? 1);
		tramos[p.id] = {inicio: t, fin: t + d};
		t += d;
	}
	return {tramos, total: t};
};

/** Avance 0 → 1 de un tramo con la curva del verbo. */
export const avance = (frame: number, tramo: Tramo, nombreCurva: string): number =>
	interpolate(frame, [tramo.inicio, tramo.fin], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
		easing: curva(nombreCurva),
	});

/** Latido: cada ciclo de latir/duracion sube y baja con latir/curva. Devuelve 0 → 1 → 0. */
export const latido = (frame: number, tramo: Tramo): number => {
	if (frame < tramo.inicio || frame >= tramo.fin) return 0;
	const ciclo = dur('latir/duracion');
	const local = (frame - tramo.inicio) % ciclo;
	const mitad = ciclo / 2;
	const f = curva('latir/curva');
	return local < mitad ? f(local / mitad) : f(1 - (local - mitad) / mitad);
};

// Textos que cambian con el estado (M3D-5): la misma regla que la web y la app, leída del núcleo de @kino/motion.

const lineal = (frame: number, tramo: Tramo) => Math.min(1, Math.max(0, (frame - tramo.inicio) / Math.max(1, tramo.fin - tramo.inicio)));

/**
 * Opacidad de un texto que sale (antes → despues) y de uno que entra, en un frame de la transición.
 * a través: el que sale usa la primera mitad y el que entra la segunda, cada mitad con la curva del verbo;
 * solo sale o solo entra: toda la duración; igual (mismo texto, puede cambiar el color): el viejo se queda y el
 * nuevo se funde encima, así el color pasa de uno a otro sin que el texto baje.
 */
export const fundidoDeTexto = (frame: number, tramo: Tramo, nombreCurva: string, antes: string, despues: string): {sale: number; entra: number} => {
	const t = lineal(frame, tramo);
	const e = curva(nombreCurva);
	switch (cambioDeTexto(antes, despues)) {
		case 'a-traves':
			return {sale: 1 - e(Math.min(1, 2 * t)), entra: e(Math.max(0, 2 * t - 1))};
		case 'sale':
			return {sale: 1 - e(t), entra: 0};
		case 'entra':
			return {sale: 0, entra: e(t)};
		default:
			return {sale: t >= 1 ? 0 : 1, entra: e(t)};
	}
};
