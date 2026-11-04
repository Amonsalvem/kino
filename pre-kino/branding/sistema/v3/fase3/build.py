import json,re,random,html
from apca import lc
e=html.escape
src=open('explorar.src.html').read()
import pathlib
R=pathlib.Path(__file__).resolve().parent
_dtcg=R/'../../../../gorr-brand-system/clientes/kino/build/kino-tokens.css'
tok=(_dtcg if _dtcg.exists() else R/'../sitio/kino-tokens.css').read_text(encoding='utf8')
o=json.load(open('oscuro-ajustado.json'))
sp=open(R/'../sitio/sprite.svg').read(); sp=re.search(r'<defs>(.*)</defs>',sp,re.S).group(1)
mark=open('mark.json').read(); word=json.dumps(open('wordmark.txt').read())
random.seed(4); c=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 500"><rect width="400" height="500" fill="#011F16"/>']
for _ in range(70):
  x,y,r=random.uniform(0,400),random.uniform(0,500),random.uniform(18,46)
  c.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="#0B2A20" stroke="#2A483D" stroke-width="1.5"/><circle cx="{x+r*.2:.0f}" cy="{y-r*.15:.0f}" r="{r*.18:.0f}" fill="#17362B"/>')
c.append('</svg>'); cel=''.join(c)
E=[('Previsto','previsto','Pase creado para una franja futura.'),('Sin confirmar','sin-confirmar','Enviado; el lector aún no responde.'),('Vigente','vigente','El lector lo confirmó y está en su franja.'),('Por vencer','por-vencer','Entra en la ventana de aviso.'),('Usado','usado','Código de un solo uso que ya sirvió.'),('Vencido','vencido','Terminó solo. Un final no es un error.'),('Revocado','revocado','Alguien lo cortó; queda su nombre.'),('Rechazado','rechazado','Evento en la entrada, con motivo.'),('Dato personal','identidad','Cédula, rostro o teléfono a la vista.')]
def chip(n,k): return f'<span class="chip{" sc" if k=="sin-confirmar" else ""}" style="color:{o[k+"-texto"]};background:{o[k+"-fondo"] if k!="sin-confirmar" else "transparent"};border-color:{o[k+"-borde"]}">{n}</span>'
fondo=lambda k: o[k+"-fondo"] if k!="sin-confirmar" else "#011F16"
chips=''.join(chip(n,k) for n,k,_ in E)
filas=''.join(f'<tr><td>{chip(n,k)}</td><td>{e(d)}</td><td class="mono"><span class="sw" style="background:{o[k+"-texto"]}"></span>{o[k+"-texto"]}</td><td class="mono">{abs(lc(o[k+"-texto"],fondo(k)))}</td><td class="mono">{abs(lc(o[k+"-borde"],fondo(k)))}</td></tr>' for n,k,d in E)
base_rows=[('Texto secundario','#BECBC6',o['texto-secundario'],'#17362B',75),('Texto tenue (solo ≥ 24 px)','#86A799',o['texto-tenue'],'#17362B',60),('Borde con información','#517064',o['borde-definido'],'#17362B',30)]
bf=''.join(f'<tr><td>{n}</td><td class="mono">{a}</td><td class="mono">{abs(lc(a,bg))}</td><td class="mono">{b}</td><td class="mono"><b>{abs(lc(b,bg))}</b></td><td class="mono">≥ {m}</td></tr>' for n,a,b,bg,m in base_rows)
bf+=f'<tr><td>Texto sobre el botón Crear Pase</td><td class="mono">#00140C sobre #00BB83</td><td class="mono">{lc("#00140C","#00BB83")}</td><td class="mono">#00140C sobre #00D595</td><td class="mono"><b>{lc("#00140C","#00D595")}</b></td><td class="mono">≥ 60</td></tr>'
estados=open('estados.tpl').read().format(chips=chips,bf=bf,filas=filas)
preg=open('preguntas.tpl').read()
s=src.replace('{{TOKENS}}',tok).replace('{{T_SEC}}',o['texto-secundario']).replace('{{T_TEN}}',o['texto-tenue']).replace('{{B_DEF}}',o['borde-definido'])
s=s.replace('{{VIG_T}}',o['vigente-texto']).replace('{{VIG_F}}',o['vigente-fondo']).replace('{{VIG_B}}',o['vigente-borde'])
s=s.replace('{{SPRITE}}',sp).replace('{{MARK}}',mark).replace('{{WORD}}',word).replace('{{CELULAS}}',cel)
s=s.replace('{{HTML_EXTRA}}',json.dumps({'estados':estados,'preguntas':preg},ensure_ascii=False))
open('parada-3.html','w').write(s); print(len(s)//1024,'KB')
