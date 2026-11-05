---
status: open
description: As issues #37788, #37826, #37949, #38347 e #38342 e os PRs #37806, #37971 e #37926 tratam de workers em hosts remotos, ProxyCommand, mensageria de plugins e SSH CLI.
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

Rastreado das issues abertas no upstream [`stablyai/orca#38347`](https://github.com/stablyai/orca/issues/38347),
[`stablyai/orca#38342`](https://github.com/stablyai/orca/issues/38342),
[`stablyai/orca#38343`](https://github.com/stablyai/orca/issues/38343),
[`stablyai/orca#38341`](https://github.com/stablyai/orca/issues/38341),
[`stablyai/orca#38340`](https://github.com/stablyai/orca/issues/38340),
[`stablyai/orca#37788`](https://github.com/stablyai/orca/issues/37788),
[`stablyai/orca#37826`](https://github.com/stablyai/orca/issues/37826) e
[`stablyai/orca#37949`](https://github.com/stablyai/orca/issues/37949), além dos PRs
[`stablyai/orca#37971`](https://github.com/stablyai/orca/pull/37971),
[`stablyai/orca#37926`](https://github.com/stablyai/orca/pull/37926) e
[`stablyai/orca#37806`](https://github.com/stablyai/orca/pull/37806).

## O problema

1. **Hosts SSH atrás de ProxyCommand travados por porta 6768 em uso (`#38347`):**
   Em servidores remotos acessados via túneis ou Coder ProxyCommand, quando uma sessão anterior encerra ou é desconectada
   manualmente, o processo `orca serve` anterior permanece prendendo a porta 6768, impossibilitando novas conexões e
   deixando o ambiente em estado zumbi difícil de recuperar sem matar o processo manualmente via terminal SSH direto.
2. **Workers de plugins isolados da máquina onde os repositórios moram (`#37788`):** ao conectar a um ambiente de
   execução pareado remoto (`orcad`), o daemon remoto não possui o serviço de execução de plugins. Todos os workers de
   plugins rodam localmente no processo Electron do desktop, longe dos arquivos, ferramentas e repositórios Git remotos.
   Além disso, as views declarativas de plugins só podiam ser renderizadas na barra lateral direita, sem suporte a
   abertura como abas dedicadas de workspace.
3. **Isolamento de plugins entre cliente desktop pareado e host remoto (`#38342`, `#38343`, `#38341`, `#38340`):**
   - Não havia como um plugin rodando no host repassar pequenas mensagens ou sincronizar estado com a instância do mesmo
     plugin rodando no cliente desktop conectado (`#38343`);
   - Falta de renderização de painéis de plugins remotos no cliente desktop pareado (`#38342`);
   - Falta de sinalização de superfície em foco (`ui:focus`) para que plugins saibam onde o usuário está trabalhando (`#38341`);
   - Dificuldade dos plugins em distinguir perguntas interativas do agente de esperas de background comuns (`#38340`).
4. **Falta de gerenciamento CLI de servidores SSH para agentes (`#37826`, `#37949`, `#37971`):** embora o runtime possua
   as chamadas RPC internas de gerenciamento de alvos SSH (`ssh.target-management.v1`), faltavam comandos públicos na
   linha de comando para listar e remover hosts salvos (`orca host rm` / `brza host rm`). Agentes autônomos que
   provisionam e desprovisionam máquinas em nuvem não conseguiam limpar hosts efêmeros nem respeitar regras de blocos
   `Match` importados do `~/.ssh/config`.
5. **Respeito a `IdentitiesOnly` no transporte SSH nativo (`#37926`):** conexões manuais com chave específica falhavam
   quando o agente SSH local oferecia múltiplas identidades antes da chave configurada, porque o transporte interno não
   repassava o parâmetro `IdentitiesOnly=yes`.
6. **Falta de suporte a syntax highlight para MDX em painéis de plugins (`#37806`):** plugins que exibem código e
   documentação rica não tinham suporte a realce de sintaxe de arquivos `.mdx`.

## O caminho proposto no upstream

- **Para hosts e transporte SSH (`#38347`, `#37971`, `#37949`, `#37926`, `#37826`):**
  - Implementa detecção e liberação limpa de portas ocupadas (6768) ao inicializar servidor remoto em ambientes ProxyCommand;
  - Implementa `orca host rm <host-alias>` na CLI para remoção de servidores salvos com confirmação ou flag `--yes`;
  - Aplica estritamente a diretiva `IdentitiesOnly` em conexões SSH manuais no transporte embutido;
  - Documenta a resolução de blocos `Match` na importação de configurações SSH do sistema.
- **Para plugins (`#38342`, `#38343`, `#38341`, `#38340`, `#37788`, `#37806`):**
  - Introduzir relay de mensagens leves entre o worker do host e o plugin pareado no cliente desktop (`#38343`);
  - Suporte para expor painéis de plugins hospedados remotamente diretamente no app desktop pareado (`#38342`);
  - Introduzir evento declarativo de foco de interface (`ui:focus`) e tipagem de prompts (`agent prompt kind`);
  - Introduzir propriedade no manifesto do plugin (ex.: `"runsOn": "workspace"`) permitindo execução remota;
  - Habilitar gramática de sintaxe MDX para visualizadores de documentação.

## O que fazer

- Incorporar o subcomando `brza host rm` e o respeito a `IdentitiesOnly` no ferramental de infraestrutura do `brza-studio`
  e `tools-kit`.
- Mitigar retenção de portas em reconexões remotas (`#38347`).
- Preparar a infraestrutura de plugins para comunicação pareada host-cliente (`#38342`, `#38343`).
