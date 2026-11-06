---
status: open
phase: interview
origin: request
ready: "não — faltam o Desenho e os Passos"
scope:
  - workspace
  - brza-studio
opened: 2026-10-30
owner: Anderson
tags:
  - tooling
---

# PLN-004: Os runtimes Codex, `agy` e Grok trabalham no fluxo do workspace como o Claude

- **Retomar:** a Entrevista fechou até a R19. A 12.2 saiu decidida pela medição (o Claude padrão nos três focos; o
  `agy` e o Codex como segundo passe, por `--runtime`); a R13 e a R14 fixaram a norma do pacote, o render do `.toml`,
  o `tomllib` e os modelos (Codex: `gpt-6-astra` em `high`, sem a medição do `high`); a R15 decidiu o papel no `brza
  delegate` e o `--runtime` obrigatório; a R16 e a 16.5 puseram `agents` e `skills` em `.brzAgents/`, com
  `.claude/agents` e `.claude/skills` como links, o D15 emendado, e a memória dos subagentes real em
  `.claude/agent-memory/`, com `.brzAgents/memory` como link para ela. A R18 (2026-11-06) trouxe o Grok ao plano, pelo
  pedido de 2026-11-03: um wrapper `grok-brza` com `GROK_FOLDER_TRUST=0`, o adaptador em `.grok/rules/runtime.md`, e
  os hooks do núcleo saindo cedo com `GROK_HOOK_EVENT`, com um `.grok/hooks/runtime.json` do pacote chamando o
  `measure_runtimes.py grok`. A R19 decidiu o `GROK_MEMORY=0` no wrapper, os papéis herdando o modelo do pai e o Grok
  no D12; a 19.3, depois da medição que Anderson pediu (`/private/tmp/pln004/bench/out/pontuacao-grok.md`), pôs o
  `brza delegate --runtime grok` em `--permission-mode plan --sandbox read-only`, com `grok-4.6` em `medium`. Falta a
  R17 de volta (a medição, o `~/.zshrc` e as sessões, P8 a P11 do `designer`, agora com o Grok), o Desenho reescrito
  com o `.brzAgents` e o Grok (D1, D4, D5, D7, D8, D9, D11, D12, D15 e D16) no `pln-004-design-v2.md`, no scratch, e a
  aprovação, na mensagem, antes de gravá-lo em `PLN-004-design.md`. O código passa ao `brza-workflow`, com o pacote
  `packages/runtimes`, executado pela sessão `workspace`.
- **Dividido:** [PLN-004 — Entrevista](PLN-004-interview.md)

## Pedido

- **Origem:** pedido livre, no chat do BrzA Studio, na sessão `brza-workspace-80` ("Integrar codex e agy ao fluxo"),
  aberta na `master`, de 2026-10-30. A partida é o plano de chats do workspace de origem (R1.3). Toca o
  [PLN-001](../PLN-001-o-brza-studio-generico/PLN-001-plan.md), que já marca os passos que outro runtime pode executar,
  e a issue
  [O Codex chamado pela sessão Claude aparece como subagente no chat do BrzA Studio](../../work/issues/codex-como-subagente-no-chat-do-claude.md),
  do `studio`, que se liga a este plano (R1.2).

"vamos integrar o `codex` e o `agy` ao nosso fluxo de trabalho" — Anderson, em 2026-10-30.

"agora temos que inserir também o `Grok`" — Anderson, em 2026-11-03, na sessão `workspace`; entra neste plano pela
R18.1. O Grok é o Grok Build CLI 1.0.70, e entra nas quatro frentes abaixo; o que ele já lê do `.claude/` — a norma, as
skills, os papéis e os hooks — não pede gerador nem link novo.

As frentes do pedido, pela R1.2, numeradas para a Cobertura:

1. **Base:** o adaptador no `.codex/config.toml` e em `.agents/rules/`, e as funções `codex` e `agy` para o
   brza-workspace e o brza-studio, com a identidade do `brz-anderson` (R1.4) e a `BRZA_WORKSPACE`;
2. **Papéis e memória:** o `collector`, o `implementer`, o `reviewer` e o `designer` em `.codex/agents/*.toml` e
   `.agents/agents/*.md`, gravando na memória do workstream, gerados para não divergir do `.claude/agents/`;
3. **Medição:** o `measure.py` lendo o rollout do Codex e o transcript do `agy`, com o runtime em cada linha;
4. **Delegação e sessões:** a sessão Claude manda revisão e levantamento ao Codex e ao `agy`, só leitura, e o
   `brza sessions` abre sessão Codex ou `agy` no worktree. Esta frente leva também os três focos de revisão —
   simplicidade, defeito e convenção —, um por runtime, que Anderson mandou para cá na triagem do porte das skills do
   workspace de origem, em 2026-10-31 ("Com a frente 4", no [O porte das skills do workspace de origem para o workspace](../../work/worklogs/2026-10-31-o-porte-das-skills-do-workspace-de-origem.md)).

### Cobertura

> Rascunho: os critérios são propostas até a rodada que os confirma; o passo e o teste saem do Desenho.

| Origem   | Critério de aceite                                                                                                                  | Passo | Teste (nível) |
| :------- | :---------------------------------------------------------------------------------------------------------------------------------- | :---- | :------------ |
| `R1.2` 1 | o `codex` e o `agy` abertos no brza-workspace, no brza-studio e nos worktrees deles leem a norma do `AGENTS.md` pelo adaptador próprio | —     | —             |
| `R1.2` 1 | o commit feito numa sessão Codex, no worktree, sai com o noreply do `brz-anderson`, e o push vai pela chave `personal` com a aprovação de Anderson (R1.4, R5.3); o `agy` não comita (R5.1) | —     | —             |
| `R3.3`   | a medição do Codex grava o `guardian_review` numa linha própria, ligada ao pai e fora da soma dele (R5.2)                           | —     | —             |
| `R3.1`   | a memória gravada fora do Claude leva `metadata.runtime`, e o evento `memory` o carrega (R4.1)                                      | —     | —             |
| `R18.2`  | o `grok` aberto pelo `grok-brza` — no terminal e no chat do app, pelo `agentCmdOverrides.grok` — carrega a norma, as skills, os papéis e o `env` do projeto no brza-workspace, no brza-studio e nos worktrees | —     | —             |
| `R18.3`  | a sessão Grok lê o vocabulário do `.grok/rules/runtime.md`, e não o do adaptador do Claude Code                                     | —     | —             |
| `R18.4`  | numa sessão Grok confiada, os hooks do núcleo saem sem gravar, e a linha da sessão vem do `measure_runtimes.py grok`, com o filho fora da soma do pai | —     | —             |
| `R1.2` 2 | os quatro papéis existem nos três runtimes, gerados de uma fonte só, e a geração acusa a divergência                                 | —     | —             |
| `R1.2` 2 | o papel rodado no Codex ou no `agy` grava na memória do workstream da sessão                                                         | —     | —             |
| `R1.2` 3 | a sessão Codex e a `agy` geram linhas em `.measurements/measurements.jsonl`, com o `runtime` e o `workstream`                        | —     | —             |
| `R1.2` 4 | a sessão Claude pede revisão e levantamento ao Codex e ao `agy` sem que eles gravem no repositório                                   | —     | —             |
| `R1.2` 4 | o `brza sessions` abre uma sessão Codex ou `agy` no worktree do workstream                                                           | —     | —             |
| `R1.2` 4 | a revisão delegada roda com um foco por runtime: simplicidade, defeito ou convenção                                                  | —     | —             |

### Fora de escopo

- **O que é só do workspace de origem** — as contas de lá, o plugin de lá, a guarda —, pela R1.3. Fica no plano de chats de lá.
- **O código do `brza`** — o `brza sessions`, o `claude-brza` —, pela R1.1. Vai como pedido ao `tools-kit`, que o
  executa numa sessão dele.
- **O chat Antigravity do BrzA Studio.** É um servidor ACP gerenciado pelo app, que não é o `agy` e ignora o
  `agentCmdOverrides` (`brza-studio/src/main/acp/acp-launch-specs.ts:261-265`); o `agy` deste plano é o do terminal e o
  do `brza sessions`.
- **O Codex como cartão de subagente no chat do BrzA Studio.** Fica na issue do `studio`, ligada a este plano pela R1.2.

## Entrevista

As rodadas R1–R19 estão em [PLN-004 — Entrevista](PLN-004-interview.md), por passarem de 400 linhas.

## Worklogs

- 2026-10-30 — aberto; R1 trazida da sessão `brza-workspace-80`; o levantamento do plano de chats de origem; R2 a R4; as sondas; R5; o rascunho
  do Desenho, pelo `designer`; R6. Parou nas sondas da R6.1.
  [O PLN-004: a abertura do Codex e do agy no fluxo](../../work/worklogs/2026-10-30-pln-004-a-abertura-do-codex-e-do-agy-no-fluxo.md)
- 2026-10-31 — as sondas da R6.1; o `/hooks` de Anderson, sem o hook rodar; R7 e R8. Parou na
  aprovação do Desenho.
  [O PLN-004: as sondas da R6 e o Desenho do Codex e do agy](../../work/worklogs/2026-10-31-pln-004-as-sondas-e-o-desenho.md)
- 2026-10-31 — fora do plano, a triagem do porte do workspace de origem mandou à frente 4 os três focos de revisão.
  [O porte das skills do workspace de origem para o workspace](../../work/worklogs/2026-10-31-o-porte-das-skills-do-workspace-de-origem.md)
- 2026-11-02 — a revisão do plano contra a migração ao `brza-workflow` (PLN-006), o `Retomar` e a frente 4 com os três
  focos; R10 a R12, e as medições da auditoria de fatos e da revisão por runtime. Parou no desenho do experimento da
  12.2.
  [O PLN-004: a revisão do plano contra a migração ao brza-workflow](../../work/worklogs/2026-11-02-pln-004-a-revisao-contra-o-pln-006.md)
- 2026-11-03 — a R12.2 decidida (o Claude como padrão, o `agy` e o Codex como segundo passe) e a divisão do plano em
  `-plan` e `-interview`. Parou antes do Desenho.
  [O PLN-004: a R12.2 fecha e o plano se divide](../../work/worklogs/2026-11-03-pln-004-a-12-2-fecha-e-o-plano-se-divide.md)
- 2026-11-06 — a R18 (o Grok entra no plano, com o `grok-brza`, o `.grok/rules/runtime.md` e os hooks saindo cedo), o
  plano renomeado, a R19 e a medição da 19.3 no banco da R12.2 (o `grok-4.6` em `medium`, em `plan` com `--sandbox
  read-only`). Parou antes da R17 de volta.
  [O PLN-004: o Grok entra no plano](../../work/worklogs/2026-11-06-pln-004-o-grok-entra-no-plano.md)
