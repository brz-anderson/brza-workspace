---
status: done
scope:
  - workspace
opened: 2026-11-02
completed: 2026-11-02
tags:
  - tooling
---

# REV-003: o `brza-workflow` dos passos P1–P7 do PLN-006, em `b9210a6`

Revisão adversária do `reviewer`, em 2026-11-02, de
[PLN-006: O `brza init` monta a norma num workspace do zero](../../plans/PLN-006-o-brza-init-monta-a-norma-do-zero/PLN-006-plan.md),
antes do P8. A régua foi a Cobertura, o Desenho, as rodadas R1–R16 e os desvios X1–X26, e não a devolução de quem
implementou. Os experimentos rodaram em clones temporários, com `HOME`, `GIT_CONFIG_GLOBAL` e `BRZA_REGISTRY` de
mentira; nada foi rodado contra o `~/.local/bin`, o `~/.config` ou o `brza-workspace` reais. A sessão refez a evidência
do A1, do A2 e do A6. Os destinos foram escolhidos pela regra de Anderson para o plano, "escolha sempre o recomendado".

## Achados

### A1 — O primeiro sync do P8 desfaria o P11 do PLN-005, sem recusa

> bug · importante · confiança 97 · → corrigido aqui

**Evidência:** `git -C ~/Projects/brza-workspace log --oneline d85c783..origin/master` → `2c9a546` e `cfa058e`; o
`fact_audit.py` do núcleo tinha o `shasum` da `d85c783` (`552d631860`), e não o da `origin/master` (`7fd3b2f60c`); o
`brza-sync --dry-run --core-only` num clone da `master` saiu com 0 e escreveria o `fact_audit.py`, os dois scripts e o
`CLAUDE.md` antigos, porque o arquivo fora do lock é sobrescrito (R15.1). Corrigido no `brza-workflow@ebeb779`, o
porte dos dois commits.

### A2 — O manifesto do P8 sem `[checker]` faria o checador dar 18 erros no `studio`

> bug · importante · confiança 90 · → corrigido aqui

**Evidência:** `core/.claude/hooks/brza_root.py:560-561` põe o `worklogs_link_from` no `born` quando o `[checker]`
falta; o checador de hoje usa `2026-10-28` (`check_notes.py:51`); com `2026-10-26`, o checador do núcleo nos worktrees
reais dá 18 erros no `studio`, e o `brza note commit` recusaria lá. O P8 grava o manifesto do `brza-workspace` com
`[checker].worklogs_link_from = "2026-10-28"`.

### A3 — O D12 tira o `brza_runtime.py` de `scripts/brza/` sem trocar o cabeçalho dos scripts locais

> lacuna · importante · confiança 90 · → corrigido aqui

**Evidência:** `brza-app:29-30`, `brza-dev:31-32`, `brza-shot:38-39`, `brza-test:31-32` e `brza-tree:40-41` fazem
`sys.path.insert(0, HERE)` e importam o `brza_runtime` vizinho; o cabeçalho novo só está no docstring do
`bin/brza-install:24-31`, e nenhum item do D12 o aplica. O P8 troca o cabeçalho dos cinco antes de tirar o runtime.

### A4 — O `changed` que não chegou ao índice nunca se repara

> bug · importante · confiança 95 · → corrigido aqui

**Evidência:** issue criada, status mudado num commit com `--no-push`, outro commit com push e `brza note index
--rebuild` → "em dia", com o índice em `open` e o workstream em `in_progress`; o `rebuild` (`bin/brza-note:557-588`)
pula todo id que já está no índice, contra o D11 e o X11. O `--rebuild` passa a comparar o vigente com o `HEAD` de cada
branch.

### A5 — O `brza init --branch main` cria um workspace sem `plan-open`

> bug · importante · confiança 97 · → corrigido aqui

**Evidência:** o init com `--branch main` sai com 0, e o `plan-open` dá `recusado: a origin/master não existe`;
`bin/brza-note:99` fixa a `master`, `:371-404` o `origin` e `:253` o `push -u origin`. A R15.4 deixou isso "até haver
workspace com outro remote", e o P5 passou a criá-lo. O índice e o push passam a ler o manifesto.

### A6 — O esqueleto de issue do `brza note new` nasce reprovado pelo checador do mesmo núcleo

> bug · importante · confiança 97 · → corrigido aqui

**Evidência:** o molde `ISSUE` do `bin/brza-note:125-133` não tem `description`, e o checador do núcleo a exige na nota
nova desde `2026-11-01` (`DESCRIPTION_FROM`); o teste de aceite do init passava porque roda o checador num workspace
sem nota. Depois do P8, nenhum workstream commitaria issue nova. O esqueleto ganha o campo.

### A7 — Duas issues de mesmo nome em workstreams diferentes viram um id só

> bug · sugestão · confiança 95 · → corrigido aqui

**Evidência:** reproduzido com os workstreams `app` e `outro`: a segunda `issue:<slug>` toma o estado vigente da
primeira, que some. Hoje não há nome repetido no `brza-workspace`. O `commit` passa a recusar a nota nova cujo id já
é de outro workstream.

### A8 — Texto do app e desta máquina no núcleo genérico

> desvio · sugestão · confiança 92 · → corrigido aqui

**Evidência:** `core/CLAUDE.md:22` traz `/private/tmp/claude-501/…` e o chat do app; `open-and-plan.md:57-64` traz o
`ORCA_CHAT_SCRATCH_DIR`, a skill `orca-chat-visuals` e o `::orca-visual`; nem o `FOREIGN` do `bin/brza-init:58` nem o
teste de ouro procuram `orca` ou `claude-`. O texto vai ao pacote do cliente, e a conferência passa a procurá-lo.

### A9 — O X26 aponta o molde errado, e há mais nome do `brza-studio` no `bin/brza-note`

> desvio · sugestão · confiança 95 · → corrigido aqui

**Evidência:** o "O pedido de Anderson" do `bin/brza-note:117` é do molde de worklog, e não do de issue; há nome do
`brza-studio` em `:4` e `:193-213`.

### A10 — A Cobertura e o D12 não sabem do workstream `brand` nem do PLN-007

> lacuna · sugestão · confiança 95 · → corrigido aqui

**Evidência:** a Cobertura (R5.1) diz "PLN-001 a PLN-006", e o D12, item 7, três workstreams; existem o `brand` e o
PLN-007, e a `master` diz "Último PLN usado: 007". O P8 confere o índice contra todos os workstreams e planos.

### A11 — O `brza-sync` e o `brza-init` dizem rodar no 3.9

> desvio · sugestão · confiança 90 · → corrigido aqui

**Evidência:** a suíte do sync não carrega no `/usr/bin/python3` 3.9.6, e a camada 2 chama o `brza-note`, que exige o
3.10 (X6). Os docstrings passam a dizer o que roda no 3.9: os hooks e o `brza_root`.

### A12 — O `--relink` apaga arquivo que não é link

> bug · importante · confiança 95 · → falso

**Por que é falso:** a recusa do plano vem antes de qualquer `unlink`.

**Evidência:** `bin/brza-install:121-122` e `:142-143`.

### A13 — Um caminho `../` no lock apaga arquivo fora da raiz

> bug · importante · confiança 95 · → falso

**Por que é falso:** o guard do sync roda o `git status` no caminho, que recusa o que está fora do repositório.

**Evidência:** entrada plantada com o sha256 certo → "is outside repository", e o arquivo ficou.

### A14 — O `brza init` escreve fora do diretório

> bug · importante · confiança 95 · → falso

**Por que é falso:** fora do diretório, só o registro é escrito, e por último (X24).

**Evidência:** a fumaça com `HOME` e `BRZA_REGISTRY` temporários; nada mudou fora do diretório e do registro.

### A15 — O commit do índice perde linha ou mexe no checkout principal

> bug · importante · confiança 92 · → falso

**Por que é falso:** ele parte da `origin/master` recém-buscada e empurra sem force, por commit sem checkout.

**Evidência:** duas mutações no índice derrubaram 2 e 3 testes; o checkout principal sujo ficou idêntico.

### A16 — O núcleo público vaza segredo ou dado pessoal novo

> bug · importante · confiança 90 · → falso

**Por que é falso:** o que há de pessoal nos testes já estava no `brza-workspace`, também público, e não há segredo.

**Evidência:** a varredura da árvore do `brza-workflow@b9210a6`.

## O que rodou

`tests/cli` → 372 OK; `tests/hooks` → 244 OK, e no 3.9.6 → 244 OK, 5 skips; checador → saída 0. Três experimentos
em clones temporários, com o dry-run do estágio 2 do P8.
