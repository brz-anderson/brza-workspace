---
status: open
description: Os PRs #43488, #43493, #43351, #43319 e as issues #43487, #43443, #43373 trazem nome do worktree no explorer, botões de novo arquivo/pasta e drive letters no WSL.
scope:
  - brza-studio
  - workspace
priority: high
opened: 2026-11-06
tags:
  - design
  - tooling
---

# Seletor de branches na status bar e suporte a workspaces em pastas multirrepositório

Rastreado dos PRs abertos no upstream [`stablyai/orca#43488`](https://github.com/stablyai/orca/pull/43488) (resolve Issue [`#43487`](https://github.com/stablyai/orca/issues/43487)),
[`stablyai/orca#43493`](https://github.com/stablyai/orca/pull/43493),
além da issue [`stablyai/orca#43443`](https://github.com/stablyai/orca/issues/43443),
[`stablyai/orca#43351`](https://github.com/stablyai/orca/pull/43351) (resolve Issue [`#43373`](https://github.com/stablyai/orca/issues/43373)),
[`stablyai/orca#43319`](https://github.com/stablyai/orca/pull/43319),
[`stablyai/orca#43171`](https://github.com/stablyai/orca/pull/43171),
[`stablyai/orca#43193`](https://github.com/stablyai/orca/pull/43193),
[`stablyai/orca#43244`](https://github.com/stablyai/orca/pull/43244),
[`stablyai/orca#43044`](https://github.com/stablyai/orca/pull/43044),
além das issues [`stablyai/orca#43384`](https://github.com/stablyai/orca/issues/43384),
[`stablyai/orca#43383`](https://github.com/stablyai/orca/issues/43383),
[`stablyai/orca#43157`](https://github.com/stablyai/orca/pull/43157) (resolve Issue [`#43156`](https://github.com/stablyai/orca/issues/43156)),
[`stablyai/orca#43121`](https://github.com/stablyai/orca/pull/43121),
[`stablyai/orca#43113`](https://github.com/stablyai/orca/pull/43113),
[`stablyai/orca#33600`](https://github.com/stablyai/orca/pull/33600),
[`stablyai/orca#41930`](https://github.com/stablyai/orca/pull/41930) (resolve Issue [`#41929`](https://github.com/stablyai/orca/issues/41929)),
[`stablyai/orca#39999`](https://github.com/stablyai/orca/pull/39999),
[`stablyai/orca#39977`](https://github.com/stablyai/orca/pull/39977),
[`stablyai/orca#39779`](https://github.com/stablyai/orca/pull/39779) (resolve Issue [`#39777`](https://github.com/stablyai/orca/issues/39777)),
[`stablyai/orca#39637`](https://github.com/stablyai/orca/pull/39637),
[`stablyai/orca#39575`](https://github.com/stablyai/orca/pull/39575),
[`stablyai/orca#39572`](https://github.com/stablyai/orca/pull/39572) (resolve Issue [`#39545`](https://github.com/stablyai/orca/issues/39545)),
[`stablyai/orca#39018`](https://github.com/stablyai/orca/pull/39018),
[`stablyai/orca#39000`](https://github.com/stablyai/orca/pull/39000) (resolve [`#38931`](https://github.com/stablyai/orca/issues/38931)),
[`stablyai/orca#38955`](https://github.com/stablyai/orca/pull/38955),
[`stablyai/orca#38869`](https://github.com/stablyai/orca/pull/38869),
[`stablyai/orca#38836`](https://github.com/stablyai/orca/pull/38836),
[`stablyai/orca#38831`](https://github.com/stablyai/orca/pull/38831),
[`stablyai/orca#38904`](https://github.com/stablyai/orca/pull/38904) e
[`stablyai/orca#38875`](https://github.com/stablyai/orca/pull/38875), além da issue
[`stablyai/orca#38830`](https://github.com/stablyai/orca/issues/38830).

## O problema

1. **Atrito ao configurar a localização de projetos em novos hosts (`#43157`, resolve `#43156`):**
   Ao vincular um projeto existente a um host pareado ou servidor SSH, o usuário precisava digitar manualmente o caminho do diretório ou navegar por uma janela genérica de seleção, mesmo quando já existiam checkouts válidos do repositório no host remoto.
2. **Ocultação e filtragem incorreta de folder workspaces na barra lateral (`#43121`, `#33600`):**
   Workspaces de pasta (*folder workspaces*) fixados com pin não eram destacados devidamente na barra lateral, e projetos distintos misturavam suas pastas de trabalho filhas sem aplicar a filtragem por projeto selecionado.
3. **Incapacidade de anexar worktrees existentes a folder workspaces via CLI (`#39018`):**
   Ao tentar anexar um worktree existente a um folder workspace pai com `orca worktree set --parent-worktree folder:<id>`,
   o comando era rejeitado ("Folder parents are accepted only by orca worktree create"). Além disso, rodar `--parent-worktree active`
   a partir do próprio terminal do folder workspace falhava com "No Orca-managed worktree contains the current directory".
4. **Colisão de sufixo numérico na criação sequencial de worktrees (`#39000`, resolve `#38931`):**
   O gerador automático de sufixos reciclava o número `-100` após `-99`, colidindo com branches locais já existentes e
   abortando a criação de novos worktrees com erro fatal.
5. **Falta de API protegida para remoção de branches locais integrados (`#38955`):**
   A limpeza automatizada de branches após merge exigia invocações diretas de git sem validação de checkout ou barreiras
   de integridade com worktrees ativos.
6. **Invisibilidade e atrito para alternar branches no desktop (`#38869`, `#38836`):**
   O nome do branch ativo não ficava exposto na barra de status inferior. Para trocar de branch no desktop, o desenvolvedor
   era forçado a abrir um terminal manual, pois a interface só oferecia opções de "criar novo worktree". Além disso, o
   cabeçalho do painel de Source Control não permitia alternar ou derivar branches no mesmo checkout, ignorando as novas
   validações de segurança introduzidas no upstream (`#38744`).
7. **Controle de versão cego em workspaces de pasta multirrepositório (`#38831`):**
   Ao abrir uma pasta que agrupa múltiplos repositórios ou worktrees vinculados (*folder workspace*), o painel de Source
   Control exibia apenas uma mensagem estática de "No Git repository found", obrigando o desenvolvedor a navegar para cada
   worktree filho individualmente para verificar alterações pendentes, diffs ou realizar commits.
8. **Ausência de aninhamento visual de workspaces sob pastas na sidebar e mobile (`#38904`, `#38875`):**
   Projetos multirrepositório não agrupavam seus worktrees filhos de maneira hierárquica na barra lateral do desktop nem
   no cliente móvel, poluindo a lista de workspaces planos.
9. **Ocultação indevida de workspace ao remover subdiretório `.git` aninhado (`#38830`):**
   A deleção acidental de um repositório `.git` aninhado desanexava todo o workspace pai e ocultava as abas de agentes ativos.
10. **Dificuldade de inicialização de worktrees em pastas multirrepositório vazias (`#39575`):**
    Ao abrir uma pasta com repositórios Git mas sem worktrees anexados, os painéis de Source Control, Attached Worktrees
    e PR Checks exibiam apenas mensagens estáticas de "No attached worktrees yet" sem ação para criar o primeiro checkout.
11. **Criação de árvores de pastas vazias com espaço inicial em repositórios (`#39572`, `#39545`):**
    Ao colar um caminho com espaço inicial (ex.: `" /Users/user/dev"`) nas configurações de Workspace Directory, o caminho não era
    sanitizado antes da validação. Como o Node `posix.isAbsolute` retorna `false` para caminhos iniciados por espaço, o Orca tratava a
    rota como relativa e criava pastas `" <repo>/ /Users/user/dev"` em todos os repositórios registrados.
12. **Incompatibilidade de seletores `path:` e `name:` com Folder Workspaces na CLI (`#39637`):**
    Agentes e comandos da CLI podiam referenciar folder workspaces apenas pelo identificador literal `folder:<id>`, pois seletores
    como `path:` e `name:` buscavam exclusivamente Git worktrees em repositórios. Além disso, o comando `worktree ps` unificava
    indevidamente linhas de workspaces com mesmo ID em hosts distintos (ex.: `local` e `ssh:server`).
13. **Ausência de Source Control de pastas multirrepositório no app mobile (`#39999`):**
    O cliente mobile não conseguia inspecionar status de controle de versão nem branches alterados em folder workspaces,
    restringindo a visualização de diffs e commits pendentes a repositórios Git isolados.
14. **Incapacidade de renomear projetos pelo menu da barra lateral (`#39977`):**
    Não havia ação rápida no cabeçalho de projetos na barra lateral para renomear projetos/workspaces de forma intuitiva,
    exigindo edições manuais em arquivos de configuração ou recadastramento.
15. **Janela em branco ao abrir workspace de outra branch pelo seletor de branches (`#41930`, resolve `#41929`):**
    Ao selecionar "Open workspace" para uma branch que pertencia a outro workspace cujas abas haviam sido fechadas, a ação
    invocava apenas a mutação interna `setActiveWorktree`. Como não passava pelo ciclo de ativação do usuário, a tela permanecia
    completamente em branco até o operador clicar manualmente na linha correspondente na barra lateral.
16. **Falta de identificação do worktree no cabeçalho do File Explorer (`#43488`, resolve `#43487`):**
    Ao navegar por múltiplos worktrees, o cabeçalho do explorador de arquivos mostrava apenas o nome da pasta raiz sem explicitar a qual branch ou worktree os arquivos abertos pertenciam.
17. **Ausência de botões rápidos de criação de arquivos e pastas no File Explorer (`#43443`):**
    A barra de ferramentas do explorador de arquivos não continha botões diretos "New File" e "New Folder", forçando o uso repetitivo do menu de contexto.
18. **Falha ao mover projetos sob letras de drive mapeadas no WSL (`#43493`):**
    Projetos salvos em caminhos mapeados por letras de drive no subsistema Linux falhavam ao serem movidos ou organizados por causa de discrepâncias na normalização de caminhos.

## O que o upstream implementa e corrige

- **Nome do worktree no cabeçalho do File Explorer (`#43488`, resolve `#43487`):**
  - Exibe o nome do worktree corrente no topo do painel do explorador de arquivos, facilitando a identificação imediata do contexto de branch ativo.
- **Botões "New File" e "New Folder" na barra do File Explorer (`#43443`):**
  - Adiciona botões de ação rápida para criação de novo arquivo e nova pasta na toolbar do explorador.
- **Movimentação de projetos em unidades de drive mapeadas no WSL (`#43493`):**
  - Trata caminhos com letras de unidade Windows mapeadas para o ambiente WSL na rotina de mover projetos.
- **Sugestão de checkouts existentes na definição de pasta de projeto (`#43157`, resolve `#43156`):**
  - Ao configurar a localização de um projeto em um host, inspeciona o sistema de arquivos e sugere checkouts Git existentes compatíveis com o repositório, permitindo vinculação imediata em 1 clique sem digitação de caminhos.
- **Exibição correta de folder workspaces pinados e filtragem por projeto (`#43121`, `#33600`):**
  - Mantém pastas fixadas visíveis no topo da seção de workspaces e filtra a árvore de pastas respeitando estritamente o projeto selecionado.
- **Recolhimento e ocultação de projetos movidos (`#43113`):**
  - Permite aos desenvolvedores colapsar e ocultar referências a projetos que foram movidos de caminho.
- **Resolução unificada de seletores para Worktrees e Folder Workspaces (`#39637`):**
  - Implementa `resolveWorkspaceCandidate` suportando `path:` e `name:` para pastas de trabalho, sob o opt-in `matchFolderWorkspaces`
    (capability `workspace-selector.folder-match.v1`) em `worktree.show`, `worktree.set` e `worktree.create`;
  - Trata colisões com `selector_ambiguous` discriminando tipo, host, caminho e seletor inequívoco (`identity:` para repositórios ou `folder:<id>`);
  - Diferencia checkouts em múltiplos hosts no `worktree ps`, compondo chaves por host + ID e mantendo atividades de PTY vinculadas ao host comprovado;
  - Traduz caminhos Linux de distribuições chamadoras no WSL para caminhos UNC armazenados para folder workspaces.
- **Criação rápida de worktrees em pastas vazias (`#39575`):**
  - Nos painéis de Source Control, Attached Worktrees e PR Checks de pastas sem worktrees anexados, lista os repositórios Git da pasta
    com botões diretos "Create worktree", criando o checkout nomeado com base na pasta sem sair do contexto;
  - Valida se o branch já existe no repositório antes de criar, abrindo o modal preenchido caso o nome esteja ocupado.
- **Sanitização estrita com `.trim()` em `workspaceDir` (`#39572`, resolve `#39545`):**
  - Aplica `.trim()` no input de configurações, no sanitizador IPC e em todas as rotas de resolução de base path de worktree,
    garantindo que espaços antes ou depois da barra não corrompam caminhos absolutos nem criem diretórios espúrios.
- **Anexação de worktrees existentes a Folder Workspaces (`#39018`):**
  - Habilita `orca worktree set --parent-worktree folder:<id>` para vincular worktrees preexistentes a uma pasta pai;
  - Resolve `--parent-worktree active`/`current` para a pasta pai do próprio terminal ou checkout envolvente;
  - Permite rodar `orca worktree create` sem `--repo` dentro do folder workspace listando interativamente os repositórios contidos na pasta;
  - Garante estritamente um único pai por worktree no banco persistente de workspaces.
- **Sufixo numérico inteligente para novos worktrees (`#39000`):**
  - Inicia a contagem automática de sufixos sempre acima do maior índice numérico já existente no repositório, eliminando colisões de branch.
- **Exclusão segura de branches locais integrados (`#38955`):**
  - Adiciona o subcomando `orca repo delete-branch` com validação de commit integrado, verificação de branch protegido e cerca transacional (*mutation fence*).
- **Segmento de branch interativo na Status Bar (`#38869`):**
  - Adiciona o componente `BranchStatusSegment` no canto inferior esquerdo da barra de status com popover pesquisável e fetch em background.
- **Alternância e derivação de branches no Source Control (`#38836`):**
  - Transforma o cabeçalho do Source Control (`⎇ main ▾`) em um seletor para trocar, derivar ou navegar entre checkouts.
- **Source Control multinível para Folder Workspaces (`#38831`):**
  - Renderiza seções colapsáveis por worktree no Source Control de pastas multirrepositório.
- **Hierarquia de pastas e linhagem cross-machine (`#38904`, `#38875`):**
  - Aninha workspaces sob a pasta pai na barra lateral do desktop e mobile com resolução persistente na criação.
- **Busca combinada de projetos e hosts nos seletores de workspace (`#39779`, resolve `#39777`):**
  - Introduz o matcher compartilhado `project-host-query`, permitindo digitar `<host> <projeto>` nos drawers de seleção e no desktop.
- **Source Control de folder workspaces no cliente móvel (`#39999`):**
  - Expõe as alterações, diffs e arquivos modificados de projetos de pasta multirrepositório no aplicativo móvel.
- **Renomeação de projeto no menu do cabeçalho da barra lateral (`#39977`):**
  - Inclui a opção "Rename project" no menu de opções do cabeçalho de projeto da barra lateral.
- **Abertura de workspace pelo branch picker com reativação completa (`#41930`, resolve `#41929`):**
  - Assegura que a ação "Open workspace" reative abas e restaure processos em repouso.
- **Preservação de nomes de branch separados por barras (`#43171`):**
  - Mantém a integridade de nomes de branches que contêm barras (como `feature/nova-tela` ou `bugfix/auth/token`) na criação e chaveamento de workspaces, prevenindo sanitizações indevidas que achatavam ou corrompiam o nome no Git.
- **Opção para fixar novos workspaces diretamente na criação (`#43193`):**
  - Adiciona configuração e controle visual para definir novos workspaces como pinados automaticamente na barra lateral, agilizando o acesso a frentes de trabalho prioritárias.
- **Abertura contextual de seletor de projetos (`#43244`, `#43044`):**
  - O seletor de pastas de projetos passa a reabrir no último diretório navegado e adjacente ao projeto local mais recente, reduzindo cliques repetitivos.
- **Faixas visuais alternadas de projeto e densidade vertical compacta na sidebar (`#43351`, resolve Issue `#43373`):**
  - Implementa faixas sutis com sombreamento/cor alternada entre blocos de projetos vizinhos na barra lateral de worktrees, além de reduzir o padding vertical para acomodar mais workspaces visíveis na tela.
- **Preservação de título de primeira tarefa na barra lateral após renomeação de branch (`#43319`):**
  - Quando o branch de um worktree é renomeado, a barra lateral preserva o título da primeira tarefa resolvida em vez de regredir para rótulos genéricos.
- **Menu de contexto de projetos para criação direta de workspaces e suspensão em lote (`#43384`, `#43383`):**
  - Adiciona ao menu de clique direito do cabeçalho de projetos as ações "New workspace" e "Sleep all workspaces of project".

## O que fazer no BrzA Studio

1. Adotar faixas alternadas e densidade vertical compacta na barra lateral de worktrees (`#43351`, Issue `#43373`).
2. Preservar o título contextual na sidebar após renomeação de branch (`#43319`).
3. Adicionar opções de criação de workspace e suspensão de projeto em lote ao menu de contexto da sidebar (`#43384`, `#43383`).
4. Sugerir checkouts existentes ao configurar a localização de um projeto no host (`#43157`, resolve `#43156`).
5. Garantir renderização de folder workspaces fixados no topo da barra lateral e filtragem por projeto (`#43121`, `#33600`).
6. Preservar nomes de branches com barras no padrão Git em novos workspaces (`#43171`).
7. Oferecer a opção de pin automático de novos workspaces na criação (`#43193`).
8. Reabrir o seletor de pastas de projeto no último diretório e junto aos projetos recentes (`#43244`, `#43044`).
9. Adotar os comandos CLI de vinculação de worktrees a pastas (`#39018`), permitindo reorganizar worktrees sob pastas de projeto.
10. Incorporar a correção de sufixos numéricos (`#39000`) e a exclusão segura de branches (`#38955`).
11. Integrar o `BranchStatusSegment` na barra de status do `brza-studio` (`#38869`).
12. Adotar o botão "Create worktree" nos painéis vazios de pastas multirrepositório (`#39575`).
13. Aplicar sanitização e `.trim()` em todos os campos de diretório de workspace para evitar criação de pastas acidentais (`#39572`).
14. Suportar seletores unificados `path:` e `name:` para folder workspaces na CLI e separar instâncias por host no `worktree ps` (`#39637`).
15. Integrar a busca combinada de projetos e hosts (`project-host-query`, `#39779`) nos modais de criação de workspace.
16. Expor a visão de Source Control para folder workspaces no cliente móvel (`#39999`).
17. Incluir a ação "Rename project" no menu de contexto de projeto da sidebar (`#39977`).
18. Adotar a ativação completa via `activateAndRevealWorktree` na abertura de workspaces a partir do branch picker (`#41930`, resolve `#41929`).
19. Exibir o nome do worktree ativo no cabeçalho do File Explorer (`#43488`, resolve `#43487`).
20. Adicionar botões de "New File" e "New Folder" na toolbar do File Explorer (`#43443`).
21. Suportar movimentação de projetos hospedados sob unidades mapeadas de WSL (`#43493`).
