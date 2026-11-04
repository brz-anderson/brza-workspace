---
scope:
  - workspace
  - brza-workflow
---

# Medição de produtividade por tarefa

## O que foi feito

Anderson perguntou se `opened`/`completed` do worklog deveriam levar data e hora em ISO 8601. Correram dois consultores `designer` em paralelo, um pela data só e outro pelo ISO 8601 no worklog.

Os dois convergiram em três pontos:
- O carimbo mediria a escrita da nota, não a tarefa, porque o worklog nasce no `close-task`, no fim.
- O `completed` com hora repete o git.
- O que falta é o início da tarefa e a ligação entre o worklog e a sessão medida.

Ficou corrigido que a norma do worklog não tem esses campos (`work/README.md:310-311`), e que os worklogs de hoje que os trazem saem dela.

Anderson trocou a pergunta pelo pedido: "precisamos de uma forma de medir nossa produtividade, quanto realmente demoramos para executar as tarefas, quanto gastamos de recursos em cada tarefa - aqui inclui custo da API, recurso de maquina e tempo corrido - para irmos afinando o fluxo".

Na rodada seguinte, escolheu "tools-kit (Recomendado)" e "Sessão nova agora (Recomendado)". Foi aberta a sessão `tools-kit-produtividade`, em `.worktrees/tools-kit`, com o pedido citado, os fatos dos consultores e as lacunas para a entrevista. A devolução é o plano commitado em `workstream/tools-kit`.

Nenhum código foi alterado. Até o plano decidir, os worklogs daqui seguem a norma, sem `opened`/`completed`.
