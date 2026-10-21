# Tareas de mantenimiento y regresión

## Contrato
Todas las tareas incluyen acción, subpasos, dependencias, criterio de hecho y ambos campos `_Requirements:_` e `_Invariants:_`. Referenciar criterios funcionales, NFR e invariantes reales.

Una tarea de cambio o blindaje debe referenciar al menos un requisito o invariante. Una tarea transversal (baseline, spike o documentación) puede usar ambos `-` únicamente si incluye `_Justification:_` con la decisión, superficie o tareas que habilita. Es una excepción explícita de trazabilidad, no permiso para trabajo fuera de alcance.

```markdown
- [ ] 1. Registrar baseline de las pruebas existentes
  - Identificar el comando en la configuración del proyecto y ejecutarlo al implementar este plan.
  - Dependencias: ninguna.
  - Criterio de hecho: resultado y fallos previos registrados antes de cambios.
  - _Requirements: -_ | _Invariants: -_
  - _Justification: gate previo a las modificaciones de la superficie aprobada._

- [ ] 2. Blindar la respuesta actual sin el parámetro nuevo
  - Crear prueba contra el código actual para el contrato I.1.
  - Dependencias: baseline resuelto, tarea 1.
  - Criterio de hecho: prueba pasa antes de modificar ese contrato.
  - _Requirements: -_ | _Invariants: I.1_

- [ ] 3. Extender el contrato con el parámetro aprobado
  - Añadir solo el comportamiento 1.1; preservar la respuesta sin parámetro.
  - Dependencias: tarea 2.
  - Criterio de hecho: caso nuevo cubierto y test de I.1 sigue pasando.
  - _Requirements: 1.1_ | _Invariants: I.1_
```

## Orden
1. Baseline: distinguir fallos previos de infraestructura y ausencia de pruebas.
2. Regression Shield: caracterización de invariantes antes de cada modificación que las afecta.
3. Spikes cuando una incertidumbre impida planificar; nunca excusa para cambiar producción.
4. Delta según dependencias y riesgo observado. Las capas son etiquetas, no un orden universal.
5. Pruebas del delta e integración de puntos de contacto de forma aislada.
6. Documentación afectada.
7. No-Regression Validation después del último cambio ejecutable; si hay un cambio posterior, repetir la validación.

## Cuando no hay tests o no pueden ejecutarse
No inventar baseline verde. Planificar la infraestructura mínima y pruebas de caracterización. Si el entorno no permite automatizar, describir una comprobación manual reproducible, sus límites y la decisión humana pendiente. Una prueba fallida no demuestra por sí sola que producción está rota. Registrar causa y no autorizar el cambio afectado hasta acordar tratamiento del bloqueo.

## Checklist
- Cada invariante tiene prueba existente o tarea de blindaje/verificación explícita.
- Cada criterio funcional y NFR tiene implementación y validación.
- Cada punto de riesgo medio/alto tiene mitigación y tarea asociada.
- Cada modificación cita lo preservado y el blindaje previo.
- Cada tarea tiene criterio de hecho y referencias o justificación transversal válida.
- La validación final cubre flujos relevantes y todas las invariantes con resultados, sin prometer riesgo cero.
- Ninguna tarea aparece completada por haber sido redactada.
