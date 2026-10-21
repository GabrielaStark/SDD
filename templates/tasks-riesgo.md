# Tasks: [Feature de mantenimiento]
> Estado: BORRADOR | Entradas aprobadas: [requisitos y diseño, versiones]

## Regression Shield
- [ ] 1. Registrar el baseline de los módulos afectados
  - Revisar el comando y el entorno antes de ejecutar durante la implementación.
  - Dependencias: ninguna.
  - Criterio de hecho: resultado, alcance y fallos previos registrados; bloqueos con tratamiento acordado.
  - _Requirements: -_ | _Invariants: -_
  - _Justification: gate previo a los cambios de la superficie aprobada._

- [ ] 2. Blindar [ID de invariante y comportamiento]
  - Archivos: [prueba y componente observado].
  - Dependencias: baseline resuelto, tarea 1.
  - Criterio de hecho: prueba de caracterización pasa contra el comportamiento actual antes de modificarlo.
  - _Requirements: -_ | _Invariants: [I.N]_

## Spikes (si aplica)
[Pregunta concreta, límite, resultado esperado, dependencias y trazabilidad o justificación.]

## Delta por dependencias y riesgo
- [ ] 3. [Modificar o añadir una capacidad acotada]
  - Archivos/componentes: [rutas].
  - Preservar: [comportamientos observables de las invariantes].
  - Dependencias: [blindaje y otras tareas previas].
  - Criterio de hecho: [criterio nuevo verificado y blindaje conservado].
  - _Requirements: [criterios/NFR]_ | _Invariants: [I.N o -]_

## Tests del delta e integración
[Tareas de validación del cambio y coexistencia con la misma anatomía.]

## Documentación
[Actualizar solo documentos afectados; referenciar requisitos/invariantes o justificar la tarea transversal.]

## No-Regression Validation
- [ ] N. Verificar el cambio y todas las invariantes después del último cambio ejecutable
  - Ejecutar suites y verificaciones manuales acordadas; registrar alcance y resultados.
  - Dependencias: todas las tareas que modifican comportamiento/configuración ejecutable.
  - Criterio de hecho: resultados del delta y de cada invariante documentados, sin fallos nuevos ni bloqueos sin resolver.
  - _Requirements: [criterios/NFR del delta]_ | _Invariants: [todas las invariantes reales]_

## Matriz de cobertura y límites
| Criterio/invariante | Implementación | Blindaje previo | Validación final |
|---|---|---|---|
[No confundir ausencia de pruebas con baseline verde. No prometer riesgo cero.]
