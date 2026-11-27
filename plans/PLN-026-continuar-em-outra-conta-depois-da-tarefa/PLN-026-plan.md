---
status: in_progress
phase: execution
origin: request
description: O chat que bateu no limite troca de conta e continua na conta nova quando a tarefa em segundo plano termina, sem perder o resultado dela.
ready: sim
estimate_h: 20.5
executed_h: 1
remaining_h: 10
scope:
  - brza-studio
opened: 2026-11-26
owner: Anderson
priority: high
tags:
  - chat
---

# PLN-026: O Continuar em outra conta espera a tarefa em segundo plano e continua na conta nova

- **Retomar:** fase 1 (P1–P3) e o código do P5 feitos; R9 respondida; os consertos da revisão da fase 1 (A1–A5) em curso na `pln-026-p5`, na branch dela (X14); depois revisão da parte nova, CI, push, DMG, C1 e C2. P6.2 espera pedido de Anderson.
- **Dividido:** [PLN-026 — Desenho](PLN-026-design.md)

## Pedido

- **Origem:** pedido livre, na sessão do workstream `studio` de 2026-11-26, depois do
  [sync das v1.4.263 e v1.4.278](../../work/worklogs/2026-11-26-sync-das-v1-4-263-e-v1-4-278-do-upstream.md).
  O botão é o P79 do PLN-001 ([o worklog do P79](../../work/worklogs/2026-11-02-pln-001-p79-continuar-em-outra-conta-e-retomar-por-padrao.md)).

"o \"Continuar em outra conta\" deixou de funcionar após o sync"

### Cobertura

| Origem     | Critério de aceite                                                                                                                         | Passo  | Teste (nível)                                                                                       |
| :--------- | :----------------------------------------------------------------------------------------------------------------------------------------- | :----- | :-------------------------------------------------------------------------------------------------- |
| `Pedido 1` | Num chat que segue a seleção, com tarefa em segundo plano, o Continuar em outra conta continua na conta escolhida, sem bater no limite de novo | P2, P3 | `structured-agent-session-account-switch.brza.test.ts` de `it.fails` para `it` (unidade); C1 (manual) |
| `R3.1`     | O host continua sozinho quando a tarefa termina, sem perder o resultado dela                                                                | P2     | casos 1, 2 e 6 de D2 (unidade)                                                                      |
| `R4.1`     | Se o acordar não vem em 30 s, a continuação leva o resultado da tarefa                                                                      | P2     | caso 10 de D2 (unidade)                                                                             |
| `R4.2`     | A tarefa que não termina em 30 min encerra a espera com aviso                                                                               | P2, P3 | caso 9 de D2 (unidade)                                                                              |
| `R4.3`     | O Cancelar da linha, o Stop, fechar o chat e a seleção voltar cancelam o pedido                                                             | P2, P3 | casos 4 e 5 de D2 (unidade)                                                                         |
| `R4.4`     | Uma mensagem nova durante a espera não cancela o pedido                                                                                     | P2     | caso de D2 (unidade), condicionado à sonda (P1)                                                     |
| `R5.1`     | A linha de limite mostra "Vai continuar em {conta} quando a tarefa em segundo plano terminar", com Cancelar                                 | P3     | teste do renderer (unidade); C1 (manual)                                                            |
| `R5.2`     | O chat fixado não recusa nem perde o resultado com tarefa de fundo                                                                          | P5     | testes da fase 2 (unidade); C2 (manual)                                                             |
| `R5.3`     | O provável defeito do auto-continue do upstream fica provado ou descartado, numa issue                                                      | P6     | teste na issue (unidade)                                                                            |

### Fora de escopo

- **Persistir o pedido no journal SQLite.** O reinício do app corta a tarefa de fundo, e depois dele o Continuar da linha
  já vai à conta selecionada; persistir só pouparia um clique (Desenho, "O que ataquei"). Fica fora.
- **Copiar o transcript para a conta nova.** O perfil de cada conta liga `projects/` ao home padrão; a cópia não serve e
  arrisca histórico velho (R5 não perguntou; recomendação do Desenho, `D` não há).

## Restrições

- **Mudança mínima em arquivo do upstream.** O `structured-agent-session-host.ts` tem 18 commits do upstream desde
  2026-09-01: só linhas de montagem; o resto em `brza/`.

## Entrevista

### Rodada 1 — o sintoma (enviada 2026-11-26)

> **Apresentado antes:** o caminho do botão (aparecer, `agentSession.options`, a troca, o Continuar) e que o conserto do
> PR #1 (`0849f8b4253`) só tirou o `try/finally` de dentro dos componentes.

Respondida em 2026-11-26.

1. **O que acontece.** Opções: o botão não aparece; aparece e dá erro; troca, mas não continua; nada acontece ao clicar.
   **Resposta:** "Troca, mas não continua".

### Rodada 2 — o caso (enviada 2026-11-26)

> **Apresentado antes:** um `implementer` derrubou três hipóteses com teste (o Continuar sai calado; falta o sinal de
> "o chat mudou de conta"; retoma na conta antiga) e deixou três suspeitos (histórico na outra conta; troca descartada
> calada; tarefa em segundo plano). Testes de guarda em `brza-studio@bb137633c35`.

Respondida em 2026-11-26.

1. **Na tela.** **Resposta:** "Responde e bate no limite de novo".
2. **Conta do chat.** **Resposta:** "Seguia a selecionada".
3. **Tarefa em segundo plano.** **Resposta:** "Sim".

### Rodada 3 — o comportamento (enviada 2026-11-26)

> **Apresentado antes:** a causa provada — com trabalho em segundo plano aberto ou devendo acordar o lead, o host mantém o
> agente na conta antiga de propósito (upstream #45478), e a continuação vai para ele. Teste `it.fails` em
> `brza-studio@b5573520d9d`. O chat fixado recusa com tarefa aberta e perde o acordar com tarefa terminada.

Respondida em 2026-11-26.

1. **O que o botão faz com tarefa aberta.** Opções:
   - avisar e não continuar (recomendada) — custo: pouco código no renderer, um sinal do host e as strings; se paga: agora;
   - mover o chat de fato, fixando-o — custo: o chat fica fixado, ignorando a seleção; se paga: se o botão deve sempre mover;
   - forçar a troca na hora — custo: a tarefa morre, e muda código que protege trabalho no upstream; se paga: só se continuar
     na hora vale mais que a tarefa;
   - trocar e continuar quando a tarefa acabar — custo: desenho novo no host; se paga: se esperar é aceitável.

   **Decidido — "Trocar e continuar quando a tarefa acabar".**

### Rodada 4 — o comportamento do desenho (enviada 2026-11-26)

> **Apresentado antes:** o desenho H1 do `designer` ([Desenho](PLN-026-design.md)): o pedido fica em memória no host,
> espera o trabalho acabar e manda a continuação comum, que já troca a conta pelo caminho do envio; sonda de ~30 min
> antes de implementar.

Respondida em 2026-11-26.

1. **Como o resultado da tarefa chega à conta nova.** Opções:
   - dois turnos, com rede de segurança (recomendada) — custo: ~40 linhas e a sonda; se paga: no primeiro caso em que a CLI
     não acorda numa conta esgotada;
   - só os dois turnos — custo: zero; se paga: só se a sonda provar que a CLI sempre acorda;
   - um turno só na conta nova — custo: ~60 linhas e corrida com o acordar; se paga: nunca, enquanto a recomendada cobrir.

   **Decidido — "Dois turnos, com rede de segurança (Recomendado)".**

2. **Tarefa que nunca termina.** Opções:
   - espera sem prazo, com Cancelar (recomendada) — custo: nenhum; se paga: agora;
   - prazo de 30 min e aviso — custo: ~20 linhas, um texto e um teste; se paga: quando uma tarefa esquecida segurar o pedido.

   **Decidido — "Prazo de 30 min e aviso".** O desfecho no prazo ficou na R7.2.

3. **O que cancela o pedido** (múltipla). Opções: o Cancelar da linha; o Stop; fechar o chat; a seleção voltar à conta
   antiga — todas recomendadas, cada uma de ~3 a ~15 linhas, que se pagam agora.

   **Decidido — as quatro.**

4. **Mensagem nova durante a espera.** Opções:
   - cancela o pedido (recomendada) — custo: ~5 linhas; se paga: agora;
   - não cancela — custo: zero, mas depende de a mensagem ficar no transcript (F9); se paga: depois da sonda, se F9 valer.

   **Decidido — "Não cancela".** Condicionado à sonda (P1): se F9 cair, volta a rodada.

### Rodada 5 — o escopo (enviada 2026-11-26)

Respondida em 2026-11-26.

1. **A linha na espera.** Opções: texto na linha com Cancelar (recomendada; ~60 linhas, strings e 2 testes; se paga:
   agora); só um toast (~10 linhas, sem Cancelar; nunca, com o Cancelar escolhido).
   **Decidido — "Texto na linha + Cancelar (Recomendado)".**
2. **O chat fixado (P36).** Opções: fase 2 do mesmo plano (recomendada; ~+1 dia, quase todo em arquivo do fork; se paga
   no primeiro fixado com tarefa de fundo); issue à parte (zero agora); fica de fora (nunca).
   **Decidido — "Fase 2 do mesmo plano (Recomendado)".**
3. **O auto-continue do upstream numa troca pelo seletor.** Opções: issue com teste e reportar (recomendada; ~1 h); barrar
   no fork (~2 linhas num arquivo do upstream com 14 commits); nada.
   **Decidido — "Issue com teste e reportar (Recomendado)".**
4. **A sonda.** Opções: rede derrubada agora, conta real depois (recomendada; ~30 min); só com conta esgotada (a
   implementação para até lá); sem sonda (o comportamento real só aparece no uso).
   **Decidido — "Rede derrubada agora, conta real depois (Recomendado)".**

### Rodada 6 — o destino (enviada 2026-11-26)

Respondida em 2026-11-26.

1. **Onde mora o plano.** Opções: `PLN` no workstream `studio` (recomendada); seção num worklog de hoje (só se tudo
   fechasse hoje). **Decidido — "PLN no workstream studio (Recomendado)".**

### Rodada 7 — o corte e o fim do prazo (enviada 2026-11-26, em texto)

> **Apresentado antes:** a tabela P1–P6 com executor e estimativa (20,5 h; fase 1 P1–P4, ~11,5 h).

Respondida em 2026-11-26: "R7 recomendados, pode executar o plano".

1. **O corte.** Opções:
   - aceitar P1–P6 (recomendada) — custo: nenhum; se paga: na fase 1;
   - dividir P5 e P6 em plano próprio — custo: outro plano e outra entrevista; se paga: só se a fase 1 precisar fechar antes;
   - juntar P2 e P3 — custo: um commit maior; se paga: só numa sessão só.

   **Decidido — aceitar P1–P6.** É o aceite do plano.
2. **O fim do prazo de 30 min.** Opções:
   - encerrar o pedido e avisar na linha (recomendada) — custo: ~20 linhas e um teste; se paga: quando uma tarefa esquecida
     segurar o pedido;
   - avisar e continuar esperando — custo: o mesmo; se paga: se a tarefa é longa de propósito;
   - avisar, parar a tarefa e continuar — custo: perde a tarefa; se paga: nunca, pela R3.

   **Decidido — encerrar o pedido e avisar na linha.**

### Rodada 8 — os pontos do P5 e o relato ao upstream (enviada 2026-11-26)

> **Apresentado antes:** o D5 detalhado pelo P5 (a troca é o próprio disparo no fixado) e o P6 provado.

Respondida em 2026-11-26.

1. **O seletor do composer num fixado com acordar devido** (hoje para o agente e o resultado se perde). Opções:
   - recusar até o acordar (recomendada) — custo: ~5 linhas em arquivo só do fork e 1 teste; se paga: na primeira troca pelo
     seletor logo depois de uma tarefa terminar;
   - deixar como está — custo: zero; se paga: nunca;
   - adiar a troca também no seletor — custo: ~+30 linhas e um estado novo; se paga: só com muito uso do seletor com tarefa.

   **Decidido — "Recusar até o acordar (Recomendado)".**
2. **A troca recusada no disparo.** Opções:
   - passageira espera, definitiva encerra (recomendada) — custo: ~15 linhas e 1 texto; se paga: na primeira mensagem nova
     durante a espera;
   - encerrar em qualquer recusa — custo: ~5 linhas; se paga: só se mensagem nova na espera for rara.

   **Decidido — "Passageira espera, definitiva encerra (Recomendado)".**
3. **Abrir a issue no `stablyai/orca`.** Opções: abrir agora (publica num repositório de terceiros; se paga quando o upstream
   corrigir); ainda não (o rascunho fica na issue do fork). **Decidido — "Ainda não".** O P6.2 fica a pedido.

### Rodada 9 — a revisão da fase 1 (enviada 2026-11-26)

> **Apresentado antes:** a revisão da fase 1 — A1 (alta: o pedido some calado quando o disparo não acha o corte), A2 (qualquer
> `agentSession.cancel` derruba o pedido), A3 (a seleção voltar só cancela na publicação seguinte), A4 (casos sem prova) e A5
> (o módulo perto do `max-lines`). A1, A4 e o cartão de pergunta do A2 se consertam de todo jeito.

Respondida em 2026-11-27.

1. **O Stop de uma tarefa na faixa cancela o pedido?** Opções:
   - não, só o Stop do chat cancela (recomendada) — custo: ~4 linhas em arquivo só do fork e 1 teste; se paga: na primeira vez
     que alguém parar a tarefa para seguir logo;
   - qualquer Stop cancela — custo: zero, mas parar a tarefa derruba o pedido sem aviso; se paga: só se parar a tarefa quiser
     dizer "desisti".

   **Decidido — "Não, só o Stop do chat cancela (Recomendado)".**
2. **A seleção voltar tira a linha na hora?** Opções:
   - sim, na hora (recomendada) — custo: 1 a 2 linhas em arquivo do upstream e 1 teste; se paga: na primeira volta da seleção
     durante a espera;
   - deixar e abrir issue — custo: zero; a linha fica errada até 30 min. Se paga: nunca, se a seleção raramente voltar.

   **Decidido — "Sim, na hora (Recomendado)".**

## Desenho

### O que este desenho assume

- **R3.1:** o botão troca a conta e o host continua sozinho quando a tarefa termina.
- **R4.1:** dois turnos (o acordar na conta antiga, a continuação na nova), com o fallback de 30 s.
- **R4.2, R7.2:** prazo de 30 min; no fim, o pedido se encerra e a linha avisa, e o botão volta.
- **R4.3:** cancelam o Cancelar da linha, o Stop, fechar o chat e a seleção voltar à conta do agente.
- **R4.4:** mensagem nova não cancela, se a sonda confirmar F9.
- **R5.1–R5.4:** linha com texto e Cancelar; fixado na fase 2; issue do upstream; sonda com rede derrubada agora.

O Terreno, com as fontes `F1`–`F23`, as alternativas H2 e H3 e o que caiu estão em [PLN-026 — Desenho](PLN-026-design.md).

### D1 — O pedido adiado no host — `src/main/native-chat/agent-session-wire/brza/brza-deferred-usage-limit-continue.ts` (P2)

- **Origem:** R3.1, R4.2, R4.3, R4.4
- **Contexto:** o host mantém o agente na conta antiga enquanto há trabalho aberto ou acordar devido
  (`structured-agent-session-outgrown-child.ts:129-183`); nada o solta quando o trabalho acaba.

#### Como fica

- `arm({ sessionId, turnItemId })`, sob o `serialize` do host: sem agente, agente já na conta da seleção ou sem trabalho
  devido → `{ kind: 'now' }`; senão guarda `{ turnItemId, armedAt, account }` num `Map`, publica o status e devolve
  `{ kind: 'deferred' }`.
- Um timer de 2 s, ligado só enquanto há pedido. A cada volta: **cancela** se o chat fechou ou saiu do host, ficou fixado,
  a seleção voltou à conta do agente, houve Stop pessoal ou o Cancelar da linha; **descarta sem aviso** se não há mais corte
  (o acordar deu certo na conta antiga); **espera** enquanto há trabalho aberto ou acordar devido; **encerra com aviso** aos
  30 min (R4.2, R7.2): o pedido sai do `Map`, o status leva `expired` e a linha avisa.
- Mensagem nova da pessoa não cancela (R4.4).
- `cancel`, `readState` e `dispose`; montado no `structured-agent-session-host.ts` em ~3 linhas.

### D2 — O disparo e a rede de segurança (P2)

- **Origem:** R4.1
- **Como fica:** quando o trabalho acaba e o acordar completa (com corte novo, no limite da conta antiga), o host envia o
  `usageLimitContinueMutation` do corte mais novo pelo mesmo `send` do auto-continue
  (`structured-agent-session-usage-limit-continue-message.ts:12-35`). O `retireOutgrownChild` do loop de entrega solta o
  agente, e o `startProviderChild` relança com `--resume` na conta da seleção. `superseded` conta como feito. **Fallback:**
  se a tarefa assentou há 30 s e o acordar não veio, o host para o agente e envia a continuação com o resultado da tarefa
  no corpo, no formato `<task-notification>` (id, estado, resumo, `output_file`).
- **Testes:** o `it.fails` vira `it`, dirigido pelo `arm`; casos: (1) tarefa terminada devendo o acordar → continua em
  `/homes/b`; (2) tarefa aberta com handle do provider → espera e depois vai a B; (3) sem retenção → `now`; (4) Cancelar pela
  RPC; (5) Stop, chat fechado, seleção de volta; (6) o acordar dá certo na conta antiga → cai sem aviso; (7) o auto-continue
  chega antes → um envio só; (8) reinício; (9) prazo de 30 min; (10) fallback de 30 s; mais o caso de mensagem nova (R4.4).

### D3 — A RPC e a capacidade (P2)

- **Origem:** R3.1, R4.3
- **Como fica:** `agentSession.brzaContinueAfterWork` e o cancelar, com os params em `src/shared/rpc-contract/brza/`; a
  capacidade em `structured-agent-session-surface-capabilities.ts` (1 linha). Host sem a capacidade (mais velho ou remoto):
  o renderer faz o `onContinue()` de hoje.

### D4 — O status e a linha de limite (P3)

- **Origem:** R5.1, R4.2
- **Como fica:** o campo `brzaContinueAfterWork?: { account, since, expired? }` em `src/shared/agent-session/brza/`,
  espalhado no `structured-agent-session-status-summary.ts` (1 linha, como o `agent-session-status-account-switch.ts`). Em
  `BrzaContinueInOtherAccount.tsx` e no hook dele: no chat que segue a seleção, depois do `switchTo`, chama o `arm`; com
  `deferred`, cancela o auto-continue agendado do corte e a linha mostra "Vai continuar em {conta} quando a tarefa em
  segundo plano terminar", com Cancelar; com o prazo vencido, o aviso. Strings nos catálogos do desktop.

### D5 — O chat fixado (P5)

- **Origem:** R5.2
- **Contexto:** o `commitAccountSwitchRecord` só move o record com o lease solto, sem processo
  (`src/main/runtime/agent-session-account-switch-record.ts:19-25`); por isso o `switchAccount` recusa com trabalho aberto
  (`structured-conversation-command-admission.ts:77-83`) e para o agente sem olhar o acordar devido
  (`operations/structured-agent-session-account-switch.ts:101-111`). No fixado, a troca é o próprio disparo.
- **Como fica:**
  1. **O botão:** no fixado, com a capacidade, **primeiro** o `arm` com `{ sessionId, turnItemId, accountId, account }`;
     `now` → o caminho de hoje (`switchTo` + `onContinue`); `deferred` → cancela o auto-continue agendado do corte e a linha
     mostra a espera de D4.
  2. **O `arm`:** sem agente, sem trabalho devido ou já fixado na conta alvo → `now`; senão guarda o pedido com
     `target: { kind: 'pin', accountId, account, pinAtArm, callerKey }` → `deferred`. Nada roda no `arm`.
  3. **A espera:** o timer de D1; cancela pelo Cancelar da linha, o Stop, o chat fechado, o prazo de 30 min e **o pino
     mudar desde o `arm`** (no lugar de "a seleção voltou").
  4. **O disparo** (o trabalho acabou e o acordar completou em A, com corte novo), fora do `serialize` do timer: lê o fence;
     chama `host.conversationCommands.switchAccount` com envelope cunhado no host (o `prepareAccountSwitch` copia o
     transcript, o pino vai a B, a divisória "Account switched - {conta}" vem depois do acordar); envia o
     `usageLimitContinueMutation` do corte mais novo com o fence lido antes da troca; o `startProviderChild` lança em B pelo
     pino com `--resume`. `superseded` conta como feito. O fallback de 30 s (X1) é o mesmo disparo, com o resultado no corpo.
  5. **Onde:** o `target` (`selection`/`pin`) e o disparo do fixado na peça do P2 (~50 linhas, ou um
     `brza-deferred-continue-pinned.ts` ao lado); `accountId?`/`account?` nos params da RPC de D3; nenhuma linha nova no
     `structured-agent-session-host.ts` além das do P2; o renderer como em (1).
  6. **R8.1:** o seletor do composer recusa com "Wait for background tasks to finish before using this command." enquanto
     o acordar é devido (`structuredAgentSessionChildOwesWork` antes do `stopAgent`, em arquivo só do fork).
  7. **R8.2:** no disparo, recusa passageira (`turnActive`, `messagesUnsettled`) espera a próxima volta; definitiva
     (`unknown-account`) encerra o pedido e a linha avisa, como no fim do prazo.
  8. **Os params** (X7): `accountId?` no `BrzaContinueAfterWorkParams` e o `target` (`selection`/`pin`) no pedido.

### D6 — O auto-continue do upstream numa troca pelo seletor (P6)

- **Origem:** R5.3
- **Como fica:** issue no workstream `studio` com o teste que prova ou descarta F14 (a varredura do auto-continue atribui
  a conta pela seleção e não olha a retenção — `structured-agent-session-usage-limit-account-hold.ts:95-99`,
  `structured-agent-session-usage-limit-disposition.ts:25-40`); provado, reportar ao upstream.

## Passos

### P1 — A sonda da CLI

Executa D2 (F9, F10) · executor: sessão do `brza-studio`

Estimado: 0.5 h · Executado: 0.5 h

- [x] **1.** Rodar a CLI do Claude em `stream-json` com uma tarefa em segundo plano (`sleep 30`), derrubar a rede antes de
  a tarefa acabar e conferir no `.jsonl` se o turno do acordar começa (F10) e se a notificação fica no transcript (F9).
- [x] **2.** Registrar no plano; se F9 cair, a R4.4 volta à rodada. A prova com conta esgotada de verdade fica para C1.

**Evidência:** CLI 2.1.322, `-p --input-format stream-json --output-format stream-json`, `sleep 30` em segundo plano, rede
derrubada só para o processo por um proxy `HTTPS_PROXY` local. **F10 vale:** aos 30 s, `system/task_notification`, um
`system/init` novo 0,1 s depois, 10 `system/api_retry` em ~3 min e `result` `is_error: true` (ECONNRESET). **F9 vale:** o
registro `user` `origin.kind: task-notification` foi gravado às 01:42:52.064Z, antes da primeira `api-request`
(01:42:52.084Z). A mensagem da pessoa durante a queda também ficou no transcript, e o `--resume` num processo novo viu as
duas (a R4.4 fica de pé). O texto da saída não vem na notificação, só o `output-file`. Artefatos no scratch da sessão
`pln-026-fase-1`, fora do repositório.

### P2 — O pedido adiado, o disparo e a RPC no host

Executa D1, D2, D3 · executor: sessão do `brza-studio`, branch `fix/pln-026-continuar-em-outra-conta` (a partir de
`fix/continue-other-account`, que tem os testes de guarda `bb137633c35` e `b5573520d9d`)

Estimado: 7 h · Executado: 0.3 h

- [x] **1. Teste que falha:** o `it.fails` de `structured-agent-session-account-switch.brza.test.ts` reescrito pelo `arm`.
- [x] **2. Implementar** D1, D2 e D3.
- [x] **3. Os casos de D2** — unidade, por caminho.
- [x] **4.** `pnpm typecheck`, `pnpm lint`, commit.

**Evidência:** `brza-studio@ff5ce19b54a` (branch `fix/pln-026-continuar-em-outra-conta`, no origin como `fix/pln-026-fase-1`; reescrito duas vezes, X9 e X11). Novos em `brza/`:
`brza-deferred-usage-limit-continue.ts` (264 linhas), `brza-continue-after-work-{wake-up,status,wiring}.ts`, a RPC
`agentSession.brzaContinueAfterWork`/`brzaCancelContinueAfterWork` e a capacidade
`agent-session.structured.brza-continue-after-work.v1`. `vitest` nos dois `.brza.test.ts` novos → 13 passed; regressão em 7
arquivos (`recovery/`, `account-switch` do host e de `operations/`, `usage-limit-queue-recovery`, status) → 68 passed;
mutação com o disparo desligado derruba os casos 1, 2, 10 e R4.4. `pnpm typecheck` verde; lint só com o
`check:code-quality:changed` do ambiente (0 achados com `ORCA_CODE_QUALITY_BASE=9eef46284d8`).

### P3 — A linha de limite na espera

Executa D4 · executor: sessão do `brza-studio`

Estimado: 3 h · Executado: 0.2 h

- [x] **1. Teste que falha** do renderer: a linha na espera, o Cancelar, o aviso do prazo, o host sem a capacidade.
- [x] **2. Implementar** D4 e as strings.
- [x] **3.** Testes por caminho, typecheck, lint, gates de idioma, commit.

**Evidência:** `brza-studio@0f866eff56a` (era `6741d0471b9`, X11): `brza/use-brza-continue-after-work{,-status}.ts`, `brza/BrzaContinueAfterWorkLine.tsx`,
`BrzaContinueInOtherAccount.tsx` e o hook; no upstream, só o tipo de 2 linhas em `NativeChatUsageLimitActions.tsx`. Strings
em en, pt, es, fr, ja, ko, zh ("Vai continuar em {{account}} quando a tarefa em segundo plano terminar", "Cancelar", o aviso
do prazo, "Dispensar"). `vitest`: os 4 do PLN-026 → 23 passed; `native-chat/usage` e `native-chat/brza` → 156 passed; host →
68 passed. Os seis gates de idioma com saída 0; `pnpm typecheck` verde; lint só com o `check:code-quality:changed` do ambiente
(passa com `ORCA_CODE_QUALITY_BASE=9eef46284d8`).

### P4 — Revisão, CI e push

Executa P2, P3 · executor: a sessão que conduz (`reviewer`, CI `node-next-compat.yml`)

Estimado: 1 h · Executado: — h

- [ ] **1.** Revisão adversária; achados com destino.
- [ ] **2.** CI da branch igual à `master`; fast-forward e push; DMG para C1.

**Evidência:**

### P5 — Fase 2: o chat fixado

Executa D5 · executor: sessão do `brza-studio`

Estimado: 8 h · Executado: — h

- [x] **1.** Detalhar D5 (rodada se houver ponto sem lastro). Ver o D5; os pontos foram à R8.
- [ ] **2.** Teste que falha, implementação, testes, commit, revisão, CI e push. Host, RPC, R8.1, R8.2 e renderer feitos
  sobre a fase 1 final (`df6c9619be8`, `0e585b4d06a`); em curso, na mesma branch, os consertos da revisão da fase 1 (A1–A5,
  R9); depois revisão da parte nova, CI e push junto com a fase 1.

**Evidência (parcial):** `brza-studio@64d47dc5c56` (branch `fix/pln-026-p5-fixado`):
`structured-agent-session-account-switch-pinned.brza.test.ts`, dois `it.fails` — com tarefa aberta, hoje recusa
`backgroundTasksRunning`; com tarefa terminada devendo o acordar, hoje para o agente antes do acordar →
`Tests 2 expected fail (2)`. Depois, `brza-studio@af45663b8cb` (merge do P2) e `brza-studio@2805db580ea`: `accountId?` nos
params (X7), `brza-continue-after-work-pin.ts` (novo), o disparo `switchThenContinue`, R8.1 no
`operations/structured-agent-session-account-switch.ts` e R8.2; `vitest` em 5 arquivos (o fixado, os da fase 1 e os de troca
do upstream) → 33 passed; o caso da R8.1 cai sem a recusa. `pnpm typecheck` verde. Executado até aqui: 3 h.

### P6 — A issue do auto-continue do upstream

Executa D6 · executor: sessão do `brza-studio` e a sessão que conduz

Estimado: 1 h · Executado: — h (0,5 h até aqui)

- [x] **1.** Teste que prova ou descarta F14; issue no workstream `studio` com o resultado.
- [ ] **2.** Provado: reportar ao upstream (a pedido de Anderson).

**Evidência:** F14 provado. `brza-studio@c3289c12c9a` (branch `test/pln-026-p6-auto-continue`):
`structured-agent-session-usage-limit-account-switch.brza.test.ts:26`, `it.fails` → "1 expected fail"; sem o `it.fails`,
`expected { handed: 1, agent: 'kept on A' } to not deeply equal …`. Controles: sem a troca, nada sai antes do reset; sem o
acordar devido, o agente é trocado. Issue:
[O auto-continue entrega a continuação ao agente retido na conta esgotada](../../work/issues/o-auto-continue-entrega-ao-agente-retido-na-conta-esgotada.md),
com o rascunho do relato ao upstream.

## Regressão

- **O Continuar em outra conta sem tarefa em segundo plano** continua como hoje (troca e continua na hora): caso 3 de D2 e
  o teste `NativeChatUsageLimitContinueAfterSwitch.brza.test.tsx` (`bb137633c35`).
- **O auto-continue e o Continuar comum da linha de limite** do upstream: os testes de `native-chat/usage` e
  `agent-session-wire/recovery`, por caminho.

## Pendências conhecidas

- [O auto-continue entrega a continuação ao agente retido na conta esgotada](../../work/issues/o-auto-continue-entrega-ao-agente-retido-na-conta-esgotada.md)
  — de P6; o reporte ao upstream espera o pedido de Anderson.

## Casos manuais

| ID  | Critério                                                    | Passos                                                                                                                                      | Esperado                                                                                                     | Observado | Veredito |
| :-- | :---------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------ | :----------------------------------------------------------------------------------------------------------- | :-------- | :------- |
| C1  | `Pedido 1`, `R5.1`                                          | Num chat que segue a seleção, com uma tarefa em segundo plano rodando, bater no limite; escolher outra conta em "Continue in another account" | A linha diz que vai continuar na outra conta; quando a tarefa termina, o chat continua lá, com o resultado dela | —         | —        |
| C2  | `R5.2`                                                      | O mesmo com um chat fixado numa conta                                                                                                       | Idem, sem recusa                                                                                             | —         | —        |

## Desvios

- **X1 — A rede de segurança de 30 s olha o começo do turno do acordar.** O P1 mostrou que o acordar em nova tentativa
  leva ~3 min para completar; contar 30 s até completar dispararia o fallback no meio do turno. Fica: dispara só se não há
  turno ativo do provider 30 s depois do `settledAt`. Afeta P2 e D2 (o caso 10).

- **X2 — O host ficou no limite de linhas.** O `structured-agent-session-host.ts` estava em 299/300; a montagem virou um campo
  de 1 linha, o `dispose` e o Stop nas linhas que já existiam, e a reexportação no `structured-agent-session-host-background.ts`.
  O host fica em 300/300: o próximo sync que somar uma linha estoura o `max-lines`. Afeta P2 e a Restrição.
- **X3 — O Stop vem pelo `host.cancel`**, não pelo `readStopping` no timer, que só vale durante o `working`. Afeta D1.
- **X4 — O status leva `turnItemId`** além de `{ account, since, expired? }`, para a linha casar com o corte. Afeta D4.
- **X5 — O fallback leva id, estado e resumo da tarefa, sem o `output_file`**, que a `AgentChildWorkView` não tem. Afeta D2.
- **X6 — Os casos 2 e 7 de D2:** o 2 simula o trabalho aberto pelo `hasOpenDispatch` (o rig não tem o handle do provider); o
  7 aceita os dois desfechos com um envio aceito só (o auto-continue moveu antes, ou `continuationSuperseded`).
- **X7 — Os params do D3 fecharam sem o `accountId`/`target` do fixado**; o recado ao P2 chegou depois do commit. O P5
  acrescenta os campos opcionais na mesma RPC (arquivo só do fork), sem abrir outra.

- **X8 — A R8.2, lida assim:** definitivas são as recusas de conta do `prepareAccountSwitch`
  (`claudeAccountFolderMissing`, `claudeAccountSetupFailed`); toda outra espera a próxima volta, limitada pelo prazo de 30 min,
  que no fixado corre antes do disparo. Quando a conta recusa, o agente já foi parado pelo `switchAccount` e o chat fica no
  pino de antes, em repouso; o status leva `expired` + `accountUnavailable`.
- **X9 — O timer de 2 s do D1 virou sinal empurrado.** O `setInterval` esbarrava no `check:recurring-timer-ratchet`; o pedido
  assina o `subscribeStatus` do host e confere a cada publicação de status, com timers de disparo único só para os 30 min e
  os 30 s. Entrou como fixup no P2; sem mudança no baseline (`check-recurring-timer-ratchet.mjs` → OK). Afeta D1 e o P5.
- **X10 — A linha da espera vive no componente do fork** (`BrzaUsageLimitContinueInOtherAccount`), no lugar do botão; o
  `NativeChatUsageLimitRow.tsx` do upstream não mudou. O aviso do prazo ganhou "Dispensar", que chama o cancelar. Os
  catálogos `tr` e `zh-Hant` não levam as strings, como no P79. Afeta D4.

- **X11 — A branch da fase 1 foi reescrita de novo depois de enviada.** Um recado atrasado (o ponto de extensão do fixado:
  `target?`, `accountId?`, `account?` opcional, o `Pending` com `target`, o dep `switchAccount`) entrou no P2 por
  `rebase --autosquash`: P2 `ff5ce19b54a`, P3 `0f866eff56a`. O `--force-with-lease` no origin foi barrado pelo classificador;
  a fase 1 foi ao origin como `fix/pln-026-fase-1`, e a `fix/pln-026-continuar-em-outra-conta` do origin ficou no
  `6741d0471b9` antigo. O P5 adota os nomes da fase 1.

- **X12 — A branch do P5 foi reconstruída sobre a fase 1 final** (`0f866eff56a`), em vez de mesclada, para não carregar as
  três versões da fase 1; os commits antigos ficam num backup local. O P5 adotou os nomes da fase 1 (`target`, `accountId`,
  o dep `switchAccount`).
- **X13 — O P5 achou e consertou o A1** (`withoutCut`): sem corte, o pedido espera a linha do limite quando o turno mais novo
  falhou; encerra calado se o turno deu certo ou se um envio pendente já continua o chat. A fixture da fase 1 ganhou `fail`
  e `limitRow`. Afeta D2.
- **X14 — A fase 1 e o P5 vão ao `master` juntos**, pela branch do P5: os consertos da revisão da fase 1 entram lá, e o P4
  (revisão, CI, push) cobre as duas.

## Worklogs

- 2026-11-26 — abertura: R1–R7, D1–D6, P1–P6 aceitos; execução autorizada. P1 fechado (X1); P2/P3, P5 e P6 em três
  sessões do `brza-studio` em paralelo.
  [O Continuar em outra conta depois do sync](../../work/worklogs/2026-11-26-continuar-em-outra-conta-depois-do-sync.md)

## Fechamento

- [ ] Todo passo `[x]` com evidência, ou `[-]` com motivo.
- [ ] Todo achado com destino que existe.
- [ ] Um resumo por commit ou PR do `brza-studio` da entrega, com o link do plano.
- [ ] O durável saiu para a casa dona e está em `## Decisões` e `## Documentação`.
- [ ] As decisões que o plano respondeu estão `done`, citando a rodada.
- [ ] `status: done`, `phase: closed` e `completed` no frontmatter.
