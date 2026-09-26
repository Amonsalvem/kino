"""Tokens de Kino para motion: lee los DTCG del repositorio y los deja listos para Lottie y Remotion.

Ningún valor de movimiento o color vive aquí: todo sale de gorr-brand-system/clientes/kino/tokens.
Escribe tokens.motion.json, que lee la composición de Remotion.
"""
import json
import math
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
TOKENS = RAIZ / 'gorr-brand-system/clientes/kino/tokens'
FPS = 60


def _cargar(*nombres):
    arbol = {}
    for n in nombres:
        _fundir(arbol, json.loads((TOKENS / n).read_text()))
    return arbol


def _fundir(a, b):
    for k, v in b.items():
        if isinstance(v, dict) and isinstance(a.get(k), dict):
            _fundir(a[k], v)
        else:
            a[k] = v


def _nodo(arbol, ruta):
    n = arbol
    for p in ruta.split('.'):
        n = n[p]
    return n


def _valor(arbol, ruta):
    v = _nodo(arbol, ruta)['$value']
    while isinstance(v, str) and v.startswith('{'):
        v = _nodo(arbol, v[1:-1])['$value']
    return v


def _hojas(n, prefijo=''):
    for k, v in n.items():
        if k.startswith('$'):
            continue
        if isinstance(v, dict) and '$value' in v:
            yield prefijo + k
        elif isinstance(v, dict):
            yield from _hojas(v, prefijo + k + '.')


def frames(ms):
    """Duración en ms a frames, redondeando al frame más cercano."""
    return int(math.floor(ms * FPS / 1000 + 0.5))


def cargar(tema='oscuro'):
    base = ['10-primitivo-color.tokens.json', '20-primitivo-tipo.tokens.json', '30-primitivo-medida.tokens.json',
            '35-primitivo-forma.tokens.json', '40-movimiento.tokens.json', '50-semantico-comun.tokens.json']
    arbol = _cargar(*base, f'tema/{tema}.tokens.json')
    mov = arbol['primitivo']['movimiento']
    t = {'fps': FPS, 'tema': tema, 'duracion': {}, 'escalonado': {}, 'curva': {}, 'distancia': {}, 'verbo': {},
         'color': {}, 'radio': {}, 'espacio': {}, 'linea': {}}
    for k in _hojas(mov['duracion']):
        ms = mov['duracion'][k]['$value']['value']
        t['duracion'][k] = {'token': f'duracion/{k}', 'frames': frames(ms)}
    for k in _hojas(mov['escalonado']):
        ms = mov['escalonado'][k]['$value']['value']
        t['escalonado'][k] = {'token': f'escalonado/{k}', 'frames': frames(ms)}
    for k in _hojas(mov['curva']):
        t['curva'][k] = mov['curva'][k]['$value']
    for k in _hojas(mov['distancia']):
        t['distancia'][k] = mov['distancia'][k]['$value']['value']
    # Verbos: alias semánticos (aparecer/duracion → duracion/tarjeta, etc.).
    sem_mov = arbol['semantico']['movimiento']
    for verbo in _hojas(sem_mov):
        ref = sem_mov
        for p in verbo.split('.'):
            ref = ref[p]
        destino = ref['$value'][1:-1].split('.')  # primitivo.movimiento.<familia>.<nombre>
        t['verbo'][verbo.replace('.', '/')] = f'{destino[2]}/{destino[3]}'
    for k in _hojas(arbol['semantico']):
        if k.startswith(('superficie.', 'texto.', 'acento.', 'accion.', 'estado.', 'borde.')):
            v = _valor(arbol, 'semantico.' + k)
            if isinstance(v, dict) and 'hex' in v:
                alfa = v.get('alpha', 1)
                t['color'][k.replace('.', '/')] = v['hex'] if alfa >= 1 else v['hex'] + f'{round(alfa * 255):02X}'
    # Primitivos de color: solo para fondos de imagen (aurora), nunca para estados.
    t['primitivo'] = {}
    for k in _hojas(arbol['primitivo']['color']):
        v = _valor(arbol, 'primitivo.color.' + k)
        if isinstance(v, dict) and 'hex' in v:
            t['primitivo'][k.replace('.', '/')] = v['hex']
    for k in ('control', 'tarjeta', 'chip'):
        t['radio'][k] = _valor(arbol, f'semantico.forma.radio.{k}')['value']
    for k in _hojas(arbol['primitivo']['medida']['espacio']):
        t['espacio'][k] = arbol['primitivo']['medida']['espacio'][k]['$value']['value']
    for k in ('fino', 'foco'):
        t['linea'][k] = arbol['primitivo']['medida']['linea'][k]['$value']['value']
    return t


def resolver_duracion(t, nombre):
    """'aparecer/duracion' o 'duracion/tarjeta' → frames."""
    if nombre in t['verbo']:
        nombre = t['verbo'][nombre]
    familia, clave = nombre.split('/')
    return t[familia][clave]['frames']


def resolver_curva(t, nombre):
    if nombre in t['verbo']:
        nombre = t['verbo'][nombre]
    return t['curva'][nombre.split('/')[1]]


if __name__ == '__main__':
    salida = {tema: cargar(tema) for tema in ('oscuro', 'claro')}
    destino = Path(__file__).parent / 'tokens.motion.json'
    destino.write_text(json.dumps(salida, ensure_ascii=False, indent=1) + '\n')
    o = salida['oscuro']
    print('frames a', FPS, 'fps:', {k: v['frames'] for k, v in o['duracion'].items()},
          {k: v['frames'] for k, v in o['escalonado'].items()})
    print('verbos:', o['verbo'])
    print(len(o['color']), 'colores semánticos')
