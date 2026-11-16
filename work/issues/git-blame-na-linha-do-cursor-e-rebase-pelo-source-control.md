---
status: open
description: Os PRs #42982, #42949, #42997 e a issue #42924 trazem git blame inline na linha do cursor no editor, rebase direto a partir do base branch no Source Control e suporte a submódulos Git.
scope:
  - brza-studio
  - workspace
  - brza-workflow
priority: high
opened: 2026-11-16
tags:
  - tooling
  - design
---

# Git Blame inline na linha do cursor, rebase pelo Source Control e suporte a submódulos

Rastreado dos PRs abertos no upstream [`stablyai/orca#42982`](https://github.com/stablyai/orca/pull/42982),
[`stablyai/orca#42949`](https://github.com/stablyai/orca/pull/42949),
[`stablyai/orca#42997`](https://github.com/stablyai/orca/pull/42997) e
da issue [`stablyai/orca#42924`](https://github.com/stablyai/orca/issues/42924).

## O problema

1. **Ausência de anotação de autoria e histórico de alterações na linha ativa do editor (`#42982`):**
   Ao inspecionar arquivos no editor integrado, o desenvolvedor ou agente não consegue ver de imediato quem alterou a linha sob o cursor, qual foi a mensagem do commit ou quando a alteração foi realizada. Para consultar o histórico, é necessário abrir o terminal ou recorrer a ferramentas externas como `git blame` / `git log -L`, quebrando o fluxo de leitura e depuração de código.
2. **Falta de ação direta para rebase contra a branch base no Source Control (`#42949`):**
   No painel de Source Control, quando o branch atual está defasado em relação à branch base (upstream/main), o desenvolvedor precisa abrir um terminal manual para executar `git rebase <base-branch>` ou resolver conflitos fora da UI. A linha que indica a branch base no painel de controle de versão é estática e não oferece ações contextuais de sincronização ou rebase.
3. **Impossibilidade de definir o nome do branch programaticamente na criação de workspaces via plugins (`#42997`):**
   A API de automação e plugins `workspace.create` gerava ou utilizava nomes padronizados de branch sem permitir que scripts de orquestração especificassem o nome exato da branch de trabalho desejada para o novo workspace.
4. **Falta de suporte de primeira classe a submódulos Git (`#42924`):**
   Workspaces em repositórios que dependem de submódulos Git enfrentam dificuldades na sincronização de estado, detecção de alterações pendentes nos submódulos e checkout recursivo automático ao criar worktrees isolados, gerando erros de build por dependências ausentes.

## O que o upstream implementa

1. **Git blame inline na linha do cursor (`#42982`):**
   - Implementa anotação inline discreta no editor na linha onde o cursor está posicionado, exibindo o autor do commit, o tempo relativo da alteração (ex.: "3 months ago") e o resumo da mensagem de commit;
   - Atualiza de forma assíncrona e debounceada sem bloquear a digitação no buffer do editor;
   - Permite clicar na anotação ou passar o ponteiro para inspecionar os detalhes do commit completo (hash SHA-1, autor, data e mensagem integral).
2. **Rebase a partir da linha da branch base no Source Control (`#42949`):**
   - Adiciona ação contextual diretamente na linha da branch base no painel Source Control (botão e menu de contexto de rebase);
   - Permite disparar `git rebase` contra a base de forma assistida, com detecção imediata de conflitos e suporte aos fluxos de continuidade ou aborto do rebase pela própria interface.
3. **Parâmetro de nome de branch em `workspace.create` para plugins (`#42997`):**
   - Estende a API de plugins permitindo que `workspace.create` receba a propriedade `branchName` explícita, assegurando que o novo worktree seja inicializado no branch correto sem necessidade de renomeação manual subsequente.
4. **Rastreamento de arquitetura para submódulos Git (`#42924`):**
   - Mapeia os requisitos para suporte completo a `git submodule` em workspaces gerenciados, incluindo checkout recursivo automático na criação de worktrees e visualização unificada de status no Source Control.

## O que fazer no BrzA Studio

- Adotar a anotação de Git blame na linha do cursor no editor do Studio (`#42982`), com renderização sutil e painel de detalhes do commit.
- Integrar a ação de rebase direto na linha da branch base na visualização de Source Control (`#42949`).
- Expor o parâmetro `branchName` na chamada `workspace.create` dos plugins e extensões do Studio (`#42997`).
- Planejar e incorporar a gestão recursiva de submódulos Git na criação de worktrees e painel de Source Control (`#42924`).
