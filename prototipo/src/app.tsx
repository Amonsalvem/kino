// Escenario del prototipo: elige actor (o todos a la vez), controla el reloj y muestra cada interacción con su regla.
import {render} from 'preact';
import {useEffect, useLayoutEffect, useRef, useState} from 'preact/hooks';
import {adelantar, ahora, cambiarVelocidad, E, hora24, INTERACCIONES, reiniciar, velocidadActual, type Actor} from './modelo';
import {Escala, Marca, Micelio, Telefono, useIndicador, useKino, usePresencia} from './componentes';
import {Residente} from './residente';
import {Visita} from './visita';
import {Porteria} from './porteria';
import {Administracion} from './administracion';
import {animar, C, D, variablesCss} from './movimiento';

type Vista = Actor | 'todos';
const q = new URLSearchParams(location.search);
const leerLocal = (k: string) => {
	try {
		return localStorage.getItem(k);
	} catch {
		return null;
	}
};
const guardarLocal = (k: string, v: string) => {
	try {
		localStorage.setItem(k, v);
	} catch {
		/* sin almacenamiento */
	}
};

const ACTORES: {k: Vista; t: string; d: string}[] = [
	{k: 'todos', t: 'Todos a la vez', d: 'Lo que hace uno le cambia la pantalla a otro'},
	{k: 'residente', t: 'Residente', d: 'Otorga y revoca'},
	{k: 'visita', t: 'Visita', d: 'Sin cuenta'},
	{k: 'porteria', t: 'Portería', d: 'El lector decide'},
	{k: 'administracion', t: 'Administración', d: 'Fija las franjas'},
];

function Escenario() {
	const est = useKino(1000);
	const [vista, setVista] = useState<Vista>((q.get('actor') as Vista) || (leerLocal('kino-proto-vista') as Vista) || 'todos');
	const [bio, setBio] = useState(q.get('tema') ? q.get('tema') === 'bio' : leerLocal('kino-proto-bio') !== '0');
	const [panel, setPanel] = useState(q.get('panel') !== '0');
	const solo = q.get('solo') === '1';

	useEffect(() => {
		document.documentElement.dataset.bio = bio ? '1' : '0';
		guardarLocal('kino-proto-bio', bio ? '1' : '0');
	}, [bio]);
	useEffect(() => guardarLocal('kino-proto-vista', vista), [vista]);
	useEffect(() => {
		const k = (e: KeyboardEvent) => {
			if ((e.target as HTMLElement).closest('input')) return;
			const n = Number(e.key);
			if (n >= 1 && n <= 5) setVista(ACTORES[n - 1].k);
			if (e.key === 'b') setBio((x) => !x);
			if (e.key === 'i') setPanel((x) => !x);
		};
		addEventListener('keydown', k);
		return () => removeEventListener('keydown', k);
	}, []);

	// Cambio de actor: los dispositivos se acomodan y llegan en cascada; el estado de cada uno no se pierde.
	const lienzo = useRef<HTMLElement>(null);
	const actores = useRef<HTMLElement>(null);
	const vistaAntes = useRef(vista);
	useIndicador(actores, vista);
	useLayoutEffect(() => {
		if (vistaAntes.current === vista) return;
		vistaAntes.current = vista;
		lienzo.current?.querySelectorAll('.puesto').forEach((n, i) => animar(n, [{opacity: 0, transform: 'translateY(14px) scale(.97)'}, {opacity: 1, transform: 'none'}], {duration: D.tarjeta, easing: C.crecer, delay: i * 70, fill: 'backwards'}));
	}, [vista]);
	const [notas, notasSale] = usePresencia(panel && !solo);

	const ultima = INTERACCIONES.find((i) => i.id === est.ultima);
	const hechas = INTERACCIONES.filter((i) => i.estado === 'implementada');
	const v = velocidadActual();

	return (
		<div class={`escenario ${solo ? 'escenario--solo' : ''} ${notas ? '' : 'escenario--sin-panel'}`}>
			{bio && <Micelio clase="micelio--escenario" densidad={60} />}
			{!solo && (
				<header class="escenario__cabeza">
					<div class="escenario__marca">
						<Marca tam={30} />
						<span>
							<b>Kino · Prototipo</b>
							<span class="tenue">Entrega 3</span>
						</span>
					</div>
					<nav ref={actores} class="actores con-indicador" aria-label="Actor">
						<span class="indicador" aria-hidden="true" />
						{ACTORES.map((a, i) => (
							<button class={vista === a.k ? 'activo' : ''} onClick={() => setVista(a.k)} title={`${a.d} · tecla ${i + 1}`}>
								{a.t}
							</button>
						))}
					</nav>
					<div class="reloj">
						<span class="mono reloj__hora">{hora24(ahora())}</span>
						{[1, 60, 600].map((x) => (
							<button class={v === x ? 'activo' : ''} onClick={() => cambiarVelocidad(x)} title={x === 1 ? 'Tiempo real' : `${x} veces más rápido`}>
								{x === 1 ? '1×' : `${x}×`}
							</button>
						))}
						<button onClick={() => adelantar(30)} title="Adelantar 30 minutos">+30 min</button>
						<button class={bio ? 'activo' : ''} onClick={() => setBio(!bio)} title="Tecla B">
							Biopunk
						</button>
						<button onClick={() => setPanel(!panel)} title="Tecla I">Notas</button>
						<button onClick={reiniciar} title="Volver al inicio de la demo">Reiniciar</button>
					</div>
				</header>
			)}
			<main ref={lienzo} class={`escenario__lienzo escenario__lienzo--${vista}`}>
				{(vista === 'todos' || vista === 'residente') && (
					<div class="puesto puesto--telefono">
						{vista === 'todos' && <span class="puesto__rotulo">Residente</span>}
						<Escala ancho={390} alto={844} max={solo ? 3 : 1}>
							<Telefono etiqueta="App del residente">
								<Residente />
							</Telefono>
						</Escala>
					</div>
				)}
				{(vista === 'todos' || vista === 'visita') && (
					<div class="puesto puesto--telefono">
						{vista === 'todos' && <span class="puesto__rotulo">Visita</span>}
						<Escala ancho={390} alto={844} max={solo ? 3 : 1}>
							<Telefono etiqueta="Teléfono de la visita" claro>
								<Visita />
							</Telefono>
						</Escala>
					</div>
				)}
				{(vista === 'todos' || vista === 'porteria') && (
					<div class="puesto puesto--tableta">
						{vista === 'todos' && <span class="puesto__rotulo">Portería</span>}
						<Escala ancho={1080} alto={760} max={solo ? 3 : 1}>
							<div class="tableta" role="region" aria-label="Pantalla de portería">
								<Porteria />
							</div>
						</Escala>
					</div>
				)}
				{vista === 'administracion' && (
					<div class="puesto puesto--portatil">
						<Escala ancho={1280} alto={800} max={solo ? 3 : 1}>
							<div class="portatil" role="region" aria-label="Administración">
								<Administracion />
							</div>
						</Escala>
					</div>
				)}
			</main>
			{notas && (
				<aside class={`notas ${notasSale ? 'notas--sale' : ''}`} aria-live="polite">
					{ultima ? (
						<div class="nota-interaccion" key={ultima.id + est.vistas.size}>
							<span class="mono nota-interaccion__id">{ultima.id}</span>
							<h2>{ultima.nombre}</h2>
							<dl>
								<div><dt>Disparador</dt><dd>{ultima.disparador}</dd></div>
								<div><dt>Respuesta</dt><dd>{ultima.respuesta}</dd></div>
								<div><dt>Regla</dt><dd>{ultima.regla}</dd></div>
								<div><dt>HikCentral</dt><dd>{ultima.hik}</dd></div>
							</dl>
						</div>
					) : (
						<p class="secundario">Toca algo: aquí aparece la interacción, su regla y su efecto en el lector.</p>
					)}
					<div class="cobertura">
						<span class="rotulo">
							Vistas {hechas.filter((i) => est.vistas.has(i.id)).length} de {hechas.length}
						</span>
						<ol>
							{INTERACCIONES.map((i) => (
								<li class={`${est.vistas.has(i.id) ? 'vista' : ''} ${i.estado === 'planeada' ? 'planeada' : ''}`} title={i.disparador}>
									<span class="mono">{i.id}</span> {i.nombre}
									{i.estado === 'planeada' && <em> · planeada</em>}
								</li>
							))}
						</ol>
					</div>
				</aside>
			)}
		</div>
	);
}

const estilo = document.createElement('style');
estilo.textContent = variablesCss();
document.head.append(estilo);
if (q.get('reducido') === '1') document.documentElement.dataset.reducido = '1';
render(<Escenario />, document.getElementById('app')!);
(window as unknown as {kino: unknown}).kino = {E, adelantar, cambiarVelocidad, reiniciar};
