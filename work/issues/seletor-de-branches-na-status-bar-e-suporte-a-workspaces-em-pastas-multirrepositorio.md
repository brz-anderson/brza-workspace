---
status: open
description: Os PRs #41930, #39999, #39977, #39779, #39637 trazem ativação consistente de workspace pelo branch picker, source control mobile em pastas e seletores de projetos.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#41930`](https://github.com/stablyai/orca/pull/41930) (resolve Issue [`#41929`](https://github.com/stablyai/orca/issues/41929)),
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

1. **Incapacidade de anexar worktrees existentes a folder workspaces via CLI (`#39018`):**
   Ao tentar anexar um worktree existente a um folder workspace pai com `orca worktree set --parent-worktree folder:<id>`,
   o comando era rejeitado ("Folder parents are accepted only by orca worktree create"). Além disso, rodar `--parent-worktree active`
   a partir do próprio terminal do folder workspace falhava com "No Orca-managed worktree contains the current directory".
2. **Colisão de sufixo numérico na criação sequencial de worktrees (`#39000`, resolve `#38931`):**
   O gerador automático de sufixos reciclava o número `-100` após `-99`, colidindo com branches locais já existentes e
   abortando a criação de novos worktrees com erro fatal.
3. **Falta de API protegida para remoção de branches locais integrados (`#38955`):**
   A limpeza automatizada de branches após merge exigia invocações diretas de git sem validação de checkout ou barreiras
   de integridade com worktrees ativos.
4. **Invisibilidade e atrito para alternar branches no desktop (`#38869`, `#38836`):**
   O nome do branch ativo não ficava exposto na barra de status inferior. Para trocar de branch no desktop, o desenvolvedor
   era forçado a abrir um terminal manual, pois a interface só oferecia opções de "criar novo worktree". Além disso, o
   cabeçalho do painel de Source Control não permitia alternar ou derivar branches no mesmo checkout, ignorando as novas
   validações de segurança introduzidas no upstream (`#38744`).
5. **Controle de versão cego em workspaces de pasta multirrepositório (`#38831`):**
   Ao abrir uma pasta que agrupa múltiplos repositórios ou worktrees vinculados (*folder workspace*), o painel de Source
   Control exibia apenas uma mensagem estática de "No Git repository found", obrigando o desenvolvedor a navegar para cada
   worktree filho individualmente para verificar alterações pendentes, diffs ou realizar commits.
6. **Ausência de aninhamento visual de workspaces sob pastas na sidebar e mobile (`#38904`, `#38875`):**
   Projetos multirrepositório não agrupavam seus worktrees filhos de maneira hierárquica na barra lateral do desktop nem
   no cliente móvel, poluindo a lista de workspaces planos.
7. **Ocultação indevida de workspace ao remover subdiretório `.git` aninhado (`#38830`):**
   A deleção acidental de um repositório `.git` aninhado desanexava todo o workspace pai e ocultava as abas de agentes ativos.
8. **Dificuldade de inicialização de worktrees em pastas multirrepositório vazias (`#39575`):**
   Ao abrir uma pasta com repositórios Git mas sem worktrees anexados, os painéis de Source Control, Attached Worktrees
   e PR Checks exibiam apenas mensagens estáticas de "No attached worktrees yet" sem ação para criar o primeiro checkout.
9. **Criação de árvores de pastas vazias com espaço inicial em repositórios (`#39572`, `#39545`):**
   Ao colar um caminho com espaço inicial (ex.: `" /Users/user/dev"`) nas configurações de Workspace Directory, o caminho não era
   sanitizado antes da validação. Como o Node `posix.isAbsolute` retorna `false` para caminhos iniciados por espaço, o Orca tratava a
   rota como relativa e criava pastas `" <repo>/ /Users/user/dev"` em todos os repositórios registrados.
10. **Incompatibilidade de seletores `path:` e `name:` com Folder Workspaces na CLI (`#39637`):**
    Agentes e comandos da CLI podiam referenciar folder workspaces apenas pelo identificador literal `folder:<id>`, pois seletores
    como `path:` e `name:` buscavam exclusivamente Git worktrees em repositórios. Além disso, o comando `worktree ps` unificava
    indevidamente linhas de workspaces com mesmo ID em hosts distintos (ex.: `local` e `ssh:server`).
11. **Ausência de Source Control de pastas multirrepositório no app mobile (`#39999`):**
    O cliente mobile não conseguia inspecionar status de controle de versão nem branches alterados em folder workspaces,
    restringindo a visualização de diffs e commits pendentes a repositórios Git isolados.
12. **Incapacidade de renomear projetos pelo menu da barra lateral (`#39977`):**
    Não havia ação rápida no cabeçalho de projetos na barra lateral para renomear projetos/workspaces de forma intuitiva,
    exigindo edições manuais em arquivos de configuração ou recadastramento.
13. **Janela em branco ao abrir workspace de outra branch pelo seletor de branches (`#41930`, resolve `#41929`):**
    Ao selecionar "Open workspace" para uma branch que pertencia a outro workspace cujas abas haviam sido fechadas, a ação
    invocava apenas a mutação interna `setActiveWorktree`. Como não passava pelo ciclo de ativação do usuário, a tela permanecia
    completamente em branco até o operador clicar manualmente na linha correspondente na barra lateral.

## O que o upstream implementa e corrige

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
  - Introduz o matcher compartilhado `project-host-query`, permitindo digitar `<host> <projeto>` (ex.: `box orca`) nos drawers
    de seleção de projetos e no quick-pick do cliente móvel, além do combobox de projetos no desktop;
  - Atualiza simultaneamente o projeto e o host de execução (*Run on*) em uma única seleção rápida.
- **Source Control de folder workspaces no cliente móvel (`#39999`):**
  - Expõe as alterações, diffs e arquivos modificados de projetos de pasta multirrepositório no aplicativo móvel;
  - Permite inspecionar o status de cada repositório Git vinculado diretamente pelo celular sem necessidade de acessar sessões de terminal.
- **Renomeação de projeto no menu do cabeçalho da barra lateral (`#39977`):**
  - Inclui a opção "Rename project" no menu de opções do cabeçalho de projeto da barra lateral;
  - Abre modal direto para atualizar o nome amigável do projeto/workspace e propaga a alteração para a lista de projetos e histórico.
- **Abertura de workspace pelo branch picker com reativação completa (`#41930`, resolve `#41929`):**
  - Altera a ação "Open workspace" no branch picker para utilizar `activateAndRevealWorktree(id, { navigationIntent: 'user-open' })`;
  - Garante que a abertura restabeleça abas padrão (shell ou chat nativo), desperte agentes em sleep mode e registre a visita, evitando janelas em branco quando as abas anteriores haviam sido fechadas.

## O que fazer no BrzA Studio

1. Adotar os comandos CLI de vinculação de worktrees a pastas (`#39018`), permitindo reorganizar worktrees sob pastas de projeto.
2. Incorporar a correção de sufixos numéricos (`#39000`) e a exclusão segura de branches (`#38955`).
3. Integrar o `BranchStatusSegment` na barra de status do `brza-studio` (`#38869`).
4. Adotar o botão "Create worktree" nos painéis vazios de pastas multirrepositório (`#39575`).
5. Aplicar sanitização e `.trim()` em todos os campos de diretório de workspace para evitar criação de pastas acidentais (`#39572`).
6. Suportar seletores unificados `path:` e `name:` para folder workspaces na CLI e separar instâncias por host no `worktree ps` (`#39637`).
7. Integrar a busca combinada de projetos e hosts (`project-host-query`, `#39779`) nos modais de criação de workspace.
8. Expor a visão de Source Control para folder workspaces no cliente móvel (`#39999`).
9. Incluir a ação "Rename project" no menu de contexto de projeto da sidebar (`#39977`).
10. Adotar a ativação completa via `activateAndRevealWorktree` na abertura de workspaces a partir do branch picker (`#41930`, resolve `#41929`).
