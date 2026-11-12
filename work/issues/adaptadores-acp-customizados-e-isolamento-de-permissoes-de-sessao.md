---
status: open
description: Os PRs #41229, #41201, #41243, #38826, #38807 trazem redação de credenciais em ACP stderr, comando oficial do Cursor e isolamento de variáveis.
scope:
  - brza-studio
  - brza-workflow
priority: high
opened: 2026-11-03
tags:
  - chat
  - tooling
---

# Adaptadores ACP customizados e isolamento de permissões de sessão

<!-- pln-014-despacho -->
> **Despacho (PLN-014/R1.1):** classe `ausente` · casa `studio`
> Merge no upstream não muda `status`. PLN-014/R1, 2026-11-12.

Rastreado dos PRs abertos no upstream [`stablyai/orca#41229`](https://github.com/stablyai/orca/pull/41229) (resolve Issue [`#41170`](https://github.com/stablyai/orca/issues/41170)),
[`stablyai/orca#41201`](https://github.com/stablyai/orca/pull/41201) (resolve Issue [`#41185`](https://github.com/stablyai/orca/issues/41185)),
[`stablyai/orca#41243`](https://github.com/stablyai/orca/pull/41243),
[`stablyai/orca#41228`](https://github.com/stablyai/orca/pull/41228),
[`stablyai/orca#41230`](https://github.com/stablyai/orca/pull/41230),
[`stablyai/orca#38826`](https://github.com/stablyai/orca/pull/38826),
[`stablyai/orca#38807`](https://github.com/stablyai/orca/pull/38807) (Issue [`#38806`](https://github.com/stablyai/orca/issues/38806)),
[`stablyai/orca#37842`](https://github.com/stablyai/orca/pull/37842),
[`stablyai/orca#37895`](https://github.com/stablyai/orca/pull/37895) (Issue [`#37889`](https://github.com/stablyai/orca/issues/37889)),
[`stablyai/orca#37861 (CLOSED sem merge no upstream)`](https://github.com/stablyai/orca/pull/37861) (Issue [`#37859 (CLOSED no upstream)`](https://github.com/stablyai/orca/issues/37859)),
[`stablyai/orca#37862`](https://github.com/stablyai/orca/issues/37862) e
[`stablyai/orca#37883 (MERGED no upstream; não está no fork)`](https://github.com/stablyai/orca/pull/37883), além das issues
[`stablyai/orca#38866`](https://github.com/stablyai/orca/issues/38866) e
[`stablyai/orca#38849`](https://github.com/stablyai/orca/issues/38849).

## O problema

1. **Incompatibilidade de contas Codex armazenadas no chaveiro do sistema operacional (`#38826`):**
   O app presumia que credenciais do Codex sempre residiam em arquivos `~/.codex/auth.json`. No Windows Credential Manager
   e sistemas com chaveiros nativos (`keyring` / `secret_auth_storage`), nenhum arquivo `auth.json` é gerado, fazendo com que
   o gerenciador de contas do app marcasse o usuário erroneamente como deslogado ("Needs sign-in") e falhasse com ENOENT
   ao provisionar homes gerenciadas.
2. **Gravação incorreta do marcador de confiança do workspace para o Cursor (`#38807`, `#38806`):**
   Ao iniciar o `cursor-agent` em um novo worktree, o app tentava pré-autorizar a pasta escrevendo em `~/.cursor/projects/<slug>`.
   Porém, o algoritmo de slug substituía apenas caracteres ilegais no Windows em vez de converter todos os caracteres não
   alfanuméricos (como `_`, `.`, espaços) em hífens repetidos colapsados, fazendo com que o Cursor ignorasse o marcador e
   exibisse repetidamente o modal de confiança.
3. **Escalação indevida de permissões no repasse de sessão para host SSH pareado (`#38866`):**
   Ao transferir (*handoff*) uma sessão de agente para um host Linux remoto pareado por SSH, o app repassava a flag de permissão
   do cliente local (ex.: `--dangerously-skip-permissions` / `full-access`) em vez de respeitar a política de segurança configurada
   no host remoto (`auto` / sandbox restrita).
4. **Falta de conector de primeira classe e scanner para o agente ZeroClaw (`#38849`):**
   O agente ZeroClaw (`zeroclaw`) não possuía registro no catálogo `TuiAgent`, tornando sessões em `~/.zeroclaw/` invisíveis no
   AI Vault e sem suporte a descoberta de skills canônicas.
5. **Agentes ACP externos limitados a adaptadores hardcoded (`#37842`):** para rodar agentes baseados no Agent Client
   Protocol (ACP) com interface gráfica de Native Chat, o runtime aceitava apenas os dialetos pré-compilados no binário.
6. **\"Allow for this session\" persistia permissões definitivas no disco (`#37895`, `#37889`):** no chat de Claude Code,
   ao aprovar uma ferramenta com \"Allow for this session\", o app repassava a sugestão com `destination: \"localSettings\"`,
   gravando permanentemente a regra em `<projeto>/.claude/settings.local.json`.
7. **Fallback silencioso de modelo (`#37861 (CLOSED sem merge no upstream)`, `#37859 (CLOSED no upstream)`):** quando o Claude realizava fallback automático de modelo,
   o composer permanecia fixado no modelo antigo sem feedback ao usuário.
8. **Tarefas de background sem inspeção de saída ao vivo (`#37862`):** comandos disparados em background pelo agente
   exibiam apenas uma linha de status estática no chat.

## O que o upstream implementa e corrige

- **Detecção de credenciais em Keyring para contas Codex (`#38826`):**
  - Consulta o CLI do Codex diretamente para resolver credenciais salvas no chaveiro do sistema, sincronizando cópias
    compatíveis em `auth.json` apenas quando exigido pelas homes isoladas gerenciadas pelo app.
- **Normalização de slugs de confiança para o Cursor (`#38807`):**
  - Alinha a geração de slugs em `~/.cursor/projects/` com a regra oficial do `cursor-agent` 2026.11, garantindo que
    pastas com pontos, sublinhados e caracteres especiais sejam reconhecidas como confiáveis de imediato.
- **Respeito às políticas de segurança do host remoto em handoffs (`#38866`):**
  - Corrige a propagação de permissões para priorizar as restrições e políticas de segurança definidas no host remoto de execução.
- **Suporte nativo ao agente ZeroClaw (`#38849`):**
  - Registra o `zeroclaw` no catálogo de agentes TUI, integra a descoberta de skills e indexa transcrições JSONL no AI Vault.
- **Adaptadores ACP customizados configuráveis no host (`#37842`):** permite declarar adaptadores arbitrários em
  `customAgentAdapters` nas configurações do host, definindo comando, argumentos, variáveis de ambiente e transporte (`stdio` ou `sse`).
- **Isolamento estrito de aprovações de sessão (`#37895`):** reescreve o destino de regras de "Allow for this session" para
  `"session"` no RPC de aprovação, mantendo as permissões apenas em memória.
- **Reflexo de fallback e visibilidade de turnos (`#37861 (CLOSED sem merge no upstream)`, `#37883 (MERGED no upstream; não está no fork)`):** exibe alertas no chat e ajusta o seletor do composer
  quando há fallback de modelo.
- **Redação de credenciais e segredos em stderr de agentes ACP (`#41229`, resolve `#41170`):**
  - Aplica filtros de higienização de credenciais, chaves e tokens de autenticação em saídas de stderr emitidas por agentes ACP
    antes de armazená-las em mensagens de erro do chat e nas transcrições salvas em disco.
- **Transição para o comando oficial `agent` do Cursor (`#41201`, resolve `#41185`):**
  - Adota `agent` em vez do binário legado `cursor-agent`, alinhando flags de inicialização e rotas de descoberta com a versão oficial atual.
- **Isolamento de variáveis de ambiente de tarefas Codex (`#41243`):**
  - Impede que variáveis de ambiente injetadas em tarefas de geração de código e Codex vazem para agentes de chat e outros adaptadores de texto.
- **Contenção e sandbox para sessões Hermes (`#41228`, `#41230`, `#41231`):**
  - Limita a herança de ambiente e acesso CLI a chats Hermes, impede ativação indevida de `--yolo` em trocas de permissão e inclui checks de setup nas configurações.

## O que fazer

- Implementar a redação de segredos e credenciais em stderr de adaptadores ACP (`#41229`, resolve `#41170`).
- Adotar o comando oficial `agent` do Cursor (`#41201`, resolve `#41185`) e o isolamento de variáveis do Codex (`#41243`).
- Aplicar as regras de contenção e sandbox para sessões Hermes (`#41228`, `#41230`).
- Adotar o suporte a credenciais em Keyring do Codex (`#38826`) e a correção de slugs de trust do Cursor (`#38807`).
- Garantir que permissões de agentes respeitem as configurações do host de execução em ambientes remotos (`#38866`).
- Portar o suporte de adaptadores customizados ACP (`#37842`) e o conector ZeroClaw (`#38849`) para o `brza-studio`.
