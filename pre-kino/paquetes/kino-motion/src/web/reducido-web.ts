// Keyframes de WAAPI en modo reducido (parte web; el núcleo no conoce el DOM).
/** Keyframes de WAAPI en modo reducido: se quitan transformaciones; si no queda nada, se funde. */
export function reducirKeyframes(frames: Keyframe[]): Keyframe[] {
	const sinMover = frames.map((f) => {
		const {transform: _t, translate: _tr, scale: _s, rotate: _r, ...resto} = f as Record<string, unknown>;
		return resto as Keyframe;
	});
	const cambia = sinMover.some((f) => Object.keys(f).some((k) => !['offset', 'easing', 'composite'].includes(k)));
	return cambia ? sinMover : [];
}
