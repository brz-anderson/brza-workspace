# O que é só deste workspace

O `brza init` escreveu este arquivo uma vez, e o `brza sync` nunca o toca: é do `brza-workspace`, e é
daqui que o `AGENTS.md` e o `CLAUDE.md` mandam ler o que não vale para todo workspace. O Claude Code o carrega no
arranque, junto do `CLAUDE.md`, porque `.claude/rules/*.md` sem `paths` entra no contexto.

## Os plugins e os servidores MCP

- **Para todos os workstreams**, no `.claude/settings.json`: o `context7`. Não há `.mcp.json`, nem servidor MCP próprio.
- **Para um workstream só**, no `.claude/settings.local.json` do worktree dele, fora do git: o `skill-creator`, no
  `workspace`.

Plugin e servidor novo entram aqui, com o escopo, no mesmo commit que os habilita.

## Os testes que o `reviewer` roda aqui

Além do que o papel manda, a revisão de mudança no `brza` roda os `unittest` dos scripts locais, em
`scripts/brza/tests/`, e os do `brza-workflow`, em `~/Projects/brza-workflow/tests/` (`cli`, `hooks` e
`notes-checker`).

## As notas de outro workspace

Nota, plano ou decisão que mora em outro workspace fica lá, e daqui se cita sem link, sem o nome do workspace e sem o
ID da nota: o ID de lá colide com o daqui, e o `refs` o contaria. Descreva a nota pelo assunto. O mesmo vale para quem
aponta uma nota de lá como origem.
