---
status: open
phase: interview
origin: request
description: Liga o advisor tool do Claude Code no papel executor, mede o custo dele na medição e decide pelo piloto se o fluxo o adota.
ready: "não — falta a rodada 1 (onde mora o custo do advisor, o modelo, como ligar só no executor); isso trava o Desenho"
scope:
  - brza-workflow
opened: 2026-11-06
owner: Anderson
tags:
  - tooling
---

# PLN-015: O executor consulta um advisor mais forte, com o custo medido e a política por papel

- **Retomar:** aberto em 2026-11-06 com o Pedido, a Cobertura e o Fora de escopo rascunhados. Próximo: fechar a
  rodada 1 e gravá-la na Entrevista; depois, o Desenho (D1 medição, D2 política, D3 norma do `implementer`, D4 piloto).

## Pedido

- **Origem:** pedido livre de Anderson em 2026-11-06, numa sessão aberta no `brza-workflow`
  (`beb7e7e4-0184-455d-9274-8d3ef9c4a107`), sobre a documentação do
  [advisor tool](https://platform.claude.com/docs/pt-BR/agents-and-tools/tool-use/advisor-tool).

> "leia https://platform.claude.com/docs/pt-BR/agents-and-tools/tool-use/advisor-tool e faça uma analise de como
> podemos melhorar nosso fluxo baseado nessa feature"

A análise recomendou o advisor só no papel executor, com três fases: medir, política e norma, e piloto. Ela terminou com
a pergunta "Quer que eu abra isso como plano (`brza note plan-open`), começando pelas mudanças da fase 1 no
`measure.py`?", e Anderson respondeu:

> "sim, abra"

### Cobertura

| Origem | Critério de aceite | Passo | Teste (nível) |
| :----- | :----------------- | :---- | :------------ |
| `Pedido 1`, fase 1 | O turno com advisor sai na medição com `advisor_calls` e `advisor_cost_usd`, cada chamada pelo preço do modelo de `usage.iterations[].model`, e o `estimated_cost_usd` do turno passa a somar o advisor | a planejar | a planejar |
| `Pedido 1`, fase 1 | O `summarize_measurements.py` mostra o custo do advisor em coluna própria, por workstream e por dia | a planejar | a planejar |
| `Pedido 1`, fase 2 | A política aceita `policy.roles.<papel>.claude.advisor`, o `decide_model` devolve o advisor, e o `brza.toml` com advisor fora do Claude ou com par inválido (advisor menos capaz que o executor) é recusado com o motivo | a planejar | a planejar |
| `Pedido 1`, fase 2 | O `implementer.md` diz que, para ele, entrega durável é o arquivo escrito com a suíte verde, nunca o commit, e que conselho que contradiz a evidência volta numa segunda consulta | a planejar | a planejar |
| `Pedido 1`, fase 3 | O piloto compara fases com e sem advisor pelo custo estimado e pelos achados de revisão de cada fase, e o resultado vai a uma nota de `work/decisions/` | a planejar | a planejar |

### Fora de escopo

- **O advisor no `reviewer`.** O advisor lê o transcript inteiro do executor, e o `reviewer` tem de revisar sem ancorar
  na conclusão de quem pediu. A revisão continua sendo outro agente.
- **O advisor no `designer`, no `architect` e na sessão principal em Opus.** O advisor só liga quando é pelo menos tão
  capaz quanto o executor. Sobre Opus, só o Fable 5.1 serviria, e isso é outro plano, se o piloto se pagar.
- **O advisor no `collector` e no desempate Haiku do `resolver.py`.** São leitura em volume e classificação de uma
  chamada só, onde o advisor só soma custo.
- **Os runtimes Codex, Grok e Antigravity.** O advisor é ferramenta de servidor da API da Anthropic.

## Restrições

- **O código é do `brza-workflow`.** `core/.claude/hooks/measure.py`, `core/scripts/summarize_measurements.py`,
  `packages/mcp/brza_mcp/policy.py` e `core/.claude/agents/implementer.md` se editam lá e chegam aos workspaces pelo
  `brza sync`. Editados aqui, travam o sync seguinte.
- **O `measure.py` é também do PLN-012**, que liga a medição às tarefas. As duas mudanças no hook não podem se
  sobrescrever: a ordem entre elas é ponto da rodada 1.

## Worklogs

- 2026-11-06 — a análise do advisor tool e a abertura; Pedido, Cobertura e Fora de escopo rascunhados. Parou na
  rodada 1. [O advisor tool no fluxo, a análise e a abertura do PLN-015](../../work/worklogs/2026-11-06-advisor-tool-no-fluxo.md)
