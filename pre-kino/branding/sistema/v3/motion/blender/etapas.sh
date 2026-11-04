#!/usr/bin/env bash
# Corre varias etapas seguidas de un recurso: ./etapas.sh <id> [--reducido] etapa1 etapa2 ...
set -e
cd "$(dirname "$0")"
id=$1; shift
red=""; [ "$1" = "--reducido" ] && { red="--reducido"; shift; }
for e in "$@"; do .venv/bin/python construir.py "$id" "$e" $red "${EXTRA[@]}" 2>&1 | grep -v '^EGL' | grep -E '✓|Error|error|Traceback|File "|^\s' | grep -v '^\s*$' | tail -12; done
