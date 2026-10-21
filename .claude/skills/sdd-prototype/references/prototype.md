# Prototipo de validación

## Entregables
Colocar contenido servible exclusivamente en `public/`: index.html, pantallas y assets públicos. Mantener `context/`, `DEPLOY.md`, registros de validación y servidor fuera de esa carpeta. No incluir archivos privados en assets públicos ni referenciar rutas fuera de public.

## UI y alcance
- HTML/CSS y JavaScript mínimo, sin build obligatorio. El prototipo no selecciona la tecnología de producción.
- Banner fijo y no descartable: «MOCKUP NO FUNCIONAL — solo para validación de requisitos». Reservar espacio para no tapar contenido.
- Nombres ficticios, importes de demostración y correos con `example.com`. No trasladar datos reales de capturas.
- Navegación y estados visuales simulados; formularios sin envío real y cálculos estáticos. No conectar backend, autenticación de negocio ni persistencia real.
- Enlazar pantallas a criterios de requisitos y registrar limitaciones de la simulación.

## Recursos y servidor
Usar los recursos provistos por el usuario según su autorización. CSS local por defecto; no añadir telemetría ni dependencias remotas ocultas. Si se usa un servidor de acceso privado, copiar el ejemplo incluido; no instalar paquetes para él, pues usa módulos estándar de Node.js. Configurar AUTH_USER y AUTH_PASS por entorno, sin valores predeterminados. Mantener HOST=127.0.0.1 localmente; usar 0.0.0.0 solo si el entorno de despliegue lo requiere. En remoto, exigir TLS en el proxy: Basic Auth sobre HTTP no protege credenciales en tránsito.

El servidor limita archivos a public, rechaza rutas ocultas y symlinks que salgan de public, y no publica documentos del proyecto. No implementar una base de datos ni rutas de negocio. El prototipo sigue siendo un artefacto de validación, no una aplicación de producción.

## Feedback y cambios estructurales
Crear un registro nuevo por iteración. Preservar feedback y aprobaciones anteriores. El estado inicial es PENDIENTE; solo registrar APROBADO con confirmación humana identificable de esa versión.

Un rol, entidad, flujo, integración o restricción nuevo requiere revisar requisitos. Registrar lo pedido, pedir detalles faltantes y mostrar un delta a requisitos si el usuario lo solicita. Conservar IDs; no modificar silenciosamente una especificación aprobada. Esperar aprobación de los requisitos actualizados antes de implementar ese cambio en las pantallas. Este proceso puede hacerse directamente, sin otra skill.

Si hay demasiados cambios de alcance para una iteración, recomendar revisar el conjunto de requisitos. No convertir feedback ambiguo en decisiones de negocio.

## Despliegue y revisión
Generar DEPLOY.md con plataforma elegida, ejecución local, variables sin valores y pasos verificados de despliegue. Consultar documentación vigente para servicios externos cuando sea necesario; no inventar precios o características de planes. Publicar, enviar invitaciones, crear cuentas o hacer push solo cuando exista autorización del usuario para ello.

Comprobar navegación, accesibilidad básica, banners, ausencia de datos reales, autenticación si aplica y separación de documentos privados. Registrar pruebas ejecutadas y pruebas pendientes. La aprobación visual no demuestra correctitud de reglas de negocio ni certifica seguridad del producto final.
