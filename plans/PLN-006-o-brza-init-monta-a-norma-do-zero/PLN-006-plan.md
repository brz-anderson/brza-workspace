---
status: done
phase: closed
origin: request
description: O brza init monta a norma num workspace do zero, e o brza-workspace a segue do brza-workflow pelo brza sync.
ready: sim
estimate_h: 27
executed_h: 5.4
remaining_h: 0
scope:
  - workspace
opened: 2026-10-31
completed: 2026-11-02
owner: Anderson
tags:
  - tooling
---

# PLN-006: O `brza init` monta a norma num workspace do zero

- **Retomar:** fechado em 2026-11-02. O `brza-workspace` segue o `brza-workflow@a313ec5` pelo `brza sync`; as sobras
  estão em [As sobras do PLN-006 no brza-workflow e no plano](../../work/issues/as-sobras-do-pln-006.md).
- **Dividido:** [PLN-006 — Entrevista](PLN-006-interview.md) · [PLN-006 — Desenho](PLN-006-design.md)

## Pedido

- **Origem:** pedido livre, na sessão do workstream `workspace` de 2026-10-31.

> "nós já temos mecanismos para inicializar a norma inteira, com AGENTS CLAUDE plans/ wiki/ work/ skills/ agents/ num
> repositório do zero?"

Respondido que não, Anderson pediu: "plano".

### Cobertura

| Origem         | Critério de aceite                                                                                                                                                                                  | Passo  | Teste (nível)                                         |
| :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----- | :---------------------------------------------------- |
| `Pedido 1`     | `brza init <dir>` cria, num diretório vazio, um workspace com `AGENTS.md`, `CLAUDE.md`, `README.md`, `plans/`, `wiki/`, `work/`, `.claude/skills/`, `.claude/agents/`, hooks e `settings.json`, e o `notes-checker` roda verde nele | P5     | unidade, num diretório temporário                     |
| `R1.2`         | O workspace inicializado aponta para o repositório de código dele, sem caminho fixo a `brza-workspace` ou `brza-studio` no que foi copiado                                                         | P3, P5 | unidade                                               |
| `R1.4`         | Uma mudança no núcleo genérico chega ao workspace inicializado pelo `brza sync`, sem tocar a parte local dele                                                                                     | P6     | unidade                                               |
| `Pedido 1`     | O `brza-workspace` segue funcionando depois da separação genérico/local: hooks, skills, `brza note` e os testes de hoje                                                                            | P1, P7, P8 | as três suítes (unidade); a Regressão (manual)    |
| `R4.1`, `R7.1` | Do repositório de código, inclusive de um worktree fora do diretório dele, o `brza where`, os hooks e o `claude-brza` acham o workspace pelo `~/.config/brza/workspaces.toml`; sem entrada, nada; o `brza register` recusa ligar um código a dois workspaces | P2 | unidade, com `BRZA_REGISTRY` e um worktree temporário |
| `R4.4`         | O `CLAUDE.md` do workspace inicializado começa com `@AGENTS.md`                                                                                                                                    | P3     | unidade                                               |
| `R5.1`, `R5.3` | `brza note plan-open` numera pelo índice (maior + 1) e grava `created` na `origin/master`; dois `plan-open` em corrida saem com números diferentes                                                 | P4     | unidade, com remote bare local                        |
| `R5.3`, `R7.4` | `brza note commit` de plano, issue ou decisão com frontmatter mudado acrescenta uma linha `changed` na `origin/master` sem tocar o checkout principal; sem mudança, nenhuma linha                  | P4     | unidade                                               |
| `R5.2`         | Duas linhas acrescentadas em paralelo se juntam pelo `merge=union`, e o estado vigente de cada id é o de maior `ts`                                                                                | P4     | unidade                                               |
| `R5.1`         | Depois da migração, o índice traz todos os planos (PLN-001 a PLN-007, A10), issues e decisões de todos os workstreams                                                                                             | P8     | `brza note index --rebuild` e a contagem (manual)     |
| `R6.2`         | Com um arquivo do núcleo editado no workspace, o `brza sync` não o escreve, mostra o diff e sai com 1; `--force <caminho>` o escreve e atualiza o lock                                             | P6     | unidade                                               |

### Fora de escopo

- **A norma dentro do próprio repositório de código, sem workspace separado.** Fica de fora pela R1.2; volta como plano
  novo se um projeto pedir.
- **Generalizar o `brza tree` e o `brza test` para outro repositório de código.** Já decidido no
  [PLN-003: O workflow do workspace roda igual no BrzA Studio e no Orca, por plugins e pelo `brza`](../PLN-003-o-workflow-nos-dois-clients/PLN-003-plan.md),
  R2.3, no workstream `tools-kit`; este plano não o refaz.
- **O coordenador que lê o índice da `master`.** Pela R5.4, vai a
  [O coordenador se baseia no índice de notas da master](../../work/issues/o-coordenador-le-o-indice-da-master.md); o
  PLN-006 entrega só o índice.

## Entrevista

As rodadas R1–R17 e a regra da recomendada estão em [PLN-006 — Entrevista](PLN-006-interview.md), por passarem de
400 linhas.

## Desenho

O Desenho, D1–D12, está em [PLN-006 — Desenho](PLN-006-design.md), por passar de 400 linhas.

## Passos

> Do P1 ao P7 só o `brza-workflow` muda, e o `brza-workspace` segue como hoje; o P8 é o único que o toca, em estágios
> (R6.4). Cada passo só executa a pedido explícito de Anderson.

### P1 — O `brza-workflow` nasce com o núcleo, o CLI e os testes verdes

Executa D1, D3 · executor: `implementer`; o `gh repo create brz-anderson/brza-workflow --public` pela sessão

Estimado: 1,5 h · Executado: 0,3 h

- [x] **1. Criar o repositório** e o layout do D1
- [x] **2. Copiar** o núcleo, o CLI e os testes pela fronteira do D3, sem os scripts locais nem o `resume_guard`
- [x] **3. Rodar** as três suítes lá — `scripts/brza/tests`, `.claude/hooks/tests`, `notes-checker` — e ver passar
- [x] **4. Commit e push** no `brza-workflow`

**Evidência:** `brza-workflow@83fce24`, a partir de `brza-workspace@d85c783` · `python3 -m unittest discover -s
tests/hooks` → 159 OK, 1 skip (P3) · `-s tests/cli` → 165 OK, 1 skip (P7) · `tests/notes-checker/run.py` → saída 0;
hooks e checador passam também no `/usr/bin/python3` 3.9.6. Desvios X1–X6.

### P2 — A raiz sai do cwd e do registro, no CLI e nos hooks

Executa D6, D7 · executor: `implementer`

Estimado: 4,5 h · Executado: 0,4 h

- [x] **1. Testes que falham**: o `brza where` de um worktree fora do diretório, sem entrada no registro, e o `brza
  register` recusando um código já ligado
- [x] **2. Implementar** o `brza_root`, o registro, o `brza where` e o `brza register`; os hooks e o `brza_runtime`
  passam a usá-lo, sem `tomllib`
- [x] **3. Rodar e ver passar**, também no `/usr/bin/python3` 3.9
- [x] **4. Commit**

**Evidência:** `brza-workflow@273c47d`, no merge `ca22efe` · na `master` depois do merge: `tests/cli` → 216 OK, 1 skip
(P7) · `tests/hooks` → 193 OK, 1 skip (P3), e no `/usr/bin/python3` 3.9.6 → 193 OK, 4 skips (3 sem `tomllib`, 1 do
P3) · `tests/notes-checker/run.py` → saída 0. O parser confere contra o `tomllib` em 14 documentos válidos, 17
inválidos e 8 fora do subconjunto. Desvios X8–X10; pontos R11.

### P3 — O manifesto, o lock, o motor e a norma em molde

Executa D2, D4, D5 · executor: `implementer`

Estimado: 3,5 h · Executado: 0,4 h

- [x] **1. Teste de ouro que falha**: o render do núcleo com o manifesto do `brza-workspace` sai igual à `master`
  daqui, menos a lista fechada do D12
- [x] **2. Implementar** o parser TOML, o render `{{tabela.chave}}`, o lock; pôr os placeholders nos `.md`, tirar o
  workspace de origem (R8.2), o `@AGENTS.md` e as `.claude/rules/`
- [x] **3. Rodar e ver passar**
- [x] **4. Commit**

**Evidência:** `brza-workflow@acf8bef`, o merge do P3 sobre o P7 · na `master`: `tests/hooks` → 244 OK, e no
`/usr/bin/python3` 3.9.6 → 244 OK, 5 skips (sem `tomllib`) · `tests/cli` → 264 OK · `tests/notes-checker/run.py` →
saída 0. O teste de ouro reproduz os 16 `.md` da `master` do `brza-workspace@d85c783`, salvo a lista fechada de 37
trocas em `tests/hooks/golden_differences.py`, que o P8 reusa; um `X` plantado em `core/work/README.md` o fez reprovar.
Um teste confere que, com outro manifesto, não sobra nada do `brza-workspace` no núcleo. Desvios X18–X20; pontos R14.

### P4 — O índice da `master`

Executa D11 · executor: `implementer`; o texto da norma e a nota de decisão pela sessão

Estimado: 5 h · Executado: 0,6 h

- [x] **1. Testes que falham**: o `plan-open` em corrida, a linha `changed` do `commit` sem tocar o checkout principal,
  o `merge=union` e o estado vigente pelo maior `ts`
- [x] **2. Implementar** o `brza note plan-open`, a linha do `commit`, o `brza note index --rebuild`, o
  `.gitattributes` e o campo `description` no checador e no molde
- [x] **3. Rodar e ver passar**
- [x] **4. A norma**: o texto do `AGENTS.md` e da `plan-runner` do D11, e a nota de decisão da R8.4, como proposta
- [x] **5. Commit**

**Evidência:** `brza-workflow@8b2a355`, no merge `ca22efe` · no worktree: `tests/cli` → 196 OK, 1 skip; os dois
`plan-open` em processos reais, 6 de 6 sem flake · na `master` depois do merge, as suítes do P2 · a norma em
`core/AGENTS.md`, `core/plans/README.md`, `core/work/README.md` e na `plan-runner` (`SKILL.md`, `open-and-plan.md`,
`close.md`, `plan-template.md`) · a proposta
[O índice de notas mora na `master`, a única exceção à regra da norma](../../work/decisions/o-indice-de-notas-mora-na-master.md),
`open`. Desvios X11–X13; pontos R12.

### P5 — O `brza init`

Executa D8 · executor: `implementer`

Estimado: 3 h · Executado: 0,4 h

- [x] **1. Teste de aceite que falha**: o init num diretório temporário, com o checador verde e sem caminho fixo
- [x] **2. Implementar**
- [x] **3. Rodar e ver passar**
- [x] **4. Commit**

**Evidência:** `brza-workflow@b9210a6` · `tests/cli` → 372 OK (51 do `test_brza_init.py`, 3 novos do shell) ·
`tests/hooks` → 244 OK · checador → saída 0 · o `test_brza_init.py` falhou sem o `bin/brza-init`, e o do shell, contra
o `brza.zsh` antigo · 8 mutações do `brza-init`, todas mortas · fumaça por processo, com `HOME`, `GIT_CONFIG_GLOBAL` e
registro temporários: `brza-init <dir> --name acme-notes --code <código> --title Acme --package client` → saída 0, um
commit local com o autor do manifesto, `check_notes.py --root <dir>` → 0 erros, 0 avisos, e o registro com o par. O X18
e o X20 foram consertados no mesmo commit. Desvios X24–X26; pontos R16.

### P6 — O `brza sync`, camada 1

Executa D9 · executor: `implementer`

Estimado: 3 h · Executado: 0,4 h

- [x] **1. Testes que falham**: a mudança do núcleo chega sem tocar a parte local; o arquivo editado é recusado com o
  diff, e o `--force` o escreve
- [x] **2. Implementar**
- [x] **3. Rodar e ver passar**
- [x] **4. Commit**

**Evidência:** `brza-workflow@9356995` · `tests/cli` → 318 OK (49 do `test_brza_sync.py`, 5 novos no
`test_brza_note.py`) · `tests/hooks` → 244 OK, e no 3.9.6 → 244 OK, 5 skips · checador → saída 0 · cinco mutações
plantadas (escrever o editado, lock quebrado como ausente, o dry-run aplicar, apagar o editado, pular o pull)
derrubaram cada uma ao menos um teste · fumaça com o `core/` real num diretório temporário: 28 arquivos escritos e o
lock com 28 sha256. Os testes vieram na mesma passada do código, sem o vermelho antes; a mutação o supre. Desvios
X21–X23; pontos R15.

### P7 — O `install`, o lançador, o `doctor` e os scripts locais

Executa D10 · executor: `implementer`

Estimado: 2 h · Executado: 0,3 h

- [x] **1. Testes que falham** do `--client`, do `--local` e do `--relink`, e do `doctor` com o registro
- [x] **2. Implementar**, com o `claude-brza`, o `brza-sessions` e o bloco do shell sem nome fixo
- [x] **3. Rodar e ver passar**
- [x] **4. Commit**

**Evidência:** `brza-workflow@d60b037` · `tests/cli` → 264 OK, sem skip (o do installer saiu, X4) · `tests/hooks` →
193 OK, 1 skip (P3) · `tests/notes-checker/run.py` → saída 0 · o `brza-install --all --client --relink` rodado com o
`HOME` trocado e o bloco do shell testado no zsh de verdade. O que o P8 precisa — o bloco do shell, a ordem dos
comandos, o cabeçalho dos scripts locais — está no próprio `brza-install` e no `packages/client/shell/brza.zsh`.
Desvios X14–X16; pontos R13. Só o vermelho do `doctor` foi visto antes do código; nos outros, os testes vieram antes,
mas a rodada vermelha não foi capturada.

### P8 — O `brza-workspace` vira cliente do `brza-workflow`

Executa D12, D10 · executor: a sessão do `workspace`

Estimado: 3 h · Executado: 1,2 h

- [x] **1. Estágio 1**: o manifesto, as rules e o índice, povoado pelo `index --rebuild`, entram; os scripts de hoje os
  ignoram
- [x] **2. Estágio 2**: o `brza sync --dry-run` mostra só a lista fechada do D12
- [x] **3. Estágio 3**: o `brza register`, o relink do `~/.local/bin` e o bloco do `~/.zshrc`, ao worklog em "Fora do
  workspace"; o sync real
- [x] **4. Conferir** a Regressão inteira

**Evidência**, na ordem do D12:
- **1:** `brza-workspace@2e6ea1d` (manifesto, com o `[checker]` do A2, a `.claude/rules/workspace.md`, o
  `.gitattributes` e o README com o `brand` e a chave de acesso); o índice `@1fd3be0`, 29 linhas — PLN-001 a PLN-007,
  17 issues e 5 decisões de `brand`, `studio`, `tools-kit` e `workspace` (A10).
- **2:** `brza-register` → `~/.config/brza/workspaces.toml`; o `brza-where` dá `notes` no worktree e `code` no
  `brza-studio`.
- **3:** `brza-sync --dry-run --core-only` → saída 0, 18 escritos e 2 apagados (o `resume_guard`), sem o `fact_audit.py`
  (A1) nem o `settings.json`; os `.py` conferidos à mão.
- **4:** o `index --rebuild` de novo → "em dia".
- **5:** `brza-install --all --client --relink` e `--chat-command --relink`; o `brza doctor` → `ok` em identidade,
  medição, links (16), registro e chat. O `--local` foi para depois do 6 (X27).
- **6:** `brza sync --core-only` → `brza-workspace@a45018c` (`brza-workflow@2286f31`); `@bbe723b` tira de
  `scripts/brza/` o que foi ao núcleo e os testes antigos, e troca o cabeçalho dos cinco scripts locais (A3) →
  `python3 -m unittest discover -s scripts/brza/tests` → 94 OK, e os cinco `--help` sobem; o `--local` → nada a trocar.
- **7:** `brza note sync` → `brand`, `studio`, `tools-kit` e `workspace` mesclados e enviados.
- **8:** o `~/.zshrc` passa a `source` do `packages/client/shell/brza.zsh` e a `brza_claude_fallback` ao workspace de origem;
  `zsh -n` ok, e a `claude` roteia: `--agents` no `brza-studio`, `--settings` no worktree, o workspace de origem fora.
- **9:** a trava do `/compact` com a memória suja → `decision: block` e a linha `guard` com `workstream: workspace`;
  os turnos novos gravam o `workstream`; a linha `changed` do índice sai deste commit do plano.

### P9 — A revisão adversária e o README do `brza-workflow`

Executa todos · executor: `reviewer`; o README pela sessão

Estimado: 1,5 h · Executado: 1,4 h

- [x] **1. A revisão**, com o parecer em `work/reviews/pln-006-o-brza-init.md`
- [x] **2. Cada achado com destino**

**Evidência:** duas revisões em vez de uma — a do `brza-workflow` antes da migração e a da migração depois dela (X29),
nos pareceres de `## Revisões`, com os 19 achados corrigidos e os 9 falsos derrubados · os consertos em
`brza-workflow@2286f31` e `@a313ec5` e em `brza-workspace@f12fdd4` · na `master` do `brza-workflow` em `a313ec5`:
`tests/cli` → 413 OK, `tests/hooks` → 287 OK, e no `/usr/bin/python3` 3.9.6 → 287 OK, 5 skips, o checador → saída 0 ·
o sync da norma nova no `brza-workspace` → `afc3859`, com o merge nos quatro workstreams; de um repositório alheio,
com a `BRZA_WORKSPACE`, o `brza sync` recusa e diz os dois caminhos · o README do `brza-workflow` em `@6d6ad2f`.

## Regressão

- **O `brza-workspace` segue funcionando a cada estágio do P8.** Como se confere: as três suítes de hoje, o `brza note
  commit` e o `brza note sync` num workstream, e uma linha `turn` com o `workstream` preenchido na medição.
- **O `compact_guard` segue barrando.** Como se confere: `.claude/hooks/tests/test_compact_guard.py` e um `/compact`
  manual com nota sem commit.
- **As sessões do `brza-studio` acham o workspace.** Como se confere: o `brza where` e o `measure.py` de um checkout do
  `brza-studio`, pelo registro.

## Desvios

- **X1 — `tests/` em subpastas** `cli/`, `hooks/` e `notes-checker/`, onde o D1 diz só `tests/`. Separa as três suítes e
  os caminhos relativos de cada uma; afeta P1.
- **X2 — O `brza-note` do núcleo chama o `brza-sessions` do pacote do cliente** para o nome da sessão. A R10.1 decidiu
  que ele devolve `None` sem o pacote; afeta P6.
- **X3 — O pacote do cliente acha o `brza_runtime` pelo `sys.path` do checkout.** A R10.2 confirmou que é o desenho da
  R3.2; o P7 só garante o link.
- **X4 — Dois testes em skip**: o `SettingsTest` do `fact_audit`, até o P3 criar o `core/.claude/settings.hooks.json`
  (R10.3), e o do installer, até o P7.
- **X5 — Um `.gitignore` na raiz do `brza-workflow`**, que o D1 não lista (R10.4).
- **X6 — O CLI segue exigindo Python 3.10 ou mais** (`str | None`), como na origem; só os hooks e o `brza_root`
  rodam no 3.9. Vai ao README no P9.
- **X7 — As levas mudam: P2 e P4; depois P3 e P7; depois P5 e P6.** A R9 previa P2, P3 e P4 juntos, mas o parser
  TOML mora no `brza_root.py` (D2) e serve ao registro do P2 e ao manifesto do P3; o P3 espera o P2. Escolha da sessão,
  pela regra da recomendada.
- **X8 — O P2 não tocou o `bin/brza-note`.** Ele já compara o common dir com `runtime.WORKSPACE` e `runtime.STUDIO`,
  que agora vêm do `brza_root`; os `origin/master` literais dele ficam para o P6 (D9). Afeta P6.
- **X9 — O `brza_root` difere do D6 em três detalhes:** `registry_path()` é função, e não constante, para ler o
  ambiente na hora; o `find` ganhou `branch=False`, porque só o `measure` paga a chamada ao git; o parser aceita
  inteiro e booleano, porque o `schema = 1` do manifesto pede inteiro.
- **X10 — O `brza_runtime.discover()` cai no legado** (`BRZA_WORKSPACE` sem manifesto, ou `~/Projects/brza-workspace`)
  quando não acha workspace, para os scripts de hoje não quebrarem antes do P8; o nome fixo sai no P7 ou no P8.
- **X11 — O `commit` compara com a linha vigente do índice, e não com o commit anterior** como o D11 dizia: o
  `plan-open` já grava `created`, e o índice se conserta no commit seguinte quando um push falha.
- **X12 — O `brza note commit` aceita o caminho antigo de um rename**, com `git rm --cached` para o que sumiu do disco;
  antes o `git add` falhava, e o `changed` com o `path` novo da R8.1 não sairia.
- **X13 — O `plan-open` não cria o arquivo do plano**: reserva o número, grava a linha e imprime o caminho; quem grava é
  a `plan-runner`. O `--no-push` não grava linha, e o `--rebuild` recolhe depois.
- **X14 — O `--local <dir>` aceita a raiz do workspace ou a pasta dos scripts**, e o `--all` liga só o `bin/`; o
  pacote do cliente vai pelo `--client`. O `claude-brza` segue só pelo `--chat-command`.
- **X15 — O bloco do shell divide `<raiz> <papel>` pela última palavra** (`${w% *}`, `${w##* }`), e não pelo `${=w}`
  do D10, que quebrava raiz com espaço no nome.
- **X16 — O `claude-brza` e o `brza where` não têm legado**: sem manifesto e sem registro, a sessão sobe sem hooks. No
  P8, o manifesto e o `brza register` vêm antes de qualquer relink.
- **X17 — O P6 vem antes do P5**, e não junto: o passo 6 do D8 roda a camada 1 do sync no diretório novo. Escolha da
  sessão, pela regra da recomendada.
- **X18 — O bloco do shell tem duas cópias e uma chamada ao workspace de origem**: o `packages/client/shell/brza.zsh` do P7 cai na
  função `claude` do workspace de origem, contra a R8.2, e o `templates/README.md` do P3 traz outra cópia do bloco. O P5, dono do molde do
  README, os reconcilia.
- **X19 — O `render` ganhou o parâmetro `escape`**, e o `render_settings` escapa o valor para JSON; o
  `templates/.brza/workspace.toml` é a saída exata do `dump_manifest`, para o P5 ter uma fonte só.
- **X20 — Ficaram no núcleo**, só com placeholders, o exemplo de agente com o prefixo do workspace de origem no docstring do `measure.py:135` e o
  parágrafo do `CLAUDE.md` sobre o `--agents` do `claude-brza`, que é do cliente. O primeiro sai no P5, com o X18.
- **X21 — O `brza sync` sem `--core-only` roda também a camada 2**, o `brza-note sync`, por subprocesso; o
  `--dry-run` e o `--core-only` não a rodam. O D9 não dizia o que o `--core-only` excluía.
- **X22 — O commit do `brza-workflow` é o da `origin/<ref>`**, depois do `fetch`, com o `<ref>` local só sem `origin`:
  o commit local não empurrado não entra no workspace. O `--ref` não grava no manifesto.
- **X23 — O `resume_guard.py` e o teste dele saem no primeiro sync**, mesmo fora do lock, por uma lista `RETIRED`; os
  `.claude/hooks/tests/*` e o `notes-checker/tests/run.py` do `brza-workspace` saem por `git rm` no P8 (R15.3).
- **X24 — O `brza init` registra por último**: confere (8), commita (9) e só então grava o registro (7), para a falha da
  conferência não deixar entrada no único arquivo fora do diretório. A conferência varre os cinco termos —
  `brza-workspace`, `brza-studio`, `Anderson`, `brz-anderson` e o nome do workspace de origem —, salvo o que o manifesto traz.
- **X25 — O `brza init` ganhou `--code-github`**, e grava o checkout principal quando o `--code` é um worktree; com o
  `brza-workflow` em detached, o `core.ref` cai no `master`.
- **X27 — O `--local` vem depois do estágio 6, e não no 5**: antes de o 6 tirar de `scripts/brza/` o que foi ao
  núcleo, ele religaria o `brza-note` e o `brza-install` de lá, desfazendo o `--all`. Pela regra da recomendada.
- **X28 — Entraram na `master` do `brza-workspace`, no estágio 1, o README e a `.claude/rules/workspace.md` com o que o
  sync tira do `AGENTS.md` e do `CLAUDE.md`** (a lista dos workstreams, com o `brand`; a chave `personal` e o `gh`; o
  `skill-creator` do `workspace`), para nada sumir; o D12 só citava o manifesto, as rules, o `.gitattributes` e o
  índice.
- **X29 — O P9 teve duas revisões, e não uma**: a do `brza-workflow` antes da migração, que achou o A1 do PLN-005 que
  o sync desfaria, e a da migração depois dela. Escolha da sessão, pela regra da recomendada; a primeira poupou o P8 de
  desfazer trabalho alheio.
- **X26 — Sobrou um nome pessoal no CLI do núcleo**: o molde de issue do `bin/brza-note:117` diz "O pedido de Anderson".
  O `bin/` não é renderizado; vai à revisão do P9.

## Revisões

- [REV-003: o `brza-workflow` dos passos P1–P7 do PLN-006, em `b9210a6`](../../work/reviews/REV-003-pln-006-o-brza-init.md) —
  2026-11-02, 11 achados e 5 falsos; A1 corrigido no porte (`ebeb779`), A2, A3 e A10 no P8, os outros num conserto
  antes dele, todos pela regra da recomendada.
- [REV-004: a migração do `brza-workspace` para cliente do `brza-workflow`, o P8 do PLN-006](../../work/reviews/REV-004-pln-006-a-migracao.md)
  — 2026-11-02, 8 achados e 4 falsos, e o incidente do `fa4152f`, desfeito por Anderson; A2, A6 e A7 corrigidos no
  `brza-workspace`, e A1, A3, A4, A5 e A8 no `brza-workflow`, pela regra da recomendada.

## Decisões

- [O índice de notas mora na `master`, a única exceção à regra da norma](../../work/decisions/o-indice-de-notas-mora-na-master.md)
  — R8.4, `done` na R17.1.

## Worklogs

- 2026-10-31 — aberto; R1–R8 respondidas, a R2.1 em texto livre e confirmada na R3.1, a R4.3 em texto livre e
  fechada na R5; D1–D12 gravados no `-design`, P1–P9 escritos (27 h); aceito na R9; P1–P7 feitos, com a R10 e, pela
  regra da recomendada, as R11–R16. Parou na R17, antes do P8.
  [PLN-006: a abertura do brza init](../../work/worklogs/2026-10-31-pln-006-a-abertura-do-brza-init.md)
- 2026-11-02 — R17 respondida; a proposta do índice decidida; o P8 começa pelo porte do PLN-005, com a revisão do
  `brza-workflow` (P9) em paralelo.
  [PLN-006: a migração do brza-workspace](../../work/worklogs/2026-11-02-pln-006-a-migracao-do-brza-workspace.md)
- 2026-11-02 — P8 e P9 feitos: a migração em nove estágios, as duas revisões e os consertos; o incidente do `fa4152f`,
  desfeito por Anderson. Fechado.
  [PLN-006: a migração do brza-workspace](../../work/worklogs/2026-11-02-pln-006-a-migracao-do-brza-workspace.md)

## Pendências conhecidas

- [As sobras do PLN-006 no brza-workflow e no plano](../../work/issues/as-sobras-do-pln-006.md) — seis pendências
  deixadas para depois pelas rodadas, nenhuma travando o uso de hoje.
- [O coordenador se baseia no índice de notas da master](../../work/issues/o-coordenador-le-o-indice-da-master.md) —
  de R5.4; o índice que ele lê já existe.

## Documentação

- `brz-anderson/brza-workflow`: o repositório novo, com o núcleo, o CLI, os moldes, o pacote do cliente, os testes e o
  README (`@6d6ad2f`), criado em P1.
- A norma do `brza-workspace`, na `master`: o `AGENTS.md`, o `CLAUDE.md`, o `work/README.md`, o `plans/README.md` e a
  `plan-runner`, que agora chegam pelo `brza sync` (`a45018c`, `afc3859`); o README local e a
  `.claude/rules/workspace.md` (`2e6ea1d`, `f12fdd4`), em P8 e P9.

## Fechamento

- [x] Todo passo `[x]` com evidência, ou `[-]` com motivo.
- [x] Todo achado com destino que existe: os 19 corrigidos, e os 9 falsos com o porquê, nos dois pareceres.
- [x] Trabalho só em notas, no `brza-workspace` e no `brza-workflow`, sem pull request do `brza-studio`: não há
      resumo de PR.
- [x] O durável saiu para a casa dona e está em `## Decisões` e `## Documentação`: a decisão do índice em
      `work/decisions/`, a norma comum no `brza-workflow`, a local no `brza-workspace`.
- [x] As decisões que o plano respondeu estão `done`, citando a rodada.
- [x] `status: done`, `phase: closed` e `completed` no frontmatter.

A Janela não houve. O plano estimou 27 h e executou 5,4 h, numa execução quase toda delegada a subagentes, com 31
escolhas e mais 4 do fechamento decididas pela regra da recomendada.
