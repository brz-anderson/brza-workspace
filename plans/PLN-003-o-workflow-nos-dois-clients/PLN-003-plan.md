---
status: open
phase: design
origin: request
ready: não — faltam os itens D, os Passos e a medição da fase 0 (R7.3)
scope:
  - workspace
  - brza-studio
opened: 2026-10-29
owner: Anderson
tags:
  - tooling
---

# PLN-003: O workflow do workspace roda igual no BrzA Studio e no Orca, por plugins e pelo `brza`

- **Retomar:** a Entrevista fechou nas rodadas 1 a 7. O próximo é escrever os itens `D` a partir da matriz do
  Desenho, com os riscos da fase 0 como hipóteses (R7.3), e depois os Passos, com o P0 numa sessão `pln-003-p0`. O P7
  do PLN-002 corre na sessão `pln-002-p7`.
- **Mudou a norma (2026-10-29):** a trava de retomada saiu, e a sessão passou a ser por frente, não por tarefa
  ([Uma sessão por frente de trabalho, sem trava de retomada e com o cache de 1 h](../../work/decisions/uma-sessao-por-frente-e-sem-trava-de-retomada.md)). O Desenho ainda conta com a
  trava no roteador (M2) e na tabela de conflitos (`PLN-003-design.md:181-182`): ajustar antes dos itens `D`.
- **Dividido:** [PLN-003 — Entrevista](PLN-003-interview.md) · [PLN-003 — Desenho](PLN-003-design.md)

## Pedido

- **Origem:** pedido livre, no chat do BrzA Studio de 2026-10-29. Relaciona-se com o
  [PLN-002](../PLN-002-os-comandos-brza/PLN-002-plan.md), sem depender do P7 dele (R1.4).

"vamos criar um plugin do Orca para o Workspace e um plugin do Claude + MCP para o Workflow e ajustar a CLI `brza` para
que o workflow funcione tanto no client `BrzA Studio` quanto no `Orca`" — Anderson, em 2026-10-29.

Os itens do pedido, numerados para a Cobertura:

1. o plugin do Orca para o Workspace;
2. o plugin do Claude com o MCP para o Workflow — o fluxo do workspace e o recurso Workflow do Claude Code (R1.1);
3. a CLI `brza` ajustada para o workflow funcionar no BrzA Studio e no Orca;
4. a CLI instala e atualiza o app, o plugin do Orca, o plugin do Claude e o MCP, e inicia e para o MCP; e é ela mesma
   instalável por `npm`, `npx`, `pnpm`, `brew`, `pip` e `winget`.

"o `BrzA CLI` deve conseguir instalar/atualizar o app `BrzA Studio`, o plugin do `Orca`, o plugin do `Claude`, o MCP -
iniciar/parar tbm -, como fazemos para que o CLI possa ser instalado com `npm|npx|pnpm|brew|pip|winget install`?" —
Anderson, em 2026-10-29, na mesma sessão.

### Cobertura

> Rascunho: os critérios são propostas até a rodada que os confirma; o passo e o teste saem do Desenho.

| Origem     | Critério de aceite                                                                                      | Passo | Teste (nível) |
| :--------- | :------------------------------------------------------------------------------------------------------ | :---- | :------------ |
| `Pedido 1` | o mesmo `orca-plugin.json` instala nos dois apps e mostra o painel do workspace com planos e notas abertos | —     | —             |
| `Pedido 1` | os comandos do plugin mandam o `brza` certo ao terminal do worktree em foco                             | —     | —             |
| `Pedido 2` | o plugin do Claude traz as skills, os hooks e o MCP do workspace, e sobe nos chats dos dois apps          | —     | —             |
| `Pedido 2` | o plugin traz roteiros de Workflow do Claude Code para o fluxo do workspace                               | —     | —             |
| `Pedido 4` | `pipx install brza` e `brew install brz-anderson/tap/brza` instalam o CLI, com o `brza` e os `brza-*` no PATH | —     | —             |
| `Pedido 4` | `brza app install` baixa o DMG da release e troca o app; `--from-source` compila da `origin/master`            | —     | —             |
| `Pedido 4` | `brza mcp start`, `stop` e `status` controlam o servidor residente                                           | —     | —             |
| `Pedido 3` | `brza <sub>` acha o app que está rodando — BrzA Studio ou Orca — sem caminho fixo                        | —     | —             |

## Worklogs

- 2026-10-29 — aberto; R1 a R7 fecharam a Entrevista; o Terreno e a matriz foram ao Desenho; o P7 saiu à sessão
  `pln-002-p7`. Parou antes dos itens `D`.
  [O PLN-003: a entrevista do workflow nos dois clients](../../work/worklogs/2026-10-29-pln-003-a-entrevista-do-workflow-nos-dois-clients.md)

