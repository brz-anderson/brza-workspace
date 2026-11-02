---
status: open
description: Quatro consertos pequenos na master do brza-studio que a caçada de achados da v1.4.246 achou: o CLI empacotado sem um módulo, o contrato cruzado sem 5 métodos do fork, 9 linhas com ORCA no coreano e o fundo do código do Markdown.
scope:
  - brza-studio
opened: 2026-11-02
tags:
  - tooling
---

# Pequenos consertos do fork depois do sync da v1.4.246

Achados do `collector` de qualidade e do `reviewer` na caçada de achados da v1.4.246, em 2026-11-02, em
`brza-studio@384d4b08fd6`; a `origin/master` não tinha andado quando os conferi. Cada item é pequeno, e todos cabem num
commit só na `master`, quando Anderson mandar a sessão de correção.

## 1. O CLI empacotado não acha um módulo do resolvedor — média, alta se o build reproduzir

- **O teste** `loads worktree link validation from the installed CLI` falha **só no fork**, rodado 3 vezes: `JSON Parse
  error: Unexpected EOF` (`src/main/cli/packaged-cli-assets.test.ts:54`). Na v1.4.246 pura, passa.
- **A causa**, lida no stderr do CLI empacotado: `Cannot find module './command-path-directory'`. O `asarUnpack` do fork
  só desempacota o `command-path-resolver.js` (`config/electron-builder.config.cjs:342`, `fb7eb5a9082`), e o resolvedor da
  v1.4.246 passou a importar `./command-path-directory` e o worker client (`command-path-resolver.ts:7-8`), que ficam
  dentro do asar.
- **Inferido:** se o build real (electron-vite) gera o resolvedor autocontido; o teste usa `tsc` solto.
- **Correção:** acrescentar o `command-path-directory.js` (e o do worker client) ao `asarUnpack`, e conferir `brza foo`
  pelo app empacotado, no build manual.

## 2. O contrato cruzado não lista 5 métodos do fork — média

- **O teste** `cross-version-agent-session-wire` falha só no fork: `expected [ …(51) ] to have a length of 46 but got 51`
  (`tests/e2e/cross-version-wire/cross-version-agent-session-wire.unit.test.ts:362`). Na pura o mesmo arquivo falhou por
  outro motivo (`Lock file is already being held`), e a comparação por arquivo escondeu isso.
- **Os 5 métodos fora do `STRUCTURED_CALLS`** (`structured-agent-session-surface-calls.ts:20`): `forkThroughMessage`
  (`structured-agent-session-message-fork.ts:11`), `switchAccount` (`…-switch-account.ts:16`), `usageLimitAutoResume`,
  `usageLimitAutoResumeCancel` e `usageLimitAutoResumeList` (`…-usage-limit-auto-resume.ts:26,35,44`).
- **Correção:** acrescentar as 5 chamadas, cada uma com params válidos; trocar só o número não serve.

## 3. Nove linhas do coreano com `ORCA` em caixa alta — baixa a média

- `src/renderer/src/i18n/locales/ko.json`, linhas 20744, 20770, 21091 (duas ocorrências), 21094, 21100, 21106, 21112,
  21117 e 21130. O script de rebrand trocou só `\bOrca\b`; a v1.4.246 pura tem as mesmas linhas. Conferi na
  `origin/master`: 9 linhas com `ORCA` fora de `ORCA_*`.
- **Correção:** `ORCA` → `BrzA Studio` nessas linhas; os `ORCA_*` de variável de ambiente ficam.

## 4. O fundo do código do Markdown segue o modo pedido, e não o do Monaco — baixa

- O `markdownSurfaceTheme` aplica `--markdown-code-canvas` pelo modo **pedido** (`settings.theme`)
  (`markdown-surface-theme.ts:64-65,87`), e o Monaco tira o modo do `useDocumentDarkTheme()`, o **pintado**, que o "Match
  Terminal" pode inverter (`use-document-dark-theme.ts:17-24`, `use-monaco-theme.ts:11-13`).
- **O cenário:** o app pede escuro, o "Match Terminal" pinta claro, e o Markdown tem tema próprio escuro; o fundo escuro
  entra sob o Monaco claro, e o texto some. Confiança do `reviewer`: 82, lido e não rodado.
- **Correção:** comparar com o modo do Monaco (`useDocumentDarkTheme()`, ou a base do tema de editor quando há override).

## Fica de fora, com o porquê

- **As seis suítes `cross-version-wire` que não executam em nenhum dos lados** (a harness procura
  `src/shared/agent-session-record.ts`, que na v1.4.246 está em `src/shared/agent-session/lifecycle/`): herdado do
  upstream.
- **58 chaves novas do fork sem tradução fora de `en` e `pt`:** o upstream já aceita `missing` com fallback em inglês (a
  pura tem de 264 a 599 por idioma).
- **11 textos que mandam rodar `orca …` enquanto o CLI do fork é `brza`:** inferido; o `orca` empacotado existe e é
  idêntico ao `brza`, então só confunde.
- **"Orca Computer Use.app" mantido:** a identidade de TCC é compartilhada, e renomear pede build nativo e permissões
  reconcedidas.
