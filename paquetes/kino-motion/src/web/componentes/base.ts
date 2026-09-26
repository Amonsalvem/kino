// Base de los componentes: Shadow DOM, estilos con tokens de marca y reacción al cambio de modo.
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
