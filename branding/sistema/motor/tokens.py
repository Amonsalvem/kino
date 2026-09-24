import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI); os.chdir(RAIZ)
import json
from color import *
P = json.load(open('palette.json'))['paleta']
TS = json.load(open('typescale.json'))

def C(fam, k): return P[fam][str(k)]
checks=[]
def chk(fg,bg,minimo,que):
    r=wcag(unhex(fg),unhex(bg)); a=apca(unhex(fg),unhex(bg))
    checks.append({'par':que,'fg':fg,'bg':bg,'wcag':round(r,2),'apca':round(a,1),'minimo':minimo,'pasa':bool(r>=minimo)})
    return r

# ---------- CAPA 1: primitivos ----------
prim = {'color':{}, 'medida':{}, 'tipo':{}}
for fam in ['sustrato','hueso']:
    prim['color'][fam] = {k:{'$value':v,'$type':'color'} for k,v in P[fam].items()}
for fam in ['biolum','ambar','carmin','violeta','indigo']:
    prim['color'][fam] = {k:{'$value':v,'$type':'color'} for k,v in P[fam].items()}

ESPACIO = {'3xs':'0.125rem','2xs':'0.25rem','xs':'0.5rem','s':'0.75rem','m':'1rem',
           'l':'1.5rem','xl':'2rem','2xl':'3rem','3xl':'4.5rem','4xl':'7rem'}
RADIO = {'nada':'0','xs':'2px','s':'4px','m':'8px','l':'14px','arco':'999px 999px 4px 4px','pleno':'999px'}
prim['medida']['espacio']={k:{'$value':v,'$type':'dimension'} for k,v in ESPACIO.items()}
prim['medida']['radio']={k:{'$value':v,'$type':'dimension'} for k,v in RADIO.items()}
prim['tipo']['escala']={k:{'$value':v['clamp'],'$type':'dimension'} for k,v in TS.items()}
prim['tipo']['familia']={
 'display':{'$value':"'Archivo', 'Archivo Expanded', system-ui, sans-serif",'$type':'fontFamily'},
 'texto':{'$value':"'Archivo', system-ui, -apple-system, sans-serif",'$type':'fontFamily'},
 'dato':{'$value':"'JetBrains Mono', ui-monospace, 'SF Mono', monospace",'$type':'fontFamily'}}

# ---------- CAPA 2: semantica ----------
OSC = {
 'superficie':{'abismo':C('sustrato',100),'base':C('sustrato',200),'elevada':C('sustrato',300),
               'membrana':C('sustrato',400),'inversa':C('hueso',100)},
 'borde':{'tenue':C('sustrato',500),'definido':C('sustrato','d32'),'foco':C('biolum','d70')},
 'texto':{'primario':C('hueso',100),'secundario':C('hueso',500),'tenue':C('sustrato',800),
          'inverso':C('sustrato',100),'sobre-acento':C('sustrato',100)},
 'acento':{'base':C('biolum','d70'),'fuerte':C('biolum','d110'),'sordo':C('biolum','d15')},
}
CLA = {
 'superficie':{'abismo':C('hueso',300),'base':C('hueso',100),'elevada':'#FFFFFF',
               'membrana':C('hueso',200),'inversa':C('sustrato',100)},
 'borde':{'tenue':C('hueso',400),'definido':C('hueso','l32'),'foco':C('biolum','l45')},
 'texto':{'primario':C('sustrato',100),'secundario':C('sustrato',400),'tenue':C('sustrato',600),
          'inverso':C('hueso',100),'sobre-acento':C('hueso',100)},
 'acento':{'base':C('biolum','l70'),'fuerte':C('biolum','l110'),'sordo':C('hueso',200)},
}
# estados: fondo / borde / texto (verificados entre si)
EST_OSC = {
 'vigente':      (C('biolum','d15'),  C('biolum','d32'),  C('biolum','d110')),
 'por-vencer':   (C('ambar','d15'),   C('ambar','d32'),   C('ambar','d110')),
 'vencido':      (C('sustrato',300),  C('sustrato','d32'),  C('sustrato',800)),
 'negado':       (C('carmin','d15'),  C('carmin','d32'),  C('carmin','d110')),
 'sin-confirmar':('transparent',      C('sustrato','d32'),  C('hueso',500)),
 'identidad':    (C('violeta','d15'), C('violeta','d32'), C('violeta','d110')),
}
EST_CLA = {
 'vigente':      (C('hueso',100), C('biolum','l32'),  C('biolum','l70')),
 'por-vencer':   (C('hueso',100), C('ambar','l32'),   C('ambar','l70')),
 'vencido':      (C('hueso',300), C('hueso','l32'),     C('sustrato',600)),
 'negado':       (C('hueso',100), C('carmin','l32'),  C('carmin','l70')),
 'sin-confirmar':('transparent',  C('hueso','l32'),     C('sustrato',500)),
 'identidad':    (C('hueso',100), C('violeta','l32'), C('violeta','l70')),
}
# ---------- verificacion ----------
for tema,S,E in [('oscuro',OSC,EST_OSC),('claro',CLA,EST_CLA)]:
    b=S['superficie']['base']
    chk(S['texto']['primario'],b,4.5,f'{tema}: texto primario / superficie base')
    chk(S['texto']['secundario'],b,4.5,f'{tema}: texto secundario / superficie base')
    chk(S['texto']['tenue'],b,3.0,f'{tema}: texto tenue / superficie base')
    chk(S['acento']['base'],b,3.0,f'{tema}: acento / superficie base')
    chk(S['texto']['sobre-acento'],S['acento']['base'],4.5,f'{tema}: texto sobre acento')
    chk(S['borde']['definido'],b,3.0,f'{tema}: borde definido / superficie base')
    for n,(f,bo,t) in E.items():
        fondo = b if f=='transparent' else f
        chk(t,fondo,4.5,f'{tema}: texto de estado {n}')
        chk(bo,b,3.0,f'{tema}: borde de estado {n}')

sem = {'oscuro':OSC,'claro':CLA,'estado':{'oscuro':EST_OSC,'claro':EST_CLA}}
json.dump({'$description':'Kino — tokens DTCG. Capa 1 primitivos, capa 2 semantica, capa 3 tenant.',
           'primitivo':prim,'semantico':sem}, open('motor/semantica.json','w'), indent=1, ensure_ascii=False)
json.dump(checks, open('contraste.json','w'), indent=1, ensure_ascii=False)

fail=[c for c in checks if not c['pasa']]
print('verificaciones: %d  fallan: %d'%(len(checks),len(fail)))
for c in fail: print('  FALLA', c['par'], c['fg'],'/',c['bg'],'=',c['wcag'],'min',c['minimo'])
