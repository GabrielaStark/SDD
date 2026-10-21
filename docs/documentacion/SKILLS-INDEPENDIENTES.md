# Decisiones de adaptación

- Conservar los nueve nombres y la ubicación .claude/skills para compatibilidad con usuarios actuales. El ZIP elimina la dependencia de esa ubicación: contiene solamente la carpeta de skill.
- Incorporar el procedimiento de los subagentes en cada SKILL.md; conservar los subagentes como adaptadores opcionales. La skill define capacidades, no aislamiento de contexto ni un modelo concreto.
- Empaquetar plantillas y reglas necesarias dentro de cada carpeta. La duplicación puntual de EARS entre paquetes es deliberada para que no dependan entre sí; dentro de cada paquete hay una referencia EARS explícita.
- Aceptar documentos externos y texto de intención. Validar contenido y aprobación, no el nombre del generador.
- Conservar revisión humana y trazabilidad. Registrar la versión aprobada; no confundir checklist aprobado por un modelo con autorización humana. Gates de texto son orientación, no enforcement técnico.
- Unificar rutas por defecto de onboarding bajo docs/, aceptar documentos previos en raíz y no sobrescribir instrucciones existentes.
- Definir explícitamente la excepción de trazabilidad de tareas transversales mediante Justification. Ordenar mantenimiento por dependencias y riesgo, con validación después del último cambio ejecutable.
- Distinguir ausencia de pruebas, fallos previos e infraestructura de regresiones introducidas. Planificar caracterización cuando falten tests.
- Separar public/ de contexto y logs en prototipos; quitar credenciales por defecto y dependencias del servidor opcional. No automatizar despliegue ni aprobación del cliente.
- Mantener la licencia MIT original en los paquetes. No cambiar licencias ni condiciones comerciales durante esta adaptación.

## Alcance de la validación
El validador comprueba metadatos, recursos locales, aislamiento de paquetes, consistencia de copias de templates y contenido de ZIP. Los tests ejercitan fallos del empaquetador y el servidor de prototipo. Las evaluaciones con agentes se realizan sobre extracciones limpias; ver PUBLICACION.md. Nada de esto certifica compatibilidad de todos los clientes ni aceptación por Agensi.
