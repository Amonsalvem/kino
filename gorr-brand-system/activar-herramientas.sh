#!/usr/bin/env bash
# Activa las herramientas del informe que la sesión de Claude no puede descargar (su red bloquea npm y GitHub).
# Correr UNA vez desde la Terminal del Mac, que sí tiene red:
#   cd ".../kino/gorr-brand-system" && bash activar-herramientas.sh
# Después, Claude las usa sin red desde la carpeta.
set -euo pipefail
cd "$(dirname "$0")"

nosync () {  # iCloud «Optimizar almacenamiento» expulsa node_modules y rompe los builds en silencio.
  local dir="$1"
  if [ -d "$dir/node_modules" ] && [ ! -L "$dir/node_modules" ]; then
    mv "$dir/node_modules" "$dir/node_modules.nosync"
  fi
  mkdir -p "$dir/node_modules.nosync"
  [ -L "$dir/node_modules" ] || ln -s node_modules.nosync "$dir/node_modules"
  echo "  $dir/node_modules → node_modules.nosync (fuera de iCloud)"
}

echo "1/4 · node_modules fuera de iCloud"
nosync .
nosync ../branding/sistema

echo "2/4 · paquetes npm del informe"
npm install --save-dev \
  @terrazzo/cli @terrazzo/plugin-css \
  @adobe/leonardo-contrast-colors \
  apca-w3 colorparsley \
  utopia-core \
  promptfoo
npm install --save colorjs.io iconoir
(cd ../branding/sistema && npm install)

echo "3/4 · repositorios de referencia"
mkdir -p vendor
[ -d vendor/w3c-design-tokens-agent-skill ] || git clone --depth 1 https://github.com/dgtlntv/w3c-design-tokens-agent-skill vendor/w3c-design-tokens-agent-skill
[ -d vendor/anthropic-skills ] || git clone --depth 1 --filter=blob:none --sparse https://github.com/anthropics/skills vendor/anthropic-skills \
  && (cd vendor/anthropic-skills && git sparse-checkout set skills/brand-guidelines skills/skill-creator 2>/dev/null || true)

echo "4/4 · versiones"
{
  date -u +"activado %Y-%m-%dT%H:%M:%SZ"
  node -v
  for p in @terrazzo/cli @terrazzo/plugin-css @adobe/leonardo-contrast-colors apca-w3 utopia-core promptfoo colorjs.io iconoir; do
    printf '%s %s\n' "$p" "$(node -p "require('./node_modules/$p/package.json').version" 2>/dev/null || echo 'NO INSTALADO')"
  done
  ls vendor
} | tee versiones-herramientas.txt

if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
  echo
  echo "Falta ANTHROPIC_API_KEY para correr promptfoo (evals de voz). Opcional: sin ella, las evals se siguen corriendo con subagentes."
fi
echo "Listo. Avísale a Claude."
