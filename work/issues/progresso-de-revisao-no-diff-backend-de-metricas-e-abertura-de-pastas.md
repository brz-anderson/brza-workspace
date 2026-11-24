---
status: open
description: Largura de Markdown (#48047/#48022), CRLF no Windows (#48122), skeletons em checks (#47812) e restauração de abas (#47262).
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

## O que o upstream implementa e corrige

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


