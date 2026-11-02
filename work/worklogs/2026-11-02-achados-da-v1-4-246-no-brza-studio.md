---
scope:
  - brza-studio
date: 2026-11-02
tags:
  - release
  - chat
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
