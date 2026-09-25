#!/usr/bin/env python3
"""Fase 5 · las diez comprobaciones del encargo sobre el sitio construido.
Uso: python3 fase5.py [variables-figma.json]
Escribe informe.json e informe.md en esta carpeta. Sale con 1 si alguna comprobación falla.
Supuestos: el sitio está construido (sitio/construir.py) y los tokens también (npm run ciclo -- kino)."""
import html, json, pathlib, re, subprocess, sys
R = pathlib.Path(__file__).resolve().parent
S = R / '../sitio'
GBS = R / '../../../../gorr-brand-system'
K = GBS / 'clientes/kino'
SITIO = (S / 'build/kino-sistema-de-marca.html').read_text(encoding='utf8')
TEXTO = (S / 'texto-visible.md').read_text(encoding='utf8')
res = []


def reg(n, nombre, pasa, detalle, evidencia=''):
    res.append({'n': n, 'comprobacion': nombre, 'pasa': bool(pasa), 'detalle': detalle, 'evidencia': evidencia})


# 1 · Términos prohibidos y «permiso» en el texto visible
voz = json.loads((K / 'voz.json').read_text(encoding='utf8'))
evitar = [v['no'] if isinstance(v, dict) and 'no' in v else v for v in voz['vocabulario'].get('evitar', [])]
evitar = [x if isinstance(x, str) else x.get('termino', '') for x in evitar]
vacios = ['fluido', 'fluida', 'sin fricciones', 'experiencia', 'potenciar', 'transformar', 'robusto', 'integral', 'innovador', 'seamless',
          'permiso', 'permisos', 'contraseña', 'imagina', 'descubre', 'en kino creemos', 'oops', 'algo salió mal']
hall = []
for t in vacios:
    for m in re.finditer(r'(?i)(?<![\wáéíóúñ])' + re.escape(t) + r'(?![\wáéíóúñ])', TEXTO):
        linea = TEXTO[:m.start()].count('\n') + 1
        hall.append(f'l{linea} «{m.group(0)}»')
exclam = [f'l{i + 1}' for i, l in enumerate(TEXTO.split('\n')) if '!' in l or '¡' in l]
rayas = [f'l{i + 1}' for i, l in enumerate(TEXTO.split('\n')) if '—' in l]
reg(1, 'Términos prohibidos, «permiso», exclamaciones y rayas en el texto visible', not (hall or exclam or rayas),
    f'{len(hall)} términos, {len(exclam)} exclamaciones, {len(rayas)} rayas', '; '.join(hall + exclam + rayas)[:400])

# 2 · npm run voz -- kino sobre todo el texto
arch = [S / 'texto-visible.md', S / 'build/muestras-ux.md']
p = subprocess.run(['node', str(GBS / 'herramientas/voz.mjs'), 'kino', *map(str, arch)], capture_output=True, text=True, cwd=GBS)
m = re.search(r'(\d+) hallazgos · (\d+) errores', p.stdout)
reg(2, 'npm run voz -- kino sobre el texto visible y los textos de la app', m and m.group(1) == '0', m.group(0) if m else p.stdout[-200:])

# 3 · Límites de largo de UX writing
ux = json.loads((S / 'build/verbal-verificacion.json').read_text(encoding='utf8'))
fuera = [u for u in ux if not u['pasa']]
reg(3, 'Límites de largo de UX writing (botón ≤ 3, estado ≤ 20, WhatsApp ≤ 45)', not fuera, f'{len(ux) - len(fuera)} de {len(ux)} dentro del límite',
    '; '.join(f'{u["momento"]}: {u["palabras"]}' for u in fuera))

# 4 · Mezclas de tú y usted dentro de una audiencia
usted = re.compile(r'(?i)\b(usted|ustedes)\b|\b(su|sus)\s+(conjunto|consejo|administración)\b')
tu = re.compile(r'(?i)\b(tú|tu|tus|tienes|puedes|dile|pídele|créale|entra a kino)\b')
mix_app = [u['texto'] for u in ux if not u['momento'].startswith('Administración') and re.search(r'(?i)\busted\b', u['texto'])]
mix_adm = [u['texto'] for u in ux if u['momento'].startswith('Administración') and tu.search(u['texto'])]
# Piezas para la administración en Aplicaciones: una página, correo, presentación.
piezas_adm = re.findall(r'<div class="(?:hoja en-claro|correo en-claro|diapo[^"]*)"[^>]*>(.*?)</div></div>', SITIO, flags=re.S)
mix_piezas = [re.sub(r'<[^>]+>', ' ', x)[:80] for x in piezas_adm if tu.search(re.sub(r'<[^>]+>', ' ', x)) and 'Desde el lunes' not in x]
reg(4, 'Tú con residente y visita, usted con la administración, sin mezclar', not (mix_app or mix_adm or mix_piezas),
    f'app con usted: {len(mix_app)} · administración con tú: {len(mix_adm)} · piezas para administración con tú: {len(mix_piezas)}', '; '.join(mix_app + mix_adm + mix_piezas))

# 5 · APCA en todos los pares
con = json.loads((K / 'reportes/contraste.json').read_text(encoding='utf8'))
malos = [f'{c["tema"]}: {c["que"]} Lc {c["apcaLc"]}' for c in con if not c['pasa']]
sin_apca = [c['que'] for c in con if c.get('apcaMin') is None]
reg(5, 'APCA en todos los pares texto y fondo (Lc 75 · 60 · 45 · 30)', not malos and not sin_apca,
    f'{len(con)} mediciones, {len(malos)} fallos, {len(sin_apca)} sin mínimo APCA', '; '.join(malos + sin_apca))

# 6 · Diff entre tokens DTCG, kino-brand.css y variables de Figma
resu = json.loads((K / 'build/tokens.resuelto.json').read_text(encoding='utf8'))
brand = (R / '../../kino-brand.css').read_text(encoding='utf8')
en_css = set(re.findall(r'(--kino-[\w-]+)\s*:', brand))
dtcg = {'--' + k for k in resu['primitivos']} | {'--' + k for k in resu['temas']['oscuro']}
falta_css = sorted(dtcg - en_css)
figma_txt = ''
falta_fig = []
if len(sys.argv) > 1 and pathlib.Path(sys.argv[1]).exists():
    fig = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf8'))
    # Las sombras van como estilos de efecto: Figma no guarda sombras en variables.
    en_fig = {v['css'] for v in fig['variables']} | {e['css'] for e in fig.get('estilosDeEfecto', [])}
    falta_fig = sorted(dtcg - en_fig)
    # La exportación (figma/exportar_variables.py) ya compara los dos modos, los números y las cadenas.
    difer = list(fig['diferencias']) if 'diferencias' in fig else [v['css'] for v in fig['variables'] if v.get('tipo') == 'COLOR' and v.get('modo', 'Oscuro') == 'Oscuro' and v['css'] in dtcg and str(v.get('valor', '')).upper() != str(resu['temas']['oscuro'].get(v['css'][2:]) or resu['primitivos'].get(v['css'][2:], '')).upper()]
    figma_txt = f' · Figma: {len(fig["variables"]) and len({v["css"] for v in fig["variables"]})} variables y {len({e["css"] for e in fig.get("estilosDeEfecto", [])})} estilos de efecto, {len(falta_fig)} tokens sin variable, {len(difer)} valores distintos (color en los dos modos, números y cadenas)'
    falta_fig += difer
else:
    figma_txt = ' · Figma: sin exportar (pasa variables-figma.json)'
reg(6, 'Diff entre tokens DTCG, kino-brand.css y variables de Figma', not falta_css and not falta_fig and 'sin exportar' not in figma_txt,
    f'DTCG {len(dtcg)} · kino-brand.css: {len(falta_css)} faltan' + figma_txt, '; '.join((falta_css + falta_fig)[:30]))

# 7 · Componentes sin ligar a variables (valores sueltos en la capa de componentes)
comp = (R / '../../capa-componentes.css').read_text(encoding='utf8')
comp_sin_com = re.sub(r'/\*.*?\*/', '', comp, flags=re.S)
sueltos = re.findall(r'#[0-9a-fA-F]{3,8}\b|\b\d+(?:\.\d+)?(?:px|ms)\b', comp_sin_com)
fig_sueltos = []
if len(sys.argv) > 1 and pathlib.Path(sys.argv[1]).exists():
    fig_sueltos = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf8')).get('componentesSinLigar', [])
reg(7, 'Componentes sin ligar a variables (CSS y Figma)', not sueltos and not fig_sueltos,
    f'capa-componentes.css: {len(sueltos)} valores sueltos · Figma: {len(fig_sueltos)} nodos con color sin variable', '; '.join(sueltos + fig_sueltos[:20]))

# 8 · Decisiones sin justificación de la plataforma
dec = (R / '../../../../decisiones.md').read_text(encoding='utf8')
bloques = re.split(r'\n### ', dec)[1:]
sin_por = [b.split('\n')[0] for b in bloques if not b.startswith('Estado') and not re.search(r'(?i)\*\*(por qué|justificación|trazabilidad|efecto)', b)]
tabla_x = re.findall(r'^\| (X\d+) \|.*\| ([^|]+) \|$', dec, flags=re.M)
x_sin = [x for x, j in tabla_x if not j.strip() or j.strip() == '—']
deptos = re.findall(r'<section class="vista" id="([\w-]+)"[^>]*data-num="(0[3-9]|1[0-2])"', SITIO)
sin_traza = [d for d, _ in deptos if SITIO.count(f'id="{d}.') and 'class="traza"' not in SITIO[SITIO.index(f'id="{d}"'):SITIO.index('</section>', SITIO.index(f'id="{d}"'))]]
reg(8, 'Decisiones sin justificación de la plataforma', not (sin_por or x_sin or sin_traza),
    f'decisiones.md: {len(bloques)} con detalle, {len(sin_por)} sin «Por qué» · tabla X: {len(x_sin)} sin «Responde a» · departamentos sin traza: {len(sin_traza)}',
    '; '.join(sin_por + x_sin + sin_traza))

# 9 · Enlaces y anclas rotas
ids = set(re.findall(r'\bid="([^"]+)"', SITIO))
refs = set(re.findall(r'href="#([^"]+)"', SITIO))
dinamicas = {'inicio', 'conocer', 'usar'}
rotas = sorted(r for r in refs if r not in ids and r.split('.')[0] not in dinamicas and "'" not in r and '+' not in r)
externos = sorted(set(re.findall(r'href="(https?://[^"]+)"', SITIO)))
reg(9, 'Enlaces y anclas rotas', not rotas, f'{len(refs)} anclas internas, {len(rotas)} rotas · {len(externos)} enlaces externos', '; '.join(rotas))

# 10 · Cobertura de la definición de terminado
COB = json.loads((R / 'cobertura.json').read_text(encoding='utf8'))
faltan = []
total = 0
for depto, items in COB.items():
    for item, ancla in items.items():
        total += 1
        if ancla.startswith('PENDIENTE'):
            continue
        if f'id="{ancla}"' not in SITIO:
            faltan.append(f'{depto}: {item} → #{ancla}')
pend_n = sum(1 for d in COB.values() for a in d.values() if a.startswith('PENDIENTE'))
reg(10, 'Cobertura de la definición de terminado', not faltan, f'{total} elementos · {total - len(faltan) - pend_n} con su ancla en el sitio · {pend_n} [PENDIENTE] con motivo · {len(faltan)} faltan',
    '; '.join(faltan))

(R / 'informe.json').write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf8')
md = ['| # | Comprobación | Resultado | Detalle |', '|---|---|---|---|']
md += [f'| {r["n"]} | {r["comprobacion"]} | {"PASA" if r["pasa"] else "FALLA"} | {r["detalle"]}{(" · " + r["evidencia"]) if r["evidencia"] and not r["pasa"] else ""} |' for r in res]
(R / 'informe.md').write_text('\n'.join(md) + '\n', encoding='utf8')
print('\n'.join(md))
sys.exit(0 if all(r['pasa'] for r in res) else 1)
