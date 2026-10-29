---
scope:
  - workspace
  - brza-studio
---

# O PLN-003: a entrevista do workflow nos dois clients

O pedido de Anderson, em 2026-10-29, no chat do BrzA Studio: "vamos criar um plugin do Orca para o Workspace e um plugin
do Claude + MCP para o Workflow e ajustar a CLI `brza` para que o workflow funcione tanto no client `BrzA Studio` quanto
no `Orca`". Depois ele acrescentou a instalação e a distribuição do CLI, a medição das features por frente e a norma do
workspace como uma das frentes. A sessão abriu o
[PLN-003: O workflow do workspace roda igual no BrzA Studio e no Orca, por plugins e pelo `brza`](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-plan.md)
e fechou a Entrevista. Não houve implementação.

## O que se fez

**As rodadas 1 a 7**, gravadas no
[PLN-003 — Entrevista](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-interview.md):
- **R1:** o escopo — o Workflow são os dois sentidos, o plugin do Orca tem painel e comandos, e o plano não espera o P7.
- **R2:** a CLI nos dois clients — a detecção, o `brza` próprio, o `tree` e o `test` generalizados, `install` e `doctor`.
- **R3:** a distribuição — pública e por fases, Python stdlib, o app pela release, o MCP HTTP residente.
- **R4:** o painel, as skills, os roteiros e o MCP como orquestrador.
- **R5:** a regra e o agente que desempata, o executor com gate, o repositório `brz-anderson/brza` e o "P7 agora".
- **R6:** o P7 numa sessão nova, o `DESIGN.md` como design system, o `brza.toml` e o aviso à sessão principal.
- **R7:** o semáforo por conta e runtime, o `ARCHITECTURE.md` e a fase 0 numa sessão própria.

**O levantamento**, por seis subagentes em leitura — cinco Sonnet e um Opus. Os agregados ficaram no
[PLN-003 — Desenho](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-design.md), no Terreno e na matriz
feature × frente: o plugin do Orca, o MCP no chat, o plugin do Claude, o orquestrador, as 34 sugestões das notas e a
alocação pelos critérios C1 a C8.

**O P7 do PLN-002 saiu daqui:** a linha "Pedido de fora" no `Retomar` do PLN-002, e a sessão `pln-002-p7` aberta pelo
`brza-sessions`, com as decisões citadas.

## O que se aprendeu

- **O painel de plugin do Orca não recebe dados do worker.** Não há canal no protocolo, e a CSP barra fs e fetch. O
  contorno é o HTML regenerado na pasta dev.
- **O chat dos dois apps carrega os plugins do projeto.** Ele roda o `claude` pelo SDK com `settingSources`. Por isso o
  plugin e o MCP chegam sem mexer no fork.
- **A `orchestration` do Orca não agenda.** Ela não tem fila nem limite. O uso por conta já sai do
  `orca account list --json`.
- **O `measure.py:84-87` grava as duas contas do app como `home`.** O roteamento por conta não é medível até esse
  conserto.
- **Um subagente rodou `git fetch upstream` no `brza-studio`** fora do pedido de só leitura. Só as refs remotas mudaram.

## O que ficou

- **Os itens `D` e os Passos**, com os riscos da fase 0 como hipóteses: estão no `Retomar` do plano.
- **O P7:** corre na sessão `pln-002-p7`.

## Fora do workspace

- **O quê e onde:** a sessão `pln-002-p7`, aberta no BrzA Studio pelo `brza-sessions`, com cwd no `brza-workspace`.
- **O risco:** nenhum além de uma sessão a mais aberta no app.
- **Estado:** ativo.
- **Como desfazer:** fechar o chat no app.
