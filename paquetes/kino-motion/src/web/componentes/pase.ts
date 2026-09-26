// <kino-pase>: la tarjeta de un Pase. Interpreta la partitura de cada transición (núcleo/pase.ts).
//
//   <kino-pase quien="Andrés Gómez" casa="Casa 14" desde="…" hasta="…" estado="sin-confirmar" enviado="…"></kino-pase>
//   pase.aplicar('confirmar', {lector: 'Lector Portería', hora: new Date()})
//
// Estado honesto: sin evidencia del lector, el componente no muestra «vigente» ni «por vencer»; muestra «sin confirmar».
import {transicion, transicionEntre, type Estado, type Evento, type Pista, type Transicion} from '../../nucleo/pase';
import {reducirPistas} from '../../nucleo/reducido';
import {ms, TOKENS} from '../../nucleo/tokens';
import {animar} from '../animar';
import {entrar} from '../disposicion';
import {registrar} from '../entorno';
import {definir, hora, KinoElemento} from './base';
import type {KinoEstado} from './estado';
import './estado';
import './vigencia';

const NECESITA_EVIDENCIA: ReadonlySet<string> = new Set(['vigente', 'por-vencer']);

export class KinoPase extends KinoElemento {
	static observedAttributes = ['estado', 'quien', 'casa', 'codigo', 'desde', 'hasta', 'enviado', 'lector', 'confirmado', 'revoco', 'revocado', 'usado'];
	private estadoPintado: Estado | null = null;

	protected montar() {
		this.estilo(`
:host{display:block;position:relative;--d:var(--kino-mov-duracion-corto);--c:var(--kino-mov-curva-crecer)}
.tarjeta{position:relative;display:grid;gap:8px;padding:20px;border-radius:var(--kino-forma-radio-tarjeta, 14px);background:var(--kino-superficie-elevada);isolation:isolate}
.borde{position:absolute;inset:0;border-radius:inherit;pointer-events:none;border:1px solid var(--kino-estado-vigente-borde);transition:border-color var(--d) var(--c),opacity var(--d) var(--c)}
.borde.discontinuo{border-style:dashed;border-color:var(--kino-estado-sin-confirmar-borde);opacity:0}
.cabeza{display:flex;align-items:center;justify-content:space-between;gap:12px}
.quien{font:700 17px/1.2 var(--kino-fuente-texto, 'Archivo', sans-serif);margin:0;position:relative}
.quien.mono{font-weight:400}
.dato{margin:0;font-size:13px;color:var(--kino-texto-secundario)}
.nota{margin:0;font-size:12px;min-block-size:1.3em;color:var(--kino-texto-tenue)}
.corte{position:absolute;left:0;right:0;top:46%;block-size:2px;background:var(--kino-estado-revocado-texto);transform-origin:left center;transform:scaleX(0);pointer-events:none}
.tachado{position:absolute;left:0;right:0;top:55%;block-size:2px;background:var(--kino-estado-usado-texto);transform-origin:left center;transform:scaleX(0)}
kino-vigencia{margin-block-start:4px}
:host([data-estado="sin-confirmar"]) .borde.discontinuo{opacity:1}
:host([data-estado="sin-confirmar"]) .borde.continuo{opacity:0}
:host([data-estado="previsto"]) .borde.continuo{border-color:var(--kino-estado-previsto-borde)}
:host([data-estado="por-vencer"]) .borde.continuo{border-color:var(--kino-estado-por-vencer-borde)}
:host([data-estado="vencido"]) .borde.continuo,:host([data-estado="usado"]) .borde.continuo,:host([data-estado="revocado"]) .borde.continuo{border-color:var(--kino-estado-vencido-borde)}
:host([data-estado="revocado"]) .tarjeta{background:var(--kino-superficie-base)}
:host([data-estado="revocado"]) .nota{color:var(--kino-estado-revocado-texto)}
:host([data-estado="vigente"]) .nota,:host([data-estado="por-vencer"]) .nota{color:var(--kino-estado-vigente-texto)}
:host([data-estado="vencido"]) .tarjeta,:host([data-estado="usado"]) .tarjeta,:host([data-estado="revocado"]) .tarjeta{opacity:.72}
`);
		this.raiz.innerHTML += `
<article class="tarjeta" part="tarjeta">
  <span class="borde continuo" part="borde"></span><span class="borde discontinuo"></span>
  <div class="cabeza"><p class="quien"><span class="nombre"></span><span class="tachado"></span></p><kino-estado></kino-estado></div>
  <p class="dato mono"></p>
  <p class="nota mono"></p>
  <kino-vigencia></kino-vigencia>
  <span class="corte" part="corte"></span>
</article>`;
		this.pintar(false);
		if (this.hasAttribute('entrar')) entrar(this, Number(this.getAttribute('retraso') ?? 0));
	}

	private pendiente = false;
	private cambioDeEstado = false;
	attributeChangedCallback(nombre: string, antes: string | null, ahora: string | null) {
		if (!this.isConnected || antes === ahora) return;
		// Los atributos llegan de a uno: se pinta una vez por tanda, así el orden (estado antes que lector) no importa.
		this.cambioDeEstado ||= nombre === 'estado';
		if (this.pendiente) return;
		this.pendiente = true;
		queueMicrotask(() => {
			this.pendiente = false;
			const animarCambio = this.cambioDeEstado;
			this.cambioDeEstado = false;
			this.pintar(animarCambio);
		});
	}

	/** Estado que se puede mostrar sin mentir: vigente y por vencer exigen la confirmación del lector. */
	get estadoHonesto(): Estado {
		const pedido = (this.getAttribute('estado') ?? 'previsto') as Estado;
		if (NECESITA_EVIDENCIA.has(pedido) && !(this.getAttribute('lector') && this.getAttribute('confirmado'))) {
			console.warn(`kino-pase: «${pedido}» sin confirmación del lector; se muestra «sin confirmar».`);
			return 'sin-confirmar';
		}
		return pedido;
	}

	/** Aplica un evento con sus datos (valida que la transición exista). */
	aplicar(evento: Evento, datos: {lector?: string; hora?: Date; autor?: string} = {}) {
		const t = transicion(this.estadoHonesto, evento);
		const cuando = (datos.hora ?? new Date()).toISOString();
		if (evento === 'confirmar') {
			if (!datos.lector) throw new Error('confirmar exige el lector que confirmó');
			this.setAttribute('lector', datos.lector);
			this.setAttribute('confirmado', cuando);
		}
		if (evento === 'enviar') this.setAttribute('enviado', cuando);
		if (evento === 'revocar') {
			if (!datos.autor) throw new Error('revocar exige quién revocó');
			this.setAttribute('revoco', datos.autor);
			this.setAttribute('revocado', cuando);
		}
		if (evento === 'usar') this.setAttribute('usado', cuando);
		this.setAttribute('estado', t.a);
	}

	private pintar(animarCambio: boolean) {
		const estado = this.estadoHonesto;
		const previo = this.estadoPintado;
		const t = animarCambio && previo && previo !== estado ? transicionEntre(previo, estado) : undefined;
		// Tiempo del cambio: el del verbo de la transición (color de chip y bordes incluidos).
		const dur = t ? ms(t.duracion) : ms('duracion/corto');
		const curva = `var(--kino-mov-curva-${((TOKENS.verbo as Record<string, string>)[t?.curva ?? 'curva/crecer'] ?? t?.curva ?? 'curva/crecer').split('/')[1]})`;
		this.style.setProperty('--d', `${dur}ms`);
		this.style.setProperty('--c', curva);
		this.style.setProperty('--kino-estado-dur', `${dur}ms`);
		this.style.setProperty('--kino-estado-curva', curva);

		this.$('.nombre').textContent = this.getAttribute('codigo') ?? this.getAttribute('quien') ?? '';
		this.$('.quien').classList.toggle('mono', this.hasAttribute('codigo'));
		this.$('.dato').textContent = this.dato(estado);
		this.$('.nota').textContent = this.nota(estado);
		const chip = this.raiz.querySelector('kino-estado') as KinoEstado;
		chip.setAttribute('estado', estado);
		const vig = this.raiz.querySelector('kino-vigencia')!;
		for (const a of ['desde', 'hasta']) if (this.hasAttribute(a)) vig.setAttribute(a, this.getAttribute(a)!);
		vig.setAttribute('estado', estado);
		vig.toggleAttribute('hidden', ['previsto', 'sin-confirmar'].includes(estado));
		this.dataset.estado = estado;
		// Sin atributo estado todavía no hay un estado real: el primero que llegue es el inicial, no un cambio.
		this.estadoPintado = this.hasAttribute('estado') ? estado : null;

		if (t) this.interpretar(t, chip);
		else if (animarCambio && previo && previo !== estado) registrar(null, {etiqueta: `${previo} → ${estado} sin transición: cambio directo`, elemento: this, duracion: 0, tokens: '—', reducido: this.reducido});
		if (!t && estado === 'vigente' && !previo) chip.latir();
	}

	/** Ejecuta la partitura: cada pista, en su parte, con la duración y la curva del verbo. */
	private interpretar(t: Transicion, chip: KinoEstado) {
		const pistas = this.reducido ? reducirPistas(t.pistas) : [...t.pistas];
		const partes: Record<string, HTMLElement | undefined> = {
			tarjeta: this.$('.tarjeta'), nota: this.$('.nota'), corte: this.$('.corte'), tachado: this.$('.tachado'),
			barra: (this.raiz.querySelector('kino-vigencia') as HTMLElement & {barra?: HTMLElement})?.barra,
		};
		const opts = {duracion: t.duracion, curva: t.curva, etiqueta: `${t.evento}: ${t.de.join('|')} → ${t.a}`} as const;
		let fin: Animation | null = null;
		for (const p of pistas) {
			const el = partes[p.parte];
			if (!el) continue; // chip, borde y punto cambian por CSS con el mismo tiempo
			const kf = this.keyframes(p, el);
			if (kf) fin = animar(el, kf, {...opts, etiqueta: `${t.evento} · ${p.parte} ${p.propiedad}`, canal: `${p.parte}-${p.propiedad}`}) ?? fin;
		}
		registrar(null, {etiqueta: opts.etiqueta, elemento: this, duracion: ms(t.duracion), tokens: `${t.duracion} · ${t.curva}`, reducido: this.reducido});
		this.dispatchEvent(new CustomEvent('transicion', {detail: {evento: t.evento, a: t.a, deja: t.deja}, bubbles: true, composed: true}));
		if (t.late) {
			const esperar = fin ? fin.finished.catch(() => {}) : new Promise((r) => setTimeout(r, ms(t.duracion)));
			esperar.then(() => chip.latir());
		}
	}

	private keyframes(p: Pista, el: HTMLElement): Keyframe[] | null {
		const n = (v: number | string) => (v === 'subida' ? TOKENS.distancia.subida : v === 'actual' ? null : Number(v));
		switch (p.propiedad) {
			case 'opacidad':
				return [{opacity: n(p.de) ?? Number(getComputedStyle(el).opacity)}, {opacity: n(p.a)!}];
			case 'y':
				return [{transform: `translateY(${n(p.de)}px)`}, {transform: `translateY(${n(p.a)}px)`}];
			case 'escalaX': {
				const de = n(p.de) ?? (new DOMMatrixReadOnly(getComputedStyle(el).transform).a || 0);
				return [{transform: `scaleX(${de})`}, {transform: `scaleX(${n(p.a)})`}];
			}
			default:
				return null;
		}
	}

	private dato(e: Estado) {
		const casa = this.getAttribute('casa') ?? '';
		const f = (a: string) => (this.getAttribute(a) ? hora(new Date(this.getAttribute(a)!)) : '');
		const franja = this.getAttribute('desde') && this.getAttribute('hasta') ? `${f('desde')}–${f('hasta')}` : '';
		const partes: Record<Estado, string> = {
			previsto: `${casa} · ${franja}`,
			'sin-confirmar': `${casa} · enviado ${f('enviado')}`,
			vigente: `${casa} · ${franja}`,
			'por-vencer': `${casa} · vence ${f('hasta')}`,
			vencido: `${casa} · venció ${f('hasta')}`,
			usado: `${casa} · entró ${f('usado')}`,
			revocado: `${casa} · ${franja}`,
		};
		return partes[e].replace(/ · $/, '');
	}

	private nota(e: Estado) {
		const f = (a: string) => (this.getAttribute(a) ? hora(new Date(this.getAttribute(a)!)) : '');
		if ((e === 'vigente' || e === 'por-vencer') && this.getAttribute('lector')) return `Confirmó ${this.getAttribute('lector')} · ${f('confirmado')}`;
		if (e === 'revocado' && this.getAttribute('revoco')) return `Revocó ${this.getAttribute('revoco')} · ${f('revocado')}`;
		return '';
	}
}
definir('kino-pase', KinoPase);
