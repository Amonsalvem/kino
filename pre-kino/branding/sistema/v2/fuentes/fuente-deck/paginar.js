/* Kino · paginación del deck (24 sep 2026)
   Un gesto de scroll = una lámina. La rueda, el trackpad, el gesto táctil y el teclado
   llevan a la lámina siguiente o a la anterior con la curva de la cortina.
   Si una lámina es más alta que la pantalla (tablas largas, teléfono), primero se
   recorre por dentro y el cambio de lámina llega con el siguiente gesto en el borde.
   En escritorio cada lámina se ajusta a la pantalla con `zoom` (hasta 0,68) antes de
   recurrir al scroll interno. Con «reducir movimiento» el cambio es instantáneo. */
(function () {
  'use strict';
  if (matchMedia('print').matches) return;
  const raiz = document.documentElement;
  const secs = [...document.querySelectorAll('main > section')];
  if (!secs.length) return;
  const barra = 46;
  const reducido = () => matchMedia('(prefers-reduced-motion: reduce)').matches;
  const escritorio = () => innerWidth >= 900 && innerHeight >= 560;

  raiz.classList.add('paginado');
  raiz.style.scrollBehavior = 'auto';

  let actual = 0, animando = false;
  const alto = () => innerHeight - barra;

  /* ── Ajuste a la pantalla ─────────────────────────────────────────────── */
  function ajustar() {
    const h = alto();
    raiz.style.setProperty('--alto-lamina', h + 'px');
    for (const s of secs) {
      const dentro = s.querySelector(':scope > .interior');
      if (!dentro) continue;
      dentro.style.zoom = ''; dentro.style.width = '';
      if (!escritorio() || s.classList.contains('plena')) continue;
      const cs = getComputedStyle(s);
      const disponible = h - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom);
      /* Se escala como una lámina: letra y ancho a la vez (con solo zoom, lo que
         depende del ancho, como un lienzo SVG, no se achica). Dos pasadas porque el
         alto final depende del reflujo. */
      let z = 1;
      for (let k = 0; k < 3; k++) {
        const alto = dentro.getBoundingClientRect().height;
        if (alto <= disponible - 2) break;
        z = Math.max(.68, z * (disponible - 3) / alto);
        dentro.style.zoom = z.toFixed(3);
        dentro.style.width = (100 * z).toFixed(2) + '%';
        if (z === .68) break;
      }
    }
    irA(actual, true);
  }

  /* ── Movimiento entre láminas ─────────────────────────────────────────── */
  const curva = (t) => (t < .5 ? 8 * t * t * t * t : 1 - Math.pow(-2 * t + 2, 4) / 2); // ≈ (.76,0,.24,1)
  function irA(i, instantaneo) {
    i = Math.max(0, Math.min(secs.length - 1, i));
    const destino = secs[i].offsetTop - barra;
    const cambio = i !== actual, atras = i < actual;
    actual = i;
    if (cambio) secs[i].scrollTop = atras ? secs[i].scrollHeight : 0;
    if (cambio) seguirNav(i);
    const entrar = () => { if (cambio && window.__kinoEntrar) window.__kinoEntrar(secs[i]); };
    if (instantaneo || reducido()) { scrollTo(0, destino); entrar(); return; }
    const origen = scrollY, d = destino - origen;
    if (!d) { entrar(); return; }
    const dur = Math.min(760, 420 + Math.abs(d) / alto() * 90);
    /* La coreografía de la lámina arranca al 45 % del recorrido, como la portada con la
       cortina: se ve completa en pantalla y no hay espera al llegar. */
    setTimeout(entrar, dur * .45);
    const t0 = performance.now();
    animando = true;
    (function paso(ahora) {
      const t = Math.min(1, (ahora - t0) / dur);
      scrollTo(0, origen + d * curva(t));
      if (t < 1) requestAnimationFrame(paso);
      else { animando = false; finAnim = performance.now(); }
    })(t0);
  }
  window.KinoPaginas = { irA, get actual() { return actual; }, total: secs.length };

  /* La barra de navegación se desplaza para mostrar el enlace de la lámina activa. */
  const nav = document.querySelector('.barra nav');
  function seguirNav(i) {
    const a = nav && nav.querySelector('a[data-i="' + i + '"]');
    if (!a) return;
    nav.scrollTo({ left: a.offsetLeft - nav.clientWidth / 2 + a.offsetWidth / 2, behavior: reducido() ? 'auto' : 'smooth' });
  }

  /* ¿La lámina puede seguir desplazándose por dentro en esa dirección? */
  const puede = (s, dir) => dir > 0 ? s.scrollTop + s.clientHeight < s.scrollHeight - 2 : s.scrollTop > 2;

  /* ── Rueda y trackpad ─────────────────────────────────────────────────────
     Un gesto es una racha de eventos sin pausas de más de 160 ms. Un gesto cambia
     como mucho una lámina, y solo si empezó en el borde: la inercia de recorrer una
     lámina larga no salta a la siguiente. */
  let ultimo = 0, gestoEnBorde = false, gestoUsado = false, gestoDir = 0, previo = 0, finAnim = 0;
  addEventListener('wheel', (ev) => {
    if (ev.ctrlKey || document.querySelector('.visor.abierto')) return;
    const dy = Math.abs(ev.deltaY) >= Math.abs(ev.deltaX) ? ev.deltaY : 0;
    if (!dy) return;
    const dir = Math.sign(dy), s = secs[actual], ahora = performance.now();
    /* Tras un cambio, la inercia del trackpad sigue llegando (y un hilo ocupado la
       espacia): se exige una pausa más larga o un impulso nuevo claramente más fuerte. */
    const umbral = animando || ahora - finAnim < 900 ? 360 : 170;
    const impulso = gestoUsado && !animando && Math.abs(dy) > 28 && Math.abs(dy) > previo * 1.8;
    const nuevo = ahora - ultimo > umbral || dir !== gestoDir || impulso;
    ultimo = ahora; previo = Math.abs(dy);
    if (nuevo) { gestoEnBorde = !puede(s, dir); gestoUsado = false; gestoDir = dir; }
    if (puede(s, dir) && !animando) return;              // scroll interno nativo
    ev.preventDefault();
    if (animando || gestoUsado || !gestoEnBorde || Math.abs(dy) < 4) return;
    gestoUsado = true;
    irA(actual + dir);
  }, { passive: false });

  /* ── Táctil ───────────────────────────────────────────────────────────── */
  let y0 = null, x0 = 0, bordeArriba = false, bordeAbajo = false;
  addEventListener('touchstart', (ev) => {
    if (ev.touches.length !== 1) { y0 = null; return; }
    const s = secs[actual];
    y0 = ev.touches[0].clientY; x0 = ev.touches[0].clientX;
    bordeArriba = !puede(s, -1); bordeAbajo = !puede(s, 1);
  }, { passive: true });
  addEventListener('touchend', (ev) => {
    if (y0 === null || animando) return;
    const t = ev.changedTouches[0], dy = y0 - t.clientY, dx = x0 - t.clientX;
    y0 = null;
    if (Math.abs(dy) < 48 || Math.abs(dx) > Math.abs(dy)) return;
    if (dy > 0 && bordeAbajo) irA(actual + 1);
    if (dy < 0 && bordeArriba) irA(actual - 1);
  }, { passive: true });

  /* ── Teclado ──────────────────────────────────────────────────────────── */
  addEventListener('keydown', (ev) => {
    if (ev.target.closest && ev.target.closest('input,textarea,select,[contenteditable="true"]')) return;
    if (document.querySelector('.visor.abierto')) return;
    const s = secs[actual];
    const k = ev.key;
    let dir = 0, interno = false;
    if (k === 'ArrowRight' || k === 'PageDown') dir = 1;
    else if (k === 'ArrowLeft' || k === 'PageUp') dir = -1;
    else if (k === 'ArrowDown' || (k === ' ' && !ev.shiftKey)) { dir = 1; interno = true; }
    else if (k === 'ArrowUp' || (k === ' ' && ev.shiftKey)) { dir = -1; interno = true; }
    else if (k === 'Home') { ev.preventDefault(); ev.stopImmediatePropagation(); irA(0); return; }
    else if (k === 'End') { ev.preventDefault(); ev.stopImmediatePropagation(); irA(secs.length - 1); return; }
    if (!dir) return;
    ev.preventDefault(); ev.stopImmediatePropagation();
    if (animando) return;
    if (interno && puede(s, dir)) { s.scrollBy({ top: dir * s.clientHeight * .8, behavior: reducido() ? 'auto' : 'smooth' }); return; }
    irA(actual + dir);
  }, true);

  /* ── Enlaces internos (barra de navegación y anclas) ──────────────────── */
  document.addEventListener('click', (ev) => {
    const a = ev.target.closest && ev.target.closest('a[href^="#"]');
    if (!a) return;
    const i = secs.findIndex((s) => '#' + s.id === a.getAttribute('href'));
    if (i < 0) return;
    ev.preventDefault();
    irA(i);
  });


  let espera;
  addEventListener('resize', () => { clearTimeout(espera); espera = setTimeout(ajustar, 120); });
  const inicio = secs.findIndex((s) => '#' + s.id === location.hash);
  actual = inicio > 0 ? inicio : 0;
  ajustar();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(ajustar);
})();
