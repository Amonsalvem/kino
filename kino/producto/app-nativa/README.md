# App nativa de Kino · qué falta para construirla

Plan para el programador y Alejandro. Fuente de lo que existe: `kino/investigacion/observacion/2026-11-17-inspeccion-app-soykino.md`. Las decisiones que pide están como PROPUESTA en `kino/canon/decisiones.md` (D-016 y D-017).

## Conclusión

La app nativa no empieza por pantallas. Empieza por una API sobre el backend de Laravel que ya existe. Con el programador disponible todo el tiempo, una primera versión del residente puede llegar a TestFlight y a prueba interna de Google Play en unas 6 semanas. Esa cifra es **inferida**: no hay medición de la velocidad del equipo.

```
Semana   1    2    3    4    5    6    7    8
API      ████████████
Cuentas  ██                               (Apple tarda en aprobar la cuenta de empresa)
Arreglos ████████                         (correo de HikCentral, KEY sin usuario)
App           ██████████████████
Push               ████████
Pruebas                      ██████████   (TestFlight y Play interna con 10 casas de Villas)
Tiendas                                ███ (revisión de Apple y Google)
```

## Alcance de la primera versión

Una app para el **residente**. La administración sigue en la web. La portería sigue en la web hasta la fase 2.

| Función | Ya existe en la web | En la app nativa |
|---|---|---|
| Crear y compartir KEY (visita y colaborador recurrente) | Sí | Sí, con compartir por WhatsApp |
| Ver quién entró a mi casa | Sí, en Accesos | Sí, con **aviso push** al entrar |
| Paquetes | Sí | Sí, con aviso push |
| Pagar la cuota | Sí (Wompi, en prueba) | Sí, por el checkout web de Wompi |
| Reservas | Sí | Sí |
| Vehículos y personas de mi casa | Sí | Sí |
| Ingreso con código por WhatsApp | **No** | Sí |

La visita no instala nada. Recibe el KEY en un enlace web con QR (`proyecto.md`, decisiones tomadas).

## Qué falta, por bloque

### 1. Backend y API

| Falta | Detalle | Dueño |
|---|---|---|
| API REST versionada (`/api/v1`) | Laravel Sanctum con token por dispositivo. Reusa modelos y políticas de Filament | Programador |
| Contrato OpenAPI | Archivo `openapi.yaml` en el repositorio del código. La app se genera contra él | Programador |
| Aislamiento por comunidad en la API | Hoy abrir otra comunidad cierra la sesión (R9). La API debe responder 403, no cerrar sesión | Programador |
| Ingreso por WhatsApp | Código de un solo uso con plantilla de autenticación de WhatsApp Business. Teléfono único (`proyecto.md`) | Programador |
| Registro de dispositivos para push | Tabla de tokens FCM y APNs por usuario | Programador |
| Eventos que disparan push | Entrada de un KEY, paquete recibido, cobro nuevo. El evento de puerta ya llega (A4) | Programador |
| Dónde vive el código y de quién es | Pendiente desde D-003 | Alejandro |

### 2. Arreglos que la app hereda si no se hacen antes

| Arreglo | Por qué bloquea | Fuente |
|---|---|---|
| Quitar el correo obligatorio en el alta a HikCentral | Hoy obliga a inventar correos (A6) y tumbó a Refugio | `proyecto.md`, hechos vigentes; A6 |
| KEY sin crear un usuario permanente | La app vendería el KEY como algo que no es | A5 |
| Definir quién aprueba un KEY «Pendiente» | La regla del canon es que el residente autoriza | R4 |
| Una sola regla de datos mínimos en Crear KEY | La pantalla se contradice | R2 |
| KEY temporal en HikCentral | Usar la reserva de visitas del OpenAPI de HikCentral Professional (sección «Visitor Management»), no `add_person`. **Por verificar** con la versión instalada en Villas | [Guía OpenAPI 2.6.1](https://pinfo.hikvision.com/hkwsen/unzip/20240806113350_60387_doc/HikCentral%20Professional%20OpenAPI%20V2.6.1_Developer%20Guide_V2.6.1_20240806.pdf), consultada 16 nov 2026 |

### 3. Cuentas y trámites

| Trámite | Costo | Tiempo | Bloquea |
|---|---|---|---|
| Sociedad de Kino (SAS) con NIT | Sin dato | Sin dato | Cuenta de empresa en Apple y contrato con Wompi |
| Número D-U-N-S | Gratis | 1 a 2 semanas | Cuenta de empresa en Apple |
| Apple Developer Program, cuenta de empresa | USD 99 al año | Días a semanas | Publicar en App Store |
| Google Play Console, cuenta de empresa | USD 25, una vez | Días | Publicar en Google Play |
| WhatsApp Business Platform (Meta) | Cobro por mensaje de autenticación; tarifa de Colombia **por verificar** | Verificación del negocio: días | Ingreso por WhatsApp |
| Firebase (FCM) y llave APNs | Gratis | Horas | Push |
| Wompi, cuenta productiva | Comisión por transacción **por verificar** | Sin dato | Cobrar cuotas reales |

Las cuentas deben quedar a nombre de Kino, no de una persona. Si una persona se va, la app no se pierde.

### 4. Reglas de las tiendas que afectan el diseño

| Regla | Efecto en Kino |
|---|---|
| Apple exige borrar la cuenta desde la app si la app permite crearla | Botón «Eliminar mi cuenta» en el perfil |
| La cuota de administración es un servicio fuera de la app | Se cobra con Wompi, sin la compra integrada de Apple ni Google |
| Apple pide una cuenta de prueba para revisar | Crear un residente de prueba en una comunidad de demostración, no en Villas |
| Política de privacidad pública y aviso de datos personales (Ley 1581 de 2012) | Ya existe `soykino.com/politica-de-privacidad.html`; revisar que cubra la app y la ubicación si se usa |

### 5. Tecnología propuesta (D-016)

| Opción | A favor | En contra |
|---|---|---|
| **A · React Native con Expo, en TypeScript (recomendada)** | TypeScript es la regla del repositorio (`kino/codigo/README.md`). Una base para iOS y Android. EAS compila y publica sin Mac propio. Actualizaciones sin pasar por la tienda para cambios de JavaScript | Una capa más que aprender si el programador solo sabe PHP |
| B · Flutter | Rendimiento y diseño consistentes | Otro lenguaje (Dart); rompe la regla de TypeScript |
| C · Envolver la web actual (Capacitor) | Lo más rápido: días | Filament no está hecho para celular; push y WhatsApp quedan a medias; Apple puede rechazar una web envuelta |
| D · Nativo puro (Swift y Kotlin) | Máximo control | Dos apps, el doble de trabajo |

### 6. Diseño

| Falta | Fuente |
|---|---|
| Pantallas móviles del residente en Figma con la marca nueva | D-004 B; la marca nueva aún no tiene archivo en `kino/marca/README.md` |
| Ícono, pantalla de inicio y capturas para las tiendas | Sin fuente |
| Textos en español y con el vocabulario del canon (KEY, visita, nunca «permiso») | `proyecto.md` |

Si la marca no llega a tiempo, la app sale con una base neutra y tokens cambiables. **Costo:** un segundo pase de diseño antes de la versión pública.

### 7. Pruebas

| Prueba | Con quién | Criterio de salida |
|---|---|---|
| Pruebas automáticas de la API | Programador | Cada endpoint con su prueba; aislamiento entre comunidades probado |
| TestFlight y prueba interna de Play | 10 casas de Villas, con colaboradores | 30 KEY creados y usados en la puerta en 2 semanas |
| Prueba del KEY en la puerta | Portería de Villas | El evento de entrada queda ligado al KEY y llega el push |

### 8. Fase 2 (después de la primera versión)

1. App o modo tableta de **portería** con lectura de QR.
2. Modo **colaborador**: la empleada o el jardinero ve sus KEY recurrentes.
3. Notificaciones a la administración.

## Riesgos

| Riesgo | Señal | Acción |
|---|---|---|
| Apple tarda con la cuenta de empresa | Sin D-U-N-S en la semana 2 | Publicar primero en Google Play |
| El KEY temporal no entra a HikCentral | La reserva de visitas no existe en la versión de Villas | Usar QR validado por portería mientras tanto; no prometer apertura automática |
| Nadie usa el KEY (hoy: 1 en Villas) | Menos de 30 KEY en la prueba | Entrevistar a 5 residentes antes de seguir |
