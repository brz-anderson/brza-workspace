---
status: open
description: Os PRs #40935, #39649, #39606, #39276 e as issues #41008, #39619 tratam de imagens geradas no chat, badges de modelo/effort de subagentes e isolamento de status.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#40935`](https://github.com/stablyai/orca/pull/40935),
[`stablyai/orca#39649`](https://github.com/stablyai/orca/pull/39649) (resolve Issue [`#39619`](https://github.com/stablyai/orca/issues/39619)),
[`stablyai/orca#39606`](https://github.com/stablyai/orca/pull/39606) (resolve Issue [`#37379`](https://github.com/stablyai/orca/issues/37379)),
[`stablyai/orca#39276`](https://github.com/stablyai/orca/pull/39276) (Issue [`#39275`](https://github.com/stablyai/orca/issues/39275)),
[`stablyai/orca#39082`](https://github.com/stablyai/orca/pull/39082) (Issue [`#39074`](https://github.com/stablyai/orca/issues/39074)),
[`stablyai/orca#39079`](https://github.com/stablyai/orca/pull/39079) (Issue [`#39073`](https://github.com/stablyai/orca/issues/39073)),
além das issues [`stablyai/orca#41008`](https://github.com/stablyai/orca/issues/41008) e
[`stablyai/orca#39619`](https://github.com/stablyai/orca/issues/39619),
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
8. **Subagentes do OpenCode 2.x não renderizados no Chat UI (`#39276`, `#39275`):**
   Quando um agente OpenCode delegava tarefas a subagentes auxiliares (`subagent` no 2.x ou `task` no 1.x), as ações do filho
   apareciam como ferramentas genéricas na conversa principal, sem identificação do subagente, sem cartão dedicado de estado
   (running/done/stopped) e sem presença na faixa de agentes ativos acima do composer.
9. **Sessões irmãs do OpenCode em serviço compartilhado tratadas como subagentes (`#39619`):**
   Ao conectar múltiplos terminais ao mesmo serviço `opencode serve --service`, o hook do OpenCode considerava qualquer sessão ativa
   no fluxo de eventos como subagente da pane observada. Isso fazia com que abas ociosas exibissem o spinner `working` continuamente
   enquanto uma sessão irmã trabalhava.
10. **Poluição de títulos de abas do Claude Code com texto de aviso após `/clear` (`#39606`, resolve `#37379`):**
    Após rodar `/clear`, o título da aba no Orca assumia o texto bruto `<local-command-caveat>The command below was run directly in Claude Code...`
    em vez de preservar o título ao vivo (`✳ Claude Code`), permanecendo ilegível até o envio do próximo prompt real.
11. **Sobrescrita, duplicação e desaparecimento de imagens geradas no Native Chat (`#40935`):**
    Quando agentes geravam imagens (artboards, mockups ou diagramas), a entrega do artefato sobrescrevia o texto em prosa da
    resposta final quando chegava com atraso, aparecia duplicada caso a resposta já a incorporasse, ou desaparecia completamente
    ao navegar de volta pelo histórico de sessões anteriores.
12. **Invisibilidade do modelo e nível de esforço de subagentes no painel de agentes (`#41008`):**
    No painel de agentes da sessão do Claude ("1 agent — working", com nome, ferramenta ativa, tokens e tempo), não havia exibição
    do modelo e esforço de raciocínio de cada subagente. Quando agentes customizados ou chamadas dinâmicas utilizavam modelos
    discrepantes do pai (ex.: subagente executando em Opus no esforço high em sessão pai Sonnet), o operador ficava no escuro sobre
    os parâmetros de execução e custos correspondentes.

## O que o upstream implementa

- **Renderização e ciclo de vida de subagentes OpenCode no Chat UI (`#39276`):**
  - Implementa o gancho de dialeto ACP `childSession` para capturar frames filhos marcados com `_meta["opencode/child-session"]`,
    vinculando o ID do agente filho à linha do tempo da conversa;
  - Cria um cartão dedicado com o nome da tarefa delegada, exibe o status ao vivo na faixa de agentes acima do composer e
    alinha as ferramentas e comandos do filho sob o seu próprio cartão.
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
- **Supressão de textos de harness do Claude nos títulos de abas (`#39606`, resolve `#37379`):**
  - Impede que marcações de meta/harness (como `<local-command-caveat>`) sejam promovidas a título de sessão de fallback,
    preservando o título ao vivo (`✳ Claude Code`) após execuções de `/clear`.
- **Prevenção de falso status 'working' por OSC 7501 do OpenCode (`#39649`, resolve `#39619`):**
  - Filtra as sequências de escape OSC 7501 emitidas pelo OpenCode em instâncias compartilhadas (`opencode serve --service`),
    impedindo que o broadcast de status marque abas ociosas como em execução e garantindo que apenas a aba dona do comando
    exiba o status `working`.
- **Preservação de imagens geradas integradas à resposta final (`#40935`):**
  - Mantém imagens concluídas acopladas ao cartão da resposta final do assistente no desktop e cliente móvel, mesmo quando o
    artefato chega após o início do streaming de prosa;
  - Desduplica artefatos já referenciados no corpo Markdown e assegura que a projeção de histórico do SQLite retenha as
    imagens e seus controles intactos ao revisitar a sessão.
- **Exibição de modelo e nível de esforço de subagentes no painel (`#41008`):**
  - Propõe exibir badge compacto (ex.: `Opus · high`) ao lado da contagem de tokens na linha de cada subagente ativo no
    painel de agentes, extraindo a informação de `.claude/projects/.../subagents/agent-<id>.meta.json` e dos cabeçalhos de mensagens.

## O que fazer

- Integrar imagens geradas ao cartão da resposta final no chat nativo (`#40935`), evitando perdas e duplicações.
- Adotar badges de identificação de modelo e esforço de raciocínio de subagentes no painel de agentes (`#41008`).
- Adotar a supressão de textos de harness em títulos de abas do Claude (`#39606`).
- Isolar sessões irmãs do OpenCode no mesmo serviço (`#39649`, `#39619`), contendo sequências OSC 7501 e computando `working` apenas para a sessão ativa e seus filhos reais.
- Adotar a pré-visualização read-only de chats no Agent Dashboard (`#39082`) e o filtro de notificações de perguntas (`#39079`).
- Adotar o suporte nativo a subagentes OpenCode no Chat UI (`#39276`).
- Adotar o agrupamento visual de subagentes na sidebar (`#38995`) e a ação de backgrounding de ferramentas (`#38963`) no `brza-studio`.
- Portar o isolamento em threads de workers para o SQLite de histórico (`#38945`) e o rastreamento de processos órfãos (`#39013`).
