// Textos que cambian con el estado (chip, dato, nota). Decisión M3D-5 (Nico, 27 sep: A): fundido a través.
// Si un texto sale y otro entra, el que sale se va en la primera mitad del verbo y el nuevo llega en la segunda;
// así nunca se encima uno con otro. Si solo sale, se va en toda la duración; si solo entra, llega en toda la duración.

export type CambioDeTexto = 'igual' | 'entra' | 'sale' | 'a-traves';

/** Cómo cambia un texto entre dos estados. Un texto vacío es «no hay texto». */
export function cambioDeTexto(antes: string, despues: string): CambioDeTexto {
	if (antes === despues) return 'igual';
	if (!antes) return 'entra';
	if (!despues) return 'sale';
	return 'a-traves';
}

/** Tramos del cambio en ms: cuándo empieza y cuánto dura cada mitad (o el tramo único). */
export function tramosDeTexto(cambio: CambioDeTexto, duracionMs: number): {sale?: [number, number]; entra?: [number, number]} {
	const mitad = Math.round(duracionMs / 2);
	switch (cambio) {
		case 'a-traves':
			return {sale: [0, mitad], entra: [mitad, duracionMs - mitad]};
		case 'sale':
			return {sale: [0, duracionMs]};
		case 'entra':
			return {entra: [0, duracionMs]};
		default:
			return {};
	}
}
