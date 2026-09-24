#!/usr/bin/env bash
# Kino — instalación de la cadena de tokens.
# Ejecutar desde kino/branding/sistema/ en una terminal con red:
#   bash instalar.sh
set -euo pipefail

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$AQUI"

azul()  { printf '\033[1;36m%s\033[0m\n' "$*"; }
ok()    { printf '  \033[0;32m✓\033[0m %s\n' "$*"; }
aviso() { printf '  \033[0;33m!\033[0m %s\n' "$*"; }
muere() { printf '\n\033[0;31m✗ %s\033[0m\n' "$*" >&2; exit 1; }

# ---------------------------------------------------------------- 1. requisitos
azul "1/6  Requisitos"

command -v node >/dev/null 2>&1 || muere "No hay node. Instálalo con: brew install node"
command -v npm  >/dev/null 2>&1 || muere "No hay npm. Viene con node."
command -v python3 >/dev/null 2>&1 || muere "No hay python3. En macOS: xcode-select --install"

NODE_MAYOR="$(node -p 'process.versions.node.split(".")[0]')"
[ "$NODE_MAYOR" -ge 20 ] || muere "Node $(node -v): Style Dictionary 5 necesita Node 20 o superior. Actualiza con: brew upgrade node"
ok "node $(node -v)"
ok "npm  v$(npm -v)"
ok "python3 $(python3 -V | cut -d' ' -f2)"

if ! curl -sSf -o /dev/null --max-time 10 https://registry.npmjs.org/ 2>/dev/null; then
  muere "No hay salida a registry.npmjs.org desde esta terminal.
   Si estás dentro del shell de Cowork o de un proxy corporativo, sal de ahí:
   esto va en Terminal.app normal."
fi
ok "registry.npmjs.org alcanzable"

# ---------------------------------------------------------------- 2. instalar
azul "2/6  Dependencias"
echo "     Se instalan en @latest y se registra la versión resuelta."

npm install --save-dev --silent style-dictionary@latest colorjs.io@latest
npm install --save    --silent iconoir@latest

SD_VER="$(node -p "require('./node_modules/style-dictionary/package.json').version")"
CJ_VER="$(node -p "require('./node_modules/colorjs.io/package.json').version")"
IC_VER="$(node -p "require('./node_modules/iconoir/package.json').version")"
ok "style-dictionary $SD_VER"
ok "colorjs.io       $CJ_VER"
ok "iconoir          $IC_VER"

# ---------------------------------------------------------------- 3. compatibilidad
azul "3/6  Compatibilidad"
# construir-tokens.mjs está escrito para la API de Style Dictionary 5 (ESM, registerTransform con `transform`).
# La 3 y la 4 usan CommonJS y `transformer`: el build saldría mal en silencio.
SD_MAYOR="${SD_VER%%.*}"
if [ "$SD_MAYOR" != "5" ]; then
  muere "Style Dictionary $SD_VER. construir-tokens.mjs está escrito para la 5.
   Con la 3 o la 4 hay que cambiar 'transform:' por 'transformer:' y reescribir el build en CommonJS.
   Instala la 5 con: npm install --save-dev style-dictionary@^5"
fi
ok "Style Dictionary 5: la API que espera construir-tokens.mjs"

# color.js: se comprueba contra valores conocidos antes de confiar en sus cifras.
node --input-type=module -e "
import Color from 'colorjs.io';
const b = new Color('#000000'), w = new Color('#ffffff');
// color.js expone contrast(fondo, frente): el receptor es el fondo.
const wcag = w.contrast(b, 'WCAG21');
const claro = w.contrast(b, 'APCA');   // texto negro sobre blanco  -> ~106
const oscuro = b.contrast(w, 'APCA');  // texto blanco sobre negro  -> ~-107.9
if (Math.abs(wcag - 21) > 0.01)      { console.error('WCAG21 dio ' + wcag + ', se esperaba 21'); process.exit(1); }
if (Math.abs(claro - 106) > 1)       { console.error('APCA claro dio ' + claro + ', se esperaba ~106'); process.exit(1); }
if (Math.abs(oscuro + 107.9) > 1)    { console.error('APCA oscuro dio ' + oscuro + ', se esperaba ~-107.9'); process.exit(1); }

" || muere "color.js $CJ_VER no da los valores de referencia (blanco sobre negro = 21:1 y Lc 106).
   Cambió su API. Revisa verificar-contraste.mjs antes de seguir."
ok "color.js verificado contra los valores de referencia"

# ---------------------------------------------------------------- 4. construir
azul "4/6  Construcción de tokens"
cp -f kino-brand.css kino-brand.css.antes 2>/dev/null || true
npm run tokens
ok "kino-brand.css generado"

if [ -f kino-brand.css.antes ]; then
  if diff -q <(grep -o -- '--kino-[a-z0-9-]*' kino-brand.css.antes | sort -u) \
             <(grep -o -- '--kino-[a-z0-9-]*' kino-brand.css      | sort -u) >/dev/null; then
    ok "mismos nombres de token que la versión anterior"
  else
    aviso "los nombres de token cambiaron respecto a kino-brand.css.antes"
    aviso "compara con: diff <(grep -o -- '--kino-[a-z0-9-]*' kino-brand.css.antes | sort -u) <(grep -o -- '--kino-[a-z0-9-]*' kino-brand.css | sort -u)"
  fi
fi

# ---------------------------------------------------------------- 5. contraste
azul "5/6  Verificación de contraste"
npm run verificar
ok "38 pares verificados en los dos temas"

# ---------------------------------------------------------------- 6. iconos
azul "6/6  Iconos"
# La ruta interna del paquete se descubre, no se adivina.
ORIGEN="$(find node_modules/iconoir -type f -name 'user.svg' -not -path '*/node_modules/*' 2>/dev/null | head -1 | xargs -I{} dirname {} || true)"
if [ -z "$ORIGEN" ]; then
  aviso "no encontré los SVG dentro de node_modules/iconoir. Búscalos con:"
  aviso "  find node_modules/iconoir -name '*.svg' | head"
else
  mkdir -p iconos
  COPIADOS=0
  for i in user car key clock qr-code shield-alert bell home-simple calendar warning-triangle; do
    if [ -f "$ORIGEN/$i.svg" ]; then cp "$ORIGEN/$i.svg" iconos/; COPIADOS=$((COPIADOS+1)); fi
  done
  ok "$COPIADOS iconos copiados a iconos/ desde $ORIGEN"
  [ "$COPIADOS" -lt 10 ] && aviso "algunos nombres no existen en esta versión; revisa $ORIGEN"
fi

# ---------------------------------------------------------------- registro
cat > versiones.txt <<EOF
Instalado el $(date '+%Y-%m-%d %H:%M')
node                $(node -v)
npm                 v$(npm -v)
style-dictionary    $SD_VER
colorjs.io          $CJ_VER
iconoir             $IC_VER
EOF

azul ""
azul "Listo."
cat versiones.txt
azul ""
echo "Siguientes pasos, cada uno por separado:"
echo "  bash instalar-fuentes.sh     autoaloja Archivo y JetBrains Mono"
echo "  bash instalar-figma-mcp.sh   registra los MCP de Figma (pide tu token)"
echo ""
echo "Si algo falló arriba, no sigas: la cadena de Node nunca se había ejecutado."
