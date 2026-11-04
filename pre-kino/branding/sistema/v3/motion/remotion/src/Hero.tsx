// hero-ciclo-del-pase y su versión vertical.
// Supuestos: 60 fps (tokens.motion.json); la pausa entre tiempos es un ciclo de duracion/latir (pregunta pendiente
// del inventario); la aurora es fija y nunca queda detrás de un QR (esta composición no muestra QR).
import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {Boton, Burbuja, Tarjeta} from './piezas';
import {avance, latido, lineaDeTiempo} from './tiempo';
import {AURORA, dur, ESP, Estado, SUBIDA} from './tokens';

export const HERO = lineaDeTiempo([
	{id: 'presionar', duracion: 'responder/duracion'},
	{id: 'aparecer', duracion: 'aparecer/duracion'},
	{id: 'enviar', duracion: 'aparecer/duracion'},
	{id: 'espera', duracion: 'duracion/latir'},
	{id: 'confirmar', duracion: 'aparecer/duracion'},
	{id: 'vigente', duracion: 'latir/duracion', veces: 2},
	{id: 'porVencer', duracion: 'responder/duracion'},
	{id: 'caducar', duracion: 'caducar/duracion'},
	{id: 'pausa', duracion: 'duracion/latir'},
]);

/** Póster: primer frame del Pase vigente, con la línea de evidencia del lector ya visible. */
export const POSTER_HERO = HERO.tramos.vigente.inicio;

const QUIEN = 'Andrés Gómez';
const DATO = 'Casa 14 · hoy 4:00–6:00 p. m.';
const EVIDENCIA = 'Confirmó Lector Portería · 3:58 p. m.';

export type HeroProps = {reducido: boolean; vertical: boolean; poster?: number};

export const Hero: React.FC<HeroProps> = ({reducido, vertical}) => {
	const f = useCurrentFrame();
	const {tramos} = HERO;
	const pulsar = avance(f, tramos.presionar, 'responder/curva');
	const soltar = avance(f, {inicio: tramos.aparecer.inicio, fin: tramos.aparecer.inicio + dur('responder/duracion')}, 'responder/curva');
	const a = avance(f, tramos.aparecer, 'aparecer/curva');
	const e = avance(f, tramos.enviar, 'aparecer/curva');
	const c = avance(f, tramos.confirmar, 'aparecer/curva');
	const v = avance(f, tramos.porVencer, 'responder/curva');
	const k = avance(f, tramos.caducar, 'caducar/curva');
	const brillo = reducido ? 0 : latido(f, tramos.vigente);

	// Un Pase solo es vigente después de confirmar: la capa vigente vale c, que es 0 antes de ese tramo.
	const capas: {estado: Estado; opacidad: number; dato: string; evidencia?: string; barra?: number}[] = [
		{estado: 'previsto', opacidad: 1 - e, dato: DATO},
		{estado: 'sin-confirmar', opacidad: e * (1 - c), dato: 'Casa 14 · enviado 3:41 p. m.'},
		{estado: 'vigente', opacidad: c * (1 - v), dato: DATO, evidencia: EVIDENCIA, barra: 1},
		{estado: 'por-vencer', opacidad: v * (1 - k), dato: 'Casa 14 · vence 6:00 p. m.', evidencia: EVIDENCIA, barra: 1 - k},
		{estado: 'vencido', opacidad: k, dato: 'Casa 14 · venció 6:00 p. m.', barra: 0},
	];
	const desplazar = (p: number) => (reducido ? 0 : SUBIDA * (1 - p));
	const escala = vertical ? 2.4 : 2;

	return (
		<AbsoluteFill style={{background: AURORA}}>
			<AbsoluteFill
				style={{
					display: 'flex',
					flexDirection: vertical ? 'column' : 'row',
					alignItems: 'center',
					justifyContent: 'center',
					gap: ESP.l,
					transform: `scale(${escala})`,
				}}
			>
				<div style={{display: 'flex', flexDirection: 'column', gap: ESP.l, alignItems: 'center'}}>
					<div style={{position: 'relative', width: 360, height: 176, opacity: a, transform: `translateY(${desplazar(a)}px)`}}>
						{capas.map((p) => (
							<div key={p.estado} style={{position: 'absolute', inset: 0, opacity: p.opacidad}}>
								<Tarjeta estado={p.estado} quien={QUIEN} dato={p.dato} evidencia={p.evidencia} barra={p.barra} brillo={p.estado === 'vigente' ? brillo : 0} />
							</div>
						))}
					</div>
					<Boton activo={pulsar * (1 - soltar)} />
				</div>
				<div style={{width: 320, height: 150, opacity: e, transform: `translateY(${desplazar(e)}px)`}}>
					<Burbuja lineas={['Carolina Ruiz, de la Casa 14, te dio un Pase para hoy.']} vigencia="Vigencia 4:00–6:00 p. m." />
				</div>
			</AbsoluteFill>
		</AbsoluteFill>
	);
};
