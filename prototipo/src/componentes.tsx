// Piezas compartidas: marca, íconos, Pase (tarjeta y Portal), QR, botón de mantener, dispositivos, micelio e ilustraciones.
import {useEffect, useLayoutEffect, useRef, useState} from 'preact/hooks';
import type {ComponentChildren, JSX} from 'preact';
import qrcode from 'qrcode-generator';
import type {Estado} from '../../paquetes/kino-motion/src/nucleo/pase';
import {ahora, brillo, E, esEstadia, ESTADO_TEXTO, estado, hora24, restante, suscribir, vigenciaTexto, type Pase} from './modelo';
import {animar, C, D, reducido, resorte, vibrar} from './movimiento';

// Estado vivo -------------------------------------------------------------------------------------------
export function useKino(intervalo = 1000) {
	const [, set] = useState(0);
	useEffect(() => {
		const off = suscribir(() => set((n) => n + 1));
		const t = setInterval(() => set((n) => n + 1), intervalo);
		return () => {
			off();
			clearInterval(t);
		};
	}, [intervalo]);
	return E;
}

export function useAnterior<T>(v: T) {
	const r = useRef<T>(v);
	const antes = r.current;
	useEffect(() => {
		r.current = v;
	});
	return antes;
}

// Marca ------------------------------------------------------------------------------------------------
export const Marca = ({tam = 28}: {tam?: number}) => (
	<svg viewBox="0 0 100 101.824" width={tam} height={tam * 1.018} aria-hidden="true" class="marca">
		<path fill="var(--kino-marca-bloque)" fill-rule="evenodd" d="M 3.483 0 H 96.517 A 3.483 3.483 0 0 1 100 3.483 V 101.824 H 0 V 3.483 A 3.483 3.483 0 0 1 3.483 0 Z M 18.242 86.567 V 46.766 A 31.675 31.675 0 0 1 81.592 46.766 V 86.567 Z" />
		<path fill="var(--kino-marca-gota)" d="M 50 35.987 A 16.169 17.579 0 0 1 66.169 53.566 L 50 66.667 L 33.831 53.566 A 16.169 17.579 0 0 1 50 35.987 Z" />
	</svg>
);

const P: Record<string, string> = {
	atras: 'M15 5l-7 7 7 7',
	mas: 'M12 5v14M5 12h14',
	x: 'M6 6l12 12M18 6L6 18',
	qr: 'M4 4h6v6H4zM14 4h6v6h-6zM4 14h6v6H4zM14 14h2v2h-2zM18 14h2v2h-2zM14 18h2v2h-2zM18 18h2v2h-2z',
	placa: 'M3 8h18v8H3zM7 12h4M14 12h3',
	codigo: 'M4 7h16v10H4zM8 12h.01M12 12h.01M16 12h.01',
	reloj: 'M12 7v5l3 2M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0z',
	telefono: 'M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2',
	aviso: 'M6 16V11a6 6 0 1 1 12 0v5l2 2H4zM10 20a2 2 0 0 0 4 0',
	casa: 'M4 11l8-7 8 7v9H4zM10 20v-5h4v5',
	pases: 'M5 4h14v16H5zM5 9a3 3 0 0 1 0 6M19 9a3 3 0 0 0 0 6',
	compartir: 'M12 4v11M7 9l5-5 5 5M5 14v6h14v-6',
	check: 'M5 12l5 5 9-10',
	alerta: 'M12 8v5M12 16.5v.01M10.3 3.9L2.6 17.5A2 2 0 0 0 4.3 20.5h15.4a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z',
	deshacer: 'M9 14L4 9l5-5M4 9h10a6 6 0 0 1 0 12h-3',
	ajustes: 'M4 6h10M18 6h2M4 12h4M12 12h8M4 18h12M20 18h0M14 4v4M8 10v4M16 16v4',
	persona: 'M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM4 21a8 8 0 0 1 16 0',
	lector: 'M7 3h10v18H7zM10 7h4M12 17h.01',
	resumen: 'M4 20V10M10 20V4M16 20v-7M22 20H2',
	enlace: 'M10 14a4 4 0 0 0 5.66 0l3-3a4 4 0 0 0-5.66-5.66l-1 1M14 10a4 4 0 0 0-5.66 0l-3 3a4 4 0 0 0 5.66 5.66l1-1',
	sincronizar: 'M20 11a8 8 0 0 0-14-5l-2 2M4 4v4h4M4 13a8 8 0 0 0 14 5l2-2M20 20v-4h-4',
};
export const Icono = ({n, tam = 22, ...r}: {n: keyof typeof P; tam?: number} & JSX.SVGAttributes<SVGSVGElement>) => (
	<svg viewBox="0 0 24 24" width={tam} height={tam} fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" {...r}>
		<path d={P[n]} />
	</svg>
);

// Estado -----------------------------------------------------------------------------------------------
export const ChipEstado = ({e, grande}: {e: Estado | 'rechazado'; grande?: boolean}) => (
	<span class={`chip chip--${e} ${grande ? 'chip--grande' : ''}`}>
		<span class="chip__punto" aria-hidden="true" />
		{e === 'rechazado' ? 'Rechazado' : ESTADO_TEXTO[e]}
	</span>
);

/** Barra de vida: en biopunk es una vena con flujo. */
export const Vida = ({p, e}: {p: Pase; e: Estado}) => {
	const f = e === 'vigente' || e === 'por-vencer' ? restante(p) : e === 'previsto' || e === 'sin-confirmar' ? 1 : 0;
	return (
		<div class={`vida vida--${e}`} role="meter" aria-valuemin={0} aria-valuemax={100} aria-valuenow={Math.round(f * 100)} aria-label="Vigencia que queda">
			<span class="vida__fluido" style={{transform: `scaleX(${f})`}} />
		</div>
	);
};

export const Iniciales = ({nombre, tono}: {nombre: string; tono?: string}) => (
	<span class={`iniciales ${tono ?? ''}`} aria-hidden="true">
		{nombre.split(' ').map((x) => x[0]).slice(0, 2).join('')}
	</span>
);

// Tarjeta del Pase en la lista -------------------------------------------------------------------------
export function TarjetaPase({p, onAbrir, retraso = 0}: {p: Pase; onAbrir: (p: Pase, el: HTMLElement) => void; retraso?: number}) {
	const e = estado(p);
	const antes = useAnterior(e);
	const ref = useRef<HTMLButtonElement>(null);
	useLayoutEffect(() => {
		if (!ref.current) return;
		animar(ref.current, [{opacity: 0, transform: 'translateY(14px) scale(.98)'}, {opacity: 1, transform: 'none'}], {duration: D.tarjeta, easing: C.crecer, delay: retraso, fill: 'backwards'});
	}, []);
	useEffect(() => {
		if (antes === e || !ref.current) return;
		transicion(ref.current, antes, e);
	}, [e]);
	return (
		<button ref={ref} class={`tarjeta tarjeta--${e} ${p.nuevo ? 'tarjeta--nueva' : ''}`} data-estado={e} style={{'--brillo': brillo(p, e)}} onClick={() => onAbrir(p, ref.current!)} aria-label={`${p.nombre}, ${ESTADO_TEXTO[e]}`}>
			<span class="membrana" aria-hidden="true" />
			<span class="tarjeta__cabeza">
				<span class="rotulo">{p.tipo === 'colaborador' ? 'Colaborador' : esEstadia(p) ? 'Estadía' : 'Visita'}</span>
				<ChipEstado e={e} />
			</span>
			<span class="tarjeta__nombre">
				{p.nombre}
				<span class="tachado" aria-hidden="true" />
			</span>
			{p.motivo && <span class="tarjeta__motivo">{p.motivo}</span>}
			<span class={`tarjeta__vigencia dato dato--${e}`}>{lineaVigencia(p, e)}</span>
			<Vida p={p} e={e} />
			<span class="corte" aria-hidden="true" />
		</button>
	);
}

export function lineaVigencia(p: Pase, e: Estado) {
	if (e === 'usado' && p.hechos.usadoEn) return `Entró a las ${hora24(p.hechos.usadoEn)}`;
	if (e === 'revocado') return `Revocado a las ${hora24(p.hechos.revocacion!.hora)}`;
	if (e === 'sin-confirmar') return 'Esperando al lector…';
	return vigenciaTexto(p);
}

/** Interpreta la partitura de cada evento del Pase (núcleo/pase.ts) sobre una tarjeta o un Portal. */
export function transicion(el: HTMLElement, de: Estado, a: Estado) {
	const op = {fill: 'none' as const};
	if (a === 'vigente' && de === 'sin-confirmar') {
		// Quorum: la señal se acumuló sin efecto visible y la luz se enciende de golpe (destello de 120 ms: sube un tercio, cae el resto).
		animar(el.querySelector('.portal__arco') ?? el, [{filter: 'brightness(1)'}, {filter: 'brightness(1.7)', offset: 0.36}, {filter: 'brightness(1)'}], {duration: D.instante, easing: 'linear', ...op});
		// Tres latidos con sístole corta (un tercio del ciclo) y después brillo quieto, como los hongos luminiscentes.
		animar(el.querySelector('.chip__punto'), [{transform: 'scale(1)'}, {transform: 'scale(1.7)', offset: 0.12}, {transform: 'scale(1)', offset: 0.33}, {transform: 'scale(1)'}], {duration: D.latir, iterations: 3, easing: C.latir});
		animar(el.querySelector('.vida'), [{opacity: 0, transform: 'scaleX(.4)'}, {opacity: 1, transform: 'none'}], {duration: D.tarjeta, easing: C.crecer});
		// La nota de lo que pasó sube (partitura: confirmar).
		animar(el.querySelector('.tarjeta__vigencia'), [{opacity: 0, transform: 'translateY(8px)'}, {opacity: 1, transform: 'none'}], {duration: D.crecer, easing: C.crecer});
		vibrar(20);
	} else if (a === 'revocado') {
		animar(el.querySelector('.corte'), [{transform: 'scaleX(0)'}, {transform: 'scaleX(1)'}], {duration: D.corto, easing: C.revocar, fill: 'forwards'});
		vibrar([12, 40, 12]);
	} else if (a === 'usado') {
		animar(el.querySelector('.tachado'), [{transform: 'scaleX(0)'}, {transform: 'scaleX(1)'}], {duration: D.corto, easing: C.crecer, fill: 'forwards'});
	} else if (a === 'vencido') {
		animar(el.querySelector('.portal__arco') ?? el, [{filter: 'saturate(1)', opacity: 1}, {filter: 'saturate(.35)', opacity: 0.72}], {duration: D.decaer, easing: C.decaer});
	} else if (a === 'por-vencer') {
		animar(el.querySelector('.chip'), [{transform: 'scale(1.12)'}, {transform: 'none'}], {duration: D.crecer, easing: C.crecer});
	}
}

// QR y Portal ------------------------------------------------------------------------------------------
export function QR({texto, tam = 220}: {texto: string; tam?: number}) {
	const q = qrcode(0, 'M');
	q.addData(texto);
	q.make();
	const n = q.getModuleCount();
	let d = '';
	for (let r = 0; r < n; r++) for (let c = 0; c < n; c++) if (q.isDark(r, c)) d += `M${c} ${r}h1v1h-1z`;
	return (
		<svg class="qr" viewBox={`-1 -1 ${n + 2} ${n + 2}`} width={tam} height={tam} shape-rendering="crispEdges" role="img" aria-label="Código QR del Pase">
			<path d={d} fill="currentColor" />
		</svg>
	);
}

export type ModoVista = 'qr' | 'placa' | 'codigo';

/** El Portal: el arco del logo con el QR adentro. Solo lo que es un Pase lleva arco (X8). */
export function Portal({p, modo = 'qr', claro, tam = 260}: {p: Pase; modo?: ModoVista; claro?: boolean; tam?: number}) {
	const e = estado(p);
	const antes = useAnterior(e);
	const ref = useRef<HTMLDivElement>(null);
	useEffect(() => {
		if (antes !== e && ref.current) transicion(ref.current, antes, e);
	}, [e]);
	const muerto = e === 'vencido' || e === 'revocado' || e === 'usado';
	return (
		<div ref={ref} class={`portal portal--${e} ${claro ? 'portal--claro' : ''}`} data-estado={e} style={{'--tam': `${tam}px`, '--brillo': brillo(p, e)}}>
			<span class="portal__halo" aria-hidden="true" />
			<div class="portal__arco">
				{modo === 'qr' && <QR texto={`https://kino.co/p/${p.id}`} tam={tam * 0.62} />}
				{modo === 'placa' && (
					<div class="portal__dato">
						<span class="rotulo">Placa</span>
						<span class="portal__grande">{p.placa ?? '—'}</span>
					</div>
				)}
				{modo === 'codigo' && (
					<div class="portal__dato">
						<span class="rotulo">Código</span>
						<span class="portal__grande">{p.codigo.split('').join(' ')}</span>
					</div>
				)}
				{muerto && <span class="portal__velo">{ESTADO_TEXTO[e]}</span>}
				<span class="corte" aria-hidden="true" />
			</div>
		</div>
	);
}

// Mantener presionado ----------------------------------------------------------------------------------
export function BotonMantener({onCompleto, children, ms = 800, clase = ''}: {onCompleto: () => void; children: ComponentChildren; ms?: number; clase?: string}) {
	const [carga, setCarga] = useState(false);
	const t = useRef<number>();
	const empezar = (ev: PointerEvent) => {
		(ev.currentTarget as HTMLElement).setPointerCapture?.(ev.pointerId);
		setCarga(true);
		vibrar(8);
		t.current = window.setTimeout(() => {
			setCarga(false);
			onCompleto();
		}, ms);
	};
	const soltar = () => {
		clearTimeout(t.current);
		setCarga(false);
	};
	return (
		<button
			class={`mantener ${carga ? 'mantener--cargando' : ''} ${clase}`}
			style={{'--ms': `${ms}ms`}}
			onPointerDown={empezar}
			onPointerUp={soltar}
			onPointerCancel={soltar}
			onPointerLeave={soltar}
			onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && (e.preventDefault(), onCompleto())}
		>
			<span class="mantener__relleno" aria-hidden="true" />
			<span class="mantener__texto">{children}</span>
		</button>
	);
}

// Dispositivos y escala --------------------------------------------------------------------------------
export function Escala({ancho, alto, children, max = 1}: {ancho: number; alto: number; children: ComponentChildren; max?: number}) {
	const ref = useRef<HTMLDivElement>(null);
	const [s, setS] = useState(1);
	useLayoutEffect(() => {
		const el = ref.current!;
		const medir = () => {
			const r = el.getBoundingClientRect();
			setS(Math.min(max, r.width / ancho, r.height / alto));
		};
		medir();
		const ro = new ResizeObserver(medir);
		ro.observe(el);
		return () => ro.disconnect();
	}, [ancho, alto]);
	return (
		<div ref={ref} class="escala">
			<div class="escala__caja" style={{width: ancho * s, height: alto * s}}>
				<div style={{width: ancho, height: alto, transform: `scale(${s})`, transformOrigin: '0 0'}}>{children}</div>
			</div>
		</div>
	);
}

export const Telefono = ({children, claro, etiqueta}: {children: ComponentChildren; claro?: boolean; etiqueta: string}) => {
	useKino(15000);
	return (
		<div class={`telefono ${claro ? 'telefono--claro' : ''}`} data-tema={claro ? 'claro' : 'oscuro'} role="region" aria-label={etiqueta}>
			<div class="telefono__barra">
				<span class="mono">{hora24(ahora())}</span>
				<span class="telefono__isla" aria-hidden="true" />
				<span class="telefono__senal" aria-hidden="true">
					<i />
					<i />
					<i />
				</span>
			</div>
			<div class="telefono__pantalla">{children}</div>
		</div>
	);
};

// Micelio: textura de fondo de la dirección biopunk. Se dibuja una vez: nada se mueve si no cambia un dato.
export function Micelio({densidad = 46, clase = ''}: {densidad?: number; clase?: string}) {
	const ref = useRef<HTMLCanvasElement>(null);
	useEffect(() => {
		const cv = ref.current!;
		const ctx = cv.getContext('2d')!;
		const dpr = Math.min(2, devicePixelRatio || 1);
		// Semilla fija: el mismo dibujo en cada visita.
		let s = 7;
		const azar = () => ((s = (s * 16807) % 2147483647) / 2147483647);
		const nodos = Array.from({length: densidad}, () => ({x: azar(), y: azar(), r: 0.6 + azar() * 1.8}));
		const verde = getComputedStyle(document.documentElement).getPropertyValue('--bio-filamento').trim() || '#00BB83';
		const dibujar = () => {
			const r = cv.getBoundingClientRect();
			const w = r.width;
			const h = r.height;
			cv.width = w * dpr;
			cv.height = h * dpr;
			ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
			ctx.clearRect(0, 0, w, h);
			const lim = Math.min(w, h) * 0.28;
			ctx.lineWidth = 0.8;
			ctx.strokeStyle = verde;
			ctx.fillStyle = verde;
			for (let i = 0; i < nodos.length; i++)
				for (let j = i + 1; j < nodos.length; j++) {
					const a = nodos[i];
					const b = nodos[j];
					const dist = Math.hypot((a.x - b.x) * w, (a.y - b.y) * h);
					if (dist > lim) continue;
					ctx.globalAlpha = (1 - dist / lim) * 0.32;
					ctx.beginPath();
					ctx.moveTo(a.x * w, a.y * h);
					ctx.quadraticCurveTo((a.x + b.x) * w / 2 + Math.sin(i) * 6, (a.y + b.y) * h / 2 + Math.cos(j) * 6, b.x * w, b.y * h);
					ctx.stroke();
				}
			for (const n of nodos) {
				ctx.globalAlpha = 0.55;
				ctx.beginPath();
				ctx.arc(n.x * w, n.y * h, n.r + 0.6, 0, 6.283);
				ctx.fill();
			}
			ctx.globalAlpha = 1;
		};
		dibujar();
		const ro = new ResizeObserver(dibujar);
		ro.observe(cv);
		return () => ro.disconnect();
	}, []);
	return <canvas ref={ref} class={`micelio ${clase}`} aria-hidden="true" />;
}

// Ilustraciones ----------------------------------------------------------------------------------------
// Una sola familia, hecha con la geometría del logo: el arco y la gota. Trazo de 1,7 con puntas redondas (X6),
// dos colores apagados, sin sombras ni personas. El arco aparece solo cuando la ilustración muestra un Pase (X8).
const GOTA = 'M0 -15.6A16.2 17.6 0 0 1 16.2 2L0 15.1L-16.2 2A16.2 17.6 0 0 1 0 -15.6Z';
const ARCO = 'M44 112V58a36 36 0 0 1 72 0v54';
export type TipoIlustracion = 'membrana' | 'pase-vacio' | 'llegada';
export function Ilustracion({tipo, titulo}: {tipo: TipoIlustracion; titulo?: string}) {
	return (
		<svg class={`ilustracion ilustracion--${tipo}`} viewBox="0 0 160 124" role={titulo ? 'img' : undefined} aria-label={titulo} aria-hidden={titulo ? undefined : 'true'}>
			{tipo === 'membrana' && (
				<>
					{/* Kino es una membrana: un borde vivo con una abertura por donde pasa quien tiene Pase. */}
					<path class="ilustracion__trazo" d="M118 34C104 16 74 12 52 22 28 33 18 58 26 82c8 24 34 36 60 32 18-3 30-12 36-24" />
					<path class="ilustracion__trazo ilustracion__trazo--tenue" d="M108 44C97 31 76 28 60 35 43 43 37 60 42 77c6 17 24 26 42 23 12-2 21-8 26-17" />
					<g transform="translate(130 60) scale(.62)"><path class="ilustracion__gota" d={GOTA} /></g>
				</>
			)}
			{tipo === 'pase-vacio' && (
				<>
					{/* El Pase que todavía no existe: el arco con el borde punteado de Sin confirmar. */}
					<path class="ilustracion__trazo ilustracion__trazo--punteado" d={ARCO} />
					<path class="ilustracion__trazo ilustracion__trazo--tenue" d="M34 112h92" />
					<g transform="translate(80 84) scale(.5)"><path class="ilustracion__gota ilustracion__gota--tenue" d={GOTA} /></g>
				</>
			)}
			{tipo === 'llegada' && (
				<>
					{/* Alguien llega con su Pase: el rastro punteado termina en el umbral del arco. */}
					<path class="ilustracion__trazo" d={ARCO} />
					<path class="ilustracion__trazo ilustracion__trazo--tenue" d="M18 112h124" />
					<path class="ilustracion__trazo ilustracion__trazo--punteado" d="M80 124v-12" />
					<g transform="translate(80 98) scale(.5)"><path class="ilustracion__gota" d={GOTA} /></g>
				</>
			)}
		</svg>
	);
}

export const usarResorte = resorte;
