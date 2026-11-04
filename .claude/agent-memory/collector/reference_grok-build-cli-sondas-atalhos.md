---
name: reference-grok-build-cli-sondas-atalhos
description: Como levantar e sondar o Grok Build CLI 1.0.70 (PLN-004) quase de graça: docs locais, grok inspect, env limpo, o que cada sonda custa e as armadilhas
metadata:
  type: reference
---

Aprendido em 2026-11-03 (grok 1.0.70, `/opt/homebrew/bin/grok`, ST @ 8f41dd5). Confira `grok --version` antes de reusar; o levantamento completo está em `/private/tmp/pln004/grok/levantamento.md` (scratch, some).

**Fonte mais rápida:** `~/.grok/docs/user-guide/*.md` (27 arquivos, iguais aos de `xai-org/grok-build` no GitHub; o `--agents <JSON>` NÃO está documentado em lugar nenhum, nem na web). `~/.grok/README.md` repete o guia inteiro (113 KB, só ler com `grep -n '^#'`).

**Sondas sem modelo (US$ 0):** `grok inspect [--json]` mostra instruções, skills, agentes, hooks, plugins e trust do cwd; `grok models`, `grok usage <id>`, `grok sessions list`, `grok plugin list`; `grok -p '/workflow list' --agents '<json>'` valida o parse do `--agents` sem turno. Cada turno de modelo custa ≥ US$ 0,04 (o prompt de sistema tem ~19 mil tokens).

**Armadilhas de execução**
- Sem trust o `inspect` não carrega nada de projeto (instruções, skills, hooks, `.claude/settings.json`), mas lista os agentes. Use `GROK_FOLDER_TRUST=0` por processo para não gravar `~/.grok/trusted_folders.toml`.
- Rode com `env -i HOME="$HOME" PATH="$PATH" TERM=dumb GROK_FOLDER_TRUST=0 GROK_MEMORY=0 grok -p …`: o Grok roda também os hooks de `~/.claude/settings.json` (Orca) e do plugin `fixfy` (`deny_out_of_scope_write.py`), e a memória do app vem ligada por configuração remota (captura em `~/.grok/memory-v2`).
- `--max-turns` mínimo é 1; o `-p` que passa de `--max-turns` sai com 1 e "Error: max turns reached".
- A primeira corrida sob `--sandbox` cria arquivos vazios em `~/.grok` (`bundles/`, `hooks/`, `hooks-paths`, `sandbox.toml`, `trusted_folders.toml`): conte como "Fora do workspace".
- No zsh da ferramenta `echo ===` falha ("= not found"); use outro separador.
- `/private/tmp/pln004` é symlink para o scratch com espaço: o Grok grava o cwd resolvido (`Application Support/…`) e o `~/.grok/sessions/<cwd URL-encoded>` fica com `%20`; glob com `*p1*repo*` resolve.
- Prova de leitura: a sessão do modelo grava `chat_history.jsonl` e `prompt_context.json`; o primeiro `user` traz `<always_applied_workspace_rule name=…>` por arquivo de norma e a lista de skills. Não confie na resposta do modelo para saber o que foi carregado.

**Onde o Grok guarda o que o `measure` leria:** `~/.grok/sessions/<cwd>/<id>/usage.json` (tokens e `costUsdTicks`, 1 US$ = 1e10; o pai já soma o filho), `updates.jsonl` (`turn_completed`, `subagent_finished`), `subagents/<id>/meta.json`.

**Fonte envelhecida:** o `ST` mudou entre as sondas do Codex (3e36a69) e esta (8f41dd5): o override do chat agora aceita programa + args (`structuredAgentCommandPlan`); a nota "override é um executável literal sem argumentos" do Codex precisa de reconferência.

Ver também [[reference-codex-agy-sondas-armadilhas]] e [[reference-symlink-claude-codex-agy-sondas-sem-modelo]].
