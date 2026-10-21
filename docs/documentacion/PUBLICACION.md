# Publicar skills individuales

## Unidad de distribución
Cada entrada de skills.json identifica una skill completa. Empaquetar esa carpeta con SKILL.md, sus references/assets, metadatos opcionales en agents/openai.yaml y LICENSE. No incluir agentes de Claude, documentos del proyecto ni las otras skills.

## Preparación reproducible
1. Editar el procedimiento y recursos dentro de la carpeta correspondiente. Mantener name igual al nombre de carpeta; description debe explicar la tarea y sus disparadores.
2. Actualizar versión en skills.json cuando corresponda. Si cambia un asset reflejado en templates/, ejecutar `python scripts/skills.py sync-templates`.
3. Ejecutar `python scripts/skills.py validate` y `python -m unittest discover -s tests -v`.
4. Ejecutar `python scripts/skills.py package --skill NOMBRE`. Revisar el ZIP y su hash en dist/manifest.json.
5. Extraer ese ZIP en una carpeta limpia, sin el resto de SDD. Ejecutar los escenarios de evaluación con un agente capaz de leer sus recursos. Conservar resultados y limitaciones.

## Agensi
La documentación pública consultada el 19 de octubre de 2026 describe subida de ZIP con SKILL.md y recursos de apoyo desde Creator Dashboard, opciones gratuita/de pago y revisión previa. Su distribución por MCP puede entregar instrucciones y recursos sin instalar una carpeta local.

Antes de marcar una publicación como lista, verificar en la vista previa del marketplace que los recursos referenciados se entreguen al agente y que pueda producir las salidas. No asumir que todos los agentes o mecanismos de distribución resuelven recursos del mismo modo. Si el distribuidor no puede entregar archivos de apoyo, adaptar ese paquete o informar la limitación; no publicar instrucciones con enlaces inaccesibles.

La validación local no prueba la integración con Agensi, su aceptación editorial ni las condiciones comerciales de la cuenta. Crear un borrador de publicación, completar nombre/descripción/categoría y probar el paquete dentro del destino. Publicar, fijar precio o aceptar condiciones requiere decisión del titular.

Fuentes oficiales de referencia:
- https://www.agensi.io/learn/how-to-sell-skills-on-agensi
- https://www.agensi.io/sell
- https://agentskills.io/specification

## Escenarios por skill
| Skill | Caso positivo | Caso que debe frenar o limitar |
|---|---|---|
| onboarding | Repo sin documentación | Sin tests: declarar ausencia, no inventar cobertura |
| reglas-negocio | Repo sin onboarding | Restricción solo en UI: no atribuirla al servidor |
| sdd-requirements | Entrevista con actores y reglas claras | Umbral ambiguo: preguntar, no inventarlo |
| sdd-design | Requisitos manuales aprobados | Entrada vacía/no aprobada: pedir contenido/aprobación |
| sdd-tasks | Diseño y requisitos externos aprobados | Comportamiento sin requisito: reportar inconsistencia |
| sdd-requirements-mantenimiento | Feature descrito en conversación y código | Cambio contradice invariante: separar Behavior Replaced |
| sdd-design-delta | Delta aprobado, sin BIG_PICTURE | Impacto fuera de superficie: revisar alcance |
| sdd-tasks-risk | Proyecto sin tests | Baseline desconocido: planificar caracterización, no afirmar verde |
| sdd-prototype | Requisitos aprobados, sin branding | Rol nuevo en feedback: revisar requisitos antes del HTML |

## Evidencia mínima
Registrar paquete y SHA, agente/modelo, entrada, recursos disponibles, salida, preguntas solicitadas, comprobaciones hechas y fallos. Repetir en cada cliente que se anuncie como compatible. La autoevaluación del modelo no sustituye una revisión del resultado.
