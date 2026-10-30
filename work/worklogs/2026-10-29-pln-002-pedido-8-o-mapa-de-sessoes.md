---
scope:
  - workspace
---

# O PLN-002, pedido 8: o /rename opcional e o mapa de sessões, desenhados

O pedido, em 2026-10-29, na sessão `pln-002-sessions-rename`, aberta pela sessão do `brza-workspace` que conduz o
PLN-001: retomar o PLN-002 pela plan-runner para o pedido de Anderson, "tornar o /rename opcional no `brza sessions`,
que vem desabilitado por padrão, o comando deve apenas nomear a aba no app […] e gravar num mapa de sessões, que pode ser
usado pelo orquestrador/coordenador". O registro está no
[PLN-002: Os passos manuais que se repetem entre sessões viram comandos `brza`](../../plans/PLN-002-os-comandos-brza/PLN-002-plan.md).

## O que se fez

**A leitura:** o `scripts/brza/brza-sessions` inteiro, o D7, a R9 e a R10 do PLN-002, e o D48 ao D50 e o P64 do PLN-001.
Sem o `/rename`, o `list`, o `send`, o `close`, o `running()` e o `--wait` perdem a fonte do nome; o título da aba sai do
`agentSession.rename`.

**Três rodadas, todas na recomendada, menos duas:**
- **R11:** o pedido 8 no PLN-002, com o D7 reescrito e o P9; uma revisão só, depois do P9; a flag `--rename`; o
  `--title` opcional, com o `<nome>` sem ele.
- **R12:** o mapa em **JSONL só de acréscimo** (fora da recomendada, que era JSON por nome); a leitura pelo
  `list --json`; o mapa antes do `/rename` na busca, o que reabre a R9.1; o P64 do PLN-001 sem o mapa.
- **R13:** o `.sessions/sessions.jsonl` do workspace; o `--wait` sem `--rename` espera o `claude_session`; **o verbo
  `brza sessions title`** (fora da recomendada, que era não agora); o `--rename` para a sessão de correio, na ajuda e
  na memória.

**O registro:** a R11 a R13 na Entrevista, com a R9.1 e a R9.2 reabertas; o D7 reescrito no lugar, com o mapa, o
`--json` crescido pelo `source` e pelo `opened`, os pontos "A conferir no P9" e as alternativas descartadas; o pedido 8,
cinco linhas de Cobertura, o P9 (2,5 h), o C5 e a regressão do `--wait`, no plano, que volta a `in_progress`.

## O que ficou

- **O P9**, que espera a autorização de Anderson, nesta sessão, começando pela combinação.
- **A revisão da entrega**, do P0 ao P9, depois dele (R11.2).
- **A linha no `Retomar` do PLN-001**, que vai no P9.5, com o `from=` medido; escrita agora, diria o que o código ainda
  não faz.
- **O `-plan.md` do PLN-002 passou de 400 linhas.** O `Pedido`, os `Passos` e os `Casos manuais` são do `-plan` pela
  norma; não há sufixo para eles.
