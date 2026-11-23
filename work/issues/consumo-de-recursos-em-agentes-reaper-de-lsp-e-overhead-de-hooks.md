---
status: open
description: O PR #45844 contabiliza a memória de agentes de chat e seus LSPs no Resource Manager e elimina falsos avisos de terminais.
scope:
  - brza-studio
  - tools-kit
  - workspace
priority: high
opened: 2026-11-04
tags:
  - tooling
  - infra
---

# Consumo de recursos em agentes: reaper de LSP e overhead de hooks

Rastreado dos PRs abertos no upstream [`stablyai/orca#45844`](https://github.com/stablyai/orca/pull/45844),
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

## O que o upstream propõe e implementa

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

## O que fazer

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

