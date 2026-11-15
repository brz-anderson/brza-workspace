---
status: open
description: Os PRs #42686, #42743, #42725, #42660, #42655 e as issues #42724, #42675 trazem descarte de abas ociosas no serve, exec hooks seguros no Windows e fechamento ágil de terminais.
scope:
  - brza-studio
  - tools-kit
  - workspace
priority: high
opened: 2026-11-04
tags:
  - tooling
  - infra
---

# Consumo de recursos em agentes: reaper de LSP e overhead de hooks

Rastreado dos PRs abertos no upstream [`stablyai/orca#42686`](https://github.com/stablyai/orca/pull/42686),
[`stablyai/orca#42743`](https://github.com/stablyai/orca/pull/42743),
[`stablyai/orca#42725`](https://github.com/stablyai/orca/pull/42725) (resolve Issue [`#42724`](https://github.com/stablyai/orca/issues/42724)),
[`stablyai/orca#42660`](https://github.com/stablyai/orca/pull/42660) (resolve Issue [`#19116`](https://github.com/stablyai/orca/issues/19116)),
[`stablyai/orca#42655`](https://github.com/stablyai/orca/pull/42655),
[`stablyai/orca#38189`](https://github.com/stablyai/orca/pull/38189) (Issue [`#38188`](https://github.com/stablyai/orca/issues/38188)),
[`stablyai/orca#38180`](https://github.com/stablyai/orca/pull/38180) (Issue [`#38179`](https://github.com/stablyai/orca/issues/38179)),
[`stablyai/orca#38199`](https://github.com/stablyai/orca/pull/38199) (Issue [`#38181`](https://github.com/stablyai/orca/issues/38181)),
além das issues [`stablyai/orca#42675`](https://github.com/stablyai/orca/issues/42675) e
[`stablyai/orca#42601`](https://github.com/stablyai/orca/issues/42601).

## O problema

1. **Servidores TypeScript LSP órfãos consumindo dezenas de gigabytes de RAM (`#38189`, `#38188`):** cada sessão de agente
   operando no repositório instancia seu próprio servidor de linguagem TypeScript (`tsc --lsp`). Sessões que permaneciam
   ociosas ou conectadas em segundo plano não encerravam seus servidores; em ambientes com múltiplos agentes simultâneos,
   registrou-se acúmulo de mais de 28 GB de memória de trabalho mantidos por instâncias ociosas sem qualquer arquivo aberto.
2. **Explosão de processos nos ganchos gerenciados do Claude (`#38180`, `#38179`):** a cada evento de ferramenta do Claude
   Code (`PreToolUse`), o script de hook do app disparava cerca de 17 subprocessos no macOS e até 19 no Linux para
   computar cabeçalhos, metadados de painel e identidade do agente. Com múltiplos painéis ativos, isso atingia ~35 novos
   processos por segundo; no macOS, onde cada `exec` passa pela validação do `AppleSystemPolicy`, a latência de resposta das
   ferramentas crescia substancialmente sob carga.
3. **Evicção indevida do binário do runtime Node em servidores `orcad` (`#38199`, `#38181`):** a rotina de limpeza de cache de
   artefatos (`pruneOrcadArtifactCache`) removia erroneamente a pasta `runtimes/`, quebrando execuções remotas subsequentes
   com erro `ENOENT` ao tentar disparar o binário `node`.
4. **Consumo contínuo de CPU e GPU por abas de navegador não observadas no `orca serve` (`#42660`, resolve `#19116`):**
   Abas do navegador embutido abertas em segundo plano continuavam renderizando frames e executando loops visuais mesmo sem foco ou visibilidade, retendo centenas de megabytes de memória GPU.
5. **Sobrecarga de hooks de agentes disparados sem contexto Orca ativo (`#42655`):**
   Comandos executados fora do contexto de automação do Orca disparavam rotinas completas de inspeção de hooks antes do leitor de eventos, gerando lentidão e saídas bloqueantes desnecessárias.
6. **Disparos zumbis de hooks por chamadas órfãs de python3 após desinstalação (`#42601`):**
   Hooks residuais configurados no ambiente do usuário continuavam invocando `python3` ciclicamente mesmo após a remoção ou encerramento do app principal.
7. **Retenção contínua de memória por abas ociosas no `orca serve` (`#42686`):**
   Abas abertas no navegador remoto permaneciam alocadas em memória indefinidamente mesmo após horas de inatividade, sem descarregamento automático de processos filhos.
8. **Falhas na execução de hooks do Claude no Windows com espaços em caminhos de executáveis (`#42743`):**
   Quando o Claude era instalado em caminhos contendo espaços no Windows, o formato legado de invocação de hook falhava por erro de citação de linha de comando.
9. **Atraso de ~2.1s no fechamento de terminais e estouro de tiles de custos (`#42675`, `#42725`, resolve `#42724`):**
   O fechamento de terminais interativos zsh aguardava desnecessariamente 2.1s de grace period de SIGKILL porque o zsh ignora SIGTERM por padrão; em Stats & Usage, valores altos de custos transbordavam seus cartões visuais.

## O que o upstream propõe e implementa

- **Idle reaper com watchdog para o Agent LSP Bridge (`#38189`):**
  - Implementa monitoramento de documentos abertos e tráfego em ambas as direções;
  - Encerra automaticamente instâncias do TypeScript LSP após `ORCA_TS_LSP_IDLE_MS` (padrão de 1 hora) sem tráfego e
    com zero documentos abertos;
  - Reinicia o servidor de forma transparente assim que o agente volta a abrir um arquivo;
  - Fecha adequadamente pipes de `stdin` e trata sinais `SIGBREAK`/`exit`.
- **Redução de 17 para 7 processos por evento de hook (`#38180`):**
  - Implementa `orca_hook_pack_metadata`: empacota o cabeçalho `X-Orca-Hook-Metadata` uma única vez por painel em arquivo
    temporário atômico, reutilizando-o enquanto os dados de entrada permanecerem idênticos;
  - Lê identidade de agentes no Linux via `/proc/<pid>/stat` e `boot_id` com builtins do shell e no macOS ignora `uname`
    quando `OSTYPE` já é conhecido;
  - Reduz de 17 para 7 processos no macOS (e para 6 no Linux), preservando byte a byte as mensagens entregues ao servidor de hooks.
- **Proteção da pasta de runtimes no orcad (`#38199`):**
  - Exclui explicitamente o diretório `runtimes/` da política de evicção do cache de artefatos.
- **Suspensão de renderização e liberação de GPU em abas inativas do `orca serve` (`#42660`, resolve `#19116`):**
  - Pausa o renderizador contínuo e descarrega texturas de memória de vídeo para abas do navegador que não estão ativamente visíveis na interface remota, economizando ciclos de GPU e memória RAM sob concorrência.
- **Dreno rápido e saída limpa de hooks fora do contexto Orca (`#42655`):**
  - Detecta antecipadamente a ausência de variáveis de ambiente e sockets de controle do Orca, drenando a entrada e saindo com status 0 instantaneamente sem processamento pesado.
- **Tratamento de hooks órfãos de python3 (`#42601`):**
  - Desativa com segurança hooks obsoletos ao detectar ausência do executável principal ou flags de desinstalação.
- **Descarte e restauração transparente de abas ociosas no `orca serve` (`#42686`):**
  - Descarrega processos de abas do navegador remoto após período configurável de inatividade, restaurando a página sob demanda no primeiro acesso sem perder cookies nem contexto.
- **Formato seguro de exec hook para caminhos com espaços no Windows (`#42743`):**
  - Adota chamada estruturada em array de argumentos para hooks do Claude no Windows, eliminando falhas de quoting e caminhos com espaços.
- **Confinamento de custos em Stats & Usage e sinal de encerramento de terminal (`#42725`, `#42675`, resolve `#42724`):**
  - Ajusta a tipografia e contenção em tiles de custos grandes para evitar quebra de layout;
  - Trata o sinal de fechamento de terminais zsh para evitar esperar o timeout de 2.1s de SIGKILL.

## O que fazer

- Descarregar automaticamente abas ociosas de navegador no `brza serve` e restaurá-las sob demanda (`#42686`).
- Adotar o formato seguro de exec hook para caminhos de executáveis no Windows (`#42743`).
- Conter valores grandes de custos nos cartões de Stats & Usage (`#42725`, resolve `#42724`).
- Eliminar a espera desnecessária de 2.1s no fechamento de terminais zsh (`#42675`).
- Portar a redução de overhead de hooks (`#38180`) e o reaper de LSP ocioso (`#38189`) para o `brza-studio`.
- Aplicar a suspensão de renderização e liberação de GPU em abas não observadas do `orca serve` (`#42660`, resolve `#19116`).
- Adotar a saída rápida de hooks sem contexto Orca ativo (`#42655`).
- Prevenir a execução zumbi de hooks órfãos de python3 (`#42601`).
