#!/usr/bin/env python3
"""Hook UserPromptSubmit de Claude Code: guarda cada prompt en registro-ia/.

Solo registra si se sabe quién escribe y esa persona dio consentimiento:
  - Quién: variable KINO_PERSONA o `git config kino.persona` (por ejemplo, alejandro).
  - Consentimiento: su nombre aparece con «sí» en registro-ia/consentimiento.md.
Antes de guardar, tapa teléfonos, correos, cédulas, placas y llaves.
Nunca bloquea el prompt: ante cualquier fallo, sale en silencio.
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

RAIZ = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parent.parent)
BOGOTA = timezone(timedelta(hours=-5))

TAPAR = [
    (r"\b(sk-|ghp_|gho_|xox[bp]-|AKIA)[A-Za-z0-9_\-]{8,}", "[llave]"),
    (r"[\w.+-]+@[\w-]+\.[\w.]+", "[correo]"),
    (r"(\+?57\s?)?\b3\d{2}[\s-]?\d{3}[\s-]?\d{4}\b", "[teléfono]"),
    (r"\b[A-Z]{3}[\s-]?\d{2,3}[A-Z]?\b", "[placa]"),
    (r"\b\d{1,3}(\.\d{3}){2,3}\b|\b\d{7,10}\b", "[número]"),
]


def persona():
    nombre = os.environ.get("KINO_PERSONA", "").strip().lower()
    if not nombre:
        r = subprocess.run(["git", "-C", str(RAIZ), "config", "kino.persona"], capture_output=True, text=True)
        nombre = r.stdout.strip().lower()
    return nombre


def consintio(nombre):
    archivo = RAIZ / "registro-ia" / "consentimiento.md"
    if not nombre or not archivo.exists():
        return False
    patron = re.compile(rf"^\|\s*{re.escape(nombre)}\s*\|\s*sí\s*\|", re.I | re.M)
    return bool(patron.search(archivo.read_text(encoding="utf-8")))


def tapar(texto):
    for patron, reemplazo in TAPAR:
        texto = re.sub(patron, reemplazo, texto)
    return texto


def main():
    try:
        evento = json.load(sys.stdin)
        nombre = persona()
        if not consintio(nombre):
            return
        ahora = datetime.now(BOGOTA)
        sesion = re.sub(r"[^\w-]", "", str(evento.get("session_id", "sin-sesion")))[:40]
        carpeta = RAIZ / "registro-ia" / ahora.strftime("%Y-%m")
        carpeta.mkdir(parents=True, exist_ok=True)
        linea = {
            "hora": ahora.isoformat(timespec="seconds"),
            "persona": nombre,
            "herramienta": "claude-code",
            "sesion": sesion,
            "prompt": tapar(str(evento.get("prompt", ""))),
        }
        with open(carpeta / f"{ahora:%Y-%m-%d}-{sesion}.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(linea, ensure_ascii=False) + "\n")
    except Exception:
        pass


if __name__ == "__main__":
    main()
    sys.exit(0)
