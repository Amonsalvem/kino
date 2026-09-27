// composicion-revocado y composicion-turno-porteria.
// Supuestos: 60 fps; en el turno de Portería, la separación entre lecturas es un ciclo de duracion/latir
// (misma convención de pausa que el hero, pendiente de aprobación).
import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {ARCHIVO, Evento, FilaPorteria, PaseEnSecuencia} from './piezas';
import {avance, latido, lineaDeTiempo, Tramo} from './tiempo';
import {color, dur, ESP, LINEA, SUBIDA} from './tokens';

export const REVOCADO = lineaDeTiempo([
	{id: 'aparecer', duracion: 'aparecer/duracion'},
	{id: 'vigente', duracion: 'latir/duracion'},
	{id: 'revocar', duracion: 'revocar/duracion'},
	{id: 'rechazar', duracion: 'duracion/crecer'},
]);
// Último frame: la composición dura total + 1 para que el valor final de cada tramo sea visible.
export const POSTER_REVOCADO = REVOCADO.total;

const titulo = (texto: string) => (
	<span style={{fontFamily: ARCHIVO, fontWeight: 700, fontSize: 20, color: color('texto/secundario')}}>{texto}</span>
);

export const Revocado: React.FC<{reducido: boolean; poster?: number}> = ({reducido}) => {
	const f = useCurrentFrame();
	const {tramos} = REVOCADO;
	const a = avance(f, tramos.aparecer, 'aparecer/curva');
	const r = avance(f, tramos.revocar, 'revocar/curva');
	const x = avance(f, tramos.rechazar, 'curva/crecer');
	const brillo = reducido ? 0 : latido(f, tramos.vigente);
	const evento: Evento = {estado: 'rechazado', placa: 'KMN 305', detalle: 'Casa 14 · 4:16 p. m.', motivo: 'Pase revocado por Carolina Ruiz a las 4:10 p. m.'};
	return (
		<AbsoluteFill style={{background: color('superficie/abismo'), display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: ESP['4xl']}}>
			<div style={{display: 'flex', flexDirection: 'column', gap: ESP.m, transform: 'scale(1.6)'}}>
				{titulo('Kino · Casa 14')}
				<div style={{position: 'relative', width: 360, height: 150, opacity: a, transform: `translateY(${reducido ? 0 : SUBIDA * (1 - a)}px)`}}>
					<PaseEnSecuencia frame={f} quien="Andrés Gómez" style={{position: 'absolute', inset: 0}}
						estados={[
							{estado: 'vigente', dato: 'Casa 14 · hoy 4:00–6:00 p. m.', evidencia: 'Confirmó Lector Portería · 3:58 p. m.', brillo},
							{estado: 'revocado', dato: 'Casa 14 · hoy 4:00–6:00 p. m.', evidencia: 'Revocó Carolina Ruiz · 4:10 p. m.', relleno: 'superficie/base'},
						]}
						cambios={[{tramo: tramos.revocar, curva: 'revocar/curva'}]} />
					{reducido ? null : (
						<div
							style={{
								position: 'absolute',
								left: 0,
								right: 0,
								top: '42%',
								height: LINEA.foco,
								background: color('estado/revocado/texto'),
								transformOrigin: 'left center',
								transform: `scaleX(${r})`,
							}}
						/>
					)}
				</div>
			</div>
			<div style={{display: 'flex', flexDirection: 'column', gap: ESP.m, transform: 'scale(1.3)'}}>
				{titulo('Kino Portería · Entrada principal')}
				<div style={{opacity: x, transform: `translateY(${reducido ? 0 : SUBIDA * (1 - x)}px)`}}>
					<FilaPorteria evento={evento} destello={reducido ? 0 : 1 - x} />
				</div>
			</div>
		</AbsoluteFill>
	);
};

// Turno de Portería: las filas entran solo cuando hay lectura; las que llegan juntas se escalonan.
const LECTURAS: Evento[][] = [
	[
		{estado: 'vigente', placa: 'KMN 305', detalle: 'Casa 14 · 6:02 p. m. · otorgó Carolina Ruiz'},
		{estado: 'vigente', placa: 'Código 4817', detalle: 'Casa 3 · 6:02 p. m. · otorgó Luz Marina'},
	],
	[{estado: 'vigente', placa: 'TRX 118', detalle: 'Casa 22 · 6:09 p. m. · colaborador'}],
	[{estado: 'rechazado', placa: 'KMN 305', detalle: 'Casa 14 · 6:12 p. m.', motivo: 'Pase vencido a las 6:00 p. m.'}],
	[
		{estado: 'vigente', placa: 'Código 2093', detalle: 'Casa 9 · 6:20 p. m. · otorgó Diana Arango'},
		{estado: 'vigente', placa: 'LPD 740', detalle: 'Casa 31 · 6:20 p. m. · colaborador'},
		{estado: 'vigente', placa: 'Código 5561', detalle: 'Casa 31 · 6:20 p. m. · colaborador'},
	],
];

const filasTurno = () => {
	const pausa = dur('duracion/latir');
	const esc = dur('escalonado/filas');
	const crecer = dur('duracion/crecer');
	const filas: {evento: Evento; tramo: Tramo}[] = [];
	LECTURAS.forEach((grupo, g) =>
		grupo.forEach((evento, i) => {
			const inicio = g * pausa + i * esc;
			filas.push({evento, tramo: {inicio, fin: inicio + crecer}});
		}),
	);
	return filas;
};
export const TURNO = {filas: filasTurno(), total: Math.max(...filasTurno().map((x) => x.tramo.fin))};
export const POSTER_TURNO = TURNO.total;

export const TurnoPorteria: React.FC<{reducido: boolean; poster?: number}> = ({reducido}) => {
	const f = useCurrentFrame();
	return (
		<AbsoluteFill style={{background: color('superficie/abismo'), alignItems: 'center', justifyContent: 'center'}}>
			<div style={{display: 'flex', flexDirection: 'column', gap: ESP.s, transform: 'scale(1.35)'}}>
				{titulo('Kino Portería · Entrada principal · hoy')}
				{TURNO.filas.map(({evento, tramo}, i) => {
					const p = avance(f, tramo, 'curva/crecer');
					return (
						<div key={i} style={{opacity: p, transform: `translateY(${reducido ? 0 : SUBIDA * (1 - p)}px)`}}>
							<FilaPorteria evento={evento} destello={!reducido && evento.estado === 'rechazado' && p > 0 ? 1 - p : 0} />
						</div>
					);
				})}
			</div>
		</AbsoluteFill>
	);
};
