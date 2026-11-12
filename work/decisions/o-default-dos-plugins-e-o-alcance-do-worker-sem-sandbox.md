---
status: open
description: Se o sistema de plugins do BrzA Studio fica desligado por padrão e como limitar o worker Node sem sandbox que alcança o token do runtime.
scope:
  - brza-studio
opened: 2026-11-12
owner: Anderson
priority: high
blocks: O default dos plugins e o endurecimento do worker ficam sem direção até Anderson fechar esta proposta.
trigger: Resposta explícita de Anderson nesta proposta (decidido, fechado ou pode aplicar).
tags:
  - infra
---

# O default dos plugins e o alcance do worker sem sandbox

Proposta aberta na auditoria de 2026-11-12
([Priorização: issues high × planos abertos × Context7](../worklogs/2026-11-12-priorizacao-issues-high-planos-e-context7.md)).
A issue de origem mora no workstream `studio`: *O worker de plugin sem sandbox alcança o token do runtime* (sem
`priority` no frontmatter; risco condicional a instalar plugin com worker).

## O que espera

Anderson escolhe o default do sistema de plugins e se o fork tenta isolar o token do runtime do worker.

## Evidência

- No `brza-studio` (levantamento da issue): worker com `ELECTRON_RUN_AS_NODE`, sem sandbox de permissão Node; alcança
  `userData/orca-runtime.json` (`authToken`), chaves de autoridade e diretórios `~/.claude` / `~/.codex` / `~/.ssh`.
  Frames isolados e rede do guest estão limpos; o catálogo "oficial" pula o diálogo de confiança.
- **Context7 / Electron:** `utilityProcess` / `NodeService` roda com `ServiceSandbox=kNoSandbox`; habilitar
  `nodeIntegration` desliga sandbox do renderer. Docs: `tutorial/sandbox.md`, `api/utility-process.md`.

## Opções

1. **Desligar `pluginSystemDefaultedOn` no fork (Recomendado).**  
   Custo: um default + migração de perfil. Se paga: já, se Anderson não usa plugins agora.

2. **Manter ligado e só instalar plugin lido por Anderson.**  
   Custo: nenhum código. Se paga: nunca, enquanto o catálogo upstream for tratado como oficial.

3. **Manter ligado e isolar o token do runtime do worker (permissões Node / host).**  
   Custo: mexer no host de plugins do upstream, conflito em todo sync. Se paga: só com uso real de plugins.

## Gatilho

Resposta explícita de Anderson ("decidido" / "fechado" / "pode aplicar") nesta proposta ou na issue do studio. Sem
frase, permanece `open`.
