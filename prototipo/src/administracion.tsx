// Administración: fija las franjas del conjunto y cuida la integración. No aprueba ingresos, no pone tope de visitas
// ni de duración (decisiones.md E3-2): eso lo decide cada residente.
import {useState} from 'preact/hooks';
import {ahora, anotar, E, emitir, esEstadia, estado, hora24, horaBreve, repararSync, vigenciaTexto, type Limites} from './modelo';
import {ChipEstado, Icono, Marca, useKino} from './componentes';

type Seccion = 'resumen' | 'limites' | 'lector';

export function Administracion() {
	const [s, setS] = useState<Seccion>('resumen');
	return (
		<div class="app app--admin">
			<aside class="admin__menu">
				<div class="admin__marca">
					<Marca tam={30} />
					<b>Kino Administración</b>
				</div>
				<nav class="admin__nav">
					{(
						[
							['resumen', 'Resumen', 'resumen'],
							['limites', 'Franjas', 'ajustes'],
							['lector', 'Lector e integración', 'lector'],
						] as const
					).map(([k, t, i]) => (
						<button class={`admin__item ${s === k ? 'activo' : ''}`} onClick={() => setS(k)} aria-current={s === k ? 'page' : undefined}>
							<Icono n={i} />
							{t}
						</button>
					))}
				</nav>
				<p class="nota admin__nota">La administración fija las franjas. Cada residente decide a quién otorga un Pase y por cuánto tiempo.</p>
			</aside>
			<main class="admin__principal">
				{s === 'resumen' && <Resumen ir={setS} />}
				{s === 'limites' && <Franjas />}
				{s === 'lector' && <Lector />}
			</main>
		</div>
	);
}

function Resumen({ir}: {ir: (s: Seccion) => void}) {
	const est = useKino(1000);
	const hoy = ahora().toDateString();
	const vivos = est.pases.filter((p) => ['vigente', 'por-vencer'].includes(estado(p)));
	const entradas = est.lecturas.filter((l) => l.resultado === 'entra' && l.hora.toDateString() === hoy).length;
	const rechazos = est.lecturas.filter((l) => l.resultado === 'rechazado' && l.hora.toDateString() === hoy);
	const caida = est.sync.find((x) => x.estado !== 'en-linea');
	return (
		<div class="admin__pagina">
			<header class="admin__cabeza">
				<h1 class="titulo titulo--xl">Resumen de hoy</h1>
				<p class="secundario">Villas Campestres y Refugio Campestre · {hora24(ahora())}</p>
			</header>
			{caida && (
				<button class="alerta-sync" onClick={() => ir('lector')}>
					<Icono n="alerta" tam={28} />
					<span class="alerta-sync__texto">
						<b>{caida.comunidad}: la integración con el lector está caída</b>
						<span>{caida.usuarios[0]} de {caida.usuarios[1]} usuarios y {caida.vehiculos[0]} de {caida.vehiculos[1]} vehículos sincronizados</span>
					</span>
					<span class="enlace">Ver la causa</span>
				</button>
			)}
			<div class="cifras">
				<div class="cifra"><span class="cifra__num">{vivos.length}</span><span class="rotulo">Pases vigentes</span></div>
				<div class="cifra"><span class="cifra__num">{vivos.filter(esEstadia).length}</span><span class="rotulo">Estadías</span></div>
				<div class="cifra"><span class="cifra__num">{entradas}</span><span class="rotulo">Entradas hoy</span></div>
				<div class="cifra"><span class="cifra__num">{rechazos.length}</span><span class="rotulo">Rechazos hoy</span></div>
			</div>
			<div class="admin__columnas">
				<section class="grupo">
					<h2 class="rotulo">Pases vigentes ahora</h2>
					<table class="tabla tabla--admin">
						<colgroup><col style={{width: '34%'}} /><col style={{width: '16%'}} /><col /></colgroup>
						<thead><tr><th>Quién</th><th>Casa</th><th>Vigencia</th></tr></thead>
						<tbody>
							{vivos.map((p) => (
								<tr>
									<td>{p.nombre}</td>
									<td>{p.autor.casa}</td>
									<td class="mono">{vigenciaTexto(p)}</td>
								</tr>
							))}
						</tbody>
					</table>
				</section>
				<section class="grupo">
					<h2 class="rotulo">Rechazos y su motivo</h2>
					<table class="tabla tabla--admin">
						<colgroup><col style={{width: '18%'}} /><col style={{width: '34%'}} /><col /></colgroup>
						<thead><tr><th>Hora</th><th>Quién</th><th>Motivo</th></tr></thead>
						<tbody>
							{rechazos.map((l) => (
								<tr>
									<td class="mono">{hora24(l.hora)}</td>
									<td>{l.nombre}</td>
									<td>{l.motivo}</td>
								</tr>
							))}
						</tbody>
					</table>
				</section>
			</div>
		</div>
	);
}

type Clave = 'visitaDesde' | 'visitaHasta' | 'colabDesde' | 'colabHasta';

function Franjas() {
	const est = useKino(2000);
	const [b, setB] = useState<Limites>({...est.limites});
	const [guardado, setGuardado] = useState(false);
	const cambia = (k: Clave, d: number, minV: number, maxV: number) => {
		setGuardado(false);
		setB({...b, [k]: Math.min(maxV, Math.max(minV, b[k] + d))});
		anotar('I-15');
	};
	// Pases de un día que quedarían fuera de la franja nueva (no se cortan: conservan su vigencia).
	const fuera = est.pases.filter((p) => {
		if (!['vigente', 'por-vencer', 'previsto'].includes(estado(p)) || esEstadia(p)) return false;
		const ini = p.recurrencia ? p.recurrencia.inicio : p.hechos.desde.getHours() * 60 + p.hechos.desde.getMinutes();
		const fin = p.recurrencia ? p.recurrencia.fin : p.hechos.hasta.getHours() * 60 + p.hechos.hasta.getMinutes();
		const [d, h] = p.tipo === 'colaborador' ? [b.colabDesde, b.colabHasta] : [b.visitaDesde, b.visitaHasta];
		return ini < d || fin > h;
	});
	const sucio = JSON.stringify(b) !== JSON.stringify(est.limites);
	const Franja = ({titulo, nota, desde, hasta}: {titulo: string; nota: string; desde: Clave; hasta: Clave}) => (
		<section class="grupo franja">
			<header class="franja__cabeza">
				<h2 class="titulo titulo--m">{titulo}</h2>
				<p class="nota">{nota}</p>
			</header>
			<div class="franja__controles">
				<Control rotulo="Desde" valor={horaBreve(dia(b[desde]))} menos={() => cambia(desde, -60, 0, b[hasta] - 60)} mas={() => cambia(desde, 60, 0, b[hasta] - 60)} />
				<Control rotulo="Hasta" valor={horaBreve(dia(b[hasta]))} menos={() => cambia(hasta, -60, b[desde] + 60, 1439)} mas={() => cambia(hasta, 60, b[desde] + 60, 1439)} />
			</div>
		</section>
	);
	return (
		<div class="admin__pagina">
			<header class="admin__cabeza">
				<h1 class="titulo titulo--xl">Franjas del conjunto</h1>
				<p class="secundario">Aplican a los Pases nuevos. Los activos conservan su vigencia.</p>
			</header>
			<div class="franjas">
				<Franja titulo="Visitas de un día" nota="Las estadías entran y salen a cualquier hora." desde="visitaDesde" hasta="visitaHasta" />
				<Franja titulo="Colaboradores" nota="Empleada, jardinero, técnicos recurrentes." desde="colabDesde" hasta="colabHasta" />
			</div>
			<div class="admin__guardar">
				<div class={`previa ${fuera.length ? 'previa--choca' : ''}`}>
					<b>Qué pasaría con este cambio</b>
					<span>
						{fuera.length
							? `${fuera.map((p) => p.nombre).join(', ')} ${fuera.length === 1 ? 'queda' : 'quedan'} fuera de la franja nueva. No se cortan: conservan su vigencia.`
							: 'Ningún Pase activo queda fuera de la franja nueva.'}
					</span>
				</div>
				<button
					class="accion accion--secundaria-fuerte"
					disabled={!sucio}
					onClick={() => {
						E.limites = {...b};
						emitir();
						setGuardado(true);
						anotar('I-15');
					}}
				>
					{guardado && !sucio ? 'Guardado' : 'Guardar franjas'}
				</button>
			</div>
			<p class="nota">Sin tope de visitas por casa ni de duración: lo decide el residente.</p>
		</div>
	);
}

const dia = (minutos: number) => {
	const d = new Date(ahora());
	d.setHours(0, minutos, 0, 0);
	return d;
};

const Control = ({rotulo, valor, menos, mas}: {rotulo: string; valor: string; menos: () => void; mas: () => void}) => (
	<div class="control">
		<span class="rotulo">{rotulo}</span>
		<div class="paso__fila">
			<button onClick={menos} aria-label={`Menos: ${rotulo}`}>−</button>
			<span class="mono paso__valor">{valor}</span>
			<button onClick={mas} aria-label={`Más: ${rotulo}`}>+</button>
		</div>
	</div>
);

/** Red de Physarum (Tero y otros, 2010): el tubo se engrosa con el flujo y se seca sin él.
 *  Cada tubo es una proporción sincronizada real; nada se mueve si los contadores no cambian. */
function Red({usuarios, vehiculos}: {usuarios: [number, number]; vehiculos: [number, number]}) {
	const tubo = ([n, de]: [number, number], y: number, rotulo: string) => {
		const f = de ? n / de : 0;
		const seco = f < 0.05;
		return (
			<g class={`red__tubo ${seco ? 'red__tubo--seco' : f < 0.95 ? 'red__tubo--parcial' : ''}`}>
				<path d={`M48 48C100 48 108 ${y} 162 ${y}S226 48 276 48`} style={{strokeWidth: seco ? 1.6 : 2 + f * 9}} />
				<text x="162" y={y + (y < 48 ? -12 : 24)} text-anchor="middle">{`${rotulo} · ${n} de ${de}`}</text>
			</g>
		);
	};
	return (
		<svg class="red" viewBox="0 0 332 104" role="img" aria-label={`Kino a HikCentral: ${usuarios[0]} de ${usuarios[1]} personas y ${vehiculos[0]} de ${vehiculos[1]} vehículos sincronizados`}>
			{tubo(usuarios, 26, 'Personas')}
			{tubo(vehiculos, 70, 'Vehículos')}
			<circle class="red__nodo" cx="26" cy="48" r="22" />
			<text class="red__rotulo" x="26" y="52" text-anchor="middle">Kino</text>
			<rect class="red__nodo" x="276" y="30" width="52" height="36" rx="8" />
			<text class="red__rotulo red__rotulo--tenue" x="302" y="84" text-anchor="middle">HikCentral</text>
		</svg>
	);
}

function Lector() {
	const est = useKino(500);
	return (
		<div class="admin__pagina">
			<header class="admin__cabeza">
				<h1 class="titulo titulo--xl">Lector e integración</h1>
				<p class="secundario">Kino da de alta cada Pase en HikCentral. Si el alta falla, el lector no lo conoce.</p>
			</header>
			<div class="sync-grid">
				{est.sync.map((s) => (
					<div class={`sync sync--${s.estado}`}>
						<div class="sync__cabeza">
							<b>{s.comunidad}</b>
							{s.estado === 'en-linea' ? <ChipEstado e="vigente" /> : s.estado === 'reparando' ? <span class="chip chip--sin-confirmar"><span class="chip__punto" />Sincronizando</span> : <ChipEstado e="rechazado" />}
						</div>
						{s.usuarios[1] > 0 ? (
							<>
								<Red usuarios={s.usuarios} vehiculos={s.vehiculos} />
								<dl class="datos">
									<div><dt>Usuarios en el lector</dt><dd class="mono">{s.usuarios[0]} de {s.usuarios[1]}</dd></div>
									<div><dt>Vehículos en el lector</dt><dd class="mono">{s.vehiculos[0]} de {s.vehiculos[1]}</dd></div>
									<div><dt>Errores de alta</dt><dd class="mono">{s.errores}</dd></div>
								</dl>
							</>
						) : (
							<p class="nota">Cada Pase nuevo se confirma en segundos.</p>
						)}
						{s.estado !== 'en-linea' && (
							<>
								<p class="causa"><b>Causa:</b> {s.causa}. El correo es obligatorio en el alta y la mayoría de residentes no lo tiene.</p>
								<button class="accion" disabled={s.estado === 'reparando'} onClick={() => repararSync(s.comunidad)}>
									<Icono n="sincronizar" />
									{s.estado === 'reparando' ? 'Sincronizando…' : 'Reintentar con teléfono en lugar de correo'}
								</button>
							</>
						)}
						{s.estado === 'en-linea' && s.causa && <p class="nota">{s.causa}</p>}
					</div>
				))}
			</div>
		</div>
	);
}
