---
status: open
description: Os PRs #39082, #39079, #38995, #38963, #38945 e #39013 trazem preview de chats no Dashboard, notificações só para perguntas, subagentes na sidebar e SQLite em workers.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#39082`](https://github.com/stablyai/orca/pull/39082) (Issue [`#39074`](https://github.com/stablyai/orca/issues/39074)),
[`stablyai/orca#39079`](https://github.com/stablyai/orca/pull/39079) (Issue [`#39073`](https://github.com/stablyai/orca/issues/39073)),
[`stablyai/orca#38995`](https://github.com/stablyai/orca/pull/38995) (Issue [`#38994`](https://github.com/stablyai/orca/issues/38994)),
[`stablyai/orca#38963`](https://github.com/stablyai/orca/pull/38963),
[`stablyai/orca#38945`](https://github.com/stablyai/orca/pull/38945),
[`stablyai/orca#39013`](https://github.com/stablyai/orca/pull/39013) (Issue [`#39010`](https://github.com/stablyai/orca/issues/39010)),
[`stablyai/orca#38632`](https://github.com/stablyai/orca/pull/38632),
[`stablyai/orca#38633`](https://github.com/stablyai/orca/pull/38633),
[`stablyai/orca#38640`](https://github.com/stablyai/orca/pull/38640),
[`stablyai/orca#38470`](https://github.com/stablyai/orca/pull/38470),
[`stablyai/orca#38452`](https://github.com/stablyai/orca/pull/38452),
[`stablyai/orca#38594`](https://github.com/stablyai/orca/pull/38594) (Issue [`#38592`](https://github.com/stablyai/orca/issues/38592)),
[`stablyai/orca#38627`](https://github.com/stablyai/orca/pull/38627),
[`stablyai/orca#38649`](https://github.com/stablyai/orca/pull/38649) e
[`stablyai/orca#38625`](https://github.com/stablyai/orca/pull/38625) (Issue [`#38624`](https://github.com/stablyai/orca/issues/38624)).

## O problema

1. **Incapacidade de visualizar transcrições de chats estruturados no Agent Dashboard (`#39082`, `#39074`):**
   No painel Agent Dashboard, cartões de sessões de chat estruturado não possuíam PTY associado, exibindo apenas uma mensagem
   estática de que nenhuma pré-visualização estava disponível. O usuário precisava abrir o worktree e carregar a aba para
   ler o histórico ou acompanhar o progresso.
2. **Excesso de notificações intrusivas e falta de filtro por perguntas de agentes (`#39079`, `#39073`):**
   O canal de notificações do sistema tratava qualquer evento ("Agent Needs Input", conclusões de tarefas e campainhas de
   terminal) de forma idêntica. Desenvolvedores que desejavam ser avisados apenas quando o agente realmente precisava de
   uma resposta ou esclarecimento eram inundados por alertas repetitivos de aprovações rotineiras de ferramentas.
3. **Sessões flutuantes e de subagentes dispersas na barra lateral (`#38995`, `#38994`):**
   Subagentes e sessões ad-hoc abertas fora da hierarquia primária de worktrees misturavam-se de forma plana na lista de
   workspaces da barra lateral, sem indicação visual compacta do número de subagentes trabalhando em tempo real.
4. **Travamento do chat aguardando ferramentas ou comandos Bash longos do Claude (`#38963`):**
   Comandos demorados ou subagentes executados via Claude Bash bloqueavam a continuidade do chat até o término da invocação,
   sem opção para despachar o comando em segundo plano e permitir que o operador ou o agente seguissem a conversa.
5. **Travamentos e congelamentos em históricos massivos de sessões (`#38945`):**
   O indexador e motor de busca do Agent Session History executava transações SQLite síncronas pesadas na mesma thread do
   Node/servidor, travando a UI por minutos em históricos com mais de 20.000 transcrições.
6. **Processos órfãos fora de terminais invisíveis no monitor de recursos (`#39013`, `#39010`):**
   O popover Resource Usage monitorava apenas a árvore direta de processos de terminais ativos, omitindo servidores de
   desenvolvimento desanexados iniciados pelo agente.
7. **Invisibilidade e falta de inspeção de subagentes no Native Chat (`#38632`, `#38633`, `#38470`):**
   Falta de elenco estruturado (*roster*) dos subagentes em execução no chat desktop e mobile.

## O que o upstream implementa

- **Pré-visualização read-only de chats no Agent Dashboard (`#39082`):**
  - Carrega a transcrição da conversa sob demanda em modo somente leitura reutilizando o protocolo de histórico e os
    componentes de renderização de mensagens, sem inicializar provedores pesados nem interferir nas observações de PR links.
- **Notificações opt-in exclusivamente para perguntas de agentes (`#39079`):**
  - Adiciona o controle "Questions Only" nas preferências de notificação do desktop e push móvel;
  - Discrimina perguntas reais de pedidos comuns de permissão de ferramentas, notificando o operador apenas quando sua
    resposta for indispensável para o agente avançar.
- **Agrupamento de subagentes na sidebar e badges de atividade ao vivo (`#38995`):**
  - Categoriza sessões flutuantes e subagentes filhos em agrupamentos colapsáveis na barra lateral de workspaces com badges ao vivo.
- **Ação "Background" para ferramentas e subagentes Claude (`#38963`):**
  - Adiciona o botão "Background" ao lado da ferramenta em execução no chat e na barra expandida de tarefas, liberando a conversa.
- **Worker threads dedicadas para o SQLite de Session History (`#38945`):**
  - Isola a gravação do banco em uma thread dedicada e leituras/buscas FTS em conexões WAL em threads de leitura separadas com timeout de 10s.
- **Contabilização de processos fora de terminais no Resource Usage (`#39013`):**
  - Lê as tags de ambiente `ORCA_WORKTREE_ID` e `ORCA_PANE_KEY` para rastrear processos desanexados, computando como `outsideTerminals`.
- **Barra de atividade e visualizador de subagentes no Native Chat (`#38632`, `#38633`, `#38640`):**
  - Barra de atividade no desktop e folha expansível (*sheet*) no mobile listando todos os subagentes da conversa com estado vivo.

## O que fazer

- Adotar a pré-visualização read-only de chats no Agent Dashboard (`#39082`) e o filtro de notificações de perguntas (`#39079`).
- Adotar o agrupamento visual de subagentes na sidebar (`#38995`) e a ação de backgrounding de ferramentas (`#38963`) no `brza-studio`.
- Portar o isolamento em threads de workers para o SQLite de histórico (`#38945`) e o rastreamento de processos órfãos (`#39013`).
