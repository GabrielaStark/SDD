# Anatomía y revisión de tareas

## Contrato
Cada tarea debe incluir checkbox sin marcar, ID estable, acción concreta, archivos/componentes, subpasos, dependencias, criterio de hecho y trazabilidad. No ejecutar el plan al redactarlo.

```markdown
- [ ] 1. Implementar validación del campo obligatorio
  - Componente: servicio de entrada definido en design.md.
  - Dependencias: ninguna.
  - Rechazar entrada ausente con FIELD_REQUIRED.
  - Criterio de hecho: el caso de entrada ausente cumple el contrato 1.3.
  - _Requirements: 1.3_

- [ ] 2. Crear pruebas de la validación
  - Dependencias: tarea 1.
  - Cubrir entrada ausente y entrada válida.
  - Criterio de hecho: pruebas ejecutadas con resultado registrado al implementar.
  - _Requirements: 1.3_
```

## Orden y alcance
- Ordenar por dependencias reales. Omitir capas no aplicables.
- Una tarea por ciclo de ejecución y revisión; dividir cambios que mezclan objetivos independientes.
- Incluir configuración, datos, lógica, interfaces, UI, integración, tests y documentación solo donde el diseño los justifique.
- Para tareas habilitadoras sin criterio directo: `_Requirements: -_ | _Design: ADR-001_` y explicar la dependencia. No inventar IDs de requisitos.
- Para spikes: pregunta concreta, límite acordado y salida que resuelva la incertidumbre.
- Mantener las pruebas identificables y asociadas al requisito, sin duplicar pruebas que ya cubran el comportamiento.

## Revisión
- Todo criterio funcional y NFR tiene implementación/decisión y validación asociada.
- Cada tarea tiene justificación y criterio verificable de hecho.
- No hay dependencias circulares ni tareas marcadas sin evidencia de ejecución.
- Un bloqueo de alcance se resuelve en requisitos/diseño, no se oculta como tarea.
- Al ejecutar en otra invocación, registrar comandos, resultados y revisión humana antes de marcar completo.
