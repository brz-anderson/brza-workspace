---
scope:
  - brza-workflow
refs:
  - PLN-012
---

# Desenho do PLN-012, a medida por tarefa

O pedido de Anderson, em 2026-11-03, na sessão `tools-kit-produtividade`: "siga com o `PLN-012`".

## O que se fez

- **Um `designer` levantou o que faltava e rascunhou o Desenho** do
  [PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou](../../plans/PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-plan.md),
  com testes rápidos na máquina e sobre o `.measurements/`.
- **Caiu o `ps -S` da R1.2.** Ele não soma a CPU dos filhos de outro processo; a sessão conferiu: 0:00.01 depois de um
  filho de 2 s, contra `child_cpu=2.02s` pelo `proc_pid_rusage`. A leitura passa ao `proc_pid_rusage`, sem rodada,
  porque a intenção da R1.2 é a mesma.
- **R3 e R4 respondidas**, todas na recomendada: a `## Medida` do worklog lê o turno em curso (R3.1), porque o turno do
  commit tem 77% do custo e 88% da duração da tarefa mediana; o worklog não ganha `opened` nem hora em `completed`
  (R3.2, que fecha a R0.3); o aviso do `close-task` mostra o que o commit vai fechar e os "sem tarefa" das outras
  sessões (R3.3); `brza note commit --until HH:MM` separa duas tarefas emendadas (R3.4); a medida começa no deploy, sem
  retroativo (R4.1).
- **O Desenho foi gravado** em [PLN-012 — Desenho](../../plans/PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-design.md),
  D1 a D7, com o Terreno; o plano ficou com a linha `Dividido`.

## O que ficou

- A rodada do corte dos Passos P1 a P6 (16 h), pelo `Retomar` do PLN-012.
- Esta sessão emendou duas tarefas sem worklog entre elas: a instalação do Grok e a abertura da sessão `tools-kit-grok`
  ficaram entre a abertura do PLN-012 e este Desenho. É o caso que a R3.4 trata.
