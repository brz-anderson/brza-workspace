---
status: open
description: Os PRs #38189, #38180 e #38199 do upstream reduzem drasticamente o consumo de memória e processos de agentes via idle reaper para servidores TypeScript LSP e otimização de hooks do Claude.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#38189`](https://github.com/stablyai/orca/pull/38189) (Issue
[`#38188`](https://github.com/stablyai/orca/issues/38188)),
[`stablyai/orca#38180`](https://github.com/stablyai/orca/pull/38180) (Issue
[`#38179`](https://github.com/stablyai/orca/issues/38179)) e
[`stablyai/orca#38199`](https://github.com/stablyai/orca/pull/38199) (Issue
[`#38181`](https://github.com/stablyai/orca/issues/38181)).

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

## O que fazer

Portar a redução de overhead de hooks (`#38180`) e o reaper de LSP ocioso (`#38189`) para o `brza-studio`, assegurando que
workflows com dezenas de agentes concorrentes não degradem a CPU nem esgotem a memória da máquina de desenvolvimento.
