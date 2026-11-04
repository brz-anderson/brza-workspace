---
name: reference-symlink-claude-codex-agy-sondas-sem-modelo
description: Como sondar symlink de agents/skills/memória em Claude, Codex e agy quase de graça, o que o brza-sync faz com link, e as armadilhas do levantamento do .brzAgents (PLN-004)
metadata:
  type: reference
---

Confirmado em 2026-11-03 (Claude Code 2.1.318, Codex 0.166.0, agy 1.4.12; BW HEAD 7a18392). Confira as versões antes de reusar.

**Sondas baratas**
- Claude: `claude -p "ok" --model haiku --max-turns 1 --max-budget-usd 0.05 --output-format stream-json --verbose --no-session-persistence </dev/null` num dir `git init` mostra `agents`, `skills` e `slash_commands` na mensagem `system/init`: US$ 0,002 por sonda. `claude agents` NÃO lista agentes (gerencia sessões de fundo).
- Subagente com `memory: project`: peça no prompt "chame o subagente X, espere, repita a resposta"; sem "espere" ele vira assíncrono e o `Write` aparece no nível principal. Use `parent_tool_use_id` do stream-json para separar SUB de MAIN (~US$ 0,006 por turno).
- Codex: `command codex debug prompt-input "x"` lista as skills do cwd sem modelo e sem gravar confiança no `~/.codex/config.toml` (conferir `grep -c <dir> ~/.codex/config.toml`).
- agy: `agy agents` não aceita flag depois do subcomando (`agy --settings ... agents`), e não listou o papel de sonda nem em `.agents/agents`; use `agy -p ... --output-format json` (≈23 mil tokens, 40 s) para skills.
- Em `-p`, qualquer escrita sob `.claude/` pede permissão ("sensitive file"), mesmo sem symlink: a sonda de edição de agente por link fica inconclusiva; compare sempre com um controle de diretório real.

**O que a sonda mostrou (não confie sem reler os `sonda-*`)**
- `.claude/agent-memory` como symlink: o `Write`/`Edit` do subagente com `memory: project` foi negado (3 de 3), o controle real gravou; a leitura pelo link funciona. A doc de erros (`errors.md`, "Refusing to write into symlinked directory") só descreve o caso em que o diretório que contém o arquivo é o link.
- `git add`/`git status` por pathspec através de link: vazio / "beyond a symbolic link"; `MEMORY_PATHS` (`brza-note:105`) e `NOTE_PATHS` (`compact_guard.py:31`) quebram se a memória real mudar de lugar.
- `brza-sync` não entrega link: workspace novo ganha arquivo de texto com o alvo; diretório real no caminho dá `SyncError ... Is a directory`. O D15 como escrito falha na transição (escreve antes de apagar) e o `commit_and_push` (`brza-sync:429`) dá `git add` de caminho sob o link novo.
- `check_notes.py`, `brza-agents`, `measure.memory_dirs` funcionam com os diretórios por link.

**Sonda da memória por link (2026-11-03, `sonda-mem/run.py`, ≈US$ 0,0055 por execução)**: nenhuma saída em `-p` — link relativo, absoluto, link só no papel, `permissions.allow` absoluto + `--add-dir`, hook `PreToolUse` allow (disparou e foi ignorado) e `dontAsk` negaram; só o diretório real grava. Doc: `.claude` é protegido, exceção só para `.md` de `agent-memory` (`permission-modes.md#protected-paths`), e `permissions.allow` não pré-aprova caminho protegido; allow do `.claude/settings.json` nem vale em `-p` sem confiança (use `settings.local.json`). Armadilhas: caminho do scratch tem espaço, então comando de hook precisa de aspas; `--permission-mode bypassPermissions` é negado pelo classificador da sessão; o curl de `https://code.claude.com/docs/en/<pagina>.md` dá a página inteira para `grep`.

**Atalhos de contagem**: regex `\.claude(/|['"] */ *['"])(agents|skills|agent-memory)` pega também `Path('.claude') / 'skills'`; o ouro do BW (`tests/hooks/fixtures/golden/master`, 19 arquivos) é cópia da master antiga e `test_golden_render.py:81` compara a lista de `.md` por caminho. O ST (`~/Projects/brza-studio`) tem `.worktrees/` com cópias e `tests/e2e/.cross-version-checkouts`: exclua-os do grep. Só um workspace está no registro (`~/.config/brza/workspaces.toml`).

Ver também [[reference-brza-workflow-depois-da-migracao]] e [[reference-codex-agy-sondas-armadilhas]].
