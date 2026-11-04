#!/usr/bin/env bash
# Prepara una sesión de Claude Code (nube o local) para trabajar Kino.
# Lo corre el hook SessionStart de .claude/settings.json. Su salida entra al contexto de la sesión.
set -u
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
ok(){ echo "  [ok] $1"; }
falta(){ echo "  [FALTA] $1"; }
echo "Entorno Kino · $(date -u +%Y-%m-%dT%H:%MZ)"

command -v node >/dev/null && ok "node $(node -v)" || falta "node (se necesita 20+)"
command -v python3 >/dev/null && ok "$(python3 --version)" || falta "python3"

# Dependencias de gorr-brand-system (colorjs.io, apca-w3, utopia-core, promptfoo...)
if [ -d "$RAIZ/gorr-brand-system/node_modules/colorjs.io" ]; then
  ok "gorr-brand-system/node_modules ya instalado"
else
  ( cd "$RAIZ/gorr-brand-system" && timeout 240 npm install --no-audit --no-fund --loglevel=error >/tmp/kino-npm.log 2>&1 ) \
    && ok "npm install en gorr-brand-system" \
    || falta "npm install en gorr-brand-system (ver /tmp/kino-npm.log). Plan B: branding/sistema/v3/fase3/apca.py"
fi

# Navegador para las pruebas visuales (scripts/capturar.mjs)
CHROME="$(ls -d /opt/pw-browsers/chromium-*/chrome-linux/chrome 2>/dev/null | head -1)"
if [ -n "$CHROME" ]; then ok "Chromium: $CHROME"; else
  command -v chromium >/dev/null && ok "Chromium: $(command -v chromium)" || falta "Chromium (probar: npx playwright install chromium)"
fi
node -e "require.resolve('playwright')" >/dev/null 2>&1 || NODE_PATH="$(npm root -g)" node -e "require.resolve('playwright')" >/dev/null 2>&1 \
  && ok "paquete playwright" || falta "paquete playwright (npm i -g playwright con PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1)"

# Construcción rápida del sitio para confirmar que la cadena funciona
( cd "$RAIZ/branding/sistema/v3/sitio" && python3 construir.py >/tmp/kino-sitio.log 2>&1 ) \
  && ok "sitio construido (branding/sistema/v3/sitio/build/)" || falta "construir.py (ver /tmp/kino-sitio.log)"

echo "Pendiente de comprobar por Claude, no por este script:"
echo "  - herramienta Artifact (publicar láminas)"
echo "  - conector de Figma: whoami y get_metadata del archivo BO7UnDO9iE0aG6yUpNj0bc"
echo "  - skill figma-use cargada antes de use_figma"
exit 0
