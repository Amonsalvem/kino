#!/usr/bin/env python3
"""Arma muestras-detector.md para el detector de IA: titulares, ledes, definiciones y leyendas de cada
sección del sitio (sin ejemplos incorrectos) más el microcopy final de la app."""
import html, pathlib, re
R = pathlib.Path(__file__).resolve().parent
s = (R / '../sitio/build/kino-sistema-de-marca.html').read_text(encoding='utf8')
s = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', s, flags=re.S)
txt = lambda x: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', x))).strip()
out = ['# Textos del sistema de marca Kino, por sección\n']
for m in re.finditer(r'<section class="vista" id="([\w-]+)" data-titulo="([^"]+)"(.*?)</section>', s, flags=re.S):
    sid, tit, body = m.groups()
    if sid == 'glosario':
        continue
    body = re.sub(r'<(p|span|div|code)[^>]*class="[^"]*\b(no|antes|tachado|plantilla|ej-mal)\b[^"]*"[^>]*>.*?</\1>', '', body, flags=re.S)
    items = []
    for tag in re.findall(r'<(?:h2|p class="lede"|dd|figcaption)[^>]*>(.*?)</(?:h2|p|dd|figcaption)>', body, flags=re.S):
        t = txt(tag)
        if 12 < len(t) < 400 and t not in items:
            items.append(t)
    out.append(f'\n## {tit} (#{sid})\n' + '\n'.join('- ' + t for t in items[:28]))
ux = [l for l in (R / '../sitio/build/muestras-ux.md').read_text(encoding='utf8').splitlines() if l.strip() and not l.startswith(('Se elimina', '(se une'))]
out.append('\n## Microcopy de la app (textos finales)\n' + '\n'.join('- ' + l for l in ux))
(R / 'muestras-detector.md').write_text('\n'.join(out) + '\n', encoding='utf8')
print('muestras-detector.md', sum(1 for l in '\n'.join(out).split('\n') if l.startswith('- ')), 'textos')
