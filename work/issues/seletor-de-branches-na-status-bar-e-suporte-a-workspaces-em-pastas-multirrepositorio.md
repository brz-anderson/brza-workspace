---
status: open
description: Os PRs #38869, #38836, #38831, #38904 e #38875 trazem seletor de branches na status bar e no Source Control, seções por worktree em pastas e hierarquia multirrepositório.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#38869`](https://github.com/stablyai/orca/pull/38869),
[`stablyai/orca#38836`](https://github.com/stablyai/orca/pull/38836),
[`stablyai/orca#38831`](https://github.com/stablyai/orca/pull/38831),
[`stablyai/orca#38904`](https://github.com/stablyai/orca/pull/38904) e
[`stablyai/orca#38875`](https://github.com/stablyai/orca/pull/38875), além das issues
[`stablyai/orca#38931`](https://github.com/stablyai/orca/issues/38931) e
[`stablyai/orca#38830`](https://github.com/stablyai/orca/issues/38830).

## O problema

1. **Invisibilidade e atrito para alternar branches no desktop (`#38869`, `#38836`):**
   O nome do branch ativo não ficava exposto na barra de status inferior. Para trocar de branch no desktop, o desenvolvedor
   era forçado a abrir um terminal manual, pois a interface só oferecia opções de "criar novo worktree". Além disso, o
   cabeçalho do painel de Source Control não permitia alternar ou derivar branches no mesmo checkout, ignorando as novas
   validações de segurança introduzidas no upstream (`#38744`).
2. **Controle de versão cego em workspaces de pasta multirrepositório (`#38831`):**
   Ao abrir uma pasta que agrupa múltiplos repositórios ou worktrees vinculados (*folder workspace*), o painel de Source
   Control exibia apenas uma mensagem estática de "No Git repository found", obrigando o desenvolvedor a navegar para cada
   worktree filho individualmente para verificar alterações pendentes, diffs ou realizar commits.
3. **Ausência de aninhamento visual de workspaces sob pastas na sidebar e mobile (`#38904`, `#38875`):**
   Projetos multirrepositório não agrupavam seus worktrees filhos de maneira hierárquica na barra lateral do desktop nem
   no cliente móvel, poluindo a lista de workspaces planos. Ademais, a linhagem (*lineage*) de pais era recalculada a cada
   atualização, sobrescrevendo links manuais e desconsiderando filhos em servidores ou VMs remotas pareadas.
4. **Colisão de sufixo numérico na criação sequencial de worktrees (`#38931`):**
   O gerador automático de nomes de worktrees incrementava sufixos de `-1` até `-99`, mas após `-99` voltava incorretamente
   para `-100` e reciclava referências locais já existentes, abortando comandos de criação com `Branch already exists locally`.
5. **Ocultação indevida de workspace ao remover subdiretório `.git` aninhado (`#38830`):**
   A criação acidental de um repositório git aninhado executava `git init` redundante em uma subpasta; quando o usuário
   removia aquele `.git` secundário, o observador do app desanexava todo o workspace do projeto pai e ocultava as abas de
   chat ativas do agente sem qualquer mecanismo de recuperação via interface.

## O que o upstream implementa e corrige

- **Segmento de branch interativo na Status Bar (`#38869`):**
  - Adiciona o componente `BranchStatusSegment` no canto inferior esquerdo da barra de status, exibindo o branch corrente
    com ícone indicador;
  - Ao clicar, abre um popover pesquisável listando branches locais e remotos (`origin`), ordenados pelos commits mais
    recentes, com fetch em background para refletir o estado do servidor sem emitir toasts espúrios.
- **Alternância e derivação de branches no Source Control (`#38836`):**
  - O cabeçalho do Source Control transforma o nome do branch (`⎇ main ▾`) em um seletor completo: permite trocar de branch
    local, rastrear branch remoto, criar um novo branch a partir do commit ativo ou navegar para outro workspace onde o
    branch já esteja em checkout (*Open workspace*), aplicando as travas de proteção contra commits sujos.
- **Source Control multinível para Folder Workspaces (`#38831`):**
  - O painel de Source Control agora detecta todos os worktrees vinculados à pasta multirrepositório e renderiza uma seção
    colapsável por worktree (com branch, contagem ahead/behind, rascunho de mensagem e grupos Staged/Changes/Untracked);
  - Clicar em um arquivo abre a aba rotulada com o nome do respectivo repositório no folder workspace atual, preservando
    operações de Git e limites de inotify.
- **Hierarquia de pastas e linhagem cross-machine (`#38904`, `#38875`):**
  - Aninha os workspaces filhos visualmente sob o folder workspace pai na barra lateral do desktop e no cliente móvel;
  - Resolve pais de tarefas no momento da criação do workspace em vez de a cada refresh, garantindo persistência de
    desanexações e suportando pastas locais parentando filhos em máquinas SSH ou WSL.
- **Robustez de nomes de worktree e repositórios aninhados (`#38931`, `#38830`):**
  - Evita colisões numéricas na expansão de nomes de branch e previne que deleções de `.git` locais destruam a referência
    do workspace principal ou derrubem chats de agentes em execução.

## O que fazer no BrzA Studio

1. Integrar o `BranchStatusSegment` na barra de status do `brza-studio`, facilitando a alternância rápida de workstreams e
   branches pelo desenvolvedor e mantendo paridade ergonômica com editores modernos.
2. Adotar o suporte a seções por worktree no Source Control para pastas de workspaces compostos (como o próprio ecossistema
   BrzA, que agrupa `.worktrees/*`).
3. Portar a resolução de aninhamento de `folder workspaces` na barra lateral para manter a lista de workstreams organizada.
