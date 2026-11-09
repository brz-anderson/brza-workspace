---
name: reference-pln004-levantar-vizinhos-todas-as-branches
description: Atalhos para levantar, em todas as branches workstream/*, o que toca Codex/agy/Grok e o PLN-004; onde estão os vizinhos e o que envelheceu (2026-11-09)
metadata:
  type: reference
---

- **Índice primeiro:** `python3` sobre `.brza/index.jsonl` da raiz, último registro por `id`, dá 188 notas com workstream/status/phase em 1 chamada; depois
  `git grep -c -iE 'codex|antigravity|\bagy\b|grok|PLN-004|brzAgents|dispatch' workstream/<b> -- plans work/issues work/decisions work/reviews wiki` por branch
  mostra onde o peso está. No zsh, glob em pathspec do `git grep` precisa de aspas (`'plans/PLN-017*'`), e `echo ====` quebra (`=cmd`): use aspas.
- **Vizinhos do PLN-004:** `tools-kit` PLN-013 (feito, base do D11/D12), PLN-009, PLN-012 (dono do `measure.py`), PLN-015, PLN-010; `playground` PLN-017
  (já publicou `brza sessions usage/--model/wait`, skill `meeting-runner` em `.claude/skills/` real); `studio` PLN-011 (bloqueado), issue `codex-como-subagente…`;
  `workspace` issues `fronteira-…-antigravity` e `a-sessao-no-brza-studio-nao-recebe-a-identidade…`.
- **Fontes que envelheceram:** `brza-sessions` mudou muito em 2026-11-09 (`chat_blocker` em `:168`, não `:443`); slugs `*-da-fixfy-*` renomeados para
  `*-do-workspace-de-origem-*` no `tools-kit` (o índice guarda o id velho); o "noreply" do PLN-004 contradiz o `env` da `master` (Gmail, desde 2026-11-03);
  `check_notes.py` dá 0 avisos mesmo quando o plano não tem as seções de ponteiro.
- `grep -c Fixfy` no v3 do scratch dá 12; regra de `.claude/rules/workspace.md` proíbe o nome.
