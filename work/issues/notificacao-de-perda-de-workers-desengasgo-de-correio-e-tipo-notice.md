---
status: open
description: Os PRs #41426, #41424, #41423, #41422, #40983 trazem encerramento de loop de mail remoto, corte de CPU em saída de PTY e limpeza de bookkeeping.
scope:
  - brza-studio
  - brza-workflow
priority: high
opened: 2026-11-11
tags:
  - tooling
  - infra
  - chat
---

# Notificação de perda de workers, desengasgo de correio e tipo notice

Rastreado dos PRs abertos no upstream [`stablyai/orca#41426`](https://github.com/stablyai/orca/pull/41426) (STA-14936),
[`stablyai/orca#41424`](https://github.com/stablyai/orca/pull/41424) (STA-14935),
[`stablyai/orca#41423`](https://github.com/stablyai/orca/pull/41423) (STA-14934),
[`stablyai/orca#41422`](https://github.com/stablyai/orca/pull/41422) (STA-14933),
[`stablyai/orca#40983`](https://github.com/stablyai/orca/pull/40983),
[`stablyai/orca#40972`](https://github.com/stablyai/orca/pull/40972),
[`stablyai/orca#40977`](https://github.com/stablyai/orca/pull/40977) (resolve Issue [`#40968`](https://github.com/stablyai/orca/issues/40968)),
[`stablyai/orca#40967`](https://github.com/stablyai/orca/pull/40967),
[`stablyai/orca#40963`](https://github.com/stablyai/orca/pull/40963),
[`stablyai/orca#40949`](https://github.com/stablyai/orca/pull/40949) e
[`stablyai/orca#40962`](https://github.com/stablyai/orca/pull/40962) (resolve Issue [`#40956`](https://github.com/stablyai/orca/issues/40956)).

## O problema

1. **Perda silenciosa de workers em falhas de inicialização ou fechamento de painel (`#40983`):**
   Quando um coordenador despachava tarefas para subagentes/workers, se a inicialização do terminal falhasse por limites
   de PTYs do sistema, se o usuário fechasse manualmente o painel do worker no app, se o terminal caísse ou se o agente
   terminasse inesperadamente, o coordenador não recebia nenhuma notificação direta. Ficava aguardando indefinidamente
   por relatórios de conclusão que nunca chegariam.
2. **Ausência de tipo de mensagem puramente informativo entre agentes (`#40972`):**
   Ao despachar uma mensagem endereçada com `--to` sem especificar `--type`, o sistema tratava a mensagem como `status`.
   Mensagens de `status` inseriam automaticamente cabeçalhos que sugeriam resposta e comandos de reply, fazendo com que
   workers interrompessem tarefas em andamento para responder notas que eram meramente informativas.
3. **Travamento permanente da fila de correio remoto ao responder a perguntas (`#40977`, resolve `#40968`):**
   Quando um worker em servidor pareado utilizava `orchestration send --type question` e o coordenador respondia com
   `orchestration reply`, a entrega local falhava com `question_not_found` porque apenas o comando `ask` persistia o registro
   em `remote_questions`. O item permanecia sem confirmação (*unacked*), travando completamente toda a fila de mensagens
   subsequentes para o mesmo worker, embora `send` e `reply` continuassem acusando sucesso na CLI.
4. **Impossibilidade de parar ou retomar workers de chat após reinicialização do app (`#40967`, `#40963`):**
   Workers de chat ou terminais interrompidos por um restart do Orca/Studio ficavam em estado inconsistente: o coordenador
   não conseguia interromper nem despachar acompanhamentos (*follow-ups*) limpos após a reinicialização da aplicação.
5. **Falha `agent_not_in_foreground` em inicialização de workers Claude sob bash (`#40962`, resolve `#40956`):**
   Ao invocar `worker-start --agent claude` em ambientes Linux/macOS com bash, funções de profile do Claude deixavam um
   subshell bash em primeiro plano no grupo de processos do terminal, fazendo o supervisor rejeitar o arranque com erro
   `agent_not_in_foreground`.

## O que o upstream implementa

- **Alerta padronizado de workers perdidos (`#40983`):**
  - Adiciona o motivo `lost` em `reportWorkerTurnStop`, unificando saídas por falha de start, fechamento manual de painel,
    morte de terminal ou queda de sessão de agente;
  - Dispara um alerta único e desduplicado por `Dispatch` para a caixa postal do coordenador, informando causa, recursos
    deixados para trás e comando sugerido de retentativa;
  - Atualiza `worker-read` e `worker-show` para exibirem `never started: <reason>` em vez do genérico `has no agent terminal`.
- **Tipo de mensagem nativo `notice` na orquestração (`#40972`):**
  - Cria o tipo armazenado `notice` para despachos entre agentes, tornando-o o padrão para qualquer envio com `--to` sem tipo explícito;
  - Exibe no worker a faixa informativa `(notice)` acompanhada de `[For your information: no reply needed.]`, eliminando comandos
    espúrios de reply e deixando claro que não é exigida resposta imediata;
  - Reorganiza a tipologia de mensagens entre agentes em três categorias principais: `notice` (informativa), `question` (pergunta/resposta)
    e `handoff` (transferência de responsabilidade).
- **Desengasgo de filas de relay para perguntas remotas (`#40977`, resolve `#40968`):**
  - Registra a pergunta remota em `remote_questions` também no fluxo de `orchestration send --type question` em servidores pareados,
    permitindo que a resposta do coordenador seja confirmada e desobstrua a entrega de mensagens posteriores.
- **Resiliência pós-restart e recuperação de terminais (`#40967`, `#40963`, `#40949`):**
  - Permite interromper e despachar follow-up para workers de chat cujo processo tenha sido interrompido com a aplicação;
  - Notifica formalmente perda de pareamento quando um servidor pareado for desconectado ou removido.
- **Substituição de subshell no profile do Claude (`#40962`, resolve `#40956`):**
  - Substitui o subshell intermediário no wrapper do Claude por `exec`, garantindo que o executável do Claude assuma diretamente
    o primeiro plano do grupo de processos do PTY.
- **Encerramento de loop de busca de correio remoto quando ocioso (`#41426`, STA-14936):**
  - Finaliza o loop contínuo de pull de mensagens em servidores pareados assim que todas as conexões de Run associadas terminam,
    evitando que requisições vazias continuem rodando indefinidamente (~180 requisições/hora por servidor).
- **Leitura preguiçosa da saída final de terminal apenas para workers (`#41424`, STA-14935):**
  - Defer a reconstrução das últimas 15 linhas do buffer (até 2.000 linhas ou 256 KB) para o momento em que um relatório de saída
    de worker for efetivamente gerado, eliminando trabalho de CPU desnecessário no fechamento de terminais comuns.
- **Liberação de bookkeeping de turnos no encerramento de chats (`#41423`, STA-14934):**
  - Descarta as entradas de rastreamento de turnos no `worker stop reporter` quando um chat é fechado, estancando o vazamento
    de memória em sessões de longa duração.
- **Encerramento automático de cartões de aprovação órfãos no arranque (`#41422`, STA-14933):**
  - Durante o startup, identifica e encerra cartões de aprovação de chat cujas respostas já foram registradas antes de uma queda ou restart,
    impedindo que cartões sem resposta fiquem abertos eternamente na interface do coordenador.

## O que fazer

1. Incorporar no `brza-studio` o manipulador `reportWorkerTurnStop` com motivo `lost` para que o coordenador em sessões multiagente
   seja notificado prontamente caso subagentes morram ou sofram falhas de terminal (`#40983`).
2. Adotar a tipologia `notice` como padrão em envios interagentes na CLI e biblioteca de orquestração do BrzA (`#40972`).
3. Aplicar o encerramento do loop de correio remoto (`#41426`) e a leitura sob demanda da cauda de terminal de workers (`#41424`).
4. Limpar o bookkeeping de chats fechados (`#41423`) e encerrar aprovações órfãs no startup (`#41422`).
5. Aplicar o patch de desobstrução de relay para perguntas de workers remotos (`#40977`).
6. Assegurar que scripts de startup do Claude executem com substituição direta de processo (`exec`) em perfis shell (`#40962`).
