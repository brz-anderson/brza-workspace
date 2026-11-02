---
name: reference-brza-workflow-depois-da-migracao
description: Onde mora cada peça depois do PLN-006 (BW = ~/Projects/brza-workflow), o que o sync toca, e os atalhos para conferir citações antigas do PLN-004
metadata:
  type: reference
---

Confirmado em 2026-11-02 (confira que os caminhos ainda existem). Vale para levantamento de Codex/agy ou de qualquer citação anterior à migração.

**Onde mora (BW = `~/Projects/brza-workflow`, com `.git`; BZ = worktree do workspace)**
- Núcleo: `BW/core/` (AGENTS.md e CLAUDE.md em molde `{{tabela.chave}}`, skills, papéis, hooks `measure|compact_guard|fact_audit|brza_root`, `scripts/summarize_measurements|fact_outcome`). BZ recebe cópia igual byte a byte (`cmp` basta); `.md` chega renderizado, então `cmp` falha e vale conferir o hash do `.brza/core.lock`.
- CLI: `BW/bin/{brza-note,brza-sync,brza-init,brza-install,brza-agents,brza-where,brza-register,brza_runtime.py}`; cliente: `BW/packages/client/{bin,shell/brza.zsh,core/.claude/rules/brza-client.md}`. Locais do BZ: só `scripts/brza/{brza-app,brza-dev,brza-shot,brza-test,brza-tree}` e `tests/`; `~/.local/bin/brza-{app,dev,shot,test,tree}` apontam ao checkout principal (master).
- `brza sync` só escreve `core/` + `packages/<nome>/core/` (só `.md` renderiza); arquivo fora do núcleo e do lock é ignorado, nunca apagado. `commands()` do install usa o glob `brza-*`: `codex-brza` não casa.
- Testes: `BW/tests/{cli,hooks,notes-checker}`; `test_brza_scripts.py:161` proíbe nome fixo (`brza-workspace`, `def repo_of`) nos scripts genéricos.
- `brza-where`, `brza-agents --help` e `BRZA_WORKSPACE=` vazio rodam sem estado (leitura pura); `brza-install` sem argumento foi NEGADO pelo classificador ("Unauthorized Persistence") mesmo sendo só leitura: leia o código em vez de rodar.
- Fontes velhas: o rascunho/plano do PLN-004 cita `brza_runtime.py`, `claude-brza`, `brza-sessions`, `README.md:53` e `~/.zshrc:57,79-98` pelo layout de antes; `AGENTS.md:207`→`:226`, `:22-23`→`:33-34`. O ST já tinha 3 citações fora de linha antes da migração (`codex-structured-launch-resolution.ts:85-93`, `tui-agent-launch-command.ts:41-46`): o dado certo está em `:94-98,126,131-134` e `:107-112`.

**Atalhos**
- No zsh, `git show $rev:caminho` lê `$rev:c` como modificador: use `${rev}:caminho`.
- Para saber se uma citação do ST "nunca bateu" ou "deslocou": `git rev-list -1 --before=<data do rascunho> HEAD` e `git show ${rev}:arquivo | sed -n a,bp`.
- Branch `workstream/tools-kit`: `git ls-tree -r --name-only` + `git show <b>:<f> | grep -m1 '^status:'` lista issue/plano abertos em um laço; o tools-kit também commita no BW (brza devices).
- `grep -rniE 'codex|antigravity|\bagy\b' BW --exclude-dir=.git --exclude-dir=__pycache__` = 0: nada de Codex/agy em BW.
- `check_notes.py` dá 0/0 mesmo com plano > 400 linhas: a divisão em `-interview.md` (`plans/README.md:15`) não é cobrada pelo checador.

Ver também [[reference-brza-norma-acoplamento-atalhos]] (anterior à migração) e [[reference-codex-agy-sondas-armadilhas]].
