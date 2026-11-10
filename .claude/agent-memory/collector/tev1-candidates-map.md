---
name: tev1-candidates-map
description: Onde mora cada ponto de decisão fechada (CLI, MCP resolver, meeting-runner, plan-runner, hooks, Studio) e atalhos de medição do levantamento do tev1 em 2026-11-09
metadata:
  type: reference
---

- Chamada existente ao tev1: `~/Projects/brza-workflow/packages/mcp/brza_mcp/resolver.py:115-126` (`_tev1`), cadeia em :89-109, Haiku em :128; só 1 pergunta (`layer`). `tev1_min_confidence` não tem padrão (policy.py:49) e não está no workspace: tudo vai ao Haiku. Só 7 eventos `route.resolver` medidos.
- plan-runner e migration-runner não têm scripts: a classificação é prosa na SKILL.md (Passo 1 linha 54, Passo 2 linha 77; migration ops linha 20-24). Uso real: plan-runner 39 skills, migration-runner 0.
- `brza-note` é todo regex/caminho/frontmatter (note_kind:1138); `brza quota` não existe como binário (cota em limits.py/resolver.choose_account, numérica).
- Studio: falhas e cota do chat já são tipadas; heurística de texto só no TUI (agent-title-status.ts:229, startup-dialog-blocked-signals.ts:34 com `RuntimeTerminalWaitBlockedReason` em shared/runtime-terminal-contracts.ts:317).
- measurements.jsonl: `fact_audit` tem `cost_usd`; `fact_check` NÃO tem custo (só `fact_audit`); `.measurements/fact-audit/` fica vazio (apagado após auditoria). `event` é a chave (não `type`).
- Calibração de voto: `tally.parse_worklog` sobre `work/worklogs/*reuniao-*.md` dá voto_por_proposta/posicao; só a R3 do carvão tem tabela `O voto` (90 linhas). Linha `Fatos lidos` ainda não existe em nenhum worklog (regra de 2026-11-09). Os `estado-r*.json` têm `voto` sempre nulo; fixtures `reuniao-*.json` são só definição de personas.
