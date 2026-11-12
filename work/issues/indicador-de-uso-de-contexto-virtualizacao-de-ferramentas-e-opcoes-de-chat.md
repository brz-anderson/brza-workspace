---
status: open
description: Os PRs #41546, #41552, #41544 e #41491 trazem indicador de contexto no chat, virtualização de saídas de ferramentas, opções por conversa e retenção de OMP em idle.
scope:
  - brza-studio
  - brza-workflow
priority: high
opened: 2026-11-12
tags:
  - chat
  - tooling
---

# Indicador de uso de contexto, virtualização de ferramentas e opções de chat

Rastreado dos PRs abertos no upstream [`stablyai/orca#41546`](https://github.com/stablyai/orca/pull/41546) (atendendo às Issues [`#29995`](https://github.com/stablyai/orca/issues/29995) e [`#41119`](https://github.com/stablyai/orca/issues/41119)),
[`stablyai/orca#41552`](https://github.com/stablyai/orca/pull/41552),
[`stablyai/orca#41544`](https://github.com/stablyai/orca/pull/41544) (STA-14534 e STA-14532) e
[`stablyai/orca#41491`](https://github.com/stablyai/orca/pull/41491) (tickets 5122 e 5141).

## O problema

1. **Ausência de visibilidade contínua do consumo de contexto no chat nativo (`#41546`, `#29995`, `#41119`):**
   - Usuários e agentes operando em sessões longas não dispunham de um indicador visual permanente da ocupação da janela de contexto (ex.: 600k / 1M tokens), dependendo apenas de inspeções manuais esporádicas;
   - Sem essa leitura, compactações de histórico ou descartes de contexto aconteciam sem aviso prévio perceptível, prejudicando o planejamento de turnos de alta complexidade.
2. **Lentidão e congelamento da UI ao expandir execuções de ferramentas com saídas extensas (`#41552`):**
   - No Native Chat, abrir uma ferramenta (`tool run`) que gerou centenas ou milhares de linhas (ex.: saídas de compilação, testes unitários ou dumps) renderizava todos os elementos DOM simultaneamente;
   - Essa carga excessiva no renderer causava travamentos graves na interface, lentidão na rolagem e atrasos na resposta da aplicação.
3. **Disparo acidental de rascunhos no terminal ao trocar opções de modelo no chat (`#41544`):**
   - Em sessões de chat associadas a terminais de agentes, uma alteração de modelo ou esforço na interface podia submeter inadvertidamente um rascunho de comando já digitado no prompt do terminal;
   - Além disso, fechar a visualização descartava seleções de opções mantidas localmente, e respostas tardias de configuração podiam atualizar uma conversa diferente da que originou o pedido.
4. **Encerramento prematuro de tarefas de segundo plano do OMP na limpeza de ociosidade (`#41491`):**
   - A rotina de varredura periódica de ociosidade do chat nativo encerrava processos de agentes após o limite configurado (ex.: 15 minutos), sem validar adequadamente se processos filhos do OMP ainda possuíam tarefas nativas de background em execução;
   - Isso provocava cancelamento forçado de comandos assíncronos e perda irreparável de arquivos e relatórios produzidos por workers.

## O que o upstream propõe e implementa

1. **Medidor persistente de uso de contexto em desktop e mobile (`#41546`):**
   - Adiciona leitura visual persistente (com anel gráfico e detalhamento de tokens, ex.: 607.7k / 1M) na barra inferior do Native Chat;
   - Opera sobre mensagens retidas no transcript sem introduzir polling concorrente, separando accounting de thread principal versus sidechains e preservando conformidade entre plataformas.
2. **Virtualização da listagem de linhas de ferramentas abertas (`#41552`):**
   - Implementa janela virtualizada (`NativeChatToolRunMemberList` e `use-native-chat-tool-run-window`), renderizando apenas as linhas estritamente visíveis na área de visualização;
   - Suporta acompanhamento dinâmico durante emissões em lote, preserva a posição de rolagem do leitor mesmo com a busca aberta e reduz drasticamente o consumo de memória do DOM.
3. **Vinculação estrita de opções à conversa e proteção de rascunhos (`#41544`):**
   - Associa as seleções de opções e modelo diretamente à conversa destinatária, prevenindo que atualizações tardias afetem outros chats;
   - Intercepta comandos de troca de modelo quando há um rascunho pendente no terminal do agente, bloqueando o envio antes de qualquer escrita no fluxo do terminal e exibindo aviso na UI.
4. **Preservação de processos filhos de OMP com trabalho ativo em background (`#41491`):**
   - Refina o coletor de ociosidade (`acp-structured-idle-sweep`) para preservar o PID e tokens de processos OMP enquanto houver tarefas em background em andamento;
   - Assegura que saídas atrasadas de shells nativos sejam recuperadas com sucesso mesmo após intervalos longos de inatividade, encerrando os processos apenas no fechamento explícito da UI.

## O que fazer

- Adotar o indicador visual de consumo de contexto no Native Chat do `brza-studio` (`#41546`), oferecendo visibilidade direta para modelos de contexto amplo como Gemini 2.5 e Claude 5.5.
- Incorporar a virtualização de linhas em execuções de ferramentas abertas (`#41552`), eliminando gargalos de desempenho na exibição de logs e testes extensos.
- Integrar a proteção de rascunhos e isolamento de opções por conversa (`#41544`), evitando disparos indevidos em instâncias de terminal associadas ao chat.
- Garantir a retenção de processos OMP durante o ciclo de idle-sweep (`#41491`), resguardando comandos longos executados em segundo plano.
