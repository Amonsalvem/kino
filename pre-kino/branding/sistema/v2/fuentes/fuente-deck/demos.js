/* Demostraciones del sistema de movimiento. Leen curvas y duraciones de los tokens
   (--kino-movimiento-*) para que lo que se ve sea exactamente lo que se especifica. */
(function(){
  const reducido = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const tok = (n) => getComputedStyle(document.documentElement).getPropertyValue('--kino-movimiento-' + n).trim();
  const curva = (n) => tok('curva-' + n) || 'ease';
  const ms = (n) => parseFloat(tok('duracion-' + n)) || 400;
  const anima = (el, frames, o) => reducido ? null : el.animate(frames, { fill: 'both', ...o });

  document.querySelectorAll('.curva').forEach((b) => {
    b.addEventListener('click', () => {
      const bola = b.querySelector('.pista-c b'), pista = b.querySelector('.pista-c');
      const d = pista.clientWidth - bola.offsetWidth - 6;
      anima(bola, [{ transform: 'translateX(0)' }, { transform: `translateX(${d}px)` }],
        { duration: +b.dataset.ms, easing: `cubic-bezier(${b.dataset.curva})` });
    });
  });

  const est = (el, e, t) => { el.dataset.e = e; el.textContent = t; };
  const escenas = {
    cascada(s){ [...s.children].forEach((c, i) => anima(c, [{ opacity: 0, transform: 'translateY(26px) scale(.965)' }, { opacity: 1, transform: 'none' }],
      { duration: ms('tarjeta'), delay: i * 90, easing: curva('crecer') })); },
    filas(s){ [...s.children].forEach((c, i) => anima(c, [{ opacity: 0, transform: 'translateX(-22px)' }, { opacity: 1, transform: 'none' }],
      { duration: 620, delay: i * 55, easing: curva('crecer') })); },
    texto(s){ anima(s.firstElementChild, [{ opacity: 0, transform: 'translateY(14px)', filter: 'blur(6px)' }, { opacity: 1, transform: 'none', filter: 'blur(0)' }],
      { duration: ms('tarjeta'), easing: curva('crecer') }); },
    otorgar(s){ const p = s.querySelector('.mini-pase'); est(p.querySelector('.est'), 'sin-confirmar', 'Sin confirmar');
      p.className = 'mini-pase sc';
      anima(p, [{ opacity: 0, transform: 'translateY(18px) scale(.94)' }, { opacity: 1, transform: 'none' }], { duration: ms('crecer'), easing: curva('crecer') }); },
    confirmar(s){ const p = s.querySelector('.mini-pase'), e = p.querySelector('.est');
      p.className = 'mini-pase sc'; est(e, 'sin-confirmar', 'Sin confirmar');
      setTimeout(() => { p.className = 'mini-pase vivo'; est(e, 'vigente', 'Vigente');
        anima(e, [{ transform: 'scale(.85)' }, { transform: 'scale(1)' }], { duration: 420, easing: 'cubic-bezier(.34,1.56,.64,1)' });
        e.classList.remove('relatir'); void e.offsetWidth; }, reducido ? 0 : 900); },
    caducar(s){ const p = s.querySelector('.mini-pase'), e = p.querySelector('.est'), b = p.querySelector('.ventana i');
      p.className = 'mini-pase vivo'; est(e, 'por-vencer', '40 min'); b.style.right = '60%';
      const a = anima(b, [{ right: '60%' }, { right: '100%' }], { duration: ms('decaer') * 1.6, easing: curva('decaer') });
      const fin = () => { p.className = 'mini-pase'; est(e, 'vencido', 'Vencido');
        anima(p, [{ opacity: 1 }, { opacity: .62 }], { duration: ms('decaer'), easing: curva('decaer') }); };
      a ? a.finished.then(fin) : fin(); },
    revocar(s){ const p = s.querySelector('.mini-pase'), e = p.querySelector('.est');
      p.className = 'mini-pase vivo'; est(e, 'vigente', 'Vigente'); p.style.opacity = '';
      setTimeout(() => { anima(p, [{ transform: 'translateX(0)' }, { transform: 'translateX(-6px)' }, { transform: 'none' }], { duration: 240, easing: curva('revocar') });
        p.className = 'mini-pase'; est(e, 'negado', 'Negado'); }, reducido ? 0 : 500); },
  };
  document.querySelectorAll('[data-rep]').forEach((b) => {
    const s = document.querySelector(`[data-demo="${b.dataset.rep}"]`);
    b.addEventListener('click', () => escenas[b.dataset.rep]?.(s));
  });
  /* Cada escena corre una vez cuando su lámina entra. */
  const vistas = new WeakSet();
  const io = new IntersectionObserver((es) => es.forEach((x) => {
    if (!x.isIntersecting || vistas.has(x.target)) return;
    vistas.add(x.target); const k = x.target.dataset.demo;
    setTimeout(() => escenas[k]?.(x.target), 900);
  }), { threshold: .6 });
  document.querySelectorAll('[data-demo]').forEach((s) => io.observe(s));
})();
