---
status: open
description: Os PRs #41850, #41815, #41824 trazem orca chat send/close, orca agent list/show/read por sessão unificada e renomeação de contas salvas.
scope:
  - brza-studio
  - brza-workflow
  - brza-cli
priority: high
opened: 2026-11-13
tags:
  - tooling
  - chat
---

# Controle de agentes e chats pela CLI por ID de sessão e rotulagem de contas

Rastreado dos PRs abertos no upstream [`stablyai/orca#41850`](https://github.com/stablyai/orca/pull/41850),
[`stablyai/orca#41815`](https://github.com/stablyai/orca/pull/41815) e
[`stablyai/orca#41824`](https://github.com/stablyai/orca/pull/41824) (resolve Issue [`#21182`](https://github.com/stablyai/orca/issues/21182)).

## O problema

1. **Incapacidade de continuar ou fechar conversas existentes de chat nativo pela CLI (`#41850`):**
   - O comando `orca agent launch` era a única forma via CLI de iniciar mensagens com agentes de chat, mas sempre abria uma nova aba do zero sem carregar o histórico de conversas anteriores;
   - Scripts e orquestradores que precisavam dar instruções contínuas ou nudges em um chat existente eram forçados a criar dezenas de abas concorrentes, sem nenhuma opção de fechar abas programaticamente (`orca chat close`).
2. **Falta de inspeção e leitura direta de agentes por ID de sessão canônico (`#41815`):**
   - Sistemas externos (bridges Slack, assistentes de voz, agendadores e outros agentes coordenadores) não tinham uma interface consolidada para listar agentes em execução entre worktrees, chats nativos e abas de terminal sob uma mesma chave de identificação;
   - Para ler o que um agente respondeu, dependia-se de raspagem frágil de telas de terminal (`orca terminal read`) ou APIs proprietárias específicas de cada provedor, sem suporte a leitura por cursores ou histórico completo sem despertar o agente.
3. **Impossibilidade de distinguir e rotular contas salvas de Claude e Codex com o mesmo e-mail (`#41824`, resolve `#21182`):**
   - Na listagem de contas em *Settings > Accounts*, seletores da status bar, toasts e na CLI (`orca account list`), contas pessoais e corporativas que utilizavam o mesmo e-mail apareciam com descrições idênticas;
   - Usuários não conseguiam atribuir apelidos ou nomes amigáveis para diferenciar organizações, e os diálogos de remoção não especificavam claramente qual diretório e credenciais seriam deletados.

## O que o upstream implementa

1. **Subcomandos `orca chat send` e `orca chat close` na CLI (`#41850`):**
   - Introduz `orca chat send --session <id> (--text <text> | --text-file <path|->) [--json]`, enviando texto diretamente para a conversa existente com suporte a enfileiramento (`queue-if-active`) se o turno estiver em execução;
   - Introduz `orca chat close --session <id> [--json]`, encerrando a sessão do agente e fechando a aba com preservação integral no Session History;
   - Reutiliza os métodos de host existentes com permissão `workspace`, sem exigir novos métodos RPC ou permissões extras.
2. **Comandos universais `orca agent list`, `show` e `read` por `orcaSessionId` (`#41815`):**
   - Permite listar (`orca agent list [--worktree <selector>] [--state <state>]`), localizar (`orca agent show <id>`) e ler conversas completas (`orca agent read <id> [--limit <n>] [--cursor <cursor>]`) tanto para chats nativos quanto para agentes de terminal;
   - Utiliza o identificador persistente `orca_session_id:<agent>_<uuid>` para roteamento determinístico entre hosts pareados e WSL sem inicializar ou acordar processos dormindo.
3. **Renomeação amigável e rotulagem clara de contas Claude e Codex (`#41824`, resolve `#21182`):**
   - Adiciona a ação **Rename** para contas salvas em *Settings > Accounts*, armazenando nomes customizados por host em `managedAccountDisplayNames.claude|codex`;
   - Exibe o formato `Nome (email)` na status bar, toasts, CLI e clientes móveis, e aceita o nome customizado em `orca account select` e `orca account rm`;
   - Esclarece nos diálogos de remoção o caminho exato e escopo dos arquivos a serem apagados no host local ou remoto.

## O que fazer

- Adotar os comandos `brza chat send` e `brza chat close` (`#41850`) para viabilizar envio contínuo e encerramento de conversas via CLI e automações.
- Implementar os comandos universais `brza agent list`, `brza agent show` e `brza agent read` (`#41815`) para unificar inspeção de chats e agentes de terminal por `orca_session_id`.
- Incorporar a renomeação amigável de contas salvas de IA e exibição de apelidos na barra de status e CLI (`#41824`, resolve `#21182`).
