// Acceso tipado a los tokens: solo se aceptan nombres que existen.
import {TOKENS} from '../tokens.generados';
import {bezier, type Bezier, type Easing} from './curvas';
import {resolver, type Resorte} from './resorte';

export {TOKENS};
export type NombreDuracion = `duracion/${keyof typeof TOKENS.duracion}` | keyof typeof TOKENS.verbo;
export type NombreCurva = `curva/${keyof typeof TOKENS.curva}` | keyof typeof TOKENS.verbo;
export type NombreResorte = keyof typeof TOKENS.resorte;
export type NombreEscalonado = keyof typeof TOKENS.escalonado;

const alias = (n: string): string => (TOKENS.verbo as Record<string, string>)[n] ?? n;

/** Duración en ms de un token de duración o de un verbo ('aparecer/duracion'). */
export function ms(nombre: NombreDuracion): number {
	const [familia, clave] = alias(nombre).split('/');
	if (familia !== 'duracion') throw new Error(`«${nombre}» no es una duración`);
	const v = (TOKENS.duracion as Record<string, number>)[clave];
	if (v === undefined) throw new Error(`duración desconocida: ${nombre}`);
	return v;
}

export function curvaDe(nombre: NombreCurva): Bezier {
	const [familia, clave] = alias(nombre).split('/');
	if (familia !== 'curva') throw new Error(`«${nombre}» no es una curva`);
	const c = (TOKENS.curva as Record<string, readonly number[]>)[clave];
	if (!c) throw new Error(`curva desconocida: ${nombre}`);
	return c as unknown as Bezier;
}

export const easing = (nombre: NombreCurva): Easing => bezier(curvaDe(nombre));

export function resorteDe(nombre: NombreResorte): Resorte {
	const r = TOKENS.resorte[nombre];
	return {rigidez: r.rigidez, amortiguacion: r.amortiguacion, masa: r.masa};
}

export const solucionResorte = (nombre: NombreResorte, v0 = 0) => resolver(resorteDe(nombre), v0);

/** Frames a 60 fps de una duración, redondeando al más cercano (para Lottie, Remotion y Blender). */
export const frames = (nombre: NombreDuracion, fps: number = TOKENS.fps) => Math.floor((ms(nombre) * fps) / 1000 + 0.5);
