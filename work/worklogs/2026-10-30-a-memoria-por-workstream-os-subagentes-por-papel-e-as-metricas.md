---
scope:
  - workspace
  - brza-studio
---

# A memória por workstream, os subagentes por papel e as métricas

O pedido de Anderson, em 2026-10-30, na sessão `brza-workspace-73`, logo depois do corte em workstreams: "todo agente
deve ter memória própria, assim podemos acompanhar o "aprendizado" em cada frente de trabalho e ter métricas pra poder
melhorar o fluxo cada vez mais". A decisão está em
[Cada workstream aprende na memória dele, com subagentes por papel e métricas por workstream](../decisions/cada-workstream-aprende-na-memoria-dele.md).

## O que se fez

- **O levantamento:** o runtime dá uma memória só por repositório, para todos os worktrees ("all worktrees and
  subdirectories within the same git repository share one auto memory directory"); o `autoMemoryDirectory` a desvia, e
  o `memory: project` do subagente grava em `.claude/agent-memory/<nome>/` do projeto.
- **As rodadas:** três de perguntas e a do texto, "A.1 e F.1", mais a E, "Symlink para o workstream".
- **Os agentes:** `collector` e `implementer` em Sonnet, `reviewer` e `designer` em Opus, todos com `memory: project`,
  escritos nesta sessão.
- **O código, por dois subagentes Sonnet em paralelo:**
  - a medição: o `workstream` em toda linha, o evento `memory` pelo retrato e as rodadas no `turn`; o
    `summarize_measurements.py --by-workstream`; e o `read_from`, que cortava a linha do transcript no U+2028 e perdia
    rodadas. `python3 -m unittest discover -s .claude/hooks/tests` → 56 OK.
  - o `brza`: o `brza note workstream` e o `memory-setup` com o `settings.local.json`, o aviso de memória suja no
    `commit`, o `brza tree` com o `autoMemoryDirectory` e o symlink, o `brza-agents` e o `--agents` no `claude-brza`.
    `python3 -m unittest discover -s scripts/brza/tests` → 229 OK.
- **A base das rodadas:** nos 235 `AskUserQuestion` dos transcripts deste workspace até aqui, 188 saíram na
  recomendada, 40 em outra opção e 7 em texto livre.
- **A norma e o código** em `77f018c` na `master`, levados aos três workstreams pelo `brza note sync`.
- **A memória:** o `brza note memory-setup` ligou os três worktrees; as três memórias do `brza-studio` foram copiadas ao
  `memory/` do `studio` (`2a3ea80`); as duas da memória compartilhada daqui viraram norma no `CLAUDE.md` e no
  `AGENTS.md` e saíram.
- **O `brza-studio`:** `/.claude/agent-memory` no `.gitignore` (`3e36a6945f2`).

## O que ficou

- **O `~/.zshrc`:** a permissão para editá-lo foi negada nesta sessão; o bloco novo de `brza_where` e `brza_claude`, com
  o `--agents` no `brza-studio`, está no `README.md`, e Anderson o copia. Até lá, a sessão do `brza-studio` aberta pelo
  terminal sobe sem os subagentes por papel; a do chat, pelo `claude-brza`, já os tem.
- **O `brza-install --all`:** liga o `brza-agents` no `~/.local/bin`; também ficou para Anderson rodar.
- **Os worktrees do `brza-studio` que já existiam** (`pln-001-pedido-32`, `pln-001-pedido-33`) não têm o
  `settings.local.json` nem o symlink, que só o `brza tree` novo cria.
- **Os pontos dos dois subagentes** que ficaram na recomendada, para Anderson confirmar: o retrato por worktree, a master
  sem memória medida, o plano ambíguo como `null`, o `session_id` aproximado no evento `memory`, a pergunta recusada fora
  da conta, o `MEMORY.md` fora das memórias vivas, o `.gitignore` do workspace com o `settings.local.json`, e o aviso de
  memória suja por arquivo.
- **A sessão aberta no meio da mudança** não carrega os agentes novos; eles valem da próxima sessão em diante.

## Fora do workspace

- **A memória compartilhada do runtime**, em `~/.claude/projects/-Users-andepb-Projects-brza-workspace/memory/`.
  - O quê: saíram `abrir-sessao-nova-pelo-brza-sessions.md` e `aprovacao-de-texto-em-mensagem-e-nao-na-caixa.md`, e o
    `MEMORY.md` ficou vazio.
  - Risco: a sessão aberta na `master` deixa de ver as duas; o conteúdo está no `CLAUDE.md` e no `AGENTS.md`.
  - Estado: ativo.
  - Como desfazer: reescrever os dois arquivos a partir do `CLAUDE.md` ("A própria sessão abre a sessão nova") e do
    `AGENTS.md` ("A rodada que aprova um texto vai na mensagem").
