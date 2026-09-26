// Hooks de motion para React Native (Reanimated 3 + Gesture Handler 2).
import {useEffect, useMemo, useRef, useState} from 'react';
import {useColorScheme} from 'react-native';
import {Gesture} from 'react-native-gesture-handler';
import Animated, {
	cancelAnimation, Easing, interpolate, interpolateColor, runOnJS, useAnimatedProps, useAnimatedStyle, useReducedMotion, useSharedValue,
	withDelay, withRepeat, withSequence, withSpring, withTiming, type SharedValue,
} from 'react-native-reanimated';
import {resorte, tiempo, tiempoMs} from './configuracion';
import {curvaDe, escalonar, ms, TOKENS, vigenciaRestante, type Estado, type Evidencia} from './nucleo';


import {estadoHonesto, planDeTransicion, valoresDeEstado, type Clave, type Valores} from './plan';
import {formatoCifra, proyectarW, resistenciaW} from './worklets';

export type Tema = 'oscuro' | 'claro';

// Entorno ----------------------------------------------------------------------------------------------------
/** Movimiento reducido del sistema operativo (iOS «Reducir movimiento», Android «Quitar animaciones»). */
export const useMovimientoReducido = () => useReducedMotion();

/** Tema de color de Kino según el sistema, salvo que se fije. */
export function useTemaKino(fijo?: Tema) {
	const esquema = useColorScheme();
	const tema: Tema = fijo ?? (esquema === 'light' ? 'claro' : 'oscuro');
	return useMemo(() => {
		const tabla = TOKENS.color[tema] as Record<string, string>;
		const color = (token: string) => {
			const c = tabla[token];
			if (!c) throw new Error(`color sin token: ${token}`);
			return c;
		};
		return {tema, color};
	}, [tema]);
}

// El Pase ----------------------------------------------------------------------------------------------------
const CLAVES: Clave[] = ['tarjeta', 'discontinuo', 'barra', 'barraEscala', 'nota', 'notaY', 'corte', 'corteOp', 'tachado', 'tachadoOp'];

/**
 * Movimiento de un Pase. Recibe el estado pedido y la evidencia del lector; devuelve el estado que se muestra
 * (vigente exige evidencia) y los estilos animados de cada parte. Cada cambio de estado ejecuta su partitura.
 */
export function usePaseMotion(estadoPedido: Estado, evidencia: Evidencia | null | undefined, temaFijo?: Tema) {
	const reducido = useMovimientoReducido();
	const {color, tema} = useTemaKino(temaFijo);
	const estado = estadoHonesto(estadoPedido, evidencia);
	if (estado !== estadoPedido && __DEV__) console.warn(`usePaseMotion: «${estadoPedido}» sin confirmación del lector; se muestra «sin confirmar».`);

	const inicial = valoresDeEstado(estado);
	const v = {} as Record<Clave, SharedValue<number>>;
	for (const k of CLAVES) v[k] = useSharedValue(inicial[k]); // eslint-disable-line react-hooks/rules-of-hooks
	const progreso = useSharedValue(1);
	const brillo = useSharedValue(0);
	const familia = (e: Estado, parte: 'fondo' | 'borde' | 'texto') => color(`estado/${e}/${parte}`);
	const fondoDe = useSharedValue(familia(estado, 'fondo'));
	const fondoA = useSharedValue(familia(estado, 'fondo'));
	const bordeDe = useSharedValue(familia(estado, 'borde'));
	const bordeA = useSharedValue(familia(estado, 'borde'));
	const textoDe = useSharedValue(familia(estado, 'texto'));
	const textoA = useSharedValue(familia(estado, 'texto'));
	const previo = useRef<Estado | null>(null);

	const latir = (retraso: number) => {
		cancelAnimation(brillo);
		brillo.value = 0;
		if (reducido) return;
		const mitad = tiempoMs(ms('latir/duracion') / 2, curvaDe('latir/curva'));
		brillo.value = withDelay(retraso, withRepeat(withSequence(withTiming(1, mitad), withTiming(0, mitad)), TOKENS.latirCiclos, false));
	};

	useEffect(() => {
		const de = previo.current;
		previo.current = estado;
		const plan = de && de !== estado ? planDeTransicion(de, estado, reducido, TOKENS.distancia.subida) : null;
		fondoA.value = familia(estado, 'fondo');
		bordeA.value = familia(estado, 'borde');
		textoA.value = familia(estado, 'texto');
		if (!plan) {
			// Primer render o cambio sin transición: se pinta el estado sin moverse.
			const final = valoresDeEstado(estado);
			for (const k of CLAVES) v[k].value = final[k];
			fondoDe.value = fondoA.value;
			bordeDe.value = bordeA.value;
			textoDe.value = textoA.value;
			progreso.value = 1;
			if (estado !== 'vigente') brillo.value = 0;
			else if (!de) latir(0);
			return;
		}
		fondoDe.value = familia(plan.color.de, 'fondo');
		bordeDe.value = familia(plan.color.de, 'borde');
		textoDe.value = familia(plan.color.de, 'texto');
		const cfg = tiempoMs(plan.duracionMs, plan.bezier);
		for (const [k, val] of Object.entries(plan.fijar)) v[k as Clave].value = val as number;
		progreso.value = 0;
		progreso.value = withTiming(1, cfg);
		for (const p of plan.pasos) {
			if (p.de !== 'actual') v[p.clave].value = p.de;
			v[p.clave].value = withTiming(p.a, cfg);
		}
		if (estado !== 'vigente') brillo.value = 0;
		if (plan.late) latir(plan.duracionMs);
	}, [estado, reducido]); // eslint-disable-line react-hooks/exhaustive-deps

	// Cambio de tema: los colores se actualizan sin animar.
	useEffect(() => {
		fondoDe.value = fondoA.value = familia(estado, 'fondo');
		bordeDe.value = bordeA.value = familia(estado, 'borde');
		textoDe.value = textoA.value = familia(estado, 'texto');
	}, [tema]); // eslint-disable-line react-hooks/exhaustive-deps

	const estilos = {
		tarjeta: useAnimatedStyle(() => ({opacity: v.tarjeta.value})),
		bordeContinuo: useAnimatedStyle(() => ({opacity: 1 - v.discontinuo.value, borderColor: interpolateColor(progreso.value, [0, 1], [bordeDe.value, bordeA.value])})),
		bordeDiscontinuo: useAnimatedStyle(() => ({opacity: v.discontinuo.value})),
		chip: useAnimatedStyle(() => ({
			backgroundColor: interpolateColor(progreso.value, [0, 1], [fondoDe.value, fondoA.value]),
			borderColor: interpolateColor(progreso.value, [0, 1], [bordeDe.value, bordeA.value]),
		})),
		chipTexto: useAnimatedStyle(() => ({color: interpolateColor(progreso.value, [0, 1], [textoDe.value, textoA.value])})),
		punto: useAnimatedStyle(() => ({backgroundColor: interpolateColor(progreso.value, [0, 1], [bordeDe.value, bordeA.value])})),
		brillo: useAnimatedStyle(() => ({opacity: brillo.value})),
		barra: useAnimatedStyle(() => ({opacity: v.barra.value})),
		nota: useAnimatedStyle(() => ({opacity: v.nota.value, transform: [{translateY: v.notaY.value}]})),
		corte: useAnimatedStyle(() => ({opacity: v.corteOp.value, transform: [{scaleX: v.corte.value}]})),
		tachado: useAnimatedStyle(() => ({opacity: v.tachadoOp.value, transform: [{scaleX: v.tachado.value}]})),
	};
	return {estado, estilos, valores: v as Record<keyof Valores, SharedValue<number>>, color, tema};
}

/**
 * Vigencia con la hora real: devuelve un SharedValue de 1 a 0 que baja con el reloj hasta la hora de vencimiento.
 * En modo reducido no se anima: se actualiza una vez por minuto.
 */
export function useVigencia(desde: Date, hasta: Date, estado: Estado) {
	const reducido = useMovimientoReducido();
	const r = useSharedValue(vigenciaRestante({desde, hasta}, new Date()));
	useEffect(() => {
		const ahora = () => (estado === 'vencido' ? 0 : vigenciaRestante({desde, hasta}, new Date()));
		cancelAnimation(r);
		r.value = ahora();
		const queda = hasta.getTime() - Date.now();
		if (['vencido', 'usado', 'revocado'].includes(estado) || queda <= 0) return;
		if (reducido) {
			const id = setInterval(() => (r.value = ahora()), 60_000);
			return () => clearInterval(id);
		}
		r.value = withTiming(0, {duration: queda, easing: Easing.linear}); // motion-ok: reloj real
		return () => cancelAnimation(r);
	}, [desde.getTime(), hasta.getTime(), estado, reducido]); // eslint-disable-line react-hooks/exhaustive-deps
	return r;
}

// Tocar ------------------------------------------------------------------------------------------------------
/** Presionar un control: se hunde con resorte/tacto y vuelve con el mismo resorte. El color cambia en «instante». */
export function usePresion() {
	const reducido = useMovimientoReducido();
	const escala = useSharedValue(1);
	const activo = useSharedValue(0);
	const cfgColor = tiempo('duracion/instante', 'curva/crecer');
	return {
		alPresionar: () => {
			if (!reducido) escala.value = withSpring(TOKENS.escala.presion, resorte('tacto'));
			activo.value = withTiming(1, cfgColor);
		},
		alSoltar: () => {
			escala.value = reducido ? 1 : withSpring(1, resorte('tacto'));
			activo.value = withTiming(0, cfgColor);
		},
		escala,
		activo,
		estilo: useAnimatedStyle(() => ({transform: [{scale: escala.value}]})),
	};
}

/**
 * Hoja inferior. abrir()/cerrar() con resorte/hoja; `gesto` para el asa: al soltar, si la proyección de la
 * velocidad pasa de la mitad se cierra continuando la velocidad del dedo; si no, vuelve.
 * Reducido: sin deslizarse, aparece o se va por fundido con la duración de «crecer».
 */
export function useHoja(altura: number, alCerrar?: () => void) {
	const reducido = useMovimientoReducido();
	const y = useSharedValue(altura);
	const opacidad = useSharedValue(reducido ? 0 : 1);
	const inicio = useSharedValue(0);
	const cfg = resorte('hoja');
	const fundido = tiempo('duracion/crecer', 'curva/crecer');
	const avisar = () => alCerrar?.();

	const abrir = () => {
		if (reducido) {
			y.value = 0;
			opacidad.value = 0;
			opacidad.value = withTiming(1, fundido);
		} else {
			opacidad.value = 1;
			y.value = withSpring(0, cfg);
		}
	};
	const cerrar = (velocidad = 0) => {
		if (reducido) {
			opacidad.value = withTiming(0, fundido, (fin) => {
				if (fin) {
					y.value = altura;
					runOnJS(avisar)();
				}
			});
		} else {
			y.value = withSpring(altura, {...cfg, velocity: velocidad}, (fin) => fin && runOnJS(avisar)());
		}
	};
	const gesto = Gesture.Pan()
		.onStart(() => {
			cancelAnimation(y);
			inicio.value = y.value;
		})
		.onUpdate((e) => {
			const bruto = inicio.value + e.translationY;
			y.value = bruto < 0 ? resistenciaW(bruto, altura) : bruto;
		})
		.onEnd((e) => {
			if (reducido) {
				if (y.value > altura / 3) {
					opacidad.value = withTiming(0, fundido, (fin) => {
						if (fin) {
							y.value = altura;
							runOnJS(avisar)();
						}
					});
				} else y.value = 0;
				return;
			}
			if (proyectarW(y.value, e.velocityY) > altura / 2) {
				y.value = withSpring(altura, {...cfg, velocity: e.velocityY}, (fin) => fin && runOnJS(avisar)());
			} else y.value = withSpring(0, {...cfg, velocity: e.velocityY});
		});
	const estiloHoja = useAnimatedStyle(() => ({transform: [{translateY: y.value}], opacity: opacidad.value}));
	const estiloVelo = useAnimatedStyle(() => ({opacity: interpolate(y.value, [0, altura], [0.6, 0], 'clamp') * opacidad.value}));
	return {abrir, cerrar, gesto, estiloHoja, estiloVelo, y};
}

// Datos ------------------------------------------------------------------------------------------------------
/** Número que llega a su valor con resorte/firme (sin pasarse). Úsalo con <NumeroKino>. */
export function useNumeroAnimado(valor: number, decimales = 0) {
	const reducido = useMovimientoReducido();
	const n = useSharedValue(valor);
	useEffect(() => {
		n.value = reducido ? valor : withSpring(valor, resorte('firme'));
	}, [valor, reducido]); // eslint-disable-line react-hooks/exhaustive-deps
	const props = useAnimatedProps(() => ({text: formatoCifra(n.value, decimales), defaultValue: formatoCifra(n.value, decimales)}) as never);
	return {n, props};
}

/**
 * «aparecer» como hook: sube distancia/subida, escala desde escala/entrada y funde con la curva exacta del token.
 * Funciona igual en iOS, Android y web. Reducido: solo funde, misma duración.
 */
export function useEntrada(retraso = 0) {
	const reducido = useMovimientoReducido();
	const p = useSharedValue(0);
	useEffect(() => {
		p.value = withDelay(retraso, withTiming(1, tiempo('aparecer/duracion', 'aparecer/curva')));
	}, []); // eslint-disable-line react-hooks/exhaustive-deps
	const subida = TOKENS.distancia.subida;
	const escala = TOKENS.escala.entrada;
	return useAnimatedStyle(() =>
		reducido
			? {opacity: p.value}
			: {opacity: p.value, transform: [{translateY: (1 - p.value) * subida}, {scale: escala + (1 - escala) * p.value}]},
	);
}

/** Retrasos de una cascada (máximo y tope del sistema), para entradaKino(retraso). */
export const useCascada = (n: number) => useMemo(() => escalonar(n), [n]);

/** Reloj de un minuto para textos que cuentan tiempo real («hace 3 min»). */
export function useMinuto() {
	const [ahora, setAhora] = useState(() => Date.now());
	useEffect(() => {
		const id = setInterval(() => setAhora(Date.now()), 30_000);
		return () => clearInterval(id);
	}, []);
	return ahora;
}

export {Animated};
