# Calidad de requisitos

## Estructura
1. Introduction: problema, usuarios y alcance en un párrafo, sin decisiones de implementación.
2. Requirements: una capacidad coherente por Requirement N, con User Story y Acceptance Criteria.
3. Non-Functional Requirements: solo los aplicables, medibles y con IDs NFR-N.
4. Out of Scope: exclusiones explícitas; si no hay, indicarlo.
5. Glossary: términos del dominio que puedan interpretarse de varias maneras.
6. Open Questions: decisiones pendientes; no ocultarlas como requisitos cerrados.

Usar la plantilla incluida. Las historias siguen «Como [rol], quiero [capacidad], para [propósito]». Los criterios siguen la referencia EARS incluida en este paquete. Conservar IDs al editar; no renumerar criterios aprobados sin un mapa de equivalencias.

## Síntesis de material
- Inventariar fuentes y registrar cuáles se leyeron, cuáles no son accesibles y por qué.
- Resumir interpretación inicial y confirmar actores y alcance cuando el material admita varias lecturas.
- Preguntar por reglas, permisos, límites, condiciones de error y resultados observables que no estén definidos. No fabricar umbrales de rendimiento o políticas del negocio.
- Evitar duplicados y requisitos solapados. No convertir decisiones de interfaz observadas en capturas en políticas de autorización sin corroboración.
- Validar incrementalmente el contenido nuevo con el usuario, dejando los pendientes visibles.

## Reingeniería
Contrastar documentación y código, sin asumir que uno describe intención aprobada. Por cada criterio derivado del código, anotar fuente y confianza:

```markdown
1. WHEN a valid request is submitted THE SYSTEM SHALL calculate the amount using the configured rate table.
   <!-- confidence: medium; source: src/calculator.py:20-35 -->
```

La fuente del ejemplo debe sustituirse por evidencia real. Usar confianza alta con corroboración, media con implementación clara sin corroboración y baja para inferencias. Preguntar si una anomalía debe preservarse o corregirse. Mantener secciones Detected Anomalies y Coverage Map cuando ayuden a distinguir alcance observado de alcance pendiente. Un hallazgo de baja confianza no se transforma en política aprobada por repetirlo en un documento.

## Actualización por feedback
Conservar el documento y IDs existentes. Identificar cambios de actores, entidades, flujos, integración o restricciones. Redactar solo el delta acordado, registrar fuentes y dejar explícito qué decisiones downstream requieren nueva revisión. La aprobación anterior no cubre automáticamente el alcance nuevo.

## Checklist
- [ ] Problema, actores, capacidades y propósito de cada historia definidos.
- [ ] Criterios atómicos, comprobables, con errores y casos borde acordados.
- [ ] IDs funcionales y NFR estables y utilizables en trazabilidad.
- [ ] EARS conforme a la referencia, sin decisiones de framework/base de datos.
- [ ] Exclusiones y términos ambiguos resueltos o registrados.
- [ ] Fuentes reales, cobertura declarada e inferencias diferenciadas.
- [ ] En reingeniería, anomalías e intención por confirmar separadas.
- [ ] Estado del borrador y aprobación humana correctamente registrados.

Si falta información, entregar un borrador BLOQUEADO con preguntas concretas. No declarar completitud ni continuar a diseño sin la aprobación exigida.
