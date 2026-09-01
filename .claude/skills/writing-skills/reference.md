# Referencia: frontmatter y sustituciones de skills

Fuente: documentación oficial de Claude Code (Extend Claude with skills). Todos los
campos son opcionales; los booleanos aceptan `true/false`, `yes/no`, `on/off`, `1/0`.
El `---` de apertura debe ser la primera línea del archivo.

## Dónde viven las skills

| Nivel | Ruta | Alcance |
| --- | --- | --- |
| Personal | `~/.claude/skills/<nombre>/SKILL.md` | Todos tus proyectos |
| Proyecto | `.claude/skills/<nombre>/SKILL.md` | Solo este repo (se commitea) |
| Plugin | `<plugin>/skills/<nombre>/SKILL.md` | Donde el plugin esté activo |

Conflictos de nombre: enterprise > personal > proyecto > bundled. En este repo la raíz
es `farmacia_app/`; un `.claude/` por encima de la raíz **no se carga**.

## Cómo se obtiene el nombre del comando

| Ubicación | Origen del comando |
| --- | --- |
| `~/.claude/skills/<dir>/` o `.claude/skills/<dir>/` | Nombre de la carpeta |
| `.claude/commands/<archivo>.md` | Nombre del archivo sin extensión |
| Plugin `skills/<dir>/` | `name` del frontmatter o carpeta, con prefijo `plugin:` |

En skills personales o de proyecto, `name` es **solo la etiqueta de display**; el
comando siempre sale del nombre de la carpeta.

## Tabla completa de frontmatter

| Campo | Req. | Descripción |
| --- | --- | --- |
| `name` | No | Nombre de display en los listados. Por defecto, el nombre de la carpeta. |
| `description` | Recomendado | Qué hace y cuándo usarla. Claude lo usa para decidir si la carga. Si falta, usa el primer párrafo del cuerpo. Se trunca a **1.536 caracteres** junto con `when_to_use`. Pon primero el caso de uso principal. |
| `when_to_use` | No | Contexto extra: frases disparadoras, ejemplos de peticiones. Se añade a `description` y cuenta para el límite de 1.536. |
| `argument-hint` | No | Pista de autocompletado, p. ej. `[issue-number]` o `[filename] [format]`. |
| `arguments` | No | Argumentos posicionales con nombre para `$name`. String separado por espacios o lista YAML; los nombres mapean a posiciones en orden. |
| `disable-model-invocation` | No | `true` evita que Claude la cargue sola. Para workflows manuales (`/commit`, `/deploy`). También la excluye de precargarse en subagentes y de tareas programadas. Default `false`. |
| `user-invocable` | No | `false` la oculta del menú `/` y de invocación por nombre: solo Claude la usa. Para conocimiento de fondo. Default `true`. |
| `allowed-tools` | No | Herramientas que Claude puede usar sin pedir permiso durante el turno que invoca la skill. Se limpia con el siguiente mensaje. String separado por espacios/comas o lista YAML. |
| `disallowed-tools` | No | Herramientas retiradas del pool mientras la skill está activa. Para skills autónomas que nunca deben llamar, p. ej., `AskUserQuestion`. |
| `model` | No | Modelo mientras la skill está activa. Mismos valores que `/model`, o `inherit`. Con `context: fork` fija el modelo del subagente. |
| `effort` | No | Nivel de esfuerzo mientras la skill está activa: `low`, `medium`, `high`, `xhigh`, `max`. |
| `context` | No | `fork` ejecuta la skill en un subagente aparte. |
| `agent` | No | Qué tipo de subagente usar cuando `context: fork`. |
| `background` | No | Solo con `context: fork`. `false` espera el resultado en el mismo turno. Default `true`. |
| `hooks` | No | Hooks que se registran al invocar la skill y siguen el resto de la sesión. |
| `paths` | No | Globs que limitan cuándo se autoactiva. Mismo formato que las reglas por ruta de `memory`. |
| `shell` | No | `bash` (default) o `powershell` para los `` !`comando` `` de la skill. |
| `metadata` | No | Mapa YAML libre para tus propias herramientas. Claude Code no actúa sobre él. |
| `license` | No | Licencia de la skill (spec Agent Skills). |
| `compatibility` | No | Requisitos de entorno (spec Agent Skills). Máx. 500 caracteres. |

## Sustituciones de string en el cuerpo

| Variable | Descripción |
| --- | --- |
| `$ARGUMENTS` | Todos los argumentos tal cual se pasaron. |
| `$ARGUMENTS[N]` / `$N` | Argumento por índice 0-based (`$0`, `$1`, …). Usa comillas para valores con espacios. |
| `$name` | Argumento con nombre declarado en `arguments`. |
| `${CLAUDE_SESSION_ID}` | ID de la sesión actual. |
| `${CLAUDE_EFFORT}` | Nivel de esfuerzo actual. |
| `${CLAUDE_SKILL_DIR}` | Carpeta que contiene el `SKILL.md`. Úsala para referenciar scripts propios de la skill. |
| `${CLAUDE_PROJECT_DIR}` | Raíz del proyecto. |
| `${CLAUDE_PLUGIN_ROOT}` / `${CLAUDE_PLUGIN_DATA}` | Solo en skills de plugin. |

Un placeholder indexado sin argumento (`$2` cuando solo pasaste uno) se queda tal cual.
Un `$name` sin valor se expande a cadena vacía. Para un `$` literal antes de dígito o
`ARGUMENTS`, escápalo: `\$1.00`.

### Inyección dinámica de contexto

- `` !`comando` `` — Claude Code ejecuta el comando y sustituye la línea por su salida
  **antes** de que Claude lea la skill.
- ```` ```! ```` bloque — igual, para comandos multilínea.
- `@ruta` — adjunta el archivo referenciado.

Ejemplo de skill que preaprueba su propio script:

```yaml
---
name: render-chart
description: Renderiza un chart desde un CSV
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/render.sh *)
---

Ejecuta `${CLAUDE_SKILL_DIR}/scripts/render.sh <csv-file>` para renderizar el chart.
```

## Archivos de apoyo (progressive disclosure)

```
mi-skill/
├── SKILL.md        # requerido — visión general y navegación
├── reference.md    # detalle, se carga cuando hace falta
├── examples.md     # ejemplos, se cargan cuando hacen falta
└── scripts/
    └── helper.py   # se ejecuta, no se carga en contexto
```

Referencia cada archivo desde `SKILL.md` para que Claude sepa qué contiene y cuándo
abrirlo. Mantén `SKILL.md` por debajo de 500 líneas.

## Compatibilidad con el spec Agent Skills

Fuera de Claude Code (subida a claude.ai, Skills API, `package_skill.py`) solo son
válidos **6 campos**: `name`, `description`, `license`, `compatibility`, `metadata`,
`allowed-tools`. Incluir cualquier otro hace fallar el empaquetado con error duro. Las
funciones de cuerpo propias de Claude Code (inyección dinámica) no funcionan en
claude.ai chat ni por API.

## Validación

`claude plugin validate .claude/skills/`

Una skill se ignora sin error si no tiene frontmatter válido. `description` ausente usa
el primer párrafo del cuerpo.
