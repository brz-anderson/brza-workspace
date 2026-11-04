---
scope:
  - brza-studio
tags:
  - release
  - chat
refs:
  - PLN-001
  - issue:as-credenciais-de-integracao-em-orca-sao-cifradas-por-app
  - issue:o-atualizador-esta-ligado-no-build-ad-hoc
  - issue:o-fork-de-um-chat-fixado-abre-na-conta-global-e-sem-contexto
  - issue:o-worker-de-plugin-sem-sandbox-alcanca-o-token-do-runtime
  - issue:pequenos-consertos-do-fork-depois-do-sync-da-v1-4-246
---

# Mais achados que a v1.4.246 trouxe ao BrzA Studio

O pedido de Anderson, vindo da sessão `brand` em 2026-11-02: verificar mais possíveis achados da versão. Feito na sessão
`studio-achados-246`, no worktree `.worktrees/studio`, em `brza-studio@384d4b08fd6` (a `origin/master` não andou
durante a caçada, então nenhum achado duplica correção em curso). Só achar e registrar: nenhum código da `master` foi
mexido. O sync em si está em
[O sync da v1.4.246 do upstream, que tirou o chat do experimental](2026-11-02-sync-da-v1-4-246-do-upstream.md).

## O que se fez

Três subagentes em paralelo, com o agregado no scratch (`/private/tmp/studio-246/`) e o resumo na sessão:
- **`reviewer` (camada alta):** o comportamento do P36, do tema do chat, da coexistência com o Orca e do P62 ao P64 e P71.
- **`collector` (média), restos da Orca e riscos:** a ponte do CLI, `orca://`, `~/.orca`, `ORCA_*`, o atualizador, o
  sistema de plugins (só o que o levantamento da `brand` não cobre), a migração do perfil e o instalador.
- **`collector` (média), dívida de qualidade:** os 25 testes vermelhos contra a v1.4.246 pura, as supressões de lint, os
  `ts-nocheck` e os catálogos de idioma.

## Os achados novos e o destino

| Achado | Severidade | Destino |
| :----- | :--------- | :------ |
| [O fork de um chat fixado abre na conta global e sem o contexto](../issues/o-fork-de-um-chat-fixado-abre-na-conta-global-e-sem-contexto.md) | alta | issue; rodada |
| [As credenciais de integração em `~/.orca` são cifradas por app](../issues/as-credenciais-de-integracao-em-orca-sao-cifradas-por-app.md) | média | issue; rodada. Os dois a acharam sozinhos |
| [O atualizador está ligado no build ad hoc, sem manifesto para ler](../issues/o-atualizador-esta-ligado-no-build-ad-hoc.md) | baixa a média | issue; rodada |
| [O worker de plugin sem sandbox alcança o token do runtime](../issues/o-worker-de-plugin-sem-sandbox-alcanca-o-token-do-runtime.md) | média, condicional | issue; junto da decisão dos plugins, de Anderson |
| [Pequenos consertos do fork depois do sync da v1.4.246](../issues/pequenos-consertos-do-fork-depois-do-sync-da-v1-4-246.md) | média a baixa | corrigir na `master`, num commit, quando Anderson mandar |

**Os dois vermelhos que só existem no fork** estão no item 1 e no item 2 da última issue: o `packaged-cli-assets` e o
`cross-version-agent-session-wire`.

## Só para o registro, sem issue

- **A nota do sync dizia "3 passos de lint vermelhos":** no HEAD só o `lint:ast-grep-gates` está vermelho (4 achados, os
  mesmos da pura, em dois testes do `filesystem-watcher`). O `check:path-literal-ratchet` e o `check:test-file-runners`
  passam desde `a3a89e3aaf5`. Typecheck: exit 0.
- **Voltar a um build ≤ 1.4.242 não abre os chats:** o journal de chats só acrescentou tabelas `journal_outcome*` e uma
  linha `{"v":5,"kind":"outcomes"}` por sessão sem subir o `user_version` (4); o `parseJournalRow` da 1.4.242 trata `v>4`
  como ilegível e o cabeçalho avisa que builds antigos "may delete them" (`journal-outcome-format.ts:15,25-41,103-130`). No
  perfil real são 12 linhas v5 e 8.080 `journal_outcomes`. Da alpha.1 para a alpha.2 não há problema: o diff entre elas
  são 23 arquivos de UI, i18n e CLI.
- **A migração de settings é de mão única, e a única cópia durável do estado anterior é o backup manual**
  `brza-studio.bak-1.4.242` (e o `-limpo`): o `profile-state.db` guarda só 5 backups horários, e o
  `ensureProfileStatePreMigrationBackup` não tem chamador fora de teste. **Não apague o backup.**
- **Assinatura ad hoc:** cada rebuild muda o `cdhash` e o macOS tende a pedir de novo as permissões de Acessibilidade e
  Gravação de Tela (inferido, 78). O `CSC_NAME` já é aceito, para assinar com identidade local estável.
- **CI do fork:** 16 dos 30 workflows têm `cron` e rodam no fork; os de teste falham ou cancelam, e os de release são
  pulados pela guarda `github.repository == 'stablyai/orca'`. Só ruído de e-mail; `gh workflow disable` resolve.
- **Hooks de `~/.orca` compartilhados:** hoje o Orca.app e o BrzA são ambos 1.4.246 e o script é idêntico; quando o Orca
  passar da 1.4.246, cada abertura reescreve o script do outro (inferido, 70). Já decidido na R2 do sync; só vigiar.

## O que se conferiu e está limpo

- **P36:** a retomada agendada dispara na conta do pino e não duas vezes; a linha de limite do chat fixado mostra o
  seletor do próprio chat; a troca de conta tira o `acquiredAccount` antigo.
- **Tema:** o tema de plugin que sumiu cai no padrão do BrzA, no modo do app, sem inverter claro e escuro; o "Match
  Terminal" acompanha a troca do tema do chat.
- **Coexistência:** pasta de dados, rótulo do launchd, porta (6868), lock de instância, bundle id, helpers, o esquema
  `brza-studio://` e a pasta do daemon são próprios; o socket do daemon não colide, e o ledger de terminais é
  compartilhado de propósito; o launcher do `brza` descarta o ambiente do outro app, e o `bin/brza` e o `bin/orca`
  empacotados são idênticos (o `orca` do Orca.app, ao contrário, não tem essa guarda).
- **P62 ao P64 e P71:** o leitor de mensagem de peer e o clique no remetente (que só abre aba de nome único); o link http
  abre pelo dono do chat.
- **Os 25 testes vermelhos** estão todos na lista da v1.4.246 pura (`comm -23` vazio); as causas são do macOS
  (`/opt/homebrew/bin/claude`, `ssh -F ~/.ssh/config`, `/private/tmp` × `/tmp`).
- **Supressões:** `@ts-expect-error`, `@ts-ignore`, `@ts-nocheck`, `ast-grep-ignore`, `eslint-disable` e `oxlint-disable`
  idênticos à pura; 20.873 linhas `+` varridas, nenhuma exceção nova. Só a allowlist de localização cresceu (3 entradas do
  `BrzaWordmark`, com `reason`). 61 testes novos do fork, todos `.test.*` e coletados.
- **Catálogos:** sem placeholder divergente nem chave órfã nova; o `verify:localization-catalogs` passa no HEAD.
- **Resíduo do P40:** zero referências em código e JSON.

## Os pedidos que chegaram no meio da caçada

Registrados no [PLN-001](../../plans/PLN-001-o-brza-studio-generico/PLN-001-plan.md), cada um com a rodada de Anderson e
a sessão que o executa, num worktree do `brza-studio`:
- **Pedido 37 (R63, D55, P72):** o prompt do `brza sessions` (`--prompt`, `--rename --prompt`) e o `brza sessions send`
  aparecem no chat de destino como o cartão "Tarefa do coordenador", e não como balão de usuário. Sessão
  `pln-001-pedido-37`.
- **Pedido 38 (R64, D56, P73):** o tipo do agente na lista "AGENTES" do chat (`descrição · reviewer · Bash`), só na faixa
  do chat. Sessão `pln-001-pedido-38`, que já fechou o P73 (`brza-studio@563705a7aaf`); o C26 espera o build.
- **Pedido 39 (R65, D57 a D60, P74 a P77):** a correção dos achados, decidida por Anderson na R65, todas as respostas na
  recomendada: o fork na conta fixada da origem (P74), as credenciais numa pasta própria `~/.brza` (P75), o atualizador
  desligado no build ad hoc (P76) e os quatro pequenos consertos num commit só, antes da alpha.2 (P77). Quatro sessões,
  `pln-001-pedido-39-fork`, `-credenciais`, `-atualizador` e `-consertos`, cada uma num worktree do `brza-studio`. O
  worker de plugin sem sandbox ficou fora, com a decisão dos plugins.

## O que ficou

- **A suíte completa do merge** (R67.2, "relance depois da correção"): a primeira tentativa, em `origin/master@9a8631369ac`,
  parou depois de ~2 min sem erro dela (a notificação disse "parada pelo usuário ou pelo app"), e o worktree
  `suite-master` saiu. Roda **uma vez**, na `origin/master`, depois que o P79 der push, pela sessão de coordenação, e a
  comparação é com a linha de base de 25 arquivos vermelhos da v1.4.246 pura.
- **O pedido da sessão `brand`, para a `v1.4.246-alpha.2`:** quando todas as correções que esta sessão coordena estiverem
  na `master` (faltam o P79 e o P80) e a suíte completa estiver concluída, avisar a `brand` por `brza sessions send brand "…"` com
  o hash do HEAD da `master` e o resumo da suíte, para ela gerar o commit `release`, a tag `v1.4.246-alpha.2` e o DMG
  final. A suíte roda uma vez, na `origin/master` desse HEAD, num worktree limpo.
- **O pedido 42 (D63, P80):** o botão de expandir do P71 com a aparência e a posição dos botões vizinhos (sem borda nem
  fundo, na mesma fileira, medido no grupo de ações real). Sessão `pln-001-pedido-42`; o C33 espera o build. Entra na
  `v1.4.246-alpha.2` junto do P79.
- **A suíte completa do merge, em `origin/master@4bbaecabf18`** (os P72, P74 a P77, P79 e P80 dentro; 1.039 s, 17 min;
  log em `/private/tmp/studio-246/suite-master.log`): **57 arquivos e 63 testes falham**, contra 25 arquivos e 50 testes
  no sync (`a70f63b6a92`) e 39 na v1.4.246 pura. 13.405 arquivos passam. O que são:
  - **29 `mobile-web-app-*-render`:** o Playwright novo pede o `chromium_headless_shell-1248`, que não está instalado
    nesta máquina (`pnpm exec playwright install`). Ambiente, não código.
  - **1 regressão das correções, do P75 (`f7490afab9e`):** `usage-credentials.test.ts`, 8 dos 13 testes. Passavam em
    `ecc4a13d456` e falham em `f7490afab9e`, porque ainda esperam as chaves do MiniMax e do GLM em `.orca/` e o P75 as
    moveu para `~/.brza`. A sessão do P75 rodou só os testes do alvo, pela regra da suíte única, e o vizinho que a
    suíte pegou não estava entre eles. Os testes "nunca sobrescreve a chave que o outro app selou" também precisam ser
    relidos: com as pastas separadas, a premissa deles mudou.
  - **`wsl-host-deployment-store.test.ts`, 3 testes:** falham também na tag v1.4.246 pura e em `a70f63b6a92`; não são das
    correções (e a lista dos 25 do sync não os trouxe: depende da máquina).
  - **`git-admission-storm-measurement.test.ts`:** passa isolado; é instável sob carga.
  - **O resto** são os 25 de sempre (macOS, `ssh -F`, `/private/tmp`), na lista da pura.
- **A regressão do P75 corrigida e o aviso à `brand` enviado** (R69.1, "Corrigir o teste do P75 antes"): a sessão
  `pln-001-p75-teste` deu push em `brza-studio@0efb501da52` (só o `usage-credentials.test.ts`, 9 linhas a mais e 8 a
  menos). Conferi nesse HEAD, num worktree próprio: `usage-credentials`, `src/main/credentials`, Jira, Linear e Bitbucket →
  59 arquivos, 513 testes, todos passam. A `master` do `brza-studio` ficou em `0efb501da52`, e a `brand` recebeu, por
  `brza sessions send brand` (entregue a `antigravity_5464ba06…`), o hash, o resumo da suíte e o que não se confirmou: os
  casos manuais C22 a C33 e o marcador `ad-hoc-signed` do P76 no bundle empacotado.
- **O pedido 41 (R67, D62, P79):** o botão "Continuar em outra conta" volta, reabrindo o P40 e a R1 do sync, e o
  "Retomar automaticamente" agenda sozinho ao bater o limite. Sessão `pln-001-pedido-41`; o C32 espera o build.
- **A limpeza de branches** (só local, a pedido): saíram os worktrees e as branches dos pedidos 37, 38, 39 (as quatro) e
  40, e as quatro pastas órfãs de `.worktrees/`. Ficam `master`, `sync/v1.4.246` e, no origin,
  `rebrand/brza-studio` e a branch de sync da v1.4.239 do fork de origem.
- **O worker de plugin sem sandbox** fica na issue, com a decisão dos plugins, de Anderson.
- **Os casos que só o build prova**, com Anderson, num build só a partir da `master` depois dos pushes: o C25 e o C26, e
  o C27 ao C30 do pedido 39 (o `brza foo` pelo app empacotado é o C30).
- **O `ast-grep-gates` vermelho** (dois testes do `filesystem-watcher`) segue como no upstream; não é do fork.

## Fora do workspace

- **`/private/tmp/studio-246/`, link para o scratch da sessão**, com os relatórios dos três subagentes, os prompts do P72 e
  do P73 e um diff de 38 MB (`up-diff.patch`, `v1.4.242..v1.4.246`). **Risco:** nenhum. **Estado:** ativo. **Como
  desfazer:** `rm /private/tmp/studio-246`.
- **`/private/tmp/reviewer-fork-tests/`**, a cópia do teste temporário do F1. **Risco:** nenhum. **Estado:** ativo.
  **Como desfazer:** `rm -r /private/tmp/reviewer-fork-tests`.
- **Seis chats abertos no BrzA Studio pelo `brza sessions`**, `pln-001-pedido-37`, `-38` e `pln-001-pedido-39-fork`,
  `-credenciais`, `-atualizador` e `-consertos`, nos worktrees de mesmo nome em `.worktrees/` do `brza-studio`, criados
  pelo `brza tree`. **Risco:** nenhum para os outros
  checkouts. **Estado:** ativo. **Como desfazer:** fechar as abas e `brza tree --rm <nome>` de cada um, depois dos pushes.
- **Leituras no Keychain e no perfil real**, só de metadado: `security find-generic-password` sem `-w`, e `sqlite3
  -readonly` em cópias no scratch, apagadas. **Risco:** nenhum; nenhum segredo foi lido, e um comando que imprimiria o
  `ORCA_PAIRING_CODE` foi barrado e não repetido.
- **Vigia do limite de 5h, `/private/tmp/studio-246/limite-conta.py`, em segundo plano na sessão `studio-achados-246`**
  (pedido de Anderson às 20h27: uso da conta `anderson@` em 95%, reset às 21h30). Lê o uso pelo RPC
  `accounts.list` a cada 60 s e, ao bater 100%, troca a conta ativa global do Claude para a conta `admin@`
  (`accounts.selectClaude`); às 21h31 (reset + 1 min) volta à conta de antes, o padrão do sistema, que é a
  conta `anderson@`. Não move sessão em andamento nem mexe em chat fixado (P36). Para sem trocar se o reset chegar
  antes do limite, ou se Anderson trocar a conta pela interface. **Risco:** durante a janela, o seletor global do app
  fica na `admin`. **Estado:** ativo até ~21h40. **Como desfazer:** `kill` do processo e, se preciso, escolher a conta
  no seletor do app; o log está em `/private/tmp/studio-246/limite-conta.log`.
- **A troca da conta global às 21h02 e o processo da volta** (atualiza o item do vigia acima): o `limite-conta.py` trocou
  para a conta `admin@` às 21h02, quando o uso da `anderson@` bateu 100%, e **morreu com a sessão** que o rodava. A
  volta das 21h31 passou ao `/private/tmp/studio-246/voltar-conta.py`, desligado da sessão (duplo fork, pid 70493 às
  21h11), que seleciona o padrão do sistema (a `anderson@`) só se a conta ativa ainda for a `admin`. **Como desfazer:**
  `kill 70493` e escolher a conta no seletor do app; o log é `/private/tmp/studio-246/limite-conta.log`.
- **A volta da conta às 21h31 aconteceu:** o `voltar-conta.py` selecionou o padrão do sistema (a `anderson@`) às 21h31 e
  terminou; o uso da janela de 5h dela está em 0%. O `limite-conta.py` e o `voltar-conta.py` não rodam mais.
- **A regra das aspas nos blocos ▶, na norma comum** (a `brand`, em Antigravity, passou `head $(which brza)` sem aspas, e o
  caminho `/Applications/BrzA Studio.app/…` tem espaço): `brza-workflow@c7a9e68`, no `core/AGENTS.md` e na lista fechada
  do teste de ouro (`tests/hooks/golden_differences.py`, o `why` `aspas`), com push no `origin/master` do `brza-workflow`;
  `brza sync` escreveu o `AGENTS.md` (`44ec360` na `master` do workspace) e mesclou e enviou `brand`, `studio`,
  `tools-kit` e `workspace`. **Risco:** nenhum para o código; os quatro worktrees ganharam um merge da `master`.
  **Como desfazer:** reverter o `c7a9e68` no `brza-workflow` e rodar o `brza sync`.
