// Matemática de gestos, sin DOM: la usan la web y la app (en la app, copiada como worklet).

/** Resistencia elástica: pasado el límite, el desplazamiento rinde cada vez menos (como en iOS). */
export const resistencia = (exceso: number, dimension: number, c = 0.55) =>
	Math.sign(exceso) * (1 - 1 / ((Math.abs(exceso) * c) / dimension + 1)) * dimension;

/** Dónde se detendría un lanzamiento con esa velocidad (px/s), con desaceleración por milisegundo. */
export const proyectar = (pos: number, velocidad: number, desaceleracion = 0.998) => pos + (velocidad / 1000) * (desaceleracion / (1 - desaceleracion));
