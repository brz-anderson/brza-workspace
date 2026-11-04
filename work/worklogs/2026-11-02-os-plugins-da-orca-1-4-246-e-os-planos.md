---
scope:
  - brza-studio
  - workspace
refs:
  - PLN-001
  - PLN-003
  - PLN-007
  - issue:os-restos-da-orca-a-vista-no-brza-studio
---

# Os plugins da Orca 1.4.246 e o que mudam nos planos

Anderson pediu, na sessão `brand`: "verifique como funcionam os plugins adicionados nessa ultima versão do Orca
(upstream), pode mudar os planos futuros que temos". Antes, no mesmo dia, pediu para tirar os agentes "Não instalado" do
menu "+" do app.

## O menu "+" sem os agentes não instalados

O seletor (`AgentLaunchPickerMenu.tsx`) e o menu antigo de linhas (`QuickLaunchButton.tsx`) passaram a omitir o agente sem
nenhuma superfície e com linha `chat-unavailable` de motivo `not-installed`; os outros motivos (SSH, WSL, falha de
verificação) seguem à vista. Teste novo `AgentLaunchPickerMenu.not-installed.test.tsx`, que falhou antes e passa depois; o
`pnpm check:changed --base=master --force` passou nos 24 checks. **Commitada e mergeada por fast-forward na `master` do `brza-studio` como `7cb41bbd5c4`**, por pedido de Anderson, depois de
um rebase sobre o `d3d636f` (outra sessão avançou a `master` no meio). Os 107 arquivos de teste de `agent/` e `tab-bar/`
passaram de novo depois do rebase. **Push dado depois, a pedido de Anderson** (`d3d636f..7cb41bb`). Não está no app
instalado: falta um build novo. O worktree e a branch foram removidos. A tela de instalar skill (`SkillInstallAgentPicker`) também diz "Not installed" e ficou
como está.

## O levantamento dos plugins

Um `collector` leu, só leitura, os docs, a skill de autoria e o código de plugins do `brza-studio`, separando o que está na
`v1.4.246` do que só existe no `upstream/main` (279 commits à frente, API do host 1.3, `engines.orca >=1.4.248`). O agregado,
com 116 fatos marcados, estava em `/private/tmp/plugins-orca/levantamento.md` (scratch; copiado para
`/private/tmp/pln-003-plugins-levantamento.md`). A sessão conferiu por conta própria quatro fatos: a versão instalada é a
`1.4.246-alpha.1`, `pluginSystemEnabled` é o padrão desde esta versão, `hooks` e `statusBarItems` são `1.4.248`, e
`skills`/`mcpServers`/`agentHarnesses` seguem reservados.

**O que muda nos planos:**

- **PLN-003 (`tools-kit`):** o Terreno do plugin do Orca envelheceu ("sem canal worker→painel", três métodos do host, "fork
  só manifest 1"); o painel TSX com worker pede o C5 reaberto, com um spike no app instalado. A orquestração segue no MCP e
  no `brza` até a base chegar a 1.4.248. O plugin do Claude com MCP (R4.3, R4.4) não muda.
- **A issue das skills de documento do workspace de origem:** o plugin do Orca não contribui skills, então o veículo é o plugin do Claude.
- **PLN-007:** nada; tema de plugin não toca o chat nem a marca.
- **Próximo sync:** só quando houver tag; os hooks e a API nova de plugins vêm junto, e plugin com `engines.orca >=1.4.248`
  não carrega no fork antes disso.

## O que se decidiu

Rodada respondida por Anderson em 2026-11-02:

- **"Onde registro o que o levantamento mudou nos planos?"**: "Sessão no tools-kit (Recomendado)". Aberta como
  `pln-003-plugins` ("PLN-003: o Terreno do plugin do Orca"), com o pedido em `/private/tmp/pln-003-prompt-plugins.md`.
- **"O app chama `onorca.dev` … O que fazemos?"**: "Medir antes (Recomendado)". Medido, e o resultado está na issue
  [Os restos da Orca à vista no BrzA Studio](../issues/os-restos-da-orca-a-vista-no-brza-studio.md): telemetria desligada no
  nosso build, `kill-list` e `stats` por GET sem identidade, catálogos da `stablyai` à vista. **A decisão (deixar, ou
  desligar o sistema por padrão) volta a Anderson com esses fatos; nada foi mudado.**

## Pendente

- O commit `release: v1.4.246-alpha.2` (`2511b6298d7`) e a tag anotada `v1.4.246-alpha.2` estão gerados localmente na
  `master` do `brza-studio` (sobre `0efb501da52`, após os pedidos 37 a 42 do PLN-001 e a suíte completa na sessão
  `studio-achados-246`), e o DMG final está em
  `~/Projects/brza-studio/dist/brza-studio-1.4.246-alpha.2-macos-arm64.dmg` (250 MB, com `Resources/ad-hoc-signed`
  presente). Falta Anderson instalar/conferir o DMG e pedir o push do commit e da tag.
- Anderson decide o que fazer com as chamadas a `onorca.dev` e com os catálogos da `stablyai`.
- A sessão `pln-003-plugins` atualiza o Terreno e o C5 do PLN-003.

## Fora do workspace

- **A sessão `pln-003-plugins`** aberta pelo `brza sessions` no worktree `tools-kit`; **estado:** ativa; **como desfazer:**
  `brza sessions close pln-003-plugins`.
- **O commit `7cb41bb` no origin do `brza-studio`** (`git push origin master`, a pedido de Anderson); **como desfazer:** só com
  `--force`, que não se faz sem pedido. O worktree e a branch da mudança foram removidos.
- **`git fetch upstream --tags --prune`** no `brza-studio`: atualizou `upstream/main` (leitura, só refs remotas).
- **A tag `v1.4.246-alpha.1` no origin do `brza-studio`** (`git push origin v1.4.246-alpha.1`, a pedido de Anderson), apontando para
  `6d47623`; **risco:** tag publicada não se move sem `--force`; **como desfazer:** `git push origin :refs/tags/v1.4.246-alpha.1`.
- **A sessão `studio-achados-246`** ("Studio: achados da 1.4.246") aberta pelo `brza sessions` no worktree `studio`, a pedido de
  Anderson, para procurar achados novos da v1.4.246; o pedido está em `/private/tmp/studio-prompt-achados-246.md`. Coordenou os
  pedidos 37 a 42 do PLN-001 e a suíte completa, e avisou a sessão `brand`; **estado:** concluída (`done`); **como desfazer:**
  `brza sessions close studio-achados-246`.
- **O commit `2511b6298d7` (`release: v1.4.246-alpha.2`) e a tag anotada `v1.4.246-alpha.2` no `brza-studio`**, só locais,
  sobre `0efb501da52`; **risco:** a `master` local está 1 commit à frente do origin; **estado:** ativos; **como desfazer:**
  `git tag -d v1.4.246-alpha.2` e `git reset --hard origin/master`, antes do push.
- **O DMG `~/Projects/brza-studio/dist/brza-studio-1.4.246-alpha.2-macos-arm64.dmg`** (250 317 900 bytes, SHA-256
  `8d04beff619b3aa02f3c8a048bc3568bcfb27bdc5a9fb273c9298a46e0c180b4`), gerado num worktree temporário `.worktrees/pln-007-build`
  já removido; **risco:** nenhum (`dist/` está no `.gitignore`); **estado:** ativo; **como desfazer:** apagar o arquivo.
