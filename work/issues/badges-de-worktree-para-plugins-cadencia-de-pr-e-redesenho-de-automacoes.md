---
status: open
description: Os PRs #46945, #46933, #46908 e #46846 tratam host de automação de bots, grace period de dark-wake, runtime_access_denied em status e hooks de workspace off-thread.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#46945`](https://github.com/stablyai/orca/pull/46945) (resolve Issue [`#46919`](https://github.com/stablyai/orca/issues/46919)),
[`stablyai/orca#46933`](https://github.com/stablyai/orca/pull/46933) (resolve Issue [`#46932`](https://github.com/stablyai/orca/issues/46932)),
[`stablyai/orca#46908`](https://github.com/stablyai/orca/pull/46908) (refs Issue [`#46027`](https://github.com/stablyai/orca/issues/46027)),
[`stablyai/orca#46846`](https://github.com/stablyai/orca/pull/46846),
[`stablyai/orca#46624`](https://github.com/stablyai/orca/pull/46624) (refs Issue [`#46564`](https://github.com/stablyai/orca/issues/46564)),
[`stablyai/orca#46584`](https://github.com/stablyai/orca/pull/46584) (resolve Issue [`#46564`](https://github.com/stablyai/orca/issues/46564)),
[`stablyai/orca#46593`](https://github.com/stablyai/orca/pull/46593),
[`stablyai/orca#46522`](https://github.com/stablyai/orca/pull/46522),
[`stablyai/orca#41598`](https://github.com/stablyai/orca/pull/41598) (resolve Issue [`#41369`](https://github.com/stablyai/orca/issues/41369)),
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
7. **Rotulagem genérica e errônea de gatilhos em execuções de automações (`#46624`, `#46584`, resolve `#46564`):**
   Na visão de detalhes da execução (desktop e mobile), qualquer execução de automação disparada por eventos (Webhook, GitHub, Slack) era rotulada genericamente como "Trigger: Scheduled". Além disso, quando eventos subsequentes se agrupavam em uma execução em andamento, o campo `run.event` era sobrescrito, corrompendo a identificação do gatilho original.
8. **Mensagens crípticas de ajuda e erros de sintaxe em agendamentos de automação (`#46593`):**
   A sintaxe e os erros de agendamento de automações (`automation schedule`) emitiam mensagens genéricas do parser cron sem orientar sobre formatos aceitos ou apontar o campo com erro.
9. **Dificuldade de acesso a cookies de autenticação no navegador embutido (`#46522`):**
   A opção "Import Cookies" ficava oculta no submenu profundo do navegador embutido, dificultando a importação de sessões para testes autenticados de automação e web scraping.
10. **Abertura de automação de bots apontando para o host local em vez do host de execução (`#46945`, resolve `#46919`):**
    Ao navegar para os detalhes ou editar uma automação associada a bots executando em nós remotos (WSL ou SSH), o link da interface abria o contexto no host local da UI em vez do host onde o bot reside, provocando falhas de carregamento e comandos apontando para caminhos inexistentes.
11. **Retenções de dark-wake congelando a janela de carência de execuções perdidas (`#46933`, resolve `#46932`):**
    Quando um computador acordava em modo dark-wake (suspensão parcial do sistema operacional com tela desligada), automações com hold ativo paralisavam a contagem do período de tolerância (*grace period*) para execuções agendadas atrasadas, resultando em acúmulo e disparo desordenado de tarefas quando o sistema despertava por completo.
12. **Classificação enganosa de falhas de permissão como daemons inativos no `orca status` (`#46908`, refs `#46027`):**
    Quando comandos `orca status` ou diagnósticos de runtime encontravam recusa de permissão de leitura nos descritores ou sockets do daemon, o comando reportava falsamente que o daemon não estava em execução ("not running"), em vez de sinalizar explicitamente erro de acesso de permissão.
13. **Travamentos e congelamentos da interface durante execução de hooks de workspace (`#46846`):**
    As validações de hooks de workspace executavam checagens síncronas diretamente na thread principal (main thread) do aplicativo, causando travamentos e congelamentos momentâneos no renderer durante a alternância ou abertura de workspaces volumosos.

## O que o upstream implementa e corrige

- **Navegação de automações de bots roteada para o host correto (`#46945`, resolve `#46919`):**
  - Roteia a abertura de automações vinculadas a bots para o host proprietário (WSL, SSH ou runtime host remoto), garantindo visualização correta de logs e paths.
- **Isolamento de dark-wake holds e proteção ao período de carência de agendamentos (`#46933`, resolve `#46932`):**
  - Impede que retenções temporárias de dark-wake congelem o relógio de grace period de execuções perdidas, garantindo despacho ordenado de tarefas atrasadas ao despertar.
- **Sinalização explícita de `runtime_access_denied` em verificações de status (`#46908`, refs `#46027`):**
  - Reporta o estado específico `runtime_access_denied` em vez de falso negativo de processo parado quando houver falha de permissão no socket ou arquivo de lock do daemon.
- **Execução assíncrona de checagens de hooks de workspace fora da thread principal (`#46846`):**
  - Move a verificação e resolução de hooks de workspace para worker threads em background, preservando a fluidez de 60fps da UI durante transições de workspace.
- **Identificação real e durável de gatilhos em execuções de automação (`#46624`, `#46584`, resolve `#46564`):**
  - Registra e preserva o campo imutável `triggeredBy` no ato de criação da execução, evitando que eventos agrupados posteriormente substituam a fonte original;
  - Exibe a fonte real do evento (Webhook, GitHub, Slack, etc.) em Run Details e clientes móveis em vez de marcar genericamente como `Scheduled`.
- **Ajuda e mensagens de erro descritivas para agendamento de automações (`#46593`):**
  - Clarifica a sintaxe esperada nas mensagens de ajuda e detalha os motivos de recusa em cron expressions inválidas na CLI de automações.
- **Opção 'Import Cookies' no topo do menu do navegador embutido (`#46522`):**
  - Promove "Import Cookies" para o primeiro item do menu de opções `⋯` do navegador integrado, acelerando fluxos de autenticação em automações e testes.

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

1. Preservar o gatilho original de automações em `triggeredBy` e rotular execuções de eventos pela sua fonte real (`#46624`, `#46584`, resolve `#46564`).
2. Adotar mensagens de erro detalhadas e ajuda clara na validação de agendamentos cron (`#46593`).
3. Posicionar a ação 'Import Cookies' no topo do menu de contexto do navegador embutido (`#46522`).
4. Adotar as configurações nativas de integração e handoff de workspaces para plugins (`#41598`, resolve `#41369`).
5. Incorporar a navegação unificada de páginas de automações (`#41620`).
6. Avaliar a API mínima de diagnósticos de plugins para o editor nativo (`#41616`).
7. Eliminar o trabalho repetido de Git (fetches e merge checks) durante o monitoramento de checks de PR (`#41332`).
8. Desligar o polling em segundo plano de rate limits para provedores desativados em configurações (`#41268`, resolve `#41269`).
9. Tornar assíncrona a descoberta de caminhos de setup e atribuição de spans Git (`#41325`).
10. Adotar o ponto de extensão `contributes.worktreeBadges` (`#40557`) no runtime de plugins do `brza-studio`, permitindo que skills e ferramentas especializadas exibam seus badges e menus contextuais na sidebar.
11. Incorporar a configuração `prAutoRefresh` em `Settings` (`#40541`) para aliviar carga de CPU e API rate limits em máquinas compartilhadas.
12. Atualizar o layout do painel de automações (`#40507`) para melhor ergonomia de inspeção e prevenção de cliques destrutivos.
13. Adotar a atualização sob demanda (`visible-only`) de issues do GitHub ao reativar a janela (`#40534`), desobstruindo a fila da CLI.
14. Incorporar a checagem `hasTerminalCommandPainted` em `tui-idle` (`#40539`) para garantir entrega segura de comandos via `orchestration dispatch`.
15. Garantir persistência de fullscreen nativo pós-reinício (`#40540`).
16. Rotear a navegação e edição de automações de bots para o host real de execução em nós remotos e WSL (`#46945`, resolve `#46919`).
17. Manter a integridade do período de carência de automações agendadas sob despertares em dark-wake (`#46933`, resolve `#46932`).
18. Distinguir falhas de permissão de acesso ao runtime reportando `runtime_access_denied` no `brza status` (`#46908`, refs `#46027`).
19. Mover a checagem de hooks de workspace para worker threads para eliminar congelamentos na UI (`#46846`).

