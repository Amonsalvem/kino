// App del residente: ingreso por WhatsApp, Pases vivos, crear, compartir, detalle, extender y revocar.
import {useEffect, useLayoutEffect, useMemo, useRef, useState} from 'preact/hooks';
import {
	ahora, anotar, compartir, crearPase, cuentaRegresiva, deshacerRevocar, diasTexto, duraMasDeUnDia, duracionTexto, E, emitir, esEstadia, estado, extender,
	fechaCorta, hora24, horaBreve, horaCorta, horaTexto, min, RECIENTES, RESIDENTE, revocar, validar, ventana, vigenciaTexto, type Modo, type Pase, type Tipo,
} from './modelo';
import {BotonMantener, ChipEstado, Cifra, useAnterior, Digitos, Fundir, Icono, Ilustracion, Iniciales, lineaVigencia, Marca, Portal, Relevo, TarjetaPase, useFlip, useIndicador, useKino, usePresencia, type ModoVista} from './componentes';
import {animar, C, D, morfar, R, reducido, vibrar, volar} from './movimiento';
import {animarResorte, arrastrar} from '../../paquetes/kino-motion/src/web/fisica';

type Pantalla = {v: 'ingreso'} | {v: 'inicio'; tab: 'pases' | 'avisos' | 'casa'} | {v: 'detalle'; id: string};

export function Residente() {
	const est = useKino(1000);
	const [pant, setPant] = useState<Pantalla>(est.sesion ? {v: 'inicio', tab: 'pases'} : {v: 'ingreso'});
	const [hoja, setHoja] = useState<null | {precarga?: (typeof RECIENTES)[number]}>(null);
	const [banner, setBanner] = useState<string | null>(null);
	// Al entrar desde la bienvenida, el inicio llega en cascada.
	const [llegada, setLlegada] = useState(false);
	const vistosAvisos = useRef(0);
	// Continuidad: desde dónde viaja el Pase al abrir el detalle y a dónde vuelve al cerrarlo.
	const origen = useRef<DOMRect | null>(null);
	const regreso = useRef<{id: string; r: DOMRect} | null>(null);

	useEffect(() => {
		if (!est.sesion && pant.v !== 'ingreso') setPant({v: 'ingreso'});
	}, [est.sesion]);

	// Aviso de llegada o rechazo: cae desde arriba.
	const propios = est.avisos.filter((a) => a.para === 'residente');
	useEffect(() => {
		if (propios.length > vistosAvisos.current && est.sesion) {
			const a = propios[propios.length - 1];
			setBanner(a.id);
			anotar('I-11');
			vibrar(a.tono === 'vigente' ? 25 : [20, 60, 20]);
			const t = setTimeout(() => setBanner(null), 5200);
			vistosAvisos.current = propios.length;
			return () => clearTimeout(t);
		}
		vistosAvisos.current = propios.length;
	}, [propios.length]);
	const [aviso, avisoSale] = usePresencia(propios.find((a) => a.id === banner));

	return (
		<div class="app app--residente">
			{pant.v === 'ingreso' && <Ingreso onListo={() => (setLlegada(true), setPant({v: 'inicio', tab: 'pases'}))} />}
			{pant.v === 'inicio' && (
				<Inicio tab={pant.tab} regreso={regreso} llegada={llegada} onLlego={() => setLlegada(false)} onTab={(tab) => setPant({v: 'inicio', tab})} onAbrir={(p, el) => ((origen.current = el?.getBoundingClientRect() ?? null), setPant({v: 'detalle', id: p.id}))} onCrear={(precarga) => setHoja({precarga})} />
			)}
			{pant.v === 'detalle' && <Detalle id={pant.id} origen={origen.current} onVolver={(r) => ((regreso.current = r ? {id: pant.id, r} : null), setPant({v: 'inicio', tab: 'pases'}))} />}
			{hoja && <HojaCrear precarga={hoja.precarga} onCerrar={() => setHoja(null)} onVer={(p, r) => ((origen.current = r ?? null), setHoja(null), setPant({v: 'detalle', id: p.id}))} />}
			{aviso && (
				<button
					class={`banner banner--${aviso.tono} ${avisoSale ? 'sale' : ''}`}
					onClick={(ev) => {
						// El Pase sale del aviso: el banner es el origen del vuelo al detalle.
						origen.current = (ev.currentTarget as HTMLElement).getBoundingClientRect();
						setBanner(null);
						if (aviso.paseId) setPant({v: 'detalle', id: aviso.paseId});
					}}
				>
					<Marca tam={22} />
					<span>
						<b>{aviso.titulo}</b>
						<span>{aviso.texto}</span>
					</span>
				</button>
			)}
			<Deshacer />
		</div>
	);
}

// Ingreso --------------------------------------------------------------------------------------------
function Ingreso({onListo}: {onListo: () => void}) {
	const [paso, setPaso] = useState<'numero' | 'codigo' | 'bienvenida'>('numero');
	const [tel, setTel] = useState(RESIDENTE.telefono);
	const [cod, setCod] = useState('');
	const [notiActiva, setNoti] = useState(false);
	const [noti, notiSale] = usePresencia(notiActiva);
	const raiz = useRef<HTMLDivElement>(null);
	const CODIGO = '482913';
	const valido = tel.replace(/\D/g, '').length === 10;

	const enviar = () => {
		setPaso('codigo');
		setTimeout(() => setNoti(true), 900);
	};
	const autollenar = () => {
		setNoti(false);
		CODIGO.split('').forEach((_, i) => setTimeout(() => setCod(CODIGO.slice(0, i + 1)), 90 * (i + 1)));
	};
	useEffect(() => {
		if (cod.length !== 6) return;
		if (cod !== CODIGO) return;
		const t = setTimeout(() => {
			setPaso('bienvenida');
			anotar('I-01');
		}, 380);
		return () => clearTimeout(t);
	}, [cod]);
	useEffect(() => {
		if (paso !== 'bienvenida') return;
		// La bienvenida se despide antes de dar paso al inicio: sube un poco y se funde.
		const t = setTimeout(() => {
			const a = [...(raiz.current?.querySelectorAll('.ingreso__marca, .ingreso__pasos') ?? [])].map((n, i) => animar(n, [{opacity: 1}, {opacity: 0, transform: 'translateY(-12px)'}], {duration: D.corto * 0.6, easing: C.salir, delay: i * 40, fill: 'forwards'}))[1];
			const listo = () => {
				E.sesion = true;
				emitir();
				onListo();
			};
			a && !reducido() ? a.finished.then(listo, listo) : listo();
		}, 1500);
		return () => clearTimeout(t);
	}, [paso]);

	return (
		<div ref={raiz} class="ingreso">
			{/* La bienvenida amanece con la aurora oficial: el único momento ceremonial del ingreso. */}
			{paso === 'bienvenida' && <span class="aurora aurora--ingreso" aria-hidden="true" />}
			<div class="ingreso__marca">
				<Marca tam={56} />
				<span class="ingreso__logotipo">KINO</span>
			</div>
			<Relevo k={paso} dir={paso === 'numero' ? -1 : 1} clase="ingreso__pasos">
				{(k) =>
					k === 'numero' ? (
				<div class="ingreso__cuerpo">
							<h1 class="titulo">Entra con tu WhatsApp</h1>
							<p class="secundario">Te enviamos un código de 6 cifras.</p>
							<label class="campo">
								<span class="rotulo">Tu número</span>
								<span class="campo__fila">
									<span class="mono tenue">+57</span>
									<input inputMode="numeric" value={tel} onInput={(e) => setTel((e.target as HTMLInputElement).value)} aria-label="Número de WhatsApp" />
								</span>
							</label>
							<button class="accion" disabled={!valido} onClick={enviar}>
								Enviar código
							</button>
							<p class="nota">Si es tu primera vez, te reconocemos por la cédula que tiene la administración.</p>
						</div>
					) : k === 'codigo' ? (
				<div class="ingreso__cuerpo">
							<h1 class="titulo">Escribe el código</h1>
							<p class="secundario">Llegó al WhatsApp de {tel}</p>
							<div class="otp" onClick={autollenar}>
								{Array.from({length: 6}, (_, i) => (
									<span class={`otp__celda ${cod[i] ? 'otp__celda--llena' : ''} ${i === cod.length ? 'otp__celda--foco' : ''}`}>{cod[i] ?? ''}</span>
								))}
							</div>
							<input class="otp__entrada" inputMode="numeric" maxLength={6} value={cod} onInput={(e) => setCod((e.target as HTMLInputElement).value.replace(/\D/g, ''))} aria-label="Código de 6 cifras" />
							<button class="enlace" onClick={() => setPaso('numero')}>
								Cambiar número
							</button>
						</div>
					) : (
				<div class="ingreso__cuerpo ingreso__bienvenida">
							<span class="rotulo">{RESIDENTE.comunidad}</span>
							<h1 class="titulo">Hola, Carolina</h1>
							<p class="secundario">{RESIDENTE.casa}</p>
						</div>
					)
				}
			</Relevo>
			{noti && (
				<button class={`notificacion ${notiSale ? 'sale' : ''}`} onClick={autollenar}>
					<span class="notificacion__app">Mensajes · ahora</span>
					<b>Kino</b>
					<span>Tu código es {CODIGO.slice(0, 3)} {CODIGO.slice(3)}. Vence en 10 minutos.</span>
					<span class="notificacion__accion">Tocar para llenar</span>
				</button>
			)}
		</div>
	);
}

// Inicio ---------------------------------------------------------------------------------------------
type Tab = 'pases' | 'avisos' | 'casa';

const ORDEN_TAB: Tab[] = ['pases', 'avisos', 'casa'];
function Inicio({tab, regreso, llegada, onLlego, onTab, onAbrir, onCrear}: {tab: Tab; regreso: {current: {id: string; r: DOMRect} | null}; llegada?: boolean; onLlego?: () => void; onTab: (t: Tab) => void; onAbrir: (p: Pase, el?: HTMLElement) => void; onCrear: (pre?: (typeof RECIENTES)[number]) => void}) {
	const est = useKino(1000);
	// Pestañas: el contenido entra desde el lado hacia el que se movió la barra.
	const scroll = useRef<HTMLDivElement>(null);
	const tabAntes = useRef(tab);
	useLayoutEffect(() => {
		const dir = Math.sign(ORDEN_TAB.indexOf(tab) - ORDEN_TAB.indexOf(tabAntes.current));
		tabAntes.current = tab;
		if (dir) animar(scroll.current, [{opacity: 0, transform: `translateX(${dir * 18}px)`}, {opacity: 1, offset: 0.45}, {opacity: 1, transform: 'none'}], {duration: D.crecer, easing: C.crecer});
	}, [tab]);
	// Desde la bienvenida: la cabecera, los recientes, las listas y la barra llegan en cascada.
	const raiz = useRef<HTMLDivElement>(null);
	useLayoutEffect(() => {
		if (!llegada) return;
		onLlego?.();
		const piezas = raiz.current?.querySelectorAll('.cabecera, .seccion, .barra-inferior') ?? [];
		piezas.forEach((n, i) => animar(n, [{opacity: 0, transform: 'translateY(18px)'}, {opacity: 1, transform: 'none'}], {duration: D.tarjeta, easing: C.crecer, delay: i * 60, fill: 'backwards'}));
	}, []);
	const barra = useRef<HTMLElement>(null);
	useIndicador(barra, tab);
	const [pie, pieSale] = usePresencia(tab === 'pases');
	const vuelo = regreso.current;
	useEffect(() => {
		regreso.current = null;
	});
	const t = ahora();
	const firma = est.pases.map((p) => estado(p, t)).join();
	const grupos = useMemo(() => {
		const ahora_: Pase[] = [];
		const proximos: Pase[] = [];
		const anteriores: Pase[] = [];
		for (const p of est.pases) {
			const e = estado(p, t);
			if (e === 'vigente' || e === 'por-vencer' || e === 'sin-confirmar') ahora_.push(p);
			else if (e === 'previsto') proximos.push(p);
			else anteriores.push(p);
		}
		return {ahora_, proximos, anteriores};
	}, [est.pases.length, firma]);
	const [verAnt, setVerAnt] = useState(false);
	// Un Pase que cambia de grupo (Ahora → Anteriores) o uno nuevo: los demás se acomodan y él viaja (FLIP).
	useFlip(scroll, `${tab}|${verAnt}|${[...grupos.ahora_, ...grupos.proximos, ...grupos.anteriores].map((p) => p.id).join()}`);
	const estadias = grupos.ahora_.filter(esEstadia).length;
	const colab = grupos.ahora_.filter((p) => p.tipo === 'colaborador').length;

	return (
		<div ref={raiz} class="inicio">
			<div ref={scroll} class="pantalla__scroll">
				{tab === 'pases' && (
					<>
						<header class="cabecera">
							<span class="aurora" aria-hidden="true" />
							<div class="cabecera__fila">
								<span class="chip-dato">{RESIDENTE.comunidad} · {RESIDENTE.casa}</span>
								<Marca tam={24} />
							</div>
							<h1 class="titulo titulo--xl">Tus Pases</h1>
							<dl class="resumen-casa">
								<div>
									<dd class="mono">
										<Cifra v={grupos.ahora_.length} />
									</dd>
									<dt>vivos ahora</dt>
								</div>
								<div>
									<dd class="mono">
										<Cifra v={estadias} />
									</dd>
									<dt>{estadias === 1 ? 'estadía' : 'estadías'}</dt>
								</div>
								<div>
									<dd class="mono">
										<Cifra v={colab} />
									</dd>
									<dt>{colab === 1 ? 'colaborador' : 'colaboradores'}</dt>
								</div>
							</dl>
						</header>

						<section class="seccion">
							<h2 class="rotulo">Volver a invitar</h2>
							<div class="recientes">
								{RECIENTES.map((r) => (
									<button class="reciente" onClick={() => (anotar('I-03'), onCrear(r))}>
										<Iniciales nombre={r.nombre} tono={r.tipo} />
										<span>{r.nombre.split(' ')[0]}</span>
									</button>
								))}
							</div>
						</section>

						{grupos.ahora_.length === 0 && grupos.proximos.length === 0 && (
							<div class="vacio vacio--ilustrado">
								<Ilustracion tipo="pase-vacio" />
								<p class="secundario">No tienes Pases vivos. Crea uno cuando esperes a alguien.</p>
							</div>
						)}
						{grupos.ahora_.length > 0 && (
							<section class="seccion">
								<h2 class="rotulo" data-k="g-ahora">Ahora</h2>
								<div class="lista">{grupos.ahora_.map((p, i) => <TarjetaPase key={p.id} p={p} retraso={i * 90} vuelo={vuelo?.id === p.id ? vuelo.r : undefined} onAbrir={(p, el) => (anotar('I-02'), onAbrir(p, el))} />)}</div>
							</section>
						)}
						{grupos.proximos.length > 0 && (
							<section class="seccion">
								<h2 class="rotulo" data-k="g-proximos">Próximos</h2>
								<div class="lista">{grupos.proximos.map((p, i) => <TarjetaPase key={p.id} p={p} retraso={i * 90} vuelo={vuelo?.id === p.id ? vuelo.r : undefined} onAbrir={onAbrir} />)}</div>
							</section>
						)}
						{grupos.anteriores.length > 0 && (
							<section class="seccion">
								<button class="enlace" data-k="g-anteriores" onClick={() => setVerAnt(!verAnt)} aria-expanded={verAnt}>
									<Fundir t={`${verAnt ? 'Ocultar' : 'Ver'} Pases anteriores · ${grupos.anteriores.length}`} />
								</button>
								{verAnt && <div class="lista">{grupos.anteriores.map((p, i) => <TarjetaPase key={p.id} p={p} retraso={i * 55} vuelo={vuelo?.id === p.id ? vuelo.r : undefined} onAbrir={onAbrir} />)}</div>}
							</section>
						)}
						<div class="relleno-pie" />
					</>
				)}
				{tab === 'avisos' && <Avisos onAbrir={onAbrir} />}
				{tab === 'casa' && <MiCasa />}
			</div>
			{pie && (
				<div class={`pie-accion pie-accion--sobre-barra ${pieSale ? 'sale' : ''}`}>
					<button class="accion accion--crear" onClick={() => onCrear()}>
						<Icono n="mas" />
						Crear Pase
					</button>
				</div>
			)}
			<nav ref={barra} class="barra-inferior con-indicador" aria-label="Secciones">
				<span class="indicador" aria-hidden="true" />
				{(
					[
						['pases', 'Pases', 'pases'],
						['avisos', 'Avisos', 'aviso'],
						['casa', 'Mi casa', 'casa'],
					] as const
				).map(([k, txt, ic]) => (
					<button class={`barra-inferior__item ${tab === k ? 'activo' : ''}`} onClick={() => onTab(k)} aria-current={tab === k ? 'page' : undefined}>
						<Icono n={ic} />
						<span>{txt}</span>
						{k === 'avisos' && E.avisos.some((a) => a.para === 'residente') && <i class="punto-aviso" />}
					</button>
				))}
			</nav>
		</div>
	);
}

const avisosVistos = new Set<string>();
function Avisos({onAbrir}: {onAbrir: (p: Pase, el?: HTMLElement) => void}) {
	const est = useKino(2000);
	const lista = [...est.avisos.filter((a) => a.para === 'residente')].reverse();
	return (
		<div class="pagina">
			<h1 class="titulo titulo--xl">Avisos</h1>
			{lista.length === 0 && (
				<div class="vacio vacio--ilustrado">
					<Ilustracion tipo="llegada" />
					<p class="secundario">Aquí aparece cada entrada con tu Pase y cada rechazo con su motivo.</p>
					<p class="nota">Prueba: en Portería, lee el QR de Andrés.</p>
				</div>
			)}
			<div class="lista">
				{lista.map((a) => {
					const p = est.pases.find((x) => x.id === a.paseId);
					// Solo entra el aviso que no se había visto; los demás ya estaban ahí.
					const nuevo = !avisosVistos.has(a.id);
					avisosVistos.add(a.id);
					return (
						<button key={a.id} class={`fila-aviso fila-aviso--${a.tono} ${nuevo ? 'fila-aviso--nueva' : ''}`} onClick={(ev) => p && onAbrir(p, ev.currentTarget as HTMLElement)}>
							<span class="mono tenue">{hora24(a.hora)}</span>
							<span class="fila-aviso__texto">
								<b>{a.titulo}</b>
								<span class="secundario">{a.texto}</span>
							</span>
						</button>
					);
				})}
			</div>
		</div>
	);
}

function MiCasa() {
	const est = useKino(2000);
	const L = est.limites;
	return (
		<div class="pagina">
			<div class="pagina__cabeza">
				<h1 class="titulo titulo--xl">Mi casa</h1>
				<p class="secundario">{RESIDENTE.casa} · {RESIDENTE.comunidad}</p>
			</div>
			<section class="grupo">
				<h2 class="rotulo">Lo que decides tú</h2>
				<p class="nota">Cuántas visitas tienes y cuánto se queda cada una. Una estadía puede durar semanas o meses.</p>
			</section>
			<section class="grupo">
				<h2 class="rotulo">Lo que fija la administración</h2>
				<dl class="datos">
					<div><dt>Visitas de un día</dt><dd class="mono">{horaBreve(dia(L.visitaDesde))} a {horaBreve(dia(L.visitaHasta))}</dd></div>
					<div><dt>Colaboradores</dt><dd class="mono">{horaBreve(dia(L.colabDesde))} a {horaBreve(dia(L.colabHasta))}</dd></div>
					<div><dt>Estadías</dt><dd class="mono">a cualquier hora</dd></div>
				</dl>
			</section>
			<section class="grupo">
				<h2 class="rotulo">Vehículos</h2>
				<dl class="datos">
					<div><dt>Mazda 3 gris</dt><dd class="mono">JKL 482</dd></div>
				</dl>
				<p class="nota">El cambio de número de WhatsApp pasa por la administración.</p>
			</section>
			<button class="secundario-btn" onClick={() => ((E.sesion = false), emitir())}>Cerrar sesión</button>
		</div>
	);
}

const dia = (minutos: number) => {
	const d = new Date(ahora());
	d.setHours(0, minutos, 0, 0);
	return d;
};

// Hoja: crear Pase -----------------------------------------------------------------------------------
type Cuando = 'horas' | 'dia' | 'estadia';
const PLAZOS: {k: string; dias: number; txt: string}[] = [
	{k: '3d', dias: 3, txt: '3 días'},
	{k: '1s', dias: 7, txt: '1 semana'},
	{k: '1m', dias: 30, txt: '1 mes'},
	{k: '3m', dias: 90, txt: '3 meses'},
];

function HojaCrear({precarga, onCerrar, onVer}: {precarga?: (typeof RECIENTES)[number]; onCerrar: () => void; onVer: (p: Pase, r?: DOMRect) => void}) {
	useKino(1000);
	const t0 = ahora();
	const [tipo, setTipo] = useState<Tipo>(precarga?.tipo ?? 'visita');
	const [nombre, setNombre] = useState(precarga?.nombre ?? '');
	const [tel, setTel] = useState(precarga?.telefono ?? '');
	const [placa, setPlaca] = useState(precarga?.placa ?? '');
	const [motivo] = useState(precarga?.motivo);
	const [cuando, setCuando] = useState<Cuando>('horas');
	const [horas, setHoras] = useState(3);
	const [manana, setManana] = useState(false);
	const [dias, setDiasEstadia] = useState(7);
	const [diasColab, setDiasColab] = useState<number[]>([1, 2, 3, 4, 5]);
	const [franja, setFranja] = useState<[number, number]>([7, 17]);
	const [creado, setCreado] = useState<Pase | null>(null);
	const [enviado, setEnviado] = useState(false);
	const [boton, setBoton] = useState<DOMRect | null>(null);
	const hojaRef = useRef<HTMLDivElement>(null);
	const fondoRef = useRef<HTMLDivElement>(null);
	const asaRef = useRef<HTMLDivElement>(null);
	const arribaAntes = useRef<number | null>(null);
	const segmentado = useRef<HTMLDivElement>(null);
	const opcionesCuando = useRef<HTMLDivElement>(null);

	useLayoutEffect(() => {
		animar(hojaRef.current, [{transform: 'translateY(100%)'}, {transform: 'none'}], {duration: R.hoja.ms, easing: R.hoja.linear});
		animar(fondoRef.current, [{opacity: 0}, {opacity: 1}], {duration: D.corto});
	}, []);

	const cerrar = () => {
		const a = animar(hojaRef.current, [{transform: getComputedStyle(hojaRef.current!).transform}, {transform: 'translateY(105%)'}], {duration: D.corto, easing: C.salir, fill: 'forwards'});
		animar(fondoRef.current, [{opacity: 1}, {opacity: 0}], {duration: D.corto, fill: 'forwards'});
		a ? (a.onfinish = onCerrar) : onCerrar();
	};

	// Gesto con física (@kino/motion/web): la hoja sigue al dedo, se resiste hacia arriba y, al soltar,
	// decide por la posición proyectada con la velocidad de los últimos 80 ms; vuelve con el resorte desde esa velocidad.
	useEffect(() => {
		const asa = asaRef.current;
		const hoja = hojaRef.current;
		if (!asa || !hoja) return;
		let y = 0;
		const k = () => hoja.getBoundingClientRect().height / (hoja.offsetHeight || 1) || 1;
		const poner = (v: number) => ((y = v), (hoja.style.transform = v ? `translateY(${v}px)` : ''));
		const g = arrastrar(asa, {
			eje: 'y', min: 0, max: hoja.offsetHeight, inicial: () => y * k(),
			alEmpezar: () => hoja.getAnimations().forEach((a) => a.cancel()),
			alMover: (p) => poner(p / k()),
			alSoltar: (p, v) => {
				anotar('I-04');
				const pos = p / k();
				if (pos + (v / k()) * 0.2 > hoja.offsetHeight * 0.3) return cerrar();
				animarResorte({de: pos, a: 0, velocidad: v / k(), resorte: 'hoja', alCambiar: poner, elemento: hoja});
			},
		});
		return () => g.soltar();
	}, []);

	// La hoja cambia de alto (al crear, al cambiar de Visita a Colaborador o de plazo): el borde de arriba se
	// desliza a su lugar en vez de saltar (FLIP). Se mide en el render, antes de que cambie el DOM.
	const forma = `${tipo}|${cuando}|${!!creado}`;
	const formaAntes = useRef(forma);
	if (formaAntes.current !== forma) {
		formaAntes.current = forma;
		if (arribaAntes.current == null) arribaAntes.current = hojaRef.current?.getBoundingClientRect().top ?? null;
	}
	useLayoutEffect(() => {
		const h = hojaRef.current;
		if (!h || arribaAntes.current == null) return;
		const k = h.getBoundingClientRect().height / (h.offsetHeight || 1) || 1;
		const d = (arribaAntes.current - h.getBoundingClientRect().top) / k;
		arribaAntes.current = null;
		if (Math.abs(d) > 1) animar(h, [{transform: `translateY(${d}px)`}, {transform: 'none'}], {duration: R.hoja.ms, easing: R.hoja.linear});
	});
	useIndicador(segmentado, tipo);
	useIndicador(opcionesCuando, `${tipo}|${cuando}`);

	const rango = (): {desde: Date; hasta: Date} => {
		const d = new Date(t0);
		d.setSeconds(0, 0);
		if (tipo === 'colaborador') {
			const a = new Date(d);
			a.setHours(franja[0], 0, 0, 0);
			const b = new Date(d);
			b.setHours(franja[1], 0, 0, 0);
			return {desde: a, hasta: b};
		}
		if (cuando === 'horas') return {desde: d, hasta: new Date(d.getTime() + horas * 3_600_000)};
		if (cuando === 'dia') {
			const a = new Date(d);
			if (manana) a.setDate(a.getDate() + 1);
			else a.setHours(Math.max(d.getHours(), 0));
			if (manana) a.setHours(8, 0, 0, 0);
			const b = new Date(a);
			b.setHours(21, 0, 0, 0);
			return {desde: a, hasta: b};
		}
		const b = new Date(d);
		b.setDate(b.getDate() + dias);
		b.setHours(21, 0, 0, 0);
		return {desde: d, hasta: b};
	};
	const r = rango();
	const recurrencia = tipo === 'colaborador' ? {dias: diasColab, inicio: min(franja[0]), fin: min(franja[1])} : undefined;
	const errorFranja = validar({tipo, desde: r.desde, hasta: r.hasta, recurrencia});
	const telOk = tel.replace(/\D/g, '').length === 10;
	const motivoBoton = !nombre.trim() ? 'Escribe quién viene' : !telOk ? 'Falta el WhatsApp (10 cifras)' : tipo === 'colaborador' && diasColab.length === 0 ? 'Elige al menos un día' : errorFranja;
	const estadia = tipo === 'visita' && duraMasDeUnDia(r);
	const L = E.limites;

	useEffect(() => {
		if (estadia) anotar('I-05');
	}, [estadia]);

	const crear = (ev: MouseEvent) => {
		if (motivoBoton) return;
		const modos: Modo[] = ['qr', 'codigo', ...(placa.trim() ? (['placa'] as Modo[]) : [])];
		vibrar(15);
		// I-06: el botón se convierte en el Pase. Se guarda su forma para la transformación de contenedor.
		setBoton((ev.currentTarget as HTMLElement).getBoundingClientRect());
		arribaAntes.current = hojaRef.current?.getBoundingClientRect().top ?? null;
		setCreado(crearPase({tipo, nombre, telefono: tel, motivo, placa, modos, desde: r.desde, hasta: r.hasta, recurrencia}));
		anotar('I-06');
	};

	const resumen =
		tipo === 'colaborador'
			? `${diasTexto(diasColab) || 'Sin días'} · ${horaBreve(r.desde)} a ${horaBreve(r.hasta)} · hasta que lo revoques`
			: estadia
				? `Estadía · hoy al ${fechaCorta(r.hasta, t0)} · ${duracionTexto(r.desde, r.hasta)} · entra y sale`
				: `${fechaCorta(r.desde, t0) === 'hoy' ? 'Hoy' : 'Mañana'} · ${horaBreve(r.desde)} a ${horaBreve(r.hasta)} · entra y sale`;

	return (
		<div class="capa">
			<div ref={fondoRef} class="capa__fondo" onClick={cerrar} />
			<div ref={hojaRef} class="hoja" role="dialog" aria-label="Crear Pase">
				<div ref={asaRef} class="hoja__asa">
					<i />
					<div class="hoja__titulo">
						<span class="titulo titulo--m">
							<Fundir t={creado ? 'Pase creado' : 'Nuevo Pase'} />
						</span>
						<button class="icono-btn" onClick={cerrar} aria-label="Cerrar">
							<Icono n="x" />
						</button>
					</div>
				</div>
				{!creado ? (
					<div class="hoja__cuerpo">
						<div ref={segmentado} class="segmentado con-indicador" role="tablist">
							<span class="indicador" aria-hidden="true" />
							{(['visita', 'colaborador'] as Tipo[]).map((k) => (
								<button role="tab" aria-selected={tipo === k} class={tipo === k ? 'activo' : ''} onClick={() => setTipo(k)}>
									{k === 'visita' ? 'Visita' : 'Colaborador'}
								</button>
							))}
						</div>
						<div class="grupo">
							<label class="campo">
								<span class="rotulo">¿Quién viene?</span>
								<input value={nombre} placeholder="Nombre y apellido" onInput={(e) => setNombre((e.target as HTMLInputElement).value)} />
							</label>
							<label class="campo">
								<span class="rotulo">Su WhatsApp</span>
								<input class="mono" inputMode="numeric" value={tel} placeholder="300 000 0000" onInput={(e) => setTel((e.target as HTMLInputElement).value)} />
							</label>
							<p class="nota">Ahí le llega el Pase. No instala nada ni crea cuenta.</p>
						</div>

						<Relevo k={tipo} dir={tipo === 'visita' ? -1 : 1}>
							{(k) =>
								k === 'visita' ? (
							<div class="grupo">
								<span class="rotulo">¿Por cuánto tiempo?</span>
								<div ref={opcionesCuando} class="opciones con-indicador" role="radiogroup">
									<span class="indicador" aria-hidden="true" />
									{(
										[
											['horas', 'Unas horas'],
											['dia', 'Un día'],
											['estadia', 'Se queda'],
										] as [Cuando, string][]
									).map(([k, txt]) => (
										<button role="radio" aria-checked={cuando === k} class={`opcion ${cuando === k ? 'activo' : ''}`} onClick={() => setCuando(k)}>
											{txt}
										</button>
									))}
								</div>
								{cuando === 'horas' && <Paso rotulo="Dura" valor={`${horas} h`} menos={() => setHoras(Math.max(1, horas - 1))} mas={() => setHoras(Math.min(18, horas + 1))} />}
								{cuando === 'dia' && (
									<div class="opciones opciones--2">
										<button class={`opcion ${!manana ? 'activo' : ''}`} onClick={() => setManana(false)}>Hoy</button>
										<button class={`opcion ${manana ? 'activo' : ''}`} onClick={() => setManana(true)}>Mañana</button>
									</div>
								)}
								{cuando === 'estadia' && (
									<>
										<div class="opciones opciones--2">
											{PLAZOS.map((x) => (
												<button class={`opcion ${dias === x.dias ? 'activo' : ''}`} onClick={() => setDiasEstadia(x.dias)}>
													{x.txt}
												</button>
											))}
										</div>
										<Paso rotulo="Hasta" valor={fechaCorta(r.hasta, t0)} menos={() => setDiasEstadia(Math.max(2, dias - 1))} mas={() => setDiasEstadia(Math.min(365, dias + 1))} />
									</>
								)}
								<label class="campo">
									<span class="rotulo">Placa · opcional</span>
									<input class="mono mayus" value={placa} placeholder="ABC 123" onInput={(e) => setPlaca((e.target as HTMLInputElement).value)} />
								</label>
							</div>
					) : (
							<div class="grupo">
								<span class="rotulo">Días que viene</span>
								<div class="dias">
									{['D', 'L', 'M', 'M', 'J', 'V', 'S'].map((l, i) => (
										<button class={diasColab.includes(i) ? 'activo' : ''} aria-pressed={diasColab.includes(i)} aria-label={['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'][i]} onClick={() => setDiasColab(diasColab.includes(i) ? diasColab.filter((x) => x !== i) : [...diasColab, i])}>
											{l}
										</button>
									))}
								</div>
								<div class="pasos">
									<Paso rotulo="Entra" valor={horaBreve(dia(franja[0] * 60))} menos={() => setFranja([Math.max(0, franja[0] - 1), franja[1]])} mas={() => setFranja([Math.min(franja[1] - 1, franja[0] + 1), franja[1]])} />
									<Paso rotulo="Sale" valor={horaBreve(dia(franja[1] * 60))} menos={() => setFranja([franja[0], Math.max(franja[0] + 1, franja[1] - 1)])} mas={() => setFranja([franja[0], Math.min(23, franja[1] + 1)])} />
								</div>
							</div>
								)
							}
						</Relevo>
						<div class={`previa-pase ${errorFranja ? 'previa-pase--choca' : ''}`}>
							<span class="rotulo">
								<Fundir t={errorFranja ? 'Fuera de la franja del conjunto' : 'Así queda'} />
							</span>
							<span class="dato">
								<Fundir t={resumen} />
							</span>
							{(errorFranja || (tipo === 'visita' && !estadia)) && (
								<span class="nota">
									{tipo === 'visita' ? `Las visitas de un día entran de ${horaTexto(L.visitaDesde)} a ${horaTexto(L.visitaHasta)}` : `Los colaboradores entran de ${horaTexto(L.colabDesde)} a ${horaTexto(L.colabHasta)}`}
								</span>
							)}
						</div>
					</div>
				) : (
					<Creado p={creado} desde={boton} capa={hojaRef.current} enviado={enviado} onEnviar={() => (setEnviado(true), compartir(creado))} onVer={(r) => onVer(creado, r)} />
				)}
				{!creado && (
					<div class="hoja__pie">
						<button class="accion accion--crear" aria-disabled={!!motivoBoton} onClick={crear}>
							{motivoBoton ? <span class="accion__motivo">{motivoBoton}</span> : 'Crear Pase'}
						</button>
					</div>
				)}
			</div>
		</div>
	);
}

const Paso = ({rotulo, valor, menos, mas}: {rotulo: string; valor: string; menos: () => void; mas: () => void}) => (
	<div class="paso">
		<span class="rotulo">{rotulo}</span>
		<div class="paso__fila">
			<button onClick={menos} aria-label={`Menos: ${rotulo}`}>−</button>
			<span class="mono paso__valor">
				<Fundir t={valor} />
			</span>
			<button onClick={mas} aria-label={`Más: ${rotulo}`}>+</button>
		</div>
	</div>
);

function Creado({p, desde, capa, enviado, onEnviar, onVer}: {p: Pase; desde: DOMRect | null; capa: HTMLElement | null; enviado: boolean; onEnviar: () => void; onVer: (r?: DOMRect) => void}) {
	useKino(500);
	const e = estado(p);
	const ref = useRef<HTMLDivElement>(null);
	const texto = useRef<HTMLDivElement>(null);
	const acciones = useRef<HTMLDivElement>(null);
	useLayoutEffect(() => {
		const arco = ref.current?.querySelector<HTMLElement>('.portal__arco');
		// Transformación de contenedor: el botón verde crece, se curva en arco y se vuelve papel; después aparece el QR.
		if (desde && capa && arco)
			morfar(desde, arco, {fondoDesde: '#00D595', fondoHacia: '#F4FFFA', radioDesde: '16px', radioHacia: '50% 50% 14px 14px / 46% 46% 14px 14px', capa});
		// Lo demás llega cuando el Pase ya tomó forma: superpuesto, no en fila.
		[texto.current, acciones.current].forEach((n, i) =>
			animar(n, [{opacity: 0, transform: 'translateY(12px)'}, {opacity: 1, transform: 'none'}], {duration: D.crecer, easing: C.crecer, delay: R.pase.ms * 0.55 + i * 60, fill: 'backwards'}),
		);
	}, []);
	return (
		<div class="hoja__cuerpo creado">
			<div ref={ref} class="creado__portal">
				<Portal p={p} tam={220} inclinable />
			</div>
			<div ref={texto} class="creado__texto">
				<ChipEstado e={e} grande />
				<h2 class="titulo titulo--l">{p.nombre}</h2>
				<p class="dato dato--vigente">{vigenciaTexto(p)}</p>
				<p class="nota">{e === 'sin-confirmar' ? 'Kino lo envió al lector. Queda vigente cuando el lector confirme.' : 'El lector lo confirmó. Ya puede entrar.'}</p>
			</div>
			<div ref={acciones} class="creado__acciones">
				<button class={`accion ${enviado ? 'accion--hecho' : ''}`} onClick={onEnviar} disabled={enviado}>
					<span key={enviado ? 'si' : 'no'} class={enviado ? 'icono-brota' : undefined}>
						<Icono n={enviado ? 'check' : 'compartir'} />
					</span>
					<Fundir t={enviado ? `Enviado a ${p.nombre.split(' ')[0]}` : 'Enviar por WhatsApp'} />
				</button>
				<button class="secundario-btn" onClick={() => onVer(ref.current?.querySelector('.portal__arco')?.getBoundingClientRect())}>
					Ver el Pase
				</button>
			</div>
		</div>
	);
}

// Detalle --------------------------------------------------------------------------------------------
function Detalle({id, origen, onVolver}: {id: string; origen: DOMRect | null; onVolver: (r?: DOMRect) => void}) {
	useKino(1000);
	const p = E.pases.find((x) => x.id === id);
	const [modo, setModo] = useState<ModoVista>('qr');
	const [error, setError] = useState<string | null>(null);
	const ref = useRef<HTMLDivElement>(null);
	const portal = useRef<HTMLDivElement>(null);
	const modos = useRef<HTMLDivElement>(null);
	const cuenta = useRef<HTMLSpanElement>(null);
	useIndicador(modos, modo);
	const resto = () => [...(ref.current?.querySelectorAll<HTMLElement>('.barra-sup, .modos, .detalle__cuerpo, .pie-accion') ?? [])];
	useLayoutEffect(() => {
		if (!origen) return void animar(ref.current, [{opacity: 0, transform: 'translateX(28px)'}, {opacity: 1, transform: 'none'}], {duration: D.crecer, easing: C.crecer});
		// Elemento compartido: la tarjeta se vuelve el Portal. Lo demás llega cuando el Pase va a medio camino.
		volar(portal.current?.querySelector<HTMLElement>('.portal'), origen);
		resto().forEach((n, i) => animar(n, [{opacity: 0, transform: 'translateY(14px)'}, {opacity: 1, transform: 'none'}], {duration: D.crecer, easing: C.crecer, delay: R.pase.ms * 0.35 + i * 40, fill: 'backwards'}));
	}, []);
	// Volver: lo demás se va primero y más rápido (salida al 60 %); el Pase se queda y aterriza en su tarjeta.
	const volver = () => {
		const r = portal.current?.querySelector('.portal__arco')?.getBoundingClientRect();
		const a = resto().map((n) => animar(n, [{opacity: 1}, {opacity: 0}], {duration: D.corto * 0.6, easing: C.salir, fill: 'forwards'}));
		const fin = a.find(Boolean);
		if (fin && !reducido()) fin.finished.then(() => onVolver(r)).catch(() => onVolver(r));
		else onVolver(r);
	};
	const e = p ? estado(p) : 'vencido';
	const antes = useAnterior(e);
	const vivo = e === 'vigente' || e === 'por-vencer' || e === 'previsto' || e === 'sin-confirmar';
	const [pie, pieSale] = usePresencia(vivo);
	const [errorVisible, errorSale] = usePresencia(error);
	// Al revocar o vencer, Extender sale y lo de abajo sube a su lugar (FLIP); al deshacer, vuelve.
	const [ext, extSale] = usePresencia(vivo && p?.tipo === 'visita');
	const conCuenta = e === 'vigente' || e === 'por-vencer';
	useFlip(ref, `${!!ext}|${conCuenta}`);
	// Usado: el nombre se tacha también aquí, no solo en el Portal.
	useEffect(() => {
		if (antes !== e && e === 'usado') animar(ref.current?.querySelector('.detalle__cabeza .tachado'), [{transform: 'scaleX(0)'}, {transform: 'scaleX(1)'}], {duration: D.corto, easing: C.crecer});
	}, [e]);
	const extenderCon = (h: number) => {
		const err = extender(p!, h);
		setError(err);
		if (err) return;
		// La vigencia crece: la cifra destella una vez y la hora nueva se funde.
		const n = cuenta.current;
		n?.classList.remove('cuenta__num--destello');
		void n?.offsetWidth;
		n?.classList.add('cuenta__num--destello');
		vibrar(10);
	};
	if (!p) return null;
	const v = ventana(p);
	const extensiones: [string, number][] = esEstadia(p) ? [['+1 semana', 168], ['+1 mes', 720]] : [['+1 h', 1], ['+1 día', 24], ['+1 semana', 168]];
	return (
		<div ref={ref} class={`detalle detalle--${e}`}>
			<div class="barra-sup">
				<button class="icono-btn" onClick={volver} aria-label="Volver">
					<Icono n="atras" />
				</button>
				<span class="titulo titulo--s">{p.tipo === 'colaborador' ? 'Pase · colaborador' : esEstadia(p) ? 'Pase · estadía' : 'Pase · visita'}</span>
				<span class="barra-sup__hueco" />
			</div>
			<div class="pantalla__scroll">
				<div ref={portal} class="detalle__portal">
					<Portal p={p} modo={modo} tam={232} inclinable />
					<div ref={modos} class="modos con-indicador" role="tablist">
						<span class="indicador" aria-hidden="true" />
						{p.modos.map((m) => (
							<button role="tab" aria-selected={modo === m} class={modo === m ? 'activo' : ''} onClick={() => setModo(m)}>
								<Icono n={m} tam={18} />
								{m === 'qr' ? 'QR' : m === 'placa' ? 'Placa' : 'Código'}
							</button>
						))}
					</div>
				</div>
				<div class="detalle__cuerpo">
					<div class="detalle__cabeza">
						<ChipEstado e={e} grande />
						<h1 class="titulo titulo--l">
							{p.nombre}
							<span class="tachado" />
						</h1>
						<p class={`dato dato--${e}`}>
							<Fundir t={lineaVigencia(p, e)} />
						</p>
						{conCuenta && (
							<p class="cuenta entra">
								<span class="rotulo">Vence en</span>
								<span ref={cuenta} class="mono cuenta__num">
									<Digitos t={cuentaRegresiva(v.hasta)} />
								</span>
							</p>
						)}
					</div>
					{ext && (
						<section class={`grupo entra ${extSale ? 'sale' : ''}`}>
							<h2 class="rotulo">Extender</h2>
							<div class={`opciones opciones--${extensiones.length}`}>
								{extensiones.map(([txt, h]) => (
									<button class="opcion" onClick={() => extenderCon(h)}>
										{txt}
									</button>
								))}
							</div>
							{errorVisible && <p class={`nota nota--error entra ${errorSale ? 'sale' : ''}`}>{errorVisible}</p>}
						</section>
					)}
					<section class="grupo" data-k="traza">
						<h2 class="rotulo">Lo que pasó</h2>
						<ol class="traza">
							{[...p.traza].reverse().map((t) => (
								<li key={`${t.hora.getTime()}-${t.texto}`} class={`traza__item traza__item--${t.tipo}`}>
									<span class="mono">{fechaCorta(t.hora) === 'hoy' ? hora24(t.hora) : fechaCorta(t.hora)}</span>
									<span>{t.texto}</span>
								</li>
							))}
						</ol>
					</section>
				</div>
			</div>
			{pie && (
				<div class={`pie-accion pie-accion--fijo ${pieSale ? 'sale' : ''}`}>
					<BotonMantener onCompleto={() => revocar(p)} clase="mantener--revocar">
						Mantén presionado para revocar
					</BotonMantener>
				</div>
			)}
		</div>
	);
}

function Deshacer() {
	const est = useKino(250);
	const d = est.deshacer;
	const queda = d ? Math.max(0, d.hasta - Date.now()) : 0;
	if (d && queda <= 0) E.deshacer = undefined;
	const [vis, sale] = usePresencia(d && queda > 0 ? d : null);
	if (!vis) return null;
	return (
		<div class={`deshacer ${sale ? 'sale' : ''}`} role="status">
			<span>Pase revocado. El lector ya no lo acepta.</span>
			<button onClick={deshacerRevocar} disabled={sale}>
				<Icono n="deshacer" tam={18} />
				Deshacer ·{' '}
				<Digitos t={String(Math.max(1, Math.ceil(queda / 1000)))} />
			</button>
		</div>
	);
}
