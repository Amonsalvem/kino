#!/usr/bin/env python3
"""Piezas del Pase como archivos sueltos, con la forma Portal (X1) y la llamada de portería (X11).
Salidas en build/:
  pase-vivo.html          la página del enlace (sigue el tema del teléfono; oscuro por defecto)
  pase-vivo-vencido.html  el mismo Pase cuando venció: ofrece «Llamar al residente»
  imagen-visita.html      la imagen del WhatsApp, a 1080 px de ancho (render.mjs la pasa a PNG)
  imagen-colaborador.html
  pdf.html                el PDF opcional, carta y en claro (render.mjs lo imprime)
  senal-entrada.html      señal de 60 × 40 cm
  porteria.html           Kino Portería con un rechazo por Pase vencido
Las piezas salen de ../sitio/deptos/pase.py: el sitio y estos archivos usan el mismo código."""
import pathlib, re, sys
R = pathlib.Path(__file__).resolve().parent
S = R / '../sitio'
sys.path.insert(0, str(S))
from deptos import pase                      # noqa: E402
from deptos.comun import TOKENS_CSS, fuentes_incrustadas  # noqa: E402
from deptos.d06_iconografia import simbolos  # noqa: E402

componentes = re.sub(r'^@import[^;]+;\s*$', '', (R / '../../capa-componentes.css').read_text(encoding='utf8'), flags=re.M)
b = R / '../../../../gorr-brand-system/clientes/kino/build'
locales = ''.join(re.sub(r'^[^{]+\{', '.%s{' % c, (b / f).read_text(encoding='utf8'), count=1) for f, c in (('tema-oscuro.css', 'en-oscuro'), ('tema-claro.css', 'en-claro')))
deptos_css = (S / 'deptos.css').read_text(encoding='utf8')
sprite = f'<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{simbolos()}</defs></svg>'
# Las fuentes van incrustadas: el PNG y el PDF no pueden depender de que la red alcance Google Fonts.
FUENTES = fuentes_incrustadas()


NB = '\u00a0'
def _nb(t):
    t = re.sub(r'(\d{1,2}:\d{2}) ([ap])\. m\.', lambda m: m.group(1)+NB+m.group(2)+'.'+NB+'m.', t)
    t = re.sub(r'\b([A-Z]{3}) (\d{3})\b', lambda m: m.group(1)+NB+m.group(2), t)
    return t


def pagina(titulo, cuerpo, css_extra='', tema='oscuro'):
    cuerpo = re.sub(r'>[^<]+<', lambda m: _nb(m.group(0)), cuerpo)
    return f'''<!doctype html>
<html lang="es" data-tema="{tema}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titulo}</title>{FUENTES}
<style>{TOKENS_CSS}
{locales}
{componentes}
{deptos_css}
*,*::before,*::after{{box-sizing:border-box}}
body{{margin:0;background:var(--kino-superficie-base);color:var(--kino-texto-primario);font-family:var(--kino-fuente-texto);line-height:1.5}}
.mono,.kino-dato{{font-family:var(--kino-fuente-dato);font-feature-settings:"zero" 1}}
.cifra{{font-family:var(--kino-fuente-dato);font-weight:700}}
{css_extra}</style></head>
<body>{sprite}{cuerpo}</body></html>
'''


# El Pase vivo es la pantalla completa del teléfono: sin marco, a todo el ancho y con el tema del sistema.
VIVO = ('.pase-vivo{max-inline-size:30rem;margin-inline:auto;border:0;border-radius:0;min-block-size:100vh}'
        '.pv-cuerpo{padding:1.2rem 1rem 2rem}.pv-portal{inline-size:min(70%,16rem)}'
        '@media (min-width:48rem){body{padding:2rem 0}.pase-vivo{border-radius:1.4rem;min-block-size:0;border:1px solid var(--kino-borde-definido)}}')
IMAGEN = 'body{background:transparent}.pieza-pase{max-inline-size:none;inline-size:1080px;border-radius:0}'
PDF = ('@page{size:letter;margin:0}body{background:var(--kino-fijo-blanco)}'
       '.pase-pdf{max-inline-size:none;inline-size:8.5in;border-radius:0;box-shadow:none}'
       'html,body{block-size:11in;overflow:hidden}.pase-pdf>.in{block-size:calc(11in - 2px);aspect-ratio:auto}.pdf-cuerpo{grid-template-columns:40cqi 1fr!important}.pdf-nombre{font-size:6cqi}.pdf-franja{font-size:3cqi}'
       '.pase-pdf .pp-datos{font-size:2.8cqi}.pase-pdf .pp-datos .kino-dato{font-size:3.4cqi}.pdf-modos{font-size:2.4cqi}.pdf-pie{font-size:2.1cqi}')
SENAL = ('body{display:grid;place-items:center;min-block-size:100vh;padding:1rem}'
         '.senal-entrada{max-inline-size:60rem}')
PORT = ('body{padding:clamp(0rem,2vw,2rem)}.vista-porteria{max-inline-size:80rem;margin-inline:auto}'
        '@media (min-width:60rem){.po-cuerpo{grid-template-columns:minmax(0,26rem) minmax(0,1fr);align-items:start}'
        '.po-fila{grid-template-columns:4rem 1fr 6rem 6rem auto;font-size:.95rem}.po-fila>span:nth-child(4){display:block}}'
        '@media (max-width:30rem){.po-fila{grid-template-columns:2.6rem minmax(0,1fr) auto}.po-fila>span:nth-child(3){display:none}}')

(R / 'build').mkdir(exist_ok=True)
salidas = {
    'pase-vivo.html': pagina('Pase de Andrés Gómez · Kino', pase.vivo('vigente', tema=''), VIVO),
    'pase-vivo-vencido.html': pagina('Pase vencido · Kino', pase.vivo('vencido', tema=''), VIVO),
    'imagen-visita.html': pagina('Imagen del Pase · visita', pase.imagen('vigente'), IMAGEN),
    'imagen-colaborador.html': pagina('Imagen del Pase · colaborador', pase.imagen('vigente', 'Colaborador'), IMAGEN),
    'pdf.html': pagina('Pase de Andrés Gómez · PDF', pase.pdf(), PDF, 'claro'),
    'senal-entrada.html': pagina('Señal de la entrada · Kino', pase.senal(tema=''), SENAL),
    'porteria.html': pagina('Kino Portería', pase.porteria(tema=''), PORT),
}
for nombre, html in salidas.items():
    (R / 'build' / nombre).write_text(html, encoding='utf8')
print('ok', ', '.join(salidas))
