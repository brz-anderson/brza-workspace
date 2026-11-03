---
scope:
  - brza-studio
  - brza-workflow
opened: 2026-11-03
completed: 2026-11-03
refs:
  - issue:ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins
---

# Aprofundamento da CLI de chats e API de plugins

## O que foi feito

Aprofundada a issue [Ler e enviar mensagens a chats pela CLI e expor Native Chat aos plugins](../issues/ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins.md), confrontando upstream e código local.

Identificado o PR aberto #33115 e a cobertura existente de `brza sessions`. Registradas as lacunas de leitura, recibos, identidade de sessão nos plugins e compatibilidade de protocolo. O diagnóstico de invisibilidade integral dos chats foi corrigido para cobertura parcial no checkout atual.

Leituras de código e API, sem execução de testes de produto, alteração de código ou envio entre sessões. O recorte de implementação permanece pendente na issue.
