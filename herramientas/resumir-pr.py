#!/usr/bin/env python3
"""Resumen de PR para aprobar rápido.

Uso:
  python3 herramientas/resumir-pr.py --comentar N    comenta o actualiza el resumen en el PR N
  python3 herramientas/resumir-pr.py --panel         actualiza el issue «Panel de PR» con los PR abiertos
  python3 herramientas/resumir-pr.py --ver N         imprime el resumen del PR N sin publicar nada
  python3 herramientas/resumir-pr.py --ver-panel     imprime el panel sin publicar nada

Lo corre .github/workflows/resumen-pr.yml. Necesita GITHUB_TOKEN y GITHUB_REPOSITORY
(dueño/repo). No usa IA ni dependencias: lee la plantilla del PR, la lista de archivos
y los chequeos, y aplica las reglas de AGENTS.md y kino/canon/.
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

API = os.environ.get("GITHUB_API_URL", "https://api.github.com")
REPO = os.environ.get("GITHUB_REPOSITORY", "Amonsalvem/kino")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
MARCA_COMENTARIO = "<!-- resumen-pr -->"
ETIQUETA_PANEL = "panel-pr"
TITULO_PANEL = "Panel de PR"
MAX_PANEL = 60000  # el cuerpo de un issue admite 65 536 caracteres

# Qué toca cada ruta y por qué importa al aprobar. El orden manda: gana la primera que calce.
ZONAS = [
    ("pre-kino/", "pre-kino", "bloquea", "Toca `pre-kino/`, que es de solo lectura (AGENTS.md §5.3)"),
    ("kino/canon/decisiones.md", "canon", "decide", "Cambia `decisiones.md`: confirma cada PROPUESTA o APROBADA"),
    ("kino/canon/", "canon", "decide", "Cambia el canon, que manda sobre el resto (AGENTS.md §3)"),
    ("AGENTS.md", "orden", "decide", "Cambia las reglas de todas las IA"),
    ("CLAUDE.md", "orden", "decide", "Cambia las reglas de Claude"),
    (".github/", "orden", "decide", "Cambia la automatización de GitHub (chequeos, plantilla)"),
    (".claude/", "orden", "decide", "Cambia hooks o skills de Claude"),
    ("herramientas/", "orden", "revisa", "Cambia scripts compartidos"),
    ("personas/", "orden", "decide", "Cambia el perfil de una persona"),
    ("kino/marca/", "marca", "decide", "Marca: nada se aprueba sin tu respuesta explícita (CLAUDE.md, Paradas)"),
    ("kino/producto/", "producto", "decide", "Producto: flujos o reglas de negocio"),
    ("kino/codigo/", "codigo", "revisa", "Código de la app"),
    ("kino/investigacion/", "investigacion", "revisa", "Evidencia nueva: revisa que cada dato tenga fuente"),
    ("eafit/", "eafit", "revisa", "Entrega académica: no es decisión de producto"),
    ("registro-ia/", "orden", "leve", ""),
]
PESO = {"bloquea": 0, "decide": 1, "revisa": 2, "leve": 3}
ETIQUETA_NIVEL = {
    "bloquea": "🔴 Corregir antes",
    "decide": "🟠 Decisión tuya",
    "revisa": "🟡 Lectura normal",
    "leve": "🟢 Rápido",
}

# Palabras que el vocabulario de Kino prohíbe (AGENTS.md §5.8). Solo en líneas agregadas.
VOCABULARIO = [
    (re.compile(r"\bpermisos?\b", re.I), "«permiso» (nunca se usa: es Pase o cuenta)"),
    (re.compile(r"\binvitad[oa]s?\b", re.I), "«invitado» (en la interfaz es «visita»)"),
]
# Posibles datos sensibles (AGENTS.md §5.10). Es un aviso, no una prueba.
SENSIBLES = [
    (re.compile(r"\b3\d{2}[ -]?\d{3}[ -]?\d{4}\b"), "posible teléfono celular"),
    (re.compile(r"\b(c\.?c\.?|c[eé]dula)\s*:?\s*\d{6,10}\b", re.I), "posible cédula"),
    (re.compile(r"\b[A-Z]{3}[ -]?\d{3}\b"), "posible placa"),
    (re.compile(r"(api[_-]?key|secret|password|contrase[nñ]a|token)\s*[:=]\s*\S{8,}", re.I), "posible secreto"),
    (re.compile(r"\b(sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16})\b"), "posible llave"),
]
BINARIOS = re.compile(r"\.(png|jpe?g|gif|webp|pdf|mp4|mov|zip|psd|fig|blend|ai|key|pptx?|docx?)$", re.I)
ESTADOS = {"added": "nuevo", "modified": "cambiado", "removed": "borrado", "renamed": "movido y cambiado"}
PR_GRANDE_ARCHIVOS = 40
PR_GRANDE_LINEAS = 1500


# ---------- GitHub ----------

def api(metodo, ruta, datos=None):
    url = ruta if ruta.startswith("http") else f"{API}{ruta}"
    cuerpo = json.dumps(datos).encode() if datos is not None else None
    pedido = urllib.request.Request(url, data=cuerpo, method=metodo)
    pedido.add_header("Accept", "application/vnd.github+json")
    pedido.add_header("X-GitHub-Api-Version", "2022-11-28")
    pedido.add_header("User-Agent", "kino-resumen-pr")
    if TOKEN:
        pedido.add_header("Authorization", f"Bearer {TOKEN}")
    if cuerpo:
        pedido.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(pedido) as r:
        texto = r.read().decode()
        return json.loads(texto) if texto else None


def paginar(ruta, limite=10):
    sep = "&" if "?" in ruta else "?"
    todo = []
    for pagina in range(1, limite + 1):
        lote = api("GET", f"{ruta}{sep}per_page=100&page={pagina}")
        if isinstance(lote, dict):  # check-runs viene envuelto
            lote = lote.get("check_runs", [])
        todo.extend(lote)
        if len(lote) < 100:
            break
    return todo


def datos_pr(n):
    pr = api("GET", f"/repos/{REPO}/pulls/{n}")
    archivos = paginar(f"/repos/{REPO}/pulls/{n}/files", limite=30)
    commits = paginar(f"/repos/{REPO}/pulls/{n}/commits", limite=3)
    try:
        chequeos = paginar(f"/repos/{REPO}/commits/{pr['head']['sha']}/check-runs", limite=1)
    except urllib.error.HTTPError:
        chequeos = []
    return pr, archivos, commits, chequeos


# ---------- Análisis ----------

def seccion(cuerpo, titulo):
    """Texto de una sección «## titulo» de la plantilla, sin comentarios HTML."""
    m = re.search(rf"^##\s+{re.escape(titulo)}\s*\n(.*?)(?=^##\s|\Z)", cuerpo or "", re.S | re.M | re.I)
    if not m:
        return ""
    return re.sub(r"<!--.*?-->", "", m.group(1), flags=re.S).strip()


def zona(ruta):
    for prefijo, area, nivel, motivo in ZONAS:
        if ruta == prefijo or ruta.startswith(prefijo):
            return area, nivel, motivo
    if "/" not in ruta:
        return "orden", "revisa", "Cambia un archivo de la raíz (README, CONVENCIONES)"
    return "otro", "revisa", ""


def lineas_agregadas(parche):
    for linea in (parche or "").splitlines():
        if linea.startswith("+") and not linea.startswith("+++"):
            yield linea[1:]


def analizar(pr, archivos, commits, chequeos):
    cuerpo = pr.get("body") or ""
    movidos, para_leer, binarios = [], [], []
    areas, observar = {}, []
    nivel = "leve"
    vistos_motivo = set()
    hallazgos_texto = []

    for a in archivos:
        ruta, estado = a["filename"], a["status"]
        area, niv, motivo = zona(ruta)
        if a.get("previous_filename"):
            area_antes, niv_antes, motivo_antes = zona(a["previous_filename"])
            if PESO[niv_antes] < PESO[niv] and niv_antes == "bloquea":
                area, niv, motivo = area_antes, niv_antes, motivo_antes
        solo_movido = estado == "renamed" and a.get("changes", 0) == 0
        # Mover algo dentro de su zona no pide decisión; cambiar su contenido sí.
        if solo_movido and niv != "bloquea":
            niv = "leve"
        areas[area] = areas.get(area, 0) + 1
        if PESO[niv] < PESO[nivel]:
            nivel = niv
        if motivo and not solo_movido and motivo not in vistos_motivo:
            vistos_motivo.add(motivo)
            observar.append((niv, motivo))
        if solo_movido:
            movidos.append(a)
        elif BINARIOS.search(ruta):
            binarios.append(a)
        else:
            para_leer.append(a)
        if ruta.startswith(("registro-ia/", "pre-kino/")):
            continue
        for texto in lineas_agregadas(a.get("patch")):
            for patron, motivo_v in VOCABULARIO:
                if patron.search(texto) and "nunca" not in texto.lower():
                    hallazgos_texto.append(("revisa", f"Vocabulario: {motivo_v} en `{ruta}`"))
            for patron, motivo_s in SENSIBLES:
                if patron.search(texto):
                    grave = "secreto" in motivo_s or "llave" in motivo_s
                    hallazgos_texto.append(("bloquea" if grave else "revisa",
                                            f"Datos sensibles: {motivo_s} en `{ruta}`. Confirma que no sea real"))

    for h in dict.fromkeys(hallazgos_texto):
        observar.append(h)
        if PESO[h[0]] < PESO[nivel]:
            nivel = h[0]

    agregadas = sum(a.get("additions", 0) for a in para_leer)
    quitadas = sum(a.get("deletions", 0) for a in para_leer)
    if len(para_leer) > PR_GRANDE_ARCHIVOS or agregadas + quitadas > PR_GRANDE_LINEAS:
        observar.append(("revisa", f"PR grande: {len(para_leer)} archivos y {agregadas + quitadas} líneas para leer. Pide partirlo por tema si mezcla trabajos"))
        if PESO["revisa"] < PESO[nivel]:
            nivel = "revisa"
    if len(areas) >= 3:
        observar.append(("revisa", f"Mezcla {len(areas)} áreas ({', '.join(sorted(areas))}): un PR por tarea (AGENTS.md §5.1)"))
    if binarios:
        observar.append(("revisa", f"{len(binarios)} archivo(s) binarios (imágenes, PDF, etc.): ábrelos en la pestaña de archivos"))
    if not seccion(cuerpo, "Uso de IA"):
        observar.append(("bloquea", "Falta la sección «Uso de IA» (AGENTS.md §5.7)"))
        nivel = "bloquea"
    if not re.search(r"\b(cierra|closes|fixes|resuelve|parte de|relacionado con)\s+#\d+", cuerpo, re.I):
        observar.append(("revisa", "No enlaza un issue con «Cierra #N» (CONVENCIONES.md)"))
    if "menor" in [e["name"] for e in pr.get("labels", [])] and nivel in ("decide", "bloquea"):
        observar.append(("revisa", "Tiene la etiqueta `menor` pero toca zonas que piden tu decisión"))

    fallidos = [c["name"] for c in chequeos if c.get("conclusion") in ("failure", "timed_out", "cancelled", "action_required")]
    pendientes = [c["name"] for c in chequeos if c.get("status") != "completed"]
    if fallidos:
        estado_ci = "❌ " + ", ".join(sorted(set(fallidos)))
        observar.append(("bloquea", f"Chequeos fallidos: {', '.join(sorted(set(fallidos)))}"))
        nivel = "bloquea"
    elif pendientes:
        estado_ci = "⏳ corriendo"
    elif chequeos:
        estado_ci = "✅"
    else:
        estado_ci = "sin chequeos"

    observar.sort(key=lambda h: PESO[h[0]])
    return {
        "nivel": nivel,
        "areas": areas,
        "movidos": movidos,
        "para_leer": para_leer,
        "binarios": binarios,
        "agregadas": agregadas,
        "quitadas": quitadas,
        "observar": observar,
        "ci": estado_ci,
        "commits": commits,
        "que": seccion(cuerpo, "Qué cambia"),
        "por_que": seccion(cuerpo, "Por qué"),
        "decisiones": seccion(cuerpo, "Decisiones"),
        "verificacion": seccion(cuerpo, "Cómo se verificó"),
    }


# ---------- Texto ----------

def recortar(texto, maximo=400):
    texto = re.sub(r"\n{3,}", "\n\n", texto.strip())
    return texto if len(texto) <= maximo else texto[:maximo].rsplit(" ", 1)[0] + " […]"


def cita(texto, vacio):
    texto = recortar(texto) if texto else f"_{vacio}_"
    return "\n".join("> " + l for l in texto.splitlines())


def resumen(pr, r):
    n = pr["number"]
    filas = []
    for a in sorted(r["para_leer"], key=lambda a: (PESO[zona(a["filename"])[1]], a["filename"]))[:40]:
        antes = f" (antes `{a['previous_filename']}`)" if a.get("previous_filename") else ""
        filas.append(f"| {ETIQUETA_NIVEL[zona(a['filename'])[1]].split()[0]} | `{a['filename']}`{antes} | {ESTADOS.get(a['status'], a['status'])} | +{a['additions']} −{a['deletions']} |")
    if len(r["para_leer"]) > 40:
        filas.append(f"| | … y {len(r['para_leer']) - 40} más | | |")
    observar = "\n".join(f"- {ETIQUETA_NIVEL[niv].split()[0]} {txt}" for niv, txt in r["observar"]) or "- Nada fuera de lo normal"
    commits = "\n".join(f"- `{c['sha'][:7]}` {c['commit']['message'].splitlines()[0]}" for c in r["commits"][:15])
    areas = ", ".join(f"{a} ({k})" for a, k in sorted(r["areas"].items(), key=lambda x: -x[1]))
    partes = [
        MARCA_COMENTARIO,
        f"## Resumen para aprobar · {ETIQUETA_NIVEL[r['nivel']]}",
        f"**Autor:** @{pr['user']['login']} · **Áreas:** {areas or 'ninguna'} · **Chequeos:** {r['ci']}",
        "### De qué trata",
        cita(r["que"], "El PR no llenó «Qué cambia»"),
        "**Por qué**",
        cita(r["por_que"], "El PR no llenó «Por qué»"),
        "**Decisiones**",
        cita(r["decisiones"], "No declara decisiones"),
        "### Qué se hizo",
        f"- **Para leer:** {len(r['para_leer'])} archivo(s), +{r['agregadas']} −{r['quitadas']} líneas\n"
        f"- **Solo movidos, idénticos:** {len(r['movidos'])} (git comprobó que no cambiaron: no se leen)\n"
        f"- **Binarios:** {len(r['binarios'])}\n"
        f"- **Commits:** {len(r['commits'])}",
        "### Qué observar",
        observar,
    ]
    if filas:
        partes += [
            "<details><summary>Archivos para leer, de más a menos delicado</summary>\n",
            "| | Archivo | Estado | Líneas |\n|---|---|---|---|\n" + "\n".join(filas),
            "\n</details>",
        ]
    if commits:
        partes += ["<details><summary>Commits</summary>\n", commits, "\n</details>"]
    partes.append(
        f"<sub>Generado por `herramientas/resumir-pr.py` sin IA. Revisa commit por commit en "
        f"[la pestaña Commits](https://github.com/{REPO}/pull/{n}/commits) y marca «Viewed» en cada archivo leído.</sub>"
    )
    return "\n\n".join(partes)


def fila_panel(pr, r):
    n = pr["number"]
    dias = (datetime.now(timezone.utc) - datetime.fromisoformat(pr["created_at"].replace("Z", "+00:00"))).days
    estado = "borrador" if pr.get("draft") else "**listo**"
    principal = r["observar"][0][1] if r["observar"] else "Nada fuera de lo normal"
    areas = ", ".join(sorted(r["areas"])) or "·"
    return (f"| {ETIQUETA_NIVEL[r['nivel']].split()[0]} | [#{n}](https://github.com/{REPO}/pull/{n}) {pr['title']} "
            f"| @{pr['user']['login']} | {estado} | {areas} | {len(r['para_leer'])} (+{r['agregadas']} −{r['quitadas']}) "
            f"| {len(r['movidos'])} | {r['ci']} | {dias} d | {principal} |")


def panel(prs_analizados):
    orden = sorted(prs_analizados, key=lambda x: (x[0].get("draft", False), PESO[x[1]["nivel"]], x[0]["number"]))
    ahora = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    filas = "\n".join(fila_panel(pr, r) for pr, r in orden)
    conteo = {}
    for _, r in orden:
        conteo[r["nivel"]] = conteo.get(r["nivel"], 0) + 1
    resumen_niveles = " · ".join(f"{ETIQUETA_NIVEL[k]}: {conteo[k]}" for k in PESO if k in conteo)
    cabecera = [
        "<!-- panel-pr: este issue lo reescribe la Action «Resumen de PR». No lo edites a mano -->",
        f"**{len(orden)} PR abiertos** · {resumen_niveles} · actualizado {ahora}",
        f"Orden: primero los listos para revisar, y dentro de cada grupo lo que hay que corregir, luego lo que pide tu decisión, luego el resto. "
        f"Cómo aprobar en volumen: [CONVENCIONES.md](https://github.com/{REPO}/blob/main/CONVENCIONES.md#cómo-se-revisa-y-aprueba-un-pr).",
        "| | PR | Autor | Estado | Áreas | Para leer | Movidos | Chequeos | Abierto | Lo primero que observar |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    texto = "\n\n".join(cabecera[:3]) + "\n\n" + "\n".join(cabecera[3:]) + "\n" + filas
    detalles = []
    for pr, r in orden:
        obs = "\n".join(f"- {ETIQUETA_NIVEL[niv].split()[0]} {t}" for niv, t in r["observar"]) or "- Nada fuera de lo normal"
        detalles.append(
            f"<details><summary><b>#{pr['number']}</b> {pr['title']}</summary>\n\n"
            f"**De qué trata**\n\n{cita(r['que'], 'No llenó «Qué cambia»')}\n\n"
            f"**Por qué**\n\n{cita(r['por_que'], 'No llenó «Por qué»')}\n\n"
            f"**Decisiones**\n\n{cita(r['decisiones'], 'No declara decisiones')}\n\n"
            f"**Qué observar**\n\n{obs}\n\n</details>"
        )
    cuerpo = texto + "\n\n## Detalle\n\n" + "\n\n".join(detalles)
    if len(cuerpo) > MAX_PANEL:
        cuerpo = texto + "\n\n_El detalle no cabe en el issue: está en el comentario de resumen de cada PR._"
    return cuerpo


# ---------- Publicar ----------

def comentar(n):
    pr, archivos, commits, chequeos = datos_pr(n)
    texto = resumen(pr, analizar(pr, archivos, commits, chequeos))
    for c in paginar(f"/repos/{REPO}/issues/{n}/comments", limite=5):
        if MARCA_COMENTARIO in (c.get("body") or ""):
            api("PATCH", f"/repos/{REPO}/issues/comments/{c['id']}", {"body": texto})
            print(f"Resumen actualizado en #{n}")
            return
    api("POST", f"/repos/{REPO}/issues/{n}/comments", {"body": texto})
    print(f"Resumen publicado en #{n}")


def armar_panel():
    analizados = []
    for p in paginar(f"/repos/{REPO}/pulls?state=open", limite=3):
        pr, archivos, commits, chequeos = datos_pr(p["number"])
        analizados.append((pr, analizar(pr, archivos, commits, chequeos)))
    return panel(analizados), len(analizados)


def actualizar_panel():
    cuerpo, cuantos = armar_panel()
    existentes = [i for i in paginar(f"/repos/{REPO}/issues?state=open&labels={ETIQUETA_PANEL}", limite=1)
                  if "pull_request" not in i]
    if existentes:
        api("PATCH", f"/repos/{REPO}/issues/{existentes[0]['number']}", {"body": cuerpo, "title": TITULO_PANEL})
        print(f"Panel actualizado en #{existentes[0]['number']} con {cuantos} PR")
    else:
        nuevo = api("POST", f"/repos/{REPO}/issues", {"title": TITULO_PANEL, "body": cuerpo, "labels": [ETIQUETA_PANEL]})
        print(f"Panel creado en #{nuevo['number']} con {cuantos} PR")


def main(argv):
    if argv[:1] == ["--comentar"] and len(argv) == 2:
        comentar(int(argv[1]))
    elif argv[:1] == ["--panel"]:
        actualizar_panel()
    elif argv[:1] == ["--ver-panel"]:
        print(armar_panel()[0])
    elif argv[:1] == ["--ver"] and len(argv) == 2:
        pr, archivos, commits, chequeos = datos_pr(int(argv[1]))
        print(resumen(pr, analizar(pr, archivos, commits, chequeos)))
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
