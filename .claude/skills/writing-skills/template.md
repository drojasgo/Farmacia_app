---
# Renombra este archivo a SKILL.md dentro de .claude/skills/<nombre-carpeta>/
# El nombre de la carpeta ES el comando (/nombre-carpeta). Usa kebab-case.

# Único campo realmente recomendado. Tercera persona, caso de uso principal primero,
# incluye frases disparadoras. Se trunca a 1.536 caracteres en el listado.
description: >-
  <Qué hace la skill en una frase.> Úsala cuando <disparador 1>, <disparador 2> o
  <el usuario pida ...>.

# --- Opcionales: descomenta lo que necesites ---

# name: <etiqueta-de-display>            # en skills de proyecto el comando igual sale de la carpeta
# when_to_use: "frases de ejemplo que diría el usuario; cuenta para el límite de 1.536"
# argument-hint: "[nombre-tabla]"
# arguments: [entidad, formato]          # habilita $entidad y $formato en el cuerpo
# disable-model-invocation: true         # solo el usuario la invoca (workflows con efectos)
# user-invocable: false                  # solo Claude la invoca (conocimiento de fondo)
# allowed-tools: Read, Grep, Bash(git status)
# model: inherit
# context: fork                          # ejecutar en subagente aparte
# paths: "db/**, backend/alembic/**"     # autocarga solo al tocar estos archivos
---

# <Título de la skill>

## Cuándo aplica

<1-2 frases. Cuándo es relevante y cuándo NO.>

## Contexto en vivo (opcional — inyección dinámica)

<!-- La siguiente línea se sustituye por la salida del comando antes de que Claude lea la skill -->
!`git status --short`

## Pasos / instrucciones

1. <Di QUÉ hacer, no narres el porqué.>
2. <...>
3. <...>

## Notas del proyecto (D'asaro)

- Identificadores y textos en español; snake_case en BD.
- Datos de salud o pagos → Ley 1581/2012 y PCI-DSS (ver `CLAUDE.md`).

## Recursos adicionales (opcional)

- Detalle extenso → [reference.md](reference.md)
- Ejemplos → [examples.md](examples.md)
