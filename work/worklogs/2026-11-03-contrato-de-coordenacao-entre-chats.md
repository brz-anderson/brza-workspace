---
scope:
  - brza-studio
  - brza-workflow
opened: 2026-11-03
completed: 2026-11-03
refs:
  - issue:ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins
---

# Contrato de coordenação entre chats

## O que foi feito

Registrada na issue [Ler e enviar mensagens a chats pela CLI e expor Native Chat aos plugins](../issues/ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins.md) a resposta literal de Anderson escolhendo coordenação entre sessões como foco do detalhamento, sem início de implementação.

Conferidos os contratos de fila, submissão, replay e origem do coordenador no código local. A mutação separa recusa, fila e submissão; esta última pode estar `pending`, `accepted`, `rejected` ou `unknown`. Os testes existentes documentam replay sem novo disparo e preservação de `unknown` em retries.

Identificado que a CLI atual só encaminha a origem do coordenador para orquestração e launch, enquanto o wrapper também a informa em `agentSession.send`. Uma integração precisa preservar essa informação.

A proposta e as alternativas de acompanhamento e envio ficaram para rodada na conversa, com registro de pendência na issue. Somente notas foram alteradas; testes de produto não foram executados.
