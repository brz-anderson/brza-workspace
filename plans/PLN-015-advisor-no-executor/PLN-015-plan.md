---
status: open
phase: design
origin: request
description: Liga o advisor tool do Claude Code no papel executor, mede o custo dele na medição e decide pelo piloto se o fluxo o adota.
ready: "não — falta o Desenho (D1 medição, D2 norma do implementer, D3 piloto); isso trava os Passos"
scope:
  - brza-workflow
opened: 2026-11-06
owner: Anderson
priority: medium
tags:
  - tooling
---

# PLN-015: O executor consulta um advisor mais forte, com o custo medido e a política por papel

- **Retomar:** aberto e com a R1 respondida em 2026-11-06. Próximo: o Desenho — D1 o custo do advisor no
  `measure.py` e no `summarize_measurements.py`, D2 a norma do `implementer`, D3 o protocolo do piloto.

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
| `Pedido 1`, `R1.2`, `R1.3` | A sessão do `implementer` no piloto abre com `claude --advisor opus` (Opus 5.5), e a medição do turno mostra as consultas | a planejar | a planejar |
| `Pedido 1`, fase 2 | O `implementer.md` diz que, para ele, entrega durável é o arquivo escrito com a suíte verde, nunca o commit, e que conselho que contradiz a evidência volta numa segunda consulta | a planejar | a planejar |
| `Pedido 1`, fase 3 | O piloto compara fases com e sem advisor pelo custo estimado e pelos achados de revisão de cada fase, e o resultado vai a uma nota de `work/decisions/` | a planejar | a planejar |

### Fora de escopo

- **O advisor na política e no dispatch do MCP** (`policy.roles.<papel>.claude.advisor`, o `--advisor` no worker).
  Pela R1.3, só entra se o piloto se pagar: a decisão do piloto abre o plano ou a issue dele.
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
- **O `measure.py` é também do PLN-012**, que liga a medição às tarefas. Pela R1.1, o custo do advisor entra aqui,
  antes, e o desenho do PLN-012 parte do hook com o advisor.

## Entrevista

### Rodada 1 — a medição, o modelo, como ligar e a prioridade (enviada 2026-11-06)

> **Apresentado antes:** a análise da documentação do advisor tool e do Claude Code 2.1.319, no
> [worklog da sessão](../../work/worklogs/2026-11-06-advisor-tool-no-fluxo.md): o advisor só no papel executor; o
> custo dele só em `usage.iterations[]`, fora do que o `measure.py:316-424` soma; o advisor vale para a sessão inteira,
> e os subagentes herdam; o conselho do Opus 5.5 volta criptografado.

Respondida em 2026-11-06.

1. **Onde fica o custo do advisor no `measure.py`, que o PLN-012 também vai reescrever.** Opções:
   - aqui, antes do PLN-012 (recomendada) — custo: ~2 h agora e o desenho do PLN-012 rebaseado sobre o hook novo; se
     paga: no piloto, que sem isso mediria o advisor como grátis;
   - dentro do PLN-012, com `depends_on` — custo: o piloto espera o PLN-012 inteiro (16 h, sem corte aceito); se paga:
     só quando o PLN-012 executar;
   - issue separada — custo: zero agora; se paga: nunca, enquanto ninguém a pegar.

   **Decidido — aqui, antes do PLN-012.**

2. **O modelo do advisor no piloto.** Opções:
   - Opus 5.5 (recomendada) — custo: o preço do Opus 5.5 por consulta, e o conselho não se lê; se paga: no fim do
     piloto, se os achados por fase caírem;
   - Opus 4.8 — custo: o piloto mede um modelo que não iria à produção; se paga: só se ler o conselho mudar decisão;
   - Fable 5.1 — custo: o mais caro, com consentimento no Claude Code e escopo na sessão principal; se paga: só depois
     de um piloto do Opus com ganho.

   **Decidido — Opus 5.5.**

3. **Como ligar só no executor, se o Claude Code liga para a sessão inteira.** Opções:
   - manual no piloto (recomendada) — `claude --advisor opus` na sessão do `implementer`, e o dispatch só se o piloto
     se pagar; custo: zero código agora; se paga: agora;
   - `--advisor` pelo dispatch do MCP — custo: ~4 h, mais ler o `worker-start` do `brza-studio`; se paga: no piloto;
   - `advisorModel` no `settings.json` do workspace — custo: o `collector` e todo subagente Sonnet também ganham
     advisor; se paga: nunca, para este objetivo.

   **Decidido — manual no piloto.** A política e o dispatch saem para o Fora de escopo, condicionados ao piloto.

4. **A prioridade.** Opções: `medium` (recomendada) — custo: o piloto começa em dias; se paga: quando a fila andar ·
   `high` — custo: atrasa o PLN-012 e os demais do `tools-kit`; se paga: logo, se o custo do executor for o gargalo ·
   `low` — custo: zero agora; se paga: só quando alguém retomar.

   **Decidido — `medium`.**

## Worklogs

- 2026-11-06 — a análise do advisor tool e a abertura; Pedido, Cobertura e Fora de escopo rascunhados; R1 respondida,
  e o plano vai ao Desenho. [O advisor tool no fluxo, a análise e a abertura do PLN-015](../../work/worklogs/2026-11-06-advisor-tool-no-fluxo.md)
