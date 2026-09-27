// Componentes de referencia para la app: el Pase, el chip de estado, el botón, la hoja, la espera del lector y el número.
// Dibujan con los tokens de marca del tema del sistema; las fuentes se pasan por FuentesKino (la app las carga).
import React, {createContext, useContext, useEffect, useMemo, type ReactNode} from 'react';
import {Pressable, StyleSheet, Text, TextInput, View, type StyleProp, type TextStyle, type ViewStyle} from 'react-native';
import {GestureDetector} from 'react-native-gesture-handler';
import Animated, {interpolateColor, useAnimatedStyle, useSharedValue, withTiming} from 'react-native-reanimated';
import {tiempo} from './configuracion';
import {useEntrada, usePaseMotion, useHoja, useMinuto, useNumeroAnimado, usePresion, useTemaKino, useVigencia, type Tema} from './hooks';
import {TOKENS, type Estado, type Evidencia} from './nucleo';

// Fuentes ----------------------------------------------------------------------------------------------------
export type Fuentes = {titulo: string; texto: string; dato: string};
const FuentesContexto = createContext<Fuentes>({titulo: 'Archivo-Bold', texto: 'Archivo-Regular', dato: 'JetBrainsMono-Regular'});
/** Nombres de las fuentes cargadas por la app (expo-font o react-native.config.js). */
export const FuentesKino = ({fuentes, children}: {fuentes: Fuentes; children: ReactNode}) => (
	<FuentesContexto.Provider value={fuentes}>{children}</FuentesContexto.Provider>
);
const useFuentes = () => useContext(FuentesContexto);

const ETIQUETA: Record<Estado, string> = {
	previsto: 'Previsto', 'sin-confirmar': 'Sin confirmar', vigente: 'Vigente', 'por-vencer': 'Por vencer',
	vencido: 'Vencido', usado: 'Usado', revocado: 'Revocado',
};
const E = TOKENS.forma.espacio;
const R = TOKENS.forma.radio;
const hora = (d: Date) => d.toLocaleTimeString('es-CO', {hour: 'numeric', minute: '2-digit'});

// Pase -------------------------------------------------------------------------------------------------------
export type PaseKinoProps = {
	quien?: string;
	codigo?: string;
	casa: string;
	desde: Date;
	hasta: Date;
	estado: Estado;
	enviado?: Date;
	evidencia?: Evidencia | null;
	revocacion?: {nombre: string; hora: Date} | null;
	usadoEn?: Date;
	tema?: Tema;
	style?: StyleProp<ViewStyle>;
	testID?: string;
};

/** La tarjeta del Pase. Cada cambio de `estado` ejecuta su partitura; vigente sin evidencia se muestra sin confirmar. */
export function PaseKino(p: PaseKinoProps) {
	const f = useFuentes();
	const {estado, estilos, valores, color} = usePaseMotion(p.estado, p.evidencia, p.tema);
	const vigencia = useVigencia(p.desde, p.hasta, estado);
	const barra = useAnimatedStyle(() => ({transform: [{scaleX: vigencia.value * valores.barraEscala.value}]}));
	const franja = `${hora(p.desde)}–${hora(p.hasta)}`;
	const dato: Record<Estado, string> = {
		previsto: `${p.casa} · ${franja}`,
		'sin-confirmar': `${p.casa} · enviado ${p.enviado ? hora(p.enviado) : ''}`,
		vigente: `${p.casa} · ${franja}`,
		'por-vencer': `${p.casa} · vence ${hora(p.hasta)}`,
		vencido: `${p.casa} · venció ${hora(p.hasta)}`,
		usado: `${p.casa} · entró ${p.usadoEn ? hora(p.usadoEn) : ''}`,
		revocado: `${p.casa} · ${franja}`,
	};
	const nota =
		(estado === 'vigente' || estado === 'por-vencer') && p.evidencia
			? `Confirmó ${p.evidencia.lector} · ${hora(p.evidencia.hora)}`
			: estado === 'revocado' && p.revocacion
				? `Revocó ${p.revocacion.nombre} · ${hora(p.revocacion.hora)}`
				: '';
	const colorNota = estado === 'revocado' ? color('estado/revocado/texto') : color('estado/vigente/texto');
	const colorBarra = estado === 'por-vencer' ? color('estado/por-vencer/borde') : ['vencido', 'usado', 'revocado'].includes(estado) ? color('estado/vencido/borde') : color('estado/vigente/borde');

	return (
		<Animated.View
			testID={p.testID}
			accessibilityRole="summary"
			accessibilityLabel={`${p.quien ?? p.codigo}, ${ETIQUETA[estado]}, ${dato[estado]}. ${nota}`}
			style={[s.tarjeta, {backgroundColor: color(estado === 'revocado' ? 'superficie/base' : 'superficie/elevada')}, estilos.tarjeta, p.style]}
		>
			<Animated.View pointerEvents="none" style={[StyleSheet.absoluteFill, s.borde, estilos.bordeContinuo]} />
			<Animated.View pointerEvents="none" style={[StyleSheet.absoluteFill, s.borde, {borderStyle: 'dashed', borderColor: color('estado/sin-confirmar/borde')}, estilos.bordeDiscontinuo]} />
			<View style={s.cabeza}>
				<View>
					<Text style={[s.quien, {color: color('texto/primario'), fontFamily: p.codigo ? f.dato : f.titulo}]}>{p.codigo ?? p.quien}</Text>
					{p.codigo ? <Animated.View style={[s.tachado, {backgroundColor: color('estado/usado/texto')}, estilos.tachado]} /> : null}
				</View>
				<ChipAnimado estado={estado} estilos={estilos} fuente={f.titulo} discontinuo={estado === 'sin-confirmar'} />
			</View>
			<Text style={[s.dato, {color: color('texto/secundario'), fontFamily: f.dato}]}>{dato[estado]}</Text>
			<Animated.Text style={[s.nota, {color: colorNota, fontFamily: f.dato}, estilos.nota]}>{nota}</Animated.Text>
			<Animated.View style={[s.pista, {backgroundColor: color('superficie/membrana')}, estilos.barra]}>
				<Animated.View style={[s.barra, {backgroundColor: colorBarra}, barra]} />
			</Animated.View>
			<Animated.View pointerEvents="none" style={[s.corte, {backgroundColor: color('estado/revocado/texto')}, estilos.corte]} />
		</Animated.View>
	);
}

function ChipAnimado({estado, estilos, fuente, discontinuo}: {estado: Estado; estilos: ReturnType<typeof usePaseMotion>['estilos']; fuente: string; discontinuo: boolean}) {
	return (
		<Animated.View accessibilityRole="text" style={[s.chip, discontinuo && {borderStyle: 'dashed'}, estilos.chip]}>
			<Animated.View style={[s.punto, estilos.punto]}>
				<Animated.View style={[StyleSheet.absoluteFill, s.puntoBrillo, estilos.brillo]} />
			</Animated.View>
			<Animated.Text style={[s.chipTexto, {fontFamily: fuente}, estilos.chipTexto]}>{ETIQUETA[estado]}</Animated.Text>
		</Animated.View>
	);
}

/** Chip de estado suelto (listas, encabezados). */
export function EstadoKino({estado, evidencia, tema}: {estado: Estado; evidencia?: Evidencia | null; tema?: Tema}) {
	const f = useFuentes();
	const m = usePaseMotion(estado, evidencia, tema);
	return <ChipAnimado estado={m.estado} estilos={m.estilos} fuente={f.titulo} discontinuo={m.estado === 'sin-confirmar'} />;
}

// Entrar -----------------------------------------------------------------------------------------------------
/** Envuelve lo que aparece: «aparecer» con retraso (de useCascada), exacto en todas las plataformas. */
export function EntraKino({retraso = 0, children, style}: {retraso?: number; children: ReactNode; style?: StyleProp<ViewStyle>}) {
	const estilo = useEntrada(retraso);
	return <Animated.View style={[estilo, style]}>{children}</Animated.View>;
}

// Botón ------------------------------------------------------------------------------------------------------
export function BotonKino({children, onPress, variante = 'primaria', tema, style}: {children: ReactNode; onPress?: () => void; variante?: 'primaria' | 'secundaria'; tema?: Tema; style?: StyleProp<ViewStyle> | false}) {
	const f = useFuentes();
	const {color} = useTemaKino(tema);
	const pr = usePresion();
	const [reposo, activo, texto] =
		variante === 'primaria' ? [color('accion/fondo'), color('accion/fondo-activo'), color('accion/texto')] : [color('superficie/membrana'), color('superficie/elevada'), color('texto/primario')];
	const fondo = useAnimatedStyle(() => ({backgroundColor: interpolateColor(pr.activo.value, [0, 1], [reposo, activo])}));
	return (
		<Pressable accessibilityRole="button" onPress={onPress} onPressIn={pr.alPresionar} onPressOut={pr.alSoltar}>
			<Animated.View style={[s.boton, fondo, pr.estilo, style]}>
				<Text style={[s.botonTexto, {color: texto, fontFamily: f.titulo}]}>{children}</Text>
			</Animated.View>
		</Pressable>
	);
}

// Hoja -------------------------------------------------------------------------------------------------------
/** Hoja inferior arrastrable. Requiere GestureHandlerRootView en la raíz de la app. */
export function HojaKino({abierta, alCerrar, altura = 420, children, tema}: {abierta: boolean; alCerrar: () => void; altura?: number; children: ReactNode; tema?: Tema}) {
	const {color} = useTemaKino(tema);
	const h = useHoja(altura, alCerrar);
	useEffect(() => {
		if (abierta) h.abrir();
	}, [abierta]); // eslint-disable-line react-hooks/exhaustive-deps
	if (!abierta) return null;
	return (
		<View style={StyleSheet.absoluteFill} accessibilityViewIsModal>
			<Pressable style={StyleSheet.absoluteFill} onPress={() => h.cerrar()} accessibilityLabel="Cerrar">
				<Animated.View style={[StyleSheet.absoluteFill, {backgroundColor: color('superficie/abismo')}, h.estiloVelo]} />
			</Pressable>
			<Animated.View style={[s.hoja, {height: altura, backgroundColor: color('superficie/elevada')}, h.estiloHoja]}>
				<GestureDetector gesture={h.gesto}>
					<View style={s.asa} accessibilityLabel="Arrastra para cerrar">
						<View style={[s.asaMarca, {backgroundColor: color('texto/tenue')}]} />
					</View>
				</GestureDetector>
				{children}
			</Animated.View>
		</View>
	);
}

// Espera del lector ------------------------------------------------------------------------------------------
/** La espera real del lector, sin spinner: la línea llega una vez y el texto cuenta los minutos. */
export function EsperaLectorKino({lector, enviado, confirmado, tema}: {lector: string; enviado: Date; confirmado?: Date | null; tema?: Tema}) {
	const f = useFuentes();
	const {color} = useTemaKino(tema);
	const ahora = useMinuto();
	const trazo = useSharedValue(0);
	const ok = useSharedValue(confirmado ? 1 : 0);
	useEffect(() => {
		trazo.value = withTiming(1, tiempo('duracion/trazo', 'curva/crecer'));
	}, []); // eslint-disable-line react-hooks/exhaustive-deps
	useEffect(() => {
		ok.value = withTiming(confirmado ? 1 : 0, tiempo('aparecer/duracion', 'aparecer/curva'));
	}, [confirmado]); // eslint-disable-line react-hooks/exhaustive-deps
	const sin = color('estado/sin-confirmar/borde');
	const vig = color('estado/vigente/borde');
	const linea = useAnimatedStyle(() => ({transform: [{scaleX: trazo.value}], backgroundColor: interpolateColor(ok.value, [0, 1], [sin, vig])}));
	const nodo = useAnimatedStyle(() => ({borderColor: interpolateColor(ok.value, [0, 1], [sin, vig])}));
	const min = Math.floor((ahora - enviado.getTime()) / 60_000);
	const texto = confirmado ? `Confirmó ${lector} · ${hora(confirmado)}` : `Enviado ${hora(enviado)} · ${lector} aún no confirma${min >= 1 ? ` · ${min} min` : ''}`;
	return (
		<View accessibilityLiveRegion="polite">
			<View style={s.flujo}>
				<View style={[s.nodo, {borderColor: sin, borderStyle: 'dashed'}]} />
				<Animated.View style={[s.linea, linea]} />
				<Animated.View style={[s.nodo, nodo]} />
			</View>
			<Text style={[s.datoPeq, {color: confirmado ? color('estado/vigente/texto') : color('texto/secundario'), fontFamily: f.dato}]}>{texto}</Text>
		</View>
	);
}

// Número -----------------------------------------------------------------------------------------------------
const AnimatedTextInput = Animated.createAnimatedComponent(TextInput);
/** Número que cambia con resorte/firme, cifras tabulares y separador es-CO. */
export function NumeroKino({valor, decimales = 0, style}: {valor: number; decimales?: number; style?: StyleProp<TextStyle>}) {
	const {props} = useNumeroAnimado(valor, decimales);
	const inicial = useMemo(() => String(valor), []); // eslint-disable-line react-hooks/exhaustive-deps
	return <AnimatedTextInput editable={false} underlineColorAndroid="transparent" defaultValue={inicial} animatedProps={props} style={[{fontVariant: ['tabular-nums'], padding: 0}, style]} />;
}

const s = StyleSheet.create({
	tarjeta: {borderRadius: R.tarjeta, padding: E.m + E['2xs'], gap: E.xs, overflow: 'hidden'},
	borde: {borderRadius: R.tarjeta, borderWidth: 1},
	cabeza: {flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: E.s},
	quien: {fontSize: 17},
	tachado: {position: 'absolute', left: 0, right: 0, top: '55%', height: 2, transformOrigin: 'left'},
	dato: {fontSize: 13},
	nota: {fontSize: 12, minHeight: 16},
	pista: {height: 4, borderRadius: 2, overflow: 'hidden', marginTop: E['2xs']},
	barra: {flex: 1, transformOrigin: 'left'},
	corte: {position: 'absolute', left: 0, right: 0, top: '46%', height: 2, transformOrigin: 'left'},
	chip: {flexDirection: 'row', alignItems: 'center', gap: 6, paddingHorizontal: 10, paddingVertical: 3, borderRadius: R.chip, borderWidth: 1},
	punto: {width: 6, height: 6, borderRadius: 3, overflow: 'hidden'},
	puntoBrillo: {borderRadius: 3, backgroundColor: TOKENS.color.oscuro['estado/vigente/texto']},
	chipTexto: {fontSize: 13},
	boton: {minHeight: 48, paddingHorizontal: 20, borderRadius: R.control, alignItems: 'center', justifyContent: 'center'},
	botonTexto: {fontSize: 16},
	hoja: {position: 'absolute', left: 0, right: 0, bottom: 0, borderTopLeftRadius: 20, borderTopRightRadius: 20, paddingHorizontal: 20, paddingBottom: 28},
	asa: {height: 28, alignItems: 'center', justifyContent: 'center'},
	asaMarca: {width: 40, height: 4, borderRadius: 2},
	flujo: {flexDirection: 'row', alignItems: 'center', gap: 8},
	nodo: {width: 14, height: 14, borderRadius: 7, borderWidth: 1},
	linea: {flex: 1, height: 2, transformOrigin: 'left'},
	datoPeq: {fontSize: 13, marginTop: 10},
});
