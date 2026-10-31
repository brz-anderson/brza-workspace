# brza-workspace

O workspace pessoal de Anderson para o **BrzA Studio** (`~/Projects/brza-studio`, o fork do Orca que antes se chamava
`orca-dev`): os planos, o registro do que foi feito e as decisões ficam aqui, e o código fica no `brza-studio`.

As pastas de notas não moram na `master`, que guarda só a norma: cada frente de trabalho é uma branch
`workstream/<nome>`, com worktree em `.worktrees/<nome>`. Os de agora são o `studio` (o app), o `tools-kit` (o `brza`,
os scripts e os plugins) e o `workspace` (a própria norma).

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

# Testar os hooks de medição
python3 -m unittest discover -s .claude/hooks/tests

# Resumir a medição de .measurements/measurements.jsonl
python3 scripts/summarize_measurements.py
```

A norma de agente está no [`AGENTS.md`](AGENTS.md), e o adaptador do Claude Code no [`CLAUDE.md`](CLAUDE.md). O commit
é com o `brz-anderson`, pelo `env` do `.claude/settings.json`, e o push vai pela chave `personal`: a norma à `master`, e
as notas à branch do workstream.

## Funções do shell

O `.claude/settings.json` daqui não é herdado pelo `brza-studio`, que fica ao lado deste repositório. Este bloco do
`~/.zshrc` passa a configuração às sessões abertas nos dois. Se ele mudar, mude aqui e copie para lá. A `fixfy_claude`
é a função do workspace da Fixfy, que atende o resto.

```zsh
# Workspace BrzA: o bloco de "Funções do shell", no README.md do brza-workspace. Mude lá e copie para cá.
BRZA_WORKSPACE="$HOME/Projects/brza-workspace"
BRZA_STUDIO="$HOME/Projects/brza-studio"

# "workspace" ou "studio" quando o cwd está no brza-workspace ou no brza-studio (worktrees inclusive), nada fora.
# Caminho físico e sem maiúsculas, como o fixfy_where.
brza_where() {
  local here root label
  here=$(pwd -P | tr '[:upper:]' '[:lower:]')
  for label in workspace studio; do
    case $label in workspace) root="$BRZA_WORKSPACE" ;; studio) root="$BRZA_STUDIO" ;; esac
    root=$(cd "$root" 2>/dev/null && pwd -P | tr '[:upper:]' '[:lower:]') || continue
    case "$here/" in "$root"/*) echo $label; return ;; esac
  done
}

# Claude Code no BrzA: o --settings do brza-workspace (hooks de medição e a identidade do brz-anderson) e a raiz
# para os hooks; no brza-studio, também o --agents com os subagentes por papel do brza-workspace (brza-agents), se
# houver e se a chamada não trouxer o seu; o gh fica no perfil padrão.
brza_claude() {
  local -a agents=()
  local json
  if [ "$(brza_where)" = studio ] && [[ " $* " != *" --agents"* ]]; then
    json=$(brza-agents 2>/dev/null)
    [ -n "$json" ] && agents=(--agents "$json")
  fi
  BRZA_WORKSPACE="$BRZA_WORKSPACE" command claude --settings "$BRZA_WORKSPACE/.claude/settings.json" "${agents[@]}" "$@"
}

claude()     { if [ -n "$(brza_where)" ]; then brza_claude "$@"; else fixfy_claude "$@"; fi; }
adm-claude() { CLAUDE_CONFIG_DIR="$HOME/.claude-adm" claude "$@"; }
claude-adm() { adm-claude "$@"; }
```
