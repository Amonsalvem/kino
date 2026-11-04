"""Escala tipografica fluida: calcula el clamp() de cada paso entre 360 y 1440 px."""
import os, sys, json
AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(AQUI))

MINVW, MAXVW = 360, 1440
BASE_MIN, BASE_MAX = 16.0, 18.0
R_MIN, R_MAX = 1.200, 1.260

out = {}
for i in range(-1, 7):
    mn = BASE_MIN * (R_MIN ** i); mx = BASE_MAX * (R_MAX ** i)
    slope = (mx - mn) / (MAXVW - MINVW); inter = mn - slope * MINVW
    out[str(i)] = {'min_px': round(mn, 2), 'max_px': round(mx, 2),
                   'clamp': 'clamp(%.3frem, %.3frem + %.3fvw, %.3frem)'
                            % (mn / 16, inter / 16, slope * 100, mx / 16)}
json.dump(out, open('typescale.json', 'w'), indent=1)
print('typescale.json ·', len(out), 'pasos')
