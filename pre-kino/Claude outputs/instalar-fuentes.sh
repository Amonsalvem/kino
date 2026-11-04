#!/usr/bin/env bash
# Kino — autoaloja Archivo y JetBrains Mono (ambas OFL 1.1).
# Quita la dependencia de Google Fonts en tiempo de ejecución: la app de portería
# puede quedar sin conexión, y una fuente que no carga deja las placas en una
# familia de respaldo que no distingue 0 de O.
set -euo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

azul() { printf '\033[1;36m%s\033[0m\n' "$*"; }
ok()   { printf '  \033[0;32m✓\033[0m %s\n' "$*"; }
muere(){ printf '\n\033[0;31m✗ %s\033[0m\n' "$*" >&2; exit 1; }

# UA de un navegador moderno: sin esto Google Fonts devuelve TTF en vez de WOFF2.
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
mkdir -p fonts

descargar() {
  local nombre="$1" url="$2"
  azul "$nombre"
  local css
  css="$(curl -sSf --max-time 30 -H "User-Agent: $UA" "$url")" \
    || muere "no pude pedir la hoja de $nombre a Google Fonts"
  echo "$css" > "fonts/.$nombre.css"
  python3 - "$nombre" <<'PY'
import re, sys, subprocess, pathlib
nombre = sys.argv[1]
css = pathlib.Path(f'fonts/.{nombre}.css').read_text()
urls = re.findall(r'url\((https://fonts\.gstatic\.com/[^)]+\.woff2)\)', css)
if not urls:
    print('  sin woff2 en la respuesta', file=sys.stderr); sys.exit(1)
mapa = {}
for u in dict.fromkeys(urls):
    archivo = f'{nombre}-{u.rsplit("/",1)[-1]}'
    destino = pathlib.Path('fonts') / archivo
    if not destino.exists():
        subprocess.run(['curl','-sSf','--max-time','60','-o',str(destino),u], check=True)
    mapa[u] = archivo
for u, a in mapa.items():
    css = css.replace(u, a)
pathlib.Path(f'fonts/{nombre}.css').write_text(css)
print(f'  {len(mapa)} archivo(s) woff2 · fonts/{nombre}.css')
PY
  rm -f "fonts/.$nombre.css"
  ok "$nombre autoalojada"
}

descargar archivo \
  'https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,100..900;1,62..125,100..900&display=swap'
descargar jetbrains-mono \
  'https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400..700&display=swap'

# Reemplaza el @import por los dos @import locales.
python3 - <<'PY'
import re, pathlib
p = pathlib.Path('capa-componentes.css')
s = p.read_text()
nuevo = "@import url('fonts/archivo.css');\n@import url('fonts/jetbrains-mono.css');"
s2 = re.sub(r"@import url\('https://fonts\.googleapis\.com/[^']+'\);", nuevo, s, count=1)
if s2 == s:
    print('  el @import de Google Fonts ya no estaba: no toqué nada')
else:
    p.write_text(s2)
    print('  capa-componentes.css apunta ahora a fonts/')
PY

azul ""
echo "Falta reconstruir para que el cambio entre en kino-brand.css:"
echo "  npm run construir"
echo ""
echo "Las rutas de fonts/*.css son relativas al CSS, no a la página."
echo "Si kino-brand.css se sirve desde otra carpeta, ajusta el prefijo."
