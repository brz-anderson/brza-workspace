---
scope:
  - workspace
  - brza-studio
refs:
  - PLN-003
  - issue:skills-de-documento-do-workspace-de-origem-num-plugin
---

# O PLN-003: o Terreno do plugin do Orca na 1.4.246

Pedido de Anderson, vindo da sessão `brand` em 2026-11-02: "verifique como funcionam os plugins adicionados nessa ultima versão do Orca (upstream), pode mudar os planos futuros que temos". Ele respondeu "Sessão no tools-kit (Recomendado)" para onde registrar o que o levantamento mudou. O levantamento foi de um `collector` só de leitura sobre o `~/Projects/brza-studio` (tag `v1.4.246` e `upstream/main`), com 116 fatos marcados, no scratch, fora do git.

## O que se fez

- **[`PLN-003-design.md`](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-design.md), seção "O plugin do Orca":** reescrita contra a `v1.4.246`, com `Fnn` e arquivo em cada ponto. Seis linhas do Terreno de 2026-10-29 estão marcadas "envelheceu":
  - o canal worker↔painel existe (`plugin.request`, `orca.panels.handle/post`), nos painéis HTML e nos TSX;
  - o `terminal.sendText` é só do worker na 1.4.246 (`plugin-host-api.ts:146-155`), e era do painel na 1.4.244. Isto o pedido não dizia: os botões da R1.2 exigem worker;
  - o frame isolado vem ligado (`plugin-frame-isolation.ts:9`), e o `connect-src 'none'` ficou só no `srcdoc`;
  - o fork lê manifesto 2, e o `engines` do plugin passa a `>=1.4.246`;
  - `storage:own`, `secrets:own` e `settings:own` já são os nomes da 1.4.246;
  - os eventos viraram `workspace.created`, `workspace.removed`, `agent.status.changed` e `workspace.changed`.
- **O limite do worker no host**, o que só existe no `upstream/main` (`engines.orca >=1.4.248`, que não carrega no fork) e o que segue reservado e vazio (`skills`, `mcpServers`, `agentHarnesses`, `taskSources`) estão no Terreno, com a segurança do `trusted-worker` para a análise de risco da fase 0.
- **O C5 (UI nos dois apps) virou hipótese a medir no P0**, com o spike de sete perguntas escrito no próprio C5. B7, M17 e a R1.2/R4.2 da lista de premissas ficaram marcados "em revisão".
- **Issue [As skills de documento do workspace de origem num possível plugin do BrzA](../issues/skills-de-documento-do-workspace-de-origem-num-plugin.md):** acrescentado o fato de que o plugin do Orca não contribui skills (reservado e vazio), então o veículo é o plugin do Claude. O gatilho não mudou.
- **O `Retomar` do [PLN-003](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-plan.md)** manda retomar pelo spike do C5.

## A decisão de Anderson

Rodada sobre qual caminho o spike mede, respondida em 2026-11-02: **"Medir os dois: HTML+worker e TSX+worker (Recomendado)"**. Vale como a escolha do que o spike mede; não fecha R1.2 nem o painel. O `DESIGN.md` da R6.2, que descreve o painel HTML, não vale para o painel TSX, e fica para depois do spike.

## O que não foi testado

Nada rodou em app: o painel, o `plugin.request`, o `terminal.sendText` do worker, o alcance do `127.0.0.1`, o `plugin shot` na sessão do chat do Studio. O "o painel não alcança o MCP residente" é inferência (80), pelo proxy de loopback do frame. O `~/.orca` e o `devPluginPaths` não foram relidos; o `[]` nos dois apps é de 2026-10-29.

## Retomar

O spike do C5, num plugin mínimo `trusted-worker` com dois painéis, em pasta dev, nos dois apps. Fica no `Retomar` do PLN-003. A issue dos restos da Orca e a decisão sobre `onorca.dev` são da sessão `brand`; o sync com o `upstream/main` não foi pedido.
