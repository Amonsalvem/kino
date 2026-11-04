// Inspector de motion: panel flotante para revisar el movimiento en la página real.
// Cámara lenta, modo reducido, resaltado de lo que se mueve y registro con los tokens de cada animación.
import {alAnimar, animacionesVivas, fijarVelocidad, obtenerVelocidad, type Registro} from './entorno';

export function montarInspector(destino: HTMLElement = document.body) {
	if (document.getElementById('kino-inspector')) return;
	const panel = document.createElement('aside');
	panel.id = 'kino-inspector';
	panel.setAttribute('aria-label', 'Inspector de motion');
	panel.innerHTML = `
<style>
#kino-inspector{position:fixed;right:16px;bottom:16px;z-index:99;inline-size:min(320px,calc(100vw - 32px));max-block-size:46vh;display:flex;flex-direction:column;gap:8px;padding:12px;border-radius:12px;
 background:var(--kino-superficie-elevada);color:var(--kino-texto-primario);box-shadow:0 12px 32px rgb(0 0 0 / .4),inset 0 0 0 1px var(--kino-superficie-membrana);font:13px/1.4 var(--kino-fuente-texto,'Archivo',sans-serif)}
#kino-inspector .cuerpo{display:grid;gap:8px;min-block-size:0;overflow:hidden}
#kino-inspector[data-plegado] .cuerpo{display:none}
#kino-inspector .fila{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
#kino-inspector button{font:700 12px/1 inherit;padding:7px 10px;border-radius:6px;border:1px solid var(--kino-superficie-membrana);background:var(--kino-superficie-base);color:inherit;cursor:pointer}
#kino-inspector button[aria-pressed="true"]{background:var(--kino-accion-fondo);color:var(--kino-accion-texto);border-color:transparent}
#kino-inspector ol{margin:0;padding:0;list-style:none;overflow:auto;display:grid;gap:4px;font-family:var(--kino-fuente-dato,'JetBrains Mono',monospace);font-size:11px}
#kino-inspector li{padding:6px 8px;border-radius:6px;background:var(--kino-superficie-base)}
#kino-inspector li b{color:var(--kino-estado-vigente-texto);font-weight:400}
#kino-inspector .t{color:var(--kino-texto-tenue)}
.kino-resaltado{outline:1px dashed var(--kino-estado-previsto-borde)!important;outline-offset:2px}
</style>
<div class="fila"><strong>Motion</strong><span class="t vivas"></span><button type="button" class="plegar" aria-expanded="true">Plegar</button></div>
<div class="cuerpo">
 <div class="fila" role="group" aria-label="Velocidad">${[0.1, 0.25, 1].map((v) => `<button type="button" data-v="${v}" aria-pressed="${v === obtenerVelocidad()}">${v}×</button>`).join('')}</div>
 <div class="fila"><button type="button" class="reducido" aria-pressed="false">Movimiento reducido</button><button type="button" class="resaltar" aria-pressed="false">Resaltar</button></div>
 <ol></ol>
</div>`;
	destino.append(panel);
	// En pantallas angostas empieza plegado para no tapar lo que se revisa.
	if (innerWidth < 1500) panel.setAttribute('data-plegado', '');
	const lista = panel.querySelector('ol')!;
	const vivas = panel.querySelector('.vivas')!;
	panel.querySelectorAll<HTMLButtonElement>('[data-v]').forEach((b) =>
		b.addEventListener('click', () => {
			fijarVelocidad(Number(b.dataset.v));
			panel.querySelectorAll('[data-v]').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
		}),
	);
	const bRed = panel.querySelector<HTMLButtonElement>('.reducido')!;
	bRed.setAttribute('aria-pressed', String(document.documentElement.dataset.movimiento === 'reducido'));
	bRed.addEventListener('click', () => {
		const on = document.documentElement.dataset.movimiento !== 'reducido';
		document.documentElement.dataset.movimiento = on ? 'reducido' : 'completo';
		bRed.setAttribute('aria-pressed', String(on));
	});
	let resaltar = false;
	const bRes = panel.querySelector<HTMLButtonElement>('.resaltar')!;
	bRes.addEventListener('click', () => {
		resaltar = !resaltar;
		bRes.setAttribute('aria-pressed', String(resaltar));
	});
	const plegar = panel.querySelector<HTMLButtonElement>('.plegar')!;
	if (panel.hasAttribute('data-plegado')) {
		plegar.textContent = 'Abrir';
		plegar.setAttribute('aria-expanded', 'false');
	}
	plegar.addEventListener('click', () => {
		const p = panel.toggleAttribute('data-plegado');
		plegar.setAttribute('aria-expanded', String(!p));
		plegar.textContent = p ? 'Abrir' : 'Plegar';
	});
	alAnimar((r: Registro) => {
		const li = document.createElement('li');
		li.innerHTML = `<b></b> <span class="t"></span><br><span></span>`;
		li.children[0].textContent = r.etiqueta || r.elemento.tagName.toLowerCase();
		li.children[1].textContent = `${Math.round(r.duracion)} ms${r.reducido ? ' · reducido' : ''}`;
		li.children[3].textContent = r.tokens;
		lista.prepend(li);
		while (lista.children.length > 30) lista.lastChild!.remove();
		if (resaltar && r.duracion > 0) {
			r.elemento.classList.add('kino-resaltado');
			setTimeout(() => r.elemento.classList.remove('kino-resaltado'), r.duracion / obtenerVelocidad());
		}
	});
	const contar = () => {
		vivas.textContent = `${animacionesVivas().length} en curso`;
		requestAnimationFrame(contar);
	};
	contar();
}
