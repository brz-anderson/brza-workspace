---
status: open
description: Os PRs #41765, #41760, #41483, #41480, #41457 trazem varreduras offline rápidas, runner automático em background e proteção de worktrees no cleanup.
scope:
  - brza-studio
  - workspace
  - brza-workflow
priority: high
opened: 2026-11-12
tags:
  - tooling
  - infra
---

# Proteção de arquivos ignorados no cleanup, compactação de histórico de chat e validação de TUI idle

Rastreado dos PRs abertos no upstream [`stablyai/orca#41765`](https://github.com/stablyai/orca/pull/41765),
[`stablyai/orca#41760`](https://github.com/stablyai/orca/pull/41760),
[`stablyai/orca#41483`](https://github.com/stablyai/orca/pull/41483),
[`stablyai/orca#41480`](https://github.com/stablyai/orca/pull/41480),
[`stablyai/orca#41457`](https://github.com/stablyai/orca/pull/41457),
[`stablyai/orca#41446`](https://github.com/stablyai/orca/pull/41446),
[`stablyai/orca#41392`](https://github.com/stablyai/orca/pull/41392),
[`stablyai/orca#41366`](https://github.com/stablyai/orca/pull/41366) (STA-14925 / STA-2380) e
[`stablyai/orca#41384`](https://github.com/stablyai/orca/pull/41384).

## O problema

1. **Perda silenciosa de arquivos locais e segredos ignorados (`.env`) na exclusão de worktrees (`#41446`):**
   - Ao excluir ou limpar um worktree pelo diálogo de cleanup ou pela barra lateral, a checagem `git status` ignorava arquivos
     desconsiderados pelo `.gitignore` (ex.: `.env`, arquivos de configuração local ou chaves privadas);
   - O comando `git worktree remove` apagava pastas e arquivos sem qualquer aviso, levando à perda irreparável de segredos
     locais que não existiam em nenhum outro checkout.
2. **Crescimento descontrolado do banco SQLite de histórico de chat com revisões intermediárias (`#41392`):**
   - No streaming de respostas no chat nativo, cada revisão parcial do texto emitido pelo modelo gravava uma linha completa
     da mensagem no banco de dados. Em conversas com centenas de turnos, o arquivo chegava a centenas de megabytes (ex.: 884 MB para 26k registros),
     gerando lentidão e fragmentação desnecessária no disco;
   - Leituras de abertura e restauração necessitam apenas da primeira versão (para evidência de admissão) e da versão mais recente
     (para exibição final), tornando todas as revisões intermediárias lixo redundante.
3. **Falso estado de prontidão (`tui-idle`) em instâncias adotadas do Claude (`#41366`, STA-14925):**
   - O PR `#40539` garantiu que o Claude só seja considerado ocioso e pronto para despachos após desenhar sua caixa de entrada
     (`❯` + NBSP após `DECSET 2031`). Porém, essa validação era aplicada exclusivamente quando o app iniciava o processo diretamente;
   - Em abas adotadas ou iniciadas por comandos externos cujo título OSC identificava o Claude, o sistema caía na checagem genérica
     de "qualquer texto visível". Mensagens emitidas por hooks de shell (ex.: `zsh-you-should-use`) enganavam o detector,
     fazendo o orquestrador despachar comandos antes do Claude estar pronto e perdendo prompts.
4. **Rajadas desnecessárias de requisições de badges do Linear ao focar a janela (`#41384`):**
   - Cada retorno de foco à janela do app revalidava todos os badges de tarefas do Linear montados na tela após 60 segundos de inatividade,
     gerando centenas de requisições à API do Linear em paralelo sem que o usuário estivesse interagindo com aquelas tarefas.
5. **Visibilidade persistente de workspaces durante cleanup demorado em background (`#41483`):**
   - Na exclusão de workspaces com grande volume de arquivos, a linha permanecia visível na barra lateral durante todo o processo de limpeza em segundo plano;
   - Caso o app sofresse encerramento ou reinicialização durante o processo, o cleanup ficava incompleto e o registro de remoção era perdido.
6. **Execuções duplicadas e concorrentes de `git worktree list` em repositórios grandes (`#41480`):**
   - Dois caches desacoplados no processo principal (um da barra lateral com TTL de 5s e outro de runtime para CLI/agentes com TTL de 30s) disparavam leituras repetidas de worktrees;
   - Em repositórios com centenas de worktrees, o app executava `git worktree list` a cada ~48s, gerando sobrecarga desnecessária de CPU e I/O.
7. **Disparo indevido de atalho de exclusão de workspace com foco no terminal ou editor (`#41457`):**
   - O atalho de teclado para exclusão de workspace não verificava se o foco estava na árvore da barra lateral, abrindo diálogos de exclusão mesmo quando o usuário estava digitando no terminal ou editor.
8. **Sobrecarga de rede e lentidão nas varreduras de cleanup de worktrees (`#41765`):**
   - A varredura de histórico Git para verificar se o trabalho de um worktree já havia sido integrado (`merged`/`squashed`) realizava downloads lentos de blobs faltantes em clones parciais (`--filter=blob:none`);
   - Em repositórios com dezenas de worktrees, a checagem demorava mais de 20s e corria o risco de expirar antes de concluir.
9. **Ausência de automação em segundo plano para aplicação de regras de limpeza de workspaces (`#41760`):**
   - A limpeza de workspaces exigia abertura manual do diálogo de cleanup a partir da barra de status, acumulando branches mesclados, checkouts inativos e diretórios órfãos ao longo do tempo.

## O que o upstream propõe e implementa

1. **Varredura at-risk de arquivos ignorados antes de remover worktrees (`#41446`):**
   - Implementa `readWorktreeAtRiskLocalFiles`, listando arquivos com `git ls-files -o -i --exclude-standard --directory`;
   - Descarta pastas regeneráveis (`node_modules`, `dist`, `.venv`, `.next`, `target`, `vendor`), symlinks e arquivos idênticos
     aos do checkout principal (como `.env` padrão replicado pelo setup);
   - Apresenta aviso explícito no modal de exclusão e na barra lateral ("Ignored files will be lost: .env, local/"), bloqueando
     a deleção automática sem confirmação prévia do operador.
2. **Compactação contínua de histórico de chat mantendo apenas primeiro e último registro (`#41392`):**
   - Adiciona um gatilho de esquema (`journal_outcome_item_supersede`) que apaga imediatamente a revisão anterior assim que uma
     nova revisão do mesmo item é gravada, estabilizando o custo por escrita em O(1);
   - Roda uma rotina de compactação em thread de worker dedicada 2 minutos após o arranque, paginada em 64 registros com duty cycle de 10%,
     reduzindo a base de itens pela metade sem impacto no loop de eventos principal e reutilizando páginas liberadas no SQLite.
3. **Corroboração de marcador de composer para instâncias do Claude identificadas por título (`#41366`):**
   - Estende a exigência do marcador de entrada `❯` para qualquer painel identificado como Claude interativo via título OSC (`paintAgent`);
   - Ignora comandos que executam em modo print (`-p`, `--output-format json`) ou pipelines com pagers (`less`, `more`), assegurando
     que ferramentas de automação e orquestração nunca enviem prompts antes do composer interativo estar pronto.
4. **Desativação de refetch de badges do Linear por evento de foco (`#41384`):**
   - Remove os listeners de foco de janela para badges montados, atualizando detalhes apenas na montagem ou via notificação
     específica pós-escrita de ferramentas locais, reduzindo requisições em 83,3%.
5. **Ocultação imediata de linha na UI e persistência de cleanup em tabela durável (`#41483`):**
   - Registra exclusões em tabela durável (`worktree-removal-table.ts`) e oculta a linha da visualização imediatamente (`removal-visibility.ts`);
   - Em reinicializações do app com remoções pendentes, o processo retoma o cleanup de arquivos e do registro Git sem intervenção manual.
6. **Proprietário único de listagem de worktrees por repositório (`#41480`):**
   - Cria modelo centralizado por repositório e runtime Git, unificando os acessos da barra lateral e do catálogo de runtime;
   - Reutiliza leituras em andamento para requisições concorrentes e invalida o cache apenas diante de mutações ou eventos estruturais do watcher.
7. **Restrição de atalhos de exclusão de workspace à seleção da barra lateral (`#41457`):**
   - Vincula o listener de teclado de exclusão estritamente ao container da barra lateral quando focado (`use-sidebar-workspace-delete-keyboard.ts`);
   - Garante que teclas pressionadas no terminal ou editor nunca acionem a caixa de confirmação de exclusão.
8. **Varredura offline 4x mais rápida de cleanup de workspaces (`#41765`):**
   - Executa as checagens de merge e provas Git com `GIT_NO_LAZY_FETCH=1` e `GIT_ALLOW_PROTOCOL=none`, impedindo fetches acidentais de rede em clones parciais;
   - Memoiza referências base (`createWorkspaceCleanupRepoRefs`) por repositório durante a varredura e otimiza a busca de squashes (`git log --name-only --no-renames` + `patch-id` apenas para commits com conjunto idêntico de arquivos tocados), reduzindo o tempo de varredura de ~23s para ~5s.
9. **Execução automática de regras de cleanup de workspace em background por host (`#41760`):**
   - Implementa o `WorkspaceCleanupRunner` com ciclo de avaliação compartilhada (`evaluateWorkspaceCleanup`), disparado 2 minutos após o boot, a cada hora e 10s após alterações de regras;
   - Executa isoladamente no host/processo dono do repositório (desktop local, orcad de SSH ou WSL), revalidando evidências (pins, drafts não salvos, terminais abertos, daemons e arquivos dirty) imediatamente antes da remoção segura via `queueWorkspaceDelete`.

## O que fazer

- Adotar a varredura offline rápida de cleanup (`#41765`), eliminando lazy fetches do Git e acelerando o cálculo de merges e squashes.
- Incorporar o runner de background de cleanup de workspaces (`#41760`) com revalidação estrita de evidências e proteção contra deleção acidental.
- Adotar a tabela durável de cleanup com ocultação imediata de workspaces em remoção (`#41483`).
- Unificar o gerenciamento de cache de worktrees por repositório para eliminar chamadas redundantes a `git worktree list` (`#41480`).
- Restringir os atalhos de exclusão de workspace exclusivamente ao foco na barra lateral (`#41457`).
- Adotar a detecção e proteção de arquivos ignorados em risco (`readWorktreeAtRiskLocalFiles`) antes da exclusão de workspaces (`#41446`).
- Incorporar o gatilho de substituição direta de revisões de chat (`journal_outcome_item_supersede`) para estancar o crescimento do SQLite (`#41392`).
- Aplicar a corroboração do marcador do composer para instâncias adotadas do Claude no `tui-idle` (`#41366`).
- Adotar a política de cache de badges do Linear sem revalidação por foco de janela (`#41384`).
