# Calidad del diseño delta

## Las nueve secciones
1. Overview del Delta: stack heredado y alcance exacto del cambio.
2. Architecture: distinguir componentes existentes usados, existentes modificados y nuevos; declarar responsabilidades.
3. Data Model Delta: solo cambios de datos pertinentes, compatibilidad y recuperación cuando apliquen.
4. Interface Contracts Delta: comportamiento anterior, extensión y parte preservada de contratos afectados.
5. Technical Decisions: ADR-DNNN para decisiones nuevas; citar las heredadas sin rediseñarlas.
6. Critical Flows Afectados: interacciones nuevas y coexistencia con flujos vigentes.
7. Error & Edge Case Strategy: integrar errores nuevos con el contrato existente.
8. Testing Strategy: pruebas del delta y caracterización/regresión de invariantes.
9. Traceability: criterios funcionales/NFR y una tabla separada de invariantes con pruebas.

Usar N/A con explicación cuando una sección no aplique. La plantilla es una guía; los stacks que aparecen como ejemplo no son dependencias de esta skill.

## Contexto heredado
Mapas técnicos y documentos en raíz o docs/ son opcionales. Si faltan, inspeccionar el código para identificar stack, componentes y contratos relevantes. No exigir ejecutar onboarding ni otro agente. Corroborar la documentación existente y declarar límites si falta código.

## Alcance y compatibilidad
- Toda modificación debe corresponder a la superficie aprobada. Si aparecen impactos adicionales, explicarlos y solicitar revisión del alcance antes de diseñarlos como acordados.
- No reemplazar arquitectura, stack o contratos ajenos al cambio. Si el requisito exige hacerlo, señalar la incompatibilidad de alcance y pedir una decisión.
- Conservar comportamiento por defecto y consumidores existentes donde se hayan definido invariantes; separar extensiones de reemplazos aprobados.
- Una columna con DEFAULT no demuestra por sí sola compatibilidad: revisar consumidores, queries, serialización, constraints y despliegues coexistentes.
- Para cambios de datos, explicitar transición, comprobaciones, recuperación y cualquier riesgo de pérdida; no prometer rollback de operaciones irreversibles.
- Tratar cada integración de riesgo medio/alto con mitigación concreta, no con frases como «sin impacto» sin evidencia.

## ADR del delta
```markdown
### ADR-D001: [Decisión nueva]
- Contexto: [requisito y restricciones heredadas]
- Decisión: [cambio acotado]
- Consecuencias positivas: [beneficio]
- Consecuencias negativas: [riesgo, coste o limitación]
```

## Invariantes y verificación
| Invariante | Componente/fuente | Prueba existente o propuesta | ¿Ejecutada? | Limitación |
|---|---|---|---|---|

Si no hay tests, proponer caracterización antes del cambio. Si el entorno impide ejecutarlos, declarar la limitación y la comprobación pendiente. No inventar métodos de test existentes ni resultados. Una tabla no constituye garantía de no regresión.

## Tamaño y contenido
Permitir diagramas, contratos, tipos, esquemas y pseudocódigo breve. No implementar funciones. Mantener el delta revisable; 200–500 líneas es una orientación, nunca un mínimo. Si supera 600, proponer dividirlo. Un cambio pequeño puede describirse en menos espacio conservando las nueve secciones.

## Checklist
- [ ] Versión aprobada y superficie/invariantes válidas.
- [ ] Arquitectura corroborada, documentos opcionales correctamente tratados.
- [ ] Cambios y componentes nuevos justificados por alcance.
- [ ] Compatibilidad evaluada, no presumida.
- [ ] Decisiones nuevas con ADR y consecuencias.
- [ ] Criterios funcionales y NFR con diseño y verificación.
- [ ] Cada invariante con prueba existente, propuesta o limitación explícita.
- [ ] Requisitos reemplazados separados de invariantes preservadas.
- [ ] Pendientes y aprobación humana visibles; ningún cambio en código o producción.
