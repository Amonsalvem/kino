"""Convierte las fuentes del repositorio (branding/sistema/fonts, WOFF2 latin) a TTF para Blender.
Blender no lee WOFF2; fontTools + brotli sí. No se descarga ninguna fuente."""
from pathlib import Path
import re

RAIZ = Path(__file__).resolve().parents[5]
FUENTES = RAIZ / 'branding/sistema/fonts'
CACHE = Path(__file__).resolve().parent / '.fuentes'


def ttf(familia):
    """familia: 'jetbrains-mono' o 'archivo'. Toma el archivo del bloque «latin» normal de su CSS."""
    CACHE.mkdir(exist_ok=True)
    destino = CACHE / f'{familia}.ttf'
    if destino.exists():
        return destino
    css = (FUENTES / f'{familia}.css').read_text()
    bloques = re.findall(r'/\* (\S+) \*/\s*@font-face \{(.*?)\}', css, re.S)
    archivo = next(re.search(r'url\(([^)]+)\)', b).group(1) for sub, b in bloques
                   if sub == 'latin' and 'font-style: normal' in b)
    from fontTools.ttLib import TTFont
    f = TTFont(str(FUENTES / archivo))
    f.flavor = None
    f.save(str(destino))
    return destino
