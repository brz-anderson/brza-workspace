---
scope:
  - brza-studio
---

# Os blocos de 120 colunas na largura "Total" e os links em azul claro no chat

O P52 e o P53 do [PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat](../../plans/PLN-001-o-brza-studio-generico/PLN-001-plan.md),
executados em 2026-10-27 na sessão `brza-studio-chat-blocos-120-colunas`, a partir do pedido da sessão `fixfy-9b`.
Commits `f130a85e578`, `9d289d2b631` e `52f7051a45d` na `master` do `brza-studio`. A evidência detalhada está nos
passos do plano.

## O que Anderson respondeu

- **Alinhamento** do bloco de 120 colunas quando sobra espaço: à esquerda, com o texto.
- **Outros elementos na regra:** o diff de edição e, numa segunda rodada, os diagramas e visuais (o Mermaid e o
  visual inline). A saída de ferramenta fica de fora. Os visuais vieram de uma outra sessão com a mesma tarefa
  (`brza-studio-chat-markdown-largura-e-links`), que relatou a resposta. Anderson a confirmou nesta sessão antes da
  implementação.

## O que se fez

- Uma regra só do BrzA, `brza-chat-wide-blocks.css`, sob `@container style(--chat-width: full)`. O upstream ganhou o
  `--chat-width` no `nativeChatAppearanceStyle`, a moldura da tabela e atributos `data-native-chat-*` no diff e no
  visual inline.
- Toda moldura tem a mesma borda externa: 120 colunas da fonte de código, mais o `px-3.5` do bloco, mais 2px de borda.
- O `--chat-link` em `brza-chat-link.css`, `#79c0ff` no escuro e `#0969da` no claro, seguindo o esquema do chat também
  no modo "igualar ao terminal".

## O que se aprendeu

- **`120ch` não dá 120 colunas no chat.** O `body` tem `letter-spacing: 0.01em`, herdado como 0,16px, e o `ch` não o
  conta: o avanço real é de 7,385px, e não 7,225px, e o bloco mostrava ~117 colunas. Uma régua `::before` de altura zero,
  com 120 zeros na fonte de código, mede o avanço real.
- **A ordem entre CSS importados por módulos diferentes não é garantida.** Por isso a cor do link se troca na própria
  linha upstream, e não por uma regra de mesma especificidade que dependesse de vir depois.
- **O Chromium do Electron 43 tem `@container style()` de propriedade customizada e `attr()` tipado**, e é com eles que
  a regra se liga e se desliga sem tocar no React.

## O que ficou aberto

- A conferência no BrzA Studio com Anderson, na largura "Total" (P52.4 e P53.3): um bloco curto e um longo, uma tabela,
  o painel estreito e o link nos dois temas.
- O visual inline não foi medido, porque precisa de runtime.

## Fora do workspace

- **O quê e onde:** os commits `f130a85e578`, `9d289d2b631` e `52f7051a45d`, com push na `master` de
  `brz-anderson/brza-studio`. **Risco:** mudam a aparência do chat na largura "Total" e a cor dos links para todos os
  builds feitos da `master`. **Estado:** ativo. **Como desfazer:** `git revert` dos três commits, com push.
- **O quê e onde:** o worktree `~/Projects/brza-studio/.worktrees/chat-markdown-largura-e-links` e a branch
  `feat/chat-markdown-largura-e-links`. **Risco:** nenhum. **Estado:** removidos no fim. **Como desfazer:** nada a
  desfazer.
- **O quê e onde:** as screenshots da fixture temporária, em `.cache/fixtures/` do worktree, e um protótipo no
  scratchpad da sessão. **Risco:** nenhum. **Estado:** a fixture não foi commitada; o `.cache` saiu com o worktree.
  **Como desfazer:** nada a desfazer.
