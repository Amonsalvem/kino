// Resorte amortiguado resuelto de forma analítica (sin integrar paso a paso).
// Los parámetros son los mismos de Reanimated withSpring, SwiftUI interpolatingSpring y Compose spring():
// rigidez (stiffness), amortiguación (damping) y masa (mass). Así un resorte se porta igual en web y app.
import type {Easing} from './curvas';

export type Resorte = {rigidez: number; amortiguacion: number; masa: number};

export type Solucion = {
	/** Avance 0 → 1 en el instante t (segundos). Puede pasar de 1 si el resorte rebota. */
	avance: (t: number) => number;
	/** Velocidad del avance (1/s) en t. */
	velocidad: (t: number) => number;
	/** Tiempo (s) desde el que el resorte queda dentro de la tolerancia y casi quieto. */
	asentamiento: number;
	/** Fracción que se pasa del destino (0 si no rebota). */
	rebote: number;
	/** Razón de amortiguación ζ. */
	zeta: number;
	/** Easing normalizado a la duración de asentamiento, para usar como curva. */
	easing: Easing;
};

/**
 * @param v0 velocidad inicial del avance en 1/s (por ejemplo, la del dedo al soltar, dividida por la distancia).
 */
export function resolver({rigidez: k, amortiguacion: c, masa: m}: Resorte, v0 = 0, tolerancia = 0.001): Solucion {
	const w0 = Math.sqrt(k / m);
	const zeta = c / (2 * Math.sqrt(k * m));
	// Desplazamiento respecto del destino: x(0) = 1, x'(0) = -v0. Avance = 1 - x.
	const x0 = 1;
	const dx0 = -v0;
	let x: (t: number) => number;
	let dx: (t: number) => number;
	if (zeta < 1) {
		const wd = w0 * Math.sqrt(1 - zeta * zeta);
		const B = (dx0 + zeta * w0 * x0) / wd;
		x = (t) => Math.exp(-zeta * w0 * t) * (x0 * Math.cos(wd * t) + B * Math.sin(wd * t));
		dx = (t) => {
			const e = Math.exp(-zeta * w0 * t);
			return e * ((B * wd - zeta * w0 * x0) * Math.cos(wd * t) - (x0 * wd + zeta * w0 * B) * Math.sin(wd * t));
		};
	} else if (zeta === 1) {
		const B = dx0 + w0 * x0;
		x = (t) => Math.exp(-w0 * t) * (x0 + B * t);
		dx = (t) => Math.exp(-w0 * t) * (B - w0 * (x0 + B * t));
	} else {
		const s = Math.sqrt(zeta * zeta - 1);
		const r1 = -w0 * (zeta - s);
		const r2 = -w0 * (zeta + s);
		const Bc = (dx0 - r1 * x0) / (r2 - r1);
		const A = x0 - Bc;
		x = (t) => A * Math.exp(r1 * t) + Bc * Math.exp(r2 * t);
		dx = (t) => A * r1 * Math.exp(r1 * t) + Bc * r2 * Math.exp(r2 * t);
	}
	const avance = (t: number) => 1 - x(t);
	const velocidad = (t: number) => -dx(t);
	// Asentamiento: último instante en que el desplazamiento o la velocidad superan la tolerancia (paso de 1 ms, hasta 10 s).
	let asentamiento = 0;
	let rebote = 0;
	for (let t = 0; t <= 10; t += 0.001) {
		const d = x(t);
		if (-d > rebote) rebote = -d;
		if (Math.abs(d) > tolerancia || Math.abs(dx(t)) > tolerancia * 10) asentamiento = t;
	}
	asentamiento = Math.max(asentamiento, 0.001);
	const easing: Easing = (p) => (p <= 0 ? 0 : p >= 1 ? 1 : avance(p * asentamiento));
	return {avance, velocidad, asentamiento, rebote, zeta, easing};
}
