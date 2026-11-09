---
title: "KINO · Roadmap, estrategia de servicio y presupuesto"
subtitle: "Estrategia de crecimiento, salida al mercado, expansión y presupuesto a diciembre de 2027"
author:
  - "Nicolás Ramírez Acosta · marca y estrategia"
  - "Alejandro Monsalve Marín · técnica y lógica"
date: "Universidad EAFIT · LE005 Diseño para el Servicio y la Experiencia · noviembre de 2026"
lang: es
---

# Resumen

KINO es una plataforma de control de acceso para conjuntos cerrados. Hoy opera en beta en Monte Sereno Villas Campestres, El Retiro (Antioquia). Este documento define cómo KINO pasa del piloto a un producto que se vende y se sostiene.

| Pregunta | Respuesta corta |
|---|---|
| ¿Qué resolvemos? | Quien conoce a la visita (el residente) no tiene autoridad para dejarla entrar, y quien tiene autoridad (portería) no la conoce |
| ¿A quién vendemos? | Solo a la administración del conjunto. Primero, a conjuntos campestres del oriente antioqueño con hardware HikCentral |
| ¿En qué orden crecemos? | Villas Campestres → Refugio Campestre → conjuntos vecinos → Valle de Aburrá |
| ¿Cómo cobramos? | Piso por conjunto + cobro por casa construida + implementación única. Comisión de pagos desde la etapa 03 |
| ¿Cuánto cuesta? | $24,6 millones en efectivo a diciembre de 2027 ($74,9 millones si se valora el trabajo de los socios) |
| ¿Cuándo se sostiene? | Con Villas y Refugio pagando, desde julio de 2027 |

Las cifras en pesos colombianos (COP). Cada dato lleva su fuente entre corchetes; la lista está al final. *Inferido* marca una deducción del equipo que todavía no tiene prueba.

```
1. Estrategia de servicio     ¿Qué resolvemos y para quién?
2. Salida al mercado          ¿A quién vendemos primero y cómo?
3. Expansión                  ¿Cuándo y hacia dónde crecemos?
4. Roadmap                    ¿En qué orden y en qué fechas?
5. Presupuesto                ¿Cuánto cuesta y cuánto entra?
6. Medición                   ¿Cómo sabemos que funciona?
```

# 1. Estrategia de servicio

## 1.1 Problema

Hoy la persona que conoce a la visita (el residente) no tiene autoridad para dejarla entrar. La persona con autoridad (portería y administración) no la conoce. El ingreso se resuelve por chat, llamada y cuaderno [1] [2].

**Pregunta guía.** ¿Cómo reunir conocimiento y autoridad para decidir quién entra?

## 1.2 Propuesta de valor por actor

| Actor | Hoy | Con KINO |
|---|---|---|
| Residente | Llama a portería o manda un chat | Prepara un Pase para su visita o su colaborador, dentro de los límites de la administración |
| Visita | Espera mientras portería llama a la casa | Recibe el Pase sin crear una cuenta: QR, placa o código de un solo uso |
| Colaborador (empleada, jardinero, técnico) | Entra por costumbre o por llamada, cada día | Recibe un Pase con vigencia y franja horaria. Es el ingreso más frecuente |
| Portería | Llama, anota y decide sin saber | Atiende solo las excepciones. El lector de la puerta valida el Pase |
| Administración | Da de alta personas una por una y ve poco | Fija cupos, duración y franjas. Ve autor, motivo y vigencia de cada ingreso |
| Consejo de administración | Recibe quejas sin datos | Recibe un informe: quién entró, cuándo y con autorización de quién (inferido) |

## 1.3 Diferencia frente a la competencia

La autonomía del residente no diferencia a KINO: otras plataformas, como Neivor, ya la ofrecen. KINO se diferencia en tres cosas juntas:

```
        ┌──────────────────────────────┐
        │  1. Integración probada con  │
        │  el hardware del conjunto    │
        │  (HikCentral: placa, rostro, │
        │  talanquera)                 │
        └──────────────┬───────────────┘
                       │
   ┌───────────────────┴───────────────────┐
   │                                       │
┌──┴─────────────┐               ┌─────────┴────────┐
│ 2. Pase sin    │               │ 3. Autoridad del │
│ cuenta para la │               │ residente dentro │
│ visita         │               │ de los límites   │
│                │               │ de la admin.     │
└────────────────┘               └──────────────────┘
```

**Riesgo.** El pilar 1 todavía no está probado para el Pase temporal. En Refugio Campestre, 0 de 312 usuarios están sincronizados con HikCentral. Los 711 errores de sincronización vienen del campo de correo obligatorio [1]. Mientras el pilar 1 no esté probado, KINO no lo vende como un hecho.

## 1.4 Qué compra el conjunto

KINO vende un servicio de tres partes [4]:

```
PRODUCTO            INTEGRACIÓN              ACOMPAÑAMIENTO
App y panel    +    Conexión con el     +    5 momentos por conjunto:
                    hardware que ya          Diagnóstico → Configuración →
                    tiene el conjunto        Capacitación → Operación
                                             asistida → Soporte
```

## 1.5 Recorrido del Pase

| Actor | Paso | Pantalla | Regla de negocio | Dato que se guarda |
|---|---|---|---|---|
| Residente | Entra a la app | Ingreso con código por WhatsApp | Teléfono obligatorio y único | Sesión, teléfono |
| Residente | Crea el Pase | Acceso previsto | Debe caber en el cupo, la duración y la franja de la administración | Autor, motivo, vigencia, modo |
| Residente | Comparte el Pase | Compartir | La visita no crea cuenta | Envío |
| Visita o colaborador | Llega a la puerta | QR, placa o código | El lector valida, no el vigilante | Evento del lector |
| Portería | Atiende la excepción | Panel de portería | Sin Pase válido, se llama al residente | Excepción manual |
| Administración | Revisa | Bitácora | Nadie edita un registro | Historial |

**Brecha.** La app publicada hoy pide correo, contraseña o cuenta de Google. El recorrido pide código por WhatsApp. El roadmap incluye este cambio (capítulo 4).

# 2. Salida al mercado

## 2.1 Quién compra y quién decide

Solo la administración del conjunto compra KINO. En propiedad horizontal, la decisión pasa por tres instancias:

```
Administrador ──propone──► Consejo ──recomienda──► Asamblea ──aprueba el presupuesto──► Contrato
```

La asamblea aprueba el presupuesto del conjunto. La reunión ordinaria se hace una vez al año, en los tres meses siguientes al cierre del período presupuestal [3].

**Efecto en la venta (inferido).** Si el período cierra en diciembre, la asamblea se reúne entre enero y marzo. Un conjunto que conoce KINO en noviembre puede incluirlo en su presupuesto del año siguiente. Un conjunto que lo conoce en abril espera un año, o paga con un rubro que ya existe, como seguridad.

## 2.2 Perfil del primer cliente

Hipótesis para validar con 5 administradores (inferido a partir del piloto).

| Criterio | Perfil | Por qué |
|---|---|---|
| Tipo | Conjunto campestre o parcelación | Monte Sereno es de este tipo |
| Zona | Oriente antioqueño: El Retiro, Rionegro, La Ceja, Llanogrande | Distancia corta para implementar y dar soporte |
| Hardware | Ya tiene lector de placa o de rostro sobre HikCentral | KINO conecta lo que el conjunto ya pagó |
| Dolor | Visitas y colaboradores frecuentes; portería que llama a la casa | Es el problema del diagnóstico |

## 2.3 Cabeza de playa

```
Paso 1  Monte Sereno Villas Campestres   Beta en uso
          │  medir y publicar el caso
          ▼
Paso 2  Refugio Campestre                Hardware instalado, integración caída
          │  reparar la sincronización
          ▼
Paso 3  Conjuntos vecinos del oriente    Con HikCentral; llegan por referido
          ▼
Paso 4  Medellín y Valle de Aburrá       Solo con el servicio estandarizado
```

Refugio Campestre es el segundo cliente natural: tiene el hardware y ya conoce el problema (inferido). Reparar su sincronización prueba el pilar 1 de la diferencia.

## 2.4 Canales de adquisición

| Canal | Cómo funciona | Costo | Estado |
|---|---|---|---|
| Referido de administradores | Un administrador lleva varias copropiedades y recomienda a otros | Bajo | Inferido; validar en entrevistas |
| Instaladores de HikCentral | El instalador vende el hardware; KINO le da el software que lo hace útil | Comisión por definir | Inferido; sin alianza firmada |
| Caso del piloto | Informe con datos medidos de Monte Sereno | Bajo | Depende del hito H3 |
| soykino.com y redes | Pedido de demostración | Bajo | Sitio en línea |
| Eventos de propiedad horizontal | Charlas a administradores | Medio | Sin contacto |

## 2.5 Embudo de venta

```
Contacto ─► Diagnóstico gratuito ─► Propuesta ─► Consejo ─► Asamblea ─► Implementación
           (usuarios, vehículos,
            hardware existente)
```

El diagnóstico gratuito también vende: muestra al conjunto su propio problema con datos (inferido).

## 2.6 Modelos de ingreso evaluados

**Ancla de valor.** Un puesto de vigilancia 24 horas le cuesta al conjunto entre $17,1 y $19,6 millones al mes en 2026 [10] [11]. El piso de KINO ($1.550.000) equivale a cerca del 9 % de un puesto.

**Costo marginal.** Una casa más casi no sube el costo de KINO: la infraestructura y el trabajo son fijos (capítulo 5). Después del punto de equilibrio, cada peso nuevo es margen (inferido).

| Modelo | Cómo cobra | Rentabilidad | Riesgo |
|---|---|---|---|
| A · Por casa | Una tarifa por casa construida | Media: un conjunto pequeño casi no paga | Bajo |
| **B · Piso + casa** | Una tarifa fija por conjunto más una tarifa por casa | Alta: el piso cubre el soporte de cada conjunto | Bajo |
| C · Por valor | Una fracción del costo de un puesto de vigilancia | Alta | Medio: exige probar el ahorro en portería |
| **D · Comisión de pagos** | Margen sobre la pasarela cuando el residente paga la cuota de administración en la app | La más alta a escala: crece sin trabajo extra | Alto: exige alianza con la pasarela y el módulo de pagos |
| **E · Implementación** | Cobro único al empezar | Media: da caja al inicio y filtra clientes | Bajo |
| F · Canal de instaladores | Comisión por hardware o reventa de KINO | Baja en ingreso, alta en adquisición | Medio |

Para el modelo D, la pasarela Wompi cobra 2,65 % + $700 + IVA en pagos en línea y 1 % + IVA en pagos con QR [16].

**Descartados.** Cobrar a la visita (recibe el Pase sin cuenta). Cobrar al residente (solo compra la administración). Marca blanca (KINO mantiene su marca). Vender datos de ingresos (Ley 1581 de 2012 [17]).

**Modelo elegido: B + E desde el primer conjunto, y D desde la etapa 03 de producto.**

**Precio.** Por ahora, KINO iguala el precio de su competidor directo, Unita: $1.550.000 al mes por conjunto + $10.900 al mes por casa construida [5]. La implementación vale $3.200.000 por conjunto, una vez (40 horas × $80.000 [8]). El precio se valida con administradores antes de cerrar un contrato (fase 4). KINO no adopta el contrato a 60 meses de Unita; esa condición está por decidir.

# 3. Expansión

KINO crece en dos ejes: más conjuntos y más módulos. Cada paso tiene una condición. Sin la condición, el paso no empieza.

```
            MÓDULOS
              ▲
  Etapa 05    │                                ● Escala comercial
  Etapa 04    │                        ● Seguridad y bienestar
  Etapa 03    │                ● Paquetería, reservas y pagos
  Etapa 02    │        ● Portal de administración y residentes
  Etapa 01    ● Acceso (hoy)
              └──────┬─────────┬──────────┬───────────► CONJUNTOS
                  1 conjunto  2-3 del    10+ del oriente
                  (piloto)    oriente    y Valle de Aburrá
```

| Paso | Condición para empezar |
|---|---|
| De 1 a 2 conjuntos | El Pase temporal genera el evento del lector en Monte Sereno |
| De 2 a 10 conjuntos | Precio probado y costo de implementación medido en 2 conjuntos |
| Etapa 02 | Etapa 01 estable: errores de sincronización por debajo de un umbral por fijar |
| Etapa 03 | Clientes que pidan el módulo y paguen por él |
| Etapa 04 | Revisión legal de biometría y de datos de salud |

Fuentes de las etapas y condiciones: [4] [5] [6].

**Marca.** KINO mantiene su marca propia en todos los conjuntos. El nombre del conjunto aparece solo como dato, nunca con su logo ni sus colores.

# 4. Roadmap

## 4.1 Fases

| Fase | Objetivo | Estado a noviembre de 2026 |
|---|---|---|
| 0 · Descubrimiento | Entender el problema, los actores y el hardware | Hecho |
| 1 · Marca e identidad | Construir una identidad propia | En curso: identidad nueva en construcción |
| 2 · Diseño y prototipo | Prototipo de los 3 roles: 172 pantallas, app y web | Hecho; faltan pruebas de usabilidad |
| 3 · Piloto | Validar KINO en operación real en Monte Sereno | En curso; beta desde enero de 2026 |
| 4 · Modelo y precio | Probar el precio con administradores | Pendiente |
| 5 · Lanzamiento | Sitio, video, redes y caso del piloto | Sitio soykino.com en línea |
| 6 · Escalamiento | Etapas de producto 02 a 05 y nuevos conjuntos | Pendiente |
| 7 · Legal | Registro de marca, política de datos y contrato tipo | Registro de marca radicado |

Fuente: [5] [6].

## 4.2 Cronograma

```
                    2026        2027
                    nov  dic │ ene  feb  mar │ abr  may  jun │ jul  ago  sep │ oct  nov  dic
Fase 3 Piloto       ████████████████████████
  Login WhatsApp    ████████
  Pase temporal         ████████████
  Colaboradores              ████████
Fase 4 Precio            ████████████
Fase 5 Lanzamiento  ██                ████
Fase 6 Escalar                             ████████████████████████████████████████
Fase 7 Legal        ████████████
Hitos               H1                 H2   H3                                       H5
```

| Hito | Fecha | Se cumple cuando | Estado |
|---|---|---|---|
| H1 · soykino.com | nov 2026 | Sitio en línea con HTTPS y correo | Cumplido |
| H2 · Cierre de la beta | mar 2027 | Login por WhatsApp, Pase temporal con evento del lector y KPI medidos cada semana | Pendiente |
| H3 · Informe del piloto | abr 2027 | Resultados medidos y caso publicado | Pendiente |
| H4 · Refugio Campestre | jul 2027 | Sincronización reparada y Refugio pagando | Pendiente |
| H5 · Nuevos conjuntos | dic 2027 | Al menos un conjunto nuevo firmado | Pendiente |

Fechas propuestas a partir del plan operativo del 28 de octubre de 2026 [6].

## 4.3 Tareas clave y responsables

| Tarea | Por qué | Responsable |
|---|---|---|
| Ingreso con código por WhatsApp | La app publicada pide correo y contraseña | Alejandro, Manuel |
| Quitar el correo obligatorio | Causa los 711 errores de sincronización [1] | Alejandro, Daniel |
| Pase temporal con evento del lector | Sin esto no se prueba la diferencia | Alejandro, Daniel |
| Pase de colaborador con franja | Es el ingreso más frecuente | Alejandro |
| Registro validado contra la cédula | El administrador ya no aprueba registros | Alejandro |
| Reparar la sincronización en Refugio Campestre | Segundo cliente y prueba del pilar 1 | Daniel, Manuel |
| Actualizar la versión de MySQL | Ahorra USD 144 al mes, el 41 % del costo de AWS (capítulo 5) | Alejandro, Manuel |
| Entrevistas a 5 administradores | Validar perfil, canales y precio | Juan Esteban, Nicolás |
| Caso del piloto y contenido | Canal de adquisición | Henry, Nicolás |

**Equipo.** Nicolás Ramírez (marca y estrategia), Alejandro Monsalve (técnica y lógica), Juan Esteban (comercial), Manuel (tecnología), Daniel (IoT) y Henry (marca). Todos son socios.

# 5. Presupuesto

Horizonte: noviembre de 2026 a diciembre de 2027 (14 meses). Fuente de dinero: capital propio de los socios [9].

**Dos vistas.** La vista *en efectivo* suma lo que KINO paga. La vista *de sostenimiento* suma también el trabajo de los socios, valorado aunque hoy nadie cobra [8] [9].

**Supuestos**

| Supuesto | Valor | Fuente |
|---|---|---|
| Tasa de cambio | $3.300 por USD: techo del rango previsto para noviembre de 2026. TRM del 4 de noviembre: $3.235,59 | [12] [13] |
| Equipo | Nadie cobra; todos son socios | [9] |
| Unidades | Villas Campestres: 400 totales, 100 construidas. Refugio Campestre: 680 totales, 400 construidas | [9] |
| Unidad que paga | Solo la casa construida (inferido: un lote vacío no recibe visitas) | |
| Reserva para imprevistos | 15 % | [8] |

## 5.1 Inversión ya hecha

| Rubro | Valor |
|---|---|
| Registro de marca, una clase | $1.200.000 [9] |

## 5.2 Infraestructura (AWS)

| Componente | USD al mes | COP al mes |
|---|---|---|
| Servidores, discos, base de datos, balanceadores, integración y red | 147,56 | 486.948 |
| Soporte extendido de MySQL 8 | 144,00 | 475.200 |
| Almacenamiento, respaldos, registros y transferencia | 58,44 | 192.852 |
| **Total AWS** | **350,00** | **1.155.000** |

Fuente: [8]. Incluye producción y pruebas.

**Ahorro posible (inferido).** AWS cobra el soporte extendido por usar una versión de MySQL fuera de su soporte estándar. Si se actualiza la base de datos, el cobro desaparece: USD 144 al mes, el 41 % de AWS.

## 5.3 Herramientas y trabajo

| Rubro | COP al mes | En efectivo | Fuente |
|---|---|---|---|
| Claude Pro, 1 cuenta (USD 20) | 66.000 | Sí | [9] [14] |
| Grok, 1 cuenta (USD 30) | 99.000 | Sí | [9] |
| Figma Professional, 1 puesto mensual (USD 20) | 66.000 | Sí | [9] [15] |
| Hospedaje de la página web (USD 20) | 66.000 | Sí | [9] |
| Mensajes de WhatsApp para el ingreso (≈ USD 1) | 3.300 | Sí | [18] |
| Soporte funcional: 20 h × $60.000 | 1.200.000 | No, socios | [8] |
| Mantenimiento técnico e integración: 16 h × $100.000 | 1.600.000 | No, socios | [8] |
| Coordinación y seguimiento: 4 h × $80.000 | 320.000 | No, socios | [8] |

**WhatsApp (inferido).** 500 casas × 2 ingresos a la app al mes = 1.000 mensajes. A USD 0,001 por mensaje, son USD 1 al mes. El residente comparte el Pase desde su propio WhatsApp; ese envío no le cuesta a KINO.

**Capacidad.** 40 horas al mes, en horario hábil. No incluye atención 24 horas [8].

## 5.4 Costo mensual

| Rubro | En efectivo | Sostenimiento |
|---|---|---|
| AWS | 1.155.000 | 1.155.000 |
| Herramientas y WhatsApp | 300.300 | 300.300 |
| Trabajo de los socios (valorado) | 0 | 3.120.000 |
| Subtotal | 1.455.300 | 4.575.300 |
| Reserva 15 % | 218.295 | 686.295 |
| **Total al mes** | **1.673.595** | **5.261.595** |

## 5.5 Costo total a diciembre de 2027

| Vista | 14 meses | Marca | **Total** |
|---|---|---|---|
| En efectivo | 23.430.330 | 1.200.000 | **24.630.330** |
| Sostenimiento | 73.662.330 | 1.200.000 | **74.862.330** |

## 5.6 Ingresos

Precio del capítulo 2: $1.550.000 por conjunto + $10.900 por casa, al mes, más $3.200.000 de implementación. Villas Campestres no paga implementación porque ya está implementada. La comisión de pagos empieza en la etapa 03 y no entra en este horizonte.

| Conjunto | Cálculo | Al mes |
|---|---|---|
| Villas Campestres (100 casas) | 1.550.000 + 100 × 10.900 | 2.640.000 |
| Refugio Campestre (400 casas) | 1.550.000 + 400 × 10.900 | 5.910.000 |
| Conjunto nuevo (200 casas, supuesto) | 1.550.000 + 200 × 10.900 | 3.730.000 |

Los escenarios cambian cuántos conjuntos pagan y desde cuándo. El precio es el mismo.

| Escenario | Quién paga y desde cuándo | Cálculo | Ingreso a dic 2027 |
|---|---|---|---|
| Conservador | Solo Villas, desde abril de 2027 (después de H3): 9 meses | 2.640.000 × 9 | 23.760.000 |
| **Base** | Villas desde marzo de 2027 (10 meses). Refugio desde julio de 2027 (6 meses), más su implementación | 2.640.000 × 10 + 5.910.000 × 6 + 3.200.000 | **65.060.000** |
| Optimista | Lo anterior y un conjunto nuevo desde octubre de 2027 (3 meses), con implementación | 65.060.000 + 3.730.000 × 3 + 3.200.000 | 79.450.000 |

## 5.7 Resultado a diciembre de 2027

| Escenario | Ingresos | En efectivo | Sostenimiento |
|---|---|---|---|
| Conservador | 23.760.000 | −870.330 | −51.102.330 |
| **Base** | **65.060.000** | **+40.429.670** | **−9.802.330** |
| Optimista | 79.450.000 | +54.819.670 | +4.587.670 |

Sin impuestos ni comisiones.

**Por qué el sostenimiento sale negativo en el escenario base.** Los costos empiezan en noviembre de 2026 y el cobro empieza en marzo de 2027:

| Tramo | Ingreso al mes | Resultado al mes | Meses | Acumulado |
|---|---|---|---|---|
| nov 2026 a feb 2027 | 0 | −5.261.595 | 4 | −21.046.380 |
| mar a jun 2027 | 2.640.000 (Villas) | −2.621.595 | 4 | −10.486.380 |
| jul a dic 2027 | 8.550.000 (Villas + Refugio) | +3.288.405 | 6 | +19.730.430 |
| Implementación de Refugio | | | | +3.200.000 |
| Registro de marca | | | | −1.200.000 |
| **Total** | | | | **−9.802.330** |

Ese saldo es el valor del tiempo que los socios ponen antes de que KINO pueda pagarlo; no es dinero que sale de la caja. Con +$3,3 millones al mes, se recupera hacia marzo de 2028 (inferido).

## 5.8 Punto de equilibrio mensual

| Conjuntos que pagan | Ingreso al mes | Cubre el efectivo (1.673.595) | Cubre el sostenimiento (5.261.595) |
|---|---|---|---|
| Villas Campestres sola | 2.640.000 | Sí | 50 % |
| Villas + Refugio | 8.550.000 | Sí | Sí, con +3.288.405 |
| Villas + Refugio + uno nuevo | 12.280.000 | Sí | Sí, con +7.018.405 |

**Lectura (inferido).**

1. Villas Campestres sola cubre el costo en efectivo.
2. Villas y Refugio cubren el sostenimiento completo, con el trabajo de los socios incluido.
3. Reparar la sincronización de Refugio es la tarea con más efecto en el presupuesto.
4. En un conjunto de 100 casas, el piso ($1,55 millones) pesa más que el cobro por casa ($1,09 millones). Un conjunto pequeño puede verlo caro. Esto se valida en la fase 4.
5. Si se actualiza MySQL, el costo en efectivo baja a $1.127.115 al mes.

## 5.9 Fuera del presupuesto

| Rubro | Motivo |
|---|---|
| Hardware HikCentral | Lo pagó Monte Sereno [9] |
| Desplazamientos | No se incluyen [9] |
| Equipos, licencias, red y energía de cada conjunto | Sin responsable confirmado [8] |
| Funciones nuevas | Sin estimar [8] |
| Atención 24 horas | Fuera de la capacidad de 40 horas [8] |
| Abogado: política de datos y contrato tipo | Sin cotización |
| Impuestos y comisiones | Sin dato [8] |

# 6. Medición

No hay líneas base todavía. Cada indicador dice cómo se mide y una meta inicial propuesta, que se ajusta con la primera medición [5].

| Área | Indicador | Fórmula | Meta inicial |
|---|---|---|---|
| Marca | Tráfico web | Usuarios únicos en soykino.com | 200 en 90 días |
| Marca | Conversión a demostración | Solicitudes ÷ usuarios únicos | 3 % en 90 días |
| Marca | Comunidad en redes | Seguidores y publicaciones al mes | 150 seguidores y 4 publicaciones al mes a 90 días |
| Piloto | Adopción | Casas con un residente activo ÷ casas del padrón | 25 % a 60 días; 50 % a 120 días |
| Piloto | Ingresos digitales | Se reporta en tres cifras: placas sincronizadas, excepciones manuales y Pases confirmados por el lector | Línea base en el mes 1 |
| Piloto | Pases de colaborador | Pases de colaborador ÷ Pases emitidos | Línea base en el mes 1 |
| Piloto | Tiempo en portería | Mediana entre la llegada y el registro de entrada | ≤ 45 segundos |
| Piloto | Satisfacción | NPS de residentes; CSAT de portería y administración (1 a 5) | NPS ≥ 30; CSAT ≥ 4,0 |
| Técnica | Errores de sincronización | Errores por semana | Umbral para pasar a la etapa 02 |
| Negocio | Embudo comercial | Conjuntos contactados y propuestas enviadas | 5 contactados y 2 propuestas en 6 meses |
| Negocio | Tasa de cierre | Propuestas aceptadas ÷ enviadas | Revisar al llegar a 5 propuestas |
| Negocio | Ingreso recurrente mensual | Σ (piso + casas × cobro por casa) | $8,55 millones con Villas + Refugio |
| Negocio | Costo de adquisición | Gasto comercial ÷ conjuntos firmados | Línea base con el primer cierre |
| Negocio | Recuperación de la implementación | Costo de implementación ÷ margen mensual del conjunto | Línea base con Refugio |

# Fuentes

1. Equipo KINO. Inspección directa del sistema de control de acceso de Monte Sereno (panel de administración y HikCentral). Septiembre de 2026.
2. Equipo KINO. Entrevistas a 5 residentes de Monte Sereno. 2 de septiembre de 2026.
3. Congreso de Colombia. Ley 675 de 2001, régimen de propiedad horizontal, artículos 38 y 39. http://www.secretariasenado.gov.co/senado/basedoc/ley_0675_2001.html
4. KINO. *Productos y servicios v2*, documento comercial. 3 de noviembre de 2026.
5. KINO. *El camino de KINO*, presentación de estrategia (Figma Slides), láminas 7 a 34. Octubre de 2026. Incluye la tarifa de referencia del competidor (lámina 32) y los indicadores SMART.
6. KINO. *Plan operativo EMP-002, Gantt*. 28 de octubre de 2026.
7. KINO. *Estrategia de servicio* (Figma Slides), 21 láminas. Noviembre de 2026.
8. KINO. *Presupuesto mensual: infraestructura y operación*. 8 de noviembre de 2026.
9. Equipo KINO. Datos de operación: unidades por conjunto, gastos actuales, costo del registro de marca y fuente de capital. 9 de noviembre de 2026.
10. Noticias RCN. «Salario de vigilantes quedó fijado para este 2026». https://www.noticiasrcn.com/economia/la-supervigilancia-fijo-tarifas-minimas-de-vigilancia-para-2026-989255. Consulta: 9 de noviembre de 2026.
11. El Espectador. «Tarifas de vigilancia y seguridad privada en 2026». https://www.elespectador.com/economia/tarifas-de-vigilancia-y-seguridad-privada-en-2026-asi-suben-los-precios/. Consulta: 9 de noviembre de 2026.
12. El Colombiano. Proyección de la tasa de cambio para noviembre de 2026. https://www.elcolombiano.com/inicio/dolar-colombia-proyeccion-tasa-cambio-noviembre-2026-GF43201403. Consulta: 9 de noviembre de 2026.
13. Dólar Colombia. TRM del 4 de noviembre de 2026. https://www.dolar-colombia.com/2026-11-04. Consulta: 9 de noviembre de 2026.
14. Anthropic. «How much does Claude Pro cost?». https://support.anthropic.com/en/articles/8325610-how-much-does-claude-pro-cost. Consulta: 9 de noviembre de 2026.
15. Figma. Foro de la comunidad, precio del plan Professional. https://forum.figma.com/report-a-problem-6/why-does-the-professional-plan-price-change-at-checkout-57528. Consulta: 9 de noviembre de 2026.
16. Enter.co. «Wompi baja la tarifa del QR al 1 %». https://www.enter.co/fintech/wompi-baja-la-tarifa-del-qr-al-1-y-amplia-los-pagos-desde-el-celular/. Consulta: 9 de noviembre de 2026.
17. Congreso de Colombia. Ley 1581 de 2012, protección de datos personales.
18. Chatalog. Precios de la plataforma de WhatsApp Business. https://docs.chatalog.ai/platform-setup/whatsapp-connection-guide/whatsapp-pricing-update. Consulta: 8 de noviembre de 2026.

## Uso de inteligencia artificial

| Herramienta | Uso |
|---|---|
| Grok (xAI) | Nicolás Ramírez preparó con Grok la primera versión del roadmap y del sistema de medición, a partir de los documentos de KINO |
| Claude (Anthropic) | Alejandro Monsalve trabajó con Claude la revisión de esa versión contra las decisiones del proyecto, la redacción de la salida al mercado, la expansión y los modelos de ingreso, la búsqueda de tarifas públicas y los cálculos del presupuesto |

Los datos de operación, las cifras de costos, el modelo de ingresos elegido y el precio son decisiones del equipo KINO. Las herramientas de IA no aportaron datos propios; cada cifra externa tiene su fuente en esta lista.
