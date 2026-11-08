#!/usr/bin/env python3
"""Pasa a limpio en kino/canon/decisiones.md lo que Alejandro aprueba comentando un PR.

Uso:
  python3 herramientas/aplicar-decisiones.py N [carpeta]   aplica en la copia del PR N que está en carpeta (por defecto .)
  python3 herramientas/aplicar-decisiones.py N --ver       solo muestra qué cambiaría

Lee los comentarios del PR N (en líneas, en revisiones y en la conversación). Solo cuentan los de
APROBADORES. Frases que entiende, en cualquier parte del comentario:
  Apruebo D-005                 Apruebo D-005, opción A
  Descarto D-005: motivo
Por cada una, cambia el título «## D-005 · … · PROPUESTA …» por «… · APROBADA (Alejandro, 8 nov 2026) · opción A»
y agrega debajo el enlace al comentario. Si la decisión ya no está en PROPUESTA, no la toca.
No integra nada: integrar sigue siendo de Alejandro. Lo corre .github/workflows/aprobar-decisiones.yml.
"""
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

API = os.environ.get("GITHUB_API_URL", "https://api.github.com")
REPO = os.environ.get("GITHUB_REPOSITORY", "Amonsalvem/kino")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
APROBADORES = {"Amonsalvem": "Alejandro"}  # D-003: Alejandro aprueba todo
ARCHIVO = "kino/canon/decisiones.md"
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
COLOMBIA = timezone(timedelta(hours=-5))

FRASE = re.compile(
    r"\b(apruebo|descarto)\s+(D-\d{3})"
    r"(?:\s*,?\s*(?:con\s+la\s+)?opci[oó]n\s+([A-Za-z0-9]+))?"
    r"(?:\s*[:.\-]\s*([^\n]+))?",
    re.I,
)


def api(ruta):
    pedido = urllib.request.Request(f"{API}{ruta}")
    pedido.add_header("Accept", "application/vnd.github+json")
    pedido.add_header("User-Agent", "kino-aplicar-decisiones")
    if TOKEN:
        pedido.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(pedido) as r:
        return json.loads(r.read().decode())


def paginar(ruta):
    todo = []
    for pagina in range(1, 11):
        lote = api(f"{ruta}?per_page=100&page={pagina}")
        todo.extend(lote)
        if len(lote) < 100:
            break
    return todo


def comentarios(n):
    """Comentarios de aprobadores, del más viejo al más nuevo: (fecha, login, url, texto)."""
    salida = []
    for c in paginar(f"/repos/{REPO}/pulls/{n}/comments"):
        salida.append((c["created_at"], c["user"]["login"], c["html_url"], c["body"]))
    for c in paginar(f"/repos/{REPO}/issues/{n}/comments"):
        salida.append((c["created_at"], c["user"]["login"], c["html_url"], c["body"]))
    for r in paginar(f"/repos/{REPO}/pulls/{n}/reviews"):
        if r.get("body"):
            salida.append((r["submitted_at"], r["user"]["login"], r["html_url"], r["body"]))
    return sorted(c for c in salida if c[1] in APROBADORES and c[3])


def fecha_corta(iso):
    d = datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(COLOMBIA)
    return f"{d.day} {MESES[d.month - 1]} {d.year}"


def ordenes(n):
    """La última palabra de un aprobador sobre cada decisión manda."""
    resultado = {}
    for fecha, login, url, texto in comentarios(n):
        for m in FRASE.finditer(texto):
            verbo, ident, opcion, motivo = m.groups()
            resultado[ident.upper()] = {
                "aprobada": verbo.lower() == "apruebo",
                "opcion": opcion.upper() if opcion and len(opcion) == 1 else opcion,
                "motivo": (motivo or "").strip(),
                "quien": APROBADORES[login],
                "fecha": fecha_corta(fecha),
                "url": url,
            }
    return resultado


def aplicar(texto, ordenes_pr, n):
    cambios = []
    lineas = texto.splitlines(keepends=True)
    salida = []
    for linea in lineas:
        m = re.match(r"^(##\s+(D-\d{3})\s+·\s+.+?)\s+·\s+PROPUESTA\b.*$", linea.rstrip("\n"))
        orden = ordenes_pr.get(m.group(2)) if m else None
        if not orden:
            salida.append(linea)
            continue
        ident = m.group(2)
        if orden["aprobada"]:
            estado = f"APROBADA ({orden['quien']}, {orden['fecha']})"
            if orden["opcion"]:
                estado += f" · opción {orden['opcion']}"
        else:
            estado = f"DESCARTADA ({orden['quien']}, {orden['fecha']})"
        nota = f"**{'Aprobación' if orden['aprobada'] else 'Descarte'}.** [Comentario de {orden['quien']} en el PR #{n}]({orden['url']})"
        if orden["motivo"] and not orden["aprobada"]:
            nota += f": «{orden['motivo']}»"
        salida.append(f"{m.group(1)} · {estado}\n")
        salida.append("\n")
        salida.append(nota + ".\n" if not nota.endswith("»") else nota + "\n")
        cambios.append(f"{ident} → {estado}")
    return "".join(salida), cambios


def main(argv):
    if not argv or not argv[0].isdigit():
        print(__doc__)
        return 2
    n = int(argv[0])
    ver = "--ver" in argv
    carpeta = Path(next((a for a in argv[1:] if not a.startswith("--")), "."))
    ruta = carpeta / ARCHIVO
    if not ruta.exists():
        print(f"No hay {ARCHIVO} en la rama del PR #{n}: nada que aplicar")
        return 0
    ordenes_pr = ordenes(n)
    if not ordenes_pr:
        print(f"PR #{n}: no hay «Apruebo D-…» ni «Descarto D-…» de un aprobador")
        return 0
    nuevo, cambios = aplicar(ruta.read_text(encoding="utf-8"), ordenes_pr, n)
    if not cambios:
        print(f"PR #{n}: {', '.join(sorted(ordenes_pr))} ya no están en PROPUESTA o no están en este PR")
        return 0
    if ver:
        print("\n".join(cambios))
    else:
        ruta.write_text(nuevo, encoding="utf-8")
        print("Aplicado: " + "; ".join(cambios))
    salida_gh = os.environ.get("GITHUB_OUTPUT")
    if salida_gh:
        with open(salida_gh, "a", encoding="utf-8") as f:
            f.write(f"cambios={'; '.join(cambios)}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
