// Curvas cúbicas (cubic-bezier) resueltas con precisión y su conversión a la función CSS linear().
// Supuestos: x1 y x2 en [0, 1] (curvas válidas en CSS); precisión de 1e-7 en x.

export type Bezier = readonly [number, number, number, number];
export type Easing = (t: number) => number;

const coef = (p1: number, p2: number) => {
	const c = 3 * p1;
	const b = 3 * (p2 - p1) - c;
	const a = 1 - c - b;
	return {a, b, c};
};

/** Devuelve la función de easing de un cubic-bezier. Newton-Raphson con respaldo por bisección. */
export function bezier([x1, y1, x2, y2]: Bezier): Easing {
	const cx = coef(x1, x2);
	const cy = coef(y1, y2);
	const x = (u: number) => ((cx.a * u + cx.b) * u + cx.c) * u;
	const dx = (u: number) => (3 * cx.a * u + 2 * cx.b) * u + cx.c;
	const y = (u: number) => ((cy.a * u + cy.b) * u + cy.c) * u;
	const resolver = (t: number) => {
		let u = t;
		for (let i = 0; i < 8; i++) {
			const e = x(u) - t;
			if (Math.abs(e) < 1e-7) return u;
			const d = dx(u);
			if (Math.abs(d) < 1e-6) break;
			u -= e / d;
		}
		let lo = 0;
		let hi = 1;
		u = t;
		for (let i = 0; i < 60; i++) {
			const e = x(u) - t;
			if (Math.abs(e) < 1e-7) return u;
			if (e > 0) hi = u;
			else lo = u;
			u = (lo + hi) / 2;
		}
		return u;
	};
	return (t: number) => (t <= 0 ? 0 : t >= 1 ? 1 : y(resolver(t)));
}

export const cssBezier = (b: Bezier) => `cubic-bezier(${b.join(', ')})`;

/**
 * Convierte cualquier easing en la función CSS linear() con los puntos justos para no perder forma
 * (subdivide donde la curva se aparta de la recta). Soportada en Chrome 113, Safari 17.2 y Firefox 112.
 */
export function cssLinear(f: Easing, tolerancia = 0.002, maxPuntos = 120): string {
	const puntos: [number, number][] = [
		[0, f(0)],
		[1, f(1)],
	];
	const dividir = (a: [number, number], b: [number, number], profundidad: number) => {
		const tm = (a[0] + b[0]) / 2;
		const vm = f(tm);
		const recta = (a[1] + b[1]) / 2;
		if (profundidad < 10 && (Math.abs(vm - recta) > tolerancia || profundidad < 3)) {
			const m: [number, number] = [tm, vm];
			puntos.push(m);
			dividir(a, m, profundidad + 1);
			dividir(m, b, profundidad + 1);
		}
	};
	dividir(puntos[0], puntos[1], 0);
	puntos.sort((p, q) => p[0] - q[0]);
	const usados = puntos.length > maxPuntos ? puntos.filter((_, i) => i % Math.ceil(puntos.length / maxPuntos) === 0 || i === puntos.length - 1) : puntos;
	const r = (n: number) => +n.toFixed(4);
	return `linear(${usados.map(([t, v], i) => (i === 0 || i === usados.length - 1 ? `${r(v)}` : `${r(v)} ${r(t * 100)}%`)).join(', ')})`;
}
