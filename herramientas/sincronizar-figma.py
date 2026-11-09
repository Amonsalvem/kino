#!/usr/bin/env python3
"""Copia al repositorio un registro de los archivos de Figma de Kino.

Lee los proyectos de Figma de FIGMA_PROJECT_IDS con la llave FIGMA_TOKEN (solo
lectura) y escribe en kino/figma/:
  README.md            índice: archivo, tipo, última edición, enlace
  <archivo>.md         páginas, marcos de primer nivel y estilos de cada archivo
  miniaturas/<archivo>.png

Solo reescribe un archivo cuando su fecha de edición en Figma cambió, para que
el PR diario muestre únicamente lo nuevo. Los nombres que vienen de Figma van
entre comillas invertidas: así el chequeo de texto no los toma como prosa.

Uso:
  FIGMA_TOKEN=... FIGMA_PROJECT_IDS=123,456 python3 herramientas/sincronizar-figma.py
  ... --ver   muestra qué cambiaría, sin escribir

Límite: la API de variables de Figma (tokens) solo existe en planes Enterprise.
"""
import json
import os
import re
import sys
import unicodedata
import urllib.request
from pathlib import Path

API = "https://api.figma.com/v1"
SALIDA = Path("kino/figma")
TIPOS = {"figma": "Diseño", "slides": "Slides", "figjam": "FigJam"}
ENLACE = {"figma": "design", "slides": "slides", "figjam": "board"}


def pedir(ruta, token):
    req = urllib.request.Request(f"{API}{ruta}", headers={"X-Figma-Token": token})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def bajar(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return r.read()


def slug(texto):
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-") or "sin-nombre"


def codigo(texto):
    return "`" + str(texto).replace("`", "'").replace("|", "/") + "`"


def leer_estado():
    """Fecha de edición registrada por clave de archivo, sacada del índice."""
    indice = SALIDA / "README.md"
    if not indice.exists():
        return {}
    m = re.search(r"<!-- estado: (.*?) -->", indice.read_text(encoding="utf-8"))
    return json.loads(m.group(1)) if m else {}


def ficha(meta, doc):
    tipo = meta.get("editorType", "figma")
    url = f"https://www.figma.com/{ENLACE.get(tipo, 'design')}/{meta['key']}"
    lineas = [
        f"# {codigo(meta['name'])}",
        "",
        "Registro generado por `herramientas/sincronizar-figma.py`. La fuente es Figma: no se edita aquí.",
        "",
        "| Campo | Valor |",
        "|---|---|",
        f"| Enlace | {url} |",
        f"| Tipo | {TIPOS.get(tipo, tipo)} |",
        f"| Proyecto | {codigo(meta['proyecto'])} |",
        f"| Última edición en Figma | {meta['last_modified']} |",
        f"| Versión | {doc.get('version', '')} |",
        "",
        f"![Miniatura](miniaturas/{meta['slug']}.png)",
        "",
        "## Páginas y marcos de primer nivel",
        "",
    ]
    for pagina in doc.get("document", {}).get("children", []):
        lineas.append(f"- {codigo(pagina['name'])}")
        for hijo in pagina.get("children", []):
            lineas.append(f"  - {codigo(hijo['name'])} ({hijo.get('type', '').lower()})")
    estilos = doc.get("styles", {})
    lineas += ["", "## Estilos", ""]
    if estilos:
        lineas += ["| Nombre | Tipo |", "|---|---|"]
        for e in sorted(estilos.values(), key=lambda e: (e.get("styleType", ""), e.get("name", ""))):
            lineas.append(f"| {codigo(e.get('name', ''))} | {e.get('styleType', '').lower()} |")
    else:
        lineas.append("Sin estilos publicados.")
    return "\n".join(lineas) + "\n"


def indice(archivos, estado):
    lineas = [
        "# Figma",
        "",
        "Registro diario de los archivos de Figma de Kino. Lo escribe la Action «Sincronizar Figma»; no se edita a mano.",
        "La fuente es Figma (D-003). Este registro sirve para que los agentes del repositorio sepan qué existe y qué cambió.",
        "",
        "| Archivo | Tipo | Proyecto | Última edición | Ficha |",
        "|---|---|---|---|---|",
    ]
    for a in sorted(archivos, key=lambda a: a["last_modified"], reverse=True):
        tipo = a.get("editorType", "figma")
        url = f"https://www.figma.com/{ENLACE.get(tipo, 'design')}/{a['key']}"
        lineas.append(
            f"| [{codigo(a['name'])}]({url}) | {TIPOS.get(tipo, tipo)} | {codigo(a['proyecto'])} "
            f"| {a['last_modified'][:16].replace('T', ' ')} UTC | [{a['slug']}.md]({a['slug']}.md) |"
        )
    lineas += ["", f"<!-- estado: {json.dumps(estado, sort_keys=True)} -->"]
    return "\n".join(lineas) + "\n"


def main(argv):
    token = os.environ.get("FIGMA_TOKEN")
    proyectos = [p.strip() for p in os.environ.get("FIGMA_PROJECT_IDS", "").split(",") if p.strip()]
    if not token or not proyectos:
        print("Falta FIGMA_TOKEN o FIGMA_PROJECT_IDS. No se hace nada.")
        return 0
    ver = "--ver" in argv
    previo = leer_estado()
    archivos, usados = [], set()
    for pid in proyectos:
        datos = pedir(f"/projects/{pid}/files", token)
        for f in datos.get("files", []):
            f["proyecto"] = datos.get("name", pid)
            base = previo.get(f["key"], {}).get("s") or slug(f["name"])
            nombre, n = base, 2
            while nombre in usados:
                nombre, n = f"{base}-{n}", n + 1
            usados.add(nombre)
            f["slug"] = nombre
            archivos.append(f)

    for a in archivos:
        if a["key"] in previo:
            a.setdefault("editorType", previo[a["key"]].get("t", "figma"))
    cambiados = [a for a in archivos if previo.get(a["key"], {}).get("m") != a["last_modified"]]
    retirados = sorted(set(previo) - {a["key"] for a in archivos})
    for a in cambiados:
        print(f"{'nuevo' if a['key'] not in previo else 'cambió'}: {a['name']} ({a['last_modified']})")
    for k in retirados:
        print(f"ya no está en los proyectos: {previo[k].get('s', k)}")
    if ver or (not cambiados and not retirados):
        if not cambiados and not retirados:
            print("Sin cambios en Figma.")
        return 0

    (SALIDA / "miniaturas").mkdir(parents=True, exist_ok=True)
    for a in cambiados:
        doc = pedir(f"/files/{a['key']}?depth=2", token)
        a["editorType"] = doc.get("editorType", a.get("editorType", "figma"))
        (SALIDA / f"{a['slug']}.md").write_text(ficha(a, doc), encoding="utf-8")
        if a.get("thumbnail_url"):
            try:
                (SALIDA / "miniaturas" / f"{a['slug']}.png").write_bytes(bajar(a["thumbnail_url"]))
            except Exception as e:  # una miniatura que falla no detiene el registro
                print(f"miniatura sin bajar: {a['name']}: {e}")
    for k in retirados:
        for ruta in (SALIDA / f"{previo[k].get('s')}.md", SALIDA / "miniaturas" / f"{previo[k].get('s')}.png"):
            if previo[k].get("s") and ruta.exists():
                ruta.unlink()
    estado = {a["key"]: {"m": a["last_modified"], "t": a.get("editorType", "figma"), "s": a["slug"]} for a in archivos}
    (SALIDA / "README.md").write_text(indice(archivos, estado), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
