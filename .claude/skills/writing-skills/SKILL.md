---
name: writing-skills
description: >-
  Guía para crear una skill de Claude Code en este repo
  (.claude/skills/<nombre>/SKILL.md): estructura de carpeta, campos de frontmatter,
  cómo redactar la description, progressive disclosure y cómo probarla. Úsala cuando
  alguien pida crear, escribir, diseñar o revisar una skill o slash command, o
  pregunte cómo funcionan las skills.
---

# Escribir una skill

## 1. ¿Skill, CLAUDE.md o subagente?

- **Skill** — un procedimiento, checklist o material de referencia que se repite. El
  cuerpo carga solo cuando se usa, así que texto largo casi no cuesta hasta que hace
  falta.
- **CLAUDE.md** — hechos que deben estar SIEMPRE presentes (stack, convenciones,
  restricciones del proyecto). Si una sección de `CLAUDE.md` se convirtió en un
  procedimiento, pásala a una skill.
- **Subagente** (`.claude/agents/`) — trabajo que conviene aislar en su propio
  contexto y que devuelve un resultado (revisión, investigación, diseño).

## 2. Crear la skill

```bash
mkdir -p .claude/skills/<nombre>/
```

- El **nombre de la carpeta es el comando**: `.claude/skills/deploy/` → `/deploy`.
  Usa kebab-case (minúsculas y guiones).
- Escribe `SKILL.md` con frontmatter YAML entre `---` y el cuerpo en markdown debajo.
- El `---` de apertura debe ser la primera línea del archivo, si no, Claude Code trata
  todo el archivo como contenido.
- Claude Code detecta cambios en `.claude/skills/` en caliente (sin reiniciar). Si
  creas la carpeta `.claude/skills/` por primera vez, reinicia.

## 3. La `description` (lo que más importa)

Claude decide si carga la skill leyendo la `description`. Reglas:

- **Tercera persona**, describe qué hace y cuándo usarla.
- **Caso de uso principal primero**: el listado trunca `description` + `when_to_use` a
  1.536 caracteres.
- Incluye **disparadores**: "Úsala cuando…", frases de ejemplo, palabras clave que el
  usuario diría.
- Concreta: "Revisa migraciones de Postgres antes de aplicarlas", no "ayuda con la
  base de datos".

## 4. El cuerpo: conciso

Una vez cargada, la skill **permanece en contexto entre turnos**: cada línea es un
coste recurrente de tokens.

- Di *qué* hacer, no narres *cómo* ni *por qué*.
- Objetivo: **< 500 líneas**. Si crece, mueve el detalle a archivos aparte
  (`reference.md`, `examples.md`) y enlázalos desde `SKILL.md`.
- Mismo criterio de concisión que para `CLAUDE.md`.

## 5. Frontmatter frecuente

Solo `description` es realmente recomendable. Los demás son opcionales.

| Campo | Para qué |
| --- | --- |
| `name` | Etiqueta en los listados (en skills de proyecto el comando sigue saliendo del nombre de la carpeta). |
| `description` | Qué hace y cuándo usarla. |
| `when_to_use` | Disparadores extra; se añade a `description` (mismo límite de 1.536). |
| `argument-hint` | Pista de autocompletado, p. ej. `[nombre-tabla]`. |
| `arguments` | Argumentos posicionales con nombre para sustituir `$nombre` en el cuerpo. |
| `disable-model-invocation: true` | Solo el usuario la invoca. Para workflows con efectos: `/deploy`, `/commit`, `/send-*`. |
| `user-invocable: false` | Solo Claude la invoca. Para conocimiento de fondo que no es una acción. |
| `allowed-tools` | Herramientas preaprobadas mientras la skill está activa (se limpia en el siguiente mensaje). |
| `model` | Modelo mientras la skill está activa, o `inherit`. |
| `context: fork` | Ejecuta la skill en un subagente aparte. |
| `paths` | Globs; Claude solo la autocarga al trabajar con archivos que casen. |

Tabla completa y reglas de nombres → [reference.md](reference.md).

## 6. Inyección dinámica de contexto (solo Claude Code)

- `` !`comando` `` — ejecuta el comando y mete su salida en la skill antes de que
  Claude la lea (p. ej. `` !`git diff HEAD` ``).
- `@ruta/archivo` — adjunta el archivo.
- `$ARGUMENTS`, `$0` / `$1`, `$nombre` — argumentos de la invocación.
- `${CLAUDE_PROJECT_DIR}`, `${CLAUDE_SKILL_DIR}`, `${CLAUDE_SESSION_ID}` — rutas y datos
  de sesión.

Detalle y ejemplos → [reference.md](reference.md).

## 7. Probar

- Invócala directa: `/<nombre>`.
- O escribe una frase que dispare su `description` y comprueba que Claude la carga.
- Valida el frontmatter: `claude plugin validate .claude/skills/`.

## 8. Checklist D'asaro

- Identificadores y textos en **español**, snake_case en lo que toque BD.
- Si la skill maneja **datos de salud** (encuesta nutricional, perfil) o **pagos**:
  recuerda Ley 1581/2012 (Habeas Data, cifrado en reposo) y PCI-DSS (nunca datos de
  tarjeta; pagos vía Wompi/PayU). Ver `CLAUDE.md`.
- Skills y subagentes van en `farmacia_app/.claude/` (dentro del repo, se comparten).

## 9. Plantilla

Copia [template.md](template.md) como punto de partida y renómbralo a `SKILL.md`
dentro de la carpeta de tu skill.
