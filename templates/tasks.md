<!--
TEMPLATE: tasks.md
Framework: SDD (Spec-Driven Development)

Reglas absolutas:
- Cada tarea: checkbox + número + verbo concreto + sub-pasos + criterio de hecho + footer
- Una tarea = una sesión de agente (1-3 archivos, 50-200 líneas)
- Orden por dependencias técnicas, NO por valor de negocio
- Tests SIEMPRE como tareas independientes, NUNCA como sub-pasos
- Footer obligatorio: _Requirements: X.Y, ..._  (puede ser `-` para setup)
- Cada criterio EARS del requirements.md debe estar referenciado en al menos una tarea

Antes de cerrar este archivo, ejecutar el checklist de auto-validación
definido en .claude/skills/sdd-tasks/SKILL.md

Anatomía de tarea:
- [ ] N. [Verbo] [objeto concreto]
  - [Sub-paso 1: archivos a tocar / patrón a aplicar]
  - [Sub-paso 2]
  - Criterio de hecho: [cómo se sabe que terminó]
  - _Requirements: X.Y, X.Z_

Verbos permitidos: Implementar, Crear, Modificar, Agregar, Refactorizar,
                   Configurar, Validar, Documentar
-->

# Tasks: [Nombre del feature o sistema]

## Setup

- [ ] 1. Configurar estructura inicial del proyecto
  - Crear estructura de carpetas: `src/{ui,api,services,repositories,db}`
  - Inicializar dependencias del package manager
  - Configurar linter, formatter, y tsconfig (si aplica)
  - Criterio de hecho: `npm install` corre limpio, linter pasa en proyecto vacío
  - _Requirements: -_

- [ ] 2. Configurar entorno de testing
  - Instalar framework de tests (vitest/jest/playwright según design §8)
  - Configurar coverage y CI mínimo
  - Criterio de hecho: `npm test` corre con un test trivial pasando
  - _Requirements: -_

## Data Model

- [ ] 3. Crear schema y migración de tabla [nombre]
  - Definir entidad según design §3
  - Generar migración con índices declarados
  - Aplicar migración localmente
  - Criterio de hecho: tabla existe, índices verificables con `\d` o equivalente
  - _Requirements: [X.Y]_

<!-- Repetir tarea por cada entidad del design §3 -->

## Data Access Layer

- [ ] N. Implementar repositorio [NombreRepository]
  - Crear archivo `src/repositories/[nombre]Repository.ts`
  - Implementar métodos según contratos del design §4
  - Aislar queries: ningún SQL fuera de este archivo
  - Criterio de hecho: métodos compilan, types pasan
  - _Requirements: [X.Y, X.Z]_

- [ ] N+1. Tests de integración para [NombreRepository]
  - Caso éxito: insert + read recupera el dato correctamente
  - Caso error: constraint violation retorna error tipado
  - Caso borde: query sobre tabla vacía
  - Criterio de hecho: todos los tests del archivo pasan
  - _Requirements: [X.Y, X.Z]_

## Business Logic

- [ ] N. Implementar servicio [NombreService]
  - Crear archivo `src/services/[nombre]Service.ts`
  - Implementar casos de uso según design §2 y §4
  - Validar reglas de negocio antes de delegar al repository
  - Criterio de hecho: lógica pura, no toca BD directo
  - _Requirements: [X.Y]_

- [ ] N+1. Tests unitarios para [NombreService]
  - Mockear repositorios
  - Cubrir camino feliz y casos error EARS del requirements
  - Criterio de hecho: coverage > 80% del archivo
  - _Requirements: [X.Y]_

## API / Interface

- [ ] N. Implementar endpoint/handler [nombre]
  - Crear archivo `src/api/[nombre].ts`
  - Validar payload de entrada con schema
  - Invocar servicio correspondiente
  - Mapear errores del servicio a códigos tipados del design §4
  - Criterio de hecho: endpoint compila, contratos coinciden con design §4
  - _Requirements: [X.Y]_

- [ ] N+1. Tests de integración para endpoint [nombre]
  - Caso éxito: payload válido → respuesta esperada
  - Caso error: cada tipo de error EARS retorna código correcto
  - Caso borde: payload mal formado / faltante
  - Criterio de hecho: todos los tests pasan
  - _Requirements: [X.Y, X.Z]_

## UI / Client

- [ ] N. Implementar pantalla/componente [nombre]
  - Crear componente según wireframes o descripción del requirements
  - Validar input en cliente (espejo de validación servidor)
  - Invocar API correspondiente
  - Manejar estados: loading, success, error tipados
  - Criterio de hecho: componente renderiza, integra con API mockeada
  - _Requirements: [X.Y]_

## Integration Tests (E2E)

- [ ] N. Tests E2E del flujo "[nombre del flujo crítico]"
  - Cubrir el flujo completo según design §6
  - Camino feliz: usuario completa la operación de inicio a fin
  - Camino error: al menos un caso de error del requirements
  - Criterio de hecho: tests E2E pasan en CI
  - _Requirements: [X.Y, X.Z, X.W]_

## Documentation

- [ ] N. Documentar uso del feature
  - Actualizar README con sección del nuevo feature
  - Documentar endpoints públicos (si aplica)
  - Agregar ejemplos de uso
  - Criterio de hecho: lector externo entiende qué hace el feature y cómo usarlo
  - _Requirements: -_

<!--
Patrones opcionales:

Spike (cuando hay incertidumbre técnica):
- [ ] N. Spike: investigar [pregunta concreta]
  - Pregunta a responder: [una línea]
  - Output esperado: mini-ADR agregado a design.md
  - Timebox: [horas máximo]
  - _Requirements: -_

Refactor preventivo:
- [ ] N. Refactor preventivo: limpiar [módulo X] antes de tarea N+M
  - Extraer [Y] a su propio módulo
  - Sin cambio de comportamiento (tests existentes siguen pasando)
  - _Requirements: -_

Validación intermedia:
- [ ] N. Validar integración tareas 1-N
  - Correr suite completa de tests hasta este punto
  - Verificar criterios EARS [X.Y, ...] manualmente con caso de uso real
  - _Requirements: [X.Y, X.Z]_

Tarea opcional (para MVP):
- [ ] N. (opcional) [Verbo] [acción]
  - ...
  - _Requirements: [no funcional]_

Tareas paralelizables (mismo número base, sufijo letra):
- [ ] 7a. Implementar [cosa A]
- [ ] 7b. Implementar [cosa B]
-->
