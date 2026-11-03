---
status: open
description: As issues #37788 e #37826 e o PR #37806 trazem suporte a workers de plugins no host do workspace remoto, gerenciamento CLI de targets SSH e coloração de código MDX em plugins.
scope:
  - brza-studio
  - workspace
  - tools-kit
priority: medium
opened: 2026-11-03
tags:
  - tooling
  - infra
---

# Workers de plugins em hosts remotos e gerenciamento CLI de SSH

Rastreado das issues abertas no upstream [`stablyai/orca#37788`](https://github.com/stablyai/orca/issues/37788) e
[`stablyai/orca#37826`](https://github.com/stablyai/orca/issues/37826), além do PR
[`stablyai/orca#37806`](https://github.com/stablyai/orca/pull/37806).

## O problema

1. **Workers de plugins isolados da máquina onde os repositórios moram (`#37788`):** ao conectar a um ambiente de
   execução pareado remoto (`orcad`), o daemon remoto não possui o serviço de execução de plugins. Todos os workers de
   plugins rodam localmente no processo Electron do desktop, longe dos arquivos, ferramentas e repositórios Git remotos.
   Além disso, as views declarativas de plugins só podiam ser renderizadas na barra lateral direita, sem suporte a
   abertura como abas dedicadas de workspace.
2. **Falta de gerenciamento CLI de servidores SSH para agentes (`#37826`):** embora o runtime possua as chamadas RPC
   internas de gerenciamento de alvos SSH (`ssh.target-management.v1`), não havia comandos públicos na linha de comando
   (`orca ssh target add/list/update/remove`). Agentes autônomos que provisionam instâncias e máquinas remotas em nuvem
   não conseguiam registrá-las dinamicamente para uso imediato pelo app sem intervenção manual do usuário na UI.
3. **Falta de suporte a syntax highlight para MDX em painéis de plugins (`#37806`):** plugins que exibem código e
   documentação rica não tinham suporte a realce de sintaxe de arquivos `.mdx`.

## O caminho proposto no upstream

- **Para plugins (`#37788`, `#37806`):**
  - Introduzir propriedade no manifesto do plugin (ex.: `"runsOn": "workspace"`) permitindo que o processo worker seja
    executado diretamente no host remoto (`orcad` ou via SSH);
  - Permitir que painéis de plugins sejam abertos como abas completas de workspace no editor principal;
  - Habilitar gramática de sintaxe MDX para visualizadores de documentação.
- **Na CLI de SSH (`#37826`):**
  - Expor subcomandos `brza ssh target add`, `list`, `update` e `remove` com suporte completo a flags de porta, usuário,
    chave de identidade (`--identity-file`), jump host (`--jump-host`) e saída JSON estruturada.

## O que fazer

Avaliar a extensão do runtime do `brza-studio` e CLI do `brza` para incorporar comandos de targets SSH e preparar a
arquitetura de plugins para rodar workers junto aos worktrees remotos.
