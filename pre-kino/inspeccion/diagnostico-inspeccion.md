# Diagnóstico de la inspección por rol — app Montesereno / Kino

Inspección directa de la aplicación en producción, del 14 al 16 de septiembre de 2026, sobre cinco sujetos: residente sin datos, residente/propietario con datos, super administrador, administrador (dos comunidades) y portero. 60 observaciones registradas en los archivos `observaciones-*.jsonl`, cada una marcada como observada o inferida. La matriz de capacidad por rol está en `matriz-capacidades.csv`.

---

## 1. Lo que hay que corregir del brief

**El super administrador no aprueba cada ingreso a mano.** No aprueba ninguno. No existe cola de aprobación de ingresos ni pantalla de visitas pendientes en ninguno de los cuatro paneles del sistema. Lo verificamos rol por rol.

> **Errata del 21 de septiembre de 2026.** Sí existe una cola, pero no es de ingresos: `/super-admin/sso-registration-requests` («Registration requests», anidada bajo *Users*) aprueba **cuentas**. 4 solicitudes, las cuatro aprobadas, una de ellas con rol `Visitor`. Se escapó porque el inventario de menús se hizo sobre enlaces de primer nivel y pertenece al alta por Google, excluida por decisión del equipo. No cambia el hallazgo de fondo: lo que se aprueba es una cuenta, y el resultado sigue siendo una vinculación permanente sin fecha ni vigencia. Refuerza el hallazgo 3: el invitado de hoy no solo necesita cuenta, necesita que alguien apruebe su solicitud a mano. Detalle en `claude/reporte-inspeccion-por-rol.md` del proyecto de Claude.

Lo que hay en su lugar: el lector de la puerta (placa por ANPR, biométrico) consulta una lista cargada de antemano. Autorizar a alguien significa **darlo de alta como usuario** con documento, teléfono y correo, y sincronizarlo al hardware. Es una vinculación administrativa, no una decisión sobre una visita.

Eso reformula el problema con más precisión: el sistema **no tiene el concepto de permiso temporal para una persona**. No es que el residente no pueda otorgarlo; es que nadie puede, porque no existe.

---

## 2. Los cinco hallazgos que sostienen el diagnóstico

**1. El residente ya concede acceso físico, sin que nadie lo apruebe.** Registramos una placa inventada y quedó "Permitido" al instante, y llegó a sincronizarse con el sistema de acceso. Dos renglones más abajo, la misma pantalla dice: *"El estado de acceso es controlado por los administradores"*. La autoridad existe, el producto la niega en pantalla, y el residente no sabe que la tiene.

**2. La temporalidad ya está construida, para los carros.** Cada vehículo tiene "Válido Desde" y "Válido Hasta", ventanas de un año. El portero ve esas fechas. El administrador las ve. El dueño del carro no. Lo que el rediseño tendría que inventar para las visitas ya está implementado; está oculto justo para quien sabría cuánto debería durar.

**3. El invitado no es una visita, es un miembro permanente.** En la ficha de una propiedad aparecen personas con rol "Visitante" asociadas de forma indefinida, con cuenta. No hay fecha, no hay vigencia, no hay evento. Por eso el invitado necesita registrarse: no lo están invitando, lo están matriculando en un sistema de seguridad física.

**4. El requisito que molesta al residente es el mismo que rompe la integración.** Los 711 errores de HikCentral son todos la misma operación, `add_person`, con el mismo mensaje: *"Incorrect request parameter. [email parameter error]"*. Sin resolver desde agosto. El correo obligatorio, que obliga al invitado a tener cuenta, es el campo que está tumbando la sincronización con el hardware.

**5. Simetría invertida del conocimiento.** El portero de turno ve la cédula, el teléfono y el correo de los 312 residentes, la vigencia de sus permisos y si sus carros están realmente sincronizados. El residente no ve nada de eso sobre sí mismo. Quien menos decide es quien más ve.

---

## 3. El hallazgo más grave, ya confirmado

**En Refugio Campestre, la app y la puerta están desconectadas.**

| | Refugio Campestre | Villas Campestres |
|---|---|---|
| Usuarios registrados | 312 | 888 |
| Sincronizados con HikCentral | **0** | 887 |
| Vehículos registrados | 44 | 757 |
| Vehículos sincronizados | **1** | 757 |
| Vehículos "permitidos" según la app | 43 | 746 |

Mismo producto, mismo código, mismo administrador. En Refugio, 43 carros figuran como permitidos y uno solo existe para el sistema físico.

**Confirmado por el equipo (16 de septiembre): Refugio Campestre sí tiene el hardware instalado.** Con eso, estos números dejan de ser una instalación en curso y pasan a ser una integración caída: la app lleva meses mostrando permisos que la puerta desconoce, sobre lectores que ya están puestos. El único nivel de acceso configurado en todo el sistema pertenece a Villas, y los 711 errores de `add_person` son consistentes con eso.

Si los cinco residentes entrevistados el 2 de septiembre son de Refugio, esto le da otra base a lo que contaron.

---

## 4. Estado general del producto, en datos

- Un solo nivel de acceso en todo el sistema ("General Access Level"), binario, sin horarios ni tipos de persona, con 0 personas asignadas y sin sincronizar desde mayo.
- Un solo super administrador para 893 usuarios y 2 comunidades.
- 441 trabajos en cola fallidos.
- Cero zonas comunes configuradas en Refugio: por eso ningún residente puede reservar, aunque la función esté completa en los dos extremos.
- Cero contratistas registrados, siendo el ingreso de trabajadores el más frecuente del conjunto.
- Dos claves de traducción crudas visibles a los usuarios: `app.domestic_employee` y `app.vehicles_synced`.
- El panel del super administrador está en inglés y mezcla decisiones del conjunto con infraestructura (colas SQS, logs de ECS).

---

## 5. Observaciones de seguridad para el cliente

Van aparte del trabajo académico, y conviene que las oiga de ustedes:

- Cualquier residente puede habilitar cualquier placa, al instante, sin validación de formato ni verificación de que el vehículo sea suyo. Lo comprobamos con una placa inventada.
- El portero tiene acceso de lectura a los datos de identificación de todos los residentes.
- Un intento de entrar a una comunidad ajena cierra la sesión del usuario en vez de mostrarle un mensaje.

---

## 6. Qué no se inspeccionó

- El rol **Visitante** dentro de la app: se sabe que existe en el modelo de datos, no qué pantallas ve.
- Los flujos de alta por Google: se dejaron fuera por decisión del equipo, al ser una variante del inicio de sesión.
- Vistas de registros existentes en la cuenta vacía (no había datos que mirar).
- La inspección del primer día se hizo a 530px de ancho; a partir del propietario se usó ancho de escritorio.
