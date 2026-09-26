// Plan de movimiento del Pase para la app: traduce la partitura del núcleo a valores animables.
// Sin React Native: se prueba con vitest y lo consumen los hooks de Reanimated.
import {curvaDe, ms, reducirPistas, transicionEntre, type Bezier, type Estado, type Evidencia, type Pista, type Transicion} from './nucleo';

/** Valores que dibujan un Pase. Cada uno es un SharedValue en la app. */
export type Valores = {
	tarjeta: number; // opacidad de la tarjeta
	discontinuo: number; // 1 = borde discontinuo (sin confirmar), 0 = continuo
	barra: number; // opacidad de la barra de vigencia
	barraEscala: number; // factor sobre la vigencia real (0 al caducar)
	nota: number; // opacidad de la nota (evidencia del lector o autor)
	notaY: number; // desplazamiento de la nota
	corte: number; // escala X de la línea de revocar
	corteOp: number;
	tachado: number; // escala X del tachado del código
	tachadoOp: number;
};
export type Clave = keyof Valores;

/** Cómo se ve cada estado en reposo. */
export function valoresDeEstado(e: Estado): Valores {
	const terminado = e === 'vencido' || e === 'usado' || e === 'revocado';
	const confirmado = e === 'vigente' || e === 'por-vencer';
	return {
		tarjeta: terminado ? 0.72 : 1,
		discontinuo: e === 'sin-confirmar' ? 1 : 0,
		barra: e === 'previsto' || e === 'sin-confirmar' ? 0 : 1,
		barraEscala: e === 'vencido' ? 0 : 1,
		nota: confirmado || e === 'revocado' ? 1 : 0,
		notaY: 0,
		corte: e === 'revocado' ? 1 : 0,
		corteOp: 1,
		tachado: e === 'usado' ? 1 : 0,
		tachadoOp: 1,
	};
}

const CLAVE: Record<string, Clave> = {
	'tarjeta/opacidad': 'tarjeta', 'borde/trazo': 'discontinuo', 'barra/opacidad': 'barra', 'barra/escalaX': 'barraEscala',
	'nota/opacidad': 'nota', 'nota/y': 'notaY', 'corte/escalaX': 'corte', 'corte/opacidad': 'corteOp',
	'tachado/escalaX': 'tachado', 'tachado/opacidad': 'tachadoOp',
};

export type PasoPlan = {clave: Clave; de: number | 'actual'; a: number};
export type Plan = {
	transicion: Transicion;
	duracionMs: number;
	bezier: Bezier;
	/** Valores que se fijan de inmediato antes de animar (en reducido: las escalas quedan en su valor final). */
	fijar: Partial<Valores>;
	pasos: PasoPlan[];
	/** El chip y el borde cambian de color entre estos estados. */
	color: {de: Estado; a: Estado};
	late: boolean;
};

const numero = (v: number | string, subida: number): number | 'actual' =>
	v === 'actual' ? 'actual' : v === 'subida' ? subida : v === 'continuo' ? 0 : v === 'discontinuo' ? 1 : Number(v);

/** Plan para pasar de un estado a otro, o null si no hay transición (entonces el cambio es directo). */
export function planDeTransicion(de: Estado, a: Estado, reducido: boolean, subida: number): Plan | null {
	const t = transicionEntre(de, a);
	if (!t) return null;
	const pistas: Pista[] = reducido ? reducirPistas(t.pistas) : [...t.pistas];
	const final = valoresDeEstado(a);
	const fijar: Partial<Valores> = {};
	if (reducido) {
		// Lo que se dibujaba (escalaX) queda en su escala final y aparece o se va por opacidad.
		for (const k of ['corte', 'tachado', 'barraEscala'] as const) fijar[k] = final[k];
		fijar.notaY = 0;
	}
	const pasos: PasoPlan[] = [];
	for (const p of pistas) {
		const clave = CLAVE[`${p.parte}/${p.propiedad}`];
		if (!clave) continue; // chip y borde: color, van por el progreso de color
		pasos.push({clave, de: numero(p.de, subida), a: numero(p.a, subida) as number});
	}
	return {transicion: t, duracionMs: ms(t.duracion), bezier: curvaDe(t.curva), fijar, pasos, color: {de, a}, late: Boolean(t.late)};
}

/** Estado que se puede mostrar sin mentir: vigente y por vencer exigen evidencia del lector. */
export function estadoHonesto(pedido: Estado, evidencia?: Evidencia | null): Estado {
	return (pedido === 'vigente' || pedido === 'por-vencer') && !evidencia ? 'sin-confirmar' : pedido;
}
