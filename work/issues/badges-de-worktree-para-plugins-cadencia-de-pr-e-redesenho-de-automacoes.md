---
status: open
description: Os PRs #41598, #41620, #41332, #41268, #41325 trazem configurações nativas de plugins, unificação de automações e corte de Git em CI.
scope:
  - brza-studio
  - workspace
  - brza-workflow
priority: high
opened: 2026-11-10
tags:
  - tooling
  - design
  - infra
---

# Badges de worktree para plugins, cadência de PR e redesenho de automações

Rastreado dos PRs abertos no upstream [`stablyai/orca#41598`](https://github.com/stablyai/orca/pull/41598) (resolve Issue [`#41369`](https://github.com/stablyai/orca/issues/41369)),
[`stablyai/orca#41620`](https://github.com/stablyai/orca/pull/41620),
[`stablyai/orca#41332`](https://github.com/stablyai/orca/pull/41332),
[`stablyai/orca#41268`](https://github.com/stablyai/orca/pull/41268) (resolve Issue [`#41269`](https://github.com/stablyai/orca/issues/41269)),
[`stablyai/orca#41325`](https://github.com/stablyai/orca/pull/41325),
[`stablyai/orca#40557`](https://github.com/stablyai/orca/pull/40557),
[`stablyai/orca#40541`](https://github.com/stablyai/orca/pull/40541) (atendendo STA-8667),
[`stablyai/orca#40507`](https://github.com/stablyai/orca/pull/40507),
[`stablyai/orca#40534`](https://github.com/stablyai/orca/pull/40534),
[`stablyai/orca#40539`](https://github.com/stablyai/orca/pull/40539) (resolve STA-2380) e
[`stablyai/orca#40540`](https://github.com/stablyai/orca/pull/40540) (resolve Issue [`#40510`](https://github.com/stablyai/orca/issues/40510)).

## O problema

1. **Incapacidade de plugins adicionarem badges contextuais e ações nos cartões de workspace (`#40557`):**
   Plugins de workspace não tinham como sinalizar visualmente nos cartões da barra lateral que determinado checkout
   contém um projeto específico (ex.: Unity, Godot, Rust, monorrepositórios) nem oferecer atalhos diretos associados ao
   workspace sem que o usuário recorra ao Command Palette ou abra terminais manuais.
2. **Sobrecarga de CPU e taxa de requisições por sondagem contínua de PRs e CI checks (`#40541`):**
   O aplicativo revalida todos os Pull Requests e verificações de CI visíveis a cada 1–2 minutos. Em ambientes compartilhados
   com múltiplos desenvolvedores conectados via `orca serve` ou contra servidores corporativos GitHub Enterprise, essa sondagem
   em segundo plano consome núcleos de CPU e esgota limites de cota da API sem que haja ninguém olhando para a tela.
3. **Visão poluída e ações arriscadas no detalhe de automações (`#40507`):**
   A tela de detalhes de automações reunia agendamento, host, métricas de execução e custos em grids densos de difícil leitura,
   enquanto ações potencialmente destrutivas (Pausar e Deletar) ficavam expostas ao lado do botão primário de execução ("Run Now"),
   propiciando cliques acidentais.
4. **Varredura global em rajada de issues do GitHub ao restaurar/focar a janela (`#40534`):**
   Sempre que a janela do app retornava ao foco (ao desminimizar, voltar de outro Space ou reativar de tela cheia), o Orca
   disparava leituras `gh` em segundo plano para todas as issues vinculadas de cada workspace cadastrado. Em workspaces
   com centenas de issues, isso saturava a fila compartilhada de 4 slots do GitHub por minutos, travando a abertura de PRs e abas de CI.
5. **Falso pronto (`tui-idle`) em inicializações a frio do Claude Code no terminal (`#40539`):**
   Ao iniciar o Claude Code, o shell emitia imediatamente o título da janela (`claude`). Se o startup a frio do Claude
   demorasse mais de 3 segundos em silêncio, o orquestrador interpretava o terminal como pronto para entrada e injetava
   a tarefa (`orchestration dispatch --inject`) com a tela ainda em branco, perdendo a instrução.
6. **Perda do estado de tela cheia nativo após reiniciar o aplicativo (`#40540`, resolve `#40510`):**
   No macOS e Linux, se o usuário estivesse usando o aplicativo em modo tela cheia nativo do sistema operacional, qualquer
   reinício (ou atualização automática) restaurava a janela em modo janela comum, exigindo novo acionamento manual.

## O que o upstream implementa e corrige

- **Ponto de contribuição `contributes.worktreeBadges` para plugins (`#40557`):**
  - Permite que manifestos de plugins (`engines.orca >=1.4.256`) declarem badges condicionais nos cartões de workspace;
  - Avalia condições `when.pathExists` (com profundidade `searchDepth: 0..3` e filtro de `host`) de forma assíncrona, em lote e com cache no processo principal, sem expor dados do workspace ao worker até que uma ação seja disparada;
  - Renderiza o ícone SVG diretamente ao lado do nome do workspace e disponibiliza as ações associadas em menu dedicado e no menu de contexto do workspace;
  - Repassa contexto seguro `{ worktree, folder }` para os comandos do worker.
- **Cadência configurável de atualização de PRs (`#40541`):**
  - Adiciona `Settings → Git & Source Control → PR Auto-Refresh`:
    - `Default`: 1 min (selecionado) / 2 min (visíveis);
    - `Reduced (5×)`: 5 min / 10 min;
    - `Minimal (10×)`: 10 min / 20 min;
    - `Off`: desliga os timers em segundo plano;
  - Em servidores `orca serve`, clientes pareados compartilham a resposta em cache até a expiração do intervalo do host, desacoplando o consumo de rede do número de clientes conectados.
- **Redesenho hierárquico da visão de automações (`#40507`):**
  - Reorganiza a página de detalhes com fluxo vertical: cabeçalho com status badge e botão destacado `Run Now`, seguido de faixa de saúde (`Last run`, `Next run` e custo estimado com contagem de tokens);
  - Painéis laterais limpos para agendamento e parâmetros de execução;
  - Seção expansível para o prompt da automação com botão dedicado de cópia para a área de transferência;
  - Ações de pausa e exclusão movidas com segurança para menu dropdown "…".
- **Desativação de varreduras globais de issues no retorno da janela (`#40534`):**
  - Elimina a varredura indiscriminada de issues ao focar a janela, restringindo o refresh exclusivamente a cartões visíveis no viewport (`visible-only` com janela de 5 minutos);
  - Libera a fila concorrente do GitHub CLI para respostas imediatas em PRs, checks e merges.
- **Verificação estrita de pintura de comando (`hasTerminalCommandPainted`) no `tui-idle` (`#40539`):**
  - Exige que o processo em execução tenha efetivamente desenhado texto após o marcador de comando OSC 133;C antes de declarar o terminal como ocioso e pronto para injeção de tarefas.
- **Persistência do estado de tela cheia nativa (`#40540`):**
  - Registra a flag de fullscreen nativo nas preferências de restauração de janela e aplica `setFullScreen(true)` logo após a inicialização no desktop.
- **Eliminação de trabalho Git repetido no watch de checks de CI (`#41332`):**
  - Desacopla o monitoramento contínuo de status de CI do cálculo prévio de arquivos em conflito e detalhes de stack da branch base: 500 leituras de watch passaram de 500 fetches e 422 verificações de mesclagem (2.688 comandos Git) para zero;
  - Preserva o enriquecimento completo de arquivos conflitantes estritamente para leituras explícitas, ativas ou disparadas no mobile.
- **Suspensão de requisições de rate limit para agentes desativados (`#41268`, resolve `#41269`):**
  - Ao desativar Claude ou Codex em Settings > Agents, desconecta o `RateLimitService` do polling de cota (`api.anthropic.com` / `chatgpt.com`), prevenindo emissão de pacotes fora de túneis VPN/proxy e protegendo contas contra suspensões geográficas.
- **Atribuição de demanda Git e descoberta assíncrona de caminhos de setup (`#41325`):**
  - Substitui o spawn síncrono de processos Git no processo principal durante a preparação de scripts de setup pelo executor assíncrono com timeout de 15s, além de etiquetar demandas de catalogação e leituras de status.
- **Configurações nativas de integração e handoff escopado por workspace para plugins (`#41598`, resolve `#41369`):**
  - Adiciona painel nativo de configurações de integração para plugins (`IntegrationsPane`), permitindo parametrização direta sem abrir janelas de navegador externas;
  - Suporta handoff escopado de workspaces para agentes de plugins, validando seletores de rotas e proprietários no processo hospedeiro sem expor credenciais ou chaves sensíveis.
- **Unificação da experiência visual e navegação de páginas de automações (`#41620`):**
  - Consolida as diferentes telas de automações em uma interface unificada (Opção D do redesign), agrupando listagem de rotinas, histórico de execuções e formulário de criação em abas fluidas e consistentes com o design system.
- **API mínima de diagnósticos de plugins para o editor nativo ([`#41616`](https://github.com/stablyai/orca/issues/41616)):**
  - Propõe interface enxuta para que plugins de linter e extensões de linguagem publiquem marcadores e diagnósticos diretamente na calha e nos painéis do editor sem sobrecarga de protocolos LSP completos.

## O que fazer no BrzA Studio

1. Adotar as configurações nativas de integração e handoff de workspaces para plugins (`#41598`, resolve `#41369`).
2. Incorporar a navegação unificada de páginas de automações (`#41620`).
3. Avaliar a API mínima de diagnósticos de plugins para o editor nativo (`#41616`).
4. Eliminar o trabalho repetido de Git (fetches e merge checks) durante o monitoramento de checks de PR (`#41332`).
5. Desligar o polling em segundo plano de rate limits para provedores desativados em configurações (`#41268`, resolve `#41269`).
6. Tornar assíncrona a descoberta de caminhos de setup e atribuição de spans Git (`#41325`).
7. Adotar o ponto de extensão `contributes.worktreeBadges` (`#40557`) no runtime de plugins do `brza-studio`, permitindo que skills e ferramentas especializadas exibam seus badges e menus contextuais na sidebar.
8. Incorporar a configuração `prAutoRefresh` em `Settings` (`#40541`) para aliviar carga de CPU e API rate limits em máquinas compartilhadas.
9. Atualizar o layout do painel de automações (`#40507`) para melhor ergonomia de inspeção e prevenção de cliques destrutivos.
10. Adotar a atualização sob demanda (`visible-only`) de issues do GitHub ao reativar a janela (`#40534`), desobstruindo a fila da CLI.
11. Incorporar a checagem `hasTerminalCommandPainted` em `tui-idle` (`#40539`) para garantir entrega segura de comandos via `orchestration dispatch`.
12. Garantir persistência de fullscreen nativo pós-reinício (`#40540`).
