"""Convierte las fuentes del repositorio (branding/sistema/fonts, WOFF2 latin) a TTF para Blender.
Blender no lee WOFF2 ni elige instancias de una fuente variable; fontTools + brotli sí. No se descarga ninguna fuente.

Archivo y JetBrains Mono son variables: ttf() fija el peso (wght) y el ancho (wdth, en %) con varLib.instancer,
así el 3D usa los mismos cortes que la web (Archivo 700 en nombre y chip; X5: 112 % en titulares).
"""
from pathlib import Path
import re

RAIZ = Path(__file__).resolve().parents[5]
FUENTES = RAIZ / 'branding/sistema/fonts'
CACHE = Path(__file__).resolve().parent / '.fuentes'


def ttf(familia, peso=400, ancho=100):
    """familia: 'jetbrains-mono' o 'archivo'. Toma el archivo del bloque «latin» normal de su CSS."""
    CACHE.mkdir(exist_ok=True)
    destino = CACHE / f'{familia}-{peso}-{ancho}.ttf'
    if destino.exists():
        return destino
    css = (FUENTES / f'{familia}.css').read_text()
    bloques = re.findall(r'/\* (\S+) \*/\s*@font-face \{(.*?)\}', css, re.S)
    archivo = next(re.search(r'url\(([^)]+)\)', b).group(1) for sub, b in bloques
                   if sub == 'latin' and 'font-style: normal' in b)
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer
    f = TTFont(str(FUENTES / archivo))
    f.flavor = None
    if 'fvar' in f:
        ejes = {a.axisTag: (a.minValue, a.maxValue) for a in f['fvar'].axes}
        fijar = {}
        if 'wght' in ejes:
            fijar['wght'] = min(max(peso, ejes['wght'][0]), ejes['wght'][1])
        if 'wdth' in ejes:
            fijar['wdth'] = min(max(ancho, ejes['wdth'][0]), ejes['wdth'][1])
        f = instancer.instantiateVariableFont(f, fijar)
    f.save(str(destino))
    return destino
