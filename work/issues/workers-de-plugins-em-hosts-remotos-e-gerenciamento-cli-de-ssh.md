---
status: open
description: Os PRs #41910, #40589, #38774 e as issues #37788, #37826, #37949, #38347 e #38673 trazem painéis de plugins no host pareado, deltas de catálogo em servidores pareados, orca host rm na CLI e correções remotas.
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

<!-- pln-014-despacho -->
> **Despacho (PLN-014/R1.1):** classe `parcial` · casa `studio`
> Merge no upstream não muda `status`. PLN-014/R1, 2026-11-12.

Rastreado dos PRs abertos no upstream [`stablyai/orca#41910`](https://github.com/stablyai/orca/pull/41910),
[`stablyai/orca#40589`](https://github.com/stablyai/orca/pull/40589) (resolve Issue [`#38342`](https://github.com/stablyai/orca/issues/38342)),
[`stablyai/orca#38774`](https://github.com/stablyai/orca/pull/38774) (Issues [`#37826`](https://github.com/stablyai/orca/issues/37826) e [`#37949`](https://github.com/stablyai/orca/issues/37949)),
além das issues [`stablyai/orca#38673`](https://github.com/stablyai/orca/issues/38673),
[`stablyai/orca#38669`](https://github.com/stablyai/orca/issues/38669),
[`stablyai/orca#38347`](https://github.com/stablyai/orca/issues/38347),
[`stablyai/orca#38342`](https://github.com/stablyai/orca/issues/38342),
[`stablyai/orca#38343`](https://github.com/stablyai/orca/issues/38343),
[`stablyai/orca#38341`](https://github.com/stablyai/orca/issues/38341),
[`stablyai/orca#38340`](https://github.com/stablyai/orca/issues/38340) e
[`stablyai/orca#37788`](https://github.com/stablyai/orca/issues/37788), e dos PRs
[`stablyai/orca#38782`](https://github.com/stablyai/orca/pull/38782),
[`stablyai/orca#37971`](https://github.com/stablyai/orca/pull/37971),
[`stablyai/orca#37926`](https://github.com/stablyai/orca/pull/37926) e
[`stablyai/orca#37806`](https://github.com/stablyai/orca/pull/37806).

## O problema

1. **Remoção de servidores SSH restrita à interface gráfica (`#38774`, `#37826`, `#37949`):**
   Agentes de IA e scripts de CI/CD que criam instâncias remotas efêmeras não conseguiam remover alvos SSH salvos via CLI,
   acumulando conexões fantasmas e nomes customizados no app principal.
2. **Falha de comandos CLI somente-leitura remotos com `chmod EPERM` local (`#38673`):**
   Comandos CLI de leitura remota (ex.: `orca worktree ps --environment <server>`) falhavam abruptamente no macOS com
   `EPERM: operation not permitted, chmod '<userData>/orca'` ao tentar registrar métricas de uso de ambiente em disco local.
3. **Criação de novo workspace desviando para o runtime remoto ativo (`#38669`, `#38782`):**
   Ao tentar criar um novo workspace com opção visível "Run on: Local Mac" enquanto um workspace em runtime remoto (VM)
   estava focado, o criador criava inadvertidamente o novo worktree no servidor remoto em vez da máquina local.
4. **Hosts SSH atrás de ProxyCommand travados por porta 6768 em uso (`#38347`):**
   Em servidores remotos acessados via túneis ou Coder ProxyCommand, quando uma sessão anterior encerra ou é desconectada
   manualmente, o processo `orca serve` anterior permanece prendendo a porta 6768, impossibilitando novas conexões e
   deixando o ambiente em estado zumbi difícil de recuperar sem matar o processo manualmente via terminal SSH direto.
5. **Workers de plugins isolados da máquina onde os repositórios moram (`#37788`):** ao conectar a um ambiente de
   execução pareado remoto (`orcad`), o daemon remoto não possui o serviço de execução de plugins. Todos os workers de
   plugins rodam localmente no processo Electron do desktop, longe dos arquivos, ferramentas e repositórios Git remotos.
6. **Isolamento de plugins entre cliente desktop pareado e host remoto (`#38342`, `#38343`, `#38341`, `#38340`):**
   - Falta de repasse de mensagens leves entre o worker no host e o plugin pareado no cliente desktop (`#38343`);
   - Falta de renderização de painéis de plugins remotos no cliente desktop pareado (`#38342`).
7. **Respeito a `IdentitiesOnly` no transporte SSH nativo (`#37926`):** conexões manuais com chave específica falhavam
   quando o agente SSH local oferecia múltiplas identidades antes da chave configurada, porque o transporte interno não
   repassava o parâmetro `IdentitiesOnly=yes`.
8. **Latência e sobrecarga de polling de catálogo de worktrees em servidores pareados (`#41910`):**
   Clientes pareados e feeds móveis dependiam de varreduras completas (`worktree.ps`) repetidas a intervalos fixos para detectar
   alterações de status, branches e novos worktrees em daemons remotos, gerando latência de vários segundos e tráfego redundante.

## O caminho proposto no upstream

- **Deltas reativos de catálogo via `worktreeRowsChanged` (`#41910`):**
  - Implementa evento `worktreeRowsChanged` emitido pelo daemon de servidor pareado contendo apenas as linhas de catálogo modificadas;
  - Clientes conectados e feeds remotos sincronizam atualizações em ~2s sem necessidade de varredura total.
- **Subcomando CLI `orca host rm` com limpeza profunda (`#38774`, resolve `#37826` e `#37949`):**
  - Adiciona `orca host rm <host>` permitindo excluir servidores SSH diretamente pelo terminal;
  - Limpa de forma consistente em todo o aplicativo o estado da conexão ao vivo, alvos pareados e rótulos customizados.
- **Correção no roteamento de criação de novos workspaces (`#38782`, resolve `#38669`):**
  - Assegura que a escolha explícita do seletor "Run on" (ex.: máquina local) seja respeitada mesmo quando uma VM remota
    estiver em foco no momento da abertura do composer.
- **Tratamento de permissões locais em consultas remotas (`#38673`):**
  - Isola a gravação de telemetria local para evitar bloqueios `EPERM` durante consultas somente leitura via CLI.
- **Execução de painéis de plugins no host pareado do workspace focado (`#40589`, resolve `#38342`):**
  - Implementa RPC de streaming `plugins.panelSession` (host-admin) com validação de fingerprint de consentimento idêntico em ambas as pontas;
  - Faz com que chamadas de host e pushes de eventos do painel na barra lateral direita conversem diretamente com a cópia do plugin no computador remoto onde o workspace vive;
  - Renderiza nota informativa `Running on <host>` no topo do painel e cai de volta em execução local caso o host remoto não tenha o plugin instalado ou seja inalcançável.
- **Liberação de portas e robustez SSH (`#38347`, `#37926`):**
  - Limpeza de processos zumbis de `orca serve` e aplicação estrita de `IdentitiesOnly`.
- **Comunicação de plugins host-cliente (`#38343`):**
  - Relay leve de mensagens entre o worker no host e o plugin pareado no cliente desktop.

## O que fazer

- Adotar o evento reativo `worktreeRowsChanged` (`#41910`) para atualização contínua e rápida de catálogo de worktrees em servidores pareados e feeds móveis.
- Adotar a sessão remota de painéis de plugins via `plugins.panelSession` (`#40589`) para que painéis de plugins na barra lateral reflitam com fidelidade os dados do host onde o workspace ativo está hospedado.
- Implementar `brza host rm` (`#38774`) na CLI do `brza`, permitindo ciclo de vida completo de servidores em automações.
- Adotar o isolamento estrito de host em criação de novos workspaces (`#38782`) no `brza-studio`.
- Incorporar o fix de permissões `chmod EPERM` (`#38673`) no ferramental de infraestrutura.
