# Guía para agentes

Reglas comunes para toda IA que trabaje en Kino: Claude (Code, claude.ai, Cowork) y Grok (Grok Build). Es la fuente única. `CLAUDE.md` la importa y solo agrega lo propio de Claude.

## 1. Quién decide

| Persona | Papel |
|---|---|
| Alejandro | Aprueba todo, desde el chat del proyecto Kino de Claude (D-008) o comentando el PR en GitHub |
| Nico | Propone, con un issue o un PR |
| IA | Propone y ejecuta. Nunca aprueba. Integra a `main` solo con la orden «integra #N» de Alejandro en el chat (D-008) |

**Lo que la IA hace sin pedir permiso**, siempre en un PR con la etiqueta `menor`: orden de archivos, correcciones de texto, enlaces rotos y cambios de código que no alteran el comportamiento. Todo lo demás espera la aprobación de Alejandro.

## 2. Antes de trabajar

1. Lee [`kino/canon/proyecto.md`](kino/canon/proyecto.md) y [`kino/canon/decisiones.md`](kino/canon/decisiones.md).
2. Lee el perfil de quien te pide el trabajo en [`personas/`](personas/) y aplícalo.
3. Revisa los PR en borrador abiertos. Si alguno toca las mismas carpetas que vas a tocar, avisa antes de empezar.

## 3. Qué manda sobre qué

1. Lo que Alejandro dice en la sesión. Si es una regla de alcance general, regístrala en `decisiones.md` antes de terminar, o se pierde.
2. `kino/canon/decisiones.md`, entradas APROBADAS.
3. `kino/canon/proyecto.md`.
4. Evidencia: `pre-kino/inspeccion/` (observado) > entrevistas del 2 sep > documentos académicos.
5. El resto de `pre-kino/`: contexto, nunca una decisión vigente.

## 4. Dónde va cada cosa

| Trabajo | Carpeta |
|---|---|
| Hechos, decisiones, vocabulario | `kino/canon/` |
| Evidencia nueva | `kino/investigacion/` |
| Identidad de marca (la fuente es Figma) | `kino/marca/` |
| Flujos, reglas de negocio, pantallas | `kino/producto/` |
| Apps y paquetes | `kino/codigo/` |
| Entregas académicas | `eafit/` |
| Scripts sin marca | `herramientas/` |
| Perfiles de trabajo de cada persona | `personas/` |
| Registro de prompts y consentimiento | `registro-ia/` |

Si lo que vas a crear no encaja en ninguna, pregunta antes de inventar una carpeta.

## 5. Reglas de trabajo

1. **Una rama y un PR en borrador por tarea.** Nunca se escribe directo en `main`.
2. **Las tareas viven en GitHub Issues.** El trabajo en curso son los PR en borrador.
3. **Pre-kino es de solo lectura.** Se lee y se cita con su ruta completa.
4. **Cada afirmación lleva fuente.** Cita el archivo. Si el dato no está en el repositorio, dilo. Las cifras de mercado van con fuente web y fecha.
5. **Nada de generalidades ni relleno.** Conclusión primero. No repitas lo que ya está escrito en otro archivo: enlázalo.
6. **Muletillas.** Todo texto pasa por la skill `corrector-muletillas` antes de subirse. GitHub corre `herramientas/revisar-texto.py` en cada PR, sobre los archivos que cambian y el cuerpo del PR, y bloquea lo que tenga errores.
7. **Uso de IA declarado.** Todo PR llena la sección «Uso de IA» de la plantilla (skill `registro-ia`). GitHub bloquea el PR si falta.
8. **Vocabulario.** «Pase» (de la visita o el colaborador) no se mezcla con «cuenta» (del residente). Nunca «permiso». «Visita», no «invitado».
9. **Español** en archivos, commits, PR y texto visible.
10. **Secretos fuera.** Nada de llaves, contraseñas, cédulas, teléfonos ni placas reales.

## 6. Skills

Viven en `.claude/skills/`. Si tu herramienta no las carga sola, abre el `SKILL.md` y síguelo como instrucciones.

| Skill | Cuándo |
|---|---|
| `corrector-muletillas` | Antes de subir cualquier texto |
| `registro-ia` | Al abrir o actualizar un PR o un issue |
| `mentor` | En toda sesión con Alejandro |

Las skills de pre-kino (`pre-kino/skills/`) y el plugin arcana son registro histórico. No se usan.

## 7. Agentes en GitHub

| Agente | Cuándo corre | Qué hace | Guía |
|---|---|---|---|
| Curador de agentes y skills (D-013) | Cada lunes, 6 a. m. en Colombia, o a mano | Revisa skills, agentes y hooks contra lo que Kino necesita y el estado del arte en IA. Abre un PR en borrador con cambios e informe. Nunca integra | [`herramientas/curador/README.md`](herramientas/curador/README.md) |

Una skill o un agente nuevo puede venir del curador. Se revisa como cualquier PR.
