// La visita, sin cuenta: recibe el mensaje y abre el Pase vivo en el navegador (en claro, X1).
import {useLayoutEffect, useRef, useState} from 'preact/hooks';
import {anotar, corto, cuentaRegresiva, E, estado, hora24, horaCorta, ventana, vigenciaTexto} from './modelo';
import {ChipEstado, Icono, Ilustracion, Marca, Portal, QR, useKino, type ModoVista} from './componentes';
import {animar, C, D, R, volar} from './movimiento';

export function Visita() {
	const est = useKino(1000);
	const [vista, setVista] = useState<'chat' | 'pase'>('chat');
	// Continuidad: el QR de la imagen del WhatsApp crece hasta volverse el Pase vivo.
	const origen = useRef<DOMRect | null>(null);
	const p = est.pases.find((x) => x.id === est.visitaPaseId && x.compartido) ?? est.pases.find((x) => x.compartido);
	if (!p)
		return (
			<div class="app app--visita">
				<div class="vacio vacio--ilustrado">
					<Ilustracion tipo="pase-vacio" />
					<p class="nota">Aún no hay Pases enviados.</p>
				</div>
			</div>
		);
	return (
		<div class="app app--visita">
			{vista === 'chat' ? <Chat onAbrir={(r) => ((origen.current = r ?? null), setVista('pase'), anotar('I-09'))} /> : <PaseVivo id={p.id} origen={origen.current} onVolver={() => setVista('chat')} />}
		</div>
	);
}

function Chat({onAbrir}: {onAbrir: (r?: DOMRect) => void}) {
	const est = useKino(1000);
	const p = est.pases.find((x) => x.id === est.visitaPaseId && x.compartido) ?? est.pases.find((x) => x.compartido)!;
	const revocado = est.avisos.find((a) => a.para === 'visita' && a.paseId === p.id);
	return (
		<div class="chat">
			<div class="chat__cabeza">
				<Icono n="atras" />
				<span class="chat__avatar">CR</span>
				<span>
					<b>Carolina Ruiz</b>
					<span class="tenue">en línea</span>
				</span>
			</div>
			<div class="chat__cuerpo">
				<div class="burbuja burbuja--suya">
					<span>Hola {p.nombre.split(' ')[0]}, te espero. Te mando el Pase para entrar.</span>
					<span class="burbuja__hora">{hora24(p.compartido!)}</span>
				</div>
				<button class="burbuja burbuja--suya burbuja--pase" onClick={(ev) => onAbrir((ev.currentTarget as HTMLElement).querySelector('.imagen-pase__arco')?.getBoundingClientRect())}>
					<span class="imagen-pase">
						<span class="imagen-pase__cabeza">
							<Marca tam={18} />
							<span class="rotulo">Pase · {p.tipo === 'visita' ? 'Visita' : 'Colaborador'}</span>
						</span>
						<span class="imagen-pase__arco">
							<QR texto={`https://kino.co/p/${corto(p)}`} tam={92} />
						</span>
						<b>{p.nombre}</b>
						<span class="mono">{vigenciaTexto(p)}</span>
						<span class="mono">Código {p.codigo}{p.placa ? ` · ${p.placa}` : ''}</span>
					</span>
					<span class="enlace-chat">
						<Icono n="enlace" tam={16} />
						kino.co/p/{corto(p)}
					</span>
					<span class="burbuja__hora">{hora24(p.compartido!)}</span>
				</button>
				{revocado && (
					<div class="burbuja burbuja--sistema">
						<span>{revocado.texto} a las {horaCorta(revocado.hora)}. El enlace ya muestra que no está activo.</span>
					</div>
				)}
			</div>
			<div class="chat__pie">
				<span>Escribe un mensaje</span>
			</div>
		</div>
	);
}

function PaseVivo({id, origen, onVolver}: {id: string; origen: DOMRect | null; onVolver: () => void}) {
	const raiz = useRef<HTMLDivElement>(null);
	useLayoutEffect(() => {
		const el = raiz.current;
		if (!el) return;
		// La página del navegador funde; el Pase viaja desde la imagen del chat y lo demás llega a medio camino.
		animar(el, [{opacity: 0}, {opacity: 1}], {duration: D.corto, easing: C.crecer});
		volar(el.querySelector<HTMLElement>('.portal'), origen);
		el.querySelectorAll<HTMLElement>('.pase-vivo__fila, .pase-vivo__cuerpo > h1, .pase-vivo__cuerpo > p, .modos, .pase-vivo__instruccion').forEach((n, i) =>
			animar(n, [{opacity: 0, transform: 'translateY(10px)'}, {opacity: 1, transform: 'none'}], {duration: D.crecer, easing: C.crecer, delay: R.pase.ms * 0.35 + i * 40, fill: 'backwards'}),
		);
	}, []);
	useKino(1000);
	const p = E.pases.find((x) => x.id === id)!;
	const [modo, setModo] = useState<ModoVista>('qr');
	const e = estado(p);
	const v = ventana(p);
	const instruccion =
		e === 'usado' ? `Entraste a las ${horaCorta(p.hechos.usadoEn!)}`
		: e === 'revocado' ? `${p.autor.nombre} revocó este Pase. Escríbele si fue un error.`
		: e === 'vencido' ? `${p.autor.nombre} puede extenderlo: venció a las ${horaCorta(v.hasta)}`
		: e === 'sin-confirmar' ? 'El lector está recibiendo tu Pase. Tarda unos segundos.'
		: e === 'previsto' ? `Antes de las ${horaCorta(v.desde)} el lector no lo acepta`
		: p.entradas.length ? `Entraste a las ${horaCorta(p.entradas[p.entradas.length - 1])}. Puedes salir y volver hasta las ${horaCorta(v.hasta)}.`
		: modo === 'qr' ? 'Acerca el QR al lector y espera la luz verde.'
		: modo === 'placa' ? 'Llega con el carro: el lector lee la placa solo.'
		: 'Dile este código a portería.';
	return (
		<div ref={raiz} class="pase-vivo" data-tema="claro">
			<div class="navegador">
				<button class="icono-btn" onClick={onVolver} aria-label="Volver al chat">
					<Icono n="atras" tam={18} />
				</button>
				<span class="navegador__url">kino.co/p/{corto(p)}</span>
			</div>
			<div class="pantalla__scroll pase-vivo__cuerpo">
				<div class="pase-vivo__fila">
					<ChipEstado e={e} />
					<span class="chip-dato">Villas Campestres</span>
				</div>
				<h1 class="titulo titulo--l">{p.nombre}</h1>
				<p class="secundario">{vigenciaTexto(p)} · otorgó {p.autor.nombre}</p>
				{(e === 'vigente' || e === 'por-vencer') && <p class={`dato dato--${e}`}>Vence en {cuentaRegresiva(v.hasta)}</p>}
				<div class="pase-vivo__portal">
					<Portal p={p} modo={modo} claro tam={270} inclinable />
				</div>
				<div class="modos" role="tablist">
					{p.modos.map((m) => (
						<button role="tab" aria-selected={modo === m} class={modo === m ? 'activo' : ''} onClick={() => setModo(m)}>
							<Icono n={m} tam={18} />
							{m === 'qr' ? 'QR' : m === 'placa' ? 'Placa' : 'Código'}
						</button>
					))}
				</div>
				<p class="instruccion">{instruccion}</p>
				<div class="pase-vivo__pie">
					<Marca tam={18} />
					<span>Pase de Kino. Sin cuenta ni app.</span>
				</div>
			</div>
		</div>
	);
}
