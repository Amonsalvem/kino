#!/usr/bin/env bash
# Kino — registra los MCP de Figma en Claude Code.
# El token no se guarda en ningún archivo de este repositorio.
set -euo pipefail

azul() { printf '\033[1;36m%s\033[0m\n' "$*"; }
ok()   { printf '  \033[0;32m✓\033[0m %s\n' "$*"; }
muere(){ printf '\n\033[0;31m✗ %s\033[0m\n' "$*" >&2; exit 1; }

command -v claude >/dev/null 2>&1 || muere "No encuentro el comando 'claude'. Instala Claude Code primero."

azul "Antes de seguir"
cat <<'TXT'
  En este proyecto ya aparece conectado el MCP oficial de Figma, que cubre
  lectura: get_design_context, get_variable_defs, get_screenshot.
  Los dos de abajo añaden:
    figma-console        extracción más rica y handoff a código
    claude-talk-to-figma escritura sobre el canvas, con cuentas gratuitas
  Si no vas a generar pantallas desde Figma, no instales ninguno.
TXT
printf '\n¿Seguir? [s/N] '
read -r SEGUIR
case "$SEGUIR" in s|S|si|Si|SI) ;; *) echo "Cancelado."; exit 0;; esac

# ------------------------------------------------------------- figma-console
azul ""
azul "figma-console-mcp"
cat <<'TXT'
  Necesita un token personal de Figma.
  Settings -> Security -> Personal access tokens, con lectura en:
  file content, file versions, variables y comments.
  Empieza por figd_ y no se escribe en pantalla.
TXT
printf '\nToken de Figma: '
read -rs FIGMA_TOKEN
echo
[ -n "$FIGMA_TOKEN" ] || muere "token vacío"
case "$FIGMA_TOKEN" in figd_*) ;; *) muere "un token de Figma empieza por figd_";; esac

claude mcp add figma-console -s user \
  -e "FIGMA_ACCESS_TOKEN=$FIGMA_TOKEN" \
  -e ENABLE_MCP_APPS=true \
  -- npx -y figma-console-mcp@latest
unset FIGMA_TOKEN
ok "figma-console registrado"

# -------------------------------------------------------- claude-talk-to-figma
azul ""
printf '¿Instalar también claude-talk-to-figma (escritura sobre el canvas)? [s/N] '
read -r ESCRITURA
case "$ESCRITURA" in
  s|S|si|Si|SI)
    claude mcp add ClaudeTalkToFigma -s user \
      -- npx -p claude-talk-to-figma-mcp@latest claude-talk-to-figma-mcp-server
    ok "ClaudeTalkToFigma registrado"
    cat <<'TXT'

  Faltan dos pasos manuales:
    1. Arranca el servidor WebSocket en otra pestaña:
         npx claude-talk-to-figma-mcp
    2. En Figma Desktop: Plugins -> Development -> Import plugin from manifest
       y elige src/claude_mcp_plugin/manifest.json de la carpeta que creó el paso 1.
  Con el plugin abierto, copia el identificador de canal y dile al agente:
       Connect to Figma, channel {id}
TXT
    ;;
  *) echo "  Omitido." ;;
esac

azul ""
echo "Comprueba el registro con:  claude mcp list"
echo "Reinicia Claude Code para que los tome."
