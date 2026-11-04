---
status: done
scope:
  - workspace
opened: 2026-11-02
completed: 2026-11-02
tags:
  - tooling
---

# REV-004: a migração do `brza-workspace` para cliente do `brza-workflow`, o P8 do PLN-006

Revisão adversária do `reviewer`, em 2026-11-02, do P8 de
[PLN-006: O `brza init` monta a norma num workspace do zero](../../plans/PLN-006-o-brza-init-monta-a-norma-do-zero/PLN-006-plan.md),
contra o D12, a Regressão e o parecer anterior,
[REV-003: o `brza-workflow` dos passos P1–P7 do PLN-006, em `b9210a6`](REV-003-pln-006-o-brza-init.md). Os destinos seguiram a
regra de Anderson para o plano, "escolha sempre o recomendado".

**Incidente.** O ensaio do segundo sync, rodado de um clone temporário, escreveu na `master` real o commit `fa4152f`,
com o autor `t <t@t>`, só no `.brza/core.lock` e sem push: a `BRZA_WORKSPACE` herdada da sessão venceu o cwd (A1). A
trava do runtime barrou o `reset` do revisor, a sessão não o repassou, e Anderson escolheu "Eu rodo o reset
(Recomendado)": `git reset --keep bca0a4f`, e a `master` voltou à `origin`.

## Achados

### A1 — O `brza sync` e o `brza note` escrevem no workspace da `BRZA_WORKSPACE`, e não no do cwd

> bug · importante · confiança 97 · → corrigido aqui

**Evidência:** `core/.claude/hooks/brza_root.py:434-440` toma a variável como raiz mesmo com o cwd em outro
repositório, com `role=None`, e só o `brza-where` confere o papel; `cd exp1/ws && BRZA_WORKSPACE=exp2/ws brza-sync
--core-only --no-push` → o commit cai no `exp2`; no real, o `fa4152f`. O `brza sync` e todo subcomando do `brza note`
passam a recusar, com os dois caminhos na mensagem.

### A2 — O README local ainda tem o bloco antigo do shell

> desvio · importante · confiança 96 · → corrigido aqui

**Evidência:** `README.md:57-90` mantinha o bloco antigo e "mude aqui e copie para lá", contra o `brza.zsh:3` e o
`~/.zshrc:51-54`; a `.claude/rules/brza-client.md:11` manda ler a seção. Corrigido em `brza-workspace@f12fdd4`.

### A3 — A norma não diz que a norma comum se edita no `brza-workflow`

> lacuna · importante · confiança 93 · → corrigido aqui

**Evidência:** `AGENTS.md:61` e `agent-instructions-writer/SKILL.md:41,58` mandavam editar na `master`; num clone, um
commit no `AGENTS.md` da `master` e o `brza-sync --dry-run --core-only` → `recusado: AGENTS.md`, saída 1, em toda
rodada. A regra entra no `core/` dos dois.

### A4 — O `--dry-run` diz "nada", e o sync real commita só o lock

> bug · sugestão · confiança 97 · → corrigido aqui

**Evidência:** com o `brza-workflow` em `6d6ad2f`, que só mudou o README dele, o dry-run imprime `dry-run: nada foi
escrito`, e o real gera um commit só do lock (`bin/brza-sync:363-380`). O lock passa a mudar só com arquivo mudado.

### A5 — O legado do X10 não saiu

> desvio · sugestão · confiança 95 · → corrigido aqui

**Evidência:** `bin/brza_runtime.py:35-42` cai no `~/Projects/brza-workspace` sem workspace achado, com o manifesto
`{}`. O `discover()` passa a devolver `None`, e quem precisa do workspace recusa.

### A6 — Texto local saiu do núcleo sem destino local

> lacuna · sugestão · confiança 90 · → corrigido aqui

**Evidência:** o gate de testes do `reviewer.md:36` e as linhas do `work/README.md` sobre as notas de outro
workspace (`:177`) não chegaram à `.claude/rules/workspace.md` nem ao README. Corrigido em `brza-workspace@f12fdd4`.

### A7 — A volta dos links depende do `/private/tmp`

> lacuna · sugestão · confiança 85 · → corrigido aqui

**Evidência:** 8 dos 13 alvos de `links-antes.txt` não existem desde o `bbe723b`; a volta funciona por `git worktree
add --detach <dir> a45018c`, com os oito `--help` saindo com 0, e o worklog não o dizia. Premissa: o macOS limpa o
`/private/tmp`. O worklog do dia passou a trazer o comando e a lista.

### A8 — A docstring do `measure.py:24` ainda cita o `resume_guard.py`

> desvio · sugestão · confiança 95 · → corrigido aqui

**Evidência:** `core/.claude/hooks/measure.py:24`.

### A9 — O worktree acharia o próprio worktree como raiz

> bug · importante · confiança 95 · → falso

**Por que é falso:** o `brza_root` sobe pelo git common dir ao checkout principal.

**Evidência:** o `brza-where` e o `--settings` dão `/Users/andepb/Projects/brza-workspace` de dentro de
`.worktrees/workspace`.

### A10 — A migração perdeu script, teste ou comportamento do `settings.json`

> bug · importante · confiança 93 · → falso

**Por que é falso:** cada script e teste apagado tem o par no `brza-workflow`, e a chave `hooks` não mudou.

**Evidência:** os 9 scripts apagados têm link em `~/.local/bin` para o `brza-workflow`; `git diff 948fd91 a45018c --
.claude/settings.json` vazio.

### A11 — Os achados A2, A3 e A10 do parecer anterior voltaram

> bug · importante · confiança 95 · → falso

**Por que é falso:** os três seguem fechados.

**Evidência:** o checador dá 0 erros nos quatro worktrees; o índice tem os 29 ids, com o workstream certo; os cinco
scripts locais respondem ao `--help`, e `scripts/brza/tests` dá 94 OK.

### A12 — A Regressão do plano não se sustenta

> bug · importante · confiança 92 · → falso

**Por que é falso:** o `brza note commit`, o `brza note sync` e a trava do `/compact` funcionam num clone com remote
bare, e a função `claude` roteia certo nos quatro lugares.

**Evidência:** no clone `exp2`, o commit deu o push e gravou `changed` na `origin/master`; o sync mesclou `studio` e
`workspace`; o `compact_guard pre` deu `block` no 3.9 e no 3.15; os `turn` e `subagent` desde as 12:55 levam o
`workstream`.

## O que rodou

`brza-where` em sete lugares; os 15 `--help`; o `brza-doctor`; `scripts/brza/tests` → 94 OK no 3.15; no
`brza-workflow`, `tests/hooks` → 283 OK, `tests/cli` → 395 OK, o checador → 0; experimentos em
`/private/tmp/pln006/rev/exp1` e `exp2`.
