# Código

Apps y paquetes del producto.

## Estructura prevista

| Carpeta | Qué va |
|---|---|
| `apps/` | Aplicaciones que se despliegan: app del residente, panel de administración, portería, servicios |
| `paquetes/` | Bibliotecas compartidas entre apps: modelo de datos, cliente de HikCentral, tokens de la marca nueva |

Cada app o paquete lleva su `README.md` con: qué hace, cómo se instala, cómo se prueba y quién lo mantiene.

## Reglas

- TypeScript por defecto. Supuestos declarados arriba de cada módulo que dependa de algo externo.
- Pruebas junto al código. Un PR que cambia comportamiento trae su prueba.
- Secretos en variables de entorno, nunca en el repositorio. `.env.example` sí se versiona.
- Los paquetes de motion de pre-kino (`../../pre-kino/paquetes/`) son de la marca anterior. Se pueden leer como referencia técnica.
