---
status: open
description: Os PRs #38378, #38334, #38367, #38168 e #38193 trazem persistência de workspaces aninhados, integridade de submódulos, limpeza e destaques na barra lateral.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#38378`](https://github.com/stablyai/orca/pull/38378),
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
[`stablyai/orca#38361`](https://github.com/stablyai/orca/issues/38361),
[`stablyai/orca#38214`](https://github.com/stablyai/orca/issues/38214),
[`stablyai/orca#38112`](https://github.com/stablyai/orca/issues/38112),
[`stablyai/orca#38017`](https://github.com/stablyai/orca/issues/38017),
[`stablyai/orca#15323`](https://github.com/stablyai/orca/issues/15323) e
[`stablyai/orca#37761`](https://github.com/stablyai/orca/issues/37761).

## O que está entrando no upstream

1. **Preservação de workspaces de servidor aninhados após reinício (`#38378`):**
   - Garante que a estrutura aninhada de workspaces em servidores remotos permaneça preservada e visível na hierarquia
     correta mesmo após a reinicialização do app desktop.
2. **Atualização e integridade de alterações em submódulos Git (`#38334`, `#38318`):**
   - Corrige bug onde diffs e árvores de alterações em submódulos expandidos ficavam obsoletos ou vazios e perdiam pastas
     internas na exibição da sidebar.
3. **Destaque visual para o chat focado nas linhas de agentes (`#38367`):**
   - Destaca graficamente a linha do chat ativo dentro dos cartões de workspace da barra lateral, facilitando saber qual
     sessão está em primeiro plano.
4. **Opção de ocultar worktree principal na barra lateral (`#38361`):**
   - Proposta para permitir manter o worktree primário fora da lista da sidebar em projetos focados exclusivamente em worktrees de feature.
5. **Limpeza de workspaces inativos e indicador de repositório (`#38281`):**
   - Introduz interface aprimorada para limpeza em lote e arquivamento de workspaces ociosos ou obsoletos;
   - Adiciona um indicador visual explícito do repositório de origem junto aos cartões de workspace.
6. **API com permissão para aparência dinâmica desktop de plugins (`#38282`, `#38277`):**
   - Expõe endpoint controlado por permissões que permite aos plugins ajustar dinamicamente elementos de UI e aparência
     no app desktop sem violar o isolamento do sandbox.
7. **Fallback com detecção de conteúdo binário para editores (`#38296`, `#38249`):**
   - Garante que editores customizados baseados em plugins detectem previamente arquivos binários e acionem o fallback
     apropriado em vez de tentar renderizar texto corrompido.
8. **Ações de colapso e expansão em massa de workspaces (`#38168`, resolve `#38138`):**
   - Adiciona as ações "Collapse all" e "Expand all" no menu de opções de workspaces e atalho de teclado configurável,
     permitindo recolher instantaneamente dezenas de worktrees abertos na barra lateral.
9. **Dashboard Global Home (`#38193`, resolve `#38134`):**
   - Implementa a visão global de Home independente de workspaces: exibe status consolidado da frota de agentes, limites
     e consumo de contas de IA e atividades recentes em um único painel.
10. **Preservação de worktrees ocultos ao adicionar projetos (`#38208`):**
    - Garante que worktrees descobertos que foram explicitamente ocultados pelo usuário permaneçam ocultos após a adição
      de um novo projeto no app.
11. **Criação de grupos de projeto vazios na sidebar e CLI (`#38214`, `#38118`):**
    - Permite criar grupos vazios diretamente pelo menu de contexto da barra lateral ou via CLI (`orca project-group create`),
      facilitando a preparação de estruturas antes da alocação de repositórios.
12. **Criação de folder workspaces via CLI (`#38112`):**
    - Proposta de expor `orca workspace create --folder <path>` na CLI, permitindo que agentes configurem workspaces
      sem depender da interface gráfica.
13. **Clarificação visual da hierarquia da barra lateral (`#38089`, `#38017`):**
    - Introduz rótulos de grupos de projetos, blocos delimitados de projetos e ênfase visual em atividade recente,
      permitindo distinguir grupos, projetos e workspaces individuais de relance;
    - Resolve confusão visual em workspaces com muitos repositórios e branches vinculadas.
14. **Organização de listas de workspaces, boards e catálogos por proprietário (`#38092`):**
    - Agrupa listas de workspaces e boards de acompanhamento segundo seus proprietários/origens, facilitando a navegação
      multiprojeto.
15. **Reapontamento de projetos baseados em pastas movidas (`#38078`):**
    - Ao mover ou renomear uma pasta de projeto em disco, o app reaponta a entrada existente em vez de criar um projeto
      duplicado com configurações zeradas (corrige `#30807`).
16. **Supressão de resíduos de escape codes em terminais (`#38049`):**
    - Elimina sequências de escape incompletas (ex.: `"43B"`) impressas na linha de comando logo após a troca de workspace ativo.
17. **Workspace card plugins e seções na barra lateral (`#37650`, `#37654`, `#37661`, `#37664`):**
    - `sidebarCards` como ponto de contribuição declarativa de plugins (fase 2);
    - Card Studio e painel de customização de cartões (fase 3);
    - catálogo oficial de cartões e galeria de estados (fase 4);
    - organização da lista de workspaces da barra lateral em seções (fase L).
18. **Expressividade, workers em tempo real e segurança de cartões (`#37696`, `#37730`, `#37761`):**
    - renderização customizada de agentes por plugins, tempos relativos dinâmicos ("2m ago"), i18n e campos vivos;
    - travas anti-spoofing para impedir que cartões disfarcem status de agentes;
    - `#37730` preserva cor roxa para PRs mesclados em cartões e `#37761` permite ações secundárias dentro de `ListItem`.

## O que fazer

- Adotar o atalho e ação "Collapse all / Expand all" (`#38168`) e a visão Home (`#38193`) no `brza-studio`.
- Incorporar a persistência de workspaces aninhados (`#38378`) e a correção de submódulos (`#38334`).
- Incorporar a interface de limpeza de workspaces inativos e indicador de repositório (`#38281`).
- Avaliar a nova API de aparência dinâmica para plugins (`#38282`) e fallback de binários (`#38296`).
- Incorporar os comandos `project-group` (`#38118`) no `brza-cli` para que scripts de automação criem e organizem workstreams
  automaticamente na barra lateral do `brza-studio`.
