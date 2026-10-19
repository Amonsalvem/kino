#!/usr/bin/env bash
# Uso: bash codificar.sh residente|administracion
# Cuadros RGBA de render/personaje-<id>/ → entrega-3/personajes/<id>.webm (VP9 con alfa, 15 fps) y <id>.png (último cuadro).
set -euo pipefail
id=$1; dir=render/personaje-$id; dest=../../../../../entrega-3/personajes
ffmpeg -y -loglevel error -framerate 15 -pattern_type glob -i "$dir/*.png" \
  -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 32 -auto-alt-ref 0 "$dest/$id.webm"
cp "$(ls $dir/*.png | tail -1)" "$dest/$id.png"
