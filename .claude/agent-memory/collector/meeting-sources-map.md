---
name: meeting-sources-map
description: Onde moram os dados das reuniões multiagente (briefing, rodadas, mapa de sessões, custo Claude/Codex/Grok) e as armadilhas que enganaram no levantamento de 2026-11-08
metadata:
  type: reference
---

**Onde mora cada coisa (reuniões Carvão em Brasa e MCP remoto, 2026-11-07):**
- Material fora do git: `WT/.sessions/reuniao-brasa/` e `WT/.sessions/reuniao-mcp-remoto/` (WT = `.worktrees/playground`).
- **`sessions.jsonl` e `measurements.jsonl` ficam na raiz do repo** (`/Users/andepb/Projects/brza-workspace/.sessions/` e `.measurements/`), NÃO no worktree; o `.sessions/` do worktree só tem as pastas das reuniões.
- `sessions.jsonl` só tem `open`, `session`, `close`, `title`: sem evento de `send`; `claude_session` liga o nome ao `session_id` do measurements; `provider_session` liga ao rollout do Codex (uuid no nome do arquivo).
- Custo Claude: `measurements.jsonl`, eventos `turn` e `subagent`, campos `estimated_cost_usd`, `duration_s`, `tokens.cache_read`; filtrar `workstream == playground` e `timestamp` (já em -03:00). A sessão de coordenação continua em 11-08 (soma muda muito: filtre o dia).
- Codex: `~/.codex/sessions/2026/11/07/rollout-*.jsonl`: `task_started`/`task_complete` (latência e `error` de limite) e último `token_count.info.total_token_usage`; sem US$. `turn_context` dá modelo e esforço.
- Grok e Antigravity: sem tokens em lugar nenhum (`~/.grok/memtrace` é só RAM; `~/.gemini/antigravity-cli/log` sem tokens). O Grok grava auto-memória fora do repo em `~/.grok/memory-v2/workspaces/brza-workspace-*/topics/`.
- Consolidação feita pela coordenação: `work/issues/reuniao-multiagente-com-personas-pelo-brza-sessions.md` (fricção) e as seções "As personas" dos dois `-coordenacao.md`.

**Armadilhas:**
- As tabelas "nota dos colegas" da coordenação B excluem a nota da Faísca (R3 tardia); recalcular dos worklogs dá outros decimais.
- Hora do limite do Codex: coordenação diz 21h41, rollout mostra 21:37 nas personas.
- Prazos nos `rodada-*.md` não são monotônicos; ignorar como sinal.
- Worklogs de B têm `## O que ficou` vazio; M não tem a seção.

**Atalho que poupou leitura:** regex nas tabelas `#### Placar`, `#### O voto`, `#### Os colegas` dos worklogs reproduz todas as tabelas da coordenação; `cat -n` nos `rodada-N.md` dá a linha de cada regra.
