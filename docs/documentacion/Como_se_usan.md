# Manual del Framework SDD

> Guía práctica paso a paso. Si ya leíste `SDD.md` (la guía conceptual), este es el "hands-on": cómo se usa en la vida real, qué esperar en cada paso, y qué hacer cuando algo no sale como debería.

---

## Índice

1. [Para qué sirve esto](#1-para-qué-sirve-esto)
2. [Antes de empezar](#2-antes-de-empezar)
3. [Setup del proyecto](#3-setup-del-proyecto)
4. [El pipeline en una imagen](#4-el-pipeline-en-una-imagen)
5. [Fase 1: Levantamiento de requerimientos](#5-fase-1-levantamiento-de-requerimientos)
6. [Fase 2: Diseño técnico](#6-fase-2-diseño-técnico)
7. [Fase 3: Descomposición en tareas](#7-fase-3-descomposición-en-tareas)
8. [Fase 4: Ejecución del código](#8-fase-4-ejecución-del-código)
9. [Reglas de oro durante el uso](#9-reglas-de-oro-durante-el-uso)
10. [Troubleshooting](#10-troubleshooting)
11. [Glosario rápido](#11-glosario-rápido)

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
├── .claude/agents/       (4 archivos .md)
├── .claude/skills/       (3 carpetas con SKILL.md)
├── docs/inputs/          (vacía, con .gitkeep)
├── docs/analysis/        (vacía, con .gitkeep)
├── docs/documentacion/   (SDD.md, MANUAL.md)
└── templates/            (3 archivos .md)
```

### Paso 3: Abrir Claude Code

```bash
claude
```

### Paso 4: Verificar que los subagentes se cargaron

Dentro de Claude Code:

```
/agents
```

Debes ver:

- `analista-entrevistas`
- `arqueologo-codigo`
- `disenador-arquitecto`
- `descompositor-tareas`

**Si NO aparecen los 4**: revisa la sección [Troubleshooting](#10-troubleshooting).

**No avances al pipeline si no aparecen los 4.** Resolver el problema ahorita es 5 minutos; descubrirlo a media fase es perder horas de trabajo.

---

## 4. El pipeline en una imagen

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
                  [✋ TÚ apruebas]
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
                  [✋ TÚ apruebas]
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
                  [✋ TÚ apruebas]
                            │
                            ▼
              [tarea por tarea + revisión humana]
                            │
                            ▼
                  ┌──────────────────────┐
                  │ código + tests       │
                  └──────────────────────┘
```

Los ✋ son **gates humanos obligatorios**. Si saltas uno, te disparas en el pie.

---

## 5. Fase 1: Levantamiento de requerimientos

### Primero decide: ¿greenfield o brownfield?

| Tu situación                                                                                                    | Subagente a usar                                                                                                                                 |
| --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| Vas a construir algo desde cero. Tienes material de descubrimiento (entrevistas, transcripciones, formularios). | `analista-entrevistas`                                                                                                                           |
| Hay un sistema legacy existente que vas a modernizar. Tienes acceso al código + análisis previo.                | `arqueologo-codigo`                                                                                                                              |
| Es mitad y mitad (sistema legacy pero el feature nuevo no existe en él)                                         | Empieza con `arqueologo-codigo` para documentar lo existente, luego `analista-entrevistas` para el feature nuevo. Dos requirements.md separados. |

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

## 6. Fase 2: Diseño técnico

### Pre-requisito

**`docs/requirements.md` aprobado por ti.** Si no, detente y termina la Fase 1 primero.

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

```
Use the disenador-arquitecto subagent to produce docs/design.md
```

### Paso 3: Qué esperar

| Fase del agente            | Qué hace                                                                                                                     | Tu trabajo                                                                    |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| **1. Lectura**             | Lee `requirements.md` y `CONSTITUTION.md` si existe. Te lista cuántos Requirements detectó y qué decisiones técnicas faltan. | Confirmar el alcance.                                                         |
| **2. Decisiones técnicas** | Te entrega preguntas numeradas sobre stack, persistencia, despliegue, autenticación, integraciones.                          | Responder. Si ya están en `CONSTITUTION.md`, el agente las usa sin preguntar. |
| **3. Generación**          | Genera las **9 secciones del design.md** una por una.                                                                        | Revisar cada sección antes de aprobar la siguiente.                           |
| **4. Trazabilidad**        | Construye la tabla final conectando cada criterio EARS → componente → test.                                                  | Verificar que no haya huecos.                                                 |
| **5. Auto-validación**     | Ejecuta checklist del SKILL.                                                                                                 | Esperar 100% ✅.                                                              |
| **6. Cierre**              | Declara listo.                                                                                                               | Tú apruebas o pides cambios.                                                  |

### Paso 4: Las 9 secciones que debe tener el design.md

1. Overview
2. Architecture (con diagrama Mermaid)
3. Data Model
4. Interface Contracts
5. Technical Decisions (ADRs)
6. Critical Flows (diagramas de secuencia Mermaid)
7. Error & Edge Case Strategy
8. Testing Strategy
9. Traceability (tabla obligatoria)

### Paso 5: Cómo validar

- [ ] Tiene las 9 secciones en orden.
- [ ] Entre 300-800 líneas. Si pasa de 800, el feature es muy grande y hay que partirlo en sub-features.
- [ ] **Cero funciones completas de código** (pseudocódigo está bien, código no).
- [ ] Cada ADR tiene consecuencias positivas Y NEGATIVAS (si no, la decisión no se pensó).
- [ ] Los errores están tipados como enum (`"USER_NOT_FOUND"`), no descritos en prosa.
- [ ] La tabla de Traceability está completa: cada criterio EARS aparece con su componente y su test.

Si todo está, di explícitamente **"aprobado, sigue con tasks"**.

---

## 7. Fase 3: Descomposición en tareas

### Pre-requisito

**`docs/design.md` aprobado por ti.**

### Paso 1: Invoca el agente

```
Use the descompositor-tareas subagent to produce docs/tasks.md
```

### Paso 2: Qué esperar

El agente:

1. Lee `design.md` y `requirements.md` completos.
2. Te lista cuántas tareas estima generar (aproximado).
3. Mapea cada criterio EARS a tarea(s) tentativa(s).
4. Genera el `tasks.md` por **capas arquitectónicas**: Setup → Data Model → Data Access → Business Logic → API → UI → Integration Tests → Documentation.
5. Cada tarea tiene checkbox, número, verbo concreto, sub-pasos, criterio de hecho, y footer `_Requirements: X.Y_`.
6. Hace una pasada de podado (quita redundantes, parte las grandes, promueve tests a tareas independientes).
7. Auto-valida.

### Paso 3: Cómo validar

- [ ] El archivo está organizado por capas (no por feature).
- [ ] Cada tarea tiene los 5 elementos: checkbox + número + verbo + sub-pasos + criterio de hecho + footer.
- [ ] Tareas son chiquitas (1-3 archivos, 50-200 líneas estimadas).
- [ ] Tests están como tareas independientes, **no como sub-pasos**.
- [ ] Cada criterio EARS del requirements.md aparece referenciado en al menos una tarea.
- [ ] Hay al menos una tarea de tests E2E al final.

### Recomendación importante

**Dale una hora a podar tasks.md tú misma** antes de empezar a ejecutar. Esa hora te ahorra cinco horas de errores durante el desarrollo. Busca:

- Tareas demasiado grandes que el agente no partió → pártelas.
- Tareas redundantes "por completitud" → quítalas.
- Tests escondidos como sub-pasos → promuévelos a tarea.

---

## 8. Fase 4: Ejecución del código

Aquí ya no usas los 4 subagentes del framework. Usas Claude Code directamente con sus capacidades estándar, **una tarea a la vez**.

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

Cuando se cumplen LAS TRES condiciones:

- Todas las tareas en `tasks.md` están en `[x]`.
- Todos los tests pasan.
- La tabla de Traceability del `design.md` está cubierta end-to-end.

No antes.

---

## 9. Reglas de oro durante el uso

Pega esto en una nota o en un comentario al inicio de tu sesión:

1. **Una fase a la vez. Un gate humano entre cada una.** No avances con dudas.
2. **No le dejes al agente rellenar huecos.** Si pregunta, responde. Mejor 10 preguntas hoy que 100 bugs mañana.
3. **Tú revisas, no el agente.** La auto-validación del agente es el piso, no el techo. Tu revisión humana es la que decide.
4. **Una tarea = una sesión.** Nunca "ejecuta todo".
5. **Si una regla del SKILL no te encaja, el caso probablemente no es para SDD.** No inventes excepciones — las reglas son absolutas a propósito.
6. **Versiona todo.** `requirements.md`, `design.md`, `tasks.md` viven en git. Cambios después de aprobar = commit nuevo, no edición silenciosa.

---

## 10. Troubleshooting

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

---

## 11. Glosario rápido

- **SDD** (Spec-Driven Development, Desarrollo Dirigido por Especificaciones): metodología donde las specs son el artefacto primario y el código se genera a partir de ellas.
- **EARS** (Easy Approach to Requirements Syntax): notación formal para escribir criterios de aceptación. Usa palabras clave fijas: `THE SYSTEM SHALL`, `WHEN`, `WHILE`, `WHERE`, `IF/THEN`.
- **Greenfield**: proyecto desde cero. No hay código previo.
- **Brownfield**: proyecto que parte de un sistema legacy existente que hay que modernizar o reescribir.
- **User Story (Historia de Usuario)**: descripción corta de una necesidad en formato "Como [rol], quiero [acción], para [objetivo]".
- **Acceptance Criteria (Criterios de Aceptación)**: condiciones testeables que definen "está hecho". En SDD se escriben en EARS.
- **ADR** (Architecture Decision Record): registro corto de una decisión técnica con su contexto, consecuencias positivas y negativas.
- **Quality Gate**: punto de revisión humana obligatoria entre fases. No es opcional.
- **Trazabilidad**: capacidad de rastrear cada línea de código → tarea → componente del design → criterio EARS → historia de usuario.
- **Subagente**: instancia de Claude con system prompt propio, herramientas propias, identidad propia. Cada uno hace un trabajo específico.
- **Skill**: archivo `SKILL.md` con reglas y procedimientos que un subagente consulta. Es la "constitución" compartida.
- **CONSTITUTION.md**: archivo opcional con principios inmutables de un proyecto (stack obligatorio, patrones, vetos).
- **Vibe-coding**: pedirle código a la IA conversacionalmente sin estructura. Funciona para prototipos, rompe para producción.

---

## Cierre

Este manual cubre el uso normal. Para el "por qué" detrás de cada decisión del framework, lee [`SDD.md`](./SDD.md).

Si encuentras algo que no está aquí o que te trabó, agrega una nota al archivo `LEARNINGS.md` en la raíz del repo. Los frameworks se afinan con uso, no con diseño aislado.

**Buena suerte. Y recuerda: una fase a la vez, una tarea por sesión, tú apruebas.**
