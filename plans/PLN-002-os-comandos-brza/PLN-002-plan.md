---
status: in_progress
phase: execution
origin: issue
origin_ref: os-comandos-brza-que-viram-o-pln-002
ready: sim — o P2; o P7 espera a sessão da 2d, reaberta por Anderson
estimate_h: 18
executed_h: 0.2
remaining_h: 16.5
scope:
  - workspace
  - brza-studio
opened: 2026-10-28
owner: Anderson
tags:
  - tooling
---

# PLN-002: Os passos manuais que se repetem entre sessões viram comandos `brza`

- **Retomar:** o P0 e o P1 estão feitos; o runtime comum está em `brza-workspace@9e95a2c`. O próximo é o P2, o
  `brza tree`, numa sessão `pln-002-p2` que Anderson abre a pedido. Depois dele, o P3 ao P6 podem correr em paralelo
  (R4.4), e o P7 espera a 2d.
- **Dividido:** [PLN-002 — Entrevista](PLN-002-interview.md) · [PLN-002 — Desenho](PLN-002-design.md)

## Pedido

- **Origem:** [Os comandos `brza` que viram o PLN-002](../../work/issues/os-comandos-brza-que-viram-o-pln-002.md), com
  o levantamento e as rodadas em
  [Os comandos brza que faltam, levantados nas notas e nos scripts](../../work/worklogs/2026-10-28-os-comandos-brza-que-faltam.md).

"Acione a plan-runner e escreva o PLN-002 a partir de work/issues/os-comandos-brza-que-viram-o-pln-002.md: um passo por
comando, com as rodadas dos pontos de desenho listados na issue." — Anderson, na sessão `pln-002-comandos-brza`, em
2026-10-28.

Os itens da issue, numerados para a Cobertura:

0. o despacho `brza X` → `brza-X`, passo 0 ("Sim, passo 0 do PLN-002 (Recomendado)");
1. `brza tree <nome>` / `--rm`;
2. `brza dev` / `--stop`;
3. `brza test`;
4. `brza doctor`;
5. `brza sessions list|send|close`;
6. `brza note new|commit`;
7. `brza app install`.

### Cobertura

| Origem     | Critério de aceite                                                                                           | Passo | Teste (nível)                                         |
| :--------- | :----------------------------------------------------------------------------------------------------------- | :---- | :---------------------------------------------------- |
| `Pedido 0` | `brza <sub>` desconhecido executa o `brza-<sub>` do PATH                                                     | P0    | teste do `brza-studio` (unidade); C2 (manual)         |
| R3.4, R6.1 | o runtime tem o envio ao chat, o `STUDIO` e o worktree, e os 21 testes de hoje passam                        | P1    | `test_brza_runtime.py` (unidade)                      |
| R4.1       | `brza install --all` liga todo `brza-*`, inclusive ele mesmo                                                 | P1    | `InstallTest` (unidade)                               |
| `Pedido 1` | `brza tree x` cria `.worktrees/x` em `feat/x` da `origin/master`, com `node_modules` real                    | P2    | `test_brza_tree.py`, com repositório temporário       |
| R1.4       | `--rm` recusa o worktree sujo, o não mergeado e a branch sem commit sem `--force`                            | P2    | `test_brza_tree.py` (unidade)                         |
| `Pedido 2` | `brza dev` sobe o build visível do worktree e semeia o perfil vazio; `--stop` encerra só o runner vivo       | P3    | `test_brza_dev.py` (unidade); C1 (manual)             |
| `Pedido 3` | `brza test` separa a falha nova da que já falhava na master e sempre passa `--base=origin/master`            | P4    | `test_brza_test.py` (unidade); uma corrida real       |
| `Pedido 7` | `brza app install` constrói da `origin/master`, pergunta, recusa com o app aberto sem `--yes` e instala      | P5    | `test_brza_app.py` (unidade); C2 (manual)             |
| `Pedido 6` | `brza note new` cria o esqueleto do gênero; `note commit` barra o erro do checador e commita por caminho     | P6    | `test_brza_note.py` (unidade)                         |
| `Pedido 5` | `brza sessions list`, `send` e `close` acham o chat pelo nome; o `close` não usa `--resume`                  | P7    | `test_brza_sessions.py` (unidade); C3 (manual)        |
| `Pedido 4` | `brza doctor` sai com 1 quando falta identidade, medição, link ou override, e diz o comando que conserta     | P8    | `test_brza_doctor.py` (unidade); C4 (manual)          |

### Fora de escopo

- **O `ship`, o `fanout` e o status da Run.** Ficaram fora nas rodadas da `brza-comandos-lacunas`, como diz a
  [issue de origem](../../work/issues/os-comandos-brza-que-viram-o-pln-002.md).
- **Os scripts da Fixfy.** Já têm gatilho em
  [Os scripts de orquestração da Fixfy que ficaram fora do port para o BrzA](../../work/issues/scripts-da-fixfy-fora-do-port-para-o-brza.md).
- **Dois dev builds no mesmo worktree.** R2.2.
- **Apagar os dois órfãos de hoje.** O `conferencia-p52-p53` pode servir às conferências pendentes do PLN-001; o
  `brza tree --list` os mostra, e quem remove é Anderson.

## Restrições

- **O contrato do runtime só cresce.** Nenhum nome de hoje do `brza_runtime.py` muda, e os testes de
  `scripts/brza/tests` seguem passando (o aviso da `brza-workspace-80`, na issue).
- **O checkout principal do `brza-studio` não é tocado.** O que precisa de código parte de worktree da `origin/master`
  (R1.2, R2.4, R3.3).
- **O `close` não reabre.** Nada de `--resume` nem "restart" (`AGENTS.md`, "Uma tarefa, uma sessão, um worklog").

## Pré-requisitos

- **P0 na `origin/master`:** `git -C ~/Projects/brza-studio merge-base --is-ancestor 9a81e65c852 origin/master` sai 0.
  Sem isso, os scripts rodam pelo nome `brza-<sub>`, e o P5 espera.
- **O P1 antes do P2 ao P8:** todos importam do runtime novo (R4.4).
- **A 2d reaberta, para o P7:** Anderson abre a sessão da combinação (R5.2). Sem ela, o P7 espera, e os outros seguem.

## Passos

> Cada passo roda numa sessão `pln-002-pN` do `brza-workspace`, aberta por Anderson (R5.3), com commit direto na
> `master` e `git add` por caminho. O teste de cada script carrega o script com `runpy.run_path`, como os de hoje, e o
> que toca o git usa um repositório temporário com uma `origin` local. Comando dos testes, da raiz:
> `python3 -m unittest discover -s scripts/brza/tests`.

### P0 — O despacho `brza X` → `brza-X`

Executa a [issue do despacho](../../work/issues/cli-brza-manda-subcomando-desconhecido-ao-brza-x-do-path.md) · executor:
`brza-cli-subcomandos`, fora desta sessão

- [x] **1. O desvio no CLI**, com teste e a conferência de ponta a ponta com o `out/cli/index.js` novo no Electron do app
  instalado.
- [ ] **2. A reinstalação**, que vai ao P5, por resposta de Anderson: "No brza app install (Recomendado)".

**Evidência:** `brza-studio@9a81e65c852`, com push na `master`; o worklog está em `## Worklogs`. As horas estão lá, fora
da estimativa deste plano.

### P1 — A base comum: o runtime e o `brza install --all`

Executa D1 · executor: sessão `pln-002-p1`

Estimado: 1,5 h · Executado: 0,2 h

- [x] **1. Testes que falham:** `test_brza_runtime.py` com `canonicalize`, `send_mutation`, `worktree_add` (detached e
  com branch, num repositório temporário) e `install_offline` (com o `pnpm` trocado por um falso, que sai 1 e depois 0);
  o `InstallTest` com o `--all` ligando um `brza-*` novo e o próprio `brza-install`.
- [x] **2. Implementar:** mover o `canonicalize`, o `send_mutation` e o `send_to_chat` para o runtime; o `brza-run` e o
  `brza-sessions` importam e reexportam; os patches dos testes passam a `brza_runtime.rpc`. Somar `STUDIO`, `git`,
  `worktree_add`, `install_offline` e `worktree_remove`. O `--all` no `brza-install`, e a ajuda nova. Ver X1.
- [x] **3. Rodar e ver passar:** `python3 -m unittest discover -s scripts/brza/tests`.
- [x] **4. Ligar:** `scripts/brza/brza-install --all`, e `brza install` mostra todo link `ok`.
- [x] **5. Commit** — `feat(brza): o runtime comum e o brza install --all (PLN-002/P1)`.

**Evidência:** `brza-workspace@9e95a2c`, com push na `master`.
- `python3 -m unittest discover -s scripts/brza/tests` → `Ran 33 tests … OK`. Eram 21, que seguem entre eles; o
  `test_brza_runtime.py` traz 10 casos novos, e o `InstallTest` traz 2.
- `scripts/brza/brza-install --all` ligou o `brza-install`. Pelo link, o `brza-install` mostra `claude-brza`,
  `brza-install`, `brza-run` e `brza-sessions` como `ok`. O `brza install` ainda dá `Unknown command: install` no app
  instalado, porque o despacho chega com o P5; por isso a ajuda segue com os nomes `brza-install`/`brza-run` até o P5.5.

### P2 — O `brza tree`

Executa D2 · executor: sessão `pln-002-p2`

Estimado: 2,5 h · Executado: — h

- [ ] **1. Testes que falham:** criar com o tipo padrão e com `--type` e `--base`; o install offline que falha mantém o
  worktree e imprime o comando; `--rm` recusa o sujo, o não mergeado e a branch sem commit próprio sem `--force`, e
  remove o mergeado limpo; `--rm` no órfão; `--list` marca os órfãos; `--chat` chama o `brza-sessions --checkout`.
- [ ] **2. Implementar** `scripts/brza/brza-tree` sobre o `worktree_add` e o `install_offline`.
- [ ] **3. Rodar e ver passar**, e uma corrida real: `brza tree pln-002-p2-prova`, conferir que o `node_modules` não é
  link, e `brza tree --rm pln-002-p2-prova --force`.
- [ ] **4. Ligar e commit** — `brza install --all`; `feat(brza): brza tree (PLN-002/P2)`.

**Evidência:** —

### P3 — O `brza dev`

Executa D3 · executor: sessão `pln-002-p3`

Estimado: 2 h · Executado: — h

- [ ] **1. Testes que falham:** o seed só no perfil vazio, e o `--no-seed` e o `--reset`; o `--background` põe o
  `ORCA_BACKGROUND_LAUNCH=1`; recusa com build vivo; o `--stop` com pid vivo de runner, morto, e vivo de outro processo
  (o `ps` trocado por um falso).
- [ ] **2. Implementar** `scripts/brza/brza-dev`.
- [ ] **3. Rodar e ver passar**, e o C1 com Anderson.
- [ ] **4. Ligar e commit** — `feat(brza): brza dev (PLN-002/P3)`.

**Evidência:** —

### P4 — O `brza test`

Executa D4 · executor: sessão `pln-002-p4`

Estimado: 2,5 h · Executado: — h

- [ ] **1. Testes que falham:** a lista dos testes alterados e dos vizinhos; o `--base=origin/master` sempre presente;
  os três grupos do relatório, com o vitest e o `check:changed` trocados por falsos; o worktree temporário sai mesmo
  quando o baseline falha.
- [ ] **2. Implementar** `scripts/brza/brza-test`.
- [ ] **3. Rodar e ver passar**, e uma corrida real num worktree do `tree`, com o tempo do `check:changed` medido e
  anotado no passo.
- [ ] **4. Ligar e commit** — `feat(brza): brza test (PLN-002/P4)`.

**Evidência:** —

### P5 — O `brza app install`, a reinstalação do P0 e a troca dos textos

Executa D5 · executor: sessão `pln-002-p5`; a instalação, com Anderson

Estimado: 2,5 h · Executado: — h

- [ ] **1. Testes que falham:** a pergunta antes do `ditto`; a recusa com o app aberto sem `--yes` (saída 2); o build no
  worktree temporário, ou no `--from`; o `--clean`; o worktree temporário sai mesmo com o build falhando.
- [ ] **2. Implementar** `scripts/brza/brza-app`, com o subcomando `install`.
- [ ] **3. Rodar e ver passar.**
- [ ] **4. Primeiro uso, com Anderson:** o C2. O `brza app install` roda de um terminal fora do app, com o app fechado.
- [ ] **5. A troca dos textos:** `brza-install`/`brza-run` por `brza install`/`brza run` na ajuda dos scripts e no
  `CLAUDE.md:33`.
- [ ] **6. Commit** — `feat(brza): brza app install (PLN-002/P5)`.

**Evidência:** —

### P6 — O `brza note`

Executa D6 · executor: sessão `pln-002-p6`

Estimado: 2 h · Executado: — h

- [ ] **1. Testes que falham:** o esqueleto de worklog e de issue, num `work/` temporário, e a recusa do que existe; o
  `commit` que para no erro do checador, o `git add` só dos caminhos dados (com outro arquivo sujo ao lado) e o
  `pull --rebase`, o push e o `--no-push`.
- [ ] **2. Implementar** `scripts/brza/brza-note`.
- [ ] **3. Rodar e ver passar**, e o primeiro uso real: o worklog da própria sessão sai do `brza note new`.
- [ ] **4. Ligar e commit** — pelo próprio `brza note commit`.

**Evidência:** —

### P7 — O `brza sessions list|send|close`

Executa D7 · executor: a sessão da 2d, reaberta por Anderson (R5.2)

Estimado: 3 h · Executado: — h

- [ ] **1. A combinação:** a 2d confere os dois pontos em aberto do D7 — o título da aba e o `reason: 'user'` vindo de
  script — e ajusta o D7. Uma divergência da proposta volta à Entrevista antes do código.
- [ ] **2. Testes que falham:** `list` sobre um `session.tabs.listAll` falso; `send` pelo nome; `close` pelo nome, sem
  `--resume`; nome ausente e nome repetido.
- [ ] **3. Implementar** no `scripts/brza/brza-sessions`, mantendo o `open` de hoje.
- [ ] **4. Rodar e ver passar**, e o C3 com Anderson.
- [ ] **5. Commit** — `feat(brza): brza sessions list, send e close (PLN-002/P7)`.

**Evidência:** —

### P8 — O `brza doctor`

Executa D8 · executor: sessão `pln-002-p8`

Estimado: 2 h · Executado: — h

- [ ] **1. Testes que falham:** cada erro e cada aviso do D8, inclusive o do app velho, com o ambiente e o `rpc`
  trocados; a saída 1 com erro e 0 sem.
- [ ] **2. Implementar** `scripts/brza/brza-doctor`, com o `link_state` do `brza-install`.
- [ ] **3. Rodar e ver passar**, e o C4 com Anderson.
- [ ] **4. Ligar e commit** — `feat(brza): brza doctor (PLN-002/P8)`.

**Evidência:** —

## Regressão

- **O `brza-run`, o `brza-sessions open` e o `brza-install --chat-command` seguem iguais.** Como se confere:
  `python3 -m unittest discover -s scripts/brza/tests`, com os 21 testes de hoje entre os que passam, a cada passo.
- **Os links de hoje em `~/.local/bin` seguem `ok`.** Como se confere: `brza install`, depois do P1 e de cada passo.

## Desvios

- **X1 — O `git` do runtime recebe `cwd: Path | None = None`, e não `cwd: Path = STUDIO`.** O padrão ligado na
  definição ignora o `STUDIO` trocado no teste e o `BRZA_STUDIO` lido depois; o contrato não muda. Afeta o P1 e o D1.

## Casos manuais

| ID  | Critério                                         | Passos                                                                                       | Esperado                                                        | Observado | Veredito |
| :-- | :----------------------------------------------- | :------------------------------------------------------------------------------------------- | :-------------------------------------------------------------- | :-------- | :------- |
| C1  | `Pedido 2`: o dev build sobe e para pelo `brza`  | `brza tree c1-prova`; `brza dev` nele; usar; `brza dev --stop`                               | janela visível com o chat ligado; o `--stop` fecha e libera     |           |          |
| C2  | `Pedido 7` e `Pedido 0`: o app reinstalado       | app fechado; num terminal, `brza-app install`; abrir o app; `brza sessions --help` no chat e no terminal | o app abre na versão nova; a ajuda do `brza-sessions` responde nos dois | |          |
| C3  | `Pedido 5`: o `close` fecha o chat por nome      | `brza sessions open c3-prova`; `brza sessions list`; `brza sessions close c3-prova`          | o chat some da lista e da tela, sem aba órfã                    |           |          |
| C4  | `Pedido 4`: o `doctor` no chat e no terminal     | `brza doctor` num chat do app e num terminal sem a função `claude`                           | 0 no chat; no terminal, os erros com o comando que conserta     |           |          |

## Worklogs

- 2026-10-28 — P1, o runtime comum e o `brza-install --all`, em `brza-workspace@9e95a2c`; X1 no `git`. Nada travou.
  [O PLN-002/P1: o runtime comum e o brza-install --all](../../work/worklogs/2026-10-28-pln-002-p1-o-runtime-comum-e-o-install-all.md)
- 2026-10-28 — P0, o despacho, feito pela `brza-cli-subcomandos` em `brza-studio@9a81e65c852`. A reinstalação e a troca
  dos textos ficam para o `brza app install`.
  [O CLI brza despacha o subcomando desconhecido ao brza-X do PATH](../../work/worklogs/2026-10-28-o-cli-brza-despacha-ao-brza-x-do-path.md)
- 2026-10-28 — aberto; o Terreno foi levantado, a R1 a R7 fecharam, o D1 a D8 e o P1 a P8 foram escritos, e o plano foi
  aceito na R7.4.
  [O PLN-002 escrito: os comandos brza, com as rodadas de desenho](../../work/worklogs/2026-10-28-pln-002-comandos-brza.md)

## Pendências conhecidas

- [O check de import boundaries está vermelho na master pelo `external-subcommand.ts` do `brza X`](../../work/issues/import-boundaries-vermelho-pelo-external-subcommand.md)
  — do P0, aberta pela sessão do PLN-001; o `spawn` direto de `node:child_process` vai ao `@orca/process-host`.

## Fechamento

- [ ] Todo passo `[x]` com evidência, ou `[-]` com motivo.
- [ ] Todo achado com destino que existe.
- [ ] O durável saiu para a casa dona e está em `## Documentação`: a ajuda dos scripts e o `CLAUDE.md`.
- [ ] `status: done`, `phase: closed` e `completed` no frontmatter.
