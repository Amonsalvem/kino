// Textos que cambian con el estado (M3D-5, Nico, 27 sep: A): fundido a través.
// La regla es la del núcleo (paquetes/kino-motion/src/nucleo/textos.ts), la misma que usan la web y la app.
// Aquí solo se traduce a opacidad por frame. tramosDeTexto recibe frames en lugar de ms: solo divide la duración.
import {cambioDeTexto, tramosDeTexto} from '../../../../../../paquetes/kino-motion/src/nucleo/textos';
import {avance, Tramo} from './tiempo';

/** Paso de un estado al siguiente: tramo y curva del verbo. */
export type Cambio = {tramo: Tramo; curva: string};

const sub = (t: Tramo, [desde, dura]: [number, number]): Tramo => ({inicio: t.inicio + desde, fin: t.inicio + desde + dura});

/**
 * Opacidad del texto de la capa i, cuando cada capa es un estado y cambios[i] lleva de la capa i a la i + 1.
 * - A través: el texto que sale se va en la primera mitad y el que entra llega en la segunda.
 * - Solo sale o solo entra: toda la duración.
 * - Igual: el nuevo llega encima en toda la duración y el viejo se queda hasta el final; si solo cambia el color,
 *   no hay hueco de opacidad.
 */
export const opacidadTexto = (f: number, textos: (string | undefined)[], cambios: Cambio[], i: number): number => {
	let o = 1;
	if (i > 0) {
		const {tramo, curva} = cambios[i - 1];
		const cambio = cambioDeTexto(textos[i - 1] ?? '', textos[i] ?? '');
		const {entra} = tramosDeTexto(cambio, tramo.fin - tramo.inicio);
		o *= cambio === 'igual' ? avance(f, tramo, curva) : entra ? avance(f, sub(tramo, entra), curva) : 0;
	}
	if (i < cambios.length) {
		const {tramo, curva} = cambios[i];
		const cambio = cambioDeTexto(textos[i] ?? '', textos[i + 1] ?? '');
		const {sale} = tramosDeTexto(cambio, tramo.fin - tramo.inicio);
		o *= cambio === 'igual' ? (f < tramo.fin ? 1 : 0) : sale ? 1 - avance(f, sub(tramo, sale), curva) : 1;
	}
	return o;
};
