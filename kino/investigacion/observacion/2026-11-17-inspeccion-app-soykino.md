# Inspección de soykino.com y app.soykino.com (16 y 17 nov 2026)

Inspección directa, en solo lectura, desde el Chrome de Alejandro. No se creó, editó ni aprobó nada. Los datos personales vistos no se transcriben. Todo lo de este archivo es **observado**, salvo lo marcado como inferido.

## Conclusión

La integración con la puerta funciona en Villas y es el activo que se vende. El KEY, el ingreso sin contraseña y el registro sin aprobación no están construidos como dice el canon. La app web no tiene API: la app nativa empieza por construirla.

```
Lo que funciona                 Lo que falta o falla
─────────────────               ─────────────────────────────────────────
Villas ⇄ HikCentral (100 %)     Refugio ⇄ HikCentral (0 %)
Eventos de puerta en vivo       KEY en uso real (1 en Villas, de prueba)
Contratistas y seguridad social Visita sin cuenta (el KEY crea un usuario)
Pagos con Wompi (en prueba)     Ingreso por WhatsApp, API, app nativa
```

## Cobertura

| Rol | Comunidad | Estado |
|---|---|---|
| Residente | Refugio (`/app/1`) | Inspeccionado |
| Administrador | Refugio (`/admin/1`) | Inspeccionado |
| Administrador | Villas (`/admin/2`) | Inspeccionado |
| Portería | Villas (`/guard/2`) | Inspeccionado |
| Super administrador | Todas | Pendiente: falta sesión |
| Contratista | `/contractor` | Pendiente: falta sesión |
| Visita | Enlace del KEY | Pendiente: no hay KEY vigente para abrir |

## Tecnología observada

| Pieza | Observado |
|---|---|
| Sitio | HTML estático con Google Analytics y un chat de Impulso (`api-chat.impulso.com.co`) |
| App | Laravel, Filament, Livewire, Alpine y Laravel Echo (tiempo real) |
| API | `/api`, `/api/v1` y `/api/user` responden 404 |
| PWA | Sin `manifest.json` |
| Paneles | `/app/{comunidad}` (residente), `/admin/{comunidad}`, `/guard` (portería), `/contractor` |
| Ingreso | Correo y contraseña en los tres paneles; Google solo en residente. Sin «olvidé mi contraseña» visible. Sin código por WhatsApp |

**Inferido:** sin API, una app nativa no tiene a qué conectarse. Filament genera pantallas en el servidor; no expone datos para un cliente móvil.

## Cifras por comunidad (17 nov 2026, 9:30 p. m.)

| Dato | Villas | Refugio |
|---|---|---|
| Usuarios | 1.684 | 388 |
| Usuarios sincronizados con HikCentral | **1.684** | **0** |
| Vehículos | 851 | 117 |
| Vehículos sincronizados | 844 | 1 |
| Eventos de puerta en el día | 1.660 (54 sin identificar) | 0 |
| KEY creados | 1 (prueba) | 2 |
| Unidades configuradas | 87 | 231 |
| Empresas contratistas | 27 | sin dato |
| Zonas comunes | 1 | sin dato |
| Cobros | 4 de $15.000 (prueba); 3 pagos fallidos en 30 días | 1 de $15.000 (prueba) |
| Solicitudes de registro por aprobar | 1 | 0 |

Comparación con septiembre (`pre-kino/inspeccion/diagnostico-inspeccion.md` §3): Villas pasó de 887 a 1.684 usuarios sincronizados. Refugio sigue en 0. La integración de Refugio sigue caída dos meses después.

El canon y D-014 usan 100 casas para Villas. La app tiene 87 unidades configuradas. Falta confirmar cuál cifra se factura.

## Hallazgos por rol

### Residente (Refugio)

| # | Hallazgo | Efecto |
|---|---|---|
| R1 | Menú: Inicio, Accesos, KINO KEY, Paquetería, Pagos, Reservas, Perfil, Vehículos, Propiedades | Cubre el alcance que vende el sitio |
| R2 | Crear KEY pide «Documento*» como obligatorio y luego dice «agrega al menos uno: documento, teléfono, correo o placa» | Regla contradictoria en la misma pantalla |
| R3 | El KEY tiene vigencia (ahora, hoy, mañana, fecha) y modo **recurrente** para aseo, jardín o clases | El colaborador ya tiene camino. Bien |
| R4 | Los estados del KEY incluyen Pendiente, Aprobada y Denegada | **Inferido:** alguien aprueba. Choca con la regla de que el residente autoriza a sus visitas y colaboradores (`proyecto.md`, decisiones tomadas) |
| R5 | El filtro «Propiedad destino» lista todas las unidades de la comunidad | El residente ve unidades que no son suyas |
| R6 | En «Mis propiedades» la cuenta figura con rol «Visitante» en su propia casa; el encabezado dice «Residente» | Rol inconsistente |
| R7 | Sigue visible la clave cruda `app.domestic_employee` | Igual que en septiembre |
| R8 | El perfil y la pantalla de ingreso llaman al KEY con una palabra vetada por el vocabulario | Contradice `AGENTS.md` §5.8 |
| R9 | Abrir la URL de otra comunidad cierra la sesión sin mensaje | Igual que en septiembre. Se reprodujo el 16 nov |
| R10 | La reserva la aprueba la administración «si la zona lo requiere» | Coherente con los límites de la administración |

### Administrador (Villas y Refugio)

| # | Hallazgo | Efecto |
|---|---|---|
| A1 | 14 secciones: inicio, accesos, paquetes, pagos, reservas, solicitudes de registro, usuarios, vehículos, ajustes, unidades, autorizaciones, contratistas, trabajadores, zonas, bitácora | Panel completo |
| A2 | El panel está casi todo en inglés, con partes en español | Producto para Colombia con interfaz mezclada |
| A3 | Inicio de Refugio dice «la sincronización está al día» con 0 de 388 usuarios sincronizados | Aviso falso; oculta la falla principal |
| A4 | Accesos en tiempo real: placa (ANPR) y biométrico, con responsable y rol. 54 eventos «sin rol identificado» en Villas | El dato que pide el aviso de llegada ya existe |
| A5 | La bitácora registra «Usuario creado» al crear un KEY | La visita sigue siendo un usuario permanente (`proyecto.md`, hechos vigentes) |
| A6 | Los trabajadores de contratistas tienen correos inventados del tipo `trabajadorNNNN@villas.com` | **Inferido:** parche para el correo obligatorio que exige HikCentral (`add_person`) |
| A7 | Ajustes: control de seguridad social para empleados y contratistas, con modo alerta o bloqueo | Función diferencial para colaboradores |
| A8 | El registro con Google espera aprobación del administrador | Choca con «el registro se valida contra la cédula» (`proyecto.md`) |
| A9 | Pagos: cuotas de administración, cobro único, cartera por edad y estado por unidad | El módulo de D-012 existe; solo tiene cobros de prueba |
| A10 | Usuarios: acción masiva «Sincronizar con HikCentral» y filtro por ID de HikCentral | Herramienta para reparar Refugio |

### Portería (Villas)

| # | Hallazgo | Efecto |
|---|---|---|
| P1 | Menú en español: Validar, En vivo, Bitácora, Paquetería, Reservas de hoy, Personas, Vehículos | Panel pensado para tableta |
| P2 | «Validar KINO KEY» con la cámara de la tableta o un lector, o escribiendo placa, documento o código | La validación del KEY ya existe en la web. La app nativa de portería no es urgente |
| P3 | «En vivo» muestra entradas y salidas por placa (ANPR) y biométrico, con responsable y rol | El vigilante ve el mismo flujo que la administración |
| P4 | Personas que entran a diario por placa aparecen con rol «Visitante» | **Inferido:** «Visitante» se usa para gente permanente; confirma que la visita sigue siendo un miembro |
| P5 | «Personas» (solo consulta) deja ver correo, teléfono, documento, fecha de nacimiento y contacto de emergencia de toda la comunidad | La simetría invertida de septiembre sigue (`proyecto.md`, hechos vigentes). Riesgo de datos personales (Ley 1581 de 2012) |
| P6 | Paquetería: registro con foto y aviso al residente | El aviso existe; falta saber por qué canal llega (correo o WhatsApp) |
| P7 | La bitácora de KEY tiene una sola entrada: la prueba del 17 nov | Igual a A5: el KEY no se usa en Villas |

### Sitio soykino.com

| # | Hallazgo | Efecto |
|---|---|---|
| S1 | Ofrece «Con tu marca: tu nombre y tus colores sobre la tecnología de KINO» | Contradice D-009 (marca propia, sin marca blanca) |
| S2 | Usa la misma palabra vetada en varias secciones | Contradice `AGENTS.md` §5.8 |
| S3 | Única llamada a la acción: correo `mailto:` | Sin formulario ni agenda; no mide prospectos |
| S4 | Sin enlaces a App Store ni Google Play | Coherente: la app nativa no existe |
| S5 | Segmentos: parcelaciones, conjuntos y edificios, clubes | El target no está priorizado |
| S6 | Pagos «con Wompi», con aviso de que no hay recaudo activo en todas las comunidades | Texto honesto; sirve de modelo |

## Qué falta inspeccionar

1. Super administrador: colas, errores de HikCentral (711 en septiembre) y trabajos fallidos.
2. Contratista (`/contractor`): qué ve la empresa.
3. Enlace del KEY que recibe la visita.
4. Quién aprueba un KEY en estado «Pendiente».
