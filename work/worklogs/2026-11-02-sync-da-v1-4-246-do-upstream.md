---
scope:
  - brza-studio
date: 2026-11-02
tags:
  - release
  - chat
---

# O sync da v1.4.246 do upstream, que tirou o chat do experimental

O pedido de Anderson, em 2026-11-02: trazer ao fork a última versão do upstream (`stablyai/orca`), a que tirou o modo
de chat do experimental (#36110). Feito na sessão `studio-75`, no worktree `brza-studio/.worktrees/sync-v1.4.246`.
A `master` do `brza-studio` ficou congelada para o
[PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat](../../plans/PLN-001-o-brza-studio-generico/PLN-001-plan.md)
até o push. Pela coordenação com a sessão `studio-89`, só ela grava no PLN-001.

## O que se fez

Push direto na `master` do `brza-studio`, `abc5e78c243..a70f63b6a92`:
- `1cf5d4bb6cf` — "Merge tag 'v1.4.246'". O lint-staged do pre-commit nos 18 mil arquivos do merge foi morto, e o
  commit saiu com `--no-verify`; o lint completo rodou depois.
- `a70f63b6a92` — "fix: finish the v1.4.246 sync". O rebrand, o lint e as correções da revisão, com o hook.

**O tamanho.** A v1.4.246 estava 1.554 commits à frente do último sync (`c98a2d639c7`), e o merge deu 404 arquivos em
conflito. 293 deles vinham do commit de rebrand `b2918daf60b`, que trocou "Orca" por "BrzA Studio" em 2.151 arquivos.

**A resolução, por partes:**
- **Rebrand:** um script comparou cada trecho diff3 com a base e resolveu os 1.393 trechos que só tinham o rebrand. O
  resultado é o texto do upstream com a mesma troca, em 195 arquivos.
- **Idiomas:** os catálogos entraram por merge de três vias, chave a chave. Nas 19 chaves em que os dois lados mudaram,
  ficou o texto do upstream.
- **Apagados pelo upstream:** os 73 arquivos foram aceitos como apagados. Os casos de coexistência e do P36 foram
  portados para testes em `brza/`.
- **#34824:** o cartão de mensagem entre agentes, que tinha entrado por cherry-pick, ficou com a versão do upstream.
- **Os 119 arquivos com features do fork:** quatro `implementer` em paralelo, um por área — tema e editor; contas e
  sessão; chat e mensagens; build, identidade e coexistência.
- **Rebrand dos textos novos do upstream:** um `implementer`, em todos os catálogos do desktop e nas strings do código.
- **Correções de lint e dos 6 testes:** dois `implementer`.
- **Revisão adversária:** um `reviewer`.

**As rodadas**, todas respondidas por Anderson em 2026-11-02, pelo AskUserQuestion, nesta sessão:
- **R1.**
  - Alvo: "Tag v1.4.246 (Recomendado)".
  - Textos novos com Orca: "Tudo agora".
  - P40 × #31241: "Fica o do upstream (Recomendado)".
  - P36 × #30955: "Mantém o P36 (Recomendado)".
- **R2.**
  - P36 × troca global: "O pino vence (Recomendado)".
  - Match Terminal: "O que o terminal mostra (Recomendado)".
  - Hooks no desinstalador NSIS: "Pular a remoção (Recomendado)".
  - Extras: "Temas de plugin no chat" e "brza-studio://plugins".
- **R3.**
  - Mobile: "Deixar Orca (Recomendado)".
  - Caminho no Windows: "Encurtar a pasta para BrzA (Recomendado)".
  - Refinamentos do rebrand: "Alemão com hífens" e "Linhas dos geradores".
  - Link do P71: "Fica como os outros links (Recomendado)".
- **R4.**
  - Limite no chat fixado: "Seletor do chat (Recomendado)".
  - Login no chat fixado: "Issue, fora do sync (Recomendado)".

## O que do fork caiu ou mudou

- **P40 saiu.** Foram removidos o `BrzaContinueInOtherAccount`, o teste dele e a chave `continueInOtherAccount`. A linha
  do limite ficou com o `NativeChatUsageLimitActions` do upstream e o nosso "Retomar automaticamente".
- **P36 ficou, e o pino vence.**
  - O chat fixado lança e lista modelos na conta do pino (`pinnedClaudeAccountHome`), e a troca limpa o
    `acquiredAccount`.
  - Na linha do limite, o chat fixado usa a troca por chat (`brza/BrzaPinnedAccountSwitch.tsx`); o sem pino usa o
    seletor global.
- **O tema do chat (P58 ao P60).**
  - O "Match Terminal" segue o tema do chat quando o terminal segue o chat.
  - Os temas de terminal de plugin entram no seletor do chat.
  - A junção tinha perdido os overrides de cor do terminal por cima do tema do chat, e eles voltaram como o D46 manda.
- **Islands Dark:** passa a ser o fallback do `useMonacoTheme` do upstream, para todas as superfícies.
- **P71:** o link http da prévia de Markdown abre pelo dono, para passar no gate de leitura de foco do upstream. Sem
  dono, não abre, como os outros links do chat.
- **P62 ao P64:** o leitor de peer, o "Hand-back from" e o clique no remetente foram portados por cima do cartão do
  upstream.
- **Coexistência.**
  - O `orca-protocol-registration.ts` do upstream registrava o `orca://` no Windows; agora usa o esquema do BrzA.
  - O `brza-studio://plugins` passa a ser aceito.
  - A pasta do daemon no Windows passa a `%LOCALAPPDATA%\BrzA`, do tamanho de `Orca`, para o caminho caber no orçamento
    do conpty. O desinstalador limpa também a pasta antiga.
  - O desinstalador não remove mais os hooks de `~/.orca`, que são compartilhados com o Orca original.
- **Rebrand.** O desktop é BrzA Studio em todos os catálogos, inclusive os novos de, ru, tr e zh-Hant.
  - Fica Orca: o mobile, o texto para agentes e as linhas que alimentam os guias de plugin e de skill embarcados.
- **Achados da revisão, corrigidos.**
  - A estrela do GitHub apontava para `brz-anderson/orca`, que não existe.
  - O filtro de processos do desinstalador não casava com a pasta nova.
  - O `verify-dev-channel-packaging.mjs` esperava `orca-*` e reprovaria o build dev no CI.

## Os testes

- **Linha de base:** a suíte e o lint também rodaram num worktree da v1.4.246 pura.
- **Suíte inteira:** no fim, 25 arquivos falham (50 testes), contra 39 na pura. Os 25 também falham na pura.
  - A primeira rodada deu 979 `disk I/O error` do SQLite, que não voltaram. Eram da carga das rodadas em paralelo.
- **Typecheck:** 0 erros.
- **Lint:** 3 passos vermelhos, que também falham na pura (`check:test-file-runners`, `lint:ast-grep-gates`,
  `check:path-literal-ratchet`).
- **Mobile:** não foi tipado nem testado, porque as dependências dele não estão instaladas.
- **Tempo:** a suíte inteira leva cerca de 16 min neste Mac (M5 Pro, 15 núcleos), com a máquina livre.

## Para o PLN-001

A `studio-89` encerrou antes do push, e o relatório que ela pediu fica aqui:
- **O passo do sync:** os commits, as rodadas acima e os testes.
- **P40 e C14 como `[-]`:** pela R1, "Fica o do upstream (Recomendado)".
- **Desvios:** a seção "O que do fork caiu ou mudou".
- **O build dos casos manuais:** o C1 ao C24 (menos o C14), o P57, o P61 e o P65 podem ser conferidos num build só, a
  partir da `master` em `a70f63b6a92`.

## O que ficou

- **Issue nova:** [O chat fixado numa conta pelo P36 entra na conta global](../issues/chat-fixado-na-conta-entra-na-conta-global.md).
  O defeito já existia antes do merge.
- **Os 233 commits do `upstream/main` depois da v1.4.246** entram no próximo sync.
- **O worktree `brza-studio/.worktrees/sync-v1.4.246`** fica até o build conferir o merge.

## Fora do workspace

- **`pnpm install` com rede, no worktree de sync do `brza-studio`.**
  - **Onde:** baixou ao store global do pnpm, `~/Library/pnpm`, os pacotes que a v1.4.246 pede.
  - **Risco:** nenhum para os outros checkouts; o store só cresce.
  - **Estado:** ativo.
  - **Como desfazer:** `pnpm store prune`.
- **Checkout raiz do `brza-studio` na `master` nova (`a70f63b6a92`), por fast-forward.**
  - **Risco:** o `node_modules` dele ficou com as dependências da versão anterior, e o build ou os testes dali falham
    até o `pnpm install`.
  - **Estado:** pendente o `pnpm install` no checkout raiz.
  - **Como desfazer:** rodar `pnpm install` no checkout raiz.
- **Link `/private/tmp/brza-sync`, para o scratch da sessão.**
  - **Risco:** nenhum; some no reboot.
  - **Estado:** ativo.
  - **Como desfazer:** `rm /private/tmp/brza-sync`.
