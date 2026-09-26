// Movimiento de disposición: FLIP para reordenar sin saltos, y transiciones entre pantallas con View Transitions.
import {escalonar, salida} from '../nucleo/coreografia';
import {TOKENS} from '../nucleo/tokens';
import {animar, terminada} from './animar';
import {esReducido} from './entorno';

/**
 * FLIP: mide, aplica el cambio, mide otra vez y anima cada elemento desde donde estaba con el resorte «pase».
 * Los que aparecen entran con «aparecer», en cascada.
 */
export async function flip(contenedor: Element, cambiar: () => void | Promise<void>) {
	const antes = new Map<Element, DOMRect>();
	for (const el of contenedor.children) antes.set(el, el.getBoundingClientRect());
	await cambiar();
	const nuevos: Element[] = [];
	const promesas: Promise<void>[] = [];
	for (const el of contenedor.children) {
		const r0 = antes.get(el);
		if (!r0) {
			nuevos.push(el);
			continue;
		}
		const r1 = el.getBoundingClientRect();
		const dx = r0.left - r1.left;
		const dy = r0.top - r1.top;
		if (Math.abs(dx) < 0.5 && Math.abs(dy) < 0.5) continue;
		promesas.push(terminada(animar(el, [{transform: `translate(${dx}px, ${dy}px)`}, {transform: 'none'}], {resorte: 'pase', canal: 'disposicion', etiqueta: 'reordenar'})));
	}
	const retrasos = escalonar(nuevos.length);
	nuevos.forEach((el, i) => promesas.push(terminada(entrar(el, retrasos[i]))));
	await Promise.all(promesas);
}

/** «aparecer»: sube distancia/subida, escala desde escala/entrada y funde. */
export function entrar(el: Element, retraso = 0) {
	const d = TOKENS.distancia.subida;
	return animar(
		el,
		[
			{opacity: 0, transform: `translateY(${d}px) scale(${TOKENS.escala.entrada})`},
			{opacity: 1, transform: 'none'},
		],
		{duracion: 'aparecer/duracion', curva: 'aparecer/curva', retraso, canal: 'entrada', etiqueta: 'aparecer'},
	);
}

/** Salida: lo inverso de entrar, más corta (coreografia/salida-factor). Devuelve cuando terminó. */
export async function salir(el: Element) {
	const d = TOKENS.distancia.subida;
	const a = animar(el, [{opacity: 1, transform: 'none'}, {opacity: 0, transform: `translateY(${d / 2}px) scale(${TOKENS.escala.entrada})`}], {
		duracionMs: salida('aparecer/duracion'),
		curva: 'curva/salir',
		canal: 'entrada',
		etiqueta: 'salir',
	});
	await terminada(a);
}

/** Quita un elemento de una lista: sale, y los demás se acomodan con FLIP. */
export async function quitar(el: Element) {
	const padre = el.parentElement;
	await salir(el);
	if (padre) await flip(padre, () => el.remove());
	else el.remove();
}

export type TipoVista = 'adelante' | 'atras' | 'hoja' | 'fundido';

/**
 * Cambio de pantalla con View Transitions. Un elemento con `view-transition-name` igual en las dos vistas
 * (por ejemplo, pase-<id>) viaja de una a otra con el resorte «pase». Sin soporte o en reducido, funde.
 */
export async function transicionDeVista(actualizar: () => void | Promise<void>, tipo: TipoVista = 'adelante') {
	const doc = document as Document & {startViewTransition?: (cb: () => void | Promise<void>) => {finished: Promise<void>}};
	if (!doc.startViewTransition) {
		await actualizar();
		return;
	}
	const raiz = document.documentElement;
	raiz.dataset.transicion = esReducido() ? 'fundido' : tipo;
	try {
		await doc.startViewTransition(actualizar).finished;
	} finally {
		delete raiz.dataset.transicion;
	}
}
