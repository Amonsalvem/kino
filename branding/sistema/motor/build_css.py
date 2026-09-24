import json
T=json.load(open('kino-tokens.json'))
P=T['primitivo']; S=T['semantico']
L=[]
L.append("/* Kino — capa de marca. Generado desde kino-tokens.json (formato DTCG).")
L.append("   No editar a mano: editar los tokens y regenerar. */")
L.append("@import url('https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,100..900;1,62..125,100..900&family=JetBrains+Mono:wght@400;500;700&display=swap');")
L.append("/* Para producción: autoalojar ambas familias (OFL 1.1) y borrar el @import. */\n")

def block(sel, pairs, indent='  '):
    L.append(sel+' {')
    for k,v in pairs: L.append(f'{indent}{k}: {v};')
    L.append('}\n')

prim=[]
for fam,steps in P['color'].items():
    for k,v in steps.items(): prim.append((f'--kino-{fam}-{k}', v['$value']))
for k,v in P['medida']['espacio'].items(): prim.append((f'--kino-espacio-{k}', v['$value']))
for k,v in P['medida']['radio'].items():   prim.append((f'--kino-radio-{k}', v['$value']))
for k,v in P['tipo']['escala'].items():    prim.append((f'--kino-texto-{k.replace("-","n")}', v['$value']))
for k,v in P['tipo']['familia'].items():   prim.append((f'--kino-fuente-{k}', v['$value']))
prim += [('--kino-peso-display','800'),('--kino-peso-titulo','700'),('--kino-peso-texto','400'),
         ('--kino-peso-dato','500'),('--kino-ancho-display','112'),
         ('--kino-interlinea-apretada','1.04'),('--kino-interlinea-titulo','1.16'),
         ('--kino-interlinea-texto','1.6'),('--kino-tracking-display','-0.02em'),
         ('--kino-tracking-dato','0.04em'),
         ('--kino-transicion-crecer','420ms cubic-bezier(.16,.84,.30,1)'),
         ('--kino-transicion-decaer','900ms cubic-bezier(.62,.03,.86,.34)'),
         ('--kino-transicion-pulso','1800ms cubic-bezier(.45,0,.55,1)'),
         ('--kino-medida-columna','62ch'),('--kino-reticula-columnas','12'),
         ('--kino-reticula-canal','var(--kino-espacio-l)')]
block(':root', prim)

def sem_pairs(theme):
    d=S[theme]; out=[]
    for grupo in ['superficie','borde','texto','acento']:
        for k,v in d[grupo].items(): out.append((f'--kino-{grupo}-{k}', v))
    for n,(f,b,t) in S['estado'][theme].items():
        out += [(f'--kino-estado-{n}-fondo',f),(f'--kino-estado-{n}-borde',b),(f'--kino-estado-{n}-texto',t)]
    out += [('color-scheme','dark' if theme=='oscuro' else 'light')]
    return out

L.append('/* Tema canónico: oscuro. El sustrato es el estado por defecto de la marca. */')
block(':root, :root[data-tema="oscuro"]', sem_pairs('oscuro'))
block(':root[data-tema="claro"]', sem_pairs('claro'))
L.append('@media (prefers-color-scheme: light) {')
L.append('  :root:not([data-tema="oscuro"]) {')
for k,v in sem_pairs('claro'): L.append(f'    {k}: {v};')
L.append('  }\n}\n')

L.append("""/* ---- Capa 3: tenant (marca blanca) ----
   Un conjunto puede cambiar la piel. No puede cambiar los estados:
   vigente, por vencer, vencido, negado, sin confirmar e identidad
   significan lo mismo en todos los conjuntos, o la trazabilidad deja de ser comparable. */""")
block(':root', [('--kino-tenant-nombre','"Kino"'),
                ('--kino-tenant-acento','var(--kino-acento-base)'),
                ('--kino-tenant-marca','var(--kino-acento-base)'),
                ('--kino-tenant-radio','var(--kino-radio-m)')])

L.append("""/* ---- Base ---- */
*, *::before, *::after { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body {
  margin: 0;
  background: var(--kino-superficie-base);
  color: var(--kino-texto-primario);
  font-family: var(--kino-fuente-texto);
  font-size: var(--kino-texto-0);
  line-height: var(--kino-interlinea-texto);
  font-variation-settings: 'wdth' 100;
}
h1, h2, h3 { font-family: var(--kino-fuente-display); line-height: var(--kino-interlinea-titulo);
  letter-spacing: var(--kino-tracking-display); font-weight: var(--kino-peso-display);
  font-variation-settings: 'wdth' var(--kino-ancho-display); text-wrap: balance; margin: 0 0 var(--kino-espacio-m); }
h1 { font-size: var(--kino-texto-5); line-height: var(--kino-interlinea-apretada); }
h2 { font-size: var(--kino-texto-3); }
h3 { font-size: var(--kino-texto-1); }
p  { max-width: var(--kino-medida-columna); text-wrap: pretty; }
.kino-dato { font-family: var(--kino-fuente-dato); font-weight: var(--kino-peso-dato);
  letter-spacing: var(--kino-tracking-dato); font-variant-numeric: tabular-nums slashed-zero; }
:where(a, button, input, select, [tabindex]):focus-visible {
  outline: 2px solid var(--kino-borde-foco); outline-offset: 2px; border-radius: var(--kino-radio-s); }

/* ---- Estados: el color solo nombra hechos confirmados ---- */
.kino-estado { display: inline-flex; align-items: center; gap: var(--kino-espacio-2xs);
  padding: var(--kino-espacio-3xs) var(--kino-espacio-xs); border-radius: var(--kino-radio-s);
  border: 1px solid currentColor; font-family: var(--kino-fuente-dato);
  font-size: var(--kino-texto-n1); letter-spacing: var(--kino-tracking-dato); text-transform: uppercase; }
.kino-estado::before { content: ''; inline-size: .5em; block-size: .5em; border-radius: var(--kino-radio-pleno);
  background: currentColor; flex: none; }
.kino-estado[data-estado="vigente"]       { background: var(--kino-estado-vigente-fondo);
  border-color: var(--kino-estado-vigente-borde); color: var(--kino-estado-vigente-texto); }
.kino-estado[data-estado="vigente"]::before { animation: kino-latido var(--kino-transicion-pulso) ease-in-out infinite; }
.kino-estado[data-estado="por-vencer"]    { background: var(--kino-estado-por-vencer-fondo);
  border-color: var(--kino-estado-por-vencer-borde); color: var(--kino-estado-por-vencer-texto); }
.kino-estado[data-estado="vencido"]       { background: var(--kino-estado-vencido-fondo);
  border-color: var(--kino-estado-vencido-borde); color: var(--kino-estado-vencido-texto); }
.kino-estado[data-estado="negado"]        { background: var(--kino-estado-negado-fondo);
  border-color: var(--kino-estado-negado-borde); color: var(--kino-estado-negado-texto); }
.kino-estado[data-estado="identidad"]     { background: var(--kino-estado-identidad-fondo);
  border-color: var(--kino-estado-identidad-borde); color: var(--kino-estado-identidad-texto); }
/* Sin confirmar: sin relleno y con borde discontinuo. La interfaz no afirma lo que el lector no confirmó. */
.kino-estado[data-estado="sin-confirmar"] { background: transparent; border-style: dashed;
  border-color: var(--kino-estado-sin-confirmar-borde); color: var(--kino-estado-sin-confirmar-texto); }
.kino-estado[data-estado="sin-confirmar"]::before { background: transparent;
  border: 1px dashed currentColor; }

/* ---- Vigencia: la vida que le queda a un permiso ---- */
.kino-vigencia { --kino-vida: 1; display: block; block-size: 3px; inline-size: 100%;
  background: var(--kino-borde-tenue); border-radius: var(--kino-radio-pleno); overflow: hidden; }
.kino-vigencia::after { content: ''; display: block; block-size: 100%;
  inline-size: calc(var(--kino-vida) * 100%); background: var(--kino-estado-vigente-texto);
  transition: inline-size var(--kino-transicion-decaer); }
.kino-vigencia[data-aviso="por-vencer"]::after { background: var(--kino-estado-por-vencer-texto); }
.kino-vigencia[data-aviso="vencido"]::after    { background: var(--kino-estado-vencido-texto); }

@keyframes kino-latido { 0%,100% { opacity: 1; } 50% { opacity: .35; } }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: .001ms !important; transition-duration: .001ms !important; }
}

/* ---- Marca ---- */
.kino-marca { color: var(--kino-tenant-marca); display: inline-block; }
.kino-marca svg { display: block; block-size: 100%; inline-size: auto; }
""")
open('kino-brand.css','w').write('\n'.join(L))
print('kino-brand.css', len('\n'.join(L)), 'bytes')
