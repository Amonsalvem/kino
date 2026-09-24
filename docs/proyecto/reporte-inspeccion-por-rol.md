# Reporte de inspección por rol — app Montesereno / Kino

Documento vivo: https://claude.ai/code/artifact/1fa4f4cf-6a15-4adc-8702-7aa2df30cadc

Reporte sujeto por sujeto de la inspección del 14 al 16 de septiembre de 2026, armado directamente desde los cinco `observaciones-*.jsonl` y `matriz-capacidades.csv` de `kino/inspeccion/`. Complementa a `diagnostico-inspeccion.md` (que organiza por hallazgo) organizando por actor.

Contenido: método y límites · matriz de capacidades por rol · un apartado por sujeto (residente sin datos, residente/propietario con datos, administrador, super administrador, portero) · lo que ningún rol puede hacer · anexo de seguridad para el cliente · defectos visibles y cifras de salud · qué no se inspeccionó y qué falta verificar.

Conteo de evidencia: 59 observaciones, todas marcadas `observado`; solo dos con `ejecutado: true` (el registro de la placa TST001 y su verificación en el panel de super administrador).

## Errata del 21 de septiembre: sí existe una cola de aprobación

Nico aportó una captura de `/super-admin/sso-registration-requests` (**Registration requests**, anidada bajo *Users* en el panel de super administrador). Corrige una afirmación que estaba en `diagnostico-inspeccion.md`, en `claude/diagnostico-consolidado-v1.md` y en las instrucciones del proyecto.

Qué muestra: tabla con User, Email, Community, Property, Role, Status y Created. 4 solicitudes, las cuatro `Approved` — tres del equipo (Nico ×2 como Resident en Villas V 1047 y Owner en Refugio 346; Alejandro como **Visitor** en Refugio sin propiedad) y una de una residente de Villas, creada el 15 de agosto de 2026.

Qué corrige y qué no:

- **Falso desde ahora:** «no existe bandeja ni cola de aprobación» en ninguno de los cuatro paneles. Sí existe una.
- **Sigue en pie:** el super administrador no aprueba *ingresos*. Lo que aprueba esa cola es una **cuenta**, y el resultado sigue siendo la vinculación permanente de una persona. No hay fecha, vigencia ni evento.
- **Refuerza H5:** una de las cuatro filas es un `Visitor`. El invitado de hoy no solo necesita cuenta, necesita que alguien apruebe su solicitud a mano.
- **Toca una decisión tomada:** «el registro no lo aprueba el administrador, se valida contra la cédula». Sigue siendo válida como diseño, pero pasa de *construir lo que falta* a *reemplazar un paso humano que hoy existe*. Hay que decir qué pasa con esa pantalla y con las solicitudes en curso.

Por qué se escapó en la inspección: el inventario de menús se hizo sobre enlaces de primer nivel y `Registration requests` es un ítem anidado; además pertenece al flujo de alta por Google (la ruta empieza por `sso-`), que el equipo excluyó por decisión propia.

**Pendiente de edición:** la línea de `<hechos_vigentes>` en las instrucciones del proyecto que dice «no existe bandeja ni cola de aprobación» debe reescribirse como «no existe cola de aprobación **de ingresos**; sí existe una de **registro de cuentas** en el panel de super administrador».

## Preguntas abiertas que dejó la errata

1. ¿Aprobar una solicitud dispara `add_person` en HikCentral o solo crea la cuenta? Ata directamente con los 711 errores.
2. ¿Qué pasa al rechazar y qué ve el solicitante?
3. ¿El administrador de comunidad tiene esa pantalla o es exclusiva del super administrador?
4. ¿Desde cuándo existe la cola y por qué solo 4 solicitudes frente a 893 usuarios?
5. Rehacer el inventario de menús a dos niveles en los cuatro paneles antes de sustentar.

## Otros pendientes

- Borrar la placa de prueba `TST001` (id 799, Refugio Campestre), que quedó sincronizada con el sistema físico de acceso.
- El portero se inspeccionó en Villas (comunidad 2) y los residentes en Refugio (comunidad 1): las comparaciones entre esos dos roles cruzan comunidades.
