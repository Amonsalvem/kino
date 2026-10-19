// App del residente: ingreso por WhatsApp, Pases vivos, crear, compartir, detalle, extender y revocar.
import {useEffect, useLayoutEffect, useMemo, useRef, useState} from 'preact/hooks';
import {
	ahora, anotar, compartir, crearPase, cuentaRegresiva, deshacerRevocar, diasTexto, duraMasDeUnDia, duracionTexto, E, emitir, esEstadia, estado, extender,
	fechaCorta, hora24, horaBreve, horaCorta, horaTexto, min, RECIENTES, RESIDENTE, revocar, validar, ventana, vigenciaTexto, type Modo, type Pase, type Tipo,
} from './modelo';
import {BotonMantener, ChipEstado, Icono, Ilustracion, Iniciales, lineaVigencia, Marca, Micelio, Portal, TarjetaPase, useKino, type ModoVista} from './componentes';
import {animar, C, D, R, vibrar} from './movimiento';

type Pantalla = {v: 'ingreso'} | {v: 'inicio'; tab: 'pases' | 'avisos' | 'casa'} | {v: 'detalle'; id: string};

export function Residente() {
	const est = useKino(1000);
	const [pant, setPant] = useState<Pantalla>(est.sesion ? {v: 'inicio', tab: 'pases'} : {v: 'ingreso'});
	const [hoja, setHoja] = useState<null | {precarga?: (typeof RECIENTES)[number]}>(null);
	const [banner, setBanner] = useState<string | null>(null);
	const vistosAvisos = useRef(0);

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
	const aviso = propios.find((a) => a.id === banner);

	return (
		<div class="app app--residente">
			{pant.v === 'ingreso' && <Ingreso onListo={() => setPant({v: 'inicio', tab: 'pases'})} />}
			{pant.v === 'inicio' && (
				<Inicio tab={pant.tab} onTab={(tab) => setPant({v: 'inicio', tab})} onAbrir={(p) => setPant({v: 'detalle', id: p.id})} onCrear={(precarga) => setHoja({precarga})} />
			)}
			{pant.v === 'detalle' && <Detalle id={pant.id} onVolver={() => setPant({v: 'inicio', tab: 'pases'})} />}
			{hoja && <HojaCrear precarga={hoja.precarga} onCerrar={() => setHoja(null)} onVer={(p) => (setHoja(null), setPant({v: 'detalle', id: p.id}))} />}
			{aviso && (
				<button class={`banner banner--${aviso.tono}`} onClick={() => (setBanner(null), aviso.paseId && setPant({v: 'detalle', id: aviso.paseId}))}>
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
	const [noti, setNoti] = useState(false);
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
		const t = setTimeout(() => {
			E.sesion = true;
			emitir();
			onListo();
		}, 1700);
		return () => clearTimeout(t);
	}, [paso]);

	return (
		<div class="ingreso">
			<div class="ingreso__marca">
				<Marca tam={56} />
				<span class="ingreso__logotipo">KINO</span>
			</div>
			{paso === 'numero' && (
				<div class="ingreso__cuerpo entra">
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
			)}
			{paso === 'codigo' && (
				<div class="ingreso__cuerpo entra">
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
			)}
			{paso === 'bienvenida' && (
				<div class="ingreso__cuerpo ingreso__bienvenida entra">
					<Ilustracion tipo="membrana" />
					<span class="rotulo">{RESIDENTE.comunidad}</span>
					<h1 class="titulo">Hola, Carolina</h1>
					<p class="secundario">{RESIDENTE.casa}</p>
				</div>
			)}
			{noti && (
				<button class="notificacion" onClick={autollenar}>
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

function Inicio({tab, onTab, onAbrir, onCrear}: {tab: Tab; onTab: (t: Tab) => void; onAbrir: (p: Pase) => void; onCrear: (pre?: (typeof RECIENTES)[number]) => void}) {
	const est = useKino(1000);
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
	const estadias = grupos.ahora_.filter(esEstadia).length;
	const colab = grupos.ahora_.filter((p) => p.tipo === 'colaborador').length;

	return (
		<div class="inicio">
			<div class="pantalla__scroll">
				{tab === 'pases' && (
					<>
						<header class="cabecera">
							<Micelio clase="micelio--cabecera" densidad={26} />
							<span class="aurora" aria-hidden="true" />
							<div class="cabecera__fila">
								<span class="chip-dato">{RESIDENTE.comunidad} · {RESIDENTE.casa}</span>
								<Marca tam={24} />
							</div>
							<h1 class="titulo titulo--xl">Tus Pases</h1>
							<dl class="resumen-casa">
								<div>
									<dd class="mono">{grupos.ahora_.length}</dd>
									<dt>vivos ahora</dt>
								</div>
								<div>
									<dd class="mono">{estadias}</dd>
									<dt>{estadias === 1 ? 'estadía' : 'estadías'}</dt>
								</div>
								<div>
									<dd class="mono">{colab}</dd>
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
								<h2 class="rotulo">Ahora</h2>
								<div class="lista">{grupos.ahora_.map((p, i) => <TarjetaPase key={p.id} p={p} retraso={i * 90} onAbrir={(p) => (anotar('I-02'), onAbrir(p))} />)}</div>
							</section>
						)}
						{grupos.proximos.length > 0 && (
							<section class="seccion">
								<h2 class="rotulo">Próximos</h2>
								<div class="lista">{grupos.proximos.map((p, i) => <TarjetaPase key={p.id} p={p} retraso={i * 90} onAbrir={onAbrir} />)}</div>
							</section>
						)}
						{grupos.anteriores.length > 0 && (
							<section class="seccion">
								<button class="enlace" onClick={() => setVerAnt(!verAnt)} aria-expanded={verAnt}>
									{verAnt ? 'Ocultar' : 'Ver'} Pases anteriores · {grupos.anteriores.length}
								</button>
								{verAnt && <div class="lista">{grupos.anteriores.map((p, i) => <TarjetaPase key={p.id} p={p} retraso={i * 55} onAbrir={onAbrir} />)}</div>}
							</section>
						)}
						<div class="relleno-pie" />
					</>
				)}
				{tab === 'avisos' && <Avisos onAbrir={onAbrir} />}
				{tab === 'casa' && <MiCasa />}
			</div>
			{tab === 'pases' && (
				<div class="pie-accion pie-accion--sobre-barra">
					<button class="accion accion--crear" onClick={() => onCrear()}>
						<Icono n="mas" />
						Crear Pase
					</button>
				</div>
			)}
			<nav class="barra-inferior" aria-label="Secciones">
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

function Avisos({onAbrir}: {onAbrir: (p: Pase) => void}) {
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
					return (
						<button class={`fila-aviso fila-aviso--${a.tono}`} onClick={() => p && onAbrir(p)}>
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

function HojaCrear({precarga, onCerrar, onVer}: {precarga?: (typeof RECIENTES)[number]; onCerrar: () => void; onVer: (p: Pase) => void}) {
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
	const hojaRef = useRef<HTMLDivElement>(null);
	const fondoRef = useRef<HTMLDivElement>(null);
	const arrastre = useRef<{y0: number; dy: number; t0: number} | null>(null);

	useLayoutEffect(() => {
		animar(hojaRef.current, [{transform: 'translateY(100%)'}, {transform: 'none'}], {duration: R.hoja.ms, easing: R.hoja.linear});
		animar(fondoRef.current, [{opacity: 0}, {opacity: 1}], {duration: D.corto});
	}, []);

	const cerrar = () => {
		const a = animar(hojaRef.current, [{transform: getComputedStyle(hojaRef.current!).transform}, {transform: 'translateY(105%)'}], {duration: D.corto, easing: C.salir, fill: 'forwards'});
		animar(fondoRef.current, [{opacity: 1}, {opacity: 0}], {duration: D.corto, fill: 'forwards'});
		a ? (a.onfinish = onCerrar) : onCerrar();
	};

	// Gesto: arrastrar la hoja hacia abajo para cerrarla.
	const bajar = (e: PointerEvent) => {
		if ((e.target as HTMLElement).closest('button')) return;
		arrastre.current = {y0: e.clientY, dy: 0, t0: performance.now()};
		(e.currentTarget as HTMLElement).setPointerCapture(e.pointerId);
	};
	const mover = (e: PointerEvent) => {
		const a = arrastre.current;
		if (!a) return;
		const escala = hojaRef.current!.getBoundingClientRect().height / hojaRef.current!.offsetHeight || 1;
		a.dy = Math.max(-20, (e.clientY - a.y0) / escala);
		hojaRef.current!.style.transform = `translateY(${a.dy < 0 ? a.dy * 0.3 : a.dy}px)`;
	};
	const soltar = () => {
		const a = arrastre.current;
		arrastre.current = null;
		if (!a) return;
		const v = a.dy / Math.max(1, performance.now() - a.t0);
		anotar('I-04');
		if (a.dy > 140 || v > 0.6) cerrar();
		else {
			animar(hojaRef.current, [{transform: `translateY(${a.dy}px)`}, {transform: 'none'}], {duration: R.hoja.ms, easing: R.hoja.linear});
			hojaRef.current!.style.transform = '';
		}
	};

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
		animar(ev.currentTarget as HTMLElement, [{transform: 'scale(1)'}, {transform: 'scale(.94)'}, {transform: 'scale(1)'}], {duration: R.tacto.ms, easing: R.tacto.linear});
		vibrar(15);
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
				<div class="hoja__asa" onPointerDown={bajar} onPointerMove={mover} onPointerUp={soltar} onPointerCancel={soltar}>
					<i />
					<div class="hoja__titulo">
						<span class="titulo titulo--m">{creado ? 'Pase creado' : 'Nuevo Pase'}</span>
						<button class="icono-btn" onClick={cerrar} aria-label="Cerrar">
							<Icono n="x" />
						</button>
					</div>
				</div>
				{!creado ? (
					<div class="hoja__cuerpo">
						<div class="segmentado" role="tablist">
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

						{tipo === 'visita' ? (
							<div class="grupo">
								<span class="rotulo">¿Por cuánto tiempo?</span>
								<div class="opciones" role="radiogroup">
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
						)}

						<div class={`previa-pase ${errorFranja ? 'previa-pase--choca' : ''}`}>
							<span class="rotulo">{errorFranja ? 'Fuera de la franja del conjunto' : 'Así queda'}</span>
							<span class="dato">{resumen}</span>
							{(errorFranja || (tipo === 'visita' && !estadia)) && (
								<span class="nota">
									{tipo === 'visita' ? `Las visitas de un día entran de ${horaTexto(L.visitaDesde)} a ${horaTexto(L.visitaHasta)}` : `Los colaboradores entran de ${horaTexto(L.colabDesde)} a ${horaTexto(L.colabHasta)}`}
								</span>
							)}
						</div>
					</div>
				) : (
					<Creado p={creado} enviado={enviado} onEnviar={() => (setEnviado(true), compartir(creado))} onVer={() => onVer(creado)} />
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
			<span class="mono paso__valor">{valor}</span>
			<button onClick={mas} aria-label={`Más: ${rotulo}`}>+</button>
		</div>
	</div>
);

function Creado({p, enviado, onEnviar, onVer}: {p: Pase; enviado: boolean; onEnviar: () => void; onVer: () => void}) {
	useKino(500);
	const e = estado(p);
	const ref = useRef<HTMLDivElement>(null);
	useLayoutEffect(() => {
		animar(ref.current, [{opacity: 0, transform: 'scale(.6) translateY(40px)', filter: 'blur(8px)'}, {opacity: 1, transform: 'none', filter: 'blur(0)'}], {duration: D.tarjeta, easing: C.crecer});
	}, []);
	return (
		<div class="hoja__cuerpo creado">
			<div ref={ref} class="creado__portal">
				<Portal p={p} tam={220} />
			</div>
			<div class="creado__texto">
				<ChipEstado e={e} grande />
				<h2 class="titulo titulo--l">{p.nombre}</h2>
				<p class="dato dato--vigente">{vigenciaTexto(p)}</p>
				<p class="nota">{e === 'sin-confirmar' ? 'Kino lo envió al lector. Queda vigente cuando el lector confirme.' : 'El lector lo confirmó. Ya puede entrar.'}</p>
			</div>
			<div class="creado__acciones">
				<button class={`accion ${enviado ? 'accion--hecho' : ''}`} onClick={onEnviar} disabled={enviado}>
					<Icono n={enviado ? 'check' : 'compartir'} />
					{enviado ? `Enviado a ${p.nombre.split(' ')[0]}` : 'Enviar por WhatsApp'}
				</button>
				<button class="secundario-btn" onClick={onVer}>
					Ver el Pase
				</button>
			</div>
		</div>
	);
}

// Detalle --------------------------------------------------------------------------------------------
function Detalle({id, onVolver}: {id: string; onVolver: () => void}) {
	useKino(1000);
	const p = E.pases.find((x) => x.id === id);
	const [modo, setModo] = useState<ModoVista>('qr');
	const [error, setError] = useState<string | null>(null);
	const ref = useRef<HTMLDivElement>(null);
	useLayoutEffect(() => {
		animar(ref.current, [{opacity: 0, transform: 'translateX(28px)'}, {opacity: 1, transform: 'none'}], {duration: D.crecer, easing: C.crecer});
	}, []);
	if (!p) return null;
	const e = estado(p);
	const v = ventana(p);
	const vivo = e === 'vigente' || e === 'por-vencer' || e === 'previsto' || e === 'sin-confirmar';
	const extensiones: [string, number][] = esEstadia(p) ? [['+1 semana', 168], ['+1 mes', 720]] : [['+1 h', 1], ['+1 día', 24], ['+1 semana', 168]];
	return (
		<div ref={ref} class="detalle">
			<div class="barra-sup">
				<button class="icono-btn" onClick={onVolver} aria-label="Volver">
					<Icono n="atras" />
				</button>
				<span class="titulo titulo--s">{p.tipo === 'colaborador' ? 'Pase · colaborador' : esEstadia(p) ? 'Pase · estadía' : 'Pase · visita'}</span>
				<span class="barra-sup__hueco" />
			</div>
			<div class="pantalla__scroll">
				<div class="detalle__portal">
					<Portal p={p} modo={modo} tam={232} />
					<div class="modos" role="tablist">
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
						<p class={`dato dato--${e}`}>{lineaVigencia(p, e)}</p>
						{(e === 'vigente' || e === 'por-vencer') && (
							<p class="cuenta">
								<span class="rotulo">Vence en</span>
								<span class="mono cuenta__num">{cuentaRegresiva(v.hasta)}</span>
							</p>
						)}
					</div>
					{vivo && p.tipo === 'visita' && (
						<section class="grupo">
							<h2 class="rotulo">Extender</h2>
							<div class={`opciones opciones--${extensiones.length}`}>
								{extensiones.map(([txt, h]) => (
									<button class="opcion" onClick={() => setError(extender(p, h))}>
										{txt}
									</button>
								))}
							</div>
							{error && <p class="nota nota--error">{error}</p>}
						</section>
					)}
					<section class="grupo">
						<h2 class="rotulo">Lo que pasó</h2>
						<ol class="traza">
							{[...p.traza].reverse().map((t) => (
								<li class={`traza__item traza__item--${t.tipo}`}>
									<span class="mono">{fechaCorta(t.hora) === 'hoy' ? hora24(t.hora) : fechaCorta(t.hora)}</span>
									<span>{t.texto}</span>
								</li>
							))}
						</ol>
					</section>
				</div>
			</div>
			{vivo && (
				<div class="pie-accion pie-accion--fijo">
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
	if (!d) return null;
	const queda = Math.max(0, d.hasta - Date.now());
	if (queda <= 0) {
		E.deshacer = undefined;
		return null;
	}
	return (
		<div class="deshacer" role="status">
			<span>Pase revocado. El lector ya no lo acepta.</span>
			<button onClick={deshacerRevocar}>
				<Icono n="deshacer" tam={18} />
				Deshacer · {Math.ceil(queda / 1000)}
			</button>
		</div>
	);
}
