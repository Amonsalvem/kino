# Incongruencias entre las dos carpetas — 21 de septiembre de 2026

Revisión de `montesereno/projects/kino` y `u/decimo_semestre/enfasis` contra los hechos vigentes de la inspección de septiembre. Conclusión primero, luego la evidencia, luego lo que queda abierto.

---

## Conclusión

Hay **una sola incompatibilidad de fondo**, y todo lo demás son sus réplicas: los documentos escritos antes del 16 de septiembre sostienen que *el Super Administrador aprueba cada ingreso a mano*, y la inspección mostró que no aprueba ninguno. Esa premisa es el cimiento del brief, de las tres guías del curso y del relato de las entregas de agosto.

El caso más delicado no es que se repita, sino que **la Guía de consolidación la atribuye a «inspección directa, sep. 2026»**: cita como fuente el documento que dice lo contrario. Si alguien del lado del cliente conoce el sistema, esa línea es rebatible en un segundo.

Y una segunda capa, interna al proyecto de Claude: el `reporte-inspeccion-por-rol.md` del 21 de septiembre trae una errata que contradice tanto al diagnóstico como a las instrucciones del proyecto, y estaba marcada como «pendiente de edición» sin aplicar.

---

## 1. La premisa refutada, y dónde vive

| Documento | Fecha | Qué afirma | Estado |
|---|---|---|---|
| `enfasis/CLAUDE.md` | ago | Proyecto «Arcana»; vigilante «telefonista»; residente atado al teléfono; arquetipos Valeria/Carlos como canon-lock; plugin `arcana` obligatorio | **Reescrito**. La versión anterior quedó como `CLAUDE.anterior-arcana.md` |
| `servicios.../entregas/Brief Kino.docx` | 4 sep | «El conjunto depende de que una sola persona, el Super Administrador, apruebe a mano cada ingreso» (39 menciones de aprobación) | Conservado: entrega presentada |
| `.../Kino_Guia_cliente_entorno.docx` | 16 sep | «El Super Admin aprueba cada ingreso; el vigilante solo supervisa» | Conservado: entrega presentada |
| `.../Kino_Guia_consolidacion_diagnostico_pregunta_guia.docx` | 16 sep | Lo mismo, **atribuido a «inspección directa, sep. 2026»** | Conservado: entrega presentada |
| `.../Kino_Guia_experiencia_deseada.docx` | 16 sep | Lo mismo, como hallazgo H1, con fuente «Inspección de la app» | Conservado: entrega presentada |
| `ixd/Entregas/Kino_IxD_E1_Documento_Conceptual_FORMATO.docx` | 24 ago | Vigilante que valida a mano cada ingreso sin placa | Conservado: entrega presentada |
| `ixd/Entregas/Kino_Documento_Integrador_Biblia_E1_1.docx` | 24 ago | Arquetipos Valeria/Carlos; misma premisa | Conservado: entrega presentada |
| `ixd/Arcana.docx` | ago | Documento de arranque: nombre Arcana, telefonista, Valeria/Carlos, cifras 8.800 y 1.080 | Conservado: origen del encargo |

**Por qué no se borraron las entregas.** Son el registro de lo que se presentó y lo que se calificó; borrarlas no corrige nada y pierde la trazabilidad de la propia evolución del diagnóstico. Lo que hacía falta era que nadie las reutilizara como fuente por error, y eso ya está resuelto: la nueva `enfasis/CLAUDE.md` §5 las lista una por una con su advertencia.

**Ninguna de ellas menciona** los 711 errores, los 312 usuarios de Refugio ni los 893 del sistema. No es que estén desactualizadas en un detalle: no incorporan la inspección en absoluto.

---

## 2. Las siete incompatibilidades de `enfasis/CLAUDE.md`

Era el archivo más peligroso porque es un archivo de instrucciones: manda comportamiento, no solo describe.

1. **Nombre.** «Proyecto Arcana», con canon-lock sobre el nombre. El proyecto es Kino.
2. **Marca.** Canon-lock navy `#1B2F4E` + Inter. La marca Kino vive en `kino/branding/sistema/` con otra paleta y otras tipografías.
3. **Premisa del servicio.** Modelo «reactivo»: residente atado al teléfono, vigilante telefonista. La inspección mostró que nadie autoriza en el momento: el lector decide contra una lista precargada.
4. **Arquetipos.** Valeria Gómez y Carlos Ramírez fijados como canon-lock. Vienen del trabajo 2026-1 de otro equipo, no tienen respaldo en la evidencia de esta fase, y ponen al vigilante como usuario primario cuando el reparto real de autoridad es otro.
5. **Contradicción interna.** §2 dice «el equipo cursa solo dos materias»; §3 habla de «las 4 materias del énfasis».
6. **Herramientas inexistentes.** Ordena usar un plugin `arcana` y una carpeta `canon/` que no están en ninguna de las dos carpetas conectadas.
7. **Argumento derogado.** Presenta la autonomía del residente como el diferenciador, que es justo lo que la regla 5 del proyecto prohíbe repetir (Neivor ya la ofrece).

Además arrastraba las cifras «8.800 copropiedades del Valle de Aburrá» y «1.080 copropiedades», que el propio archivo marcaba como derogadas en §6 y seguía usando en §1.

---

## 3. La errata interna del proyecto, ahora aplicada

`claude/reporte-inspeccion-por-rol.md` (21 sep) corrigió una afirmación que estaba en tres lugares: existe `/super-admin/sso-registration-requests`, una cola de aprobación anidada bajo *Users*, con 4 solicitudes aprobadas, una de ellas con rol `Visitor`.

Estaba marcada como «pendiente de edición» y sin aplicar. Ya se aplicó en:

- `diagnostico-inspeccion.md` §1 y §6 (proyecto y copia local).
- `claude/diagnostico-consolidado-v1.md` §1 fila 1, H2, H5, §3 y §5.
- La nueva `enfasis/CLAUDE.md` §2.

**Queda pendiente para el equipo:** la línea de `<hechos_vigentes>` en las instrucciones del proyecto que dice «no existe bandeja ni cola de aprobación». La redacción precisa es: *no existe cola de aprobación de ingresos; sí existe una de registro de cuentas en el panel de super administrador.*

El hallazgo de fondo no cambia — lo que se aprueba es una cuenta, y el resultado sigue siendo vinculación permanente sin vigencia — pero sí cambia una decisión tomada: «el registro no lo aprueba el administrador, se valida contra la cédula» pasa de *construir lo que falta* a *reemplazar un paso humano que hoy existe*.

---

## 4. Duplicados y obsoletos eliminados

| Qué | Por qué |
|---|---|
| `kino/branding/sistema/_obsoleto/kino-tokens.json` | Duplicado byte a byte de `motor/semantica.json` |
| `kino/branding/sistema/_obsoleto/Kino_Deck_diagnostico.antes.html` | Versión anterior del deck, ya reemplazada |
| `enfasis/_duplicados_por_revisar/` (3 guías) | Versiones de las 06:16 del 16 sep, superadas por las de las 06:35 en `entregas/` |
| Todo el material de flujos | Decisión del equipo: se rehacen desde cero |

Se corrigió también `kino/proyecto-claude-kino.md`, cuya lista de archivos de conocimiento nombraba seis documentos ya borrados, y cuya copia de las instrucciones del proyecto está congelada en el 17 de septiembre.

---

## 5. Lo que no se tocó, y por qué

- **Las entregas académicas presentadas.** Registro, no fuente. Marcadas en `enfasis/CLAUDE.md` §5.
- **`ixd/Arcana.docx` y `montesereno/Arcana/`.** Documentos de 2026-1 y del arranque: contexto histórico. La regla 1 del proyecto ya los pone en el último lugar de la jerarquía de evidencia.
- **Las plantillas en blanco del curso.** Son los formatos oficiales que hay que diligenciar.
- **La evidencia cruda de la inspección.** `observaciones-*.jsonl`, `matriz-capacidades.csv`, `frontera-residente.json`, `sistema-inspeccion-roles.md`.

---

## 6. Lo que falta por verificar

1. Si las tres guías del 16 de septiembre ya fueron calificadas, o si todavía se pueden corregir antes de la sustentación. La atribución falsa de la Guía de consolidación es el punto más expuesto.
2. Si el equipo quiere mantener Valeria y Carlos como arquetipos para la Biblia, o construir los actores desde la evidencia de la inspección.
3. Las preguntas que abrió la errata: si aprobar una solicitud dispara `add_person` en HikCentral, qué ve quien es rechazado, si el administrador de comunidad tiene esa pantalla, y por qué solo hay 4 solicitudes frente a 893 usuarios.
4. `enfasis/CLAUDE.anterior-arcana.md` se conservó por si hay algo de logística del curso que no pasé a la versión nueva.
