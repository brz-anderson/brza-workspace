---
scope:
  - brza-studio
tags:
  - release
  - chat
refs:
  - PLN-011
---

# O sync da v1.4.251 do upstream, que trouxe o cartão de arquivos alterados

O pedido de Anderson, em 2026-11-06: trazer ao BrzA Studio o cartão "N arquivos alterados +X" de cada turno do chat
(#38256, `e5a960cbf9f`), que está na `v1.4.251`, e o botão Hide com o switch "Changed files summary" (#38756,
`c5f1c590098`), que ainda está fora de tag. Na rodada da sessão `workspace`, a resposta foi "Sync da v1.4.251 + pick
(Recomendado)". Feito na sessão do workstream `studio`, no worktree `brza-studio/.worktrees/sync-v1.4.251`, como no
[sync da v1.4.246](2026-11-02-sync-da-v1-4-246-do-upstream.md). A `master` do `brza-studio` ficou congelada até o push.

## O que se fez

Push direto na `master` do `brza-studio`, `1ef93b3ba7f..cb573babbfd`:
- `c96b82cd77c`: "Merge tag 'v1.4.251'", com `--no-verify`, porque o lint-staged não aguenta o merge.
- `e2657324f3c`: "fix: finish the v1.4.251 sync". Leva o rebrand dos textos novos, o typecheck, o lint e as decisões da
  R2 e da R3.
- `397bbc0789c`: "fix: the v1.4.251 sync review findings".
- `3fd207da9b8`: o cherry-pick de `c5f1c590098` (`-x`), limpo.
- `687a967a5f0`: o catálogo de inglês de boot, regerado depois do pick.
- `cb573babbfd`: "fix(runtime): only a remote rewind waits on the capability check". Ver "O que a suíte pegou".

**O tamanho.** A `v1.4.251` estava 846 commits à frente. O upstream fez 8.018 renomeações e apagou 12 mil arquivos. A base
do merge foi `54ef0dea2045`, um commit do `main` deles. O merge deu 610 arquivos em conflito: 355 `UU`/`AA` e 255
`UD`, que são arquivos que o fork mudou e o upstream apagou.

**A resolução, por partes:**
- **Por script**, com o `classify_hunks.py` e o `merge_locales.py` da 246:
  - 169 arquivos em que o conflito era só rebrand;
  - 179 `UD` em que o fork só tinha rebrand, aceitos como apagados;
  - os catálogos de idioma, por merge de três vias;
  - o `package.json` fica com a versão `1.4.251` e o `build:mac` do fork no caminho novo.
- **Por área**, cinco `implementer` em paralelo, com um brief comum:
  - tema e settings;
  - contas e sessão;
  - interface do chat;
  - núcleo do chat;
  - build e identidade.

  Foram 248 arquivos. Os testes do fork que o upstream apagou foram portados para `brza/` quando a feature continua.
- **Depois:**
  - um `implementer` levou os 11 erros de typecheck e as decisões da R2;
  - outro fez a varredura do rebrand: 121 valores nos catálogos e cerca de 95 linhas em 60 arquivos;
  - um terceiro consertou o lint;
  - um `reviewer` fez a revisão adversária;
  - um `implementer` consertou os achados e as falhas novas da suíte.

**As rodadas**, todas respondidas por Anderson em 2026-11-06, pelo AskUserQuestion, nesta sessão:
- **R1, antes de congelar:**
  - PLN-011 × congelamento: "Sync agora; eu mesclo no 011 (Recomendado)";
  - decisões da 246: "Repetir as da 246 (Recomendado)".
- **R2, os pontos dos `implementer`:**
  - retomada automática no limite: "Upstream, ligado por padrão (Recomendado)";
  - modo inicial do Markdown: "'preview' na configuração (Recomendado)";
  - fonte do código no chat: "Seguir o editor (Recomendado)".
- **R3, os pontos do rebrand:**
  - saída de CLI de plugin: "Trocar para BrzA Studio (Recomendado)";
  - "renamed Orca skills", o segundo "Orca": "Volta a Orca (Recomendado)".

**Os pontos que a revisão propôs para rodada e a sessão resolveu pela regra das rodadas**, sem perguntar. A regra é: o
upstream vence na estrutura e no texto, e a feature do fork se porta por cima.
- R-A: o build local do Windows passa para `desktop-distribution/windows/`.
- R-B: o nome do executável e o do desinstalador do Windows vêm do `brand-identity.ts`.
- R-C: o link do diálogo de requisito do macOS fica o do upstream.
- R-D: os três textos que o lint tinha encurtado voltam ao texto do upstream, com a constante num módulo `brza/`.
- O relay do mobile fica com "Orca", pela decisão do mobile da 246.

## O que do fork caiu ou mudou

- **O P79 saiu.** O "Retomar automaticamente" passa a ser a retomada do upstream (`nativeChatAutoContinueAfterUsageLimit`,
  com o switch em Settings › Chat › Behavior). No BrzA ela vem ligada por padrão, também no perfil que não tem a chave.
  O agendador do fork (host, RPC, hook, componente, capacidades e chaves de idioma) foi removido. O "Continuar em outra
  conta" ficou, e cancela a retomada do upstream.
- **O Markdown abre na prévia** como o valor `'preview'` do `markdownDefaultViewMode` do upstream, que é o padrão no
  BrzA. Settings e o menu de contexto ganharam a opção "Preview".
- **A fonte do código no chat** segue a do editor, como no upstream. A do terminal era o comportamento antigo do próprio
  upstream.
- **O "Show more" do cartão de mensagem entre agentes** saiu, porque o upstream o tirou: o cartão agora nasce dobrado.
- **A estrutura nova do upstream:**
  - os três métodos do fork no adapter router foram para uma subclasse, `brza/brza-structured-agent-session-adapter-router.ts`,
    porque o arquivo do upstream já tem 300 linhas;
  - o tipo dos métodos foi para `brza/brza-adapter-methods.ts`;
  - os schemas do journal do fork foram para `journal/brza/`.
- **O build:**
  - a entrada da CLI e o `asarUnpack` seguem o `command-path-resolver` que o upstream moveu (A1). Sem isso, o
    `build:mac` parava, e um teste de contrato novo confere as duas listas;
  - o `build:win` aponta para o script movido.

## Os testes

- **Linha de base**, num worktree da `v1.4.251` pura:
  - typecheck com 0 erros;
  - lint com 2 passos vermelhos de 41, `check:code-quality:changed` e `lint:ast-grep-gates`;
  - suíte com 19 arquivos e 31 testes vermelhos em 11.036 arquivos, em 16 min.
- **Suíte inteira no sync**, no HEAD com o pick, `687a967a5f0`:
  - 19 arquivos e 32 testes vermelhos, sem `disk I/O error`;
  - 18 arquivos estão na lista da pura;
  - o `git-admission-storm-measurement`, que é instável sob carga, passou;
  - um arquivo era regressão do sync. Ver "O que a suíte pegou".
- **A suíte do meio**, em `e2657324f3c`, antes da revisão, tinha 27 arquivos vermelhos. Nove eram só do sync, e todos
  foram consertados em `397bbc0789c`.
- **No HEAD final:**
  - typecheck com 0 erros;
  - lint com os 2 vermelhos da pura, e o `ast-grep` só com os 4 achados do `filesystem-watcher` dela;
  - `pnpm build:electron-vite` com exit 0.
- **A suíte inteira não rodou de novo depois de `cb573babbfd`**, que muda 3 linhas. Rodaram o teste que falhava e os 139
  arquivos de `src/renderer/src/runtime/` e `launch-cancel-tombstones-compat/`, todos verdes.
- **O mobile** não foi tipado nem testado, porque as dependências dele não estão instaladas.

## O que a suíte pegou

O R-D levou a checagem do rewind a um helper `brza/` que fazia `await` em toda chamada de sessão estruturada. O microtask
a mais pôs o `agentSession.close` depois do `session.tabs.listAll` ao drenar um cancelamento restaurado, e o
`structured-agent-session-launch-cancellation.test.ts` falhava sempre, inclusive isolado.
- **A causa:** o teste passava em `e2657324f3c` e falhava em `397bbc0789c`, num worktree temporário `bisect-251`.
- **O conserto:** o `await` volta a acontecer só no rewind de ambiente remoto, como no upstream.

## O PLN-011

Pela R1, a `master` nova foi mesclada em `feat/pln-011-chat-cli`:
- `4edb2ebc4db` é o merge, com `--no-verify` e sem conflito de texto. Os três conflitos de CLI previstos sumiram, porque o
  sync já tinha juntado o rebrand.
- `f3cca185afa` leva dois imports de `src/cli/brza/` aos módulos que a 251 moveu.
- Typecheck com 0 erros. `src/cli` e os testes do PLN-011 deram 202 arquivos e 2.069 testes verdes.
- A branch foi enviada ao origin, onde ainda não existia.
- O C1 precisa de um app de dev recompilado a partir dela.

## O que ficou

- **A conferência no app**, com Anderson, num build da `master` em `cb573babbfd`:
  - o cartão "N arquivos alterados" aparece num turno com edição e expande a lista;
  - o Hide some com o cartão e mostra o toast;
  - o switch "Changed files summary", em Settings › Chat UI › Appearance, desliga e religa o cartão;
  - a retomada ligada por padrão no limite;
  - o Markdown abrindo na prévia.
- **Os 233 commits do `upstream/main` depois da `v1.4.251`**, menos o `c5f1c590098`, entram no próximo sync.
- **Os worktrees `sync-v1.4.251`, `base-v1.4.251` e `bisect-251` do `brza-studio`** ficam até o build conferir o merge.
- **O mobile** segue sem tipagem nem teste neste Mac.

## Fora do workspace

- **`pnpm install` com rede nos worktrees `sync-v1.4.251` e `base-v1.4.251` do `brza-studio`.**
  - **Onde:** o store global do pnpm, `~/Library/pnpm`, com os pacotes que a 251 pede.
  - **Risco:** nenhum para os outros checkouts; o store só cresce.
  - **Estado:** ativo.
  - **Como desfazer:** `pnpm store prune`.
- **Branch `feat/pln-011-chat-cli` no origin (`brz-anderson/brza-studio`)**, criada pelo push do merge.
  - **Risco:** nenhum.
  - **Estado:** ativo.
  - **Como desfazer:** `git push origin --delete feat/pln-011-chat-cli`.
- **Link `/private/tmp/brza-sync-251`**, para o scratch da sessão. Guarda os briefs, as devoluções, as rodadas, os logs
  das suítes e a revisão.
  - **Risco:** nenhum; some no reboot.
  - **Estado:** ativo.
  - **Como desfazer:** `rm /private/tmp/brza-sync-251`.
- **`/tmp/rv251/`**, os scripts de leitura do `reviewer`.
  - **Risco:** nenhum.
  - **Estado:** ativo.
  - **Como desfazer:** `rm -r /tmp/rv251`.
