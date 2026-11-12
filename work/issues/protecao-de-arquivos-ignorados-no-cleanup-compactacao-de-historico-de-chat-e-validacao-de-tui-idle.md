---
status: open
description: Os PRs #41446, #41392, #41366, #41384 trazem aviso de perda de .env no cleanup, compactação SQLite de chat sem histórico intermediário e idle seguro.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#41446`](https://github.com/stablyai/orca/pull/41446),
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

## O que fazer

- Adotar a detecção e proteção de arquivos ignorados em risco (`readWorktreeAtRiskLocalFiles`) antes da exclusão de workspaces (`#41446`).
- Incorporar o gatilho de substituição direta de revisões de chat (`journal_outcome_item_supersede`) para estancar o crescimento do SQLite (`#41392`).
- Aplicar a corroboração do marcador do composer para instâncias adotadas do Claude no `tui-idle` (`#41366`).
- Adotar a política de cache de badges do Linear sem revalidação por foco de janela (`#41384`).
