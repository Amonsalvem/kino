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

En una sesión en la nube, define la variable de entorno `KINO_PERSONA=alejandro` en la configuración del entorno. Sin eso, el hook no guarda nada.

## Qué se tapa antes de guardar

Teléfonos, correos, cédulas y números largos, placas y llaves de API. Aun así, no pegues secretos en un prompt.
