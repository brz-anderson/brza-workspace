---
scope:
  - brza-workflow
tags:
  - tooling
refs:
  - PLN-009
  - PLN-012
  - PLN-013
  - PLN-015
---

# O advisor tool no fluxo, a análise e a abertura do PLN-015

O pedido de Anderson, em 2026-11-06, na sessão `beb7e7e4-0184-455d-9274-8d3ef9c4a107`, aberta no `brza-workflow`:
"leia https://platform.claude.com/docs/pt-BR/agents-and-tools/tool-use/advisor-tool e faça uma analise de como podemos
melhorar nosso fluxo baseado nessa feature". Depois da análise, Anderson pediu para abrir o plano: "sim, abra".

O plano é o [PLN-015: O executor consulta um advisor mais forte, com o custo medido e a política por papel](../../plans/PLN-015-advisor-no-executor/PLN-015-plan.md).

## O que se fez

- **A documentação do advisor tool, lida inteira.** Um executor mais barato consulta um modelo mais forte no meio do
  turno, numa chamada do lado do servidor. A ferramenta é a `advisor_20260301`, com o beta `advisor-tool-2026-03-01`.
  O advisor tem de ser pelo menos tão capaz quanto o executor. Os tokens dele vêm só em `usage.iterations[]`, nas
  entradas `advisor_message`, e não no `usage` principal. Com Opus 5.5 ou Fable de advisor, o conselho volta
  criptografado (`advisor_redacted_result`); só o `claude-opus-4-8` devolve texto legível. Pela doc, Sonnet com esforço
  médio e Opus de advisor chegou à qualidade do Sonnet com esforço padrão, gastando menos em código.
- **O suporte no Claude Code 2.1.319, achado no binário.** Há a configuração `advisorModel`, a flag `--advisor <model>`
  (fora da ajuda), o comando `/advisor` e o `CLAUDE_CODE_DISABLE_ADVISOR_TOOL`. O advisor vale para a sessão inteira, e
  os subagentes herdam: "Advisor will not activate on the main model (advisor is less capable); subagents may still use
  it". Não se achou como ligar por subagente no frontmatter.
- **O prompt que o Claude Code injeta manda commitar antes da última consulta** ("make your deliverable durable: write
  the file, save the result, commit the change"). Isso contraria o "sem commit" do `implementer.md`.
- **A medição de hoje deixaria o advisor de fora.** O `core/.claude/hooks/measure.py:316-424` soma só o `usage`
  principal de cada pedido. Não se conferiu se o transcript grava o `iterations`, porque não há transcript com advisor
  na máquina.
- **A recomendação:** o advisor só no papel executor (`implementer` e o dispatch com `role: executor`, Sonnet com
  esforço médio), com Opus de advisor. Ficam de fora o `reviewer` (ancoragem), o `designer` e o `architect` (Opus, onde
  o advisor não liga), o `collector`, o desempate do `resolver.py` e os runtimes fora do Claude. Três fases: medir,
  política e norma, piloto A/B.
- **O PLN-015 aberto** no `tools-kit`, ao lado do PLN-009, do PLN-012 e do PLN-013, que tratam do MCP e da medição.

- **A rodada 1 do PLN-015, respondida com as quatro recomendadas.** O custo do advisor entra no `measure.py` por este
  plano, antes do PLN-012; o advisor do piloto é o Opus 5.5; o piloto liga à mão (`claude --advisor opus`), e a
  política e o dispatch só entram se ele se pagar; a prioridade é `medium`.

## O que ficou

- O Desenho do PLN-015: D1 o custo do advisor na medição, D2 a norma do `implementer`, D3 o protocolo do piloto.
- O PLN-012 precisa partir do `measure.py` com o advisor (PLN-015/R1.1).
