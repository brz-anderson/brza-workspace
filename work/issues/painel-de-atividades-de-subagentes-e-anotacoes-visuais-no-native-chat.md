---
status: open
description: Os PRs #38632, #38633, #38640, #38594 e #38627 trazem barra de subagentes e transcript viewer no chat nativo, anotações em imagens e otimização para chats longos.
scope:
  - brza-studio
  - brza-workflow
priority: high
opened: 2026-11-05
tags:
  - chat
  - tooling
---

# Painel de atividades de subagentes e anotações visuais no Native Chat

Rastreado dos PRs abertos no upstream [`stablyai/orca#38632`](https://github.com/stablyai/orca/pull/38632),
[`stablyai/orca#38633`](https://github.com/stablyai/orca/pull/38633),
[`stablyai/orca#38640`](https://github.com/stablyai/orca/pull/38640),
[`stablyai/orca#38470`](https://github.com/stablyai/orca/pull/38470),
[`stablyai/orca#38452`](https://github.com/stablyai/orca/pull/38452),
[`stablyai/orca#38594`](https://github.com/stablyai/orca/pull/38594) (Issue [`#38592`](https://github.com/stablyai/orca/issues/38592)),
[`stablyai/orca#38627`](https://github.com/stablyai/orca/pull/38627),
[`stablyai/orca#38649`](https://github.com/stablyai/orca/pull/38649) e
[`stablyai/orca#38625`](https://github.com/stablyai/orca/pull/38625) (Issue [`#38624`](https://github.com/stablyai/orca/issues/38624)).

## O problema

1. **Invisibilidade e falta de inspeção de subagentes no Native Chat (`#38632`, `#38633`, `#38470`):**
   Embora o agente coordenador no Native Chat pudesse instanciar subagentes em segundo plano para delegar tarefas auxiliares,
   o chat desktop e mobile não exibia um elenco estruturado (*roster*) dos subagentes em execução. O usuário não conseguia
   ver o estado do subagente, abrir seu transcript dedicado para inspecionar comandos ou descartar em lote processos concluídos/falhos.
2. **Falta de ferramentas de anotação posicional em imagens anexadas (`#38594`, `#38592`):**
   Ao debater interfaces, capturas de tela ou diagramas com o agente, o usuário não tinha uma forma direta de apontar
   regiões específicas da imagem. Era necessário descrever textualmente com imprecisão ou editar a imagem em aplicativos
   externos antes do upload.
3. **Degradação de performance em conversas longas sob streaming (`#38627`):**
   A cada atualização de status coalescida (a cada ~60 ms durante o streaming do modelo), o servidor reavaliava o status
   do chat reescaneando o histórico completo de dezenas de milhares de itens de diário. Em conversas com mais de 5.000 turnos,
   essa computação consumia 35–40 ms da janela de 60 ms na main thread, congelando a interface gráfica e enfileirando
   chamadas RPC e requisições remotas.
4. **Interrupção de chats ativos após atualizações ou reinício (`#38649`):**
   Por padrão, a opção "Resume working chats automatically after a restart" vinha desativada para novos usuários, deixando
   sessões em meio a tarefas longas travadas em diálogos de revisão manual em vez de prosseguirem autonomamente.
5. **Legibilidade visual de comandos e código inline (`#38625`, `#38624`):**
   Cores e estilos de código inline e ênfase em negrito nos balões de chat não podiam ser ajustados, dificultando a leitura
   sob certos temas escuros.

## O que o upstream implementa

- **Barra de atividade e visualizador de subagentes no Native Chat (`#38632`, `#38633`, `#38640`):**
  - Adiciona barra de atividade no desktop e folha expansível (*sheet*) no mobile listando todos os subagentes da conversa
    com estado vivo, pré-visualização e descarte em lote de filhos finalizados ou com erro;
  - Permite abrir a transcrição completa do subagente diretamente pela barra de agentes ou pelo cartão de spawn, mantendo
    o composer principal conectado ao agente líder;
  - Persiste descartes por sessão e conecta subagentes desvinculados ao histórico unificado.
- **Leitura estruturada de subagentes e tarefas a partir de transcripts (`#38470`, `#38452`):**
  - Implementa camada de dados que extrai dinamicamente subagentes e árvores de tarefas geradas por qualquer provedor
    ao longo de todo o histórico da conversa.
- **Anotações e comentários posicionais numerados em imagens (`#38594`):**
  - Permite clicar com o botão direito em imagens de chat ou previews e selecionar "Comment on image";
  - Abre editor visual onde o usuário posiciona marcadores numerados (pins com percentual de coordenadas), insere notas
    textuais vinculadas e gera a imagem com marcações renderizadas em PNG acoplada diretamente ao rascunho do composer.
- **Eliminação de rescaneamento desnecessário em chats longos (`#38627`):**
  - Substitui o reprocessamento global de itens de diário por índices incrementais em memória, reduzindo o tempo de CPU
    por atualização de 40 ms para menos de 1 ms em sessões extensas.
- **Retomada automática pós-reinício ativada por padrão (`#38649`):**
  - Define como padrão para novas instalações e perfis a retomada automática de agentes ativos após reinicializações.
- **Configuração de destaque para negrito e código inline (`#38625`):**
  - Expõe opções em preferências para customizar a tonalidade de texto em negrito e tags de código no chat.

## O que fazer

- Adotar a barra de atividades de subagentes (`#38632`, `#38633`) e a camada de extração de transcripts (`#38470`) no `brza-studio`.
- Incorporar o editor de anotações em imagens (`#38594`) para enriquecer o workflow multimodal com agentes.
- Portar as otimizações de performance para chats longos (`#38627`) no backend de chat do `brza-studio`.
