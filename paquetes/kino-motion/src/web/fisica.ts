// Resortes por cuadro (requestAnimationFrame) para lo que sale de un gesto: arrancan con la velocidad del dedo.
// Y el gesto de arrastre, con velocidad medida y resistencia elástica fuera de los límites.
import {resistencia} from '../nucleo/gestos';
import {resolver} from '../nucleo/resorte';
import {resorteDe, type NombreResorte} from '../nucleo/tokens';
import {esReducido, obtenerVelocidad, registrar} from './entorno';

export type Control = {detener: () => void; terminado: Promise<void>};

/**
 * Lleva un valor de `de` a `a` con un resorte del sistema. `velocidad` en unidades/s (la del gesto).
 * Interrumpible: detener() deja el valor donde está.
 */
export function animarResorte(o: {
	de: number;
	a: number;
	velocidad?: number;
	resorte: NombreResorte;
	alCambiar: (v: number) => void;
	etiqueta?: string;
	elemento?: Element;
}): Control {
	let listo!: () => void;
	const terminado = new Promise<void>((r) => (listo = r));
	const distancia = o.a - o.de;
	if (esReducido() || Math.abs(distancia) < 1e-6) {
		o.alCambiar(o.a);
		listo();
		return {detener: () => {}, terminado};
	}
	const s = resolver(resorteDe(o.resorte), (o.velocidad ?? 0) / distancia);
	if (o.elemento) registrar(null, {etiqueta: o.etiqueta ?? 'resorte', elemento: o.elemento, duracion: s.asentamiento * 1000, tokens: `resorte/${o.resorte}`, reducido: false});
	let t = 0;
	let ultimo = performance.now();
	let id = 0;
	const paso = (ahora: number) => {
		t += ((ahora - ultimo) / 1000) * obtenerVelocidad();
		ultimo = ahora;
		if (t >= s.asentamiento) {
			o.alCambiar(o.a);
			listo();
			return;
		}
		o.alCambiar(o.de + distancia * s.avance(t));
		id = requestAnimationFrame(paso);
	};
	id = requestAnimationFrame(paso);
	return {
		detener: () => {
			cancelAnimationFrame(id);
			listo();
		},
		terminado,
	};
}


export type Arrastre = {soltar: () => void};

/**
 * Arrastre en un eje con captura del puntero. alMover recibe la posición (con resistencia fuera de [min, max]);
 * alSoltar recibe posición y velocidad (px/s, medida en los últimos 80 ms).
 */
export function arrastrar(
	el: HTMLElement,
	o: {eje: 'x' | 'y'; min: number; max: number; inicial: () => number; alEmpezar?: () => void; alMover: (p: number) => void; alSoltar: (p: number, v: number) => void},
): Arrastre {
	let activo = false;
	let origen = 0;
	let base = 0;
	let muestras: {t: number; p: number}[] = [];
	let pos = 0;
	const coord = (e: PointerEvent) => (o.eje === 'x' ? e.clientX : e.clientY);
	const dim = () => (o.eje === 'x' ? el.offsetWidth : el.offsetHeight) || 1;
	const abajo = (e: PointerEvent) => {
		if (e.button !== 0) return;
		activo = true;
		origen = coord(e);
		base = o.inicial();
		muestras = [{t: e.timeStamp, p: base}];
		el.setPointerCapture(e.pointerId);
		o.alEmpezar?.();
	};
	const mover = (e: PointerEvent) => {
		if (!activo) return;
		const bruto = base + coord(e) - origen;
		pos = bruto < o.min ? o.min + resistencia(bruto - o.min, dim()) : bruto > o.max ? o.max + resistencia(bruto - o.max, dim()) : bruto;
		muestras.push({t: e.timeStamp, p: pos});
		muestras = muestras.filter((m) => e.timeStamp - m.t <= 80);
		o.alMover(pos);
	};
	const arriba = (e: PointerEvent) => {
		if (!activo) return;
		activo = false;
		el.releasePointerCapture?.(e.pointerId);
		const a = muestras[0];
		const b = muestras[muestras.length - 1];
		const v = a && b && b.t > a.t ? ((b.p - a.p) / (b.t - a.t)) * 1000 : 0;
		o.alSoltar(pos, v);
	};
	el.addEventListener('pointerdown', abajo);
	el.addEventListener('pointermove', mover);
	el.addEventListener('pointerup', arriba);
	el.addEventListener('pointercancel', arriba);
	el.style.touchAction = o.eje === 'y' ? 'pan-x' : 'pan-y';
	return {
		soltar: () => {
			el.removeEventListener('pointerdown', abajo);
			el.removeEventListener('pointermove', mover);
			el.removeEventListener('pointerup', arriba);
			el.removeEventListener('pointercancel', arriba);
		},
	};
}

