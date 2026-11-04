// <kino-estado estado="vigente">: el chip de estado de un Pase.
// Cambia de color con el verbo que le indique quien lo contiene (--kino-estado-dur, --kino-estado-curva).
// El punto late solo en vigente, un máximo de latir.ciclos veces, y se queda quieto (WCAG 2.2.2).
import {TOKENS} from '../../nucleo/tokens';
import {animar} from '../animar';
import type {NombreCurva} from '../../nucleo/tokens';
import {definir, ETIQUETA, fundirTexto, KinoElemento} from './base';

export class KinoEstado extends KinoElemento {
	static observedAttributes = ['estado'];
	private latido: Animation | null = null;
	/** Lo fija quien contiene el chip justo antes de cambiar el estado: el texto se funde a través (M3D-5). */
	fundido?: {ms: number; curva: NombreCurva};

	protected montar() {
		this.estilo(`
:host{display:inline-flex;--d:var(--kino-estado-dur, var(--kino-mov-duracion-corto));--c:var(--kino-estado-curva, var(--kino-mov-curva-crecer))}
.chip{display:inline-flex;align-items:center;gap:6px;padding:3px 10px;border-radius:var(--kino-forma-radio-chip, 4px);font:700 13px/1.3 var(--kino-fuente-texto, 'Archivo', sans-serif);white-space:nowrap;
 border:1px solid var(--borde);background:var(--fondo);color:var(--texto);
 transition:background-color var(--d) var(--c),border-color var(--d) var(--c),color var(--d) var(--c)}
.punto{position:relative;inline-size:6px;block-size:6px;border-radius:50%;background:var(--borde);transition:background-color var(--d) var(--c)}
.brillo{position:absolute;inset:-1px;border-radius:50%;background:var(--kino-estado-vigente-texto);opacity:0}
:host([estado="sin-confirmar"]) .chip{border-style:dashed}
:host([estado="sin-confirmar"]) .punto{background:transparent;box-shadow:inset 0 0 0 1px var(--borde)}
:host([estado="revocado"]) .punto,:host([estado="rechazado"]) .punto{border-radius:1px}
${Object.keys(ETIQUETA).map((e) => `:host([estado="${e}"]){--fondo:var(--kino-estado-${e}-fondo);--borde:var(--kino-estado-${e}-borde);--texto:var(--kino-estado-${e}-texto)}`).join('\n')}
`);
		this.raiz.innerHTML += `<span class="chip" part="chip"><span class="punto" part="punto"><span class="brillo"></span></span><span class="texto"></span></span>`;
		this.pintar();
	}

	attributeChangedCallback(_n: string, antes: string | null, ahora: string | null) {
		if (this.isConnected && antes !== ahora) this.pintar();
	}

	/** Vuelve a latir (lo llama kino-pase al terminar «confirmar»). */
	latir() {
		this.latido?.cancel();
		if (this.getAttribute('estado') !== 'vigente') return;
		// Un ciclo sube y baja con curva/latir; se repite latir.ciclos veces y se detiene.
		this.latido = animar(this.$('.brillo'), [{opacity: 0}, {opacity: 1, offset: 0.5}, {opacity: 0}], {
			duracion: 'latir/duracion',
			curva: 'latir/curva',
			iteraciones: TOKENS.latirCiclos,
			etiqueta: 'latir',
		});
	}

	protected alCambiarModo() {
		if (this.reducido) this.latido?.cancel();
	}

	private pintar() {
		const e = this.getAttribute('estado') ?? 'previsto';
		const t = this.raiz.querySelector('.texto') as HTMLElement | null;
		const nuevo = ETIQUETA[e] ?? e;
		if (t && this.fundido && t.textContent) fundirTexto(t, nuevo, this.fundido.ms, this.fundido.curva);
		else if (t) t.textContent = nuevo;
		this.fundido = undefined;
		this.setAttribute('role', 'status');
		if (e !== 'vigente') this.latido?.cancel();
	}
}
definir('kino-estado', KinoEstado);
