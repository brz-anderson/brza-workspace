# O que é só deste workspace

O `brza init` escreveu este arquivo uma vez, e o `brza sync` nunca o toca: é do `brza-workspace`, e é
daqui que o `AGENTS.md` e o `CLAUDE.md` mandam ler o que não vale para todo workspace. O Claude Code o carrega no
arranque, junto do `CLAUDE.md`, porque `.claude/rules/*.md` sem `paths` entra no contexto.

## Os plugins e os servidores MCP

- **Para todos os workstreams**, no `.claude/settings.json`: o `context7`. Não há `.mcp.json`, nem servidor MCP próprio.
- **Para um workstream só**, no `.claude/settings.local.json` do worktree dele, fora do git: o `skill-creator`, no
  `workspace`. **No `playground`, o `skill-creator` está no `.claude/settings.json` da branch**, versionado, por pedido
  de Anderson em 2026-11-08: toda skill desse workstream se cria e se revisa por ele.

Plugin e servidor novo entram aqui, com o escopo, no mesmo commit que os habilita.

## Os testes que o `reviewer` roda aqui

Além do que o papel manda, a revisão de mudança no `brza` roda os `unittest` dos scripts locais, em
`scripts/brza/tests/`, e os do `brza-workflow`, em `~/Projects/brza-workflow/tests/` (`cli`, `hooks` e
`notes-checker`).

## As notas de outro workspace

Nota, plano ou decisão que mora em outro workspace fica lá, e daqui se cita sem link, sem o nome do workspace e sem o
ID da nota: o ID de lá colide com o daqui, e o `refs` o contaria. Descreva a nota pelo assunto. O mesmo vale para quem
aponta uma nota de lá como origem.

## A suíte completa do `brza-studio` só roda na CI do GitHub

**Na máquina, só o alvo:** os testes dos arquivos tocados e dos vizinhos, por caminho, com `--maxWorkers=2` —
`pnpm test <arquivo> --maxWorkers=2` ou `pnpm test:changed <caminho> --maxWorkers=2`. Nada de `pnpm test` sem
caminho nem `vitest run` sem filtro: a suíte abre um worker por núcleo, e um só `pnpm test` ocupou 3,5 GB em 15
processos `bun.exe` em 2026-11-11, travando a máquina para as outras sessões.

**A suíte completa vai ao `node-next-compat.yml`**, que roda a suíte unitária em `ubuntu-24.04` do GitHub, todo dia na
`master` e sob demanda em qualquer branch ou tag, em cerca de 15 min:

```bash
git push origin <branch>
gh workflow run node-next-compat.yml -R brz-anderson/brza-studio --ref <branch>
```

- **O `pr.yml` não serve:** só dispara em PR, e o push do `brza-studio` vai direto à `master`.
- **A linha de base do sync** é a mesma rodada na tag pura do upstream: `git push origin <tag>` antes, porque o fork
  não traz as tags dele. O vermelho se compara arquivo a arquivo.
- **A evidência** diz o que rodou na máquina e traz o link da rodada da CI, do `gh run list -w node-next-compat.yml`.
