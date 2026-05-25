# SDD Framework

> Framework de Spec-Driven Development con subagentes especializados para Claude Code.

Repo template para arrancar cualquier proyecto con metodología SDD adaptada a nuestro flujo de trabajo. Incluye **tres pipelines paralelos**:

- **Greenfield** — construir sistema desde cero
- **Brownfield-rewrite** — reescribir/modernizar un legacy
- **Mantenimiento** — agregar features a un sistema en producción **sin romper** lo existente

Más subagentes especializados, skills compartidos como constitución, templates y documentación completa.

---

## Quick Start

### 1. Elige tu pipeline

| Tu situación | Pipeline | Cómo "instalar" el framework |
|---|---|---|
| Construir desde cero (tienes entrevistas, formularios, imágenes) | **Greenfield** | Clonar como repo nuevo |
| Reescribir legacy (tienes código + arqueología previa) | **Brownfield-rewrite** | Clonar como repo nuevo |
| Sistema en producción + agregar feature sin romper nada | **Mantenimiento** | Copiar `.claude/`, `templates/`, `docs/features/` y `docs/documentacion/` **al repo del sistema existente** |

### 2a. Greenfield / Brownfield-rewrite: clonar como template

```bash
gh repo create mi-proyecto-nuevo --template GabrielaStark/SDD
# o
git clone https://github.com/GabrielaStark/SDD.git mi-proyecto-nuevo
cd mi-proyecto-nuevo && rm -rf .git && git init
```

Carga inputs:
- **Greenfield**: material de levantamiento en `docs/inputs/` (transcripciones, imágenes, formularios).
- **Brownfield-rewrite**: análisis arqueológico previo en `docs/analysis/` + código legacy accesible.

### 2b. Mantenimiento: instalar sobre repo legacy existente

Desde la raíz de tu repo legacy (donde está el sistema en producción), copia-pega este bloque:

```bash
git clone --depth 1 https://github.com/GabrielaStark/SDD.git /tmp/sdd && \
cp -r /tmp/sdd/.claude /tmp/sdd/templates . && \
mkdir -p docs/documentacion docs/features && \
cp /tmp/sdd/docs/documentacion/*.md docs/documentacion/ && \
cp /tmp/sdd/docs/features/README.md docs/features/ && \
rm -rf /tmp/sdd
```

Esto agrega al repo legacy: `.claude/`, `templates/`, `docs/documentacion/` y `docs/features/`. No toca nada más.

**Antes del primer feature** (una sola vez por repo) — genera el sustrato corriendo las skills `onboarding` y `reglas-negocio` desde Claude Code. Producen `docs/CLAUDE.md`, `docs/BIG_PICTURE.md` y `docs/REGLAS_DE_NEGOCIO.md`.

**Por cada feature nuevo**:

```bash
mkdir -p docs/features/<slug-del-feature>
cp templates/intent.md docs/features/<slug-del-feature>/intent.md
# edita docs/features/<slug-del-feature>/intent.md
```

### 3. Abrir Claude Code y ejecutar el pipeline

```
# Verificar que los subagentes estén disponibles (deberías ver 8)
/agents

# Fase 1 — Requirements (elige UNO según tu pipeline)
Use the analista-entrevistas subagent to produce docs/requirements.md                                # greenfield
Use the arqueologo-codigo subagent to produce docs/requirements.md                                   # brownfield-rewrite
Use the analista-feature-mantenimiento subagent to produce docs/features/<slug>/requirements.md     # mantenimiento

# [revisión humana → aprobación]

# Fase 2 (opcional) — Prototipo visual (transversal, solo si UI relevante)
Use the prototipador-visual subagent to produce docs/prototype/                  # construcción
Use the prototipador-visual subagent to produce docs/features/<slug>/prototype/  # mantenimiento

# [loop iterativo con cliente → aprobación del cliente]

# Fase 3 — Design (elige UNO según pipeline)
Use the disenador-arquitecto subagent to produce docs/design.md                                # construcción
Use the disenador-delta-mantenimiento subagent to produce docs/features/<slug>/design.md       # mantenimiento

# [revisión humana → aprobación]

# Fase 4 — Tasks (elige UNO según pipeline)
Use the descompositor-tareas subagent to produce docs/tasks.md                                       # construcción
Use the descompositor-riesgo-mantenimiento subagent to produce docs/features/<slug>/tasks.md         # mantenimiento

# [revisión humana → aprobación]

# Fase 5 — Ejecución: una tarea por sesión
```

### 4. Leer la documentación completa

Toda la guía paso a paso, anti-patrones, FAQ y referencia de componentes está en:

- 📖 [`docs/documentacion/SDD.md`](docs/documentacion/SDD.md) — guía conceptual del framework
- 📋 [`docs/documentacion/Como_se_usan.md`](docs/documentacion/Como_se_usan.md) — manual paso a paso
- 🎨 [`docs/documentacion/PROTOTIPO.md`](docs/documentacion/PROTOTIPO.md) — fase opcional de prototipo
- 🔧 [`docs/documentacion/MANTENIMIENTO.md`](docs/documentacion/MANTENIMIENTO.md) — pipeline de mantenimiento

---

## ¿Qué es SDD?

**Spec-Driven Development** es una práctica donde escribes especificaciones formales primero y el agente IA genera código a partir de ellas. Las specs son el artefacto primario versionado; el código es consecuencia.

Resuelve el problema del vibe-coding: prototipos rápidos pero código frágil. SDD recupera disciplina de ingeniería sin perder velocidad.

Está en fase "Assess" del Tech Radar de Thoughtworks (2025-2026). Práctica emergente bien fundamentada que probablemente sea estándar en 2027.

---

## Arquitectura del framework

```
SDD/
├── .claude/
│   ├── agents/                                       ← 8 subagentes especializados
│   │   ├── analista-entrevistas.md                  ← greenfield: material → requirements
│   │   ├── arqueologo-codigo.md                      ← brownfield-rewrite: legacy → requirements
│   │   ├── prototipador-visual.md                    ← (opcional) requirements → mockup desplegado
│   │   ├── disenador-arquitecto.md                   ← construcción: requirements → design
│   │   ├── descompositor-tareas.md                   ← construcción: design → tasks
│   │   ├── analista-feature-mantenimiento.md         ← mantenimiento: intent + código prod → requirements (delta)
│   │   ├── disenador-delta-mantenimiento.md          ← mantenimiento: requirements (delta) → design (delta)
│   │   └── descompositor-riesgo-mantenimiento.md     ← mantenimiento: design (delta) → tasks (por riesgo)
│   └── skills/                                       ← 9 constituciones compartidas
│       ├── sdd-requirements/SKILL.md                 ← construcción
│       ├── sdd-prototype/SKILL.md                    ← transversal (fase opcional)
│       ├── sdd-design/SKILL.md                       ← construcción
│       ├── sdd-tasks/SKILL.md                        ← construcción
│       ├── sdd-requirements-mantenimiento/SKILL.md   ← mantenimiento
│       ├── sdd-design-delta/SKILL.md                 ← mantenimiento
│       ├── sdd-tasks-risk/SKILL.md                   ← mantenimiento
│       ├── onboarding/SKILL.md                       ← auxiliar: genera CLAUDE.md + BIG_PICTURE.md
│       └── reglas-negocio/SKILL.md                   ← auxiliar: genera REGLAS_DE_NEGOCIO.md
├── docs/
│   ├── inputs/                                       ← material crudo (greenfield)
│   ├── analysis/                                     ← análisis previo (brownfield-rewrite)
│   ├── features/                                     ← pipeline mantenimiento
│   │   └── <slug>/{intent,requirements,design,tasks}.md
│   ├── requirements.md                               ← OUTPUT construcción
│   ├── prototype/                                    ← OUTPUT prototipo (construcción)
│   ├── design.md                                     ← OUTPUT construcción
│   ├── tasks.md                                      ← OUTPUT construcción
│   └── documentacion/
│       ├── SDD.md                                    ← guía conceptual
│       ├── Como_se_usan.md                           ← manual paso a paso
│       ├── PROTOTIPO.md                              ← decisiones de la fase opcional
│       └── MANTENIMIENTO.md                          ← decisiones del pipeline de mantenimiento
└── templates/                                        ← templates con guía inline
    ├── requirements.md, design.md, tasks.md          ← construcción
    └── intent.md, requirements-mantenimiento.md,     ← mantenimiento
        design-delta.md, tasks-riesgo.md
```

---

## Tres pipelines en una imagen

```
GREENFIELD                BROWNFIELD-REWRITE          MANTENIMIENTO
(desde cero)              (reescribir legacy)         (feature a sistema en prod)
    │                          │                              │
    ▼                          ▼                              ▼
docs/inputs/              docs/analysis/                docs/features/<X>/
    │                          │                              │
    ▼                          ▼                              ▼
analista-                 arqueologo-                  analista-feature-
entrevistas               codigo                       mantenimiento
    │                          │                              │
    └──────────┬───────────────┘                              │
               ▼                                              ▼
   docs/requirements.md                            docs/features/<X>/requirements.md
   (sistema completo)                              (DELTA + Surface of Contact
               │                                    + Invariantes Preservadas)
       [gate humano]                                          │
               │                                       [gate humano]
               ▼                                              │
   (prototipo opcional, transversal a los tres) ──────────────┤
               │                                              │
       [gate cliente]                                         │
               ▼                                              ▼
   disenador-arquitecto                            disenador-delta-mantenimiento
               │                                              │
               ▼                                              ▼
   docs/design.md                                  docs/features/<X>/design.md
   (arquitectura completa)                         (delta sobre arq. heredada)
       [gate humano]                                  [gate humano]
               ▼                                              ▼
   descompositor-tareas                            descompositor-riesgo-
                                                    mantenimiento
               │                                              │
               ▼                                              ▼
   docs/tasks.md                                   docs/features/<X>/tasks.md
   (orden por capa)                                (orden por RIESGO de regresión)
       [gate humano]                                  [gate humano]
               │                                              │
               └────────────────────┬─────────────────────────┘
                                    ▼
                        tarea por sesión + revisión humana → código + tests
```

**Los gates humanos no son opcionales.** Saltarse uno propaga errores 10x a la siguiente fase.

**Diferencia clave del pipeline de mantenimiento**: la arquitectura/stack son **heredados e inmutables**, los artefactos describen solo el **delta**, las tasks van ordenadas por **riesgo de regresión** (Regression Shield primero, No-Regression Validation al final), y se documentan explícitamente las **Invariantes Preservadas** del sistema existente.

---

## Reglas no negociables

1. **Una tarea = una sesión del agente codificador.** Nunca "ejecuta todo tasks.md".
2. **Cada fase requiere aprobación humana explícita** antes de pasar a la siguiente.
3. **Los SKILLs son absolutos.** Si una regla no encaja en un caso, el caso probablemente no es para SDD — no inventes excepciones.
4. **Trazabilidad bidireccional.** Cada línea de código se justifica en una tarea → decisión de design → criterio EARS → historia de usuario.
5. **(Mantenimiento)** El Regression Shield va primero, la No-Regression Validation va última. Ambas son obligatorias.

---

## Stack y requisitos

- **Claude Code** instalado
- Acceso a modelo Claude Opus (recomendado para los 8 subagentes)
- Material según el pipeline:
  - Greenfield: entrevistas, transcripciones, formularios
  - Brownfield-rewrite: código legacy + arqueología previa
  - Mantenimiento: código en producción + descripción del feature
- (Mantenimiento recomendado) Skills auxiliares `onboarding` y `reglas-negocio` (ya incluidas en `.claude/skills/`) para generar el sustrato (`CLAUDE.md`, `BIG_PICTURE.md`, `REGLAS_DE_NEGOCIO.md`)

---

## Licencia y autoría

Framework creado por [iamgabstark_](https://github.com/GabrielaStark) bajo el contexto de Gema.

Adaptación de prácticas SDD documentadas por GitHub Spec Kit, AWS Kiro y JetBrains Junie al flujo de trabajo de Claude Code con subagentes y skills.