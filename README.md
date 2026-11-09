<h1>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/brz-anderson/brza-studio/master/resources/brand/brza-workspace-lockup-horizontal-dark.svg" />
    <img src="https://raw.githubusercontent.com/brz-anderson/brza-studio/master/resources/brand/brza-workspace-lockup-horizontal-light.svg" alt="BrzA Workspace" height="48" />
  </picture>
</h1>

O workspace pessoal de Anderson para o **BrzA Studio** (`~/Projects/brza-studio`, o fork do Orca que antes se chamava
`orca-dev`): os planos, o registro do que foi feito e as decisões ficam aqui, e o código fica no `brza-studio`.

As pastas de notas não moram na `master`, que guarda só a norma: cada frente de trabalho é uma branch
`workstream/<nome>`, com worktree em `.worktrees/<nome>`. Os de agora são o `studio` (o app), o `tools-kit` (o `brza`,
os scripts e os plugins), o `workspace` (a própria norma), o `brand` (a identidade visual da marca) e o `playground`
(onde se testam fluxos de trabalho antes de entrarem na norma ou no ferramental) e o `logi-options` (a configuração do
Logi Options+ da Logitech: atalhos e Ring Actions do mouse MX Master 4).

| Pasta | O que guarda |
| :---- | :----------- |
| `plans/` | Os planos, uma pasta por plano (`plans/PLN-001-…/`), com a norma no [`plans/README.md`](plans/README.md) |
| `work/issues/` | Pendência, dívida, bug conhecido e investigação |
| `work/worklogs/` | O registro de cada trabalho feito, um assunto por arquivo |
| `work/decisions/` | A questão e a decisão no mesmo arquivo, de `open` a `done` |
| `work/reviews/` | Parecer sobre um artefato numa versão |
| `work/notes/` | Rascunho do dia, de onde o conteúdo é promovido |
| `wiki/guides/` | Como Anderson usa uma ferramenta, API ou produto |

A norma de escrita das notas está no [`work/README.md`](work/README.md). Os comandos rodam da raiz deste repositório.

```bash
# Conferir as notas antes de commitar, no worktree do workstream
python3 .claude/skills/notes-checker/scripts/check_notes.py

# Levar a norma da master a cada worktree de workstream
brza note sync

# Testar os hooks, o CLI brza e o checador: no checkout do brza-workflow (ao lado deste)
python3 -m unittest discover -s ~/Projects/brza-workflow/tests/hooks

# Testar os scripts locais do brza-studio (app, dev, shot, test, tree)
python3 -m unittest discover -s scripts/brza/tests

# Trazer a norma do brza-workflow e levá-la aos workstreams
brza sync

# Resumir a medição de .measurements/measurements.jsonl
python3 scripts/summarize_measurements.py

# O acerto da confiança dos fatos do designer e do collector
python3 scripts/summarize_measurements.py --facts

# Os fatos a conferir, e o desfecho de um deles
python3 scripts/fact_outcome.py --pending
python3 scripts/fact_outcome.py <agente>:<F3> holds|fails "<porquê>" --ref <PLN-NNN/R…>
```

A norma de agente está no [`AGENTS.md`](AGENTS.md), e o adaptador do Claude Code no [`CLAUDE.md`](CLAUDE.md). O commit
é com o `brz-anderson`, pelo `env` do `.claude/settings.json`, e o push vai pela chave `personal`: a norma à `master`, e
as notas à branch do workstream.

**A chave de acesso e o `gh`.** O `origin` é `git@personal:brz-anderson/brza-workspace.git`, pelo alias `personal` do
`~/.ssh/config` padrão, que o `GIT_SSH_COMMAND` do `env` aponta. O `gh` usa o perfil padrão, com a conta `brz-anderson`
ativa (`gh auth switch`).

## Funções do shell

O `.claude/settings.json` daqui não é herdado pelo `brza-studio`, que fica ao lado deste repositório. Quem acha o
workspace do cwd — pelo `.brza/workspace.toml`, ou, no `brza-studio`, pelo `~/.config/brza/workspaces.toml` — e passa a
configuração às sessões abertas nos dois é o bloco do shell do `brza-workflow`, que **não é copiado para cá**: a fonte
única é o `packages/client/shell/brza.zsh` do checkout do `brza-workflow`.

No `~/.zshrc` desta máquina, ele entra assim, com a função de outro workspace para o que fica fora dos dois:

```zsh
source "$HOME/Projects/brza-workflow/packages/client/shell/brza.zsh"
brza_claude_fallback() { outro_claude "$@"; }  # o nome real da função fica só no ~/.zshrc
adm-claude() { CLAUDE_CONFIG_DIR="$HOME/.claude-adm" claude "$@"; }
claude-adm() { adm-claude "$@"; }
```

O bloco pede o `brza-where` e o `brza-agents` no PATH, que o `brza install --all` do `brza-workflow` liga.
