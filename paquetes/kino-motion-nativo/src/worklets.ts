// Funciones que corren en el hilo de UI (worklets). Sin React Native: se prueban en Node.

// Matemática de gestos como worklets (mismas fórmulas que núcleo/gestos.ts; hay una prueba que lo verifica).
export function resistenciaW(exceso: number, dimension: number): number {
	'worklet';
	const c = 0.55;
	return Math.sign(exceso) * (1 - 1 / ((Math.abs(exceso) * c) / dimension + 1)) * dimension;
}
export function proyectarW(pos: number, velocidad: number): number {
	'worklet';
	const d = 0.998;
	return pos + (velocidad / 1000) * (d / (1 - d));
}

/** Cifra con separador de miles «.» (es-CO), en un worklet. */
export function formatoCifra(n: number, decimales = 0): string {
	'worklet';
	const f = Math.pow(10, decimales);
	const r = Math.round(n * f) / f;
	const [entero, dec] = Math.abs(r).toFixed(decimales).split('.');
	let s = '';
	for (let i = 0; i < entero.length; i++) {
		if (i > 0 && (entero.length - i) % 3 === 0) s += '.';
		s += entero[i];
	}
	return (r < 0 ? '-' : '') + s + (dec ? ',' + dec : '');
}

