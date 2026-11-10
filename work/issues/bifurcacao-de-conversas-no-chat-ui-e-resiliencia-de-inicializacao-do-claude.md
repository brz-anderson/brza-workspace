---
status: open
description: Os PRs #40705, #40548, #40558, #39823, #38326, #39168, #38001 e #38381 trazem fork para novo worktree, identidade nativa, persistência de contas e resiliência de startup.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#40705`](https://github.com/stablyai/orca/pull/40705) (resolve Issue [`#40704`](https://github.com/stablyai/orca/issues/40704)),
[`stablyai/orca#40548`](https://github.com/stablyai/orca/pull/40548),
[`stablyai/orca#40558`](https://github.com/stablyai/orca/pull/40558),
[`stablyai/orca#39823`](https://github.com/stablyai/orca/pull/39823) (atendendo à Issue [`#38326`](https://github.com/stablyai/orca/issues/38326)),
[`stablyai/orca#38001`](https://github.com/stablyai/orca/pull/38001) (resolve Issue [`#37707`](https://github.com/stablyai/orca/issues/37707)),
[`stablyai/orca#38326`](https://github.com/stablyai/orca/pull/38326),
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
8. **Vazamento e colisão de identidade em subprocessos do Claude (`#40548`):**
   Ao gerar títulos em segundo plano ou executar comandos auxiliares do Claude, o runtime mesclava a identidade do chat
   interativo nativo com as credenciais do processo cliente, provocando substituições indevidas de conta e inconsistência de sessão.
9. **Perda de estado de contas Claude durante atualização em segundo plano (`#40558`):**
   Durante ciclos de renovação de credenciais ou refresh em background, o estado de runtime e as tabelas de mapeamento de
   sessões das contas ativas do Claude eram sobrescritos ou descartados, desestabilizando conversas em andamento.
10. **Aba inoperante ao retomar conversa de CLI com transcript inexistente (`#38001`, resolve `#37707`):**
   Ao tentar retomar uma sessão de histórico do Claude CLI cuja transcrição em disco estivesse corrompida, vazia ou ausente,
   a interface do Native Chat congelava aguardando mensagens inexistentes, criando uma aba morta sem recuperação automática.
11. **Impossibilidade de bifurcar chats para novos worktrees isolados com histórico completo (`#40705`, resolve `#40704`):**
   A ação "Fork from this response" só permitia criar uma cópia em uma nova aba dentro do mesmo worktree. Ao desejar testar
   uma abordagem arriscada, refatoração paralela ou investigação paralela sem sobrescrever arquivos locais, o desenvolvedor
   tinha que abrir manualmente um terminal, criar outro worktree e colar um resumo limitado, perdendo a conversa original do agente.

## O que o upstream implementa

- **Bifurcação de chat diretamente para novo worktree com histórico nativo (`#40705`, resolve `#40704`):**
  - Adiciona menu no botão de Fork com opções: "In a new tab", "Into a new worktree…" e "As a background subagent…";
  - Permite escolher a base do novo branch (Main branch ou This branch), cria o worktree e solicita cópia nativa da conversa para o novo diretório (`destinationCwd`):
    - Claude: grava a cópia no bucket de projeto da nova pasta;
    - Codex e agentes ACP: bifurcam a sessão apontando o novo folder como `cwd`;
  - "As a background subagent…" inicializa o agente em segundo plano no novo worktree com a tarefa informada e endereço de reporte automático via `orca orchestration send`;
  - Organiza os novos worktrees de fork aninhados visualmente sob o worktree pai na barra lateral e exibe link "Forked from" funcional.
- **Identidade nativa estrita e delimitação de lançamento para o Claude (`#40548`):**
  - Restringe a identidade de chat do Claude estritamente ao ambiente nativo interativo do Studio/Orca;
  - Isola a geração de títulos e execuções em segundo plano sob identidades separadas de cliente e impõe limites rígidos
    de lançamento no SDK para evitar vazamento em overrides de conta.
- **Preservação de estado de runtime por conta Claude no refresh (`#40558`):**
  - Mantém o estado de execução e os mapas de sessão individuais de cada conta Claude durante ciclos de atualização em background,
    prevenindo desconexões e perda de contexto de autenticação.
- **Inicialização limpa ao retomar conversas sem transcript salvo (`#38001`, resolve `#37707`):**
  - Identifica proativamente quando uma conversa de CLI a ser retomada não possui arquivo de transcrição válido no disco;
  - Inicializa imediatamente uma sessão limpa e funcional notificando o desenvolvedor, eliminando abas travadas.
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
- **Bifurcação de respostas copiadas a partir do chat original (`#39823`, atendendo `#38326`):**
  - Respostas copiadas acima do divisor de um fork pertencem ao chat original; a ação "Fork from this response" sobre essas mensagens
    resolve e bifurca a partir da conversa original raiz (inclusive recursivamente através de bifurcações de bifurcações);
  - Oculta o botão "Rewind" nas respostas copiadas acima do divisor no desktop e mobile, e garante que o rewinding no primeiro prompt
    abaixo do divisor retorne exatamente ao ponto de bifurcação;
  - Se a conversa original tiver sido deletada ou não contiver mais a resposta, a solicitação é recusada antes de criar abas órfãs.
- **Atalho Cmd+R a partir do Chat Composer (`#38388`):**
  - Integra o handler de renomeação de aba ao editor de texto do composer de chat.
- **Cartão `/usage` para Codex no Native Chat (`#38352`):**
  - Renderiza o cartão rico de consumo e limites de tokens ao invocar o comando de barra `/usage` em chats Codex.
- **Navegação com setas em cartões de perguntas (`#38335`):**
  - Habilita suporte a teclado (Left/Right) para percorrer perguntas sequenciais em cards interativos do chat.

## O que fazer

- Adotar o fork de conversas diretamente para novos worktrees e subagentes em segundo plano com reporte via orquestração (`#40705`).
- Adotar a contenção de identidade nativa e fronteira de lançamento do Claude (`#40548`).
- Incorporar a preservação de estado de runtime por conta no refresh do Claude (`#40558`).
- Implementar o fallback seguro para nova sessão ao retomar conversas sem transcript salvo (`#38001`).
- Adotar o recurso de fork de mensagens (`#38326`) e a resolução de forks a partir do chat original raiz (`#39823`) no `brza-studio`.
- Adotar a replicação fiel de transcrições nativas e recibos de identidade na bifurcação de chats (`#39168`).
- Incorporar o aumento de timeout de inicialização do Claude CLI para 180s (`#38381`) para estabilizar o carregamento de
  projetos com MCP servers no `brza-studio`.
- Adotar as melhorias de teclado e comandos (`#38388`, `#38352`, `#38335`) nas interfaces de chat nativo.
