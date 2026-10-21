# Calidad del diseño técnico

## Las nueve secciones
| Sección | Decisiones a explicitar |
|---|---|
| 1. Overview | Stack acordado, arquitectura y entorno de operación |
| 2. Architecture | Componentes, responsabilidades, límites y dependencias |
| 3. Data Model | Entidades, relaciones, constraints, índices y políticas de borrado cuando apliquen |
| 4. Interface Contracts | Firmas, payloads, tipos, validaciones, códigos y errores observables |
| 5. Technical Decisions | ADRs de decisiones no obvias con contexto y consecuencias positivas/negativas |
| 6. Critical Flows | Orden de operaciones y errores en flujos donde importan las interacciones |
| 7. Error & Edge Case Strategy | Validación, recuperación, reintentos, degradación y límites |
| 8. Testing Strategy | Verificaciones por criterio funcional/NFR, nivel y condiciones de prueba |
| 9. Traceability | Mapa completo de criterio a componente/decisión y verificación |

Marcar N/A con motivo si una sección no aplica. No inventar una base de datos para llenar Data Model ni una API HTTP para llenar contratos. Usar la plantilla como estructura, no como elección predeterminada de stack.

## Contratos y arquitectura
- Decidir según requisitos y restricciones aprobadas; separar opciones aún pendientes.
- Una responsabilidad clara por componente. Declarar límites que eviten introducir comportamiento fuera de alcance.
- En datos relacionales, especificar PK/FK, nulabilidad, unicidad, índices justificados y políticas de cascade; adaptar al paradigma real.
- En interfaces, concretar tipos y comportamiento de error; no sustituir un contrato por «devuelve un error apropiado».
- Para operaciones distribuidas, declarar supuestos de idempotencia y recuperación cuando lo exijan los requisitos.
- Mermaid solo para relaciones o secuencias que ayuden a revisar. Dividir diagramas grandes.
- Mantener trazabilidad también para seguridad, rendimiento, accesibilidad y demás NFR aprobados.

## ADR
```markdown
### ADR-001: [Decisión]
- Contexto: [restricción o criterio que la motiva]
- Decisión: [alternativa elegida y alcance]
- Consecuencias positivas: [beneficios]
- Consecuencias negativas: [costes y límites]
```

No reabrir decisiones aprobadas sin evidencia nueva; si una decisión necesaria contradice requisitos, reportarlo antes de seguir.

## Límites de implementación y tamaño
Permitir contratos, firmas, esquemas de datos y pseudocódigo de alto nivel. No escribir funciones completas de implementación. Mantener un documento revisable: 300–700 líneas es una orientación para sistemas grandes, nunca un mínimo. Para un alcance pequeño, un diseño breve puede ser suficiente. Si supera 800 líneas, proponer división por alcance y preservar trazabilidad.

## Trazabilidad
| Criterio | Componente/decisión | Verificación prevista | Estado |
|---|---|---|---|
| 1.1 | [componente] | [prueba específica] | planeada |
| NFR-1 | [decisión] | [métrica y condiciones] | planeada |

No confundir pruebas previstas con pruebas ejecutadas. Cada criterio debe tener cobertura; cada componente debe justificarse por requisitos o restricciones explícitas.

## Checklist
- [ ] Requisitos sustantivos y aprobación de la versión actual verificados.
- [ ] Nueve secciones con decisiones concretas o N/A justificado.
- [ ] Stack y restricciones acordados; ninguna funcionalidad añadida por intuición.
- [ ] Contratos y errores específicos; ADRs con costes.
- [ ] Flujos críticos y casos de error cubiertos.
- [ ] Trazabilidad funcional y NFR completa, sin pruebas ficticias.
- [ ] Sin código de implementación, sin rellenar por alcanzar una cantidad de líneas.
- [ ] Pendientes y estado de revisión visibles; la aprobación final la da el humano.
