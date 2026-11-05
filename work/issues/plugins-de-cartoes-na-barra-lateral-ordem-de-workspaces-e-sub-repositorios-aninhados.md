---
status: open
description: Os PRs #38588, #38634, #38561, #38518, #38378 e #38168 trazem menu de ações de agentes na sidebar, colapso em massa de projetos, menu "+" em cartões e nomes de abas consistentes.
scope:
  - brza-studio
  - workspace
priority: medium
opened: 2026-11-03
tags:
  - design
  - tooling
---

# Plugins de cartões na barra lateral, ordem de workspaces e sub-repositórios aninhados

Rastreado dos PRs abertos no upstream [`stablyai/orca#38588`](https://github.com/stablyai/orca/pull/38588) (Issue [`#38586`](https://github.com/stablyai/orca/issues/38586)),
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
[`stablyai/orca#37730`](https://github.com/stablyai/orca/pull/37730),
[`stablyai/orca#37557`](https://github.com/stablyai/orca/pull/37557) e
[`stablyai/orca#37510`](https://github.com/stablyai/orca/pull/37510), além das issues
[`#38617`](https://github.com/stablyai/orca/issues/38617),
[`#38550`](https://github.com/stablyai/orca/issues/38550),
[`#38361`](https://github.com/stablyai/orca/issues/38361),
[`#38214`](https://github.com/stablyai/orca/issues/38214),
[`#38112`](https://github.com/stablyai/orca/issues/38112),
[`#38017`](https://github.com/stablyai/orca/issues/38017),
[`#15323`](https://github.com/stablyai/orca/issues/15323) e
[`#37761`](https://github.com/stablyai/orca/issues/37761).

## O que está entrando no upstream

1. **Menu de ações diretas na linha de agentes da barra lateral (`#38588`, `#38586`):**
   - Adiciona menu contextual acessível em cada linha compacta de agente nos cartões de workspace:
     - **Rename:** renomeia a sessão ativa do agente no próprio local;
     - **Continue in Terminal:** bifurca/continua a sessão estruturada em uma nova aba de terminal;
     - **Copy Session ID:** copia o identificador interno da sessão do provedor;
     - **Close:** encerra a sessão e fecha a aba correspondente sem precisar localizá-la e ativá-la na barra superior.
2. **Ações para colapsar e expandir todos os projetos (`#38634`):**
   - Adiciona controles globais no cabeçalho da barra lateral para recolher ou expandir simultaneamente todos os agrupamentos
     de projetos e seus respectivos worktrees.
3. **Metadados de criação e atividade na listagem de workspaces (`#38617`):**
   - Exponibiliza os campos `createdAt` e `lastActivityAt` na RPC `workspace.list` e CLI, facilitando automações de limpeza.
4. **Botão de criação "+" ao lado do título do workspace na sidebar (`#38561`):**
   - Adiciona botão acessível "New tab" ao lado do nome do workspace nos cartões da barra lateral, abrindo o mesmo
     `WorkspaceCreateMenu` disponível na barra de abas superior (lançamento de agente, terminal, browser ou markdown);
   - Elimina a necessidade de selecionar primeiro o workspace e depois se deslocar até a barra superior.
5. **Preservação do nome real da sessão do agente em abas de terminal (`#38518`):**
   - Unifica a hierarquia de nomes de abas (`resolveTabNameSource`): renomeação manual → nome de comando rápido → título
     ao vivo do OpenCode → nome próprio da sessão do agente → título gerado pelo primeiro prompt;
   - Impede que abas de terminais com agentes ativos fiquem presas em títulos genéricos do primeiro prompt.
6. **Opção para ocultar chip de projeto em cartões fixados da sidebar (`#38550`):**
   - Proposta para permitir ocultar o badge redundante de projeto em cartões de workspace fixados.
7. **Preservação de workspaces de servidor aninhados após reinício (`#38378`):**
   - Garante que a estrutura aninhada de workspaces em servidores remotos permaneça preservada e visível na hierarquia
     correta mesmo após a reinicialização do app desktop.
8. **Atualização e integridade de alterações em submódulos Git (`#38334`, `#38318`):**
   - Corrige bug onde diffs e árvores de alterações em submódulos expandidos ficavam obsoletos ou vazios e perdiam pastas
     internas na exibição da sidebar.
9. **Destaque visual para o chat focado nas linhas de agentes (`#38367`):**
   - Destaca graficamente a linha do chat ativo dentro dos cartões de workspace da barra lateral, facilitando saber qual
     sessão está em primeiro plano.
10. **Opção de ocultar worktree principal na barra lateral (`#38361`):**
    - Proposta para permitir manter o worktree primário fora da lista da sidebar em projetos focados exclusivamente em worktrees de feature.
11. **Limpeza de workspaces inativos e indicador de repositório (`#38281`):**
    - Interface aprimorada para limpeza em lote e indicador visual de repositório de origem.
12. **API com permissão para aparência dinâmica desktop de plugins (`#38282`, `#38277`):**
    - Expõe endpoint controlado por permissões para que plugins ajustem elementos de UI no app desktop.
13. **Fallback com detecção de conteúdo binário para editores (`#38296`, `#38249`):**
    - Detecção prévia de arquivos binários acionando fallback em editores customizados de plugins.
14. **Ações de colapso e expansão em massa de workspaces (`#38168`, resolve `#38138`):**
    - "Collapse all" e "Expand all" no menu de opções de workspaces e atalho configurável.
15. **Dashboard Global Home (`#38193`, resolve `#38134`):**
    - Visão consolidada da frota de agentes e limites de uso em um único painel.
16. **Preservação de worktrees ocultos ao adicionar projetos (`#38208`):**
    - Garante que worktrees explicitamente ocultados permaneçam ocultos.
17. **Criação de grupos de projeto vazios na sidebar e CLI (`#38214`, `#38118`):**
    - Subcomando `orca project-group create` e menu de contexto.
18. **Criação de folder workspaces via CLI (`#38112`):**
    - Proposta para `orca workspace create --folder <path>`.

## O que fazer

- Implementar o menu contextual de ações de agentes na sidebar (`#38588`) no `brza-studio`.
- Adicionar os controles de colapso e expansão em massa de projetos (`#38634`).
- Incorporar o botão de novo item "+" nos cartões de workspace (`#38561`) e a resolução de títulos (`#38518`).
- Incorporar os comandos `project-group` (`#38118`) no `brza-cli`.
