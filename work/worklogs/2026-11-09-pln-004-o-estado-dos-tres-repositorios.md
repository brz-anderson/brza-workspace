---
scope:
  - workspace
refs:
  - PLN-004
  - PLN-010
  - PLN-012
  - PLN-013
  - PLN-017
  - PLN-018
sessions:
  - 508e76c8-5e4d-4f7f-9e83-7d94df55b2f8
---

# O PLN-004: o estado dos três repositórios

Anderson pediu em 2026-11-09, na sessão `workspace`: "faça um levantamento de tudo que já foi feito nos projetos —
`brza-studio` | `brza-workflow` incluindo CLI e MCP | `brza-workspace` incluindo todos os workstreams — e atualize o
`PLN-004`". O plano é o
[PLN-004: Os runtimes Codex, `agy` e Grok trabalham no fluxo do workspace como o Claude](../../plans/PLN-004-os-runtimes-codex-agy-e-grok-no-fluxo/PLN-004-plan.md);
a sessão anterior está em [O PLN-004: o Grok entra no plano](2026-11-06-pln-004-o-grok-entra-no-plano.md).

## O que se fez

- **Três `collector`s em paralelo**, um por repositório, só leitura. Os agregados estão em
  `/private/tmp/pln004/estado-2026-11-09/` (`studio.md`, `workflow.md` e `workspace.md`). Cada um cruzou o achado com os
  `D1` a `D16` do Desenho v3. A sessão conferiu no disco os fatos que mudam o plano.
- **`brza-workflow@db6bd28`** (86 commits desde 2026-10-30):
  - **o que ainda não existe:** nada do pacote do PLN-004. Não há `packages/runtimes`, wrappers, `.brzAgents`,
    `GROK_HOOK_EVENT` nem `runtime` no `measure.py`. O `brza install` só põe o override do Claude, e o `brza sync` não
    trata link nem `.toml`;
  - **o `brza sessions`:** abre os quatro agentes pelo `orchestration worker-start --agent`, só no chat e sem
    `--surface` (`brza-sessions:926`), e ganhou personas, `wait`, `read`, `close` e `usage` (`3d3d2bb`, `db6bd28`, do
    PLN-017). O `usage` lê o rollout do Codex e dá `unmeasured` ao Grok e ao `agy` (`:792`). O `chat_blocker` recebe
    só o checkout e devolve `None` dentro do workspace (`:168-172`);
  - **o `dispatch` do MCP:** abre workers nos três runtimes, com os modelos do `policy.py:29-41` (`grok-4.7` nos três
    papéis). Não tem sandbox nem papel `reviewer`;
  - **a medida por tarefa:** o PLN-012 mudou o `measure.py` e o resumo. São três caminhos de soma, o custo se chama
    `estimated_cost_usd`, e a tarefa liga a sessão pelo `CLAUDE_CODE_SESSION_ID`;
  - **por `D`:** `D1` a `D6`, `D8`, `D15` e `D16` intactos; `D7` e `D13` parciais; `D9` e `D10` intactos, mas com
    premissas vencidas; `D11` sobreposto ao `dispatch`, como a R20.1 aceitou; `D12` em conflito com o `brza-sessions`
    de hoje;
  - **os testes:** `tests/hooks`, 348 OK; `tests/mcp`, 390 OK; `notes-checker`, passa; `tests/cli` sem
    `BRZA_WORKSPACE`, 581 testes com 2 falhas, que vêm do `CLAUDE_CODE_SESSION_ID` da sessão que rodou, e não de
    código.
- **`brza-studio@8abbde720ce`** (1249 commits desde 2026-10-30, quase todos de refatoração):
  - **as seis suposições do plano valem:** o chat do Grok é ACP e honra o override com argumentos; o app não confia a
    pasta do Grok (sem `preflightTrust`, sem preset, sem `GROK_FOLDER_TRUST` nem `GROK_MEMORY` em `src/`); o chat do
    Antigravity ignora o override (`acp-launch-specs.ts:296`); o chat do Codex roda `… app-server`; o app lê a cota do
    Grok; o Codex chamado pelo Claude ainda não vira subagente;
  - **fato novo:** o app instala sozinho um hook global do Grok em `~/.grok/hooks/orca-status.json`. Ele só age em
    painel de terminal do app e se mescla ao hook de projeto do `D8`;
  - **o que não existe no app:** personas e reunião multiagente.
- **Os seis workstreams** (o índice tem 188 ids):
  - **o que pesa sobre o PLN-004:**
    - o PLN-013 (`tools-kit`, fechado), que já entregou o `--agent` dos quatro e o `dispatch`;
    - o PLN-017 (`playground`, em execução), com as personas no `brza sessions`;
    - o PLN-012 (`tools-kit`), sob o `measure.py`;
    - o PLN-010 (`tools-kit`, entrevista), que troca o transporte do `brza sessions`;
    - a issue das memórias que sobem à norma (`playground`), nas mesmas linhas do `core/AGENTS.md` que o `D4`;
  - **a identidade:** o `env` da `master` manda o Gmail do `brz-anderson` desde 2026-11-03 (`.claude/settings.json:5-7`),
    e o plano ainda dizia noreply;
  - **o checador:** nenhum `backlink-missing`, e nenhum bloqueio em vigor sobre o PLN-004.
- **O F20 do PLN-017 estava errado para o Grok.** Ele dizia que o Grok não grava token. A sessão Grok de hoje no
  `playground` tem `usage.json`, com `inputTokens` 2.632.760, `outputTokens` 24.264 e `costUsdTicks` 18.738.880.000
  (US$ 1,87). A pedido de Anderson ("peça pra ela atualizar o plano"), o fato foi à `playground-06`, que o conferiu e
  o encaminhou à sessão dona do PLN-017 pelo Run dele.
- **O PLN-004 atualizado:**
  - o `Retomar` reescrito com o estado;
  - a Cobertura com a identidade do `env` e a linha do `brza sessions` marcada como entregue pelo PLN-013;
  - o "Fora de escopo" corrigido pela R10.2 e com a linha do Antigravity em `:296`;
  - a seção `## Pendências conhecidas`, com as quatro issues vizinhas;
  - a R21 preparada e não enviada, com nove pontos e a lista do que se corrige na gravação sem rodada.

- **A segunda atualização**, a pedido de Anderson ("atualize o plano"), com o que nasceu depois do levantamento: o
  [PLN-018: O turno do Grok e do Codex entra no log, e a tarefa carimba o id dessa sessão](../../plans/PLN-018-o-grok-e-o-codex-na-medicao/PLN-018-plan.md), do `tools-kit` (aberto na mesma tarde, prioridade alta, commitado lá
  e ainda sem sessão dona), que grava a linha
  `turn` do Grok e do Codex, o terreno do `D9` e da R18.4; e a issue do `playground` sobre o custo do Grok no `brza
  sessions usage`. O `Retomar` os cita, a issue entrou em `## Pendências conhecidas`, e a R21 ganhou o ponto 10, sobre
  quem grava a linha. Depois do commit dele no `tools-kit`, o PLN-018 entrou por link no `Retomar` do PLN-004.

## O que ficou

- **A R21**, quando Anderson retomar as rodadas, e depois o v3 com a R20 e a R21, a aprovação e a gravação do Desenho. O
  `Retomar` do plano diz de onde se parte.
- **O scratch** (`/private/tmp/pln004/`, com o v3 e os agregados de hoje) não vai ao git, e some se a máquina
  reiniciar.
- **As 2 falhas do `tests/cli` do `brza-workflow`** dependem do `CLAUDE_CODE_SESSION_ID` herdado. Não são deste plano,
  e ficam como fato para quem mexer no `brza note`.

## Medida

Corrido 25 min — agente 8 min, quem pediu 16 min, pausa 0 s · US$ 10,42 (turnos 5,45, subagentes 4,97) · CPU 29,25 s do `claude` e 492,30 s dos comandos, RSS até 514 MB · 8 turnos, 1 sessão · até 19:47 de 2026-11-09, pelo `brza note commit`
