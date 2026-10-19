# Barrido de diagramación del prototipo · 19 oct 2026

Fuente: `prototipo/pruebas/barrido.mjs` sobre 23 pantallas a tamaño real (teléfono 390 × 844, portería 1080 × 760, administración 1280 × 800), más la revisión de una captura por pantalla. El script mide texto cortado, elementos fuera del dispositivo, objetivos táctiles menores de 44 px, letra menor de 12 px y separaciones fuera de la escala (4, 8, 12, 16, 24, 32, 48). Lo que el script no ve (jerarquía, aire, alineación) sale de las capturas.

## Resultado antes de corregir

| Tipo | Hallazgos | Dónde |
|---|---|---|
| Fuera del dispositivo | 18 | Portería: al abrir «Digitar código» la columna lateral se ensancha 44 px y se sale del borde |
| Objetivo táctil < 44 px | 7 reales | Enlaces de 39 px («Ver Pases anteriores», «Cambiar número»), días de la semana de 39 px de ancho |
| Letra < 12 px | 2 | Hora de la burbuja (11 px) y rótulo de la imagen del Pase (10 px) en el chat de la visita |
| Separación fuera de escala | 6 | Células del cupo (5 px) |
| Desborde decorativo | 6 | Aurora de la cabecera (recortada por el contenedor, sin efecto visible) |

## Lo que se ve en las capturas

### Portería (la pantalla más débil)
| # | Problema | Por qué importa |
|---|---|---|
| P1 | El panel de resultado es un rectángulo grande con tres bloques flotando en el centro; arriba y abajo queda aire sin función | Se lee desde 3 m: el veredicto tiene que dominar y el resto alinearse a una retícula |
| P2 | La talanquera flota debajo del panel, chica y separada del resultado | Es la consecuencia física de la lectura y queda como adorno |
| P3 | La animación del veredicto es un fundido con escala y unos rayos encima del texto; el rechazo y el ingreso se mueven igual | La respuesta tiene que decir sí o no antes de que se lea la palabra |
| P4 | Los datos (Casa, Otorgó, Vigencia, Entró con) usan columnas de ancho desigual; «Vigencia» empuja a las demás | Sin retícula, el ojo salta |
| P5 | La lista de llegadas se corta a media tarjeta sin indicar que hay más | Parece un error de render |
| P6 | En la bitácora, quien entró aparece con el chip «Vigente» | El evento es «Entró»; el estado del Pase es otra cosa |
| P7 | El teclado para digitar empuja la columna fuera del borde | Ver tabla anterior |

### Residente
| # | Problema |
|---|---|
| R1 | En la tarjeta del colaborador, el rótulo «Colaborador · Aseo y cocina» se parte en dos líneas junto al chip y la vigencia corta «p. / m.» en otra línea |
| R2 | El indicador de cupo («2 de 5 visitas activas · tope de la administración») se parte en dos líneas desalineadas con las células |
| R3 | El botón fijo «Crear Pase» tapa la última tarjeta sin un borde que lo separe del contenido |
| R4 | En Crear Pase, los cuatro atajos de «¿Cuándo?» quedan 3 + 1, con «Otra hora» huérfano |
| R5 | En el detalle, el botón fijo de revocar tapa el título del grupo «Extender» |
| R6 | Los tres modos (QR, Código, Placa) tienen anchos distintos y no comparten borde con el Portal |
| R7 | El chip de estado, el nombre y la vigencia del detalle no comparten margen con el grupo «Lo que pasó» |

### Visita
| # | Problema |
|---|---|
| V1 | Letra de 10 y 11 px en la imagen del Pase y la hora del mensaje |

### Administración
| # | Problema |
|---|---|
| A1 | El resumen deja media pantalla vacía y la tabla de rechazos reparte columnas sin relación con el contenido |
| A2 | Límites: los controles tienen el mismo peso que el botón de guardar; la vista previa queda lejos del control que se movió |

## Qué se corrige
Todo lo anterior, más los cambios de E3-2 (sin cupo ni duración máxima, estadías largas) que también tocan la diagramación de la hoja y del inicio. El resultado después de corregir va al final de este archivo.

## Resultado después de corregir

| Tipo | Antes | Después | Nota |
|---|---|---|---|
| Fuera del dispositivo | 18 | 0 | El teclado de portería usa `minmax(0,1fr) auto` |
| Hijo más ancho que su padre | no se medía | 0 | Regla nueva del script: encontró los pasos «Entra / Sale» del colaborador montados uno sobre otro; ahora van en filas |
| Letra < 12 px | 2 | 0 | |
| Separación fuera de escala | 6 | 0 | Las células del cupo salieron con E3-2 |
| Objetivo táctil < 44 px | 7 | 0 reales | Quedan 34 de 43,9 px (redondeo del escalado) y los días de la semana, de 44 × 48 |

| # | Qué cambió |
|---|---|
| P1–P2 | El panel tiene retícula: veredicto y texto a la izquierda, talanquera a la derecha dentro del panel, datos en una franja de ancho completo abajo |
| P3 | Coreografía nueva: la ola nace en el lector, el ícono se dibuja, el texto sube en cascada. Entra: la talanquera sube con resorte y baja sola a los 4 s, con barra «Se cierra sola». No entra: el veredicto niega una vez, la luz roja late dos veces y la talanquera queda abajo (si seguía abierta por el ingreso anterior, baja) |
| P4 | Datos con columnas fijas (Casa, Otorgó, Con, Vigencia) |
| P5 | La lista de llegadas se desvanece al final |
| P6 | La bitácora dice «Entró» para el evento |
| R1–R7 | Rótulos con elipsis, «Unas horas / Un día / Se queda» en tres columnas iguales, plazos en dos, pie fijo con borde, modos de igual ancho, márgenes comunes en el detalle |
| A1–A2 | Resumen en cifras y dos tablas; Franjas en dos tarjetas con su vista previa junto a «Guardar franjas» |

Fotogramas de la coreografía: `node prototipo/pruebas/fotogramas.mjs` (0 a 4.600 ms, entra y no entra).
