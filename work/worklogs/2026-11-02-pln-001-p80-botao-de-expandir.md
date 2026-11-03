---
scope:
  - brza-studio
tags:
  - chat
refs:
  - PLN-001
---

# O P80 do PLN-001, o botão de expandir com a aparência e a fileira dos vizinhos

O pedido 42, de Anderson: "esse também, deixe o botão de expandir da mesma cor que o restante e corrija o alinhamento",
com a imagem de um bloco de código do chat sem cabeçalho: o ⤢ com fundo escuro e borda, sobre a borda de cima do
bloco, fora da fileira do quebrar e do copiar. A sessão `pln-001-pedido-42` executou o P80 pelo D63, no worktree
`~/Projects/brza-studio/.worktrees/pln-001-pedido-42`, branch `fix/pln-001-pedido-42`, sem rodada.

## A leitura do D63

A leitura de `brza-studio@9a8631369ac` se sustentou no código, com as linhas um pouco deslocadas. Os três pontos "A
conferir no passo":

- **Como achar o grupo de ações:** um atributo `data-native-chat-code-actions` nos dois contêineres do
  `NativeChatCodeBlock.tsx`. O arquivo já carrega linhas do BrzA, e o atributo dá conflito visível num sync, enquanto o
  "pai do primeiro botão" quebraria calado se o upstream embrulhasse um botão.
- **O grupo que some fora do hover:** o ⤢ é portado ao `body`; apontar para ele tira o hover do bloco, e o quebrar e o
  copiar sumiriam. Enquanto o ⤢ aparece, o bloco leva `data-brza-expand-shown`, e um CSS do BrzA mantém o grupo aceso; os
  dois somem juntos.
- **A tela cheia** (`BrzaExpandOverlay`) não mudou.

## O que mudou

`brza-studio@d501bb230ff`, na `master`: o ⤢ com as classes do copiar, sem borda, fundo nem sombra; a posição medida no
grupo de ações (o topo dele, e 2 px + 24 px à esquerda), com e sem cabeçalho e com o executar; o bloco sem grupo (saída
de ferramenta, diff) no canto de dentro, a 4 px. Arquivos: `BrzaExpandLayer.tsx`, `BrzaExpandLayer.test.tsx` (5 testes
novos, com o `NativeChatCodeBlock` real), `NativeChatCodeBlock.tsx` (o atributo, duas linhas) e o novo
`brza/brza-expand-button.css`.

## Desvios

- **X78 — A reserva de 90 px no bloco sem cabeçalho.** O `pr-16` do `pre` cabia só no quebrar e no copiar; com o ⤢ na
  fileira, a primeira linha longa ficaria sob ele, e o C33 pede "sem cobrir texto". O CSS do BrzA reserva mais 26 px só
  no bloco sem cabeçalho (`:first-child`; o `:has()` foi barrado pela verificação de restyle do `check:changed`).
- **X79 — O ⤢ some quando o ponteiro sai do chat.** O teste do próprio botão no `mouseover` da raiz nunca disparava (o
  botão vive fora dela); a raiz agenda o sumiço no `mouseleave`, e o botão o cancela no `mouseenter`.
- **X80 — O `oxfmt` e o `oxlint` diretos não acharam os arquivos do worktree** com os caminhos juntos. O `oxfmt --check`
  passou arquivo por arquivo; o lint que vale é o do `lint-staged` do commit e o do `check:changed`. A suspeita, não
  confirmada, é o `.worktrees/` do `.git/info/exclude`.

## O que rodou

- Antes do código, os 5 testes novos falharam; depois, `pnpm test` por caminho com `--maxWorkers=2` no
  `BrzaExpandLayer.test.tsx`, no `NativeChatCodeBlock.test.tsx` e no `NativeChatCodeBlock.load-failure.test.tsx` → 26
  passaram.
- `pnpm tc:web` → sem erro. `pnpm check:changed --base=origin/master --maxWorkers=2` → 24 de 24.
- Uma fixture local, fora do commit e apagada, nos temas claro e escuro: o ⤢ transparente na fileira, à esquerda do
  quebrar e do copiar, no bloco sem cabeçalho, no de `ts` e no de `bash` com o executar.
- Suíte inteira: roda depois do push, pela coordenação.

## O que ficou aberto

- **O C33**, de Anderson, num build novo: o build instalado não tem este commit.

## Fora do workspace

- O `brza-studio` ganhou o commit `d501bb230ff` na `master`, com push direto para `brz-anderson/brza-studio`
  (`9a8631369ac..d501bb230ff`).
- O worktree `~/Projects/brza-studio/.worktrees/pln-001-pedido-42` e a branch `fix/pln-001-pedido-42` ficaram.
