---
status: open
phase: interview
origin: request
ready: "não — falta a entrevista: o levantamento do PLN-011 da Fixfy e a rodada 2"
scope:
  - workspace
  - brza-studio
opened: 2026-10-30
owner: Anderson
tags:
  - tooling
---

# PLN-004: O Codex e o `agy` trabalham no fluxo do workspace como o Claude

- **Retomar:** aberto, com a R1 trazida da sessão `brza-workspace-80`. O próximo é o levantamento do PLN-011 da Fixfy
  por peça, pelo `collector`, com o agregado no scratch, e a rodada 2 com os pontos sem lastro.

## Pedido

- **Origem:** pedido livre, no chat do BrzA Studio, na sessão `brza-workspace-80` ("Integrar codex e agy ao fluxo"),
  aberta na `master`, de 2026-10-30. A partida é o PLN-011 da Fixfy (R1.3),
  `~/Projects/fixfy/plans/PLN-011-claude-codex-e-antigravity-no-mesmo-ecossistema/`. Toca o
  [PLN-001](../PLN-001-o-brza-studio-generico/PLN-001-plan.md), que já marca os passos que outro runtime pode executar,
  e a issue
  [O Codex chamado pela sessão Claude aparece como subagente no chat do BrzA Studio](../../work/issues/codex-como-subagente-no-chat-do-claude.md),
  do `studio`, que se liga a este plano (R1.2).

"vamos integrar o `codex` e o `agy` ao nosso fluxo de trabalho" — Anderson, em 2026-10-30.

As frentes do pedido, pela R1.2, numeradas para a Cobertura:

1. **Base:** o adaptador no `.codex/config.toml` e em `.agents/rules/`, e as funções `codex` e `agy` para o
   brza-workspace e o brza-studio, com a identidade do `brz-anderson` (R1.4) e a `BRZA_WORKSPACE`;
2. **Papéis e memória:** o `collector`, o `implementer`, o `reviewer` e o `designer` em `.codex/agents/*.toml` e
   `.agents/agents/*.md`, gravando na memória do workstream, gerados para não divergir do `.claude/agents/`;
3. **Medição:** o `measure.py` lendo o rollout do Codex e o transcript do `agy`, com o runtime em cada linha;
4. **Delegação e sessões:** a sessão Claude manda revisão e levantamento ao Codex e ao `agy`, só leitura, e o
   `brza sessions` abre sessão Codex ou `agy` no worktree.

### Cobertura

> Rascunho: os critérios são propostas até a rodada que os confirma; o passo e o teste saem do Desenho.

| Origem   | Critério de aceite                                                                                                                  | Passo | Teste (nível) |
| :------- | :---------------------------------------------------------------------------------------------------------------------------------- | :---- | :------------ |
| `R1.2` 1 | o `codex` e o `agy` abertos no brza-workspace, no brza-studio e nos worktrees deles leem a norma do `AGENTS.md` pelo adaptador próprio | —     | —             |
| `R1.2` 1 | o commit feito numa sessão Codex ou `agy` sai com o noreply do `brz-anderson` e vai pela chave `personal` (R1.4)                      | —     | —             |
| `R1.2` 2 | os quatro papéis existem nos três runtimes, gerados de uma fonte só, e a geração acusa a divergência                                 | —     | —             |
| `R1.2` 2 | o papel rodado no Codex ou no `agy` grava na memória do workstream da sessão                                                         | —     | —             |
| `R1.2` 3 | a sessão Codex e a `agy` geram linhas em `.measurements/measurements.jsonl`, com o `runtime` e o `workstream`                        | —     | —             |
| `R1.2` 4 | a sessão Claude pede revisão e levantamento ao Codex e ao `agy` sem que eles gravem no repositório                                   | —     | —             |
| `R1.2` 4 | o `brza sessions` abre uma sessão Codex ou `agy` no worktree do workstream                                                           | —     | —             |

### Fora de escopo

- **O que é só da Fixfy** — as contas `fixfy-*`, o `fixfy-plugin`, a guarda —, pela R1.3. Fica no PLN-011 de lá.
- **O código do `brza`** — o `brza sessions`, o `claude-brza` —, pela R1.1. Vai como pedido ao `tools-kit`, que o
  executa numa sessão dele.
- **O Codex como cartão de subagente no chat do BrzA Studio.** Fica na issue do `studio`, ligada a este plano pela R1.2.

## Entrevista

### Rodada 1 — destino, escopo, partida e identidade (enviada 2026-10-30)

**Apresentado antes**, na sessão `brza-workspace-80`:
- **Os binários:** `codex-cli 0.164.0` e `agy 1.4.8` instalados. As funções `codex` e `agy` do `~/.zshrc` só tratam a
  Fixfy (`fixfy_where`); fora dela, chamam o binário puro, sem a identidade e sem a medição.
- **A norma:** neutra — o `AGENTS.md` mais um adaptador por runtime —, mas só existe o adaptador do Claude, o
  `CLAUDE.md`.
- **O que já toca o assunto:** o PLN-001 marca os passos para outro runtime
  (`workstream/studio:plans/PLN-001-o-brza-studio-generico/PLN-001-plan.md:933`), e a issue
  `workstream/studio:work/issues/codex-como-subagente-no-chat-do-claude.md` trata o Codex chamado pela sessão Claude.
- **O precedente:** o PLN-011 da Fixfy, com as peças em `~/Projects/fixfy/.codex/` (`config.toml` com
  `developer_instructions`, `agents/*.toml`, `hooks.json`) e em `~/Projects/fixfy/.agents/` (`rules/runtime.md`,
  `agents/*.md`, `hooks.json`, `mcp_config.json`, `plugins.json`). Lá, o P4, o P5, o P8.5 e o P9 foram reabertos (R27),
  e o P13, o guia de custo por peça, não foi feito.

Respondida em 2026-10-30, na sessão `brza-workspace-80`, e trazida a este plano sem perguntar de novo. O custo e o
"se paga" de cada opção ficaram naquela sessão; chegaram aqui as opções e as respostas.

1. **Destino.** Opções:
   - PLN-004 no workspace (recomendada);
   - PLN-004 no tools-kit;
   - emenda ao PLN-003.

   **Decidido — "PLN-004 no workspace (Recomendado)".** O que é código do `brza` (`sessions`, `claude-brza`) vai como
   pedido ao `tools-kit`.

2. **Escopo**, seleção múltipla. Opções:
   - Base: adaptador e shell;
   - Papéis e memória;
   - Medição;
   - Delegação e sessões.

   **Decidido — as quatro**, como estão no Pedido. A delegação inclui um pedido ao `tools-kit` e a issue do `studio`
   ligada ao plano.

3. **Partida.** Opções:
   - portar o PLN-011 (recomendada);
   - desenhar do zero.

   **Decidido — "Portar o PLN-011 (Recomendado)".** Um `collector` levanta as peças da Fixfy, os desvios X1–X8 e os
   passos reabertos; o desenho tira o que é só de lá (as contas `fixfy-*`, o `fixfy-plugin`, a guarda).

4. **Identidade.** Opções:
   - brz-anderson, igual ao Claude (recomendada);
   - uma conta por runtime.

   **Decidido — "brz-anderson, igual ao Claude (Recomendado)".** As funções do shell exportam o mesmo
   `GIT_AUTHOR_*`/`GIT_COMMITTER_*` e o `GIT_SSH_COMMAND` do `env` do `.claude/settings.json`.

## Worklogs

- 2026-10-30 — aberto; R1 trazida da sessão `brza-workspace-80`. Parou antes do levantamento do PLN-011.
  [O PLN-004: a abertura do Codex e do agy no fluxo](../../work/worklogs/2026-10-30-pln-004-a-abertura-do-codex-e-do-agy-no-fluxo.md)
