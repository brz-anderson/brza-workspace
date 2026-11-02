---
scope:
  - workspace
  - brza-studio
---

# O PLN-004: a revisão do plano contra a migração ao brza-workflow

Anderson pediu, na sessão `workspace`, em 2026-11-02: "revise o plano contra as mudanças feitas no `BrzA Studio`,
`brza-workspace` e `brza-workflow`". O plano é o
[PLN-004: O Codex e o `agy` trabalham no fluxo do workspace como o Claude](../../plans/PLN-004-o-codex-e-o-agy-no-fluxo/PLN-004-plan.md);
o dia anterior está em
[O PLN-004: as sondas da R6 e o Desenho do Codex e do agy](2026-10-31-pln-004-as-sondas-e-o-desenho.md).

## O que se fez

- **O levantamento**, pelo `collector`, com o agregado no scratch da sessão (`pln-004-revisao-mudancas.md`): 38
  citações do plano e do rascunho do Desenho conferidas contra o disco, 19 batem e 19 não, e uma linha por item `D1` a
  `D14` sobre onde o artefato mora hoje. Conferi por conta própria as que pesam: as linhas do app, os três focos no
  `reviewer.md`, o `brza-where` e o `~/.zshrc`.
- **O que a migração do PLN-006 mudou** para o plano:
  - **A norma comum é do núcleo.** O `AGENTS.md`, o `CLAUDE.md`, o `plans/README.md` e o `work/README.md` estão no
    `.brza/core.lock`; editá-los aqui trava o `brza sync` seguinte, e o `core/AGENTS.md` é molde, sem lugar para
    adaptador de runtime. O `README.md` é local.
  - **O sync só escreve o que é do núcleo** (`core/` e `packages/<nome>/core/`): o `.codex/` e o `.agents/` ficam
    intocados, e um pacote novo no manifesto é possível (`brza init --package`), mas só existe o `client`.
  - **O código do `brza` saiu do `brza-workspace`.** O `claude-brza`, o `brza-sessions`, o `brza-agents`, o
    `brza_runtime`, o `measure.py` com os testes e o `summarize_measurements.py` vivem no `brza-workflow`; o `repo_of`,
    o `roots` e o `inside` do `claude-brza` não existem mais, e o `brza install` só liga o `claude` como override. O
    `brza-tree` segue local.
  - **O bloco do shell é do pacote do cliente** (`packages/client/shell/brza.zsh`, com o `brza-where`): o defeito do
    `cd ""` deixou de existir, o `~/.zshrc` só faz `source` dele, e o `codex()` e o `agy()` do `~/.zshrc` continuam
    sendo só da Fixfy.
  - **O `fact_audit.py` e o `measure.py` são só do Claude:** o primeiro chama `claude -p --model haiku` e roda só no
    `SubagentStop` do `settings.json`; o segundo não tem modo `codex` nem `agy`.
  - **O `tools-kit`** não tem item do PLN-004, e o PLN-006 foi executado pela sessão `workspace` nos dois repositórios.
  - **O `brza-workflow` não tem `plans/` nem `work/`** e não cita Codex nem `agy`.
- **No app:** a issue `codex-como-subagente-no-chat-do-claude`, do `studio`, está como estava; o cartão de handoff do
  upstream (#36848) grava um `agent-handoff` quando o chat nativo roda `agent launch`, o que toca o "caminho 1" dela.
- **No plano:** o `Retomar` reescrito (dizia "R6 a R8", e a R9 já estava gravada), e a frente 4 com os três focos de
  revisão, que só estavam no `Retomar`, com a linha da Cobertura.

## O que ficou

- **A rodada 10**, no chat: onde moram `.codex/` e `.agents/`; quem executa o código no `brza-workflow`; o fallback dos
  hooks; o `measure.py` e a auditoria de fatos; onde entram o `codex()` e o `agy()`; onde entra o foco da revisão.
- **O plano passa de 400 linhas** (480 hoje), e o `plans/README.md` manda a Entrevista ao `-interview.md`; a divisão vai
  depois da R10, que ainda acrescenta à Entrevista.
- **O rascunho do Desenho** (556 linhas, no scratch) é reescrito depois da R10, e só então vai à aprovação.
- **As 19 citações que não batem** estão na tabela do agregado; três nunca sustentaram o fato (a linha do app para o
  `app-server` e a `permissionPolicy`, a do `agentCmdOverrides` no terminal e a do X3 do PLN-011).
