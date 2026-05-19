# SDD Framework

> Framework de Spec-Driven Development con subagentes especializados para Claude Code.

Repo template para arrancar cualquier proyecto con metodología SDD adaptada a nuestro flujo de trabajo. Incluye subagentes para greenfield y brownfield, skills compartidos como constitución, templates y documentación completa.

---

## Quick Start

### 1. Clonar como template

```bash
gh repo create mi-proyecto-nuevo --template GabrielaStark/SDD
# o
git clone https://github.com/GabrielaStark/SDD.git mi-proyecto-nuevo
cd mi-proyecto-nuevo && rm -rf .git && git init
```

### 2. Cargar inputs

- **Greenfield**: mete material de levantamiento en `docs/inputs/` (transcripciones, imágenes, formularios).
- **Brownfield**: mete análisis arqueológico previo en `docs/analysis/` + código legacy accesible.

### 3. Abrir Claude Code y ejecutar el pipeline

```
# Verificar que los subagentes estén disponibles
/agents

# Fase 1 — Requirements (elige uno según el caso)
Use the analista-entrevistas subagent to produce docs/requirements.md
Use the arqueologo-codigo subagent to produce docs/requirements.md

# [revisión humana → aprobación]

# Fase 2 — Design
Use the disenador-arquitecto subagent to produce docs/design.md

# [revisión humana → aprobación]

# Fase 3 — Tasks
Use the descompositor-tareas subagent to produce docs/tasks.md

# [revisión humana → aprobación]

# Fase 4 — Ejecución: una tarea por sesión
```

### 4. Leer la documentación completa

Toda la guía paso a paso, anti-patrones, FAQ y referencia de componentes está en:

📖 [`docs/documentacion/SDD.md`](docs/documentacion/SDD.md)

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
│   ├── agents/                            ← 4 subagentes especializados
│   │   ├── analista-entrevistas.md       ← greenfield: material → requirements
│   │   ├── arqueologo-codigo.md           ← brownfield: legacy → requirements
│   │   ├── disenador-arquitecto.md        ← requirements → design
│   │   └── descompositor-tareas.md        ← design → tasks
│   └── skills/                            ← constituciones compartidas
│       ├── sdd-requirements/SKILL.md
│       ├── sdd-design/SKILL.md
│       └── sdd-tasks/SKILL.md
├── docs/
│   ├── inputs/                            ← material crudo (greenfield)
│   ├── analysis/                          ← análisis previo (brownfield)
│   ├── requirements.md                    ← OUTPUT fase 1
│   ├── design.md                          ← OUTPUT fase 2
│   ├── tasks.md                           ← OUTPUT fase 3
│   └── documentacion/SDD.md               ← guía completa
└── templates/                             ← templates con guía inline
    ├── requirements.md
    ├── design.md
    └── tasks.md
```

---

## Pipeline en una imagen

```
inputs/ o analysis/
        ↓
[analista o arqueologo] → docs/requirements.md → [gate humano]
        ↓
[disenador-arquitecto]  → docs/design.md       → [gate humano]
        ↓
[descompositor-tareas]  → docs/tasks.md        → [gate humano]
        ↓
   tarea por sesión + revisión humana → código + tests
```

**Los gates humanos no son opcionales.** Saltarse uno propaga errores 10x a la siguiente fase.

---

## Reglas no negociables

1. **Una tarea = una sesión del agente codificador.** Nunca "ejecuta todo tasks.md".
2. **Cada fase requiere aprobación humana explícita** antes de pasar a la siguiente.
3. **Los SKILLs son absolutos.** Si una regla no encaja en un caso, el caso probablemente no es para SDD — no inventes excepciones.
4. **Trazabilidad bidireccional.** Cada línea de código se justifica en una tarea → decisión de design → criterio EARS → historia de usuario.

---

## Stack y requisitos

- **Claude Code** instalado
- Acceso a modelo Claude Opus (recomendado para los 4 subagentes)
- Material de levantamiento o código legacy según el modo

---

## Licencia y autoría

Framework creado por [iamgabstark_](https://github.com/GabrielaStark) bajo el contexto de Gema.

Adaptación de prácticas SDD documentadas por GitHub Spec Kit, AWS Kiro y JetBrains Junie al flujo de trabajo de Claude Code con subagentes y skills.