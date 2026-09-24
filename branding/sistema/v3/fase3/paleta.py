import math, json
from apca import lc, wcag
def srgb2lin(c): return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
def lin2srgb(c): return 12.92*c if c<=0.0031308 else 1.055*c**(1/2.4)-0.055
def hex2oklch(h):
    h=h.lstrip('#'); r,g,b=[srgb2lin(int(h[i:i+2],16)/255) for i in (0,2,4)]
    l=0.4122214708*r+0.5363325363*g+0.0514459929*b; m=0.2119034982*r+0.6806995451*g+0.1073969566*b; s=0.0883024619*r+0.2817188376*g+0.6299787005*b
    l,m,s=[x**(1/3) for x in (l,m,s)]
    L=0.2104542553*l+0.7936177850*m-0.0040720468*s; a=1.9779984951*l-2.4285922050*m+0.4505937099*s; bb=0.0259040371*l+0.7827717662*m-0.8086757660*s
    return L, math.hypot(a,bb), math.degrees(math.atan2(bb,a))%360
def oklch2hex(L,C,H):
    for _ in range(60):
        a=C*math.cos(math.radians(H)); b=C*math.sin(math.radians(H))
        l=(L+0.3963377774*a+0.2158037573*b)**3; m=(L-0.1055613458*a-0.0638541728*b)**3; s=(L-0.0894841775*a-1.2914855480*b)**3
        r=4.0767416621*l-3.3077115913*m+0.2309699292*s; g=-1.2684380046*l+2.6097574011*m-0.3413193965*s; bl=-0.0041960863*l-0.7034186147*m+1.7076147010*s
        if all(-1e-4<=x<=1+1e-4 for x in (r,g,bl)): break
        C*=0.95
    return '#'+''.join(f'{round(max(0,min(1,lin2srgb(max(0,x))))*255):02X}' for x in (r,g,bl))
def subir(h, bg, meta, techo=0.99):
    L,C,H=hex2oklch(h)
    while L<techo:
        x=oklch2hex(L,C,H)
        if abs(lc(x,bg))>=meta: return x
        L+=0.005
    return oklch2hex(techo,C,H)
BASE='#011F16'; ELEV='#0B2A20'; MEMB='#17362B'
out={}
out['texto-secundario']=subir('#BECBC6',MEMB,77)
out['texto-tenue']=subir('#86A799',MEMB,62)
out['borde-definido']=subir('#517064',MEMB,32)
out['borde-tenue']='#2A483D'
fondos={'vigente':'#00422C','por-vencer':'#503300','revocado':'#0B2A20','rechazado':'#79000F','identidad':'#3E1C96','previsto':'#092D93','usado':'#0B2A20','vencido':'#0B2A20','sin-confirmar':BASE}
semillas={'vigente':'#00EAA5','por-vencer':'#FFC36D','revocado':'#FFBEB8','rechazado':'#FFBEB8','identidad':'#CAC9FF','previsto':'#B6CEFF','usado':'#E5F3ED','vencido':'#A0C3B4','sin-confirmar':'#DBE9E3'}
for k,f in fondos.items():
    out[k+'-fondo']=f; out[k+'-texto']=subir(semillas[k],f,77)
    out[k+'-borde']=subir(semillas[k] if k not in('vencido','usado','sin-confirmar','revocado') else '#86A799',f,34)
rep=[]
for k,v in out.items():
    if k.endswith('-texto') or k.startswith('texto'):
        bg=out.get(k.replace('-texto','-fondo'),MEMB) if k.endswith('-texto') else MEMB
        rep.append((k,v,bg,lc(v,bg),lc(v,BASE),wcag(v,bg)))
    elif 'borde' in k:
        bg=out.get(k.replace('-borde','-fondo'),MEMB); rep.append((k,v,bg,lc(v,bg),lc(v,BASE),wcag(v,bg)))
for r in rep: print(f'{r[0]:24} {r[1]} sobre {r[2]}  Lc {r[3]:6}  (base {r[4]:6})  WCAG {r[5]}')
print('acento #00BB83 base',lc('#00BB83',BASE),' texto oscuro sobre acento',lc('#00140C','#00BB83'))
json.dump(out,open('oscuro-ajustado.json','w'),indent=1)
