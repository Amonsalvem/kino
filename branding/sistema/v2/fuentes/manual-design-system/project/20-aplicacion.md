# Cómo se aplica

Reglas para llevar el sistema al deck, a los documentos y a la aplicación.

## Deck

Una lámina es una superficie `kino-superficie-base` con margen superior `kino-espacio-3xl`. El shell de referencia es el deck **Kino Sistema de Marca** (barra de navegación, progreso, cortina, aurora, coreografía por lámina); se copia de ahí, no se reconstruye. El movimiento está en `40-movimiento.md`.

- Apertura: bloqueo vertical de la marca, `display-1`, y nada más. Sin subtítulo.
- Lámina de contenido: `display-3` arriba, una sola idea, y la evidencia debajo en `cuerpo-s`.
- Lámina de cifra: `display-2` con la cifra completa y su denominador («0 de 312»), y la fuente en `menor` bajo ella.
- Toda afirmación del diagnóstico lleva su grado —observado o inferido— en `etiqueta`, y el archivo del que sale en `menor`. Es la regla de evidencia del proyecto, no un adorno tipográfico.
- Los estados se dibujan con el componente `Estado` real, no redibujados a mano: si una lámina muestra un `vigente`, tiene que ser el mismo verde que la app.
- Marca de agua: la gota en `kino-texto-tenue` a 24 px en la esquina inferior derecha, respetando su aire mínimo. En la lámina de apertura no va.

## Documentos

- Cuerpo en `cuerpo` sobre `kino-superficie-base`, 62 caracteres de medida.
- Títulos en `titulo-1` y `titulo-2`. El documento no usa `display`: el display es para presentar, no para leer.
- Las tablas llevan cifras en `kino-dato`, alineadas a la derecha, con `tabular-nums`.
- Las citas de la inspección van en bloque, con borde izquierdo de 2 px en `kino-borde-definido` y el archivo de origen al final en `menor`.
- El encabezado lleva el bloqueo horizontal a 28 px; el pie, la fecha en `kino-dato` y el estado del documento («borrador», «revisado») en `etiqueta`. No se usa el componente `Estado` para eso: sus seis estados son del pase y no se amplían.

## Aplicación

- Lo que el residente crea es un `Pase`. Lo que ve el portero es el mismo `Pase`, con los datos personales truncados.
- El conjunto aparece como dato («Refugio Campestre · Casa 14») en `kino-texto-secundario`. La marca en pantalla es siempre Kino.
- Ninguna pantalla muestra un estado que el lector no haya confirmado. Si no hay confirmación, es `sin-confirmar`, aunque la base de datos diga «Permitido».
- El botón que otorga el pase es el único elemento con `kino-acento-base` de relleno en su pantalla.
- Los límites que fija la administración —cupos, duración máxima, franjas horarias— se muestran como texto en `kino-texto-secundario` dentro del formulario del residente, no como errores después de enviarlo.
- Toda pantalla que capture o muestre cédula, rostro o teléfono lleva `kino-resplandor-identidad` y una línea que dice para qué se usa ese dato y cuánto tiempo se guarda.

## Lo que no se hace

- No se usa el verde `vigente` para «éxito» genérico. Guardar un formulario no es un pase vivo.
- No se dibujan colas de aprobación ni bandejas de pendientes: el sistema no las tiene y dibujarlas repondría un cuello de botella que nunca existió.
- No se ilustra con candados, huellas dactilares genéricas ni escudos.
- No se sustituye la marca de Kino por la del conjunto, ni se recolorea el sistema por conjunto.
- No se pone texto de menos de 18 px en 700 sobre el acento.
- No se anima nada que no cambie de estado. La aurora no entra en la aplicación de trabajo.
