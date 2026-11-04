---
status: open
description: O `brza sessions` não tem como escolher a conta do Claude; a sessão nova sobe na conta ativa do app, mesmo quando a sessão de origem roda em outra.
scope:
  - workspace
opened: 2026-11-02
priority: low
tags:
  - tooling
---

# O brza sessions abre a sessão na conta ativa do app, e não na da sessão de origem

O `brza sessions` abre a sessão nova no chat do BrzA Studio, e o chat usa a conta do Claude que está ativa no app. A
sessão de origem pode rodar em outra conta, e nada no comando diz isso nem deixa escolher. O `brza sessions --help` lista
`--title`, `--rename`, `--checkout`, `--prompt`, `--prompt-file`, `--wait` e `--dry-run`, e nenhuma opção de conta.

Achado em 2026-11-02, na sessão do `brand`, quando Anderson pediu o conserto da
[issue do brza shot](brza-shot-quebra-com-os-tokens-do-painel-movidos.md) "em sessão própria", na conta de
administração (`~/.claude-adm`). O `brza sessions brza-shot-fix --checkout .worktrees/tools-kit` subiu na conta padrão
(`~/.claude/sessions/77277.json`), e a sessão teve de ser fechada com `--force` antes de commitar.
O que se fez no lugar foi abrir uma aba de terminal no worktree e rodar o `adm-claude`
(`CLAUDE_CONFIG_DIR=~/.claude-adm`), com o `"$ORCA_CLI_COMMAND" terminal create` e `send`. O registro está no
[worklog de 2026-11-02](../worklogs/2026-11-02-pln-007-o-desenho-da-marca-brza.md), na seção "O conserto do brza shot,
em sessão própria".

## O pedido

Fechar o buraco de um dos dois jeitos, ou dos dois. O `brza sessions` mora no pacote `client` do `brza-workflow`, e a
norma dele chega a este workspace pelo `brza sync`; as duas mudanças são lá, e não aqui.

- **Dizer na norma:** uma frase em "O pacote do cliente" (`.claude/rules/brza-client.md` aqui, e a fonte no `core/` do
  `brza-workflow`), com o que `brza sessions` faz — usa a conta ativa do app — e o que fazer quando a sessão tem de
  rodar em outra conta: terminal com o `adm-claude`. Custo: uma frase e um `brza sync`, não medido.
- **Dar a escolha ao comando:** uma opção que passe o `CLAUDE_CONFIG_DIR` à sessão nova, ou um aviso quando a conta ativa
  do app difere da conta da sessão de origem. Custo: código no `client` e teste, não medido; só vale se a conta
  de administração for usada com frequência.

Pelo `AGENTS.md`, o que vale para todos os workstreams sobe à norma. A decisão de qual dos dois é de Anderson.
