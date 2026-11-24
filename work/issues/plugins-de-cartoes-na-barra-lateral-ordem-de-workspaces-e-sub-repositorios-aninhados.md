---
status: open
description: Ritmo do App Rail (#48049/#48084), draft guard em plugins (#48176/#48075), popover na status bar (#48088) e bot sidebar (#48132/#48020).
scope:
  - brza-studio
  - workspace
priority: high
opened: 2026-11-03
tags:
  - design
  - tooling
references:
  - https://github.com/stablyai/orca/pull/44653
  - https://github.com/stablyai/orca/pull/42558
  - https://github.com/stablyai/orca/pull/48212
  - https://github.com/stablyai/orca/pull/48258
  - https://github.com/stablyai/orca/pull/41896
  - https://github.com/stablyai/orca/issues/48264
  - https://github.com/stablyai/orca/pull/48049
  - https://github.com/stablyai/orca/pull/48084
  - https://github.com/stablyai/orca/pull/48045
  - https://github.com/stablyai/orca/pull/48176
  - https://github.com/stablyai/orca/issues/48075
  - https://github.com/stablyai/orca/issues/48088
  - https://github.com/stablyai/orca/issues/48132
  - https://github.com/stablyai/orca/issues/48020
  - https://github.com/stablyai/orca/pull/48157
  - https://github.com/stablyai/orca/pull/48127
  - https://github.com/stablyai/orca/pull/48061
  - https://github.com/stablyai/orca/pull/48003
  - https://github.com/stablyai/orca/pull/47935
  - https://github.com/stablyai/orca/pull/47922
  - https://github.com/stablyai/orca/pull/47902
  - https://github.com/stablyai/orca/pull/47968
  - https://github.com/stablyai/orca/pull/47871
  - https://github.com/stablyai/orca/issues/47693
  - https://github.com/stablyai/orca/issues/46796
  - https://github.com/stablyai/orca/issues/47862
  - https://github.com/stablyai/orca/commit/2f31a354146
  - https://github.com/stablyai/orca/commit/84cd9c16126
---

# Plugins de cartões na barra lateral, ordem de workspaces e sub-repositórios aninhados

<!-- pln-014-despacho -->
> **Despacho (PLN-014/R1.1):** classe `ausente` · casa `studio`
> Merge no upstream não muda `status`. PLN-014/R1, 2026-11-12.

Rastreado dos PRs abertos no upstream [`stablyai/orca#47935`](https://github.com/stablyai/orca/pull/47935),
[`stablyai/orca#47922`](https://github.com/stablyai/orca/pull/47922),
[`stablyai/orca#47902`](https://github.com/stablyai/orca/pull/47902),
[`stablyai/orca#47968`](https://github.com/stablyai/orca/pull/47968),
[`stablyai/orca#47871`](https://github.com/stablyai/orca/pull/47871),
[`stablyai/orca#47915`](https://github.com/stablyai/orca/pull/47915) (commit `2f31a354146`),
[`stablyai/orca#47884`](https://github.com/stablyai/orca/pull/47884) (commit `84cd9c16126`),
além das issues [`stablyai/orca#47693`](https://github.com/stablyai/orca/issues/47693),
[`stablyai/orca#46796`](https://github.com/stablyai/orca/issues/46796),
[`stablyai/orca#47862`](https://github.com/stablyai/orca/issues/47862),
[`stablyai/orca#47805`](https://github.com/stablyai/orca/pull/47805) (resolve Issue [`#47776`](https://github.com/stablyai/orca/issues/47776)),
[`stablyai/orca#47750`](https://github.com/stablyai/orca/pull/47750),
[`stablyai/orca#47816`](https://github.com/stablyai/orca/pull/47816),
[`stablyai/orca#47743`](https://github.com/stablyai/orca/pull/47743),
[`stablyai/orca#47739`](https://github.com/stablyai/orca/pull/47739),
[`stablyai/orca#47683`](https://github.com/stablyai/orca/pull/47683),
[`stablyai/orca#47542`](https://github.com/stablyai/orca/pull/47542),
[`stablyai/orca#47249`](https://github.com/stablyai/orca/pull/47249),
[`stablyai/orca#47679`](https://github.com/stablyai/orca/pull/47679),
[`stablyai/orca#42658`](https://github.com/stablyai/orca/pull/42658) (resolve Issue [`#42657`](https://github.com/stablyai/orca/issues/42657)),
[`stablyai/orca#42638`](https://github.com/stablyai/orca/pull/42638) (relacionado a [`#42637`](https://github.com/stablyai/orca/issues/42637)),
[`stablyai/orca#42558`](https://github.com/stablyai/orca/pull/42558) (relacionado a [`#41707`](https://github.com/stablyai/orca/issues/41707) e [`#28300`](https://github.com/stablyai/orca/issues/28300)),
[`stablyai/orca#42085`](https://github.com/stablyai/orca/pull/42085) (resolve Issue [`#42080`](https://github.com/stablyai/orca/issues/42080)),
[`stablyai/orca#42057`](https://github.com/stablyai/orca/pull/42057),
[`stablyai/orca#42068`](https://github.com/stablyai/orca/pull/42068),
[`stablyai/orca#40597`](https://github.com/stablyai/orca/pull/40597) (fecha Issue [`#39620`](https://github.com/stablyai/orca/issues/39620)),
[`stablyai/orca#40604`](https://github.com/stablyai/orca/pull/40604) (resolve Issue [`#40392`](https://github.com/stablyai/orca/issues/40392)),
[`stablyai/orca#40603`](https://github.com/stablyai/orca/pull/40603) (resolve Issue [`#40397`](https://github.com/stablyai/orca/issues/40397)),
[`stablyai/orca#40334`](https://github.com/stablyai/orca/pull/40334) (resolve Issue [`#40333`](https://github.com/stablyai/orca/issues/40333)),
[`stablyai/orca#40323`](https://github.com/stablyai/orca/pull/40323) (resolve Issue [`#40322`](https://github.com/stablyai/orca/issues/40322)),
[`stablyai/orca#40023`](https://github.com/stablyai/orca/pull/40023),
[`stablyai/orca#40004`](https://github.com/stablyai/orca/pull/40004),
[`stablyai/orca#39542`](https://github.com/stablyai/orca/pull/39542) (resolve Issue [`#39541`](https://github.com/stablyai/orca/issues/39541)),
[`stablyai/orca#39538`](https://github.com/stablyai/orca/pull/39538) (Issue [`#39537`](https://github.com/stablyai/orca/issues/39537)),
[`stablyai/orca#39532`](https://github.com/stablyai/orca/pull/39532) (resolve Issue [`#39531`](https://github.com/stablyai/orca/issues/39531)),
[`stablyai/orca#39490`](https://github.com/stablyai/orca/pull/39490),
[`stablyai/orca#39588`](https://github.com/stablyai/orca/pull/39588) (resolve Issue [`#39584`](https://github.com/stablyai/orca/issues/39584)),
[`stablyai/orca#39582`](https://github.com/stablyai/orca/pull/39582) (resolve Issue [`#39573`](https://github.com/stablyai/orca/issues/39573)),
[`stablyai/orca#39559`](https://github.com/stablyai/orca/pull/39559) (resolve Issue [`#39549`](https://github.com/stablyai/orca/issues/39549)),
[`stablyai/orca#39100`](https://github.com/stablyai/orca/pull/39100) (resolve Issue [`#38617`](https://github.com/stablyai/orca/issues/38617)),
[`stablyai/orca#39080`](https://github.com/stablyai/orca/pull/39080),
[`stablyai/orca#39081`](https://github.com/stablyai/orca/pull/39081),
[`stablyai/orca#38588`](https://github.com/stablyai/orca/pull/38588) (Issue [`#38586`](https://github.com/stablyai/orca/issues/38586)),
[`stablyai/orca#38634`](https://github.com/stablyai/orca/pull/38634),
[`stablyai/orca#38561`](https://github.com/stablyai/orca/pull/38561),
[`stablyai/orca#38518`](https://github.com/stablyai/orca/pull/38518),
[`stablyai/orca#38378`](https://github.com/stablyai/orca/pull/38378),
[`stablyai/orca#38334`](https://github.com/stablyai/orca/pull/38334) (Issue [`#38318`](https://github.com/stablyai/orca/issues/38318)),
[`stablyai/orca#38367`](https://github.com/stablyai/orca/pull/38367),
[`stablyai/orca#38281`](https://github.com/stablyai/orca/pull/38281),
[`stablyai/orca#38282`](https://github.com/stablyai/orca/pull/38282) (Issue [`#38277`](https://github.com/stablyai/orca/issues/38277)),
[`stablyai/orca#38296`](https://github.com/stablyai/orca/pull/38296) (Issue [`#38249`](https://github.com/stablyai/orca/issues/38249)),
[`stablyai/orca#38168`](https://github.com/stablyai/orca/pull/38168) (Issue [`#38138`](https://github.com/stablyai/orca/issues/38138)),
[`stablyai/orca#38193`](https://github.com/stablyai/orca/pull/38193) (Issue [`#38134`](https://github.com/stablyai/orca/issues/38134)),
[`stablyai/orca#38208`](https://github.com/stablyai/orca/pull/38208),
[`stablyai/orca#38118`](https://github.com/stablyai/orca/pull/38118) (Issue [`#8766`](https://github.com/stablyai/orca/issues/8766)),
[`stablyai/orca#38089`](https://github.com/stablyai/orca/pull/38089),
[`stablyai/orca#38092`](https://github.com/stablyai/orca/pull/38092),
[`stablyai/orca#38078`](https://github.com/stablyai/orca/pull/38078),
[`stablyai/orca#38049`](https://github.com/stablyai/orca/pull/38049),
[`stablyai/orca#37650`](https://github.com/stablyai/orca/pull/37650),
[`stablyai/orca#37654`](https://github.com/stablyai/orca/pull/37654),
[`stablyai/orca#37661`](https://github.com/stablyai/orca/pull/37661),
[`stablyai/orca#37664`](https://github.com/stablyai/orca/pull/37664),
[`stablyai/orca#37696`](https://github.com/stablyai/orca/pull/37696),
[`stablyai/orca#37730 (MERGED no upstream; não está no fork)`](https://github.com/stablyai/orca/pull/37730),
[`stablyai/orca#37557`](https://github.com/stablyai/orca/pull/37557) e
[`stablyai/orca#37510`](https://github.com/stablyai/orca/pull/37510), além das issues
[`#39086`](https://github.com/stablyai/orca/issues/39086),
[`#38550`](https://github.com/stablyai/orca/issues/38550),
[`#38361`](https://github.com/stablyai/orca/issues/38361),
[`#38214`](https://github.com/stablyai/orca/issues/38214),
[`#38112`](https://github.com/stablyai/orca/issues/38112),
[`#38017`](https://github.com/stablyai/orca/issues/38017),
[`#42632`](https://github.com/stablyai/orca/issues/42632),
[`#18401`](https://github.com/stablyai/orca/issues/18401),
[`#15323`](https://github.com/stablyai/orca/issues/15323) e
[`#37761`](https://github.com/stablyai/orca/issues/37761).

## O que está entrando no upstream

1. **Exposição de timestamps de criação e atividade na API de plugins (`#39100`, resolve `#38617`):**
   - Os registros retornados por `workspace.list` passam a incluir `createdAt` e `lastActivityAt` (em milissegundos epoch);
   - Permite que plugins e automações identifiquem workspaces antigos, inativos ou abandonados para higienização programática
     sem depender de scripts auxiliares de terminal.
2. **Opção para ocultar projetos e grupos vazios na barra lateral (`#39080`):**
   - Adiciona configuração para recolher ou omitir automaticamente pastas de projetos e agrupamentos que não possuam
     worktrees ativos ou abas abertas, limpando a árvore de navegação.
3. **Indicador de estado visual com cor no ícone do Linear (`#39081`):**
   - Renderiza a cor de status da issue do Linear diretamente no ícone correspondente na barra lateral e nos cartões de tarefas.
4. **Resolução de sessões de folder-workspaces no filtro Projects do Search Palette (`#39086`):**
   - Corrige falha onde selecionar o filtro de projeto na paleta de busca ocultava indevidamente sessões pertencentes a
     workspaces do tipo pasta multirrepositório.
5. **Menu de ações diretas na linha de agentes da barra lateral (`#38588`, `#38586`):**
   - Adiciona menu contextual acessível em cada linha compacta de agente nos cartões de workspace:
     - **Rename:** renomeia a sessão ativa do agente no próprio local;
     - **Continue in Terminal:** bifurca/continua a sessão estruturada em uma nova aba de terminal;
     - **Copy Session ID:** copia o identificador interno da sessão do provedor;
     - **Close:** encerra a sessão e fecha a aba correspondente sem precisar localizá-la e ativá-la na barra superior.
6. **Ações para colapsar e expandir todos os projetos (`#38634`):**
   - Adiciona controles globais no cabeçalho da barra lateral para recolher ou expandir simultaneamente todos os agrupamentos
     de projetos e seus respectivos worktrees.
7. **Botão de criação "+" ao lado do título do workspace na sidebar (`#38561`):**
   - Adiciona botão acessível "New tab" ao lado do nome do workspace nos cartões da barra lateral, abrindo o mesmo
     `WorkspaceCreateMenu` disponível na barra de abas superior.
8. **Preservação do nome real da sessão do agente em abas de terminal (`#38518`):**
   - Unifica a hierarquia de nomes de abas (`resolveTabNameSource`): renomeação manual → nome de comando rápido → título
     ao vivo do OpenCode → nome próprio da sessão do agente → título gerado pelo primeiro prompt.
9. **Opção para ocultar chip de projeto em cartões fixados da sidebar (`#38550`):**
   - Proposta para permitir ocultar o badge redundante de projeto em cartões de workspace fixados.
10. **Preservação de workspaces de servidor aninhados após reinício (`#38378`):**
    - Garante que a estrutura aninhada de workspaces em servidores remotos permaneça preservada e visível na hierarquia correta.
11. **Atualização e integridade de alterações em submódulos Git (`#38334`, `#38318`):**
    - Corrige bug onde diffs e árvores de alterações em submódulos expandidos ficavam obsoletos ou vazios na exibição da sidebar.
12. **Destaque visual para o chat focado nas linhas de agentes (`#38367`):**
    - Destaca graficamente a linha do chat ativo dentro dos cartões de workspace da barra lateral.
13. **Opção de ocultar worktree principal na barra lateral (`#38361`):**
    - Proposta para permitir manter o worktree primário fora da lista da sidebar em projetos focados exclusivamente em worktrees de feature.
14. **Limpeza de workspaces inativos e indicador de repositório (`#38281`):**
    - Interface aprimorada para limpeza em lote e indicador visual de repositório de origem.
15. **API com permissão para aparência dinâmica desktop de plugins (`#38282`, `#38277`):**
    - Expõe endpoint controlado por permissões para que plugins ajustem elementos de UI no app desktop.
16. **Fallback com detecção de conteúdo binário para editores (`#38296`, `#38249`):**
    - Detecção prévia de arquivos binários acionando fallback em editores customizados de plugins.
17. **Ações de colapso e expansão em massa de workspaces (`#38168`, resolve `#38138`):**
    - "Collapse all" e "Expand all" no menu de opções de workspaces e atalho configurável.
18. **Dashboard Global Home (`#38193`, resolve `#38134`):**
    - Visão consolidada da frota de agentes e limites de uso em um único painel.
19. **Preservação de worktrees ocultos ao adicionar projetos (`#38208`):**
    - Garante que worktrees explicitamente ocultados permaneçam ocultos.
20. **Criação de grupos de projeto vazios na sidebar e CLI (`#38214`, `#38118`):**
    - Subcomando `orca project-group create` e menu de contexto.
21. **Criação de folder workspaces via CLI (`#38112`):**
    - Proposta para `orca workspace create --folder <path>`.
22. **Cabeçalho compacto opcional em cartões de workspace (`#39542`, resolve `#39541`):**
    - Introduz o preset de layout "Compact header" em Workspace options -> Card layout. Condensa o nome do branch, contagem/disclosure
      de agentes e ação direta de trabalho vinculado em uma única linha de título, economizando 66px verticais por cartão.
23. **Indentação de linhas sob seções de host remoto (`#39538`, `#39537`):**
    - Indenta visualmente os cartões de workspace pertencentes a hosts remotos ou pareados sob suas respectivas seções de host,
      melhorando a hierarquia visual na barra lateral.
24. **Preservação de grupos colapsados sob a seção de host correta (`#39532`, resolve `#39531`):**
    - Corrige bug de ordenação visual onde grupos de projetos colapsados saltavam para o topo da lista acima das seções de host.
25. **Desduplicação de projetos compartilhados nos filtros da barra lateral (`#39588`, resolve `#39584`):**
    - Evita que um projeto compartilhado entre múltiplos hosts apareça duplicado na lista de filtros da barra lateral,
      agrupando checkouts por projeto e omitindo entradas redundantes.
26. **Exibição contínua de status de PR em cartões de workspaces adormecidos (`#39582`, `#39583`, resolve `#39573`):**
    - Mantém o badge e indicador de status do Pull Request visíveis mesmo quando o workspace está em repouso (*sleeping*).
27. **Atenuação visual de contadores de referências vinculadas (`#39559`, resolve `#39549`):**
    - Reduz o tamanho e brilho excessivo dos contadores de referências e tarefas vinculadas nos cartões de workspace.
28. **Deduplicação de repositórios placeholder em sessões offline (`#39490`):**
    - Durante a hidratação de sessões enquanto o host remoto está desconectado, o app sintetizava repositórios placeholder duplicados
      para o mesmo diretório caso houvesse discrepância de IDs;
    - O PR `#39490` casa repositórios pelo caminho normalizado (`normalizeRuntimePathForComparison`) no mesmo host, consolidando worktrees
      sob uma única entrada na barra lateral.
29. **Ocultação indevida de worktrees remotos por filtro local de repo-id (`#18401`):**
    - O filtro `filterRepoIds` aplicava checagens restritas ao catálogo local, ocultando todos os worktrees situados em hosts remotos pareados
      e corrompendo a reordenação por arrasto quando grupos de worktrees fixados estavam ativos.
30. **Menus de app nos popouts da barra de trilho e configuração de estilo de barra lateral (`#40004`):**
    - Popouts abertos a partir da barra de trilho (*rail popouts*) passam a renderizar menus nativos da aplicação;
    - Introduz configuração de estilo visual da barra lateral (`sidebarStyle`), permitindo customizar densidade e aparência da árvore.
31. **Agrupamento explícito por host na barra lateral (`#40023`):**
    - Adiciona a opção "Group by: Host" nos controles da barra lateral, permitindo alternar entre agrupamento explícito por máquina e visão de lista única.
32. **Fixação persistente de projetos e grupos (`isPinned`) e ordenação intercalada (`#40334`, resolve `#40333`):**
    - Adiciona a propriedade persistida `isPinned` em `Repo` e `ProjectGroup`, permitindo fixar projetos, grupos e subgrupos no topo do seu respectivo nível na sidebar;
    - Mantém os itens fixados ancorados no topo tanto no modo de ordenação manual quanto por atividade recente (*Recent*);
    - Permite intercalar livremente a ordenação manual entre subgrupos e projetos irmãos dentro de um grupo expandido, sem travar subgrupos rigidamente no topo.
33. **Criação direta de grupos/subgrupos, menu hierárquico de reparenting e drag-and-drop transversal (`#40323`, resolve `#40322`):**
    - Adiciona botão `NewProjectGroupButton` na barra de ferramentas da sidebar para criar grupos raiz vazios;
    - Adiciona opção `New subgroup` e menu de reparenting hierárquico indentado `Move to group` com filtro anti-ciclo;
    - Permite arrastar e soltar projetos e grupos entre diferentes grupos, subgrupos e nível raiz, com cálculo geométrico real de linhas indicadoras de soltura (*drop indicators*).
34. **Grupos nomeados e colapsáveis na seção Pinned (`#40597`, fecha `#39620`):**
    - Permite organizar worktrees fixados em grupos nomeados na seção Pinned (`pinnedGroups`, `pinnedGroupByWorktreeIdentity`);
    - Menus de contexto de cartões fixados ganham "Add to group → New group…" e movimentação entre grupos ou retorno a pinos avulsos;
    - Grupos podem ser renomeados, movidos ou removidos sem desafixar seus workspaces, e o estado de colapso é preservado entre sessões com qualificação por host.
35. **Ação "Move to top" no menu de cabeçalho de projetos (`#40604`, resolve `#40392`):**
    - Adiciona o item "Move to top" ao menu "…" do cabeçalho de projetos, movendo instantaneamente o projeto para o topo da lista raiz ou do seu grupo sem necessidade de arrasto manual longo;
    - Desabilitado quando o item já é o primeiro da lista, reutilizando o fluxo consolidado de ordenação e persistência do drag commit.
36. **Workspaces à frente de abas abertas na busca digitada da Jump Palette (`#40603`, resolve `#40397`):**
    - Ao digitar qualquer busca no Cmd+J, a seção de Workspaces é sempre posicionada antes de Open Tabs (`!hasQuery`), facilitando o retorno rápido a workspaces (inclusive suspensos) com destaque e navegação por teclado instantâneos.
37. **Painéis de plugins como páginas de navegação principal da sidebar (`#42085`, resolve `#42080`):**
    - Permite que plugins registrem uma entrada na barra de navegação superior esquerda (ao lado de Tasks, Automations e Orca Mobile), abrindo o painel em largura total como página dedicada em vez de aba secundária na barra lateral direita.
38. **Editores customizados de plugins em abas de diff de arquivo único (`#42057`):**
    - Permite que arquivos tratados por plugins (ex.: diagramas BPMN, esquemas de dados, mockups) ofereçam sua própria visualização gráfica de diff diretamente na aba de comparação de alterações do Source Control, lado a lado com o diff textual padrão.
39. **Popovers de plugins pertencentes ao host na barra de status (`#42068`):**
    - Proposta de RFC para que plugins declarem itens interativos de status bar cujos dados e popovers pertençam ao daemon do host onde o workspace executa.
40. **Ícones SVG customizados para painéis de plugins e herança tipográfica (`#42558`, `#42575`):**
    - Permite que painéis de plugins utilizem arquivos SVG relativos ao plugin como ícone da activity-bar; o host valida os arquivos de tamanho delimitado e os serve com restrição de segurança, desenhando-os na sidebar como máscara monocromática com fallback gracioso;
    - Propaga a família tipográfica do Studio para os frames dos plugins através da variável CSS `--orca-font-family`.
41. **Preservação de extensões de arquivos não salvos de plugins no primeiro salvamento (`#42658`, resolve `#42657`):**
    - Garante que arquivos gerados dinamicamente por plugins (como `.excalidraw` ou diagramas) mantenham sua extensão correta no diálogo inicial de "Save as", impedindo regressão indesejada para texto plano `.txt`.
42. **Persistência de painéis de plugins ativos em background na sidebar (`#42632`):**
    - Mantém painéis de plugins que reproduzem mídia ou realizam tarefas contínuas vivos em segundo plano mesmo quando outra aba da sidebar for ativada, prevenindo interrupção de reprodução de mídia.
43. **Coexistência de subpastas `source.path` e hooks de worker em plugins (`#42638`, relacionado a `#42637`):**
    - Estabiliza a resolução de caminhos de arquivos em plugins que combinam subpastas customizadas de código com ganchos de execução assíncrona em workers.
44. **Preservação da visibilidade do workspace ativo ao alternar workspaces suspensos (`#47683`):**
    - Ao alternar "Toggle Sleeping Workspaces", a inclusão de linhas acima do workspace ativo o empurrava para fora do campo visual devido à ancoragem de scroll no topo;
    - A sidebar agora revela o workspace ativo via virtualizador, rolando suavemente apenas o necessário para mantê-lo visível na tela, inclusive em workspaces remotos SSH.
45. **Resolução de grafia canônica de `gitdir` em volumes case-insensitive (`#47542`):**
    - Em volumes como macOS APFS e Windows NTFS, `git rev-parse --show-toplevel` retorna a grafia em disco (ex.: `My-Repo/my-task`), enquanto `git worktree list` retorna a grafia registrada no Git (`my-repo/my-task`);
    - O binding de terminais abertos por `worker-start` lia o toplevel, causando desencontro de ID no registro da sidebar e deixando worktrees órfãos. Agora o sistema lê o backlink em `.git/worktrees/<name>/gitdir` e adota a grafia canônica do Git.
46. **Estabilização de rescans em repositórios massivos com listagem de worktrees lenta (`#47249`):**
    - A janela de frescor do catálogo iniciava no começo da varredura, tornando-o obsoleto logo na chegada se a listagem fosse lenta e forçando re-varreduras contínuas; agora a janela de frescor é calculada a partir da conclusão da varredura, e leituras durante a atualização respondem das linhas publicadas anteriormente em background.
47. **Tratamento definitivo de chats de projetos removidos como `agent_session_workspace_removed` (`#47679`):**
    - Ao tentar revelar um chat cujo projeto foi excluído do app, a recusa retornava como erro desconhecido exibindo "Retry in a moment" indefinidamente. Agora a sessão reporta `agent_session_workspace_removed`, informando claramente no desktop e mobile que o projeto foi removido.
48. **Quebra de linha para erros longos de Git no card do Source Control (`#47805`, resolve `#47776`):**
    - Quando o Git falha ao ler um workspace (ex.: "Branch compare failed"), paths ou hashes longos no erro bruto excediam a largura da sidebar e empurravam todo o painel horizontalmente, cortando a caixa de commit e botões de ação;
    - O PR `#47805` aplica quebra de linha de emergência (`break-all` / `whitespace-pre-wrap`) no texto do erro dentro do card, mantendo o painel de Source Control contido na largura correta da sidebar.
49. **Contenção de foco no diálogo de branch após resultado de nome mantido (`#47750`):**
    - Quando o diálogo de auto-name de branch exibia "Branch name kept", devolvia o foco do teclado para o botão de fechar. Se outro modal estivesse sobreposto com foco ativo, o hand-back transferia o foco indevidamente para o botão de fechar do outro diálogo;
    - O PR `#47750` restringe a devolução de foco estritamente aos nós descendentes do próprio diálogo de branch.
50. **Aninhamento hierárquico de grupos de projetos via drag-and-drop e menu de contexto (`#47816`):**
    - Permite aninhar grupos de projetos dentro de outros grupos na sidebar soltando o cabeçalho de um grupo sobre outro ou selecionando o destino no menu de contexto do grupo ("Move to group"), com cálculo de prevenção de dependência cíclica.
51. **Contagem visível de Bots e Projetos nos cabeçalhos da sidebar (`#47743`, fecha `#47747`):**
    - Os cabeçalhos de seção da sidebar passam a exibir contadores numéricos imediatos no formato "Bots (4)" e "Projects (2)", lendo diretamente as coleções reativas de bots e repositórios sem duplicar estado na memória nem computar overhead em segundo plano.
52. **Revelação e rastreamento automático do arquivo ativo no File Explorer (`#47739`):**
    - Introduz a configuração `explorerRevealActiveFile` (default `true`) sob Settings → Appearance → Window & sidebar → Advanced → File explorer;
    - Rastreia automaticamente abas de arquivos ativas em modos `edit`, `markdown-preview` e `diff` de arquivo único, expandindo nós ancestrais colapsados, resetando escopos de pasta se o arquivo estiver fora do display root atual, aplicando seleção visível com `bg-accent text-accent-foreground` e rolando até a linha sem flash âmbar;
    - Preserva seleções manuais enquanto o mesmo arquivo permanecer ativo e adiciona o comando `fileExplorer.revealActiveFile` ("Reveal Active File in Explorer") na Command Palette.
53. **Espaçamento e dimensões desproporcionais dos botões no App Rail (`#47915`, commit `2f31a354146`):**
    - O trilho de aplicativos (App Rail) exibia botões grandes que consumiam espaço horizontal; o commit reduz os botões para 28px com ícones compactos de 16px, otimizando a área da janela.
54. **Ausência de status visível em bots quando a seção da sidebar está colapsada (`#47884`, commit `84cd9c16126`, e `#47693`):**
    - Quando a seção Bots na barra lateral era recolhida, os avatares dos bots não exibiam dicas de status ou badges "Needs you", deixando o operador sem retorno visual sobre atenções pendentes.
55. **Comportamento inesperado do atalho de exclusão na barra lateral sem item selecionado (`#47935`):**
    - Ao acionar a tecla Delete/Backspace com o foco na barra lateral mas sem nenhum item selecionado na lista, a ação de exclusão não atuava sobre o workspace aberto, deixando o desenvolvedor sem resposta de UI.
56. **Abertura de caminhos absolutos no worktree incorreto via CLI (`#47922`):**
    - Ao invocar a CLI com caminho absoluto de arquivo, o app abria o arquivo no worktree genérico em foco em vez do worktree que realmente continha aquele caminho no disco.
57. **Seção Bots densa e verticalmente longa sem suporte a colunas paralelas (`#47902`):**
    - Bots fixados ocupavam uma única coluna vertical densa na barra lateral, forçando rolagem vertical excessiva; o PR introduz disposição em duas colunas para bots fixados.
58. **Desatualização de status de PR de workspaces fora da linha da barra lateral (`#47968`):**
    - Quando o status de PR de um workspace era consultado fora de sua linha direta na sidebar (ex.: em diálogos ou popovers), o cache mantinha dados defasados sem refresh adequado.
59. **Baixo contraste entre aba ativa e abas inativas (`#47871`):**
    - A distinção visual entre a aba em primeiro plano e as demais abas no topo do painel apresentava baixo contraste de cores, dificultando a identificação imediata da aba focada.
60. **Badges de projeto ausentes ou não configuráveis na barra lateral (`#44653`, commit `28dfb5df111`):**
    - A lista de projetos na barra lateral não permitia vincular badges contextuais de status ou contadores customizados, dificultando a identificação imediata de repositórios com pendências críticas.
61. **Ícones SVG inline ausentes para painéis e extensões de plugins (`#42558`, commit `29827448c5f`):**
    - Plugins não podiam injetar seus próprios ícones vetoriais SVG inline na barra de atividades e nos painéis da barra lateral, ficando limitados aos ícones pré-definidos do sistema.
62. **Falta de aviso contextual quando um quadro/board da sidebar é movido (`#48212`):**
    - Ao reorganizar visualmente boards de tarefas ou painéis de automação na barra lateral, os usuários perdiam a localização do painel sem uma dica explicativa de redirecionamento (*sidebar board moved hint*).
63. **Falta de foco explícito no painel ao alternar abas da barra de abas (`#48258`):**
    - Clicar em uma aba na tab-strip ativava a visão gráfica mas não transferia o foco de entrada de teclado para o container do painel correspondente, exigindo um clique adicional para começar a digitar.
64. **Extravasamento e corte de abas em painéis estreitos com múltiplas abas abertas (`#41896`):**
    - Quando múltiplos painéis verticais eram divididos, painéis estreitos exibiam abas comprimidas sem modo condensado legível, ocultando títulos e status.
65. **Truncamento de texto sem tooltip/hover com conteúdo completo (`#48264`):**
    - Componentes de texto truncado por reticências na sidebar e nos cartões de itens não exibiam o texto na íntegra ao passar o cursor do mouse (hover), impossibilitando a leitura de títulos longos.

## O que fazer

- Quebrar linhas de erros longos de Git dentro dos cards do Source Control para evitar extravasamento lateral da sidebar (`#47805`, resolve `#47776`).
- Conter a devolução de foco do teclado estritamente dentro do diálogo de branch (`#47750`).
- Permitir aninhar grupos de projetos via drag-and-drop e menu de contexto com prevenção de ciclos (`#47816`).
- Exibir contadores de bots e projetos nos cabeçalhos da barra lateral (`#47743`, fecha `#47747`).
- Implementar revelação automática do arquivo ativo no File Explorer (`explorerRevealActiveFile`) e comando de revelação manual (`#47739`).
- Reter o workspace ativo na visão da sidebar através do virtualizador ao exibir/ocultar workspaces suspensos (`#47683`).
- Adotar a grafia canônica de `.git/worktrees/<name>/gitdir` em volumes case-insensitive para prevenir worktrees órfãos (`#47542`).
- Calcular a janela de frescor de repositórios a partir do término do scan e responder do cache durante atualizações em background (`#47249`).
- Reportar `agent_session_workspace_removed` e mensagem clara para chats de projetos removidos (`#47679`).
- Preservar a extensão correta de arquivos de plugins no primeiro salvamento (`#42658`, resolve `#42657`).
- Manter a execução de painéis de plugins em background na alternância de abas da sidebar (`#42632`).
- Suportar subpastas `source.path` e hooks de workers em plugins (`#42638`, `#42637`).
- Suportar ícones SVG customizados na activity-bar para painéis de plugins e herança de fonte (`#42558`, `#42575`).
- Suportar abertura de painéis de plugins como páginas dedicadas na navegação principal (`#42085`, resolve `#42080`).
- Oferecer editores customizados de plugins em abas de diff de arquivo único no Source Control (`#42057`).
- Avaliar a especificação de status-bar popovers pertencentes ao host para plugins (`#42068`).
- Adotar grupos nomeados e colapsáveis para workspaces na seção Pinned (`#40597`).
- Adicionar o atalho/ação "Move to top" no menu de cabeçalho de projetos (`#40604`).
- Posicionar Workspaces à frente de Open Tabs na busca digitada da Jump Palette (`#40603`).
- Adotar a deduplicação de repositórios placeholder offline por caminho normalizado (`#39490`).
- Corrigir o escopo de `filterRepoIds` para preservar worktrees de hosts remotos pareados (`#18401`).
- Adotar o layout opcional "Compact header" nos cartões de workspace (`#39542`), reduzindo a rolagem vertical na sidebar.
- Incorporar as correções de indentação por host (`#39538`) e ordenação de grupos colapsados (`#39532`).
- Aplicar a desduplicação de filtros de projeto (`#39588`) e a visibilidade de PRs em workspaces em repouso (`#39582`).
- Adotar a exposição de `createdAt` e `lastActivityAt` na API de plugins (`#39100`) para suportar métricas do `brza-workflow`.
- Implementar as opções de ocultar projetos vazios (`#39080`) e o menu contextual de ações de agentes na sidebar (`#38588`).
- Adicionar os controles de colapso e expansão em massa de projetos (`#38634`).
- Incorporar o botão de novo item "+" nos cartões de workspace (`#38561`) e a resolução de títulos (`#38518`).
- Adotar a configuração de estilo de barra lateral (`sidebarStyle`) e menus nativos em popouts do rail (`#40004`).
- Integrar a opção de agrupamento explícito por host ("Group by: Host") na barra lateral (`#40023`).
- Adotar a fixação de projetos e grupos (`isPinned`) com ordenação intercalada de subgrupos e projetos (`#40334`).
- Integrar a criação direta de grupos/subgrupos na sidebar e arrasto reparenting transversal (`#40323`).
- Compactar os botões do App Rail para 28px com ícones de 16px (`#47915`).
- Exibir avatares recortados com dicas de status e destaque "Needs you" em bots com a seção colapsada (`#47884`, `#47693`).
- Aplicar a ação de exclusão da sidebar ao workspace aberto quando a lista focada não tiver seleção explícita (`#47935`).
- Abrir arquivos com caminho absoluto no worktree correto que contém o arquivo (`#47922`).
- Dispor bots fixados em duas colunas paralelas na barra lateral (`#47902`).
- Manter o status de PR atualizado quando consultado fora da linha da barra lateral (`#47968`).
- Aumentar o contraste visual da aba ativa em relação às demais abas (`#47871`).
- Ajustar o ritmo e espaçamento dos botões do App Rail (espaçamento inicial de 40px e gap refinado de 10px) (`#48049`, `#48084`).
- Permitir que destinos do App Rail ocupem a página inteira de forma fluida (`#48045`, commit `c363299cdac`).
- Confirmar fechamento de abas cujo editor customizado de plugin retém edições não salvas (`#48176`, resolve Issue `#48075`).
- Permitir que itens da barra de status de plugins abram painéis como popovers flutuantes (`#48088`).
- Exibir a descrição do bot abaixo do nome na barra lateral (`#48132`).
- Aprimorar visibilidade na barra lateral de bots para seleção ativa, tarefas concluídas e workers em background (`#48020`).
- Simplificar o cabeçalho do Bot Home com ações de topo condensadas (`#48157`).
- Refinar seletor de novos membros de grupos de bots (`#48127`, commit `737a50d831b`).
- Polir cabeçalho e chips de links de itens de trabalho (`#48061`).
- Exibir card de preview do GitHub ao passar o mouse sobre chip de PR ou issue do item (`#48003`, commit `212a1f746ee`).
- Adotar badges de status de projetos na barra lateral (`#44653`, commit `28dfb5df111`).
- Habilitar suporte a ícones vetoriais SVG inline para painéis de plugins (`#42558`, commit `29827448c5f`).
- Exibir dica contextual de reposicionamento quando um board da barra lateral for movido (`#48212`).
- Garantir que a alternância de abas na tab-strip transfira imediatamente o foco de entrada para o painel selecionado (`#48258`).
- Condensar o layout de abas em painéis estreitos preservando legibilidade (`#41896`).
- Exibir tooltip completo ao passar o cursor sobre textos truncados na interface (`#48264`).

