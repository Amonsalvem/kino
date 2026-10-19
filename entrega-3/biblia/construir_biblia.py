"""Llena la plantilla Diex de la Biblia (documento integrador) con el contenido de Kino para la entrega 3.

Uso: python3 entrega-3/biblia/construir_biblia.py
Lee  entrega-3/fuentes/BIBLIA_Formato_Documento_Integrador_Diex_EAFIT.docx
Escribe entrega-3/Kino_Biblia_E3.docx

Conserva los estilos de la plantilla: solo reemplaza los textos guía «Escribe aquí…» y los campos de portada.
El contenido vive en contenido.py para que se pueda corregir sin tocar el XML.
"""
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from contenido import PORTADA, EQUIPO, RESUMEN, SECCIONES, HECHOS  # noqa: E402

PLANTILLA = AQUI.parent / 'fuentes' / 'BIBLIA_Formato_Documento_Integrador_Diex_EAFIT.docx'
SALIDA = AQUI.parent / 'Kino_Biblia_E3.docx'

TINTA = '1F2937'
TEAL = '12868F'


def run(texto, b=False, i=False, color=TINTA, sz=20, mono=False):
    rpr = ''
    if mono:
        rpr += '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/>'
    if b:
        rpr += '<w:b/><w:bCs/>'
    if i:
        rpr += '<w:i/><w:iCs/>'
    rpr += f'<w:color w:val="{color}"/><w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>'
    return f'<w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve">{escape(texto)}</w:t></w:r>'


def rich(texto, **kw):
    """**negrita** dentro de un texto."""
    partes = re.split(r'(\*\*[^*]+\*\*)', texto)
    return ''.join(run(p[2:-2], b=True, **kw) if p.startswith('**') else run(p, **kw) for p in partes if p)


def par(texto, after=80, ind=0, **kw):
    sangria = f'<w:ind w:left="{ind}" w:hanging="{200 if ind else 0}"/>' if ind else ''
    return f'<w:p><w:pPr><w:spacing w:after="{after}" w:line="276" w:lineRule="auto"/>{sangria}</w:pPr>{rich(texto, **kw)}</w:p>'


def subtitulo(texto):
    return f'<w:p><w:pPr><w:keepNext/><w:spacing w:before="120" w:after="60"/></w:pPr>{run(texto, b=True, color=TEAL, sz=20)}</w:p>'


def tabla(filas, anchos=None):
    n = len(filas[0])
    total = 9760
    anchos = anchos or [total // n] * n
    grid = ''.join(f'<w:gridCol w:w="{a}"/>' for a in anchos)
    borde = '<w:{0} w:val="single" w:sz="4" w:space="0" w:color="D8DCE8"/>'
    bordes = ''.join(borde.format(k) for k in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV'])
    out = [f'<w:tbl><w:tblPr><w:tblW w:w="{total}" w:type="dxa"/><w:tblBorders>{bordes}</w:tblBorders><w:tblLayout w:type="fixed"/></w:tblPr><w:tblGrid>{grid}</w:tblGrid>']
    for k, fila in enumerate(filas):
        out.append('<w:tr>' + ('<w:trPr><w:tblHeader/></w:trPr>' if k == 0 else ''))
        for j, celda in enumerate(fila):
            fondo = '<w:shd w:val="clear" w:color="auto" w:fill="E8F4F4"/>' if k == 0 else ''
            out.append(
                f'<w:tc><w:tcPr><w:tcW w:w="{anchos[j]}" w:type="dxa"/>{fondo}<w:tcMar><w:top w:w="60" w:type="dxa"/><w:left w:w="90" w:type="dxa"/><w:bottom w:w="60" w:type="dxa"/><w:right w:w="90" w:type="dxa"/></w:tcMar></w:tcPr>'
                f'<w:p><w:pPr><w:spacing w:after="0"/></w:pPr>{rich(str(celda), sz=17, b=(k == 0))}</w:p></w:tc>'
            )
        out.append('</w:tr>')
    out.append('</w:tbl>')
    out.append('<w:p><w:pPr><w:spacing w:after="60"/></w:pPr></w:p>')
    return ''.join(out)


FIGURAS = []  # (rId, archivo) que main() copia a word/media y registra en las relaciones


def figura(archivo, pie):
    """Imagen a todo el ancho del texto (9760 twips), con su pie en cursiva."""
    from PIL import Image
    ruta = AQUI / 'figuras' / archivo
    w, h = Image.open(ruta).size
    cx = 9760 * 635  # twips → EMU
    cy = int(cx * h / w)
    rid = f'rIdKino{len(FIGURAS) + 1}'
    FIGURAS.append((rid, ruta))
    n = len(FIGURAS)
    dib = (
        f'<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/>'
        f'<wp:docPr id="{900 + n}" name="Figura {n}" descr="{escape(pie)}"/>'
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:nvPicPr><pic:cNvPr id="{900 + n}" name="{archivo}"/><pic:cNvPicPr/></pic:nvPicPr>'
        f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>'
        '</a:graphicData></a:graphic></wp:inline></w:drawing></w:r>'
    )
    return (f'<w:p><w:pPr><w:keepNext/><w:spacing w:before="60" w:after="40"/></w:pPr>{dib}</w:p>'
            + par(f'Figura {n}. {pie}', i=True, color='4B5563', sz=17, after=120))


def bloque(items):
    """items: lista de str (párrafo), ('h', str), ('-', str) viñeta, ('t', filas[, anchos]), ('n', str) nota,
    ('img', archivo en figuras/, pie)."""
    out = []
    for it in items:
        if isinstance(it, str):
            out.append(par(it))
        elif it[0] == 'h':
            out.append(subtitulo(it[1]))
        elif it[0] == '-':
            out.append(par('•  ' + it[1], after=50, ind=360))
        elif it[0] == 't':
            out.append(tabla(it[1], it[2] if len(it) > 2 else None))
        elif it[0] == 'n':
            out.append(par(it[1], i=True, color='4B5563', sz=18))
        elif it[0] == 'img':
            out.append(figura(it[1], it[2]))
    return ''.join(out)


def reemplazar_parrafo(xml, marcador, nuevo):
    """Reemplaza el párrafo que contiene `marcador` (y el párrafo vacío que la plantilla deja después)."""
    i = xml.find(marcador)
    if i < 0:
        raise SystemExit(f'no encontré: {marcador}')
    ini = xml.rfind('<w:p ', 0, i)
    fin = xml.find('</w:p>', i) + len('</w:p>')
    # La plantilla deja párrafos vacíos para escribir a mano; con contenido sobran.
    while True:
        m = re.match(r'<w:p [^>]*><w:pPr><w:spacing w:after="60"/></w:pPr></w:p>', xml[fin:])
        if not m:
            break
        fin += m.end()
    return xml[:ini] + nuevo + xml[fin:]


def llenar_celda(xml, rotulo, valor):
    """En la fila de la portada cuyo primer campo es `rotulo`, cambia el texto de la segunda celda."""
    i = xml.find(f'>{rotulo}<')
    if i < 0:
        raise SystemExit(f'no encontré la fila {rotulo}')
    fila_fin = xml.find('</w:tr>', i)
    tc2 = xml.find('<w:tc>', i)
    p_ini = xml.find('<w:p ', tc2)
    p_fin = xml.rfind('</w:p>', p_ini, fila_fin) + len('</w:p>')
    ppr = re.search(r'<w:pPr>.*?</w:pPr>', xml[p_ini:p_fin])
    nuevo = f'<w:p>{ppr.group(0) if ppr else ""}{run(valor, sz=20)}</w:p>'
    return xml[:p_ini] + nuevo + xml[p_fin:]


def main():
    tmp = Path(tempfile.mkdtemp())
    with zipfile.ZipFile(PLANTILLA) as z:
        z.extractall(tmp)
    doc = tmp / 'word' / 'document.xml'
    x = doc.read_text(encoding='utf-8')

    for rotulo, valor in PORTADA.items():
        x = llenar_celda(x, rotulo, valor)

    # Equipo: los campos «____» en orden (nombre, rol, correo por integrante).
    campos = [v for persona in EQUIPO for v in persona]
    for valor in campos:
        m = re.search(r'<w:r><w:rPr><w:color w:val="9AA0AE"/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr><w:t>_{10,}</w:t></w:r>', x)
        if not m:
            break
        x = x[: m.start()] + run(valor, sz=20) + x[m.end():]
    x = re.sub(r'<w:t>_{10,}</w:t>', '<w:t>—</w:t>', x)

    x = reemplazar_parrafo(x, 'Escribe aquí el resumen ejecutivo de tu proyecto…', bloque(RESUMEN))
    for codigo, items in SECCIONES:
        x = reemplazar_parrafo(x, 'Escribe aquí el contenido de tu proyecto…', bloque(items))
    if 'Escribe aquí' in x:
        raise SystemExit('quedó un texto guía sin reemplazar')

    # Lista de verificación: marca lo que esta entrega deja completo.
    hechos = set(HECHOS)
    def marcar(m):
        fila = m.group(0)
        cod = re.search(r'>(\d\.\d)  ', fila)
        if cod and cod.group(1) in hechos:
            fila = fila.replace('<w:t>☐</w:t>', '<w:t>☑</w:t>', 1)
        return fila
    x = re.sub(r'<w:tr[ >].*?</w:tr>', marcar, x, flags=re.S)

    doc.write_text(x, encoding='utf-8')
    # Figuras: a word/media y a las relaciones del documento.
    rels = tmp / 'word' / '_rels' / 'document.xml.rels'
    r = rels.read_text(encoding='utf-8')
    (tmp / 'word' / 'media').mkdir(exist_ok=True)
    for rid, ruta in FIGURAS:
        destino = f'media/kino-{ruta.name}'
        shutil.copy(ruta, tmp / 'word' / destino)
        r = r.replace('</Relationships>', f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="{destino}"/></Relationships>')
    rels.write_text(r, encoding='utf-8')
    if SALIDA.exists():
        SALIDA.unlink()
    with zipfile.ZipFile(SALIDA, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in sorted(tmp.rglob('*')):
            if f.is_file():
                z.write(f, f.relative_to(tmp).as_posix())
    shutil.rmtree(tmp)
    print(f'ok {SALIDA.relative_to(AQUI.parent.parent)} · {len(SECCIONES)} apartados · {len(FIGURAS)} figuras · {len(hechos)} marcados en la lista')


if __name__ == '__main__':
    main()
