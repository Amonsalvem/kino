// <kino-vigencia desde="…" hasta="…" estado="vigente">: la barra de vigencia con la hora real.
// No es una animación de adorno: la barra baja al ritmo del reloj (lineal, en tiempo real) hasta la hora de vencimiento.
// En modo reducido no se mueve: se actualiza una vez por minuto.
// La pista es superficie/elevada: la tarjeta del Pase es membrana (M3D-4) y la pista debe verse sobre ella.
import {vigenciaRestante} from '../../nucleo/pase';
import {definir, KinoElemento} from './base';

export class KinoVigencia extends KinoElemento {
	static observedAttributes = ['desde', 'hasta', 'estado'];
	private reloj: Animation | null = null;
	private minuto = 0;

	protected montar() {
		this.estilo(`
:host{display:block;block-size:4px}
:host([hidden]){display:none}
.pista{position:relative;block-size:100%;border-radius:2px;background:var(--kino-superficie-elevada);overflow:hidden}
.barra{position:absolute;inset:0;transform-origin:left center;background:var(--color, var(--kino-estado-vigente-borde));
 transition:background-color var(--kino-estado-dur, var(--kino-mov-duracion-corto)) var(--kino-estado-curva, var(--kino-mov-curva-crecer))}
:host([estado="por-vencer"]){--color:var(--kino-estado-por-vencer-borde)}
:host([estado="vencido"]),:host([estado="usado"]),:host([estado="revocado"]){--color:var(--kino-estado-vencido-borde)}
`);
		this.raiz.innerHTML += `<div class="pista" role="progressbar" aria-valuemin="0" aria-valuemax="100"><div class="barra" part="barra"></div></div>`;
		this.correr();
	}

	protected desmontar() {
		this.reloj?.cancel();
		clearInterval(this.minuto);
	}

	attributeChangedCallback() {
		if (this.isConnected) this.correr();
	}

	protected alCambiarModo() {
		this.correr();
	}

	/** Barra actual (para que kino-pase la anime al caducar). */
	get barra() {
		return this.$('.barra');
	}

	private correr() {
		this.reloj?.cancel();
		clearInterval(this.minuto);
		const barra = this.barra;
		if (!barra) return;
		const desde = new Date(this.getAttribute('desde') ?? Date.now());
		const hasta = new Date(this.getAttribute('hasta') ?? Date.now());
		const estado = this.getAttribute('estado');
		const pista = this.$('.pista');
		const actualizar = () => {
			const r = estado === 'vencido' ? 0 : vigenciaRestante({desde, hasta}, new Date());
			pista.setAttribute('aria-valuenow', String(Math.round(r * 100)));
			return r;
		};
		const r = actualizar();
		barra.style.transform = `scaleX(${r})`;
		const quedaMs = hasta.getTime() - Date.now();
		if (['vencido', 'usado', 'revocado'].includes(estado ?? '') || quedaMs <= 0) return;
		if (this.reducido) {
			this.minuto = window.setInterval(() => (barra.style.transform = `scaleX(${actualizar()})`), 60_000);
			return;
		}
		// Tiempo real: lineal de lo que queda a 0 durante lo que falta. La linealidad aquí es el reloj, no una curva de marca.
		this.reloj = barra.animate([{transform: `scaleX(${r})`}, {transform: 'scaleX(0)'}], {duration: quedaMs, easing: 'linear', fill: 'forwards'}); // motion-ok: reloj real
		this.reloj.finished.then(
			() => this.dispatchEvent(new CustomEvent('vigencia-agotada', {bubbles: true, composed: true})),
			() => {},
		);
		this.minuto = window.setInterval(actualizar, 60_000);
	}
}
definir('kino-vigencia', KinoVigencia);
