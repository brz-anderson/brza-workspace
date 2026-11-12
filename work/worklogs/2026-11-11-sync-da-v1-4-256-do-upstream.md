---
scope:
  - brza-studio
tags:
  - release
  - chat
refs:
  - PLN-011
  - PLN-014
  - PLN-019
  - PLN-021
  - issue:o-teste-da-cli-empacotada-falha-na-ci-linux-do-fork
sessions:
  - 5f596faf-ab1f-41f4-91fc-9ab63eb31c3a
---

# O sync da v1.4.256 do upstream, que tirou o Bifurcar do fork

O pedido de Anderson, em 2026-11-11: "iniciar sync com o upstream, leia as notas e planos do workstream/playground".
Feito na sessão do workstream `studio`, no worktree `brza-studio/.worktrees/sync-v1.4.256`, na branch `sync/v1.4.256`,
como nos syncs da [v1.4.246](2026-11-02-sync-da-v1-4-246-do-upstream.md) e da
[v1.4.251](2026-11-06-sync-da-v1-4-251-do-upstream.md). A `master` do `brza-studio` ficou congelada até o push.

## O que o `playground` disse para o sync

- **O radar não rastreia versão, só número de PR.** O último ciclo, de 2026-11-11 0h BRT, viu até o #40986. As issues
  do `playground` citam 91 PRs que estão na `v1.4.256` e 15 que estão só no `upstream/main`.
- **O PLN-014 do `playground` barra o porte à mão e a emenda das quinze issues, não o sync**: "merge no upstream não é
  patch". Nenhuma nota do `playground` mudou.
- **O checklist que veio de lá**, conferido no merge:
  - a issue de CI ("Resultados de CI no chat e disparo automático de agentes em falhas de PR") pede o
    `NativeChatPullRequestEventLine` em `src/`: chegou, com a fixture e a montagem no `NativeChatNoticeRow`;
  - o PLN-021 lê `src/renderer/src/assets/main.css:194` e `mobile/src/theme/mobile-theme.ts`: o primeiro mudou
    (+156/−14), o segundo ganhou 5 linhas, e o script de deriva do plano vai avisar;
  - o PLN-019 cita `src/main/runtime/startup-dialog-blocked-signals.ts`, que o #39625 moveu para
    `src/main/runtime/terminal/wait/`.

## O que se fez

Push direto na `master` do `brza-studio`, `049a890a837..2b490c84526`, por fast-forward da branch `sync/v1.4.256`:
- `5c35b1dc6e6`: "Merge tag 'v1.4.256'", com `--no-verify`.
- `9461440a3a2`: "fix: finish the v1.4.256 sync". Leva o rebrand dos textos novos, o typecheck, o lint e as decisões da
  R2.
- `8f24e43dc6e`: "fix: the v1.4.256 sync review findings", as decisões da R3.
- `7042258b9a2`: dois testes de contrato do fork atrás dos movimentos da 256.
- `e3bc8f04009`: o bundle web do mobile sem as tabelas de idioma do `zod`.
- `2b490c84526`: a CLI acha os subcomandos externos no PATH sem o resolver do `main`, e o teste de troca de conta do
  fork fecha os bancos do journal antes de apagar a pasta. Ver "O que a CI pegou".

**O tamanho.** A `v1.4.256` estava 1.103 commits à frente; a base do merge foi `7634d08f743` (`v1.4.251~5`). O upstream
moveu cerca de 4,6 mil arquivos e apagou 5,3 mil. O merge deu 796 arquivos em conflito: 518 `UU`/`AA` e 278 `UD`.

**A resolução, por partes:**
- **Por script**, com o `classify_hunks.py`, o `classify_ud.py` e o `merge_locales.py` dos syncs anteriores:
  - 341 arquivos em que o conflito era só rebrand;
  - 219 `UD` em que o fork só tinha rebrand, aceitos como apagados;
  - os cinco catálogos de idioma, chave a chave; 10 chaves ficaram com o valor do fork quando o rebrand elidia
    ("d'Orca", "Orca가") e foram refeitas à mão;
  - o `package.json`, na versão `1.4.256`.
- **Por área**, cinco `implementer` em paralelo, com um brief comum: a interface do chat (37), o resto do renderer
  (55), o `src/main` (54), shared, CLI e config (26) e os `UD` com feature (59).
- **Depois**, três `implementer` em paralelo — o Fork, o conserto e a varredura do rebrand —, um `reviewer` e um
  `implementer` para os achados.

**As rodadas**, todas respondidas por Anderson em 2026-11-11, pelo AskUserQuestion, nesta sessão:
- **R1, antes de começar:**
  - alvo: "v1.4.256 (Recomendado)";
  - conferência que ficou da 251: "Junto, no build da 256 (Recomendado)";
  - worktrees dos syncs anteriores: "Remover ao fim deste sync (Recomendado)";
  - PLN-011: "Mesclar ao fim do sync (Recomendado)".
- **R2, os pontos dos grupos:**
  - Fork: "Só o do upstream, com o P74 (Recomendado)";
  - helper do rewind: "Apagar o helper (Recomendado)";
  - Islands Dark: "Acrescentar, com teste (Recomendado)";
  - seleção do chat com tema de terminal: "Portar agora".
- **R3, os achados da revisão:**
  - imagem de tool-result: "A leitura espera a escrita (Recomendado)";
  - resíduo do Bifurcar: "Apagar o resíduo agora (Recomendado)";
  - CLI de plugins: "Não: rebrandar (Recomendado)".
- **R4, o fechamento:**
  - push: "Logo depois da CI, conferir na master";
  - o desvio da imagem (abaixo): "Aceitar o desvio (Recomendado)".

**Sem rodada, pelas decisões dos syncs anteriores:** a saída para agentes de plugins e orquestração e o nome do tema
gravado no settings do Claude Code ficam "Orca" (texto para agentes, marcador gravado em arquivo do usuário).

## O que do fork caiu ou mudou

- **O Bifurcar saiu.** O "Fork from this response" do upstream (#38326 e seguintes) faz o mesmo. O P74 — o fork de um
  chat fixado abre na conta dele — passou para o Fork do upstream, em `src/main/native-chat/brza/brza-fork-account-pin.ts`
  e duas linhas em `structured-agent-session-fork.ts`, com teste. Saíram também o RPC `agentSession.forkThroughMessage`,
  o `resumeFrom.accountSwitch`, o `structured-session-adoption-account-pin.ts` e o divisor "Account switched" do fork, que
  o Fork do upstream não traz.
- **O helper do rewind saiu**: a 256 já faz o que o `cb573babbfd` fazia.
- **O pick do #38756** (Hide do cartão de arquivos alterados) deu lugar ao do upstream. O switch "Changed files summary"
  está agora em Settings › Chat.
- **O Islands Dark** ganhou as regras escuras de Markdown do Monaco, num módulo `brza/`, com teste.
- **O chat com tema de terminal** ganhou a seleção legível e o reset dos tokens de texto do #39432.
- **A imagem de tool-result** passou a ser gravada sem bloquear, por causa do ratchet novo de fs síncrono; a leitura
  espera a escrita pendente. **O desvio aceito na R4:** na falha de escrita, o bloco ainda nasce, e a leitura dá erro
  explícito, porque o decoder do upstream é síncrono.
- **O `ad-hoc-signed-build.ts`** ganhou +1 no `config/main-sync-fs-baseline.txt`, com o aval do revisor.
- **Os schemas `shared` do fork** importam `* as z` de `zod`; o `{ z }` levava as tabelas de idioma ao bundle web do
  mobile, e o build do Mac parava.

## Os testes

- **Linha de base na `v1.4.256` pura, no Mac:**
  - lint com 2 passos vermelhos de 44, `check:code-quality:changed` e `lint:ast-grep-gates`;
  - suíte com 53 arquivos e 97 testes vermelhos em 8.368 arquivos, em 35 min.
- **A suíte do merge no Mac foi encerrada** pela sessão `studio-64`, a pedido de Anderson, depois de 26 min: a regra
  nova é que a suíte completa só roda na CI do GitHub
  ([A suíte completa do brza-studio passou a rodar só na CI do GitHub](2026-11-11-suite-completa-so-na-ci.md)). Até o
  corte, 51 arquivos vermelhos, 46 da lista da pura. Dos 5 restantes, 3 passam isolados e 2 eram testes do fork atrás
  da 256, consertados em `7042258b9a2`.
- **No HEAD, no Mac:** typecheck com 0 erros; lint com os 2 vermelhos da pura e o `ast-grep` só com os 4 achados do
  `filesystem-watcher-real.test.ts`; os testes de cada conserto; `pnpm build:mac` com exit 0 e a identidade BrzA
  (`com.brzanderson.brzastudio`, esquema `brza-studio`).
- **A suíte na CI** (`node-next-compat.yml`), pela norma nova:
  - a `v1.4.256` pura, rodada 43122587247: verde. Os 53 vermelhos do Mac eram do ambiente;
  - a branch em `e3bc8f04009`, rodada 43119921699: 2 testes vermelhos, consertados em `2b490c84526`;
  - a branch em `2b490c84526`, rodada 43124774284: 1 teste vermelho, que já falhava na `master` do fork
    (rodada 43071063005, em `049a890a837`). Foi para
    [O teste da CLI empacotada falha na CI Linux do fork](../issues/o-teste-da-cli-empacotada-falha-na-ci-linux-do-fork.md).
  - o `node-next-compat.yml` tem um grupo de concorrência único com `cancel-in-progress`: o segundo disparo cancela o
    primeiro. A linha de base e a branch rodam uma depois da outra.

## O que a CI pegou

- **A CLI empacotada.** O `brza <subcomando externo>` do fork carregava o `command-path-resolver` do `main`, que na 256
  puxa o `command-path-directory` e um worker. No app real os chunks vão para fora do asar e funciona, mas o
  `packaged-cli-assets.test.ts` empacota arquivo a arquivo pelo `asarUnpack`, e a CLI caía em `Cannot find module`.
  A CLI ganhou `src/cli/brza/external-subcommand-path.ts`, que busca só no PATH com os checks do `shared`.
- **O teste de troca de conta do fork** apagava a pasta com os bancos do journal abertos (`ENOTEMPTY` no Node 26). Ele
  chama agora o `closeTestJournalHostDatabases()`, como os vizinhos do upstream.
- **O build do Mac** parava no `build-mobile-web-app-bundle`, que na 256 recusa as tabelas de idioma do `zod` no bundle:
  os schemas `shared` do fork usavam `import { z }`.

## O PLN-011

Pela R1, a `master` nova foi mesclada em `feat/pln-011-chat-cli`, com o merge `0ca6ac7abb5` (`--no-verify`) já no
origin. Oito conflitos, todos de CLI de chat: a 256 trouxe o `chat rename` (#38719), que se soma ao list/read/send. A
evidência do chamador no `agentSession.send` passou ao mecanismo novo do upstream (`CALLER_CHAT_METHODS` em
`src/cli/runtime/orchestration-compatibility-envelope.ts`), e os três casos do `client-execution-host.test.ts`, que o
upstream apagou (#40115), foram para `src/cli/brza/chat-caller-evidence.test.ts`. Typecheck com 0 erros; `src/cli` com
156 arquivos verdes. O C1 precisa de um app de dev recompilado dessa branch.

## O que ficou

- **A conferência no app**, com Anderson, pelo DMG `~/Downloads/brza-studio-1.4.256-macos-arm64.dmg`, pelo roteiro: cartão de arquivos alterados e Hide; o switch "Changed files summary" em Settings › Chat; um só botão de
  Fork, e o fork de chat fixado na conta dele; Markdown na prévia e com cor no Islands Dark; a seleção no chat com tema
  de terminal; o "Continuar em outra conta" e a retomada; a imagem de tool-result; a convivência com o Orca.
- **O teste da CLI empacotada na CI Linux**, na issue acima.
- **Os 214 commits do `upstream/main` depois da `v1.4.256`** entram no próximo sync.

## O DMG e os worktrees

A pedido de Anderson ("gere o DMG e remova os worktrees"):
- **O DMG** saiu do `pnpm build:mac --dmg` no `sync-v1.4.256`, em `2b490c84526`, o mesmo commit da `master`. O
  `hdiutil verify` deu válido, e ele foi copiado para `~/Downloads/brza-studio-1.4.256-macos-arm64.dmg`, com 237 MB e
  sha256 `d7e4957eca62712330c216ba689ac405e00579e61a139d540b79e0a57336d1c9`. É assinado ad hoc e sem notarização.
- **Os worktrees `sync-v1.4.246`, `sync-v1.4.251`, `base-v1.4.251`, `bisect-251`, `sync-v1.4.256` e `base-v1.4.256`**
  do `brza-studio` saíram com `git worktree remove`, todos limpos. As branches `sync/*` ficam. Ficaram o
  `brza-dark-theme`, o `feature-1`, o `pln-008-d11` e o `pln-011-chat-cli`.
- **O scratch da sessão se perdeu** quando a sessão reiniciou: os briefs, as devoluções, a revisão e os logs das suítes
  que estavam em `/private/tmp/brza-sync-256` não existem mais. O que importa deles está neste worklog.

## Fora do workspace

- **`pnpm install` nos worktrees `sync-v1.4.256` e `base-v1.4.256` do `brza-studio`.**
  - **Onde:** o store global do pnpm, `~/Library/pnpm`.
  - **Risco:** nenhum para os outros checkouts; o store só cresce.
  - **Estado:** ativo.
  - **Como desfazer:** `pnpm store prune`.
- **A tag `v1.4.256` e a branch `sync/v1.4.256` no origin (`brz-anderson/brza-studio`)**, para a CI, e três rodadas
  do `node-next-compat.yml` disparadas à mão (a quarta foi cancelada pelo grupo de concorrência).
  - **Risco:** nenhum.
  - **Estado:** ativo.
  - **Como desfazer:** `git push origin --delete sync/v1.4.256` e `git push origin :refs/tags/v1.4.256`.
- **O DMG em `~/Downloads/brza-studio-1.4.256-macos-arm64.dmg`.**
  - **Risco:** nenhum; é cópia do build local, assinado ad hoc.
  - **Estado:** ativo.
  - **Como desfazer:** apagar o arquivo.
- **Link `/private/tmp/brza-sync-256`**, para o scratch da sessão. Guarda os briefs, as devoluções, as rodadas, os logs e
  a revisão.
  - **Risco:** nenhum; some no reboot.

## Custo da tarefa

Corrido 21 h 25 min — agente 49 min, quem pediu 3 h 31 min, pausa 17 h 5 min · US$ 62,32 (turnos 18,63, subagentes 43,69) · CPU 9 min do `claude` e 6 h 20 min dos comandos, RSS até 433 MB · 22 turnos, 1 sessão · até 23:43 de 2026-11-11, pelo `brza note commit`
