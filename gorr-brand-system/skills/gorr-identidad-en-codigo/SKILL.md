---
name: gorr-identidad-en-codigo
description: Genera y verifica la identidad visual de un cliente de GORR como tokens DTCG 2025.10 (paleta por contraste, escala Utopia, capa semántica por temas, CSS) y migra sistemas heredados. Usar en las fases 3 y 4 del playbook o cuando falle validar o contraste.
---

# GORR · Identidad visual en código

Trabajas sobre `clientes/<id>/` del repo `gorr-brand-system`. La fuente de verdad es `marca.config.json` + `tokens/`; el CSS se genera.

## Color
1. En `marca.config.json → color`, cada familia lleva `h` y `cmax` (OKLCH) o una `semilla` hex, más `significa` y `porque`. Sin `porque`, pregunta qué problema resuelve la familia antes de generarla.
2. `neutros` define superficies por luminosidad (`L`); `fondos` elige el fondo de cada lado (`d` oscuro, `l` claro).
3. `objetivos` son razones WCAG. Cada familia sale con `d<razón×10>` y `l<razón×10>` (ej. `d45` = 4.5:1 sobre el fondo oscuro).
4. Literales que la capa semántica necesita (blanco, negro de sombra, transparente) van en `color.fijos`, nunca escritos en `tokens/tema/`.
5. `npm run paleta -- <id>`. Para contrastar con Adobe Leonardo, usa `reportes/leonardo-entrada.json` en leonardocolor.io. Alternativa rápida: Radix Colors.

## Tipo y espacio
`tipo.min` y `tipo.max` (base y escala), `vwMin` y `vwMax`, `pasos`. Ajusta en utopia.fyi/type/calculator y copia los parámetros. `espacio: {}` activa el espacio fluido con pares «uno arriba». `npm run tipo -- <id>`.

## Capa semántica
- `tokens/tema/<tema>.tokens.json`: solo alias `{primitivo.color.…}`. Un literal ahí es error de `validar`, también dentro de sombras y bordes.
- Nombres por rol (superficie, texto, borde, acento, estado), no por color.
- Temas en `marca.config.json → temas`, con `selector` y `esquema` (light/dark). El primero es el canónico.

## Compuertas
```bash
npm run ciclo -- <id>       # o por partes: validar, construir, contraste
```
- **validar** falla → lee el mensaje: alias roto, tipo que no coincide o literal en la capa semántica. Corrige en la fuente.
- **contraste** falla → no bajes el mínimo de `pares.json`. Cambia el alias semántico a un paso con más contraste (ej. `d32` → `d45`). Un borde que transporta significado tiene que cumplir sobre **toda** superficie donde caiga: agrega el par para cada superficie.
- **APCA bajo Lc 60 en texto de cuerpo**: no bloquea, pero repórtalo al equipo con el par y el valor. Si el texto es corto y en negrita (etiquetas), puede aceptarse; es decisión del equipo, no tuya.

## Migrar un sistema heredado
```bash
npm run importar -- <id> <origen.json> tokens/30-<nombre>.tokens.json --excluir ruta.a,ruta.b
npm run importar -- <id> <tema-origen.json> tokens/tema/<tema>.tokens.json
```
Convierte hex, dimensiones, `clamp()`, sombras en cadena y familias. Los literales de la capa semántica que coincidan con `color.fijos` pasan a alias; si no coinciden, `validar` los reporta: agrégalos a `fijos` o apúntalos a un primitivo. Lo que no tiene forma DTCG queda en `com.gorr.css-crudo` con aviso.

## Uso en piezas
```html
<link rel="stylesheet" href="<id>-tokens.css">
<body data-tema="<tema>">
```
Solo variables `--<prefijo>-*`. Un hex en un deck o documento es un error de revisión.
