// Tokens de @kino/motion → configuraciones de Reanimated.
// Supuestos: Reanimated 3. Se pasa ReduceMotion.Never porque Kino no salta al final en modo reducido:
// aplica su propia política (desplazamientos → fundidos con la misma duración). Ver plan.ts y hooks.ts.
import {Easing, ReduceMotion, type WithSpringConfig, type WithTimingConfig} from 'react-native-reanimated';
import {curvaDe, ms, resorteDe, TOKENS, type Bezier, type NombreCurva, type NombreDuracion, type NombreResorte} from './nucleo';

/** withTiming con la duración y la curva de dos tokens (o de un verbo: 'aparecer/duracion', 'aparecer/curva'). */
export const tiempo = (duracion: NombreDuracion, curva: NombreCurva): WithTimingConfig => tiempoMs(ms(duracion), curvaDe(curva));

/** withTiming con una duración derivada de un token (por ejemplo, salida()) y una curva. */
export function tiempoMs(duracionMs: number, [x1, y1, x2, y2]: Bezier): WithTimingConfig {
	return {duration: duracionMs, easing: Easing.bezier(x1, y1, x2, y2), reduceMotion: ReduceMotion.Never};
}

/**
 * withSpring con un resorte del sistema. Mismos parámetros físicos que la web (rigidez, amortiguación, masa),
 * así que el movimiento es el mismo. `velocidad` en unidades/s, la del gesto (event.velocityY).
 */
export function resorte(nombre: NombreResorte, velocidad = 0): WithSpringConfig {
	const r = resorteDe(nombre);
	return {stiffness: r.rigidez, damping: r.amortiguacion, mass: r.masa, velocity: velocidad, reduceMotion: ReduceMotion.Never};
}

export {TOKENS};
