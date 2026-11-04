---
scope:
  - brza-studio
  - brza-workflow
opened: 2026-11-03
completed: 2026-11-03
refs:
  - issue:ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins
---

# Abertura dos planos de chats pela CLI

## O que foi feito

Feitas duas rodadas sobre o plano da issue [Ler e enviar mensagens a chats pela CLI e expor Native Chat aos plugins](../issues/ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins.md), registradas nela:
- **Planos:** um por workstream, no `studio` e no `tools-kit`.
- **Cobertura:** a issue inteira, em fases por prioridade.
- **Issues:** uma por frente, criada no workstream da frente.

Conferido no upstream: o `#37774` foi integrado em 2026-11-03, e falta no checkout local `8f41dd56a33`; o `#37802` e o `#37467` continuam abertos.

Pela norma de pedido de outro workstream, esta sessão não gravou os planos. Abriu duas sessões pelo `brza sessions`, com o pedido, as rodadas citadas e as slugs fixadas:
- **`studio-chats-cli`**, no `studio`: as cinco issues das frentes do `brza-studio` e o `PLN` `chats-pela-cli-e-plugins`.
- **`tools-kit-chats-cli`**, no `tools-kit`: a issue `brza-sessions-sobre-o-brza-chat` e o `PLN` dela, com `depends_on` no do `studio`.

Nenhum código foi alterado.

## Pendente

- Passar a issue de origem a `done`, com os links para as issues novas, quando elas estiverem commitadas em `workstream/studio` e `workstream/tools-kit`. O pendente está registrado na própria issue.
