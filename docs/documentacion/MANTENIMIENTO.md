# Pipeline de Mantenimiento — Decisiones de Diseño

> ADR que congela las decisiones del pipeline de mantenimiento del framework SDD (agregar features a sistemas en producción sin romper lo que ya funciona). Esta es la fuente de verdad sobre el **porqué** de los agentes `analista-feature-mantenimiento`, `disenador-delta-mantenimiento`, `descompositor-riesgo-mantenimiento` y sus skills correspondientes. Si los artefactos divergen de este doc, este doc manda hasta que se actualice.

---

## Índice

1. [Propósito](#1-propósito)
2. [Posición en el ecosistema de pipelines del framework](#2-posición-en-el-ecosistema-de-pipelines-del-framework)
3. [Cuándo aplicar este pipeline (árbol de decisión)](#3-cuándo-aplicar-este-pipeline-árbol-de-decisión)
4. [Decisiones congeladas](#4-decisiones-congeladas)
5. [Estructura del artefacto `docs/features/<feature>/`](#5-estructura-del-artefacto-docsfeaturesfeature)
6. [El sustrato: CLAUDE.md, BIG_PICTURE.md, REGLAS_DE_NEGOCIO.md](#6-el-sustrato-claudemd-big_picturemd-reglas_de_negociomd)
7. [Las tres garantías de no-regresión](#7-las-tres-garantías-de-no-regresión)
8. [Comparación con los otros pipelines](#8-comparación-con-los-otros-pipelines)
9. [Anti-patrones](#9-anti-patrones)

---

## 1. Propósito

`analista-entrevistas` y `arqueologo-codigo` cubren proyectos donde se **construye o se reconstruye** un sistema. El framework asumía que SDD entra al inicio del ciclo de vida.

Pero la realidad de la mayoría de los proyectos en producción es **mantenimiento**: agregar features a un sistema que ya funciona, sin romperlo. Eso es un escenario distinto:

- La arquitectura está dada — no se diseña, se respeta.
- El stack está dado — no se elige, se hereda.
- Hay reglas de negocio implementadas que no pueden romperse — son **invariantes**, no requisitos a redocumentar.
- El cambio es **un delta**, no un sistema completo — los artefactos deben acotarse a eso.

Este pipeline introduce **tres agentes nuevos + tres skills nuevos** que viven dentro del mismo framework SDD pero operan bajo reglas adaptadas. El resultado: un feature agregado con la misma disciplina formal que SDD aplica a greenfield, pero **sin sobrediseñar** y **sin tocar lo que ya funciona**.

**Lo que el pipeline NO es:**

- No es una alternativa a `arqueologo-codigo` para reescritura — sigue habiendo brownfield-rewrite cuando el plan es rehacer el sistema.
- No es un atajo "metan el feature como puedan" — mantiene rigor de specs, EARS y gates humanos.
- No es excusa para ignorar el sistema existente — exige documentarlo antes (skills `onboarding` y `reglas-negocio`).

**Lo que el pipeline SÍ es:**

- Disciplina SDD acotada al delta del feature.
- Documentación explícita de la **superficie de contacto** con el código existente.
- Documentación explícita de las **invariantes preservadas** del sistema.
- Tasks ordenadas por riesgo de regresión, con blindaje (tests de regresión) ANTES de tocar código.
- Gate final de no-regresión obligatorio antes de cerrar.

---

## 2. Posición en el ecosistema de pipelines del framework

El framework SDD tiene **tres pipelines paralelos**, todos viven en el mismo template y comparten skills agnósticas (formato EARS) pero tienen agentes y artefactos propios:

```
                              ┌─────────────────┐
                              │   Template SDD  │
                              │  (un solo repo) │
                              └────────┬────────┘
                                       │
              ┌────────────────────────┼────────────────────────┐
              ▼                        ▼                        ▼
    ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
    │  GREENFIELD      │     │ BROWNFIELD-      │     │  MANTENIMIENTO   │
    │                  │     │ REWRITE          │     │                  │
    │ analista-        │     │ arqueologo-      │     │ analista-feature │
    │ entrevistas      │     │ codigo           │     │ -mantenimiento   │
    │       ↓          │     │       ↓          │     │       ↓          │
    │ requirements.md  │     │ requirements.md  │     │ requirements.md  │
    │ (sistema nuevo)  │     │ (sistema reescr) │     │ (delta feature)  │
    │       ↓          │     │       ↓          │     │       ↓          │
    │ (prototipo       │     │ (prototipo       │     │ (prototipo       │
    │  opcional)       │     │  opcional)       │     │  opcional —      │
    │       ↓          │     │       ↓          │     │  ver §4.D6)      │
    │ disenador-       │     │ disenador-       │     │       ↓          │
    │ arquitecto       │     │ arquitecto       │     │ disenador-delta- │
    │       ↓          │     │       ↓          │     │ mantenimiento    │
    │ design.md        │     │ design.md        │     │       ↓          │
    │ (full)           │     │ (full)           │     │ design.md (delta)│
    │       ↓          │     │       ↓          │     │       ↓          │
    │ descompositor-   │     │ descompositor-   │     │ descompositor-   │
    │ tareas           │     │ tareas           │     │ riesgo-          │
    │       ↓          │     │       ↓          │     │ mantenimiento    │
    │ tasks.md         │     │ tasks.md         │     │       ↓          │
    │ (capas)          │     │ (capas)          │     │ tasks.md (riesgo)│
    └──────────────────┘     └──────────────────┘     └──────────────────┘
              │                        │                        │
              └────────────────────────┼────────────────────────┘
                                       ▼
                         [tarea por sesión + código]
```

**El template es el mismo.** Cuando clonas el framework, traes los **8 agentes y 7 skills**. El pipeline correcto se identifica por:

1. Convención de carpetas distintas: `docs/inputs/` (greenfield), `docs/analysis/` (rewrite), `docs/features/<X>/` (mantenimiento).
2. Naming convention: agentes de mantenimiento llevan sufijo `-mantenimiento`.
3. Árbol de decisión en `Como_se_usan.md` § Fase 0.

**Los porteros estrictos en cada agente** son lo que evita confusión cruzada: si invocas el agente equivocado en el repo equivocado, no encuentra sus pre-condiciones y se detiene avisando.

---

## 3. Cuándo aplicar este pipeline (árbol de decisión)

```
                    ¿Tienes un sistema en
                       producción HOY?
                              │
                ┌─────────────┴─────────────┐
                │                           │
              NO ── tienes solo idea       SÍ
                    o legacy roto           │
                    sin querer mantener     │
                            ↓               │
                  GREENFIELD                │
                  (analista-entrevistas)    │
                            ┐               │
                                            │
                              ¿Lo vas a reescribir
                              completo / modernizar
                                arquitectura?
                                            │
                              ┌─────────────┴─────────────┐
                              │                           │
                            SÍ                          NO
                              │                           │
                              ↓                           ↓
                  BROWNFIELD-REWRITE                MANTENIMIENTO
                  (arqueologo-codigo)              (este pipeline)
                                                    │
                                                    ↓
                                            ¿Cuántos features
                                              vas a agregar?
                                                    │
                                            ┌───────┴───────┐
                                          UNO              VARIOS
                                            │                 │
                                            ↓                 ↓
                                    1 feature/        Una carpeta
                                    docs/features/    docs/features/
                                                      por feature
```

Reglas de oro para no equivocarse:

- **El sistema funciona en producción + agregas algo nuevo sin romper = mantenimiento.**
- **El sistema funciona pero vas a rehacer arquitectura = brownfield-rewrite.**
- **No hay sistema o está siendo descartado completo = greenfield.**

Si dudas: lee `Como_se_usan.md` §1.

---

## 4. Decisiones congeladas

Cada decisión en formato breve: **Decisión · Por qué · Consecuencias negativas aceptadas**.

### D1. Pipeline hermano, no extensión de los existentes

- **Decisión**: el pipeline de mantenimiento vive como tercer flujo paralelo a greenfield y brownfield-rewrite, con agentes y skills propios.
- **Por qué**: hacer "mode-aware" los agentes existentes (analista, arqueologo, disenador, descompositor) introduce ramas condicionales que multiplican modos de falla. Los agentes lineales son más robustos.
- **Consecuencia aceptada**: duplicación controlada de algunos conceptos (ej. tabla de Traceability aparece en sdd-design y en sdd-design-delta con reglas distintas). La duplicación entre dos cosas estables es más barata que el acoplamiento entre dos cosas que cambian.

### D2. Tres agentes nuevos, no uno solo

- **Decisión**: el pipeline de mantenimiento usa tres agentes (`analista-feature-mantenimiento`, `disenador-delta-mantenimiento`, `descompositor-riesgo-mantenimiento`), uno por artefacto.
- **Por qué**: el patrón "un agente = un artefacto" es lo que da robustez al framework. Cada agente es portero estricto de un solo output.
- **Consecuencia aceptada**: el humano invoca tres veces en lugar de una. Vale la pena por los gates intermedios.

### D3. Artefactos en `docs/features/<feature>/`, no en `docs/` raíz

- **Decisión**: los artefactos del feature viven en `docs/features/<slug-del-feature>/{intent,requirements,design,tasks}.md`.
- **Por qué**: un sistema en producción tendrá múltiples features a lo largo del tiempo. Aplastar todo en `docs/requirements.md` raíz pierde historial; una carpeta por feature lo preserva.
- **Consecuencia aceptada**: los paths son más largos. La estructura del repo crece. Trade-off aceptable.

### D4. Surface of Contact + Invariantes Preservadas son obligatorias

- **Decisión**: el `requirements.md` de mantenimiento debe tener ambas secciones, no son opcionales.
- **Por qué**: omitirlas elimina la base para no-regresión. La probabilidad de romper algo en producción sin documentar contactos e invariantes es ~100%.
- **Consecuencia aceptada**: el requirements.md de mantenimiento es más largo que uno greenfield del mismo tamaño de feature.

### D5. Tasks ordenadas por riesgo, no por capa

- **Decisión**: la estructura del `tasks.md` de mantenimiento empieza con `## Regression Shield` y termina con `## No-Regression Validation`, no con `## Setup` ni `## Documentation`.
- **Por qué**: en mantenimiento no hay Setup (el sistema ya está montado). Y la garantía de no romper viene de tests de regresión PRIMERO, no de validación al final.
- **Consecuencia aceptada**: el humano aprende dos estructuras de tasks.md distintas (sdd-tasks vs sdd-tasks-risk). El sufijo en los nombres y la documentación lo hacen explícito.

### D6. Fase de prototipo es opcional pero compatible con mantenimiento

- **Decisión**: `prototipador-visual` PUEDE usarse en el pipeline de mantenimiento si el feature introduce UI nueva que el cliente quiere validar antes.
- **Por qué**: la fase opcional de prototipo es transversal al framework — su input es un `requirements.md` aprobado, sea del pipeline que sea.
- **Consecuencia aceptada**: para features de mantenimiento sin UI o triviales, conviene saltarla. El humano decide. El skill `sdd-prototype` no requiere cambios.
- **Path**: si se usa, el prototipo vive en `docs/features/<feature>/prototype/`, no en `docs/prototype/` raíz (lo mantiene scoped al feature).

### D7. Sustrato recomendado pero no obligatorio

- **Decisión**: los agentes leen `docs/CLAUDE.md`, `docs/BIG_PICTURE.md`, `docs/REGLAS_DE_NEGOCIO.md` si existen, pero pueden continuar sin ellos.
- **Por qué**: forzar el sustrato bloquearía a equipos que descubren SDD a mitad de un proyecto en producción.
- **Consecuencia aceptada**: sin sustrato, la calidad del análisis depende más de cuánto código el agente lee directamente. Se documenta el riesgo en Open Questions.

### D8. Trazabilidad doble en tasks: EARS + Invariantes

- **Decisión**: cada tarea del `tasks.md` de mantenimiento lleva footer `_Requirements: X.Y_ | _Invariants: I.A_`.
- **Por qué**: las invariantes son tan importantes como los EARS — necesitan trazabilidad propia para que el humano pueda auditar el blindaje y la no-regresión.
- **Consecuencia aceptada**: el footer es más largo. Compensa con auditabilidad.

### D9. Verbo `Blindar` y verbo `Verificar regresión` exclusivos de mantenimiento

- **Decisión**: el skill `sdd-tasks-risk` introduce dos verbos nuevos: `Blindar` (escribir test de regresión sobre código existente) y `Verificar regresión` (correr suite completa + verificar invariantes).
- **Por qué**: estos verbos no aparecen en construcción (donde no hay invariantes preexistentes). Tenerlos explícitos refuerza la disciplina del pipeline.
- **Consecuencia aceptada**: el listado de verbos permitidos es más largo en mantenimiento. Documentado en el skill.

### D10. Tasks de integración son aisladas, una por punto de coexistencia

- **Decisión**: cada fila de Surface of Contact con riesgo medio/alto genera **una tarea aislada** en la sección `## Integration` del tasks.md.
- **Por qué**: cuando integras un feature con un flujo existente, el riesgo es local. Agrupar varios puntos en una tarea grande mezcla riesgos y vuelve la revisión más difícil.
- **Consecuencia aceptada**: el tasks.md tiene más tareas. Cada una es chica y revisable.

---

## 5. Estructura del artefacto `docs/features/<feature>/`

```
docs/features/<slug-del-feature>/
├── intent.md                 ← INPUT humano (descripción del feature)
├── requirements.md           ← OUTPUT analista-feature-mantenimiento
├── design.md                 ← OUTPUT disenador-delta-mantenimiento
├── tasks.md                  ← OUTPUT descompositor-riesgo-mantenimiento
└── (prototype/)              ← OUTPUT opcional prototipador-visual si UI relevante
```

**Slug**: kebab-case, descriptivo, sin caracteres especiales. Ej: `exportar-reportes-pdf`, `notificaciones-push`, `auth-mfa`.

**Un feature = una carpeta = un ciclo SDD acotado.** Si el feature es demasiado grande (más de ~25-30 tareas), se parte en sub-features cada uno con su carpeta.

---

## 6. El sustrato: CLAUDE.md, BIG_PICTURE.md, REGLAS_DE_NEGOCIO.md

Estos tres archivos viven en `docs/` raíz (no dentro de `features/`) porque aplican al sistema completo:

- **`docs/CLAUDE.md`** — guía del repo. Generada por la skill `onboarding` (incluida en `.claude/skills/onboarding/`). Contiene: cómo se levanta el ambiente, comandos de build/test, convenciones de naming, estructura de carpetas, dependencias clave. El agente de mantenimiento la usa para saber cómo correr los tests existentes.
- **`docs/BIG_PICTURE.md`** — radiografía arquitectónica. Generada también por `onboarding`. Contiene: capas, módulos, flujo de datos, integraciones externas, patrones usados. El agente de mantenimiento la usa para saber qué arquitectura es "lo heredado e inmutable".
- **`docs/REGLAS_DE_NEGOCIO.md`** — reglas de negocio explícitas. Generada por la skill `reglas-negocio` (incluida en `.claude/skills/reglas-negocio/`). Contiene: roles, permisos, flujos de estados, validaciones, mapa funcional. El agente de mantenimiento la usa para identificar invariantes con seguridad.

Si no existen, el agente puede continuar pero recomienda al humano correrlas primero. La calidad del análisis mejora ~10x con el sustrato.

**Estas dos skills SÍ son del framework SDD** (`.claude/skills/onboarding/` y `.claude/skills/reglas-negocio/`), no son externas. Son skills auxiliares del pipeline de mantenimiento: agnósticas al pipeline SDD per se (sirven para analizar cualquier repo), pero el pipeline de mantenimiento las usa como sustrato. Por eso van empaquetadas con el framework — para que cualquiera que clone el template las tenga listas sin instalación extra.

---

## 7. Las tres garantías de no-regresión

El pipeline está construido sobre tres garantías que se refuerzan mutuamente:

### Garantía 1: Fases 1-3 son read-only sobre el código de producción

`analista-feature-mantenimiento` y `disenador-delta-mantenimiento` solo leen código. Sus outputs son `.md`. Es **matemáticamente imposible romper producción durante análisis y diseño**.

### Garantía 2: Tests de blindaje ANTES de modificar código

La sección `## Regression Shield` del tasks.md ejecuta primero. Si una invariante no tiene test, se crea **antes** de tocar el módulo. La modificación posterior se valida contra ese blindaje.

### Garantía 3: Gate final de No-Regression Validation

La última tarea del tasks.md es obligatoria: correr toda la suite + verificar cada invariante manualmente. Si una invariante se rompió, el feature **no se cierra** hasta que se resuelva.

**Estas tres garantías combinadas hacen que el pipeline de mantenimiento sea genuinamente más seguro que codear el feature a mano**, no menos.

---

## 8. Comparación con los otros pipelines

| Aspecto | Greenfield | Brownfield-Rewrite | Mantenimiento |
|---|---|---|---|
| Premisa | Construir desde cero | Reescribir legacy | Agregar feature sin romper |
| Input | Entrevistas, transcripciones | Análisis arqueológico + código legacy | Intent del feature + código en prod |
| Stack | Se decide en design | Se decide en design | **Heredado** del sistema existente |
| Arquitectura | Se diseña | Se diseña | **Heredada** — solo se diseña el delta |
| Scope del `requirements.md` | Sistema completo | Sistema completo (reescrito) | **Solo el delta** |
| Surface of Contact | N/A | N/A | **Obligatoria** |
| Invariantes Preservadas | N/A | N/A (sí "Anomalies") | **Obligatorias** |
| Orden de tasks | Por capa arquitectónica | Por capa arquitectónica | **Por riesgo de regresión** |
| Tests de regresión | N/A | N/A | **Tareas de blindaje obligatorias** |
| Validación final | Tests del feature | Tests del sistema reescrito | **Tests del feature + verificación de invariantes** |
| Tamaño típico del design.md | 300-800 líneas | 300-800 líneas | **200-600 líneas** (es solo delta) |
| Agentes | analista-entrevistas → disenador-arquitecto → descompositor-tareas | arqueologo-codigo → disenador-arquitecto → descompositor-tareas | **analista-feature-mantenimiento → disenador-delta-mantenimiento → descompositor-riesgo-mantenimiento** |
| Skills | sdd-requirements, sdd-design, sdd-tasks (+ sdd-prototype opcional) | mismas | **sdd-requirements-mantenimiento, sdd-design-delta, sdd-tasks-risk** (+ sdd-prototype opcional) |

---

## 9. Anti-patrones

### Conceptuales

- ❌ Usar este pipeline para reescribir partes del sistema "porque ya estamos aquí". Si el plan es reescritura, usar `arqueologo-codigo`. Mezclar pipelines rompe la disciplina del framework.
- ❌ Saltarse el sustrato (`onboarding` / `reglas-negocio`) porque "yo conozco el sistema". El conocimiento humano no se versiona; los archivos sí. Sin sustrato, futuros features pierden contexto.
- ❌ Tratar las invariantes como "deseo": "el sistema no se rompe". Una invariante es testeable, sin excepción.
- ❌ Permitir que el design.md proponga cambios fuera de Surface of Contact. Si lo hace, el alcance se rompió silenciosamente.
- ❌ Saltarse Regression Shield "porque tenemos prisa". Garantiza descubrir regresiones en producción.
- ❌ Saltarse No-Regression Validation "porque se ve bien". El gate final es no negociable.

### Operativos

- ❌ Modificar código existente sin escribir antes el test de blindaje.
- ❌ Marcar tarea de modificación como `[x]` sin haber corrido los tests del módulo modificado.
- ❌ Tareas de integración agrupadas (varias coexistencias en una tarea).
- ❌ Trazabilidad doble con ambos `-` en el footer (`_Requirements: -_ | _Invariants: -_`) — al menos uno debe tener referencia.
- ❌ Verbos vagos en tasks ("Trabajar en X", "Hacer Y"). Sigue siendo prohibido como en sdd-tasks.

### De gobernanza

- ❌ "Ejecuta todo `tasks.md`". Rompe garantizado, igual que en greenfield. Una tarea = una sesión = una revisión.
- ❌ Aprobar requirements sin haber leído Surface of Contact e Invariantes Preservadas. Esas dos secciones son **el contrato** del feature.
- ❌ Aprobar design sin verificar que no rediseña arquitectura. La auto-validación del agente puede equivocarse — la revisión humana es la última línea.

---

## Cierre

Este pipeline cierra el hueco más grande que tenía el framework SDD: aplicar la disciplina de specs-primero a **mantenimiento de sistemas en producción**, no solo a construcción.

La filosofía: **lo que no se documenta como invariante, no se garantiza**. Si quieres no romper algo, anótalo, refencia el código, blíndalo con test. Lo demás es esperanza.

Para uso operativo paso a paso, ver [`Como_se_usan.md`](Como_se_usan.md) §5C (mantenimiento).
Para fundamentos generales del framework, ver [`SDD.md`](SDD.md).
