"""Arma variables-figma.json con la exportación de las variables de Figma (use_figma, en dos mitades)
y compara los dos modos contra los tokens DTCG resueltos.
Uso: python3 exportar_variables.py export-parte-1.json export-parte-2.json [export-efectos.json]
Las sombras no caben en una variable de Figma: van como estilos de efecto con colores ligados a Primitivos."""
import json, pathlib, sys
R = pathlib.Path(__file__).resolve().parent
K = R / '../../../../gorr-brand-system/clientes/kino'
filas = json.loads(pathlib.Path(sys.argv[1]).read_text())['parte'] + json.loads(pathlib.Path(sys.argv[2]).read_text())['parte2']
COLS = {'P': 'Primitivos', 'C': 'Color', 'E': 'Espacio y radio', 'M': 'Movimiento', 'T': 'Tipografía'}
TIPOS = {'C': 'COLOR', 'F': 'FLOAT', 'S': 'STRING'}
variables = [{'css': c, 'coleccion': COLS[k], 'modo': m, 'tipo': TIPOS[t], 'valor': v} for c, k, m, t, v in filas]
resu = json.loads((K / 'build/tokens.resuelto.json').read_text(encoding='utf8'))
TEMA = {'Oscuro': 'oscuro', 'Claro': 'claro'}
def esperado(css, modo):
    k = css[2:]
    if modo in TEMA and k in resu['temas'][TEMA[modo]]: return resu['temas'][TEMA[modo]][k]
    return resu['primitivos'].get(k) or resu['temas']['oscuro'].get(k)
def norm(v):
    s = str(v).strip().upper()
    return 'TRANSPARENTE' if s in ('TRANSPARENT', 'TRANSPARENTE') or s.startswith('OKLCH(0 0 0 / 0') or s.endswith('/ 0)') else s
dif = []
for v in variables:
    if v['tipo'] != 'COLOR': continue
    e = esperado(v['css'], v['modo'])
    if e is None: dif.append(f"{v['css']} ({v['modo']}): sin token DTCG"); continue
    if norm(e) != norm(v['valor']): dif.append(f"{v['css']} ({v['modo']}): Figma {v['valor']} · DTCG {e}")
import re
todo = {**resu['primitivos'], **resu['temas']['oscuro']}
for v in variables:
    if v['tipo'] == 'COLOR': continue
    e = todo.get(v['css'][2:])
    if e is None: dif.append(f"{v['css']}: sin token DTCG"); continue
    s = str(e)
    if v['tipo'] == 'STRING':
        if v['valor'].split(',')[0].strip() not in s: dif.append(f"{v['css']}: Figma {v['valor']} · DTCG {s}")
        continue
    m = re.match(r'clamp\(([\d.]+)rem,.*,\s*([\d.]+)rem\)', s)
    if m: exp = float(m[1] if v['modo'] == '360 px' else m[2]) * 16
    else:
        n = re.match(r'-?[\d.]+', s); exp = float(n[0]) if n else None
        if exp is not None and s.endswith('rem'): exp *= 16
        if exp is not None and s.endswith('s') and not s.endswith('ms'): exp *= 1000
    if exp is None or abs(exp - float(v['valor'])) > 0.02: dif.append(f"{v['css']} ({v['modo']}): Figma {v['valor']} · DTCG {s}")
# Estilos de efecto (sombras): se reconstruye el box-shadow y se compara con el tema de cada estilo.
efectos = []
if len(sys.argv) > 3:
    hexa = lambda c: '#' + ''.join(f'{round(x * 255):02X}' for x in c[:3])
    for e in json.loads(pathlib.Path(sys.argv[3]).read_text()):
        nombre, tema = e['nombre'].split(' · ')
        css = '--kino-' + nombre.lower().replace('/', '-')
        sombra = ', '.join(('inset ' if f['t'] == 'INNER_SHADOW' else '') + f"{f['x']} {f['y']}px {f['r']}px {f['s']}px {hexa(f['c'])}".replace(' 0px', ' 0').replace('0 0px', '0 0') for f in e['efectos'])
        norm_s = lambda x: re.sub(r'\b0px\b', '0', x).upper()
        dtcg_s = resu['temas'][tema].get(css[2:], '')
        efectos.append({'css': css, 'estilo': e['nombre'], 'modo': tema, 'valor': sombra, 'ligados': [f['ligado']['color'] for f in e['efectos'] if f.get('ligado')]})
        if norm_s(sombra) != norm_s(dtcg_s): dif.append(f"{css} ({tema}): Figma {sombra} · DTCG {dtcg_s}")
salida = {'exportado': '2026-09-25', 'archivo': 'BO7UnDO9iE0aG6yUpNj0bc', 'variables': variables, 'estilosDeEfecto': efectos, 'componentesSinLigar': [],
          'auditoriaPinturas': {'fecha': '2026-09-25', 'paginas': 14, 'pinturasSinVariable': 0, 'como': 'js/p4-auditoria-y-exportacion.js: rellenos y trazos SOLID sin variable ligada, todas las páginas salvo Referencias'},
          'diferencias': dif}
(R / 'variables-figma.json').write_text(json.dumps(salida, ensure_ascii=False, indent=1), encoding='utf8')
print(len(efectos), 'estilos de efecto ·', len(variables), 'filas ·', len({v['css'] for v in variables}), 'variables ·', len(dif), 'diferencias (color en los dos modos, números y cadenas)')
print('\n'.join(dif[:40]))
