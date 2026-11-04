// Wrapper @remotion/lottie que produce el mp4_preview de cada recurso Lottie.
// Supuestos: la pausa antes y después de la animación dura un ciclo de duracion/latir (solo en la vista previa,
// no en el recurso); el fondo es superficie/abismo porque los recursos tienen fondo transparente. La cortina se
// ve sobre la aurora (la lámina siguiente de una presentación); si no, sus hojas se confunden con el fondo.
import React, {useEffect, useState} from 'react';
import {AbsoluteFill, cancelRender, continueRender, delayRender, Freeze, Sequence, staticFile} from 'remotion';
import {Lottie, LottieAnimationData} from '@remotion/lottie';
import {AURORA, color, dur} from './tokens';
import './piezas'; // carga Archivo y JetBrains Mono antes del primer frame

export type VistaLottieProps = {archivo: string; op: number; ancho: number; alto: number; loop: boolean; aurora?: boolean};

export const pausaVista = () => dur('duracion/latir');

export const VistaLottie: React.FC<VistaLottieProps> = ({archivo, op, ancho, alto, loop, aurora}) => {
	const [datos, setDatos] = useState<LottieAnimationData | null>(null);
	const [handle] = useState(() => delayRender(`Cargando ${archivo}`));
	useEffect(() => {
		fetch(staticFile(archivo))
			.then((r) => r.json())
			.then((json) => {
				setDatos(json);
				continueRender(handle);
			})
			.catch((err) => cancelRender(err));
	}, [archivo, handle]);
	if (!datos) return null;
	const pausa = pausaVista();
	const lottie = <Lottie animationData={datos} loop={loop} style={{width: ancho, height: alto}} />;
	return (
		<AbsoluteFill style={{background: aurora ? AURORA : color('superficie/abismo'), alignItems: 'center', justifyContent: 'center'}}>
			<div style={{width: ancho, height: alto}}>
				<Sequence durationInFrames={pausa} layout="none">
					<Freeze frame={0}>{lottie}</Freeze>
				</Sequence>
				<Sequence from={pausa} durationInFrames={op} layout="none">
					{lottie}
				</Sequence>
				<Sequence from={pausa + op} layout="none">
					<Freeze frame={Math.max(op - 1, 0)}>{lottie}</Freeze>
				</Sequence>
			</div>
		</AbsoluteFill>
	);
};
