#!/usr/bin/env python3
"""Especificación de variables de Figma derivada de los tokens DTCG (una sola fuente de verdad).
Escribe espec.json: colecciones, modos y variables con valor o alias por modo."""
import json, pathlib
R = pathlib.Path(__file__).resolve().parent
K = R / '../../../../gorr-brand-system/clientes/kino'

def cargar(archivos):
    arbol = {}
    def fusionar(a, b):
        for k, v in b.items():
            if isinstance(v, dict) and k in a and isinstance(a[k], dict) and '$value' not in v: fusionar(a[k], v)
            else: a[k] = v
    for f in archivos: fusionar(arbol, json.loads(f.read_text(encoding='utf8')))
    return arbol

def aplanar(n, ruta=(), tipo=None, out=None):
    out = {} if out is None else out
    tipo = n.get('$type', tipo)
    if '$value' in n:
        out['.'.join(ruta)] = {'valor': n['$value'], 'tipo': tipo, 'desc': n.get('$description', '')}
        return out
    for k, v in n.items():
        if not k.startswith('$') and isinstance(v, dict): aplanar(v, ruta + (k,), tipo, out)
    return out

base = sorted((K / 'tokens').glob('*.tokens.json'))
prim = aplanar(cargar(base))
temas = {t: aplanar(cargar(base + [K / f'tokens/tema/{t}.tokens.json'])) for t in ('oscuro', 'claro')}

def nombre_figma(ruta):
    p = ruta.split('.')
    if p[0] == 'primitivo':
        p = p[1:]
        if p[0] in ('medida', 'movimiento', 'tipo'): p = p[1:]
        return '/'.join(p)
    p = p[1:]  # semantico.x.y → x/y
    if p[0] == 'movimiento': p = p[1:]
    return '/'.join(p)

def coleccion(ruta, tipo):
    p = ruta.split('.')
    if p[0] == 'primitivo':
        if p[1] == 'color': return 'Primitivos'
        if p[1] == 'movimiento': return 'Movimiento'
        if p[1] == 'tipo': return 'Tipografía'
        return 'Espacio y radio'
    if p[1] == 'movimiento': return 'Movimiento'
    if p[1] == 'forma': return 'Espacio y radio'
    return 'Color'

def figma_valor(v, tipo):
    if isinstance(v, str) and v.startswith('{'):
        return {'alias': nombre_figma(v.strip('{}')), 'coleccion': coleccion(v.strip('{}'), tipo)}
    if tipo == 'color':
        h = v['hex'].lstrip('#'); a = v.get('alpha', 1)
        return {'rgba': [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)] + [a]}
    if tipo in ('dimension', 'duration'):
        if isinstance(v, dict) and v.get('unit') == 'rem': return {'num': round(v['value'] * 16, 2)}
        return {'num': v['value'] if isinstance(v, dict) else v}
    if tipo in ('number', 'fontWeight'):
        return {'num': v}
    if tipo == 'fontFamily':
        return {'str': v[0] if isinstance(v, list) else v}
    if tipo == 'cubicBezier':
        return {'str': 'cubic-bezier(' + ', '.join(str(x) for x in v) + ')'}
    return None

TIPO = {'color': 'COLOR', 'dimension': 'FLOAT', 'duration': 'FLOAT', 'number': 'FLOAT', 'fontWeight': 'FLOAT', 'fontFamily': 'STRING', 'cubicBezier': 'STRING'}
vars_ = []
for ruta, t in prim.items():
    if ruta.startswith('semantico') or t['tipo'] not in TIPO: continue
    vars_.append({'col': coleccion(ruta, t['tipo']), 'nombre': nombre_figma(ruta), 'tipo': TIPO[t['tipo']], 'desc': t['desc'], 'css': '--kino-' + '-'.join(x for x in ruta.split('.') if x not in ('primitivo', 'semantico', 'color', 'medida', 'tipo')),
                  'modos': {'Valor': figma_valor(t['valor'], t['tipo'])}})
for ruta, t in temas['oscuro'].items():
    if not ruta.startswith('semantico') or t['tipo'] not in TIPO: continue
    col = coleccion(ruta, t['tipo'])
    modos = {'Oscuro': figma_valor(t['valor'], t['tipo']), 'Claro': figma_valor(temas['claro'][ruta]['valor'], t['tipo'])} if col == 'Color' else {'Valor': figma_valor(t['valor'], t['tipo'])}
    vars_.append({'col': col, 'nombre': nombre_figma(ruta), 'tipo': TIPO[t['tipo']], 'desc': t['desc'], 'css': '--kino-' + '-'.join(x for x in ruta.split('.') if x not in ('primitivo', 'semantico', 'color', 'medida', 'tipo')), 'modos': modos})
json.dump({'variables': vars_}, open(R / 'espec.json', 'w'), ensure_ascii=False)
from collections import Counter
print(Counter(v['col'] for v in vars_), len(vars_))
