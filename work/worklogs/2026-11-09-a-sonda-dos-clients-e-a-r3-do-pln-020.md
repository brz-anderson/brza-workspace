---
scope:
  - workspace
  - brza-workflow
tags:
  - tooling
  - planning
refs:
  - PLN-020
sessions:
  - 2477d2a4-7778-41c8-9b3b-fb839339bf9a
---

# A sonda dos clients e a R3 do PLN-020: as skills chegam por symlink, e o MCP fica para o que o client não faz

O pedido de Anderson, em 2026-11-09, no workstream `playground`: "comece", depois das rodadas 1 e 2 do
[PLN-020: Os fluxos do workspace rodam em qualquer client, pelas skills distribuídas e por verbos do brza-orchestrator](../../plans/PLN-020-os-fluxos-em-qualquer-client-pelo-brza-orchestrator/PLN-020-plan.md).
O primeiro passo era a sonda: o Codex roda as skills do workspace?

## O que se fez

### O ambiente isolado

- **O clone:** repositório bare como `origin`, um clone com a `master`, e os worktrees dos seis workstreams, tudo no
  scratch da sessão.
- **As variáveis:** `BRZA_WORKSPACE` e `MEASURE_DIR` apontando para o clone, porque o `brza note` escreve no workspace
  da `BRZA_WORKSPACE` (`brza-workflow/bin/brza-note:1663`) e mede na mesma raiz (`:698`). Sem isso, o commit da sonda
  iria ao workspace real.
- **A identidade:** a sonda do fechamento rodou sem `GIT_AUTHOR_*`, sem `CLAUDE_CODE_SESSION_ID` e com o `user.email`
  do repositório real, como numa sessão do Codex.

### O que se mediu

O Terreno M1–M11 está no PLN-020. Em resumo:

| Client | Catálogo | Fluxo |
| :-- | :-- | :-- |
| Codex `0.166.0` | só com `.agents/skills -> ../.claude/skills` | "confere as notas" e "fecha a tarefa" ativam as skills sozinhos e chegam ao `brza note commit`; o sandbox barra o `.git`, a identidade sai do `.git/config` e a tarefa fica sem `session_id` |
| `cursor-agent 2026.10.22` | lê o `.claude/skills` sem nada | não rodado |
| Antigravity (`agy`) | só com o symlink, e corta `meeting-runner` e `agent-instructions-writer` por orçamento do catálogo | não rodado |
| Gemini CLI | não instalado | — |

O modo sem sandbox do Codex foi barrado pelo classificador do modo auto desta sessão. O commit final foi rodado pela
sessão com o comando e o ambiente que o Codex montou. Ele passou, com push e índice no `origin` do clone, e a linha
`task` saiu com `session_id: null`.

### A R3

Respondida por Anderson, pela pergunta com opções:
- symlink no `core/` do `brza-workflow`;
- `close_task`, `start_task`, `index_query` e `decision_record` no Desenho, e o `check_notes` fora;
- a identidade da norma gravada no `.git/config` pelo `brza doctor`, com emenda no `AGENTS.md`;
- o corte do Antigravity aceito e registrado.

O texto das opções, com custo e quando se paga, está na Entrevista do PLN-020.

## Fora do workspace

- **Sessões do Codex** — o quê e onde: cinco rollouts de `codex exec` em `~/.codex/sessions/2026/11/09/`, de 22:51 a
  22:54, com o cwd no scratch. Risco: nenhum além do histórico. Estado: encerradas. Como desfazer: `codex delete
  <id>` em cada uma, ou deixar.
- **Confiança do Cursor no clone** — o quê e onde: `cursor-agent --trust` no worktree do clone; o arquivo onde o
  Cursor guarda a confiança não foi achado por busca. Risco: nenhum, porque o diretório some com o scratch. Estado:
  pode seguir registrado. Como desfazer: apagar o clone.
- **Conversas do Antigravity** — o quê e onde: três conversas em `~/.gemini/antigravity-cli/brain/` e no
  `cache/last_conversations.json`. Risco: nenhum além do histórico. Estado: encerradas. Como desfazer: apagar as
  pastas em `brain/`.

## Retomar

O próximo passo está no `Retomar` do PLN-020: a R4, que decide os verbos de plano e de migração e os MCP prompts da
R1.2, e o Desenho de D1 a D6.

## Custo da tarefa

Corrido 13 min — agente 12 min, quem pediu 1 min, pausa 0 s · US$ 2,19 (turnos 2,19, subagentes 0,00) · CPU 14 s do `claude` e 36 s dos comandos, RSS até 524 MB · 1 turno, 1 sessão · até 23:03 de 2026-11-09, pelo `brza note commit`
