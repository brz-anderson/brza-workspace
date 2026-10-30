# brza-workspace

O workspace pessoal de Anderson para o **BrzA Studio** (`~/Projects/brza-studio`, o fork do Orca que antes se chamava
`orca-dev`): os planos, o registro do que foi feito e as decisões ficam aqui, e o código fica no `brza-studio`.

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
# Conferir as notas antes de commitar
python3 .claude/skills/notes-checker/scripts/check_notes.py

# Testar os hooks de medição
python3 -m unittest discover -s .claude/hooks/tests

# Resumir a medição de .measurements/measurements.jsonl
python3 scripts/summarize_measurements.py
```

A norma de agente está no [`AGENTS.md`](AGENTS.md), e o adaptador do Claude Code no [`CLAUDE.md`](CLAUDE.md). O commit
é com o `brz-anderson`, pelo `env` do `.claude/settings.json`, e o push vai direto na `master`, pela chave `personal`.

## Funções do shell

O `.claude/settings.json` daqui não é herdado pelo `brza-studio`, que fica ao lado deste repositório. Este bloco do
`~/.zshrc` passa a configuração às sessões abertas nos dois. Se ele mudar, mude aqui e copie para lá. A `fixfy_claude`
é a função do workspace da Fixfy, que atende o resto.

```zsh
# Workspace BrzA: o bloco de "Funções do shell", no README.md do brza-workspace. Mude lá e copie para cá.
BRZA_WORKSPACE="$HOME/Projects/brza-workspace"
BRZA_STUDIO="$HOME/Projects/brza-studio"

# "yes" quando o cwd está no brza-workspace ou no brza-studio (worktrees inclusive), nada fora. Caminho físico e sem
# maiúsculas, como o fixfy_where.
brza_where() {
  local here root
  here=$(pwd -P | tr '[:upper:]' '[:lower:]')
  for root in "$BRZA_WORKSPACE" "$BRZA_STUDIO"; do
    root=$(cd "$root" 2>/dev/null && pwd -P | tr '[:upper:]' '[:lower:]') || continue
    case "$here/" in "$root"/*) echo yes; return ;; esac
  done
}

# Claude Code no BrzA: o --settings do brza-workspace (hooks de medição e a identidade do brz-anderson) e a raiz
# para os hooks; o gh fica no perfil padrão.
brza_claude() {
  BRZA_WORKSPACE="$BRZA_WORKSPACE" command claude --settings "$BRZA_WORKSPACE/.claude/settings.json" "$@"
}

claude()     { if [ -n "$(brza_where)" ]; then brza_claude "$@"; else fixfy_claude "$@"; fi; }
adm-claude() { CLAUDE_CONFIG_DIR="$HOME/.claude-adm" claude "$@"; }
claude-adm() { adm-claude "$@"; }
```
