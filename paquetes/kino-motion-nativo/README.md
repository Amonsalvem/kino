# @kino/motion-nativo · adaptador para React Native

Versión 0.1 (26 sep 2026). Usa los tokens de motion aprobados (decisiones.md, M1). Lleva el sistema de motion de Kino (`paquetes/kino-motion`) a React Native
con **Reanimated 3** y **Gesture Handler 2**. Usa el mismo núcleo que la web: los mismos tokens, los mismos
resortes físicos, la misma partitura de cada transición del Pase y la misma regla de estado honesto.

```bash
npm install --legacy-peer-deps
npm run verificar     # tipos → 9 pruebas → arnés web → 9 pruebas en navegador
```

## En la app

```bash
npx expo install react-native-reanimated react-native-gesture-handler
```

- `babel.config.js`: `plugins: ['react-native-reanimated/plugin']` (último de la lista).
- Raíz: `<GestureHandlerRootView style={{flex: 1}}>` y `<FuentesKino fuentes={{titulo: 'Archivo-Bold', texto: 'Archivo-Regular', dato: 'JetBrainsMono-Regular'}}>`
  con las fuentes cargadas (por ejemplo, con `expo-font` desde `branding/sistema/fonts`).
- Importa del paquete (en este repositorio, `paquetes/kino-motion-nativo/src`). El núcleo viene de
  `paquetes/kino-motion/src/nucleo`, sin DOM.

```tsx
<PaseKino quien="Andrés Gómez" casa="Casa 14" desde={desde} hasta={hasta}
          estado={estado} enviado={enviado} evidencia={confirmacion} revocacion={revocacion} />
```

Cambia `estado` y el Pase ejecuta la partitura de esa transición (confirmar cierra el borde, muestra la
evidencia y hace latir el punto; revocar cruza la línea…). Si pides `vigente` sin `evidencia`, se muestra
`sin confirmar` y avisa en desarrollo. El estado se puede derivar de los hechos con `estadoDelPase()` del núcleo.

## Qué trae

| Pieza | Qué hace |
|---|---|
| `tiempo(duracion, curva)`, `tiempoMs()`, `resorte(nombre, velocidad)` | Tokens → `WithTimingConfig` y `WithSpringConfig`. Los resortes usan rigidez, amortiguación y masa: el mismo movimiento que en la web |
| `planDeTransicion()`, `valoresDeEstado()`, `estadoHonesto()` | La partitura del núcleo traducida a valores animables (puro, probado en Node) |
| `usePaseMotion()` | Estilos animados de cada parte del Pase: tarjeta, bordes, chip, punto y brillo, barra, nota, corte y tachado |
| `useVigencia()` | Vigencia con la hora real (en reducido, una actualización por minuto) |
| `usePresion()` | Presionar con `resorte/tacto` y color en `duracion/instante` |
| `useHoja()` | Hoja con gesto: resistencia elástica, proyección de la velocidad y cierre que continúa el lanzamiento |
| `useEntrada()`, `<EntraKino>` | «aparecer» exacto en iOS, Android y web; `useCascada(n)` para los retrasos |
| `entradaKino`, `salidaKino`, `disposicionKino` | Animaciones de disposición de Reanimated (entrar, salir y reacomodar con `resorte/pase`). Solo en iOS y Android |
| `useNumeroAnimado()`, `<NumeroKino>` | Números con `resorte/firme` y formato es-CO, en el hilo de UI |
| `<PaseKino>`, `<EstadoKino>`, `<BotonKino>`, `<HojaKino>`, `<EsperaLectorKino>` | Componentes de referencia con los tokens de marca y el tema del sistema |

## Movimiento reducido

Se lee de `useReducedMotion()` (iOS «Reducir movimiento», Android «Quitar animaciones»). Kino no salta al final:
desplazamientos y escalas pasan a fundidos con la misma duración, los latidos se detienen y la hoja aparece por
fundido. Por eso las configuraciones pasan `reduceMotion: ReduceMotion.Never`: la política la aplica el adaptador.

## Verificación (26 sep)

- `tsc` sin errores contra React Native 0.76, Reanimated 3.16 y Gesture Handler 2.20.
- 9 pruebas: el plan de cada transición coincide con el estado final; en reducido nada se desplaza; los worklets
  de gestos dan lo mismo que el núcleo; formato de cifras.
- Arnés web (react-native-web + Vite, `web/`): 9 pruebas en Chromium. Recorre previsto → sin confirmar →
  vigente → revocado, comprueba el estado honesto y que la hoja se abre y se cierra lanzándola con el puntero.
- `lint-motion`: 0 hallazgos.

## Límites conocidos

- **No se ha corrido en un dispositivo iOS ni Android.** Los tipos y el arnés web pasan, pero falta probarlo en
  un simulador o dispositivo (Expo Go o una build de desarrollo).
- **Reanimated en web** solo acepta curvas con nombre en sus animaciones de disposición, y fija en posición
  absoluta lo que entra con un `Keyframe` propio. Por eso `entradaKino`, `salidaKino` y `disposicionKino`
  devuelven `undefined` en web. Para la web del producto está `@kino/motion` (Web Components), que es exacto.
- El arnés web necesita un plugin de Vite para el puente de Reanimated con react-native-web
  (`web/vite.config.mjs`). Metro y Expo no lo necesitan.
