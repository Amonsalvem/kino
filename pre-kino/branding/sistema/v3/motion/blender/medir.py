"""Mide si los colores de estado salen con el hex de su token en un render.

    python medir.py <png> <token> [<token> …] [--json=salida.json]

Por cada token cuenta los píxeles opacos cuyo color es el hex del token con ±1 por canal (redondeo de 8 bits), y da
la distancia mínima (ΔE CIE76 en Lab) de cualquier píxel al token. «Exacto» = al menos 20 píxeles con ±1.
"""
import json
import sys

import numpy as np
from PIL import Image

import kino3d as k


def lab(rgb):
    c = rgb / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    m = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    xyz = c @ m.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


def medir(ruta, tokens):
    im = np.asarray(Image.open(ruta).convert('RGBA')).astype(np.int32)
    opaco = im[..., 3] >= 250
    px = im[..., :3][opaco]
    lab_px = lab(px.astype(np.float64))
    out = {}
    for t in tokens:
        h = k.hexa(t)
        obj = np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)])
        exactos = int((np.abs(px - obj).max(axis=1) <= 1).sum())
        de = float(np.sqrt(((lab_px - lab(obj[None].astype(np.float64))) ** 2).sum(-1)).min()) if len(px) else None
        out[t] = {'hex': h, 'pixeles_exactos': exactos, 'delta_e_min': round(de, 2) if de is not None else None,
                  'exacto': exactos >= 20}
    return out


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    res = medir(args[0], args[1:])
    for t, r in res.items():
        print(f"{'✓' if r['exacto'] else '✗'} {t:32} {r['hex']}  {r['pixeles_exactos']:6d} px exactos · ΔE mín {r['delta_e_min']}")
    salida = next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--json=')), None)
    if salida:
        json.dump({'archivo': args[0], 'tokens': res}, open(salida, 'w'), ensure_ascii=False, indent=1)
