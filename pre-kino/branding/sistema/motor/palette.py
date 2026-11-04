import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI); os.chdir(RAIZ)
import json
from color import *
import numpy as np

# --- familias: hue heredado de Propuesta 1, chroma y luminosidad mutados ---
FAM = {
 # nombre        H     Cmax   linaje
 'sustrato':  (168.0, 0.042, 'carbon #2C2D2F -> sesgo verde de medio de cultivo'),
 'hueso':     (170.0, 0.016, 'hueso #E1E8EE -> enfriado hacia el verde'),
 'biolum':    (163.0, 0.190, 'menta #B2E8DB -> misma familia, chroma al maximo'),
 'ambar':     ( 75.0, 0.170, 'nueva: la vigencia que se agota'),
 'carmin':    ( 25.0, 0.180, 'nueva: el rechazo'),
 'violeta':   (286.1, 0.180, 'morado #7266CA -> intacto, ahora significa identidad'),
 'indigo':    (264.0, 0.170, 'indigo #00177D -> profundidad'),
}

def step(L,H,Cmax):
    C=clip_chroma(L,Cmax,H); rgb=np.clip(oklch_to_rgb(L,C,H),0,1)
    return hexof(rgb), rgb, L, C

# sustrato: escala de superficies oscuras por luminosidad OKLCh
SUS_L = [0.170,0.215,0.258,0.305,0.375,0.465,0.575,0.700]
HUE_L = [0.980,0.952,0.922,0.882,0.832,0.772,0.695,0.615]

pal={}; meta={}
H,Cm,_=FAM['sustrato']
pal['sustrato']={ (i+1)*100: step(L,H,Cm)[0] for i,L in enumerate(SUS_L) }
H,Cm,_=FAM['hueso']
pal['hueso']={ (i+1)*100: step(L,H,Cm)[0] for i,L in enumerate(HUE_L) }

BG_D = unhex(pal['sustrato'][200])   # fondo oscuro canonico (superficie/base)
BG_L = unhex(pal['hueso'][100])      # fondo claro canonico

TARGETS = [1.5, 2.3, 3.2, 4.5, 7.0, 11.0]
report={}
for fam in ['biolum','ambar','carmin','violeta','indigo','sustrato','hueso']:
    H,Cm,_=FAM[fam]
    pal[fam]=pal.get(fam,{}); report[fam]={}
    # pasos sobre fondo oscuro (aclarando)
    for t in TARGETS:
        L,C,rgb,c = solve_contrast(t, BG_D, H, Cm, lighter=True)
        key='d%d'%int(t*10)
        pal[fam][key]=hexof(rgb)
        report[fam][key]={'objetivo':t,'wcag':round(c,2),'apca':round(apca(rgb,BG_D),1),'L':round(L,3),'C':round(C,3)}
    # pasos sobre fondo claro (oscureciendo)
    for t in TARGETS:
        L,C,rgb,c = solve_contrast(t, BG_L, H, Cm, lighter=False)
        key='l%d'%int(t*10)
        pal[fam][key]=hexof(rgb)
        report[fam][key]={'objetivo':t,'wcag':round(c,2),'apca':round(apca(rgb,BG_L),1),'L':round(L,3),'C':round(C,3)}

json.dump({'paleta':pal,'contraste':report,'fondos':{'oscuro':pal['sustrato'][100],'claro':pal['hueso'][100]}},
          open('palette.json','w'), indent=1, ensure_ascii=False)

print('SUSTRATO', ' '.join(pal['sustrato'].values()))
print('HUESO   ', ' '.join(pal['hueso'].values()))
for f in ['biolum','ambar','carmin','violeta','indigo','sustrato','hueso']:
    print('%-8s D:'%f, ' '.join('%s(%.1f)'%(pal[f]['d%d'%int(t*10)], report[f]['d%d'%int(t*10)]['wcag']) for t in TARGETS))
    print('%-8s L:'%'', ' '.join('%s(%.1f)'%(pal[f]['l%d'%int(t*10)], report[f]['l%d'%int(t*10)]['wcag']) for t in TARGETS))
