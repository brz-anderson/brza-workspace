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

   **Decidido — "Liga da feat, via launchd (Recomendado)"**. Ligado em 2026-11-03: `brza-mcp start` → "de pé", o
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
   `brza sessions`, com o servidor na configuração.

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

   **Decidido — "2 (Recomendado)"**. "Permite ao coordenador e ao wrapper distinguir recomeço por reset de falha real
   diretamente pelo código de saída, sem precisar inspecionar o payload do erro."

2. **O reset repetido.** Opções: aceitar e documentar (recomendada) — custo: uma linha no guia e um teste; até 200
   itens relidos por leitura; se paga: agora · contorno no cliente — custo: ~1 h, revisões antigas perdidas sem aviso;
   se paga: só com medição · mudar o host — custo: contrato `strict` e conflito no sync; se paga: nunca na fase 1.

   **Decidido — "Aceitar e documentar (Recomendado)"**. "Preserva a fidelidade ao contrato do host sem introduzir
   divergências no sync com o upstream, evitando perda silenciosa de revisões no cliente."

3. **Quanto o cursor lê.** Opções: uma página `after` de 200 linhas (recomendada) — custo: recusar o `--limit` e um
   campo; se paga: agora · `--limit` conta linhas — custo: a flag muda de sentido; se paga: só se 200 linhas pesarem ·
   lê até `hasNewer` falso — custo: saída sem teto; se paga: nunca.

   **Decidido — "Uma página after de 200 linhas (Recomendado)"**. "Garante paginação exata por construção e
   previsibilidade de consumo, evitando saída sem teto ou ambiguidade semântica na flag de limite."

4. **Os nomes das flags.** Opções: adotar os do PLN-010 (recomendada) — custo: reescrever a R6.2 e a R6.3 só no nome;
   se paga: já · manter os da R6 — custo: o PLN-010 muda o Desenho; se paga: nunca · os dois, como alias — custo:
   superfície dupla; se paga: nunca.

   **Decidido — "Adotar os do PLN-010 (Recomendado)"**: `--since`, `--operation` e o campo `operation` no recibo, com a
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

   **Decidido — "Esperar o pending resolver, teto 30 s (Recomendado)"**. "Preserva a semântica do código 0 para
   confirmação real e 3 para incerteza na coordenação entre sessões, sem nunca reportar sucesso falso antes da entrega
   resolver."

2. **Os valores do `held_by`.** Opções: `question | working | null` (recomendada) — custo: um campo e dois testes; se
   paga: na fase 1 · com `paused` e `blocked` — custo: o `blocked` não aparece na página; se paga: só se o wrapper agir
   diferente · só `question | working` — custo: valor falso; se paga: nunca.

   **Decidido — "question | working | null (Recomendado)"**, com `queuePaused: true` na pausa. "Evita reportar working
   falso quando a fila já escoou ou está pausada, mantendo o held_by fiel aos dados reais expostos pelo histórico."

3. **O replay `returned` ou `withdrawn`.** Opções: sair 1, `rejected` (recomendada) — custo: duas linhas e dois testes;
   se paga: no primeiro retry depois de um Stop · sair 0 — custo: diz "na fila" para o que não sai; se paga: nunca.

   **Decidido — "Sair 1, com submission.state rejected (Recomendado)"**. "Cumpre o princípio de nunca reportar sucesso
   falso em replays de mensagens retiradas ou com falha definitiva que não serão entregues."

4. **Onde mora a extensão.** Opções: `src/cli/brza/` (recomendada) — custo: quatro arquivos pequenos; se paga: no sync
   do `#33115` fundido · tudo no `chat.ts` — custo: conflito em cada função; se paga: no sync, nunca.

   **Decidido — "Em src/cli/brza/, com o chat.ts só chamando (Recomendado)"**. "Isola as extensões do fork no padrão
   das outras pastas brza/, minimizando divergências e conflitos no rebase com o upstream após o merge do #33115."

### Rodada 10 — a navegação (enviada 2026-11-03, ao `agy`)

> **Apresentado antes:** o Terreno da fase 2, no [Desenho](PLN-011-design.md).

Respondida em 2026-11-03, pelo `agy`.

1. **Como o `focus` navega.** Opções: ramo de chat no `terminal.reveal`, no renderer (recomendada) — custo: o nome
   enganoso e 1 teste; se paga: na fase 2 · RPC novo `agentSession.focus` — custo: schema, catálogo e IPC novos; se
   paga: se o upstream aceitar · só `agentSession.reveal` — custo: não traz a janela; se paga: nunca.

   **Decidido — "Ramo de chat no terminal.reveal, no renderer (Recomendado)"**. "Evita criar RPCs e schemas novos que
   gerem conflitos no sync com o upstream, reusando o relay existente para trazer a janela ao primeiro plano e
   resolvendo a aba no renderer."

2. **Quando a barra lateral segue.** Opções: sempre, derivada da aba ativa (recomendada) — custo: ajustar dois
   arquivos, com testes; se paga: na fase 2 · só em mudança externa — custo: dois estados; se paga: nunca · só pelo
   `focus` — custo: atalho e notificação divergem; se paga: nunca.

   **Decidido — "Sempre, derivada da aba ativa (Recomendado)"**. "Elimina o estado duplicado que causa a divergência
   visual relatada, mantendo a barra lateral sempre sincronizada com a aba ativa independente da origem da navegação."

3. **O que a Jump Palette ganha.** Opções: só título e recentes (recomendada) — custo: ramo novo no builder e na
   ativação; se paga: na fase 2 · título e conteúdo — custo: indexar transcript; se paga: só com busca de conteúdo.

   **Decidido — "Só título e recentes (Recomendado)"**. "Atende à navegação de chats na Jump Palette com menor
   divergência e sem a sobrecarga ou complexidade de indexar o texto dos transcripts."

4. **A prova da fase 2.** Opções: unidade e caso manual (recomendada) — custo: ~20 min de Anderson no app; se paga: no
   fim da fase 2 · só unidade — custo: nenhum de Anderson; se paga: agora, sem prova do foco da janela.

   **Decidido — "Unidade + caso manual (Recomendado)"**. "Cumpre a diretriz de comprovar a lógica com testes de
   unidade e verificar manualmente no app o foco de janela e a experiência visual real."

### Rodada 11 — plugins, `account usage` e o journal (enviada 2026-11-03, ao `agy`)

> **Apresentado antes:** o Terreno da fase 4 e o D11, no [Desenho](PLN-011-design.md); o `#37802` segue aberto, com
> 459 arquivos, e a R4.3 manda a fase 3 esperar a integração.

Respondida em 2026-11-03, pelo `agy`.

1. **`agents.list` e o evento.** Opções: campos opcionais novos, conferindo antes no app (recomendada) — custo: o minor
   não sobe; se paga: na fase 4 · método novo `agents.listChats` — custo: superfície nova; se paga: se o plugin precisar
   detectar · mudar a forma — custo: quebra o contrato; se paga: nunca.

   **Decidido — "Campos opcionais novos, conferindo antes no app (Recomendado)"**. "Respeita a regra frozen da Host API
   1 de que resultados apenas crescem sem quebrar plugins existentes, além de validar antes no app o comportamento real
   das sessões."

2. **O caminho em `workspace.readContext`.** Opções: não agora (recomendada) — custo: o plugin segue adivinhando o
   `cwd`; se paga: até a sandbox do worker · por capacidade nova — custo: manifest e diálogo; se paga: com plugin de
   status line · sim para todos — custo: `cwd` e `transcriptPath` em frames isolados; se paga: nunca.

   **Decidido — "Não agora (Recomendado)"**. "Mantém a restrição intencional contra o vazamento de caminhos locais e
   transcrições para frames isolados antes da introdução de sandboxing ou modelo de permissões."

3. **Quando portar o `#37467`.** Opções: agora (recomendada) — custo: 1 conflito trivial e o rebrand das strings; se
   paga: na fase 5 · esperar o upstream — custo: a CLI só no sync; se paga: no próximo sync.

   **Decidido — "Agora, aplicando o diff com o conflito à mão (Recomendado)"**. "O diff é restrito à CLI, tem
   dependências prontas no fork e traz apenas um conflito trivial de rebrand, liberando o avanço da fase 5 e o consumo
   pelo PLN-010."

4. **Como o plano fecha sem o `#37802`.** Opções: a fase 3 vira issue fora de escopo e o plano fecha (recomendada) —
   custo: a frente do journal volta por issue; se paga: ao fim da fase 5 · o plano fica `blocked` — custo: aberto por
   tempo indefinido; se paga: quando o upstream integrar · portar o PR aberto — custo: 459 arquivos instáveis; se paga:
   nunca, enquanto aberto.

   **Decidido — "Fase 3 vira issue fora de escopo e o plano fecha (Recomendado)"**. "Mantém a decisão da R4.3 de não
   absorver 459 arquivos de um PR instável no upstream e permite encerrar o plano ao concluir a fase 5 sem bloqueios
   indefinidos."
