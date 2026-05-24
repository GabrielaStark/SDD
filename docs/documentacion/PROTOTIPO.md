# Fase de Prototipo — Decisiones de Diseño

> ADR que congela las decisiones de la fase opcional de prototipado visual entre `requirements.md` y `design.md`. Esta es la fuente de verdad sobre el **porqué** del agente `prototipador-visual` y el skill `sdd-prototype`. Si los artefactos divergen de este doc, este doc manda hasta que se actualice.

---

## Índice

1. [Propósito](#1-propósito)
2. [Posición en el pipeline](#2-posición-en-el-pipeline)
3. [Decisiones congeladas](#3-decisiones-congeladas)
4. [Estructura del artefacto `docs/prototype/`](#4-estructura-del-artefacto-docsprototype)
5. [Política de despliegue](#5-política-de-despliegue)
6. [Loop iterativo con el cliente](#6-loop-iterativo-con-el-cliente)
7. [Válvula de retorno al analista](#7-válvula-de-retorno-al-analista)
8. [Anti-patrones](#8-anti-patrones)

---

## 1. Propósito

`requirements.md` es texto. El cliente lee texto y asiente. Después ve la UI y dice "no, así no". Esa brecha entre texto aprobado y mental model real es **el problema que esta fase resuelve**.

La fase de prototipo introduce un **mockup interactivo de alta fidelidad** entre `requirements.md` aprobado y `design.md`, desplegado en una URL real que se le muestra al cliente. El cliente valida o pide ajustes; los cambios se reflejan **primero en `requirements.md`** y luego en una nueva iteración del prototipo. Cuando el cliente está convencido, el pipeline continúa hacia `design.md`.

**Lo que la fase NO es**:

- No es código de producción
- No es la decisión de stack (eso sigue siendo de `design.md`)
- No es un wireframe baja-fidelidad (Figma a mano, boxes y líneas)
- No es un prototipo funcional con backend real (los botones no guardan datos)

**Lo que la fase SÍ es**:

- Validación temprana del **qué visual** y del **flujo** con el cliente
- Mecanismo para detectar requisitos faltantes antes de cementarlos en diseño
- Artefacto throwaway, versionado, reemplazable

---

## 2. Posición en el pipeline

```
inputs/ o analysis/
        ↓
[analista | arqueologo] → docs/requirements.md → [gate humano]
        ↓
        ↓  ← ─ ─ ─ válvula de retorno ─ ─ ─ ┐
        ↓                                    │
[prototipador-visual] (opcional)             │
   ↓                                         │
   loop: prototipo ⇄ validation-log ─ ─ ─ ─ ┘
   ↓ (puede actualizar requirements.md)
   ↓
   docs/prototype/ desplegado → [gate cliente: aprobación]
        ↓
[disenador-arquitecto] → docs/design.md → [gate humano]
        ↓
[descompositor-tareas] → docs/tasks.md  → [gate humano]
        ↓
   tarea por sesión → código + tests
```

**Opcionalidad**: la fase se ejecuta solo si el proyecto tiene UI relevante. Backend puro, CLIs y librerías la saltan sin culpa.

**Gate adicional**: el cliente aprueba la versión final del prototipo antes de pasar a `design.md`. Es un gate humano más, no un gate técnico — sigue la disciplina del framework.

---

## 3. Decisiones congeladas

Cada decisión en formato breve: **Decisión · Por qué · Consecuencias negativas aceptadas**.

### D1. Fase opcional, no obligatoria

- **Decisión**: la fase se invoca explícitamente cuando el proyecto tiene UI relevante. No se ejecuta automáticamente al cerrar `requirements.md`.
- **Por qué**: no todos los proyectos son UI-driven. Forzar prototipo en un servicio backend infla el pipeline sin valor.
- **Consecuencia aceptada**: requiere criterio humano para decidir si invocarla. No hay flag automático.

### D2. Agente separado, no sub-paso del analista

- **Decisión**: `prototipador-visual` es un agente nuevo en `.claude/agents/`, con su propio skill `sdd-prototype`.
- **Por qué**: las responsabilidades son distintas. El analista consolida texto; el prototipador genera HTML. Mezclarlas viola el principio de "un agente, un trabajo bien definido".
- **Consecuencia aceptada**: un archivo más en `.claude/agents/` y uno más en `.claude/skills/`.

### D3. Stack del prototipo: HTML estático + Tailwind CDN

- **Decisión**: HTML + Tailwind por CDN + JS vanilla o Alpine.js para interacciones mínimas. Sin build, sin frameworks, sin dependencias instaladas.
- **Por qué**: (1) throwaway por naturaleza — nadie confunde HTML con CDN con código de producción; (2) stack-agnóstico — no contamina la decisión de framework que se toma en `design.md`; (3) cero fricción de setup.
- **Consecuencia aceptada**: techo visual más bajo que v0/Lovable/Figma. Para validación de flujo alcanza; para portafolio de diseñador, no.

### D4. Despliegue default: Railway

- **Decisión**: Railway como plataforma default. Server mínimo de Node con `express` + `express-basic-auth` sirviendo la carpeta estática. Credenciales por env vars (`AUTH_USER`, `AUTH_PASS`).
- **Por qué**: el dev ya conoce y usa Railway. Basic auth resuelve privacidad de prototipos con info sensible. Setup en dashboard una vez, redeploy automático con `git push`.
- **Consecuencia aceptada**: dependencia de cuenta Railway. Se mitiga ofreciendo alternativas (ver §5).

### D5. Despliegue configurable

- **Decisión**: Railway es default pero el dev puede elegir Netlify, Vercel, Cloudflare Pages, GitHub Pages o despliegue manual. La elección se declara en `CONSTITUTION.md` (si existe) o el agente la pregunta una vez.
- **Por qué**: el framework es de uso genérico. Imponer Railway sería rígido y elimina valor para devs que ya tienen su stack de despliegue.
- **Consecuencia aceptada**: el agente debe mantener instrucciones de `DEPLOY.md` para ~5 plataformas. Manejable.

### D6. El agente NO hace push ni deploy

- **Decisión**: el agente genera los archivos y un `DEPLOY.md` con instrucciones, pero **nunca hace `git add`, `git commit`, `git push` ni `railway up`** por su cuenta. El humano despliega manualmente.
- **Por qué**: consistente con la filosofía de gates humanos del framework. Mantiene el control de qué se publica al cliente en manos del humano.
- **Excepción explícita**: si el humano le pide *"haz push"* en una sesión, el agente puede hacerlo en esa invocación específica.
- **Consecuencia aceptada**: un paso manual extra por iteración. Es barato y mantiene la disciplina.

### D7. Banner permanente "MOCKUP NO FUNCIONAL"

- **Decisión**: todo prototipo incluye un banner fijo, visible en todas las pantallas, con texto similar a *"MOCKUP NO FUNCIONAL — solo para validación de requisitos. Ningún botón guarda datos reales."*. Datos en pantalla son obviamente falsos (Lorem, "Cliente Demo", etc.).
- **Por qué**: evita el síndrome "esto ya está casi listo" del cliente. Salvaguarda barata contra que el prototipo se vuelva spec de facto.
- **Consecuencia aceptada**: estética degradada por el banner. Cliente serio entiende; ese es el punto.

### D8. Cambios cosméticos vs cambios estructurales

- **Decisión**: el prototipador puede iterar libremente sobre cambios cosméticos. Si detecta que el feedback del cliente implica un **cambio estructural** (nueva entidad, nuevo actor, nuevo flujo completo, requisito faltante), se detiene y devuelve al `analista-entrevistas`. Ver §7.
- **Por qué**: si el prototipo intenta "absorber" requisitos nuevos sin actualizar `requirements.md`, rompe la trazabilidad EARS — corazón del framework.
- **Consecuencia aceptada**: latencia mayor en algunos casos (volver al analista antes de continuar el loop). Es el precio de no contaminar la fuente de verdad.

### D9. `validation-log` lo llena el dev, no el cliente

- **Decisión**: el archivo `validation-log-vN.md` lo escribe el dev del framework con transcripción/notas de las observaciones del cliente. No se asume que el cliente edite Markdown ni que tenga acceso a GitHub.
- **Por qué**: el 90% de los clientes no usan git. Pretender lo contrario es planificar para falla.
- **Consecuencia aceptada**: paso manual de transcripción por iteración. Aceptable.

### D10. Loop iterativo con commit por iteración

- **Decisión**: cada iteración del prototipo es un commit separado (`prototype v1`, `v2`, `v3`) con su propio `validation-log-v1.md`, `v2.md`, etc.
- **Por qué**: historial real de qué cambió y por qué entre iteraciones. Útil cuando el cliente dice "pero esto antes estaba así".
- **Consecuencia aceptada**: más commits en el repo. Trivial.

### D11. Sin branding → placeholders genéricos

- **Decisión**: si en la iteración 1 no hay branding/logos disponibles, el agente genera con placeholders genéricos (colores neutros, tipografía system, logo `[LOGO]` en cuadro gris). Lo anota en `validation-log-v1.md`.
- **Por qué**: bloquearse en la iteración 1 esperando assets visuales es contraproducente. La iteración 1 es de estructura y flujo, no de pulido visual.
- **Consecuencia aceptada**: primera versión visualmente cruda. El loop se encarga.

### D12. Terminología: "mockup interactivo" / "maqueta clickable"

- **Decisión**: el agente y todos los artefactos usan los términos **mockup interactivo** o **maqueta clickable**. NUNCA "prototipo funcional".
- **Por qué**: precisión técnica. Un prototipo funcional implica backend real y lógica funcional, que no es lo que producimos. Mockup interactivo = visual de alta fidelidad con clicks que cambian pantallas pero sin lógica de negocio real.
- **Consecuencia aceptada**: hay que educar a clientes que esperan "prototipo" en el sentido genérico. El banner lo deja claro.

### D13. El prototipo NO decide el stack final

- **Decisión**: el HTML+Tailwind del prototipo es throwaway. `design.md` decide el stack real (React, Vue, Svelte, HTMX, Astro, etc.) sin estar atado al lenguaje del prototipo.
- **Por qué**: la decisión de stack vive en `design.md` con sus ADRs. Pre-comprometerla en el prototipo viola la disciplina del framework.
- **Consecuencia aceptada**: posible fricción social si el cliente ve el HTML y asume "esto será React". El agente debe ser explícito en el `DEPLOY.md` y en la presentación: "el visual final puede diferir; lo que se valida es el flujo, no el código".

---

## 4. Estructura del artefacto `docs/prototype/`

```
docs/prototype/
├── index.html                    # mockup principal, banner permanente
├── pantallas/                    # otras pantallas si el flujo lo requiere
│   ├── login.html
│   ├── dashboard.html
│   └── ...
├── assets/                       # imágenes, logos (placeholders si no hay branding)
│   └── ...
├── context/                      # INPUT: brief de branding, notas del cliente
│   ├── branding.md               # colores, tipografía, tono (puede estar vacío)
│   ├── logos/                    # archivos de marca si existen
│   └── referencias/              # screenshots inspiracionales si existen
├── server.js                     # express + basic auth (default: Railway)
├── package.json                  # "start": "node server.js"
├── validation-log-v1.md          # observaciones del cliente sobre v1
├── validation-log-v2.md          # observaciones sobre v2 (si existe)
├── ...
└── DEPLOY.md                     # instrucciones de despliegue (default Railway + alternativas)
```

**Reglas**:

- `context/` es **input**: lo llena el dev antes de invocar al agente con material que tenga.
- `validation-log-vN.md` es **input al agente para la iteración N+1**: lo llena el dev tras mostrar la versión N al cliente.
- Todo lo demás es **output** del agente.

---

## 5. Política de despliegue

### Default: Railway

**Setup (una sola vez, en dashboard de Railway)**:

1. Crear proyecto, conectar repo de GitHub
2. Root directory: `docs/prototype/`
3. Variables de entorno: `AUTH_USER`, `AUTH_PASS`
4. Rama a vigilar (default: la rama activa del proyecto)

**Redeploy (cada iteración)**:

1. `git add docs/prototype/`
2. `git commit -m "prototype vN"`
3. `git push`
4. Railway detecta y redespliega automáticamente

### Alternativas soportadas (el agente las documenta en `DEPLOY.md`)

| Plataforma | Auth privado | Setup | Notas |
|---|---|---|---|
| **Railway** (default) | Basic auth via `server.js` | Dashboard one-time | Recomendado para sensible |
| **Netlify** | Drag & drop o git connect | Cuenta gratis | Basic auth solo en plan pago |
| **Vercel** | Git connect | Cuenta gratis | Password protection en Pro |
| **Cloudflare Pages** | Cloudflare Access | Dashboard | Free tier generoso |
| **GitHub Pages** | Público por defecto | Settings → Pages | NO para info sensible |
| **Manual** | Lo que el dev decida | — | Agente entrega solo los archivos |

### Cómo se decide la plataforma

- Si existe `CONSTITUTION.md` con `prototype_deploy: <plataforma>` → se usa esa.
- Si no, el agente pregunta una vez en la iteración 1. La elección se anota en `DEPLOY.md` para futuras iteraciones.

---

## 6. Loop iterativo con el cliente

### Flujo de una iteración

1. **Iteración N**: el agente genera/actualiza `docs/prototype/` (incluyendo HTML, assets, `DEPLOY.md`).
2. El humano despliega manualmente (`git push` o `railway up` según plataforma).
3. El humano muestra al cliente la URL desplegada.
4. El cliente da feedback (verbal, Slack, Loom, lo que sea).
5. El humano transcribe feedback en `docs/prototype/validation-log-v{N}.md`.
6. El humano invoca al agente: *"itera al prototipo con base en validation-log-v{N}.md"*.
7. El agente clasifica el feedback (cosmético vs estructural — ver §7) y genera iteración N+1.

### Cuándo cerrar el loop

El loop se cierra cuando el cliente aprueba explícitamente. El humano marca la aprobación así:

- Commit final con tag tipo `prototype-approved-v{N}`
- Última línea en el `validation-log-v{N}.md`: `Status: APROBADO por cliente el YYYY-MM-DD`

Sin esa señal explícita, `disenador-arquitecto` no debe arrancar.

### Sanity check informal

Si en la iteración **3 o 4** el cliente sigue pidiendo cambios estructurales (no cosméticos), eso es señal de que `requirements.md` estaba incompleto o mal levantado. El agente debe sugerir explícitamente al humano: *"Iteración N detectó M cambios estructurales acumulados. Recomendación: volver al analista-entrevistas antes de continuar el loop."*

No es una regla dura — es un alerta que el humano evalúa.

---

## 7. Válvula de retorno al analista

Cuando el feedback del cliente revela algo que **no es un cambio de UI sino un requisito faltante**, el flujo se detiene y vuelve al analista.

### Señales de "esto es estructural, no cosmético"

- Cliente menciona una **entidad nueva** ("ah, y necesito que cada cliente tenga proyectos asociados") — entidad no estaba en `requirements.md`.
- Cliente menciona un **actor nuevo** ("y debería poder loguearse el supervisor también") — actor no estaba contemplado.
- Cliente menciona un **flujo completo nuevo** ("y antes de calcular debe pasar por aprobación de jefe") — flujo no estaba.
- Cliente menciona una **integración con sistema externo** ("y esto debe mandar correos automáticamente"/"...sincronizar con CRM").
- Cliente menciona un **requisito no funcional duro nuevo** ("y debe funcionar offline").

### Qué hace el agente en estos casos

1. Se detiene. NO intenta resolverlo en HTML.
2. Reporta al humano: *"Detecté un cambio estructural en el feedback: [descripción]. Esto no se resuelve en el prototipo, requiere actualizar `requirements.md`. Recomiendo invocar `analista-entrevistas` para añadir el Requirement correspondiente antes de continuar la iteración."*
3. Espera instrucción explícita del humano: (a) volver al analista, o (b) ignorar ese feedback en esta iteración y continuar con el resto.

### Qué hace el `analista-entrevistas` cuando recibe la válvula

El analista debe contemplar este caso de uso secundario: recibir feedback estructural desde el prototipador y actualizar `requirements.md` añadiendo el Requirement nuevo (con su User Story y EARS). Ver actualización en `.claude/agents/analista-entrevistas.md`.

Después de actualizar `requirements.md`, el humano vuelve a invocar al prototipador para la siguiente iteración con el contexto enriquecido.

---

## 8. Anti-patrones

### Del agente

- ❌ Generar código de producción "ya que estamos" (componentes React reales, hooks, estado complejo).
- ❌ Hacer push o deploy sin instrucción explícita.
- ❌ Omitir el banner "MOCKUP NO FUNCIONAL".
- ❌ Inventar datos que parezcan reales (nombres de clientes reales, números coherentes que confundan).
- ❌ Intentar resolver un cambio estructural en HTML en lugar de devolver al analista.
- ❌ Decidir el stack del proyecto en el prototipo (pre-comprometer React/Vue/etc.).
- ❌ Bloquearse en iteración 1 esperando branding.

### Del humano usando el framework

- ❌ Saltarse el gate de aprobación del cliente y arrancar `disenador-arquitecto` con prototipo "casi aprobado".
- ❌ Editar el HTML a mano entre iteraciones (el HTML debe regenerarse desde el agente, no mantenerse a mano).
- ❌ Usar el prototipo como spec en lugar de actualizar `requirements.md` cuando hay cambios reales.
- ❌ Desplegar a GitHub Pages prototipos con info sensible del cliente.
- ❌ Iterar más de 4-5 veces sin replantearse si el problema está en `requirements.md`.

### Del cliente (mitigaciones)

El cliente puede caer en patrones que el agente y el banner mitigan, pero el humano debe estar atento:

- Cliente trata el prototipo como "el sistema casi listo" → el banner lo desinfla, recordar verbalmente que es validación.
- Cliente quiere especificar todo vía screenshots del HTML en lugar de pedir cambios a `requirements.md` → el dev traduce screenshots a cambios formales antes de iterar.

---

## Cierre

Esta fase es una herramienta poderosa para validación temprana, pero solo funciona si se respeta su rol: **es validación visual del qué, no decisión técnica del cómo, ni reemplazo de `requirements.md` o `design.md`**. Si la fase se convierte en "diseñar la app via HTML", se rompió la disciplina del framework.

La frase que el dev debe poder decirle al cliente cuando vea el prototipo:

> *"Esto que ves es para que valides el flujo y el contenido. El sistema final va a verse parecido pero no idéntico, y va a tener funcionalidad real detrás. Si algo te hace ruido aquí, dímelo ahora — es 100 veces más barato cambiarlo ahora que después."*
