import json, sys; sys.path.insert(0,'.')
T=json.load(open('kino-tokens.json')); P=json.load(open('palette.json'))['paleta']
S=T['semantico']; OSC=S['oscuro']; CLA=S['claro']; EO=S['estado']['oscuro']; EC=S['estado']['claro']

col=[]; used=set()
def add(name, osc, cla, usage):
    col.append({'name':name,'value':{'oscuro':osc,'claro':cla},'usage':usage})
    used.add(osc); used.add(cla)

U = {
 'superficie-abismo':'Fondo de la aplicación bajo todo lo demás: el sustrato. Texto: kino-texto-primario.',
 'superficie-base':'Superficie por defecto de página y pantalla. Es el fondo contra el que se generó toda la escala.',
 'superficie-elevada':'Paneles y hojas que flotan sobre la base.',
 'superficie-membrana':'Tarjetas: un permiso, una persona, un vehículo. La unidad que se puede abrir.',
 'superficie-inversa':'Bloques invertidos y el reverso de la marca.',
 'borde-tenue':'Separadores dentro de una misma superficie. No transporta significado.',
 'borde-definido':'Borde de control (campo, botón secundario). 3:1 sobre kino-superficie-base.',
 'borde-foco':'Anillo de foco de teclado. Sólido, nunca punteado, nunca solo color.',
 'texto-primario':'Texto corrido y títulos sobre kino-superficie-base, -elevada y -membrana.',
 'texto-secundario':'Etiquetas y texto de apoyo sobre las mismas superficies.',
 'texto-tenue':'Metadatos de baja prioridad, 24px o más, o en negrita desde 19px.',
 'texto-inverso':'Texto sobre kino-superficie-inversa.',
 'texto-sobre-acento':'Texto y iconos sobre kino-acento-base. Nunca blanco literal.',
 'acento-base':'Acción principal: el botón que otorga un permiso. Bioluminiscencia.',
 'acento-fuerte':'Estado presionado y enlaces sobre superficies oscuras.',
 'acento-sordo':'Relleno de apoyo del acento. No es texto.',
}
for grupo in ['superficie','borde','texto','acento']:
    for k in OSC[grupo]:
        n=f'kino-{grupo}-{k}'
        add(n, OSC[grupo][k], CLA[grupo][k], U[f'{grupo}-{k}'])

EU={
 'vigente':'Permiso vivo y confirmado por el lector.',
 'por-vencer':'Vigencia que se agota dentro de la ventana de aviso.',
 'vencido':'Permiso que terminó su vida. Sin color: no es un error, es un final.',
 'negado':'Ingreso rechazado o permiso revocado.',
 'sin-confirmar':'Lo que la app aún no sabe del mundo físico. Sin relleno y con borde discontinuo.',
 'identidad':'Dato personal o biométrico: cédula, rostro, teléfono. Zona regulada.',
}
for n in EO:
    for i,parte in enumerate(['fondo','borde','texto']):
        add(f'kino-estado-{n}-{parte}',
            '#00000000' if EO[n][i]=='transparent' else EO[n][i],
            '#00000000' if EC[n][i]=='transparent' else EC[n][i],
            {'fondo':f'Relleno del estado «{n}». {EU[n]}',
             'borde':f'Borde del estado «{n}». 3:1 sobre kino-superficie-base.',
             'texto':f'Texto e indicador del estado «{n}». 4.5:1 sobre su propio relleno.'}[parte])

# primitivos efectivamente usados + escalas neutras completas
prim=[]
LIN={'sustrato':'Carbón #2C2D2F de la Propuesta 1, sesgado al verde del medio de cultivo.',
     'hueso':'Hueso #E1E8EE de la Propuesta 1, enfriado hacia el verde.',
     'biolum':'Menta #B2E8DB de la Propuesta 1 con el chroma llevado al límite del gamut.',
     'ambar':'Familia nueva: no existía lenguaje para la vigencia que se agota.',
     'carmin':'Familia nueva: no existía lenguaje para el rechazo.',
     'violeta':'Morado #7266CA de la Propuesta 1, intacto. Ahora significa identidad.',
     'indigo':'Índigo #00177D de la Propuesta 1. Profundidad y enlaces.'}
for fam in ['sustrato','hueso']:
    for k in ['100','200','300','400','500','600','700','800']:
        prim.append({'name':f'kino-{fam}-{k}','value':P[fam][k],
            'usage':f'Primitivo. {LIN[fam]} Paso {k} de la escala de luminosidad OKLCh.'})
for fam in ['biolum','ambar','carmin','violeta','indigo']:
    for k,v in P[fam].items():
        if v in used:
            base = 'fondo oscuro' if k.startswith('d') else 'fondo claro'
            prim.append({'name':f'kino-{fam}-{k}','value':v,
                'usage':f'Primitivo. {LIN[fam]} Generado a {int(k[1:])/10}:1 sobre el {base}.'})

tokens={
 'name':'Kino','version':1,
 'meta':{'source':'Inspección de la app por rol, sep 2026 + tablero Propuesta 1'},
 'color':{'themes':[{'id':'oscuro','name':'Sustrato'},{'id':'claro','name':'Laboratorio'}],
          'tokens':col+prim},
 'type':{
   'families':{
     'display':'"Archivo", "Archivo Expanded", system-ui, sans-serif',
     'texto':'"Archivo", system-ui, -apple-system, sans-serif',
     'dato':'"JetBrains Mono", ui-monospace, "SF Mono", monospace'},
   'groups':[
    {'name':'Display','family':'display','styles':[
      {'name':'display-1','fontSize':'72px','lineHeight':'1.04','fontWeight':800,'letterSpacing':'-0.02em','usage':'Portada y apertura de sección. Una sola por pantalla.','sample':'Quién entra'},
      {'name':'display-2','fontSize':'57px','lineHeight':'1.04','fontWeight':800,'letterSpacing':'-0.02em','usage':'Cifra o afirmación única en un lienzo.','sample':'0 de 312'},
      {'name':'display-3','fontSize':'45px','lineHeight':'1.08','fontWeight':800,'letterSpacing':'-0.015em','usage':'Título de lámina en deck.','sample':'La membrana'}]},
    {'name':'Título','family':'display','styles':[
      {'name':'titulo-1','fontSize':'36px','lineHeight':'1.16','fontWeight':700,'usage':'Título de pantalla.','sample':'Acceso previsto'},
      {'name':'titulo-2','fontSize':'28px','lineHeight':'1.2','fontWeight':700,'usage':'Título de sección dentro de una pantalla.','sample':'Quién autorizó'},
      {'name':'titulo-3','fontSize':'23px','lineHeight':'1.25','fontWeight':700,'usage':'Título de tarjeta o de grupo.','sample':'Colaboradores'}]},
    {'name':'Texto','family':'texto','styles':[
      {'name':'cuerpo','fontSize':'18px','lineHeight':'1.6','fontWeight':400,'usage':'Texto corrido en documentos y manual.','sample':'El residente ya concede acceso físico al registrar una placa.'},
      {'name':'cuerpo-s','fontSize':'16px','lineHeight':'1.55','fontWeight':400,'usage':'Texto por defecto en la aplicación.','sample':'Permiso válido hasta el viernes a las 6:00 p. m.'},
      {'name':'menor','fontSize':'14px','lineHeight':'1.5','fontWeight':400,'usage':'Pies de tabla y texto de apoyo. Nunca para un estado.','sample':'Autorizado por Ana Ruiz, casa 14'}]},
    {'name':'Dato','family':'dato','styles':[
      {'name':'placa','fontSize':'23px','lineHeight':'1.2','fontWeight':700,'letterSpacing':'0.06em','usage':'Placa de vehículo y código de un solo uso. Cifras tabulares y cero barrado.','sample':'HTK 481'},
      {'name':'dato','fontSize':'16px','lineHeight':'1.4','fontWeight':500,'letterSpacing':'0.04em','usage':'Horas, fechas, cédulas e identificadores en línea.','sample':'19 sep · 14:32'},
      {'name':'etiqueta','fontSize':'13px','lineHeight':'1.3','fontWeight':500,'letterSpacing':'0.08em','usage':'Etiqueta de estado en versalitas. Siempre acompañada de palabra, no solo color.','sample':'SIN CONFIRMAR'}]}]},
 'spacing':{'tokens':[
   {'name':'kino-espacio-3xs','value':'2px','usage':'Separación entre el punto de estado y su palabra.'},
   {'name':'kino-espacio-2xs','value':'4px','usage':'Relleno vertical de una etiqueta de estado.'},
   {'name':'kino-espacio-xs','value':'8px','usage':'Relleno horizontal de una etiqueta; separación entre iconos.'},
   {'name':'kino-espacio-s','value':'12px','usage':'Separación entre campos de un formulario.'},
   {'name':'kino-espacio-m','value':'16px','usage':'Relleno interno de tarjeta y separación entre párrafos.'},
   {'name':'kino-espacio-l','value':'24px','usage':'Canal de la retícula y separación entre tarjetas.'},
   {'name':'kino-espacio-xl','value':'32px','usage':'Separación entre bloques dentro de una pantalla.'},
   {'name':'kino-espacio-2xl','value':'48px','usage':'Separación entre secciones.'},
   {'name':'kino-espacio-3xl','value':'72px','usage':'Margen superior de una lámina de deck.'},
   {'name':'kino-espacio-4xl','value':'112px','usage':'Aire de portada.'}]},
 'radius':{'tokens':[
   {'name':'kino-radio-nada','value':'0','usage':'Bordes que se apoyan en el borde de la pantalla o de la lámina.'},
   {'name':'kino-radio-xs','value':'2px','usage':'Indicador de vigencia y microbarras.'},
   {'name':'kino-radio-s','value':'4px','usage':'Etiquetas de estado, campos, anillo de foco.'},
   {'name':'kino-radio-m','value':'8px','usage':'Tarjetas y botones. Radio por defecto del tenant.'},
   {'name':'kino-radio-l','value':'14px','usage':'Hojas y paneles grandes.'},
   {'name':'kino-radio-pleno','value':'999px','usage':'Puntos de estado y barras de vigencia.'}]},
 'shadow':{'note':'Kino no usa sombra proyectada: usa resplandor. Una superficie viva emite luz; una apagada, no.',
   'tokens':[
   {'name':'kino-resplandor-vigente','value':{'oscuro':'0 0 0 1px '+P['biolum']['d45']+', 0 0 28px -8px '+P['biolum']['d110'],
                                              'claro':'0 0 0 1px '+P['biolum']['l45']+', 0 0 22px -10px '+P['biolum']['l45']},
    'usage':'Tarjeta de permiso vigente y botón principal en foco.'},
   {'name':'kino-resplandor-identidad','value':{'oscuro':'0 0 0 1px '+P['violeta']['d45']+', 0 0 28px -8px '+P['violeta']['d110'],
                                                'claro':'0 0 0 1px '+P['violeta']['l45']+', 0 0 22px -10px '+P['violeta']['l45']},
    'usage':'Bloque que muestra o captura un dato personal o biométrico.'},
   {'name':'kino-relieve-membrana','value':{'oscuro':'0 1px 0 0 '+P['sustrato']['500']+' inset, 0 12px 32px -20px #000000',
                                            'claro':'0 1px 0 0 #ffffff inset, 0 10px 26px -20px #0b201a'},
    'usage':'Elevación mínima de una tarjeta sobre la superficie base.'}]},
}
json.dump(tokens, open('ds/project/tokens.json','w'), indent=1, ensure_ascii=False)
print('color tokens:', len(tokens['color']['tokens']), '| semanticos:', len(col), '| primitivos:', len(prim))
