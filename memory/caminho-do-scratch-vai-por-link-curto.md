---
name: caminho-do-scratch-vai-por-link-curto
description: Subagente erra o caminho do scratch do chat do BrzA Studio (hash longo); passe um link curto em /private/tmp
metadata:
  node_type: memory
  type: project
  originSessionId: 746b7a51-6fa4-47d9-95ef-35afb7fcc654
  modified: 2026-10-31T10:49:47.810Z
---

O scratch do chat do BrzA Studio fica em `~/Library/Application Support/brza-studio/chat-scratch/<hash de 32>`. Em
2026-10-31, o `collector` e uma execução de medição copiaram o caminho sem o `0` final do hash: um gravou numa pasta
nova com o nome errado, a outra parou achando que o clone não existia. Com um link curto
(`ln -sfn "<scratch>/<pasta>" /private/tmp/<nome>`), as dez execuções seguintes acertaram.

**Why:** o caminho tem espaço e um hash que o modelo transcreve mal; o erro não dá falha, dá arquivo no lugar errado.

**How to apply:** ao delegar trabalho que lê ou grava no scratch, crie o link curto e passe só ele no pedido. Vale para
todos os workstreams: é candidato à norma, no `CLAUDE.md`, junto da linha do scratch na tabela de vocabulário.
