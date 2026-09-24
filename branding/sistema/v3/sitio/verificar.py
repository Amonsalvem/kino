import re,json
t=open('texto-visible.md').read().split('\n')
chk={'rayas':'—','permiso':r'(?i)(?<![\wá-ú])permisos?(?![\wá-ú])'}
for k,p in chk.items():
  h=[l for l in t if re.search(p,l)]; print(k,len(h)); [print('  ',x[:100]) for x in h[:5]]
ux=json.load(open('build/verbal-verificacion.json'))
usted=re.compile(r'(?i)\b(usted|ustedes|su|sus|le)\b')
tu=re.compile(r'(?i)\b(tú|tu|tus|te|tienes|puedes|escribe|elige|revisa|revoca|muestra|acerca|avanza|dile|pídele|entra|crea|copia|ignora)\b')
mix=[u for u in ux if not u['momento'].startswith('Administración') and usted.search(u['texto']) and not re.search(r'(?i)\ble (llega|dio|pidió)\b',u['texto'])]
print('tú/usted residente-visita, posibles usted:',len(mix)); [print('  ',m['momento'],'::',m['texto']) for m in mix]
print('fuera de límite:',sum(not u['pasa'] for u in ux),'de',len(ux))
