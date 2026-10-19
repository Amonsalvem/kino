// Portería: el lector decide y portería ve el porqué. Se lee desde 3 m.
// Coreografía de la lectura (decaer, crecer y firme de @kino/motion):
//   leyendo  → el lector parpadea en ámbar y una línea barre la ventana del lector
//   entra    → una ola verde nace del lector y llena el panel; el check se dibuja; el texto sube en cascada de 90 ms;
//              la talanquera sube con resorte firme y baja sola a los 4 s, con la cuenta a la vista
//   no entra → la misma ola en carmín; la X se dibuja; el veredicto niega una vez; la talanquera no se mueve y la luz roja late dos veces
// Con movimiento reducido todo se vuelve fundido (movimiento.ts).
import {useEffect, useLayoutEffect, useRef, useState} from 'preact/hooks';
import {ahora, E, estado, hora24, leer, llamar, vigenciaTexto, type Lectura, type Modo} from './modelo';
import {ChipEstado, Icono, Marca, Sinapsis, useKino} from './componentes';
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

function Panel({estado: ep, leyendo, ultima, pulso, llamada, onLlamar}: {estado: string; leyendo: Llegada | null; ultima: Lectura | null; pulso: number; llamada: string; onLlamar: (id: string) => void}) {
	const panel = useRef<HTMLDivElement>(null);
	const ola = useRef<HTMLSpanElement>(null);
	const brazo = useRef<SVGGElement>(null);
	const luz = useRef<SVGCircleElement>(null);
	const cuenta = useRef<HTMLSpanElement>(null);
	const pase = ultima?.paseId ? E.pases.find((p) => p.id === ultima.paseId) : undefined;
	const entra = ultima?.resultado === 'entra';

	useLayoutEffect(() => {
		if (!ultima || !panel.current) return;
		const el = panel.current;
		// 0 · una lectura nueva corta la anterior: la talanquera parte de donde esté, no de un estado viejo
		const giro = brazo.current ? getComputedStyle(brazo.current).transform : 'none';
		brazo.current?.getAnimations().forEach((a) => a.cancel());
		cuenta.current?.getAnimations().forEach((a) => a.cancel());
		const abierta = giro !== 'none' && giro !== 'matrix(1, 0, 0, 1, 0, 0)';
		// 1 · la ola nace en el lector y llena el panel
		animar(ola.current, [{clipPath: 'circle(0% at 86% 64%)', opacity: 1}, {clipPath: 'circle(150% at 86% 64%)', opacity: 1}], {duration: D.tarjeta, easing: C.crecer, fill: 'both'});
		// 2 · el ícono se dibuja
		el.querySelectorAll<SVGPathElement>('.veredicto__trazo').forEach((p, i) =>
			animar(p, [{strokeDashoffset: 1}, {strokeDashoffset: 0}], {duration: D.crecer, easing: C.crecer, delay: 140 + i * 90, fill: 'both'}),
		);
		// 3 · el texto sube en cascada
		el.querySelectorAll<HTMLElement>('[data-cascada]').forEach((n) => {
			const i = Number(n.dataset.cascada);
			animar(n, [{opacity: 0, transform: 'translateY(18px)'}, {opacity: 1, transform: 'none'}], {duration: D.crecer, easing: C.crecer, delay: 160 + i * 90, fill: 'both'});
		});
		if (entra) {
			// 4a · la talanquera sube con resorte firme, espera y baja con decaer
			animar(brazo.current, [{transform: 'rotate(0deg)'}, {transform: 'rotate(-84deg)'}], {duration: R.firme.ms, easing: R.firme.linear, delay: 220, fill: 'forwards'})?.finished.then(() =>
				animar(brazo.current, [{transform: 'rotate(-84deg)'}, {transform: 'rotate(0deg)'}], {duration: D.decaer, easing: C.decaer, delay: ABIERTA_MS - R.firme.ms, fill: 'forwards'}),
			).catch(() => {});
			animar(cuenta.current, [{transform: 'scaleX(1)'}, {transform: 'scaleX(0)'}], {duration: ABIERTA_MS, easing: 'linear', delay: 220, fill: 'both'});
		} else {
			// 4b · el veredicto niega una vez; la luz roja late dos veces; si quedó abierta por el ingreso anterior, baja
			if (abierta) animar(brazo.current, [{transform: giro}, {transform: 'rotate(0deg)'}], {duration: D.decaer, easing: C.decaer, fill: 'forwards'});
			if (!reducido())
				animar(el.querySelector('.veredicto'), [{transform: 'translateX(0)'}, {transform: 'translateX(-10px)'}, {transform: 'translateX(8px)'}, {transform: 'translateX(-4px)'}, {transform: 'translateX(0)'}], {duration: D.crecer, easing: C.revocar, delay: 560});
			animar(luz.current, [{opacity: 1}, {opacity: 0.25}, {opacity: 1}, {opacity: 0.25}, {opacity: 1}], {duration: D.latir, easing: C.latir, delay: 200});
		}
	}, [ultima?.id]);

	return (
		<section ref={panel} class={`lector lector--${ep}`} aria-live="polite">
			<span ref={ola} class="lector__ola" aria-hidden="true" />
			<div class="lector__contenido">
				{ep === 'reposo' && (
					<div class="lector__texto">
						<span class="rotulo">Lector en línea</span>
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
					</div>
				)}
			</div>
			{ultima && pase && (
				<dl class="lector__datos" key={`d${ultima.id}`} data-cascada="3">
					<div><dt>Casa</dt><dd>{pase.autor.casa}</dd></div>
					<div><dt>Otorgó</dt><dd>{pase.autor.nombre}</dd></div>
					<div><dt>Con</dt><dd class="mono">{ultima.modo === 'qr' ? 'QR' : ultima.modo === 'placa' ? ultima.valor : 'código'}</dd></div>
					<div><dt>Vigencia</dt><dd class="mono">{vigenciaTexto(pase)}</dd></div>
				</dl>
			)}
			<div class="lector__escena">
				<Sinapsis activa={pulso} tono={entra ? 'vigente' : 'rechazado'} />
				<svg class="puerta" viewBox="0 0 240 200" aria-hidden="true">
					<rect class="puerta__piso" x="0" y="168" width="240" height="2" />
					<rect class="puerta__poste" x="22" y="78" width="40" height="92" rx="8" />
					<rect class="puerta__ventana" x="30" y="88" width="24" height="18" rx="4" />
					{ep === 'leyendo' && <rect class="puerta__barrido" x="30" y="88" width="24" height="2" />}
					<circle ref={luz} class="puerta__luz" cx="42" cy="122" r="6" />
					<g ref={brazo} class="puerta__brazo" style={{transformOrigin: '42px 142px', transformBox: 'view-box'}}>
						<rect x="40" y="136" width="196" height="12" rx="6" />
						{[0, 1, 2, 3, 4].map((i) => (
							<rect class="puerta__franja" x={70 + i * 34} y="136" width="16" height="12" />
						))}
					</g>
				</svg>
				<div class="lector__cuenta" hidden={!entra}>
					<span class="rotulo">Se cierra sola</span>
					<span class="lector__cuenta-pista"><span ref={cuenta} /></span>
				</div>
			</div>
		</section>
	);
}
