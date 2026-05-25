# Manual del Framework SDD

> Guía práctica paso a paso. Si ya leíste `SDD.md` (la guía conceptual), este es el "hands-on": cómo se usa en la vida real, qué esperar en cada paso, y qué hacer cuando algo no sale como debería.

---

## Índice

1. [Para qué sirve esto](#1-para-qué-sirve-esto)
2. [Antes de empezar](#2-antes-de-empezar)
3. [Setup del proyecto](#3-setup-del-proyecto)
4. [Los tres pipelines en una imagen](#4-los-tres-pipelines-en-una-imagen)
5. [Fase 0: Elegir pipeline (greenfield / brownfield-rewrite / mantenimiento)](#5-fase-0-elegir-pipeline)
6. [Fase 1: Levantamiento de requerimientos](#6-fase-1-levantamiento-de-requerimientos)
   - [5A. Greenfield](#5a-greenfield--usando-analista-entrevistas)
   - [5B. Brownfield-rewrite](#5b-brownfield-rewrite--usando-arqueologo-codigo)
   - [5C. Mantenimiento (sistema en prod + feature nuevo)](#5c-mantenimiento--usando-analista-feature-mantenimiento)
   - [Fase 1.5 (opcional): Prototipo visual](#fase-15-opcional-prototipo-visual)
7. [Fase 2: Diseño técnico](#7-fase-2-diseño-técnico)
8. [Fase 3: Descomposición en tareas](#8-fase-3-descomposición-en-tareas)
9. [Fase 4: Ejecución del código](#9-fase-4-ejecución-del-código)
10. [Reglas de oro durante el uso](#10-reglas-de-oro-durante-el-uso)
11. [Troubleshooting](#11-troubleshooting)
12. [Glosario rápido](#12-glosario-rápido)

---

## 1. Para qué sirve esto

Este framework te permite construir software de forma estructurada usando Claude Code y subagentes especializados. En vez de pedirle código a un agente "a ver qué sale" (vibe-coding), escribes especificaciones formales primero y el código se genera a partir de ellas con disciplina.

**Lo que entregas al final**: código que funciona, está testeado, y cada línea se puede rastrear hasta un requerimiento concreto del cliente.

**Lo que NO es**: una herramienta para hacer prototipos rápidos. Si lo único que necesitas es un MVP de 4 horas para validar una idea, esto es demasiado overhead. SDD vale la pena cuando vas a producción con clientes reales.

---

## 2. Antes de empezar

### Qué necesitas instalado

- **Claude Code** (CLI de Anthropic). Si no lo tienes:
  ```bash
  curl -fsSL https://claude.ai/install.sh | bash
  ```
- **Git** (para versionar tus specs).
- **Una suscripción que te dé acceso a Claude Opus** (los 4 subagentes están configurados con `model: opus`).

### Conocimiento mínimo asumido

- Saber qué es una terminal y cómo abrir Claude Code en un repo.
- Conocer markdown básico (vas a leer y editar `.md`).
- Tener noción de qué es un agente IA (no hace falta ser experto).

### Tiempo estimado

- **Setup inicial del repo**: 5-10 minutos.
- **Primera fase (requirements)**: 30-90 minutos según material que tengas.
- **Segunda fase (design)**: 45-90 minutos.
- **Tercera fase (tasks)**: 20-45 minutos.
- **Cuarta fase (código)**: depende del feature. Una tarea = 15-45 minutos en sesión.

No es rápido. Es **predecible**. Esa es la diferencia con vibe-coding.

---

## 3. Setup del proyecto

### Paso 1: Clonar el framework como template

Si está como repo template en GitHub:

```bash
gh repo create mi-proyecto-nuevo --template GabrielaStark/SDD
cd mi-proyecto-nuevo
```

O manualmente:

```bash
git clone https://github.com/GabrielaStark/SDD.git mi-proyecto-nuevo
cd mi-proyecto-nuevo
rm -rf .git
git init
```

### Paso 2: Verificar la estructura

Asegúrate de que estos archivos estén:

```
mi-proyecto-nuevo/
├── .claude/agents/       (8 archivos .md — 5 construcción + 3 mantenimiento)
├── .claude/skills/       (7 carpetas con SKILL.md — 4 construcción + 3 mantenimiento)
├── docs/inputs/          (vacía, con .gitkeep — pipeline greenfield)
├── docs/analysis/        (vacía, con .gitkeep — pipeline brownfield-rewrite)
├── docs/features/        (vacía — pipeline mantenimiento; una subcarpeta por feature)
├── docs/documentacion/   (SDD.md, Como_se_usan.md, PROTOTIPO.md, MANTENIMIENTO.md)
└── templates/            (7 archivos .md — 3 construcción + 1 intent + 3 mantenimiento)
```

**Importante para mantenimiento**: si vas a usar el pipeline de mantenimiento, en lugar de clonar el framework como repo nuevo, lo que harás es **copiar `.claude/` + `templates/` + las carpetas `docs/` relevantes** al repo del sistema en producción donde quieres meter el feature. Detalles en [Fase 0](#5-fase-0-elegir-pipeline).

### Paso 3: Abrir Claude Code

```bash
claude
```

### Paso 4: Verificar que los subagentes se cargaron

Dentro de Claude Code:

```
/agents
```

Debes ver los 8 subagentes:

**Pipeline de construcción (greenfield + brownfield-rewrite):**
- `analista-entrevistas`
- `arqueologo-codigo`
- `prototipador-visual` (transversal, también aplica a mantenimiento)
- `disenador-arquitecto`
- `descompositor-tareas`

**Pipeline de mantenimiento:**
- `analista-feature-mantenimiento`
- `disenador-delta-mantenimiento`
- `descompositor-riesgo-mantenimiento`

**Si NO aparecen los 8**: revisa la sección [Troubleshooting](#11-troubleshooting).

**No avances al pipeline si no aparecen todos.** Resolver el problema ahorita es 5 minutos; descubrirlo a media fase es perder horas de trabajo.

> **Nota**: aunque ves los 8 agentes en cualquier proyecto, solo vas a usar los del pipeline correspondiente a tu escenario. Los demás son porteros estrictos: si los invocas en el contexto equivocado, se detienen sin hacer nada. Eso es por diseño.

---

## 4. Los tres pipelines en una imagen

El framework tiene **tres pipelines paralelos**. Eliges uno en Fase 0, según tu escenario:

```
                     ┌─────────────────────────────┐
                     │  Fase 0: elige pipeline     │
                     │  (ver §5)                   │
                     └──────────────┬──────────────┘
                                    │
       ┌────────────────────────────┼────────────────────────────┐
       ▼                            ▼                            ▼
┌──────────────┐            ┌────────────────┐         ┌───────────────────┐
│ GREENFIELD   │            │ BROWNFIELD-    │         │ MANTENIMIENTO     │
│              │            │ REWRITE        │         │                   │
│ desde cero   │            │ reescribir     │         │ feature a sistema │
│              │            │ legacy         │         │ en producción     │
└──────┬───────┘            └────────┬───────┘         └─────────┬─────────┘
       │                             │                           │
       ▼                             ▼                           ▼
  docs/inputs/                 docs/analysis/             docs/features/<X>/
  (entrevistas,                (arqueología               (intent.md escrito
   formularios,                 previa +                   por ti describiendo
   imágenes)                    código legacy)             el feature)
       │                             │                           │
       ▼                             ▼                           ▼
  analista-                    arqueologo-                 analista-feature-
  entrevistas                  codigo                      mantenimiento
       │                             │                           │
       └─────────────┬───────────────┘                           │
                     ▼                                           ▼
        docs/requirements.md                          docs/features/<X>/requirements.md
        (sistema completo)                            (DELTA + Surface of Contact
                     │                                 + Invariantes Preservadas)
            [✋ TÚ apruebas]                                     │
                     │                                  [✋ TÚ apruebas]
                     ▼                                           │
        ┌──────────────────────┐                                 │
        │ prototipador-visual  │ ◄── (transversal, también       │
        │ (opcional, si UI)    │      aplica a mantenimiento)    │
        └──────────────────────┘                                 │
                     │                                           │
            loop: prototipo ⇄ cliente                            │
                     │                                           │
            [✋ Cliente aprueba]                                  │
                     │                                           │
                     ▼                                           ▼
        ┌──────────────────────┐                       ┌─────────────────────┐
        │ disenador-arquitecto │                       │ disenador-delta-    │
        │                      │                       │ mantenimiento       │
        └──────────────────────┘                       └─────────────────────┘
                     │                                           │
                     ▼                                           ▼
            docs/design.md                          docs/features/<X>/design.md
            (arquitectura completa,                 (DELTA sobre arquitectura
             9 secciones, 300-800 líneas)            heredada inmutable,
                     │                               200-600 líneas)
            [✋ TÚ apruebas]                                     │
                     │                                  [✋ TÚ apruebas]
                     ▼                                           │
        ┌──────────────────────┐                                 ▼
        │ descompositor-tareas │                       ┌─────────────────────┐
        └──────────────────────┘                       │ descompositor-      │
                     │                                  │ riesgo-             │
                     ▼                                  │ mantenimiento       │
            docs/tasks.md                              └─────────────────────┘
            (orden por capa                                      │
             arquitectónica)                                     ▼
                     │                              docs/features/<X>/tasks.md
            [✋ TÚ apruebas]                        (orden por RIESGO de regresión:
                     │                               Regression Shield primero,
                     │                               No-Regression Validation
                     │                               al final)
                     │                                           │
                     │                                  [✋ TÚ apruebas]
                     └────────────────┬────────────────────────┘
                                      ▼
                      [una tarea por sesión + revisión humana]
                                      │
                                      ▼
                              código + tests
```

Los ✋ son **gates humanos obligatorios**. Si saltas uno, te disparas en el pie.

**Observación clave**: los tres pipelines comparten filosofía (specs primero, gates humanos, trazabilidad, una tarea por sesión) pero usan agentes, skills y artefactos distintos. El template del framework incluye TODOS, tú usas solo los de tu pipeline.

---

## 5. Fase 0: Elegir pipeline

Antes de invocar cualquier agente, tienes que decidir en qué pipeline vives. Esto se hace **una vez por proyecto** (o **una vez por feature** en el caso de mantenimiento).

### Árbol de decisión

```
                ¿Tienes un sistema funcionando en producción?
                                │
            ┌───────────────────┴───────────────────┐
            │                                       │
           NO                                       SÍ
            │                                       │
            ▼                                       ▼
    ┌──────────────┐                  ¿Quieres reescribir / cambiar
    │ GREENFIELD   │                  arquitectura completa o solo
    │              │                  agregar features?
    │ Vas a        │                                │
    │ construir    │                  ┌─────────────┴─────────────┐
    │ desde cero   │                  │                           │
    │              │                Reescribir                Agregar feature
    │ Inputs:      │                  │                           │
    │ entrevistas, │                  ▼                           ▼
    │ formularios, │           ┌──────────────┐         ┌──────────────────┐
    │ imágenes     │           │ BROWNFIELD-  │         │ MANTENIMIENTO    │
    └──────────────┘           │ REWRITE      │         │                  │
                               │              │         │ Inputs: intent   │
                               │ Inputs:      │         │ del feature +    │
                               │ arqueología  │         │ código en prod   │
                               │ previa +     │         │                  │
                               │ código       │         │ Sustrato         │
                               │ legacy       │         │ recomendado:     │
                               └──────────────┘         │ CLAUDE.md,       │
                                                        │ BIG_PICTURE.md,  │
                                                        │ REGLAS_DE_       │
                                                        │ NEGOCIO.md       │
                                                        └──────────────────┘
```

### Tabla de decisión rápida

| Tu situación | Pipeline | Agente inicial |
|---|---|---|
| Cliente nuevo, idea nueva, tienes entrevistas/transcripciones/formularios. | **Greenfield** | `analista-entrevistas` |
| Sistema legacy roto/anticuado que vas a **rehacer**. Tienes acceso al código + análisis previo. | **Brownfield-rewrite** | `arqueologo-codigo` |
| Sistema **en producción** que funciona. Quieres **agregar** algo sin romper. | **Mantenimiento** | `analista-feature-mantenimiento` |
| Sistema legacy pero el feature nuevo **no existe** en él (mitad y mitad) | Decide caso por caso: si vas a redescribir el sistema viejo + agregar nuevo, **rewrite + greenfield** (dos requirements.md). Si vas a respetar el viejo y solo agregar, **mantenimiento**. |
| Sistema en producción + el feature requiere **rehacer arquitectura** | NO es mantenimiento. Es **rewrite parcial del módulo afectado** primero, después feature de mantenimiento. |

### Cómo se "instala" el framework según pipeline

**Greenfield y brownfield-rewrite**: clonas el repo template como nuevo proyecto:

```bash
gh repo create mi-proyecto-nuevo --template GabrielaStark/SDD
cd mi-proyecto-nuevo
```

**Mantenimiento**: el framework se **agrega encima** del repo del sistema en producción. NO crees un repo nuevo. Lo que harás:

```bash
cd /ruta/al/repo/del/sistema-en-prod   # tu repo de producción, intacto
# Copiar las piezas del framework SDD necesarias:
cp -r /ruta/al/clone/de/SDD/.claude .
cp -r /ruta/al/clone/de/SDD/templates .
mkdir -p docs/features
cp -r /ruta/al/clone/de/SDD/docs/documentacion docs/
```

**Importante para mantenimiento**: solo copias `.claude/` (agentes y skills) + `templates/` + `docs/documentacion/` + `docs/features/` vacío. **NO copies** `docs/inputs/`, `docs/analysis/`, ni los archivos `requirements.md`/`design.md`/`tasks.md` raíz — esos son del pipeline de construcción y van a estorbar.

Si el repo del cliente ya tiene un `.claude/` propio o un `CLAUDE.md` propio, **no los sobreescribas**. Fusiona con cuidado o pregunta al cliente cómo proceder.

### Una vez elegido el pipeline

Salta directo a la sección correspondiente:

- Greenfield → [Fase 1, sección 5A](#5a-greenfield--usando-analista-entrevistas)
- Brownfield-rewrite → [Fase 1, sección 5B](#5b-brownfield-rewrite--usando-arqueologo-codigo)
- Mantenimiento → [Fase 1, sección 5C](#5c-mantenimiento--usando-analista-feature-mantenimiento)

---

## 6. Fase 1: Levantamiento de requerimientos

Esta fase produce el `requirements.md` correspondiente a tu pipeline. Tres caminos según lo elegido en Fase 0:

| Pipeline | Subagente | Output |
|---|---|---|
| Greenfield | `analista-entrevistas` | `docs/requirements.md` (sistema completo) |
| Brownfield-rewrite | `arqueologo-codigo` | `docs/requirements.md` (sistema completo, descrito desde código) |
| Mantenimiento | `analista-feature-mantenimiento` | `docs/features/<slug>/requirements.md` (delta del feature) |

---

### 5A. Greenfield — usando `analista-entrevistas`

#### Paso 1: Prepara el material

Mete en `docs/inputs/` todo lo que tengas:

- Transcripciones de entrevista (`.md` o `.txt`).
- Screenshots de pantallas existentes, sistemas competidores, formularios.
- Fotos de diagramas a mano alzada.
- PDFs de documentos del cliente.
- Notas sueltas tuyas con observaciones.

No te preocupes por organizarlo perfecto. El agente lee todo.

#### Paso 2: Invoca el agente

En Claude Code, escribe exactamente:

```
Use the analista-entrevistas subagent to produce docs/requirements.md
from the material in docs/inputs/
```

#### Paso 3: Qué esperar

El agente va a ejecutar **5 fases** internamente. Tu trabajo es responder cuando pregunte.

| Fase del agente                 | Qué hace                                                                                                                                        | Tu trabajo                                                                            |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| **1. Inventario**               | Lista todos los archivos que encontró, te resume qué leyó.                                                                                      | Confirmar que su lectura inicial es correcta. Si malinterpretó algo, corrígelo ahora. |
| **2. Identificación de huecos** | Te entrega **preguntas numeradas** sobre cosas ambiguas, casos borde no cubiertos, actores no definidos, restricciones no funcionales ausentes. | Responder TODAS las preguntas por número. No le dejes rellenar con suposiciones.      |
| **3. Síntesis incremental**     | Genera el `requirements.md` sección por sección y te lo muestra.                                                                                | Revisar cada `Requirement N` y decir si captura lo levantado o si falta/sobra algo.   |
| **4. Auto-validación**          | Ejecuta el checklist del SKILL contra el archivo. Te reporta cada ítem como ✅ o ❌.                                                            | Esperar a que llegue a 100% ✅.                                                       |
| **5. Cierre**                   | Declara "listo para revisión final".                                                                                                            | Hacer **tú** la revisión manual y aprobar (o pedir cambios).                          |

#### Paso 4: Cómo validar el output

Antes de aprobar, verifica manualmente:

- [ ] Cada `### Requirement N` tiene una `**User Story:**` en español con la fórmula completa "Como X, quiero Y, para Z".
- [ ] Cada Requirement tiene al menos un criterio EARS en inglés.
- [ ] Los criterios usan SOLO `SHALL` (nunca `should`, `would`, `may`).
- [ ] No hay implementación (frameworks, librerías, bases de datos específicas) — eso va en design, no aquí.
- [ ] Existe la sección `## Out of Scope` con cosas explícitas que NO se van a hacer.
- [ ] Tú puedes leer el documento de corrido y entender qué hay que construir.

Si todo eso está, di explícitamente algo como **"aprobado, sigue con design"**. Si no, pide los cambios específicos y el agente itera.

---

### 5B. Brownfield — usando `arqueologo-codigo`

#### Paso 1: Prepara el material

- Mete en `docs/analysis/` todos los `.md` con tu análisis arqueológico previo (notas, mapeo de módulos, hallazgos).
- Asegúrate de que el código legacy esté accesible en el repo (puede ser un submódulo, una carpeta dedicada, o referenciado).

#### Paso 2: Invoca el agente

```
Use the arqueologo-codigo subagent to produce docs/requirements.md
from the analysis in docs/analysis/ and the legacy code in [ruta_al_código]
```

Reemplaza `[ruta_al_código]` con la ruta real (ej. `./legacy/`).

#### Paso 3: Qué esperar

Similar al analista, pero con dos diferencias clave:

1. **El agente clasifica cada comportamiento** en una de estas categorías:
   - `feature intencional` (alta confianza, va al requirements.md)
   - `probable feature` (media confianza, va con anotación)
   - `probable bug` (NO va al requirements, va a sección `Detected Anomalies` para que tú decidas)
   - `ambiguo` (te pregunta antes de clasificar)

2. **Cada criterio derivado de código lleva un comentario de trazabilidad**:
   ```markdown
   1. WHEN the user clicks "Calcular" THE SYSTEM SHALL recalculate all fields.
      <!-- confidence: high; source: src/forms/calc.js:142-178 -->
   ```

#### Paso 4: Secciones extras que vas a ver

Además de la estructura normal, este `requirements.md` tendrá:

- `## Detected Anomalies` — cosas que parecen bug, **tú decides** si se preservan o se corrigen en la modernización.
- `## Open Questions` — cosas que ni el agente ni tú pudieron resolver al momento.
- `## Coverage Map` — tabla "módulo legacy → Requirement que lo cubre". Sirve para detectar código legacy huérfano o requirements sin código.

#### Paso 5: Cómo validar

Mismo checklist que greenfield, MÁS:

- [ ] Cada criterio derivado de código tiene su `<!-- confidence: X; source: Y -->`.
- [ ] No quedan criterios con confianza `low` sin resolución (o se promovieron, o se movieron a Open Questions).
- [ ] La sección `## Detected Anomalies` tiene contenido si se detectaron cosas raras.
- [ ] La sección `## Coverage Map` está completa.

---

### 5C. Mantenimiento — usando `analista-feature-mantenimiento`

> Pipeline para **agregar un feature a un sistema en producción sin romper lo que ya funciona**.
> Si todavía no lo tienes claro, vuelve a [Fase 0](#5-fase-0-elegir-pipeline) y verifica.

#### Pre-requisito recomendado: generar el sustrato

Antes del primer feature de mantenimiento sobre un sistema, **se recomienda fuertemente** correr dos skills auxiliares (vienen incluidas en `.claude/skills/`, no son del pipeline de mantenimiento per se pero su output sirve de sustrato):

```
# 1. Para generar CLAUDE.md y BIG_PICTURE.md (radiografía del repo)
Skill: onboarding

# 2. Para generar REGLAS_DE_NEGOCIO.md (roles, permisos, flujos, validaciones)
Skill: reglas-negocio
```

Estos archivos viven en `docs/` raíz (no dentro de `features/`) porque aplican a todo el sistema. El agente del pipeline los lee como base.

**¿Y si no los tengo?** Puedes continuar igual — el agente avisa del riesgo y se aplica con más cuidado. Pero la calidad del análisis y la captura de invariantes mejora ~10x con el sustrato. Si vas a meter más de un feature en el sistema, vale la pena correr esto **una vez**.

#### Paso 1: Crear la carpeta del feature

Define un slug para el feature (kebab-case, descriptivo). Ejemplos: `exportar-reportes-pdf`, `notificaciones-push`, `auth-mfa`.

```bash
mkdir -p docs/features/exportar-reportes-pdf
```

#### Paso 2: Escribir el `intent.md`

Copia el template y rellénalo:

```bash
cp templates/intent.md docs/features/exportar-reportes-pdf/intent.md
```

Ahora abre el archivo y describe el feature en lenguaje de negocio. Las secciones del template son:

- **Qué queremos** — descripción del feature
- **Por qué** — problema que resuelve
- **Quién pidió** — stakeholder
- **En qué área del sistema vive (intuición inicial)** — tu mejor adivinanza, no tiene que ser preciso
- **Out of scope explícito** — qué NO va a estar
- **Pistas técnicas conocidas (opcional)** — si ya sabes que toca ciertos archivos
- **Stakeholder técnico** — quién resuelve dudas técnicas
- **Fecha / urgencia** — contexto

**Importante**: este es un input para el agente, no un documento formal. Escríbelo en prosa libre. El agente lo refina y formaliza después.

#### Paso 3: Invoca el agente

En Claude Code, dentro del repo del sistema en producción, escribe:

```
Use the analista-feature-mantenimiento subagent to produce
docs/features/exportar-reportes-pdf/requirements.md from the intent at
docs/features/exportar-reportes-pdf/intent.md and the production code in this repo
```

Reemplaza `exportar-reportes-pdf` con tu slug real.

#### Paso 4: Qué esperar

El agente va a ejecutar **7 fases** internamente. Tu trabajo es responder cuando pregunte.

| Fase del agente | Qué hace | Tu trabajo |
|---|---|---|
| **1. Lectura del intent + sustrato** | Lee `intent.md`, `docs/CLAUDE.md`, `docs/BIG_PICTURE.md`, `docs/REGLAS_DE_NEGOCIO.md` (si existen), mapea estructura del código. Reporta qué encontró. | Confirmar la lectura inicial. Si malinterpretó algo, corrígelo. Si falta sustrato, el agente te avisa — decide si pausas para correrlo o continúas. |
| **2. Triangulación intent ↔ código** | Para cada capacidad del intent, localiza módulos relacionados en el código y mapea Surface of Contact (qué módulos toca el feature, lee, modifica, o NO toca). | Validar el mapa preliminar. |
| **3. Identificación de invariantes** | Infiere invariantes preservadas (comportamientos del sistema que NO deben cambiar) con referencias al código. Te las presenta numeradas (`I.1`, `I.2`, ...). | Confirmar o descartar cada invariante numerada. Mejor sobre-listar y descartar que omitir. |
| **4. Resolución de huecos** | Preguntas numeradas sobre actores, casos borde, NFR del feature, out-of-scope, términos ambiguos. | Responder TODAS las preguntas por número. |
| **5. Síntesis incremental** | Genera el `requirements.md` sección por sección y te lo muestra. | Revisar cada sección. Surface of Contact e Invariantes Preservadas son las más críticas. |
| **6. Auto-validación** | Ejecuta el checklist del SKILL contra el archivo. Reporta ✅ / ❌. | Esperar a 100% ✅. |
| **7. Cierre** | Declara "listo para revisión final". | Hacer **tú** la revisión manual y aprobar (o pedir cambios). |

#### Paso 5: Cómo validar el output

El `requirements.md` de mantenimiento es distinto del de greenfield. Verifica:

- [ ] Existe sección `## Contexto` con qué/por qué/quién/dónde vive el feature.
- [ ] Existe sección `## Surface of Contact` con tabla rellena. **Cada fila** lista un módulo/archivo/endpoint/tabla que el feature toca, lee, o explícitamente NO toca, con su nivel de riesgo.
- [ ] Existe sección `## Invariantes Preservadas` con mínimo una invariante numerada `**I.N**`, cada una con comentario `<!-- source: archivo:líneas -->`.
- [ ] Existe sección `## Tests Existentes a Preservar` con tabla que indica qué tests cubren cada invariante (y cuáles son **gaps** sin test).
- [ ] Existe sección `## Requirements (del delta)` con al menos un `### Requirement N` que describe **solo el feature nuevo**, no el sistema.
- [ ] Cada Requirement con `**User Story:** Como X, quiero Y, para Z.` en español.
- [ ] Acceptance Criteria en inglés con `SHALL` únicamente.
- [ ] Existe sección `## Out of Scope (del feature)` explícita.
- [ ] El requirements **NO documenta el sistema completo** — solo el delta.
- [ ] El requirements **NO propone reescribir** arquitectura existente. Si lo hace, pausa: probablemente el pipeline correcto es brownfield-rewrite, no mantenimiento.

Si todo está, di explícitamente **"aprobado, sigue con design"** (o pasa a la fase opcional de prototipo si el feature tiene UI nueva).

#### Caso especial: el feature requiere cambiar arquitectura

Si en el camino descubres que el feature **no se puede meter sin tocar arquitectura existente** (ej. necesitas Redis y el sistema no lo tenía, o el feature implica rehacer el módulo de auth), el agente te lo señala como **alerta crítica**.

Opciones:

1. **Salir del pipeline de mantenimiento** y planear un `brownfield-rewrite` del módulo afectado **antes** del feature. Después del rewrite, volver a mantenimiento para el feature.
2. **Reducir scope** del feature para evitar el cambio arquitectónico.
3. **Aceptar el cambio arquitectónico** y documentarlo explícitamente con un ADR especial en el design (eso ya es mantenimiento con riesgo elevado — el humano decide).

El framework no te obliga a una opción — te obliga a **hacer explícita la decisión**.

---

## Fase 1.5 (opcional): Prototipo visual

> Esta fase es **opcional** y **transversal** a los tres pipelines. Aplica cuando el proyecto o feature tiene UI relevante y quieres validar visualmente con el cliente antes de pasar a diseño técnico. Si es backend puro, CLI o librería, sáltala.

### Pre-requisito

- **Greenfield / brownfield-rewrite**: `docs/requirements.md` aprobado por ti.
- **Mantenimiento**: `docs/features/<slug>/requirements.md` aprobado por ti, y el feature introduce UI nueva o cambios visuales que el cliente quiere validar.

Si no, detente y termina la Fase 1 primero.

### Diferencia de path según pipeline

El prototipo vive en distintas rutas según el pipeline:

| Pipeline | Carpeta del prototipo |
|---|---|
| Greenfield / brownfield-rewrite | `docs/prototype/` |
| Mantenimiento | `docs/features/<slug>/prototype/` |

El agente `prototipador-visual` detecta automáticamente cuál usar leyendo qué `requirements.md` está aprobado. Si dudas, pasa el path explícitamente en la invocación.

### ¿Cuándo usarla?

| Tu situación | ¿Invocar prototipo? |
|---|---|
| Proyecto con UI, cliente no-técnico que necesita "ver para creer" | **Sí** |
| Proyecto con UI, pero el flujo es tan simple que con requirements queda claro | Probablemente no |
| Backend puro, CLI, librería sin frontend | **No** |

La regla práctica: si sospechas que el cliente va a decir "no, así no" cuando vea la UI final, vale la pena invertir en esta fase. Es 100x más barato cambiar un HTML throwaway que código de producción.

### Paso 1: Prepara el material (opcional pero recomendado)

Crea la carpeta `docs/prototype/context/` y mete lo que tengas:

- `branding.md` — colores, tipografía, tono de marca del cliente.
- `logos/` — archivos de marca (PNG, SVG).
- `referencias/` — screenshots de competidores, inspiración visual, pantallas existentes.

Si no tienes nada de esto, no pasa nada. El agente genera con placeholders genéricos en la primera iteración (colores neutros, logo `[LOGO]` en cuadro gris, tipografía del sistema). El branding se incorpora en iteraciones posteriores.

### Paso 2: Invoca el agente

En Claude Code:

```
Use the prototipador-visual subagent to produce docs/prototype/
```

### Paso 3: Qué esperar (iteración 1)

| Fase del agente | Qué hace | Tu trabajo |
|---|---|---|
| **1. Lectura** | Lee `requirements.md`, `context/` y `CONSTITUTION.md` (si existe). Reporta: cantidad de requirements, pantallas inferidas, estado del branding, plataforma de despliegue. | Confirmar que su lectura es correcta. |
| **2. Plataforma** | Te pregunta dónde desplegar (Railway default, Netlify, Vercel, Cloudflare Pages, GitHub Pages, manual). Solo pregunta si no está en `CONSTITUTION.md`. | Elegir con un número. |
| **3. Inventario de pantallas** | Lista las pantallas que va a generar, para qué Requirement aplica cada una, y qué interacciones serán simuladas vs. estáticas. | Aprobar el plan o ajustar. |
| **4. Generación** | Genera `docs/prototype/` completo: HTML + Tailwind CDN, banner permanente "MOCKUP NO FUNCIONAL", datos falsos, `server.js` con basic auth, `DEPLOY.md`, y `validation-log-v1.md` vacío. | Revisar los archivos generados. |
| **5. Auto-validación** | Ejecuta checklist del SKILL ítem por ítem. Reporta ✅ o ❌. | Esperar 100% ✅. |
| **6. Cierre** | Te dice que despliegues manualmente con las instrucciones de `DEPLOY.md`. | Desplegar, mostrar al cliente. |

**Importante**: el agente **NO** hace `git push` ni despliega por su cuenta. Tú controlas qué se publica. Si quieres que él haga push, díselo explícitamente en la sesión.

### Paso 4: Despliegue (tú lo haces)

Sigue las instrucciones de `docs/prototype/DEPLOY.md`. El flujo típico con Railway:

1. **Setup (una vez)**: crear proyecto en Railway, conectar repo, configurar root directory `docs/prototype/`, poner env vars `AUTH_USER` y `AUTH_PASS`.
2. **Redeploy (cada iteración)**:
   ```bash
   git add docs/prototype/
   git commit -m "prototype v1"
   git push
   ```
   Railway redespliega automáticamente.

### Paso 5: El loop iterativo con el cliente

Este es el flujo que se repite hasta que el cliente apruebe:

1. **Le muestras al cliente** la URL desplegada con las credenciales.
2. **El cliente da feedback** (verbal, por Slack, Loom, lo que sea).
3. **Tú transcribes** el feedback en `docs/prototype/validation-log-v1.md`:
   - **Cambios cosméticos** → lo que el agente puede iterar en HTML (color, posición, texto).
   - **Cambios estructurales** → cosas que implican requirements nuevos (rol nuevo, entidad nueva, flujo nuevo).
   - **Preguntas sin resolver** → dudas que quedaron abiertas.
   - **Decisión**: marcas si está aprobado, si necesita otra iteración, o si hay que volver al analista.
4. **Invocas al agente de nuevo**:
   ```
   Use the prototipador-visual subagent to iterate on docs/prototype/
   based on validation-log-v1.md
   ```
5. El agente genera v2, tú despliegas, muestras, transcribes, repites.

### Cambios estructurales: la válvula de retorno

Si el cliente pide algo que no está en requirements (un actor nuevo, una entidad nueva, un flujo completo nuevo, una integración externa), **el agente se detiene**. No intenta resolverlo en HTML — eso rompería la trazabilidad EARS.

El flujo es:

1. El agente te avisa: *"Esto es un cambio estructural, necesita pasar por `analista-entrevistas`."*
2. Tú invocas al `analista-entrevistas` para actualizar `requirements.md`.
3. Apruebas el requirements actualizado (gate humano normal).
4. Vuelves a invocar al `prototipador-visual` con el contexto enriquecido.

### Paso 6: Cuándo cerrar el loop

Cuando el cliente aprueba explícitamente:

1. En el último `validation-log-v{N}.md`, marca `Status: APROBADO` con fecha.
2. Commit final con tag `prototype-approved-v{N}`.

**Sin esa aprobación explícita, no avances a Fase 2 (design).**

### Paso 7: Cómo validar antes de mostrar al cliente

Antes de cada despliegue, verifica:

- [ ] Todas las pantallas tienen el banner fijo amarillo "MOCKUP NO FUNCIONAL" (no removible).
- [ ] Los datos visibles son obviamente falsos ("Cliente Demo", "$1,234.56", "usuario@ejemplo.com").
- [ ] El HTML usa solo Tailwind CDN + JS vanilla — no hay React, Vue ni nada con build.
- [ ] `DEPLOY.md` tiene instrucciones claras y NO contiene credenciales reales.
- [ ] Los clicks navegan entre pantallas pero no ejecutan lógica de negocio real.
- [ ] Si hubo cambios estructurales, se canalizaron al `analista-entrevistas` antes de iterar.

### Heurísticas importantes

- **Iteración 1 no necesita branding**. Valida estructura y flujo, no pulido visual.
- **Si llegas a la iteración 4-5** y el cliente sigue pidiendo cambios estructurales, el problema está en `requirements.md`. Vuelve al analista para una pasada completa.
- **El prototipo NO decide el stack**. Que esté en HTML+Tailwind no significa que el sistema final lo será. Eso lo decide `design.md`.
- **El prototipo es throwaway**. No se reutiliza como código de producción.

Si el cliente aprobó el prototipo, di explícitamente **"aprobado, sigue con design"** y pasa a la Fase 2.

---

## 7. Fase 2: Diseño técnico

> Esta fase usa **distinto agente según pipeline**. Asegúrate de invocar el correcto.

| Pipeline | Subagente | Output |
|---|---|---|
| Greenfield / brownfield-rewrite | `disenador-arquitecto` | `docs/design.md` |
| Mantenimiento | `disenador-delta-mantenimiento` | `docs/features/<slug>/design.md` |

### Pre-requisito

- **Greenfield / brownfield-rewrite**: `docs/requirements.md` aprobado por ti.
- **Mantenimiento**: `docs/features/<slug>/requirements.md` aprobado por ti.

Si no, detente y termina la Fase 1 primero.

### Paso 1: (opcional pero recomendado) Crea un `CONSTITUTION.md`

Antes de invocar al diseñador, si tienes decisiones técnicas estándar del proyecto o del cliente (stack obligatorio, patrones, librerías vetadas), créa un archivo `CONSTITUTION.md` en la raíz con esas decisiones inmutables. El agente lo va a leer y respetar.

Ejemplo de `CONSTITUTION.md`:

```markdown
# Constitución del Proyecto

## Stack obligatorio

- Lenguaje: TypeScript 5+
- Frontend: React 18 + Tailwind
- Backend: Node 20+ con Fastify
- BD: PostgreSQL 15+

## Patrones obligatorios

- Repository pattern para acceso a datos
- Servicios sin estado
- Error handling tipado (nunca strings)

## Librerías vetadas

- Moment.js (usar date-fns)
- Lodash (usar funciones nativas o Ramda)
```

Sin `CONSTITUTION.md`, el agente te va a preguntar todas estas cosas en la Fase 2 de su workflow.

### Paso 2: Invoca el agente

**Greenfield / brownfield-rewrite:**

```
Use the disenador-arquitecto subagent to produce docs/design.md
```

**Mantenimiento:**

```
Use the disenador-delta-mantenimiento subagent to produce
docs/features/<slug>/design.md
```

### Paso 3: Qué esperar (construcción — greenfield + brownfield-rewrite)

| Fase del agente            | Qué hace                                                                                                                     | Tu trabajo                                                                    |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| **1. Lectura**             | Lee `requirements.md` y `CONSTITUTION.md` si existe. Te lista cuántos Requirements detectó y qué decisiones técnicas faltan. | Confirmar el alcance.                                                         |
| **2. Decisiones técnicas** | Te entrega preguntas numeradas sobre stack, persistencia, despliegue, autenticación, integraciones.                          | Responder. Si ya están en `CONSTITUTION.md`, el agente las usa sin preguntar. |
| **3. Generación**          | Genera las **9 secciones del design.md** una por una.                                                                        | Revisar cada sección antes de aprobar la siguiente.                           |
| **4. Trazabilidad**        | Construye la tabla final conectando cada criterio EARS → componente → test.                                                  | Verificar que no haya huecos.                                                 |
| **5. Auto-validación**     | Ejecuta checklist del SKILL.                                                                                                 | Esperar 100% ✅.                                                              |
| **6. Cierre**              | Declara listo.                                                                                                               | Tú apruebas o pides cambios.                                                  |

### Paso 3 (variante): Qué esperar (mantenimiento)

El agente `disenador-delta-mantenimiento` ejecuta **7 fases** internas (similares pero acotadas al delta):

| Fase del agente | Qué hace | Tu trabajo |
|---|---|---|
| **1. Lectura completa** | Lee `requirements.md` del feature, `BIG_PICTURE.md`, `REGLAS_DE_NEGOCIO.md`, `CONSTITUTION.md` si existen, y los componentes listados en Surface of Contact. Reporta stack heredado, patrones detectados, componentes del delta. | Confirmar alcance. |
| **2. Mapeo de invariantes a tests** | Para cada invariante del requirements, identifica si tiene test existente. Las que no tienen test van a Regression Shield. | Validar el mapeo. |
| **3. Decisiones técnicas (solo del delta)** | Preguntas numeradas sobre decisiones NUEVAS del feature. NO te pregunta stack porque está heredado. | Responder. Si una decisión nueva contradice una decisión heredada, el agente te alerta — decides cómo proceder. |
| **4. Generación** | Genera las **9 secciones del design delta** (200-600 líneas, no 300-800). | Revisar sección por sección. La sección 2.2 (Delta Architecture con Mermaid) y la sección 8 (tabla invariantes → tests) son las más críticas. |
| **5. Validación de no-invasión** | Cruza componentes del design contra Surface of Contact del requirements. Si el design propone tocar algo no autorizado, te alerta. | Decidir: actualizar Surface of Contact (vuelta al analista) o quitar del design. |
| **6. Auto-validación** | Checklist del SKILL `sdd-design-delta`. | Esperar 100% ✅. |
| **7. Cierre** | Declara listo. | Tú apruebas o pides cambios. |

### Paso 4: Las 9 secciones que debe tener el design.md

**Construcción** (`docs/design.md`):

1. Overview
2. Architecture (con diagrama Mermaid)
3. Data Model
4. Interface Contracts
5. Technical Decisions (ADRs)
6. Critical Flows (diagramas de secuencia Mermaid)
7. Error & Edge Case Strategy
8. Testing Strategy
9. Traceability (tabla obligatoria)

**Mantenimiento** (`docs/features/<slug>/design.md`) — mismas 9 secciones pero acotadas al delta:

1. Overview del Delta
2. Architecture (2.1 Arquitectura Heredada inmutable + 2.2 Delta Architecture con Mermaid diferenciando nuevo/modificado/existente)
3. Data Model Delta (solo entidades nuevas o modificaciones, ALTER explícito si modifica)
4. Interface Contracts Delta (endpoints nuevos + extensiones a existentes con qué preservan)
5. Technical Decisions (ADRs del delta, prefijo `D001`) + sección "Decisiones heredadas que se mantienen"
6. Critical Flows Afectados + sección "Coexistencia con flujos existentes"
7. Error & Edge Case Strategy del Delta
8. Testing Strategy (delta + tabla obligatoria invariantes → tests de regresión)
9. Traceability (tabla doble: criterios EARS del delta + invariantes preservadas)

### Paso 5: Cómo validar

**Construcción**:

- [ ] Tiene las 9 secciones en orden.
- [ ] Entre 300-800 líneas. Si pasa de 800, el feature es muy grande y hay que partirlo en sub-features.
- [ ] **Cero funciones completas de código** (pseudocódigo está bien, código no).
- [ ] Cada ADR tiene consecuencias positivas Y NEGATIVAS (si no, la decisión no se pensó).
- [ ] Los errores están tipados como enum (`"USER_NOT_FOUND"`), no descritos en prosa.
- [ ] La tabla de Traceability está completa: cada criterio EARS aparece con su componente y su test.

**Mantenimiento** (adicional a lo de construcción):

- [ ] Entre 200-600 líneas (más corto porque es solo delta).
- [ ] La sección 2 tiene 2.1 Arquitectura Heredada Y 2.2 Delta Architecture.
- [ ] El diagrama Mermaid de 2.2 distingue visualmente componentes **nuevos / modificados / existentes** (colores o estilos distintos).
- [ ] Ningún componente del design queda fuera de la Surface of Contact del requirements (no se invade territorio no autorizado).
- [ ] La sección 6 tiene "Coexistencia con flujos existentes" si Surface of Contact tiene filas riesgo medio/alto.
- [ ] ADRs solo para decisiones NUEVAS del delta (prefijo `D001`). Decisiones heredadas se citan, no se redeciden.
- [ ] Sección 8 tiene tabla `Invariante → Test que la valida → ¿Existe hoy?`. Cualquier invariante sin test existente lleva tarea de blindaje en tasks.md.
- [ ] Sección 9 Traceability tiene **doble tabla**: criterios EARS del delta + invariantes preservadas.
- [ ] Cambios en data model son compatibles hacia atrás (NOT NULL con DEFAULT, etc.).

Si todo está, di explícitamente **"aprobado, sigue con tasks"**.

---

## 8. Fase 3: Descomposición en tareas

> Esta fase usa **distinto agente según pipeline**.

| Pipeline | Subagente | Output | Orden |
|---|---|---|---|
| Greenfield / brownfield-rewrite | `descompositor-tareas` | `docs/tasks.md` | Por capa arquitectónica |
| Mantenimiento | `descompositor-riesgo-mantenimiento` | `docs/features/<slug>/tasks.md` | **Por riesgo de regresión** |

### Pre-requisito

- **Construcción**: `docs/design.md` aprobado por ti.
- **Mantenimiento**: `docs/features/<slug>/design.md` aprobado por ti.

### Paso 1: Invoca el agente

**Construcción:**

```
Use the descompositor-tareas subagent to produce docs/tasks.md
```

**Mantenimiento:**

```
Use the descompositor-riesgo-mantenimiento subagent to produce
docs/features/<slug>/tasks.md
```

### Paso 2: Qué esperar (construcción)

El agente:

1. Lee `design.md` y `requirements.md` completos.
2. Te lista cuántas tareas estima generar (aproximado).
3. Mapea cada criterio EARS a tarea(s) tentativa(s).
4. Genera el `tasks.md` por **capas arquitectónicas**: Setup → Data Model → Data Access → Business Logic → API → UI → Integration Tests → Documentation.
5. Cada tarea tiene checkbox, número, verbo concreto, sub-pasos, criterio de hecho, y footer `_Requirements: X.Y_`.
6. Hace una pasada de podado (quita redundantes, parte las grandes, promueve tests a tareas independientes).
7. Auto-valida.

### Paso 2 (variante): Qué esperar (mantenimiento)

El agente `descompositor-riesgo-mantenimiento`:

1. Lee `design.md` delta y `requirements.md` delta completos.
2. Mapea estructura de tests existentes (con Glob/Read).
3. Te lista cantidad estimada de tareas, cuántas invariantes a blindar, cuántos puntos de integración aislados.
4. Genera el `tasks.md` con **estructura por riesgo**:
   - **Regression Shield** (PRIMERO): verificar suite existente + `Blindar` invariantes sin test
   - Spike (opcional)
   - Data Model Delta (si aplica)
   - Backend Delta
   - API Delta
   - Frontend Delta (si aplica)
   - **Integration** (una tarea aislada por punto de coexistencia)
   - Integration Tests (E2E del feature)
   - **No-Regression Validation** (ÚLTIMO): suite completa + verificar todas las invariantes
   - Documentation
5. Cada tarea con footer **doble**: `_Requirements: X.Y_ | _Invariants: I.A_`.
6. Hace pasada de podado y auto-valida.

### Paso 3: Cómo validar

**Construcción**:

- [ ] El archivo está organizado por capas (no por feature).
- [ ] Cada tarea tiene los 5 elementos: checkbox + número + verbo + sub-pasos + criterio de hecho + footer.
- [ ] Tareas son chiquitas (1-3 archivos, 50-200 líneas estimadas).
- [ ] Tests están como tareas independientes, **no como sub-pasos**.
- [ ] Cada criterio EARS del requirements.md aparece referenciado en al menos una tarea.
- [ ] Hay al menos una tarea de tests E2E al final.

**Mantenimiento** (adicional):

- [ ] La primera sección es `## Regression Shield`. Tiene al menos: tarea 1 = ejecutar suite existente + una tarea `Blindar` por cada invariante sin test.
- [ ] Las tareas con verbo `Blindar` van ANTES de las tareas que modifican el módulo correspondiente.
- [ ] Cada tarea tiene footer doble: `_Requirements: X.Y_ | _Invariants: I.A_` (al menos uno con referencia, no ambos `-`).
- [ ] Las tareas de `Modificar` declaran explícitamente QUÉ preservar (referencia a la invariante correspondiente).
- [ ] Sección `## Integration` tiene **una tarea aislada por cada punto de coexistencia** (cada fila de Surface of Contact con riesgo medio/alto). NO se agrupan.
- [ ] La última sección es `## No-Regression Validation` con una tarea final de verbo `Verificar regresión` que cubre **TODAS** las invariantes.
- [ ] Cada invariante del requirements aparece referenciada en al menos una tarea.
- [ ] Cada criterio EARS del delta aparece referenciado en al menos una tarea de implementación.

### Recomendación importante

**Dale una hora a podar tasks.md tú misma** antes de empezar a ejecutar. Esa hora te ahorra cinco horas de errores durante el desarrollo. Busca:

- Tareas demasiado grandes que el agente no partió → pártelas.
- Tareas redundantes "por completitud" → quítalas.
- Tests escondidos como sub-pasos → promuévelos a tarea.
- (Mantenimiento) Tareas de integración agrupadas → sepáralas, una por punto de coexistencia.
- (Mantenimiento) Tareas de modificación sin invariante a preservar → revisa si te falta el blindaje correspondiente en Regression Shield.

---

## 9. Fase 4: Ejecución del código

Aquí ya no usas los subagentes del framework. Usas Claude Code directamente con sus capacidades estándar, **una tarea a la vez**.

### El patrón correcto (no hay otro)

Para cada tarea pendiente en `tasks.md`:

1. Abre una **conversación nueva** en Claude Code.
2. Dale contexto mínimo y enfocado:

   ```
   Quiero que ejecutes la tarea N de docs/tasks.md.

   Contexto relevante:
   - docs/requirements.md (criterios EARS: X.Y, X.Z)
   - docs/design.md (sección 3 Data Model y sección 4 Interface Contracts)

   Lee primero, luego ejecuta solo esa tarea.
   ```

3. El agente ejecuta SOLO esa tarea.
4. **Tú revisas el resultado**: el código, los tests, que cumpla el criterio de hecho de la tarea.
5. Itera dentro de esa conversación hasta que esté bien.
6. Marca `[x]` en `tasks.md`.
7. Cierra la conversación.
8. Conversación nueva para la siguiente tarea.

### El anti-patrón fatal

❌ "Lee tasks.md y ejecuta todo".

Rompe siempre, sin excepción. Razones:

- Pérdida de contexto a la mitad → decisiones inconsistentes entre tareas.
- Errores se propagan sin revisión humana.
- Imposibilidad de hacer rollback granular si algo sale mal.
- El agente marca tareas como completas con código que no funciona.

**Una tarea = una sesión = una revisión humana = un `[x]`.** Sin atajos.

### Cuándo terminaste el feature

**Construcción** — cuando se cumplen LAS TRES condiciones:

- Todas las tareas en `tasks.md` están en `[x]`.
- Todos los tests pasan.
- La tabla de Traceability del `design.md` está cubierta end-to-end.

**Mantenimiento** — cuando se cumplen LAS CINCO condiciones:

- Todas las tareas en `tasks.md` están en `[x]`.
- La suite **completa** de tests del repo pasa (no solo los nuevos del feature).
- **Cada invariante** del `requirements.md` se verificó manualmente y sigue cumpliéndose.
- La tabla de Traceability cubre criterios EARS del delta E invariantes preservadas.
- La tarea final `Verificar regresión` (sección No-Regression Validation) está en `[x]`.

**Sin No-Regression Validation, NO se cierra el feature. Es no negociable.**

### Consideraciones específicas de mantenimiento durante ejecución

1. **Antes de empezar la tarea 1 del Regression Shield**: confirma que el repo está limpio (sin cambios sin commit) y que la suite completa de tests del repo pasa en verde. Si no, **detente** — el sistema está roto independientemente del feature.

2. **Las tareas `Blindar` van antes de las tareas de modificación de su módulo**. Esto es por diseño. No las saltes "para ir más rápido".

3. **Después de cada tarea de `Modificar`**: corre los tests del módulo modificado (no toda la suite todavía, solo los del módulo) y verifica que los tests de blindaje correspondientes siguen pasando. Solo entonces marca `[x]`.

4. **Las tareas de Integration son aisladas**. Una por sesión, como cualquier otra. NO las agrupes en "voy a hacer todas las integraciones de un jalón".

5. **La tarea final `Verificar regresión`** es la más importante de todo el feature. Tómate el tiempo:
   - Corre TODA la suite del repo (ej. `mvn test`, `npm test`, `pytest`, según el stack).
   - Para cada invariante de `requirements.md`, verifica **manualmente** que el comportamiento referenciado sigue siendo idéntico.
   - Si algo falla, no marques `[x]`. Detente, investiga, repara. Solo cierras cuando todo está verde.

---

## 10. Reglas de oro durante el uso

Pega esto en una nota o en un comentario al inicio de tu sesión:

### Generales (los tres pipelines)

1. **Una fase a la vez. Un gate humano entre cada una.** No avances con dudas.
2. **No le dejes al agente rellenar huecos.** Si pregunta, responde. Mejor 10 preguntas hoy que 100 bugs mañana.
3. **Tú revisas, no el agente.** La auto-validación del agente es el piso, no el techo. Tu revisión humana es la que decide.
4. **Una tarea = una sesión.** Nunca "ejecuta todo".
5. **Si una regla del SKILL no te encaja, el caso probablemente no es para SDD.** No inventes excepciones — las reglas son absolutas a propósito.
6. **Versiona todo.** `requirements.md`, `design.md`, `tasks.md` viven en git. Cambios después de aprobar = commit nuevo, no edición silenciosa.

### Adicionales para mantenimiento

7. **Antes del primer feature, corre `onboarding` y `reglas-negocio`** (skills auxiliares incluidas en el framework). Generan el sustrato `CLAUDE.md` + `BIG_PICTURE.md` + `REGLAS_DE_NEGOCIO.md`. Sin sustrato, el análisis pierde mucha calidad.
8. **Surface of Contact e Invariantes Preservadas son el contrato del feature.** Si las apruebas sin leer línea por línea, no te quejes después de regresiones.
9. **Regression Shield primero, sin excepción.** Los tests de blindaje van antes que el código nuevo. Saltarlos garantiza regresiones.
10. **No-Regression Validation no es opcional.** La última tarea del tasks.md es obligatoria. "Se ve bien" no es validación — correr la suite + verificar invariantes manualmente sí.
11. **Si el feature requiere cambiar arquitectura, sal del pipeline.** Eso ya no es mantenimiento. Decide: rewrite del módulo afectado, reducir scope, o aceptar el cambio con ADR especial.

---

## 11. Troubleshooting

### "Los subagentes no aparecen al ejecutar `/agents`"

Posibles causas:

- **Path incorrecto**: la carpeta `.claude/agents/` debe estar en la **raíz del repo** donde abres Claude Code, no anidada.
- **Frontmatter roto**: abre cada `.md` de los agentes y verifica que el YAML al inicio (entre `---` y `---`) esté bien formado. Errores comunes: comillas mal cerradas, indentación inconsistente.
- **Nombres con mismatch**: el campo `name:` dentro del YAML debe coincidir con el nombre del archivo (sin la extensión `.md`). Si renombraste un archivo, también renombra el `name:`.
- **Versión de Claude Code muy vieja**: actualiza con `claude update`.

### "El agente no aplica las reglas del SKILL"

Posibles causas:

- **Tu versión de Claude Code no soporta el campo `skills:` en subagents** (feature relativamente reciente).
- **Solución rápida**: edita el system prompt del subagente y agrega al inicio del cuerpo: `Antes de cualquier acción, lee .claude/skills/<nombre>/SKILL.md y aplica sus reglas estrictamente.`
- **Path incorrecto**: el SKILL debe estar en `.claude/skills/<nombre>/SKILL.md` (carpeta con el mismo nombre que el `name:` del SKILL).

### "El agente quiere inventar en lugar de preguntar"

Esto pasa cuando:

- El system prompt no se cargó bien (verifica el frontmatter del subagente).
- El modelo configurado es muy chico (los subagentes están en `model: opus` por defecto — si cambiaste a `sonnet` o `haiku`, vuelve a Opus).
- El material que cargaste en `docs/inputs/` es muy parco — si tienes poco contexto, el agente tiene poco con qué identificar huecos.

**Mitigación inmediata**: dile explícitamente "no rellenes huecos, hazme preguntas numeradas sobre cualquier ambigüedad".

### "El requirements.md me quedó enorme (100+ Requirements)"

El feature es demasiado grande. Pártelo:

- Identifica subdominios funcionales (ej. "autenticación", "cálculo de impuestos", "exportación de reportes").
- Crea un repo o sub-feature por cada uno, con su propio `requirements.md / design.md / tasks.md`.
- Documenta las dependencias entre sub-features en un archivo raíz.

Heurística: si tu requirements.md pasa de 30-40 Requirements, ya es demasiado para un solo ciclo.

### "Hay contradicciones entre requirements y design"

Probablemente cambiaron requirements después de aprobar design (o viceversa) y no se sincronizó. Solución:

- Vuelve a la fase que cambió primero.
- Vuelve a ejecutar la siguiente fase con el cambio.
- No edites manualmente design.md sin volver a validar contra requirements.md.

**Anti-patrón**: tratar de "remendar" el design.md a mano para que cuadre con el nuevo requirement. Casi siempre rompe la trazabilidad.

### "El agente marca una tarea como `[x]` pero el código no funciona"

Esto es el modo de falla más común de SDD. Causas:

- La tarea no tenía "Criterio de hecho" suficientemente concreto.
- El agente se auto-validó optimista (los agentes implementadores siempre son optimistas sobre su trabajo).

**Mitigación**:

- Antes de marcar `[x]`, corre tú los tests específicos de la tarea.
- Verifica manualmente que se cumple el criterio EARS referenciado en el footer.
- Si vas a aceptar `[x]` solo por la declaración del agente, mínimo lee el diff completo del código que generó.

**Solución estructural**: en el siguiente ciclo, considera meter un **subagente verificador independiente** (no incluido en este framework v1) que revise el output con goal opuesto: encontrar fallas, no completar.

### "El agente entró en loop preguntándome cosas que ya respondí"

Pasa cuando:

- Cerraste y reabriste Claude Code (perdió contexto de la sesión).
- La conversación se volvió muy larga (>50 turns) y el agente está perdiendo coherencia.

**Solución**:

- Termina lo que estés haciendo con un buen estado del archivo (`requirements.md` guardado).
- Abre conversación nueva.
- Invoca al subagente diciéndole: "lee `docs/requirements.md` actual y continúa desde el Requirement N en adelante".

### Mantenimiento

#### "El agente `analista-feature-mantenimiento` me dice que el feature requiere cambiar arquitectura"

Esto NO es un bug — es por diseño. El agente detectó que tu feature **no se puede meter sin tocar arquitectura existente** (ej. cambiar el stack, reemplazar un módulo entero, romper compatibilidad hacia atrás).

Opciones:

1. **Reescritura previa del módulo afectado**: salir del pipeline de mantenimiento, hacer un ciclo SDD completo de `brownfield-rewrite` para ese módulo, después volver a mantenimiento para el feature.
2. **Reducir el scope del feature**: limitar lo que el feature hace para evitar el cambio arquitectónico.
3. **Aceptar el cambio arquitectónico** y documentarlo con un ADR especial en el design.md delta marcado como **alerta crítica**.

El framework no decide por ti — te obliga a hacer la decisión explícita.

#### "El requirements.md de mantenimiento me quedó documentando todo el sistema en vez del delta"

Pasa cuando:

- El `intent.md` está demasiado vago y el agente intenta inferir todo del código.
- Falta el sustrato (`CLAUDE.md`, `BIG_PICTURE.md`) y el agente intenta reconstruirlo.

**Solución**:

- Mejora el `intent.md`: agrega más contexto sobre QUÉ específicamente cambia y QUÉ NO.
- Si falta sustrato, **pausa y corre `onboarding` y `reglas-negocio`** antes de continuar.
- Vuelve a invocar al agente diciendo: "el scope es solo el delta — Surface of Contact ≤ N módulos, no documentar el sistema completo".

#### "Las invariantes que detectó el agente son demasiado vagas"

Pasa cuando:

- El sustrato `REGLAS_DE_NEGOCIO.md` no existe o está incompleto.
- El código tiene comportamientos críticos sin tests que los documenten.

**Solución**:

- Pídele al agente que **referencie código** para cada invariante (`<!-- source: archivo:líneas -->`). Sin fuente, no es invariante.
- Si una invariante no se puede traducir a un test concreto, descártala — no era invariante real, era deseo.
- Si descubres comportamientos críticos sin test durante este análisis, ese gap se llena con tareas de `Blindar` en el tasks.md. Es valioso descubrirlo aquí, no en producción.

#### "El design delta me propone tocar cosas fuera de Surface of Contact"

El agente debería detectarlo en su Fase 5 (Validación de no-invasión), pero si se le escapó:

**Solución**:

- Vuelve al humano: ¿el componente extra **sí** se debería tocar (entonces actualizar Surface of Contact del requirements — válvula de retorno al analista) o **no** se debería tocar (entonces quitar del design)?
- NO permitas que el design crezca silenciosamente. Cada componente fuera de Surface of Contact es un riesgo no autorizado.

#### "El tasks.md me ordenó por capas en vez de por riesgo"

El agente correcto para mantenimiento es `descompositor-riesgo-mantenimiento`, NO `descompositor-tareas`. Si invocaste el equivocado, el output sale en formato de construcción (Setup → Data Model → ...) en vez de riesgo (Regression Shield → ... → No-Regression Validation).

**Solución**:

- Borra el `tasks.md` generado.
- Vuelve a invocar con `descompositor-riesgo-mantenimiento`.
- Verifica que el agente detecta el contexto de mantenimiento (lee Surface of Contact + Invariantes del requirements).

#### "Tarea de modificación marca `[x]` pero el módulo modificado tiene tests rotos"

Esto significa que **el agente codificador rompió código existente sin que tú lo notaras**. Es exactamente lo que mantenimiento debe prevenir.

**Solución estructural**:

- Antes de marcar `[x]` en cualquier tarea de `Modificar`, **siempre** ejecuta los tests del módulo modificado.
- Si el agente declara "tests pasan" sin haberlos corrido, **no le creas**. Verifica tú.
- Si descubres regresión tarde, **revierte el commit de esa tarea** y vuelve a hacerla con más cuidado (probablemente faltaba un test de blindaje que no se escribió).

#### "Corrí No-Regression Validation y descubrí que una invariante se rompió"

**No cierres el feature**. Detente y diagnostica:

1. ¿Qué tarea(s) tocaron el módulo donde se rompió la invariante?
2. ¿Esas tareas tenían footer `_Invariants: I.X_` correctamente?
3. ¿Existía un test de blindaje (`Blindar I.X`) que debió detectar el problema antes? ¿pasó cuando se escribió?
4. Si el test de blindaje sigue verde pero la invariante está rota → el test estaba mal escrito. Corrige el test, después corrige el código.
5. Si el test de blindaje está roto → el código rompió lo que el blindaje protegía. Corrige el código.

El gate final está ahí para atrapar exactamente esto. Si saltó la alarma, hizo su trabajo. Ahora el tuyo es resolverlo antes de cerrar.

---

## 12. Glosario rápido

### Conceptos generales

- **SDD** (Spec-Driven Development, Desarrollo Dirigido por Especificaciones): metodología donde las specs son el artefacto primario y el código se genera a partir de ellas.
- **EARS** (Easy Approach to Requirements Syntax): notación formal para escribir criterios de aceptación. Usa palabras clave fijas: `THE SYSTEM SHALL`, `WHEN`, `WHILE`, `WHERE`, `IF/THEN`.
- **User Story (Historia de Usuario)**: descripción corta de una necesidad en formato "Como [rol], quiero [acción], para [objetivo]".
- **Acceptance Criteria (Criterios de Aceptación)**: condiciones testeables que definen "está hecho". En SDD se escriben en EARS.
- **ADR** (Architecture Decision Record): registro corto de una decisión técnica con su contexto, consecuencias positivas y negativas.
- **Quality Gate**: punto de revisión humana obligatoria entre fases. No es opcional.
- **Trazabilidad**: capacidad de rastrear cada línea de código → tarea → componente del design → criterio EARS → historia de usuario.
- **Subagente**: instancia de Claude con system prompt propio, herramientas propias, identidad propia. Cada uno hace un trabajo específico.
- **Skill**: archivo `SKILL.md` con reglas y procedimientos que un subagente consulta. Es la "constitución" compartida.
- **CONSTITUTION.md**: archivo opcional con principios inmutables de un proyecto (stack obligatorio, patrones, vetos).
- **Vibe-coding**: pedirle código a la IA conversacionalmente sin estructura. Funciona para prototipos, rompe para producción.

### Pipelines

- **Greenfield**: proyecto desde cero. No hay código previo. Pipeline con `analista-entrevistas` → `disenador-arquitecto` → `descompositor-tareas`.
- **Brownfield-rewrite**: sistema legacy existente que se va a **reescribir** o modernizar arquitectura completa. Pipeline con `arqueologo-codigo` → `disenador-arquitecto` → `descompositor-tareas`.
- **Mantenimiento**: sistema en **producción** al que se le agrega un feature nuevo **sin romper** lo que ya funciona. Stack y arquitectura están dados. Pipeline con `analista-feature-mantenimiento` → `disenador-delta-mantenimiento` → `descompositor-riesgo-mantenimiento`.

### Conceptos específicos de mantenimiento

- **Delta**: el conjunto de cambios que un feature de mantenimiento introduce. Los artefactos del pipeline de mantenimiento describen **solo el delta**, no el sistema completo.
- **Surface of Contact**: tabla en el `requirements.md` de mantenimiento que lista exhaustivamente los módulos, archivos, endpoints, tablas que el feature toca, lee, modifica o explícitamente NO toca. Cada fila con nivel de riesgo (alto / medio / bajo).
- **Invariantes Preservadas**: lista numerada (`I.1`, `I.2`, ...) de comportamientos del sistema existente que NO deben cambiar tras el feature. Cada una con referencia al código fuente (`<!-- source: archivo:líneas -->`) y un test (existente o de blindaje) que la valida.
- **Sustrato (de mantenimiento)**: los tres archivos `docs/CLAUDE.md`, `docs/BIG_PICTURE.md` y `docs/REGLAS_DE_NEGOCIO.md` que documentan el sistema existente. Generados por las skills auxiliares `onboarding` y `reglas-negocio` (incluidas en `.claude/skills/`). Recomendados pero no obligatorios.
- **Intent.md**: archivo de entrada del pipeline de mantenimiento. Lo escribe el humano describiendo el feature en lenguaje de negocio. Vive en `docs/features/<slug>/intent.md`.
- **Regression Shield**: primera sección del `tasks.md` de mantenimiento. Tareas de blindaje (verbo `Blindar`) que escriben tests de regresión sobre código existente que el feature va a tocar. Se ejecutan ANTES de cualquier modificación.
- **No-Regression Validation**: última sección obligatoria del `tasks.md` de mantenimiento. Tarea de verbo `Verificar regresión` que corre suite completa + verifica cada invariante manualmente antes de cerrar el feature.
- **Trazabilidad doble**: cada tarea del `tasks.md` de mantenimiento lleva footer `_Requirements: X.Y_ | _Invariants: I.A_`, conectando tanto criterios EARS del delta como invariantes preservadas.
- **Blindar**: verbo nuevo de tareas en pipeline de mantenimiento. Significa "escribir un test de regresión sobre código existente para asegurar que su comportamiento actual se preserve durante el feature".
- **Coexistencia**: estrategia de cómo el delta convive con flujos existentes sin alterarlos. Documentada en sección 6 del `design.md` delta cuando hay puntos de Surface of Contact con riesgo medio/alto.
- **Válvula de retorno (mantenimiento)**: cuando el design propone tocar algo fuera de Surface of Contact, volver al analista para actualizar el requirements antes de seguir.

### Skills auxiliares del framework (usadas como sustrato del pipeline de mantenimiento)

- **onboarding** (skill): protocolo de reconocimiento para proyectos heredados. Genera `CLAUDE.md` (guía del repo) y `BIG_PICTURE.md` (radiografía arquitectónica). Recomendada antes del primer feature de mantenimiento sobre un sistema. Vive en `.claude/skills/onboarding/`.
- **reglas-negocio** (skill): extrae roles, permisos, flujos de estados, validaciones, mapa funcional del código existente. Genera `docs/REGLAS_DE_NEGOCIO.md`. Recomendada antes del primer feature de mantenimiento. Vive en `.claude/skills/reglas-negocio/`.

Aunque son del framework SDD, son **agnósticas al pipeline SDD per se** — sirven para analizar cualquier repo, no solo proyectos que usen SDD. El pipeline de mantenimiento las usa porque su output es exactamente el sustrato que el agente `analista-feature-mantenimiento` necesita.

---

## Cierre

Este manual cubre el uso normal. Para el "por qué" detrás de cada decisión del framework, lee [`SDD.md`](./SDD.md).

Si encuentras algo que no está aquí o que te trabó, agrega una nota al archivo `LEARNINGS.md` en la raíz del repo. Los frameworks se afinan con uso, no con diseño aislado.

**Buena suerte. Y recuerda: una fase a la vez, una tarea por sesión, tú apruebas.**
