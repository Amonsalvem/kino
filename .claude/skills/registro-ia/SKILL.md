---
name: registro-ia
description: Deja constancia de cómo se usó la IA en cada PR o issue de Kino y mejora la forma en que cada persona trabaja con ella. Úsala al abrir o actualizar un PR o un issue, al terminar una sesión de trabajo, o cuando pidan «registra el uso de IA», «qué prompts se usaron» o «revisa cómo pedí esto».
---

# Registro de uso de IA

Tres trabajos: declarar el uso de IA en el PR, dejar una nota concreta para pedir mejor la próxima vez y mantener al día el perfil de la persona.

## 1. Sección «Uso de IA» del PR

Todo PR la llena; GitHub bloquea el PR si está vacía. Formato:

```markdown
## Uso de IA

| Campo | Valor |
|---|---|
| Herramienta y modelo | Claude Code, Opus 5.5 |
| Pidió | alejandro |
| Sesión | enlace de la sesión, si existe |
| Prompts | `registro-ia/2026-11/2026-11-04-<sesión>.jsonl`, o el resumen de cada pedido si no hay registro |
| Qué hizo la IA | Lo que escribió o cambió |
| Qué hizo la persona | Lo que decidió, corrigió o aprobó |

**Nota de práctica:** una sola mejora para el próximo pedido.
```

- **Claude Code:** el hook ya guardó los prompts en `registro-ia/`. Súbelos en el mismo PR.
- **claude.ai, Cowork y Grok:** no se capturan solos. Resume cada pedido en una línea, con las palabras de la persona cuando importen.
- **Sin consentimiento** (`registro-ia/consentimiento.md`): no copies sus prompts. Escribe solo la herramienta y qué hizo la IA.

## 2. Nota de práctica

Lee los prompts de la sesión y elige **el problema que más costó**, no una lista. Ejemplos de lo que se busca:

| Problema | Señal en el prompt | Nota |
|---|---|---|
| Falta referencia | Pidió un resultado sin decir contra qué compararlo | «La próxima vez, enlaza el frame de Figma o el archivo que sirve de modelo» |
| Ambigüedad | La IA tuvo que preguntar o rehacer | Cita la frase ambigua y propón la versión clara |
| Tarea mezclada | Un prompt con tres trabajos distintos | Sugiere partirlo en issues |
| Sin criterio de terminado | No se sabía cuándo estaba listo | Sugiere decir cómo se verifica |

Si la sesión no tuvo problemas, escribe «Sin nota». No inventes una.

## 3. Perfil de la persona

El perfil está en `personas/<nombre>.md`. Léelo al empezar y aplícalo.

- Agrega una corrección solo si la persona la dijo o si se repitió en **dos PR**. Cita los dos.
- No agregues datos personales, de salud ni de dinero, ni opiniones sobre la persona.
- El cambio al perfil va en el PR, y Alejandro lo aprueba.

## Lo que esta skill no puede hacer

No entra en la cuenta de IA de nadie ni cambia su configuración. Todo lo que mejora el trabajo vive en el repositorio y llega a cada IA porque lo lee aquí.
