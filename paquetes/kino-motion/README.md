# @kino/motion · sistema de motion de Kino

Versión 0.1 (26 sep 2026). Los tokens nuevos están aprobados (decisiones.md, M1). Es la base con la que se van a construir la web y la app: tokens,
un núcleo sin DOM que sirve en cualquier plataforma, un runtime web con componentes y las herramientas para
que el motion no se degrade con el tiempo.

```bash
npm install
npm run verificar      # tokens → build → tipos → 23 pruebas → lint-motion → Lab → 14 pruebas de navegador
npm run lab            # lab/dist/kino-motion-lab.html: el sistema en vivo, con inspector
```

## Por qué está hecho así

El stack de la web y la app no está decidido. Por eso el sistema tiene tres capas y ninguna amarra a un framework:

| Capa | Qué es | Dónde sirve |
|---|---|---|
| Tokens | Duraciones, curvas y verbos de la marca (DTCG) más resortes físicos, coreografía y escalas | Todas: CSS, TS, JSON portable, Figma, Lottie, Blender |
| Núcleo (`src/nucleo`) | Curvas, resortes analíticos, coreografía, máquina de estados del Pase, política de movimiento reducido. Sin DOM ni dependencias | Web, React Native, servidor, generadores de video |
| Runtime web (`src/web`) | `animar()` interrumpible, física de gestos, FLIP, View Transitions, 9 Web Components, inspector | Cualquier web: HTML, React 19, Vue, Svelte, PWA o Capacitor |

Los resortes se definen con **rigidez, amortiguación y masa**: los mismos tres números de Reanimated
(`withSpring`), SwiftUI (`interpolatingSpring`) y Compose (`spring`). Si la app termina siendo nativa, el
movimiento es idéntico. El Lab genera el código para cada plataforma.

## Reglas

1. **Solo se mueve lo que le pasa a un Pase.** Cada animación responde a un cambio real.
2. **El estado no miente.** `estadoDelPase(hechos, ahora, aviso)` deriva el estado de los hechos. La única
   transición que llega a «vigente» es `confirmar` y exige al lector. `<kino-pase>` se niega a mostrar
   «vigente» sin él. Una prueba recorre 20 000 combinaciones de hechos sin confirmación: ninguna da vigente.
3. **Lo que se toca responde a la mano.** Los gestos terminan en un resorte que parte de la velocidad del dedo y
   se puede interrumpir a mitad de camino.
4. **Exacto, sin rebote.** Ningún resorte pasa de 3 % de rebote (ζ ≥ 0,75). La prueba lo verifica.
5. **El tiempo es el real.** La barra de vigencia baja con el reloj. Esperar al lector no tiene spinner: la línea
   llega una vez y el texto cuenta los minutos.
6. **Reducido no es apagado.** Desplazamientos y escalas pasan a fundidos con la misma duración y el mismo orden;
   los latidos se detienen.
7. **Lo que se va no hace esperar.** Salir dura el 60 % de entrar y usa `curva/salir`.
8. **Cascadas con tope.** Máximo 8 elementos escalonados y 520 ms en total; con más, el paso se comprime.
9. **Solo se mueve la pantalla.** En un cambio de vista, la barra y la navegación se quedan quietas
   (`view-transition-name: pantalla`); el Pase tocado viaja porque es el mismo objeto.

## Tokens

- Fuente de marca (no se duplican): `gorr-brand-system/clientes/kino/tokens/40-movimiento.tokens.json` y los
  verbos de `50-semantico-comun.tokens.json`.
- Nuevos y aprobados (M1), en `tokens/motion.tokens.json`: `resorte/{tacto,hoja,pase,firme}`, `curva/salir`,
  `coreografia/{cascada-maximo,cascada-tope,salida-factor}`, `latir/ciclos`, `escala/{presion,entrada}`,
  `profundidad/*`, `aviso/visible`.
- `npm run tokens` genera `src/tokens.generados.ts` (tipado), `dist/kino-motion.css` (tokens de marca +
  `--kino-mov-*`, con los resortes como `linear()`) y `dist/tokens.json` (portable, con frames a 60 fps).

| Resorte | Rigidez · amortiguación · masa | ζ | Se asienta | Rebote | Para |
|---|---|---|---|---|---|
| `tacto` | 520 · 34 · 1 | 0,745 | 396 ms | 2,98 % | Presionar y soltar |
| `hoja` | 260 · 30 · 1 | 0,93 | 479 ms | 0,03 % | Hojas y todo lo que se arrastra |
| `pase` | 180 · 22 · 1 | 0,82 | 689 ms | 1,11 % | Un Pase que cambia de lugar |
| `firme` | 400 · 40 · 1 | 1 | 494 ms | 0 % | Números y datos |

## Núcleo

```ts
import {estadoDelPase, transicion, reducirPistas, escalonar, lineaDeTiempo, resolver, resorteDe, ms, frames} from '@kino/motion/nucleo';

estadoDelPase({desde, hasta, enviadoAlLector, confirmacion}, new Date(), 30 * 60_000); // 'sin-confirmar'
transicion('sin-confirmar', 'confirmar');  // partitura: verbo, duración, curva, pistas por parte, qué deja
transicion('previsto', 'confirmar');       // lanza TransicionInvalida
escalonar(12);                             // retrasos con máximo y tope
resolver(resorteDe('hoja'), velocidadDelDedo).avance(t);
frames('aparecer/duracion');               // 49, para Lottie, Remotion o Blender
```

La **partitura** de cada transición (`TRANSICIONES` en `src/nucleo/pase.ts`) dice qué parte del Pase se mueve
(tarjeta, borde, chip, barra, corte, tachado, nota), qué propiedad, de qué valor a cuál, con qué verbo y qué deja
en pantalla como prueba. La web la interpreta en `<kino-pase>`; una app nativa, un generador de Lottie o una
escena de Blender pueden leer la misma partitura.

## Runtime web

```ts
import '@kino/motion';                 // registra los componentes
import {animar, animarResorte, arrastrar, flip, quitar, transicionDeVista, montarInspector} from '@kino/motion';

animar(el, [{opacity: 0}, {opacity: 1}], {duracion: 'aparecer/duracion', curva: 'aparecer/curva', canal: 'entrada'});
animar(boton, [{transform: 'scale(.97)'}], {resorte: 'tacto', canal: 'presion', desdeActual: true});
transicionDeVista(() => mostrarDetalle(id), 'adelante');
```

- `animar()` solo acepta nombres de tokens. Con `canal`, una animación nueva interrumpe a la anterior desde donde iba.
  Respeta el modo reducido y deja el valor final como estilo (no acumula `fill`).
- `animarResorte()` y `arrastrar()`: física de gestos con velocidad medida y resistencia elástica.
- `flip()`, `quitar()`, `entrar()`: listas que se reacomodan sin saltos.
- Modo reducido: la preferencia del sistema, o `data-movimiento="reducido|completo"` en `<html>`.

### Componentes

| Etiqueta | Qué hace |
|---|---|
| `<kino-pase>` | La tarjeta del Pase. Interpreta la partitura de cada transición; `pase.aplicar('confirmar', {lector})`. Honesto por construcción |
| `<kino-estado>` | Chip de estado. El punto late `latir/ciclos` veces al quedar vigente y se detiene |
| `<kino-vigencia>` | Barra de vigencia con la hora real; emite `vigencia-agotada` |
| `<kino-lista>` | Cascada de entrada; `insertar()`, `quitar()` y `ordenar()` con FLIP |
| `<kino-accion>` | Botón con resorte al presionar |
| `<kino-hoja>` | Hoja inferior que se arrastra y se lanza; Escape y foco |
| `<kino-aviso>` | Avisos con `aria-live` |
| `<kino-espera-lector>` | La espera honesta del lector |
| `<kino-numero>` | Números con resorte firme y cifras tabulares |

En React 19 los Web Components funcionan directo (`<kino-pase estado="vigente" …/>`). Los colores salen de las
variables de marca (`--kino-estado-*`, `--kino-superficie-*`), así que siguen el tema de la página.

## Herramientas

| Herramienta | Para qué |
|---|---|
| Lab (`npm run lab`) | Ver y probar todo: estados del Pase con su partitura, listas, gestos, pantallas, laboratorio de resortes con código para cada plataforma, coreografía, tabla de tokens |
| Inspector (`montarInspector()`) | En cualquier página: cámara lenta 0,1× y 0,25×, modo reducido, resaltado de lo que se mueve y registro de cada animación con sus tokens |
| `lint-motion` | Falla si alguien escribe una duración, una curva o un easing genérico a mano. Excepción explícita: `// motion-ok: <razón>` |
| `probar-lab` | 14 pruebas en navegador: estado honesto, reducido, pantallas, sin desborde en 390 px y sin errores |

## Lo que falta decidir

- El stack de la web y la app. Para React Native ya está el adaptador con Reanimated en `paquetes/kino-motion-nativo`
  (misma partitura, mismos resortes, mismo estado honesto).
- La ventana de aviso («por vencer») es un parámetro. La fija la administración de cada conjunto.
- Los tokens nuevos están aprobados (M1), pero todavía viven en el paquete. Falta llevarlos a los DTCG de
  `gorr-brand-system/clientes/kino/tokens` y a la colección Movimiento de Figma.
