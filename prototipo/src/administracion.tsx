// Administración: fija el marco (límites) y cuida la integración. No aprueba ingresos.
import {useState} from 'preact/hooks';
import {activosDeLaCasa, ahora, anotar, E, emitir, estado, hora24, horaTexto, repararSync, type Limites} from './modelo';
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
				{(
					[
						['resumen', 'Resumen', 'resumen'],
						['limites', 'Límites', 'ajustes'],
						['lector', 'Lector e integración', 'lector'],
					] as const
				).map(([k, t, i]) => (
					<button class={`admin__item ${s === k ? 'activo' : ''}`} onClick={() => setS(k)}>
						<Icono n={i} />
						{t}
					</button>
				))}
				<span class="nota admin__nota">La administración fija límites. Los ingresos los otorga cada residente.</span>
			</aside>
			<main class="admin__principal">
				{s === 'resumen' && <Resumen ir={setS} />}
				{s === 'limites' && <LimitesVista />}
				{s === 'lector' && <Lector />}
			</main>
		</div>
	);
}

function Resumen({ir}: {ir: (s: Seccion) => void}) {
	const est = useKino(1000);
	const hoy = ahora().toDateString();
	const activos = est.pases.filter((p) => ['vigente', 'por-vencer'].includes(estado(p))).length;
	const entradas = est.lecturas.filter((l) => l.resultado === 'entra' && l.hora.toDateString() === hoy).length;
	const rechazos = est.lecturas.filter((l) => l.resultado === 'rechazado' && l.hora.toDateString() === hoy);
	const caida = est.sync.find((x) => x.estado !== 'en-linea');
	return (
		<div class="admin__pagina">
			<h1 class="titulo titulo--xl">Resumen de hoy</h1>
			<p class="secundario">Villas Campestres y Refugio Campestre · {hora24(ahora())}</p>
			{caida && (
				<button class="alerta-sync" onClick={() => ir('lector')}>
					<Icono n="alerta" tam={28} />
					<span>
						<b>{caida.comunidad}: la integración con el lector está caída</b>
						<span>{caida.usuarios[0]} de {caida.usuarios[1]} usuarios y {caida.vehiculos[0]} de {caida.vehiculos[1]} vehículos sincronizados</span>
					</span>
					<span class="enlace">Ver la causa</span>
				</button>
			)}
			<div class="cifras">
				<div class="cifra"><span class="cifra__num">{activos}</span><span class="rotulo">Pases vigentes ahora</span></div>
				<div class="cifra"><span class="cifra__num">{entradas}</span><span class="rotulo">Entradas hoy</span></div>
				<div class="cifra"><span class="cifra__num">{rechazos.length}</span><span class="rotulo">Rechazos hoy</span></div>
				<div class="cifra"><span class="cifra__num">0</span><span class="rotulo">Ingresos que aprobaste</span></div>
			</div>
			<section class="grupo">
				<h2 class="rotulo">Rechazos y su motivo</h2>
				<table>
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
	);
}

function LimitesVista() {
	const est = useKino(2000);
	const [b, setB] = useState<Limites>({...est.limites});
	const [guardado, setGuardado] = useState(false);
	const cambia = (k: keyof Limites, d: number, minV: number, maxV: number) => {
		setGuardado(false);
		setB({...b, [k]: Math.min(maxV, Math.max(minV, b[k] + d))});
		anotar('I-15');
	};
	const activos = activosDeLaCasa();
	const exceso = Math.max(0, activos - b.cupoPorCasa);
	const largos = est.pases.filter((p) => p.tipo === 'visita' && ['vigente', 'por-vencer', 'previsto'].includes(estado(p)) && (p.hechos.hasta.getTime() - p.hechos.desde.getTime()) / 3_600_000 > b.duracionMaxH).length;
	const sucio = JSON.stringify(b) !== JSON.stringify(est.limites);
	return (
		<div class="admin__pagina">
			<h1 class="titulo titulo--xl">Límites del conjunto</h1>
			<p class="secundario">Aplican a los Pases nuevos. Los activos conservan su vigencia.</p>
			<div class="limites-grid">
				<Control rotulo="Visitas activas por casa" valor={`${b.cupoPorCasa}`} menos={() => cambia('cupoPorCasa', -1, 1, 20)} mas={() => cambia('cupoPorCasa', 1, 1, 20)} nota="Cuántos Pases de visita puede tener una casa al mismo tiempo" />
				<Control rotulo="Duración máxima de una visita" valor={`${b.duracionMaxH} h`} menos={() => cambia('duracionMaxH', -1, 1, 24)} mas={() => cambia('duracionMaxH', 1, 1, 24)} nota="Un Pase de visita no puede durar más" />
				<Control rotulo="Las visitas entran desde" valor={horaTexto(b.visitaDesde)} menos={() => cambia('visitaDesde', -60, 0, b.visitaHasta - 60)} mas={() => cambia('visitaDesde', 60, 0, b.visitaHasta - 60)} />
				<Control rotulo="Las visitas entran hasta" valor={horaTexto(b.visitaHasta)} menos={() => cambia('visitaHasta', -60, b.visitaDesde + 60, 1439)} mas={() => cambia('visitaHasta', 60, b.visitaDesde + 60, 1439)} />
				<Control rotulo="Colaboradores desde" valor={horaTexto(b.colabDesde)} menos={() => cambia('colabDesde', -60, 0, b.colabHasta - 60)} mas={() => cambia('colabDesde', 60, 0, b.colabHasta - 60)} />
				<Control rotulo="Colaboradores hasta" valor={horaTexto(b.colabHasta)} menos={() => cambia('colabHasta', -60, b.colabDesde + 60, 1439)} mas={() => cambia('colabHasta', 60, b.colabDesde + 60, 1439)} />
			</div>
			<div class={`previa ${exceso || largos ? 'previa--choca' : ''}`}>
				<b>Qué pasaría con este cambio</b>
				<span>
					{exceso || largos
						? `La Casa 14 tiene ${activos} visitas activas${exceso ? `: quedaría ${exceso} por encima del tope` : ''}${largos ? `; ${largos} Pase dura más que el nuevo máximo` : ''}. No se cortan: conservan su vigencia y el tope aplica al siguiente.`
						: 'Ningún Pase activo queda por fuera del nuevo marco.'}
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
				{guardado && !sucio ? 'Guardado · aplica desde el próximo Pase' : 'Guardar límites'}
			</button>
		</div>
	);
}

const Control = ({rotulo, valor, menos, mas, nota}: {rotulo: string; valor: string; menos: () => void; mas: () => void; nota?: string}) => (
	<div class="control">
		<span class="rotulo">{rotulo}</span>
		<div class="paso__fila">
			<button onClick={menos} aria-label={`Menos: ${rotulo}`}>−</button>
			<span class="mono paso__valor">{valor}</span>
			<button onClick={mas} aria-label={`Más: ${rotulo}`}>+</button>
		</div>
		{nota && <span class="nota">{nota}</span>}
	</div>
);

function Lector() {
	const est = useKino(500);
	return (
		<div class="admin__pagina">
			<h1 class="titulo titulo--xl">Lector e integración</h1>
			<p class="secundario">Kino da de alta cada Pase en HikCentral. Si el alta falla, el lector no lo conoce.</p>
			<div class="sync-grid">
				{est.sync.map((s) => (
					<div class={`sync sync--${s.estado}`}>
						<div class="sync__cabeza">
							<b>{s.comunidad}</b>
							{s.estado === 'en-linea' ? <ChipEstado e="vigente" /> : s.estado === 'reparando' ? <span class="chip chip--sin-confirmar"><span class="chip__punto" />Sincronizando</span> : <ChipEstado e="rechazado" />}
						</div>
						{s.usuarios[1] > 0 ? (
							<>
								<div class="sync__barra"><i style={{transform: `scaleX(${s.usuarios[0] / s.usuarios[1]})`}} /></div>
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
