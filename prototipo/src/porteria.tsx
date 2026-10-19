// Portería: el lector decide y portería ve el porqué. Se lee desde 3 m.
// Coreografía de la lectura (entrega-3/motion-e-ilustracion.md): la escena 3D aprobada de la portería de noche
// es el fondo del panel. Leyendo, la cámara llega; el veredicto aparece en el mismo cuadro en que la luz del lector
// se enciende; si entra, la talanquera sube en el video y tres anillos convergen sobre la luz; si no entra, la escena
// se congela con la luz en rojo y el panel se contrae. Con movimiento reducido: pósters fijos y fundidos.
import {useEffect, useLayoutEffect, useRef, useState} from 'preact/hooks';
import {ahora, E, estado, hora24, leer, llamar, vigenciaTexto, type Lectura, type Modo} from './modelo';
import {ChipEstado, Icono, Marca, useKino} from './componentes';
import {animar, C, D, R, reducido, vibrar} from './movimiento';

type Llegada = {etiqueta: string; modo: Modo; valor: string; quien: string};
const MODO: Record<Modo, string> = {qr: 'QR', placa: 'placa', codigo: 'código'};
const ABIERTA_MS = 4000;

export function Porteria() {
	const est = useKino(1000);
	const [ultima, setUltima] = useState<Lectura | null>(null);
	const [leyendo, setLeyendo] = useState<Llegada | null>(null);
	const [pulso, setPulso] = useState(0);
	const [llamada, setLlamada] = useState<'no' | 'llamando' | 'contesto'>('no');
	const [teclado, setTeclado] = useState<'' | 'codigo' | 'placa'>('');
	const [entrada, setEntrada] = useState('');

	const hoy = ahora().toDateString();
	const esperados = est.pases.filter((p) => ['vigente', 'por-vencer', 'previsto', 'sin-confirmar'].includes(estado(p)) || p.entradas.some((x) => x.toDateString() === hoy));
	const vencidos = est.pases.filter((p) => ['vencido', 'revocado'].includes(estado(p)));
	const llegadas: Llegada[] = [
		...esperados.flatMap((p) => p.modos.map((m) => ({etiqueta: m === 'qr' ? 'QR' : m === 'placa' ? p.placa! : `Código ${p.codigo}`, modo: m, valor: m === 'qr' ? p.id : m === 'placa' ? p.placa! : p.codigo, quien: p.nombre}))),
		...vencidos.slice(0, 2).map((p) => ({etiqueta: 'QR', modo: 'qr' as Modo, valor: p.id, quien: p.nombre})),
		{etiqueta: 'XYZ 999', modo: 'placa', valor: 'XYZ 999', quien: 'Carro sin Pase'},
	];

	const simular = (l: Llegada) => {
		setLeyendo(l);
		setUltima(null);
		setLlamada('no');
		setTimeout(() => {
			const r = leer(l.modo, l.valor);
			setLeyendo(null);
			setUltima(r);
			setPulso((n) => n + 1);
			vibrar(r.resultado === 'entra' ? 30 : [30, 80, 30]);
		}, 1100);
	};

	useEffect(() => {
		if (llamada !== 'llamando') return;
		const t = setTimeout(() => setLlamada('contesto'), 2600);
		return () => clearTimeout(t);
	}, [llamada]);

	const enviarTeclado = () => {
		if (!entrada.trim() || !teclado) return;
		simular({etiqueta: entrada, modo: teclado, valor: entrada, quien: teclado === 'codigo' ? 'Código digitado' : 'Placa digitada'});
		setEntrada('');
		setTeclado('');
	};

	const estadoPanel = leyendo ? 'leyendo' : ultima ? ultima.resultado : 'reposo';

	return (
		<div class="app app--porteria">
			<header class="porteria__cabeza">
				<Marca tam={30} />
				<b>Kino Portería</b>
				<span class="tenue">Villas Campestres · Portería principal</span>
				<span class="mono porteria__hora">{hora24(ahora())}</span>
			</header>
			<div class="porteria__cuerpo">
				<div class="porteria__principal">
					<Panel estado={estadoPanel} leyendo={leyendo} ultima={ultima} pulso={pulso} llamada={llamada} onLlamar={(id) => (setLlamada('llamando'), llamar(E.pases.find((p) => p.id === id)!))} />
					<section class="bitacora">
						<h2 class="rotulo">Hoy en la entrada</h2>
						<div class="bitacora__tabla">
							<table class="tabla">
								<colgroup>
									<col style={{width: '11%'}} />
									<col style={{width: '22%'}} />
									<col style={{width: '13%'}} />
									<col style={{width: '17%'}} />
									<col />
								</colgroup>
								<thead>
									<tr><th>Hora</th><th>Quién</th><th>Con</th><th>Resultado</th><th>Motivo · otorgó</th></tr>
								</thead>
								<tbody>
									{est.lecturas.slice(0, 3).map((l) => (
										<tr class={l.id === ultima?.id ? 'nueva' : ''}>
											<td class="mono">{hora24(l.hora)}</td>
											<td>{l.nombre}</td>
											<td class="mono">{l.modo === 'qr' ? 'QR' : l.modo === 'placa' ? l.valor : 'código'}</td>
											<td>{l.resultado === 'entra' ? <span class="chip chip--vigente"><span class="chip__punto" />Entró</span> : <ChipEstado e="rechazado" />}</td>
											<td class="tabla__motivo">{l.motivo ?? `Otorgó ${l.autor}`}</td>
										</tr>
									))}
								</tbody>
							</table>
						</div>
					</section>
				</div>
				<aside class="porteria__lateral">
					<h2 class="rotulo">Simular una llegada</h2>
					<div class="llegadas">
						{llegadas.slice(0, 10).map((l) => (
							<button class="llegada" onClick={() => simular(l)} disabled={!!leyendo}>
								<Icono n={l.modo} tam={20} />
								<span class="llegada__texto">
									<b>{l.quien}</b>
									<span class="mono tenue">{l.etiqueta}</span>
								</span>
							</button>
						))}
					</div>
					<div class="porteria__digitar">
						<div class="opciones opciones--2">
							<button class={`opcion ${teclado === 'codigo' ? 'activo' : ''}`} onClick={() => setTeclado(teclado === 'codigo' ? '' : 'codigo')}>Digitar código</button>
							<button class={`opcion ${teclado === 'placa' ? 'activo' : ''}`} onClick={() => setTeclado(teclado === 'placa' ? '' : 'placa')}>Digitar placa</button>
						</div>
						{teclado && (
							<form class="teclado" onSubmit={(e) => (e.preventDefault(), enviarTeclado())}>
								<input class="mono mayus" autoFocus value={entrada} placeholder={teclado === 'codigo' ? '4817' : 'KMN 305'} onInput={(e) => setEntrada((e.target as HTMLInputElement).value)} aria-label={teclado === 'codigo' ? 'Código' : 'Placa'} />
								<button class="accion">Leer</button>
							</form>
						)}
					</div>
				</aside>
			</div>
		</div>
	);
}

// Escena 3D aprobada (M3D-2, M3D-3, M3D-6): portería de noche, el lector confirma y la talanquera sube.
// Tiempos del video (60 fps, 4,33 s): la cámara llega hasta 1,85 s; la luz del lector se enciende en 1,85 s;
// la talanquera sube entre 2,5 y 3,0 s. La lectura del prototipo dura 1,1 s, así que arranca en 0,75 s y el
// veredicto coincide con el cuadro en que la luz se enciende. Espejada: el lector queda a la derecha del texto.
const CINE = {reposo: 0.75, espera: 1.8, confirma: 1.85, rechazo: 1.7};
const LUZ = {x: 100 - 30.3, y: 51.1}; // posición de la luz del lector en el cuadro espejado, en %

function Panel({estado: ep, leyendo, ultima, llamada, onLlamar}: {estado: string; leyendo: Llegada | null; ultima: Lectura | null; pulso: number; llamada: string; onLlamar: (id: string) => void}) {
	const panel = useRef<HTMLDivElement>(null);
	const video = useRef<HTMLVideoElement>(null);
	const cine = useRef<HTMLDivElement>(null);
	const cuenta = useRef<HTMLSpanElement>(null);
	const diana = useRef<HTMLDivElement>(null);
	const pase = ultima?.paseId ? E.pases.find((p) => p.id === ultima.paseId) : undefined;
	const entra = ultima?.resultado === 'entra';
	const red = reducido();
	const [cuadro, setCuadro] = useState<'reposo' | 'abierta' | 'rechazo'>('reposo');

	// El video solo acepta una posición cuando ya cargó sus metadatos; antes de eso, espera.
	const ir = (t: number, reproducir: boolean) => {
		const v = video.current;
		if (!v) return;
		const aplicar = () => {
			if (Math.abs(v.currentTime - t) > 0.12) v.currentTime = t;
			if (reproducir) v.play().catch(() => {});
			else v.pause();
		};
		if (v.readyState >= 1) aplicar();
		else v.addEventListener('loadedmetadata', aplicar, {once: true});
	};
	useEffect(() => {
		if (!red) ir(CINE.reposo, false);
	}, []);

	// leyendo: la cámara avanza hacia el lector, como el carro que llega, y se detiene frente a él (1,80 s)
	//          hasta que el lector decide: la luz nunca se enciende antes del veredicto.
	useEffect(() => {
		if (ep !== 'leyendo') return;
		setCuadro('reposo');
		if (red) return;
		ir(CINE.reposo, true);
		let id = 0;
		const vigilar = () => {
			const v = video.current;
			if (v && v.currentTime >= CINE.espera) return v.pause();
			id = requestAnimationFrame(vigilar);
		};
		id = requestAnimationFrame(vigilar);
		return () => cancelAnimationFrame(id);
	}, [ep, leyendo?.etiqueta]);

	useLayoutEffect(() => {
		if (!ultima || !panel.current) return;
		const el = panel.current;
		const anillos = [...(diana.current?.children ?? [])];
		[el, cine.current, cuenta.current, ...anillos].forEach((n) => n?.getAnimations().forEach((a) => a.cancel()));
		// 1 · el veredicto (color, ícono y palabra) ya está en el primer cuadro; el ícono se traza sin espera
		el.querySelectorAll<SVGPathElement>('.veredicto__trazo').forEach((p, i) =>
			animar(p, [{strokeDashoffset: 1}, {strokeDashoffset: 0}], {duration: D.corto, easing: C.crecer, delay: i * 40, fill: 'both'}),
		);
		// 2 · lo secundario entra en cascada de 20 ms
		el.querySelectorAll<HTMLElement>('[data-cascada]').forEach((n) => {
			const i = Number(n.dataset.cascada);
			if (i === 0) return;
			animar(n, [{opacity: 0, transform: 'translateY(8px)'}, {opacity: 1, transform: 'none'}], {duration: D.corto, easing: C.crecer, delay: i * 20, fill: 'both'});
		});
		if (entra) {
			// 3a · la luz del lector se enciende en el video en este mismo cuadro; la talanquera sube 650 ms después
			setCuadro('abierta');
			if (!red) ir(CINE.confirma, true);
			// sinapsis: tres anillos convergen sobre la luz real del lector
			anillos.forEach((a, i) =>
				animar(a, [{transform: 'translate(-50%,-50%) scale(3)', opacity: 0}, {transform: 'translate(-50%,-50%) scale(1)', opacity: 1, offset: 0.7}, {transform: 'translate(-50%,-50%) scale(1)', opacity: 0}], {duration: D.tarjeta * 2, easing: C.crecer, delay: i * 90, fill: 'both'}),
			);
			animar(cuenta.current, [{transform: 'scaleX(1)'}, {transform: 'scaleX(0)'}], {duration: ABIERTA_MS, easing: 'linear', fill: 'both'});
			// 3b · se cierra sola: la escena vuelve a reposo con un fundido, sin saltar
			const t = setTimeout(() => {
				const c = cine.current;
				const volver = () => (setCuadro('reposo'), red ? undefined : ir(CINE.reposo, false));
				if (!c) return volver();
				animar(c, [{opacity: 1}, {opacity: 0.25}], {duration: D.corto, easing: C.salir, fill: 'forwards'})?.finished.then(() => {
					volver();
					animar(c, [{opacity: 0.25}, {opacity: 1}], {duration: D.crecer, easing: C.crecer, fill: 'forwards'});
				}).catch(() => {});
			}, ABIERTA_MS);
			return () => clearTimeout(t);
		}
		// 3c · no entra: la escena se congela antes de que la luz se encienda; la luz roja late dos veces;
		//      el panel se contrae rápido y se recupera lento (Mimosa pudica)
		setCuadro('rechazo');
		if (!red) ir(CINE.rechazo, false);
		if (!red) animar(el, [{transform: 'scale(1)'}, {transform: 'scale(.985)', offset: D.instante / (D.instante + D.decaer)}, {transform: 'scale(1)'}], {duration: D.instante + D.decaer, easing: C.decaer});
		animar(el.querySelector('.lector__luz'), [{opacity: 0}, {opacity: 1}, {opacity: 0.35}, {opacity: 1}, {opacity: 0.35}, {opacity: 1}], {duration: D.latir, easing: C.latir, fill: 'forwards'});
	}, [ultima?.id]);

	const poster = `assets/porteria-${cuadro === 'reposo' ? 'reposo' : cuadro === 'abierta' ? 'abierta' : 'rechazo'}.webp`;
	return (
		<section ref={panel} class={`lector lector--${ep}`} aria-live="polite">
			<div ref={cine} class="lector__cine" aria-hidden="true">
				<div class="lector__cuadro">
					{red ? (
						<img class="lector__video" src={poster} alt="" />
					) : (
						<video ref={video} class="lector__video" muted playsInline preload="auto" poster="assets/porteria-reposo.webp">
							<source src="assets/porteria.mp4" type='video/mp4; codecs="hvc1"' />
							<source src="assets/porteria.webm" type="video/webm" />
						</video>
					)}
					<span class="lector__luz" style={{left: `${LUZ.x}%`, top: `${LUZ.y}%`}} />
					<div ref={diana} class="diana" style={{left: `${LUZ.x}%`, top: `${LUZ.y}%`}}>
						<i class="diana__anillo" />
						<i class="diana__anillo" />
						<i class="diana__anillo" />
					</div>
				</div>
				<span class="lector__velo" />
			</div>
			<div class="lector__contenido">
				{ep === 'reposo' && (
					<div class="lector__texto">
						<span class="rotulo">Lector en línea · Portería principal</span>
						<span class="lector__titulo">Esperando llegada</span>
						<span class="nota">El lector permite el ingreso. Aquí se ve por qué.</span>
					</div>
				)}
				{ep === 'leyendo' && leyendo && (
					<div class="lector__texto">
						<span class="rotulo">Leyendo {MODO[leyendo.modo]}</span>
						<span class="lector__titulo">{leyendo.etiqueta}</span>
						<span class="puntos" aria-hidden="true"><i /><i /><i /></span>
					</div>
				)}
				{ultima && (
					<div class="lector__texto" key={ultima.id}>
						<span class="veredicto">
							<svg class="veredicto__icono" viewBox="0 0 24 24" aria-hidden="true">
								{entra ? <path class="veredicto__trazo" pathLength={1} d="M4.5 12.5l5 5 10-11" /> : <><path class="veredicto__trazo" pathLength={1} d="M6 6l12 12" /><path class="veredicto__trazo" pathLength={1} d="M18 6L6 18" /></>}
							</svg>
							<span data-cascada="0">{entra ? 'Puede entrar' : 'No entra'}</span>
						</span>
						<span class="lector__titulo" data-cascada="1">{ultima.nombre}</span>
						{ultima.motivo && <span class="lector__motivo" data-cascada="2">{ultima.motivo}</span>}
						{!entra && pase && (
							<div class="lector__llamar" data-cascada="4">
								{llamada === 'no' && (
									<button class="secundario-btn" onClick={() => onLlamar(pase.id)}>
										<Icono n="telefono" />
										Llamar a {pase.autor.nombre.split(' ')[0]}
									</button>
								)}
								{llamada === 'llamando' && <span class="llamando">Llamando a {pase.autor.nombre}…</span>}
								{llamada === 'contesto' && <span class="nota">{pase.autor.nombre.split(' ')[0]} contestó. Si quiere que entre, extiende el Pase y se vuelve a leer.</span>}
								<span class="nota">La llamada no abre la entrada.</span>
							</div>
						)}
						{entra && (
							<div class="lector__cuenta" data-cascada="4">
								<span class="rotulo">Se cierra sola</span>
								<span class="lector__cuenta-pista"><span ref={cuenta} /></span>
							</div>
						)}
					</div>
				)}
			</div>
			{/* La franja de datos siempre ocupa su lugar: el panel no cambia de alto entre reposo y veredicto. */}
			{ultima && pase ? (
				<dl class="lector__datos" key={`d${ultima.id}`} data-cascada="3">
					<div><dt>Casa</dt><dd>{pase.autor.casa}</dd></div>
					<div><dt>Otorgó</dt><dd>{pase.autor.nombre}</dd></div>
					<div><dt>Con</dt><dd class="mono">{ultima.modo === 'qr' ? 'QR' : ultima.modo === 'placa' ? ultima.valor : 'código'}</dd></div>
					<div><dt>Vigencia</dt><dd class="mono">{vigenciaTexto(pase)}</dd></div>
				</dl>
			) : (
				<dl class="lector__datos lector__datos--dia">
					<div><dt>Entradas hoy</dt><dd class="mono">{E.lecturas.filter((l) => l.resultado === 'entra').length}</dd></div>
					<div><dt>Rechazos hoy</dt><dd class="mono">{E.lecturas.filter((l) => l.resultado === 'rechazado').length}</dd></div>
					<div><dt>Lector</dt><dd>En línea</dd></div>
					<div><dt>{ultima ? 'Última lectura' : 'Integración'}</dt><dd>{ultima ? ultima.nombre : 'HikCentral confirmó hace 1 min'}</dd></div>
				</dl>
			)}
		</section>
	);
}
