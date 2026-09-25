# Figma · librería «Kino · Sistema de marca»

Archivo `BO7UnDO9iE0aG6yUpNj0bc` (https://www.figma.com/design/BO7UnDO9iE0aG6yUpNj0bc), en la cuenta de Alejandro. Figma no se edita a mano: los valores salen de los tokens DTCG y se sincronizan con estos scripts.

## Cómo se sincroniza

1. `python3 espec.py`: lee los tokens DTCG de `gorr-brand-system/clientes/kino/tokens/` y escribe `espec.json` (271 variables, cinco colecciones).
2. `python3 sincronizar.py`: escribe un `sync-<colección>.js` por colección. Cada uno se corre con `use_figma`, en este orden: primitivos, espacio, movimiento, tipografía, color. Crea lo que falta y actualiza valores y alias. No borra variables.
3. `js/preludio.js` define las ayudas que ligan relleno, trazo, radio, espacio y estilo de texto a una variable. Los scripts `js/p3a-*.js` y `js/p3b-*.js` construyen los componentes; `js/_run.js` es el último que se corrió (preludio más la parte que tocaba).
4. Reglas de `use_figma`: una página por llamada, llamadas en serie, fuentes cargadas antes de escribir texto.

## Cómo se verifica

1. Correr `js/p4-auditoria-y-exportacion.js` con `use_figma`. La salida pasa de 20 kB, así que se pide en dos mitades y se guardan como `export-parte-1.json` y `export-parte-2.json`. Los estilos de efecto van en `export-efectos.json`.
2. `python3 exportar_variables.py export-parte-1.json export-parte-2.json export-efectos.json` escribe `variables-figma.json` y compara con DTCG:
   - el color en los dos modos;
   - los números (el tamaño de texto en 360 px contra el mínimo del `clamp()` y en 1440 px contra el máximo);
   - las cadenas;
   - las sombras.
3. `python3 ../verificacion/fase5.py ../figma/variables-figma.json`: comprobaciones 6 y 7.

Resultado del 25 sep 2026 (después de la revisión de la Parada 4): 271 variables (con `texto/enlace`) y 3 estilos de efecto por tema; 0 tokens sin variable; 0 valores distintos; 0 pinturas sin variable en 14 páginas.

## Auto-layout y espaciado (revisión de la Parada 4)

Nico no aprobó la librería por el auto-layout y el espaciado. Se auditó y corrigió página por página:

| Qué | Antes | Después |
|---|---|---|
| Textos de ancho fijo dentro del auto-layout | 111 | 0: llenan su contenedor, con ancho máximo igual al anterior para no perder la medida de lectura |
| Filas de tarjetas con alto desigual | 6, más la fila de capas de Elevación | 0: la más alta abraza su contenido y las demás llenan ese alto |
| Espacios y paddings sin variable | 38 (Léeme con 80 de padding y 1200 de ancho; Portal con 102,4 y 51,2) | 0: todos ligados a un paso de la escala |
| Hijos que se salen de su contenedor | botón de «Lista de Pases», fila de retículas, chips del registro, texto de elevación | 0 |
| Separación entre marcos del lienzo | 40, 60, 80, 100 | 72 en todas las páginas |

Además, las pantallas de teléfono tienen alto automático con mínimo de 780, los vectores de los íconos escalan con su instancia, y el tejido celular tiene su superficie y su radio.

Scripts: `js/p5-auditoria-layout.js` y `js/p5-auditoria-tamanos.js` (diagnóstico), `js/p5-normalizar.js` (corrección, se puede volver a correr), `js/p5-verificar-layout.js` (verificación). Se corren con `use_figma`, una llamada por página, reemplazando `__PAGINA__` por el id de la página.

Las sombras (`--kino-relieve-membrana`, `--kino-resplandor-vigente`, `--kino-resplandor-identidad`) son estilos de efecto porque Figma no guarda sombras en variables. Sus colores sí van ligados a Primitivos.

## Pantallas con la jerarquía del Pase (1.2.0, propuesta F4-P5)

Nico aprobó la librería y pidió que las pantallas tomen la jerarquía de las piezas del Pase. Cada pantalla se armó con auto-layout y variables:

| Nivel | En Figma |
|---|---|
| 1 · Manda | Archivo ExtraBold ligado a `texto/2` (nombre, título) |
| 2 · Vigencia | JetBrains Mono con el color `estado/<estado>/texto` |
| 3 · Rótulo | JetBrains Mono Medium 12, mayúsculas, 8 % de tracking, `texto/secundario` |
| 4 · Grupo | Marco en `superficie/elevada`, radio `forma/radio/tarjeta`, borde `borde/tenue` |
| 5 · Acción | Instancia de Botón de acción solo en Crear Pase; Botón secundario en Extender, Entrar y Guardar límites |

- Componente nuevo **Pase en lista** (4 estados, propiedades de texto Tipo, Nombre y Vigencia). La barra de vida llena el ancho y escala.
- Las pantallas de teléfono usan el modo 360 px de Tipografía; Límites, el de 1440 px. Alto automático con mínimo de 780.
- La aurora (clon de la de la página Imagen) está solo en la cabecera de la Lista, que es la pantalla de inicio.
- Verificación (`js/p5-verificar-layout.js`) en Pantallas y Componentes: 0 marcos sin auto-layout, 0 espacios sin variable, 0 desbordes, 0 filas desiguales, 0 solapes. 0 pinturas sin variable en las cinco pantallas nuevas.

## Páginas

| Página | Qué tiene |
|---|---|
| Léeme | Cómo se usa, índice y estado de la versión |
| Plataforma | Problema, alternativas, posicionamiento, promesa, personalidad, valores, nombres y manifiesto |
| Voz y UX writing | Tono por contexto, vocabulario, textos de la app |
| Logo | Construcción, versiones, fondos, usos incorrectos |
| Color | Primitivos, roles por tema, los nueve estados |
| Tipografía | Estilos de texto ligados a variables, reglas para placas y códigos |
| Iconografía | 37 íconos en retícula de 24, trazo 1,7 |
| Imagen | Aurora, células, fondos |
| Estructura | Retículas, espaciado, radios, elevación, quiebres |
| Motion (specs) | Duraciones, curvas y coreografías |
| Componentes | Guía; componentes Icono/*, Logo/*; sets Botón de acción, Botón secundario, Campo, Selector de tipo, Estado (con ícono en Usado, Vencido y Revocado), Tarjeta de Pase y Pase en lista (1.2.0) |
| Pantallas | Lista de Pases (inicio), Crear Pase, Detalle, Acceso por código y Límites con la jerarquía del Pase (1.2.0, propuesta). Las de la 1.1.0 quedan en la sección «Pantallas 1.1.0» de la misma página |
| Aplicaciones / Plantillas | Seis plantillas para duplicar |
| Registro de cambios | Versiones 0.0 a 1.2.0 |
| Referencias | La librería anterior, sin cambios |
