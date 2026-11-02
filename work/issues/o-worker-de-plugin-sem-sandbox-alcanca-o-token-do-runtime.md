---
status: open
description: O worker confiável de plugin da 1.4.246 roda como Node sem sandbox e alcança o token do runtime e as credenciais do usuário; o sistema de plugins está ligado por padrão e o catálogo oficial pula o diálogo de confiança.
scope:
  - brza-studio
opened: 2026-11-02
tags:
  - infra
---

# O worker de plugin sem sandbox alcança o token do runtime

Achado do `collector` na caçada de achados da v1.4.246, em 2026-11-02, em `brza-studio@384d4b08fd6`. Acrescenta ao
levantamento dos plugins da branch `workstream/brand` (o worklog `2026-11-02-os-plugins-da-orca-1-4-246-e-os-planos.md`,
que não se repete aqui) o que ele não cobre: o que um plugin com worker alcança. A decisão sobre os plugins e sobre as
chamadas a `onorca.dev` segue com Anderson.

## O que prova

- **O worker roda como o próprio binário**, com `ELECTRON_RUN_AS_NODE`, `execArgv: []` e sem flag de permissão do Node
  (`src/main/plugins/workers/plugin-host-process.ts:59-67`). O ambiente é por lista de permitidos
  (`plugin-worker-env.ts:3-22`): não herda `ORCA_*`, `ORCA_PAIRING_CODE` nem tokens do shell.
- **Mesmo assim, alcança tudo o que o uid alcança:** o sistema de arquivos, a rede e o `child_process`. Em particular
  `userData/orca-runtime.json` (0600, com o `authToken` do RPC do app inteiro), `agent-session-authority.key`,
  `~/.orca/jira-tokens`, `~/.claude`, `~/.codex` e `~/.ssh`. O token do runtime fica fora do modelo de capacidades dos
  plugins.
- **O audit log não vê o Node do worker** (`plugin-audit-log.ts:3,22-23`).
- **O perfil real de Anderson tem o sistema ligado** (`pluginSystemDefaultedOn: true`), sem plugin instalado, mas com o
  catálogo, o `kill-list` e o `stats` já baixados.
- **O diálogo de confiança é pulado para plugin "oficial"**, e o oficial ainda é o catálogo da `stablyai`
  (`plugin-install-trust.ts:63-66`). O diálogo em si está completo: 16 chaves em 10 idiomas, sem falta.
- **O que está limpo:** os frames isolados ficam ligados por padrão e a rede do guest é cortada na sessão
  (`plugin-frame-isolation.ts:8`, `plugin-frame-request-policy.ts:12-19`); o plugin só escreve em `userData/plugins` e
  `userData/plugins-data/<key>`, e nada em `~/.orca`.
- **Texto sem tradução:** o prompt "{{plugin}} wants to open {{host}}" (`plugin-external-open-consent.ts:60-76`) cai em
  inglês; faltam as chaves `plugins.frameOpenExternal.*` e `frameSaveAs.*` nos 10 catálogos. O atraso é do upstream, e não
  do sync.

O risco é condicional a instalar um plugin com worker, e o `collector` o dá como médio. **Inferido:** que o `authToken`
dá acesso ao RPC inteiro; foi lido, e não rodado.

## O que resolve

Decisão de Anderson junto da dos plugins:
- **Desligar o sistema de plugins por padrão no fork** (`pluginSystemDefaultedOn: false`), ligando só quando Anderson
  quiser instalar um. Custo: um default e a migração do perfil. Se paga: já, se ele não pretende usar plugins agora.
- **Manter ligado e só instalar plugin que ele leu.** Custo: nenhum código. Se paga: nunca, se o catálogo da `stablyai`
  continuar a ser tratado como oficial.
- **Tirar o token do runtime do alcance do worker**, pelo modo de permissão do Node. Custo: mexe no host de plugins do
  upstream, com conflito em todo sync. Se paga: só se plugins virarem uso real.
