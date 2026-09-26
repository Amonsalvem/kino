// Línea de tiempo por pasos: cada paso dura lo que dice su token, uno tras otro.
import {interpolate} from 'remotion';
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
