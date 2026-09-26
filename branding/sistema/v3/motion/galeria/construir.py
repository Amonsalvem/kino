"""Galería de las piezas de motion: escribe galeria/index.html y galeria/archivos.json (ruta publicada → archivo).

    python3 construir.py

Los videos se publican junto a la página en entregables/<ruta>; se publica con root = motion/. Colores y tipos: tokens de Kino.
"""
import html
import json
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ENT = AQUI.parent / 'entregables'
T = json.loads((AQUI.parent / 'tokens.motion.json').read_text())['oscuro']
C = T['color']

REMOTION = [
    ('hero-ciclo-del-pase', 'Hero · ciclo del Pase', 'Se crea, se entrega, el lector lo confirma, entra en aviso y vence.', '16 / 9'),
    ('hero-ciclo-del-pase-movil', 'Hero móvil', 'El mismo ciclo en formato vertical.', '4 / 5'),
    ('composicion-revocado', 'Revocado', 'El residente corta el Pase y el lector lo rechaza en Portería.', '16 / 9'),
    ('composicion-turno-porteria', 'Turno de Portería', 'Las lecturas del lector entran como eventos; una es un rechazo.', '16 / 9'),
]
LOTTIE = [
    ('pase-aparecer', 'Aparecer', 'Nace como Previsto.'),
    ('pase-cascada', 'Cascada', 'Los Pases de la casa entran en orden.'),
    ('pase-confirmar', 'Confirmar', 'El lector lo confirma: sin confirmar pasa a vigente.'),
    ('pase-latir', 'Latir', 'Sigue vigente.'),
    ('pase-por-vencer', 'Por vencer', 'Entra en la ventana de aviso.'),
    ('pase-caducar', 'Caducar', 'Su vigencia se agota.'),
    ('pase-revocar', 'Revocar', 'Alguien lo corta antes de su hora.'),
    ('pase-usar', 'Usar', 'El código de un solo uso se gasta.'),
    ('entrada-rechazar', 'Rechazar', 'El lector no lo acepta en la puerta.'),
    ('pase-enviar', 'Enviar', 'El residente lo entrega a quien espera.'),
    ('control-presionar', 'Presionar', 'Tocar Crear Pase. Solo color, sin desplazamiento.'),
    ('presentacion-cortina', 'Cortina', 'Abre una lámina. Solo presentaciones.'),
    ('onboarding-1-crear', 'Onboarding 1 · Crear', 'Se crea como acceso previsto.'),
    ('onboarding-2-entregar', 'Onboarding 2 · Entregar', 'Se entrega sin que la visita cree cuenta.'),
    ('loader-sincronizacion-lote', 'Sincronización con el lector', 'Cada fila se confirma cuando el lector responde.'),
    ('vacio-primer-pase', 'Primer Pase', 'El primero reemplaza el estado vacío.'),
]
TRES_D = [
    ('pase-3d-objeto', 'aparecer', 'Pase 3D · aparecer', 'Entra en sin confirmar.'),
    ('pase-3d-objeto', 'confirmar', 'Pase 3D · confirmar', 'El borde discontinuo se cierra y queda vigente.'),
    ('pase-3d-objeto', 'latir', 'Pase 3D · latir', 'El punto de un Pase vigente respira.'),
    ('pase-3d-objeto', 'caducar', 'Pase 3D · caducar', 'La barra se vacía y el borde pasa a vencido.'),
    ('pase-3d-objeto', 'revocar', 'Pase 3D · revocar', 'Una línea cruza la tarjeta y la apaga.'),
    ('pase-3d-latir', '', 'Pase 3D en reposo', 'Confirmado, con la línea de evidencia; solo late el punto.'),
]
FALTAN = ['flujo-trazo', 'loader-espera-lector', 'onboarding-3-lector-confirma']

archivos = {}


def pub(rel):
    ruta = ENT / rel
    if not ruta.exists():
        return None
    archivos[f'entregables/{rel}'] = str(ruta.relative_to(AQUI.parents[4]))
    return f'entregables/{rel}'


def video(fuentes, clase='', poster=None, loop=True):
    srcs = ''.join(f'<source src="{s}" type=\'{t}\'>' for s, t in fuentes if s)
    p = f' poster="{poster}"' if poster else ''
    return f'<video class="{clase}" muted playsinline loop{p} preload="metadata">{srcs}</video>'


def tarjeta(titulo, que, completo, reducido, clase='', ratio=None):
    estilo = f' style="--ratio:{ratio}"' if ratio else ''
    return (f'<figure class="pieza {clase}"{estilo}><div class="marco" data-completo=\'{html.escape(completo)}\' '
            f'data-reducido=\'{html.escape(reducido)}\'>{completo}</div>'
            f'<figcaption><h3>{titulo}</h3><p>{que}</p></figcaption></figure>')


def seccion_remotion():
    out = []
    for id_, t, q, r in REMOTION:
        def v(red):
            n = f'{id_}-reducido' if red else id_
            return video([(pub(f'{id_}/{n}.av1.webm'), 'video/webm; codecs="av01.0.08M.08"'),
                          (pub(f'{id_}/{n}.h264.mp4'), 'video/mp4')], poster=pub(f'{id_}/{id_}.poster.avif'))
        out.append(tarjeta(t, q, v(False), v(True), 'ancha' if r == '16 / 9' else 'alta', r))
    return ''.join(out)


def seccion_lottie():
    out = []
    for id_, t, q in LOTTIE:
        v = lambda red: video([(pub(f'lottie-previews/{id_}{"-reducido" if red else ""}.webm'), 'video/webm'),  # noqa: E731
                               (pub(f'lottie-previews/{id_}{"-reducido" if red else ""}.mp4'), 'video/mp4')])
        out.append(tarjeta(t, q, v(False), v(True), 'cortina' if id_ == 'presentacion-cortina' else ''))
    return ''.join(out)


def seccion_3d():
    out = []
    for id_, clip, t, q in TRES_D:
        def v(red):
            n = id_ + ('.reducido' if red else '') + (f'.{clip}' if clip else '')
            return video([(pub(f'{id_}/{n}.alpha.mp4'), 'video/mp4; codecs="hvc1"'),
                          (pub(f'{id_}/{n}.alpha.webm'), 'video/webm')], 'alfa')
        out.append(tarjeta(t, q, v(False), v(True), 'tres-d'))
    n = 'conjunto-noche-lector-confirma'
    v = lambda red: video([(pub(f'{n}/{n}{".reducido" if red else ""}.vp9.webm'), 'video/webm'),  # noqa: E731
                           (pub(f'{n}/{n}{".reducido" if red else ""}.h264.mp4'), 'video/mp4')])
    out.append(tarjeta('Conjunto de noche', 'El indicador del lector pasa de sin confirmar a vigente. Nada más se mueve.',
                       v(False), v(True), 'ancha', '16 / 9'))
    return ''.join(out)


PAGINA = """<meta charset="utf-8">
<title>Motion de Kino</title>
<meta name="description" content="Galería de las piezas animadas de Kino.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;700;800&family=JetBrains+Mono:wght@400&display=swap">
<style>
:root{color-scheme:dark;
 --abismo:%(abismo)s;--base:%(base)s;--elevada:%(elevada)s;--membrana:%(membrana)s;
 --t1:%(t1)s;--t2:%(t2)s;--t3:%(t3)s;--acento:%(acento)s;--accion:%(accion)s;--accion-texto:%(accion_texto)s;
 --vig-f:%(vig_f)s;--vig-b:%(vig_b)s;--vig-t:%(vig_t)s;--sin-b:%(sin_b)s;--sin-t:%(sin_t)s;
 --r-tarjeta:14px;--r-control:8px;--r-chip:4px;
 --archivo:'Archivo',system-ui,sans-serif;--mono:'JetBrains Mono',ui-monospace,monospace}
body{background:var(--abismo);color:var(--t1);font-family:var(--archivo);font-size:15px;line-height:1.6}
.hoja{max-width:1180px;margin:0 auto;padding-inline:16px;padding-block:32px 72px;display:grid;gap:56px}
header{display:grid;gap:14px}
.marca{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--t3)}
h1{font-weight:800;font-size:clamp(34px,6vw,56px);line-height:1.04;letter-spacing:-.02em;margin:0;text-wrap:balance}
.bajada{color:var(--t2);max-width:62ch;margin:0}
.controles{display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.boton{font:700 14px/1 var(--archivo);border-radius:var(--r-control);padding:12px 16px;cursor:pointer;border:1px solid var(--membrana);background:var(--elevada);color:var(--t1)}
.boton[aria-pressed="true"]{background:var(--accion);color:var(--accion-texto);border-color:var(--accion)}
.boton:focus-visible{outline:2px solid var(--acento);outline-offset:2px}
.nota{font-family:var(--mono);font-size:12px;color:var(--t3)}
section{display:grid;gap:20px}
.cab{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:8px 20px;border-bottom:1px solid var(--membrana);padding-bottom:12px}
h2{font-weight:700;font-size:24px;margin:0}
.tecnica{font-family:var(--mono);font-size:12px;color:var(--t3)}
.rejilla{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%%,300px),1fr));gap:20px}
.rejilla.grande{grid-template-columns:repeat(auto-fill,minmax(min(100%%,520px),1fr))}
.pieza{margin:0;display:grid;gap:10px;align-content:start}
.pieza.ancha{grid-column:1/-1}
.pieza.alta .marco{max-width:440px}
.marco{border-radius:var(--r-tarjeta);overflow:hidden;background:var(--base);border:1px solid var(--elevada);aspect-ratio:var(--ratio,auto);max-width:100%%}
.marco video{display:block;width:100%%;height:100%%;object-fit:contain;background:var(--abismo)}
.tres-d .marco{background-color:var(--base);background-image:linear-gradient(45deg,var(--elevada) 25%%,transparent 25%%,transparent 75%%,var(--elevada) 75%%),linear-gradient(45deg,var(--elevada) 25%%,transparent 25%%,transparent 75%%,var(--elevada) 75%%);background-size:24px 24px;background-position:0 0,12px 12px}
.tres-d video{background:transparent}
figcaption h3{font-size:16px;font-weight:700;margin:0}
figcaption p{margin:2px 0 0;color:var(--t2);font-size:14px}
.chip{display:inline-flex;align-items:center;gap:6px;font:700 12px/1.3 var(--archivo);padding:3px 10px;border-radius:var(--r-chip);border:1px dashed var(--sin-b);color:var(--sin-t)}
.faltan{display:flex;flex-wrap:wrap;gap:8px;align-items:center;color:var(--t2);font-size:14px}
code{font-family:var(--mono);font-size:13px;color:var(--t2)}
@media (prefers-reduced-motion:reduce){.boton{transition:none}}
</style>
<div class="hoja">
<header>
 <span class="marca">Kino · sistema de marca · motion</span>
 <h1>Motion de Kino</h1>
 <p class="bajada">Cada pieza cuenta algo que le pasa a un Pase. Todas están en borrador, sin aprobar. Con el botón ves la variante de movimiento reducido: los desplazamientos pasan a fundidos y el latido se detiene.</p>
 <div class="controles">
  <button class="boton" id="reducido" type="button" aria-pressed="false">Movimiento reducido</button>
  <button class="boton" id="pausa" type="button" aria-pressed="false">Pausar todo</button>
  <span class="nota">60 fps · piezas en loop para revisarlas</span>
 </div>
</header>
<section>
 <div class="cab"><h2>Hero y composiciones</h2><span class="tecnica">Remotion · AV1 con respaldo H.264</span></div>
 <div class="rejilla grande">%(remotion)s</div>
</section>
<section>
 <div class="cab"><h2>Catálogo, onboarding, loader y vacío</h2><span class="tecnica">Lottie · vista previa mp4</span></div>
 <div class="rejilla">%(lottie)s</div>
 <p class="faltan"><span class="chip">Sin confirmar</span> Aún no existen: %(faltan)s. Esperan la curva de <code>trazo</code>.</p>
</section>
<section>
 <div class="cab"><h2>Escenas 3D</h2><span class="tecnica">Blender · VP9 y HEVC con alfa sobre damero</span></div>
 <div class="rejilla">%(tres_d)s</div>
</section>
</div>
<script>
(() => {
  const botonR = document.getElementById('reducido');
  const botonP = document.getElementById('pausa');
  let reducido = false, pausado = false;
  try { reducido = matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) {}
  const videos = () => document.querySelectorAll('.marco video');
  const reproducir = (v) => { if (!pausado) { const p = v.play(); if (p) p.catch(() => {}); } };
  const vista = new IntersectionObserver((es) => es.forEach((e) => e.isIntersecting ? reproducir(e.target) : e.target.pause()), {rootMargin: '120px'});
  // Alfa: Safari compone HEVC con alfa (hvc1); Chrome, Edge y Firefox, VP9 con alfa. Cada uno recibe solo el suyo.
  const ua = navigator.userAgent;
  const safari = /safari/i.test(ua) && !/chrome|chromium|crios|fxios|android|edg/i.test(ua);
  function pintar() {
    document.querySelectorAll('.marco').forEach((m) => {
      m.innerHTML = reducido ? m.dataset.reducido : m.dataset.completo;
      const v = m.querySelector('video');
      if (v && v.classList.contains('alfa')) {
        v.querySelectorAll('source').forEach((s) => { if (/hvc1/.test(s.type) !== safari) s.remove(); });
        v.load();
      }
      if (v) vista.observe(v);
    });
    botonR.setAttribute('aria-pressed', String(reducido));
  }
  botonR.addEventListener('click', () => { reducido = !reducido; pintar(); });
  botonP.addEventListener('click', () => {
    pausado = !pausado;
    botonP.setAttribute('aria-pressed', String(pausado));
    botonP.textContent = pausado ? 'Reanudar' : 'Pausar todo';
    videos().forEach((v) => pausado ? v.pause() : reproducir(v));
  });
  pintar();
})();
</script>
"""


def main():
    pagina = PAGINA % {
        'abismo': C['superficie/abismo'], 'base': C['superficie/base'], 'elevada': C['superficie/elevada'],
        'membrana': C['superficie/membrana'], 't1': C['texto/primario'], 't2': C['texto/secundario'], 't3': C['texto/tenue'],
        'acento': C['acento/base'], 'accion': C['accion/fondo'], 'accion_texto': C['accion/texto'],
        'vig_f': C['estado/vigente/fondo'], 'vig_b': C['estado/vigente/borde'], 'vig_t': C['estado/vigente/texto'],
        'sin_b': C['estado/sin-confirmar/borde'], 'sin_t': C['estado/sin-confirmar/texto'],
        'remotion': seccion_remotion(), 'lottie': seccion_lottie(), 'tres_d': seccion_3d(),
        'faltan': ', '.join(f'<code>{f}</code>' for f in FALTAN),
    }
    (AQUI / 'index.html').write_text(pagina)
    (AQUI / 'archivos.json').write_text(json.dumps(archivos, ensure_ascii=False, indent=1) + '\n')
    print(len(archivos), 'videos e imágenes')


if __name__ == '__main__':
    main()
