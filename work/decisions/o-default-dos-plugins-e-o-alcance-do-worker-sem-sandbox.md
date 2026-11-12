---
status: done
description: Se o sistema de plugins do BrzA Studio fica desligado por padrão e como limitar o worker Node sem sandbox que alcança o token do runtime.
scope:
  - brza-studio
opened: 2026-11-12
decided: 2026-11-12
decided_by: Anderson
owner: Anderson
priority: high
tags:
  - infra
---

# O default dos plugins e o alcance do worker sem sandbox

Decidido por Anderson em 2026-11-12, com a frase "ambos recomendado", junto da R1 do PLN-014: **desligar o sistema de
plugins por padrão no fork**.

No código atual do `brza-studio`, o default vive em `src/shared/default-global-settings.ts`
(`pluginSystemEnabled` / `pluginSystemDefaultedOn`). A normalização em
`src/shared/plugins/plugin-system-settings.ts` trata `pluginSystemDefaultedOn: true` como guarda do rollout: com ela
verdadeira, um `pluginSystemEnabled: false` explícito **permanece** desligado. Por isso o fork grava
`pluginSystemEnabled: false` e mantém `pluginSystemDefaultedOn: true` — pôr só `pluginSystemDefaultedOn: false` no
default faria o normalizer reativar o sistema.

Recusado: manter ligado e só instalar plugin lido (custo zero, nunca se paga enquanto o catálogo oficial pular
confiança). Recusado nesta passagem: isolar o token do runtime do worker (custo de host upstream); fica para se plugins
voltarem a uso real.

Evidência Context7: Electron `utilityProcess` / `NodeService` com `ServiceSandbox=kNoSandbox`.

Registrada no worklog
[R1 do PLN-014 e default dos plugins](../worklogs/2026-11-12-r1-pln-014-e-default-dos-plugins.md). O patch do fork
(`pluginSystemEnabled: false` em `src/shared/default-global-settings.ts`, mantendo `pluginSystemDefaultedOn: true`)
está pronto; o push ao `brza-studio` nesta sessão recebeu 403 do `cursor[bot]` — aplicar na sessão do `studio` ou com
a chave `personal`.
