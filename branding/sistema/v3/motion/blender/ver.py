"""Compone miniaturas RGBA sobre un fondo para revisarlas: ver.py salida.png entrada1.png [entrada2.png …] [--fondo=#011F16]
Pone cada entrada sobre el fondo y las apila en una rejilla de 2 columnas."""
import sys
from PIL import Image
fondo = next((a.split('=')[1] for a in sys.argv if a.startswith('--fondo=')), '#011F16')
rutas = [a for a in sys.argv[2:] if not a.startswith('--')]
ims = []
for r in rutas:
    im = Image.open(r).convert('RGBA')
    base = Image.new('RGBA', im.size, fondo)
    ims.append(Image.alpha_composite(base, im).convert('RGB'))
w, h = ims[0].size
cols = 1 if len(ims) == 1 else 2
filas = (len(ims) + cols - 1) // cols
lienzo = Image.new('RGB', (w * cols, h * filas), '#000000')
for i, im in enumerate(ims):
    lienzo.paste(im.resize((w, h)), ((i % cols) * w, (i // cols) * h))
lienzo.save(sys.argv[1])
