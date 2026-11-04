// El Pase: estados, eventos y la partitura de movimiento de cada transición.
// Regla de estado honesto: un Pase solo es vigente si el lector lo confirmó. Aquí eso es estructural:
// el estado se deriva de hechos (estadoDelPase) y la única transición que llega a «vigente» exige evidencia.
import type {NombreCurva, NombreDuracion} from './tokens';

export type Estado = 'previsto' | 'sin-confirmar' | 'vigente' | 'por-vencer' | 'vencido' | 'usado' | 'revocado';
export const ESTADOS: readonly Estado[] = ['previsto', 'sin-confirmar', 'vigente', 'por-vencer', 'vencido', 'usado', 'revocado'];
export const TERMINALES: ReadonlySet<Estado> = new Set(['vencido', 'usado', 'revocado']);

export type Evidencia = {lector: string; hora: Date};
export type Autor = {nombre: string; hora: Date};

/** Hechos de un Pase tal como los registra el sistema. El estado visible sale de aquí, no se escribe a mano. */
export type Hechos = {
	desde: Date;
	hasta: Date;
	enviadoAlLector?: Date;
	confirmacion?: Evidencia;
	usadoEn?: Date;
	revocacion?: Autor;
};

/** Estado visible de un Pase en el instante `ahora`. avisoMs: ventana de aviso antes de vencer (la fija la administración). */
export function estadoDelPase(h: Hechos, ahora: Date, avisoMs: number): Estado {
	if (h.revocacion) return 'revocado';
	if (h.usadoEn) return 'usado';
	if (ahora.getTime() >= h.hasta.getTime()) return 'vencido';
	if (!h.confirmacion) return h.enviadoAlLector ? 'sin-confirmar' : 'previsto';
	if (ahora.getTime() < h.desde.getTime()) return 'previsto';
	return h.hasta.getTime() - ahora.getTime() <= avisoMs ? 'por-vencer' : 'vigente';
}

/** Fracción de vigencia que queda (1 al empezar, 0 al vencer). */
export function vigenciaRestante(h: Pick<Hechos, 'desde' | 'hasta'>, ahora: Date): number {
	const total = h.hasta.getTime() - h.desde.getTime();
	if (total <= 0) return 0;
	return Math.min(1, Math.max(0, (h.hasta.getTime() - ahora.getTime()) / total));
}

// Partitura --------------------------------------------------------------------------------------------
/** Partes de un Pase que se pueden mover. Cada plataforma las dibuja a su modo; la partitura es la misma. */
export type Parte = 'tarjeta' | 'borde' | 'chip' | 'punto' | 'barra' | 'corte' | 'tachado' | 'nota';
export type Propiedad = 'opacidad' | 'y' | 'escala' | 'escalaX' | 'color' | 'trazo';
export type Pista = {parte: Parte; propiedad: Propiedad; de: number | string; a: number | string};

export type Evento = 'enviar' | 'confirmar' | 'avisar' | 'caducar' | 'usar' | 'revocar';
export type Transicion = {
	evento: Evento;
	de: readonly Estado[];
	a: Estado;
	verbo: 'responder' | 'aparecer' | 'caducar' | 'revocar';
	duracion: NombreDuracion;
	curva: NombreCurva;
	pistas: readonly Pista[];
	/** Qué debe quedar en pantalla como prueba del cambio. */
	deja?: string;
	/** El punto late al terminar (solo al quedar vigente). */
	late?: boolean;
};

const chip = (de: Estado, a: Estado): Pista[] => [
	{parte: 'chip', propiedad: 'color', de, a},
	{parte: 'borde', propiedad: 'color', de, a},
];

export const TRANSICIONES: readonly Transicion[] = [
	{
		evento: 'enviar', de: ['previsto'], a: 'sin-confirmar', verbo: 'responder',
		duracion: 'responder/duracion', curva: 'responder/curva',
		pistas: [...chip('previsto', 'sin-confirmar'), {parte: 'borde', propiedad: 'trazo', de: 'continuo', a: 'discontinuo'}],
		deja: 'La hora de envío al lector.',
	},
	{
		evento: 'confirmar', de: ['sin-confirmar'], a: 'vigente', verbo: 'aparecer',
		duracion: 'aparecer/duracion', curva: 'aparecer/curva',
		pistas: [
			...chip('sin-confirmar', 'vigente'),
			{parte: 'borde', propiedad: 'trazo', de: 'discontinuo', a: 'continuo'},
			{parte: 'barra', propiedad: 'opacidad', de: 0, a: 1},
			{parte: 'nota', propiedad: 'opacidad', de: 0, a: 1},
			{parte: 'nota', propiedad: 'y', de: 'subida', a: 0},
		],
		deja: 'Qué lector confirmó y a qué hora.',
		late: true,
	},
	{
		evento: 'avisar', de: ['vigente'], a: 'por-vencer', verbo: 'responder',
		duracion: 'responder/duracion', curva: 'responder/curva',
		pistas: [...chip('vigente', 'por-vencer'), {parte: 'barra', propiedad: 'color', de: 'vigente', a: 'por-vencer'}],
		deja: 'La hora exacta de vencimiento.',
	},
	{
		evento: 'caducar', de: ['vigente', 'por-vencer', 'sin-confirmar', 'previsto'], a: 'vencido', verbo: 'caducar',
		duracion: 'caducar/duracion', curva: 'caducar/curva',
		pistas: [
			{parte: 'barra', propiedad: 'escalaX', de: 'actual', a: 0},
			{parte: 'tarjeta', propiedad: 'opacidad', de: 1, a: 0.72},
			...chip('vigente', 'vencido'),
		],
		deja: 'A qué hora venció.',
	},
	{
		evento: 'usar', de: ['vigente', 'por-vencer'], a: 'usado', verbo: 'responder',
		duracion: 'responder/duracion', curva: 'responder/curva',
		pistas: [{parte: 'tachado', propiedad: 'escalaX', de: 0, a: 1}, ...chip('vigente', 'usado')],
		deja: 'A qué hora entró.',
	},
	{
		evento: 'revocar', de: ['previsto', 'sin-confirmar', 'vigente', 'por-vencer'], a: 'revocado', verbo: 'revocar',
		duracion: 'revocar/duracion', curva: 'revocar/curva',
		pistas: [
			{parte: 'corte', propiedad: 'escalaX', de: 0, a: 1},
			{parte: 'tarjeta', propiedad: 'opacidad', de: 1, a: 0.72},
			...chip('vigente', 'revocado'),
			{parte: 'nota', propiedad: 'opacidad', de: 0, a: 1},
		],
		deja: 'Quién revocó y a qué hora.',
	},
];

export class TransicionInvalida extends Error {}

/** Busca la transición de un evento desde un estado. Lanza si no existe: nada salta estados en silencio. */
export function transicion(desde: Estado, evento: Evento): Transicion {
	const t = TRANSICIONES.find((x) => x.evento === evento && x.de.includes(desde));
	if (!t) throw new TransicionInvalida(`«${evento}» no es posible desde «${desde}»`);
	return t;
}

/** Transición entre dos estados visibles, si existe (útil cuando el estado llega ya derivado de los hechos). */
export function transicionEntre(desde: Estado, hasta: Estado): Transicion | undefined {
	return TRANSICIONES.find((x) => x.a === hasta && x.de.includes(desde));
}

/** Eventos posibles desde un estado (para habilitar acciones en la interfaz). */
export const eventosDesde = (e: Estado): Evento[] => TRANSICIONES.filter((t) => t.de.includes(e)).map((t) => t.evento);
