#!/usr/bin/env python3
"""Genera los componentes y secciones del manual v2 (Design System artifact) desde las mismas piezas del deck."""
import re, json, sys, os
M = sys.argv[1]
sprite_full = open('sprite.svg').read()
def sprite(ids):
    syms = ''.join(re.search(r'<symbol id="i-%s"[\s\S]*?</symbol>' % i, sprite_full).group(0) for i in ids)
    return f'<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{syms}</defs></svg>'
def ic(i, cls='ic'): return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{i}"/></svg>'
BASE = ('<style>body{margin:0;padding:24px;background:var(--kino-superficie-base);color:var(--kino-texto-primario);'
        'font-family:var(--sans);font-size:17px;line-height:1.5}</style>')
def escribir(ruta, txt):
    os.makedirs(os.path.dirname(M + '/' + ruta), exist_ok=True)
    open(M + '/' + ruta, 'w').write(txt)

# ── Estado ──
escribir('components/Estado/preview.html', f'''<!-- @dsCard group="Estados" height=220 subtitle="Los seis estados del pase" -->
{BASE}
<div class="rej r3" style="gap:12px 22px">
<div class="par-est"><span class="est" data-e="vigente">Vigente</span><span class="peq">El lector confirmó el pase.</span></div>
<div class="par-est"><span class="est" data-e="por-vencer">Vence en 40 min</span><span class="peq">Dentro de la ventana de aviso.</span></div>
<div class="par-est"><span class="est" data-e="vencido">Vencido</span><span class="peq">Caducó solo.</span></div>
<div class="par-est"><span class="est" data-e="negado">Negado</span><span class="peq">Con motivo y autor.</span></div>
<div class="par-est"><span class="est" data-e="sin-confirmar">Sin confirmar</span><span class="peq">La puerta aún no responde.</span></div>
<div class="par-est"><span class="est" data-e="identidad">Dato personal</span><span class="peq">Zona regulada por la SIC.</span></div>
</div>
''')
escribir('components/Estado/README.md', '''# Estado

La etiqueta que dice en qué punto de su vida está un pase. El diagnóstico de septiembre encontró que la app no tiene lenguaje de estado y que afirma cosas del mundo físico que el lector nunca confirmó; este componente es la respuesta.

## Qué provee el consumidor

Un `<span class="est">` con `data-e` y la palabra visible. La palabra es obligatoria: el color nunca viaja solo.

```html
<span class="est" data-e="por-vencer">Vence en 40 min</span>
```

## Los seis estados

| `data-e` | Significa | Regla |
|---|---|---|
| `vigente` | Pase vivo, sincronizado y confirmado por el lector | El único punto que late, tres ciclos (WCAG 2.2.2) |
| `por-vencer` | Dentro de la ventana de aviso que fijó la administración | El texto dice cuánto queda, no «pronto» |
| `vencido` | Caducó solo | Sin color propio: un final no es un error |
| `negado` | Fuera de ventana, de límites o revocado | Dice el motivo y quién lo revocó |
| `sin-confirmar` | La app no sabe todavía qué pasó en la puerta | Sin relleno, borde discontinuo |
| `identidad` | Dato personal o biométrico a la vista | Marca la zona regulada por la SIC |

## Reglas

- `sin-confirmar` no es un estado de carga: es la respuesta honesta mientras HikCentral no confirme.
- No se inventan estados intermedios («en revisión», «pendiente de aprobación»): el sistema no tiene cola de aprobación.
- Un estado nunca se distingue solo por matiz.
- El acento no es un estado. Es la acción de otorgar.
- Para reiniciar los tres latidos cuando una vista entra, quitar y volver a poner la clase `relatir` (lo hace `KinoMovimiento.confirmar`).
''')

# ── Pase ──
boleto = f'''<div class="boleto" role="img" aria-label="Pase: autor, motivo, vigencia y modo"><div class="cab"><b>PASE</b><span class="est" data-e="vigente">Vigente</span></div>
<dl><dt>Autor</dt><dd>Ana Ruiz · casa 14</dd><dt>Motivo</dt><dd>Trabajo doméstico</dd>
<dt>Vigencia</dt><dd><div class="ventana"><i></i></div><div class="ventana-pie"><span>lun 07:00</span><span>vie 17:00 · caduca solo</span></div></dd>
<dt>Modo</dt><dd><div class="modos"><span>{ic('carro')}placa</span><span>{ic('qr')}QR</span><span>{ic('codigo')}código</span></div></dd></dl>
<div class="pie-b">{ic('sinpersona')}No crea una persona en la puerta</div></div>'''
escribir('components/Pase/preview.html', f'''<!-- @dsCard group="Pase" height=460 subtitle="El objeto del sistema: boleto y tarjeta de lista" -->
{BASE}{sprite(['carro','qr','codigo','sinpersona'])}
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:28px;align-items:start;max-width:980px">
{boleto}
<div style="display:grid;gap:10px">
<div class="mini-pase vivo"><div class="f1"><b>Marta Quintero</b><span class="est" data-e="vigente">Vigente</span></div><div class="f2">trabajo doméstico · lun–vie · 07:00–17:00</div><div class="ventana"><i style="left:0;right:22%"></i></div></div>
<div class="mini-pase sc"><div class="f1"><b>Técnico de gas</b><span class="est" data-e="sin-confirmar">Sin confirmar</span></div><div class="f2">hoy · 14:00–16:00 · enviado al lector</div></div>
<div class="mini-pase"><div class="f1"><b>Placa HTK 481</b><span class="est" data-e="por-vencer">40 min</span></div><div class="f2">visita · entró 13:12</div><div class="ventana"><i style="left:0;right:86%;background:var(--pv-bd)"></i></div></div>
<div class="mini-pase" style="opacity:.62"><div class="f1"><b>Visita del sábado</b><span class="est" data-e="vencido">Vencido</span></div><div class="f2">venció el 14 sep · 22:00</div></div>
</div></div>
''')
escribir('components/Pase/README.md', '''# Pase

El objeto que recibe un invitado o colaborador: autor, motivo, vigencia y modo, con una prohibición (no crea una persona). Es la unidad del producto y la pieza más reconocible de la marca. Un pase no es una cuenta: la cuenta la tiene el residente.

## Qué provee el consumidor

Dos formas del mismo objeto. El **boleto** (`.boleto`) es la ilustración: presentaciones, onboarding, material de venta. La **tarjeta de lista** (`.mini-pase`) es la pieza de producto.

```html
<div class="mini-pase vivo">
  <div class="f1"><b>Marta Quintero</b><span class="est" data-e="vigente">Vigente</span></div>
  <div class="f2">trabajo doméstico · lun–vie · 07:00–17:00</div>
  <div class="ventana"><i style="left:0;right:22%"></i></div>
</div>
```

Variantes de la tarjeta: `.vivo` (vigente, lleva `kino-resplandor-vigente`), `.sc` (sin confirmar: sin relleno, borde punteado), sin clase (resto de estados).

## Reglas

- Los cuatro atributos son obligatorios. Sin autor no hay constancia; sin vigencia no hay pase.
- La forma del boleto (muescas laterales, punteado bajo la cabecera, borde de acento) es exclusiva del pase.
- El pase nace `sin-confirmar` y pasa a `vigente` cuando la puerta responde (`KinoMovimiento.confirmar`).
- El residente y la portería ven el mismo objeto. En portería, cédula y teléfono van truncados y con `identidad`.
- Solo la tarjeta vigente resplandece: si todo resplandece, nada resplandece.
''')

# ── Vigencia ──
escribir('components/Vigencia/preview.html', f'''<!-- @dsCard group="Pase" height=240 subtitle="La vida que le queda a un pase" -->
{BASE}
<ul style="list-style:none;margin:0;padding:0;display:grid;gap:18px;max-width:560px">
<li><div style="display:flex;justify-content:space-between;align-items:baseline"><b>Marta Quintero · empleada</b><span class="kino-dato" style="font-size:13px;color:var(--tx3)">quedan 4 d 6 h</span></div><div class="ventana"><i style="left:0;right:22%"></i></div></li>
<li><div style="display:flex;justify-content:space-between;align-items:baseline"><b>Técnico de gas</b><span class="kino-dato" style="font-size:13px;color:var(--pv-tx)">quedan 40 min</span></div><div class="ventana"><i style="left:0;right:86%;background:var(--pv-bd)"></i></div></li>
<li><div style="display:flex;justify-content:space-between;align-items:baseline"><b>Visita del sábado</b><span class="kino-dato" style="font-size:13px;color:var(--tx3)">venció el 14 sep · 22:00</span></div><div class="ventana"><i style="left:0;right:100%"></i></div></li>
</ul>
''')
escribir('components/Vigencia/README.md', '''# Vigencia

La barra que muestra cuánta vida le queda a un pase. El campo «Válido desde / hasta» ya existe en la base de datos para los vehículos y está oculto para el dueño; esta pieza lo hace visible.

## Qué provee el consumidor

Un `.ventana` con un `<i>` cuyo `left` y `right` marcan el tramo vigente. Encima, el tiempo restante en `kino-dato`.

```html
<div class="ventana"><i style="left:0;right:86%;background:var(--pv-bd)"></i></div>
```

## Reglas

- La barra nunca va sola: una barra al 14 % no dice si son 40 minutos o 4 días.
- El aviso de «por vencer» lo decide la regla del conjunto; el componente solo lo pinta (ámbar).
- Un pase sin vigencia no existe. Un dato heredado sin fecha de fin se muestra `sin-confirmar` y se pide la fecha.
- Se vacía con `decaer` (900 ms, lento): caducar y ser revocado no se mueven igual (`KinoMovimiento.caducar`).
''')

# ── Tarjeta ──
escribir('components/Tarjeta/preview.html', f'''<!-- @dsCard group="Información" height=420 subtitle="Tarjeta, cifra, medidor, anillo, aviso y destacado" -->
{BASE}{sprite(['persona','edificio'])}
<div class="rej r4" style="margin-bottom:14px">
<div class="tj"><span class="cifra">312</span><p class="peq">personas registradas</p><div class="medidor"><i style="--v:0"></i></div><p class="medidor-pie">0 sincronizadas con la puerta</p></div>
<div class="tj"><span class="cifra">888</span><p class="peq">comunidad vecina</p><div class="medidor fuerte"><i style="--v:1"></i></div></div>
<div class="tj"><div class="anillos"><div class="anillo"><svg viewBox="0 0 36 36"><circle class="pista" cx="18" cy="18" r="15.9"/><circle class="arco" cx="18" cy="18" r="15.9" pathLength="100" stroke-dasharray="47.9 100"/></svg><div><b>47,9 %</b><span>Colombia</span></div></div></div></div>
<div class="tj acento"><p class="rol">Acento</p><h3>Lo que se propone</h3><p class="peq">Solo para la acción de otorgar o lo que la propuesta crea.</p></div>
</div>
<div class="rej r3">
<div class="aviso"><strong>Aviso.</strong> Una restricción que ordena lo demás. Ámbar, nunca rojo.</div>
<div class="destacado">Destacado: la conclusión que sostiene la vista.</div>
<div class="tj"><p class="rol">Chips</p><div style="display:flex;gap:8px;flex-wrap:wrap"><span class="chip-q">{ic('persona')}El cliente</span><span class="chip-q">{ic('edificio')}La administración</span><span class="chip-app">Permitido</span></div></div>
</div>
''')
escribir('components/Tarjeta/README.md', '''# Tarjeta

La superficie de información de Kino: membrana con relieve (`.tj`). Encima van cifras, medidores, anillos y chips. Las piezas vienen de la entrega 2.

## Qué provee el consumidor

```html
<div class="tj"><span class="cifra">312</span><p class="peq">personas registradas</p>
  <div class="medidor"><i style="--v:0"></i></div><p class="medidor-pie">0 sincronizadas con la puerta</p></div>
```

| Pieza | Clase | Cuándo |
|---|---|---|
| Tarjeta | `.tj` · `.tj.acento` | Toda agrupación. Acento solo para lo que otorga o se propone |
| Cifra | `.cifra` | Una cifra con su denominador («0 / 312»), nunca sola |
| Medidor | `.medidor > i` con `--v` (0–1) | Proporción de una cifra |
| Anillo | `.anillo` | Proporción de un todo |
| Puntos | `.puntos > i.si` | Avance contable (5 de 10) |
| Chip | `.chip-q`, `.chip-app`, `.alerta-l` | Quién responde, lo que dice la app, una alerta |
| Aviso | `.aviso` | Restricción o riesgo. Ámbar |
| Destacado | `.destacado` | La conclusión de la vista |

## Reglas

- No todo es una tarjeta: la tabla, la glosa y el pie van sin caja.
- En decks, cada `.tj` recibe foco de luz e inclinación de 4° al pasar el puntero (solo puntero fino y sin «reducir movimiento»).
- Rojo solo significa negado. Un aviso es ámbar.
''')

# ── Evidencia ──
escribir('components/Evidencia/preview.html', f'''<!-- @dsCard group="Idioma" height=260 subtitle="El grado de cada afirmación y su fuente" -->
{BASE}
<div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:18px"><span class="evid" data-g="observado">Observado</span><span class="evid" data-g="prueba">Prueba</span><span class="evid" data-g="entorno">Entorno</span><span class="evid" data-g="inferido">Inferido</span><span class="evid" data-g="abierto">Abierto</span></div>
<div class="rej r2" style="max-width:900px">
<div class="tj"><h3>Una placa inventada quedó «Permitido» al instante</h3><p class="peq">Se sincronizó con el sistema físico de acceso.</p><span class="evid" data-g="prueba">Prueba ejecutada</span><span class="fuente">inspección, sujeto 2 · 15 sep 2026</span></div>
<div class="tj"><h3>El 51,3 % de los contratos domésticos es por días</h3><p class="peq">El vínculo es intermitente.</p><span class="evid" data-g="entorno">Entorno</span><span class="fuente">DANE-GEIH vía Infobae · 9 sep 2026</span></div>
</div>
''')
escribir('components/Evidencia/README.md', '''# Evidencia

El rótulo que dice qué tan segura es una afirmación y de dónde sale. Es la regla 1 del proyecto (jerarquía de evidencia) convertida en componente, y lo que hace que Kino hable como una investigación.

## Qué provee el consumidor

```html
<span class="evid" data-g="prueba">Prueba ejecutada</span>
<span class="fuente">inspección, sujeto 2 · 15 sep 2026</span>
```

| `data-g` | Significa | Forma |
|---|---|---|
| `observado` | Lo vimos en la pantalla o en el sistema | Punto lleno, verde vigente |
| `prueba` | Lo provocamos y registramos el resultado | Rombo, acento |
| `entorno` | Fuente externa citada | Punto, índigo |
| `inferido` | Conclusión nuestra | Punteado, ámbar |
| `abierto` | Depende de una respuesta que no tenemos | Punteado, violeta, «?» |

## Reglas

- Toda afirmación de diagnóstico lleva grado y fuente. Sin fuente no se publica.
- La forma cambia con el grado, no solo el color.
- `.fuente` va en mono, con el archivo o la referencia exacta y la fecha.
''')

# ── Flujo ──
nodos = [('Inicio y fin','<rect x="2" y="8" width="116" height="36" rx="18" fill="var(--membrana)" stroke="var(--bd-def)" stroke-width="1.6"/>'),
 ('Paso o pantalla','<rect x="2" y="8" width="116" height="36" rx="4" fill="var(--elevada)" stroke="var(--bd-def)" stroke-width="1.6"/>'),
 ('Decisión','<polygon points="60,4 118,26 60,48 2,26" fill="var(--pv-bg)" stroke="var(--pv-bd)" stroke-width="1.8"/>'),
 ('Camino alterno','<path d="M4 26 H104" stroke="var(--bd-def)" stroke-width="2" stroke-dasharray="6 5" fill="none"/><path d="M102 20 L116 26 L102 32 z" fill="var(--bd-def)"/>'),
 ('Estado del sistema','<rect x="2" y="8" width="116" height="36" rx="4" fill="none" stroke="var(--bd-def)" stroke-width="1.6" stroke-dasharray="6 4"/>'),
 ('Meta lograda','<rect x="2" y="8" width="116" height="36" rx="18" fill="var(--v-bg)" stroke="var(--v-bd)" stroke-width="2"/>'),
 ('Meta no lograda','<rect x="2" y="8" width="116" height="36" rx="18" fill="var(--ng-bg)" stroke="var(--ng-bd)" stroke-width="2"/>'),
 ('Otorgar','<rect x="2" y="8" width="116" height="36" rx="4" fill="var(--ac-sordo)" stroke="var(--ac)" stroke-width="2"/>'),
 ('Pregunta abierta','<rect x="2" y="8" width="116" height="36" rx="4" fill="none" stroke="var(--id-bd)" stroke-width="1.6" stroke-dasharray="7 5"/><text x="60" y="31" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="14" fill="var(--id-tx)">?</text>')]
escribir('components/Flujo/preview.html', f'''<!-- @dsCard group="Diagramas" height=300 subtitle="Las nueve formas de un lienzo de flujo" -->
{BASE}
<div class="nodos">{''.join(f'<div class="nodo-m"><svg viewBox="0 0 120 52" aria-hidden="true">{s}</svg><div><h3>{t}</h3></div></div>' for t, s in nodos)}</div>
''')
escribir('components/Flujo/README.md', '''# Flujo

La gramática de los lienzos de recorrido: nueve formas con un significado fijo. Viene de las láminas 13 a 23 de la entrega 2 y es la forma en que Kino muestra cómo se mueve una persona por el sistema.

## Las formas

| Forma | Significa | Especificación |
|---|---|---|
| Inicio y fin | El segundo 0 y el punto donde termina | Píldora, `rx` = alto/2, membrana |
| Paso o pantalla | Una pantalla real o un acto del mundo | Rectángulo `rx` 4, elevada |
| Decisión | Bifurcación; debajo va la evidencia | Rombo ámbar (`--pv-*`) |
| Camino alterno | Por donde suele pasar el volumen hoy | Trazo 6 · 5 |
| Estado del sistema | Lo que el producto afirma | Punteado 6 · 4, sin relleno |
| Meta lograda | Llega a donde tenía que llegar | Píldora vigente |
| Meta no lograda | Termina fuera o con costo | Píldora negado |
| Otorgar | El acto que crea el pase | Rectángulo acento. Lo único con acento |
| Pregunta abierta | Depende de una respuesta pendiente | Punteado violeta con «?» |

## Reglas

- Debajo de cada caja va, en mono de 10–11 px, de dónde sale lo que afirma: pantalla, prueba o fuente.
- El lienzo va en `.lienzo` con `data-zoom`: clic para ampliar.
- En decks, los elementos entran de izquierda a derecha según su x y los trazos se dibujan (`data-traza`). Lo punteado solo se funde.
- En teléfono, el lienzo se desliza de lado; la página nunca.
''')

# ── Tabla ──
escribir('components/Tabla/preview.html', f'''<!-- @dsCard group="Información" height=240 subtitle="Tabla y matriz de capacidades" -->
{BASE}{sprite(['cruz','check'])}
<table class="cap5" style="max-width:900px"><thead><tr><th>Capacidad</th><th>Residente</th><th>Portero</th><th>Admin</th><th>Super admin</th></tr></thead><tbody>
<tr class="nadie"><td>Anunciar un visitante para una fecha</td><td class="c">{ic('cruz')}Nadie</td><td class="c">{ic('cruz')}Nadie</td><td class="c">{ic('cruz')}Nadie</td><td class="c">{ic('cruz')}Nadie</td></tr>
<tr><td>Dar de alta una persona</td><td class="c no">No</td><td class="c no">No</td><td class="c si">{ic('check')}Sí</td><td class="c si">{ic('check')}Sí</td></tr>
<tr><td>Ver la vigencia del pase</td><td class="c no">No</td><td class="c si">{ic('check')}Sí</td><td class="c si">{ic('check')}Sí</td><td class="c si">{ic('check')}Sí</td></tr>
</tbody></table>
''')
escribir('components/Tabla/README.md', '''# Tabla

Tablas y la matriz de capacidades de la entrega 2: se leen en vertical, y la fila que nadie puede cumplir es el hallazgo.

## Qué provee el consumidor

`<table>` normal; `.cap5` para la matriz de cinco columnas; `tr.nadie` para la fila que nadie cumple; `td.c.si` / `td.c.no` para las celdas; `td.k` para una clave en mono y acento.

## Reglas

- Encabezados en mono, mayúsculas, tenues, con borde definido debajo.
- Cifras en mono y tabulares. Una columna numérica nunca se centra.
- La fila `nadie` se tiñe de negado y va en negrita.
- En teléfono, la tabla se desliza de lado dentro de su contenedor; la página no.
''')

# ── Movimiento ──
mov_js = open('kino-movimiento.js').read()
escribir('components/Movimiento/preview.html', f'''<!-- @dsCard group="Movimiento" height=330 subtitle="Otorgar, confirmar, caducar, revocar" -->
{BASE}
<div class="rej r4">
<div class="escena"><p class="rol">Otorgar · crecer</p><div class="escenario"><div class="mini-pase sc" id="m-otorgar" style="width:100%"><div class="f1"><b>Marta Q.</b><span class="est" data-e="sin-confirmar">Sin confirmar</span></div></div></div><button class="demo-rep" data-m="otorgar">▶ reproducir</button></div>
<div class="escena"><p class="rol">Confirmar · latir</p><div class="escenario"><div class="mini-pase sc" id="m-confirmar" style="width:100%"><div class="f1"><b>Marta Q.</b><span class="est" data-e="sin-confirmar">Sin confirmar</span></div></div></div><button class="demo-rep" data-m="confirmar">▶ reproducir</button></div>
<div class="escena"><p class="rol">Caducar · decaer</p><div class="escenario"><div class="mini-pase vivo" id="m-caducar" style="width:100%"><div class="f1"><b>Técnico</b><span class="est" data-e="por-vencer">40 min</span></div><div class="ventana"><i style="left:0;right:40%"></i></div></div></div><button class="demo-rep" data-m="caducar">▶ reproducir</button></div>
<div class="escena"><p class="rol">Revocar · corte</p><div class="escenario"><div class="mini-pase vivo" id="m-revocar" style="width:100%"><div class="f1"><b>HTK 481</b><span class="est" data-e="vigente">Vigente</span></div></div></div><button class="demo-rep" data-m="revocar">▶ reproducir</button></div>
</div>
<script>
{mov_js}
(function(){{
  const K = window.KinoMovimiento;
  const reset = {{
    otorgar(){{ const p=document.getElementById('m-otorgar'); K.aparecer(p); }},
    confirmar(){{ const p=document.getElementById('m-confirmar'), e=p.querySelector('.est'); p.className='mini-pase sc'; e.dataset.e='sin-confirmar'; e.textContent='Sin confirmar';
      setTimeout(()=>{{ p.className='mini-pase vivo'; K.confirmar(e); }}, 700); }},
    caducar(){{ const p=document.getElementById('m-caducar'), e=p.querySelector('.est'), b=p.querySelector('.ventana i'); p.className='mini-pase vivo'; p.style.opacity=''; e.dataset.e='por-vencer'; e.textContent='40 min';
      K.caducar({{ barra:b, chip:e, tarjeta:p }}); }},
    revocar(){{ const p=document.getElementById('m-revocar'), e=p.querySelector('.est'); p.className='mini-pase vivo'; e.dataset.e='vigente'; e.textContent='Vigente';
      setTimeout(()=>{{ p.className='mini-pase'; K.revocar({{ chip:e, tarjeta:p }}); }}, 500); }},
  }};
  document.querySelectorAll('[data-m]').forEach(b=>b.addEventListener('click',()=>reset[b.dataset.m]()));
}})();
</script>
''')
escribir('components/Movimiento/README.md', '''# Movimiento

`KinoMovimiento`: la capa semántica del sistema de movimiento. Cada verbo significa algo y no se usa para otra cosa. Los valores salen de los tokens `kino-movimiento-*`; el archivo es `branding/sistema/v2/kino-movimiento.js`.

## Qué provee el consumidor

Cargar el motor (Motion Playground) si se usa, y después `kino-movimiento.js`. Si el motor está, `KinoMovimiento.registrarEnMotor()` le pasa las curvas de Kino (`M.animate(el, …, {easing: 'crecer'})`).

```js
KinoMovimiento.aparecer(tarjeta);                       // crecer · 420 ms
KinoMovimiento.confirmar(chip);                         // sin-confirmar → vigente, tres latidos
KinoMovimiento.caducar({ barra, chip, tarjeta });       // decaer · 900 ms, lento a propósito
KinoMovimiento.revocar({ chip, tarjeta });              // corte · 240 ms, deja «Negado»
KinoMovimiento.cascada(contenedor);                     // ítems de una lámina, 90 ms entre sí
KinoMovimiento.cortina();                               // apertura del deck: costura 420 + hojas 1600
```

## Reglas

- Crecer es aparecer, decaer es caducar, latir es estar vivo, revocar es cortar. Nada se anima para decorar.
- Solo `transform`, `opacity` y `filter` (compositor). La cortina va por Web Animations, no por requestAnimationFrame.
- El latido se detiene a los tres ciclos (WCAG 2.2.2).
- Con «reducir movimiento», todo salta a su estado final sin transición.
''')
print('ok')
