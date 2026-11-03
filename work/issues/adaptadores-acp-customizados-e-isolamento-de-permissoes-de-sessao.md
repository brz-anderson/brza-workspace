---
status: open
description: O PR #37842 e os PRs #37895 e #37861 trazem adaptadores ACP customizados no host, isolamento de regras de sessão do Claude e reflexo visual de fallback de modelos no chat.
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

Rastreado do PR aberto no upstream [`stablyai/orca#37842`](https://github.com/stablyai/orca/pull/37842) e das issues e PRs
[`stablyai/orca#37895`](https://github.com/stablyai/orca/pull/37895) (Issue [`#37889`](https://github.com/stablyai/orca/issues/37889)),
[`stablyai/orca#37861`](https://github.com/stablyai/orca/pull/37861) (Issue [`#37859`](https://github.com/stablyai/orca/issues/37859)),
[`stablyai/orca#37862`](https://github.com/stablyai/orca/issues/37862) e
[`stablyai/orca#37883`](https://github.com/stablyai/orca/pull/37883).

## O problema

1. **Agentes ACP externos limitados a adaptadores hardcoded (`#37842`):** para rodar agentes baseados no Agent Client
   Protocol (ACP) com interface gráfica de Native Chat, o runtime aceitava apenas os dialetos pré-compilados no binário.
   Modelos internos, executáveis com flags de sandbox customizadas ou novos provedores locais não podiam ser declarados
   sem modificar o código-fonte do app.
2. **"Allow for this session" persistia permissões definitivas no disco (`#37895`, `#37889`):** no chat de Claude Code,
   ao aprovar uma ferramenta com "Allow for this session", o app repassava a sugestão com `destination: "localSettings"`,
   gravando permanentemente a regra em `<projeto>/.claude/settings.local.json`. Isso violava a expectativa de isolamento
   temporário, permitindo que sessões futuras executassem comandos sensíveis sem confirmação.
3. **Fallback silencioso de modelo (`#37861`, `#37859`):** quando o Claude realizava fallback automático de modelo (ex.:
   de Opus para Sonnet por indisponibilidade temporária), a resposta era renderizada como bloco de conteúdo desconhecido
   e o composer permanecia fixado no modelo antigo sem feedback ao usuário.
4. **Tarefas de background sem inspeção de saída ao vivo (`#37862`):** comandos disparados em background pelo agente
   (com `run_in_background` ou timeout) exibiam apenas uma linha de status estática no chat, sem atalho para acompanhar o
   log gerado em `/private/tmp/claude-*/.../tasks/<id>.output`.

## O que o upstream implementa e corrige

- **Adaptadores ACP customizados configuráveis no host (`#37842`):** permite declarar adaptadores arbitrários em
  `customAgentAdapters` nas configurações do host, definindo comando, argumentos, variáveis de ambiente e transporte
  (`stdio` ou `sse`). O runtime instancia Native Chats com journal normalizado, aprovação de permissões e pinning de
  diretório de conta.
- **Isolamento estrito de aprovações de sessão (`#37895`):** reescreve o destino de regras de "Allow for this session"
  para `"session"` no RPC de aprovação, mantendo as permissões apenas em memória e preservando limpos os arquivos locais.
- **Reflexo de fallback e visibilidade de turnos (`#37861`, `#37883`):** exibe alertas no chat e ajusta o seletor do
  composer quando há fallback de modelo, além de manter respostas a perguntas do usuário visíveis durante a entrega.

## O que fazer

Portar o suporte de adaptadores customizados ACP (`#37842`) para o `brza-studio`, incorporar o conserto de permissões
de sessão (`#37895`) e estender o `brza-workflow` para inspeção direta de tarefas assíncronas no chat.
