# PLN-026 — Desenho

O levantamento e o desenho completos do consultor (`designer`), de 2026-11-26, como foram devolvidos. O vigente está no
`## Desenho` do [plano](PLN-026-plan.md); aqui ficam o Terreno com as fontes (`F1`–`F23`), as alternativas e o que caiu.


Worktree `~/Projects/brza-studio/.worktrees/continue-other-account`, branch `fix/continue-other-account`, sobre a
`master` `9eef46284d8`. Ponto de partida, como Anderson respondeu em 2026-11-26: "Trocar e continuar quando a tarefa
acabar — o botão troca a conta e o host continua sozinho depois que a tarefa termina." Ficaram recusadas: avisar e não
continuar, mover fixando, forçar a troca matando a tarefa.

## Levantamento

**A retenção e o envio:**
- O ramo da troca (`accountSwitch`) mantém o agente quando há trabalho aberto ou um acordar devido
  (`structured-agent-session-outgrown-child.ts:129-160`). O ramo do envio faz o mesmo, `:162-183`.
  [F1 · lido · 95]
- O envio que chega com o agente retido vai a esse agente: `retained === true` no `enqueue`
  (`structured-agent-session-input-handover.ts:96-103`, "a send that joins work still owed goes to this child").
  [F2 · lido · 90]
- Com a tarefa terminada que deve o acordar, depois do `releaseIdleChatsOnOtherAccount` e do envio da continuação,
  o envio volta `ok`, com `fence: 1`, e o agente fica em `/homes/a` (sonda no rig do `it.fails`, apagada depois).
  [F3 · rodado · 95]
- Na mesma sonda, uma visão gravada `working` sem handle aberto do provider não retém: o agente foi para `/homes/b`,
  `fence: 2`. A tarefa "aberta" vem da evidência do provider, o `open.hasOpen`
  (`structured-agent-session-status-ownership.ts:235-237`), e não da visão gravada. [F4 · rodado · 90]
- O `releaseIdleChatsOnOtherAccount` só roda quando uma seleção se aplica (`provider-account-services.ts:57-60`).
  Nada o roda de novo quando o trabalho devido acaba; o agente sai só no envio seguinte. A premissa é que esse é o
  único chamador. [F5 · lido · 85]

**O acordar do lead:**
- O `owesWakeUp` é verdadeiro enquanto existe um `settledAt` maior que o `newestTurnCompletedAt`
  (`structured-agent-session-outgrown-child.ts:31-38`). O `newestTurnCompletedAt` é o `completedAt` do turno mais
  novo, qualquer que seja o desfecho (`journal-sql-work-read.ts:149`). A premissa é que o turno do acordar, mesmo
  quando falha no limite, vira esse turno mais novo. [F6 · lido · 85]
- O acordar é um turno da própria CLI. O transcript ganha um registro `user` com `origin.kind: task-notification`,
  `turnOrigin: task_notification` e o `<output-file>` em `/private/tmp/claude-501/<projeto>/<sessão>/tasks/…`
  (`src/main/claude/__fixtures__/claude-plugin-recovery.json:2-24`). [F7 · lido · 90]
- O teste do upstream diz por que o agente fica: "A resumed agent is not reliably handed a finished task's result, so
  the wake-up keeps it" (`structured-agent-session-account-switch.test.ts:180-190`). [F8 · lido · 95]
- Sem fonte: o registro `task-notification` entra no transcript antes da chamada à API, também quando a API recusa
  pelo limite. [F9 · inferido · 60]
- Sem fonte: a CLI tenta o acordar mesmo quando o último turno acabou no limite de uso. Se não tentar, o
  `owesWakeUp` fica verdadeiro até o processo morrer, e o caso do relato de Anderson é exatamente esse.
  [F10 · inferido · 50]
- O que o upstream faz quando o acordar bate no limite: grava um corte de limite no turno iniciado pelo provider, como
  em qualquer turno. A linha aparece e, com o auto-continue ligado, entra na agenda. [F11 · inferido · 70]

**A continuação e o auto-continue:**
- A continuação é recusada como `superseded` quando ela entraria na fila, ou quando o corte mais novo não é o
  `continuationOfTurnItemId` (`journal-sql-send-admission.ts:165-172`). [F12 · lido · 90]
- O botão chama `switchTo(accountId)` e depois `onContinue()`. Este cancela o auto-continue agendado desse corte e
  envia (`BrzaContinueInOtherAccount.tsx:16-30` e `:48-52`). [F13 · lido · 95]
- A varredura do auto-continue atribui a conta pelo `launchAccountHome`, que lê a seleção, e não pelo
  `child.accountHome` (`structured-agent-session-usage-limit-account-hold.ts:95-99`). O `usageLimitCutContinuable`
  não olha a retenção (`structured-agent-session-usage-limit-disposition.ts:25-40`). Daí sai que, depois de uma troca
  de seleção sem o botão, com tarefa de fundo, o auto-continue manda a continuação ao agente retido na conta
  esgotada — o mesmo defeito, no upstream. [F14 · inferido · 70]
- O `usageLimitContinueMutation` monta no host a mesma continuação do auto-continue
  (`structured-agent-session-usage-limit-continue-message.ts:12-35`). [F15 · lido · 95]

**O chat fixado:**
- O caminho fixado recusa com `backgroundTasksRunning` quando há `liveFence` e `childWork.open`
  (`structured-conversation-command-admission.ts:77-83`). Depois para o agente sem olhar o `owesWakeUp`
  (`operations/structured-agent-session-account-switch.ts:101-111`). [F16 · lido · 95]
- O arquivo da operação fixada é só do fork: nenhum commit do upstream o toca (`git log --format=%ae`).
  [F17 · rodado · 95]

**O histórico na conta nova:**
- O setup do perfil liga `projects/` e `tasks/` do perfil ao home padrão
  (`claude-profile-history.ts:16-26` e `:63-77`, chamado em `claude-profile-setup.ts:53-55`). O transcript aparece
  em toda conta gerida. [F18 · lido · 90]
- O `claudeLaunchResumesTranscript` recusa com `historyInOtherAccount` quando o transcript está só em outra conta
  (`claude-structured-launch-home.ts:53-62`). [F19 · lido · 95]
- O `copyClaudeTranscriptsToAccount` pula o alvo que já tem o transcript (`claude-account-switch-transcript.ts:31-33`).
  Uma cópia antiga fica, sem atualizar. [F20 · lido · 95]

**O reinício e os precedentes:**
- No fechamento do app, o host para os agentes, e o trabalho de fundo é cortado: `leadDone`, "only its background
  work was cut" (`structured-agent-session-restart-resume-contract.ts:12-23` e `:34-37`). A premissa é que o
  teardown para todo agente do host. [F21 · lido · 80]
- Já há precedente para o campo do BrzA no resumo de status
  (`src/shared/agent-session/brza/agent-session-status-account-switch.ts:1-8`, espalhado em
  `structured-agent-session-status-summary.ts:120-127`). Há também para a capacidade de método novo
  (`structured-agent-session-surface-capabilities.ts:53`). [F22 · lido · 90]
- Commits do upstream desde 2026-09-01, sem merges:

  | Arquivo | Commits |
  | :------ | ------: |
  | `structured-agent-session-host.ts` | 18 |
  | `structured-agent-session-usage-limit-continue.ts` | 14 |
  | `structured-agent-session-status-summary.ts` | 13 |
  | `NativeChatUsageLimitActions.tsx` | 13 |
  | `structured-agent-session-host-delivery.ts` | 6 |
  | `structured-agent-session-outgrown-child.ts` | 5 |
  | `structured-agent-session-delivery-loop.ts` | 3 |
  | `structured-agent-session-surface-capabilities.ts` | 3 |
  | `structured-agent-session-outgrown-retirement.ts` | 1 |

  [F23 · rodado · 95]

## Desenho recomendado — H1: pedido adiado no host, em memória, disparado pelo host

**A ideia:** adiar o envio, e não a troca. Quando o trabalho devido acaba, a continuação comum sai pelo caminho do
envio. Esse caminho já tira o agente da conta antiga e o relança na conta selecionada (F1, `:175`, e os testes de
`bb137633c35`).

### O fluxo

1. **No renderer**, chat que segue a seleção (`use-brza-continue-in-other-account.ts:97-103`): o `switchTo` troca a
   seleção, como hoje. Em seguida, se o host anuncia a capacidade nova, chama
   `agentSession.brzaContinueAfterWork { sessionId, turnItemId }`. Sem a capacidade (host mais velho ou remoto), segue
   o `onContinue()` de hoje.
2. **No host**, o `arm`, sob o `serialize(sessionId)`:
   - lê o agente: se ele não existe, já está na conta da seleção ou não deve trabalho
     (`structuredAgentSessionChildOwesWork`), devolve `{ kind: 'now' }`, e o renderer chama o `onContinue()` de hoje;
   - senão, guarda `{ turnItemId, armedAt, settledSeenAt? }` num `Map`, publica o status e devolve
     `{ kind: 'deferred' }`. O renderer cancela o auto-continue agendado do corte (F13), para a varredura não mandar a
     continuação ao agente retido.
3. **A espera:** um timer de 2 s, ligado só enquanto houver pedido, confere cada pedido sob o `serialize`:
   - **cancela** se o chat fechou ou saiu do host, se ficou fixado (`record.accountSwitch`), se a seleção voltou à
     conta do agente, se houve Stop pessoal (`readStopping`) ou pelos gatilhos da rodada R1.3;
   - **descarta calado** se o corte mais novo não existe mais, isto é, se o acordar deu certo em A porque o limite
     resetou (F12);
   - **espera** enquanto houver trabalho aberto (F4) ou acordar devido (F6).
4. **O acordar**, quando a tarefa termina: a CLI em A roda o acordar sozinha, com a notificação no transcript (F7),
   bate no limite e grava um corte novo (F11). O `owesWakeUp` cai (F6).
5. **O disparo:** sem trabalho devido, o host lê o corte mais novo e envia o
   `usageLimitContinueMutation({ sessionId, cut, at, expectedRuntimeFence })` pelo mesmo `send` do auto-continue
   (F15).
   - O loop chama o `retireOutgrownChild` (`structured-agent-session-delivery-loop.ts:202`). O ramo do envio vê a
     outra conta sem trabalho devido, para o agente, e o `startProviderChild` lança na conta da seleção com
     `--resume`. Esse turno em B lê o transcript, que tem a notificação, e a continuação: o resultado chega ao lead.
   - Uma resposta `superseded` vale como feita: a varredura do auto-continue chegou antes ao corte novo e já moveu o
     chat (F12).
6. **O fallback** do acordar que não vem (F10): se a tarefa assentou há mais de 30 s e o `owesWakeUp` segue verdadeiro
   sem turno novo, o host para o agente e envia a continuação com o resultado da tarefa no corpo — id, estado, resumo e
   `output_file` da visão do `AgentChildWorkView` —, no formato do `<task-notification>`.

### O estado e onde mora cada peça

- **`src/main/native-chat/agent-session-wire/brza/brza-deferred-usage-limit-continue.ts`** (novo): a classe com
  `arm`, `cancel`, `readState(sessionId)`, `dispose`, o timer e o fallback. Os deps são os mesmos do
  `usageLimit.start`: `serialize`, `send`, `publish` e `now`, além do `retainedWork`.
- **A RPC:** `agentSession.brzaContinueAfterWork`, num arquivo do BrzA, com os params em
  `src/shared/rpc-contract/brza/…`. A capacidade `brzaContinueAfterWork` vai em
  `structured-agent-session-surface-capabilities.ts`, como o `switchAccount` (F22).
- **O status:** o campo `brzaContinueAfterWork?: { account: string; since: number }` em
  `src/shared/agent-session/brza/`, espalhado no `status-summary`, como o `accountSwitch`.
- **O renderer:** em `BrzaContinueInOtherAccount.tsx` e no hook, a linha diz "Vai continuar em {conta} quando a tarefa
  em segundo plano terminar", com o botão "Cancelar".

### O que muda em arquivo do upstream

| Arquivo | Mudança | Conflito no próximo sync |
| :------ | :------ | :----------------------- |
| `structured-agent-session-host.ts` | ~3 linhas: construir, `dispose`, expor o `arm` e o `cancel` | Alto: 18 commits do upstream (F23) |
| `structured-agent-session-status-summary.ts` | 1 spread | Médio: 13 commits |
| O catálogo de RPC e o `rpc-params-catalog.generated.ts` | 1 a 2 linhas, mais o arquivo gerado | Baixo |
| `structured-agent-session-surface-capabilities.ts` | 1 linha | Baixo: 3 commits |

O `outgrown-child.ts`, o `delivery-loop.ts`, o `input-handover.ts` e o `usage-limit-continue.ts` não mudam.

[C1 · inferido · 75]

**Custo:** ~150 linhas no módulo do host, ~40 na RPC e nos params, ~15 no status e ~60 no renderer, mais as strings
(`en-runtime-required.json` e locales) e ~8 testes de host com 2 de renderer. São 1,5 a 2 dias, pagos agora.
**Se paga:** na primeira vez que um chat que segue a seleção bate no limite com tarefa de fundo, o caso do relato.
[C2 · inferido · 60]

### O que ataquei e o que caiu

- **"O envio da continuação deveria ser o próprio pedido (H2)."** Caiu como recomendação. O defeito some no lugar
  certo e o `it.fails` fica verde como está. Mas a continuação parada fica `pending` no journal enquanto a CLI abre o
  turno do acordar no mesmo agente. O `admitFreshInput` junta envio retido ao agente (F2), e a atribuição de um turno do
  provider com uma submissão pendente não foi medida. Fica como alternativa.
- **"Copiar o transcript antes de relançar, como o fixado."** Caiu. Com o `projects/` ligado (F18), a cópia é inútil.
  Sem ele, a cópia que pula o alvo existente (F20) deixa um transcript velho em B, que vira histórico perdido em
  silêncio quando a seleção voltar. Sem a cópia, a falha aparece como `historyInOtherAccount` (F19), à vista.
- **"Persistir o pedido no SQLite."** Caiu. O fechamento do app para os agentes e corta a tarefa (F21). Depois do
  reinício não há agente retido, e o Continue da linha já vai à conta selecionada (F3/F4, `bb137633c35`). Persistir
  só pouparia um clique depois de reiniciar no meio da espera.
- **"O auto-continue estraga o pedido."** Ficou, com remendo. O botão já cancela o agendado do corte (F13), e o
  disparo trata o `superseded` como feito. A varredura com troca feita fora do botão (F14) é defeito do upstream:
  vai à rodada R2.4.
- **"Os dois turnos dependem de a CLI acordar e gravar a notificação" (F9, F10).** Ficou de pé só com o fallback do
  passo 6 e com uma sonda antes de implementar (abaixo). Sem a sonda, o desenho pode esperar um acordar que nunca vem.
- **"O `it.fails` não fica verde."** É verdade: o teste chama o `host.send` direto, e o envio direto com agente
  retido segue o contrato do upstream (F2). O teste se reescreve pelo `arm`, com o mesmo cenário.

### A sonda antes de implementar

1. Rodar a CLI com `--input-format stream-json` e uma tarefa `sleep 30` em segundo plano.
2. Antes de a tarefa acabar, derrubar a rede ou trocar a chave, para a API recusar.
3. Conferir no `.jsonl`:
   - se o turno do acordar começa (F10);
   - se o registro `task-notification` fica no transcript (F9).

Custo: ~30 min, agora. Se paga: decide se o fallback do passo 6 é rede de segurança ou caminho principal.
[C3 · inferido · 70]

A rede derrubada não é o limite de uso. A confirmação final só vem com uma conta esgotada de verdade.

## As alternativas

**H2: segurar a continuação no loop de entrega.**
- O loop para (`return this.stop`) quando a submissão é continuação de limite e o agente está retido em outra conta.
- O commit do turno do acordar acorda o loop (`afterCommit`), e o ramo do envio troca de agente.
- Muda o `delivery-loop.ts` em ~1 linha e um predicado do BrzA. Não muda o wire nem o renderer.
- Conserta também a varredura do auto-continue (F14), que usa o mesmo envio.

**Custo:** ~40 linhas e 1 linha num arquivo do upstream de 3 commits (F23). Antes disso, uma sonda no rig, de 2 a 4 h,
para medir o turno do provider com a submissão pendente e o steer no turno do acordar. A mensagem "Continue where you
left off" fica pendente enquanto a tarefa roda, e as mensagens novas da pessoa entram na fila atrás dela.
**Se paga:** só se a sonda mostrar que o journal não amarra o turno do acordar à submissão pendente. Nesse caso,
nesta fase, porque conserta o botão e a varredura juntos. [C4 · inferido · 55]

**H3: o pedido no renderer.** O renderer guarda o pedido e observa o status — faixa de tarefas, turno ativo, corte
mais novo —, e envia a continuação quando o chat fica livre.

**Custo:** ~80 linhas no renderer, sem host nem wire. Mas o renderer não vê o `hasOpenDispatch` nem o
`providerHoldsDispatch`, e teria de copiar o `owesWakeUp` (F6). Disparar cedo repete o defeito. O pedido morre quando
o painel desmonta.
**Se paga:** nunca como solução, porque o defeito volta na corrida. [C5 · inferido · 65]

**H1 com o pedido persistido no record.**

**Custo:** H1 mais um campo no record, com stored form, decode e mutação, ~+0,5 dia. Toca o formato gravado do
upstream.
**Se paga:** só quando o app reinicia no meio da espera, e aí poupa um clique (F21). [C6 · inferido · 65]

**Duas peças sem caminho:**
- **Rodar um agente novo em B já, com o antigo em A só para a tarefa:** os dois gravariam a mesma sessão da CLI.
  Saiu sem custo medido, por ser inviável.
- **Parar o agente no instante em que a tarefa assenta e entregar o resultado só no corpo:** a CLI abre o acordar no
  mesmo instante. A corrida duplica ou perde a notificação. Ficou só como fallback do passo 6, depois de 30 s sem
  acordar.

## Os pontos para rodada

### R1 — o comportamento

**R1.1 Como o resultado da tarefa chega ao lead na conta nova?**
1. **(Recomendado)** Em dois turnos, com fallback: o acordar roda em A, bate no limite e deixa a notificação no
   transcript; a continuação em B retoma. Se o acordar não vier em 30 s depois de a tarefa assentar, o host para o
   agente e manda a continuação com o resultado no corpo.
   Custo: ~40 linhas de fallback e a sonda de ~30 min, agora. Se paga: no primeiro caso em que a CLI não acorda em
   conta esgotada (F10). [C7 · inferido · 65]
2. Só os dois turnos, sem fallback: se o acordar não vier, o pedido espera até Anderson cancelar.
   Custo: zero linhas a mais. Se paga: agora, se a sonda provar que a CLI sempre acorda; senão, nunca, porque o
   pedido trava. [C8 · inferido · 60]
3. Sempre um turno em B, com o resultado no corpo: o host para o agente assim que a tarefa assenta.
   Custo: ~60 linhas e a corrida com o acordar da CLI, que pode duplicar a notificação. Se paga: nunca, enquanto a
   opção 1 cobrir. [C9 · inferido · 60]

**R1.2 Quando a tarefa nunca termina, o que acontece?**
1. **(Recomendado)** O pedido espera sem prazo. A linha mostra "Cancelar", e a faixa de tarefas mantém o Stop da
   tarefa: parar a tarefa faz o acordar e a continuação seguirem.
   Custo: nenhum além do H1. Se paga: agora. [C10 · inferido · 80]
2. Prazo de 30 min, e depois o pedido cai com um aviso na linha.
   Custo: ~20 linhas, um texto e um teste, agora. Se paga: só quando uma tarefa esquecida segurar o pedido.
   [C11 · inferido · 70]

**R1.3 O que cancela o pedido?** Marque mais de uma.
1. **(Recomendado)** "Cancelar" na linha. Custo: a RPC de cancelar, ~15 linhas. Se paga: agora.
2. **(Recomendado)** Stop pessoal. Custo: ler o `readStopping` no timer, ~3 linhas. Se paga: agora, porque "parar"
   não deve virar "continuar depois".
3. **(Recomendado)** Fechar o chat, ou ele sair do host. Custo: ~3 linhas. Se paga: agora, porque sem isso o `Map`
   vaza.
4. **(Recomendado)** A seleção volta à conta do agente. Custo: ~3 linhas. Se paga: agora, porque mover não faz mais
   sentido.

[C12 · inferido · 75]

**R1.4 Uma mensagem nova da pessoa durante a espera.**
1. **(Recomendado)** Cancela o pedido, e a mensagem segue como hoje: vai ao agente retido e bate no limite de A. A
   linha nova oferece o botão de novo.
   Custo: ~5 linhas. Se paga: agora, porque o comportamento é previsível.
2. Não cancela: a mensagem vai a A, bate no limite, e o pedido continua de pé. A continuação em B depois retoma com a
   mensagem no transcript, se F9 valer para mensagem de usuário.
   Custo: zero linhas, mas depende de F9. Se paga: depois da sonda, se F9 valer.
3. A mensagem espera junto com o pedido. É o H2.
   Custo: o do H2 (C4). Se paga: só com o H2.

[C13 · inferido · 65]

### R2 — o escopo

**R2.1 O que a interface mostra durante a espera?**
1. **(Recomendado)** Na linha do limite: "Vai continuar em {conta} quando a tarefa em segundo plano terminar" e o
   botão "Cancelar", no lugar do "Continue in another account".
   Custo: ~60 linhas de renderer, 2 strings e 2 testes, agora. Se paga: agora.
2. Só um toast no clique, sem estado na linha.
   Custo: ~10 linhas, mas sem cancelar pela interface. Se paga: nunca, se R1.3.1 entrar.

[C14 · inferido · 70]

**R2.2 O chat fixado (P36) entra?**
1. **(Recomendado)** Mesma peça, numa fase 2 do mesmo plano. No fixado, o pedido dispara o `switchAccount` e depois a
   continuação, sem recusar com tarefa aberta e sem parar antes do acordar.
   Custo: ~+1 dia, quase todo em arquivo do fork (F17). Se paga: na primeira vez que um chat fixado bate no limite
   com tarefa de fundo.
2. Uma issue própria, priorizada à parte.
   Custo: zero agora; o fixado segue recusando (F16). Se paga: quando a issue subir.
3. Fica de fora.
   Custo: zero. Se paga: nunca; a recusa fica.

[C15 · inferido · 60]

**R2.3 O histórico na conta nova.**
1. **(Recomendado)** Não copiar o transcript: confiar no `projects/` ligado (F18). Quando ele não estiver ligado, a
   falha aparece como `historyInOtherAccount` (F19).
   Custo: zero. Se paga: agora.
2. Copiar com o `copyClaudeTranscriptsToAccount` antes do disparo.
   Custo: ~20 linhas, mais o risco de uma cópia velha virar histórico perdido em silêncio quando a seleção voltar
   (F20). Se paga: só com o perfil sem `projects/` ligado.

[C16 · inferido · 70]

**R2.4 O auto-continue depois de uma troca feita fora do botão (F14)** — defeito do upstream, fora da decisão.
1. **(Recomendado)** Uma issue no fork, com o teste que prova, e a decisão de reportar ao upstream depois da prova.
   Custo: ~1 h para o teste, agora. Se paga: quando provar F14, ou quando o tirar da mesa.
2. Barrar a varredura com o predicado do BrzA no `eligible`.
   Custo: ~2 linhas em `structured-agent-session-usage-limit-continue.ts`, com 14 commits do upstream (F23). Se paga:
   na primeira troca pelo seletor com tarefa aberta e auto-continue ligado.
3. Nada.
   Custo: zero. Se paga: nunca.

[C17 · inferido · 65]

## Os testes

O `it.fails` de `b5573520d9d` vira `it`, dirigido pelo `arm`.

**No host:**
1. Tarefa terminada que deve o acordar:
   - o `arm` devolve `deferred` e o agente fica em A;
   - o turno do acordar se completa com um corte novo depois do `settledAt`;
   - o pedido envia a continuação do corte novo, e o agente vai a `/homes/b`.
2. Tarefa aberta, com handle aberto do provider (F4): espera; o handle fecha e o acordar vem; vai a B. O rig ainda não
   simula o handle aberto; isso fica a conferir.
3. Sem retenção: o `arm` devolve `now` e nada fica guardado.
4. Cancelar pela RPC: depois que o trabalho acaba, nada se envia.
5. Stop pessoal, chat fechado e seleção de volta a A: o pedido cai.
6. O acordar dá certo em A (sem corte novo): o pedido cai calado e não envia.
7. O auto-continue chega antes ao corte novo: o `superseded` vale como feito, com um envio só.
8. Reinício: o host é descartado e recriado; nenhum pedido; o Continue da linha vai a B.
9. A tarefa nunca termina: o pedido segue em todas as voltas do timer, sem envio, com o campo de status presente.
10. Fallback (R1.1): a tarefa assenta, não vem acordar em 30 s; o host para o agente e manda a continuação com o
    resultado no corpo.

**No renderer:**
1. A linha mostra a espera e o Cancelar.
2. Host sem a capacidade: segue o caminho de hoje.

## Os arquivos essenciais

1. `src/main/native-chat/agent-session-wire/recovery/structured-agent-session-outgrown-child.ts`
2. `src/main/native-chat/agent-session-wire/delivery/structured-agent-session-input-handover.ts`
3. `src/main/native-chat/agent-session-wire/recovery/structured-agent-session-usage-limit-continue.ts`
4. `src/main/native-chat/agent-session-wire/host/testing/structured-agent-session-account-switch.test.ts`
5. `src/main/native-chat/agent-session-wire/host/testing/structured-agent-session-account-switch.brza.test.ts`
6. `src/renderer/src/components/native-chat/brza/BrzaContinueInOtherAccount.tsx`
7. `src/renderer/src/components/native-chat/brza/use-brza-continue-in-other-account.ts`
8. `src/main/native-chat/agent-session-wire/operations/structured-agent-session-account-switch.ts`
9. `src/main/native-chat/agent-session-journal/journal-sql-send-admission.ts`
10. `src/main/claude/__fixtures__/claude-plugin-recovery.json`
