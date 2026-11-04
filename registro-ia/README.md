# Registro de uso de IA

Cómo se usó la IA en Kino: qué se pidió, con qué herramienta y en qué PR o issue terminó.

| Qué | Dónde |
|---|---|
| Prompts de Claude Code, guardados por el hook | `AAAA-MM/AAAA-MM-DD-<sesión>.jsonl` |
| Uso de IA en claude.ai, Cowork y Grok | Sección «Uso de IA» de cada PR (no hay forma de capturarlo solo) |
| Quién aceptó que se registren sus prompts | [`consentimiento.md`](consentimiento.md) |

## Cómo se activa en tu equipo

El hook necesita saber quién escribe:

```bash
git config kino.persona alejandro
```

En el proyecto «Kino» de Claude Code (sesiones en la nube), define la variable `KINO_PERSONA=alejandro` en *Project settings → Environment*. El comando de `git config` solo sirve si trabajas con una copia del repositorio en tu computador. Sin eso, el hook no guarda nada.

## Qué se tapa antes de guardar

Teléfonos, correos, cédulas y números largos, placas y llaves de API. Aun así, no pegues secretos en un prompt.
