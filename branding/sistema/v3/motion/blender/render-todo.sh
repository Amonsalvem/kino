#!/usr/bin/env bash
# Render de todas las escenas, una tras otra (4 núcleos: en paralelo no se gana). Registro en render.log.
cd "$(dirname "$0")"
for par in "pase-3d-objeto" "pase-3d-latir" "conjunto-noche-lector-confirma" "pase-3d-objeto --reducido" "conjunto-noche-lector-confirma --reducido" "pase-3d-latir --reducido"; do
  echo "== $par · $(date +%H:%M)" >> render.log
  .venv/bin/python construir.py $par render 2>&1 | grep -E "✓|Traceback|Error" >> render.log
done
echo "== fin · $(date +%H:%M)" >> render.log
