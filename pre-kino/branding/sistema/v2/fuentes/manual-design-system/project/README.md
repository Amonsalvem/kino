Kino es una plataforma de control de acceso para conjuntos cerrados. Este es su sistema de marca, versión 2 (23 sep 2026): una identidad propia, oscura y viva, construida sobre la estética de la segunda entrega. Cada decisión apunta a un hallazgo del diagnóstico. El recorrido completo, con el motor de movimiento funcionando, está en el deck **Kino Sistema de Marca**; este manual es la referencia de trabajo.

## Qué cambió en la versión 2

| Qué | Antes (v1, 19–22 sep) | Ahora (v2, 23 sep) | Por qué |
|---|---|---|---|
| Marca | Marca blanca: el conjunto podía cambiar la piel | **Kino es la marca.** El conjunto aparece como dato («Refugio Campestre · Casa 14»), nunca como marca | Decisión del equipo: Kino se vende y se reconoce como producto propio |
| Objeto | «Permiso» | **«Pase»** en todo: interfaz, código y material | Una palabra corta, física, que el portero y el residente dicen igual |
| Acento oscuro | `biolum-d90` `#00D595` | `biolum-d70` `#00BB83`, el de la entrega 2 | Es el color con el que el equipo ya presentó. Su texto se resuelve con una regla de tamaño (ver Color) |
| Estética | Membrana plana | Aurora de fondo, cortina de entrada, tarjetas que crecen, boleto con talón | La entrega 2 es la base de la identidad, no un tema del deck |
| Movimiento | Tres curvas | 8 duraciones, 5 curvas, 2 escalonados y 5 verbos con significado | Ver `40-movimiento.md` |
| Tokens eliminados | `kino-tenant-marca`, `kino-tenant-radio` | — | Sin capa de conjunto |

## De dónde sale este sistema

La inspección de la aplicación en producción (septiembre de 2026, los cuatro paneles por rol) encontró tres cosas que el sistema actual no sabe decir. El sistema visual existe para decirlas:

1. **No hay pase temporal.** Un invitado queda matriculado como miembro permanente con rol «Visitante», sin fecha y sin vigencia. → El sistema está construido alrededor de un objeto con vida: el pase `vigente` late, el `por-vencer` avisa, el `vencido` se apaga.
2. **La interfaz afirma lo que no sabe.** Una placa queda «Permitido» al instante aunque el hardware nunca la reciba; en Refugio Campestre hay 0 de 312 personas sincronizadas. → El estado `sin-confirmar` no tiene relleno y su borde es discontinuo. El color solo nombra hechos que el lector confirmó.
3. **La simetría está invertida.** El portero ve de los residentes datos que ellos no ven de sí mismos. → El componente `Pase` es el mismo para los dos roles, y todo dato personal va marcado con `identidad` y truncado por defecto.

Cuando tengas que decidir algo que este documento no cubre, decídelo contra esas tres frases.

## Contenido y tono

- Español, segunda persona (tuteo), voz activa. Un control dice lo que hace: «Dar pase», y el aviso dice «Pase enviado al lector». Cuando el lector confirma, el estado pasa a `vigente`.
- Tono sobrio y exacto. Perfil aprobado por el equipo el 22 sep 2026 en las cuatro dimensiones de NN/g (1 = primer polo, 5 = segundo): formalidad 2, humor 1, respeto 1, entusiasmo 2. Se confirma con hechos («vigente hasta las 6:00 p. m.») y no se celebra («¡Listo!»).
- **Pase** es lo que recibe un invitado o un colaborador, con vigencia. **Cuenta** es lo que tiene un residente. No se mezclan, ni en la interfaz ni en el código. «Permiso» ya no se usa como sustantivo del objeto.
- **Acceso previsto** es el pase que el residente prepara antes de que la persona llegue.
- **Colaborador** (empleada, técnicos) es el ingreso más frecuente y tiene la misma prioridad visual que la visita ocasional.
- **Lector** es quien permite el ingreso (placa, QR, rostro), no el vigilante.
- Sin mayúsculas sostenidas salvo en `etiqueta`, siglas y placas. Sin emoji.
- Los errores dicen qué pasó y qué hacer: «El lector no confirmó el pase. Vuelve a enviarlo o avisa a portería.» Nunca «Ups» ni disculpas.
- Las cifras van con su unidad, su denominador y su fecha: «0 de 312 sincronizados».
- No se escriben «contraseña», «aprobación de ingreso», «Arcana», «seguridad total» ni «todo queda registrado». No se describen funciones que el producto no tiene confirmadas.
- La lista completa, con los patrones que se revisan de forma automática, vive en `gorr-brand-system/clientes/kino/voz.json`.

## Fundamentos visuales

**Color.** Kino vive en oscuro: `oscuro` es el tema canónico y `claro` el segundo. Fondo de página en `kino-superficie-base` (`#011F16`), tarjetas en `kino-superficie-membrana`, texto corrido en `kino-texto-primario`. El acento `kino-acento-base` (`#00BB83`) significa una sola cosa: **otorgar un pase**. Va en el botón que lo da, en el boleto recién emitido y en la marca; en nada más. Los seis estados —`vigente`, `por-vencer`, `vencido`, `negado`, `sin-confirmar`, `identidad`— tienen sus propios tokens y nunca se sustituyen por el acento.

Cada escala se generó resolviendo un contraste objetivo contra el fondo de su tema, así que el nombre del paso es una promesa: `d45` es 4.5:1 y `d90` es 9:1. La paleta de registro está congelada en los valores de la entrega 2 (`legado/paleta-2026-09-19.json`) y Leonardo la reproduce con ΔE OK medio de 0,019.

**Regla de tamaño del acento.** El texto oscuro sobre `#00BB83` pasa WCAG con 7,63:1, pero APCA le da Lc 55,1. Por eso el texto sobre acento va a **18 px o más en peso 700** (o 21 px en 600, 24 px en 500). Un botón de Kino cumple eso por diseño; una etiqueta de 12 px sobre acento, no, y no se hace.

**Tipografía.** Archivo con eje de ancho (`wdth` 62–125) en `display` y `texto`; JetBrains Mono en `dato`. El display se usa condensado y pesado, a `display-1` una sola vez por pantalla. Placas, códigos, horas e identificadores van en `dato`, `placa` o `etiqueta`: cero barrado y cifras tabulares, porque una placa mal leída es un ingreso mal concedido.

**Espacio y retícula.** Doce columnas con canal `kino-espacio-l`. Relleno de tarjeta `kino-espacio-m`, separación entre tarjetas `kino-espacio-l`, entre secciones `kino-espacio-2xl`. El texto corrido no pasa de 62 caracteres.

**Bordes, radios y elevación.** Radio por defecto `kino-radio-m`. Kino no usa sombra proyectada: usa resplandor. `kino-resplandor-vigente` marca lo que está vivo, `kino-resplandor-identidad` lo que toca un dato personal, `kino-relieve-membrana` levanta apenas una tarjeta. Una superficie apagada no resplandece.

**Fondo vivo.** La aurora (un campo WebGL a media resolución entre menta profunda `#006B4C`, índigo `#2E2470` y la base, bajo un velo del color de fondo) es el ambiente de la marca en deck, web y pantallas de bienvenida. En la aplicación de trabajo no va: ahí el fondo es `kino-superficie-base` plano, para que lo único que se mueva sea el estado.

**Movimiento.** Cinco verbos, cada uno con su curva y su duración: `aparecer`, `confirmar`, `caducar`, `revocar` y `cascada`. Caducar es lento y revocar es seco, para que se distingan sin leer. El punto de `vigente` es lo único que se anima solo. Todo respeta `prefers-reduced-motion`. Detalle en `40-movimiento.md`.

**Estados y foco.** Anillo de foco en `kino-borde-foco`, sólido, 2 px con 2 px de separación. Todo estado lleva palabra además de color. Ningún par de estados se distingue solo por hue.

## Iconografía

Kino usa **Iconoir** (MIT, retícula de 24 × 24, trazo de 1,5), teñido con `currentColor`. El icono nunca sustituye la palabra en un estado, y la gota de la marca es el único símbolo que marca un ingreso en la traza. Sin candados ni escudos.

## El conjunto como dato

Kino es la marca en toda pantalla, documento y material. El conjunto no tiene capa de marca: no cambia colores, no cambia radios y su logotipo no sustituye al de Kino. Aparece como lo que es para el sistema, un dato: nombre de la comunidad y unidad, en `kino-texto-secundario`, junto a la persona. Así la traza de Monte Sereno y la de cualquier otro conjunto se leen con el mismo código.

## Fuente y mantenimiento

Los valores de este manual se generan; no se editan aquí. La fuente es `gorr-brand-system/clientes/kino/` (`marca.config.json`, `tokens/` en DTCG 2025.10, `voz.json`, `pares.json`). La implementación de referencia está en `branding/sistema/v2/` (`kino-sistema.css`, `kino-movimiento.js`). La verificación está en `30-verificacion.md`.

La librería de Figma es **Kino — Sistema de marca v2** (equipo de Alejandro): 113 variables en cuatro colecciones (Primitivos; Color con modos Oscuro y Claro; Espacio y radio; Movimiento), 12 estilos de texto, 6 efectos y los componentes Estado, Pase/Boleto, Pase/Fila, Flujo/Nodo, Evidencia/Grado, Evidencia/Afirmación, Tarjeta/Cifra, Tarjeta/Destacado, Tarjeta/Aviso y Marca/Bloqueo vertical. Cada variable lleva su nombre CSS (`var(--kino-…)`) como sintaxis de código.
https://www.figma.com/design/BO7UnDO9iE0aG6yUpNj0bc
