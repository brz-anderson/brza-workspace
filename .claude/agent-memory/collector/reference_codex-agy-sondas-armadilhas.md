---
name: reference-codex-agy-sondas-armadilhas
description: Como sondar o Codex 0.164 e o agy 1.4.12 sem se enrolar — armadilhas do shell, atalho sem modelo para o sandbox, onde o guardian aparece e o que o classificador nega
metadata:
  type: reference
---

Aprendido nas sondas do PLN-004 (2026-10-30); confira com `codex --version` e `agy --version` antes de confiar.

**Armadilhas de execução**
- No shell da ferramenta `codex` e `agy` são as funções da Fixfy; `fixfy_where` devolve `root` para qualquer cwd quando `FIXFY_WORKSPACE` está vazio (`cd ""` não sai do lugar). Use sempre `command codex …` e `command agy …`, senão entram `-c project_root_markers`, o MCP `firebase` e um `codex plugin marketplace upgrade`.
- `codex exec "prompt"` sem `< /dev/null` espera stdin e pendura a ferramenta Bash (vai a segundo plano em 300 s). Com `</dev/null` ainda imprime "Reading additional input from stdin..." e segue.
- O `codex exec` grava `[projects."<raiz git>"] trust_level = "trusted"` no `~/.codex/config.toml` sozinho (raiz do repositório, não do worktree). Conte isso como estado fora do workspace.
- `agy -p` com `--add-dir`: o cwd do `run_command` vira o primeiro `--add-dir` em ordem alfabética, não o cwd do processo. Sem `--add-dir` o git do worktree dá `not a git repository: (null)`.
- O classificador da sessão nega desligar o sandbox do agy (`--settings '{"enableTerminalSandbox":false}'`) e `pkill` amplo. Se a pergunta exige isso, devolva como ponto para Anderson em vez de insistir.
- `agy` num turno de exploração vaga (A2: 236 s, 452 mil tokens de cache): prompt fechado, um comando por chamada, "sem explorar".

**Atalhos**
- `codex sandbox -c 'sandbox_mode="workspace-write"' -c 'sandbox_workspace_write.writable_roots=[...]' -- <cmd>` roda o comando sob o seatbelt sem turno de modelo: testa o sandbox em segundos e de graça.
- Codex protege todo diretório chamado `.git` (e `.agents`, `.codex`, `.aws`) como leitura dentro de raiz gravável; raiz que é descendente de `.git` (`<common>/worktrees/<wt>`, `objects`, `refs`, `logs`) fica gravável. O `--add-dir <common>/.git` não adianta.
- Guardian: `session_meta.thread_source == "guardian_review"`, `parent_thread_id` do pai, `codex-auto-review`; os tokens do filho não entram no `thread_token_usage` do pai. Dispara com `-c approval_policy=on-request -c approvals_reviewer=auto_review` e um comando que o modelo escale (`require_escalated`).
- Hook do Codex sem confiança por hash é pulado em silêncio no `exec`; sem aprovação de Anderson não há como observar evento de hook.
- Transcript do agy: `BR/<conversationId>/.system_generated/logs/transcript_full.jsonl`; o `--output-format json` do `-p` já traz `usage` (in/out/thinking/cache_read) e `conversation_id`.
- `agy agents` só lista os agentes do worktree com `--add-dir <worktree>` (worktree não confiado); `tools:` do frontmatter aceita os nomes velhos (`view_file`…) e os novos (`read_file`…) e o subagente recebe a família nomeada.

Ver também [[reference-fixfy-pln-011-onde-mora]].
