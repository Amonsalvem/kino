// Base de los componentes: Shadow DOM, estilos con tokens de marca y reacción al cambio de modo.
import {cambioDeTexto, tramosDeTexto} from '../../nucleo/textos';
import type {NombreCurva} from '../../nucleo/tokens';
import {animar} from '../animar';
import {alCambiarModo, esReducido} from '../entorno';

export const ETIQUETA: Record<string, string> = {
	previsto: 'Previsto',
	'sin-confirmar': 'Sin confirmar',
	vigente: 'Vigente',
	'por-vencer': 'Por vencer',
	vencido: 'Vencido',
	usado: 'Usado',
	revocado: 'Revocado',
	rechazado: 'Rechazado',
};

/** Estilos comunes. Los colores son variables de marca (kino-tokens.css), con el tema que tenga la página. */
export const BASE_CSS = `
:host{box-sizing:border-box;font-family:var(--kino-fuente-texto, 'Archivo', system-ui, sans-serif);color:var(--kino-texto-primario)}
*,*::before,*::after{box-sizing:inherit}
.mono{font-family:var(--kino-fuente-dato, 'JetBrains Mono', ui-monospace, monospace);font-variant-numeric:tabular-nums}
`;

export abstract class KinoElemento extends HTMLElement {
	protected raiz: ShadowRoot;
	private soltarModo?: () => void;
	constructor() {
		super();
		this.raiz = this.attachShadow({mode: 'open'});
	}
	get reducido() {
		return esReducido();
	}
	connectedCallback() {
		this.soltarModo = alCambiarModo(() => this.alCambiarModo());
		this.montar();
	}
	disconnectedCallback() {
		this.soltarModo?.();
		this.desmontar();
	}
	protected abstract montar(): void;
	protected desmontar() {}
	protected alCambiarModo() {}
	protected estilo(css: string) {
		const s = document.createElement('style');
		s.textContent = BASE_CSS + css;
		this.raiz.append(s);
	}
	protected $(sel: string) {
		return this.raiz.querySelector(sel) as HTMLElement;
	}
}

export const definir = (nombre: string, clase: CustomElementConstructor) => {
	if (!customElements.get(nombre)) customElements.define(nombre, clase);
};

/** Hora corta en español de Colombia: «3:41 p. m.». */
export const hora = (d: Date) => d.toLocaleTimeString('es-CO', {hour: 'numeric', minute: '2-digit'});

const turnos = new WeakMap<HTMLElement, number>();
/**
 * Cambia el texto de un elemento con la regla M3D-5: si uno sale y otro entra, fundido a través (mitad y mitad);
 * si solo sale o solo entra, un fundido en toda la duración. Si llega otro cambio a mitad, gana el último.
 * `conPista`: el texto que entra ya lo anima la partitura (por ejemplo, la nota al confirmar); solo se pone.
 */
export function fundirTexto(el: HTMLElement, nuevo: string, duracionMs: number, curva: NombreCurva, conPista = false) {
	const cambio = cambioDeTexto(el.textContent ?? '', nuevo);
	if (cambio === 'igual') return cambio;
	const turno = (turnos.get(el) ?? 0) + 1;
	turnos.set(el, turno);
	const {sale, entra} = tramosDeTexto(cambio, duracionMs);
	const entrar = () => {
		if (turnos.get(el) !== turno) return;
		el.textContent = nuevo;
		if (!entra || conPista) return;
		animar(el, [{opacity: 0}, {opacity: 1}], {duracionMs: entra[1], curva, canal: 'texto', etiqueta: 'texto entra'});
	};
	if (!sale) {
		entrar();
		return cambio;
	}
	const a = animar(el, [{opacity: 1}, {opacity: 0}], {duracionMs: sale[1], curva, canal: 'texto', etiqueta: 'texto sale'});
	const alSalir = () => {
		if (turnos.get(el) !== turno) return;
		if (entra) entrar();
		else {
			el.textContent = '';
			el.style.opacity = '';
		}
	};
	if (a) a.finished.then(alSalir, () => {});
	else alSalir();
	return cambio;
}
