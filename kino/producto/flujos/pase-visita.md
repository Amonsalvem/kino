# Pase de visita: Acceso previsto

El recorrido describe una propuesta de servicio elegida en Kino Ops, no una función verificada en producción. El residente prepara el Pase antes de la llegada; la administración fija los límites y no aprueba cada ingreso. Fuentes: inventario externo de Kino Ops y `kino/canon/proyecto.md`.

| Actor | Paso | Pantalla | Regla de negocio | Dato que se guarda |
|---|---|---|---|---|
| Residente | Crea el Pase: quién viene, para qué y hasta cuándo | Crear Pase; identificador de frame: sin fuente | El residente autoriza dentro de los límites de la administración | Autor, persona esperada, motivo, vigencia y modo; persistencia técnica: sin fuente |
| Residente y visita | Comparte el Pase; la visita recibe QR, nombre, autorización y vigencia en el celular | Pase recibido; identificador de frame: sin fuente | La visita recibe un Pase sin cuenta; la validación no depende de mensajes a portería | Pase emitido; registro del envío: sin fuente |
| Visita y portería | La visita presenta el Pase; portería lo valida y el lector habilita el ingreso | Validación en portería; identificador de frame: sin fuente | La autorización procede del residente; la apertura física depende del lector, no de una decisión del vigilante | Validación y evento de ingreso vinculados al Pase; esquema: sin fuente |
| Residente | Recibe confirmación de quién entró y a qué hora | Aviso de llegada; identificador de frame: sin fuente | El aviso requiere confirmación del evento de entrada; no se presupone implementado | Persona, hora y referencia al Pase; entrega del aviso: sin fuente |

Fuente del recorrido: inventario de Kino Ops, fuera del repositorio. Campos de autor, motivo, vigencia y modo, visita sin cuenta, límites y función del lector: `kino/canon/proyecto.md`. La columna de datos es una especificación propuesta, no una descripción de la base de datos actual.

## Trazabilidad e integración

El Pase conserva autor, motivo y vigencia. La validación en portería deja de depender de buscar un chat. El relato dice que ocurre en segundos; no hay medición que permita prometer un tiempo de respuesta. Fuente: brief de Kino Ops, fuera del repositorio.

QR, placa y código de un solo uso conviven según `kino/canon/proyecto.md`. La sincronización con HikCentral está documentada para altas permanentes. Para el Pase temporal de este recorrido hay **sin fuente de implementación**. El aviso requiere el evento del lector, pendiente ya señalado en `pre-kino/decisiones.md`, F4-P2; esa referencia histórica no aprueba una función nueva.

## Carriles del servicio

| Momento | Residente | Visita | Portería | Administración | Sistema |
|---|---|---|---|---|---|
| Preparación | Define el Pase | Aún no llega | No interviene | Fija límites | Registra autor, motivo y vigencia |
| Entrega | Comparte el Pase | Lo recibe sin cuenta | No busca mensajes | No aprueba caso a caso | Presenta el Pase |
| Llegada | Ya autorizó | Presenta el Pase | Valida | Mantiene los límites | Aplica la validación mediante el lector |
| Confirmación | Consulta quién entró y cuándo | Completa el ingreso | No sustituye al lector | Puede consultar trazabilidad; detalle de pantalla: sin fuente | Requiere evento de entrada confirmado |

Fuente: síntesis propuesta del recorrido del inventario de Kino Ops y reglas de `kino/canon/proyecto.md`. El carril del sistema no acredita funciones existentes. Colaboradores conservan la misma prioridad que visitas; este archivo recorta solo el caso de visita. Propuestas comerciales y de piloto: D-005 y D-006, pendientes en `kino/canon/decisiones.md`.
