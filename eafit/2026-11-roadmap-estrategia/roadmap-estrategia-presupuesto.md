# Kino · Roadmap, estrategia de servicio y presupuesto

BORRADOR, 8 nov 2026. Co-creación de Alejandro con Claude, sobre el documento de Nico con Grok. Alejandro aprueba (D-003).

BORRADOR actualizado el 9 nov 2026 con los datos de presupuesto de Alejandro y su PDF de costos.

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
| Tamaño | 150 unidades construidas o más | El costo en efectivo exige de 154 a 335 unidades que paguen (Bloque 5) |
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

**Referencia de mercado.** Un competidor cobra $1.550.000 al mes de base más $10.900 por villa al mes, con contrato a 60 meses. Fuente: deck histórico, lám. 32, citado en el documento de Nico, PA-M11. Alejandro identifica este competidor como Unita y fija, por ahora, el precio de Kino igual al suyo (chat del proyecto, 9 nov 2026). El contrato a 60 meses no se adopta: falta decidirlo.

**Método de precio.** Precio por unidad = (costos fijos + costos variables del conjunto) ÷ unidades + margen. Fuente: deck histórico, lám. 31 y 32. El margen está pendiente.

### 2.7 Modelos de ingreso evaluados

Pedido de Alejandro, 9 nov 2026: buscar el modelo más rentable sin limitarse al cobro por unidad. Alejandro eligió B + E, con D desde la etapa 03 (D-010).

**Ancla de valor.** Un puesto de vigilancia 24 horas cuesta al conjunto entre $17,1 y $19,6 millones al mes en 2026. Fuente: [Noticias RCN](https://www.noticiasrcn.com/economia/la-supervigilancia-fijo-tarifas-minimas-de-vigilancia-para-2026-989255) y [El Espectador](https://www.elespectador.com/economia/tarifas-de-vigilancia-y-seguridad-privada-en-2026-asi-suben-los-precios/), consulta 9 nov 2026. Kino a $8.000 por casa en Villas Campestres (100 casas) cobra $800.000: el 4,5 % de un puesto. Inferido: el precio por unidad deja valor sin cobrar.

**Costo marginal.** Una casa más casi no sube el costo: AWS y el trabajo son fijos (Bloque 5). Inferido: cada peso de ingreso nuevo después del equilibrio es margen.

| Modelo | Cómo cobra | Villas + Refugio (500 casas), al mes | Rentabilidad | Riesgo |
|---|---|---|---|---|
| A · Por unidad (actual) | $8.000 por casa construida | 4.000.000 | Media. Un conjunto pequeño casi no paga | Bajo |
| B · Piso + unidad | $1.000.000 por conjunto + $8.000 por casa | 1.800.000 + 4.200.000 = 6.000.000 | Alta. El piso cubre el soporte de cada conjunto | Bajo. Es el esquema del competidor, con piso menor |
| C · Por valor | El mayor entre el 10 % de un puesto 24 h (≈ $1.800.000) y $8.000 por casa | 1.800.000 + 3.200.000 = 5.000.000 | Alta. Se vende contra el gasto en vigilancia | Medio. Exige probar el ahorro en portería |
| D · Comisión de pagos | Margen sobre la pasarela al pagar la cuota de administración desde la app | 500 casas × cuota C × margen m. Ejemplo: C = $400.000 (supuesto) y m = 0,5 % → 1.000.000 | La más alta a escala: crece con cada conjunto sin trabajo extra | Alto. Exige alianza con la pasarela y el módulo de pagos (etapa 03) |
| E · Implementación | Cobro único al empezar | Ejemplo: 40 h × $80.000 = 3.200.000 por conjunto, una vez | Media. Da caja al inicio y filtra clientes | Bajo |
| F · Canal de instaladores | Comisión por referir hardware, o reventa de Kino con margen para el instalador | Pendiente | Baja en ingreso; alta en adquisición | Medio |

Tarifa de la pasarela, para el modelo D: Wompi cobra 2,65 % + $700 + IVA en línea y 1 % + IVA con QR. Fuente: [Enter.co](https://www.enter.co/fintech/wompi-baja-la-tarifa-del-qr-al-1-y-amplia-los-pagos-desde-el-celular/), consulta 9 nov 2026. Las tarifas de B, C, D y E son ejemplos para comparar, no precios.

**Descartados por el canon**

| Modelo | Motivo |
|---|---|
| Cobrar a la visita | La visita recibe el Pase sin cuenta (`kino/canon/proyecto.md`) |
| Cobrar al residente | Solo la administración compra (`kino/canon/proyecto.md`) |
| Marca blanca | D-009 |
| Vender datos de ingresos | Ley 1581 de 2012 y la trazabilidad del Pase; sin revisión legal |

**Combinación elegida (D-010).** B + E desde el primer conjunto, y D desde la etapa 03. Por ahora B usa los precios de Unita: piso de $1.550.000 + $10.900 por casa. Con Villas y Refugio: 8.550.000 (B) + 1.000.000 (D) = 9.550.000 al mes. B sola cubre la vista de sostenimiento (5.261.595 al mes, Bloque 5), con el trabajo de los socios incluido. C sirve como argumento de venta: el piso equivale al 8 % de un puesto de vigilancia.

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
| Actualizar MySQL fuera del soporte extendido | Ahorra USD 144 al mes, el 41 % de AWS (Bloque 5) | Alejandro, Manuel |
| Entrevistas a 5 administradores | Validar perfil, canales y precio | Juan Esteban, Nico |

---

## Bloque 5 · Presupuesto

Horizonte: nov 2026 a dic 2027, 14 meses. EAFIT no pide un formato de presupuesto. Fuente de ambos datos: Alejandro, chat del proyecto, 9 nov 2026.

**Dos vistas.** La vista *en efectivo* suma lo que Kino paga. La vista *de sostenimiento* suma también el trabajo de los socios, valorado aunque nadie cobre. Fuente del trabajo valorado: `KINO-costos-separados-infraestructura-y-operacion.pdf`, presupuesto mensual del 8 nov 2026, compartido por Alejandro en el chat el 9 nov 2026; no está en el repositorio.

**Supuestos**

| Supuesto | Valor | Fuente |
|---|---|---|
| Tasa de cambio | $3.300 por USD | Techo del rango de $3.120 a $3.300 que prevé Bancolombia para nov 2026, según [El Colombiano](https://www.elcolombiano.com/inicio/dolar-colombia-proyeccion-tasa-cambio-noviembre-2026-GF43201403). TRM del 4 nov 2026: $3.235,59, según [dolar-colombia.com](https://www.dolar-colombia.com/2026-11-04). El PDF de costos usa $4.000 como supuesto editable |
| Equipo | Nadie cobra. Todos son socios | Alejandro, 9 nov 2026 |
| Fuente de dinero | Capital propio | Alejandro, 9 nov 2026 |
| Unidades | Villas Campestres: 400 totales, 100 construidas. Refugio Campestre: 680 totales, 400 construidas | Alejandro, 9 nov 2026 |
| Unidad que paga | Solo la unidad construida | Inferido: un lote sin casa no recibe visitas ni colaboradores |
| Reserva para imprevistos | 15 % | PDF de costos |

### 5.1 Inversión ya hecha

| Rubro | Valor (COP) | Fuente |
|---|---|---|
| Registro de marca, una clase | 1.200.000 | Alejandro, 9 nov 2026 |

### 5.2 Infraestructura AWS

| Componente | USD al mes | COP al mes | Estado según el PDF |
|---|---|---|---|
| Servidores, discos, base de datos, balanceadores, integración y red | 147,56 | 486.948 | Proyección a 720 horas, no gasto histórico |
| Soporte extendido de MySQL 8 | 144,00 | 475.200 | Proyección de un cargo observado de USD 148,80 en octubre |
| Almacenamiento, respaldos, registros y transferencia | 58,44 | 192.852 | Provisión; puede quedarse corta |
| **Total AWS** | **350,00** | **1.155.000** | El PDF da $1.400.000 a $4.000 por USD |

La cuenta AWS es compartida; el PDF no asigna su factura global a Kino. Incluye producción y pruebas.

**Ahorro posible (inferido).** El soporte extendido es un cargo de AWS por usar una versión de MySQL fuera de su soporte estándar. Actualizar la base de datos lo elimina: USD 144 al mes, el 41 % de AWS. El roadmap lo agrega como tarea.

### 5.3 Herramientas, trabajo y reserva

| Rubro | COP al mes | En efectivo | Fuente |
|---|---|---|---|
| Claude Pro, 1 cuenta: USD 20 | 66.000 | Sí | Precio: [Anthropic](https://support.anthropic.com/en/articles/8325610-how-much-does-claude-pro-cost), consulta 9 nov 2026 |
| Grok, 1 cuenta: USD 30 | 99.000 | Sí | Alejandro, 9 nov 2026 |
| Figma Professional, 1 puesto, mensual: USD 20 | 66.000 | Sí | Pago mensual: Alejandro. Precio: [Foro de Figma](https://forum.figma.com/report-a-problem-6/why-does-the-professional-plan-price-change-at-checkout-57528) |
| Hospedaje de la página web: USD 20 | 66.000 | Sí | Alejandro, 9 nov 2026 |
| Mensajes de WhatsApp para el ingreso: ≈ USD 1 | 3.300 | Sí | Cálculo abajo |
| Soporte funcional: 20 h × $60.000 | 1.200.000 | No, socios | PDF de costos |
| Mantenimiento técnico e integración: 16 h × $100.000 | 1.600.000 | No, socios | PDF de costos |
| Coordinación y seguimiento: 4 h × $80.000 | 320.000 | No, socios | PDF de costos |

**Herramientas.** El PDF propone una bolsa de USD 60 sin desglose. Este presupuesto usa las 4 cuentas que Alejandro reportó (USD 90), no la bolsa, para no contar dos veces.

**WhatsApp (inferido).** 500 unidades construidas × 2 ingresos a la app al mes = 1.000 mensajes. A USD 0,001 por mensaje son USD 1 al mes. Precio: [Chatalog](https://docs.chatalog.ai/platform-setup/whatsapp-connection-guide/whatsapp-pricing-update), consulta 8 nov 2026. El residente comparte el Pase desde su propio WhatsApp; ese envío no le cuesta a Kino.

**Capacidad.** 40 horas al mes, en horario hábil. No incluye atención 24/7. Fuente: PDF de costos.

### 5.4 Costo mensual

```
                               EN EFECTIVO    SOSTENIMIENTO
AWS                              1.155.000        1.155.000
Herramientas y WhatsApp            300.300          300.300
Trabajo de socios (valorado)             0        3.120.000
─────────────────────────────────────────────────────────────
Subtotal                         1.455.300        4.575.300
Reserva 15 %                       218.295          686.295
─────────────────────────────────────────────────────────────
Total al mes                     1.673.595        5.261.595 COP
```

El PDF da $5.474.000 al mes en la vista de sostenimiento. La diferencia sale de la tasa ($4.000 frente a $3.300) y de las herramientas.

### 5.5 Costo total a dic 2027

| Vista | 14 meses | + Marca | Total (COP) |
|---|---|---|---|
| En efectivo | 23.430.330 | 1.200.000 | **24.630.330** |
| Sostenimiento | 73.662.330 | 1.200.000 | **74.862.330** |

### 5.6 Ingresos: modelo de D-010

Modelo elegido por Alejandro el 9 nov 2026 (D-010, opción B): piso por conjunto + cobro por casa construida + implementación única. La comisión de pagos empieza en la etapa 03 y no entra antes de dic 2027. Comparación de modelos: apartado 2.7.

**Precio.** Igual al de Unita, por instrucción de Alejandro (chat del proyecto, 9 nov 2026): piso de $1.550.000 por conjunto + $10.900 por casa construida, al mes. Fuente del precio: deck histórico, lám. 32. Antes de cerrar un contrato, el precio se valida con administradores en la fase 4. Los escenarios cambian la adopción, no el precio.

| Componente | Valor |
|---|---|
| Piso por conjunto, al mes | $1.550.000 |
| Cobro por casa construida, al mes | $10.900 |
| Implementación, una vez | $3.200.000 (supuesto: 40 h × $80.000, tarifa de coordinación del PDF de costos) |

Villas Campestres no paga implementación: ya está implementada. Refugio Campestre la paga al reparar su sincronización. Inferido.

| Conjunto | Cálculo | Al mes |
|---|---|---|
| Villas Campestres (100 casas) | 1.550.000 + 100 × 10.900 | 2.640.000 |
| Refugio Campestre (400 casas) | 1.550.000 + 400 × 10.900 | 5.910.000 |
| Conjunto nuevo (200 casas, supuesto) | 1.550.000 + 200 × 10.900 | 3.730.000 |

| Escenario | Quién paga y desde cuándo | Cálculo | Ingreso a dic 2027 (COP) |
|---|---|---|---|
| Conservador | Solo Villas, desde abr 2027 (después de H3): 9 meses | 2.640.000 × 9 | 23.760.000 |
| Base | Villas desde mar 2027 (10 meses). Refugio desde jul 2027 (6 meses) más su implementación | 2.640.000 × 10 + 5.910.000 × 6 + 3.200.000 | 65.060.000 |
| Optimista | Lo anterior y un conjunto nuevo desde oct 2027 (3 meses), con implementación | 65.060.000 + 3.730.000 × 3 + 3.200.000 | 79.450.000 |

Las fechas salen del roadmap: H2 (mar 2027) y H3 (abr 2027). Refugio paga solo cuando su sincronización esté reparada.

### 5.7 Resultado a dic 2027

| Escenario | Ingresos | En efectivo (costo 24.630.330) | Sostenimiento (costo 74.862.330) |
|---|---|---|---|
| Conservador | 23.760.000 | −870.330 | −51.102.330 |
| Base | 65.060.000 | +40.429.670 | −9.802.330 |
| Optimista | 79.450.000 | +54.819.670 | +4.587.670 |

Sin impuestos ni comisiones. El sostenimiento sale negativo en los escenarios conservador y base porque los costos empiezan en nov 2026 y el cobro empieza en mar 2027. En el escenario base, desde ene 2028 el margen es de +3.288.405 al mes: el −9,8 M se recupera en unos 3 meses, hacia mar 2028. Inferido.

### 5.8 Equilibrio mensual

```
                              Al mes      Cubre efectivo    Cubre sostenimiento
                                          (1.673.595)       (5.261.595)
Villas sola                   2.640.000        Sí                50 %
Villas + Refugio              8.550.000        Sí                Sí (+3.288.405)
Villas + Refugio + nuevo     12.280.000        Sí                Sí (+7.018.405)
```

**Lectura (inferido).**
1. Con el precio de Unita, Villas Campestres sola cubre el costo en efectivo.
2. Villas y Refugio cubren el sostenimiento completo, con el trabajo de los socios incluido, y dejan +$3,3 M al mes.
3. Para un conjunto de 100 casas, el piso pesa más que el cobro por casa: $1,55 M frente a $1,09 M. Un conjunto pequeño puede ver caro el piso. Esto se valida en la fase 4.
4. Si se actualiza MySQL, el costo en efectivo baja a 1.127.115 al mes.

Reparar Refugio sigue siendo la tarea con más efecto en el presupuesto.

### 5.9 Fuera del presupuesto

| Rubro | Motivo | Fuente |
|---|---|---|
| Hardware HikCentral | Lo pagó Monte Sereno | Alejandro, 9 nov 2026 |
| Desplazamientos | No se incluyen | Alejandro, 9 nov 2026 |
| Equipos, licencias, red y energía locales | Sin responsable confirmado | PDF de costos |
| Implementaciones y funciones nuevas | Sin estimar | PDF de costos |
| Atención 24/7 | Fuera de la capacidad de 40 horas | PDF de costos |
| Abogado: política de datos y contrato tipo | Sin cotización | Este documento, Bloque 3 |
| Impuestos y comisiones | Sin dato | PDF de costos |

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
