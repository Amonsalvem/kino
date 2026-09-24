#!/usr/bin/env python3
"""Arma el sitio «Kino · Sistema de marca» en un solo HTML.
Salidas:
  build/kino-sistema-de-marca.html  documento completo (carpeta del proyecto)
  build/artefacto.html              cuerpo sin doctype (para publicar como artefacto)
"""
import pathlib, re
R = pathlib.Path(__file__).parent
leer = lambda p: (R / p).read_text(encoding='utf8')
# Fuente de verdad: los tokens DTCG del cliente kino, construidos por gorr-brand-system.
_dtcg = R / '../../../../gorr-brand-system/clientes/kino/build/kino-tokens.css'
tokens = _dtcg.read_text(encoding='utf8') if _dtcg.exists() else leer('kino-tokens.css')
sprite = leer('sprite.svg').replace('</defs>',
 '<symbol id="i-flecha" viewBox="0 0 24 24"><path d="M5 12h14"/><path d="M13 6l6 6-6 6"/></symbol>'
 '<symbol id="i-buscar" viewBox="0 0 24 24"><circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5"/></symbol>'
 '<symbol id="i-menu" viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></symbol>'
 '<symbol id="i-tema" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8"/><path d="M12 4a8 8 0 0 0 0 16z" fill="currentColor"/></symbol>'
 '</defs>')
logo_h = leer('logo-h.svg')
logo_mark = re.sub(r'<g transform.*?</g>', '', logo_h).replace('viewBox="0 0 267.960 101.824" width="268" height="102" overflow="visible"', 'viewBox="0 0 100 101.824" width="100" height="102"').replace('role="img" aria-label="Kino"', 'aria-hidden="true"')
contenido_crudo = ''.join(leer(f'contenido/{f}') for f in ['00-inicio.html', '01-plataforma.html', '02-verbal.html', '02-12.html']).replace('{{LOGO_H}}', logo_h)
# Espacios que no parten: horas, placas, códigos y teléfonos se leen como una unidad.
NB = '\u00a0'
contenido = re.sub(r'(\d{1,2}:\d{2}) ([ap])\. m\.', lambda m: m.group(1)+NB+m.group(2)+'.'+NB+'m.', contenido_crudo)
contenido = re.sub(r'\b([A-Z]{3}) (\d{3})\b', lambda m: m.group(1)+NB+m.group(2), contenido)
contenido = re.sub(r'\b(\d{3}) (\d{3}|\*{3})( \d{4})?\b', lambda m: m.group(1)+NB+m.group(2)+(NB+m.group(3)[1:] if m.group(3) else ''), contenido)

cuerpo = f'''<title>Kino · Sistema de marca</title>
<meta name="description" content="Sistema de marca de Kino: plataforma, voz, identidad visual, producto, aplicaciones y gobernanza.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&family=JetBrains+Mono:wght@400;500;600;700&display=swap">
<script>document.documentElement.setAttribute('data-tema',(function(){{try{{return localStorage.getItem('kino-tema')}}catch(e){{}}}})()||'oscuro');</script>
<style>{tokens}
{leer('sitio.css')}</style>
<a class="saltar" href="#contenido">Saltar al contenido</a>
{sprite}
<div class="progreso" aria-hidden="true"><i></i></div>
<div class="armazon">
  <aside class="indice" id="indice" aria-label="Índice" data-abierto="false">
    <a class="indice-marca" href="#inicio">{logo_h.replace('role="img" aria-label="Kino"','role="img" aria-label="Kino, inicio"')}<span>Sistema de marca</span></a>
    <div class="buscar" role="search">
      <label for="q" class="oculto">Buscar en títulos y glosario</label>
      <svg class="ic" aria-hidden="true"><use href="#i-buscar"/></svg>
      <input id="q" type="search" placeholder="Buscar" autocomplete="off" aria-controls="resultados" aria-label="Buscar en títulos y glosario">
      <kbd aria-hidden="true">/</kbd>
      <ul class="resultados" id="resultados" hidden></ul>
    </div>
    <nav class="nav" id="nav" aria-label="Secciones"></nav>
    <div class="indice-pie"><button class="boton-tenue" id="tema" type="button" aria-pressed="false"><svg class="ic" aria-hidden="true"><use href="#i-tema"/></svg> Tema claro</button></div>
  </aside>
  <div>
    <header class="barra-movil">
      {logo_mark.replace('<svg', '<svg class="logo"', 1)}
      <span class="donde" id="donde" aria-live="polite"></span>
      <button class="boton-tenue" id="abrir-indice" type="button" aria-controls="indice" aria-expanded="false"><svg class="ic" aria-hidden="true"><use href="#i-menu"/></svg> Índice</button>
    </header>
    <main id="contenido" tabindex="-1">
{contenido}
    </main>
  </div>
</div>
<script>{leer('sitio.js')}</script>
'''
(R / 'build').mkdir(exist_ok=True)
(R / 'build/artefacto.html').write_text(cuerpo, encoding='utf8')
(R / 'build/kino-sistema-de-marca.html').write_text('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n</head>\n<body>\n' + cuerpo + '</body>\n</html>\n', encoding='utf8')
print('ok', len(cuerpo))

# Texto visible para las compuertas de voz: excluye ejemplos incorrectos (.no, .tachado) y citas de la app actual (.antes).
import html as _h
_s = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', cuerpo, flags=re.S)
_s = re.sub(r'<(p|td|span|code)[^>]*class="[^"]*\b(no|antes|tachado|plantilla)\b[^"]*"[^>]*>.*?</\1>', '', _s, flags=re.S)
_s = re.sub(r'<svg.*?</svg>', lambda m: ' '.join(re.findall(r'>([^<]+)<', m.group(0))), _s, flags=re.S)
_t = _h.unescape(re.sub(r'<[^>]+>', '\n', _s))
(R / 'texto-visible.md').write_text('\n'.join(l.strip() for l in _t.split('\n') if l.strip()) + '\n', encoding='utf8')
