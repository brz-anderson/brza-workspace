---
status: done
description: Revisão independente de P4a, P4b e P6 do PLN-017, com sondas reais, contratos do runtime e encerramento guardado.
scope:
  - brza-workflow
  - workspace
opened: 2026-11-09
completed: 2026-11-09
tags:
  - chat
  - tooling
---

# REV-022: As primitivas do brza sessions e a exceção transitória do PLN-010

Revisão independente por `reviewer` Opus, em Claude, das alterações sobre `brza-workflow@d38e7b4` e da emenda ao
PLN-010 em `workstream/tools-kit`. A primeira tentativa por Antigravity recusou o modelo antes do briefing; o
recurso foi liberado e a mesma Task retomada por Claude, conforme o guia e o precedente da memória.

Régua: D2/R5/R6 do PLN-017; R7 literal de Anderson em 2026-11-09, sessão **Retomar PLN-017**; adaptações confirmadas
para `status`, `--all` somente leitura e `--peek --wait`; R3.1 literal e o custo estimado de 0,5 h transmitidos no
pedido de P6. O executor preservou a R2.1 e os passos bloqueados do PLN-010/011.

## Achados e destinos

### A1 — Fila, marcador, aba liberada e janela do histórico → corrigidos

Confiança: 90 a 92. O replay de `queued.state` devolvido era anunciado como enviado; o marcador cortava no último
dois-pontos; a espera não resolvia o worker após auto-release; e `check --all` só trazia cem mensagens.
**Evidência:** `brza-sessions:410`, `:483`, `:539`, `:568`; quatro testes reproduziram os quatro defeitos antes.
A correção normaliza os estados, usa o primeiro separador, inclui o mapa dos liberados e recupera o histórico por
`inbox` somente leitura, validando Run e normalizando remetente/payload. Os eventos alheios são preservados.

### A2 — Dispatch falho e cota sem id do provedor → corrigidos

Confiança: 85 e 88. A espera podia chegar ao timeout sem mostrar que o Dispatch falhou, ou não achar o rollout do
Codex sem `--wait` na abertura. **Evidência:** `brza-sessions:568`, `:640`; testes
`test_wait_observes_a_stopped_dispatch_without_worker_done` (`test_brza_sessions.py:1180`) e
`test_wait_quota_uses_provider_session_even_without_wait_at_open` (`:1185`), com rollout realista e persistência do id.

### A3 — Perda do relatório parcial de fechamento → corrigido

Confiança: 85. O erro do segundo alvo apagava o resultado do primeiro. **Evidência:** `brza-sessions:705`;
`test_close_prefix_reports_the_first_success_and_the_second_refusal`, `test_brza_sessions.py:1202`.
O erro agora é uma linha do alvo, mantendo `closed`, `refused` e a guarda de custódia.

### A4 — Medição após auto-release e leitura individual do ciclo de vida → corrigidas

Confiança: 85 e 80. O id do provedor só era conservado com `--wait`; um erro em `worker-show` derrubava todo o `list`.
**Evidência:** `brza-sessions:329`, `:949`; testes `test_list_preserves_other_personas_when_a_dispatch_cannot_be_read`
(`test_brza_sessions.py:1195`) e `test_open_without_wait_preserves_measured_provider_for_after_release` (`:1234`).
O segundo testa Claude e Codex após remover as abas e fazer o histórico recusar; o caso real do Codex foi medido
depois da liberação. O id tardio do Claude também é conservado pelo `wait`, com regressão própria em `:1292`.

### A5 — Teste do hook dependente do ambiente → corrigido

Confiança: 95. O novo teste podia ler o workspace real em vez da fixture. **Evidência:** o teste de `usage` do Claude
isola `workspace_root`; o revisor rodou a suíte com e sem a variável e comparou à base. As quatro falhas antigas com
`BRZA_WORKSPACE` e as duas com `CLAUDE_CODE_SESSION_ID` já existem no `d38e7b4` e ficaram fora deste diff.

### A6 — Abertura concorrente e recibos incertos → corrigidos

Confiança: 90. A guarda foi reconferida sob a trava, impedindo uma segunda abertura após a espera pelo lock.
Os envelopes reais de `stop_unknown`/`release_unknown` podem vir sem objeto `error` e agora conservam a incerteza.
**Evidência:** `brza-sessions:59`, `:901`; `test_open_rechecks_the_name_under_the_launch_lock`
(`test_brza_sessions.py:1255`), e testes dos envelopes sem `error` em `:1216` e `:1226`.

### A7 — Falha da inspeção apagava `stop_unknown` → corrigida

Confiança: 90. Uma inspeção posterior indisponível substituía o recibo incerto por `refused`.
**Evidência:** `brza-sessions:697`, `:705`; `test_stop_unknown_survives_a_failed_followup_observation`,
`test_brza_sessions.py:1262`, falhou antes. O retorno conserva recibo, `observation_error`, `stop_unknown` e saída 75,
sem liberar, abandonar ou repetir a parada.

### A8 — Falha do poll apagava eventos e pendentes → corrigida

Confiança: 85. `worker-show` indisponível fazia a espera perder o lote.
**Evidência:** `brza-sessions:627`, `:639`, `:683`; `test_wait_poll_failure_preserves_events_and_pending_persona`,
`test_brza_sessions.py:1273`, falhou antes. A observação agora fica em `lifecycle_error`, sem declarar conclusão.

### A9 — Precedência do encerramento falho sem regressão → corrigida

Confiança: 95. O código já preservava `failed` sobre um status mais antigo, mas a primeira mutação sobrevivia.
**Evidência:** `test_worker_done_failed_cannot_be_overwritten_by_an_older_status`, `test_brza_sessions.py:1283`;
o revisor refez a mutação e confirmou a queda do teste novo.

### A10 — Emenda à R1.4 e texto do fechamento → corrigidos

Confiança: 80 a 95. Retomar, Cobertura e linha histórica da R1.4 agora apontam o recorte transitório; o link resolve
pela árvore das branches e o plano aponta o worklog. **Evidência:** `PLN-010-plan.md:25`, `:73`, `:95`, `:191` e
`## Worklogs`; `check_notes.py`, zero erros e avisos. O número de testes e as provas reais do worklog foram atualizados
após a R2; SHAs, push e duração entram no fechamento mecânico da tarefa.

### A11 — Observação de `worker_done` sem regressão própria → corrigida

Confiança: 95, gravidade baixa, achado da R3. A proteção já estava correta, mas sobrevivia à mutação.
**Evidência:** `test_wait_worker_done_observation_failure_keeps_pending_and_events`, `test_brza_sessions.py:1299`;
os 100 testes passam, e retirar o `except` da observação faz esse teste falhar com saída 1 em vez de 75.
O teste e a mutação foram executados depois da devolução final, sem alterar código de produção.

## Hipóteses que caíram

- **Escalation genérica deveria virar `blocked` → falso.** O host a emite no fim normal de uma rodada que não manda
  `worker_done`, como a R6 manda. **Evidência:** a rodada inicial real fechou `done` por status e deixou a escalation
  em `events`; classificá-la como bloqueio derrubaria a rodada normal.
- **Reabrir a estimativa de 0,5 h de P6 → falso no pedido vigente.** **Evidência:** a executora recebeu expressamente
  essa estimativa para os três recursos, com a troca posterior somente do transporte; a atribuição foi corrigida
  para esse pedido, sem nova decisão implícita.
- **`info: null` quebra o Codex ou `usage` lê campos que o hook não grava → falso.** **Evidência:** fixture com
  contador nulo e último total válido; conferência das linhas reais do hook, sem alteração de `measure.py`.
- **Medição após a liberação foi presumida → falso no estado final.** **Evidência:** mapa isolado
  `pln-017-sonda/smoke-sessions.jsonl`, `pln017-smoke-usage-after-release.log` e `pln017-smoke-final-show.json`,
  mais os testes dos dois agentes medidos com histórico indisponível.

## O que rodou e o que deu

O revisor executou sondas sobre o código, comparou as falhas ambientais à base e realizou mutações das correções;
cada mutação relevante derrubou o teste correspondente. A R2 conferiu 98 testes e CLI ampla com 576 testes verdes
no estado de 95 testes específicos; o delta seguinte é coberto pela suíte específica e pela última conferência.
O executor obteve **100 testes** no estado final e **90** no snapshot isolado de P4a, antes de separar os commits.
A CLI final passou em **580 testes**, antes de acrescentar somente o teste A11. A R3 conferiu o delta e os registros,
sem bloqueio de código; L1, N1, N2 e N3 ficaram fechados, e a lacuna A11 foi corrigida após a devolução.

Hooks: 348 verdes no Python principal e no do sistema, com cinco ignorados neste último. MCP: 390 verdes. Scripts
do workspace: 113 verdes fora do sandbox. Runner de notas: saída zero. Checador: zero erros e avisos. A CLI ampla
final e os hashes de publicação ficam no worklog da tarefa.

Pareceres completos no scratch da executora, pasta `pln-017-sonda`: `review-p6.md`, `review-p4-p6.md`,
`review-p4-p6-r2.md` e `review-p4-p6-r3.md`; `last-test-mutation.log` comprova A11. Não se converteram limites
abaixo de 80 em aceite presumido.

## Referência

[O `brza sessions` recebe as primitivas da reunião e o PLN-010 registra a transição pelo `rpc`](../worklogs/2026-11-09-pln-017-sessions-e-excecao-ao-pln-010.md).
