# Kino · Roadmap, estrategia de servicio y presupuesto

BORRADOR, 8 nov 2026. Co-creación de Alejandro con Claude, sobre el documento de Nico con Grok. Alejandro aprueba (D-003).

**Etiquetas.** *Observado*: está en la inspección o en una lectura pública. *Canon*: está en `kino/canon/`. *Inferido*: deducción del equipo, sin prueba. *Pendiente*: falta un dato; nadie lo inventa.

```
Bloque 1  Estrategia de servicio     ¿Qué resolvemos y para quién?
Bloque 2  Salida al mercado          ¿A quién vendemos primero y cómo?
Bloque 3  Expansión                  ¿Cuándo y hacia dónde crecemos?
Bloque 4  Roadmap                    ¿En qué orden y en qué fechas?
Bloque 5  Presupuesto                ¿Cuánto cuesta y cuánto entra?
Bloque 6  Medición                   ¿Cómo sabemos que funciona?
```

---

## Bloque 1 · Estrategia de servicio

### 1.1 Problema

Hoy la persona que conoce a la visita (el residente) no tiene la autoridad para dejarla entrar. La persona con autoridad (portería y administración) no la conoce. El ingreso se resuelve por chat, llamada y cuaderno. Fuente: `kino/canon/proyecto.md`, hechos vigentes; `kino/investigacion/sintesis/2026-11-04-flujo-informal-acceso.md`.

**Pregunta guía.** ¿Cómo reunir conocimiento y autoridad para decidir quién entra? Fuente: canon.

### 1.2 Propuesta de valor por actor

| Actor | Hoy | Con Kino | Fuente |
|---|---|---|---|
| Residente | Llama a portería o manda un chat | Prepara un Pase para su visita o su colaborador, dentro de los límites de la administración | Canon |
| Visita | Espera mientras portería llama a la casa | Recibe el Pase sin cuenta: QR, placa o código de un solo uso | Canon |
| Colaborador | Entra por costumbre o por llamada, cada día | Recibe un Pase con vigencia y franja. Es el ingreso más frecuente | Canon; D-005 A |
| Portería | Llama, anota y decide sin saber | Valida el Pase. El lector abre la puerta | Canon |
| Administración | Aprueba altas una por una; ve poco | Fija cupos, duración y franjas. Ve autor, motivo y vigencia de cada ingreso | Canon |
| Consejo de administración | Recibe quejas sin datos | Recibe un informe de quién entró, cuándo y con autorización de quién | Inferido |

### 1.3 Diferencia frente a la competencia

La autonomía del residente no diferencia a Kino: Neivor ya la ofrece. Fuente: canon, regla 5. Kino se diferencia en tres cosas juntas:

```
        ┌──────────────────────────────┐
        │  1. Integración probada con  │
        │  el hardware del conjunto    │
        │  (HikCentral: placa, rostro, │
        │  talanquera)                 │
        └──────────────┬───────────────┘
                       │
   ┌───────────────────┼───────────────────┐
   │                   │                   │
┌──┴─────────────┐          ┌──────────────┴──┐
│ 2. Pase sin    │          │ 3. Autoridad del │
│ cuenta para la │          │ residente dentro │
│ visita         │          │ de los límites   │
│                │          │ de la admin.     │
└────────────────┘          └─────────────────┘
```

**Riesgo.** El pilar 1 todavía no está probado para el Pase temporal. Refugio Campestre tiene 0 de 312 usuarios sincronizados. Los 711 errores de HikCentral vienen del campo correo. Fuente: canon, hechos vigentes. Mientras el pilar 1 no esté probado, Kino no puede venderlo como hecho.

### 1.4 Qué compra el conjunto

Kino vende un servicio de tres partes. Fuente: momentos de implementación del documento de Nico (PDF comercial, pág. 10).

```
PRODUCTO            INTEGRACIÓN              ACOMPAÑAMIENTO
App y panel    +    Conexión con el     +    5 momentos por conjunto:
                    hardware que ya          Diagnóstico → Configuración →
                    tiene el conjunto        Capacitación → Operación
                                             asistida → Soporte
```

### 1.5 Recorrido del Pase

Formato: actor → paso → pantalla → regla de negocio → dato que se guarda. Fuente: `kino/producto/flujos/pase-visita.md` y canon.

| Actor | Paso | Pantalla | Regla de negocio | Dato que se guarda |
|---|---|---|---|---|
| Residente | Entra a la app | Ingreso con código por WhatsApp | Teléfono obligatorio y único | Sesión, teléfono |
| Residente | Crea el Pase | Acceso previsto | Debe caber en cupo, duración y franja de la administración | Autor, motivo, vigencia, modo |
| Residente | Comparte el Pase | Compartir | La visita no crea cuenta | Envío |
| Visita o colaborador | Llega a la puerta | QR, placa o código | El lector valida, no el vigilante | Evento del lector |
| Portería | Atiende la excepción | Panel de portería | Sin Pase válido, se llama al residente | Excepción manual |
| Administración | Revisa | Bitácora | Nadie edita un registro | Historial |

**Brecha observada.** El ingreso público de la app pide correo, contraseña o Google. El canon pide código por WhatsApp. Fuente: documento de Nico, §6, lectura pública de la app del 8 nov 2026. El roadmap la incluye como tarea (Bloque 4).

---

## Bloque 2 · Salida al mercado

### 2.1 Quién compra y quién decide

Solo la administración del conjunto compra Kino. Fuente: canon. En propiedad horizontal la decisión pasa por tres instancias:

```
Administrador ──propone──► Consejo ──recomienda──► Asamblea ──aprueba presupuesto──► Contrato
   (usuario y                (evalúa)               (vota el gasto
    comprador)                                       del año)
```

La asamblea aprueba el presupuesto del conjunto. La reunión ordinaria se hace una vez al año, en los tres meses siguientes al cierre del período presupuestal. Fuente: [Ley 675 de 2001](http://www.secretariasenado.gov.co/senado/basedoc/ley_0675_2001.html), arts. 38 y 39.

**Efecto en la venta (inferido).** Si el período cierra en diciembre, la asamblea se hace entre enero y marzo. Un conjunto que conoce Kino en noviembre puede incluirlo en el presupuesto de 2027. Un conjunto que lo conoce en abril espera un año o paga con un rubro que ya existe, como seguridad. **Pendiente:** confirmar con Manuel o con un administrador cómo se aprobó el gasto en Monte Sereno.

### 2.2 Perfil del primer cliente

Hipótesis para validar con 5 administradores. Inferido a partir del piloto.

| Criterio | Perfil | Por qué |
|---|---|---|
| Tipo | Conjunto campestre o parcelación | Monte Sereno, El Retiro, es de este tipo |
| Zona | Oriente antioqueño: El Retiro, Rionegro, La Ceja, Llanogrande | Distancia corta para implementar y dar soporte |
| Hardware | Ya tiene lector de placa o de rostro sobre HikCentral | Kino conecta lo que el conjunto ya pagó |
| Tamaño | Pendiente: rango de unidades | Se fija con el costo de implementación (Bloque 5) |
| Dolor | Visitas y colaboradores frecuentes, portería que llama a la casa | Es el problema del diagnóstico |

### 2.3 Cabeza de playa

```
Paso 1  Monte Sereno Villas Campestres   Uso actual declarado (D-006 A)
          │  medir, publicar el caso
          ▼
Paso 2  Refugio Campestre                Hardware instalado, integración caída (canon)
          │  reparar la sincronización
          ▼
Paso 3  Conjuntos vecinos del oriente    Con HikCentral; llegan por referido
          ▼
Paso 4  Medellín y Valle de Aburrá       Solo con el servicio estandarizado
```

Refugio es el segundo cliente natural: tiene el hardware y ya conoce el problema. Inferido. Reparar su sincronización prueba el pilar 1 de la diferencia.

### 2.4 Canales de adquisición

| Canal | Cómo funciona | Costo | Estado |
|---|---|---|---|
| Referido de administradores | Un administrador lleva varias copropiedades y recomienda a otros | Bajo | Inferido; validar con entrevistas |
| Instaladores de HikCentral | El instalador vende hardware; Kino le da el software que lo hace útil | Comisión, pendiente | Inferido; sin alianza firmada |
| Caso del piloto | Informe con datos medidos de Monte Sereno | Bajo | Depende de H3 |
| soykino.com y redes | Pedido de demostración | Bajo | Sitio observado en línea |
| Eventos de propiedad horizontal | Charlas a administradores | Medio, pendiente | Sin contacto |

### 2.5 Embudo de venta

```
Contacto ─► Diagnóstico gratuito ─► Propuesta ─► Consejo ─► Asamblea ─► Implementación
           (momento 01: usuarios,    (precio por
            vehículos, hardware)      unidad)
```

El diagnóstico gratuito sirve también para la venta: muestra al conjunto su propio problema con datos. Inferido.

### 2.6 Modelo de ingresos

Estructura del documento de Nico (deck histórico, lám. 32). Las cifras están pendientes.

| Ingreso | Cuándo se cobra | Cifra |
|---|---|---|
| Implementación | Una vez, al empezar | Pendiente |
| Suscripción por unidad | Cada mes, dentro de la cuota de administración | Pendiente |
| Módulos (paquetería, reservas, pagos) | Cada mes, según etapa de producto | Pendiente |

**Referencia de mercado.** Un competidor cobra $1.550.000 al mes de base más $10.900 por villa al mes, con contrato a 60 meses. Fuente: deck histórico, lám. 32, citado en el documento de Nico, PA-M11. No es el precio de Kino.

**Método de precio.** Precio por unidad = (costos fijos + costos variables del conjunto) ÷ unidades + margen. Fuente: deck histórico, lám. 31 y 32. El margen está pendiente.

---

## Bloque 3 · Expansión

Kino crece en dos ejes: más conjuntos y más módulos. Cada paso tiene una condición. Sin la condición, el paso no empieza.

```
            MÓDULOS
              ▲
  Etapa 05    │                                ● Escala comercial
  Etapa 04    │                        ● Seguridad y bienestar
  Etapa 03    │                ● Paquetería y reservas
  Etapa 02    │        ● Portal de admin. y residentes
  Etapa 01    ● Acceso (hoy)
              └──────┬─────────┬──────────┬───────────► CONJUNTOS
                  1 conjunto  2-3 del    10+ del
                  (piloto)    oriente    oriente y Valle de Aburrá
```

| Paso | Condición para empezar | Fuente de la condición |
|---|---|---|
| De 1 a 2 conjuntos | El Pase temporal genera evento del lector en Monte Sereno | Canon; documento de Nico, §11 |
| De 2 a 10 conjuntos | Precio v1 probado y costo de implementación medido en 2 conjuntos | Documento de Nico, fase 4 |
| Etapa 02 | Etapa 01 estable: errores de sincronización por debajo de un umbral | Umbral pendiente |
| Etapa 03 | Clientes que pidan el módulo y paguen por él | Inferido |
| Etapa 04 | Revisión legal de biometría y datos de salud | Documento de Nico, fase 8 |

**Fuera del roadmap.** Marca blanca: Kino mantiene su marca. El conjunto aparece solo como dato en texto o chip. Decisión de Alejandro del 8 nov 2026, D-009.

---

## Bloque 4 · Roadmap

Fases del documento de Nico, sin la fase 6 (marca blanca, D-009). Las fechas vienen del Gantt del 28 oct 2026 y son propuestas, no aprobadas.

```
                    2026        2027
                    nov  dic │ ene  feb  mar │ abr  may  jun │ jul  ago  sep │ oct  nov  dic
Fase 3 Piloto       ████████████████████████
  Login WhatsApp    ████████
  Pase temporal         ████████████
  Colaboradores              ████████
Fase 4 Precio            ████████████
Fase 5 Lanzamiento  ██                ████
Fase 7 Escalar                             ████████████████████████████████████████
Fase 8 Legal        ████████████
Hitos               H1                 H2   H3                                       H5
```

| Hito | Fecha propuesta | Se cumple cuando | Estado al 8 nov |
|---|---|---|---|
| H1 · soykino.com | nov 2026 | Sitio en línea con HTTPS y correo | Observado en línea |
| H2 · Cierre de la beta y de la etapa 01 | mar 2027 | Login por WhatsApp, Pase temporal con evento del lector y KPI medidos cada semana | No cumplido |
| H3 · Informe del piloto | abr 2027 | Resultados medidos y caso publicado | No cumplido |
| H4 | Retirado | Era la app de marca blanca | D-009 |
| H5 · Nuevos conjuntos | dic 2027 | Número de conjuntos pendiente | No cumplido |

### Tareas nuevas frente al documento de Nico

| Tarea | Por qué | Responsable propuesto (D-007) |
|---|---|---|
| Ingreso con código por WhatsApp | Brecha entre la app observada y el canon | Alejandro, Manuel |
| Quitar el correo obligatorio | Causa los 711 errores de HikCentral | Alejandro, Daniel |
| Pase temporal con evento del lector | Sin esto no se prueba la diferencia | Alejandro, Daniel |
| Pase de colaborador con franja | Es el ingreso más frecuente | Alejandro |
| Registro validado contra la cédula | El administrador no aprueba el registro | Alejandro |
| Reparar la sincronización en Refugio Campestre | Segundo cliente y prueba del pilar 1 | Daniel, Manuel |
| Entrevistas a 5 administradores | Validar perfil, canales y precio | Juan Esteban, Nico |

---

## Bloque 5 · Presupuesto

**Estado: estructura lista, cifras pendientes.** Las celdas «Pendiente (n)» esperan la respuesta n de Alejandro en el chat del 8 nov 2026. Las cifras públicas llevan fuente y fecha de consulta.

### 5.1 Inversión inicial (una vez)

| Rubro | Valor (COP) | Fuente |
|---|---|---|
| Registro de marca, primera clase, en línea | ≈ 1.347.500 | [Guía Uniandes](https://derecho.uniandes.edu.co/wp-content/uploads/2025/09/Como-Registrar-mi-Marca.pdf) y [cuantomecuesta.com](https://cuantomecuesta.com/co/registro-marca/), consulta 8 nov 2026. Fuente secundaria: confirmar en sic.gov.co |
| Registro de marca, cada clase adicional | ≈ 673.500 | Mismas fuentes |
| Número de clases | Pendiente (6) | Raw, con abogado |
| Honorarios legales: política de datos y contrato tipo | Pendiente (6) | Sin cotización |
| Diseño externo (Zulu) | Pendiente (3) | Sin cotización |

### 5.2 Costos fijos mensuales

| Rubro | Valor mensual (COP) | Fuente |
|---|---|---|
| AWS (sitio y app) | Pendiente (4) | Factura de AWS |
| Dominio soykino.com (anual ÷ 12) | Pendiente (4) | Registrador |
| Correo del equipo | Pendiente (4) | Proveedor y número de cuentas |
| Figma y otras suscripciones | Pendiente (4) | Facturas |
| Mensajes de WhatsApp para el ingreso | ≈ USD 0,0008 a 0,0010 por mensaje en Colombia | [Sleekflow](https://help.sleekflow.io/en_US/pricing) y [Chatalog](https://docs.chatalog.ai/platform-setup/whatsapp-connection-guide/whatsapp-pricing-update), consulta 8 nov 2026. Fuente secundaria: confirmar en la cuenta de Meta |
| Equipo (6 personas) | Pendiente (3) | Valor por persona |

**Inferido.** El costo de WhatsApp es bajo: 10.000 ingresos al mes cuestan unos USD 10. El costo grande es el equipo.

### 5.3 Costo variable por conjunto

Fórmula: horas de cada momento × valor hora + desplazamientos + hardware si lo pone Kino.

| Momento | Horas | Valor hora | Total |
|---|---|---|---|
| 01 Diagnóstico | Pendiente | Pendiente (3) | Pendiente |
| 02 Configuración e integración | Pendiente | Pendiente (3) | Pendiente |
| 03 Capacitación | Pendiente | Pendiente (3) | Pendiente |
| 04 Operación asistida | Pendiente | Pendiente (3) | Pendiente |
| 05 Soporte mensual | Pendiente | Pendiente (3) | Pendiente |
| Hardware | ¿Lo paga el conjunto? Pendiente (5) | | |

La primera ficha de costeo sale de Monte Sereno Villas Campestres. Fuente: documento de Nico, PA-M12.

### 5.4 Ingresos y punto de equilibrio

```
Ingreso mensual   = Σ conjuntos × (unidades × precio por unidad)
Costo mensual     = costos fijos + Σ soporte por conjunto
Punto de equilibrio: conjuntos necesarios = costos fijos ÷ (ingreso por conjunto − soporte por conjunto)
```

| Escenario a dic 2027 | Conjuntos | Unidades por conjunto | Precio por unidad | Ingreso mensual |
|---|---|---|---|---|
| Conservador | Pendiente (7) | Pendiente (5) | Pendiente | Pendiente |
| Base | Pendiente (7) | Pendiente (5) | Pendiente | Pendiente |
| Optimista | Pendiente (7) | Pendiente (5) | Pendiente | Pendiente |

### 5.5 Fuentes de dinero

Pendiente (7): capital propio, socios, convocatoria u otra fuente.

### 5.6 Imprevistos

Propuesta: 10 % del total de costos. Inferido; Alejandro decide el valor.

---

## Bloque 6 · Medición

Se conservan los KPI PA-M01 a PA-M12 del documento de Nico, con sus fórmulas y metas académicas propuestas. Cambios:

| Cambio | Por qué |
|---|---|
| PA-M06 se reporta en tres cifras: placas sincronizadas, excepciones manuales y Pases confirmados por el lector | Una sola cifra ocultaría que el Pase temporal no está probado |
| Nuevo: Pases de colaborador ÷ Pases emitidos | Los colaboradores tienen la misma prioridad que la visita (D-005 A) |
| Nuevo: errores de sincronización por semana | Condición para pasar a la etapa 02 |
| Nuevo: costo de adquisición por conjunto | Gasto comercial ÷ conjuntos firmados |
| Nuevo: meses para recuperar la implementación | Costo de implementación ÷ margen mensual del conjunto |
| PA-M04 mide la marca nueva, no el manual v2 de pre-kino | D-001 y D-004 B |

---

## Cambios frente al documento de Nico

| Documento de Nico | Esta versión | Fuente |
|---|---|---|
| D-004 y D-007 como propuesta | APROBADAS el 8 nov 2026 | `kino/canon/decisiones.md` |
| Herencia de Poppins y paleta de los decks | Se quita: lo visual empieza de cero | D-004 B; D-002 |
| Fase 6 y H4 de marca blanca | Se retiran | D-009 |
| «Super Admin aprueba cuentas» | El registro se valida contra la cédula | Canon |
| Colaboradores casi ausentes | Misma prioridad que la visita | Canon; D-005 A |
| Sin mercado, canales, precio ni presupuesto | Bloques 2, 3 y 5 | Este documento |
