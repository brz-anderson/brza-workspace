---
status: open
description: Otimizacao de symlinks no editor (#49466, #49453, #49343), descarte de bitmap eager (#49434) e fim de polling de uso WSL (#49430, #49428).
scope:
  - brza-studio
  - tools-kit
  - workspace
priority: high
opened: 2026-11-04
tags:
  - tooling
  - infra
references:
  - https://github.com/stablyai/orca/pull/48937
  - https://github.com/stablyai/orca/pull/48854
  - https://github.com/stablyai/orca/pull/48853
  - https://github.com/stablyai/orca/pull/48891
  - https://github.com/stablyai/orca/pull/48885
  - https://github.com/stablyai/orca/pull/48847
  - https://github.com/stablyai/orca/pull/48869
  - https://github.com/stablyai/orca/issues/49032
  - https://github.com/stablyai/orca/issues/49007
  - https://github.com/stablyai/orca/pull/48030
  - https://github.com/stablyai/orca/pull/48204
  - https://github.com/stablyai/orca/pull/48207
  - https://github.com/stablyai/orca/pull/48736
  - https://github.com/stablyai/orca/pull/48802
  - https://github.com/stablyai/orca/pull/48734
  - https://github.com/stablyai/orca/pull/48759
  - https://github.com/stablyai/orca/pull/45956
  - https://github.com/stablyai/orca/pull/48577
  - https://github.com/stablyai/orca/pull/48486
  - https://github.com/stablyai/orca/pull/48600
  - https://github.com/stablyai/orca/issues/48656
  - https://github.com/stablyai/orca/pull/48419
  - https://github.com/stablyai/orca/pull/48400
  - https://github.com/stablyai/orca/pull/48407
  - https://github.com/stablyai/orca/issues/48457
  - https://github.com/stablyai/orca/pull/48222
  - https://github.com/stablyai/orca/pull/49252
  - https://github.com/stablyai/orca/pull/48812
  - https://github.com/stablyai/orca/pull/48219
  - https://github.com/stablyai/orca/pull/49075
  - https://github.com/stablyai/orca/pull/49076
  - https://github.com/stablyai/orca/pull/49173
  - https://github.com/stablyai/orca/pull/49171
  - https://github.com/stablyai/orca/issues/49060
  - https://github.com/stablyai/orca/issues/49062
  - https://github.com/stablyai/orca/issues/49059
  - https://github.com/stablyai/orca/issues/49080
  - https://github.com/stablyai/orca/issues/33505
  - https://github.com/stablyai/orca/pull/49466
  - https://github.com/stablyai/orca/pull/49453
  - https://github.com/stablyai/orca/pull/49343
  - https://github.com/stablyai/orca/pull/49434
  - https://github.com/stablyai/orca/pull/49433
  - https://github.com/stablyai/orca/pull/49430
  - https://github.com/stablyai/orca/pull/49428
  - https://github.com/stablyai/orca/pull/49429
  - https://github.com/stablyai/orca/pull/49426
  - https://github.com/stablyai/orca/pull/49390
  - https://github.com/stablyai/orca/pull/49369
  - https://github.com/stablyai/orca/issues/49457
  - https://github.com/stablyai/orca/issues/49444
---

# Consumo de recursos em agentes: reaper de LSP e overhead de hooks

Rastreado dos PRs no upstream [`stablyai/orca#48222`](https://github.com/stablyai/orca/pull/48222),
[`stablyai/orca#48219`](https://github.com/stablyai/orca/pull/48219),
[`stablyai/orca#48211`](https://github.com/stablyai/orca/pull/48211),
[`stablyai/orca#48261`](https://github.com/stablyai/orca/pull/48261),
[`stablyai/orca#48282`](https://github.com/stablyai/orca/pull/48282) (commit `5b59337bdeb`),
[`stablyai/orca#48030`](https://github.com/stablyai/orca/pull/48030),
[`stablyai/orca#48163`](https://github.com/stablyai/orca/pull/48163) (commit `a779ba0f522`),
[`stablyai/orca#48059`](https://github.com/stablyai/orca/pull/48059) (commit `82c7e4e2d83`),
[`stablyai/orca#47917`](https://github.com/stablyai/orca/pull/47917) (commit `552862782d4`),
[`stablyai/orca#48120`](https://github.com/stablyai/orca/pull/48120) (commit `66d362d6215`),
[`stablyai/orca#48121`](https://github.com/stablyai/orca/pull/48121) (commit `6795b42007c`),
[`stablyai/orca#47943`](https://github.com/stablyai/orca/pull/47943) (commit `2af98f82527`),
[`stablyai/orca#47927`](https://github.com/stablyai/orca/pull/47927),
[`stablyai/orca#47911`](https://github.com/stablyai/orca/pull/47911) (commit `e07572e7da5`),
[`stablyai/orca#47900`](https://github.com/stablyai/orca/pull/47900),
[`stablyai/orca#47821`](https://github.com/stablyai/orca/pull/47821),
[`stablyai/orca#47836`](https://github.com/stablyai/orca/pull/47836) (commit `edbdf6506dc`, resolve [`#47826`](https://github.com/stablyai/orca/issues/47826)),
[`stablyai/orca#47853`](https://github.com/stablyai/orca/pull/47853) (commit `4f5e1bb0cd0`, resolve [`#47825`](https://github.com/stablyai/orca/issues/47825)),
[`stablyai/orca#47580`](https://github.com/stablyai/orca/pull/47580) (commit `ab304f7ce7f`),
[`stablyai/orca#47578`](https://github.com/stablyai/orca/pull/47578) (commit `e1f3a99dd60`),
[`stablyai/orca#47835`](https://github.com/stablyai/orca/pull/47835) (commit `e375ec2921b`),
[`stablyai/orca#44265`](https://github.com/stablyai/orca/pull/44265) (commit `50284224e40`),
[`stablyai/orca#47769`](https://github.com/stablyai/orca/pull/47769) (commit `6e0805a2e1f`),
[`stablyai/orca#47765`](https://github.com/stablyai/orca/pull/47765),
[`stablyai/orca#47757`](https://github.com/stablyai/orca/pull/47757) (commit `64eb525c558`),
[`stablyai/orca#47529`](https://github.com/stablyai/orca/pull/47529) (commit `64a57263cf4`),
[`stablyai/orca#47705`](https://github.com/stablyai/orca/pull/47705) (commit `e2c8f4756e8`, refs [`#19792`](https://github.com/stablyai/orca/issues/19792)),
[`stablyai/orca#45844`](https://github.com/stablyai/orca/pull/45844),
[`stablyai/orca#43081`](https://github.com/stablyai/orca/pull/43081) (Issue [`#43095`](https://github.com/stablyai/orca/issues/43095)),
[`stablyai/orca#43106`](https://github.com/stablyai/orca/pull/43106) (resolve Issue [`#43104`](https://github.com/stablyai/orca/issues/43104)),
[`stablyai/orca#43090`](https://github.com/stablyai/orca/pull/43090) (resolve Issue [`#40261`](https://github.com/stablyai/orca/issues/40261)),
[`stablyai/orca#43142`](https://github.com/stablyai/orca/pull/43142),
[`stablyai/orca#43164`](https://github.com/stablyai/orca/pull/43164),
[`stablyai/orca#43129`](https://github.com/stablyai/orca/pull/43129) (resolve Issue [`#40636`](https://github.com/stablyai/orca/issues/40636)),
[`stablyai/orca#43004`](https://github.com/stablyai/orca/pull/43004),
[`stablyai/orca#42964`](https://github.com/stablyai/orca/pull/42964) (resolve Issue [`#42921`](https://github.com/stablyai/orca/issues/42921)),
[`stablyai/orca#42935`](https://github.com/stablyai/orca/pull/42935),
[`stablyai/orca#42889`](https://github.com/stablyai/orca/pull/42889) (resolve Issue [`#42601`](https://github.com/stablyai/orca/issues/42601)),
[`stablyai/orca#42890`](https://github.com/stablyai/orca/pull/42890),
[`stablyai/orca#42807`](https://github.com/stablyai/orca/pull/42807),
[`stablyai/orca#42760`](https://github.com/stablyai/orca/pull/42760),
[`stablyai/orca#42686`](https://github.com/stablyai/orca/pull/42686),
[`stablyai/orca#42743`](https://github.com/stablyai/orca/pull/42743),
[`stablyai/orca#42725`](https://github.com/stablyai/orca/pull/42725) (resolve Issue [`#42724`](https://github.com/stablyai/orca/issues/42724)),
[`stablyai/orca#42660`](https://github.com/stablyai/orca/pull/42660) (resolve Issue [`#19116`](https://github.com/stablyai/orca/issues/19116)),
[`stablyai/orca#42655`](https://github.com/stablyai/orca/pull/42655),
[`stablyai/orca#38189`](https://github.com/stablyai/orca/pull/38189) (Issue [`#38188`](https://github.com/stablyai/orca/issues/38188)),
[`stablyai/orca#38180`](https://github.com/stablyai/orca/pull/38180) (Issue [`#38179`](https://github.com/stablyai/orca/issues/38179)),
[`stablyai/orca#38199`](https://github.com/stablyai/orca/pull/38199) (Issue [`#38181`](https://github.com/stablyai/orca/issues/38181)),
além das issues [`stablyai/orca#42675`](https://github.com/stablyai/orca/issues/42675) e
[`stablyai/orca#42601`](https://github.com/stablyai/orca/issues/42601).

## O problema

1. **Servidores TypeScript LSP órfãos consumindo dezenas de gigabytes de RAM (`#38189`, `#38188`):** cada sessão de agente
   operando no repositório instancia seu próprio servidor de linguagem TypeScript (`tsc --lsp`). Sessões que permaneciam
   ociosas ou conectadas em segundo plano não encerravam seus servidores; em ambientes com múltiplos agentes simultâneos,
   registrou-se acúmulo de mais de 28 GB de memória de trabalho mantidos por instâncias ociosas sem qualquer arquivo aberto.
2. **Explosão de processos nos ganchos gerenciados do Claude (`#38180`, `#38179`):** a cada evento de ferramenta do Claude
   Code (`PreToolUse`), o script de hook do app disparava cerca de 17 subprocessos no macOS e até 19 no Linux para
   computar cabeçalhos, metadados de painel e identidade do agente. Com múltiplos painéis ativos, isso atingia ~35 novos
   processos por segundo; no macOS, onde cada `exec` passa pela validação do `AppleSystemPolicy`, a latência de resposta das
   ferramentas crescia substancialmente sob carga.
3. **Evicção indevida do binário do runtime Node em servidores `orcad` (`#38199`, `#38181`):** a rotina de limpeza de cache de
   artefatos (`pruneOrcadArtifactCache`) removia erroneamente a pasta `runtimes/`, quebrando execuções remotas subsequentes
   com erro `ENOENT` ao tentar disparar o binário `node`.
4. **Consumo contínuo de CPU e GPU por abas de navegador não observadas no `orca serve` (`#42660`, resolve `#19116`):**
   Abas do navegador embutido abertas em segundo plano continuavam renderizando frames e executando loops visuais mesmo sem foco ou visibilidade, retendo centenas de megabytes de memória GPU.
5. **Sobrecarga de hooks de agentes disparados sem contexto Orca ativo (`#42655`):**
   Comandos executados fora do contexto de automação do Orca disparavam rotinas completas de inspeção de hooks antes do leitor de eventos, gerando lentidão e saídas bloqueantes desnecessárias.
6. **Disparos zumbis de hooks por chamadas órfãs de python3 após desinstalação (`#42601`):**
   Hooks residuais configurados no ambiente do usuário continuavam invocando `python3` ciclicamente mesmo após a remoção ou encerramento do app principal.
7. **Retenção contínua de memória por abas ociosas no `orca serve` (`#42686`):**
   Abas abertas no navegador remoto permaneciam alocadas em memória indefinidamente mesmo após horas de inatividade, sem descarregamento automático de processos filhos.
8. **Falhas na execução de hooks do Claude no Windows com espaços em caminhos de executáveis (`#42743`):**
   Quando o Claude era instalado em caminhos contendo espaços no Windows, o formato legado de invocação de hook falhava por erro de citação de linha de comando.
9. **Atraso de ~2.1s no fechamento de terminais e estouro de tiles de custos (`#42675`, `#42725`, resolve `#42724`):**
   O fechamento de terminais interativos zsh aguardava desnecessariamente 2.1s de grace period de SIGKILL porque o zsh ignora SIGTERM por padrão; em Stats & Usage, valores altos de custos transbordavam seus cartões visuais.
10. **Overhead de memória com supervisores Electron no Native Chat (`#42760`):**
    Cada aba de chat nativo instanciada no Electron subia um processo supervisor completo com runtime web, consumindo ~46 MiB de RSS por sessão. Em ambientes com dezenas ou centenas de chats históricos (ex.: 150 abas), isso acumulava mais de 7 GB de RSS desperdiçados em background.
11. **Runtimes gerenciados obsoletos acumulando espaço em disco e sidecars de cache sem compressão (`#42807`):**
    Versões antigas de runtimes baixados pelo daemon permaneciam indefinidamente na máquina após upgrades, ocupando gigabytes em disco; além disso, sidecars de histórico de uso e telemetria de modelos (Codex, OpenCode, Muse) eram gravados como JSON plano não comprimido.
12. **Resíduos persistentes de hooks, CLI e serviços de background após desinstalação (`#42889`, resolve `#42601`):**
    Ao desinstalar o Studio ou apagar o aplicativo, hooks injetados nas configurações de agentes (`~/.claude`, `~/.codex`, `~/.gemini`), binários na `PATH`, serviços do `orca serve` e scripts em `~/.orca/agent-hooks` permaneciam órfãos gerando erros em terminais independentes.
13. **Prompts repetitivos a cada alteração no `orca.yaml` do repositório (`#42890`):**
    Qualquer edição nos comandos de setup do `orca.yaml` (ex.: novo passo no branch `main`) disparava nova caixa de diálogo de aprovação de segurança para todos os usuários em cada criação de worktree, mesmo em repositórios corporativos já confiados.
14. **Falhas de Out of Memory (OOM) no AI Vault ao varrer históricos grandes (`#42964`, resolve `#42921`):**
    A varredura e indexação de sessões históricas de múltiplos agentes em `ai-vault` operava com limite rígido padrão de heap (128-256 MB) no processo de background. Em workspaces com semanas de histórico e centenas de transcrições, o processo sofria crash de OOM e interrompia a catalogação de conversas.
15. **Sobrecarga contínua de consultas à tabela de processos no macOS (`#43004`):**
    Para verificar os nomes e estados de janelas de terminal ativas no macOS, o app realizava frequentes varreduras completas da árvore de processos do sistema operacional, gerando consumo elevado de CPU e lentidão sob concorrência.
16. **Diálogos repetitivos de aprovação de setup hooks no app móvel (`#42935`):**
    No cliente móvel, cada inicialização de workspace exigia reaprovação dos scripts de setup de `orca.yaml`, sem mecanismo de persistência de aprovação única.
17. **Disparos custosos de processos por hooks fora do app e chamadas repetidas a `ps` (`#43081`, `#43095`):**
    Comandos executados fora do aplicativo disparavam scripts de hooks gerenciados que iniciavam múltiplos processos `ps` no macOS, sobrecarregando agentes de Endpoint Security.
18. **Explosão de chamadas à API `count_tokens` na retomada de sessões do Claude (`#43106`, resolve `#43104`):**
    Ao retomar uma conversa, o relatório de contexto disparava uma requisição separada de `count_tokens` por ferramenta e item, estourando gateways e limitadores de taxa da Anthropic.
19. **Processos PTY de agentes desacoplados nunca recolhidos pelo daemon ativo (`#43090`, resolve `#40261`):**
    Quando agentes terminavam sua execução mas o PTY permanecia desacoplado, o daemon ativo não realizava o reap dos processos zumbis, acumulando descritores de arquivo.
20. **Reconstrução completa da lista de conversas do AI Vault a cada 20s (`#43142`):**
    A sincronização de títulos recriava a lista integral de sessões periodicamente, gerando pausas de GC e contenção de I/O desnecessárias.
21. **Leituras de fingerprint Git bloqueando a pool principal de I/O do runtime (`#43164`):**
    Operações lentas de verificação de integridade Git no repositório consumiam threads da libuv pool, atrasando respostas RPC de status do daemon.
22. **Sondagens redundantes de PATH no Windows para agentes desabilitados (`#43129`, resolve `#40636`):**
    O runtime verificava executáveis no disco para agentes que haviam sido desabilitados nas configurações, gerando I/O lento no Windows.
23. **Subnotificação de memória de agentes de chat e servidores de linguagem (LSP) no Resource Manager (`#45844`):**
    Como agentes de chat (Claude, Codex e CLIs de provedores iniciados via chat) executam fora dos terminais gerenciados, o Resource Manager não computava seus processos: a métrica indicava poucos gigabytes para "Agents" enquanto chats e seus LSPs retinham dezenas de gigabytes de RAM. Além disso, a listagem de sessões de terminal emitia falsos avisos amarelos sempre que um terminal iniciava ou encerrava concorrentemente durante a leitura.
24. **Carga contínua no processo principal do Electron na varredura de portas no Linux (`#47943`):**
    A cada 30 segundos, a verificação de portas abertas varria `/proc` executando `readlink` assíncrono para cada descritor de arquivo aberto na máquina diretamente no processo principal do Electron, retendo entre 400ms e 1000ms de CPU por varredura em sistemas ocupados.
25. **Inicialização precoce de workers de journal e processos de backend de usage (`#47580`, `#47578`, commits `ab304f7ce7f`, `e1f3a99dd60`):**
    O daemon subia workers de banco de journal mesmo quando nenhum chat DB existia e inicializava o processo utilitário de métricas de usage imediatamente no boot em vez de sob demanda, consumindo memória residente desnecessariamente.
26. **Lookups redundantes de workers em itens bloqueados por limites de cota (`#47835`, commit `e375ec2921b`, e `#47911`):**
    O motor de automação e itens de bots realizava varreduras completas no banco e disco para itens que limites de cota não podiam mover, além de descartar leituras de workers vinculados já assentados entre exibições.
27. **Perda silenciosa de watch em raízes locais após disparo do fusível de crash (`#44265`, commit `50284224e40`):**
    Quando um watcher local de arquivos sofria crash recorrente e o disjuntor de proteção esfriava, o runtime não reativava a observação da raiz local, deixando alterações no sistema de arquivos indetectadas.
28. **Contenção de CPU por concorrência de `check:changed` entre worktrees (`#47821`, commit `e0b56784f11`, e `#47900`):**
    Em hosts ocupados com múltiplos worktrees, execuções concorrentes de validação de alterações disputavam CPU intensamente sem serialização ou reaproveitamento do grafo de importação.
29. **Conflito de registro e hooks em workers Task do Droid (`#47836`, commit `edbdf6506dc`, e `#47853`, commit `4f5e1bb0cd0`):**
    Hooks gerenciados instalados em caminhos incorretos do Droid e eventos disparados por subagentes Task sobrescreviam indevidamente a linha do agente e o estado do painel.
30. **Invalidation de layout e restyle global de árvore DOM ao abrir ou fechar modais (`#48419`):**
    Abertura e fechamento de modais de formulário, configurações e popups acionavam recálculos de estilo síncronos e restyle em toda a árvore DOM da janela principal, gerando engasgos de frame e congelamento transitório de digitação.
31. **Saturação de I/O e tempestade de eventos de filesystem durante o primeiro despacho (`#48400`):**
    Durante o `first-work` e provisionamento inicial de branches/worktrees, watchers de diretório disparavam centenas de eventos em cascata, concorrendo com o checkout de arquivos e gerando travamentos de I/O no daemon.
32. **Processos workers de plugins e tarefas desacopladas permanecendo órfãos após encerramento (`#48407`):**
    Ao fechar abas de plugins ou finalizar despachos automatizados, processos auxiliares de plugins mantinham sockets e subprocessos abertos consumindo memória de fundo.
33. **Custo excessivo de invocações completas de `git status` para verificação de dirty status (`#48457`):**
    Consultas frequentes de estado de modificação executavam `git status --porcelain` completo mesmo em repositórios massivos sem alterações em disco.
34. **Retenção de memória e descritores de terminais/layouts em workspaces estacionados ou ocultos (`#45956`):**
    Workspaces que ficavam inativos ou minimizados continuavam retendo instâncias ativas de layout e buffers de terminal no heap do renderer e no daemon de processos, consumindo centenas de megabytes.
35. **Ordem de execução não determinística e contenção na fila de `check:changed` (`#48577`):**
    Tarefas de checagem de alteração de arquivos (`check:changed`) competiam de forma desordenada sem fila estrita de chegada, penalizando workspaces ativos com esperas arbitrárias.
36. **Servidor Codex lendo `~/.codex` como diretório de projeto (`#48486`):**
    Quando o servidor Codex inicializava, considerava a pasta de configuração de usuário como workspace de projeto, varrendo recursivamente arquivos de cache e travando a CPU.
37. **Overhead e consumo de memória no spawn de processos via fork/exec (`#48600`):**
    A instanciação de subprocessos pelo Node.js duplicava a tabela de páginas da memória da aplicação via fork padrão; a migração para `posix_spawn` eliminou picos de memória e latência de arranque.
38. **Vazamento e overhead de telemetria em probes de status contínuos (`#48656`):**
    Sondagens de telemetria de uso e recursos executavam sem throttling sob alta carga, elevando o tempo de ciclo do loop de eventos.

## O que o upstream propõe e implementa

- **Liberação de terminais e layouts de workspaces estacionados ou ocultos (`#45956`):**
  - Desaloca buffers PTY e layouts de abas em segundo plano quando um workspace é estacionado ou permanece oculto, reidratando-os sob demanda no foco.
- **Fila estrita FIFO para execuções de `check:changed` (`#48577`):**
  - Enfileira checagens de integridade e arquivos alterados em ordem rigorosa de chegada, prevenindo inanição (*starvation*) e contenção desordenada de CPU.
- **Isolamento de diretório home do servidor Codex (`#48486`):**
  - Assegura que o servidor Codex execute em sua home dedicada sem interpretar `~/.codex` ou diretórios de metadados como repositórios de projeto.
- **Substituição de spawn tradicional por `posix_spawn` nativo (`#48600`):**
  - Adota `posix_spawn` para lançamento de executáveis auxiliares e agentes, cortando custos de clonagem de heap e acelerando a criação de processos.
- **Throttling e contenção de overhead em probes de telemetria contínuos (`#48656`):**
  - Aplica amortecimento dinâmico em verificações repetidas de status de sistema sob estresse de CPU.
- **Delegação da varredura de portas no Linux para worker auxiliar e comando único `ls -ln` (`#47943`):**
  - Transfere a resolução de sockets para processos para o worker de port-scan fora do processo principal do Electron;
  - Executa um único comando `ls -ln /proc/[0-9]*/fd` com filtragem em streaming das linhas `fd -> socket:[N]`, reduzindo o custo de CPU de ~1000ms no main process para ~30-50ms no worker com fallback seguro para a varredura legada.
- **Boot sob demanda de workers de journal e processos utilitários de usage (`#47580`, `#47578`, commits `ab304f7ce7f`, `e1f3a99dd60`):**
  - Omite o boot de workers de journal SQLite quando nenhum banco de chat existe;
  - Inicializa o processo utilitário de estatísticas e limites de usage (`usage backend`) de forma lazy, apenas quando a primeira consulta de telemetria é solicitada.
- **Supressão de lookups de workers em itens bloqueados por cota e cache de workers resolvidos (`#47835`, commit `e375ec2921b`, e `#47911`):**
  - Pula a resolução de workers para itens que excederam cotas de uso e preserva em cache as leituras de workers vinculados já assentados entre visualizações de itens.
- **Reativação automática de watchers locais após resfriamento do fusível de crash (`#44265`, commit `50284224e40`):**
  - Restaura a observação de raízes locais após o período de cooldown do disjuntor de segurança do watcher.
- **Serialização de verificações de alterações e reuso de grafo de importação (`#47821`, commit `e0b56784f11`, e `#47900`):**
  - Permite a serialização de verificações `check:changed` entre worktrees concorrentes e reutiliza o grafo de dependências do event loop em inspeções locais de modificações.
- **Isolamento de hooks gerenciados do Droid e correção de registro de Task workers (`#47836`, commit `edbdf6506dc`, e `#47853`, commit `4f5e1bb0cd0`):**
  - Instala hooks gerenciados exatamente onde o Droid espera encontrá-los e impede que eventos de Task workers afetem a linha de status do agente no painel.

- **Contabilização e atribuição completa de memória de chat agents no Resource Manager (`#45844`):**
  - Cada processo de provedor de chat registra seu PID durante a execução e toda a sua árvore de processos (incluindo LSPs e ferramentas) é contabilizada sob a seção Agents;
  - Atribui a árvore de processos ao workspace e chat correspondente, exibindo o logo do provedor e nome da conversa com navegação por clique; processos compartilhados são agrupados em linha dedicada;
  - Elimina o falso aviso de erro em terminais relendo a lista dentro do mesmo orçamento de tempo e efetuando retries a cada 2s com o painel aberto;
  - Preserva a chave da aba de terminais restaurados no boot para exibir o nome correto da aba em vez de um PID cru.

- **Supressão de scripts de hook fora de painéis Orca (`#43081`):**
  - Ignora scripts de hook quando o comando não é originado de painéis gerenciados, cortando chamadas repetidas de `ps` no macOS.
- **Resumo de uso de contexto eliminando `count_tokens` repetidos (`#43106`, resolve `#43104`):**
  - Requisita resumo agregado de contexto em chamada única ao retomar sessões do Claude, estancando sobrecargas na API da Anthropic.
- **Reaper automático de PTYs desacoplados no daemon (`#43090`, resolve `#40261`):**
  - Varre e encerra processos PTY órfãos de agentes desacoplados periodicamente.
- **Sincronização incremental de títulos no AI Vault (`#43142`):**
  - Atualiza apenas itens modificados sem reconstruir a lista a cada 20 segundos.
- **Isolamento de leituras de fingerprint Git (`#43164`):**
  - Executa verificações de fingerprint em worker dedicado fora da pool principal da libuv.
- **Supressão de sondagem de PATH para agentes desativados (`#43129`, resolve `#40636`).**
- **Elevação do heap do scanner de sessões do AI Vault para 768 MB e ajuste configurável (`#42964`, resolve `#42921`):**
  - Aumenta o limite padrão de heap para 768 MB no processo auxiliar de indexação do AI Vault e expõe configuração para permitir ajuste manual em workspaces massivos, eliminando crashes de OOM.
- **Cache de nomes de terminal no macOS reduzindo consultas ao processo do sistema (`#43004`):**
  - Implementa cache local em memória dos nomes de terminais verificados, reduzindo drasticamente as invocações à tabela de processos (`sysctl`/`ps`) no macOS.
- **Aprovação única persistente de hooks de setup no cliente móvel (`#42935`):**
  - Implementa retenção de aprovação de hooks `orca.yaml` no cliente móvel, evitando prompts repetitivos a cada sincronização.
- **Substituição de supervisores Electron por agentes nativos leves no Native Chat (`#42760`):**
  - Converte os supervisores de sessão do Native Chat de processos Electron render para workers nativos enxutos;
  - Reduz o consumo de RSS de ~46 MiB/chat para menos de 1.8 MiB/chat (economia de mais de 7 GB de RAM em instalações com 150 chats).
- **Limpeza de runtimes obsoletos no boot e compressão gzip de sidecars (`#42807`):**
  - Implementa rotina de inicialização no daemon para expurgar runtimes gerenciados órfãos ou de versões anteriores que não estão em uso ativo por nenhum worktree;
  - Aplica compressão streaming gzip transparente aos sidecars de telemetria e cache de uso de tokens do Codex, OpenCode e Muse, reduzindo a pegada em disco em até 80%.
- **Idle reaper com watchdog para o Agent LSP Bridge (`#38189`):**
  - Implementa monitoramento de documentos abertos e tráfego em ambas as direções;
  - Encerra automaticamente instâncias do TypeScript LSP após `ORCA_TS_LSP_IDLE_MS` (padrão de 1 hora) sem tráfego e
    com zero documentos abertos;
  - Reinicia o servidor de forma transparente assim que o agente volta a abrir um arquivo;
  - Fecha adequadamente pipes de `stdin` e trata sinais `SIGBREAK`/`exit`.
- **Redução de 17 para 7 processos por evento de hook (`#38180`):**
  - Implementa `orca_hook_pack_metadata`: empacota o cabeçalho `X-Orca-Hook-Metadata` uma única vez por painel em arquivo
    temporário atômico, reutilizando-o enquanto os dados de entrada permanecerem idênticos;
  - Lê identidade de agentes no Linux via `/proc/<pid>/stat` e `boot_id` com builtins do shell e no macOS ignora `uname`
    quando `OSTYPE` já é conhecido;
  - Reduz de 17 para 7 processos no macOS (e para 6 no Linux), preservando byte a byte as mensagens entregues ao servidor de hooks.
- **Proteção da pasta de runtimes no orcad (`#38199`):**
  - Exclui explicitamente o diretório `runtimes/` da política de evicção do cache de artefatos.
- **Suspensão de renderização e liberação de GPU em abas inativas do `orca serve` (`#42660`, resolve `#19116`):**
  - Pausa o renderizador contínuo e descarrega texturas de memória de vídeo para abas do navegador que não estão ativamente visíveis na interface remota, economizando ciclos de GPU e memória RAM sob concorrência.
- **Dreno rápido e saída limpa de hooks fora do contexto Orca (`#42655`):**
  - Detecta antecipadamente a ausência de variáveis de ambiente e sockets de controle do Orca, drenando a entrada e saindo com status 0 instantaneamente sem processamento pesado.
- **Tratamento de hooks órfãos de python3 (`#42601`):**
  - Desativa com segurança hooks obsoletos ao detectar ausência do executável principal ou flags de desinstalação.
- **Descarte e restauração transparente de abas ociosas no `orca serve` (`#42686`):**
  - Descarrega processos de abas do navegador remoto após período configurável de inatividade, restaurando a página sob demanda no primeiro acesso sem perder cookies nem contexto.
- **Formato seguro de exec hook para caminhos com espaços no Windows (`#42743`):**
  - Adota chamada estruturada em array de argumentos para hooks do Claude no Windows, eliminando falhas de quoting e caminhos com espaços.
- **Confinamento de custos em Stats & Usage e sinal de encerramento de terminal (`#42725`, `#42675`, resolve `#42724`):**
  - Ajusta a tipografia e contenção em tiles de custos grandes para evitar quebra de layout;
  - Trata o sinal de fechamento de terminais zsh para evitar esperar o timeout de 2.1s de SIGKILL.
- **Desinstalação limpa via UI e CLI (`#42889`, resolve `#42601`):**
  - Adiciona o grupo *Settings › Advanced › Uninstall Orca* e o comando `orca uninstall [--yes] [--json]`;
  - Varre e remove atomicamente todos os hooks instalados nas configs de agentes, scripts em `~/.orca`, binários na PATH e serviços em background, mantendo os dados e projetos do usuário intactos.
- **Aprovação única de `orca.yaml` por repositório (*Always trust*) (`#42890`):**
  - Reformula o diálogo de confirmação de setup em três opções explícitas (*Always trust*, *Run once*, *Don't run*);
  - *Always trust* grava a confiança a nível de repositório, permitindo que futuras alterações no `orca.yaml` sejam executadas sem novos diálogos de confirmação.
- **Leitura em lote de frotas de bots sem releituras individuais por item (`#47769`, commit `6e0805a2e1f`):**
  - O bot work list realizava leituras individuais completas de cada agente e workspace por linha;
  - O commit consolida a leitura em uma única chamada de frota compartilhada (`fleet read`), compartilhando acessos a repositórios entre workspaces do mesmo batch e mantendo o runtime dentro do orçamento de linhas.
- **Redução de carga em banco e disco na leitura de workers vinculados a bots (`#47765`):**
  - Cada vez que a lista de itens de um bot exibia seus workers vinculados, o Orca percorria a cadeia de follow-up no banco e no disco reconstruindo queries do zero; o PR `#47765` evita alocações desnecessárias e preserva a memória do garbage collector.
- **Construção de dependências do chat host apenas na instalação (`#47757`, commit `64eb525c558`):**
  - Constrói dependências do chat host apenas no momento da instalação, eliminando a varredura repetitiva de tool-secrets em cada chamada a `ensure`.
- **Janela de operações do journal indexada por turnos ancorados (`#47529`, commit `64a57263cf4`):**
  - Ao abrir um turno antigo de uma operação terminada, o leitor percorria todas as linhas até a cabeça do chat e listava todos os envios históricos;
  - Introduz `throughAnchoredTurns`, delimitando a janela com índices criados na inicialização sem alteração de esquema, tornando o custo de carregar turnos antigos constante.
- **Expurgo do pipe do Chromium Crashpad herdado em ambientes PTY (`#47705`, commit `e2c8f4756e8`, refs `#19792`):**
  - O processo principal exportava `CHROME_CRASHPAD_PIPE_NAME` e os painéis herdavam a variável; após reinicialização do daemon, processos filhos encontravam um pipe morto gerando erros em stderr no Windows e poluição de ambiente;
  - Remove a variável de ambiente (case-insensitive) nos construtores de painel antes do merge explícito, e reutiliza o mesmo predicado no sanitizador do Antigravity ACP.
- **Conflito de hooks de subagente Droid e reset de sessão principal do terminal (`#47826` e `#47825`):**
  - Quando o Droid executa subagentes `Task`, envia eventos de hook próprios (SessionStart, Stop, SessionEnd) que resetam indevidamente a linha de sessão principal do terminal; além disso, o Droid ignora os hooks do Orca se `~/.factory/hooks.json` definir o mesmo evento que `~/.factory/settings.json`.
- **Contenção de estilo e isolamento de renderização em modais (`#48419`):**
  - Aplica CSS `contain: layout style` e scoping nos containers de diálogo/modais, evitando que o mount/unmount de popups provoque restyle e reflow síncronos na árvore inteira do documento.
- **Pausa de watchers durante o first-work de automações e branches (`#48400`):**
  - Pausa temporariamente os watchers de filesystem (`fs.watch`) durante o bootstrap inicial (`first-work`), retomando a escuta apenas após o checkout completo dos arquivos de projeto.
- **Reap garantido de workers e subprocessos de plugins órfãos (`#48407`):**
  - Registra tratadores de terminação e monitoramento de keepalive para processos de plugins desacoplados, encerrando processos filhos e liberando descritores de sockets na finalização de tarefas.
- **Cheque leve de dirty status antes de invocar `git status` (`#48457`):**
  - Compara carimbos de data/hora (`mtime`) e stat do diretório `.git` e working tree antes de despachar comandos caros de `git status --porcelain`.

## O que fazer

- Consolidar leituras de frotas de bots em uma única leitura compartilhada (`fleet read`) sem re-ler agentes por linha (`#47769`).
- Otimizar consultas de banco e disco ao listar workers vinculados a bots (`#47765`).
- Construir dependências do chat host apenas na instalação para evitar sweeps repetitivos de tool-secrets (`#47757`).
- Indexar janelas de operações no journal por turnos ancorados via `throughAnchoredTurns` (`#47529`).
- Expurgar `CHROME_CRASHPAD_PIPE_NAME` de ambientes herdados em painéis PTY e no sanitizador do Antigravity ACP (`#47705`, refs `#19792`).
- Prevenir que hooks de subagentes do Droid resetem a sessão principal do terminal e suportar `~/.factory/hooks.json` (`#47826`, `#47825`).

- Suprimir execuções de scripts de hook fora de painéis gerenciados e reduzir invocações a `ps` (`#43081`, `#43095`).
- Adotar resumo de contexto de tokens para Claude em retomadas de sessão para eliminar estouro de gateways (`#43106`, resolve `#43104`).
- Implementar o reaper de PTYs desacoplados no daemon (`#43090`, resolve `#40261`).
- Eliminar reconstruções periódicas da lista de conversas no AI Vault a cada 20s (`#43142`).
- Isolar leituras de fingerprint Git fora da thread pool principal do runtime (`#43164`).
- Suspender sondagens de executáveis no PATH no Windows para agentes desativados (`#43129`, resolve `#40636`).
- Elevar o heap do scanner de sessões do AI Vault para 768 MB configuráveis (`#42964`, resolve `#42921`).
- Cachear nomes de terminal verificados no macOS para mitigar chamadas contínuas à tabela de processos (`#43004`).
- Permitir aprovação única de hooks de setup `orca.yaml` no mobile (`#42935`).
- Implementar o comando `brza uninstall` e a seção de desinstalação limpa em *Settings › Advanced* (`#42889`, resolve `#42601`).
- Adotar a política de confiança de setup por repositório (*Always trust*) em `orca.yaml` (`#42890`).
- Substituir supervisores Electron por workers nativos leves no Native Chat (`#42760`).
- Implementar purga de runtimes gerenciados obsoletos no boot do daemon e compressão gzip de caches de telemetria (`#42807`).
- Descarregar automaticamente abas ociosas de navegador no `brza serve` e restaurá-las sob demanda (`#42686`).
- Adotar o formato seguro de exec hook para caminhos de executáveis no Windows (`#42743`).
- Conter valores grandes de custos nos cartões de Stats & Usage (`#42725`, resolve `#42724`).
- Eliminar a espera desnecessária de 2.1s no fechamento de terminais zsh (`#42675`).
- Portar a redução de overhead de hooks (`#38180`) e o reaper de LSP ocioso (`#38189`) para o `brza-studio`.
- Aplicar a suspensão de renderização e liberação de GPU em abas não observadas do `orca serve` (`#42660`, resolve `#19116`).
- Adotar a saída rápida de hooks sem contexto Orca ativo (`#42655`).
- Prevenir a execução zumbi de hooks órfãos de python3 (`#42601`).
- Contabilizar e atribuir processos e consumo de memória de agentes de chat e servidores de linguagem ao respectivo workspace no Resource Manager (`#45844`).
- Mover a varredura de sockets/portas no Linux para o worker de scan com comando único `ls -ln /proc/*/fd` fora do Electron main (`#47943`, commit `2af98f82527`).
- Postergar o boot de workers de journal e do processo de backend de usage até que haja necessidade real (`#47580`, `#47578`).
- Omitir lookups de workers vinculados para itens limitados por cota de uso e cachear workers assentados (`#47835`, `#47911`, commit `e07572e7da5`).
- Reatar a observação de raízes locais após o resfriamento do fusível de crash do watcher (`#44265`).
- Habilitar serialização de `check:changed` entre worktrees concorrentes em hosts ocupados (`#47821`, `#47900`).
- Instalar hooks gerenciados no caminho lido pelo Droid e isolar eventos de Task workers da linha de agentes (`#47836`, `#47853`).
- Eliminar checagens repetitivas de arquivos git a cada 30 segundos em todos os worktrees enquanto o aplicativo estiver ocioso (`#48030`).
- Prevenir sobreposição de tentativas concorrentes de limpeza de workspaces (`#48163`, commit `a779ba0f522`).
- Transmitir downloads e salvamentos em disco como frames binários em streaming mantendo memória heap constante (`#48059`, commit `82c7e4e2d83`).
- Construir o registro de RPCs do runtime desktop uma única vez no boot em vez de instanciar a cada chamada (`#47917`, commit `552862782d4`).
- Modularizar e limitar funções extensas do registro de sessões de navegador (`#48120`, `#48121`).
- Compactar entradas de `worktreeOwnerIndexCache` e construir correspondências de forma lazy no renderer (`#48222`).
- Reter exclusivamente chaves de configuração inspecionadas no `StampedGitConfig` do processo principal (`#48219`).
- Desduplicar objetos idênticos de modelos e esforço durante a hidratação do catálogo de agentes (`#48211`).
- Elevar o limite de conexões simultâneas do Relay por computador de 8 para 32 (`#48261`).
- Buscar o motor de renderização de diagramas do computador sob demanda apenas no primeiro desenho de diagrama no mobile (`#48282`, commit `5b59337bdeb`).
- Conter restyle e recálculo de layout na abertura e fechamento de modais com isolamento CSS (`#48419`).
- Pausar temporariamente watchers de filesystem durante first-work e criação de worktrees (`#48400`).
- Implementar encerramento determinístico e cleanup de workers de plugins desacoplados (`#48407`).
- Adotar checagem leve de mtime/stat antes de disparar `git status` completo para verificação de dirty (`#48457`).
- Desalocar buffers de terminais e layouts de workspaces estacionados ou minimizados (`#45956`).
- Adotar fila estrita FIFO de execuções para `check:changed` entre worktrees (`#48577`).
- Isolar diretório de trabalho do servidor Codex impedindo varredura de `~/.codex` (`#48486`).
- Utilizar `posix_spawn` nativo no lançamento de subprocessos auxiliares (`#48600`).
- Aplicar amortecimento dinâmico em sondagens contínuas de telemetria sob alta carga (`#48656`).
- Interromper a checagem repetitiva de arquivos git a cada 30 segundos em todos os worktrees durante a ociosidade (`#48030`).
- Impedir que dados em cache do git retenham buffers de saídas completas na memória heap (`#48204`).
- Armazenar digest SHA-256 em vez do JSON bruto na linha de base de `KeyedJsonRowCache` (`#48207`).
- Compartilhar opções de modelo idênticas ao carregar a lista de modelos salvos (`#48211`).
- Construir variáveis de ambiente para sondagem de shell apenas quando a sondagem for efetivamente executada (`#48736`).
- Omitir busca de Home de bots em faixas de abas nas quais nenhum bot resida (`#48802`).
- Reter carimbo único por remetente em conectores mesmo através de falhas sucessivas de inicialização (`#48734`).
- Notificar clientes pareados quando worktrees sofrerem alterações externas sem watcher desktop ativo (`#48759`).
- Interromper livelock no `fs.watch` no Windows quando um diretório observado for excluído (`#48937`).
- Descarregar spawns de fallback do `orca-provider-exec` para worker threads fora da main thread (`#48854`).
- Executar processos filhos POSIX com `terminationBarrier: true` em worker threads dedicadas (`#48853`).
- Impedir que digitação no editor verifique o layout de cada workspace oculto em background (`#48891`).
- Omitir lookups de histórico de workers quando nenhum worker estiver sendo vinculado (`#48885`).
- Capturar picos de memória do processo principal a cada 10s consultando a telemetria do sistema operacional (`#48847`).
- Otimizar busca de handles de terminais fechados com tabela hash em O(1) no mobile (`#48869`).
- Tratar limpeza de workers de plugins que sofreram reap para não deixar requisições travadas em cancelamento (`#49032`).
- Proteger ciclo de vida da janela no macOS contra travamentos em exceções do `NSAutoFillHeuristicController` (`#49007`).
- Compartilhar um único file watcher entre pastas aninhadas em abas do editor atrás de links simbólicos (`#49252`).
- Cessar a reescrita em disco de sessões de busca e linhas de checagem de PR inalteradas (`#48812`).
- Reter em memória apenas chaves de configuração do Git inspecionadas em `StampedGitConfig` (`#48219`).
- Interromper o reescaneamento completo de worktrees a cada salvamento de arquivos Markdown (`#49075`).
- Omitir chamada síncrona a `taskkill /T` no Windows se o processo raiz já encerrou (`#49076`, mitigando Issue `#49060`).
- Descarregar execuções de sondagem de catálogo de modelos e inicialização de CLIs da main thread no Windows (`#49062`, `#49059`).
- Habilitar watchdog persistente de travamentos do processo principal no Windows (`#49080`).
- Evitar enumeração excessiva de alvos do navegador a cada clique na página de servidores (`#49173`).
- Abrir credenciais sob demanda por chamada de ferramenta e evitar releituras de visões encerradas (`#49171`).
- Implementar confirmação por retenção de atalho ("Hold ⌘Q to quit") enquanto houver agentes em processamento ativo (`#33505`).
- Preservar watch ativo em pastas symlinked quando o afunilamento de escopo falhar e coalescer ao reabrir abas (`#49466`, `#49453`, `#49343`).
- Evitar leitura afobada (eager) de bitmaps em `DataTransfer.files` na colagem DOM no terminal (`#49434`).
- Evitar reaplicação redundante de temas e aparência a terminais headless existentes na criação de PTY (`#49433`).
- Expurgar entradas aposentadas de uso WSL e remover timer ocioso de expiração periódica (`#49430`, `#49428`).
- Computar `findIndexedWorktrees` a partir de `locationsById` em um único passo no renderer (`#49429`).
- Otimizar autocompletar de documentação Markdown cortando transformações repetitivas de strings (`#49426`).
- Interromper o recálculo contínuo do cabeçalho de uso para tooltips de chips na status bar (`#49390`).
- Ignorar checagens de proprietário no macOS para clientes de encaminhamento de portas desconectados na fila (`#49369`).
- Ler credenciais protegidas do Cursor via os-secret-store/cursor-safe-storage no Windows (`#49457`).
- Reconectar terminais automaticamente após remontagem de unidades de disco desconectadas (`#49444`).
