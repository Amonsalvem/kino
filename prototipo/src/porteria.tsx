// Portería: el lector decide y portería ve el porqué. Se lee desde 3 m.
import {useEffect, useRef, useState} from 'preact/hooks';
import {ahora, E, estado, hora24, horaCorta, leer, llamar, vigenciaTexto, type Lectura, type Modo, type Pase} from './modelo';
import {ChipEstado, Icono, Marca, Sinapsis, useKino} from './componentes';
import {animar, C, D, vibrar} from './movimiento';

type Llegada = {etiqueta: string; modo: Modo; valor: string; quien: string};

export function Porteria() {
	const est = useKino(1000);
	const [ultima, setUltima] = useState<Lectura | null>(null);
	const [leyendo, setLeyendo] = useState<Llegada | null>(null);
	const [pulso, setPulso] = useState(0);
	const [llamada, setLlamada] = useState<'no' | 'llamando' | 'contesto'>('no');
	const [teclado, setTeclado] = useState<'' | 'codigo' | 'placa'>('');
	const [entrada, setEntrada] = useState('');
	const talanquera = useRef<SVGGElement>(null);

	const hoy = ahora().toDateString();
	const esperados = est.pases.filter((p) => {
		const e = estado(p);
		return ['vigente', 'por-vencer', 'previsto', 'sin-confirmar'].includes(e) || (p.entradas.some((x) => x.toDateString() === hoy));
	});
	const vencidos = est.pases.filter((p) => ['vencido', 'revocado'].includes(estado(p)));

	const llegadas: Llegada[] = [
		...esperados.flatMap((p) => p.modos.map((m) => ({etiqueta: m === 'qr' ? 'QR' : m === 'placa' ? p.placa! : `Código ${p.codigo}`, modo: m, valor: m === 'qr' ? p.id : m === 'placa' ? p.placa! : p.codigo, quien: p.nombre}))),
		...vencidos.slice(0, 2).map((p) => ({etiqueta: 'QR', modo: 'qr' as Modo, valor: p.id, quien: p.nombre})),
		{etiqueta: 'XYZ 999', modo: 'placa', valor: 'XYZ 999', quien: 'Carro sin Pase'},
	];

	const simular = (l: Llegada) => {
		setLeyendo(l);
		setLlamada('no');
		setTimeout(() => {
			const r = leer(l.modo, l.valor);
			setLeyendo(null);
			setUltima(r);
			setPulso((n) => n + 1);
			vibrar(r.resultado === 'entra' ? 30 : [30, 80, 30]);
			if (r.resultado === 'entra' && talanquera.current) {
				animar(talanquera.current, [{transform: 'rotate(0deg)'}, {transform: 'rotate(-78deg)', offset: 0.25}, {transform: 'rotate(-78deg)', offset: 0.8}, {transform: 'rotate(0deg)'}], {duration: 4200, easing: C.crecer});
			}
		}, 900);
	};

	useEffect(() => {
		if (llamada !== 'llamando') return;
		const t = setTimeout(() => setLlamada('contesto'), 2600);
		return () => clearTimeout(t);
	}, [llamada]);

	const pase = ultima?.paseId ? est.pases.find((p) => p.id === ultima.paseId) : undefined;
	const resultadoRef = useRef<HTMLDivElement>(null);
	useEffect(() => {
		if (ultima) animar(resultadoRef.current, [{opacity: 0, transform: 'scale(.96)'}, {opacity: 1, transform: 'none'}], {duration: D.crecer, easing: C.crecer});
	}, [ultima?.id]);

	const enviarTeclado = () => {
		if (!entrada.trim() || !teclado) return;
		simular({etiqueta: entrada, modo: teclado, valor: entrada, quien: teclado === 'codigo' ? 'Código digitado' : 'Placa digitada'});
		setEntrada('');
		setTeclado('');
	};

	return (
		<div class="app app--porteria">
			<header class="porteria__cabeza">
				<Marca tam={30} />
				<b>Kino Portería</b>
				<span class="tenue">Villas Campestres · Portería principal</span>
				<span class="mono porteria__hora">{hora24(ahora())}</span>
			</header>
			<div class="porteria__cuerpo">
				<section class="lector">
					<div ref={resultadoRef} class={`lector__resultado ${leyendo ? 'lector__resultado--leyendo' : ultima ? `lector__resultado--${ultima.resultado}` : ''}`} aria-live="polite">
						<Sinapsis activa={pulso} tono={ultima?.resultado === 'rechazado' ? 'rechazado' : 'vigente'} />
						{leyendo ? (
							<div class="lector__leyendo">
								<span class="escaner" aria-hidden="true" />
								<span class="rotulo">El lector está leyendo · {leyendo.modo === 'qr' ? 'QR' : leyendo.modo === 'placa' ? 'placa' : 'código'}</span>
								<span class="lector__titulo">{leyendo.etiqueta}</span>
							</div>
						) : ultima ? (
							<div class="lector__lectura">
								<span class="lector__veredicto">
									<Icono n={ultima.resultado === 'entra' ? 'check' : 'alerta'} tam={44} />
									{ultima.resultado === 'entra' ? 'Puede entrar' : 'No entra con este Pase'}
								</span>
								<span class="lector__titulo">{ultima.nombre}</span>
								{ultima.motivo && <span class="lector__motivo">{ultima.motivo}</span>}
								{pase && (
									<dl class="lector__datos">
										<div><dt>Casa</dt><dd>{pase.autor.casa}</dd></div>
										<div><dt>Otorgó</dt><dd>{pase.autor.nombre}</dd></div>
										<div><dt>Vigencia</dt><dd class="mono">{vigenciaTexto(pase)}</dd></div>
										<div><dt>Entró con</dt><dd class="mono">{ultima.modo === 'qr' ? 'QR' : ultima.modo === 'placa' ? ultima.valor : 'código'}</dd></div>
									</dl>
								)}
								{ultima.resultado === 'rechazado' && pase && (
									<div class="lector__llamar">
										{llamada === 'no' && (
											<button class="secundario-btn" onClick={() => (setLlamada('llamando'), llamar(pase))}>
												<Icono n="telefono" />
												Llamar a {pase.autor.nombre.split(' ')[0]}
											</button>
										)}
										{llamada === 'llamando' && <span class="llamando">Llamando a {pase.autor.nombre}…</span>}
										{llamada === 'contesto' && <span class="nota">{pase.autor.nombre.split(' ')[0]} contestó. Si quiere que entre, extiende el Pase desde su app y se vuelve a leer.</span>}
										<span class="nota">La llamada no abre la entrada.</span>
									</div>
								)}
							</div>
						) : (
							<div class="lector__reposo">
								<span class="rotulo">Lector en línea</span>
								<span class="lector__titulo">Esperando llegada</span>
								<span class="nota">El lector permite el ingreso. Aquí se ve por qué.</span>
							</div>
						)}
					</div>
					<Talanquera grupo={talanquera} abierta={ultima?.resultado === 'entra'} />
				</section>
				<aside class="porteria__lateral">
					<h2 class="rotulo">Simular una llegada</h2>
					<div class="llegadas">
						{llegadas.slice(0, 9).map((l) => (
							<button class="llegada" onClick={() => simular(l)} disabled={!!leyendo}>
								<Icono n={l.modo} tam={18} />
								<span>
									<b>{l.quien}</b>
									<span class="mono tenue">{l.etiqueta}</span>
								</span>
							</button>
						))}
					</div>
					<div class="chips">
						<button class={`chip-opcion ${teclado === 'codigo' ? 'activo' : ''}`} onClick={() => setTeclado(teclado === 'codigo' ? '' : 'codigo')}>Digitar código</button>
						<button class={`chip-opcion ${teclado === 'placa' ? 'activo' : ''}`} onClick={() => setTeclado(teclado === 'placa' ? '' : 'placa')}>Digitar placa</button>
					</div>
					{teclado && (
						<form class="teclado" onSubmit={(e) => (e.preventDefault(), enviarTeclado())}>
							<input class="mono mayus" autoFocus value={entrada} placeholder={teclado === 'codigo' ? '4817' : 'KMN 305'} onInput={(e) => setEntrada((e.target as HTMLInputElement).value)} aria-label={teclado === 'codigo' ? 'Código' : 'Placa'} />
							<button class="accion">Leer</button>
						</form>
					)}
				</aside>
			</div>
			<section class="bitacora">
				<h2 class="rotulo">Hoy en la entrada</h2>
				<table>
					<thead>
						<tr><th>Hora</th><th>Quién</th><th>Con</th><th>Resultado</th><th>Motivo</th><th>Otorgó</th></tr>
					</thead>
					<tbody>
						{est.lecturas.slice(0, 5).map((l) => (
							<tr class={l.id === ultima?.id ? 'nueva' : ''}>
								<td class="mono">{hora24(l.hora)}</td>
								<td>{l.nombre}</td>
								<td class="mono">{l.modo === 'qr' ? 'QR' : l.modo === 'placa' ? l.valor : 'código'}</td>
								<td>{l.resultado === 'entra' ? <ChipEstado e="vigente" /> : <ChipEstado e="rechazado" />}</td>
								<td>{l.motivo ?? 'Entró'}</td>
								<td>{l.autor ?? '—'}</td>
							</tr>
						))}
					</tbody>
				</table>
			</section>
		</div>
	);
}

function Talanquera({grupo, abierta}: {grupo: preact.RefObject<SVGGElement>; abierta?: boolean}) {
	return (
		<svg class={`talanquera ${abierta ? 'talanquera--abierta' : ''}`} viewBox="0 0 320 120" aria-hidden="true">
			<rect x="20" y="40" width="34" height="70" rx="6" class="talanquera__poste" />
			<circle cx="37" cy="56" r="6" class="talanquera__luz" />
			<g ref={grupo} style={{transformOrigin: '37px 70px', transformBox: 'view-box'}}>
				<rect x="37" y="64" width="270" height="12" rx="6" class="talanquera__brazo" />
				{[0, 1, 2, 3, 4, 5].map((i) => (
					<rect x={70 + i * 40} y="64" width="18" height="12" class="talanquera__franja" />
				))}
			</g>
		</svg>
	);
}

export type {Pase};
