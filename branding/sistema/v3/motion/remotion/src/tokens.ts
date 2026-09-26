// Supuestos: tokens.motion.json lo escribe ../tokens.py desde los DTCG del repositorio.
// Este archivo no tiene números de movimiento propios: todo se resuelve por nombre de token.
import {Easing} from 'remotion';
import todos from '../../tokens.motion.json';

type Tema = (typeof todos)['oscuro'];
export const T: Tema = todos.oscuro;
export const FPS = T.fps;

const verbo = (nombre: string): string => (T.verbo as Record<string, string>)[nombre] ?? nombre;

/** 'aparecer/duracion' o 'duracion/tarjeta' → frames a FPS. */
export const dur = (nombre: string): number => {
	const [familia, clave] = verbo(nombre).split('/');
	const tabla = (T as unknown as Record<string, Record<string, {frames: number}>>)[familia];
	if (!tabla?.[clave]) throw new Error(`token de duración desconocido: ${nombre}`);
	return tabla[clave].frames;
};

/** 'aparecer/curva' o 'curva/crecer' → función de easing del token. */
export const curva = (nombre: string) => {
	const clave = verbo(nombre).split('/')[1];
	const c = (T.curva as Record<string, number[]>)[clave];
	if (!c) throw new Error(`token de curva desconocido: ${nombre}`);
	return Easing.bezier(c[0], c[1], c[2], c[3]);
};

/** Color semántico por token: 'estado/vigente/borde'. */
export const color = (token: string): string => {
	const v = (T.color as Record<string, string>)[token];
	if (!v) throw new Error(`color sin token: ${token}`);
	return v;
};

export const primitivo = (token: string): string => (T.primitivo as Record<string, string>)[token];
export const SUBIDA = T.distancia.subida;
export const ESP = T.espacio as Record<string, number>;
export const RADIO = T.radio;
export const LINEA = T.linea;

export type Estado = 'previsto' | 'sin-confirmar' | 'vigente' | 'por-vencer' | 'usado' | 'vencido' | 'revocado' | 'rechazado';
export const ETIQUETA: Record<Estado, string> = {
	previsto: 'Previsto',
	'sin-confirmar': 'Sin confirmar',
	vigente: 'Vigente',
	'por-vencer': 'Por vencer',
	usado: 'Usado',
	vencido: 'Vencido',
	revocado: 'Revocado',
	rechazado: 'Rechazado',
};

/** Aurora fija (d07_imagen.py · AURORA) con primitivos del repositorio. Nunca se anima. */
export const AURORA =
	`radial-gradient(120% 80% at 85% 0%,color-mix(in oklch,${primitivo('biolum/d23')} 75%,transparent),transparent 60%),` +
	`radial-gradient(90% 70% at 0% 100%,color-mix(in oklch,${primitivo('violeta/d15')} 80%,transparent),transparent 65%),` +
	`radial-gradient(60% 50% at 40% 60%,color-mix(in oklch,${primitivo('indigo/d15')} 50%,transparent),transparent 70%),${primitivo('sustrato/100')}`;
