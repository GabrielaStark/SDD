# Calidad de requisitos de mantenimiento

## Estructura del delta
| Sección | Contenido necesario |
|---|---|
| Contexto | Capacidad nueva, problema, solicitante y módulo implicado |
| Surface of Contact | Componentes, archivos, endpoints, tablas o servicios usados/modificados, evidencia y riesgo |
| Invariantes Preservadas | Comportamientos observables existentes que deben mantenerse, IDs I.N y fuente |
| Requirements del delta | Historias y criterios EARS del cambio, con IDs estables |
| Non-Functional Requirements | Restricciones nuevas o afectadas con IDs NFR-N |
| Tests Existentes a Preservar | Pruebas encontradas, invariantes cubiertas y huecos |
| Behavior Replaced | Solo si cambia intencionadamente un comportamiento previo; decisión y fuente |
| Out of Scope | Exclusiones del feature |
| Open Questions / Glossary | Incertidumbres y términos de dominio |

Usar la plantilla y la referencia EARS incluidas. Una intención en texto libre es válida; intent.md es opcional. No exigir documentación generada por otra skill.

## Superficie e invariantes
- Registrar todo componente relevante al cambio según el alcance inspeccionado; no afirmar exhaustividad del sistema completo.
- Riesgo alto: contratos compartidos, flujos críticos, incertidumbre o impacto amplio. Medio: modificación localizada. Bajo: consumo sin modificar, siempre que haya evidencia.
- Una superficie tentativa debe identificarse como tal y confirmarse con el humano. Si aparecen demasiados módulos afectados, proponer dividir el cambio.
- Cada invariante debe poder comprobarse y citar una fuente real. «La app no se rompe» no es una invariante verificable.
- No asumir que lectura implica riesgo nulo: considerar contratos, autorización, carga y efectos secundarios.
- Mantener al menos una invariante si se trata de preservación de un sistema existente; si no existe ninguna, revisar el alcance y tipo de trabajo con el usuario.

## Cambio de comportamiento
No preservar y reemplazar el mismo comportamiento a la vez. Por ejemplo, si se cambia la salida de un endpoint, documentar la parte que permanece, la que cambia, consumidores afectados y decisión explícita en Behavior Replaced. No modificar silenciosamente una invariante para que el diseño pase la revisión.

## Tests y contexto
Inspeccionar pruebas en el código. Separar existencia de ejecución; registrar pruebas no disponibles y huecos. Mapas técnicos, CLAUDE.md, BIG_PICTURE.md y REGLAS_DE_NEGOCIO.md pueden consultarse en raíz o docs/ si existen; contrastarlos con el código. Si faltan, reconocer directamente las áreas pertinentes. Su ausencia no exige instalar otras skills ni constituye por sí sola un bloqueo.

## Checklist
- [ ] Se describe el delta, no una reescritura implícita.
- [ ] Superficie con evidencia y riesgos, sin archivos inventados.
- [ ] Invariantes verificables y sin contradicción con cambios aprobados.
- [ ] Criterios funcionales/NFR atómicos y con IDs.
- [ ] Tests observados diferenciados de tests por crear o ejecutar.
- [ ] Behavior Replaced y exclusiones claros cuando correspondan.
- [ ] Incertidumbres y límites visibles, aprobación humana separada.

No garantizar ausencia de regresiones por tener un documento. El contrato sirve para planificar comprobaciones y someter el cambio a revisión.
