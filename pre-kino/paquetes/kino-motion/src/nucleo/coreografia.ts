// Coreografía: cuándo empieza cada cosa cuando varias se mueven juntas.
import {ms, TOKENS, type NombreDuracion, type NombreEscalonado} from './tokens';

/**
 * Retrasos (ms) de una cascada de n elementos. Paso del token de escalonado; del elemento cascadaMaximo en
 * adelante entran con el último escalonado; el total nunca pasa de cascadaTopeMs (el paso se comprime).
 */
export function escalonar(n: number, paso: NombreEscalonado = 'tarjetas'): number[] {
	const {cascadaMaximo, cascadaTopeMs} = TOKENS.coreografia;
	const base = TOKENS.escalonado[paso];
	const escalonados = Math.min(n, cascadaMaximo);
	const efectivo = escalonados > 1 ? Math.min(base, cascadaTopeMs / (escalonados - 1)) : base;
	return Array.from({length: n}, (_, i) => Math.round(Math.min(i, cascadaMaximo - 1) * efectivo));
}

/** Duración de salida: lo que se va dura menos que lo que llega. */
export const salida = (entrada: NombreDuracion | number) =>
	Math.round((typeof entrada === 'number' ? entrada : ms(entrada)) * TOKENS.coreografia.salidaFactor);

export type Paso = {id: string; duracion: NombreDuracion | number; despuesDe?: string; conDesfase?: number; junto?: string};
export type Tramo = {id: string; inicio: number; fin: number};

/**
 * Línea de tiempo declarativa. Cada paso empieza al terminar el anterior, salvo que diga
 * `junto` (empieza con otro paso) o `despuesDe` (empieza cuando otro termina); `conDesfase` suma ms.
 */
export function lineaDeTiempo(pasos: Paso[]): {tramos: Record<string, Tramo>; total: number} {
	const tramos: Record<string, Tramo> = {};
	let cursor = 0;
	for (const p of pasos) {
		const d = typeof p.duracion === 'number' ? p.duracion : ms(p.duracion);
		let inicio = cursor;
		if (p.junto) inicio = req(tramos, p.junto).inicio;
		if (p.despuesDe) inicio = req(tramos, p.despuesDe).fin;
		inicio += p.conDesfase ?? 0;
		tramos[p.id] = {id: p.id, inicio, fin: inicio + d};
		cursor = Math.max(cursor, inicio + d);
	}
	return {tramos, total: Math.max(0, ...Object.values(tramos).map((t) => t.fin))};
}

const req = (t: Record<string, Tramo>, id: string) => {
	if (!t[id]) throw new Error(`paso desconocido: ${id}`);
	return t[id];
};

/**
 * Coreografía de una pantalla que se abre: el título primero, las tarjetas en cascada y la acción al final.
 * Devuelve el retraso (ms) de cada rol.
 */
export function entradaDePantalla(tarjetas: number): {titulo: number; tarjetas: number[]; accion: number} {
	const cascada = escalonar(tarjetas).map((r) => r + TOKENS.escalonado.tarjetas);
	const ultima = cascada.length ? cascada[cascada.length - 1] : 0;
	return {titulo: 0, tarjetas: cascada, accion: ultima + TOKENS.escalonado.tarjetas};
}
