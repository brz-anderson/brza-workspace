---
priority: high
tags:
  - chat
  - tooling
  - design
description: Os PRs #42804, #42811, #42796 e issues #42794, #42800, #11777 trazem criação e comparação competitiva de múltiplos agentes (best-of-N), revisão de diffs com IA no Source Control e notas de worktree via CLI.
---

# Avaliação comparativa de agentes via CLI, revisão de diff com IA e notas de worktree

Rastreado dos PRs abertos no upstream [`stablyai/orca#42804`](https://github.com/stablyai/orca/pull/42804) (resolve Issue [`#42794`](https://github.com/stablyai/orca/issues/42794)),
[`stablyai/orca#42811`](https://github.com/stablyai/orca/pull/42811) (resolve Issue [`#42800`](https://github.com/stablyai/orca/issues/42800)) e
[`stablyai/orca#42796`](https://github.com/stablyai/orca/pull/42796) (resolve Issue [`#11777`](https://github.com/stablyai/orca/issues/11777)).

## O problema

1. **Processo manual e repetitivo para comparar múltiplos agentes na mesma tarefa (`#42804`, resolve `#42794`):**
   Disputar uma mesma tarefa técnica entre diferentes modelos (como Claude e Codex) para escolher a melhor implementação exigia a criação manual de N workspaces com nomes customizados, colagem idêntica do mesmo prompt em cada aba e inspeção manual dos diffs resultantes, sem ferramenta estruturada para consolidar ou avaliar os resultados.
2. **Revisões de código por IA desconectadas das notas no diff do editor (`#42811`, resolve `#42800`):**
   Ao solicitar que um agente revise alterações em um branch, o resultado vinha como texto plano no chat ou terminal. O operador precisava ler o texto, localizar manualmente cada arquivo e linha e copiar o apontamento como nota de revisão no diff antes de poder resolvê-la ou despachá-la de volta ao agente.
3. **Ausência de comandos na CLI para manipulação programática de notas de revisão (`#42796`, resolve `#11777`):**
   Scripts externos, automações de CI e agentes de linha de comando não possuíam como criar, listar ou limpar notas de revisão vinculadas a linhas específicas de arquivos em um worktree (`diffComments`), limitando a integração do ferramental de revisão ao clique manual na interface gráfica.

## O que o upstream implementa

- **Criação e comparação competitiva de múltiplos agentes via CLI (*best-of-N*) (`#42804`, resolve `#42794`):**
  - Adiciona o parâmetro `--agents <lista>` (de 2 a 6 agentes, ex.: `claude,codex,claude`) ao comando `orca worktree create`, provisionando automaticamente worktrees isolados nomeados `<nome>-<agente>` sob o mesmo parent lineage e despachando o mesmo prompt inicial de forma determinística;
  - Introduz o comando `orca worktree compare --worktree <a> --worktree <b> [...] --agent <id>`: lê as alterações de cada worktree candidato (commits desde o merge base, arquivos não commitados e untracked) e inicializa um agente juiz instruído a atribuir notas de 0 a 10 com justificativa técnica para cada tentativa e recomendar o vencedor sem alterar código.
- **Ação "Review changes with AI" no Source Control integrada a notas no diff (`#42811`, resolve `#42800`):**
  - Adiciona o item "Review changes with AI" no menu de ações `⋯` do painel de Source Control;
  - Executa a receita de ação `reviewChanges` lançando o agente de IA para auditar as alterações contra o base branch e registrar automaticamente cada problema encontrado como uma nota de revisão de código nas linhas correspondentes usando o prefixo de severidade `[critical]`, `[major]` ou `[minor]`;
  - Permite customização global ou por repositório do prompt de revisão e modelo utilizado em Configurações → Git & Source Control → Action recipes.
- **Gerenciamento de notas de revisão via CLI (`#42796`, resolve `#11777`):**
  - Adiciona o grupo de comandos `orca worktree notes`:
    - `list [--file <path>]`: lista notas registradas no workspace ativo com seus identificadores;
    - `add --file <path> --line <n> [--start-line <n>] (--body <text> | --body-file <path|->)`: adiciona anotações de revisão pontuais ou por intervalo de linhas;
    - `clear (--id <id> | --file <path> | --all)`: remove anotações específicas ou em lote;
  - Integra-se ao mecanismo atômico de mesclagem `diffComments` / `diffCommentsBase` no `worktree.set`.

## O que fazer

- Adotar o disparo paralelo de tarefas em múltiplos agentes com `orca worktree create --agents` e o avaliador `orca worktree compare` (`#42804`, resolve `#42794`).
- Integrar a ação "Review changes with AI" no painel de Source Control para geração direta de notas de revisão no diff (`#42811`, resolve `#42800`).
- Incorporar o grupo de comandos `brza worktree notes` na CLI (`#42796`, resolve `#11777`).
