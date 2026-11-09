# Kino · Roadmap, estrategia de servicio y presupuesto

BORRADOR, 8 nov 2026. Co-creación de Alejandro con Claude, sobre el documento de Nico con Grok. Alejandro aprueba (D-003).

BORRADOR actualizado el 9 nov 2026 con los datos de presupuesto de Alejandro.

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
| Tamaño | 100 a 400 unidades construidas, como Villas Campestres (100) y Refugio Campestre (400) | Con 28 a 61 unidades se cubren los costos fijos (Bloque 5) |
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

Horizonte: nov 2026 a dic 2027, 14 meses. Fuente: Alejandro, chat del proyecto, 9 nov 2026. EAFIT no pide un formato de presupuesto (misma fuente).

**Supuestos**

| Supuesto | Valor | Fuente |
|---|---|---|
| Tasa de cambio | $3.300 por USD | Techo del rango de $3.120 a $3.300 que prevé Bancolombia para nov 2026, según [El Colombiano](https://www.elcolombiano.com/inicio/dolar-colombia-proyeccion-tasa-cambio-noviembre-2026-GF43201403). TRM del 4 nov 2026: $3.235,59, según [dolar-colombia.com](https://www.dolar-colombia.com/2026-11-04). Se usa el techo para no quedarse corto |
| Equipo | Nadie cobra. Todos son socios | Alejandro, 9 nov 2026 |
| Fuente de dinero | Capital propio | Alejandro, 9 nov 2026 |
| Unidades | Villas Campestres: 400 totales, 100 construidas. Refugio Campestre: 680 totales, 400 construidas | Alejandro, 9 nov 2026 |
| Unidad que paga | Solo la unidad construida | Inferido: un lote sin casa no recibe visitas ni colaboradores |

### 5.1 Inversión ya hecha

| Rubro | Valor (COP) | Fuente |
|---|---|---|
| Registro de marca, una clase | 1.200.000 | Alejandro, 9 nov 2026 |

### 5.2 Costos fijos mensuales

| Rubro | USD al mes | COP al mes | Fuente del precio |
|---|---|---|---|
| Claude Pro, 1 cuenta | 20 | 66.000 | [Anthropic](https://support.anthropic.com/en/articles/8325610-how-much-does-claude-pro-cost), consulta 9 nov 2026 |
| Grok, 1 cuenta | 30 | 99.000 | Alejandro, 9 nov 2026 |
| Figma Professional, 1 puesto, pago mensual | 20 | 66.000 | Pago mensual: Alejandro, 9 nov 2026. Precio: [Foro de Figma](https://forum.figma.com/report-a-problem-6/why-does-the-professional-plan-price-change-at-checkout-57528) |
| Hospedaje de la página web | 20 | 66.000 | Alejandro, 9 nov 2026 |
| AWS (app) | Sin detalle | Sin detalle | Alejandro, 9 nov 2026: aún no hay costo detallado. Se agrega con la primera factura |
| Mensajes de WhatsApp para el ingreso | ≈ 1 | ≈ 3.300 | Cálculo abajo |
| **Total conocido** | **≈ 91** | **≈ 300.300** | Sin AWS |

**Cálculo de WhatsApp (inferido).** 500 unidades construidas × 2 ingresos a la app al mes = 1.000 mensajes. A USD 0,001 por mensaje son USD 1 al mes. Fuente del precio: [Chatalog](https://docs.chatalog.ai/platform-setup/whatsapp-connection-guide/whatsapp-pricing-update), consulta 8 nov 2026. El residente comparte el Pase desde su propio WhatsApp; ese envío no tiene costo para Kino.

### 5.3 Costos que el roadmap agrega

| Rubro | Valor (COP) | Estado |
|---|---|---|
| Política de tratamiento de datos y contrato tipo (abogado) | Pendiente | Sin cotización. Es obligatoria antes de escalar la biometría (Bloque 3) |
| Hardware HikCentral | 0 | Lo pagó Monte Sereno; no entra al presupuesto de Kino (Alejandro, 9 nov 2026) |
| Imprevistos | 10 % de los costos | Propuesta; Alejandro decide |

### 5.4 Costo total a dic 2027

```
Inversión ya hecha        1.200.000
Fijos conocidos  300.300 × 14 meses = 4.204.200
Imprevistos 10 % de fijos              420.420
──────────────────────────────────────────────
Total conocido                        5.824.620 COP
+ AWS × 14 meses (sin detalle)
+ abogado (sin cotización)
```

### 5.5 Ingresos: tres escenarios

El precio de Kino no está decidido. Se modela con tres precios por unidad construida al mes. El más alto es la tarifa por villa del competidor ($10.900). Fuente: deck histórico, lám. 32.

**Referencia (inferido).** El competidor cobra además una base de $1.550.000 al mes. En Villas Campestres (100 casas) eso suma $2.640.000 al mes: $26.400 por casa construida. Para un conjunto pequeño la base pesa más que la tarifa por villa. Kino puede competir sin base.

| Escenario | Precio por unidad | Conjuntos y meses que pagan | Ingreso a dic 2027 (COP) |
|---|---|---|---|
| Conservador | $5.000 | Villas Campestres (100) desde abr 2027, después de H3: 9 meses | 4.500.000 |
| Base | $8.000 | Villas (100) desde mar 2027: 10 meses. Refugio (400) desde jul 2027: 6 meses | 8.000.000 + 19.200.000 = 27.200.000 |
| Optimista | $10.900 | Villas desde mar 2027 (10 meses), Refugio desde jul 2027 (6 meses) y un conjunto nuevo de 200 unidades (supuesto) desde oct 2027 (3 meses) | 10.900.000 + 26.160.000 + 6.540.000 = 43.600.000 |

Las fechas de inicio salen del roadmap: H2 (mar 2027) y H3 (abr 2027). Refugio paga solo cuando su sincronización esté reparada. No se incluye cobro de implementación: su valor está pendiente.

### 5.6 Resultado y punto de equilibrio

| Escenario | Ingresos | Costo conocido | Resultado a dic 2027 |
|---|---|---|---|
| Conservador | 4.500.000 | 5.824.620 | −1.324.620 |
| Base | 27.200.000 | 5.824.620 | +21.375.380 |
| Optimista | 43.600.000 | 5.824.620 | +37.775.380 |

Resultados sin AWS ni abogado. Sin impuestos.

```
Punto de equilibrio mensual = costo fijo mensual ÷ precio por unidad
  a $5.000   → 300.300 ÷ 5.000  = 61 unidades
  a $8.000   → 300.300 ÷ 8.000  = 38 unidades
  a $10.900  → 300.300 ÷ 10.900 = 28 unidades
```

Villas Campestres sola (100 casas) cubre los costos fijos con cualquiera de los tres precios. Inferido, sin AWS.

### 5.7 El riesgo que el presupuesto no muestra

El costo bajo depende de que nadie cobre. Seis socios trabajan sin sueldo. Si el equipo necesita ingresos, cada sueldo S exige S ÷ precio unidades más. Ejemplo: un sueldo de $2.000.000 a $8.000 por unidad exige 250 unidades más. Esto define cuántos conjuntos necesita Kino para que el equipo pueda vivir de él. Inferido.

### 5.8 Fuera del presupuesto

| Rubro | Motivo | Fuente |
|---|---|---|
| Hardware HikCentral | Lo pagó Monte Sereno | Alejandro, 9 nov 2026 |
| Desplazamientos | No se incluyen | Alejandro, 9 nov 2026 |
| AWS | Sin costo detallado todavía | Alejandro, 9 nov 2026 |
| Sueldos | Los socios no cobran | Alejandro, 9 nov 2026 |

---|---|
| A | ¿Cuánto factura AWS al mes? |
| B | ¿Cuánto cuesta cada viaje a El Retiro? |
| C | ¿El hardware HikCentral lo pagó el conjunto? ¿Monte Sereno paga algo hoy? |
| D | Confirmar el plan de Grok y si Figma se paga mensual o anual |

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
