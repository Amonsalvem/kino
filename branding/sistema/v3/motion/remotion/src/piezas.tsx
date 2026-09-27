// Piezas de marca para las composiciones: tarjeta de Pase, chip, burbuja, botón y fila de Portería.
// Solo tokens: colores por nombre semántico, radios y espacios del repositorio.
import React from 'react';
import {cancelRender, continueRender, delayRender} from 'remotion';
import '../../../../fonts/archivo.css';
import '../../../../fonts/jetbrains-mono.css';
import {fundidoDeTexto, Tramo} from './tiempo';
import {color, ESP, ETIQUETA, Estado, LINEA, RADIO} from './tokens';

// Fuentes locales del repositorio (branding/sistema/fonts): el render no depende de la red.
export const ARCHIVO = "'Archivo', sans-serif";
export const MONO = "'JetBrains Mono', monospace";
const esperaFuentes = delayRender('Cargando Archivo y JetBrains Mono');
Promise.all(['400 16px Archivo', '700 16px Archivo', '800 16px Archivo', '400 16px "JetBrains Mono"'].map((f) => document.fonts.load(f, 'Pase ñ·–')))
	.then(() => continueRender(esperaFuentes))
	.catch((err) => cancelRender(err));

const fondoEstado = (e: Estado) => color(`estado/${e}/fondo`);

/** parte: 'cuerpo' dibuja fondo, borde y punto sin texto; 'textos' dibuja solo la etiqueta (misma geometría). */
export type Parte = 'todo' | 'cuerpo' | 'textos';
const T0 = 'transparent';

export const Chip: React.FC<{estado: Estado; brillo?: number; parte?: Parte; opTexto?: number}> = ({estado, brillo = 0, parte = 'todo', opTexto = 1}) => {
	const discontinuo = estado === 'sin-confirmar';
	const cuerpo = parte !== 'textos';
	const texto = parte !== 'cuerpo';
	const punto = ESP.xs - ESP['3xs'];
	return (
		<span
			style={{
				display: 'inline-flex',
				alignItems: 'center',
				gap: ESP['2xs'] + ESP['3xs'],
				padding: `${ESP['2xs']}px ${ESP.s}px`,
				borderRadius: RADIO.chip,
				border: `${LINEA.fino}px ${discontinuo ? 'dashed' : 'solid'} ${cuerpo ? color(`estado/${estado}/borde`) : T0}`,
				background: cuerpo ? fondoEstado(estado) : T0,
				color: texto ? color(`estado/${estado}/texto`) : T0,
				fontFamily: ARCHIVO,
				fontWeight: 700,
				fontSize: 13,
				lineHeight: 1.3,
				whiteSpace: 'nowrap',
			}}
		>
			<span style={{position: 'relative', width: punto, height: punto, opacity: cuerpo ? 1 : 0}}>
				<span
					style={{
						position: 'absolute',
						inset: 0,
						borderRadius: '50%',
						background: discontinuo ? 'transparent' : color(`estado/${estado}/borde`),
						border: discontinuo ? `${LINEA.fino}px dashed ${color(`estado/${estado}/borde`)}` : undefined,
					}}
				/>
				{estado === 'vigente' ? (
					<span style={{position: 'absolute', inset: 0, borderRadius: '50%', background: color('estado/vigente/texto'), opacity: brillo}} />
				) : null}
			</span>
			<span style={{opacity: texto ? opTexto : 1}}>{ETIQUETA[estado]}</span>
		</span>
	);
};

export type TarjetaProps = {
	estado: Estado;
	quien: string;
	dato?: string;
	evidencia?: string;
	barra?: number; // fracción de vigencia restante, 0 → 1
	brillo?: number;
	relleno?: string;
	quienMono?: boolean;
	ancho?: number;
	parte?: Parte;
	/** Opacidad de cada texto cuando parte = 'textos' (fundido a través, M3D-5). */
	op?: {quien?: number; chip?: number; dato?: number; evidencia?: number};
};

export const Tarjeta: React.FC<TarjetaProps> = ({estado, quien, dato, evidencia, barra, brillo, relleno = 'superficie/membrana', quienMono, ancho = 360, parte = 'todo', op = {}}) => {
	const pad = ESP.m + ESP['2xs'];
	const cuerpo = parte !== 'textos';
	const texto = parte !== 'cuerpo';
	const tinta = (token: string, o = 1) => ({color: texto ? color(token) : T0, opacity: texto ? o : 1});
	return (
		<div
			style={{
				width: ancho,
				boxSizing: 'border-box',
				padding: pad,
				borderRadius: RADIO.tarjeta,
				border: `${LINEA.fino}px ${estado === 'sin-confirmar' ? 'dashed' : 'solid'} ${cuerpo ? color(`estado/${estado}/borde`) : T0}`,
				background: cuerpo ? color(relleno) : T0,
				display: 'flex',
				flexDirection: 'column',
				gap: ESP.xs,
			}}
		>
			<div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: ESP.s}}>
				<span style={{fontFamily: quienMono ? MONO : ARCHIVO, fontWeight: quienMono ? 400 : 700, fontSize: 17, ...tinta('texto/primario', op.quien)}}>
					{quien}
				</span>
				<Chip estado={estado} brillo={brillo} parte={parte} opTexto={op.chip} />
			</div>
			{dato ? <span style={{fontFamily: MONO, fontSize: 13, ...tinta('texto/secundario', op.dato)}}>{dato}</span> : null}
			{evidencia ? <span style={{fontFamily: MONO, fontSize: 12, ...tinta(`estado/${estado}/texto`, op.evidencia)}}>{evidencia}</span> : null}
			{barra === undefined ? null : (
				// Pista en elevada: la tarjeta es membrana (M3D-4) y la pista debe verse sobre ella.
				<div style={{height: ESP['2xs'], borderRadius: ESP['3xs'], background: color('superficie/elevada'), overflow: 'hidden', marginTop: ESP['2xs'], opacity: cuerpo ? 1 : 0}}>
					<div
						style={{
							height: '100%',
							width: '100%',
							transformOrigin: 'left center',
							transform: `scaleX(${barra})`,
							background: color(`estado/${estado}/borde`),
						}}
					/>
				</div>
			)}
		</div>
	);
};

export const Burbuja: React.FC<{lineas: string[]; vigencia: string}> = ({lineas, vigencia}) => (
	<div
		style={{
			width: 320,
			boxSizing: 'border-box',
			padding: ESP.m,
			borderRadius: RADIO.tarjeta,
			background: color('superficie/membrana'),
			display: 'flex',
			flexDirection: 'column',
			gap: ESP['2xs'],
		}}
	>
		{lineas.map((l) => (
			<span key={l} style={{fontFamily: ARCHIVO, fontSize: 15, lineHeight: 1.4, color: color('texto/primario')}}>
				{l}
			</span>
		))}
		<span style={{fontFamily: MONO, fontSize: 13, color: color('texto/secundario')}}>{vigencia}</span>
	</div>
);

export const Boton: React.FC<{activo: number}> = ({activo}) => (
	<div style={{position: 'relative', width: 320, height: 56, borderRadius: RADIO.control, overflow: 'hidden'}}>
		<div style={{position: 'absolute', inset: 0, background: color('accion/fondo')}} />
		<div style={{position: 'absolute', inset: 0, background: color('accion/fondo-activo'), opacity: activo}} />
		<span
			style={{
				position: 'absolute',
				inset: 0,
				display: 'grid',
				placeItems: 'center',
				fontFamily: ARCHIVO,
				fontWeight: 700,
				fontSize: 16,
				color: color('accion/texto'),
			}}
		>
			Crear Pase
		</span>
	</div>
);

export type Evento = {estado: 'vigente' | 'rechazado'; placa: string; detalle: string; motivo?: string};

export const FilaPorteria: React.FC<{evento: Evento; destello?: number}> = ({evento, destello = 0}) => (
	<div
		style={{
			position: 'relative',
			width: 560,
			boxSizing: 'border-box',
			padding: ESP.m,
			borderRadius: RADIO.control,
			border: `${LINEA.fino}px solid ${color(`estado/${evento.estado}/borde`)}`,
			background: evento.estado === 'rechazado' ? fondoEstado('rechazado') : color('superficie/elevada'),
			display: 'grid',
			gridTemplateColumns: '1fr auto',
			rowGap: ESP['2xs'],
		}}
	>
		<span style={{fontFamily: MONO, fontSize: 18, letterSpacing: '0.06em', color: color('texto/primario')}}>{evento.placa}</span>
		<span style={{justifySelf: 'end'}}>
			<Chip estado={evento.estado} />
		</span>
		<span style={{fontFamily: MONO, fontSize: 12, color: color('texto/secundario')}}>{evento.detalle}</span>
		<span />
		{evento.motivo ? (
			<span style={{fontFamily: ARCHIVO, fontSize: 13, color: color(`estado/${evento.estado}/texto`)}}>{evento.motivo}</span>
		) : null}
		{destello > 0 ? (
			<span
				style={{
					position: 'absolute',
					inset: -LINEA.foco,
					borderRadius: RADIO.control,
					border: `${LINEA.foco}px solid ${color('estado/rechazado/borde')}`,
					opacity: destello,
				}}
			/>
		) : null}
	</div>
);

// Pase que cambia de estado ------------------------------------------------------------------------------------
export type EstadoDelPase = Omit<TarjetaProps, 'parte' | 'op' | 'quien'>;
export type Cambio = {tramo: Tramo; curva: string};

/**
 * Un Pase que pasa por varios estados. El cuerpo (fondo, bordes, chip, barra) se funde cruzado entre estados; los
 * textos van en una capa encima y se funden a través (M3D-5): el que sale se va en la primera mitad del verbo y el
 * que entra llega en la segunda, así nunca se enciman. cambios[i] es la transición del estado i al i + 1.
 */
export const PaseEnSecuencia: React.FC<{frame: number; quien: string; estados: EstadoDelPase[]; cambios: Cambio[]; style?: React.CSSProperties}> = ({frame, quien, estados, cambios, style}) => {
	const n = estados.length;
	const av = (c: Cambio) => fundidoDeTexto(frame, c.tramo, c.curva, 'a', 'a').entra; // avance con la curva del verbo
	const cuerpo = (i: number) => (i === 0 ? 1 : av(cambios[i - 1])) * (i === n - 1 ? 1 : 1 - av(cambios[i]));
	const textos = (e: EstadoDelPase) => ({quien, chip: ETIQUETA[e.estado], dato: e.dato ?? '', evidencia: e.evidencia ?? ''});
	const opTexto = (i: number, clave: 'quien' | 'chip' | 'dato' | 'evidencia') => {
		let o = 1;
		if (i > 0) {
			const c = cambios[i - 1];
			o *= frame < c.tramo.inicio ? 0 : fundidoDeTexto(frame, c.tramo, c.curva, textos(estados[i - 1])[clave], textos(estados[i])[clave]).entra;
		}
		if (i < n - 1) {
			const c = cambios[i];
			o *= frame >= c.tramo.fin ? 0 : frame < c.tramo.inicio ? 1 : fundidoDeTexto(frame, c.tramo, c.curva, textos(estados[i])[clave], textos(estados[i + 1])[clave]).sale;
		}
		return o;
	};
	return (
		<div style={{position: 'relative', ...style}}>
			{estados.map((e, i) => (
				<div key={`c-${e.estado}`} style={{position: 'absolute', inset: 0, opacity: cuerpo(i)}}>
					<Tarjeta {...e} quien={quien} parte="cuerpo" />
				</div>
			))}
			{estados.map((e, i) => (
				<div key={`t-${e.estado}`} style={{position: 'absolute', inset: 0}}>
					<Tarjeta {...e} quien={quien} parte="textos"
						op={{quien: opTexto(i, 'quien'), chip: opTexto(i, 'chip'), dato: opTexto(i, 'dato'), evidencia: opTexto(i, 'evidencia')}} />
				</div>
			))}
		</div>
	);
};
