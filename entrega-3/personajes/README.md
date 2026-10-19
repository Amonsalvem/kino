# Personajes de Kino · E3-9 APROBADA (19 oct)

Alcance aprobado por Nico: **solo presentaciones y onboarding**, nunca pantallas de operación (portería, rechazos, veredictos).

| | Residente | Administración |
|---|---|---|
| Archivos | `residente.webm` (VP9 con transparencia) · `residente.png` (póster y último cuadro) | `administracion.webm` · `administracion.png` |
| Lenguaje | Membrana viva verde, translúcida, con venas bioluminiscentes; brotes de micelio en la cabeza; esporas en la piel | Membrana índigo bajo placas de quitina lacada (hombros y corona); visor de luz en lugar de ojos |
| Lo que sostiene | Su Pase (el arco, X8) con QR: él sabe a quién espera | Una lámina de cristal con tres franjas y un reloj: fija el marco, no aprueba caso a caso |
| Animación (3 s, 30 fps) | Respira; el Pase sale de la mano y su borde se enciende tres veces; las venas laten con él | Respira; el visor se enciende; las tres franjas se fijan una tras otra |

**Formato: 3D biopunk** (pedido de Nico).
- Fuente: `branding/sistema/v3/motion/blender/personajes.py` (bpy 4.2, EEVEE).
- Construido por código: metabolas para la membrana, tubos para brazos y micelio, Voronoi distorsionado para las venas. Los colores salen de `tokens.motion.json`.
- Se reconstruye con `.venv/bin/python personajes.py residente|administracion --frames=1-90 --escala=67 --muestras=32` y después se codifica con ffmpeg (VP9 con alfa).
- **Safari:** muestra el póster PNG con transparencia. Para que se anime, hace falta HEVC con alfa, que solo se codifica en macOS (`avconvert` o Compressor).

La versión 2D descartada quedó en `_obsoleto-2d/`.
