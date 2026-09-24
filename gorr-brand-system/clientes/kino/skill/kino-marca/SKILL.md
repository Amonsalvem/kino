---
name: kino-marca
description: Aplica la marca Kino (color, tipografía, voz y vocabulario) a cualquier pieza: deck, documento, página HTML, interfaz o texto de producto. Usar al producir o revisar cualquier entregable de Kino.
---

# Marca Kino

> Generado por gorr-brand-system desde las fuentes del cliente. No editar a mano: cambiar marca.config.json, voz.json o tokens/ y correr `npm run ciclo -- kino`.

## Reglas que no se negocian

1. El color solo nombra hechos confirmados. Si el lector no confirmó, el estado es sin-confirmar: sin relleno y con borde discontinuo.
2. Todo estado lleva palabra además de color.
3. El acento es acción, no estado: va en lo que otorga un pase (el botón, el nodo «Otorgar» de un flujo) y en nada más.
4. Kino es la marca. El conjunto aparece como dato (texto o chip), nunca con logo ni colores propios.
5. Toda afirmación lleva su grado de evidencia (observado, prueba, entorno, inferido) y su fuente.
6. Placas, códigos, horas, rótulos y cifras van en JetBrains Mono, con cero barrado y cifras tabulares.
7. El tema oscuro es el canónico; el claro («Laboratorio») es el segundo.
8. Sin candados, escudos ni muros: Kino es una membrana.
9. Lo que se mueve significa algo: crecer es aparecer, decaer es caducar, latir es estar vivo. Nada se anima para decorar.

## Color

Cada familia significa algo. No usar una familia fuera de su significado.

| Familia | Significa | Por qué existe |
|---|---|---|
| `sustrato` | Superficies | Linaje: carbón #2C2D2F de la Propuesta 1 con sesgo verde (medio de cultivo). |
| `hueso` | Texto y tema claro | Linaje: hueso #E1E8EE enfriado hacia el verde. |
| `biolum` | Vigente y la acción de otorgar | H1/H5: no existe permiso temporal; el estado vigente tiene que verse vivo. |
| `ambar` | Vigencia que se agota | H1/H5: la vigencia no existe hoy; por-vencer la hace visible. |
| `carmin` | Rechazo | Estado negado distinguible del vencido. |
| `violeta` | Dato personal o biométrico | R4 y Res. 52185 de 2025 de la SIC: el dato de identidad se marca. |
| `indigo` | Profundidad y enlaces | Linaje: índigo #00177D de la Propuesta 1. |

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
| `--kino-borde-definido` | `#517064` |
| `--kino-borde-foco` | `#00BB83` |
| `--kino-texto-primario` | `#EFFCF7` |
| `--kino-texto-secundario` | `#BECBC6` |
| `--kino-texto-tenue` | `#86A799` |
| `--kino-texto-inverso` | `#00140C` |
| `--kino-texto-sobre-acento` | `#00140C` |
| `--kino-acento-base` | `#00BB83` |
| `--kino-acento-fuerte` | `#00EAA5` |
| `--kino-acento-sordo` | `#00422C` |
| `--kino-estado-vigente-fondo` | `#00422C` |
| `--kino-estado-vigente-borde` | `#007953` |
| `--kino-estado-vigente-texto` | `#00EAA5` |
| `--kino-estado-por-vencer-fondo` | `#503300` |
| `--kino-estado-por-vencer-borde` | `#906000` |
| `--kino-estado-por-vencer-texto` | `#FFC36D` |
| `--kino-estado-vencido-fondo` | `#0B2A20` |
| `--kino-estado-vencido-borde` | `#517064` |
| `--kino-estado-vencido-texto` | `#A0C3B4` |
| `--kino-estado-negado-fondo` | `#79000F` |
| `--kino-estado-negado-borde` | `#C33435` |
| `--kino-estado-negado-texto` | `#FFBEB8` |
| `--kino-estado-sin-confirmar-fondo` | `oklch(0 0 0 / 0)` |
| `--kino-estado-sin-confirmar-borde` | `#517064` |
| `--kino-estado-sin-confirmar-texto` | `#BECBC6` |
| `--kino-estado-identidad-fondo` | `#3E1C96` |
| `--kino-estado-identidad-borde` | `#6A56D0` |
| `--kino-estado-identidad-texto` | `#CAC9FF` |

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
| serio ↔ divertido | 1 | Se trata de quién entra a la casa de alguien. Sin chistes en estados, errores ni permisos. |
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
| permiso | pase | Desde el 23 sep el objeto se llama «pase». «Permiso» solo como explicación («un pase es un permiso de ingreso con…»). |
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
- El residente otorga el pase a sus invitados y colaboradores; la administración no aprueba cada ingreso.
- La administración fija los límites: cupos, duración y franjas horarias.
- El invitado no necesita cuenta: entra con QR, placa o un código de un solo uso.
- Todo pase tiene vigencia: desde y hasta una fecha y hora.
- El ingreso lo permite el lector de la puerta (placa, QR o rostro), no el vigilante.
- El residente entra a la app con un código por WhatsApp, sin contraseña.
- Un pase está en uno de estos estados: vigente, por vencer, vencido, negado o sin confirmar.

**No confirmado (no se afirma):**
- Avisos automáticos cuando el lector confirma una placa.
- Un historial o registro de permisos visible para la administración.
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

## Antes de entregar

1. Si hay código: solo variables `--kino-*`, ningún hex suelto.
2. Si hay texto: revisar contra la sección de voz; en el repo, `npm run voz -- kino <archivo>`.
3. Si hay combinaciones nuevas de texto y fondo: agregarlas a pares.json y correr `npm run contraste -- kino`.
