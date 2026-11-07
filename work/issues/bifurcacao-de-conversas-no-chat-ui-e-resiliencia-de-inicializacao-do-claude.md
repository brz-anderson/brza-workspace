---
status: open
description: Os PRs #38326, #39168, #38381 e os PRs #38388, #38352 e #38335 trazem bifurcação fiel de chats, resiliência de startup do Claude CLI e melhorias de navegação e teclado.
scope:
  - brza-studio
  - brza-workflow
priority: high
opened: 2026-11-05
tags:
  - chat
  - tooling
---

# Bifurcação de conversas no Chat UI e resiliência de inicialização do Claude

Rastreado dos PRs abertos no upstream [`stablyai/orca#38326`](https://github.com/stablyai/orca/pull/38326),
[`stablyai/orca#39168`](https://github.com/stablyai/orca/pull/39168),
[`stablyai/orca#38381`](https://github.com/stablyai/orca/pull/38381) (Issue [`#38369`](https://github.com/stablyai/orca/issues/38369)),
[`stablyai/orca#38388`](https://github.com/stablyai/orca/pull/38388) (Issue [`#38385`](https://github.com/stablyai/orca/issues/38385)),
[`stablyai/orca#38352`](https://github.com/stablyai/orca/pull/38352),
[`stablyai/orca#38335`](https://github.com/stablyai/orca/pull/38335) (Issue [`#38333`](https://github.com/stablyai/orca/issues/38333)),
[`stablyai/orca#38389`](https://github.com/stablyai/orca/pull/38389) e da issue
[`stablyai/orca#38355`](https://github.com/stablyai/orca/issues/38355).

## O problema

1. **Inexistência de bifurcação nativa de conversas dentro do Chat UI (`#38326`):**
   Usuários que quisessem testar abordagens alternativas a partir de uma resposta anterior do agente precisavam sair do
   Chat UI (indo para terminal) ou criar um agente totalmente do zero em um novo worktree colando o texto anterior. Não
   havia como ramificar a conversa no próprio Chat UI mantendo intacto o histórico nativo da sessão até aquele turno.
2. **Falha de timeout na inicialização de agentes no Native Chat (`#38381`, `#38369`):**
   O runtime do Chat Nativo estipulava um limite rígido de 60 segundos (`CLAUDE_INITIALIZE_TIMEOUT_MS = 60_000`) para a
   resposta do handshake de inicialização do Claude CLI. Em projetos com múltiplos servidores MCP, plugins de workspace
   (ex.: `orca-typescript` iniciando `tsc --lsp`) ou ganchos `SessionStart`, a carga ultrapassava 60s (frequentemente 70–80s
   sob contenção de CPU), abortando a abertura da aba com erro `agentSession.provider-open-failed`, enquanto o terminal
   aberto na mesma máquina funcionava sem problemas.
3. **Atalho Cmd+R inerte em abas de chat (`#38388`, `#38385`):**
   O atalho universal Cmd+R ("Rename active tab") não acionava a renomeação da aba quando o foco estava no composer do
   chat nativo, obrigando o uso de cliques no mouse.
4. **Falta de comando rápido para inspeção de limites no Codex (`#38352`):**
   Usuários do Codex em sessões de Native Chat não dispunham de um cartão visual integrado de consumo de cota e tokens ao
   digitar `/usage`.
5. **Navegação rígida por mouse em cartões de múltiplas perguntas (`#38335`, `#38333`):**
   Quando o modelo retornava cartões com múltiplas perguntas ou confirmações sequenciais, o usuário não conseguia alternar
   entre as perguntas usando as setas do teclado (Left/Right).
6. **Inconsistência entre esforço exibido e consumido (`#38355`):**
   O Native Chat exibia no cabeçalho um valor padrão de `effortLevel` descolado do nível de esforço de raciocínio real
   utilizado pelo motor do Claude na requisição.
7. **Perda de formatação e replay indevido de turnos ao bifurcar conversa (`#39168`):**
   Ao acionar a bifurcação de conversa ("Fork"), a implementação inicial tentava reconstruir as mensagens no novo chat a
   partir do histórico semântico do agente em vez de duplicar a transcrição nativa da UI. Isso resultava na perda de formatação
   rica, eliminação de timestamps originais e reexecução espúria de turnos de terminal ou ferramentas herdadas devido à falta
   de recibos imutáveis de identidade nativa.

## O que o upstream implementa

- **Ação "Fork from this response" no Chat UI (`#38326`):**
  - Adiciona botão com ícone de ramificação ao lado de respostas concluídas no Chat UI do desktop e nas ações de mensagem no app mobile;
  - Cria uma nova aba de chat no mesmo worktree e configurações (modelo, permissões), preservando o histórico completo
    e ferramentas até o fim daquele turno através de cópia nativa de transcript do Claude (em worker thread) ou thread do Codex;
  - Insere um divisor visual "Forked from <origem>" vinculando diretamente ao chat original, sem interromper nem modificar a sessão original.
- **Cópia fiel da transcrição nativa e preservação de identidades ao bifurcar (`#39168`):**
  - Refatora o mecanismo de fork para duplicar diretamente o registro serializado da conversa da UI do Orca/Studio;
  - Preserva integralmente o histórico visual, metadados de execução, timestamps e recibos imutáveis de identidades nativas herdadas,
    garantindo que o agente bifurcado não reexecute turnos concluídos e mantenha fidelidade visual exata.
- **Elevação do timeout de inicialização do Claude para 3 minutos (`#38381`):**
  - Ajusta `CLAUDE_INITIALIZE_TIMEOUT_MS` de 60s para 180s (180.000 ms), permitindo inicializações seguras de projetos
    com servidores MCP pesados e LSP associados sem falhas falsas de handshake.
- **Atalho Cmd+R a partir do Chat Composer (`#38388`):**
  - Integra o handler de renomeação de aba ao editor de texto do composer de chat.
- **Cartão `/usage` para Codex no Native Chat (`#38352`):**
  - Renderiza o cartão rico de consumo e limites de tokens ao invocar o comando de barra `/usage` em chats Codex.
- **Navegação com setas em cartões de perguntas (`#38335`):**
  - Habilita suporte a teclado (Left/Right) para percorrer perguntas sequenciais em cards interativos do chat.

## O que fazer

- Adotar o recurso de fork de mensagens (`#38326`) no `brza-studio` e `brza-workflow`.
- Adotar a replicação fiel de transcrições nativas e recibos de identidade na bifurcação de chats (`#39168`).
- Incorporar o aumento de timeout de inicialização do Claude CLI para 180s (`#38381`) para estabilizar o carregamento de
  projetos com MCP servers no `brza-studio`.
- Adotar as melhorias de teclado e comandos (`#38388`, `#38352`, `#38335`) nas interfaces de chat nativo.
