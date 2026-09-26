// Estado global del motion en la página: modo reducido, velocidad (para el inspector) y registro de animaciones.

export type Registro = {etiqueta: string; elemento: Element; duracion: number; tokens: string; inicio: number; reducido: boolean};

const oyentes = new Set<(r: Registro) => void>();
const vivas = new Set<Animation>();
let velocidad = 1;

/** Movimiento reducido: la preferencia del sistema, salvo que la página fije data-movimiento en <html>. */
export function esReducido(): boolean {
	if (typeof document === 'undefined') return false;
	const forzado = document.documentElement.dataset.movimiento;
	if (forzado === 'reducido') return true;
	if (forzado === 'completo') return false;
	return typeof matchMedia !== 'undefined' && matchMedia('(prefers-reduced-motion: reduce)').matches;
}

/** Avisa cuando cambia el modo (preferencia del sistema o atributo data-movimiento). */
export function alCambiarModo(cb: (reducido: boolean) => void): () => void {
	const mq = typeof matchMedia !== 'undefined' ? matchMedia('(prefers-reduced-motion: reduce)') : null;
	const f = () => cb(esReducido());
	mq?.addEventListener('change', f);
	const mo = new MutationObserver(f);
	mo.observe(document.documentElement, {attributes: true, attributeFilter: ['data-movimiento']});
	return () => {
		mq?.removeEventListener('change', f);
		mo.disconnect();
	};
}

export const obtenerVelocidad = () => velocidad;

/** Velocidad global (0,1 = diez veces más lento). Solo para revisar movimiento; en producción es 1. */
export function fijarVelocidad(v: number) {
	velocidad = v;
	document.documentElement.style.setProperty('--kino-mov-velocidad', String(v));
	for (const a of vivas) a.playbackRate = v;
}

export function registrar(a: Animation | null, r: Omit<Registro, 'inicio'>) {
	if (a) {
		a.playbackRate = velocidad;
		vivas.add(a);
		const fin = () => vivas.delete(a);
		a.addEventListener('finish', fin);
		a.addEventListener('cancel', fin);
	}
	const reg = {...r, inicio: performance.now()};
	for (const o of oyentes) o(reg);
}

export function alAnimar(cb: (r: Registro) => void): () => void {
	oyentes.add(cb);
	return () => oyentes.delete(cb);
}

export const animacionesVivas = () => [...vivas];
