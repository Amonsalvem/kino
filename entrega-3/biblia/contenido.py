"""Contenido de la Biblia de Kino (documento integrador Diex), entrega 3. Versión corta (19 oct 2026).

Una idea por apartado, en tabla o figura; el detalle completo vive en entrega-3/estrategia.md y en los documentos de
diagnóstico. Convención de evidencia: observado (inspección 14–16 sep 2026), prueba (5 residentes, 2 sep 2026),
entorno (fuente externa citada), inferido (lectura del equipo). Las figuras salen del deck (entrega-3/biblia/figuras).
La versión larga anterior quedó en entrega-3/_obsoleto/biblia-contenido-larga.py.
"""

PORTADA = {
    'Nombre del proyecto': 'Kino',
    'Grupo': 'Diseño para la interacción',
    'Organización': 'Kino · piloto en Monte Sereno, El Retiro (Refugio Campestre y Villas Campestres)',
    'Integrantes': 'Nicolás Ramírez · Alejandro Monsalve',
    'Semestre y año': '2026-2',
    'Fecha de entrega': 'Entrega 3 · octubre de 2026',
}

EQUIPO = [
    ('Nicolás Ramírez', 'Investigación, estrategia de servicio y sistema de marca', 'nramireza@eafit.edu.co'),
    ('Alejandro Monsalve', 'Diseño de interacción, prototipo y librería de Figma', 'amonsalvem@eafit.edu.co'),
]

RESUMEN = [
    'Kino es el control de acceso de un conjunto cerrado. Lo usan el residente, la visita, el colaborador y portería; lo compra la administración. Piloto: Monte Sereno, El Retiro.',
    '**Problema.** El residente sabe a quién espera y no tiene cómo decirlo; la administración tiene la autoridad y no sabe a quién espera; y el sistema solo crea personas permanentes. En Refugio Campestre, 0 de 312 usuarios están sincronizados con el lector (observado).',
    '**Solución.** El **Pase**: autor, motivo, vigencia y modo (QR, placa o código). Lo otorga el residente dentro de las franjas de la administración, la visita lo usa sin cuenta y Kino lo da de alta en el hardware que el conjunto ya tiene (HikCentral).',
]

S = []  # (código, items)

# 1 · CONTEXTO DEL RETO -------------------------------------------------------------------------------
S.append(('1.1', [
    'El ingreso a un conjunto pasa por cuatro actores: residente, visita o colaborador, portería y administración. Ninguno tiene la información completa cuando se decide si alguien entra, y no hay un objeto que la lleve de uno a otro.',
    ('img', 'brecha.png', 'El conocimiento y la autoridad están separados por la puerta. Pregunta guía del proyecto.'),
    ('n', 'Fuentes: diagnóstico consolidado v1; reporte de inspección por rol (14–16 sep 2026, 59 observaciones).'),
]))
S.append(('1.2', [
    ('t', [
        ['Elemento', 'Contenido'],
        ['Cliente', 'Manuel (negocio). Compra únicamente la administración del conjunto'],
        ['Visión', 'Kino empieza por quién entra y crece hacia los demás problemas de seguridad de la propiedad horizontal que descubra con sus clientes, sobre el hardware que cada conjunto ya tiene'],
        ['Misión', 'Que quien sabe quién debe entrar pueda decidirlo, dentro de las franjas del conjunto y con constancia'],
        ['Competencia', 'El método manual (llamada, minuta, WhatsApp); Neivor y ComunidadFeliz (desde la administración); ZKTeco (hardware con software propio); Portea'],
        ['Diferencia', 'Integración probada con el hardware instalado + Pase sin cuenta + autoridad del residente acotada por la administración'],
    ], [2000, 7760]),
    ('n', 'Fuentes: Brief Kino v0.2 §05–06; Neivor, página de producto (21 sep 2026).'),
]))
S.append(('1.3', [
    ('t', [
        ['Beneficiario', 'Reto', 'Oportunidad'],
        ['A1 · Residente', 'Sabe a quién espera y no puede decirlo', 'Pase con vigencia en lugar de una placa permanente'],
        ['A2 · Colaborador', 'Entra varias veces por semana y no existe un acceso por días', 'Pase recurrente por días y franja'],
        ['A3 · Visita', 'Recibe una cuenta permanente por una visita de una tarde', 'Pase sin cuenta por WhatsApp'],
        ['A4 · Administración y portería', 'No sabe quién autorizó cada ingreso', 'Franjas y constancia de cada ingreso'],
    ], [2600, 3760, 3400]),
]))
S.append(('1.4', [
    '**Expectativa.** Que el residente prepare, acote y deje constancia del ingreso de sus visitas y colaboradores, sin crear personas permanentes, sobre el hardware ya instalado.',
    ('t', [
        ['Entrega', 'Entregable'],
        ['E1', 'Diagnóstico y pregunta guía'],
        ['E2', 'Recorridos actuales y propuestos de los cuatro arquetipos'],
        ['E3 (esta)', 'Prototipo navegable con 17 interacciones, estrategia SOSTAC y esta Biblia'],
        ['E4, E5 y final', 'Implementación y evaluación'],
    ], [2000, 7760]),
]))
S.append(('1.5', [
    ('t', [
        ['Criterio de éxito del cliente', 'Cómo se verifica'],
        ['Un ingreso rutinario no pasa por la administración ni crea una persona', 'Ingresos con Pase ÷ ingresos'],
        ['Un conjunto nuevo se integra sin rehacer el producto', 'Días desde la firma hasta el primer Pase confirmado'],
        ['La integración con el lector opera', 'Usuarios sincronizados ÷ total (Refugio hoy: 0/312)'],
        ['La administración renueva', 'Contrato renovado'],
    ], [5400, 4360]),
]))

# 2 · USUARIO -----------------------------------------------------------------------------------------
S.append(('2.1', [
    'Cuatro arquetipos definidos por lo que cada uno sabe y puede hacer en el ingreso.',
    ('t', [
        ['Arquetipo', 'Qué lo define', 'Evidencia'],
        ['A1 · Residente que recibe', 'El único que sabe a quién espera y por cuánto tiempo', 'Inspección, sujetos 1 y 2; entrevistas del 2 sep'],
        ['A2 · Colaborador recurrente', 'Viene varias veces por semana; el sistema solo crea personas permanentes', '0 contratistas registrados; GEIH-DANE 2026'],
        ['A3 · Visita ocasional', 'Recibe una cuenta permanente por una visita de una tarde', '2 «Visitante» permanentes en la propiedad 346'],
        ['A4 · Administración y portería', 'Compra y opera; el portero ve todo y no puede cambiar nada', 'Sujetos 3 a 5; 1 super admin para 893 usuarios'],
    ], [2600, 3960, 3200]),
    ('n', 'Fuente: docs/proyecto/arquetipos-e-insights.md.'),
]))
S.append(('2.2', [
    ('t', [
        ['Arquetipo', 'Punto de dolor', 'Final hoy'],
        ['A1 Residente', 'Ningún destino del menú menciona visitas', 'Sale por WhatsApp'],
        ['A2 Colaborador', 'Queda dado de alta como permanente, con correo', 'Alta permanente'],
        ['A3 Visita', 'Recibe cuenta y rol «Visitante» de por vida', 'Cuenta sin fin'],
        ['A4 Administración', 'No hay bandeja de aprobación', 'Nada que auditar'],
    ], [2300, 4960, 2500]),
    '**Conclusión.** Los cuatro recorridos fallan en la puerta: nadie puede fijar desde cuándo y hasta cuándo entra alguien. A los cuatro les falta un acceso con autor, motivo y vigencia: el Pase.',
]))
S.append(('2.3', [
    ('img', 'arquetipos.png', 'Un insight por arquetipo.'),
    ('t', [
        ['Insight', 'Qué hace la estrategia'],
        ['A1 registra una placa y la deja «Permitido» sin saberlo', 'Pase con vigencia en lugar de una placa permanente'],
        ['A2: el correo que más cuesta pedir es el que rompe la puerta (711 errores)', 'Teléfono en lugar de correo'],
        ['A3: la placa es la vía que menos datos pide', 'La placa es el primer canal del Pase'],
        ['A4 da de alta personas permanentes y no aprueba ningún ingreso', 'Franjas y constancia como argumento de venta'],
    ], [5600, 4160]),
]))
S.append(('2.4', [
    'Emoción buscada: **certeza**. El residente sabe que la persona puede entrar sin llamar a portería.',
    ('t', [
        ['Nivel (Norman)', 'Decisión'],
        ['Visceral', 'El Pase vigente brilla fijo, pierde brillo al acercarse el fin, se apaga al vencer y queda cortado al revocarse'],
        ['Conductual', 'Crear un Pase en 3 toques; la franja se ve antes de crear; revocar se deshace por 5 s'],
        ['Reflexivo', 'Solo es vigente lo que el lector confirmó; cada rechazo lleva su motivo'],
    ], [2000, 7760]),
]))

# 3 · ESTRATEGIA DE SERVICIO --------------------------------------------------------------------------
S.append(('3.1', [
    ('h', 'Plan estratégico SOSTAC · las seis partes y dónde está cada una'),
    ('t', [
        ['Letra', 'Parte del plan', 'Qué contiene', 'Apartado'],
        ['S', 'Situación (diagnóstico)', 'Problema, evidencia, público objetivo (arquetipos), conclusiones del journey e insights', '1.1–1.3 · 2.1–2.3'],
        ['O', 'Objetivos', 'Objetivo general, meta general y 5 objetivos SMART con sus preguntas orientadoras', '3.1'],
        ['S', 'Estrategia', 'Una por objetivo, nombrada con sustantivo y ubicada en un eje estratégico', '3.3'],
        ['T', 'Tácticas', 'Qué se hará, cómo, quién y cuándo', '3.3'],
        ['A', 'Acción', 'Plan de acción: seis hitos de nov 2026 a oct 2027', '3.3'],
        ['C', 'Control', 'KPI con método GQM, etapas y tablero de seguimiento', '3.4'],
    ], [800, 2200, 4960, 1800]),
    ('h', 'SOSTAC · O · Objetivo general (el qué) y meta general'),
    '**Objetivo general.** Posicionar a Kino, a octubre de 2027, como el software de seguridad líder en Antioquia para la propiedad horizontal: el aliado que reúne a residentes, visitas, colaboradores, portería y administración en la decisión de quién entra.',
    '**Meta general a oct 2027.** 1.º en participación entre las copropiedades de Antioquia con lector compatible · 4 conjuntos con pago, como piso · 95 % de los Pases confirmados por el lector en menos de 60 s · 0 personas permanentes creadas para dejar entrar a alguien.',
    ('h', 'SOSTAC · O · Objetivos específicos SMART · acción + métrica + usuario + contexto + tiempo'),
    ('t', [
        ['#', 'Acción', 'Métrica', 'Usuario', 'Contexto', 'Tiempo'],
        ['OE1', 'Crear y enviar un Pase', '≤ 3 toques y < 30 s (KLM)', 'Residente (A1)', 'En el prototipo', 'Antes del 9 nov 2026'],
        ['OE2', 'Crear su primer Pase', '60 % de las casas', 'Residentes (A1)', 'Piloto en Villas Campestres', '8 semanas, ene–feb 2027'],
        ['OE3', 'Entrar con Pase, sin llamada', '80 % de sus ingresos', 'Colaboradores (A2)', 'Portería de Villas Campestres', 'Ene–mar 2027'],
        ['OE4', 'Confirmar el Pase en el lector', '98 % en < 60 s; Refugio ≥ 95 %', 'Administración (A4)', 'HikCentral de Monte Sereno', 'Antes del 31 mar 2027'],
        ['OE5', 'Renovar y firmar pilotos', '1 renovación + 2 conjuntos', 'Administración que compra', 'Antioquia, desde el Oriente', 'Antes del 31 oct 2027'],
    ], [600, 1900, 1900, 1700, 1960, 1700]),
    ('h', 'SOSTAC · O · SMART · preguntas orientadoras: relevante, quién, alcanzable y medible'),
    ('t', [
        ['#', 'Relevante · por qué importa', 'Quién lo logra', 'Alcanzable · con qué recursos', 'Medible · se logró cuando'],
        ['OE1', 'Si crear un Pase es más lento que llamar a portería, nadie lo usa', 'Equipo', 'Prototipo y recorrido automático', '≤ 3 toques y < 30 s · ya cumple'],
        ['OE2', 'La administración paga si los residentes crean Pases', 'Equipo y administración', 'Día de lanzamiento y línea por WhatsApp', '60 % de casas con un Pase'],
        ['OE3', 'El colaborador es el ingreso más frecuente', 'Equipo, Manuel y portería', 'Pase recurrente y la minuta para medir', '80 % de sus ingresos con Pase'],
        ['OE4', 'Sin integración, el lector no conoce el Pase', 'Equipo con Manuel', 'OpenAPI de HikCentral y alta con teléfono', '98 % en < 60 s; Refugio ≥ 95 %'],
        ['OE5', 'Sin contratos, Kino se acaba con la entrega de noviembre', 'Equipo e instaladores', 'Caso con KPI reales y ficha comercial', 'Renovación y 2 contratos'],
    ], [600, 3100, 1900, 2260, 1900]),
    ('n', 'OE1 ya se midió el 19 oct: 3 toques y 8 s; visita nueva, 19,4 s. Las metas de OE2, OE3 y OE5 se recalibran con la semana 1 del piloto.'),
]))
S.append(('3.2', [
    ('t', [
        ['Para', 'Kino le da', 'En lugar de'],
        ['Residente', 'Otorgar, extender y revocar Pases, y saber cuándo entró la persona', 'Llamar a portería'],
        ['Visita y colaborador', 'Entrar con QR, placa o código, sin cuenta', 'Dar sus datos de por vida'],
        ['Portería', 'Ver por qué el lector dejó o no dejó entrar', 'Supervisar sin poder actuar'],
        ['Administración (compra)', 'Fijar franjas y ver quién autorizó a quién', 'Altas permanentes sin saber quién autorizó a quién'],
    ], [2400, 4560, 2800]),
    '**Enunciado.** Para la administración de un conjunto que ya tiene lectores, Kino deja a cada residente otorgar Pases con vigencia dentro de las franjas del conjunto, con constancia de cada ingreso y sin cuentas para las visitas.',
]))
S.append(('3.3', [
    ('h', 'SOSTAC · S · Estrategias (el cómo) y SOSTAC · T · Tácticas (qué · cómo · quién · cuándo)'),
    ('t', [
        ['#', 'Estrategia · eje', 'Táctica · qué se hace y cómo', 'Quién', 'Cuándo'],
        ['OE1', 'Simplificación · eje 1', 'Botón «Volver a invitar». Cómo: las 4 visitas recientes abren la hoja con nombre, WhatsApp y placa ya puestos; el Pase sale en 3 toques', 'Equipo', 'Oct 2026 · hecho'],
        ['OE2', 'Acompañamiento · eje 4', 'Día de lanzamiento en portería. Cómo: un puesto en la entrada la semana 1; cada residente que pasa crea su primer Pase con el equipo', 'Equipo y administración', 'Semana 1, ene 2027'],
        ['OE3', 'Recurrencia · eje 3', 'Pase de colaborador. Cómo: el residente elige días y franja una vez; el lector lo acepta cada semana sin renovarlo', 'Equipo con Manuel', 'Dic 2026'],
        ['OE4', 'Integración · eje 3', 'Alta con teléfono. Cómo: Kino da de alta en HikCentral con el teléfono, no con el correo, y reintenta las 711 altas fallidas', 'Equipo con Manuel', 'Nov–dic 2026'],
        ['OE5', 'Penetración · eje 2', 'Alianza con instaladores Hikvision. Cómo: ficha comercial con los KPI del piloto para instaladores del Valle de Aburrá y el Oriente; 10 conjuntos contactados', 'Equipo', 'Abr–jun 2027'],
    ], [600, 2400, 3900, 1500, 1360]),
    ('h', 'Ejes estratégicos del curso'),
    ('t', [
        ['Eje', 'Qué es', 'Estrategias de Kino'],
        ['1 · Interactividad y personalización', 'Lo que se ve se adapta a quien lo usa', 'Simplificación'],
        ['2 · Omnicanalidad y accesibilidad', 'Canales físicos y digitales, sin limitaciones', 'Penetración · Diversificación (QR, placa, código, WhatsApp)'],
        ['3 · Automatización y gestión', 'Sistemas que organizan el recorrido y agilizan el acceso', 'Recurrencia · Integración · Transparencia · Fidelización'],
        ['4 · Soporte y acompañamiento', 'Ayuda en el momento en que alguien se traba', 'Acompañamiento · Medición'],
    ], [3200, 3600, 2960]),
    ('h', 'SOSTAC · A · Plan de acción'),
    ('img', 'plan-accion.png', 'Seis hitos, de la sustentación al liderazgo en Antioquia. El primero es académico; los demás, de producto.'),
    ('h', 'Descripción de productos · fichas de producto'),
    ('t', [
        ['Ficha', 'Qué es', 'Sirve a'],
        ['F1 · Kino Residente', 'App para otorgar, extender y revocar Pases', 'OE1, OE2, OE3'],
        ['F2 · Pase vivo', 'Página para la visita, sin cuenta ni app', 'OE2'],
        ['F3 · Kino Portería', 'Dice por qué alguien entró o no entró', 'OE3, OE4'],
        ['F4 · Kino Administración', 'Franjas y estado de la sincronización con HikCentral', 'OE4, OE5'],
        ['F5 · Conector HikCentral', 'Da de alta el Pase en el lector', 'OE4'],
        ['F6 · Kit de implementación', 'Un conjunto nuevo operando en menos de 10 días', 'OE2'],
    ], [2800, 5160, 1800]),
    ('n', 'Tácticas adicionales, horizonte de empresa, lista de mercado y fichas completas: entrega-3/estrategia.md §5, §9 y §10.'),
]))
S.append(('3.4', [
    ('h', 'SOSTAC · C · Control · KPI con método GQM: objetivo (G) → pregunta (Q) → métrica (M) y su meta'),
    'Paso a paso de la guía: determinar el objetivo, definir una variable y relacionarla con la meta. Un KPI principal por objetivo, más el de participación para el objetivo general; los resultados se reportan en la entrega 5.',
    ('t', [
        ['G', 'Q · Pregunta', 'M · KPI: variable y fórmula', 'Meta', 'Etapa', 'Cada'],
        ['OE1', '¿Crear un Pase es más rápido que llamar?', 'Tiempo para crear (KLM del recorrido)', '< 30 s', 'Comportamiento', 'Versión'],
        ['OE2', '¿Cuántas casas crean Pases?', 'Casas con ≥ 1 Pase ÷ casas registradas', '≥ 60 %', 'Conversión', 'Semana'],
        ['OE3', '¿El colaborador entra sin llamada?', 'Ingresos por lector ÷ ingresos en minuta', '≥ 80 %', 'Comportamiento', 'Semana'],
        ['OE4', '¿El lector recibe el Pase en menos de un minuto?', 'Confirmados en < 60 s ÷ creados', '≥ 98 %', 'Confianza', 'Día'],
        ['OE5', '¿La administración renueva y otros conjuntos firman?', 'Contratos firmados', '4', 'Conversión', 'Mes'],
        ['General', '¿Kino lidera en Antioquia?', 'Conjuntos con Kino ÷ copropiedades de Antioquia con lector compatible', '1.º', 'Conversión', 'Semestre'],
    ], [600, 2700, 2900, 900, 1560, 1100]),
    ('h', 'SOSTAC · C · Etapas del plan y el KPI que cubre cada una'),
    ('t', [
        ['Etapa', 'KPI'],
        ['Captación', 'Costo de adquisición por conjunto'],
        ['Comportamiento', 'Tiempo para crear (OE1) · ingresos de colaboradores con Pase (OE3)'],
        ['Conversión', 'Activación de casas (OE2) · conjuntos con pago (OE5) · participación en Antioquia (objetivo general)'],
        ['Satisfacción', 'SUS de los residentes · NPS de la administración'],
        ['Confianza', 'Confirmación del lector (OE4) · rechazos con motivo'],
        ['Compromiso', 'Retención de residentes'],
    ], [2400, 7360]),
    ('n', '«Ingresos en minuta»: la minuta es el cuaderno donde portería anota a mano cada ingreso; el KPI de OE3 divide los ingresos de colaboradores que abrió el lector con un Pase entre todos los que anotó portería. Los 13 KPI del plan están en entrega-3/estrategia.md §7.'),
    ('h', 'SOSTAC · C · Tablero de seguimiento'),
    ('img', 'tablero.png', 'Un panel por objetivo contra su meta. OE1 con datos medidos el 19 oct; OE2 a OE4 con datos de ejemplo; OE5 como plan.'),
]))
for c in ('3.5', '3.6', '3.7'):
    S.append((c, [('n', 'Se entrega en la entrega 5, con los datos del piloto.')]))

# 4 · ESPECIFICACIONES FUNCIONALES ---------------------------------------------------------------------
S.append(('4.1', [('n', 'Se entrega en la entrega 4. Base: el plan de acción de 3.3.')]))
S.append(('4.2', [('n', 'Se entrega en la entrega 4. Insumo: los flujos F-01 a F-11 de Figma «Kino · App».')]))
S.append(('4.3', [
    ('t', [
        ['Tipo', 'Requerimiento'],
        ['Funcional', 'El residente crea, extiende y revoca Pases de visita y de colaborador, de horas a meses; la administración fija franjas; la visita entra con QR, placa o código'],
        ['Funcional', 'Ingreso con código por WhatsApp; el registro se valida contra la cédula en la base'],
        ['Técnico', 'El Pase es una persona temporal en HikCentral con «Válido desde / hasta»; el teléfono reemplaza al correo'],
        ['Técnico', 'Un Pase solo es vigente si el lector lo confirmó'],
        ['Estético', 'Tema oscuro; #00BB83 marca y #00D595 crear Pase; el arco solo en lo que es un Pase'],
        ['Comunicativo', 'El objeto se llama «Pase» y la persona que llega, «Visita»; se dice qué registra el sistema, sin prometer más'],
        ['Legal', 'La biometría nunca se exige (Ley 1581 de 2012; SIC, Resolución 52185 de 2025)'],
    ], [1800, 7960]),
]))
S.append(('4.4', [('n', 'Se entrega en la entrega final.')]))

# 5 · DISEÑO DE INTERACCIÓN ---------------------------------------------------------------------------
S.append(('5.1', [
    'Modelo del residente: «yo decido quién entra a mi casa». Modelo del sistema actual: cada persona es un usuario permanente que la administración da de alta. Kino sigue el modelo del residente con un objeto: el Pase.',
    ('img', 'flujo-pase.png', 'El recorrido del Pase dentro de las franjas de la administración, y sus estados.'),
    ('t', [
        ['Atributo', 'Qué es'],
        ['Autor', 'El residente que lo otorga'],
        ['Motivo', 'Por qué entra esta persona'],
        ['Vigencia', 'Desde cuándo y hasta cuándo, de horas a meses; caduca sola'],
        ['Modo', 'Placa, QR o código de un solo uso'],
    ], [2000, 7760]),
    '**Estados.** Previsto → Sin confirmar → Vigente → Por vencer → Vencido o Revocado. Mientras está vigente, la persona entra y sale.',
]))
S.append(('5.2', [
    'Dos piezas: el Figma «Kino · App» (226 pantallas) y un prototipo en código donde los cuatro actores comparten el estado. El QA del Figma encontró 31 hallazgos; el más grave, que nada cruzaba de un actor a otro.',
    ('t', [
        ['ID', 'Interacción', 'Disparador → respuesta'],
        ['I-01', 'Código por WhatsApp', 'Enviar código → llega y se llena solo'],
        ['I-02', 'Pase vivo en la lista', 'Pasa el tiempo → la barra se consume'],
        ['I-03', 'Volver a invitar', 'Tocar a alguien reciente → hoja ya llena'],
        ['I-04', 'Hoja con gesto', 'Arrastrar → se cierra con resorte'],
        ['I-05', 'Vigencia a tu medida', 'Unas horas, un día o Se queda'],
        ['I-06', 'Nacimiento del Pase', 'Crear Pase → el botón se vuelve el arco'],
        ['I-07', 'Espera del lector', 'El lector responde → borde continuo y tres latidos'],
        ['I-08', 'Compartir por WhatsApp', 'Enviar → imagen con QR y enlace'],
        ['I-09', 'Pase vivo de la visita', 'Abrir el enlace → QR, placa o código'],
        ['I-10', 'Lectura en la entrada', 'Leer → veredicto legible desde 3 m'],
        ['I-11', 'Aviso de llegada', 'El lector deja entrar → aviso al residente'],
        ['I-12', 'Rechazo con motivo', 'Pase vencido o revocado → motivo y llamar'],
        ['I-13', 'Mantener para revocar', '0,8 s → corte y deshacer por 5 s'],
        ['I-14', 'Extender', '+1 h, +1 día, +1 semana'],
        ['I-15', 'Franjas con vista previa', 'Mover una franja → qué Pase quedaría fuera'],
        ['I-16', 'Integración caída y arreglo', 'Reintentar con teléfono → los contadores suben'],
        ['I-17', 'Movimiento reducido', 'Ajuste del sistema → fundidos'],
    ], [700, 3300, 5760]),
    ('n', 'Planeadas: Pase en la billetera, háptica por estado y rostro como cuarto modo opcional. Dirección biopunk (E3-1) y motion (E3-8), aprobados el 19 oct.'),
]))

# 6 · DISEÑO Y EVALUACIÓN DE LA EXPERIENCIA ------------------------------------------------------------
S.append(('6.1', [
    ('h', 'Versión evaluada'),
    'Se evaluó el Figma «Kino · App» (226 pantallas). Tres de sus pantallas cambiaron después de la evaluación: Crear Pase, Revocar y Límites del conjunto.',
    ('img', 'version-evaluada.png', 'Así estaba la app cuando se evaluó: Crear Pase (R-P-02), Revocar (R-P-10) y Límites del conjunto (A-03).'),
    ('h', 'Cómo se evaluó'),
    'Evaluación por inspección del equipo: recorrido cognitivo de las tareas principales y las 10 heurísticas de Nielsen, desde cinco perfiles. Los perfiles son los arquetipos del diagnóstico y los de residente del estudio de mercado de Monte Sereno (iAgency, 2024): empty nesters, pareja sin hijos y familia con hijos pequeños.',
    ('img', 'validacion.png', 'Del QA del Figma a la evaluación por inspección.'),
    ('h', 'Resultados: 11 tropiezos en 5 perfiles, 6 ya corregidos'),
    '6 corregidos en el prototipo · 3 planeados para la entrega 4 · 1 pendiente con la administración · 1 sin problema.',
    ('t', [
        ['Perfil y situación', 'Dónde se trababa', 'Sev.', 'Estado y qué cambió'],
        ['A3 · visita sin datos móviles', 'La imagen del WhatsApp no traía un QR legible', '3', 'Corregido: la imagen lleva QR, código y placa'],
        ['Empty nesters · hijos por un mes', 'Solo había Pases de horas', '3', 'Corregido: «Se queda», de 3 días a 3 meses'],
        ['A1 · revocar por error', 'El diálogo no dejaba deshacer', '3', 'Corregido: mantener presionado y deshacer por 5 s'],
        ['A1 · la visita sale a la tienda', 'El Pase quedaba usado al entrar', '3', 'Corregido: entra y sale dentro de su vigencia'],
        ['A4 · portería en hora pico', 'Una lectura tapaba la anterior', '2', 'Corregido: bitácora con la última fila resaltada'],
        ['A4 · mover una franja', 'No se veía el efecto en los Pases activos', '2', 'Corregido: vista previa del cambio'],
        ['Familia · cumpleaños con 15 invitados', 'Quince Pases, uno por uno', '3', 'Planeado: Pase de evento con un enlace y una franja'],
        ['Empty nesters · cinco familiares juntos', 'Cinco hojas iguales, una por persona', '2', 'Planeado: un Pase para varias personas de la familia'],
        ['Familia · niñera en vacaciones', 'Hay que revocar y crear de nuevo', '2', 'Planeado: editar días y franja de un recurrente'],
        ['Pareja sin hijos · número extranjero', 'El cambio de número pasa por la administración', '2', 'Pendiente con la administración: cómo se pide desde fuera'],
        ['Pareja sin hijos · de viaje', 'Extender el Pase del jardinero desde otro país', '0', 'Sin problema: extender y el aviso de llegada cubren el caso'],
    ], [2700, 2900, 600, 3560]),
    ('n', 'Severidad de Nielsen: 0 es sin problema; 4 impide la tarea. Es una inspección del equipo, sin participantes: no hay citas ni tasas de éxito.'),
    ('h', 'Así quedó'),
    ('img', 'version-corregida.png', 'Las mismas tres pantallas en el prototipo en código, después de corregir.'),
    ('n', 'Las otras tres correcciones (QR en la imagen de WhatsApp, entrar y salir con el mismo Pase, bitácora de portería) se hicieron sobre versiones anteriores del prototipo y no tienen captura fiel del antes.'),
    ('h', 'Medición de OE1 (KLM)'),
    ('t', [
        ['Tarea', 'Toques', 'Tiempo', 'Meta'],
        ['Volver a invitar a una visita reciente', '3', '8 s', '≤ 3 toques · cumple'],
        ['Visita nueva (nombre y WhatsApp)', '5', '19,4 s', '< 30 s · cumple'],
    ], [4400, 1300, 1500, 2560]),
    ('n', 'KLM (Card, Moran y Newell, 1980) predice el tiempo de alguien que ya conoce la interfaz. La prueba con residentes llega en el piloto: SUS en la semana 6.'),
]))
S.append(('6.2', [('n', 'Se entrega en la entrega 5. Métricas definidas en 3.4.')]))
S.append(('6.3', [('n', 'Se entrega en la entrega 5. Métricas: toques y tiempo KLM, SUS y discrepancia entre la app y la puerta.')]))

# 7 · IMPLEMENTACIÓN Y TECNOLOGÍA ----------------------------------------------------------------------
S.append(('7.1', [('n', 'Se entrega en la entrega 4. Base: prototipo en TypeScript con Preact y @kino/motion.')]))
S.append(('7.2', [('n', 'Se entrega en la entrega final.')]))

SECCIONES = S
HECHOS = ['1.1', '1.2', '1.3', '1.4', '1.5', '2.1', '2.2', '2.3', '2.4', '3.1', '3.2', '3.3', '4.3', '5.1', '5.2', '6.1']
