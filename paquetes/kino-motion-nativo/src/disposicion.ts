// Animaciones de disposición de Reanimated con los tokens de Kino (el equivalente nativo de entrar/salir/flip).
//   <Animated.View entering={entradaKino(retraso, reducido)} exiting={salidaKino(reducido)} layout={disposicionKino(reducido)} />
// En web devuelven undefined: Reanimated web solo acepta curvas con nombre (no el cubic-bezier de los tokens) y fija
// en posición absoluta lo que entra con un Keyframe propio. Para entrar en todas las plataformas: useEntrada / <EntraKino>.
const WEB = Platform.OS === 'web';
import {Platform} from 'react-native';
import {Easing, FadingTransition, Keyframe, LinearTransition} from 'react-native-reanimated';
import {curvaDe, ms, resorteDe, salida, TOKENS} from './nucleo';

/** «aparecer»: sube distancia/subida, escala desde escala/entrada y funde. Reducido: solo funde, misma duración. */
export function entradaKino(retraso = 0, reducido = false) {
	if (WEB) return undefined;
	const [x1, y1, x2, y2] = curvaDe('aparecer/curva');
	const easing = Easing.bezierFn(x1, y1, x2, y2);
	const subida = TOKENS.distancia.subida;
	const escala = TOKENS.escala.entrada;
	// Keyframe (no una función propia): Reanimated lo soporta igual en iOS, Android y web.
	const k = reducido
		? new Keyframe({0: {opacity: 0}, 100: {opacity: 1, easing}})
		: new Keyframe({
				0: {opacity: 0, transform: [{translateY: subida}, {scale: escala}]},
				100: {opacity: 1, transform: [{translateY: 0}, {scale: 1}], easing},
			});
	return k.duration(ms('aparecer/duracion')).delay(retraso);
}

/** Salida: lo inverso de entrar, más corta (coreografia/salida-factor) y con curva/salir. */
export function salidaKino(reducido = false) {
	if (WEB) return undefined;
	const [x1, y1, x2, y2] = curvaDe('curva/salir');
	const easing = Easing.bezierFn(x1, y1, x2, y2);
	const k = reducido
		? new Keyframe({0: {opacity: 1}, 100: {opacity: 0, easing}})
		: new Keyframe({
				0: {opacity: 1, transform: [{translateY: 0}, {scale: 1}]},
				100: {opacity: 0, transform: [{translateY: TOKENS.distancia.subida / 2}, {scale: TOKENS.escala.entrada}], easing},
			});
	return k.duration(salida('aparecer/duracion'));
}

/** Reacomodo de la lista (FLIP): resorte/pase. Reducido: fundido en el lugar con la duración de «crecer». */
export function disposicionKino(reducido = false) {
	if (WEB) return undefined;
	if (reducido) return FadingTransition.duration(ms('duracion/crecer'));
	const r = resorteDe('pase');
	return LinearTransition.springify().stiffness(r.rigidez).damping(r.amortiguacion).mass(r.masa);
}
