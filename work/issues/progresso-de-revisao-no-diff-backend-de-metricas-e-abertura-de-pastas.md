---
status: open
description: Suporte a repositorios Nostr ngit NIP-34 (#49968, #49969), reconhecimento de work items no GitLab (#49894) e retentativa de consultas Jira Cloud (#49660).
scope:
  - brza-studio
  - brza-workflow
  - workspace
priority: high
opened: 2026-11-10
tags:
  - tooling
  - infra
  - design
references:
  - https://github.com/stablyai/orca/pull/48945
  - https://github.com/stablyai/orca/pull/48579
  - https://github.com/stablyai/orca/pull/48933
  - https://github.com/stablyai/orca/pull/48905
  - https://github.com/stablyai/orca/issues/49052
  - https://github.com/stablyai/orca/issues/49040
  - https://github.com/stablyai/orca/issues/49025
  - https://github.com/stablyai/orca/pull/48732
  - https://github.com/stablyai/orca/pull/48719
  - https://github.com/stablyai/orca/pull/48682
  - https://github.com/stablyai/orca/pull/48217
  - https://github.com/stablyai/orca/issues/48797
  - https://github.com/stablyai/orca/issues/48793
  - https://github.com/stablyai/orca/issues/48845
  - https://github.com/stablyai/orca/pull/48553
  - https://github.com/stablyai/orca/pull/48558
  - https://github.com/stablyai/orca/pull/48520
  - https://github.com/stablyai/orca/pull/48587
  - https://github.com/stablyai/orca/pull/48493
  - https://github.com/stablyai/orca/pull/48663
  - https://github.com/stablyai/orca/issues/48661
  - https://github.com/stablyai/orca/pull/48650
  - https://github.com/stablyai/orca/issues/48647
  - https://github.com/stablyai/orca/pull/44229
  - https://github.com/stablyai/orca/pull/42949
  - https://github.com/stablyai/orca/pull/48373
  - https://github.com/stablyai/orca/pull/48363
  - https://github.com/stablyai/orca/pull/48351
  - https://github.com/stablyai/orca/pull/48392
  - https://github.com/stablyai/orca/pull/48429
  - https://github.com/stablyai/orca/pull/48293
  - https://github.com/stablyai/orca/pull/48294
  - https://github.com/stablyai/orca/issues/48291
  - https://github.com/stablyai/orca/issues/48279
  - https://github.com/stablyai/orca/issues/48309
  - https://github.com/stablyai/orca/pull/48047
  - https://github.com/stablyai/orca/issues/48022
  - https://github.com/stablyai/orca/pull/48122
  - https://github.com/stablyai/orca/pull/47812
  - https://github.com/stablyai/orca/pull/47262
  - https://github.com/stablyai/orca/issues/48012
  - https://github.com/stablyai/orca/issues/47870
  - https://github.com/stablyai/orca/commit/596618a7e52
  - https://github.com/stablyai/orca/commit/6efc8b5a57a
  - https://github.com/stablyai/orca/pull/47639
  - https://github.com/stablyai/orca/pull/49249
  - https://github.com/stablyai/orca/pull/49265
  - https://github.com/stablyai/orca/pull/49214
  - https://github.com/stablyai/orca/pull/49239
  - https://github.com/stablyai/orca/pull/49073
  - https://github.com/stablyai/orca/pull/49070
  - https://github.com/stablyai/orca/pull/49212
  - https://github.com/stablyai/orca/pull/49157
  - https://github.com/stablyai/orca/pull/49232
  - https://github.com/stablyai/orca/issues/49219
  - https://github.com/stablyai/orca/issues/49158
  - https://github.com/stablyai/orca/issues/49067
  - https://github.com/stablyai/orca/issues/49096
  - https://github.com/stablyai/orca/issues/43635
  - https://github.com/stablyai/orca/pull/49411
  - https://github.com/stablyai/orca/pull/49401
  - https://github.com/stablyai/orca/pull/49410
  - https://github.com/stablyai/orca/pull/49389
  - https://github.com/stablyai/orca/pull/49378
  - https://github.com/stablyai/orca/pull/49294
  - https://github.com/stablyai/orca/pull/49276
  - https://github.com/stablyai/orca/pull/49335
  - https://github.com/stablyai/orca/issues/49442
  - https://github.com/stablyai/orca/issues/49399
  - https://github.com/stablyai/orca/issues/49321
  - https://github.com/stablyai/orca/pull/49629
  - https://github.com/stablyai/orca/pull/49633
  - https://github.com/stablyai/orca/pull/49641
  - https://github.com/stablyai/orca/pull/49599
  - https://github.com/stablyai/orca/pull/49593
  - https://github.com/stablyai/orca/pull/49537
  - https://github.com/stablyai/orca/pull/49504
  - https://github.com/stablyai/orca/issues/49597
  - https://github.com/stablyai/orca/issues/49583
  - https://github.com/stablyai/orca/issues/49558
  - https://github.com/stablyai/orca/issues/49528
  - https://github.com/stablyai/orca/issues/49509
  - https://github.com/stablyai/orca/issues/49499
  - https://github.com/stablyai/orca/pull/49968
  - https://github.com/stablyai/orca/pull/49894
  - https://github.com/stablyai/orca/pull/49660
  - https://github.com/stablyai/orca/pull/49949
  - https://github.com/stablyai/orca/issues/49969
  - https://github.com/stablyai/orca/issues/49824
  - https://github.com/stablyai/orca/issues/49806
  - https://github.com/stablyai/orca/issues/49901
  - https://github.com/stablyai/orca/issues/49940
  - https://github.com/stablyai/orca/issues/49938
---

# Progresso de revisão no diff, backend de métricas e abertura de pastas

Rastreado dos commits no upstream [`stablyai/orca#47531`](https://github.com/stablyai/orca/pull/47531) (commit `596618a7e52`),
[`stablyai/orca#47932`](https://github.com/stablyai/orca/pull/47932) (commit `6efc8b5a57a`),
além da issue [`stablyai/orca#47870`](https://github.com/stablyai/orca/issues/47870),
[`stablyai/orca#47639`](https://github.com/stablyai/orca/pull/47639) (resolve Issue [`#47631`](https://github.com/stablyai/orca/issues/47631)),
[`stablyai/orca#46334`](https://github.com/stablyai/orca/pull/46334) (resolve Issue [`#46332`](https://github.com/stablyai/orca/issues/46332)),
[`stablyai/orca#46333`](https://github.com/stablyai/orca/pull/46333) (resolve Issue [`#46331`](https://github.com/stablyai/orca/issues/46331)),
[`stablyai/orca#46381`](https://github.com/stablyai/orca/pull/46381),
[`stablyai/orca#46225`](https://github.com/stablyai/orca/pull/46225) (refs Issue [`#46113`](https://github.com/stablyai/orca/issues/46113)),
[`stablyai/orca#46276`](https://github.com/stablyai/orca/pull/46276),
além da issue [`stablyai/orca#46359`](https://github.com/stablyai/orca/issues/46359),
[`stablyai/orca#40776`](https://github.com/stablyai/orca/pull/40776) (resolve Issue [`#40768`](https://github.com/stablyai/orca/issues/40768)),
[`stablyai/orca#40792`](https://github.com/stablyai/orca/pull/40792),
[`stablyai/orca#40818`](https://github.com/stablyai/orca/pull/40818) (resolve Issue [`#40675`](https://github.com/stablyai/orca/issues/40675)),
[`stablyai/orca#40627`](https://github.com/stablyai/orca/pull/40627),
[`stablyai/orca#40790`](https://github.com/stablyai/orca/pull/40790) (resolve Issue [`#40789`](https://github.com/stablyai/orca/issues/40789)),
[`stablyai/orca#40816`](https://github.com/stablyai/orca/pull/40816) e das issues
[`#40786`](https://github.com/stablyai/orca/issues/40786) e
[`#40787`](https://github.com/stablyai/orca/issues/40787).

## O problema

1. **Ausência de mapa e progresso de revisão arquivo a arquivo no diff (`#40776`, resolve `#40768`):**
   Ao revisar branches longos ou grandes pull requests no visualizador de diff do Studio, o revisor não dispunha de
   indicador de progresso persistente nem controle para marcar arquivos já inspecionados ("Viewed"). A cada recarregamento
   da aba ou alternância de arquivos, o fluxo reiniciava do zero, sem integração entre o diff e a lista de arquivos alterados
   no painel de Source Control.
2. **Contenção no processo principal e latência de timers por sondagem de métricas de uso (`#40792`, relacionado a `#40682`):**
   A coleta de métricas de uso (Claude, Codex, tokens e analytics) executava diretamente no processo principal do Electron,
   com mais de 30 handlers e varreduras bloqueando o event loop. Em frotas grandes, a latência de timers do processo principal
   chegava a mais de 1.800 ms, provocando engasgos gerais na digitação e na interface.
3. **Falha silenciosa ao clicar em links de pastas gerados pela IA no chat (`#40818`, resolve `#40675`):**
   Quando o modelo de IA citava um diretório (ex.: `src/components/` ou `/srv/repo/docs`), o link exibia o rótulo incorreto
   "Open file" e o clique não realizava nenhuma ação perceptível. Em workspaces remotos/pareados, a resolução de arquivos locais
   falhava silenciosamente e deixava o usuário sem feedback.
4. **Sobrecarga de I/O de disco por regravação completa do profile em movimentos de janela (`#40627`):**
   Cada movimentação de janela, redimensionamento ou pequena alteração visual disparava a serialização e gravação integral do
   snapshot de perfil no disco, gerando escritas desnecessárias e concorrência com o banco SQLite.
5. **Escape do comando Select All (Cmd+A) fora de notas Markdown focadas (`#40790`, resolve `#40789`):**
   Ao pressionar Cmd+A para selecionar todo o texto de uma nota Markdown aberta no editor, o foco vazava para elementos
   externos da janela ou selecionava o canvas inteiro em vez de restringir a seleção ao buffer do documento ativo.
6. **Perda da última aba fechada ao tentar reabrir a partir da tela de boas-vindas (`#40816`):**
   Após fechar todas as abas e cair na landing surface (*welcome screen*), acionar o atalho `Cmd+Shift+T` ("Reopen Closed Tab")
   não encontrava a última aba encerrada no histórico recente da sessão.
7. **Demanda por personas persistentes com governança, custos e segredos integrados (`#40786`):**
   Desenvolvedores e equipes demandam suporte nativo a personas persistentes de agentes com papéis explícitos, tarefas especializadas,
   árvore hierárquica e controle de custos e segredos por agente.
8. **Edições feitas no modo Edit não sincronizadas com o diff ao retornar para Changes (`#46334`, resolve `#46332`):**
   Ao fazer edições no modo Edit e retornar para a visualização Changes, os modelos mantidos do Monaco reutilizavam o texto antigo sem sincronizar propriedades, exibindo alterações defasadas e sobrescrevendo o texto correto ao digitar.
9. **Colapso do visualizador Monaco de diff sob o banner de modificação externa no disco (`#46333`, resolve `#46331`):**
   O componente `EditorEditFileSurface` envolvia o `ChangesModeView` em uma div com display block comum, anulando o `flex-1` e colapsando a altura do editor Monaco para 0px enquanto o banner "changed on disk" permanecia visível.
10. **Duplicação de grupos de projetos e subpastas ao escanear novamente pastas-mãe (`#46225`, refs `#46113`):**
    Escanear uma pasta-mãe pela segunda vez criava novos grupos de projeto duplicados com o mesmo caminho normalizado, gerando desorganização e perda de ordem na barra lateral.
11. **Dificuldade de fechamento de visualizador de imagem e exclusão destrutiva de pastas com worktrees filhos (`#46276`, `#46359`):**
    O visualizador de imagens exigia clique preciso no botão de fechar, e a exclusão de workspaces pais não oferecia a opção de manter seus sub-worktrees filhos preservados.
12. **Diff obsoleto servido a partir de cache após regravação in-place de arquivos (`#47639`, resolve `#47631`):**
    Quando um arquivo era reescrito in-place preservando o timestamp de modificação (`mtime`), tamanho e inode, o carimbo gerado para o arquivo na working-tree era idêntico ao anterior. Como consequência, o cache de diff servia o diff defasado antigo em vez de invalidar a visualização.
13. **Marcador de comando concluído emitido pelo próprio agente encerrando indevidamente seu comando (`#47531`, commit `596618a7e52`):**
    O terminal interpretava marcas OSC de comando concluído impressas pelo próprio agente como o término da execução, finalizando processos antes do tempo.
14. **Falha de disparo de seleção no primeiro clique em células de código de notebooks (`#47932`, commit `6efc8b5a57a`):**
    Em células de código de Jupyter notebooks, o primeiro clique do mouse falhava em iniciar a seleção de texto, demandando múltiplos cliques repetidos.
15. **Ausência de busca transversal contínua (Cmd/Ctrl+F) em todos os arquivos no diff combinado "View all changes" (`#47870`):**
    Ao visualizar todas as modificações combinadas de uma revisão, a ferramenta de busca localizava ocorrências somente dentro do arquivo ativo em foco, sem navegar entre múltiplos arquivos.
16. **Execução insegura de binários do sistema no Windows via System32 relativo (`#48293`):**
    Chamadas a utilitários de sistema no Windows (como `cmd.exe` ou `powershell.exe`) utilizavam caminhos relativos ou variáveis não validadas em vez de resolver o caminho canônico a partir de `SystemRoot` validado, gerando vulnerabilidade a DLL/binary hijacking em diretórios locais manipulados.
17. **Dificuldade de abrir a interface móvel diretamente no navegador do smartphone (`#48294`, Issue `#48291`):**
    Ao escanear o QR Code de pareamento ou clicar em "Open in browser", a aplicação tentava abrir um visualizador embutido restrito em vez de despachar a URL pareada diretamente para o navegador padrão do celular.
18. **Find in Files não permitindo pesquisar arquivos ignorados pelo Git (`#48279`):**
    A busca textual transversal do editor ("Find in Files") excluía incondicionalmente qualquer arquivo presente no `.gitignore` (como arquivos `.env`, configurações locais ou documentações geradas), sem toggle para incluir arquivos ignorados sob demanda.
19. **Sessões da CLI do Devin armazenadas em SQLite ausentes no Session History (`#48309`):**
    O painel de Session History e AI Vault não lia os bancos de dados SQLite locais criados por execuções autônomas da CLI do Devin, deixando essas sessões invisíveis no histórico unificado de conversas.
20. **Navegação rígida no diff review forçando a seção inferior Commits (`#44229`):**
    A visualização de diff dividia a tela com uma seção fixa de commits na parte inferior, reduzindo a área vertical de código e dificultando a alternância entre diff de working tree, staged e commits individuais.
21. **Ausência de ação de rebase direta a partir da linha de base-branch (`#42949`):**
    Para atualizar o branch de um worktree contra a branch base (main/master), o desenvolvedor precisava abrir o terminal ou menu de branches em vez de ter um botão de rebase direto na linha do branch base.
22. **Nomes de arquivos com caracteres não-ASCII corrompidos na geração de commits e PRs (`#48373`):**
    Módulos de IA geradores de mensagens de commit e descrições de PR escapavam ou corrompiam nomes de arquivos contendo acentos, cedilhas ou caracteres CJK (ex.: `\303\241` em vez de `á`).
23. **Falta de justificativa explicativa quando um agent Command não pode ser executado (`#48363`):**
    Quando um comando sugerido por um agente na barra de ações estava desabilitado, o botão ficava cinza sem tooltip ou indicação de motivo (ex.: worktree dirty, terminal ocupado).
24. **Lista desordenada de repositórios no diálogo de setup do GitHub (`#48351`):**
    O modal de configuração do GitHub listava todos os repositórios em lista plana alfabética, misturando repositórios pessoais e de diferentes organizações.
25. **Falta de opção para abrir a pasta/arquivo no gerenciador de arquivos do sistema a partir do File Explorer (`#48392`):**
    Não havia comando no menu de contexto do explorador de arquivos para abrir o Finder (macOS) ou Explorer (Windows) no caminho selecionado.
26. **Falta de agrupamento por projeto na CLI `orca worktree create` (`#48429`):**
    Ao criar múltiplos worktrees via CLI, eles eram alocados sem vínculo com o grupo de projetos pai correspondente.
27. **Sobrecarga de reconstrução de histórico no menu de escopo do diff review (`#48553`, STA-17982..17986):**
    Ao alternar commits ou escopo de arquivos no visualizador de diff (*scope-menu*), o componente recomputava todo o histórico de revisões anteriores de forma síncrona, provocando quedas de taxa de quadros e engasgos de rolagem.
28. **Comandos Look around falhando no Windows por falta de suporte a PowerShell e encadeamento (`#48558`):**
    A rotina de inspeção ambiental Look around no Windows tentava executar comandos encadeados com sintaxe Bash (`&&`, `;`) sem suporte nativo a pipelines PowerShell, resultando em falhas silenciosas de verificação.
29. **Ausência de `--focus text` e omissão da causa de recusa de ferramentas via CLI (`#48520`):**
    Operações de CLI que solicitavam foco no editor não suportavam focalizar diretamente blocos de texto/prosa, e quando uma ferramenta era recusada pelo agente, o motivo detalhado não era exposto no retorno estruturado.
30. **Processamento em múltiplas passagens para atribuição de mensagens de turno no journal (`#48587`, STA-18015):**
    A rotina de vinculação de turnos (*attribute turn messages*) executava sucessivos scans e atualizações no banco SQLite para atribuir mensagens de entrada e saída, duplicando I/O sob fluxos concorrentes.
31. **Perda de mensagens de início falho de chat para o conector de origem (`#48493`):**
    Quando um chat falhava antes de estabelecer o canal de comunicação, as mensagens emitidas na fase de handshake não eram transportadas de volta para o conector, deixando o cliente sem diagnósticos de erro.
32. **Incapacidade de executar scripts diretamente a partir do File Explorer (`#48663`, resolve Issue `#48661`):**
    Desenvolvedores precisavam abrir um terminal manualmente e navegar até o diretório para rodar scripts de compilação ou teste selecionados na árvore do explorador.
33. **Falta de controle de zoom no Workspace Board (`#48650`, resolve Issue `#48647`):**
    O quadro visual de workspaces e cards de tarefas (Workspace Board) não oferecia controles de ampliação ou redução (zoom in/out/reset), dificultando a visão panorâmica em monitores grandes e laptops.

## O que o upstream implementa e corrige

- **Poda de trabalho redundante de histórico no scope-menu de diff review (`#48553`):**
  - Otimiza a renderização do menu de escopo calculando apenas o delta necessário entre os commits selecionados sem reconstruir a árvore completa de histórico.
- **Suporte nativo a PowerShell e encadeamento de comandos em Look around (`#48558`):**
  - Habilita invocação via PowerShell com separadores seguros de encadeamento no Windows durante checagens Look around somente leitura.
- **Suporte a `--focus text` e reporte explícito de motivo de recusa (`#48520`):**
  - Implementa a flag `--focus text` para focar diretamente o bloco de prosa e propaga o campo `refusalReason` no resultado da ferramenta.
- **Atribuição de mensagens de turnos em passagem única no SQLite (`#48587`):**
  - Reduz as transações de atribuição de mensagens de turno para uma única passagem otimizada no journal de chat.
- **Transporte de mensagens de inicialização falha de volta ao conector (`#48493`):**
  - Encaminha logs e diagnósticos de erro ocorridos no arranque da sessão diretamente para o conector que solicitou a abertura.
- **Ação de execução de scripts a partir do menu de contexto do File Explorer (`#48663`, resolve `#48661`):**
  - Adiciona a ação "Run Script" no menu de clique direito de arquivos executáveis no explorador, disparando em terminal dedicado.
- **Controles de zoom e pan no Workspace Board (`#48650`, resolve `#48647`):**
  - Adiciona botões de zoom in (+), zoom out (-) e reset (100%), além de suporte a atalhos de teclado e gestos de pinça no trackpad.
- **Menu de escopo 'which-changes' substituindo a seção inferior de commits (`#44229`):**
  - Adiciona menu seletor de escopo no topo do diff (Working Tree, Staged, ou commit específico), liberando 100% da área vertical e permitindo navegação limpa.
- **Ação de rebase a partir da linha da base-branch (`#42949`):**
  - Introduz botão direto de rebase contra a base branch configurada na linha de status do Source Control.
- **Normalização de nomes de arquivos não-ASCII em mensagens de commit e PRs (`#48373`):**
  - Decodifica caracteres UTF-8 escapados pelo Git para renderizar nomes reais de arquivos na síntese de mensagens por IA.
- **Tooltips informativos com motivo de bloqueio em agent Commands (`#48363`):**
  - Exibe mensagem explicativa clara ao passar o mouse sobre comandos desabilitados.
- **Agrupamento por organização no modal de repositórios do GitHub (`#48351`):**
  - Organiza a lista de repositórios por conta pessoal e organizações do GitHub.
- **Comando 'Reveal in OS file manager' no File Explorer (`#48392`):**
  - Adiciona ação de menu para abrir a pasta ou arquivo no Finder/Explorer nativo do sistema operacional.
- **Agrupamento por projeto na criação de worktrees via CLI (`#48429`):**
  - Suporta flag `--project-group` em `orca worktree create` para associar o novo checkout ao grupo pai.
- **Resolução segura de caminhos do System32 via SystemRoot validado (`#48293`):**
  - Valida e ancora todos os executáveis de sistema no caminho canônico `%SystemRoot%\System32` no Windows.
- **Abertura direta da UI móvel no navegador do celular (`#48294`, resolve `#48291`):**
  - Redireciona o handshake de pareamento móvel para o navegador padrão do smartphone com suporte a web app e PWA.
- **Toggle para buscar em arquivos ignorados no Find in Files (`#48279`):**
  - Adiciona opção "Search in git-ignored files" no painel de busca global.
- **Descoberta e exibição de sessões SQLite da CLI do Devin no histórico (`#48309`):**
  - Integra o parser de sessões SQLite do Devin ao catálogo unificado de Session History.
- **Isolamento de marcas de comando concluído de agentes no terminal (`#47531`, commit `596618a7e52`):**
  - Garante que a marcação OSC de fim de comando emitida pelo agente não seja confundida com o encerramento do subprocesso.
- **Início imediato de seleção em células de notebook (`#47932`, commit `6efc8b5a57a`):**
  - Corrige o manipulador de eventos de mouse para iniciar a seleção logo no primeiro clique dentro de células de código.
- **Busca contínua (Find) transversal em arquivos no modo combined diff (`#47870`):**
  - Especificação para permitir busca Cmd/Ctrl+F percorrendo todos os blocos de arquivos na visualização combinada.


- **Invalidação de cache de diff considerando avanço de `ctime` (`#47639`, resolve `#47631`):**
  - Incorpora o `ctime` aos carimbos de arquivos da working-tree junto a `mtime`, tamanho e inode, e usa o mais recente entre os dois timestamps na guarda contra racy-writes;
  - Como a chamada `stat` já retorna `ctime`, a checagem invalida corretamente o cache em regravações in-place sem custo extra de I/O.
- **Progresso de revisão por arquivo no diff compartilhado com Source Control (`#40776`):**
  - Adiciona controle `[x] Viewed` nos cabeçalhos individuais de diff e no cabeçalho do combined diff ("View all"), com atalho `Ctrl+V` no macOS (ou `Alt+Shift+V`);
  - Arquivos marcados como vistos são automaticamente recolhidos no modo combined diff e atenuados visualmente na árvore do Source Control;
  - Persiste em `orca.reviewed-diffs.v1` com invalidação barata baseada em assinatura de conteúdo, entry signature e modified time (até 5.000 registros e poda de 90 dias).
- **Serviços de métricas de uso em processo de backend supervisionado (`#40792`):**
  - Extrai os coletores de telemetria, cache de uso e analytics para um processo de backend dedicado via MessagePort;
  - Reduz a latência de timers do processo principal de 1.836 ms para 833 ms e o atraso p99 do event loop de 10,4 ms para 5,5 ms;
  - Reconexão transparente em caso de falha do processo secundário sem derrubar o Electron principal.
- **Abertura e revelação de links de diretórios no Chat UI (`#40818`, resolve `#40675`):**
  - Detecta caminhos terminados em barra como diretórios (`isDirectoryHint`), exibindo o rótulo "Open folder";
  - Revela a pasta no explorer do worktree correspondente (suportando ambientes locais e remotos pareados) ou foca a raiz do workspace;
  - Emite notificação de erro explícita caso o caminho não exista em vez de falha silenciosa.
- **Otimização de persistência de perfil em manipulações de janela (`#40627`):**
  - Desacopla mudanças transitórias de posição de janela e redimensionamento de gravações imediatas de perfil no disco.
- **Confinamento de Select All ao editor Markdown (`#40790`):**
  - Restringe o escopo de Cmd+A estritamente ao editor de notas ativo.
- **Restauração de abas fechadas a partir da tela de boas-vindas (`#40816`):**
  - Preserva a pilha de abas fechadas acessível mesmo quando a janela estiver vazia, permitindo que `Cmd+Shift+T` reabra a última aba.
- **Reconciliação e sincronização automática entre Edit mode e Changes mode (`#46334`, resolve `#46332`):**
  - Reconcilia ambos os modelos Monaco do diff com as propriedades recebidas na montagem antes de anexar listeners, resetando modelos cujo texto mudou e preservando histórico de desfazer (undo) em abas intocadas.
- **Correção de layout flexbox no banner de alteração externa no editor (`#46333`, resolve `#46331`):**
  - Ajusta o wrapper do banner em `EditorEditFileSurface` para flex column, impedindo o colapso do editor de diff.
- **Refatoração modular de `EditorEditFileSurface` sob teto de 400 linhas (`#46381`):**
  - Modulariza a superfície de edição do editor mantendo cada arquivo sob o limite rigoroso de lint arquitetural de 400 linhas.
- **Reuso inteligente de grupos de scan com o mesmo caminho-mãe (`#46225`, refs `#46113`):**
  - Reutiliza grupos existentes na mesma conexão com caminho normalizado idêntico, reorganizando subpastas e preservando a ordem pré-existente de repositórios.
- **Visualizador de imagens com scrim em tela cheia e fechamento por clique externo (`#46276`):**
  - Adiciona scrim completo de janela ao visualizador de imagens, permitindo fechamento instantâneo ao clicar em qualquer área externa à imagem.

## O que fazer no BrzA Studio

1. Adotar o controle de arquivos revisados `[x] Viewed` no diff e Source Control (`#40776`).
2. Avaliar a migração dos serviços de uso para processo de backend supervisionado (`#40792`) para sanar travamentos no macOS.
3. Adotar o reconhecimento e revelação de pastas a partir de links no chat (`#40818`).
4. Confinar o Select All ao editor Markdown (`#40790`) e habilitar reabertura de abas a partir do welcome screen (`#40816`).
5. Acompanhar a modelagem de Personas persistentes (`#40786`) para alinhar com o ecossistema `brza-sessions` e `meeting-runner`.
6. Sincronizar modelos Monaco entre Edit mode e Changes mode reconciliando props na montagem (`#46334`, resolve `#46332`).
7. Corrigir layout flex column do banner de alteração externa para não colapsar o diff Monaco (`#46333`, resolve `#46331`).
8. Reutilizar grupos de scan na barra lateral com caminhos-mãe idênticos para evitar duplicações (`#46225`, refs `#46113`).
9. Adotar fechamento por clique externo (scrim) no visualizador de imagens (`#46276`) e avaliar suporte a "Delete, Keep Children" em workspaces (`#46359`).
10. Incluir `ctime` no carimbo de arquivos para invalidar o cache de diff do Git em regravações in-place com mtime preservado (`#47639`, resolve `#47631`).
11. Prevenir que marcas OSC de comando concluído emitidas pelo próprio agente encerrem o processo de terminal (`#47531`, commit `596618a7e52`).
12. Habilitar início imediato de seleção no primeiro clique do mouse em células de código de notebooks (`#47932`, commit `6efc8b5a57a`).
13. Implementar atalho Cmd/Ctrl+F transversal cobrindo todos os arquivos no diff combinado "View all changes" (`#47870`).
14. Adicionar configuração de largura de leitura de Markdown (largura cheia vs coluna centralizada) (`#48047`, resolve Issue `#48022`).
15. Copiar blocos de código com quebras de linha CRLF no Windows para execução ordenada em colagens multilinhas do PowerShell (`#48122`, commit `a7fbb36d436`).
16. Exibir skeletons animados estruturados enquanto checks de PR e comentários carregam no diff review (`#47812`, commit `207212b6b46`).
17. Assegurar carregamento confiável de abas restauradas do navegador após restart quando extensões estiverem instaladas (`#47262`, commit `53846893079`).
18. Tratar cabeçalhos e identidade de cliente CLI do Codex Native Chat para ambientes com proxy restritivo (`#48012`).
19. Validar caminhos de ferramentas do Windows ancorando em `SystemRoot` canônico (`#48293`).
20. Habilitar abertura da interface móvel no navegador nativo do smartphone (`#48294`, resolve `#48291`).
21. Adicionar opção para pesquisar arquivos ignorados pelo Git no Find in Files (`#48279`).
22. Incluir sessões SQLite da CLI do Devin no Session History unificado (`#48309`).
23. Substituir a seção inferior fixa de commits pelo menu de escopo 'which-changes' no topo da visualização de diff (`#44229`).
24. Adicionar ação direta de rebase contra a base branch na barra de status do Source Control (`#42949`).
25. Decodificar nomes de arquivos não-ASCII para renderização legível em mensagens de commit e descrições de PR geradas por IA (`#48373`).
26. Exibir tooltips informativos com motivo do bloqueio em agent Commands desabilitados (`#48363`).
27. Agrupar repositórios por organização no diálogo de configuração do GitHub (`#48351`).
28. Adicionar ação 'Reveal in OS file manager' (Finder / Explorer) no menu do File Explorer (`#48392`).
29. Suportar associação a grupos de projeto na criação de worktrees via CLI (`#48429`).
30. Podar recálculos desnecessários de histórico no scope-menu de diff review (`#48553`).
31. Suportar PowerShell e encadeamento seguro de comandos Look around no Windows (`#48558`).
32. Suportar flag `--focus text` e reportar o motivo formal de recusa de ferramentas (`#48520`).
33. Consolidar a atribuição de mensagens de turnos em passagem única no banco (`#48587`).
34. Transportar mensagens de chats que falharam no arranque de volta ao conector solicitante (`#48493`).
35. Permitir execução direta de scripts via clique direito no File Explorer (`#48663`, resolve `#48661`).
36. Incorporar controles de zoom e ajuste panorâmico no Workspace Board (`#48650`, resolve `#48647`).
37. Datar o PR gerado por uma cadeia de workers pela timestamp do seu passo mais recente (`#48732`).
38. Elevar o limite de links e referências associadas em itens de trabalho (`#48719`).
39. Permitir operações de escrita na área de transferência originadas por gestos em páginas pré-visualizadas (`#48682`).
40. Suportar renderização de fórmulas matemáticas (KaTeX / LaTeX) no visualizador de documentos e chat (`#48797`).
41. Corrigir decodificação de texto chinês em codificações GBK e GB18030 na visualização de git diff (`#48793`).
42. Estabilizar assistente de arrasto do Computer Use no macOS em sistemas com idiomas não-ingleses (`#48845`).
43. Centralizar configuração de abertura de links em uma opção única respeitando navegador do sistema (`#48217`).
44. Fazer fallback para endpoint `/changes` na listagem de arquivos de Merge Request em instâncias GitLab anteriores à 15.7 (`#48945`).
45. Escopar follow-ups de histórico no Source Control para otimizar tempo de carregamento de diffs (`#48579`).
46. Abrir links clicados com `Shift+Cmd+Click` no navegador padrão do sistema operacional (`#48933`, resolve Issue `#48976`).
47. Limpar e simplificar menu de Source Control no mobile exibindo apenas opções aplicáveis (`#48905`).
48. Exibir git blame diretamente na linha sob o cursor em abas de visualização de diff (`#49052`).
49. Permitir visualização e edição direta do projeto associado na tela de issues do Linear (`#49040`).
50. Evitar fechamento indesejado do menu 'Send notes to an agent' ao clicar em uma linha de agente no card do workspace (`#49025`).
- Alertar na CLI quando o comando invocado apontar para binário de outra instalação do Orca no sistema (`#49249`).
- Adicionar ação rápida "Only" para focar em projeto único no seletor da página de Tarefas (`#49265`).
- Preservar filtros e atributos do Linear na página de Tarefas ao alternar entre visões (`#49214`, resolve Issue `#49219`).
- Habilitar palavra-chave dedicada de tabulação na busca de espaços em branco de diffs (`#49239`).
- Reportar erro detalhado de resolução do branch base padrão em vez de falso "no default base" em worktrees (`#49073`).
- Otimizar indexação de atualização de CLIs e verificar hosts conectados de forma proativa (`#49212`, `#49157`, `#49232`).
- Suportar redimensionamento e comentários inline no modo de plano inline (`#49158`).
- Pré-carregar dados da tela de Tarefas para evitar carregamento em branco ao reabrir (`#49067`).
- Desabilitar botão de merge em PRs quando o usuário possuir acesso apenas de leitura ao repositório base (`#49096`).
- Estipular prazo limite (deadline) estrito para turnos de automação de host em background durante migrações WSL (`#49411`, `#49401`).
- Enumerar links apenas uma vez quando um ouvinte de conector for anexado (`#49410`).
- Aplicar preenchimento total de largura (full-width hover fill) em linhas agrupadas de configurações (`#49389`).
- Ajustar contagens prévias, retentativa e automações locais transferidas em operações WSL Move (`#49378`).
- Refinar barra de uso compacta com rótulos e ícones atenuados e numerais tabulares nítidos (`#49294`, `#49276`).
- Exibir explicações detalhadas ao bloquear atualizações e reversões por encerramento de servidor não confirmado (`#49335`).
- Corrigir links de referências de issues em chat para apontarem para o repositório de trabalho ativo em vez do upstream (`#49442`).
- Oferecer opção de largura total (full-width) na visualização rica de Markdown (`#49399`).
- Adicionar botão para salvar imagens diretamente a partir do visualizador integrado (`#49321`).
- Abrir o Git Graph de repositórios em cartões de pastas diretamente no workspace da pasta (`#49629`, resolve Issue `#49597`).
- Reverificar vereditos de preflight locais obsoletos na visualização de Tarefas (`#49633`).
- Ocultar projetos que não sejam do GitHub quando possuírem remotes adicionais conflitantes (`#49641`, resolve Issue `#49583`).
- Exibir anotações inline de `git blame` na visualização de diff de revisão (`#49558`).
- Finalizar limpa e previamente processos na pasta de instalação do Windows antes de aplicar updates (`#49599`).
- Manter linhas de configurações experimentais visíveis durante toda a sessão de ajustes (`#49593`).
- Empacotar ícones nativos de aplicativos no seletor 'Open in' eliminando requisições externas de favicons (`#49537`).
- Comparar seletores de nomes na CLI com suporte a strings Unicode em decomposição NFD (`#49504`).
- Permitir edição direta de arquivos a partir da visualização de diff (`#49528`).
- Acelerar o painel do Git com seletor persistente de branches e prévia de diff em tempo real no Histórico (`#49509`, `#49499`).
- Adicionar suporte a repositórios descentralizados Nostr NIP-34 (`ngit`) para issues e PRs no desktop (`#49968`, resolve Issue `#49969`).
- Reconhecer URLs de `work_items`, `epics` e `test_cases` na checagem de escopo de repositórios GitLab (`#49894`, resolve Issue `#49824`).
- Reexecutar consultas JQL amplas delimitando aos projetos visíveis no Jira Cloud (`#49660`).
- Mover servidor Orca salvo para novo host SSH em vez de duplicá-lo no cadastro (`#49949`).
- Preservar ordenação `ORDER BY` de consultas JQL personalizadas no Jira Tasks (`#49806`).
- Exibir contador regressivo em chips compactos quando uma janela de cota estiver prestes a resetar (`#49901`).
- Abrir arquivos ao tocar em caminhos citados em comentários de itens no mobile (`#49940`) e recolher comentários extensos com 'Show more' (`#49938`).
