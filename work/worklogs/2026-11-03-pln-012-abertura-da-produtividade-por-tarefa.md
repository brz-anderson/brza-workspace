---
scope:
  - brza-workflow
refs:
  - PLN-003
  - PLN-012
  - issue:codex-e-antigravity-sem-medida-por-tarefa
---

# Abertura do PLN-012, a produtividade medida por tarefa

O pedido de Anderson, em 2026-11-03, na sessão "Plano: chat via CLI e plugins" do `playground`, trazido à sessão
`tools-kit-produtividade`: "precisamos de uma forma de medir nossa produtividade, quanto realmente demoramos para
executar as tarefas, quanto gastamos de recursos em cada tarefa - aqui inclui custo da API, recurso de maquina e tempo
corrido - para irmos afinando o fluxo".

## O que se fez

- **Aberto o [PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou](../../plans/PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-plan.md)**,
  `origin: request`, com a Rodada 0 trazida do `playground`.
- **Conferidos os fatos do pedido**, com uma correção: o `summarize_measurements.py` mora em `core/scripts/` do
  `brza-workflow`, e não em `scripts/`.
- **Achado o elo entre a sessão e a tarefa:** o `CLAUDE_CODE_SESSION_ID` está no ambiente do `Bash` da sessão, e o
  `brza note commit` pode carimbá-lo no worklog. O mapa do `brza sessions` cobre só 25 das 100 sessões medidas desde
  2026-10-29.
- **R1 e R2 respondidas.** A tarefa é o worklog, carimbado no commit, e começa no primeiro prompt depois do marco
  anterior da sessão (R2.1). Três tempos: agente, Anderson e pausa acima de 30 min (R2.2, R2.3). A máquina vem do
  `ps -S` do `claude` no hook e do `brza run` (R1.2). As lacunas ficam à vista e ganham issue (R1.3, R2.4). O resultado
  aparece no `--by-task` e numa linha do worklog (R1.4).
- **Aberta a issue da lacuna:**
  [Codex e Antigravity ficam sem medida por tarefa](../issues/codex-e-antigravity-sem-medida-por-tarefa.md).
- **Uma sessão concorrente commitou a abertura**: outra sessão no mesmo worktree, a do `PLN-003`, gravou em `74fbe0f`
  a primeira versão do plano e um esqueleto deste worklog, com o e-mail `noreply` do GitHub, e não o do `brz-anderson`.
  Este worklog foi reescrito por cima.

## O que ficou

- O Desenho, com os pontos de "Em aberto para o Desenho" do plano, pelo `Retomar` do PLN-012.
