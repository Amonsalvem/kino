import React from 'react';
import {Composition} from 'remotion';
import manifiesto from '../../lottie/manifiesto.json';
import {POSTER_REVOCADO, POSTER_TURNO, REVOCADO, Revocado, TURNO, TurnoPorteria} from './Composiciones';
import {HERO, Hero, POSTER_HERO} from './Hero';
import {ESP, FPS} from './tokens';
import {pausaVista, VistaLottie} from './VistaLottie';

const par = (n: number) => Math.ceil(n / 2) * 2;

// Composiciones «remotion»: defaultProps.poster es el frame del póster; el pipeline codifica AV1, H.264 y AVIF.

export const Raiz: React.FC = () => (
	<>
		{[false, true].map((reducido) => {
			const s = reducido ? '-reducido' : '';
			return (
				<React.Fragment key={s}>
					<Composition id={`hero-ciclo-del-pase${s}`} component={Hero} durationInFrames={HERO.total} fps={FPS} width={1920} height={1080}
						defaultProps={{reducido, vertical: false, poster: POSTER_HERO}} />
					<Composition id={`hero-ciclo-del-pase-movil${s}`} component={Hero} durationInFrames={HERO.total} fps={FPS} width={1080} height={1350}
						defaultProps={{reducido, vertical: true, poster: POSTER_HERO}} />
					<Composition id={`composicion-revocado${s}`} component={Revocado} durationInFrames={REVOCADO.total + 1} fps={FPS} width={1920} height={1080}
						defaultProps={{reducido, poster: POSTER_REVOCADO}} />
					<Composition id={`composicion-turno-porteria${s}`} component={TurnoPorteria} durationInFrames={TURNO.total + 1} fps={FPS} width={1920} height={1080}
						defaultProps={{reducido, poster: POSTER_TURNO}} />
				</React.Fragment>
			);
		})}
		{manifiesto.recursos.map((r) => {
			const margen = r.ancho >= 1920 ? 0 : ESP.l;
			return (
				<Composition
					key={r.archivo}
					id={`vista-${r.id}${r.reducido ? '-reducido' : ''}`}
					component={VistaLottie}
					durationInFrames={pausaVista() * 2 + r.op}
					fps={r.fps}
					width={par(r.ancho + margen * 2)}
					height={par(r.alto + margen * 2)}
					defaultProps={{archivo: r.archivo, op: r.op, ancho: r.ancho, alto: r.alto, loop: r.loop, aurora: r.id === 'presentacion-cortina'}}
				/>
			);
		})}
	</>
);
