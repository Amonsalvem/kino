# Target y escala de prioridad de clientes

Propuesta para D-017. Se construye con lo que Villas demuestra hoy, no con el mercado total. Fuentes: `kino/investigacion/observacion/2026-11-17-inspeccion-app-soykino.md`, `kino/canon/proyecto.md` y pedido de Alejandro del 16 nov 2026.

## Conclusión

El cliente objetivo es **una comunidad de casas (parcelación o conjunto campestre) que ya tiene HikCentral instalado y funcionando, con 80 a 400 unidades, en el oriente antioqueño o el sur del Valle de Aburrá**. Ahí Kino repite lo que funciona en Villas sin vender hardware.

**Inferido:** la razón es la evidencia de Villas. Lo que funciona es la integración con la puerta (1.684 de 1.684 usuarios sincronizados) y el manejo de 27 empresas contratistas. El KEY todavía no se usa. Kino vende hoy integración y orden de colaboradores; el KEY es la promesa que la app nativa debe probar.

## Qué se le pide a un cliente

| Criterio | Peso | Por qué |
|---|---|---|
| Tiene Hikvision con HikCentral en operación | 30 | Es lo que Kino probó. Sin HikCentral, Kino tendría que vender e instalar hardware |
| Casas, no torres | 15 | Más vehículos (ANPR), más colaboradores y contratistas por unidad |
| 80 a 400 unidades | 15 | Con D-014, 80 unidades pagan $2.000.000 al mes; más de 400 pide más soporte del que hay |
| Flujo alto de colaboradores y contratistas | 10 | Es el ingreso más frecuente (`proyecto.md`) y Kino ya lo resuelve |
| Administración que decide antes de la asamblea | 10 | La asamblea aprueba el presupuesto en el primer trimestre (Ley 675 de 2001, art. 39) |
| A menos de 1 hora de Villas | 10 | Implementación y soporte presencial |
| Conoce Monte Sereno o comparte administrador | 10 | Referencia directa |

Puntaje sobre 100. **A**: 70 o más. **B**: 50 a 69. **C**: menos de 50.

## Escala de prioridad

```
Prioridad 0  Villas Campestres     → piloto; convertirlo en cliente que paga y referencia
Prioridad 1  Refugio y Sagrada     → después del informe del piloto (pedido de Alejandro)
Prioridad 2  Parcelaciones A       → casas + HikCentral activo, oriente antioqueño
Prioridad 3  Conjuntos B           → casas o mixtos con Hikvision sin HikCentral, o 400+ unidades
Prioridad 4  Edificios y clubes    → solo con un caso pedido; no se prospectan
Fuera        Sin hardware o con otra marca de control de acceso, hasta tener aliado de instalación
```

| Prioridad | Qué hace falta para venderle | Riesgo |
|---|---|---|
| 0 · Villas | Informe del piloto con cifras: KEY usados, eventos ligados, tiempo en portería, pagos | Si el KEY no se usa, el informe no prueba la promesa |
| 1 · Refugio y Sagrada | Reparar la sincronización de Refugio (0 de 388). Saber si Sagrada tiene hardware | Vender a Refugio con la integración caída daña la referencia |
| 2 · Parcelaciones A | Lista de prospectos con nombre, unidades, hardware y contacto | No hay lista. **Sin fuente** de cuántas existen en la zona |
| 3 · Conjuntos B | Paquete de instalación de HikCentral con un aliado (Daniel, IoT, D-007) | Kino pasa a vender proyecto de hardware |
| 4 · Edificios y clubes | Validar que el flujo de torres y socios cabe en el producto | El sitio ya los ofrece (S5) sin evidencia |

## Qué cambia en el sitio

1. Quitar «Con tu marca» (D-009).
2. Ordenar los segmentos según esta escala: parcelaciones primero.
3. Cambiar el `mailto:` por un formulario que pida unidades, tipo y hardware. Así cada prospecto llega ya con su puntaje.

## Qué falta para cerrar el target

| Dato | Para qué |
|---|---|
| Lista de 20 comunidades candidatas en El Retiro, Rionegro, La Ceja, Envigado y Llanogrande | Calcular el puntaje real |
| Qué marca de control de acceso tiene cada una | Separar A de B |
| Cuántas parcelaciones y conjuntos hay en esos municipios | Tamaño del mercado. La búsqueda web del 16 nov no encontró una cifra oficial; se pide a planeación municipal o a la Lonja |
