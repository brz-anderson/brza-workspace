---
scope:
  - workspace
  - brza-workflow
tags:
  - tooling
  - planning
refs:
  - PLN-003
  - PLN-017
  - PLN-020
sessions:
  - 2477d2a4-7778-41c8-9b3b-fb839339bf9a
---

# As ferramentas MCP dos fluxos vão a plano: a discussão e as rodadas 1 e 2

O pedido de Anderson, em 2026-11-09, no workstream `playground`: discutir a ideia de dar ao `brza-orchestrator` as
ferramentas `run_plan`, `run_meeting`, `run_migration`, `start_task`, `close_task` e `check_notes`, equivalentes às
skills, com crítica e sugestões novas. O pedido inteiro está no
[PLN-020: Os fluxos do workspace rodam em qualquer client, pelas skills distribuídas e por verbos do brza-orchestrator](../../plans/PLN-020-os-fluxos-em-qualquer-client-pelo-brza-orchestrator/PLN-020-plan.md).

## O que se fez

### A leitura antes da crítica

- As ferramentas de hoje do servidor: `dispatch`, `status` e `config`, com o gate para o que não é consultor
  (`brza-workflow/packages/mcp/brza_mcp/tools.py:1-8`, `:535-546`).
- As seis skills, separadas em determinísticas e de conversa.
- As issues da reunião MCP remoto (correio remoto, MCP no Codex Cloud, perfil remoto do RPC, proxy de autorização).
- `~/.codex/skills` e `~/.agents/skills` existem nesta máquina, com skills de terceiros: o Codex já lê skill.
- Os planos vizinhos: o PLN-017 está `done` e adiou o embrulho MCP (R1.2); o PLN-003 do `tools-kit` tem no P4 o plugin
  `brza:` com skills e `.mcp.json`, mas para o BrzA Studio e o Orca.

### A crítica e as sugestões

Oito críticas e sete ferramentas sugeridas, gravadas no "Apresentado antes" da R1 do PLN-020. O eixo: `run_*`
monolítico fere "quem pergunta e grava é a sessão principal"; o roteiro cabe nos MCP prompts; o daemon não tem o
ambiente da sessão; e as ferramentas que escrevem git ou abrem chat pago entram no gate.

### As rodadas

- **R1**, em texto, respondida "ambos recomendado": o motor é a portabilidade entre clients, com a sonda do Codex
  antes de construir; os fluxos longos viram verbos com invariante e MCP prompts.
- **R2**, pela pergunta com opções: PLN novo no `playground`; os verbos da reunião esperam a PLN-017/R1.2.

### O plano

Aberto pelo `brza note plan-open`: PLN-020, `phase: interview`, com o Pedido, a Cobertura, o Fora de escopo, as
Restrições e as rodadas 1 e 2.

## Retomar

O próximo passo está no `Retomar` do PLN-020: a sonda do Codex, e então a R3, o corte dos verbos.

## Custo da tarefa

Corrido 13 min — agente 4 min, quem pediu 9 min, pausa 0 s · US$ 1,59 (turnos 1,59, subagentes 0,00) · CPU 11,55 s do `claude` e 5,80 s dos comandos, RSS até 507 MB · 2 turnos, 1 sessão · até 22:48 de 2026-11-09, pelo `brza note commit`
