// Modelo del prototipo: un solo estado compartido por los cuatro actores.
// Decisiones (decisiones.md E3-2, Nico 19 oct): sin tope de visitas ni de duración; el residente decide la vigencia.
// Toda visita entra y sale mientras su Pase esté vigente (E3-6). Estadía = más de 20 h (E3-5); las franjas no la limitan (E3-4).
// Portería digita el código, el código dura lo mismo que el Pase y la administración no revoca (E3-2, confirmados el 19 oct).
import {estadoDelPase, vigenciaRestante, type Estado, type Hechos} from '../../paquetes/kino-motion/src/nucleo/pase';

export type Tipo = 'visita' | 'colaborador';
export type Modo = 'qr' | 'placa' | 'codigo';
export type Actor = 'residente' | 'visita' | 'porteria' | 'administracion';

export type EventoTraza = {
	hora: Date;
	tipo: 'creado' | 'enviado' | 'confirmado' | 'entro' | 'rechazado' | 'extendido' | 'revocado' | 'restaurado' | 'llamada';
	texto: string;
};

export type Recurrencia = {dias: number[]; inicio: number; fin: number}; // minutos desde medianoche

export type Pase = {
	id: string;
	tipo: Tipo;
	nombre: string;
	motivo?: string;
	telefono?: string;
	autor: {nombre: string; casa: string};
	modos: Modo[];
	placa?: string;
	codigo: string;
	hechos: Hechos;
	recurrencia?: Recurrencia;
	entradas: Date[];
	traza: EventoTraza[];
	nuevo?: boolean;
	compartido?: Date;
};

export type Limites = {visitaDesde: number; visitaHasta: number; colabDesde: number; colabHasta: number; avisoMin: number};

export type Lectura = {
	id: string;
	hora: Date;
	modo: Modo;
	valor: string;
	resultado: 'entra' | 'rechazado';
	motivo?: string;
	paseId?: string;
	nombre: string;
	casa?: string;
	autor?: string;
};

export type Aviso = {id: string; para: Actor; titulo: string; texto: string; tono: 'vigente' | 'rechazado' | 'neutro' | 'revocado'; paseId?: string; hora: Date};

export type Interaccion = {
	id: string;
	nombre: string;
	disparador: string;
	respuesta: string;
	regla: string;
	hik: string;
	estado: 'implementada' | 'planeada';
};

export type Sync = {comunidad: string; usuarios: [number, number]; vehiculos: [number, number]; errores: number; causa: string; estado: 'caida' | 'reparando' | 'en-linea'};

// Reloj simulado -----------------------------------------------------------------------------------------
const inicioReal = Date.now();
const base = (() => {
	const d = new Date();
	d.setHours(14, 2, 0, 0);
	return d.getTime();
})();
let velocidad = 1;
let desfase = 0; // ms simulados acumulados al cambiar de velocidad
let marcaReal = inicioReal;

export const ahora = () => new Date(base + desfase + (Date.now() - marcaReal) * velocidad);
export function cambiarVelocidad(v: number) {
	desfase += (Date.now() - marcaReal) * velocidad;
	marcaReal = Date.now();
	velocidad = v;
	emitir();
}
export const velocidadActual = () => velocidad;
export function adelantar(minutos: number) {
	desfase += minutos * 60_000;
	emitir();
}

const hoy = (h: number, m = 0, diasMas = 0) => {
	const d = new Date(base);
	d.setDate(d.getDate() + diasMas);
	d.setHours(h, m, 0, 0);
	return d;
};
const min = (h: number, m = 0) => h * 60 + m;

// Estado -------------------------------------------------------------------------------------------------
export const RESIDENTE = {nombre: 'Carolina Ruiz', casa: 'Casa 14', comunidad: 'Villas Campestres', telefono: '300 555 0199'};

const semilla = (): {pases: Pase[]; lecturas: Lectura[]} => {
	const andres: Pase = {
		id: 'p-andres', tipo: 'visita', nombre: 'Andrés Gómez', motivo: 'Almuerzo', telefono: '300 555 0142',
		autor: {nombre: RESIDENTE.nombre, casa: RESIDENTE.casa}, modos: ['qr', 'placa', 'codigo'], placa: 'KMN 305', codigo: '4817',
		hechos: {desde: hoy(14, 0), hasta: hoy(18, 0), enviadoAlLector: hoy(13, 58), confirmacion: {lector: 'Portería principal', hora: hoy(13, 59)}},
		entradas: [], compartido: hoy(13, 58),
		traza: [
			{hora: hoy(13, 58), tipo: 'creado', texto: 'Carolina creó el Pase'},
			{hora: hoy(13, 58), tipo: 'enviado', texto: 'Llegó por WhatsApp a Andrés'},
			{hora: hoy(13, 59), tipo: 'confirmado', texto: 'El lector de Portería principal lo confirmó'},
		],
	};
	const marta: Pase = {
		id: 'p-marta', tipo: 'colaborador', nombre: 'Marta Ospina', motivo: 'Aseo y cocina', telefono: '311 555 0177',
		autor: {nombre: RESIDENTE.nombre, casa: RESIDENTE.casa}, modos: ['qr', 'codigo'], codigo: '2093',
		hechos: {desde: hoy(7, 0), hasta: hoy(17, 0), enviadoAlLector: hoy(7, 0, -40), confirmacion: {lector: 'Peatonal', hora: hoy(7, 1, -40)}},
		recurrencia: {dias: [1, 2, 3, 4, 5], inicio: min(7), fin: min(17)},
		entradas: [hoy(7, 12)],
		traza: [
			{hora: hoy(7, 0, -40), tipo: 'creado', texto: 'Carolina creó el Pase · lunes a viernes'},
			{hora: hoy(7, 1, -40), tipo: 'confirmado', texto: 'El lector Peatonal lo confirmó'},
			{hora: hoy(7, 12), tipo: 'entro', texto: 'Entró por Peatonal con QR'},
		],
	};
	const tecnico: Pase = {
		id: 'p-tecnico', tipo: 'visita', nombre: 'Juan Pablo Ríos', motivo: 'Técnico de internet', telefono: '320 555 0110',
		autor: {nombre: RESIDENTE.nombre, casa: RESIDENTE.casa}, modos: ['codigo'], codigo: '6620',
		hechos: {desde: hoy(15, 30), hasta: hoy(17, 30), enviadoAlLector: hoy(11, 20), confirmacion: {lector: 'Portería principal', hora: hoy(11, 21)}},
		entradas: [],
		traza: [
			{hora: hoy(11, 20), tipo: 'creado', texto: 'Carolina creó el Pase'},
			{hora: hoy(11, 21), tipo: 'confirmado', texto: 'El lector de Portería principal lo confirmó'},
		],
	};
	const laura: Pase = {
		id: 'p-laura', tipo: 'visita', nombre: 'Laura Mejía', motivo: 'Cumpleaños', telefono: '315 555 0155',
		autor: {nombre: RESIDENTE.nombre, casa: RESIDENTE.casa}, modos: ['qr', 'placa'], placa: 'GHT 918', codigo: '7731',
		hechos: {desde: hoy(17, 0, -1), hasta: hoy(23, 0, -1), enviadoAlLector: hoy(16, 0, -1), confirmacion: {lector: 'Portería principal', hora: hoy(16, 1, -1)}},
		entradas: [],
		traza: [
			{hora: hoy(16, 0, -1), tipo: 'creado', texto: 'Carolina creó el Pase'},
			{hora: hoy(16, 1, -1), tipo: 'confirmado', texto: 'El lector de Portería principal lo confirmó'},
			{hora: hoy(23, 0, -1), tipo: 'enviado', texto: 'Venció sin usarse'},
		],
	};
	const rosa: Pase = {
		id: 'p-rosa', tipo: 'visita', nombre: 'Rosa Ruiz', motivo: 'Mamá · se queda', telefono: '310 555 0161',
		autor: {nombre: RESIDENTE.nombre, casa: RESIDENTE.casa}, modos: ['qr', 'codigo'], codigo: '5108',
		hechos: {desde: hoy(10, 0, -12), hasta: hoy(18, 0, 47), enviadoAlLector: hoy(9, 30, -12), confirmacion: {lector: 'Portería principal', hora: hoy(9, 31, -12)}},
		entradas: [hoy(11, 4, -12), hoy(9, 15)], compartido: hoy(9, 30, -12),
		traza: [
			{hora: hoy(9, 30, -12), tipo: 'creado', texto: 'Carolina creó el Pase · estadía de 2 meses'},
			{hora: hoy(9, 31, -12), tipo: 'confirmado', texto: 'El lector de Portería principal lo confirmó'},
			{hora: hoy(9, 15), tipo: 'entro', texto: 'Entró por Portería principal con QR'},
		],
	};
	return {
		pases: [andres, tecnico, rosa, marta, laura],
		lecturas: [
			{id: 'l-1', hora: hoy(7, 12), modo: 'qr', valor: 'QR', resultado: 'entra', paseId: 'p-marta', nombre: 'Marta Ospina', casa: 'Casa 14', autor: 'Carolina Ruiz'},
			{id: 'l-2', hora: hoy(9, 40), modo: 'placa', valor: 'BCD 220', resultado: 'rechazado', motivo: 'Placa sin Pase vigente', nombre: 'Vehículo sin Pase'},
		],
	};
};

export const RECIENTES: {nombre: string; tipo: Tipo; telefono: string; placa?: string; motivo?: string}[] = [
	{nombre: 'Andrés Gómez', tipo: 'visita', telefono: '300 555 0142', placa: 'KMN 305', motivo: 'Almuerzo'},
	{nombre: 'Laura Mejía', tipo: 'visita', telefono: '315 555 0155', placa: 'GHT 918', motivo: 'Cumpleaños'},
	{nombre: 'Felipe Ruiz', tipo: 'visita', telefono: '301 555 0123', motivo: 'Familia'},
	{nombre: 'Don Jairo', tipo: 'colaborador', telefono: '312 555 0188', motivo: 'Jardinería · sábados'},
];

export const INTERACCIONES: Interaccion[] = [
	{id: 'I-01', nombre: 'Código por WhatsApp', disparador: 'Escribir el número y tocar «Enviar código»', respuesta: 'Llega el código; los 6 dígitos se llenan solos y la app entra', regla: 'Teléfono obligatorio y único; se entra con el código', hik: 'Ninguno: la cuenta del residente no viaja al lector', estado: 'implementada'},
	{id: 'I-02', nombre: 'Pase vivo en la lista', disparador: 'Paso del tiempo', respuesta: 'La barra de vigencia se consume; vigente late; al final pasa a Por vencer y Vencido', regla: 'El estado sale de los hechos, nunca se escribe a mano', hik: 'Vencido = el lector deja de aceptarlo en su «Válido hasta»', estado: 'implementada'},
	{id: 'I-03', nombre: 'Volver a invitar', disparador: 'Tocar una persona reciente', respuesta: 'La hoja se abre con nombre, teléfono, placa y franja ya puestos', regla: 'Crear un Pase en 3 toques o menos', hik: 'La misma alta: persona temporal con fechas', estado: 'implementada'},
	{id: 'I-04', nombre: 'Hoja de Crear Pase con gesto', disparador: 'Arrastrar la hoja hacia abajo', respuesta: 'Sigue al dedo y se cierra con resorte; si se suelta antes, vuelve', regla: 'Nada se crea hasta tocar «Crear Pase»', hik: 'Ninguno', estado: 'implementada'},
	{id: 'I-05', nombre: 'Vigencia a tu medida', disparador: 'Elegir unas horas, todo el día o varios días', respuesta: 'Una visita de un día o una estadía de semanas o meses; la franja del conjunto se ve antes de crear', regla: 'Sin tope de visitas ni de duración: decide el residente (E3-2)', hik: 'Persona temporal con su «Válido desde / hasta»', estado: 'implementada'},
	{id: 'I-06', nombre: 'Nacimiento del Pase', disparador: 'Tocar «Crear Pase»', respuesta: 'El botón se convierte en el Pase con su arco; queda Sin confirmar con borde punteado', regla: 'Recién creado queda Sin confirmar', hik: 'Kino da de alta la persona temporal en HikCentral', estado: 'implementada'},
	{id: 'I-07', nombre: 'Espera del lector', disparador: 'El lector responde el alta', respuesta: 'El borde pasa de punteado a continuo, aparece la barra y el Pase late', regla: 'Vigente solo con la confirmación del lector', hik: 'add_person responde con el alta hecha', estado: 'implementada'},
	{id: 'I-08', nombre: 'Compartir por WhatsApp', disparador: 'Tocar «Enviar por WhatsApp»', respuesta: 'La visita recibe imagen y enlace al Pase vivo', regla: 'La visita no crea cuenta', hik: 'Ninguno: el enlace muestra el mismo Pase', estado: 'implementada'},
	{id: 'I-09', nombre: 'Pase vivo de la visita', disparador: 'Abrir el enlace', respuesta: 'Arco con QR, placa o código; cuenta regresiva; cambia solo si el residente revoca o extiende', regla: 'Tres modos conviven en el mismo Pase', hik: 'El QR es la credencial que el lector ya tiene', estado: 'implementada'},
	{id: 'I-10', nombre: 'Lectura en la entrada', disparador: 'Acercar QR, leer placa o digitar código', respuesta: 'El lector reconoce; la talanquera sube; el resultado se lee desde lejos', regla: 'Abre el lector; portería ve el porqué', hik: 'Evento de acceso de HikCentral', estado: 'implementada'},
	{id: 'I-11', nombre: 'Aviso de llegada', disparador: 'El lector deja entrar a la visita', respuesta: 'Al residente le llega «Andrés entró por Portería principal»', regla: 'Solo se avisa lo que el lector confirmó', hik: 'Suscripción a eventos de acceso', estado: 'implementada'},
	{id: 'I-12', nombre: 'Rechazo con motivo', disparador: 'Lectura de un Pase vencido, revocado o fuera de franja', respuesta: 'Pantalla roja con el motivo y «Llamar a Carolina»', regla: 'La llamada no abre la entrada', hik: 'El lector ya negó; Kino explica por qué', estado: 'implementada'},
	{id: 'I-13', nombre: 'Mantener para revocar', disparador: 'Mantener presionado 0,8 s', respuesta: 'Un anillo se llena; al soltar, el Pase queda cortado y aparece «Deshacer» por 5 s', regla: 'Revoca al instante; 5 s para deshacer', hik: 'Baja en HikCentral al vencer el deshacer', estado: 'implementada'},
	{id: 'I-14', nombre: 'Extender', disparador: 'Tocar +1 h, +1 día o +1 semana', respuesta: 'La barra crece y la nueva fecha entra con fundido', regla: 'Sin máximo: una visita se puede volver estadía', hik: 'Actualiza «Válido hasta»', estado: 'implementada'},
	{id: 'I-15', nombre: 'Franjas con vista previa', disparador: 'Mover una franja', respuesta: 'Se ve qué Pase activo quedaría por fuera; aplica a los nuevos', regla: 'La administración solo fija franjas', hik: 'Los activos conservan su «Válido hasta»', estado: 'implementada'},
	{id: 'I-16', nombre: 'Integración caída y arreglo', disparador: 'Tocar «Reintentar con teléfono»', respuesta: 'Los contadores suben mientras se sincroniza; la causa queda escrita', regla: 'El teléfono reemplaza al correo obligatorio', hik: '711 errores add_person por el campo correo', estado: 'implementada'},
	{id: 'I-17', nombre: 'Movimiento reducido', disparador: 'Ajuste del sistema', respuesta: 'Fundidos en lugar de escalas y latidos', regla: 'Política de @kino/motion', hik: 'Ninguno', estado: 'implementada'},
	{id: 'I-18', nombre: 'Pase en la billetera del teléfono', disparador: 'Tocar «Agregar a la billetera»', respuesta: 'El Pase vive en la pantalla bloqueada', regla: 'Sin app para la visita', hik: 'Mismo QR', estado: 'planeada'},
	{id: 'I-19', nombre: 'Háptica por estado', disparador: 'Confirmación, rechazo, revocar', respuesta: 'Vibración distinta para cada evento', regla: 'Nunca solo color', hik: 'Ninguno', estado: 'planeada'},
	{id: 'I-20', nombre: 'Rostro como cuarto modo', disparador: 'El colaborador se enrola una vez', respuesta: 'Entra sin sacar el teléfono', regla: 'Solo colaboradores recurrentes, con autorización', hik: 'Reconocimiento facial de HikCentral', estado: 'planeada'},
];

type Estado_ = {
	pases: Pase[];
	lecturas: Lectura[];
	avisos: Aviso[];
	limites: Limites;
	sync: Sync[];
	sesion: boolean;
	vistas: Set<string>;
	ultima?: string;
	visitaPaseId: string;
	deshacer?: {paseId: string; hasta: number};
};

const LIMITES: Limites = {visitaDesde: min(6), visitaHasta: min(22), colabDesde: min(6), colabHasta: min(19), avisoMin: 30};

function inicial(): Estado_ {
	const s = semilla();
	return {
		...s,
		avisos: [],
		limites: {...LIMITES},
		sync: [
			{comunidad: 'Villas Campestres', usuarios: [0, 0], vehiculos: [0, 0], errores: 0, causa: '', estado: 'en-linea'},
			{comunidad: 'Refugio Campestre', usuarios: [0, 312], vehiculos: [1, 44], errores: 711, causa: 'add_person rechaza el alta por el campo correo', estado: 'caida'},
		],
		sesion: false,
		vistas: new Set(),
		visitaPaseId: 'p-andres',
	};
}

export let E: Estado_ = inicial();

const oyentes = new Set<() => void>();
export const suscribir = (f: () => void) => (oyentes.add(f), () => oyentes.delete(f));
export function emitir() {
	oyentes.forEach((f) => f());
}
export function reiniciar() {
	E = inicial();
	desfase = 0;
	marcaReal = Date.now();
	velocidad = 1;
	emitir();
}

export function anotar(id: string) {
	E.ultima = id;
	E.vistas.add(id);
	emitir();
}

// Lógica del Pase ---------------------------------------------------------------------------------------
const avisoMs = () => E.limites.avisoMin * 60_000;

/** Ventana vigente de un Pase recurrente para el día de `t` (o la próxima). */
export function ventana(p: Pase, t = ahora()): {desde: Date; hasta: Date} {
	if (!p.recurrencia) return {desde: p.hechos.desde, hasta: p.hechos.hasta};
	const r = p.recurrencia;
	for (let i = 0; i < 8; i++) {
		const d = new Date(t);
		d.setDate(d.getDate() + i);
		const dia = d.getDay();
		if (!r.dias.includes(dia)) continue;
		const desde = new Date(d);
		desde.setHours(0, r.inicio, 0, 0);
		const hasta = new Date(d);
		hasta.setHours(0, r.fin, 0, 0);
		if (hasta.getTime() > t.getTime()) return {desde, hasta};
	}
	return {desde: p.hechos.desde, hasta: p.hechos.hasta};
}

export function estado(p: Pase, t = ahora()): Estado {
	const v = ventana(p, t);
	const h: Hechos = {...p.hechos, desde: v.desde, hasta: v.hasta};
	if (p.recurrencia && h.usadoEn) delete h.usadoEn;
	return estadoDelPase(h, t, avisoMs());
}

export const restante = (p: Pase, t = ahora()) => vigenciaRestante(ventana(p, t), t);

export const duraMasDeUnDia = (r: {desde: Date; hasta: Date}) => r.hasta.getTime() - r.desde.getTime() > 20 * 3_600_000;
export const esEstadia = (p: Pase) => p.tipo === 'visita' && duraMasDeUnDia(p.hechos);

export function validar(borrador: {tipo: Tipo; desde: Date; hasta: Date; recurrencia?: Recurrencia}): string | null {
	const L = E.limites;
	if (borrador.hasta.getTime() <= borrador.desde.getTime()) return 'La salida tiene que ser después de la llegada';
	if (borrador.tipo === 'visita') {
		// Una estadía entra y sale a cualquier hora: la franja solo aplica a las visitas de un día.
		if (duraMasDeUnDia(borrador)) return null;
		const dm = borrador.desde.getHours() * 60 + borrador.desde.getMinutes();
		const hm = borrador.hasta.getHours() * 60 + borrador.hasta.getMinutes();
		const mismoDia = borrador.desde.toDateString() === borrador.hasta.toDateString();
		if (dm < L.visitaDesde || (mismoDia && hm > L.visitaHasta)) return `Las visitas entran de ${horaTexto(L.visitaDesde)} a ${horaTexto(L.visitaHasta)}`;
	} else if (borrador.recurrencia) {
		if (borrador.recurrencia.inicio < L.colabDesde || borrador.recurrencia.fin > L.colabHasta)
			return `Los colaboradores entran de ${horaTexto(L.colabDesde)} a ${horaTexto(L.colabHasta)}`;
	}
	return null;
}

let contador = 0;
const id = (p: string) => `${p}-${Date.now().toString(36)}-${contador++}`;
const codigo4 = () => String(1000 + Math.floor(Math.random() * 9000));

export function crearPase(b: {tipo: Tipo; nombre: string; telefono: string; motivo?: string; placa?: string; modos: Modo[]; desde: Date; hasta: Date; recurrencia?: Recurrencia}): Pase {
	const t = ahora();
	const p: Pase = {
		id: id('p'), tipo: b.tipo, nombre: b.nombre.trim(), telefono: b.telefono, motivo: b.motivo,
		autor: {nombre: RESIDENTE.nombre, casa: RESIDENTE.casa},
		modos: b.modos, placa: b.placa?.toUpperCase() || undefined, codigo: codigo4(),
		hechos: {desde: b.desde, hasta: b.hasta, enviadoAlLector: t},
		recurrencia: b.recurrencia, entradas: [], nuevo: true,
		traza: [
			{hora: t, tipo: 'creado', texto: 'Carolina creó el Pase'},
			{hora: t, tipo: 'enviado', texto: 'Kino lo envió al lector de Portería principal'},
		],
	};
	E.pases.unshift(p);
	E.visitaPaseId = p.id;
	emitir();
	// El lector confirma el alta un momento después (tiempo real, no simulado: es la red).
	setTimeout(() => {
		if (p.hechos.revocacion) return;
		const c = ahora();
		p.hechos.confirmacion = {lector: 'Portería principal', hora: c};
		p.traza.push({hora: c, tipo: 'confirmado', texto: 'El lector de Portería principal lo confirmó'});
		anotar('I-07');
	}, 2600);
	return p;
}

export function compartir(p: Pase) {
	p.compartido = ahora();
	p.traza.push({hora: p.compartido, tipo: 'enviado', texto: `Llegó por WhatsApp a ${p.nombre.split(' ')[0]}`});
	E.visitaPaseId = p.id;
	anotar('I-08');
}

export function revocar(p: Pase) {
	const t = ahora();
	p.hechos.revocacion = {nombre: RESIDENTE.nombre, hora: t};
	p.traza.push({hora: t, tipo: 'revocado', texto: 'Carolina revocó el Pase'});
	E.deshacer = {paseId: p.id, hasta: Date.now() + 5000};
	E.avisos.push({id: id('a'), para: 'visita', titulo: 'Tu Pase ya no está activo', texto: `${RESIDENTE.nombre} revocó el Pase`, tono: 'revocado', paseId: p.id, hora: t});
	anotar('I-13');
}

export function deshacerRevocar() {
	const d = E.deshacer;
	if (!d) return;
	const p = E.pases.find((x) => x.id === d.paseId);
	if (p) {
		delete p.hechos.revocacion;
		p.traza.push({hora: ahora(), tipo: 'restaurado', texto: 'Carolina deshizo la revocación'});
	}
	E.deshacer = undefined;
	emitir();
}

export function extender(p: Pase, horas: number): string | null {
	const base_ = Math.max(p.hechos.hasta.getTime(), ahora().getTime());
	const nueva = new Date(base_ + horas * 3_600_000);
	p.hechos.hasta = nueva;
	p.traza.push({hora: ahora(), tipo: 'extendido', texto: `Carolina lo extendió hasta ${fechaHora(nueva)}`});
	anotar('I-14');
	return null;
}

/** Lo que pasa en la entrada cuando alguien llega. */
export function leer(modo: Modo, valor: string): Lectura {
	const t = ahora();
	const limpio = valor.replace(/\s+/g, '').toUpperCase();
	const p = E.pases.find((x) =>
		modo === 'qr' ? x.id === valor : modo === 'placa' ? x.placa?.replace(/\s+/g, '') === limpio : x.codigo === limpio,
	);
	let l: Lectura;
	if (!p) {
		l = {id: id('l'), hora: t, modo, valor, resultado: 'rechazado', motivo: modo === 'codigo' ? 'Ese código no existe' : 'Sin Pase en Kino', nombre: modo === 'placa' ? valor : 'Sin identificar'};
	} else {
		const st = estado(p, t);
		const v = ventana(p, t);
		const base_ = {id: id('l'), hora: t, modo, valor, paseId: p.id, nombre: p.nombre, casa: p.autor.casa, autor: p.autor.nombre};
		if (!p.modos.includes(modo)) l = {...base_, resultado: 'rechazado', motivo: `Este Pase no entra con ${MODO_TEXTO[modo]}`};
		else if (st === 'vigente' || st === 'por-vencer') l = {...base_, resultado: 'entra'};
		else if (st === 'revocado') l = {...base_, resultado: 'rechazado', motivo: `Revocado por ${p.hechos.revocacion!.nombre} a las ${horaCorta(p.hechos.revocacion!.hora)}`};
		else if (st === 'vencido') l = {...base_, resultado: 'rechazado', motivo: `Venció a las ${horaCorta(v.hasta)}`};
		else if (st === 'sin-confirmar') l = {...base_, resultado: 'rechazado', motivo: 'El lector todavía no recibe este Pase'};
		else l = {...base_, resultado: 'rechazado', motivo: p.recurrencia ? `Fuera de su franja: entra desde ${fechaHora(v.desde)}` : `Empieza a las ${horaCorta(v.desde)}`};

		if (l.resultado === 'entra') {
			p.entradas.push(t);
			p.traza.push({hora: t, tipo: 'entro', texto: `Entró por Portería principal con ${MODO_TEXTO[modo]}`});
			E.avisos.push({id: id('a'), para: 'residente', titulo: `${p.nombre.split(' ')[0]} entró`, texto: `Portería principal · ${MODO_TEXTO[modo]} · ${horaCorta(t)}`, tono: 'vigente', paseId: p.id, hora: t});
		} else {
			p.traza.push({hora: t, tipo: 'rechazado', texto: `Rechazado en Portería principal: ${l.motivo}`});
			E.avisos.push({id: id('a'), para: 'residente', titulo: `${p.nombre.split(' ')[0]} no pudo entrar`, texto: l.motivo!, tono: 'rechazado', paseId: p.id, hora: t});
		}
	}
	E.lecturas.unshift(l);
	anotar(l.resultado === 'entra' ? 'I-10' : 'I-12');
	return l;
}

export function llamar(p: Pase) {
	p.traza.push({hora: ahora(), tipo: 'llamada', texto: 'Portería llamó a Carolina. La llamada no abre la entrada'});
	anotar('I-12');
}

export function repararSync(comunidad: string) {
	const s = E.sync.find((x) => x.comunidad === comunidad);
	if (!s || s.estado !== 'caida') return;
	s.estado = 'reparando';
	anotar('I-16');
	const paso = () => {
		if (s.usuarios[0] < s.usuarios[1]) s.usuarios[0] = Math.min(s.usuarios[1], s.usuarios[0] + 13);
		if (s.vehiculos[0] < s.vehiculos[1] && Math.random() < 0.5) s.vehiculos[0]++;
		s.errores = Math.max(0, s.errores - 30);
		if (s.usuarios[0] >= s.usuarios[1]) {
			s.vehiculos[0] = s.vehiculos[1];
			s.errores = 0;
			s.estado = 'en-linea';
			s.causa = 'Alta con teléfono en lugar de correo · simulación';
			emitir();
			return;
		}
		emitir();
		setTimeout(paso, 90);
	};
	setTimeout(paso, 300);
}

/** Enlace corto y estable del Pase vivo (no es la credencial). */
export const corto = (p: Pase) => {
	let h = 0;
	for (const c of p.id) h = (h * 31 + c.charCodeAt(0)) >>> 0;
	return h.toString(36).slice(0, 4).padStart(4, '7');
};

// Texto --------------------------------------------------------------------------------------------------
export const MODO_TEXTO: Record<Modo, string> = {qr: 'QR', placa: 'placa', codigo: 'código'};
export const ESTADO_TEXTO: Record<Estado, string> = {
	previsto: 'Previsto', 'sin-confirmar': 'Sin confirmar', vigente: 'Vigente', 'por-vencer': 'Por vencer', vencido: 'Vencido', usado: 'Usado', revocado: 'Revocado',
};
export function horaTexto(minutos: number) {
	const h = Math.floor(minutos / 60);
	const m = minutos % 60;
	const d = new Date(base);
	d.setHours(h, m, 0, 0);
	return horaCorta(d);
}
export function horaCorta(d: Date) {
	let h = d.getHours();
	const m = d.getMinutes();
	const pm = h >= 12;
	h = h % 12 || 12;
	return `${h}:${String(m).padStart(2, '0')} ${pm ? 'p. m.' : 'a. m.'}`;
}
export function hora24(d: Date) {
	return `${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`;
}
const DIAS = ['dom', 'lun', 'mar', 'mié', 'jue', 'vie', 'sáb'];
export const diasTexto = (dias: number[]) => {
	const k = [...dias].sort().join();
	if (k === '1,2,3,4,5') return 'Lun a vie';
	if (k === '1,2,3,4,5,6') return 'Lun a sáb';
	if (k === '0,1,2,3,4,5,6') return 'Todos los días';
	return dias.map((d) => DIAS[d]).join(', ');
};
const MESES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'];
/** «hoy», «mañana», «jue» dentro de la semana; «12 nov» más lejos. */
export function fechaCorta(d: Date, t = ahora()) {
	const dias = Math.round((new Date(d).setHours(0, 0, 0, 0) - new Date(t).setHours(0, 0, 0, 0)) / 86_400_000);
	if (dias === 0) return 'hoy';
	if (dias === 1) return 'mañana';
	if (dias === -1) return 'ayer';
	if (dias > 1 && dias < 7) return DIAS[d.getDay()];
	return `${d.getDate()} ${MESES[d.getMonth()]}`;
}
/** 7 a. m., 5:30 p. m. */
export function horaBreve(d: Date) {
	return horaCorta(d).replace(':00 ', ' ');
}
export function duracionTexto(desde: Date, hasta: Date) {
	const h = (hasta.getTime() - desde.getTime()) / 3_600_000;
	if (h < 20) return `${Math.round(h)} h`;
	const d = Math.round(h / 24);
	if (d < 14) return `${d} días`;
	if (d < 60) return `${Math.round(d / 7)} semanas`;
	return `${Math.round(d / 30)} meses`;
}
export function fechaHora(d: Date) {
	const t = ahora();
	const mismo = d.toDateString() === t.toDateString();
	const man = new Date(t);
	man.setDate(man.getDate() + 1);
	return `${fechaCorta(d, t)} ${horaCorta(d)}`;
}
/** «3:30 a 5:30 p. m.» cuando las dos horas caen en la misma mitad del día; si no, cada una con la suya. */
export function franjaTexto(desde: Date, hasta: Date) {
	const a = horaBreve(desde);
	const b = horaBreve(hasta);
	const sufijo = / [ap]\. m\.$/;
	return a.match(sufijo)?.[0] === b.match(sufijo)?.[0] ? `${a.replace(sufijo, '')} a ${b}` : `${a} a ${b}`;
}
export function vigenciaTexto(p: Pase, t = ahora()) {
	const v = ventana(p, t);
	if (p.recurrencia) return `${diasTexto(p.recurrencia.dias)} · ${franjaTexto(v.desde, v.hasta)}`;
	if (esEstadia(p)) return `Hasta el ${fechaCorta(v.hasta, t)} · ${duracionTexto(v.desde, v.hasta)}`;
	const dia = fechaCorta(v.desde, t);
	return `${dia[0].toUpperCase()}${dia.slice(1)} · ${franjaTexto(v.desde, v.hasta)}`;
}
export function cuentaRegresiva(hasta: Date, t = ahora()) {
	const ms = hasta.getTime() - t.getTime();
	if (ms <= 0) return '0:00:00';
	if (ms > 86_400_000) {
		const d = Math.floor(ms / 86_400_000);
		return `${d} ${d === 1 ? 'día' : 'días'} ${Math.floor((ms % 86_400_000) / 3_600_000)} h`;
	}
	const s = Math.floor(ms / 1000);
	return `${Math.floor(s / 3600)}:${String(Math.floor((s % 3600) / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`;
}
export {hoy, min};
