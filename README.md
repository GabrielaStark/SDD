# SDD — Skills independientes

Nueve skills para especificar, comprender, diseñar y planificar software con evidencia y revisión humana. Cada carpeta contiene su procedimiento, referencias, plantillas y licencia; puede distribuirse por separado sin instalar el framework completo.

## Catálogo

| Skill | Entrada | Entrega |
|---|---|---|
| [onboarding](.claude/skills/onboarding/SKILL.md) | Código existente | Mapa técnico y guía del proyecto |
| [reglas-negocio](.claude/skills/reglas-negocio/SKILL.md) | Código existente | Reglas implementadas con evidencia y confianza |
| [sdd-requirements](.claude/skills/sdd-requirements/SKILL.md) | Entrevistas, notas o legacy | Requisitos verificables para construir o reescribir |
| [sdd-design](.claude/skills/sdd-design/SKILL.md) | Requisitos aprobados | Diseño técnico y trazabilidad |
| [sdd-tasks](.claude/skills/sdd-tasks/SKILL.md) | Requisitos y diseño aprobados | Plan de tareas por dependencias |
| [sdd-requirements-mantenimiento](.claude/skills/sdd-requirements-mantenimiento/SKILL.md) | Petición de cambio y código | Delta, superficie de contacto e invariantes |
| [sdd-design-delta](.claude/skills/sdd-design-delta/SKILL.md) | Requisitos del delta y código | Diseño del cambio y mitigaciones de regresión |
| [sdd-tasks-risk](.claude/skills/sdd-tasks-risk/SKILL.md) | Requisitos y diseño del delta | Blindaje, cambios y validación final |
| [sdd-prototype](.claude/skills/sdd-prototype/SKILL.md) | Requisitos aprobados y feedback | Mockup estático y registro de validación |

**Independiente no significa sin entradas:** una skill de diseño requiere requisitos aprobados, pero pueden estar escritos a mano o con cualquier herramienta. No exige instalar la skill que genera requisitos. Los documentos opcionales de contexto tampoco son prerrequisitos.

## Usar una sola skill

Copiar la carpeta completa elegida —no solo SKILL.md— a la ubicación de skills que admita el agente. Para un proyecto con Claude Code, esa ubicación es `.claude/skills/`; este repositorio ya conserva esa disposición. Para otros clientes, usar su mecanismo de instalación y probarlo antes de anunciar compatibilidad.

Ejemplos de petición:

- «Extrae las reglas de negocio de este repositorio usando reglas-negocio. Cita evidencia y distingue inferencias».
- «Usa sdd-design con estos requisitos aprobados. El stack está definido en el documento adjunto».
- «Planifica este cambio con sdd-tasks-risk. Estos requisitos y este diseño están aprobados; todavía no ejecutes tareas».

Se necesita acceso de lectura a las entradas. La escritura de archivos depende del agente; sin ella se entrega el contenido y se informa que no se guardó. Solo el servidor opcional del prototipo requiere Node.js. No se fija proveedor de modelo.

## Construir y validar paquetes

Requisito del empaquetador: Python 3.10+; solo biblioteca estándar.

```sh
python scripts/skills.py validate
python -m unittest discover -s tests -v
python scripts/skills.py package --skill reglas-negocio
python scripts/skills.py package
```

El último comando genera un ZIP por skill y `dist/manifest.json` con SHA-256, versión y archivos. Los ZIP son reproducibles y contienen una carpeta raíz con nombre de skill. El empaquetador verifica que enlaces y recursos permanezcan dentro de cada paquete. Dist es un resultado local, no se versiona.

Para actualizar las copias históricas de `templates/` después de editar los assets canónicos:

```sh
python scripts/skills.py sync-templates
```

Ver [publicación y verificación en Agensi](docs/documentacion/PUBLICACION.md) y [decisiones de la adaptación](docs/documentacion/SKILLS-INDEPENDIENTES.md).

## Colecciones opcionales

- **Legacy Discovery:** onboarding + reglas-negocio.
- **SDD Core:** requirements + design + tasks.
- **SDD Maintenance:** requirements-mantenimiento + design-delta + tasks-risk.
- **SDD Prototype:** validación visual independiente.

Las colecciones son agrupaciones comerciales/documentales; cada paquete sigue siendo independiente. Las aprobaciones humanas siguen presentes entre fases cuando se encadenan. Los gates son instrucciones al agente, no un sistema de autorización impuesto por software.

## Compatibilidad con el framework anterior

Los ocho archivos de `.claude/agents/` son adaptadores opcionales para Claude Code que cargan la skill correspondiente. No contienen una segunda copia del procedimiento ni fuerzan Opus. Los nombres de skills permanecen estables. `templates/` mantiene copias de compatibilidad verificadas por el validador; los originales para distribuir viven en los assets de cada skill.

Los manuales anteriores están marcados como históricos. Onboarding usa por defecto `docs/CLAUDE.md` y `docs/BIG_PICTURE.md`; también reconoce documentos existentes en raíz. El primero es una referencia técnica, no una instalación automática de instrucciones. El prototipo ahora sirve solo `public/`; migrar prototipos previos con revisión explícita, conservando documentos y contexto fuera de esa carpeta.

## Autoría y licencia

Creado por Gabriela Carmona / [iamgabstark_](https://github.com/GabrielaStark), en el contexto de Gema. Mantiene prácticas de Spec-Driven Development adaptadas al trabajo con agentes. [Licencia MIT](LICENSE), incluida en cada paquete. Publicar en un marketplace no demuestra por sí solo compatibilidad con todos los agentes ni garantiza resultados de negocio.
