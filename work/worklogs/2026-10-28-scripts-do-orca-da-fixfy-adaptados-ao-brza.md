---
scope:
  - workspace
  - brza-studio
---

# Os scripts do Orca da Fixfy adaptados ao BrzA Studio

O pedido de Anderson, em 2026-10-28: "estude os scripts criados pela fixfy-workspace, para orquestração e delegação no
Orca, para adaptarmos para o brza". Um subagente Sonnet levantou os dez scripts da Fixfy: os de `scripts/orca/`, o
`delegate.py` e o `quota.py`. Uma rodada fechou o corte, e esta sessão escreveu o que entrou. A sessão
`brza-workspace-2d` escreveu em paralelo o abridor de sessões, coordenada pelo correio do Orca.

## O que Anderson respondeu

- **Quem escreve o abridor de sessões em modo chat:** "A brza-workspace-2d (Recomendado)".
- **O chat nos checkouts do `brza-studio` passa por um wrapper:** "Adaptar o claude-orca (Recomendado)".
- **Como os scripts acham o CLI e o runtime:** "Módulo comum (Recomendado)".
- **O que entra agora:** "Núcleo do orca-sessions, orca-run", e para o resto, "marque gatilhos de revisão para os
  outros". Os gatilhos estão em
  [Os scripts de orquestração da Fixfy que ficaram fora do port para o BrzA](../issues/scripts-da-fixfy-fora-do-port-para-o-brza.md).

## O que se fez

Commit `54aefe3`, em `scripts/brza/`:
- **`brza_runtime.py`:** o módulo comum. Lê o CLI e os dados do app de `ORCA_CLI_COMMAND` e `ORCA_USER_DATA_PATH`, com
  os caminhos do BrzA Studio como padrão, e fornece o `brza(...)` (o CLI com `--json`) e o `rpc(...)` (o socket do
  `orca-runtime.json`).
- **`claude-brza`:** o `agentCmdOverrides.claude` do app.
  - No `brza-workspace` e no `brza-studio`, põe o `--settings` daqui e a `BRZA_WORKSPACE`.
  - Os worktrees do app em `~/orca/workspaces/…` são reconhecidos pelo `git --git-common-dir`.
  - Fora deles (`/`, `--version`, a Fixfy), cai no claude puro.
- **`brza-run`:** o `orca-run`, com o módulo comum no lugar do `runpy` do `orca-sessions`. É opção explícita, e a regra
  da cerca `bash` do `AGENTS.md` não muda.
- **`brza-install`:**
  - liga `claude-brza`, `brza-run` e `brza-sessions` em `~/.local/bin`;
  - aponta o `agentCmdOverrides.claude`;
  - sem flag, mostra o estado.
- **Testes:** 15, em `scripts/brza/tests/test_brza_scripts.py`. Os do `brza-run` vêm da Fixfy. A impressão digital do
  `agentSession.send` foi conferida no node contra o `structuredAgentSessionPayloadFingerprint` do `brza-studio`.

O abridor, `scripts/brza/brza-sessions`, é da `brza-workspace-2d`, que o testou contra o runtime e o commitou no
`711ed55`, com `test_brza_sessions.py`. Os 21 testes de `scripts/brza/tests/` passam.

Fora do port, no PLN-001: o achado de Anderson no chat ("nesse link, o texto ficou branco e não azul") virou o P53.4,
commit `b6cece9`.

## O que se aprendeu

- **O chat estruturado já carrega o `settings.json` do projeto.** Ele roda o `claude` com
  `--setting-sources=user,project,local`, e por isso, com o cwd no `brza-workspace`, os hooks já valiam. A lacuna era
  só nos checkouts do `brza-studio` (achado da `brza-workspace-2d`).
- **O app ainda usa os nomes do Orca por dentro:** o `orca-runtime.json` e as variáveis `ORCA_*`. Os links da Fixfy em
  `~/.local/bin` falam com o `Orca.app` e não servem ao BrzA.
- **O teste da impressão digital tem um U+2028 no texto**, e o `splitlines()` do Python o trata como quebra de linha. A
  cópia por `splitlines()` cortou a linha, e a cópia por `split('\n')` a preservou.

## O que ficou aberto

- **A conferência com Anderson:**
  - abrir um chat novo num checkout do `brza-studio`;
  - conferir que ele grava uma linha `turn` em `.measurements/` e que o `git var GIT_AUTHOR_IDENT` sai com o noreply do
    `brz-anderson`.
- **O `CLAUDE.md` ainda descreve a lacuna do chat como aberta**, em "A configuração chega pela função do shell". O
  texto muda com o aceite de Anderson.

## Fora do workspace

- **O quê e onde:** os links `~/.local/bin/claude-brza`, `~/.local/bin/brza-run` e `~/.local/bin/brza-sessions`, para
  `scripts/brza/` do checkout principal. **Risco:** nenhum fora do BrzA, porque os nomes são novos. **Estado:** ativo.
  **Como desfazer:** `rm` dos três links.
- **O quê e onde:** o `agentCmdOverrides.claude` do BrzA Studio, no perfil em
  `~/Library/Application Support/brza-studio`, que agora é `~/.local/bin/claude-brza`. **Risco:** todo chat do Claude no
  app passa pelo wrapper. Se ele quebrar, o chat não sobe, e a falha de leitura do git já cai no claude puro. **Estado:**
  ativo. **Como desfazer:** esvaziar o comando do Claude em Configurações › Agentes.
