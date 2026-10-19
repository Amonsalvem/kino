// App del residente: ingreso por WhatsApp, Pases vivos, crear, compartir, detalle, extender y revocar.
import {useEffect, useLayoutEffect, useMemo, useRef, useState} from 'preact/hooks';
import {
	activosDeLaCasa, ahora, anotar, compartir, crearPase, cuentaRegresiva, deshacerRevocar, diasTexto, E, emitir, estado, extender, hora24, horaCorta, horaTexto,
	min, RECIENTES, RESIDENTE, revocar, validar, ventana, vigenciaTexto, type Modo, type Pase, type Tipo,
} from './modelo';
import {BotonMantener, ChipEstado, Icono, Iniciales, lineaVigencia, Marca, Micelio, Portal, TarjetaPase, useKino, type ModoVista} from './componentes';
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
			<Micelio clase="micelio--ingreso" densidad={38} />
			<div class="ingreso__marca">
				<Marca tam={56} />
				<span class="ingreso__logotipo">KINO</span>
			</div>
			{paso === 'numero' && (
				<div class="ingreso__cuerpo entra">
					<h1 class="titulo">Entra con tu WhatsApp</h1>
					<p class="secundario">Te enviamos un código. Sin contraseña.</p>
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
function Inicio({tab, onTab, onAbrir, onCrear}: {tab: 'pases' | 'avisos' | 'casa'; onTab: (t: 'pases' | 'avisos' | 'casa') => void; onAbrir: (p: Pase) => void; onCrear: (pre?: (typeof RECIENTES)[number]) => void}) {
	const est = useKino(1000);
	const t = ahora();
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
	}, [est.pases.length, Math.floor(t.getTime() / 15000), est.pases.map((p) => estado(p, t)).join()]);
	const [verAnt, setVerAnt] = useState(false);
	const usados = activosDeLaCasa();
	const cupo = est.limites.cupoPorCasa;

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
							<div class="cupo" aria-label={`${usados} de ${cupo} Pases de visita activos`} onClick={() => anotar('I-05')}>
								<span class="celulas">
									{Array.from({length: cupo}, (_, i) => (
										<i class={i < usados ? 'llena' : ''} style={{animationDelay: `${i * 90}ms`}} />
									))}
								</span>
								<span class="secundario">
									<b>{usados} de {cupo}</b> visitas activas · tope de la administración
								</span>
							</div>
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
								<button class="enlace" onClick={() => setVerAnt(!verAnt)}>
									{verAnt ? 'Ocultar' : 'Ver'} Pases anteriores ({grupos.anteriores.length})
								</button>
								{verAnt && <div class="lista">{grupos.anteriores.map((p, i) => <TarjetaPase key={p.id} p={p} retraso={i * 55} onAbrir={onAbrir} />)}</div>}
							</section>
						)}
						<div style={{height: 150}} />
					</>
				)}
				{tab === 'avisos' && <Avisos onAbrir={onAbrir} />}
				{tab === 'casa' && <MiCasa />}
			</div>
			{tab === 'pases' && (
				<div class="pie-accion">
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
						{k === 'avisos' && E.avisos.filter((a) => a.para === 'residente').length > 0 && <i class="punto-aviso" />}
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
				<div class="vacio">
					<p class="secundario">Aquí llega cada vez que el lector deja entrar a alguien con tu Pase, o lo rechaza y por qué.</p>
					<p class="nota">Prueba: ve a Portería y lee el QR de Andrés.</p>
				</div>
			)}
			<div class="lista">
				{lista.map((a) => {
					const p = est.pases.find((x) => x.id === a.paseId);
					return (
						<button class={`fila-aviso fila-aviso--${a.tono}`} onClick={() => p && onAbrir(p)}>
							<span class="mono tenue">{hora24(a.hora)}</span>
							<span>
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
			<h1 class="titulo titulo--xl">Mi casa</h1>
			<p class="secundario">{RESIDENTE.casa} · {RESIDENTE.comunidad}</p>
			<section class="grupo">
				<h2 class="rotulo">Límites del conjunto</h2>
				<p class="nota">Los fija la administración. Tú decides quién entra dentro de este marco.</p>
				<dl class="datos">
					<div><dt>Visitas activas por casa</dt><dd class="mono">{L.cupoPorCasa}</dd></div>
					<div><dt>Duración máxima de una visita</dt><dd class="mono">{L.duracionMaxH} h</dd></div>
					<div><dt>Franja de visitas</dt><dd class="mono">{horaTexto(L.visitaDesde)} – {horaTexto(L.visitaHasta)}</dd></div>
					<div><dt>Franja de colaboradores</dt><dd class="mono">{horaTexto(L.colabDesde)} – {horaTexto(L.colabHasta)}</dd></div>
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

// Hoja: crear Pase -----------------------------------------------------------------------------------
type Cuando = 'ahora' | 'tarde' | 'manana' | 'personal';

function HojaCrear({precarga, onCerrar, onVer}: {precarga?: (typeof RECIENTES)[number]; onCerrar: () => void; onVer: (p: Pase) => void}) {
	useKino(1000);
	const t0 = ahora();
	const [tipo, setTipo] = useState<Tipo>(precarga?.tipo ?? 'visita');
	const [nombre, setNombre] = useState(precarga?.nombre ?? '');
	const [tel, setTel] = useState(precarga?.telefono ?? '');
	const [placa, setPlaca] = useState(precarga?.placa ?? '');
	const [motivo] = useState(precarga?.motivo);
	const [cuando, setCuando] = useState<Cuando>('ahora');
	const [desdeH, setDesdeH] = useState(Math.min(21, t0.getHours() + 1));
	const [durH, setDurH] = useState(3);
	const [dias, setDias] = useState<number[]>([1, 2, 3, 4, 5]);
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

	// Gesto: arrastrar la hoja.
	const bajar = (e: PointerEvent) => {
		arrastre.current = {y0: e.clientY, dy: 0, t0: performance.now()};
		(e.currentTarget as HTMLElement).setPointerCapture(e.pointerId);
	};
	const mover = (e: PointerEvent) => {
		const a = arrastre.current;
		if (!a) return;
		const escala = hojaRef.current!.getBoundingClientRect().height / hojaRef.current!.offsetHeight || 1;
		a.dy = Math.max(-20, (e.clientY - a.y0) / escala);
		const dy = a.dy < 0 ? a.dy * 0.3 : a.dy;
		hojaRef.current!.style.transform = `translateY(${dy}px)`;
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
		if (cuando === 'ahora') {
			d.setSeconds(0, 0);
			return {desde: d, hasta: new Date(d.getTime() + durH * 3_600_000)};
		}
		if (cuando === 'tarde') {
			d.setHours(14, 0, 0, 0);
			const h = new Date(d);
			h.setHours(18);
			return {desde: d, hasta: h};
		}
		if (cuando === 'manana') d.setDate(d.getDate() + 1);
		d.setHours(desdeH, 0, 0, 0);
		return {desde: d, hasta: new Date(d.getTime() + durH * 3_600_000)};
	};
	const r = tipo === 'visita' ? rango() : (() => {
		const d = new Date(t0);
		d.setHours(franja[0], 0, 0, 0);
		const h = new Date(t0);
		h.setHours(franja[1], 0, 0, 0);
		return {desde: d, hasta: h};
	})();
	const recurrencia = tipo === 'colaborador' ? {dias, inicio: min(franja[0]), fin: min(franja[1])} : undefined;
	const errorLimite = validar({tipo, desde: r.desde, hasta: r.hasta, recurrencia});
	const telOk = tel.replace(/\D/g, '').length === 10;
	const motivoBoton = errorLimite?.includes('tope') ? errorLimite : !nombre.trim() ? 'Escribe quién viene' : !telOk ? 'Falta el WhatsApp (10 cifras)' : tipo === 'colaborador' && dias.length === 0 ? 'Elige al menos un día' : errorLimite;
	const L = E.limites;

	useEffect(() => {
		if (errorLimite) anotar('I-05');
	}, [errorLimite]);

	const crear = (ev: MouseEvent) => {
		if (motivoBoton) return;
		const modos: Modo[] = ['qr', 'codigo', ...(placa.trim() ? (['placa'] as Modo[]) : [])];
		const btn = ev.currentTarget as HTMLElement;
		animar(btn, [{transform: 'scale(1)'}, {transform: 'scale(.94)'}, {transform: 'scale(1)'}], {duration: R.tacto.ms, easing: R.tacto.linear});
		vibrar(15);
		const p = crearPase({tipo, nombre, telefono: tel, motivo, placa, modos, desde: r.desde, hasta: r.hasta, recurrencia});
		setCreado(p);
		anotar('I-06');
	};

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
								<span class="rotulo">¿Cuándo?</span>
								<div class="chips">
									{(
										[
											['ahora', 'Ya'],
											['tarde', 'Esta tarde'],
											['manana', 'Mañana'],
											['personal', 'Otra hora'],
										] as [Cuando, string][]
									).map(([k, txt]) => (
										<button class={`chip-opcion ${cuando === k ? 'activo' : ''}`} onClick={() => setCuando(k)}>
											{txt}
										</button>
									))}
								</div>
								{(cuando === 'ahora' || cuando === 'personal' || cuando === 'manana') && (
									<div class="pasos">
										{cuando !== 'ahora' && <Paso rotulo="Desde" valor={horaCorta(r.desde)} menos={() => setDesdeH(Math.max(0, desdeH - 1))} mas={() => setDesdeH(Math.min(23, desdeH + 1))} />}
										<Paso rotulo="Dura" valor={`${durH} h`} menos={() => setDurH(Math.max(1, durH - 1))} mas={() => setDurH(durH + 1)} />
									</div>
								)}
								<p class={`vigencia-previa dato ${errorLimite ? 'dato--rechazado' : 'dato--vigente'}`}>{`${r.desde.toDateString() === t0.toDateString() ? 'Hoy' : 'Mañana'} · ${horaCorta(r.desde)} a ${horaCorta(r.hasta)}`}</p>
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
										<button class={dias.includes(i) ? 'activo' : ''} aria-pressed={dias.includes(i)} onClick={() => setDias(dias.includes(i) ? dias.filter((x) => x !== i) : [...dias, i])}>
											{l}
										</button>
									))}
								</div>
								<div class="pasos">
									<Paso rotulo="Entra" valor={horaTexto(franja[0] * 60)} menos={() => setFranja([Math.max(0, franja[0] - 1), franja[1]])} mas={() => setFranja([Math.min(franja[1] - 1, franja[0] + 1), franja[1]])} />
									<Paso rotulo="Sale" valor={horaTexto(franja[1] * 60)} menos={() => setFranja([franja[0], Math.max(franja[0] + 1, franja[1] - 1)])} mas={() => setFranja([franja[0], Math.min(23, franja[1] + 1)])} />
								</div>
								<p class={`vigencia-previa dato ${errorLimite ? 'dato--rechazado' : 'dato--vigente'}`}>{diasTexto(dias) || 'Sin días'} · se repite hasta que lo revoques</p>
							</div>
						)}

						<div class={`limites ${errorLimite ? 'limites--choca' : ''}`}>
							<Icono n="ajustes" tam={18} />
							<span>
								{tipo === 'visita'
									? `${activosDeLaCasa()} de ${L.cupoPorCasa} visitas activas · hasta ${L.duracionMaxH} h · de ${horaTexto(L.visitaDesde)} a ${horaTexto(L.visitaHasta)}`
									: `Colaboradores de ${horaTexto(L.colabDesde)} a ${horaTexto(L.colabHasta)}`}
							</span>
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
			<button onClick={menos} aria-label={`Menos ${rotulo}`}>−</button>
			<span class="mono paso__valor">{valor}</span>
			<button onClick={mas} aria-label={`Más ${rotulo}`}>+</button>
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
				<Portal p={p} tam={230} />
			</div>
			<ChipEstado e={e} grande />
			<h2 class="titulo titulo--l">{p.nombre}</h2>
			<p class="dato dato--vigente">{vigenciaTexto(p)}</p>
			<p class="nota">{e === 'sin-confirmar' ? 'Kino lo envió al lector. Queda vigente cuando el lector confirme.' : 'El lector lo confirmó. Ya puede entrar.'}</p>
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
	return (
		<div ref={ref} class="detalle">
			<div class="pantalla__scroll">
				<div class="barra-sup">
					<button class="icono-btn" onClick={onVolver} aria-label="Volver">
						<Icono n="atras" />
					</button>
					<span class="titulo titulo--s">Pase · {p.tipo === 'visita' ? 'visita' : 'colaborador'}</span>
					<span style={{width: 44}} />
				</div>
				<div class="detalle__portal">
					<Portal p={p} modo={modo} tam={250} />
					<div class="modos" role="tablist">
						{p.modos.map((m) => (
							<button role="tab" aria-selected={modo === m} class={modo === m ? 'activo' : ''} onClick={() => setModo(m)}>
								<Icono n={m} tam={18} />
								{m === 'qr' ? 'QR' : m === 'placa' ? 'Placa' : 'Código'}
							</button>
						))}
					</div>
				</div>
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
				<section class="grupo">
					<h2 class="rotulo">Lo que pasó</h2>
					<ol class="traza">
						{[...p.traza].reverse().map((t) => (
							<li class={`traza__item traza__item--${t.tipo}`}>
								<span class="mono">{hora24(t.hora)}</span>
								<span>{t.texto}</span>
							</li>
						))}
					</ol>
				</section>
				{vivo && p.tipo === 'visita' && (
					<section class="grupo">
						<h2 class="rotulo">Extender</h2>
						<div class="chips">
							{[1, 2].map((h) => (
								<button class="chip-opcion" onClick={() => setError(extender(p, h))}>
									+{h} h
								</button>
							))}
						</div>
						{error && <p class="nota nota--error">{error}</p>}
					</section>
				)}
				<div style={{height: 120}} />
			</div>
			{vivo && (
				<div class="pie-accion">
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
