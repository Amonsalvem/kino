---
name: kino-marca
description: Aplica la marca Kino (color, tipografía, voz y vocabulario) a cualquier pieza: deck, documento, página HTML, interfaz o texto de producto. Usar al producir o revisar cualquier entregable de Kino.
---

# Marca Kino

> Generado por gorr-brand-system desde las fuentes del cliente. No editar a mano: cambiar marca.config.json, voz.json o tokens/ y correr `npm run ciclo -- kino`.

## Reglas que no se negocian

1. El color solo nombra hechos confirmados. Si el lector no confirmó, el estado es Sin confirmar: sin relleno y con borde discontinuo.
2. Todo estado lleva palabra además de color. Estados del Pase: Previsto, Sin confirmar, Vigente, Por vencer, Usado, Vencido, Revocado. Evento en la entrada: Rechazado.
3. Dos verdes: #00BB83 (acento-base) es la marca, la gota del logo y el nodo «Otorgar»; #00D595 (accion-fondo) es el botón que crea un Pase. En claro, los dos pasan a #006343.
4. Kino es la marca. El conjunto aparece como dato (texto o chip), nunca con logo ni colores propios.
5. Toda afirmación lleva su grado de evidencia (observado, prueba, entorno, inferido) y su fuente.
6. Placas, códigos, horas, rótulos y cifras van en JetBrains Mono, con cero barrado y cifras tabulares.
7. El tema oscuro reajustado es el canónico; el claro es el segundo y es el del PDF del Pase.
8. Radio 14 en tarjetas, 8 en controles. El arco (radio pleno arriba) solo va en lo que es un Pase.
9. Íconos con trazo 1,7 y puntas redondas.
10. Sin candados, escudos ni muros: Kino es una membrana.
11. Lo que se mueve significa algo: crecer es aparecer (820 ms, cascada de 90 ms), decaer es caducar, latir es estar vivo. Nada se anima para decorar.

## Color

Cada familia significa algo. No usar una familia fuera de su significado.

| Familia | Significa | Por qué existe |
|---|---|---|
| `sustrato` | Superficies | Linaje: carbón #2C2D2F de la Propuesta 1 con sesgo verde (medio de cultivo). |
| `hueso` | Texto y tema claro | Linaje: hueso #E1E8EE enfriado hacia el verde. |
| `biolum` | Marca (#00BB83, d70), acción de otorgar (#00D595, d90) y el estado Vigente | H1/H5: hoy no existe el acceso temporal para una persona; el estado Vigente tiene que verse vivo. |
| `ambar` | Vigencia que se agota | H1/H5: la vigencia no existe hoy; por-vencer la hace visible. |
| `carmin` | Revocado y el evento Rechazado | Rechazado y Revocado se distinguen de Vencido: tienen causa o autor. |
| `violeta` | Dato personal o biométrico | R4 y Res. 52185 de 2025 de la SIC: el dato de identidad se marca. |
| `indigo` | Profundidad, enlaces y el estado Previsto | Linaje: índigo #00177D de la Propuesta 1. |

### Tokens semánticos (tema oscuro, canónico)

En código, usar siempre la variable, nunca el hex. El hex va solo para herramientas que no leen CSS.

| Variable | Valor |
|---|---|
| `--kino-superficie-abismo` | `#00140C` |
| `--kino-superficie-base` | `#011F16` |
| `--kino-superficie-elevada` | `#0B2A20` |
| `--kino-superficie-membrana` | `#17362B` |
| `--kino-superficie-inversa` | `#EFFCF7` |
| `--kino-borde-tenue` | `#2A483D` |
| `--kino-borde-definido` | `#6E8E81` |
| `--kino-borde-foco` | `#00BB83` |
| `--kino-texto-primario` | `#EFFCF7` |
| `--kino-texto-secundario` | `#CEDBD6` |
| `--kino-texto-tenue` | `#A5C7B8` |
| `--kino-texto-inverso` | `#00140C` |
| `--kino-texto-sobre-acento` | `#00140C` |
| `--kino-texto-enlace` | `#CCDDFE` |
| `--kino-acento-base` | `#00BB83` |
| `--kino-acento-fuerte` | `#00EAA5` |
| `--kino-acento-sordo` | `#00422C` |
| `--kino-accion-fondo` | `#00D595` |
| `--kino-accion-fondo-activo` | `#00EAA5` |
| `--kino-accion-texto` | `#00140C` |
| `--kino-marca-bloque` | `#EFFCF7` |
| `--kino-marca-gota` | `#00BB83` |
| `--kino-estado-previsto-fondo` | `#092D93` |
| `--kino-estado-previsto-texto` | `#CCDDFE` |
| `--kino-estado-previsto-borde` | `#B6CEFF` |
| `--kino-estado-sin-confirmar-fondo` | `oklch(0 0 0 / 0)` |
| `--kino-estado-sin-confirmar-texto` | `#DBE9E3` |
| `--kino-estado-sin-confirmar-borde` | `#86A799` |
| `--kino-estado-vigente-fondo` | `#00422C` |
| `--kino-estado-vigente-texto` | `#2FF8B2` |
| `--kino-estado-vigente-borde` | `#00EAA5` |
| `--kino-estado-por-vencer-fondo` | `#503300` |
| `--kino-estado-por-vencer-texto` | `#FFD49C` |
| `--kino-estado-por-vencer-borde` | `#FFC36D` |
| `--kino-estado-usado-fondo` | `#0B2A20` |
| `--kino-estado-usado-texto` | `#E5F3ED` |
| `--kino-estado-usado-borde` | `#86A799` |
| `--kino-estado-vencido-fondo` | `#0B2A20` |
| `--kino-estado-vencido-texto` | `#B8DBCC` |
| `--kino-estado-vencido-borde` | `#86A799` |
| `--kino-estado-revocado-fondo` | `#0B2A20` |
| `--kino-estado-revocado-texto` | `#FEC6C0` |
| `--kino-estado-revocado-borde` | `#86A799` |
| `--kino-estado-rechazado-fondo` | `#79000F` |
| `--kino-estado-rechazado-texto` | `#FED6D2` |
| `--kino-estado-rechazado-borde` | `#FFBEB8` |
| `--kino-estado-identidad-fondo` | `#3E1C96` |
| `--kino-estado-identidad-texto` | `#DADAFE` |
| `--kino-estado-identidad-borde` | `#CAC9FF` |
| `--kino-estado-negado-fondo` | `#79000F` |
| `--kino-estado-negado-texto` | `#FED6D2` |
| `--kino-estado-negado-borde` | `#FFBEB8` |

## Tipografía

- `--kino-fuente-display`: Archivo, Archivo Expanded, system-ui, sans-serif
- `--kino-fuente-texto`: Archivo, system-ui, -apple-system, sans-serif
- `--kino-fuente-dato`: JetBrains Mono, ui-monospace, SF Mono, monospace

Escala fluida (Utopia) de 8 pasos: `--kino-texto-0` es el cuerpo; los positivos suben, `n1` baja. Valores exactos en references/tokens.css.

## Cómo aplicarla en código

```html
<link rel="stylesheet" href="kino-tokens.css">
<body data-tema="oscuro">
```

Temas: `oscuro`, `claro`. Sin atributo, sigue la preferencia del sistema. El CSS completo está en references/tokens.css.

## Voz y tono

Perfil según las cuatro dimensiones de NN/g (1 = primer polo, 5 = segundo). Estado: aprobado por el equipo (22 sep 2026).

| Dimensión | Valor | Cómo se nota |
|---|---|---|
| formal ↔ casual | 2 | Tuteo cercano en la app; frases completas y sin jerga en documentos para la administración. |
| serio ↔ divertido | 1 | Se trata de quién entra a la casa de alguien. Sin chistes en estados, errores ni Pases. |
| respetuoso ↔ irreverente | 1 | Nunca culpar al residente ni al portero; describir lo que pasó, no a quién se le olvidó. |
| sobrio ↔ entusiasta | 2 | Confirmar con hechos (vigente hasta 6:00 p. m.) en vez de celebrar (¡Listo!). |

**Somos:**
- Exactos: decimos la hora, la placa y la vigencia, no «pronto» ni «pendiente».
- Honestos con el estado: lo que el lector no confirmó se dice sin confirmar.
- Breves: una idea por frase, el dato primero.

**No somos:**
- Alarmistas: no hablamos de amenazas, candados ni muros.
- Burocráticos: no pedimos aprobaciones que el sistema no necesita.
- Publicitarios: no prometemos seguridad total ni usamos superlativos.
- Prometedores: no describimos avisos, registros, funciones ni formas de uso que el producto no tenga confirmados. Si el contexto no lo dice, no se escribe.

### Vocabulario propio

- **pase**: El objeto que recibe un invitado o colaborador: autor, motivo, vigencia y modo (placa, QR o código). Caduca solo y no crea una persona.
- **cuenta**: Lo que tiene un residente. Un invitado nunca tiene cuenta.
- **acceso previsto**: El pase que el residente prepara antes de que llegue la persona.
- **colaborador**: Empleada, técnicos y personal recurrente. Misma prioridad que el visitante ocasional.
- **lector**: El dispositivo de la puerta (placa, QR, rostro) que permite el ingreso.
- **otorgar**: El acto de crear un pase. Es lo único que lleva el color de acento.

- Nunca mezclar «pase» y «cuenta»: Pase = invitado o colaborador, con vigencia. Cuenta = residente. Nunca intercambiables, ni en texto ni en código.

### Evitar

| No escribir | Escribir | Por qué |
|---|---|---|
| permiso | pase | El objeto se llama «Pase» (decisión F3 del encargo). En texto de producto no se usa ni como explicación. |
| cuenta del invitado | pase | Pase y cuenta no se mezclan: el invitado recibe un pase con vigencia. |
| contraseña | código por WhatsApp | Decisión tomada: el ingreso a la app es con código por WhatsApp, sin contraseña. |
| aprobación de ingreso | el residente otorga el pase | El administrador no aprueba ingresos; el residente aprueba a sus invitados y la administración fija límites. |
| el vigilante autoriza | el lector permite el ingreso | El ingreso lo permite el lector de la puerta, no el vigilante. |
| Arcana | Kino | Nombre anterior del producto. |
| seguridad total | describir qué registra y qué no | Promesa que el sistema no puede sostener. |
| todo queda registrado | nombrar solo lo que el producto confirma (ver «hechos») | Promesa absoluta: el sistema registra hechos concretos, no «todo». |

### Lo que el producto hace

Lo que el producto hace, confirmado por decisiones del equipo. El copy puede afirmarlo. Lo que no está aquí ni en el contexto de la pieza no se afirma.

**Confirmado (se puede afirmar):**
- El residente otorga el Pase a sus visitas y colaboradores; la administración no aprueba cada ingreso.
- La administración fija los límites: cupos, duración y franjas horarias.
- La visita no necesita cuenta: entra con QR, placa o un código de un solo uso.
- Todo Pase tiene vigencia: desde y hasta una fecha y hora.
- El ingreso lo permite el lector de la entrada (placa, QR o rostro), no portería.
- El residente entra a la app con un código por WhatsApp, sin contraseña.
- Un Pase está en uno de estos estados: Previsto, Sin confirmar, Vigente, Por vencer, Usado, Vencido o Revocado. En la entrada puede ocurrir el evento Rechazado, con su motivo (V5).
- El Pase llega por WhatsApp como imagen con un enlace al Pase vivo; el PDF es opcional (V7).
- Portería puede llamar al residente desde Kino cuando alguien llega con el Pase vencido. La llamada no abre la entrada (X11, dato del equipo; falta verificar el botón en producto).

**No confirmado (no se afirma):**
- Avisos automáticos cuando el lector confirma una placa.
- Un historial de Pases visible para la administración.
- Que el código se pueda digitar en el lector.

### Patrones prohibidos

- Antítesis de apertura «No es X. Es Y»: muletilla de IA. Decir directamente lo que es.
- Antítesis «no X, sino Y»: afirmar Y y quitar el contraste artificial.
- Antítesis «No un demo: el producto vivo».
- «Y» al inicio de frase como golpe dramático.
- Dos puntos de revelación. Unir con «así que» o reescribir.
- Relleno o énfasis vacío.
- Léxico de IA o de agencia: decir el hecho concreto.
- Paralelismo «el único… el único».
- Anáfora «no quiere…, no quiere…».
- Polisíndeton «Ni…, ni…, ni…» de efecto.
- Anáfora «ningún…, ninguna…».
- Cierre lapidario de efecto.
- Raya (em dash) en texto visible: usar coma, punto o paréntesis.
- Mayúsculas de énfasis. Exceptuadas las siglas conocidas y las placas (ABC-123, HTK 481).
- Regla 10: sin exclamaciones. Confirmar con el dato.
- Regla 10: arranque publicitario. Empezar por el dato.
- Regla 10: léxico vacío. Nombrar el objeto o la acción concreta.
- Regla 10: error sin decir qué pasó ni qué hacer.
- Regla 10: «no solo… sino». Decir las dos cosas o la que importa.
- Celebra en vez de confirmar con el dato (entusiasmo 2).
- Trato genérico: se nombra a la persona.
- Disculpa sin información. Decir qué pasó y qué hacer.
- Regla 10: cierre enfático que repite la idea.
- Promesa que el sistema no puede sostener.
- Antítesis «no es X: es Y».
- Usar «colaborador» o el nombre.
- Afirma lo que la puerta tal vez no confirmó. Usar «vigente» con la hora.
- Antítesis de apertura sin la segunda mitad («No es un caso raro.»). Afirmar lo que es.
- «…, ni X, ni Y»: polisíndeton de efecto.
- Tres infinitivos en fila: tríada por inercia. Quedarse con los que importan.
- Anáfora «por eso…, y por eso».
- Repite la negación después de dos puntos para rematar.
- «Real» como énfasis vacío.
- Gerundio de relleno. Presente simple.
- Anáfora «es lo…, y es lo…».
- Antítesis «…, no porque…».
- Frase hecha de remate.
- Antítesis comparativa «es de X más que de Y».
- Antítesis de cierre «X, no el Y.».
- Antítesis «No X; sí Y».
- Anáfora «sigue…, sigue…».
- Negación seguida de dos puntos que revela.

## Antes de entregar

1. Si hay código: solo variables `--kino-*`, ningún hex suelto.
2. Si hay texto: revisar contra la sección de voz; en el repo, `npm run voz -- kino <archivo>`.
3. Si hay combinaciones nuevas de texto y fondo: agregarlas a pares.json y correr `npm run contraste -- kino`.
