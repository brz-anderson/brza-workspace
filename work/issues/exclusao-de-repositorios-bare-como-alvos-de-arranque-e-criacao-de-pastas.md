---
status: open
description: Os PRs #41018, #40999, #40774 e #40852 tratam de exclusão de repositórios bare como alvos de arranque, criação de pastas sem Git e limpeza de agentes.
scope:
  - brza-studio
  - workspace
  - brza-workflow
priority: high
opened: 2026-11-11
tags:
  - tooling
  - infra
  - design
---

# Exclusão de repositórios bare como alvos de arranque e criação de pastas

Rastreado dos PRs abertos no upstream [`stablyai/orca#41018`](https://github.com/stablyai/orca/pull/41018) (resolve Issue [`#40698`](https://github.com/stablyai/orca/issues/40698) e STA-14647),
[`stablyai/orca#40999`](https://github.com/stablyai/orca/pull/40999) (resolve Issue [`#40995`](https://github.com/stablyai/orca/issues/40995)),
[`stablyai/orca#40774`](https://github.com/stablyai/orca/pull/40774) e
[`stablyai/orca#40852`](https://github.com/stablyai/orca/pull/40852).

## O problema

1. **Repositórios Git `.bare` catalogados como workspaces executáveis (`#41018`, resolve `#40698`):**
   Em projetos configurados com repositório base `.bare` e múltiplos worktrees irmãos (layout `<root>/.bare` + `<root>/.git`),
   o aplicativo listava a pasta de armazenamento bare como um workspace principal executável (*runnable workspace*).
   Ao abrir o projeto ou restaurar o foco, terminais e chats de agentes eram iniciados dentro da pasta `.bare`, um diretório
   administrativo que não contém arquivos de código em checkout. Além disso, checkouts vinculados perdiam sua identidade
   física de worktree principal, exibindo badges inconsistentes na sidebar.
2. **Exigência indevida de identidade Git na criação de projetos de pasta (`#40999`, resolve `#40995`):**
   Ao criar um novo projeto a partir de uma pasta local ou em servidor remoto via SSH, a rotina exigia a presença de
   configurações globais de identidade Git (`user.name` e `user.email`). Se o ambiente remoto não tivesse essas chaves
   definidas, a criação do folder project era abortada com erro, mesmo que o usuário desejasse apenas abrir uma pasta
   sem controle de versão.
3. **Retenção desnecessária de agentes concluídos na memória (`#40774`):**
   Agentes de chat e automações cujas tarefas já haviam terminado permaneciam retidos integralmente no estado da aplicação,
   ocupando memória RAM e acumulando handles de processos antigos no ciclo de vida do renderer.
4. **Busca difusa em Configurações sem lista direta de resultados (`#40852`):**
   A busca na tela de Settings apenas filtrava categorias gerais no menu lateral, forçando o usuário a rolar longos painéis
   para localizar o ajuste pesquisado.

## O que o upstream implementa

- **Filtragem e exclusão de repositórios bare como alvos de lançamento (`#41018`):**
  - Mantém registros completos de repositórios bare exclusivamente para o grafo administrativo do Git e persistência de histórico;
  - Oculta repositórios bare das listas de workspaces executáveis na barra lateral, no seletor de workspaces e no launchpad;
  - Recusa a inicialização de novos terminais, chats nativos e pré-checagens de automação quando o diretório alvo for confirmado como bare;
  - Seleciona automaticamente o checkout real vinculado aberto pelo usuário como diretório padrão do projeto;
  - Preserva a identidade de worktree principal para checkouts vinculados a repositórios bare, removendo o badge espúrio "Primary" do armazenamento bare.
- **Criação de projetos de pasta sem dependência de Git (`#40999`, resolve `#40995`):**
  - Permite criar folder projects locais e remotos dispensando a checagem de `user.name` e `user.email`.
- **Descarte de retenção de agentes finalizados (`#40774`):**
  - Libera instâncias e estruturas em memória de agentes cujas tarefas foram concluídas e que não estejam sob visualização ativa.
- **Lista estruturada de resultados na pesquisa de Configurações (`#40852`):**
  - Exibe uma lista direta com os cartões e opções coincidentes, permitindo salto imediato para a configuração desejada.

## O que fazer

1. Impedir que pastas de repositórios bare (`.bare`) sejam tratadas como workspaces executáveis ou diretórios de trabalho de chats e terminais (`#41018`).
2. Permitir a criação de workspaces de pasta sem exigir identidade Git pré-configurada (`#40999`).
3. Liberar da memória instâncias de agentes finalizados (`#40774`).
4. Apresentar os resultados de busca das configurações em formato de lista navegável (`#40852`).
