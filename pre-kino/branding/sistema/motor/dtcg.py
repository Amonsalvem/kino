"""Reescribe los tokens como fuente DTCG real para Style Dictionary:
   primitivos con valor, semanticos por referencia, un archivo por tema."""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI); os.chdir(RAIZ)
import json
P=json.load(open('palette.json'))['paleta']
T=json.load(open('motor/semantica.json')); S=T['semantico']
TS=json.load(open('typescale.json'))
OUT='tokens'; os.makedirs(OUT+'/tema', exist_ok=True)

# indice inverso hex -> ruta del primitivo, para escribir referencias
ref={}
for fam,steps in P.items():
    for k,v in steps.items():
        ref.setdefault(v, f'{{primitivo.color.{fam}.{k}}}')

def col(v):
    if v in ('transparent','#00000000'): return '#00000000'
    return ref.get(v, v)

prim={'primitivo':{'color':{fam:{k:{'$value':v,'$type':'color'} for k,v in steps.items()}
                            for fam,steps in P.items()},
  'medida':{
    'espacio':{k:{'$value':v,'$type':'dimension'} for k,v in
      [('3xs','2px'),('2xs','4px'),('xs','8px'),('s','12px'),('m','16px'),
       ('l','24px'),('xl','32px'),('2xl','48px'),('3xl','72px'),('4xl','112px')]},
    'radio':{k:{'$value':v,'$type':'dimension'} for k,v in
      [('nada','0'),('xs','2px'),('s','4px'),('m','8px'),('l','14px'),
       ('arco','999px 999px 4px 4px'),('pleno','999px')]}},
  'tipo':{
    'texto':{k.replace('-1','n1'):{'$value':v['clamp'],'$type':'dimension'} for k,v in TS.items()},
    'fuente':{
      'display':{'$value':'"Archivo", "Archivo Expanded", system-ui, sans-serif','$type':'fontFamily'},
      'texto':{'$value':'"Archivo", system-ui, -apple-system, sans-serif','$type':'fontFamily'},
      'dato':{'$value':'"JetBrains Mono", ui-monospace, "SF Mono", monospace','$type':'fontFamily'}}}}}
json.dump(prim, open(OUT+'/primitivo.json','w'), indent=1, ensure_ascii=False)

for tema, clave in [('oscuro','oscuro'),('claro','claro')]:
    d=S[clave]; E=S['estado'][clave]
    sem={'semantico':{}}
    for grupo in ['superficie','borde','texto','acento']:
        sem['semantico'][grupo]={k:{'$value':col(v),'$type':'color'} for k,v in d[grupo].items()}
    sem['semantico']['estado']={}
    for n,(f,b,t) in E.items():
        sem['semantico']['estado'][n]={
          'fondo':{'$value':col(f),'$type':'color'},
          'borde':{'$value':col(b),'$type':'color'},
          'texto':{'$value':col(t),'$type':'color'}}
    # Sombras. Kino no usa sombra proyectada: usa resplandor.
    # Van por referencia igual que el color, para que cambiar un matiz las arrastre.
    r = (lambda fam, paso: '{primitivo.color.%s.%s}' % (fam, paso))
    if clave == 'oscuro':
        sem['semantico']['resplandor'] = {
          'vigente':   {'$value': f"0 0 0 1px {r('biolum','d45')}, 0 0 28px -8px {r('biolum','d110')}", '$type': 'shadow'},
          'identidad': {'$value': f"0 0 0 1px {r('violeta','d45')}, 0 0 28px -8px {r('violeta','d110')}", '$type': 'shadow'}}
        sem['semantico']['relieve'] = {
          'membrana':  {'$value': f"0 1px 0 0 {r('sustrato','500')} inset, 0 12px 32px -20px #000000", '$type': 'shadow'}}
    else:
        sem['semantico']['resplandor'] = {
          'vigente':   {'$value': f"0 0 0 1px {r('biolum','l45')}, 0 0 22px -10px {r('biolum','l45')}", '$type': 'shadow'},
          'identidad': {'$value': f"0 0 0 1px {r('violeta','l45')}, 0 0 22px -10px {r('violeta','l45')}", '$type': 'shadow'}}
        sem['semantico']['relieve'] = {
          'membrana':  {'$value': "0 1px 0 0 #ffffff inset, 0 10px 26px -20px #0b201a", '$type': 'shadow'}}
    json.dump(sem, open(f'{OUT}/tema/{tema}.json','w'), indent=1, ensure_ascii=False)

# pares a verificar, por nombre de token
pares=[]
def p(fg,bg,minimo,que): pares.append({'que':que,'fg':fg,'bg':bg,'min':minimo})
p('kino-texto-primario','kino-superficie-base',4.5,'texto primario sobre superficie base')
p('kino-texto-secundario','kino-superficie-base',4.5,'texto secundario sobre superficie base')
p('kino-texto-tenue','kino-superficie-base',3.0,'texto tenue sobre superficie base')
p('kino-acento-base','kino-superficie-base',3.0,'acento sobre superficie base')
p('kino-texto-sobre-acento','kino-acento-base',4.5,'texto sobre acento')
p('kino-borde-definido','kino-superficie-base',3.0,'borde definido sobre superficie base')
p('kino-texto-inverso','kino-superficie-inversa',4.5,'texto inverso sobre superficie inversa')
for n in S['estado']['oscuro']:
    fondo = 'kino-superficie-base' if n=='sin-confirmar' else f'kino-estado-{n}-fondo'
    p(f'kino-estado-{n}-texto', fondo, 4.5, f'texto del estado {n}')
    p(f'kino-estado-{n}-borde', 'kino-superficie-base', 3.0, f'borde del estado {n}')
json.dump(pares, open('pares.json','w'), indent=1, ensure_ascii=False)
print('primitivos:', sum(len(v) for v in prim['primitivo']['color'].values()), 'colores')
print('pares por tema:', len(pares))
