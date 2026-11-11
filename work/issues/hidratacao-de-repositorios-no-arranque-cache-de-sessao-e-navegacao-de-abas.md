---
status: open
description: Os PRs #41088, #41091, #41068 e as issues #41107, #41115 trazem aceleração de arranque em grandes workspaces, cache persistente de histórico e navegação de abas.
scope:
  - brza-studio
  - workspace
  - brza-workflow
priority: high
opened: 2026-11-11
tags:
  - tooling
  - infra
---

# Hidratação de repositórios no arranque, cache de sessão e navegação de abas

Rastreado dos PRs abertos no upstream [`stablyai/orca#41088`](https://github.com/stablyai/orca/pull/41088) (atendendo à STA-14831),
[`stablyai/orca#41091`](https://github.com/stablyai/orca/pull/41091),
[`stablyai/orca#41068`](https://github.com/stablyai/orca/pull/41068) (resolve Issue [`#41062`](https://github.com/stablyai/orca/issues/41062)),
além das issues [`stablyai/orca#41107`](https://github.com/stablyai/orca/issues/41107) e
[`stablyai/orca#41115`](https://github.com/stablyai/orca/issues/41115).

## O problema

1. **Saturação do processo principal e timeouts de CLI em workspaces volumosos (`#41088`, STA-14831):**
   Ao inicializar o aplicativo com muitas pastas ou workspaces (ex.: 1.000 workspaces), o processo principal passava
   minutos saturado com uso de CPU contínuo, fazendo com que requisições da CLI sofressem timeout (>30s). A rotina de
   salvamento de ordenação inteligente (Smart-order) reconstruía isoladamente todos os objetos de repositório para
   cada workspace ordenado, acumulando mais de 166 segundos de trabalho síncrono.
2. **Re-leitura massiva de transcripts no Session History em atualizações ou troca de build (`#41091`):**
   O histórico de sessões mantinha um único banco de dados de cache (`session-parse-cache.sqlite`). Qualquer atualização
   que alterasse a versão do formato ou qualquer alternância entre builds em worktrees distintos apagava o arquivo
   inteiro, forçando o escaneamento e re-leitura completa de milhares de transcripts de sessões do disco (mais de 29.000
   arquivos no relato), gerando travamentos e exibição desnecessária da barra de progresso em varreduras que poderiam
   ser atendidas pelo cache.
3. **Impossibilidade de retornar ao workspace a partir do menu de contexto da aba (`#41068`, resolve `#41062`):**
   Ao abrir chats ou terminais a partir da barra de Atividades ou de listas globais, a aba permanecia desvinculada
   visualmente de seu contexto de origem. O menu de contexto da aba oferecia apenas ações de fechamento e divisão, sem
   uma opção direta para navegar até o workspace proprietário e revelá-lo na barra lateral.
4. **Descarte silencioso de prompt no método de plugins `agent.launch` (`#41107`):**
   Quando uma extensão ou automação invocava a API de plugins `agent.launch({ agent, prompt, ... })`, a sessão do agente
   era instanciada no workspace, porém o parâmetro textual `prompt` era descartado na inicialização, deixando o chat
   parado no estado ocioso sem executar a instrução fornecida.
5. **Nomeação incorreta de sessões retomadas na lista de agentes (`#41115`):**
   Ao resumir uma conversa ou sessão de agente preexistente em uma nova aba, a listagem de agentes atribuía à sessão o
   título do primeiro prompt submetido naquela aba específica, em vez de herdar e respeitar o nome original persistido
   da sessão retomada.

## O que o upstream implementa

- **Indexação por fase única e reutilização de registros de repositórios (`#41088`):**
  - Lê os registros de repositórios uma única vez por fase síncrona e reutiliza o índice existente para checagens de
    propriedade, listagem de catálogos e visibilidade;
  - Reduz o tempo de CPU do processo principal nos primeiros 5 minutos em 89,9% (de 177,5s para 18,0s);
  - Reduz o tempo de listagem de repositórios via CLI de mais de 30s (timeout) para apenas 140ms em frotas de 1.000 pastas.
- **Cache particionado por versão e supressão de barra de progresso silenciosa (`#41091`):**
  - Isola cada versão de formato de cache em seu próprio arquivo (`session-parse-cache.vN.sqlite`), permitindo coexistência
    entre versões de build e atualizações sem destruição do cache anterior;
  - Mantém a versão atual e a mais recente no disco, limpando apenas versões abandonadas;
  - Substitui contagem genérica de arquivos por medição de bytes lidos do disco, mantendo o indicador de progresso
    silencioso até que leituras frias reais excedam 64 MB.
- **Navegação "Go to Workspace" no menu de abas (`#41068`):**
  - Adiciona o item "Go to Workspace" ao menu de contexto de abas de chat e terminal, reaproveitando a navegação,
    rótulo e ícone da barra de Atividades para focar o workspace proprietário e filtrar a barra lateral.
- **Preservação de prompt em `agent.launch` e identidade de sessões retomadas (`#41107`, `#41115`):**
  - Propõe repassar corretamente o argumento `prompt` ao runtime do agente no despacho por plugins e carregar o título
    original da sessão no painel de agentes ao invocar resumes.

## O que fazer

1. Incorporar a otimização de leitura única de repositórios por fase síncrona (`#41088`) no `brza-studio`.
2. Adotar a estratégia de banco de dados versionado para o Session History (`#41091`), evitando re-leituras massivas de transcripts.
3. Adicionar o comando "Go to Workspace" no menu de contexto das abas de chat e terminal (`#41068`).
4. Corrigir o repasse do campo `prompt` no lançamento de agentes por plugins (`#41107`) e preservar o nome original de sessões retomadas (`#41115`).
