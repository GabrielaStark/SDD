# SDD Framework — Guía Completa

> Cómo usar este framework, qué es SDD, qué hace cada pieza, y cómo no pegarte un tiro en el pie en el intento.

---

## Índice

1. [Qué es SDD y por qué nos importa](#1-qué-es-sdd-y-por-qué-nos-importa)
2. [Anatomía del framework](#2-anatomía-del-framework)
3. [El pipeline completo](#3-el-pipeline-completo)
4. [Cómo usar este framework, paso a paso](#4-cómo-usar-este-framework-paso-a-paso)
5. [Los componentes uno por uno](#5-los-componentes-uno-por-uno)
6. [Anti-patrones que no debes cometer](#6-anti-patrones-que-no-debes-cometer)
7. [FAQ](#7-faq)

---

## 1. Qué es SDD y por qué nos importa

**SDD** (Spec-Driven Development, Desarrollo Dirigido por Especificaciones) es una práctica que apareció con fuerza en 2025 con GitHub Spec Kit y AWS Kiro. La idea central es simple:

> En vez de pedirle código a un agente IA y descubrir qué construyó después, **escribes especificaciones formales primero** y el agente genera código a partir de ellas. Las specs son el artefacto primario, versionado en el repo, y el código es consecuencia.

### El problema que resuelve

El **vibe-coding** (pedirle cosas a la IA conversacionalmente sin estructura) funciona para prototipos pero produce código frágil, inconsistente y con vulnerabilidades. SDD recupera disciplina de ingeniería sin perder velocidad.

### Por qué un framework propio en vez de Spec Kit o Kiro directo

Spec Kit y Kiro son excelentes pero:

- Son herramientas opinadas con su propio flujo
- No están adaptadas al español ni al contexto latinoamericano
- No incluyen el patrón **brownfield** (arqueología de legacy) que necesitamos para muchos clientes
- No incluyen el patrón **mantenimiento** (agregar features a sistemas en producción) que es el caso más común en el día a día
- No tienen integración nativa con nuestro stack (Claude Code, MCPs propios)

Este framework toma la metodología y la adapta a cómo trabajamos.

### Madurez

SDD está en fase **"Assess"** del Tech Radar de Thoughtworks (no "Adopt" todavía). Es práctica emergente bien fundamentada que probablemente sea estándar en 2027. Estamos temprano, no tarde.

---

## 2. Anatomía del framework

### Estructura del repo template

```
SDD/
├── README.md                                       ← punto de entrada del repo
├── .claude/
│   ├── agents/                                     ← subagentes especializados (8 en total)
│   │   ├── analista-entrevistas.md                ← greenfield: transcripción → requirements
│   │   ├── arqueologo-codigo.md                    ← brownfield-rewrite: legacy → requirements
│   │   ├── prototipador-visual.md                  ← (opcional) requirements → mockup desplegado
│   │   ├── disenador-arquitecto.md                 ← greenfield+rewrite: requirements → design
│   │   ├── descompositor-tareas.md                 ← greenfield+rewrite: design → tasks
│   │   ├── analista-feature-mantenimiento.md       ← mantenimiento: intent + código prod → requirements (delta)
│   │   ├── disenador-delta-mantenimiento.md        ← mantenimiento: requirements (delta) → design (delta)
│   │   └── descompositor-riesgo-mantenimiento.md   ← mantenimiento: design (delta) → tasks (por riesgo)
│   └── skills/                                     ← constituciones compartidas (9 en total)
│       ├── sdd-requirements/SKILL.md               ← reglas del requirements.md (construcción)
│       ├── sdd-prototype/SKILL.md                  ← reglas del docs/prototype/ (fase opcional)
│       ├── sdd-design/SKILL.md                     ← reglas del design.md (construcción)
│       ├── sdd-tasks/SKILL.md                      ← reglas del tasks.md (construcción)
│       ├── sdd-requirements-mantenimiento/SKILL.md ← reglas del requirements.md (mantenimiento)
│       ├── sdd-design-delta/SKILL.md               ← reglas del design.md (mantenimiento)
│       ├── sdd-tasks-risk/SKILL.md                 ← reglas del tasks.md (mantenimiento)
│       ├── onboarding/SKILL.md                     ← auxiliar: genera CLAUDE.md + BIG_PICTURE.md
│       └── reglas-negocio/SKILL.md                 ← auxiliar: genera REGLAS_DE_NEGOCIO.md
├── docs/
│   ├── inputs/                                     ← material crudo (greenfield)
│   ├── analysis/                                   ← análisis arqueológico previo (brownfield-rewrite)
│   ├── features/                                   ← features de mantenimiento (uno por subcarpeta)
│   │   └── <slug>/{intent,requirements,design,tasks}.md
│   ├── CLAUDE.md                                   ← (opcional) guía del repo — generada por skill `onboarding`
│   ├── BIG_PICTURE.md                              ← (opcional) radiografía arquitectónica — generada por `onboarding`
│   ├── REGLAS_DE_NEGOCIO.md                        ← (opcional) reglas de negocio — generada por `reglas-negocio`
│   ├── requirements.md                             ← OUTPUT pipeline construcción (greenfield/rewrite)
│   ├── prototype/                                  ← OUTPUT prototipo (construcción)
│   ├── design.md                                   ← OUTPUT pipeline construcción
│   ├── tasks.md                                    ← OUTPUT pipeline construcción
│   └── documentacion/
│       ├── SDD.md                                  ← este archivo
│       ├── PROTOTIPO.md                            ← decisiones de la fase opcional de prototipo
│       ├── MANTENIMIENTO.md                        ← decisiones del pipeline de mantenimiento
│       └── Como_se_usan.md                         ← manual paso a paso
└── templates/                                      ← templates con guía inline
    ├── requirements.md                             ← construcción
    ├── design.md                                   ← construcción
    ├── tasks.md                                    ← construcción
    ├── intent.md                                   ← mantenimiento (input humano)
    ├── requirements-mantenimiento.md               ← mantenimiento
    ├── design-delta.md                             ← mantenimiento
    └── tasks-riesgo.md                             ← mantenimiento
```

### Tres conceptos clave

**Subagente**: una instancia de Claude con un system prompt propio, herramientas propias, identidad propia. Cada uno hace UN trabajo bien definido.

**Skill**: un archivo `SKILL.md` con conocimiento procedural reutilizable (reglas, plantillas, validaciones). Los subagentes lo consultan automáticamente cuando lo declaran en su frontmatter.

**Template**: archivo de partida con estructura canónica y guía inline. Útil cuando alguien quiere escribir un documento a mano sin invocar al agente.

---

## 3. Los tres pipelines del framework

El framework SDD tiene **tres pipelines paralelos**. Eliges uno según el escenario:

```
                    ┌─────────────────────────────────┐
                    │   ¿Cuál es tu escenario?         │
                    └────────────────┬────────────────┘
                                     │
       ┌─────────────────────────────┼─────────────────────────────┐
       ▼                             ▼                             ▼
┌────────────┐              ┌────────────────┐            ┌──────────────────┐
│ GREENFIELD │              │ BROWNFIELD     │            │ MANTENIMIENTO    │
│            │              │ REWRITE        │            │                  │
│ Sistema    │              │ Legacy a       │            │ Sistema en prod, │
│ desde cero │              │ reescribir     │            │ agregar feature  │
└──────┬─────┘              └────────┬───────┘            └────────┬─────────┘
       │                             │                             │
       ▼                             ▼                             ▼
  docs/inputs/                docs/analysis/                docs/features/<X>/
  (transcripciones,           (arqueología                 (intent.md
   formularios,                previa +                     escrito por
   imágenes)                   código legacy)               el humano)
       │                             │                             │
       ▼                             ▼                             ▼
┌────────────┐              ┌────────────────┐            ┌──────────────────┐
│ analista-  │              │ arqueologo-    │            │ analista-feature-│
│ entrevistas│              │ codigo         │            │ mantenimiento    │
└──────┬─────┘              └────────┬───────┘            └────────┬─────────┘
       │                             │                             │
       └──────────┬──────────────────┘                              │
                  │                                                 │
                  ▼                                                 ▼
       docs/requirements.md                          docs/features/<X>/requirements.md
       (sistema completo)                            (delta + Surface of Contact
                  │                                   + Invariantes Preservadas)
                  │                                                 │
       [gate humano: aprobación]                          [gate humano: aprobación]
                  │                                                 │
                  ▼                                                 │
       ┌─────────────────────┐ ◄──── ┐                              │
       │ prototipador-visual │       │ válvula                      │
       │ (OPCIONAL — UI)     │       │ de retorno                   │
       └─────────────────────┘       │                              │
                  │                          │                              │
       loop iterativo: ─────────────────────┘                              │
       prototipo ⇄ validation-log                                          │
                  │                                                        │
                  ▼                                                        │
       docs/prototype/ desplegado                                          │
                  │                                                        │
       [gate cliente: aprobación]                                          │
                  │                                                        │
                  ▼                                                        ▼
       ┌─────────────────────┐                                  ┌──────────────────┐
       │ disenador-          │                                  │ disenador-delta- │
       │ arquitecto          │                                  │ mantenimiento    │
       └──────────┬──────────┘                                  └────────┬─────────┘
                  │                                                      │
                  ▼                                                      ▼
       docs/design.md                                          docs/features/<X>/design.md
       (arquitectura completa)                                 (delta sobre arquitectura
                  │                                             heredada inmutable)
       [gate humano: aprobación]                                          │
                  │                                            [gate humano: aprobación]
                  ▼                                                      │
       ┌─────────────────────┐                                            ▼
       │ descompositor-      │                                  ┌──────────────────┐
       │ tareas              │                                  │ descompositor-   │
       └──────────┬──────────┘                                  │ riesgo-          │
                  │                                              │ mantenimiento    │
                  ▼                                              └────────┬─────────┘
       docs/tasks.md                                                      │
       (orden por capas)                                                  ▼
                  │                                            docs/features/<X>/tasks.md
       [gate humano: aprobación]                                (orden por riesgo
                  │                                             de regresión)
                  │                                                       │
                  │                                            [gate humano: aprobación]
                  └────────────────────┬─────────────────────────────────┘
                                       ▼
                          [tarea por sesión + revisión humana]
                                       │
                                       ▼
                              código + tests
```

### Los gates humanos NO son opcionales

Entre cada fase hay un gate de revisión humana **obligatorio**. Saltarse uno propaga errores exponencialmente: el costo de arreglar un defecto crece 10x por fase.

**No hay "ejecuta todo el pipeline solo"**. Lo intentaste, falló, no insistas.

---

## 4. Cómo usar este framework, paso a paso

### Paso 0: Clonar el repo template

Este framework está pensado para clonarse a cada proyecto nuevo:

```bash
# Si usas GitHub template
gh repo create mi-proyecto-nuevo --template GabrielaStark/SDD

# O clone manual
git clone https://github.com/GabrielaStark/SDD.git mi-proyecto-nuevo
cd mi-proyecto-nuevo
rm -rf .git && git init
```

### Paso 1: Elegir pipeline (greenfield / brownfield-rewrite / mantenimiento)

| Tu situación | Pipeline | Agente inicial |
|---|---|---|
| Construir un sistema desde cero. Tienes material de descubrimiento (entrevistas, formularios, imágenes). | **Greenfield** | `analista-entrevistas` |
| Hay sistema legacy y vas a **reescribirlo / modernizar arquitectura completa**. Tienes código + análisis arqueológico. | **Brownfield-rewrite** | `arqueologo-codigo` |
| Sistema **en producción**, agregar un feature nuevo **sin romper** lo que ya funciona. Stack y arquitectura están dados. | **Mantenimiento** | `analista-feature-mantenimiento` |

Si dudas entre brownfield-rewrite y mantenimiento: **¿el plan es rehacer arquitectura?** → rewrite. **¿el plan es respetarla y solo agregar?** → mantenimiento.

### Paso 2: Cargar inputs según pipeline

**Greenfield**: mete en `docs/inputs/` todo el material crudo del levantamiento:

- Transcripciones de entrevista (`.md`, `.txt`)
- Screenshots, fotos de formularios, diagramas
- PDFs de documentos de contexto
- Notas sueltas

**Brownfield-rewrite**: mete en `docs/analysis/` los `.md` con tu análisis arqueológico previo (notas de exploración, mapeo de módulos, observaciones). El código legacy debe estar accesible en el repo o como referencia.

**Mantenimiento**:

1. (Recomendado) Corre primero las skills auxiliares `onboarding` (genera `docs/CLAUDE.md` + `docs/BIG_PICTURE.md`) y `reglas-negocio` (genera `docs/REGLAS_DE_NEGOCIO.md`) para crear el sustrato. Ambas vienen empaquetadas con el framework en `.claude/skills/`.
2. Crea la carpeta del feature: `docs/features/<slug-del-feature>/`.
3. Copia el template del intent: `cp templates/intent.md docs/features/<slug>/intent.md`.
4. Llena el `intent.md` describiendo el feature en lenguaje de negocio.

### Paso 3: Invocar el subagente correspondiente

Abre Claude Code en el repo y verifica que los agentes aparezcan:

```
/agents
```

Deberías ver los 8 subagentes. Si no, revisa que la carpeta `.claude/agents/` esté en la raíz del repo.

#### Greenfield

```
Use the analista-entrevistas subagent to produce docs/requirements.md
from the material in docs/inputs/
```

#### Brownfield-rewrite

```
Use the arqueologo-codigo subagent to produce docs/requirements.md
from the analysis in docs/analysis/ and the legacy code in [path]
```

#### Mantenimiento

```
Use the analista-feature-mantenimiento subagent to produce
docs/features/<slug>/requirements.md from the intent at
docs/features/<slug>/intent.md and the production code in this repo
```

### Paso 4: Iterar con el agente

El agente va a:

1. Listar el material que encontró
2. Confirmar tu lectura inicial
3. Identificar huecos y hacerte preguntas numeradas
4. Generar el `requirements.md` sección por sección
5. Iterar con tu feedback
6. Ejecutar auto-validación contra el SKILL
7. Declarar "listo para revisión final"

**No le dejes rellenar huecos solo**. Si te hace 10 preguntas, responde las 10. Es mejor que invente.

### Paso 5: Revisión final del requirements.md

Tú validas manualmente. Si está bien, apruebas explícitamente. Si no, pides cambios.

### Paso 6 (opcional): Prototipo visual para validación temprana con cliente

Si el proyecto tiene **UI relevante** (no es backend puro, CLI ni librería), considera invocar la fase opcional de prototipo antes de pasar a diseño. Esto te permite mostrarle al cliente un mockup interactivo desplegado en una URL real, recoger feedback temprano, y detectar requisitos faltantes ANTES de cementarlos en `design.md`.

Estructura mínima previa (opcional):

```
docs/prototype/context/
├── branding.md        ← colores, tipografía, tono (puede estar vacío)
├── logos/             ← assets de marca del cliente (opcional)
└── referencias/       ← screenshots inspiracionales (opcional)
```

Invocación:

```
Use the prototipador-visual subagent to produce docs/prototype/
```

El agente:

1. Verifica que `requirements.md` está aprobado y que el proyecto tiene UI relevante.
2. Pregunta plataforma de despliegue (default Railway; configurable a Netlify, Vercel, Cloudflare Pages, GitHub Pages o manual).
3. Genera un mini-sitio estático (HTML + Tailwind CDN) con banner permanente "MOCKUP NO FUNCIONAL" y datos obviamente falsos.
4. Genera `DEPLOY.md` con instrucciones de despliegue.
5. Genera `validation-log-v1.md` vacío para que transcribas el feedback del cliente.

**Loop iterativo**: tú haces el deploy, muestras al cliente, transcribes feedback en `validation-log-vN.md`, vuelves a invocar al agente para v{N+1}. Cuando el cliente aprueba (Status: APROBADO en el último log), pasas a Paso 7.

**Válvula de retorno**: si el feedback del cliente revela un cambio estructural (entidad nueva, actor nuevo, flujo nuevo, integración externa, NFR duro nuevo), el agente se detiene y te recomienda volver a `analista-entrevistas` para actualizar `requirements.md` ANTES de seguir iterando el prototipo.

Detalles completos: ver [`PROTOTIPO.md`](PROTOTIPO.md) y el skill `sdd-prototype`.

### Paso 7: Diseño

**Greenfield y brownfield-rewrite** — con `docs/requirements.md` aprobado:

```
Use the disenador-arquitecto subagent to produce docs/design.md
```

**Mantenimiento** — con `docs/features/<slug>/requirements.md` aprobado:

```
Use the disenador-delta-mantenimiento subagent to produce
docs/features/<slug>/design.md
```

Repite el ciclo de iteración → auto-validación → aprobación humana.

Nota: si existe `docs/prototype/` (construcción) o `docs/features/<slug>/prototype/` (mantenimiento), el diseñador lo lee como referencia informativa del flujo de UX validado, pero el stack del prototipo (HTML+Tailwind) NO se hereda. El stack real se decide en design (construcción) o se hereda del sistema existente (mantenimiento).

### Paso 8: Tareas

**Greenfield y brownfield-rewrite** — con `docs/design.md` aprobado:

```
Use the descompositor-tareas subagent to produce docs/tasks.md
```

**Mantenimiento** — con `docs/features/<slug>/design.md` aprobado:

```
Use the descompositor-riesgo-mantenimiento subagent to produce
docs/features/<slug>/tasks.md
```

Mismo ciclo de iteración → auto-validación → aprobación humana.

Diferencia clave: en mantenimiento el `tasks.md` se ordena por **riesgo de regresión** (Regression Shield primero, No-Regression Validation al final), no por capa arquitectónica.

### Paso 9: Ejecución de tareas

Con `tasks.md` aprobado, ejecutas **una tarea por sesión**:

1. Lee la siguiente tarea pendiente.
2. Conversación nueva con el agente codificador, contexto mínimo (la tarea + design relevante + requirements relevantes).
3. El agente ejecuta solo esa tarea.
4. Tú revisas el resultado.
5. Iteras hasta que esté bien.
6. Marcas `[x]` en `tasks.md`.
7. Conversación nueva para la siguiente tarea.

**Nunca** le des "ejecuta todo tasks.md de un golpe". Rompe garantizado.

---

## 5. Los componentes uno por uno

### `analista-entrevistas` (greenfield)

**Propósito**: tomar material crudo de descubrimiento y producir `requirements.md`.

**Cuándo usarlo**: cuando arrancas un feature/producto de cero y tienes material de descubrimiento (transcripciones, formularios, imágenes).

**Qué hace bien**:

- Procesa imágenes directamente (screenshots, formularios)
- Detecta huecos y pregunta numerado
- Construye el documento incrementalmente

**Qué NO hace**:

- No es entrevistador en vivo con el cliente
- No rellena huecos con suposiciones

### `arqueologo-codigo` (brownfield)

**Propósito**: tomar análisis arqueológico + código legacy y producir `requirements.md` que describa lo que el sistema **actualmente hace**.

**Cuándo usarlo**: cuando vas a modernizar/reescribir un sistema legacy y necesitas documentar formalmente su comportamiento.

**Qué hace bien**:

- Triangula arqueología vs código (detecta inconsistencias)
- Clasifica feature intencional vs probable bug
- Anota confianza por criterio (`high`/`medium`/`low`)
- Genera secciones extras: `Detected Anomalies`, `Open Questions`, `Coverage Map`

**Qué NO hace**:

- No idealiza el comportamiento ("lo que debería hacer")
- No clasifica unilateralmente comportamiento ambiguo

### `prototipador-visual` (opcional, solo proyectos con UI)

**Propósito**: tomar `requirements.md` aprobado + contexto de branding opcional, y producir un `docs/prototype/` — mockup interactivo de alta fidelidad desplegable en una URL real para validación temprana con cliente.

**Cuándo usarlo**: después de que `requirements.md` está aprobado, **solo si el proyecto tiene UI relevante**. Backend puro, CLIs y librerías la saltan.

**Qué hace bien**:

- Genera HTML estático throwaway (Tailwind CDN, JS vanilla/Alpine) — no contamina el stack real
- Banner permanente "MOCKUP NO FUNCIONAL" en todas las pantallas + datos obviamente falsos
- `server.js` con basic auth via env vars (default Railway, configurable a 5 plataformas)
- Loop iterativo con `validation-log-vN.md` versionado por iteración
- Válvula de retorno al analista cuando el feedback revela cambios estructurales
- Placeholders genéricos si falta branding (no se bloquea en iteración 1)

**Qué NO hace**:

- No genera código de producción (cero React/Vue/Svelte/Next/etc.)
- No decide el stack del proyecto (eso vive en `design.md`)
- No ejecuta `git push` ni `railway up` sin instrucción explícita
- No absorbe cambios estructurales en HTML (devuelve al analista)
- No itera sin un `validation-log-vN.md` previo escrito por el dev
- No se bloquea esperando branding en iteración 1

Para detalles completos de decisiones y reglas: ver [`PROTOTIPO.md`](PROTOTIPO.md) y el skill `sdd-prototype`.

### `disenador-arquitecto`

**Propósito**: tomar `requirements.md` aprobado y producir `design.md` con las 9 secciones obligatorias.

**Cuándo usarlo**: después de que `requirements.md` está validado por el humano.

**Qué hace bien**:

- Lee `CONSTITUTION.md` si existe (decisiones de proyecto inmutables)
- Genera diagramas Mermaid de arquitectura y secuencia
- Produce ADRs con consecuencias positivas Y negativas
- Construye la tabla de Traceability obligatoria

**Qué NO hace**:

- No inventa stack — pregunta si no está claro
- No escribe funciones completas de código

### `descompositor-tareas`

**Propósito**: tomar `design.md` aprobado y producir `tasks.md` ejecutable.

**Cuándo usarlo**: después de que `design.md` está validado por el humano.

**Qué hace bien**:

- Descompone por capas arquitectónicas (Setup → Data Model → ... → E2E)
- Cada tarea con footer de trazabilidad EARS
- Tests como tareas independientes
- Detecta cobertura: ¿cada criterio EARS tiene una tarea que lo cumple?

**Qué NO hace**:

- No deja criterios EARS huérfanos
- No mete tests como sub-pasos

### `analista-feature-mantenimiento` (mantenimiento)

**Propósito**: tomar un `intent.md` con la descripción de un feature + el código de un sistema en producción, y producir `docs/features/<slug>/requirements.md` que documente **el delta** (lo que se añade), su **Surface of Contact** con el sistema existente, y las **Invariantes Preservadas** que NO deben romperse.

**Cuándo usarlo**: cuando hay un sistema en producción y se quiere agregar un feature nuevo sin reescribir nada.

**Qué hace bien**:

- Lee sustrato si existe (`CLAUDE.md`, `BIG_PICTURE.md`, `REGLAS_DE_NEGOCIO.md`)
- Triangula intent ↔ código para mapear superficie de contacto exhaustivamente
- Identifica invariantes con referencia a código (`<!-- source: archivo:líneas -->`)
- Detecta gaps de tests existentes (módulos sin cobertura)
- Recomienda correr `onboarding` y `reglas-negocio` si falta sustrato

**Qué NO hace**:

- No documenta el sistema completo. Solo el delta.
- No rediseña arquitectura (eso es brownfield-rewrite).
- No decide stack (heredado del sistema).
- No clasifica feature ambiguo unilateralmente.

### `disenador-delta-mantenimiento` (mantenimiento)

**Propósito**: tomar `requirements.md` (delta) aprobado y producir `design.md` que describa **cómo se implementa el feature sobre la arquitectura existente** sin rediseñarla.

**Cuándo usarlo**: después de aprobar requirements del pipeline de mantenimiento.

**Qué hace bien**:

- Las 9 secciones del design pero acotadas al delta (200-600 líneas, no 300-800)
- Diagrama Mermaid distingue visualmente componentes nuevos / modificados / existentes
- ADRs solo para decisiones NUEVAS del delta (prefijo `D001`)
- Sección "Coexistencia con flujos existentes" obligatoria para puntos de riesgo medio/alto
- Tabla obligatoria invariantes → tests (existentes o nuevos de blindaje)
- Validación de no-invasión: cualquier componente fuera de Surface of Contact dispara alerta

**Qué NO hace**:

- No redecide stack heredado.
- No rediseña componentes existentes.
- No omite la sección de coexistencia.
- No propone cambios incompatibles hacia atrás sin justificación + plan.

### `descompositor-riesgo-mantenimiento` (mantenimiento)

**Propósito**: tomar `design.md` delta aprobado y producir `tasks.md` ordenado **por riesgo de regresión**.

**Cuándo usarlo**: después de aprobar design del pipeline de mantenimiento.

**Qué hace bien**:

- Estructura por riesgo: `Regression Shield → Spike → Data Delta → Backend → API → Frontend → Integration → E2E → No-Regression Validation → Docs`
- Tareas de **blindaje** (verbo `Blindar`) ANTES de cualquier modificación
- Trazabilidad doble en cada tarea (`_Requirements: X.Y_ | _Invariants: I.A_`)
- Tareas de integración aisladas (una por punto de coexistencia)
- Tarea final obligatoria de `Verificar regresión` (suite completa + invariantes)

**Qué NO hace**:

- No ordena por capa arquitectónica (eso es construcción).
- No omite Regression Shield.
- No agrupa puntos de coexistencia.
- No deja invariantes huérfanas (sin tarea que las blinde o respete).

### Skills de construcción: `sdd-requirements`, `sdd-prototype`, `sdd-design`, `sdd-tasks`

Las constituciones compartidas del pipeline de construcción (greenfield + brownfield-rewrite). Cada subagente carga el skill correspondiente y aplica sus reglas.

El skill `sdd-prototype` es específico de la fase opcional de prototipado — define estructura de `docs/prototype/`, banner obligatorio, política de datos falsos, plantilla del `server.js` con basic auth, formato del `DEPLOY.md` con tabla de plataformas, y formato del `validation-log-vN.md`. Es transversal: aplica también a mantenimiento si el feature lo amerita.

### Skills de mantenimiento: `sdd-requirements-mantenimiento`, `sdd-design-delta`, `sdd-tasks-risk`

Las constituciones del pipeline de mantenimiento. Self-contained — no extienden las skills de construcción, las **reemplazan** dentro del pipeline de mantenimiento. La duplicación es deliberada (ver `MANTENIMIENTO.md` §4.D1): mantiene cada skill como constitución absoluta sin ambigüedad de "cuál gana".

### Templates

Archivos en `templates/` con la estructura canónica y guía inline. Útiles si:

- Quieres entender la estructura sin invocar al agente
- Quieres escribir un documento a mano
- Quieres referencia rápida sin abrir el SKILL completo

---

## 6. Anti-patrones que no debes cometer

### Del flujo

- ❌ Saltar gates humanos. "Ejecuta todo el pipeline" rompe garantizado.
- ❌ Ejecutar `tasks.md` en batch en lugar de tarea por sesión.
- ❌ Validar superficialmente requirements/design y avanzar. Los errores se amplifican 10x por fase.
- ❌ Pasar a `disenador-arquitecto` con la fase de prototipo abierta (último validation-log sin `Status: APROBADO`).
- ❌ Saltarse la válvula de retorno: si el cliente revela un cambio estructural durante prototipo, hay que volver al analista, no parchar en HTML.

### Del requirements.md

- ❌ User Story sin "para Z" (el objetivo de negocio).
- ❌ Criterios EARS en mezcla con `should`/`would`/`may`/`might`/`could`. Solo `SHALL`.
- ❌ Implementación en requirements ("usar PostgreSQL"). Eso va en design.
- ❌ Múltiples comportamientos en un solo criterio (señal: aparece " and " conectando acciones).

### Del prototipo (fase opcional)

- ❌ Usar React/Vue/Svelte o cualquier framework con build. Solo HTML + Tailwind CDN + JS vanilla/Alpine.
- ❌ Omitir el banner "MOCKUP NO FUNCIONAL" o hacerlo dismissible.
- ❌ Datos visibles que parezcan reales (nombres reales del cliente, cifras coherentes, dominios de email reales).
- ❌ Implementar lógica de negocio real ("ya que estamos hago el cálculo de verdad").
- ❌ Hardcodear credenciales en `server.js` o `DEPLOY.md`.
- ❌ Desplegar prototipo con info sensible a GitHub Pages (público por defecto). Usar Railway/Cloudflare con auth.
- ❌ Sobrescribir `validation-log-vN.md` de iteraciones previas.
- ❌ Iterar más de 4-5 veces sin replantearse si el problema está en `requirements.md`.

### Del design.md

- ❌ Descripción en lugar de decisión ("se usará una base de datos apropiada").
- ❌ Funciones completas de código metidas como "ilustración".
- ❌ ADRs sin consecuencias negativas (= decisión no pensada).
- ❌ Errores narrativos ("el sistema devuelve un error apropiado"). Típalos como enum.
- ❌ Faltar la tabla de Traceability.

### Del tasks.md

- ❌ Tareas demasiado grandes (no caben en una sesión).
- ❌ Tests como sub-pasos en lugar de tareas independientes.
- ❌ Orden por valor de negocio en lugar de dependencias técnicas.
- ❌ Tareas sin footer `_Requirements: X.Y_`.
- ❌ Verbos vagos ("Trabajar en", "Hacer").
- ❌ Inflar el archivo con tareas redundantes "por completitud".

### Del pipeline de mantenimiento

- ❌ Usar mantenimiento para reescribir partes del sistema "ya que estamos aquí". Si el plan es reescritura, brownfield-rewrite.
- ❌ Omitir Surface of Contact e Invariantes Preservadas en requirements de mantenimiento.
- ❌ Saltarse Regression Shield del tasks.md.
- ❌ Saltarse No-Regression Validation final.
- ❌ Trazabilidad sin invariantes (`_Requirements: X.Y_ | _Invariants: -_` cuando sí toca código existente).
- ❌ Tareas de integración agrupadas (una por punto de coexistencia, sin excepción).
- ❌ Modificar código existente sin escribir antes el test de blindaje correspondiente.

### Del meta

- ❌ Adaptar SDD a cada caso con excepciones. Las reglas son absolutas; si una no aplica, es que el caso no es para SDD.
- ❌ Vender SDD como "lo que hacen los grandes". No lo es todavía. Es práctica emergente.
- ❌ Adoptar spec-as-source puro (specs como única fuente de verdad sin código). Experimental, no producción.

---

## 7. FAQ

### ¿Puedo saltarme el design e ir directo a tasks?

No. El design es donde se toman las decisiones técnicas que evitan que el LLM downstream invente diferente cada vez. Sin design, tasks queda en el aire y el código resultante es inconsistente.

### ¿Cuándo SÍ debo invocar la fase opcional de prototipo?

Cuando el proyecto tiene UI relevante (web app, mobile app, dashboard) Y el cliente es no técnico o el flujo es complejo. La validación temprana via mockup desplegado vale 10x lo que cuesta porque cierra el gap entre "requirements.md aprobado en texto" y "el cliente entiende qué va a recibir". Si el proyecto es backend puro, CLI o librería, sáltala.

### ¿El prototipo determina el stack final?

No. El HTML+Tailwind del prototipo es **throwaway por diseño**. La decisión de stack (React, Vue, Svelte, HTMX, Astro, lo que sea) vive en `design.md` con sus ADRs. El prototipo solo valida flujo y contenido. Si el cliente ve el HTML y asume "esto será React", el agente y el banner deben dejar claro que el visual final puede diferir.

### ¿Quién llena el `validation-log-vN.md`?

Tú (el dev que usa el framework). NO el cliente. Asumir que el cliente edita Markdown en GitHub falla en el 90% de los casos. El patrón realista es: muestras al cliente la URL, recoges feedback (verbal, Slack, Loom), lo transcribes honestamente al log. El agente lee el log para iterar.

### ¿Qué pasa si el cliente revela un requisito nuevo durante el prototipo?

El agente detecta que es un cambio estructural (entidad nueva, actor nuevo, flujo nuevo, integración nueva, NFR duro nuevo) y se detiene. Te recomienda volver al `analista-entrevistas` para actualizar `requirements.md` con el nuevo Requirement, re-aprobar requirements, y solo después volver a iterar el prototipo. Esto preserva la trazabilidad EARS — corazón del framework.

### ¿Puedo desplegar el prototipo a algo distinto a Railway?

Sí. Railway es default por basic auth fácil + setup conocido, pero el agente soporta Netlify, Vercel, Cloudflare Pages, GitHub Pages y despliegue manual. Lo declaras en `CONSTITUTION.md` con `prototype_deploy: <nombre>` o el agente te pregunta una vez. Importante: para prototipos con info sensible del cliente, evitar GitHub Pages (público por defecto).

### ¿Y si el feature es muy chico, igual hago las 3 fases?

Si el feature genuinamente cabe en 2-3 tareas, sí — pero las 3 fases pueden ser cortas. Un `requirements.md` con 1-2 Requirements, un `design.md` con secciones mínimas pero todas las 9, un `tasks.md` con 3-5 tareas. El overhead vale para mantener la disciplina.

### ¿Y si el feature es enorme?

Lo partes. Una feature = un trío `requirements/design/tasks`. Si el design pasa de 800 líneas o tasks pasa de 50 tareas, partir. Anti-patrón confirmado por Thoughtworks: spec gigante upfront + big-bang release.

### ¿Cómo manejo cambios después de aprobar requirements?

Volviendo. Si cambia un requirement después de aprobar, hay que revisar si afecta el design (probablemente sí) y si afecta tasks (probablemente también). No es "perdimos tiempo" — es exactamente lo que SDD hace bien: detecta el impacto antes de que llegue al código.

### ¿Cuándo uso mantenimiento vs brownfield-rewrite?

Pregunta única: **¿el plan es respetar la arquitectura existente o cambiarla?**

- Si respetas la arquitectura existente y agregas algo: **mantenimiento**.
- Si vas a rehacer la arquitectura (aunque preserves comportamiento): **brownfield-rewrite**.

Caso límite: un sistema "podrido" donde el cliente quiere agregar un feature pero la deuda técnica es enorme. Si el feature es chico y la deuda no bloquea, **mantenimiento** + dejar tareas opcionales de refactor preventivo. Si la deuda hace imposible meter el feature sin romper, **brownfield-rewrite** del módulo afectado primero, después feature.

### ¿Necesito correr `onboarding` y `reglas-negocio` antes de mantenimiento?

Recomendado, no obligatorio. El sustrato (`CLAUDE.md`, `BIG_PICTURE.md`, `REGLAS_DE_NEGOCIO.md`) mejora ~10x la calidad del análisis del primer agente. Sin el sustrato, el agente lee código directo pero la probabilidad de perder invariantes implícitas es mayor.

Si no tienes el sustrato y tampoco tiempo de generarlo: el agente continúa avisando del riesgo, y documenta lo no cubierto en `## Open Questions`.

### ¿Puedo usar el prototipo en mantenimiento?

Sí. Si el feature de mantenimiento introduce UI nueva que el cliente quiere validar antes, invoca `prototipador-visual` después de aprobar el requirements del feature. El prototipo vive en `docs/features/<feature>/prototype/` para mantenerlo scoped al feature. Mismas reglas que el prototipo en construcción (skill `sdd-prototype`).

### ¿Qué pasa si el feature de mantenimiento requiere cambiar arquitectura?

No es mantenimiento. Es brownfield-rewrite parcial. El agente `disenador-delta-mantenimiento` detectará el conflicto (ADR del delta contradice decisión heredada) y alertará. La respuesta correcta es: parar, decidir si el cambio arquitectónico se hace **antes** del feature (como rewrite del módulo afectado, con su propio ciclo SDD) o **se descarta**.

### ¿Puedo tener varios features de mantenimiento en paralelo?

Sí. Cada uno con su carpeta `docs/features/<slug>/`. La trazabilidad sigue siendo por feature, no se mezclan. Si dos features tocan el mismo módulo, el de Surface of Contact lo refleja y los humanos coordinan orden de ejecución.

### ¿Puedo modificar los SKILLs para adaptarlos a mi cliente?

Sí. Los SKILLs son la constitución, pero los puedes versionar por proyecto si el cliente tiene convenciones específicas. La estructura del framework asume que cada repo cliente tiene su propia copia.

### ¿Por qué EARS en inglés si trabajamos en español?

Porque los LLMs procesan EARS mucho mejor en inglés (es como lo entrenaron). User Story en español preserva contexto humano; criterios en inglés preservan precisión técnica. Es el patrón más común en repos reales.

### ¿Por qué Claude Opus y no Sonnet?

Porque el análisis de requirements/design vale la inversión. Si quieres bajar costo en pruebas iniciales, puedes cambiar a Sonnet editando el `model:` field de cada subagente.

### ¿Cómo verifico que un requirements.md está "bien"?

Cada skill tiene un checklist de auto-validación al final. El subagente lo ejecuta antes de cerrar. Tú puedes ejecutarlo manualmente cuando revisas el output.

### ¿Qué hago si el agente no aplica las reglas del SKILL?

Verifica:

1. ¿El `name:` del SKILL coincide con lo que el agente declara en su frontmatter `skills:`?
2. ¿La ubicación es correcta? `.claude/skills/<name>/SKILL.md`
3. ¿Tu versión de Claude Code soporta el campo `skills:` en subagentes?

Si la #3 falla, agrega explícitamente en el system prompt del subagente: "Antes de cualquier acción, lee `.claude/skills/<name>/SKILL.md` y aplica sus reglas".

### ¿Esto es compatible con Spec Kit, Kiro o Junie?

Conceptualmente sí — los tres archivos `requirements.md / design.md / tasks.md` siguen el patrón compartido. La diferencia es la implementación: ellos tienen sus CLI propios, nosotros usamos Claude Code con subagentes. Si en algún momento queremos exportar a Spec Kit, la conversión es directa.

---

## Cierre

SDD bien hecho es: **el formato te da la gramática; el workflow + los quality gates + el verificador independiente son los que hacen que entregue código que funciona**. Sin los tres últimos, vas a tener documentación preciosa con código mediocre.

Este framework te da el formato y el workflow. El quality gate y el rigor en la revisión los pones tú.
