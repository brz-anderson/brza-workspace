---
scope:
  - brza-studio
date: 2026-10-29
tags:
  - tooling
---

# O P59 do PLN-001, o terminal segue o chat

Anderson autorizou o P58 ao P60 do
[PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat](../../plans/PLN-001-o-brza-studio-generico/PLN-001-plan.md)
na sessão do `brza-workspace` que gravou o pedido 31, em 2026-10-29: "e já execute os passos em paralelo". O P58 veio
primeiro; o P59 rodou na sessão `pln-001-p59`, no worktree `.worktrees/pln-001-p59` do `brza-studio`, ao mesmo tempo
que o P60 noutro, e foi à `master` com push e sem PR. A evidência detalhada está no passo do plano.

## O P59 — o terminal segue o chat (D46)

Commit `brza-studio@697ee59c0bf`.

- **O campo.** O `terminalFollowsChatTheme`, ligado por padrão e lido como ligado quando falta, no
  `NativeChatGlobalSettings` (X44).
- **O resolvedor.** O `resolveTerminalChatTheme` (`src/shared/terminal-chat-theme.ts`) lê o `resolveNativeChatTheme` do
  P58, sem mudar o contrato, e devolve o `palette` do chat com o fundo no `canvas`. O `resolveEffectiveTerminalAppearance`
  o consulta primeiro, e assim o painel, a prévia, a prévia do agente, o SSH, a barra lateral e o tema do mobile seguem
  juntos (X43). O modo e o divisor vêm do esquema do chat (X41), e a frente é a do tema, sem a mistura do contraste
  (X42). A fonte, o tamanho, o peso e a altura de linha continuam do terminal, e os overrides e a opacidade valem por
  cima.
- **O main.** A semente do OSC 10/11, antes de o renderer publicar, passou ao `resolveSavedTerminalColors`, que segue o
  chat do mesmo jeito.
- **A tela.** O "Seguir o chat" abre a seção de temas do terminal; ligado, o `ThemePicker` fica inerte e o "Match dark
  mode", desabilitado, e os dois guardam a escolha. A busca das configurações acha o interruptor, e as traduções
  entraram no `en` e no `pt`.
- **Os testes.** Os 2 casos novos de `terminal-appearance.test.ts` falharam antes pelo fundo do tema próprio
  (1 failed | 30 passed) e passaram depois (31 passed). Mais um caso do modo e do divisor, em `terminal-theme.test.ts`,
  um da semente do main, em `terminal-view-attributes-ipc.test.ts`, e um da tela, em
  `TerminalThemeSections.lifecycle.test.ts`. Os 19 casos do upstream que provavam o tema próprio com as configurações
  padrão passaram a desligar o interruptor.

## O check

O `pnpm check:changed --base=origin/master --maxWorkers=2` deu 21 de 26, em 1781 s. O oxlint e o gate de qualidade
apontaram um `as () => void` num teste novo, corrigido antes do commit. Os outros vermelhos já estão na `master`: o
typecheck, por `updater-enabled.test.ts:20`; o import boundaries, pelo `external-subcommand.ts`; e 4 casos unitários,
em `open-uncommitted-entry.test.ts` e `cross-version-agent-session-wire.unit.test.ts`, que falham igual num worktree
limpo da `origin/master`. Também falha lá o `runtime-environment-store.test.ts`, pelo "this Orca itself" do rebrand.

O rebase sobre o P60 e o P62 não deu conflito: o P60 guardou o tema do Markdown no `markdownTheme`, à parte. Depois
dele, os testes das áreas tocadas deram 803 arquivos → 7492 passed, e o `pnpm tc:web` e o `tc:cli` ficaram limpos.

A primeira rodada do `pnpm test:changed` parou no reinício do app, sem resultado; os testes rodaram de novo por
diretório.

## Desvios

- **X41** — o modo e o divisor do terminal seguem o esquema do tema do chat, e não o modo do app.
- **X42** — a frente do terminal é a do tema do chat, sem a mistura do contraste.
- **X43** — seguir o chat vale em toda superfície de terminal, e a semente do OSC 10/11 também segue.
- **X44** — o campo fica no `NativeChatGlobalSettings`, e os testes do tema próprio o desligam.

## O que fica

- O C16 e o P61, a conferência no BrzA Studio, com Anderson, num build depois do P60, junto do C15 e do C17.
- O mobile recebe o tema do terminal que segue o chat, mas não ganha o interruptor.
