# {{nombre}} · Guía de contenido

Fase 2. Estructura inspirada en la Mailchimp Content Style Guide (styleguide.mailchimp.com). **Licencia:** esa guía es CC BY-NC 4.0 (no comercial): se toma la estructura, el texto se escribe propio para cada cliente. Alternativa de dominio público: 18F Content Guide.

La parte medible de esta guía vive en `../voz.json` (perfil, vocabulario, patrones). Este documento explica y da ejemplos; si algo aquí contradice `voz.json`, manda `voz.json` porque es lo que se verifica.

## 1. Voz
Quiénes somos al escribir. Copiar de `voz.json` los rasgos «somos / no somos» y dar un ejemplo real de cada uno.

## 2. Tono según la situación
La voz no cambia; el tono sí. Tabla con los momentos reales del cliente:

| Situación | Cómo se siente el lector | Tono | Ejemplo |
|---|---|---|---|
| Bienvenida | | | |
| Error / algo salió mal | | | |
| Confirmación | | | |
| Venta / anuncio | | | |

## 3. Vocabulario
Términos propios, términos a evitar y pares que no se mezclan. Fuente: `voz.json`.

## 4. Gramática y mecánica
- Tuteo / usteo:
- Números, horas, fechas y moneda (ej. «6:00 p. m.», «$ 1.200.000»):
- Mayúsculas en títulos (en español, solo la inicial):
- Signos: sin raya de efecto; comillas latinas «» o inglesas, pero una sola convención.
- Siglas permitidas:

## 5. Escribir sobre la marca
Nombre correcto, cómo no se escribe, nombres de productos.

## 6. Accesibilidad e inclusión
- Texto alternativo para imágenes: qué describir.
- Lenguaje inclusivo: decisión y alcance.
- Enlaces: el texto dice a dónde lleva (nunca «clic aquí»).

## 7. Por canal
Reglas específicas de: notificaciones, correo, redes, web, documentos formales.

## Compuerta de salida
- [ ] `npm run voz -- {{id}}` pasa sobre las muestras reales del cliente.
- [ ] Si hay textos «antes/después» del cliente, `npm run calibrar-voz` da 0 falsos positivos.
- [ ] El perfil de `voz.json` dejó de ser «borrador» y lo aprobó el cliente.
