---
priority: high
tags:
  - chat
  - tooling
  - design
description: Os PRs #42598, #42650 e #42647 trazem Devin como agente estruturado ACP com adoção de sessões, resposta citada direta a mensagens e abertura de arquivos alterados HTML e Markdown.
---

# Integração nativa do Devin no chat, respostas a mensagens específicas e abertura de arquivos alterados

Rastreado dos PRs abertos no upstream [`stablyai/orca#42598`](https://github.com/stablyai/orca/pull/42598) (resolve Issue [`#30791`](https://github.com/stablyai/orca/issues/30791)),
[`stablyai/orca#42650`](https://github.com/stablyai/orca/pull/42650) e
[`stablyai/orca#42647`](https://github.com/stablyai/orca/pull/42647).

## O problema

1. **Devin limitado a terminais sem interface de chat estruturada (`#42598`, resolve `#30791`):**
   Usuários do Devin estavam restritos a terminais PTY puros, sem suporte à interface estruturada de Native Chat com seletor de modelos, inspeção de subagentes no roster, adoção de sessões iniciadas no terminal nem geração one-shot de títulos via `devin --print`.
2. **Impossibilidade de responder pontualmente a mensagens específicas no histórico do chat (`#42650`):**
   Em conversas longas ou com múltiplos tópicos, não havia recurso para citar diretamente uma mensagem prévia do agente ou do usuário; orientações de correção ou follow-ups ficavam ambíguos no fluxo geral da conversa.
3. **Falta de atalhos diretos para abrir arquivos HTML e Markdown modificados a partir de resumos de turnos (`#42647`):**
   Quando o agente gerava ou modificava páginas HTML ou documentações Markdown, o usuário precisava navegar manualmente pela árvore de arquivos para inspecioná-los em vez de abri-los diretamente a partir de cartões de resumo do chat ou dos diffs do controle de versão.

## O que o upstream implementa

- **Execução nativa do Devin via ACP com adoção de sessões (`#42598`, resolve `#30791`):**
  - Implementa o Devin como agente nativo de chat estruturado sobre ACP (`devin acp`);
  - Suporta adoção e migração *in-place* de sessões de terminal pré-existentes para Native Chat com replay integral do histórico sem decodificador externo;
  - Captura `cognition.ai/userMessageId` e `clientMessageId`, oferecendo tolerância a notificações customizadas de extensão;
  - Mapeia chamadas `run_subagent` no roster de agentes e registra `devin --print` para geração de texto *one-shot* e geração automática de títulos de chat.
- **Resposta direta com citação a mensagens específicas (*Reply to message*) (`#42650`):**
  - Adiciona o botão e atalho de ação rápida "Reply" nas mensagens do chat;
  - Exibe a faixa visual "Replying to …" acima da caixa de mensagem, citando até 500 caracteres da mensagem alvo;
  - Permite saltar na rolagem para a mensagem original com um clique na faixa de citação e oferece botão dedicado de rewind quando desejado.
- **Abertura direta de arquivos HTML e Markdown alterados (`#42647`):**
  - Cartões de resumo de turno e visualizadores de diffs do Source Control ganham botões para abrir arquivos HTML diretamente no navegador integrado do Orca (com atualização automática em reaberturas explícitas);
  - Arquivos Markdown ganham abertura direta com visualização formatada lado a lado ou no editor nativo.

## O que fazer

- Integrar o agente Devin via ACP no Native Chat com adoção de sessões de terminal e suporte a `devin --print` (`#42598`).
- Implementar a funcionalidade de resposta citada direta (*Reply to message*) com faixa "Replying to …" e salto de rolagem (`#42650`).
- Adicionar atalhos diretos para visualização de arquivos HTML e Markdown gerados ou modificados a partir dos turnos do chat (`#42647`).
