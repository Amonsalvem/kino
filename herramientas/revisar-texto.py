#!/usr/bin/env python3
"""Chequeo de muletillas y relleno para el texto de Kino.

Uso:
  python3 herramientas/revisar-texto.py [archivos...]      revisa esos archivos
  python3 herramientas/revisar-texto.py --todo              revisa todo lo versionado fuera de pre-kino/
  python3 herramientas/revisar-texto.py --texto archivo.txt revisa un texto suelto (cuerpo de un PR)

ERROR bloquea el PR. AVISO se muestra y no bloquea.
Los patrones salen de medir los documentos del repositorio el 4 nov 2026.
No se revisan: bloques de código, código en línea, citas (líneas con >) ni
líneas con el marcador <!-- muletillas: ok -->.
"""
import re
import subprocess
import sys
from pathlib import Path

EXCLUIDOS = (
    "pre-kino/",
    ".claude/skills/corrector-muletillas/",
    "herramientas/revisar-texto.py",
    "registro-ia/",
)
EXTENSIONES = {".md", ".mdx", ".txt"}

# Alta precisión: casi nunca aparecen en texto bien escrito de este repositorio.
ERRORES = [
    (r"—", "raya (—) como conector; usa coma, dos puntos, paréntesis o punto"),
    (r"\b(tienes|tiene) (toda la )?raz[oó]n\b", "validación al lector"),
    (r"\b(excelente|gran|buena) pregunta\b", "validación al lector"),
    (r"\bcon (mucho )?gusto te ayudo\b", "relleno de cortesía"),
    (r"\bno dudes en\b", "relleno de cortesía"),
    (r"\bespero que (esto|te) (te )?(sirva|ayude)\b", "cierre de relleno"),
    (r"\b(cabe|vale la pena) (destacar|señalar|mencionar|resaltar)\b", "anuncio vacío: di el dato"),
    (r"\bes importante (destacar|señalar|mencionar|resaltar|tener en cuenta)\b", "anuncio vacío: di el dato"),
    (r"^\s*(en resumen|en conclusión|en definitiva)\b", "cierre que repite lo dicho"),
    (r"\b(tapiz|piedra angular|sin fisuras|sinergias?)\b", "palabra de IA sin contenido"),
]

# Útiles a veces; se señalan para que la persona decida.
AVISOS = [
    (r"\bno es [^.,;:\n]{1,40}, (sino|es) ", "antítesis «no es X, es Y»: úsala solo si aporta"),
    (r"\bno solo\b[^.\n]{0,80}\bsino\b", "«no solo… sino»: di las dos cosas directo"),
    (r"\b(robust[oa]s?|crucial(es)?|fundamental(es)?|profundizar|potenciar|aprovechar)\b",
     "palabra sobreusada por IA: ¿hay una más precisa?"),
]

CIFRA = re.compile(r"(\d[\d.,]*\s?(%|por ciento|millones|mil millones|COP|USD|US\$))", re.I)
FUENTE = re.compile(r"(https?://|\]\(|`[^`]+`|fuente|según|pre-kino/|kino/)", re.I)
MAX_PALABRAS_PARRAFO = 120
MAX_PALABRAS_DOCUMENTO = 1800


def limpiar(lineas):
    """Devuelve (número, línea) revisables, sin código ni citas."""
    en_codigo = False
    for n, linea in enumerate(lineas, 1):
        if linea.lstrip().startswith("```"):
            en_codigo = not en_codigo
            continue
        if en_codigo or linea.lstrip().startswith(">") or "muletillas: ok" in linea:
            continue
        yield n, re.sub(r"`[^`]*`", "", linea)


def revisar(nombre, texto):
    hallazgos = []
    lineas = texto.splitlines()
    palabras_total = 0
    parrafo, inicio = 0, 1
    for n, linea in limpiar(lineas):
        for patron, motivo in ERRORES:
            if re.search(patron, linea, re.I):
                hallazgos.append(("ERROR", n, motivo, linea.strip()))
        for patron, motivo in AVISOS:
            if re.search(patron, linea, re.I):
                hallazgos.append(("AVISO", n, motivo, linea.strip()))
        if CIFRA.search(linea) and not FUENTE.search(linea):
            hallazgos.append(("AVISO", n, "cifra sin fuente en la misma línea", linea.strip()))
        palabras = len(linea.split())
        palabras_total += palabras
        if linea.strip() and not linea.lstrip().startswith(("|", "-", "*", "#")) and not re.match(r"\s*\d+\.", linea):
            if parrafo == 0:
                inicio = n
            parrafo += palabras
            if parrafo > MAX_PALABRAS_PARRAFO:
                hallazgos.append(("AVISO", inicio, f"párrafo de más de {MAX_PALABRAS_PARRAFO} palabras: pártelo o usa una tabla", ""))
                parrafo = -10**6
        else:
            parrafo = 0
    if palabras_total > MAX_PALABRAS_DOCUMENTO:
        hallazgos.append(("AVISO", 1, f"{palabras_total} palabras: ¿sobra información o se repite algo de otro archivo?", ""))
    return hallazgos


def archivos_versionados():
    salida = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True).stdout
    return salida.splitlines()


def revisable(ruta):
    return Path(ruta).suffix in EXTENSIONES and not ruta.startswith(EXCLUIDOS) and Path(ruta).exists()


def main(argv):
    if argv[:1] == ["--texto"]:
        objetivos = [(argv[1], Path(argv[1]).read_text(encoding="utf-8"))]
    else:
        rutas = archivos_versionados() if argv[:1] == ["--todo"] else argv
        objetivos = [(r, Path(r).read_text(encoding="utf-8")) for r in rutas if revisable(r)]
    errores = avisos = 0
    en_actions = bool(__import__("os").environ.get("GITHUB_ACTIONS"))
    for nombre, texto in objetivos:
        for tipo, n, motivo, linea in revisar(nombre, texto):
            if tipo == "ERROR":
                errores += 1
            else:
                avisos += 1
            if en_actions:
                nivel = "error" if tipo == "ERROR" else "warning"
                print(f"::{nivel} file={nombre},line={n}::{motivo}")
            print(f"{tipo} {nombre}:{n} · {motivo}" + (f"\n      {linea[:140]}" if linea else ""))
    print(f"\n{len(objetivos)} archivo(s) · {errores} error(es) · {avisos} aviso(s)")
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
