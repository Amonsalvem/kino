// Piezas de marca para las composiciones: tarjeta de Pase, chip, burbuja, botón y fila de Portería.
// Solo tokens: colores por nombre semántico, radios y espacios del repositorio.
import React from 'react';
import {cancelRender, continueRender, delayRender} from 'remotion';
import '../../../../fonts/archivo.css';
import '../../../../fonts/jetbrains-mono.css';
import {color, ESP, ETIQUETA, Estado, LINEA, RADIO} from './tokens';

// Fuentes locales del repositorio (branding/sistema/fonts): el render no depende de la red.
export const ARCHIVO = "'Archivo', sans-serif";
export const MONO = "'JetBrains Mono', monospace";
const esperaFuentes = delayRender('Cargando Archivo y JetBrains Mono');
Promise.all(['400 16px Archivo', '700 16px Archivo', '800 16px Archivo', '400 16px "JetBrains Mono"'].map((f) => document.fonts.load(f, 'Pase ñ·–')))
	.then(() => continueRender(esperaFuentes))
	.catch((err) => cancelRender(err));

const fondoEstado = (e: Estado) => color(`estado/${e}/fondo`);

export const Chip: React.FC<{estado: Estado; brillo?: number}> = ({estado, brillo = 0}) => {
	const discontinuo = estado === 'sin-confirmar';
	const punto = ESP.xs - ESP['3xs'];
	return (
		<span
			style={{
				display: 'inline-flex',
				alignItems: 'center',
				gap: ESP['2xs'] + ESP['3xs'],
				padding: `${ESP['2xs']}px ${ESP.s}px`,
				borderRadius: RADIO.chip,
				border: `${LINEA.fino}px ${discontinuo ? 'dashed' : 'solid'} ${color(`estado/${estado}/borde`)}`,
				background: fondoEstado(estado),
				color: color(`estado/${estado}/texto`),
				fontFamily: ARCHIVO,
				fontWeight: 700,
				fontSize: 13,
				lineHeight: 1.3,
				whiteSpace: 'nowrap',
			}}
		>
			<span style={{position: 'relative', width: punto, height: punto}}>
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
			{ETIQUETA[estado]}
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
};

export const Tarjeta: React.FC<TarjetaProps> = ({estado, quien, dato, evidencia, barra, brillo, relleno = 'superficie/membrana', quienMono, ancho = 360}) => {
	const pad = ESP.m + ESP['2xs'];
	return (
		<div
			style={{
				width: ancho,
				boxSizing: 'border-box',
				padding: pad,
				borderRadius: RADIO.tarjeta,
				border: `${LINEA.fino}px ${estado === 'sin-confirmar' ? 'dashed' : 'solid'} ${color(`estado/${estado}/borde`)}`,
				background: color(relleno),
				display: 'flex',
				flexDirection: 'column',
				gap: ESP.xs,
			}}
		>
			<div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: ESP.s}}>
				<span style={{fontFamily: quienMono ? MONO : ARCHIVO, fontWeight: quienMono ? 400 : 700, fontSize: 17, color: color('texto/primario')}}>
					{quien}
				</span>
				<Chip estado={estado} brillo={brillo} />
			</div>
			{dato ? <span style={{fontFamily: MONO, fontSize: 13, color: color('texto/secundario')}}>{dato}</span> : null}
			{evidencia ? <span style={{fontFamily: MONO, fontSize: 12, color: color(`estado/${estado}/texto`)}}>{evidencia}</span> : null}
			{barra === undefined ? null : (
				// Pista en elevada: la tarjeta es membrana (M3D-4) y la pista debe verse sobre ella.
				<div style={{height: ESP['2xs'], borderRadius: ESP['3xs'], background: color('superficie/elevada'), overflow: 'hidden', marginTop: ESP['2xs']}}>
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
