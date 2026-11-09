---
scope:
  - brza-workflow
  - workspace
tags:
  - chat
  - tooling
refs:
  - PLN-010
  - PLN-012
  - PLN-017
  - REV-022
---

# O `brza sessions` recebe as primitivas da reunião e o PLN-010 registra a transição pelo `rpc`

## Plano aceito em 2026-11-09

Anderson pediu "coordene a execução do P4, P5 e P6". Esta sessão executora recebeu P4a, P4b e P6 do
[PLN-017: A reunião multiagente com personas roda como fluxo replicável: skill, `brza sessions` e painel no chat](../../plans/PLN-017-a-reuniao-multiagente-como-fluxo-replicavel/PLN-017-plan.md):
sondar a híbrida e os contratos reais antes do código; escrever testes que falham antes; implementar a menor mudança;
revisar, validar e publicar no `brza-workflow`; emendar somente a exceção transitória no PLN-010. P5 ficou com outra
executora. P1, P2, P7, `measure.py`, os arquivos do PLN-012 e o plano do playground ficam fora desta execução.

As decisões recebidas foram R3.1, R3.2, R4.1 e R6, de 2026-11-08, sessão `workflow-improvements`, incluindo
"Recibo, --operation e read --last pelo rpc", "wait completo, latência e usage do Codex" e
"Testar a híbrida; se falhar, worker-start puro".

## Sondas antes do código

Início observado: **2026-11-09 às 12:50:53 -03**. Executora `9e9e3082-55be-4d10-b0a4-8796db1798a7`.
O executável veio de `ORCA_CLI_COMMAND`, e os guias versionados `orchestration`, `orca-cli`,
`low-level-topology`, `coordinator-loop` e `recovery-and-cleanup` foram carregados.

- O Run **`run_7ec4f06af9d7`** isolou a sonda sob a identidade da executora. Nenhum `check` consumiu a mailbox
  do Run principal `run_2287f933d683`. Uma tentativa inicial de usar a identidade de outro chat foi recusada com
  `consumer_fenced`, sem efeitos; não houve contorno da proteção.
- A híbrida foi repetida com `--model gpt-6.1-sol --effort medium`, worktree explícito e status seguido de
  `worker_done`: Dispatch `ctx_6bf318c6cfca`. `worker-show --full` confirmou `autoReleaseAt: null`,
  `ownershipState: external` e `retainedReason: external_terminal`. A faixa apareceu sem contagem de encerramento.
  **Resultado: via pura**, conforme a R6 já autorizada.
- Claude, Codex, Grok e Antigravity abriram com `mode: structured` pelo `worker-start`, enviaram status com
  `round_id` e Dispatch e encerraram com `worker_done`. Claude, Codex e Antigravity foram observados depois do prazo
  com `releaseState: released`; o Grok exibiu "Fecha em 1:49" e **Manter aberto** na árvore e na captura da UI.
- O handle puro é `structworker_<UUID>`; o chat real vem de `terminalResource.endpointIncarnation`,
  `structured:<UUID>`, no `worker-show --full`. Não se deduz o chat pelo prefixo do handle.
- `setOption model` foi aceito em Claude e Codex. O host recusou uma operação `sonda-...` e aceitou o formato
  emitido, timestamp mais entropia. O replay da mesma operação, após o fence mudar de 1 para 2, retornou
  `replayed: true` e a submissão original, sem duplicação. `updatedAt` mudou ao entrar em `working`.
- Fora de chat e sem variáveis de identidade, `run-create` recusou com `no_active_sender_terminal`, saída 1.
  Indisponibilidade não foi convertida em aceite.

As saídas brutas e capturas estão no scratch da sessão, pasta `pln-017-sonda`, em especial
`hybrid-explicit-settled.json`, `pure-*-show.json`, `pure-*-after-deadline.json`, `grok-ui.json`,
`setOption-*-valid.json`, `operation-replay-after-close.json` e `identity-outside-chat-mutation.json`.

## Desvios técnicos e decisão posterior

**X1 — tipo da mensagem.** O host recusou `send --type message` e `check --types message,worker_done` com
`invalid_argument`, saída 1. A coordenação orientou em `msg_ceb458855bd2`: usar **`status`**, preservando a R6,
e exigir remetente, Dispatch e identificador da rodada. `--payload` não combina com flags estruturadas;
os três identificadores vão no mesmo JSON. O `--all` recupera status já entregue, e `--peek --wait` observa novos
eventos sem consumir/ack; o lote inteiro permanece disponível, inclusive perguntas e escalations.

**R7 — encerramento ativo**, resposta literal de Anderson em 2026-11-09, sessão **Retomar PLN-017**, recebida pela
coordenação: "Pedir encerramento; --force usa parada guardada (Recomendado). Custo: implementar e testar pedido por
mailbox, estado closing e protocolo de parada com confirmação; --force pode interromper trabalho ativo. Se paga: ao
encerrar uma persona travada, preservando a função do --force." O guia confirmou: `worker-release` só aceita
settled. `stop_unknown` não autoriza repetir, abandonar nem declarar fechado; `retained` também não é fechamento.

## Implementação e verificação

O código fica em `bin/brza_runtime.py`, `packages/client/bin/brza-sessions`, `tests/cli/test_brza_sessions.py` e
`README.md` do `brza-workflow`. O mapa conserva Dispatch/Run/remetentes, modelo/esforço, recibos, rodada e latência;
o fallback legado continua sem Dispatch. O leitor de uso não altera o hook.

Base: **47 testes**, OK. P4a acrescentou 17 testes que falharam antes (3 falhas e 14 erros); P4b acrescentou seis,
também falhando antes. Casos adicionais cobrem a R7, identidade, eventos antigos, uso após fechamento automático,
mudança parcial de modelo e prevenção de relançamento incerto. A suíte chegou a **100 testes verdes**: 47 anteriores
e 53 novos. O snapshot separado de P4a passa em **90 testes**, e P4b acrescenta os dez testes restantes.

O teste real pelo CLI novo abriu `pln017-smoke`, recebeu `pending` sem anunciar sucesso no envio, leu o status da
segunda rodada por mailbox com Dispatch e operação, devolveu latência de **32,063 s** e preservou 18 eventos.
`usage` achou o rollout e seus totais; `close` devolveu **`closing`**, e a persona enviou `worker_done` depois.
A primeira rodada expôs `round_id` só no body; o teste passou a exigir o comando com payload explícito no briefing.
A repetição real da rodada inicial devolveu `done` por mailbox em **30,996 s**, preservou 21 eventos e terminou com
`releaseState: released`. O `usage` real continuou medido depois da liberação da primeira persona, aberta com `--wait`;
os testes de Claude e Codex também provam a persistência sem essa flag. O mapa isolado
é `pln-017-sonda/smoke-sessions.jsonl`; os logs são `pln017-smoke-initial-wait.log` e
`pln017-smoke-usage-after-release.log`, e os `*-final-show.json` comprovam a liberação. O Grok também foi observado
`released` após o prazo, completando a evidência dos quatro runtimes.

Comando específico: `env -u BRZA_WORKSPACE PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/cli -p test_brza_sessions.py`.
Checagens amplas concluídas: CLI com **575 testes** na versão intermediária de 94 testes específicos; hooks com
**348**, MCP com **390** e scripts do workspace com **113**, verdes. Os hooks também passaram no Python do sistema,
com cinco casos ignorados por compatibilidade. MCP e scripts foram repetidos fora do sandbox após bloqueios de
swap e de `ps`/Chrome; essas falhas de ambiente não foram tratadas como aceite. O runner de `tests/notes-checker/run.py`
passou; o checador das notas deu **0 erros e 0 avisos**. A repetição final da CLI deu **580 testes verdes**, em
193,785 s, no código de produção final com 99 testes específicos; o centésimo teste, pedido na última revisão,
acrescenta somente a regressão de uma proteção já presente. Os 100 específicos passaram em 0,390 s, e a mutação que
retira essa proteção derruba o teste novo. Não houve mudança de produção depois da CLI ampla.

## Revisão e destino dos achados

P6 foi revisto por `reviewer` Opus em Claude, Dispatch `ctx_075bd0f81637`. A tentativa anterior pelo Antigravity
recusou o modelo para a autenticação atual antes do briefing (`ctx_68b25cc5174f`), e o recurso foi liberado.
O retry usou a mesma Task, conforme o guia e o precedente da memória do workstream.

Do parecer de P6: A1 (prazo no Retomar), A2 (marcadores da R1.4) e A4 (link dependente do worktree) foram corrigidos;
A5 (ponteiro para este worklog) foi acrescentado. A3 propôs reabrir o custo de 0,5 h: **falso no pedido vigente**,
que transmite expressamente essa estimativa para a troca dos três recursos. A atribuição foi corrigida para o pedido
de P6 recebido em 2026-11-09, sem inventar nova estimativa ou executar o PLN-010/011.

P4a e P4b passaram por duas rodadas de revisão independente de código, com sondas sobre o código e mutações dos
testes. Foram corrigidos: Dispatch falho sem `worker_done`; cota do Codex sem id no mapa; resultado parcial de
`close --prefix`; ids de Claude/Codex no `open` sem `--wait`; falha individual de `list`; isolamento do teste do hook;
recibo incerto sem objeto `error`; corrida de abertura; preservação da incerteza quando a inspeção falha; preservação
de eventos e pendentes quando o poll falha; e precedência de `worker_done failed`. As quatro condições de fila,
marcador, auto-release e histórico de 100 mensagens também receberam regressões que falharam antes da correção.
O id tardio do Claude passou a ser conservado durante o `wait`, com teste próprio. A R3 confirmou esse delta, fechou
os achados de código e pediu a última regressão da observação de `worker_done`; ela foi acrescentada e derrubou o
mutante sem a proteção. O parecer e os destinos ficam em
[REV-022: As primitivas do brza sessions e a exceção transitória do PLN-010](../reviews/REV-022-pln-017-sessions-e-transicao-rpc.md).

**Pendência para P7, sem mudança do contrato:** o caminho real do envio ocioso pode devolver `pending`, saída 75,
antes da confirmação do provedor. A R2.1 continua valendo: a coordenação deve ir ao `wait` ou repetir somente com a
mesma operação e o mesmo texto, sem novo disparo cego. A adequação da skill cabe à coordenação do playground.
As quatro falhas antigas com `BRZA_WORKSPACE` e as duas com `CLAUDE_CODE_SESSION_ID`, reproduzidas pelo revisor na
base `d38e7b4`, não foram corrigidas nesta tarefa; o comando exigido sem `BRZA_WORKSPACE` passa na executora.

## Fora do workspace

- **O quê e onde:** arquivos de código e testes no `brza-workflow`, listados acima. **Risco:** regressão dos comandos
  de sessões. **Estado:** commits `3d3d2bb` e `db6bd28` publicados na `master`. **Como desfazer:** reverter
  o commit específico de P4, sem tocar os commits do PLN-012.
- **O quê e onde:** chats e Run da sonda no runtime do Studio, com mapa de integração no scratch. **Risco:** abas
  temporárias remanescentes. **Estado:** workers puros encerram pelo ciclo de vida; chats híbridos ficam retidos
  como recursos externos, sem declarar liberação inexistente. **Como desfazer:** fechar apenas as abas da sonda
  identificadas no scratch, preservando as sessões de trabalho.


## Fechamento e publicação

- **P4a:** concluído, commit `3d3d2bbadcb39102765b9bb9d3f9bc75a12a8a33`, na `master` do `brza-workflow`;
  snapshot independente com 90 testes verdes antes do commit.
- **P4b:** concluído, commit `db6bd28ea7f09d7797090c24f0b181a1f1180971`, na mesma `master`;
  100 testes específicos verdes sobre o estado commitado.
- **Push do código:** `d38e7b4..db6bd28`, confirmado pelo remote `personal:brz-anderson/brza-workflow.git`;
  author e committer dos dois commits são `brz.anderson.pereira@gmail.com`. A árvore de código ficou limpa.
- **P6:** concluído na emenda do PLN-010; notas, REV-022 e memória são publicados pelo `brza note commit`
  na branch `workstream/tools-kit`, no próprio commit que versiona este registro. O SHA fica no recibo final
  da entrega à coordenação; não se cria uma referência circular ao hash dentro do próprio commit.
- **Revisão:** três rodadas independentes de código, sem bloqueio final; a última lacuna de teste foi corrigida
  com o centésimo caso e mutação comprovadamente vermelha, sem mudar código de produção.
- **Validação final:** 100 específicos, 580 na CLI ampla antes do último teste somente de regressão, 348 hooks,
  390 MCP, 113 scripts e runner de notas; checador sem erros e avisos. Logs preservados no scratch `pln-017-sonda/logs`.

## Tempo medido da executora

**1.007 h (60.40 min)** até 2026-11-09T18:06:10-03:00, obtidas dos
`task_started`/`task_complete` do rollout da própria executora, somando o turno atual até esse marco. Os três
turnos concluídos somam **2307,054 s**; a retomada começou em **2026-11-09 às 17:44:13 -03**. O intervalo suspenso
entre 13:29:46 e 17:44:13 não foi contado. A evidência é `pln-017-sonda/own-turn-times.json`.

O tempo é agregado: não se inventou uma divisão entre P4a, P4b e P6, executados de forma intercalada. Revisores
rodam em sessões próprias; não se duplicou seu tempo na soma da executora nem se estimou custo em US$.
Sem `CLAUDE_CODE_SESSION_ID` nesta sessão Codex, não se fabricou a `## Medida` do hook; o `brza note commit`
registra o que o ambiente permite. O fechamento destas notas leva poucos segundos depois do marco acima.
