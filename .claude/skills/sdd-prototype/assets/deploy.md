# Vista local y despliegue del prototipo
Estado: BORRADOR
Plataforma: [local o proveedor elegido por el usuario]

## Archivos públicos y privados
Servir únicamente public/. Conservar contexto, registros de validación, este documento y server.js fuera de public/.

## Vista privada local
Requisito: Node.js con módulos estándar. El servidor incluido no necesita npm install.
Configurar AUTH_USER y AUTH_PASS en el entorno mediante el mecanismo de secretos elegido. No poner valores en este documento, en Git ni en argumentos de comandos guardados.

```sh
node server.js
```

HOST por defecto: 127.0.0.1. PORT por defecto: 3000. Sin credenciales el servidor se niega a arrancar. Cambiar HOST solo cuando el entorno lo requiera. El directorio public/ debe existir y contener index.html.

## Despliegue remoto (solo con autorización)
[Adaptar los pasos al proveedor confirmado, verificar su documentación actual y exigir HTTPS/TLS en el proxy. Configurar variables mediante su almacén de secretos. No atribuir protección privada a un hosting que solo sirve archivos públicos.]

## Nueva versión y recuperación
[Ruta, comando verificado, versión anterior y forma de restaurarla. No publicar automáticamente.]

## Verificación
- Sin credenciales y con credenciales incorrectas: 401.
- Con credenciales válidas: index.html y recursos públicos accesibles.
- Contexto, registros, archivos ocultos y rutas que salgan de public/: inaccesibles.
- Banner visible y datos ficticios en todas las pantallas.
