# Requisitos EARS y evidencia

## Contenido
- Patrones
- Calidad y trazabilidad
- Ejemplo
- Revisión

## Patrones
Usar criterios en inglés con SHALL y respuestas observables. Mantener los IDs existentes.

| Patrón | Sintaxis |
|---|---|
| Ubicuo | THE SYSTEM SHALL response. |
| Evento | WHEN trigger THE SYSTEM SHALL response. |
| Estado | WHILE state THE SYSTEM SHALL response. |
| Capacidad opcional | WHERE feature is present THE SYSTEM SHALL response. |
| Condición indeseada | IF condition THEN THE SYSTEM SHALL response. |
| Combinado | WHILE state, WHEN trigger THE SYSTEM SHALL response. |

## Calidad y trazabilidad
- Una historia expresa rol, capacidad y propósito: `Como X, quiero Y, para Z`.
- Un criterio contiene un comportamiento comprobable. Separar calcular, mostrar y persistir.
- No usar adjetivos vagos ni inventar umbrales: preguntar cantidades, unidades y condiciones de medición.
- Identificar errores cuando el contrato lo requiera; no elegir frameworks o bases de datos en requisitos.
- Referenciar criterios funcionales como `1.1`, `1.2`; identificar NFR como `NFR-1`, `NFR-2`.
- En código heredado citar `<!-- confidence: high|medium|low; source: archivo:líneas -->` y distinguir observación de decisión de conservarla.
- Mover incertidumbres que bloquean a Open Questions. Un borrador con preguntas no es una especificación aprobada.

## Ejemplo
**User Story:** Como analista, quiero consultar el resultado de un cálculo, para revisar el importe antes de confirmarlo.

1. WHEN the user submits valid inputs THE SYSTEM SHALL calculate the amount using the approved rate table.
2. WHEN the calculation completes THE SYSTEM SHALL display the calculated amount.
3. IF a required input is missing THEN THE SYSTEM SHALL reject the calculation request with FIELD_REQUIRED.

La tabla de tasas y los campos obligatorios deben estar definidos en las entradas; este ejemplo no los inventa.

## Revisión
- Historias con propósito, criterios atómicos y comprobables.
- Alcance excluido explícito, errores y casos borde acordados.
- Evidencia rastreable y dudas visibles, sin completar huecos por intuición.
- IDs conservados, NFR identificables y aprobación humana separada de revisión propia.
