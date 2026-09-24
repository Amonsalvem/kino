/* Kino · sistema de movimiento (v2, 23 sep 2026)
   Una capa semántica sobre el motor (Motion Playground, `window.__motion`) y la Web Animations API.
   Los valores salen de los tokens --kino-movimiento-* (tokens/40-movimiento.tokens.json): aquí no hay
   números sueltos. Cada verbo significa algo y no se usa para otra cosa:
     aparecer  → algo nuevo llega (crecer)
     confirmar → el lector respondió: sin-confirmar pasa a vigente, y el punto late
     caducar   → la vigencia se agota sola (decaer, lento)
     revocar   → alguien cortó el pase (corte seco, 240 ms)
     cascada   → los ítems de una lámina entran uno por uno
   Con «reducir movimiento» todo salta a su estado final. Solo transform, opacity y filter. */
(function (global) {
  'use strict';
  const raiz = document.documentElement;
  const reducido = () => matchMedia('(prefers-reduced-motion: reduce)').matches;
  const leer = (n) => getComputedStyle(raiz).getPropertyValue('--kino-movimiento-' + n).trim();
  const ms = (n) => parseFloat(leer('duracion-' + n)) || 0;
  const curva = (n) => leer('curva-' + n) || 'ease';
  const px = (n) => parseFloat(leer('distancia-' + n)) || 0;
  const cb = (s) => (s.match(/cubic-bezier\(([^)]+)\)/) || [, ''])[1].split(',').map(Number);

  /* Registra las curvas y duraciones de Kino en el motor, para que M.animate('crecer') use lo mismo. */
  function registrarEnMotor(M = global.__motion) {
    if (!M || !M.definirTokens) return false;
    const nombres = ['crecer', 'decaer', 'latir', 'cortina', 'revocar'];
    M.definirTokens({
      duracion: Object.fromEntries(['instante', 'corto', 'crecer', 'tarjeta', 'decaer', 'trazo', 'cortina', 'latir'].map((n) => [n, ms(n)])),
      curva: Object.fromEntries(nombres.map((n) => [n, cb(curva(n))])),
      escalonado: parseFloat(leer('escalonado-tarjetas')) || 90,
      recorrido: px('subida') || 26,
    });
    return true;
  }

  const animar = (el, frames, o) => {
    if (!el) return null;
    if (reducido()) { const f = frames[frames.length - 1]; Object.assign(el.style, f); return null; }
    return el.animate(frames, { fill: 'backwards', ...o });
  };
  const fijarEstado = (chip, estado, texto) => { if (!chip) return; chip.dataset.e = estado; if (texto) chip.textContent = texto; };

  const K = {
    registrarEnMotor,
    aparecer(el, { retardo = 0 } = {}) {
      return animar(el, [{ opacity: 0, transform: `translateY(${px('subida') * .7}px) scale(.94)` }, { opacity: 1, transform: 'none' }],
        { duration: ms('crecer'), delay: retardo, easing: curva('crecer') });
    },
    cascada(contenedor, { selector = ':scope > *', retardo = 0 } = {}) {
      const items = [...contenedor.querySelectorAll(selector)];
      const paso = Math.min(parseFloat(leer('escalonado-tarjetas')) || 90, 520 / Math.max(items.length, 1));
      return items.map((it, i) => animar(it, [{ opacity: 0, transform: `translateY(${px('subida')}px) scale(.965)` }, { opacity: 1, transform: 'none' }],
        { duration: ms('tarjeta'), delay: retardo + i * paso, easing: curva('crecer') }));
    },
    filas(tabla, { retardo = 0 } = {}) {
      const filas = [...tabla.querySelectorAll('tbody > tr')];
      const paso = parseFloat(leer('escalonado-filas')) || 55;
      return filas.map((f, i) => animar(f, [{ opacity: 0, transform: 'translateX(-22px)' }, { opacity: 1, transform: 'none' }],
        { duration: 620, delay: retardo + i * paso, easing: curva('crecer') }));
    },
    /* El pase nace «sin confirmar»; cuando el lector responde, pasa a «vigente» y su punto late tres ciclos. */
    confirmar(chip, { texto = 'Vigente' } = {}) {
      fijarEstado(chip, 'vigente', texto);
      chip.classList.remove('relatir'); void chip.offsetWidth; // reinicia los tres latidos
      return animar(chip, [{ transform: 'scale(.85)' }, { transform: 'scale(1)' }], { duration: ms('corto') * 1.75, easing: 'cubic-bezier(.34,1.56,.64,1)' });
    },
    /* Caducar: la barra de vigencia se vacía despacio y el estado se apaga. Más lento que revocar a propósito. */
    caducar({ barra, chip, tarjeta } = {}) {
      const a = barra ? animar(barra, [{ transform: 'scaleX(1)', transformOrigin: 'left' }, { transform: 'scaleX(0)', transformOrigin: 'left' }],
        { duration: ms('decaer') * 1.6, easing: curva('decaer'), fill: 'forwards' }) : null;
      const fin = () => { fijarEstado(chip, 'vencido', 'Vencido');
        if (tarjeta) animar(tarjeta, [{ opacity: 1 }, { opacity: .62 }], { duration: ms('decaer'), easing: curva('decaer'), fill: 'forwards' }); };
      a ? a.finished.then(fin) : fin();
      return a;
    },
    /* Revocar: corte seco, y el estado pasa a «negado» con el motivo escrito. */
    revocar({ chip, tarjeta, texto = 'Negado' } = {}) {
      fijarEstado(chip, 'negado', texto);
      return animar(tarjeta || chip, [{ transform: 'translateX(0)' }, { transform: 'translateX(-6px)' }, { transform: 'none' }],
        { duration: ms('corto'), easing: curva('revocar') });
    },
    /* Cortina de entrada del deck: costura de acento y dos hojas que se abren (solo transform). */
    cortina(el = document.getElementById('cortina')) {
      if (!el || reducido()) { el && (el.hidden = true); return Promise.resolve(); }
      const [a, b] = el.querySelectorAll('i'), costura = el.querySelector('b');
      const c = costura.animate([{ transform: 'scaleX(0)', opacity: 0 }, { transform: 'scaleX(1)', opacity: 1 }], { duration: ms('crecer'), easing: curva('crecer'), fill: 'forwards' });
      return c.finished.then(() => Promise.all([
        a.animate([{ transform: 'none' }, { transform: 'translateY(calc(-100% - 22vh))' }], { duration: ms('cortina'), easing: curva('cortina'), fill: 'forwards' }).finished,
        b.animate([{ transform: 'none' }, { transform: 'translateY(calc(100% + 22vh))' }], { duration: ms('cortina'), easing: curva('cortina'), fill: 'forwards' }).finished,
        costura.animate([{ opacity: 1 }, { opacity: 0 }], { duration: ms('crecer'), fill: 'forwards' }).finished,
      ])).finally(() => { el.hidden = true; });
    },
    tokens: () => ({ ms, curva, px }),
  };
  global.KinoMovimiento = K;
  if (global.__motion) registrarEnMotor(global.__motion);
})(window);
