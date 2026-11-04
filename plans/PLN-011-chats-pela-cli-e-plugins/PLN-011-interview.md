# PLN-011 — Entrevista

A Entrevista do [PLN-011: Os chats do BrzA Studio se coordenam pela CLI, aparecem na navegação e chegam aos plugins](PLN-011-plan.md).
Só cresce: rodada nova vai ao fim.

As rodadas R1 a R4 foram respondidas por Anderson em 2026-11-03, na sessão "Plano: chat via CLI e plugins" do
`playground`, e estão gravadas na issue de origem com o que foi apresentado antes; entram aqui com a resposta literal,
sem perguntar de novo. As opções sem preço registrado na origem ficam sem preço aqui.

### Rodada 1 — o foco (enviada 2026-11-03, no `playground`)

> **Apresentado antes:** o aprofundamento verificado da issue de origem, no `brza-studio@8f41dd56a33` e no
> `brza-workflow`.

Respondida em 2026-11-03.

1. **Foco do detalhamento.** **Decidido:** "Coordenação entre sessões (Recomendado). Custo: adaptar list/read/send à
   CLI e integrar nomes, recibos e retry ao wrapper existente. Se paga: ao encaminhar trabalho para chats já abertos e
   acompanhar suas respostas."

### Rodada 2 — acompanhamento e envio (enviada 2026-11-03, no `playground`)

> **Apresentado antes:** as restrições do contrato — o `AgentSessionSendResult` que distingue fila de submissão, o
> `unknown` que não é envio nem falha, o replay que não resolve o `unknown`, e o cliente da CLI que não encaminha a
> origem do coordenador em `agentSession.send`.

Respondida em 2026-11-03.

1. **Acompanhamento.** **Decidido:** leitura incremental por cursor, com tratamento de cursor inválido.
2. **Envio durante atividade.** **Decidido:** preservar `queue-if-active` e expor que a mensagem está enfileirada,
   inclusive quando uma pergunta pendente retém a fila.

### Rodada 3 — abertura do plano (enviada 2026-11-03, no `playground`)

> **Apresentado antes:** o recorte já respondido (coordenação por cursor e fila, aliases de `brza sessions`, recibos e
> retry) e as frentes fora dele (focus e barra lateral, Jump Palette, robustez do journal, plugins, `account usage`).

Respondida em 2026-11-03.

1. **Destino.** Opções: `PLN` em `plans/` (recomendado); seção num worklog. **Resposta:** "um plano pra cada
   `workstream` e elas se coordenam na execução" — vai à R4.1.
2. **Recorte.** Opções: só a coordenação (recomendado); coordenação + `chat focus`; a issue inteira, por fases.
   **Resposta:** "A issue inteira, por fases".
3. **Restante.** Opções: fica na issue de origem (recomendado); vira issues próprias. **Resposta:** "issues próprias,
   repriorize individualmente" — vai à R4.2 e à R4.3.

### Rodada 4 — esclarecimento do plano (enviada 2026-11-03, no `playground`)

> **Apresentado antes:** a leitura das respostas em texto livre da R3 — `studio` para o código do `brza-studio` e
> `tools-kit` para o `brza sessions` — e o estado no upstream: `#37774` integrado em 2026-11-03 18:28 UTC e ausente do
> checkout local `8f41dd56a33`, `#37802` e `#37467` abertos.

Respondida em 2026-11-03.

1. **Workstreams.** **Decidido:** "studio + tools-kit (Recomendado)". Um `PLN` no `studio` e outro no `tools-kit`,
   este com `depends_on` no do `studio`, cada um aberto por sessão nova no worktree dele.
2. **Fases.** **Decidido:** "Todas as frentes, por prioridade (Recomendado)". Cada frente vira issue com prioridade
   própria; os planos cobrem todas, em fases na ordem da prioridade, cada fase citando a issue dela.
3. **Prioridades.** **Decidido:** "Proposta abaixo (Recomendado)". `high`: coordenação (`list/read/send`) e o porte do
   `#37774` antes do `send` **→ o `#37774` reaberto em R5.1**. `medium`: navegação (`focus`, barra lateral, Jump Palette) e o journal do `#37802`, que
   espera a integração no upstream. `low`: plugins e `account usage` (`#37467`).
4. **Issues.** **Decidido:** "No workstream da frente (Recomendado)". A sessão que abre o plano cria as issues dele.

### Rodada 5 — a base da fase 1 (enviada 2026-11-03)

> **Apresentado antes:** o Terreno da fase 1, levantado por um `collector` no `brza-studio@8f41dd56a33` e conferido
> nesta sessão. O `#37774` toca só `mobile/`, `src/renderer/src/components/native-chat/` e `src/shared/`, nenhum
> arquivo de `src/main`, e limpa o rascunho do chat de **terminal** antes de um envio do celular ou do desktop; o
> `brza chat send` fala com o host estruturado (`agentSession.send`). Portá-lo agora traz 6 conflitos de lógica e 4
> commits do upstream posteriores à `v1.4.246` (`#37212`, `#36493`, `#37334`, `#37565`). O `#33115` aplica limpo na
> `master` (`git apply --3way` num índice temporário: 11 arquivos, sem conflito), com `list` por `worktree.ps`, `read`
> por `tail`/`before`, `send` com `queue-if-active` e 10 testes, sem cursor, sem o estado da submissão e sem o motivo
> da fila. O host já tem o cursor `{epoch, sequence}` (`src/shared/agent-session-journal-identity.ts:5-8`) e cinco
> motivos de reset com a página `tail` pronta (`agent-session-journal-types.ts:477-483`,
> `agent-session-history-page.ts:87-104`). O motivo da retenção da fila (`prompt|working`) só existe no host
> (`structured-agent-session-queued-messages.ts:46-58`).

Respondida em 2026-11-03.

1. **O `#37774`, que a R4.3 punha antes do `send`.** Opções:
   - sai da fase 1 (recomendada) — custo: nenhum agora; o envio a chat PTY fica como está até o sync; se paga: já, a
     fase 1 começa sem 4 commits de pré-requisito e 6 conflitos;
   - porta antes, com os 4 prévios — custo: estimada uma sessão de código e risco de regressão no composer PTY, antes
     da coordenação; se paga: só se o `chat send` cobrir chat PTY na fase 1;
   - fica, mas no fim da fase 1 — custo: o mesmo, no fim da fase; se paga: se o Studio usar o envio do celular a chat
     PTY antes do sync.

   **Decidido — "Sai da fase 1 (Recomendado)"**: chega no próximo sync do upstream, e só se porta antes se o `chat send`
   passar a cobrir chat PTY. Reabre a parte do `#37774` da R4.3.

2. **A base do `list/read/send`.** Opções:
   - portar o `#33115` e estender (recomendada) — custo: estender o `chat read` e conviver com divergência no sync se
     o upstream fundir outra forma; se paga: na fase 1, poupa o parse do `worktree.ps`, o laço de reset e os testes;
   - escrever do zero — custo: estimado em cerca de 3 vezes o porte, sem os testes do upstream; se paga: nunca, hoje;
   - esperar o `#33115` fundir — custo: a prioridade `high` parada por tempo indefinido, com o PR aberto desde
     2026-10-24; se paga: nunca, para a coordenação de agora.

   **Decidido — "Portar o #33115 e estender (Recomendado)"**: o porte vai num commit separado, e o cursor, o recibo e o
   motivo da fila vêm depois.

3. **O cursor inválido.** Opções:
   - erro com a página `tail` (recomendada) — custo: um contrato de erro a documentar e testar; se paga: na fase 1, a
     sessão coordenadora nunca segue com estado misturado sem saber;
   - reabre sozinho, com aviso — custo: o script que não olha `reset: true` duplica ou pula itens; se paga: nunca, para
     a coordenação.

   **Decidido — "Erro com a página tail (Recomendado)"**: código de saída não zero e `cursor_reset: <motivo>`, com a
   página `tail` e o `nextCursor` novos no JSON.

4. **O motivo da fila.** Opções:
   - lê o histórico após enfileirar (recomendada) — custo: um RPC a mais por envio enfileirado, com o motivo deduzido no
     cliente; se paga: na fase 1, cumpre a R2.2 sem mudar o contrato do host;
   - o host passa a devolver o motivo — custo: muda o contrato do wire e conflita no sync; se paga: só quando um segundo
     cliente precisar do motivo.

   **Decidido — "Lê o histórico após enfileirar (Recomendado)"**: depois de `queued`, um `history tail`, e o JSON traz a
   posição, o `nextQueuedMessageId` e `held_by: question|working`.

### Rodada 6 — o contrato e a prova da fase 1 (enviada 2026-11-03)

> **Apresentado antes:** as inferências do código, com a fonte. O cursor como string opaca `epoch:sequence`, que mapeia
> 1:1 o `{epoch, sequence}` do host; o `--json` com `itemId`, `revision`, `sequence`, `nextCursor` e `hasNewer`, que
> o do `#33115` não traz; a origem do coordenador no `send` pelo `ORCA_AGENT_SESSION_ID`, como o wrapper já faz
> (`brza-workflow/bin/brza_runtime.py:95-97`), lida pelo host no `send`
> (`src/main/runtime/rpc/methods/structured-agent-session-send-compatibility.ts:10`) e ausente da CLI, que só a manda
> em `agent.launch` (`src/cli/runtime/client.ts:58,140`); e a divergência com o levantamento sobre o `fence`, que o
> host atual ignora, mas que a norma do `brza-studio` manda manter, pela compatibilidade entre versões misturadas
> (`AGENTS.md:61`).

Respondida em 2026-11-03.

1. **O código de saída do `send`.** Opções:
   - código por estado (recomendada) — custo: um contrato de códigos a documentar e testar na fase 1; se paga: no
     plano do `tools-kit`, quando o wrapper decide sem ler o JSON e o `sent: true` falso acaba;
   - sempre 0, estado só no JSON — custo: quem chama lê o JSON, e o `sent: true` falso se repete em quem esquecer; se
     paga: nunca, para a coordenação.

   **Decidido — "Código por estado (Recomendado)"**: 0 em `accepted` e `queued`; 1 em recusa e `rejected`; 3 em
   `pending` e `unknown`, entrega incerta que não se reenvia. O JSON traz sempre `delivery` e `submission.state`.

2. **O retry.** Opções:
   - `--operation-id` no `send` (recomendada) — custo: uma flag e o teste de replay na fase 1; se paga: no `tools-kit`,
     no primeiro timeout de envio, sem mensagem duplicada no chat;
   - sem retry na CLI — custo: o retry depois de um timeout duplica a mensagem, ou o wrapper mantém o socket cru; se
     paga: nunca, se o wrapper migrar para a CLI.

   **Decidido — "--operation-id no send (Recomendado)"**: o `send` imprime o `clientOperationId`, e o mesmo id com o
   mesmo texto devolve o resultado gravado, sem reenviar.

3. **O contrato inferido.** Opções:
   - confirma, lendo o `fence` (recomendada) — custo: um RPC por envio, desde a fase 1; se paga: no primeiro host
     remoto mais velho que ainda confere o `fence`;
   - confirma, sem ler o `fence` — custo: o host mais velho recusa o envio, e o código diverge do `#33115`; se paga: uma
     chamada a menos por envio, agora; com versões misturadas, nunca.

   **Decidido — "Confirma, lendo o fence (Recomendado)"**: cursor `epoch:sequence`, `--json` com os ids, origem do
   coordenador no `send` e o `expectedRuntimeFence` lido do histórico antes do envio.

4. **A prova da fase 1.** Opções:
   - unidade e um caso manual (recomendada) — custo: cerca de 30 min de Anderson no app ao fechar a fase; se paga: no
     fim da fase 1, porque a fila retida por pergunta só aparece com o agente real;
   - só unidade — custo: nenhum de Anderson; se paga: agora, mas a dedução do `held_by` só se confere no `tools-kit`.

   **Decidido — "Unidade + 1 caso manual (Recomendado)"**: `chat.test.ts` cobre cursor, reset, fila com `held_by`,
   códigos de saída, replay e origem; o C1 roda no app de dev com dois chats.

### Rodada 7 — a condução (enviada 2026-11-03)

> **Apresentado antes:** os dois pedidos de Anderson, nas palavras dele. Em 2026-11-03: "ao invés de perguntas para mim
> as lacunas do plano, faça as rodadas de perguntas com um agente `agy` `Gemini Flash 3.8 High`". E depois: "siga com
> os passos até encerrar o plano, uma revisão independente por passo executado, utilize o `MCP` do `brza-workflow` o
> `brza-orchestror` para coordenar o plano e as sessões". O orquestrador é o `brza-mcp` do PLN-009, do `tools-kit`,
> em `phase: review`, com o código só na `feat/pln-009-mcp` do `brza-workflow` (`007383a`), parado. O `dispatch` de
> papel que não é `consultant` devolve um gate. Pela norma (`brza-workflow@3826f63`), o servidor entra na sessão por
> `claude --mcp-config`.

Respondida em 2026-11-03, por Anderson.

1. **Ligar o `brza-mcp` sem o merge.** Opções:
   - liga da `feat`, via launchd (recomendada) — custo: um daemon fora do workspace e o risco de um defeito que o C2 e o
     C3 do PLN-009 pegariam; se paga: já, o PLN-011 é o primeiro uso real;
   - fecha o PLN-009 antes — custo: o PLN-011 espera; se paga: quando roda sobre código aceito;
   - sem o MCP — custo: perde o teste real do orquestrador; se paga: agora, para o PLN-009 nunca.

   **Decidido — "Liga da feat, via launchd (Recomendado)"**. → reaberta em R18.1, no caminho dos workers. Ligado em 2026-11-03: `brza-mcp start` → "de pé", o
   agente `com.brza.orchestrator` do launchd, em `http://127.0.0.1:4242/mcp`.

2. **Os gates do `dispatch`.** Opções:
   - pré-aprovados no PLN-011 (recomendada) — custo: Anderson não vê cada worker antes de abrir; se paga: já, o plano
     roda até fechar;
   - pergunto gate a gate — custo: dois gates por passo; se paga: só se Anderson quiser ver cada worker.

   **Decidido — "Pré-aprovados no PLN-011 (Recomendado)"**: a sessão coordenadora aprova os gates de `implementer` e
   `reviewer` com `ref: PLN-011`, na conta ativa, e para em qualquer outro gate (troca de conta, outro papel). Cada
   aprovação vai ao worklog.

3. **A conexão da sessão coordenadora.** Opções:
   - HTTP direto daqui (recomendada) — custo: a chamada sai como Bash, sem a linha `mcp` da medição; se paga: já;
   - reabre com `--mcp-config` — custo: o arranque de uma sessão nova; se paga: quando a medição `mcp` importar ao
     PLN-009.

   **Decidido — "Reabre com --mcp-config"**: a sessão que abriu o plano grava o `Retomar` e abre a coordenadora pelo
   `brza sessions`, com o servidor na configuração. **→ reaberta em R12.1.**

**Por delegação de Anderson (R7, "Apresentado antes"), as rodadas R8 a R11 foram respondidas pelo `agy` com o modelo
`gemini-3.8-flash-high`**, em modo `plan`, com leitura do plano, dos levantamentos e do código. Cada uma leva o porquê
que ele deu. Os prompts e as respostas brutas estão no scratch da sessão de 2026-11-03, em `agy/r8` a `agy/r11`. Nenhuma
nota de `work/decisions/` nasce dessas respostas.

### Rodada 8 — o contrato da leitura da fase 1 (enviada 2026-11-03, ao `agy`)

> **Apresentado antes:** o D3 rascunhado pelo `designer`. Hoje todo erro da CLI sai 1 (`src/cli/cli-exit-code.ts:3-13`);
> o `after` conta linhas do journal, até 200 por página (`structured-agent-session-params.ts:319-326`); na sessão que
> teve um hand-off da fila em dúvida, todo `after` da CLI local volta `cursor_compacted` até o epoch mudar
> (`agent-session-history-page.ts:87-95`, inferido). O pedido do PLN-010, recebido por correio da sessão "Plano: brza
> sessions sobre o brza chat (tools-kit)" e gravado em `workstream/tools-kit@5ef728d`: `--since <cursor>`,
> `--operation <id>`, o recibo com `operation`, o cursor inválido distinguível pelo código.

Respondida em 2026-11-03, pelo `agy`.

1. **O código do `cursor_reset`.** Opções: 2 (recomendada) — custo: uma linha da tabela e um teste; se paga: no
   `tools-kit`, quando o wrapper separa recomeçar de falhar · 1 — custo: nenhum; se paga: nunca · 4 — custo: o da 2; se
   paga: só com tabela única de códigos.

   **Decidido — "2 (Recomendado)"** → refeita às cegas em R13.1.. "Permite ao coordenador e ao wrapper distinguir recomeço por reset de falha real
   diretamente pelo código de saída, sem precisar inspecionar o payload do erro."

2. **O reset repetido.** Opções: aceitar e documentar (recomendada) — custo: uma linha no guia e um teste; até 200
   itens relidos por leitura; se paga: agora · contorno no cliente — custo: ~1 h, revisões antigas perdidas sem aviso;
   se paga: só com medição · mudar o host — custo: contrato `strict` e conflito no sync; se paga: nunca na fase 1.

   **Decidido — "Aceitar e documentar (Recomendado)"** → refeita às cegas em R13.2.. "Preserva a fidelidade ao contrato do host sem introduzir
   divergências no sync com o upstream, evitando perda silenciosa de revisões no cliente."

3. **Quanto o cursor lê.** Opções: uma página `after` de 200 linhas (recomendada) — custo: recusar o `--limit` e um
   campo; se paga: agora · `--limit` conta linhas — custo: a flag muda de sentido; se paga: só se 200 linhas pesarem ·
   lê até `hasNewer` falso — custo: saída sem teto; se paga: nunca.

   **Decidido — "Uma página after de 200 linhas (Recomendado)"** → refeita às cegas em R13.3.. "Garante paginação exata por construção e
   previsibilidade de consumo, evitando saída sem teto ou ambiguidade semântica na flag de limite."

4. **Os nomes das flags.** Opções: adotar os do PLN-010 (recomendada) — custo: reescrever a R6.2 e a R6.3 só no nome;
   se paga: já · manter os da R6 — custo: o PLN-010 muda o Desenho; se paga: nunca · os dois, como alias — custo:
   superfície dupla; se paga: nunca.

   **Decidido — "Adotar os do PLN-010 (Recomendado)"** → reaberta em R13.4.: `--since`, `--operation` e o campo `operation` no recibo, com a
   semântica da R6. "Atende de imediato ao consumidor dependente no tools-kit sem impor adaptações e dispensa aliases
   redundantes em uma interface nova sem legado."

### Rodada 9 — o contrato do envio e o código da fase 1 (enviada 2026-11-03, ao `agy`)

> **Apresentado antes:** o D4 e o D5 rascunhados. Para a CLI local, o host responde na admissão, antes da entrega ao
> provedor (`structured-agent-session-send-compatibility.ts:36-44`), e daí o `pending` deve ser o caso comum (inferido,
> não rodado); a fila também para pelo Stop ou pelo bloqueio, e pode ter escoado quando o `tail` chega; o replay pode
> voltar `returned` ou `withdrawn`; há nove pastas `src/**/brza/` só do fork.

Respondida em 2026-11-03, pelo `agy`.

1. **O `pending`.** Opções: esperar até 30 s (recomendada) — custo: ~1,5 h e 3 testes; até 30 s por envio a frio; se
   paga: na fase 1 · manter a R6.1 — custo: o wrapper perde o sinal de incerteza; se paga: se o C1 mostrar `pending`
   raro · `pending` sai 0 — custo: sucesso falso; se paga: nunca.

   **Decidido — "Esperar o pending resolver, teto 30 s (Recomendado)"** → refeita às cegas em R14.1.. "Preserva a semântica do código 0 para
   confirmação real e 3 para incerteza na coordenação entre sessões, sem nunca reportar sucesso falso antes da entrega
   resolver."

2. **Os valores do `held_by`.** Opções: `question | working | null` (recomendada) — custo: um campo e dois testes; se
   paga: na fase 1 · com `paused` e `blocked` — custo: o `blocked` não aparece na página; se paga: só se o wrapper agir
   diferente · só `question | working` — custo: valor falso; se paga: nunca.

   **Decidido — "question | working | null (Recomendado)"** → refeita às cegas em R14.2., com `queuePaused: true` na pausa. "Evita reportar working
   falso quando a fila já escoou ou está pausada, mantendo o held_by fiel aos dados reais expostos pelo histórico."

3. **O replay `returned` ou `withdrawn`.** Opções: sair 1, `rejected` (recomendada) — custo: duas linhas e dois testes;
   se paga: no primeiro retry depois de um Stop · sair 0 — custo: diz "na fila" para o que não sai; se paga: nunca.

   **Decidido — "Sair 1, com submission.state rejected (Recomendado)"** → refeita às cegas em R14.3.. "Cumpre o princípio de nunca reportar sucesso
   falso em replays de mensagens retiradas ou com falha definitiva que não serão entregues."

4. **Onde mora a extensão.** Opções: `src/cli/brza/` (recomendada) — custo: quatro arquivos pequenos; se paga: no sync
   do `#33115` fundido · tudo no `chat.ts` — custo: conflito em cada função; se paga: no sync, nunca.

   **Decidido — "Em src/cli/brza/, com o chat.ts só chamando (Recomendado)"** → refeita às cegas em R14.4.. "Isola as extensões do fork no padrão
   das outras pastas brza/, minimizando divergências e conflitos no rebase com o upstream após o merge do #33115."

### Rodada 10 — a navegação (enviada 2026-11-03, ao `agy`)

> **Apresentado antes:** o Terreno da fase 2, no [Desenho](PLN-011-design.md).

Respondida em 2026-11-03, pelo `agy`.

1. **Como o `focus` navega.** Opções: ramo de chat no `terminal.reveal`, no renderer (recomendada) — custo: o nome
   enganoso e 1 teste; se paga: na fase 2 · RPC novo `agentSession.focus` — custo: schema, catálogo e IPC novos; se
   paga: se o upstream aceitar · só `agentSession.reveal` — custo: não traz a janela; se paga: nunca.

   **Decidido — "Ramo de chat no terminal.reveal, no renderer (Recomendado)"** → refeita às cegas em R15.1.. "Evita criar RPCs e schemas novos que
   gerem conflitos no sync com o upstream, reusando o relay existente para trazer a janela ao primeiro plano e
   resolvendo a aba no renderer."

2. **Quando a barra lateral segue.** Opções: sempre, derivada da aba ativa (recomendada) — custo: ajustar dois
   arquivos, com testes; se paga: na fase 2 · só em mudança externa — custo: dois estados; se paga: nunca · só pelo
   `focus` — custo: atalho e notificação divergem; se paga: nunca.

   **Decidido — "Sempre, derivada da aba ativa (Recomendado)"** → refeita às cegas em R15.2.. "Elimina o estado duplicado que causa a divergência
   visual relatada, mantendo a barra lateral sempre sincronizada com a aba ativa independente da origem da navegação."

3. **O que a Jump Palette ganha.** Opções: só título e recentes (recomendada) — custo: ramo novo no builder e na
   ativação; se paga: na fase 2 · título e conteúdo — custo: indexar transcript; se paga: só com busca de conteúdo.

   **Decidido — "Só título e recentes (Recomendado)"** → refeita às cegas em R15.3.. "Atende à navegação de chats na Jump Palette com menor
   divergência e sem a sobrecarga ou complexidade de indexar o texto dos transcripts."

4. **A prova da fase 2.** Opções: unidade e caso manual (recomendada) — custo: ~20 min de Anderson no app; se paga: no
   fim da fase 2 · só unidade — custo: nenhum de Anderson; se paga: agora, sem prova do foco da janela.

   **Decidido — "Unidade + caso manual (Recomendado)"** → refeita às cegas em R15.4.. "Cumpre a diretriz de comprovar a lógica com testes de
   unidade e verificar manualmente no app o foco de janela e a experiência visual real."

### Rodada 11 — plugins, `account usage` e o journal (enviada 2026-11-03, ao `agy`)

> **Apresentado antes:** o Terreno da fase 4 e o D11, no [Desenho](PLN-011-design.md); o `#37802` segue aberto, com
> 459 arquivos, e a R4.3 manda a fase 3 esperar a integração.

Respondida em 2026-11-03, pelo `agy`.

1. **`agents.list` e o evento.** Opções: campos opcionais novos, conferindo antes no app (recomendada) — custo: o minor
   não sobe; se paga: na fase 4 · método novo `agents.listChats` — custo: superfície nova; se paga: se o plugin precisar
   detectar · mudar a forma — custo: quebra o contrato; se paga: nunca.

   **Decidido — "Campos opcionais novos, conferindo antes no app (Recomendado)"** → refeita às cegas em R16.1.. "Respeita a regra frozen da Host API
   1 de que resultados apenas crescem sem quebrar plugins existentes, além de validar antes no app o comportamento real
   das sessões."

2. **O caminho em `workspace.readContext`.** Opções: não agora (recomendada) — custo: o plugin segue adivinhando o
   `cwd`; se paga: até a sandbox do worker · por capacidade nova — custo: manifest e diálogo; se paga: com plugin de
   status line · sim para todos — custo: `cwd` e `transcriptPath` em frames isolados; se paga: nunca.

   **Decidido — "Não agora (Recomendado)"** → refeita às cegas em R16.2.. "Mantém a restrição intencional contra o vazamento de caminhos locais e
   transcrições para frames isolados antes da introdução de sandboxing ou modelo de permissões."

3. **Quando portar o `#37467`.** Opções: agora (recomendada) — custo: 1 conflito trivial e o rebrand das strings; se
   paga: na fase 5 · esperar o upstream — custo: a CLI só no sync; se paga: no próximo sync.

   **Decidido — "Agora, aplicando o diff com o conflito à mão (Recomendado)"** → refeita às cegas em R16.3.. "O diff é restrito à CLI, tem
   dependências prontas no fork e traz apenas um conflito trivial de rebrand, liberando o avanço da fase 5 e o consumo
   pelo PLN-010."

4. **Como o plano fecha sem o `#37802`.** Opções: a fase 3 vira issue fora de escopo e o plano fecha (recomendada) —
   custo: a frente do journal volta por issue; se paga: ao fim da fase 5 · o plano fica `blocked` — custo: aberto por
   tempo indefinido; se paga: quando o upstream integrar · portar o PR aberto — custo: 459 arquivos instáveis; se paga:
   nunca, enquanto aberto.

   **Decidido — "Fase 3 vira issue fora de escopo e o plano fecha (Recomendado)"** → refeita às cegas em R16.4.. "Mantém a decisão da R4.3 de não
   absorver 459 arquivos de um PR instável no upstream e permite encerrar o plano ao concluir a fase 5 sem bloqueios
   indefinidos."

### Rodada 12 — a sessão coordenadora, refeita (enviada 2026-11-03)

> **Apresentado antes:** o `dispatch` exige um chamador que seja sessão do chat do Studio: no teste do PLN-009, a
> sessão de terminal com `--mcp-config` caiu em `session_caller_unknown` (issue "O dispatch aceita chamador fora do
> Studio", no `tools-kit`), e o C4 só passou de um chat do Studio, por HTTP, com o `X-Brza-Session` e o
> `X-Brza-Client` dele. O `brza sessions` abre chat do Studio, mas não aceita `--mcp-config`, e o `claude-brza`
> instalado, da `master`, não exporta o `BRZA_MCP_TOKEN`.

Respondida em 2026-11-03, por Anderson.

1. **A sessão coordenadora.** Opções:
   - chat novo no Studio, MCP por HTTP (recomendada) — custo: o arranque de uma sessão nova e nenhuma linha `mcp` na
     medição; se paga: já, é o caminho provado no C4 e dá contexto limpo para as 31 h;
   - chat novo com `.mcp.json` local — custo: uma sessão de teste (~5 min) e uma emenda na `workspace.md`; se paga:
     quando a linha `mcp` da medição importar ao PLN-009;
   - esta sessão coordena, por HTTP — custo: o contexto desta sessão encosta nos ~200 mil tokens no meio do plano; se
     paga: já, mas só até a fase 1.

   **Decidido — "Chat novo no Studio, MCP por HTTP (Recomendado)"**. Conferido antes de abrir: do chat da abertura,
   `initialize` e `tools/call status` responderam pelo `/mcp`, com a fila vazia e `orchestrator.max_workers: 6`.

**Refeitas às cegas, pela regra nova de Anderson.** Em 2026-11-03, trazida pela sessão "Plano: chats pela CLI e
plugins (studio)", nas palavras dele: "se o `agy` discordar de você, discutam em rodadas até chegarem a um acordo, não
indique ao agente do `agy` qual a sua escolha recomendada, deixe que ele decida por si". As R8 a R11 tinham a
recomendada marcada, e o `agy` escolheu essa nas 16 perguntas; as R13 a R16 repetem as mesmas perguntas, com o mesmo
"Apresentado antes", sem "(Recomendado)" e com as opções embaralhadas. A recomendação da sessão coordenadora foi
gravada antes de enviar, em `/private/tmp/pln011coord/agy/minhas-recomendacoes.md`; o `agy` não leu o plano nem o
rascunho com a seção de pontos (`pln011-fase1-desenho-cego.md`). Os prompts e as respostas estão em
`/private/tmp/pln011coord/agy/`. Nenhuma nota de `work/decisions/` nasce delas.

### Rodada 13 — o contrato da leitura da fase 1, às cegas (enviada 2026-11-03, ao `agy`)

> **Apresentado antes:** o mesmo da R8, e as opções com o custo e o "se paga" da R8, reescritos sem
> adjetivo que puxe a escolha. Conversa do `agy`: `6bc36873-9dfe-420c-8fe4-45ca9d4bd1ff`.

Respondida em 2026-11-03, pelo `agy`, às cegas.

1. **O código do `cursor_reset`.** Opções, na ordem enviada: 1 · 4 · 2.

   Escolha cega do `agy`: "2" — "O código 2 distingue imediatamente o reset de cursor de falhas gerais (1) ou incertezas (3), viabilizando que o tools-kit e o coordenador reajam de forma limpa pelo código de saída." Recomendação da coordenadora, gravada antes: "2".

   **Decidido — "2"**, por acordo na primeira volta. Confirma a R8.1.

2. **O reset repetido.** Opções, na ordem enviada: Mudar o host · Aceitar e documentar · Contorno no cliente.

   Escolha cega do `agy`: "Aceitar e documentar" — "Preserva a menor divergência com o upstream sem alterar o host e evita contornos no cliente que descartariam revisões antigas, respeitando o princípio de nunca reportar falso sucesso." Recomendação da coordenadora, gravada antes: "Aceitar e documentar".

   **Decidido — "Aceitar e documentar"**, por acordo na primeira volta. Confirma a R8.2.

3. **Quanto o cursor lê.** Opções, na ordem enviada: --limit conta linhas · Lê até hasNewer false · Uma página after de 200 linhas.

   Escolha cega do `agy`: "Uma página after de 200 linhas" — "Mantém o consumo de contexto previsível e limitado por chamada paginada com hasNewer, evitando saídas sem teto e sem conflitar com a semântica do --limit existente." Recomendação da coordenadora, gravada antes: "Uma página after de 200 linhas".

   **Decidido — "Uma página after de 200 linhas"**, por acordo na primeira volta. Confirma a R8.3.

4. **Os nomes das flags.** Opções, na ordem enviada: Aceitar os dois, como alias · Manter os da R6 · Adotar os do PLN-010.

   Escolha cega do `agy`: "Manter os da R6" — "Mantém a consistência com a convenção canônica de --cursor já presente na CLI do Orca e preserva as decisões da R6, cabendo ao plano dependente (PLN-010) alinhar seu desenho." Recomendação da coordenadora, gravada antes: "Adotar os do PLN-010".

   **Discussão, volta 1.** A coordenadora defendeu "Adotar os do PLN-010": o PLN-010 é o único consumidor e já decidiu `--since` e
   `--operation` (`PLN-010-plan.md:69`, `:72`, `:94`, `:99`), e os nomes da R6 nunca foram implementados. E levou os fatos
   a favor dele, conferidos no `brza-studio`: `--cursor <cursor>` é a paginação opaca em seis specs
   (`src/cli/specs/search.ts:9`, `linear-mcp.ts:46`, `automations.ts:128`, `artifacts.ts:33`,
   `orchestration-worker-specs.ts:74` e `:147`); o único `--since` da CLI (`search.ts:9`, `:33`) recebe data ISO; não
   há convenção para a flag de operação. O `agy` contrapropôs "--cursor para o cursor, --operation para a operação e operation no recibo": "Para a leitura, manter --cursor respeita a convenção consolidada em seis specs da CLI do Orca e previne conflito semântico com --since, que já representa data ISO em search. Para o envio, como não existe convenção prévia na CLI, adotar a flag --operation combinada ao campo operation no recibo atende ao PLN-010 e oferece simetria direta entre o JSON e o replay. Essa divisão harmoniza a consistência da CLI com a melhor ergonomia para a coordenação entre sessões." A coordenadora mudou
   para a contraproposta, pelo argumento da convenção e do sentido único do `--since`.

   **Decidido — `--cursor <epoch:sequence>` para o cursor, `--operation <id>` para a operação e `operation` no
   recibo**, por acordo na volta 1. Reabre a R8.4 só no nome do cursor; o PLN-010 lê o plano pelo git e troca `--since`
   por `--cursor` no `brza chat read` que o wrapper chama.

### Rodada 14 — o contrato do envio e o código da fase 1, às cegas (enviada 2026-11-03, ao `agy`)

> **Apresentado antes:** o mesmo da R9, e as opções com o custo e o "se paga" da R9, reescritos sem
> adjetivo que puxe a escolha. Conversa do `agy`: `2d3fca3a-ea81-4116-8fd7-b421fa2cfd13`.

Respondida em 2026-11-03, pelo `agy`, às cegas.

1. **O `pending`.** Opções, na ordem enviada: Manter a R6.1 como está · pending sai 0 · Esperar o pending resolver, teto 30 s.

   Escolha cega do `agy`: "Esperar o pending resolver, teto 30 s" — "Como a CLI local recebe pending logo na admissão, sair 3 inviabilizaria o fluxo comum e sair 0 violaria o critério de nunca reportar falso sucesso se o provedor rejeitar a mensagem logo em seguida. A espera de até 30 s garante a leitura do estado definitivo da entrega e viabiliza a coordenação confiável entre sessões." Recomendação da coordenadora, gravada antes: "Esperar o pending resolver, teto 30 s".

   **Decidido — "Esperar o pending resolver, teto 30 s"**, por acordo na primeira volta. Confirma a R9.1.

2. **Os valores do `held_by`.** Opções, na ordem enviada: Só question | working · question | working | paused | blocked | null · question | working | null.

   Escolha cega do `agy`: "question | working | null" — "Evita mascarar pausa ou escoamento da fila como working e não tenta deduzir blocked, que não é exposto na página do wire. O indicador queuePaused: true cobre a pausa com clareza sem poluir o enum de retenção da fila." Recomendação da coordenadora, gravada antes: "question | working | null".

   **Decidido — "question | working | null"**, por acordo na primeira volta. Confirma a R9.2.

3. **O replay `returned` ou `withdrawn`.** Opções, na ordem enviada: Sair 0, como queued · Sair 1, com submission.state rejected.

   Escolha cega do `agy`: "Sair 1, com submission.state rejected" — "Um envio retornado ou retirado não seguirá adiante sozinho, de modo que responder 0 (queued) configuraria falso sucesso e deixaria o coordenador esperando indefinidamente. Sair 1 com submission.state rejected informa de imediato que a entrega foi frustrada após o cancelamento ou erro." Recomendação da coordenadora, gravada antes: "Sair 1, com submission.state rejected".

   **Decidido — "Sair 1, com submission.state rejected"**, por acordo na primeira volta. Confirma a R9.3.

4. **Onde mora a extensão.** Opções, na ordem enviada: Tudo em chat-sessions.ts e chat.ts · Em src/cli/brza/, com o chat.ts só chamando.

   Escolha cega do `agy`: "Em src/cli/brza/, com o chat.ts só chamando" — "Segue o padrão arquitetural do repositório de manter adições exclusivas do fork em pastas brza/ e atende ao critério de menor divergência com o stablyai/orca. Essa separação previne conflitos de código durante a sincronização que trouxer o PR #33115 fundido do upstream." Recomendação da coordenadora, gravada antes: "Em src/cli/brza/".

   **Discussão, volta 1.** A coordenadora defendeu "Em src/cli/brza/": o PLN-010 é o único consumidor e já decidiu `--since` e
   `--operation` (`PLN-010-plan.md:69`, `:72`, `:94`, `:99`), e os nomes da R6 nunca foram implementados. E levou os fatos
   a favor dele, conferidos no `brza-studio`: `--cursor <cursor>` é a paginação opaca em seis specs
   (`src/cli/specs/search.ts:9`, `linear-mcp.ts:46`, `automations.ts:128`, `artifacts.ts:33`,
   `orchestration-worker-specs.ts:74` e `:147`); o único `--since` da CLI (`search.ts:9`, `:33`) recebe data ISO; não
   há convenção para a flag de operação. O `agy` contrapropôs "--cursor para o cursor, --operation para a operação e operation no recibo": "Para a leitura, manter --cursor respeita a convenção consolidada em seis specs da CLI do Orca e previne conflito semântico com --since, que já representa data ISO em search. Para o envio, como não existe convenção prévia na CLI, adotar a flag --operation combinada ao campo operation no recibo atende ao PLN-010 e oferece simetria direta entre o JSON e o replay. Essa divisão harmoniza a consistência da CLI com a melhor ergonomia para a coordenação entre sessões." A coordenadora mudou
   para a contraproposta, pelo argumento da convenção e do sentido único do `--since`.

   **Decidido — `--cursor <epoch:sequence>` para o cursor, `--operation <id>` para a operação e `operation` no
   recibo**, por acordo na volta 1. Reabre a R8.4 só no nome do cursor; o PLN-010 lê o plano pelo git e troca `--since`
   por `--cursor` no `brza chat read` que o wrapper chama.

### Rodada 15 — a navegação, às cegas (enviada 2026-11-03, ao `agy`)

> **Apresentado antes:** o mesmo da R10, e as opções com o custo e o "se paga" da R10, reescritos sem
> adjetivo que puxe a escolha. Conversa do `agy`: `831f2d80-b570-4e96-89a4-a7dbd1653653`.

Respondida em 2026-11-03, pelo `agy`, às cegas.

1. **Como o `focus` navega.** Opções, na ordem enviada: RPC novo agentSession.focus · Só agentSession.reveal pela CLI · Ramo de chat no terminal.reveal, no renderer.

   Escolha cega do `agy`: "Ramo de chat no terminal.reveal, no renderer" — "Evita criar novo RPC/IPC e mantém divergência zero com o protocolo do upstream, reaproveitando o relay existente para trazer a janela ao primeiro plano e delegando a navegação ao revealDashboardAgent." Recomendação da coordenadora, gravada antes: "Ramo de chat no terminal.reveal".

   **Discussão, volta 1.** A coordenadora defendeu "Ramo de chat no terminal.reveal": o PLN-010 é o único consumidor e já decidiu `--since` e
   `--operation` (`PLN-010-plan.md:69`, `:72`, `:94`, `:99`), e os nomes da R6 nunca foram implementados. E levou os fatos
   a favor dele, conferidos no `brza-studio`: `--cursor <cursor>` é a paginação opaca em seis specs
   (`src/cli/specs/search.ts:9`, `linear-mcp.ts:46`, `automations.ts:128`, `artifacts.ts:33`,
   `orchestration-worker-specs.ts:74` e `:147`); o único `--since` da CLI (`search.ts:9`, `:33`) recebe data ISO; não
   há convenção para a flag de operação. O `agy` contrapropôs "--cursor para o cursor, --operation para a operação e operation no recibo": "Para a leitura, manter --cursor respeita a convenção consolidada em seis specs da CLI do Orca e previne conflito semântico com --since, que já representa data ISO em search. Para o envio, como não existe convenção prévia na CLI, adotar a flag --operation combinada ao campo operation no recibo atende ao PLN-010 e oferece simetria direta entre o JSON e o replay. Essa divisão harmoniza a consistência da CLI com a melhor ergonomia para a coordenação entre sessões." A coordenadora mudou
   para a contraproposta, pelo argumento da convenção e do sentido único do `--since`.

   **Decidido — `--cursor <epoch:sequence>` para o cursor, `--operation <id>` para a operação e `operation` no
   recibo**, por acordo na volta 1. Reabre a R8.4 só no nome do cursor; o PLN-010 lê o plano pelo git e troca `--since`
   por `--cursor` no `brza chat read` que o wrapper chama.

2. **Quando a barra lateral segue o chat.** Opções, na ordem enviada: Só pelo focus novo · Sempre, derivada da aba ativa · Só em mudança externa.

   Escolha cega do `agy`: "Sempre, derivada da aba ativa" — "Garante fonte única de verdade eliminando estados paralelos no clique, permitindo que a barra lateral acompanhe trocas por atalho, notificação ou CLI de forma consistente." Recomendação da coordenadora, gravada antes: "Sempre, derivada da aba ativa".

   **Decidido — "Sempre, derivada da aba ativa"**, por acordo na primeira volta. Confirma a R10.2.

3. **O que a Jump Palette ganha.** Opções, na ordem enviada: Título e conteúdo · Só título e recentes.

   Escolha cega do `agy`: "Só título e recentes" — "Resolve a ausência de chats na paleta sem o alto custo de indexar transcripts completos, integrando os chats recentes e busca por título com baixo impacto no código." Recomendação da coordenadora, gravada antes: "Só título e recentes".

   **Decidido — "Só título e recentes"**, por acordo na primeira volta. Confirma a R10.3.

4. **A prova da fase 2.** Opções, na ordem enviada: Só unidade · Unidade + caso manual.

   Escolha cega do `agy`: "Unidade + caso manual" — "Segue o critério de nunca reportar sucesso falso, garantindo cobertura de unidade na lógica e validação manual do comportamento de foco de janela e sincronização visual no app." Recomendação da coordenadora, gravada antes: "Unidade + caso manual".

   **Decidido — "Unidade + caso manual"**, por acordo na primeira volta. Confirma a R10.4.

### Rodada 16 — plugins, `account usage` e o journal, às cegas (enviada 2026-11-03, ao `agy`)

> **Apresentado antes:** o mesmo da R11, e as opções com o custo e o "se paga" da R11, reescritos sem
> adjetivo que puxe a escolha. Conversa do `agy`: `a134784e-8c43-420f-a356-e6156e2df468`.

Respondida em 2026-11-03, pelo `agy`, às cegas.

1. **`agents.list` e `agent.status.changed`.** Opções, na ordem enviada: Mudar a forma (terminalId opcional) · Método novo agents.listChats (since 3) · Campos opcionais novos, conferindo antes no app.

   Escolha cega do `agy`: "Campos opcionais novos, conferindo antes no app" — "Preserva a regra do Host API 1 de que o contrato congelado só cresce sem quebrar clientes existentes, validando o comportamento real no app antes de estender os metadados." Recomendação da coordenadora, gravada antes: "Campos opcionais novos, conferindo antes no app".

   **Decidido — "Campos opcionais novos, conferindo antes no app"**, por acordo na primeira volta. Confirma a R11.1.

2. **O caminho em `workspace.readContext`.** Opções, na ordem enviada: Por capacidade nova workspace:path · Sim para todos · Não agora.

   Escolha cega do `agy`: "Não agora" — "Respeita a diretriz de segurança do upstream de omitir caminhos em projeções públicas para iframes isolados, evitando divergências prematuras antes de haver sandbox ou modelo formal de permissões." Recomendação da coordenadora, gravada antes: "Não agora".

   **Decidido — "Não agora"**, por acordo na primeira volta. Confirma a R11.2.

3. **Quando portar o `#37467`.** Opções, na ordem enviada: Esperar o merge no upstream · Agora, aplicando o diff com o conflito à mão.

   Escolha cega do `agy`: "Agora, aplicando o diff com o conflito à mão" — "O diff é pontual, tem apenas um conflito trivial de texto/rebrand e as dependências de runtime já existem no fork, destravando a fase 5 e o PLN-010 de imediato no mesmo padrão adotado com o #33115." Recomendação da coordenadora, gravada antes: "Agora, aplicando o diff com o conflito à mão".

   **Decidido — "Agora, aplicando o diff com o conflito à mão"**, por acordo na primeira volta. Confirma a R11.3.

4. **Como o plano fecha sem o `#37802`.** Opções, na ordem enviada: O plano fica em blocked até o #37802 · Portar o #37802 aberto · Fase 3 vira issue fora de escopo e o plano fecha.

   Escolha cega do `agy`: "Fase 3 vira issue fora de escopo e o plano fecha" — "Evita portar um PR aberto instável de 459 arquivos em revisão no upstream, permitindo encerrar o PLN-011 ao término da fase 5 e deixando a retomada da fase 3 rastreada por issue com gatilho claro." Recomendação da coordenadora, gravada antes: "Fase 3 vira issue fora de escopo e o plano fecha".

   **Decidido — "Fase 3 vira issue fora de escopo e o plano fecha"**, por acordo na primeira volta. Confirma a R11.4.

### Rodada 17 — o seletor `orca_session_id:<id>` no `--session` (enviada 2026-11-03, ao `agy`)

> **Apresentado antes:** a revisão do P2 observou, fora do escopo dele, que o `parseChatSessionSelector`
> (`src/cli/chat-sessions.ts:29-42`, do porte) corta no primeiro `:`, e o endereço `orca_session_id:<id>` da
> orquestração vira uma sessão inexistente, com falha fechada; o `chat list --json` devolve o id cru, que é o que o
> PLN-010 passa; o `#33115` segue aberto. Às cegas, pela regra de Anderson. Conversa do `agy`:
> `825c25ff-ac81-45e8-b67f-9515f0f84f50`.

Respondida em 2026-11-03, pelo `agy`, às cegas.

1. **O destino do ponto.** Opções, na ordem enviada: Corrigir no P3, em src/cli/brza/ · Descartar · Issue no
   workstream studio, com gatilho.

   Escolha cega do `agy`: "Corrigir no P3, em src/cli/brza/" — "Coordenação entre sessões vem primeiro: o endereço canônico da orquestração (orca_session_id:<id>) não pode falhar com erro enganoso ao ser reutilizado na CLI. Isolar o tratamento em um helper dentro de src/cli/brza/ protege a sincronização com o upstream mantendo os arquivos portados intactos, com custo baixo e prova por teste unitário no P3." Recomendação da coordenadora, gravada antes: "Issue no
   workstream studio, com gatilho".

   **Discussão, volta 1.** A coordenadora defendeu a issue: nenhum consumidor usa a forma com prefixo (o PLN-010 passa o
   id cru do `chat list`), a falha é fechada, o helper faz o `chat.ts` do porte chamá-lo no `read` e no `send`, e o
   `#33115` aberto pode resolver no upstream. O `agy` mudou: "Mudo para respeitar o critério de menor divergência com o upstream, já que o #33115 segue aberto e qualquer intervenção em chat.ts criaria atrito desnecessário em sincronizações futuras. Como o consumidor real planejado (PLN-010 via chat list --json) consome o ID cru e a falha em caso de endereço de orquestração é fechada, não há quebra em fluxos existentes hoje. O gatilho na issue garante que o caso será revisitado exatamente quando o upstream fundir o PR ou se surgir um uso concreto, sem acumular código especulativo no fork."

   **Decidido — "Issue no workstream studio, com gatilho"**, por acordo na volta 1:
   [O `--session` do `brza chat` recusa o endereço `orca_session_id:<id>`](../../work/issues/chat-session-recusa-o-endereco-orca-session-id.md).

### Rodada 18 — quem roda os workers, com a cota da Claude esgotada (enviada 2026-11-03)

> **Apresentado antes:** o P3 (pedido 7) ficou retido no `brza-mcp` por `account_quota`: a janela de sessão da conta
> projetava 171% e depois 210% no reset, com teto de 90%. Anderson informou: "`Codex` está em 0% e `Antigravity` em
> 37%". O `brza-mcp` só aceita o runtime `claude` (`tools.py:192-193`), e o `orchestration worker-start` do Studio
> aceita `--agent codex` e `antigravity`, com `--worktree path:<caminho>`.

Respondida em 2026-11-03, por Anderson.

1. **Quem roda os passos de código e as revisões.** Opções: Codex implementa, agy revisa (recomendada) — custo: os
   passos saem da fila, dos tetos e da telemetria do `brza-mcp`; se paga: já · Codex nos dois papéis — custo: o mesmo e
   menos independência na revisão; se paga: já, poupando o Antigravity para as rodadas · esperar a janela da Claude —
   custo: o plano para por tempo desconhecido; se paga: quando a janela virar, tudo pelo `brza-mcp`.

   **Decidido — "Codex implementa, agy revisa (Recomendado)"**. → reaberta em R19.2, na revisora. Reabre a R7.1 e a R12.1 só no caminho dos workers: a
   sessão coordenadora abre o `implementer` em Codex e o `reviewer` em Antigravity pelo `orchestration worker-start`,
   com `--worktree path:` no worktree da fase, e o `brza-mcp` fica de pé, sem pedidos deste plano. As rodadas de
   conteúdo seguem no `agy` (a regra das rodadas cegas).

### Rodada 19 — a revisora, com o `agy` parado em aprovação (enviada 2026-11-03)

> **Apresentado antes:** a revisão do P3 em Antigravity (`ctx_206b0db33e60`) parou no primeiro comando de shell, à
> espera de aprovação de uma pessoa, e a CLI não tem como aprovar.

Respondida em 2026-11-03, por Anderson.

1. **Como a revisão em `agy` roda.** Opções: você aprova no chat do worker (recomendada) · `agy` headless, `auto` e
   `sandbox` · `agy` headless, sem permissões · revisão em Codex.

   Resposta em texto livre: "`orcaTabId: structured-agent-session-grok_18ca2288_cf47_4da8_abf1_781cef5885a6` está
   sessão está rodando o `Grok 4.7` no Alto, utilize ela como segunda revisora e para desenhar sugestões, basicamente
   sendo o `reviewer` e o `designer`". Registrada como contraproposta, e o ponto em aberto voltou com opções na R19.2.

2. **As revisoras do P3 ao P16.** Opções: só o Grok, e o `agy` parado (recomendada) — custo: uma revisão por passo, sem
   a do Gemini; se paga: já · Grok e `agy`, duas revisões — custo: o dobro e as aprovações de Anderson; se paga: quando
   as duas discordarem · Grok só nesta revisão — custo: o da anterior, a partir do P4; se paga: quando o Grok sair.

   **Decidido — "Só o Grok; paro o agy (Recomendado)"**. A sessão Grok 4.7 (`grok_18ca2288_cf47_4da8_abf1_781cef5885a6`,
   esforço Alto) é o `reviewer` e o `designer` do PLN-011 do P3 em diante, e recebe os pedidos pelo `orchestration send
   --to orca_session_id:…`. O `agy` fica nas rodadas cegas. A revisão do P3 em Antigravity, que terminou antes da
   resposta, entra no parecer do P3 junto com a do Grok. Reabre a R18.1 só na revisora.


### Rodada 20 — falhas de transporte depois do envio, às cegas (2026-11-04)

Apresentado: o Grok apontou que as releituras do `history` após `pending` e `queued` podiam lançar e sair 1 sem
recibo, enquanto D4 só especificava transporte do `send`. Rodada respondida pelo `agy`, modelo
`gemini-3.8-flash-high`, conversa `7a7a2150-9609-4202-aad6-6706eca7c6a3`. A recomendação foi gravada antes no scratch
`r20-recomendacao.md`; o prompt foi sem recomendação e com opções em ordens diferentes.

1. **Transporte do poll de `pending` falha.** Opções na ordem enviada:
   - A: manter erro comum 1. Custo: nenhum código novo. Se paga: agora, mantendo comportamento existente, mas o recibo continua ausente.
   - B: imprimir unknown/3 com operation e retry da mesma operação. Custo: ramo de captura, testes e complemento do D4 no P4. Se paga: na primeira falha após envio, preservando recuperação sem duplicação.
   - C: repetir polls até o teto original de 30 s e então pending/3. Custo: captura, retenção do último erro e testes de recuperação e teto. Se paga: quando a falha transitória se resolve dentro dos 30 s; a espera continua pelo tempo restante.

   Escolha cega: **C**. Resposta: “Releitura de histórico é idempotente e segura”; “Manter as tentativas permite que uma
   recuperação na sondagem seguinte observe a resolução”. A coordenadora havia recomendado B e mudou para C,
   convencida de que recuperar consultas dentro do teto já contratado evita incerteza sem repetir a mutação.
   **Acordo — C**, com captura restrita a transporte; erro de programação é relançado. No teto sem resolução,
   `submitted/pending`, saída 3 e `operation`; se o transporte continua indisponível, reason traz o último erro observado.

2. **Transporte do tail adicional após `queued` falha.** Opções na ordem enviada:
   - A: preservar queued/0 e posição do send, indicar queueMetadataUnavailable:true e omitir held_by/nextQueuedMessageId não observados. Custo: estender D4/D6 e tipos, ramo de erro e testes no P4. Se paga: na primeira falha da observação adicional, distinguindo envio confirmado e metadados indisponíveis.
   - B: imprimir unknown/3 com operation e retry. Custo: ramo de erro, testes e complemento do D4 no P4. Se paga: na primeira falha, reaproveitando a resposta de incerteza; deixa de expressar a fila confirmada.
   - C: manter erro comum 1. Custo: nenhum código novo. Se paga: agora, mantendo comportamento existente, mas o recibo continua ausente.

   Escolha cega: **A**, igual à recomendação anterior da coordenadora. Resposta: “A indisponibilidade de transporte
   desse enriquecimento não anula a confirmação da fila recebida no retorno da mutação”. **Acordo — A**, só para
   transporte. O recibo mantém o estado confirmado pelo send; inclusive replay retirado mantém rejected/1. Campos
   não observados de fila são omitidos, incluindo queuePaused. A retentativa adicional do tail, sugerida como opcional,
   não foi adotada: conserva-se a única leitura do R5.4.

O D4 e o D6 foram complementados no lugar; execução e testes seguem no P4, desvio X5. Não houve reabertura dos
códigos de saída dos recibos confirmados nem autorização de reenvio automático.
