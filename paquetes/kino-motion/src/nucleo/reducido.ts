// Movimiento reducido: un modo alternativo, no un apagado.
// Desplazamientos y escalas pasan a fundidos con la misma duración y el mismo orden; los loops se detienen.
import type {Pista} from './pase';

/** Convierte una pista al modo reducido. Devuelve null si la pista solo desplaza y otra pista ya funde esa parte. */
export function reducirPista(p: Pista, todas: readonly Pista[]): Pista | null {
	if (p.propiedad === 'y' || p.propiedad === 'escala') {
		const yaFunde = todas.some((q) => q.parte === p.parte && q.propiedad === 'opacidad');
		return yaFunde ? null : {parte: p.parte, propiedad: 'opacidad', de: 0, a: 1};
	}
	if (p.propiedad === 'escalaX') {
		// Una línea que se dibuja o una barra que se vacía: aparece o se va por fundido.
		const de = p.de === 'actual' ? 1 : Number(p.de);
		return {parte: p.parte, propiedad: 'opacidad', de: de > 0 ? 1 : 0, a: Number(p.a) > 0 ? 1 : 0};
	}
	return p;
}

export const reducirPistas = (pistas: readonly Pista[]): Pista[] =>
	pistas.map((p) => reducirPista(p, pistas)).filter((p): p is Pista => p !== null);

/** Keyframes de WAAPI en modo reducido: se quitan transformaciones; si no queda nada, se funde. */
export function reducirKeyframes(frames: Keyframe[]): Keyframe[] {
	const sinMover = frames.map((f) => {
		const {transform: _t, translate: _tr, scale: _s, rotate: _r, ...resto} = f as Record<string, unknown>;
		return resto as Keyframe;
	});
	const cambia = sinMover.some((f) => Object.keys(f).some((k) => !['offset', 'easing', 'composite'].includes(k)));
	return cambia ? sinMover : [];
}
