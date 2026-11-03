---
scope:
  - brza-studio
tags:
  - chat
  - auth
refs:
  - PLN-001
  - issue:o-fork-de-um-chat-fixado-abre-na-conta-global-e-sem-contexto
---

# P74: o fork de um chat fixado nasce na conta fixada

O P74 do PLN-001, do pedido 39 (R65.1), feito pela sessão `pln-001-pedido-39-fork` no worktree
`.worktrees/pln-001-pedido-39-fork` do `brza-studio`. Commit
[`bdb2b55be14`](https://github.com/brz-anderson/brza-studio/commit/bdb2b55be14), na `master`, com o push direto
(`f7490afab9e..bdb2b55be14`). A issue é
[O fork de um chat fixado abre na conta global e sem o contexto](../issues/o-fork-de-um-chat-fixado-abre-na-conta-global-e-sem-contexto.md).

## O que se fez

- **Os "A conferir no passo" do D57, lidos no código antes de escrever.** A leitura se sustentou no essencial (o defeito,
  o fluxo e o remédio da R65.1), e nada voltou como pergunta; mas a fiação é maior que a do D57 (X74, X75). Nada além do
  lançamento lê o `accountSwitch` na criação, e o lançamento já seguia o pino. O `leafUuid` ausente é, sim, um caminho
  silencioso em outro fluxo de adoção, o import de chat do CLI: virou uma issue nova, sem código.
- **O código.** O resultado do `forkThroughMessage` nomeia o pino da origem; o renderer o passa em
  `resumeFrom.accountSwitch`; o host prepara a conta (`claudeReadyAccountPin`, extraído do `claudePrepareAccountSwitch`),
  grava o `accountSwitch` no registro adotado e escreve o divisor "Conta trocada" junto da importação. Conta removida ou
  sem preparo recusa o create.
- **Os testes, antes do código.** Falharam os do renderer (2 casos), o do fork no host (2) e o do `attach` adotado (1);
  entram verdes o do resolvedor do pino e o do lançamento do fork pinado, porque o lançamento já seguia o pino. Depois:
  116 passed nos tocados; 97 arquivos, 761 passed nos vizinhos, por caminho.
- **Os gates.** `pnpm tc`, oxlint e oxfmt verdes, antes e depois do rebase. `pnpm check:changed`: 29 de 30; o passo de
  testes de unidade estourou os 30 min (X76). Suíte inteira: roda no merge, pela coordenação.

## Desvios

- **X74 — o registro adotado nasce no `reserveOwner`, e o divisor entra na importação.** O D57 apontava o `create-support`.
- **X75 — o pino vem do host, no resultado do fork, e viaja só como `accountId`.** Sem capability nova; host antigo segue
  como antes.
- **X76 — o `check:changed` estourou no passo de unidade; rodei por caminho.**

## O que ficou aberto

- **O C27 é de Anderson, no build novo, e não está marcado.** A issue fica `open` até lá.
- **Um chat adotado sem pino, como o import do CLI, ainda abre em branco** quando o transcript está noutra conta que a
  selecionada. Issue nova, com a decisão de Anderson (pinar na adoção, ou avisar com `historyInOtherAccount`). Não rodei o
  import ponta a ponta.
- **O `tests/e2e/helpers/persisted-profile-state.unit.test.ts` (bun) apareceu vermelho** na única rodada larga do
  `check:changed`; não toquei nesse caminho, e a coordenação o vê na suíte inteira.
