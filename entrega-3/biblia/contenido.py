"""Contenido de la Biblia de Kino (documento integrador Diex), entrega 3.

Cada apartado lista su fuente. Convención de evidencia del proyecto: observado (inspección 14–16 sep 2026),
prueba (5 residentes, 2 sep 2026), entorno (fuente externa citada), inferido (lectura del equipo).
El orden de SECCIONES sigue el de la plantilla: 1.1 a 7.2.
"""

PORTADA = {
    'Nombre del proyecto': 'Kino · El Pase: quién decide quién entra',
    'Grupo': 'Por confirmar',
    'Organización': 'Kino, con piloto en Monte Sereno (El Retiro, Antioquia): Refugio Campestre y Villas Campestres',
    'Integrantes': 'Nicolás Ramírez · Alejandro Monsalve',
    'Semestre y año': '2026-2',
    'Fecha de entrega': 'Por confirmar · entrega 3, octubre de 2026',
}

EQUIPO = [
    ('Nicolás Ramírez', 'Investigación, estrategia de servicio y sistema de marca', 'nramireza@eafit.edu.co'),
    ('Alejandro Monsalve', 'Diseño de interacción, prototipo y librería de Figma', 'amonsalvem@eafit.edu.co'),
]

RESUMEN = [
    'Kino es una plataforma de control de acceso para conjuntos residenciales cerrados, con un producto mínimo en operación en Monte Sereno (El Retiro). Es para el residente, que decide quién entra a su casa; para la visita y el colaborador, que entran; para portería, que opera la entrada, y para la administración del conjunto, que es quien compra.',
    'El problema que resuelve es un desajuste entre conocimiento y autoridad: el residente sabe a quién espera y no tiene cómo decirlo; la administración tiene la autoridad nominal y no sabe a quién dejar entrar; y el sistema actual solo sabe crear personas permanentes, así que la visita necesita cuenta y el colaborador queda registrado como si viviera ahí. En Refugio Campestre el hardware está instalado y 0 de 312 usuarios están sincronizados por un campo de correo obligatorio (observado).',
    'La solución es el **Pase**: un objeto con autor, motivo, vigencia y modo (QR, placa o código) que el residente otorga dentro de los límites que fija la administración, que la visita usa sin cuenta y que Kino da de alta en el hardware que el conjunto ya tiene (HikCentral). Solo se muestra vigente cuando el lector lo confirma.',
]

S = []  # (código, items)

# 1 · CONTEXTO DEL RETO -------------------------------------------------------------------------------
S.append(('1.1', [
    'El acceso a un conjunto cerrado es un servicio que ocurre entre cuatro actores que nunca están juntos: el residente que espera, la visita que llega, portería que opera la entrada y la administración que responde ante el consejo. Ninguno de ellos tiene la información completa en el momento en que se decide si alguien entra. Por eso el problema es de diseño de interacción: el servicio falla en el traspaso entre actores, no en una pantalla.',
    ('h', 'Por qué un proyecto de servicio basado en la interacción'),
    ('-', 'La decisión de quién entra la toma una persona (el residente) y la ejecuta una máquina (el lector de placas, QR o rostro). La interacción es el puente entre las dos.'),
    ('-', 'El sistema actual ya concede acceso físico cuando el residente registra una placa, mientras la pantalla le dice que lo controla la administración (observado). La interfaz contradice al servicio.'),
    ('-', 'La visita es el actor con menos interés en el sistema y al que más se le pide: hoy crea una cuenta permanente para una visita de una tarde (observado).'),
    ('h', 'Pregunta guía'),
    '¿Cómo reunir conocimiento y autoridad para decidir quién entra?',
    ('n', 'Fuentes: docs/proyecto/diagnostico-consolidado-v1.md; reporte de inspección por rol (14–16 sep 2026, 59 observaciones).'),
]))
S.append(('1.2', [
    '**Dueño del proyecto.** Manuel, cliente y negocio. Kino es la marca del producto, antes llamado Arcana. Quien compra el producto es únicamente la administración del conjunto.',
    ('t', [
        ['Elemento', 'Contenido'],
        ['Visión', 'Ser la capa de autorización entre las personas y el hardware de acceso de los conjuntos residenciales en Colombia, sin importar la marca del lector.'],
        ['Misión', 'Que quien sabe quién debe entrar pueda decidirlo, con un límite claro y una constancia de quién autorizó a quién.'],
        ['Objetivos del cliente', 'Eficiencia operativa (un ingreso rutinario no exige dar de alta a una persona), escalabilidad (un conjunto nuevo se integra sin rehacer el producto), marca sólida y fidelización de la administración.'],
        ['Competidores', 'El método manual (llamada, minuta, WhatsApp) es el más fuerte. Neivor y ComunidadFeliz nacen desde la administración y las finanzas; Neivor ya vende autogestión de visitas por QR. ZKTeco vende su hardware con su software. Portea, app de portería de Medellín.'],
        ['Diferencia', 'La suma de tres cosas: integración probada con el hardware que el conjunto ya tiene, el Pase sin cuenta para la visita y la autoridad del residente acotada por los límites de la administración.'],
    ], [2400, 7360]),
    ('n', 'Fuentes: Brief Kino v0.2 §05 y §06; Neivor, página de producto (consultada 21 sep 2026); estrategia.md §1.5.'),
]))
S.append(('1.3', [
    ('t', [
        ['Beneficiario', 'Reto principal', 'Oportunidad'],
        ['A1 · Residente que recibe', 'Sabe a quién espera y no tiene dónde expresarlo; ya abre la puerta sin saberlo al registrar una placa', 'Nombrar y acotar la autoridad que ya tiene'],
        ['A2 · Colaborador recurrente', 'El ingreso más frecuente es el que menos existe en el producto: 0 contratistas registrados', 'Un Pase recurrente por días y franja, sin correo'],
        ['A3 · Visitante ocasional', 'Entrega documento, teléfono y correo de por vida para una visita de una tarde', 'Pase sin cuenta por el canal que ya usa (WhatsApp)'],
        ['A4 · Administración y portería', 'Responde ante el consejo por ingresos que no puede rastrear; paga infraestructura que en Refugio no opera', 'Franjas en vez de aprobaciones, y constancia de cada ingreso'],
    ], [2600, 4160, 3000]),
    ('n', 'Fuentes: docs/proyecto/arquetipos-e-insights.md; trabajo doméstico por días 51,3 % en 1S-2026 (GEIH-DANE y Symplifica vía Infobae, 9 sep 2026).'),
]))
S.append(('1.4', [
    '**Expectativas.** Que el residente pueda preparar, acotar en el tiempo y dejar constancia del ingreso de sus visitas y colaboradores, sin que nadie quede dado de alta como usuario permanente, y que eso funcione sobre el hardware ya instalado.',
    ('h', 'Entregables clave'),
    ('-', 'Diagnóstico y pregunta guía (entrega 1).'),
    ('-', 'Flujos actuales y propuestos de los cuatro arquetipos y el mapa de posibilidades (entrega 2).'),
    ('-', 'Sistema de marca Kino y librería de Figma «Kino · Sistema de marca» (sep 2026).'),
    ('-', 'Prototipo navegable con 20 interacciones inventariadas, estrategia SOSTAC y esta Biblia (entrega 3).'),
    ('-', 'Implementación y evaluación (entregas 4, 5 y final).'),
]))
S.append(('1.5', [
    ('t', [
        ['Criterio de éxito según el cliente', 'Cómo se verifica'],
        ['Un ingreso rutinario no exige intervención de la administración ni dar de alta a una persona', 'Registros del sistema: ingresos con Pase ÷ ingresos'],
        ['Un conjunto nuevo se integra sin rehacer el producto', 'Días desde la firma hasta el primer Pase confirmado'],
        ['La integración con el hardware opera', 'Usuarios y vehículos sincronizados ÷ total (Refugio hoy: 0/312 y 1/44)'],
        ['La administración renueva', 'Contrato renovado y NPS de la administración'],
    ], [5400, 4360]),
    ('n', 'Las metas numéricas de cada criterio están en 3.1.'),
]))

# 2 · USUARIO -----------------------------------------------------------------------------------------
S.append(('2.1', [
    'Los arquetipos se construyeron desde la evidencia de esta fase y se definen por su posición frente al sistema, no por una biografía inventada. Con cinco entrevistas sin citas documentadas, una persona con nombre propio sería una ficción con apariencia de dato. Los arquetipos del trabajo 2026-1 (Valeria Gómez y Carlos Ramírez) no se usan: no tienen respaldo en la investigación propia y ponen al vigilante como usuario primario, que es lo que la inspección desmiente.',
    ('t', [
        ['Arquetipo', 'Qué lo define frente al sistema', 'Evidencia'],
        ['A1 · El residente que recibe', 'Único que sabe a quién espera y por cuánto tiempo, y el único que no puede expresarlo', 'Inspección, sujetos 1 y 2 (33 obs.); prueba TST001; entrevistas del 2 sep'],
        ['A2 · El colaborador recurrente', 'Vínculo intermitente y repetido; el sistema solo sabe representar permanencia', 'Rol app.domestic_employee; 0 contratistas registrados; GEIH-DANE 2026'],
        ['A3 · El visitante ocasional', 'Entrega datos de por vida para una visita de una tarde', 'Ficha de propiedad 346 con 2 «Visitante» permanentes; SIC 52185'],
        ['A4 · Administración y portería', 'Quien compra y quien opera; el portero ve todo y no puede cambiar nada', 'Sujetos 3, 4 y 5 (26 obs.); 1 super admin para 893 usuarios'],
    ], [2600, 3960, 3200]),
    ('n', 'Fuente: docs/proyecto/arquetipos-e-insights.md (21 sep 2026).'),
]))
S.append(('2.2', [
    'Los cuatro recorridos actuales se reconstruyeron con las 59 observaciones de la inspección (entrega 2, láminas 14 a 18).',
    ('t', [
        ['Arquetipo', 'Punto de dolor', 'Final del recorrido hoy', 'Oportunidad'],
        ['A1 Residente', 'El menú tiene seis destinos y ninguno menciona visitas ni ingresos', 'Sale del sistema por WhatsApp', 'Otorgar un Pase con motivo y ventana'],
        ['A2 Colaborador', 'Para entrar dos días a la semana queda dado de alta como permanente, con correo', 'Alta de personal permanente', 'Pase recurrente por días y franja'],
        ['A3 Visitante', 'La única aprobación humana del sistema aprueba su cuenta, no su ingreso', 'Cuenta sin fecha de fin', 'Pase por WhatsApp, sin cuenta'],
        ['A4 Administración', 'No existe bandeja de aprobación en ninguno de los cuatro paneles', 'Nada que auditar', 'Franjas y constancia'],
    ], [1900, 3100, 2160, 2600]),
    '**Conclusión del mapa.** Los cuatro recorridos se rompen en el mismo punto: nadie puede decir para cuándo y hasta cuándo. El objeto que falta en los cuatro es el mismo, el Pase.',
]))
S.append(('2.3', [
    ('-', '**A1.** Los residentes ya deciden quién entra, pero creen que no, porque el producto les niega en pantalla la autoridad que les dio en la base de datos. → Nombrar y acotar, no traspasar.'),
    ('-', '**A2.** El dato que más cuesta pedirle al colaborador (el correo) es el que rompe la sincronización con la puerta. → Una decisión resuelve la fricción y la falla técnica.'),
    ('-', '**A3.** La vía que menos datos personales exige (la placa por LPR) es la única que hoy no crea persona en HikCentral. → El vehículo de la visita es el primer canal del Pase.'),
    ('-', '**A4.** La administración cree conservar un control que no ejerce. → El argumento de venta es «hoy no tiene ese control y esto se lo da».'),
    ('n', 'Los veinte insights completos, cinco por arquetipo, están en el documento unificado de diagnóstico §6.'),
]))
S.append(('2.4', [
    'El diseño emocional parte de una pregunta del diagnóstico: ¿qué siente el residente cuando la app le dice una cosa y la puerta hace otra? La respuesta es desconfianza. Por eso la emoción que busca Kino es **certeza tranquila**: saber, sin tener que preguntar, que la persona puede entrar.',
    ('t', [
        ['Nivel (Norman)', 'Decisión', 'Responde a'],
        ['Visceral', 'El Pase vigente late; al vencer se apaga; al revocarse queda cortado. Tema oscuro canónico y aurora bioluminiscente, sin candados, escudos ni muros', 'Hoy no existe el concepto de acceso temporal: el estado tiene que verse vivo'],
        ['Conductual', 'Crear un Pase en 3 toques o menos; los límites se ven antes de crear; revocar se deshace durante 5 s', 'El competidor es la llamada a portería, que es gratis y conocida'],
        ['Reflexivo', 'Estado honesto: solo es vigente lo que el lector confirmó; cada rechazo lleva su motivo', 'Simetría invertida: el portero ve de los residentes lo que ellos no ven de sí mismos'],
    ], [1800, 4560, 3400]),
    ('n', 'Fuentes: decisiones.md (Parada 3 aprobada, 24 sep 2026); voz.json (perfil NN/g aprobado el 22 sep 2026).'),
]))

# 3 · ESTRATEGIA DE SERVICIO --------------------------------------------------------------------------
S.append(('3.1', [
    '**Objetivo general.** Reunir el conocimiento y la autoridad para decidir quién entra a un conjunto: que el residente otorgue, acote y revoque el ingreso de sus visitas y colaboradores, dentro de los límites de la administración, sobre el hardware que el conjunto ya tiene y sin crear personas permanentes.',
    '**Meta general (oct 2027).** 4 conjuntos con pago; 95 % de los Pases confirmados por el lector en menos de 60 s; ningún ingreso que exija dar de alta a una persona permanente.',
    ('t', [
        ['#', 'Objetivo SMART (acción + métrica + usuario + contexto + tiempo)', 'Punto de partida'],
        ['OE1', 'Lograr que el 90 % de 5 residentes de Monte Sereno cree un Pase de visita en menos de 30 s y 3 toques o menos en una prueba con el prototipo, antes del 9 nov 2026', 'La tarea no existe hoy'],
        ['OE2', 'Lograr que el 60 % de las casas de Villas Campestres cree al menos un Pase en las primeras 8 semanas del piloto (ene–feb 2027)', '0 Pases'],
        ['OE3', 'Lograr que el 80 % de los ingresos de colaboradores recurrentes de Villas ocurra con un Pase y sin llamada a portería en el primer trimestre del piloto', 'Se mide en la semana 1 con la minuta'],
        ['OE4', 'Lograr que el 98 % de los Pases quede confirmado por el lector en menos de 60 s y recuperar Refugio a ≥ 95 % de usuarios sincronizados antes del 31 mar 2027', 'Refugio: 0/312 y 711 errores'],
        ['OE5', 'Lograr que Monte Sereno renueve y que 2 conjuntos nuevos firmen piloto pagado antes del 31 oct 2027', '1 cliente'],
    ], [700, 6560, 2500]),
    ('n', 'Las metas de OE2, OE3 y OE5 son supuestos del equipo; se ajustan con la medición de la semana 1 del piloto. Detalle y KPI con método GQM: entrega-3/estrategia.md §3 y §7.'),
]))
S.append(('3.2', [
    ('t', [
        ['Para', 'Kino le da', 'Frente a'],
        ['El residente', 'Otorgar, extender y revocar Pases desde el celular, con la persona reciente a un toque, y saber cuándo entró', 'Llamar a portería o mandar un WhatsApp que nadie registra'],
        ['La visita y el colaborador', 'Entrar con QR, placa o código sin crear cuenta', 'Dar documento, teléfono y correo de por vida'],
        ['Portería', 'Ver por qué el lector dejó o no dejó entrar a alguien, y llamar al residente', 'Supervisar sin poder actuar'],
        ['La administración (compra)', 'Fijar límites y ver quién autorizó a quién, sobre el hardware que ya pagó', 'Una autoridad nominal que no ejerce y una integración caída'],
    ], [2300, 4460, 3000]),
    '**Enunciado.** Para la administración de un conjunto cerrado que ya tiene lectores instalados, Kino es la capa que deja a cada residente otorgar Pases con vigencia dentro de los límites del conjunto, con constancia de cada ingreso y sin crear cuentas para las visitas.',
]))
S.append(('3.3', [
    'Cada estrategia se nombra con un sustantivo, responde al cómo y se ubica en uno de los cuatro ejes del curso.',
    ('t', [
        ['Objetivo', 'Estrategia', 'Eje', 'Tácticas (qué · cómo · quién · cuándo)'],
        ['OE1', 'Simplificación del otorgamiento', 'Interactividad y personalización', 'Volver a invitar a un toque; límites visibles antes de crear · equipo · prototipo, oct 2026'],
        ['OE1', 'Validación con residentes reales', 'Soporte y acompañamiento', 'Prueba con 5 residentes, SEQ y SUS · equipo y administración · 27 oct – 7 nov 2026'],
        ['OE2', 'Acompañamiento de la adopción', 'Soporte y acompañamiento', 'Día de lanzamiento en la entrada; línea por WhatsApp · equipo · ene 2027'],
        ['OE2', 'Diversificación de los canales del Pase', 'Omnicanalidad y accesibilidad', 'Imagen y enlace por WhatsApp; QR, placa y código · equipo · dic 2026'],
        ['OE3', 'Recurrencia del colaborador', 'Automatización y gestión', 'Pase con días y franja en HikCentral · equipo con Manuel · dic 2026 – ene 2027'],
        ['OE4', 'Integración confiable', 'Automatización y gestión', 'Alta con teléfono; reintentar las 711; monitor de sincronización · nov 2026 – ene 2027'],
        ['OE4', 'Transparencia del estado', 'Automatización y gestión', 'Vigente solo con la respuesta del lector · prototipo hecho, producción ene 2027'],
        ['OE5', 'Penetración por los instaladores', 'Omnicanalidad y accesibilidad', 'Ficha comercial para instaladores Hikvision · abr – jun 2027'],
        ['OE5', 'Fidelización con evidencia', 'Automatización y gestión', 'Reporte semanal con entradas, rechazos y salud del lector · feb 2027'],
    ], [800, 2500, 2400, 4060]),
    ('n', 'Plan de acción, horizonte de empresa, lista de mercado y fichas de producto: entrega-3/estrategia.md §6, §9 y §10.'),
]))
for c, e in [('3.4', 'Entrega 5'), ('3.5', 'Entrega 5'), ('3.6', 'Entrega 5'), ('3.7', 'Entrega 5')]:
    S.append((c, [('n', f'Se entrega en la {e}. Los indicadores ya están definidos con el método GQM en entrega-3/estrategia.md §7.')]))

# 4 · ESPECIFICACIONES FUNCIONALES ---------------------------------------------------------------------
S.append(('4.1', [('n', 'Se entrega en la Entrega 4. El plan de acción preliminar está en entrega-3/estrategia.md §6.')]))
S.append(('4.2', [('n', 'Se entrega en la Entrega 4. Los once flujos F-01 a F-11 del archivo de Figma «Kino · App» (página 02 Flujos) son su insumo.')]))
S.append(('4.3', [
    ('t', [
        ['Tipo', 'Requerimiento', 'Origen'],
        ['Funcional', 'El residente crea, extiende y revoca Pases de visita y de colaborador; la visita entra con QR, placa o código; la administración fija franjas; el residente decide cuántas visitas y por cuánto tiempo, incluidas estadías de semanas o meses', 'Decisiones del proyecto y E3-2 (19 oct)'],
        ['Funcional', 'Ingreso a la app con código por WhatsApp, sin contraseña; el registro se valida contra la cédula que ya está en la base', 'Decisiones tomadas'],
        ['Técnico', 'El Pase se da de alta en HikCentral como persona temporal con «Válido desde / hasta»; el teléfono reemplaza al correo obligatorio', 'Hechos vigentes: 711 errores add_person'],
        ['Técnico', 'El estado se deriva de hechos: un Pase solo es vigente si el lector lo confirmó', 'Regla de estado honesto, @kino/motion'],
        ['Estético', 'Tema oscuro canónico; dos verdes (#00BB83 marca, #00D595 crear Pase); el arco solo en lo que es un Pase; JetBrains Mono para placas, horas y códigos', 'decisiones.md, Parada 3'],
        ['Comunicativo', 'Voz exacta y honesta con el estado; «Pase» y nunca «permiso»; «Visita» en la interfaz; sin exclamaciones ni promesas de seguridad total', 'voz.json, aprobado 22 sep 2026'],
        ['Legal', 'La biometría nunca se exige y siempre hay una vía no biométrica (Ley 1581 de 2012, Resolución SIC 52185 de 2025)', 'Entorno'],
    ], [1500, 5660, 2600]),
]))
S.append(('4.4', [('n', 'Se entrega en la Entrega Final (Desarrollo Front End).')]))

# 5 · DISEÑO DE INTERACCIÓN ---------------------------------------------------------------------------
S.append(('5.1', [
    '**Del modelo mental al modelo conceptual.** El modelo mental del residente es «estos son mis invitados y yo decido quién entra a mi casa». El sistema actual piensa «todos son usuarios que un tercero aprueba». El modelo conceptual de Kino adopta el del residente y lo hace objeto: el Pase.',
    ('t', [
        ['Atributo del Pase', 'Qué es', 'Responde a'],
        ['Autor', 'El residente que lo otorga. Sin autor no se puede revisar, corregir ni defender ante el consejo', 'Trazabilidad'],
        ['Motivo', 'Por qué entra esta persona', 'Constancia'],
        ['Vigencia', 'Desde cuándo y hasta cuándo, dentro del máximo que fije el conjunto. Caduca solo', 'Acceso temporal, que hoy no existe'],
        ['Modo', 'Cómo se verifica: placa, QR o código de un solo uso. Los tres conviven', 'Visita sin cuenta'],
        ['Prohibición', 'No crea una persona permanente en la puerta', 'Los 711 errores y la cuenta de la visita'],
    ], [2200, 5160, 2400]),
    ('h', 'Estados'),
    'Previsto → Sin confirmar → Vigente → Por vencer → Usado, Vencido o Revocado. En la entrada puede ocurrir el evento Rechazado, con su motivo. Cada transición tiene su verbo de movimiento: aparecer (820 ms), responder (240 ms), caducar (900 ms) y revocar.',
]))
S.append(('5.2', [
    'El diseño conceptual se representa en dos piezas que conviven: el archivo de Figma «Kino · App» (226 pantallas en oscuro y claro, cada una con su ficha) y un prototipo navegable en código donde los cuatro actores comparten un solo estado. Lo que hace uno le cambia la pantalla a otro: el residente crea el Pase, la visita lo abre, portería lo lee y al residente le llega el aviso.',
    ('h', 'QA del prototipo de Figma (19 oct 2026)'),
    'Ocho especialidades revisadas, 31 hallazgos con nodo y severidad. Los de mayor severidad: solo 22 reacciones en todo el archivo y ninguna interacción entre actores (4); ningún estado depende del tiempo (3); el residente nunca ve su Pase como objeto (3); variables «{cupo}» y «[PENDIENTE]» visibles en pantallas (3). Detalle: entrega-3/qa-prototipo.md.',
    ('h', 'Inventario de interacciones'),
    ('t', [
        ['ID', 'Interacción', 'Disparador → respuesta', 'Regla · efecto en HikCentral'],
        ['I-01', 'Código por WhatsApp', 'Enviar código → llega y se llena solo', 'Teléfono obligatorio y único'],
        ['I-02', 'Pase vivo en la lista', 'Paso del tiempo → la barra se consume; vigente late', 'Vencido = el lector deja de aceptarlo'],
        ['I-03', 'Volver a invitar', 'Tocar una persona reciente → hoja ya llena', 'Crear en 3 toques o menos'],
        ['I-04', 'Hoja con gesto', 'Arrastrar → se cierra con resorte', 'Nada se crea hasta tocar Crear Pase'],
        ['I-05', 'Vigencia a tu medida', 'Unas horas, un día o Se queda → resumen «Así queda»', 'Sin tope: persona temporal con «Válido desde / hasta»'],
        ['I-06', 'Nacimiento del Pase', 'Crear Pase → aparece el arco, Sin confirmar', 'Alta de persona temporal'],
        ['I-07', 'Espera del lector', 'Respuesta del lector → borde continuo y latido', 'Vigente solo con confirmación'],
        ['I-08', 'Compartir por WhatsApp', 'Enviar → la visita recibe imagen con QR y enlace', 'La visita no crea cuenta'],
        ['I-09', 'Pase vivo de la visita', 'Abrir el enlace → QR, placa o código y cuenta regresiva', 'El QR es la credencial del lector'],
        ['I-10', 'Lectura en la entrada', 'Leer → la talanquera sube; resultado legible desde 3 m', 'El lector permite el ingreso'],
        ['I-11', 'Aviso de llegada', 'El lector deja entrar → aviso al residente', 'Evento de acceso de HikCentral'],
        ['I-12', 'Rechazo con motivo', 'Pase vencido o revocado → motivo y llamar al residente', 'La llamada no abre la entrada'],
        ['I-13', 'Mantener para revocar', 'Mantener 0,8 s → corte y deshacer por 5 s', 'Baja al vencer el deshacer'],
        ['I-14', 'Extender', '+1 h, +1 día o +1 semana → la barra crece', 'Actualiza «Válido hasta»'],
        ['I-15', 'Franjas con vista previa', 'Mover una franja → qué Pase quedaría fuera', 'Los activos conservan su vigencia'],
        ['I-16', 'Integración caída y arreglo', 'Reintentar con teléfono → los contadores suben', '711 errores por el campo correo'],
        ['I-17', 'Movimiento reducido', 'Ajuste del sistema → fundidos', 'Política de @kino/motion'],
        ['I-18', 'Pase en la billetera (planeada)', 'Agregar → vive en la pantalla bloqueada', 'Mismo QR'],
        ['I-19', 'Háptica por estado (planeada)', 'Confirmación, rechazo, revocar → vibración distinta', 'Nunca solo color'],
        ['I-20', 'Rostro como cuarto modo (planeada)', 'Enrolamiento único → entra sin teléfono', 'Opcional, con autorización (SIC 52185)'],
    ], [700, 2300, 3660, 3100]),
    ('h', 'Exploración biopunk (propuesta)'),
    'El Pase como tejido: late mientras está vigente, se marchita al vencer, cicatriza al revocarse y el lector reconoce con una sinapsis. Se activa con la tecla B del prototipo y no toca ningún token aprobado. Queda en decisiones.md con estado PROPUESTA.',
]))

# 6 · DISEÑO Y EVALUACIÓN DE LA EXPERIENCIA ------------------------------------------------------------
S.append(('6.1', [
    'La validación de esta entrega tiene dos partes: una evaluación por inspección ya hecha sobre el prototipo y un experimento con residentes reales que se corre entre el 27 de octubre y el 7 de noviembre de 2026.',
    ('h', 'Parte 1 · Evaluación por inspección con los arquetipos (hecha)'),
    'Recorrido cognitivo de las tareas principales del prototipo, poniéndose en el contexto de cada arquetipo del diagnóstico, más la revisión de las 10 heurísticas de Nielsen. Es una evaluación de expertos; no reemplaza la prueba con usuarios.',
    ('t', [
        ['Arquetipo y contexto', 'Tarea', 'Dónde se traba', 'Sev.', 'Qué cambió'],
        ['A3 · visita que llega sin datos móviles', 'Entrar con el Pase', 'La imagen del WhatsApp no traía un QR legible', '3', 'La imagen lleva QR real, código y placa'],
        ['A1 · residente con una mano, fuera de casa', 'Crear un Pase para dentro de varias horas', 'Elegir una hora lejana exige muchos toques', '2', 'Atajos «Ya», «Esta tarde», «Mañana»'],
        ['A1 · familiar que se queda un mes', 'Crear un Pase largo', 'Solo había Pases de horas', '3', '«Se queda»: de 3 días a 3 meses, entra y sale'],
        ['A4 · portería en hora pico', 'Leer varias llegadas seguidas', 'Una lectura tapa la anterior', '2', 'Bitácora con la última fila resaltada'],
        ['A1 · revocar por error', 'Revocar un Pase', 'El diálogo no deja arreglar el error común', '3', 'Mantener presionado y deshacer por 5 s'],
        ['A4 · administración', 'Mover una franja', 'No se veía el efecto en los Pases activos', '2', 'Vista previa del cambio'],
    ], [2200, 1700, 2600, 600, 2660]),
    ('h', 'Parte 2 · Experimento con residentes (protocolo)'),
    ('-', '**Participantes.** 5 residentes de Monte Sereno, con al menos uno de Refugio y uno de Villas; uno mayor de 60 años; uno que tenga colaborador recurrente.'),
    ('-', '**Tareas.** T1 entrar con el código de WhatsApp; T2 crear un Pase para una visita que llega ya; T3 enviarlo por WhatsApp; T4 crear el Pase recurrente de su empleada; T5 extender un Pase una hora; T6 revocar un Pase y deshacerlo.'),
    ('-', '**Métricas por tarea.** Éxito sin ayuda (sí / con ayuda / no), tiempo en segundos, errores y SEQ (1 a 7). Al cierre, SUS (10 ítems).'),
    ('-', '**Guion.** Consentimiento verbal; «piensa en voz alta»; no se ayuda salvo bloqueo de 60 s; tres preguntas de cierre: qué te dio confianza, qué te dio duda, a quién se lo darías primero.'),
    ('-', '**Criterio.** OE1 se cumple si 4 de 5 crean un Pase en menos de 30 s y SUS ≥ 80.'),
    ('t', [
        ['Participante', 'T1', 'T2 (s)', 'T3', 'T4', 'T5', 'T6', 'SUS'],
        ['P1', '', '', '', '', '', '', ''],
        ['P2', '', '', '', '', '', '', ''],
        ['P3', '', '', '', '', '', '', ''],
        ['P4', '', '', '', '', '', '', ''],
        ['P5', '', '', '', '', '', '', ''],
    ], [2160, 1100, 1100, 1100, 1100, 1100, 1100, 1000]),
    ('n', 'La hoja se llena en la sesión. Los resultados entran a la Biblia (6.1 y 3.6) y al deck antes de la sustentación.'),
]))
S.append(('6.2', [('n', 'Se entrega en la Entrega 5. Métricas de la experiencia definidas: activación de casas, retención, NPS de la administración (estrategia.md §7).')]))
S.append(('6.3', [('n', 'Se entrega en la Entrega 5. Métricas de la interacción definidas: tiempo para crear un Pase, éxito de la tarea, SEQ, SUS y discrepancia app–puerta.')]))

# 7 · IMPLEMENTACIÓN Y TECNOLOGÍA ----------------------------------------------------------------------
S.append(('7.1', [('n', 'Se entrega en la Entrega 4. Base disponible: prototipo en TypeScript con Preact, @kino/motion (tokens, núcleo del Pase, runtime web) y @kino/motion-nativo (React Native).')]))
S.append(('7.2', [('n', 'Se entrega en la Entrega Final.')]))

SECCIONES = S
HECHOS = ['1.1', '1.2', '1.3', '1.4', '1.5', '2.1', '2.2', '2.3', '2.4', '3.1', '3.2', '3.3', '4.3', '5.1', '5.2', '6.1']
