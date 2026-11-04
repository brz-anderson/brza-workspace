---
status: open
description: As issues #37788, #37826 e #37949 e os PRs #37806, #37971 e #37926 trazem suporte a workers em hosts remotos, gerenciamento CLI de targets SSH (host rm) e IdentitiesOnly.
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

Rastreado das issues abertas no upstream [`stablyai/orca#37788`](https://github.com/stablyai/orca/issues/37788),
[`stablyai/orca#37826`](https://github.com/stablyai/orca/issues/37826) e
[`stablyai/orca#37949`](https://github.com/stablyai/orca/issues/37949), além dos PRs
[`stablyai/orca#37971`](https://github.com/stablyai/orca/pull/37971),
[`stablyai/orca#37926`](https://github.com/stablyai/orca/pull/37926) e
[`stablyai/orca#37806`](https://github.com/stablyai/orca/pull/37806).

## O problema

1. **Workers de plugins isolados da máquina onde os repositórios moram (`#37788`):** ao conectar a um ambiente de
   execução pareado remoto (`orcad`), o daemon remoto não possui o serviço de execução de plugins. Todos os workers de
   plugins rodam localmente no processo Electron do desktop, longe dos arquivos, ferramentas e repositórios Git remotos.
   Além disso, as views declarativas de plugins só podiam ser renderizadas na barra lateral direita, sem suporte a
   abertura como abas dedicadas de workspace.
2. **Falta de gerenciamento CLI de servidores SSH para agentes (`#37826`, `#37949`, `#37971`):** embora o runtime possua
   as chamadas RPC internas de gerenciamento de alvos SSH (`ssh.target-management.v1`), faltavam comandos públicos na
   linha de comando para listar e remover hosts salvos (`orca host rm` / `brza host rm`). Agentes autônomos que
   provisionam e desprovisionam máquinas em nuvem não conseguiam limpar hosts efêmeros nem respeitar regras de blocos
   `Match` importados do `~/.ssh/config`.
3. **Respeito a `IdentitiesOnly` no transporte SSH nativo (`#37926`):** conexões manuais com chave específica falhavam
   quando o agente SSH local oferecia múltiplas identidades antes da chave configurada, porque o transporte interno não
   repassava o parâmetro `IdentitiesOnly=yes`.
4. **Falta de suporte a syntax highlight para MDX em painéis de plugins (`#37806`):** plugins que exibem código e
   documentação rica não tinham suporte a realce de sintaxe de arquivos `.mdx`.

## O caminho proposto no upstream

- **Para hosts e transporte SSH (`#37971`, `#37949`, `#37926`, `#37826`):**
  - Implementa `orca host rm <host-alias>` na CLI para remoção de servidores salvos com confirmação ou flag `--yes`;
  - Aplica estritamente a diretiva `IdentitiesOnly` em conexões SSH manuais no transporte embutido;
  - Documenta a resolução de blocos `Match` na importação de configurações SSH do sistema.
- **Para plugins (`#37788`, `#37806`):**
  - Introduzir propriedade no manifesto do plugin (ex.: `"runsOn": "workspace"`) permitindo que o processo worker seja
    executado diretamente no host remoto (`orcad` ou via SSH);
  - Permitir que painéis de plugins sejam abertos como abas completas de workspace no editor principal;
  - Habilitar gramática de sintaxe MDX para visualizadores de documentação.

## O que fazer

Incorporar o subcomando `brza host rm` e o respeito a `IdentitiesOnly` no ferramental de infraestrutura do `brza-studio`
e `tools-kit`, permitindo ciclo de vida completo de ambientes remotos gerenciados por agentes.
