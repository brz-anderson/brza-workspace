---
scope:
  - brza-studio
  - brza-workflow
  - workspace
opened: 2026-11-14
completed: 2026-11-14
tags:
  - tooling
refs:
  - issue:alocacao-de-chats-sob-host-independente-admissao-de-git-e-cache-de-modelos
  - issue:autenticacao-mcp-no-chat-alerta-de-turnos-ativos-e-cache-de-orquestracao
  - issue:cursor-no-chat-via-acp-previa-de-links-de-imagem-bifurcacao-resiliente-e-leitura-por-voz
  - issue:painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat
  - issue:seguranca-macos-remocao-de-allow-dyld-environment-variables-dos-entitlements
---

# Radar de issues e PRs do upstream e automação de 6h (00h, 06h, 12h e 18h BRT)

## O que foi feito

### 1. Ciclo de 6h (00:00 BRT / 03:00 UTC em 2026-11-14)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-13T21:00:00Z` e `2026-11-14T03:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Cursor no Chat via ACP, prévia de links de imagem, bifurcação resiliente e leitura por voz](../issues/cursor-no-chat-via-acp-previa-de-links-de-imagem-bifurcacao-resiliente-e-leitura-por-voz.md):
     rastreia o PR `#42193` (e `#41494` — execução do agente Cursor no Native Chat via servidor ACP com modelos, esforço e planos),
     PR `#42227` (renderização automática de prévia visual de arquivos de imagem locais gerados que são linkados em respostas Markdown),
     PR `#42215` (resolve Issue `#41903` — enfileiramento confiável de `/fork` durante a geração de resposta para bifurcar após o término do turno),
     PR `#42168` (leitura em voz alta de respostas finalizadas com botão Speak e controles de fala/TTS nas configurações de chat),
     PR `#42211` (envelopamento de listas extensas de parâmetros de agentes em cartões com rolagem vertical),
     além das issues `#42214` (cópia rica com arquivo e linha de seleções Markdown) e `#42187` (limpeza de thread com `/new` no mobile).
3. **Atualização de 4 issues existentes em `work/issues/`:**
   - [Autenticação MCP no chat, alerta de turnos ativos e cache de orquestração](../issues/autenticacao-mcp-no-chat-alerta-de-turnos-ativos-e-cache-de-orquestracao.md):
     adicionados o PR `#42222` e o PR `#42224` (painel de gerenciamento de servidores MCP via `/mcp` no chat desktop e mobile para listar, reconectar e ligar/desligar servidores) e
     o PR `#42219` (cartões visuais dedicados no chat para solicitações de sign-in web requisitadas por servidores MCP e agentes).
   - [Segurança no macOS: remoção de allow-dyld-environment-variables dos entitlements e colisão de LC_UUID](../issues/seguranca-macos-remocao-de-allow-dyld-environment-variables-dos-entitlements.md):
     adicionados o PR `#42245` / Issue `#38247` (UUID de executável e assinatura dedicada para o terminal host no macOS, estabilizando permissões de Local Network no macOS Sequoia) e
     o PR `#42136` / Issue `#39405` (leitura nativa in-process do layout de teclado no macOS, eliminando processos `orca-keyboard-layout` e vazamento de portas Mach no WindowServer).
   - [Painel de atividades de subagentes e anotações visuais no Native Chat](../issues/painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat.md):
     adicionado o PR `#42254` (limpeza imediata de referências e mapa de subagentes em memória ao fechar a aba de chat correspondente).
   - [Alocação de chats locais sob host independente, admissão de Git e cache de modelos](../issues/alocacao-de-chats-sob-host-independente-admissao-de-git-e-cache-de-modelos.md):
     adicionados o PR `#42253` (I/O assíncrono para leitura e gravação de conexões de servidores remotos fora da thread principal),
     o PR `#42247` (isolamento de slots de descoberta de modelos para impedir que CLIs travadas bloqueiem outros agentes) e
     o PR `#42189` (gravação assíncrona fora da thread principal para armazenamento de extensões do navegador).
