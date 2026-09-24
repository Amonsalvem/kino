# Muestras de voz · Kino

Reunidas el 23 sep 2026 para calibrar la voz de marca. Solo se transcribe: no se corrigió ni se redactó nada.
Anonimización: el número de propiedad se reemplazó por uno ficticio (118). No aparecen nombres, teléfonos, placas ni cédulas reales.

## a) Microcopy actual de la app

Fuente: `inspeccion/observaciones-*.jsonl` (inspección directa del 14 al 16 sep 2026). Se copia tal cual, con sus tildes y mayúsculas faltantes, porque eso también es dato.

| Rol | Ruta | Pantalla | Texto en pantalla |
|---|---|---|---|
| residente | `/app/login` | Acceso | Recordarme |
| residente | `/app/login` | Acceso | Continuar con Google |
| residente | `/app/1` | Escritorio | Perfil incompleto |
| residente | `/app/1` | Escritorio | …para que administración y portería puedan contactarte |
| residente | `/app/1` | Escritorio | No tienes propiedades asociadas |
| residente | `/app/1` | Escritorio | Sin propiedades asignadas |
| residente | `/app/1` | Barra superior | Rol: Residente |
| residente | `/app/1/my-vehicles/create` | Registrar Vehículo | Registrar Vehículo |
| residente | `/app/1/my-vehicles/create` | Registrar Vehículo | Será registrado automáticamente en todas tus comunidades |
| residente | `/app/1/my-reservations` | Mis Reservas | Crear Reserva |
| residente | `/app/1/my-reservations/create` | Crear Reserva | Sólo se muestran horarios disponibles según la zona, la fecha y las reservas existentes |
| propietario | `/app/1` | Escritorio | Residente / Propietario |
| propietario | `/app/1` | Escritorio | 1 propiedad asociada. 118 - Sin zona registrada - Activo - Rol: Propietario - Personas asociadas: 4 |
| propietario | `/app/1` | Escritorio | 1 vehiculo registrado. 1 activo para ingreso. |
| propietario | `/app/1` | Escritorio | Ultimo acceso: Sin accesos recientes |
| propietario | `/app/1` | Escritorio | Paquetes pendientes · Proximas reservas · Ultimos accesos · Mis propiedades · Mis Vehiculos |
| propietario | `/app/1/my-properties` | Mis propiedades | Visitante (rol de persona asociada) |
| propietario | `/app/1/my-properties` | Mis propiedades | app.domestic_employee (clave de traducción sin traducir, visible en pantalla) |
| propietario | `/app/1/my-properties` | Mis propiedades | empleada domestica |
| propietario | `/app/1/my-vehicles` | Mis Vehiculos | Estado de Acceso |
| propietario | `/app/1/my-vehicles` | Mis Vehiculos | El estado de acceso es controlado por los administradores |
| propietario | `/app/1/my-reservations/create` | Crear Reserva | confirmada / pendiente |
| administrador | `/admin/1` | Escritorio | Permitido |
| administrador | `/admin/1` | Escritorio | app.vehicles_synced (clave de traducción sin traducir, visible en pantalla) |
| administrador | `/admin/1/users` | Usuarios | Crear Usuario |
| administrador | `/admin/1/common-areas` | Zonas Comunes | No se encontraron registros |
| administrador | `/admin/1/common-areas` | Zonas Comunes | Crear Zona comun |
| administrador | `/admin/1/contractors` | Contratistas | Crear Contratista |
| portero | `/guard/2/vehicles` | Vehiculos | Estado de Sincronizacion |
| portero | `/guard/2/vehicles` | Vehiculos | Valido Desde / Valido Hasta |
| portero | `/guard/2/packages` | Paquetes | Crear paquete |
| super_admin | `/super-admin/access-events` | Accesos en tiempo real | Autorizado |
| super_admin | `/super-admin/access-events` | Accesos en tiempo real | Sin propiedad vinculada |
| super_admin | `/super-admin/access-levels` | Access Levels | General Access Level |
| super_admin | `/super-admin/vehicles` | Vehicles | Allowed · Sync Status · Valid Until · Synced · Pending |
| super_admin | `/super-admin/hikcentral-errors` | HikCentral Errors | Incorrect request parameter. [email parameter error] |

Faltan: capturas de las pantallas de ingreso de visitantes, del mensaje de bienvenida, de los errores de formulario y de las notificaciones. Se piden al equipo; no se inició sesión en la app.

## b) Mensajes reales de portería y WhatsApp

PENDIENTE: no hay ninguno en los archivos del proyecto. Se piden al equipo (anonimizados antes de pegarlos aquí).

## c) Correcciones del equipo (antes → después)

Confirmadas por Nico o Alejandro: ninguna encontrada en los archivos. Se piden al equipo.

### Candidatas, pendientes de confirmar autoría

Fuente: `gorr-brand-system/clientes/kino/pruebas/voz-antes.md` y `voz-despues.md` (barrido del 22 sep, «registro-muletillas-2026-09-22»). Los archivos no dicen si las correcciones las hizo el equipo o un asistente; hasta confirmarlo no cuentan como correcciones del equipo.

1. Un sistema que decide quién puede entrar a su casa. Y ya está funcionando. → Un sistema que decide quién entra a su casa, y ya funciona.
2. Está funcionando hoy, con gente real usándola todos los días. → Está en producción y la gente la usa a diario.
3. Y con una restricción firme: convivir con el hardware → La condición: convivir con el hardware
4. No es un caso raro. Casi la mitad de la gente que vive en ciudad en Colombia vive bajo un régimen así, y en Medellín son dos de cada tres. Lo que se resuelva acá aplica en muchos lados. → Casi la mitad de las viviendas urbanas de Colombia están en propiedad horizontal, y en Medellín, seis de cada diez. Lo que se resuelva acá sirve para muchos otros conjuntos.
5. Es el actor con menos interés en el sistema. No quiere una cuenta, no quiere instalar nada y no tiene por qué dejar sus datos en un sistema de seguridad donde no vive. → Es el actor con menos interés en el sistema: no quiere cuenta ni instalar nada, y no tiene por qué dejar sus datos en el sistema de seguridad de un lugar donde no vive.
6. Propiedades, vehículos, reservas, paquetes. Ni visitas, ni invitados, ni autorizaciones. → Propiedades, vehículos, reservas y paquetes; nada de visitas, invitados ni autorizaciones.
7. No estudiamos «el producto». Estudiamos un hilo. → Del producto estudiamos un solo recorrido.
8. No es la función de un rol. Empieza en el residente, pasa por la administración, toca al portero y termina en el invitado. → Empieza en el residente, pasa por la administración y el portero, y termina en el invitado.
9. Tiene un principio y un final observables. Se puede cronometrar, contar y comparar. → Tiene un principio y un final observables, así que se puede cronometrar y comparar.
10. Del 14 al 16 de septiembre, dentro del sistema que la gente usa a diario. No un demo ni un prototipo: el producto vivo, con sus datos reales. → Del 14 al 16 de septiembre, sobre los datos reales de las dos comunidades.
11. de dónde sale la afirmación. Nada se escribió de memoria. → de dónde sale la afirmación.
12. Leímos la estructura, no capturas / Para cada pantalla listamos qué elementos interactivos existen y, sobre todo, cuáles no. Lo que falta no aparece en una captura. → Leímos la estructura de cada pantalla / Listamos los elementos interactivos que tiene cada pantalla y los que le faltan, que en una captura no se ven.
13. no están en ninguna columna: no puede nadie, porque el objeto no existe. Lo que sí existe está repartido al revés: el residente abre la puerta sin ver con qué vigencia; el portero ve la vigencia y no puede cambiar nada. → no las tiene nadie, porque el objeto no existe. Lo que sí existe está repartido al revés: el residente abre la puerta sin ver la vigencia, y el portero ve la vigencia pero no puede cambiar nada.
14. Ningún paso de aprobación, ninguna validación de formato: aceptó → Sin paso de aprobación ni validación de formato: aceptó
15. Y se sincronizó con el sistema físico de acceso. Es decir: esa placa abre la puerta. → Se sincronizó con el sistema físico de acceso, así que esa placa abre la puerta.
16. El residente ya decide quién entra. No lo sabe, no puede ponerle un límite y no queda constancia de que lo hizo. Eso da vuelta al problema entero: no hay que convencer a nadie de darle poder al residente, porque ya lo tiene. → El residente ya decide quién entra, pero no lo sabe, no puede ponerle límite y no queda constancia. Eso cambia el problema: no hay que convencer a nadie de darle poder al residente, porque ya lo tiene.
17. Y cuidado con confundirlo con su síntoma → No confundirlo con su síntoma
18. No nombra a quién se le quita el poder, sino a quién le corresponde: el que conoce al visitante. Eso la mantiene abierta, porque no supone que haya que desmontar nada, y le permite describir con precisión lo que la evidencia muestra: reconocer, acotar y dejar constancia de un poder que ya se ejerce. → Nombra a quien le corresponde decidir, el que conoce al visitante, en vez de a quién se le quita el poder. Así queda abierta, porque no supone desmontar nada, y describe lo que muestra la evidencia: un poder que ya se ejerce y que hay que reconocer, acotar y dejar registrado.
19. o la fuente del entorno. Ninguna caja se escribió sin eso. → o la fuente del entorno.
20. <h3>Y seis estados, que son los del sistema de marca de Kino</h3> → <h3>Los seis estados del sistema de marca de Kino</h3>
21. Es el único que sabe a quién espera, y el único que no tiene dónde decirlo. El recorrido principal termina fuera del sistema. El alterno, registrar una placa, sí abre la puerta, y lo hace sin que él lo sepa. → Sabe a quién espera y no tiene dónde decirlo. El recorrido principal termina fuera del sistema; el alterno, registrar una placa, sí abre la puerta, sin que él lo sepa.
22. El 51,3% de los contratos de trabajo doméstico fue por días en el primer semestre de 2026 y la informalidad supera el 87%. El vínculo real es intermitente; el sistema solo sabe representar permanencia. → El 51,3 % de los contratos de trabajo doméstico fue por días en el primer semestre de 2026, y la informalidad supera el 87 %.
23. <p class="pie">Entrega datos de por vida para una visita de una tarde. Es el actor → <p class="pie">Es el actor
24. El lector abre la puerta en el primer paso. Todo lo que viene después es registro. Por eso no hay cuello de botella que destrabar, y por eso la administración no puede responder ante el consejo por un ingreso concreto. → El lector abre la puerta en el primer paso y lo demás es registro. No hay cuello de botella que destrabar, y la administración no puede responder ante el consejo por un ingreso concreto.
25. No es una licencia narrativa nuestra: es que el objeto que haría alcanzable la meta no existe. → Pasa porque no existe el objeto que haría alcanzable la meta.
26. Todo lo que viene después es registro. Por eso no hay cuello de botella que destrabar: no hay nadie esperando. → Lo que viene después es registro, así que no hay cuello de botella que destrabar: nadie espera una aprobación.
27. Es lo único que hay que construir de cero, y es lo que comparten los cuatro flujos propuestos. → Es lo único que hay que construir de cero y lo comparten los cuatro flujos propuestos.
28. Sin autor no se puede revisar, ni corregir, ni defender ante el consejo. → Sin autor no se puede revisar, corregir ni defender ante el consejo.
29. Y una prohibición. No crea una persona. Esa es la restricción que ordena todas las decisiones: si un pase obliga a dar de alta a alguien, vuelve a exigir correo, vuelve a producir los errores de sincronización y vuelve a dejar una cuenta que nadie dará de baja. → Una prohibición: no crea una persona. Es la restricción que ordena las demás decisiones, porque un pase que obliga a dar de alta a alguien exige otra vez correo, reproduce los errores de sincronización y deja una cuenta que nadie dará de baja.
30. <h3>Y no hay que inventarlo entero / Dos piezas ya están construidas en el producto. → <h3>Dos piezas ya existen / El producto ya tiene dos piezas del pase.
31. Y la reserva de zona común ya pide → La reserva de zona común ya pide
32. Está vacía porque nadie configuró las zonas, no porque la pieza no exista. → Hoy está vacía porque nadie configuró las zonas.
33. Y ninguna pantalla afirma «Permitido» antes de que la puerta lo confirme. / Delta contra el flujo actual: aparece el objeto que no existía, el acto de otorgar es explícito y tiene autor, la vigencia es visible y elegible, y ninguna pantalla afirma lo que la puerta no ha confirmado. → Ninguna pantalla afirma «Permitido» antes de que la puerta lo confirme. / Delta contra el flujo actual: aparece el pase, el objeto que no existía.
34. La caducidad es el comportamiento por defecto. Y la decisión que quita el correo del camino quita también los 711 errores de sincronización. → La caducidad es el comportamiento por defecto, y la decisión que saca el correo del camino elimina también los 711 errores de sincronización.
35. El pase viaja por el canal que la persona ya usa, y no crea cuenta. La vía no biométrica es la que la norma obliga a ofrecer, y la única que hoy no rompe la integración con el hardware. / La vía más respetuosa con los datos pasa a ser la vía principal, y de paso es la única que hoy no rompe → El pase llega por el canal que la persona ya usa y no crea cuenta. La vía no biométrica es la que la norma obliga a ofrecer. / La vía que menos datos pide pasa a ser la principal, y es también la única que hoy no rompe
36. El cambio es de argumento más que de pantallas: la administración pasa de creer que controla a poder demostrarlo. Es el único control que el consejo puede auditar. → Cambia más el argumento que las pantallas: la administración pasa de creer que controla a poder demostrarlo ante el consejo.
37. Ninguna se descarta todavía por alcance. Lo que cambia entre ellas no es su valor: es de quién depende que avance. → Todavía no se descarta ninguna por alcance. Se agrupan según de quién depende que avancen.
38. La inspección vio la pantalla, no el trabajo. Antes de rediseñar hay que mirar el turno. → La inspección vio la pantalla del portero, pero no su turno, y hay que observarlo antes de rediseñar.
39. o como una combinación. Sin ella se diseña a ciegas. → o como una combinación.
40. No bloquea el diseño; sí la defensa. Es lo primero que se va a pedir. → No bloquea el diseño, pero sí la defensa, y es lo primero que van a pedir.
41. Sigue existiendo y sigue sincronizada con el sistema físico de acceso. Sigue abriendo. → Todavía existe, está sincronizada con el sistema físico de acceso y abre la puerta.
42. No entrevistamos a residentes ni a porteros: todo lo que sigue sale de recorrer el producto. → No entrevistamos a porteros, y de la prueba con cinco residentes faltan las citas textuales; lo demás sale de recorrer el producto.

## d) Textos de Kino que el equipo considera bien escritos

PENDIENTE: ningún archivo marca un texto como aprobado por el equipo. El perfil de tono sí está aprobado (22 sep: formalidad 2, humor 1, respeto 1, entusiasmo 2, en `voz.json`), pero no hay textos de referencia señalados.
