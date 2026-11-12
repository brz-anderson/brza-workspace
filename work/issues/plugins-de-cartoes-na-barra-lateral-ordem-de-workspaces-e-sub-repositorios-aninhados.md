---
status: open
description: Os PRs #40597, #40604, #40603, #40334, #40323 trazem grupos em Pinned, Move to top, Workspaces antes de abas no Cmd+J e fixação de projetos.
scope:
  - brza-studio
  - workspace
priority: high
opened: 2026-11-03
tags:
  - design
  - tooling
---

# Plugins de cartões na barra lateral, ordem de workspaces e sub-repositórios aninhados

<!-- pln-014-despacho -->
> **Despacho (PLN-014/R1.1):** classe `ausente` · casa `studio`
> Merge no upstream não muda `status`. PLN-014/R1, 2026-11-12.

Rastreado dos PRs abertos no upstream [`stablyai/orca#40597`](https://github.com/stablyai/orca/pull/40597) (fecha Issue [`#39620`](https://github.com/stablyai/orca/issues/39620)),
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

## O que fazer

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
