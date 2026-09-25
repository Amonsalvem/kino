# Figma · librería «Kino · Sistema de marca»

Archivo `BO7UnDO9iE0aG6yUpNj0bc` (https://www.figma.com/design/BO7UnDO9iE0aG6yUpNj0bc), en la cuenta de Alejandro. Figma no se edita a mano: los valores salen de los tokens DTCG y se sincronizan con estos scripts.

## Cómo se sincroniza

1. `python3 espec.py`: lee los tokens DTCG de `gorr-brand-system/clientes/kino/tokens/` y escribe `espec.json` (270 variables, cinco colecciones).
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

Resultado del 25 sep 2026: 270 variables y 3 estilos de efecto por tema; 0 tokens sin variable; 0 valores distintos; 0 pinturas sin variable en 14 páginas.

Las sombras (`--kino-relieve-membrana`, `--kino-resplandor-vigente`, `--kino-resplandor-identidad`) son estilos de efecto porque Figma no guarda sombras en variables. Sus colores sí van ligados a Primitivos.

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
| Componentes | Guía; componentes Icono/*, Logo/*; sets Botón de acción, Botón secundario, Campo, Selector de tipo, Estado, Tarjeta de Pase |
| Pantallas | Crear Pase, lista, detalle, límites, acceso por código |
| Aplicaciones / Plantillas | Seis plantillas para duplicar |
| Registro de cambios | Versiones 0.0 a 1.0.0 |
| Referencias | La librería anterior, sin cambios |
