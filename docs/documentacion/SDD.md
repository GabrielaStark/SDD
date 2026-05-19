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
- No tienen integración nativa con nuestro stack (Claude Code, MCPs propios)

Este framework toma la metodología y la adapta a cómo trabajamos.

### Madurez

SDD está en fase **"Assess"** del Tech Radar de Thoughtworks (no "Adopt" todavía). Es práctica emergente bien fundamentada que probablemente sea estándar en 2027. Estamos temprano, no tarde.

---

## 2. Anatomía del framework

### Estructura del repo template

```
SDD/
├── README.md                              ← punto de entrada del repo
├── .claude/
│   ├── agents/                            ← subagentes especializados
│   │   ├── analista-entrevistas.md       ← greenfield: transcripción → requirements
│   │   ├── arqueologo-codigo.md           ← brownfield: legacy → requirements
│   │   ├── disenador-arquitecto.md        ← requirements → design
│   │   └── descompositor-tareas.md        ← design → tasks
│   └── skills/                            ← constituciones compartidas
│       ├── sdd-requirements/SKILL.md      ← reglas del requirements.md
│       ├── sdd-design/SKILL.md            ← reglas del design.md
│       └── sdd-tasks/SKILL.md             ← reglas del tasks.md
├── docs/
│   ├── inputs/                            ← material crudo del levantamiento
│   ├── analysis/                          ← análisis arqueológico previo (brownfield)
│   ├── requirements.md                    ← OUTPUT fase 1
│   ├── design.md                          ← OUTPUT fase 2
│   ├── tasks.md                           ← OUTPUT fase 3
│   └── documentacion/SDD.md               ← este archivo
└── templates/                             ← templates para empezar de cero
    ├── requirements.md
    ├── design.md
    └── tasks.md
```

### Tres conceptos clave

**Subagente**: una instancia de Claude con un system prompt propio, herramientas propias, identidad propia. Cada uno hace UN trabajo bien definido.

**Skill**: un archivo `SKILL.md` con conocimiento procedural reutilizable (reglas, plantillas, validaciones). Los subagentes lo consultan automáticamente cuando lo declaran en su frontmatter.

**Template**: archivo de partida con estructura canónica y guía inline. Útil cuando alguien quiere escribir un documento a mano sin invocar al agente.

---

## 3. El pipeline completo

```
   docs/inputs/                           docs/analysis/
   (transcripciones,                      (arqueología
    formularios,                           previa
    imágenes,                              + código
    notas)                                   legacy)
        │                                       │
        ▼                                       ▼
   ┌────────────────────┐              ┌──────────────────┐
   │ analista-          │              │ arqueologo-      │
   │ entrevistas        │              │ codigo           │
   └────────────────────┘              └──────────────────┘
        │                                       │
        └───────────────────┬───────────────────┘
                            ▼
                  ┌──────────────────────┐
                  │ docs/requirements.md │
                  └──────────────────────┘
                            │
                  [gate humano: aprobación]
                            │
                            ▼
                  ┌──────────────────────┐
                  │ disenador-arquitecto │
                  └──────────────────────┘
                            │
                            ▼
                  ┌──────────────────────┐
                  │ docs/design.md       │
                  └──────────────────────┘
                            │
                  [gate humano: aprobación]
                            │
                            ▼
                  ┌──────────────────────┐
                  │ descompositor-tareas │
                  └──────────────────────┘
                            │
                            ▼
                  ┌──────────────────────┐
                  │ docs/tasks.md        │
                  └──────────────────────┘
                            │
                  [gate humano: aprobación]
                            │
                            ▼
              [tarea por tarea + revisión humana]
                            │
                            ▼
                  ┌──────────────────────┐
                  │ código + tests       │
                  └──────────────────────┘
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

### Paso 1: Decidir si es greenfield o brownfield

- **Greenfield**: vas a construir algo desde cero. Tienes material de descubrimiento (entrevistas, transcripciones, formularios, imágenes). → Vas a usar `analista-entrevistas`.
- **Brownfield**: hay un sistema legacy existente que quieres reescribir o modernizar. Tienes acceso al código y posiblemente análisis previo. → Vas a usar `arqueologo-codigo`.

### Paso 2: Cargar inputs

**Si es greenfield**: mete en `docs/inputs/` todo el material crudo del levantamiento:

- Transcripciones de entrevista (`.md`, `.txt`)
- Screenshots, fotos de formularios, diagramas
- PDFs de documentos de contexto
- Notas sueltas

**Si es brownfield**: mete en `docs/analysis/` los `.md` con tu análisis arqueológico previo (notas de exploración, mapeo de módulos, observaciones). El código legacy debe estar accesible en el repo o como referencia.

### Paso 3: Invocar el subagente correspondiente

Abre Claude Code en el repo y verifica que los agentes aparezcan:

```
/agents
```

Deberías ver los 4 subagentes. Si no, revisa que la carpeta `.claude/agents/` esté en la raíz del repo.

#### Greenfield

```
Use the analista-entrevistas subagent to produce docs/requirements.md
from the material in docs/inputs/
```

#### Brownfield

```
Use the arqueologo-codigo subagent to produce docs/requirements.md
from the analysis in docs/analysis/ and the legacy code in [path]
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

### Paso 6: Diseño

Con `requirements.md` aprobado:

```
Use the disenador-arquitecto subagent to produce docs/design.md
```

Repite el ciclo de iteración → auto-validación → aprobación humana.

### Paso 7: Tareas

Con `design.md` aprobado:

```
Use the descompositor-tareas subagent to produce docs/tasks.md
```

Mismo ciclo.

### Paso 8: Ejecución de tareas

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

### `sdd-requirements`, `sdd-design`, `sdd-tasks` (skills)

Las constituciones compartidas. Cada subagente carga el skill correspondiente y aplica sus reglas. Si quieres cambiar las convenciones del framework (ej. cambiar a EARS en español), editas el SKILL y los subagentes lo respetan.

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

### Del requirements.md

- ❌ User Story sin "para Z" (el objetivo de negocio).
- ❌ Criterios EARS en mezcla con `should`/`would`/`may`/`might`/`could`. Solo `SHALL`.
- ❌ Implementación en requirements ("usar PostgreSQL"). Eso va en design.
- ❌ Múltiples comportamientos en un solo criterio (señal: aparece " and " conectando acciones).

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

### Del meta

- ❌ Adaptar SDD a cada caso con excepciones. Las reglas son absolutas; si una no aplica, es que el caso no es para SDD.
- ❌ Vender SDD como "lo que hacen los grandes". No lo es todavía. Es práctica emergente.
- ❌ Adoptar spec-as-source puro (specs como única fuente de verdad sin código). Experimental, no producción.

---

## 7. FAQ

### ¿Puedo saltarme el design e ir directo a tasks?

No. El design es donde se toman las decisiones técnicas que evitan que el LLM downstream invente diferente cada vez. Sin design, tasks queda en el aire y el código resultante es inconsistente.

### ¿Y si el feature es muy chico, igual hago las 3 fases?

Si el feature genuinamente cabe en 2-3 tareas, sí — pero las 3 fases pueden ser cortas. Un `requirements.md` con 1-2 Requirements, un `design.md` con secciones mínimas pero todas las 9, un `tasks.md` con 3-5 tareas. El overhead vale para mantener la disciplina.

### ¿Y si el feature es enorme?

Lo partes. Una feature = un trío `requirements/design/tasks`. Si el design pasa de 800 líneas o tasks pasa de 50 tareas, partir. Anti-patrón confirmado por Thoughtworks: spec gigante upfront + big-bang release.

### ¿Cómo manejo cambios después de aprobar requirements?

Volviendo. Si cambia un requirement después de aprobar, hay que revisar si afecta el design (probablemente sí) y si afecta tasks (probablemente también). No es "perdimos tiempo" — es exactamente lo que SDD hace bien: detecta el impacto antes de que llegue al código.

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
