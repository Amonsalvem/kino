# Diagnóstico consolidado y pregunta guía v1 — Kino

Consolidación de los tres documentos de guía del curso (cliente y entorno, consolidación del diagnóstico, diseño de la experiencia) y del mapa de posibilidades, ajustados contra la inspección directa del 14 al 16 de septiembre de 2026.

Documento vivo completo: https://claude.ai/code/artifact/fa4efd6f-f49a-4776-98b2-b73ab9424d95
Deck de sustentación: https://claude.ai/artifact/VArWzzsnrcFFQrjCtRDFeZ · copia local en `Kino_Deck_diagnostico_2026-09-19.html`

> **Errata del 21 de septiembre de 2026.** Sí existe una cola de aprobación en el panel de super administrador (`/super-admin/sso-registration-requests`), pero aprueba **cuentas**, no ingresos: 4 solicitudes, las cuatro aprobadas, una con rol `Visitor`. Corrige la redacción de la fila 1 de §1 y del hallazgo H2, y refuerza H5. Detalle y preguntas abiertas en `claude/reporte-inspeccion-por-rol.md`.

---

## 1. Errata: seis afirmaciones corregidas

Los documentos de guía se escribieron con el Brief v0.1 (4 sep.) y la prueba con cinco residentes (2 sep.). La inspección ocurrió después y los contradice.

| # | Lo que decían las guías | Lo que se observó |
|---|---|---|
| 1 | "El Super Admin aprueba cada ingreso a mano" | No aprueba ningún **ingreso**. Lo único que aprueba a mano es el **registro de una cuenta**, en una cola anidada del panel de super administrador; no hay bandeja ni estado "pendiente" para visitas |
| 2 | "El residente no puede autorizar a su invitado" | Ya concede acceso físico al registrar una placa: queda "Permitido" al instante y se sincroniza |
| 3 | "El invitado debe crear cuenta, iniciar sesión y esperar" | Sí espera, pero a que le aprueben la **cuenta**, no el ingreso: no existe estado pendiente de visita. Queda matriculado como miembro permanente con rol "Visitante" |
| 4 | "Liberar el tiempo de aprobación manual es argumento de compra" | Hay 4 aprobaciones de cuenta en total frente a 893 usuarios: no hay tiempo de aprobación que liberar. El argumento económico hay que reconstruirlo |
| 5 | "El vigilante autoriza el ingreso" | Solo supervisa. Ya corregido por el equipo |
| 6 | La integración con hardware aparece como fortaleza | En Refugio está caída y ningún documento de guía lo recoge |

**Problema de atribución:** la Guía de consolidación atribuye la afirmación 1 a "inspección directa, sep. 2026". Esa cita no corresponde: la inspección dice lo contrario. Conviene arreglarlo antes de la sustentación.

---

## 2. Los nueve hallazgos consolidados

| ID | Hallazgo | Grado | Fuente |
|---|---|---|---|
| H1 | El permiso temporal para una persona no existe. Nadie puede otorgarlo | Observado | `matriz-capacidades.csv`, `diagnostico-inspeccion.md` §1 |
| H2 | El Super Administrador no aprueba ingresos. Autorizar es dar de alta y sincronizar. Lo que sí aprueba a mano es el registro de cuentas, en una cola anidada | Observado (+ errata del 21 sep.) | `diagnostico-inspeccion.md` §1, §4; `claude/reporte-inspeccion-por-rol.md` |
| H3 | El residente ya concede acceso físico, sin validación ni constancia. Placa inventada → "Permitido" | Observado, con prueba | `diagnostico-inspeccion.md` §2.1, §5 |
| H4 | La vigencia ya está construida para los carros, oculta para el dueño | Observado | `diagnostico-inspeccion.md` §2.2 |
| H5 | El invitado es un miembro permanente con rol "Visitante", sin fecha ni vigencia, y su cuenta pasa por aprobación manual | Observado | `diagnostico-inspeccion.md` §2.3; errata del 21 sep. |
| H6 | Refugio: 0/312 personas y 1/44 vehículos sincronizados, con hardware instalado | Observado + confirmación del equipo | `diagnostico-inspeccion.md` §3 |
| H7 | Los 711 errores son `add_person` por el campo correo. Una decisión resuelve UX y técnica | Observado | `diagnostico-inspeccion.md` §2.4 |
| H8 | Simetría invertida: el portero ve de los residentes lo que ellos no ven de sí mismos | Observado | `matriz-capacidades.csv`, §2.5 |
| H9 | El ingreso más frecuente (colaboradores) tiene cero registros en el sistema | Mixto: declarado + observado | `diagnostico-inspeccion.md` §4; GEIH 2026 |

Se conservan dos condiciones del entorno: la biometría condicionada por la SIC (Res. 52185 de 2025) y el rival diario, la llamada a portería.

---

## 3. El problema central, reformulado

> El sistema de acceso de Monte Sereno repartió mal la autoridad y después dejó de registrarla. El residente ejerce un poder de acceso que el producto no reconoce, no acota y no deja por escrito; la administración cree conservar un control que no ejerce; y el objeto que haría gobernable esa decisión, un permiso con autor, motivo y vigencia, no existe en el modelo.

| | Versión anterior | Versión corregida |
|---|---|---|
| Naturaleza | Cuello de botella | Ausencia de gobierno |
| Quién decide hoy | El Super Admin, caso por caso | El lector, contra una lista sin reglas |
| Qué hay que quitar | Un paso de aprobación | Nada para el ingreso. Para el registro sí hay un paso humano que reemplazar |
| Argumento ante la administración | "Suelte el control" | "Hoy no tiene control; esto se lo da" |

---

## 4. Pregunta guía v1 y cuatro retos

> ¿Cómo podríamos lograr que, en un conjunto cerrado como Monte Sereno, la decisión sobre quién entra la tome quien conoce al visitante, sin que la comunidad pierda control, trazabilidad ni protección de los datos de quienes ingresan?

La pregunta sobrevive; su lectura cambia. Ya no describe trasladar poder desde el Super Admin, sino reconocer, acotar y dejar constancia de un poder que el residente ya ejerce sin saberlo.

- **R1.** Reconocer y acotar la autoridad de quien conoce al visitante (H1, H3).
- **R2.** Dejar constancia de quién autorizó a quién (H3, H8).
- **R3.** Dejar entrar sin convertir a nadie en usuario (H5, H9, H4).
- **R4.** Operar sobre el hardware instalado y proteger los datos (H6, H7, SIC).

---

## 5. Cambios en el mapa de posibilidades

- **P5** (validación contra base de datos) y **P10** (entrada sin contraseña) pasan de posibilidad a decisión tomada. P10 cambia de contenido: código por WhatsApp, teléfono obligatorio y único. P5 cambia de naturaleza con la errata: ya no construye lo que falta, **reemplaza un paso humano que hoy existe**, y hay que decir qué pasa con esa pantalla y con las solicitudes en curso.
- **P9** (vehículo del visitante) sube de prioridad: la placa viaja por LPR sin crear persona en HikCentral, lo que esquiva el error de H7.
- **P6** (tablero del vigilante) agrega quitar de su vista la cédula, el teléfono y el correo de los 312 residentes.
- **P14 nueva:** reparar la sincronización de Refugio. Previa a todo lo demás si el piloto es Refugio.
- **P15 nueva:** estados honestos. Ningún estado de la interfaz puede afirmar algo del mundo físico que el lector no haya confirmado.
- **Se disuelve** la pantalla de "pase pendiente" del administrador que dibuja el lienzo del flujo de visitante ocasional. Repondría un cuello de botella que el sistema nunca tuvo para los ingresos.

---

## 6. Riesgos abiertos

1. **El riesgo técnico número uno:** si el pase del invitado se materializa como *persona* en HikCentral, el correo obligatorio reaparece y con él los 711 errores. Tres salidas sin verificar: placa por LPR, credencial temporal sin persona, o correo sintético por pase (deja deuda).
2. El OTP por WhatsApp es una migración de 893 cuentas, no un cambio de pantalla.
3. La franja horaria exige rehacer los niveles de acceso: existe un único Access Level, binario, sin horarios, sin sincronizar desde mayo.
4. "Cupo de parqueadero" y "unidad al día en cartera" no tienen datos en ningún panel.

**Argumento económico reconstruido.** El puente "liberar tiempo de aprobación manual" cayó con la inspección. Los tres que sí resisten: infraestructura pagada y sin operar en Refugio; riesgo legal con fecha (SIC); y la exposición ante el consejo de un permiso que nadie puede rastrear.

---

## 7. Lo que falta por verificar, en orden

1. ¿HikCentral admite una credencial temporal sin crear persona? (Manuel) — bloquea P1, P2 y P9.
2. ¿Qué reglas de autorización tiene escritas Monte Sereno y quién responde? (administración) — es el contenido de P4.
3. ¿Por qué está caída la sincronización de Refugio? (Manuel) — decide si el piloto es Refugio o Villas.
4. ¿Aprobar una solicitud de registro dispara `add_person` en HikCentral o solo crea la cuenta? Ata directamente con H7.
5. ¿Qué necesitaría la administración para confiar en una autorización del residente?
6. Consentimiento biométrico y vías no biométricas actuales.
7. Flujo de excepción en portería con alguien no registrado.
8. Mezcla real de tipos de ingreso, con registros del sistema.
9. Citas textuales de los cinco residentes y de qué comunidad son. Es el único eslabón de evidencia sin respaldo documentado.
10. Rehacer el inventario de menús a dos niveles en los cuatro paneles antes de sustentar: la errata del 21 sep. salió de un ítem anidado.
11. Costo de la infraestructura instalada en Refugio.
12. Comportamiento sin conexión en portería.

---

## 8. Estado de los flujos (21 de septiembre de 2026)

Todo el material de flujos se borró por decisión del equipo para rehacerlo desde cero: los 11 lienzos y sus 66 variantes de marca, los generadores, y los seis documentos `.md` (`recorte-flujos-necesarios`, `reglas-flujos-optimos`, `auditoria-ux-flujos`, `anexo-defectos-por-flujo`, `acta-reconstruccion-flujos`, `contraste-propuesta-vs-inspeccion`). Inventario en `kino/inspeccion/_borrado-flujos-2026-09-21.md`.

Lo que queda como base para rehacerlos: este documento, `diagnostico-inspeccion.md`, `claude/reporte-inspeccion-por-rol.md`, `matriz-capacidades.csv` y las 60 observaciones crudas en `observaciones-*.jsonl`. La matriz de 10 defectos × 8 flujos y el veredicto por flujo ya no existen; se reconstruyen desde esa evidencia, con la errata de §1 incorporada desde el principio.
