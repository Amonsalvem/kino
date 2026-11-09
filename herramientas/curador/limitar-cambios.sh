#!/usr/bin/env bash
# Revierte lo que el curador cambió fuera de sus rutas permitidas (herramientas/curador/prompt.md §1).
# La Action lo copia antes de que corra el curador, así el curador no puede cambiar este guardián.
# Uso: bash limitar-cambios.sh <archivo-de-avisos>   (desde la raíz del repositorio)
set -euo pipefail

avisos="${1:-/dev/stdout}"
permitido='^(\.claude/skills/|\.claude/agents/|\.claude/settings\.json$|AGENTS\.md$|CLAUDE\.md$|herramientas/prompt-grok\.md$|herramientas/curador/(prompt\.md|estado\.md|informes/)|kino/canon/decisiones\.md$)'
revertidos=()

# Archivos versionados que cambiaron o se borraron.
while IFS= read -r f; do
  [ -z "$f" ] && continue
  if ! [[ "$f" =~ $permitido ]]; then
    git checkout HEAD -- "$f"
    revertidos+=("$f")
  fi
done < <(git diff --name-only HEAD)

# Archivos nuevos.
while IFS= read -r f; do
  [ -z "$f" ] && continue
  if ! [[ "$f" =~ $permitido ]]; then
    rm -f -- "$f"
    revertidos+=("$f (nuevo)")
  fi
done < <(git ls-files --others --exclude-standard)

# decisiones.md: solo se agregan entradas PROPUESTA. Nada se borra ni se aprueba.
d=kino/canon/decisiones.md
if ! git diff --quiet HEAD -- "$d"; then
  cambio=$(git diff --unified=0 HEAD -- "$d" | tail -n +5)
  if echo "$cambio" | grep -qE '^-[^-]' || echo "$cambio" | grep -qE '^\+.*(APROBADA|DESCARTADA|REEMPLAZADA)'; then
    git checkout HEAD -- "$d"
    revertidos+=("$d (borraba o aprobaba una entrada)")
  fi
fi

if [ ${#revertidos[@]} -gt 0 ]; then
  {
    echo
    echo "### Cambios revertidos por el guardián"
    echo
    echo "El curador intentó tocar rutas fuera de su permiso. Se revirtieron:"
    echo
    for r in "${revertidos[@]}"; do echo "- \`$r\`"; done
  } >> "$avisos"
  echo "::warning::El guardián revirtió ${#revertidos[@]} cambio(s) fuera de las rutas del curador"
fi
