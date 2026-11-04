#!/usr/bin/env bash
# Resume un PR para revisarlo rápido: separa lo que solo se movió de lo que cambió de verdad.
# Uso: bash herramientas/revisar-pr.sh [base] [rama]   (por defecto: origin/main y la rama actual)
#      bash herramientas/revisar-pr.sh origin/main origin/<rama-del-pr>   para revisar el PR de otro
# Lo que sale en "Para revisar" es lo único que hay que leer. Lo movido sin cambios ya está probado por git.
set -eu
BASE="${1:-origin/main}"; RAMA="${2:-HEAD}"
DIFF="$(git diff -M --name-status "$BASE"..."$RAMA")"
contar(){ printf '%s\n' "$DIFF" | grep -cE "$1" || true; }
echo "PR: $BASE...$RAMA · $(git rev-list --count "$BASE".."$RAMA") commits"
echo
echo "Movidos sin cambios (R100, no hace falta leerlos): $(contar '^R100')"
echo "Movidos con cambios:  $(contar '^R0[0-9][0-9]')"
echo "Nuevos:               $(contar '^A')"
echo "Modificados:          $(contar '^M')"
echo "Borrados:             $(contar '^D')"
echo
echo "Carpetas de destino de lo movido:"
printf '%s\n' "$DIFF" | awk -F'\t' '/^R100/{split($3,p,"/"); print "  " p[1] "/"}' | sort | uniq -c
echo
echo "Para revisar (con líneas agregadas y quitadas):"
printf '%s\n' "$DIFF" | grep -vE '^R100' | while IFS=$'\t' read -r estado a b; do
  [ -n "$estado" ] || continue
  f="${b:-$a}"
  n="$(git diff -M --numstat "$BASE"..."$RAMA" -- "$f" ${b:+"$a"} | awk '{s+=$1; r+=$2} END{printf "+%d -%d", s, r}')"
  printf '  %-5s %-11s %s%s\n' "$estado" "$n" "$f" "${b:+  (antes: $a)}"
done
echo
echo "Por commit:"
git log --reverse --format='  %h %s' "$BASE".."$RAMA"
