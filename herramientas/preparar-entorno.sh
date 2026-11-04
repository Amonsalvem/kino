#!/usr/bin/env bash
# Prepara una sesión (nube o local) para trabajar en Kino.
# Lo corre el hook SessionStart de .claude/settings.json; su salida entra al contexto de la sesión.
# Solo comprueba: no instala ni construye nada de pre-kino.
set -u
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
ok(){ echo "  [ok] $1"; }
falta(){ echo "  [FALTA] $1"; }
echo "Entorno Kino · $(date -u +%Y-%m-%dT%H:%MZ)"

command -v node >/dev/null && ok "node $(node -v)" || falta "node (20 o más)"
command -v python3 >/dev/null && ok "$(python3 --version)" || falta "python3"
command -v git >/dev/null && ok "git, rama $(git -C "$RAIZ" branch --show-current 2>/dev/null)" || falta "git"

CHROME="$(ls -d /opt/pw-browsers/chromium /opt/pw-browsers/chromium-*/chrome-linux*/chrome 2>/dev/null | head -1)"
if [ -n "$CHROME" ]; then ok "Chromium para herramientas/capturar.mjs"; else
  command -v chromium >/dev/null && ok "Chromium: $(command -v chromium)" || falta "Chromium (herramientas/capturar.mjs no va a correr)"
fi

if command -v gh >/dev/null && gh pr list --draft --limit 10 >/dev/null 2>&1; then
  echo "PR en borrador abiertos:"; gh pr list --draft --limit 10 | sed 's/^/  /'
else echo "  [FALTA] gh: revisa a mano los PR en borrador en GitHub"; fi

echo "Recuerda: lee AGENTS.md y kino/canon/ antes de trabajar. pre-kino/ es de solo lectura."
exit 0
