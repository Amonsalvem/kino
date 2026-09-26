// Componentes de interacción: lista, acción, hoja, aviso, espera del lector y número.
import {escalonar} from '../../nucleo/coreografia';
import {TOKENS} from '../../nucleo/tokens';
import {animar, terminada} from '../animar';
import {entrar, flip, quitar} from '../disposicion';
import {proyectar} from '../../nucleo/gestos';
import {animarResorte, arrastrar, type Control} from '../fisica';
import {definir, hora, KinoElemento} from './base';

// <kino-lista> ----------------------------------------------------------------------------------------------
/** Lista de Pases: entra en cascada (con máximo y tope), y cada alta o baja reacomoda al resto con FLIP. */
export class KinoLista extends KinoElemento {
	protected montar() {
		this.estilo(`:host{display:grid;gap:var(--kino-lista-espacio, 12px)}`);
		this.raiz.innerHTML += '<slot></slot>';
		if (!this.hasAttribute('sin-entrada')) this.entrarTodo();
	}
	/** Vuelve a hacer la entrada en cascada (al abrir la pantalla). */
	entrarTodo() {
		const hijos = [...this.children];
		escalonar(hijos.length).forEach((r, i) => entrar(hijos[i], r));
	}
	/** Inserta un elemento (al principio por defecto): entra con «aparecer» y los demás bajan con resorte. */
	insertar(el: Element, antesDe: Element | null = this.firstElementChild) {
		return flip(this, () => void this.insertBefore(el, antesDe));
	}
	/** Quita un elemento: sale (más corto que entrar) y los demás suben con resorte. */
	quitar(el: Element) {
		return quitar(el);
	}
	/** Reordena con una función de orden; cada tarjeta viaja a su nuevo lugar. */
	ordenar(cmp: (a: Element, b: Element) => number) {
		return flip(this, () => [...this.children].sort(cmp).forEach((c) => this.append(c)));
	}
}
definir('kino-lista', KinoLista);

// <kino-accion> ---------------------------------------------------------------------------------------------
/** Botón de acción: al presionarlo se hunde con resorte/tacto; al soltar vuelve con el mismo resorte. */
export class KinoAccion extends KinoElemento {
	static formAssociated = true;
	protected montar() {
		this.estilo(`
:host{display:inline-block}
button{all:unset;box-sizing:border-box;display:inline-flex;align-items:center;justify-content:center;gap:8px;min-block-size:48px;padding:0 20px;border-radius:var(--kino-forma-radio-control, 8px);
 font:700 16px/1 var(--kino-fuente-texto, 'Archivo', sans-serif);cursor:pointer;background:var(--kino-accion-fondo);color:var(--kino-accion-texto);
 transition:background-color var(--kino-mov-duracion-instante) var(--kino-mov-curva-crecer)}
button:active{background:var(--kino-accion-fondo-activo)}
button:focus-visible{outline:2px solid var(--kino-borde-foco);outline-offset:2px}
:host([variante="secundaria"]) button{background:var(--kino-superficie-membrana);color:var(--kino-texto-primario)}
:host([ancho="completo"]){display:block}:host([ancho="completo"]) button{inline-size:100%}
`);
		this.raiz.innerHTML += '<button part="boton" type="button"><slot></slot></button>';
		const b = this.$('button');
		const presionar = (abajo: boolean) =>
			animar(b, [{transform: `scale(${abajo ? TOKENS.escala.presion : 1})`}], {resorte: 'tacto', canal: 'presion', desdeActual: true, etiqueta: abajo ? 'presionar' : 'soltar'});
		b.addEventListener('pointerdown', () => presionar(true));
		for (const ev of ['pointerup', 'pointerleave', 'pointercancel']) b.addEventListener(ev, () => presionar(false));
		b.addEventListener('keydown', (e) => (e.key === ' ' || e.key === 'Enter') && presionar(true));
		b.addEventListener('keyup', () => presionar(false));
	}
}
definir('kino-accion', KinoAccion);

// <kino-hoja> -----------------------------------------------------------------------------------------------
/**
 * Hoja inferior. Abre y cierra con resorte/hoja. Se arrastra: si se suelta con velocidad hacia abajo o pasada la
 * mitad, se cierra continuando la velocidad del dedo; si no, vuelve a su lugar. Escape cierra; el foco vuelve.
 */
export class KinoHoja extends KinoElemento {
	static observedAttributes = ['abierta'];
	private y = 0;
	private control: Control | null = null;
	private foco: Element | null = null;

	protected montar() {
		this.estilo(`
:host{position:fixed;inset:0;z-index:${30 + TOKENS.profundidad.hoja};pointer-events:none}
:host([abierta]){pointer-events:auto}
.velo{position:absolute;inset:0;background:var(--kino-superficie-abismo);opacity:0}
.hoja{position:absolute;left:0;right:0;bottom:0;max-block-size:88vh;overflow:auto;margin-inline:auto;max-inline-size:640px;
 background:var(--kino-superficie-elevada);border-radius:20px 20px 0 0;padding:8px 20px 28px;transform:translateY(100%);box-shadow:0 -1px 0 var(--kino-superficie-membrana)}
.asa{display:grid;place-items:center;block-size:28px;cursor:grab;touch-action:none}
.asa::before{content:"";inline-size:40px;block-size:4px;border-radius:2px;background:var(--kino-texto-tenue)}
`);
		this.raiz.innerHTML += `<div class="velo" part="velo"></div><section class="hoja" part="hoja" role="dialog" aria-modal="true" tabindex="-1"><div class="asa" aria-hidden="true"></div><slot></slot></section>`;
		const hoja = this.$('.hoja');
		this.$('.velo').addEventListener('click', () => this.cerrar());
		this.addEventListener('keydown', (e) => e.key === 'Escape' && this.cerrar());
		arrastrar(this.$('.asa'), {
			eje: 'y', min: 0, max: Infinity, inicial: () => this.y,
			alEmpezar: () => this.control?.detener(),
			alMover: (p) => this.pintar(p),
			alSoltar: (p, v) => {
				const alto = hoja.offsetHeight;
				if (this.reducido) return p > alto / 3 ? this.cerrar() : this.ir(0, 0);
				proyectar(p, v) > alto / 2 ? this.cerrar(v) : this.ir(0, v);
			},
		});
		this.pintar(this.hasAttribute('abierta') ? 0 : this.alto());
	}

	attributeChangedCallback(_n: string, antes: string | null, ahora: string | null) {
		if (!this.isConnected || (antes === null) === (ahora === null)) return;
		if (ahora !== null) this.abrir();
	}

	private alto() {
		return this.$('.hoja')?.offsetHeight || innerHeight;
	}
	private pintar(y: number) {
		this.y = y;
		const alto = this.alto();
		this.$('.hoja').style.transform = `translateY(${y}px)`;
		this.$('.velo').style.opacity = String(0.6 * (1 - Math.min(1, Math.max(0, y / alto))));
	}
	private ir(destino: number, velocidad: number) {
		this.control?.detener();
		if (this.reducido) {
			// Reducido: la hoja no se desliza, aparece o se va por fundido con la duración de «crecer».
			this.pintar(destino);
			const h = this.$('.hoja');
			return terminada(animar(h, [{opacity: destino === 0 ? 0 : 1}, {opacity: destino === 0 ? 1 : 0}], {duracion: 'duracion/crecer', etiqueta: 'hoja (reducido)'})).then(() => {
				h.style.opacity = '';
			});
		}
		this.control = animarResorte({de: this.y, a: destino, velocidad, resorte: 'hoja', alCambiar: (v) => this.pintar(v), elemento: this, etiqueta: destino === 0 ? 'abrir hoja' : 'cerrar hoja'});
		return this.control.terminado;
	}
	abrir() {
		if (!this.hasAttribute('abierta')) return this.setAttribute('abierta', '');
		this.foco = document.activeElement;
		this.pintar(this.alto());
		this.ir(0, 0);
		this.$('.hoja').focus({preventScroll: true});
	}
	async cerrar(velocidad = 0) {
		await this.ir(this.alto(), velocidad);
		this.removeAttribute('abierta');
		(this.foco as HTMLElement | null)?.focus?.();
		this.dispatchEvent(new CustomEvent('cerrada', {bubbles: true, composed: true}));
	}
}
definir('kino-hoja', KinoHoja);

// <kino-aviso> ----------------------------------------------------------------------------------------------
/** Región de avisos. aviso.mostrar('Pase enviado a Andrés · 3:41 p. m.'). Entra con «aparecer» y sale más corto. */
export class KinoAviso extends KinoElemento {
	protected montar() {
		this.estilo(`
:host{position:fixed;left:0;right:0;bottom:24px;display:grid;justify-items:center;gap:8px;z-index:${30 + TOKENS.profundidad.aviso};pointer-events:none;padding-inline:16px}
.aviso{pointer-events:auto;max-inline-size:480px;padding:12px 16px;border-radius:var(--kino-forma-radio-control, 8px);background:var(--kino-superficie-membrana);color:var(--kino-texto-primario);font-size:14px;box-shadow:0 8px 24px rgb(0 0 0 / .35)}
.aviso[data-tono="vigente"]{box-shadow:inset 0 0 0 1px var(--kino-estado-vigente-borde)}
.aviso[data-tono="rechazado"]{background:var(--kino-estado-rechazado-fondo);color:var(--kino-estado-rechazado-texto)}
`);
		this.setAttribute('role', 'status');
		this.setAttribute('aria-live', 'polite');
	}
	mostrar(texto: string, tono: 'neutro' | 'vigente' | 'rechazado' = 'neutro') {
		const a = document.createElement('div');
		a.className = 'aviso';
		a.dataset.tono = tono;
		a.textContent = texto;
		this.raiz.append(a);
		entrar(a);
		setTimeout(() => quitar(a), TOKENS.avisoVisibleMs);
		return a;
	}
}
definir('kino-aviso', KinoAviso);

// <kino-espera-lector> --------------------------------------------------------------------------------------
/**
 * La espera real del lector, sin spinner. La línea llega una vez al lector (trazo) y se queda quieta; el texto
 * dice cuánto lleva la espera. Cuando llega el atributo confirmado, el lector pasa a vigente con «aparecer».
 */
export class KinoEsperaLector extends KinoElemento {
	static observedAttributes = ['confirmado'];
	private reloj = 0;
	protected montar() {
		this.estilo(`
:host{display:block}
.fila{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:8px}
.nodo{inline-size:14px;block-size:14px;border-radius:50%;border:1px dashed var(--kino-estado-sin-confirmar-borde);background:var(--kino-superficie-elevada);
 transition:border-color var(--kino-mov-duracion-tarjeta) var(--kino-mov-curva-crecer),background-color var(--kino-mov-duracion-tarjeta) var(--kino-mov-curva-crecer)}
.linea{block-size:2px;background:var(--kino-estado-sin-confirmar-borde);transform-origin:left center;transition:background-color var(--kino-mov-duracion-tarjeta) var(--kino-mov-curva-crecer)}
.rotulos{display:flex;justify-content:space-between;font-size:11px;color:var(--kino-texto-tenue);margin-block-start:6px}
.texto{margin:10px 0 0;font-size:13px;color:var(--kino-texto-secundario)}
:host([confirmado]) .nodo.lector{border-style:solid;border-color:var(--kino-estado-vigente-borde);background:var(--kino-estado-vigente-fondo)}
:host([confirmado]) .linea{background:var(--kino-estado-vigente-borde)}
:host([confirmado]) .texto{color:var(--kino-estado-vigente-texto)}
`);
		this.raiz.innerHTML += `<div class="fila"><span class="nodo"></span><span class="linea"></span><span class="nodo lector"></span></div>
<div class="rotulos mono"><span>Kino</span><span class="nombre-lector"></span></div><p class="texto mono" aria-live="polite"></p>`;
		this.$('.nombre-lector').textContent = this.getAttribute('lector') ?? 'Lector';
		// El recorrido se dibuja una sola vez: no es un indicador de carga en bucle.
		animar(this.$('.linea'), [{transform: 'scaleX(0)'}, {transform: 'scaleX(1)'}], {duracion: 'duracion/trazo', curva: 'curva/crecer', etiqueta: 'trazo al lector'});
		this.texto();
		this.reloj = window.setInterval(() => this.texto(), 30_000);
	}
	protected desmontar() {
		clearInterval(this.reloj);
	}
	attributeChangedCallback() {
		if (this.isConnected) this.texto();
	}
	private texto() {
		const lector = this.getAttribute('lector') ?? 'el lector';
		const c = this.getAttribute('confirmado');
		const e = this.getAttribute('enviado');
		if (c) {
			clearInterval(this.reloj);
			this.$('.texto').textContent = `Confirmó ${lector} · ${hora(new Date(c))}`;
			return;
		}
		const min = e ? Math.floor((Date.now() - new Date(e).getTime()) / 60_000) : 0;
		this.$('.texto').textContent = `Enviado ${e ? hora(new Date(e)) : ''} · ${lector} aún no confirma${min >= 1 ? ` · ${min} min` : ''}`;
	}
}
definir('kino-espera-lector', KinoEsperaLector);

// <kino-numero> ---------------------------------------------------------------------------------------------
/** Número que cambia con resorte/firme (sin pasarse del valor real). Cifras tabulares, formato es-CO. */
export class KinoNumero extends KinoElemento {
	static observedAttributes = ['valor'];
	private actual = 0;
	private control: Control | null = null;
	protected montar() {
		this.estilo(`:host{display:inline;font-variant-numeric:tabular-nums}`);
		this.actual = Number(this.getAttribute('valor') ?? 0);
		this.raiz.append(document.createTextNode(this.formato(this.actual)));
	}
	attributeChangedCallback(_n: string, _a: string | null, v: string | null) {
		if (!this.isConnected) return;
		this.control?.detener();
		const destino = Number(v ?? 0);
		const decimales = Number(this.getAttribute('decimales') ?? 0);
		this.control = animarResorte({
			de: this.actual, a: destino, resorte: 'firme', elemento: this, etiqueta: 'número',
			alCambiar: (x) => {
				this.actual = x;
				this.raiz.lastChild!.textContent = this.formato(Number(x.toFixed(decimales)));
			},
		});
	}
	private formato(n: number) {
		return n.toLocaleString('es-CO', {maximumFractionDigits: Number(this.getAttribute('decimales') ?? 0)});
	}
}
definir('kino-numero', KinoNumero);

