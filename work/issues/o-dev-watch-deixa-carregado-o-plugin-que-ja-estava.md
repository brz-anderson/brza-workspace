---
status: open
description: O plugin dev watch interrompido emite unloaded, mas deixa no devPluginPaths a pasta que um dev load anterior pôs; o plugin aprovado volta a rodar quando o app abre de novo.
scope:
  - brza-studio
opened: 2026-11-03
tags:
  - tooling
---

# O dev watch deixa carregado o plugin que já estava

Achado no spike do C5 do [PLN-003](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-plan.md), em 2026-11-03, no
Orca `1.4.247`.

## O que falhou

A sequência:
1. `orca plugin dev load <pasta> --json --approve ap1-…` carregou e aprovou o plugin `local.brza-spike-c5`, um
   `trusted-worker` com `terminal:send`.
2. `orca plugin dev watch <pasta> --check --shot … --json` emitiu `loaded`, `check`, `shot` e `reloaded`.
3. Um `SIGINT` no watch emitiu `{"type":"unloaded","path":"<pasta>"}`.
4. Com o Orca fechado, o documento `settings` do `profile-state.db` ainda tinha
   `"devPluginPaths":["…/spikes/c5-plugin"]`.
5. Com o Orca aberto de novo, `orca plugin list --json` mostrava o plugin com `status: running` e `isDev: true`.

Só o `orca plugin dev unload <pasta>` tirou a pasta (`"devPluginPaths":[]`).

## Por que importa

- **O evento `unloaded` diz que a pasta saiu, e ela não saiu.** Quem confia nele deixa um worker aprovado com acesso ao
  terminal carregado no app, e o worker volta a rodar na próxima abertura.
- **Inferência, não conferida no código:** o watch só tira a pasta que ele mesmo pôs. No passo 2, a pasta já estava
  carregada. Se for isso, o defeito está no evento, que deveria dizer que a pasta continuou.

## O que fazer

Ler no `brza-studio` o caminho do `dev watch` até o `setDevPluginPaths` (`src/main/startup/main-process-plugins.ts:245`),
confirmar a inferência e decidir entre corrigir o evento e tirar a pasta. Até lá, o fim de um spike roda o `dev unload`
nos dois apps e confere o `devPluginPaths`.
