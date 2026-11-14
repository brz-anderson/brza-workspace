---
status: open
phase: design
origin: request
description: A norma e o brza note passam a aceitar builder/<nome> como workstream pessoal de um Builder, com autor próprio do agente.
ready: sim
estimate_h: 18.5
executed_h: 0
remaining_h: 18.5
priority: high
scope:
  - workspace
  - brza-workflow
opened: 2026-11-14
owner: Anderson
tags:
  - planning
  - tooling
---

# PLN-024: Norma aceita o prefixo builder/ (workstream pessoal de Builder)

- **Retomar:** plano aberto em 2026-11-14, nenhum passo executado. R1.1 a R1.6 estão fechadas. O próximo ato é o P1, quando Anderson pedir.

## Pedido

- **Origem:** pedido de Anderson, em 2026-11-14: "antes do plano do Cursor, planejar a mudança na NORMA para aceitar o prefixo `builder/` (ex.: `builder/bob-the-builder`, o workstream pessoal de um Builder/agente)." Na mesma conversa ele fechou o desenho: "criação por um SUBCOMANDO NOVO `brza note builder <nome>` (não a flag `--builder`); reaproveitar a lógica de worktree/memória/sync do `workstream` internamente para não duplicar"; "nome curto único entre `workstream/` e `builder/`, worktree `.worktrees/<nome>`, índice com `kind`"; "commits numa branch `builder/<nome>` usam o AUTOR PRÓPRIO do agente. Para o Bob: `Bob The Builder <bob@brza.dev>`"; "a criação de `builder/bob-the-builder` e o plano do Cursor (`--agent cursor`) ficam fora deste PLN, como sequência."

### Cobertura

| Origem | Critério de aceite | Passo | Teste (nível) |
| :----- | :----------------- | :---- | :------------ |
| Subcomando `brza note builder <nome>` | `brza note workstream <nome>` continua criando `workstream/<nome>`; o subcomando novo cria `builder/<nome>` reusando worktree, memória e sync | P2 | `tests/cli/test_brza_note.py` (unidade) |
| Nome curto único, worktree `.worktrees/<nome>`, `kind` no índice | A segunda frente com o mesmo nome é recusada; a linha do índice traz `kind` `builder` ou `workstream` e `worktree` `.worktrees/<nome>` | P2 | `tests/cli/test_brza_note.py` e `tests/cli/test_brza_note_index.py` (unidade) |
| Autor próprio em `builder/`, brz-anderson em `workstream/` | `brza note commit` numa branch `builder/` grava o autor configurado e recusa outro; commit em `workstream/*` não passa por essa conferência | P5 | `tests/cli/test_brza_note.py` (unidade) |
| Exceção só em `builder/` no texto da norma | O `AGENTS.md` renderizado diz que `workstream/*` segue com brz-anderson e `builder/` usa o autor do agente | P6 | `tests/hooks/test_golden_render.py` (unidade) |
| Bob e o Cursor ficam para depois | Este plano não cria a frente `builder/bob-the-builder` nem altera `brza sessions` | P1–P8 | leitura do diff do PR (manual) |

### Fora de escopo

- **A frente `builder/bob-the-builder` como workstream de notas.** A branch local com esse nome pode existir vazia, no mesmo commit da `master`, sem upstream e sem push. Criá-la pelo `brza note builder` e passar a gravar nota nela é a sequência deste plano, outro PLN.
- **O Cursor como `--agent` de `brza sessions`.** Também é sequência, depois que este plano estiver na norma. O flag hoje é `--agent`, não `--client`.

## Restrições

- **Passo deste plano só executa com pedido explícito de Anderson, um por vez.** Abrir o plano não executa P1–P8.
- **O código do `brza-workflow` entra por branch e PR.** A `master` do `brza-workspace` recebe a norma pelo `brza sync`, que o [`AGENTS.md`](../../AGENTS.md) linhas 67–78 e o `commit_and_push` de `bin/brza-sync` já autorizam. O índice da `master` continua só pelo `brza note`.
- **Commit em `workstream/*` segue com a identidade do brz-anderson.** A exceção de autor próprio vale só em `builder/`.

## Entrevista

### Rodada 1 — o prefixo builder/ (enviada 2026-11-14)

**Apresentado antes:** o `brza note` recusa qualquer branch que não comece com `workstream/`. A constante está em `bin/brza_runtime.py` linha 192, com cópias em `core/.claude/hooks/measure.py` linha 105 e `packages/mcp/brza_mcp/telemetry.py` linha 26. Não há skill `meeting-runner` nem comando de radar. O resumo diário é o `scripts/summarize_measurements.py --by-workstream`, que imprime a string que o hook gravou.

Respondida em 2026-11-14, na mensagem que autorizou abrir este plano.

1. **Como a frente nasce.** Opções apresentadas:
   - `brza note workstream --builder <nome>` (recomendada na investigação) — custo: um flag e a recusa de nome repetido, sem segundo comando; se paga: no primeiro Builder aberto;
   - subcomando novo, com o risco de duplicar worktree, memória e sync — custo: outro verbo, cobrado na implementação; se paga: se o verbo deixar claro que é outro tipo de frente.

   **Decidido — subcomando novo `brza note builder <nome>`**, reaproveitando por dentro a lógica de worktree, memória e sync do `workstream`, sem duplicar essa lógica. A flag `--builder` não entra.

2. **Nome, worktree e índice.** Opções apresentadas:
   - nome curto único entre os dois prefixos, worktree `.worktrees/<nome>`, campo `kind` no índice (recomendada) — custo: não existem `workstream/bob` e `builder/bob` ao mesmo tempo; se paga: na hora, porque o diretório do worktree é um só;
   - o mesmo nome nos dois prefixos — custo: dois donos de `.worktrees/<nome>` e do campo `workstream` do índice; se paga: nunca, com o layout pedido.

   **Decidido — a recomendada.**

3. **Quem assina o commit.** Opções apresentadas:
   - autor continua `brz-anderson` também em `builder/`, e o agente aparece só no campo `session` do índice (recomendada na investigação) — custo: o git não mostra o agente como autor; se paga: enquanto a regra das linhas 73–78 do `AGENTS.md` valer para toda branch;
   - autor próprio do agente na branch `builder/<nome>`.

   **Decidido — autor próprio do agente.** Para o Bob, `Bob The Builder <bob@brza.dev>`. Commit em `workstream/*` continua com brz-anderson. O texto do `AGENTS.md` abre essa exceção só em `builder/`.

4. **O que este plano não faz.** **Decidido —** a criação de `builder/bob-the-builder` pelo ferramental e o plano do Cursor (`--agent cursor`) ficam fora, como sequência.

5. **Onde a identidade de cada builder fica.** Opções que estavam em aberto:
   - arquivo versionado na norma, um só `builders.toml` na `master` — custo: uma linha por Builder, cobrada no registro; se paga: no primeiro `brza note commit` de um clone sem o worktree;
   - config só do worktree, fora do git — custo: cada máquina configura de novo; se paga: se a identidade fosse segredo de máquina.

   **Decidido em 2026-11-14 —** a identidade fica num manifesto versionado `.brza/builders/<nome>.toml` no brza-workspace, com o schema na norma. A config do worktree passa a ser só gerada, a partir desse arquivo. Contexto: o Builder sobrescreve o autor git fixado no `.claude/settings.json` do workspace (`GIT_AUTHOR_NAME` e `GIT_AUTHOR_EMAIL` de brz-anderson). Commit em `workstream/*` continua com esse autor do `settings.json`.

6. **O rótulo da medição.** Opções que estavam em aberto:
   - o hook grava `builder/<nome>` e o índice guarda o nome curto mais `kind` (recomendada) — custo: a mesma frente tem duas grafias, a do log e a do índice; se paga: no primeiro `--by-workstream`, que separa Builder das outras frentes sem mudar o `summarize_measurements.py`;
   - o hook grava só o nome curto — custo: o resumo diário não distingue a classe; se paga: nunca, se a pergunta do resumo for quais frentes são de Builder.

   **Decidido em 2026-11-14 —** a medição grava `builder/<nome>`. O índice continua com o nome curto e o `kind`.

## Desenho

### O que este desenho assume

- **R1.1:** o verbo novo é `brza note builder <nome>`. `brza note workstream <nome>` não ganha flag.
- **R1.2:** o nome curto é único entre `workstream/` e `builder/`. O worktree é `.worktrees/<nome>`. O índice ganha `kind`.
- **R1.3:** commit em `builder/<nome>` usa o autor do agente. O do Bob é `Bob The Builder <bob@brza.dev>`. `workstream/*` permanece com brz-anderson.
- **R1.4:** este plano não cria a frente do Bob nem mexe em `brza sessions`.
- **R1.5:** a identidade versionada é `.brza/builders/<nome>.toml`, com o schema na norma. A config do worktree só é gerada e sobrescreve o autor do `.claude/settings.json`.
- **R1.6:** a medição grava `builder/<nome>`. O índice guarda o nome curto e o `kind`.

### Terreno

#### O prefixo fixo

- **`WORKSTREAM_PREFIX`.** `brza-workflow/bin/brza_runtime.py:192`. `workstream_of_plan` só lista `refs/heads/workstream` e `refs/remotes/<remote>/workstream`, linhas 222–239.
- **As checagens do `brza note`.** `bin/brza-note`: achar o worktree nas linhas 309–313; `commit` nas 883–884; o evento `task` corta o prefixo na 727; colisão de `issue:` e `decision:` nas 968–980; `plan-open` nas 1228–1230; a linha do índice nas 1211–1217 (`workstream` sem prefixo, `worktree` `.worktrees/<nome>`); `index --rebuild` nas 1369–1376; `brza note workstream` nas 1499–1521; a lista de worktrees do `sync` nas 1548–1555.
- **O checador.** `core/.claude/skills/notes-checker/scripts/check_notes.py:212` lista só `refs/heads/workstream/` e `refs/remotes/origin/workstream/`.
- **Medição.** `core/.claude/hooks/measure.py:781` devolve vazio para branch que não é `workstream/` nem a branch da norma. O `compact_guard.py` usa essa função (linhas 71–74). `packages/mcp/brza_mcp/telemetry.py:75` guarda o nome inteiro da branch quando ela não começa com `workstream/`.
- **O texto.** `core/AGENTS.md`, `core/plans/README.md`, `core/work/README.md`, as skills `close-task`, `migration-runner` e `notes-checker`, e `templates/README.md`. O `sed` do `close-task` está na diferença de ouro `tests/hooks/golden_differences.py:285`.
- **O que o sync não reescreve.** O `README.md` deste workspace, linhas 11–15, é local. O `scripts/migrate_pln008.py:339` é migração já feita e fica como está.

### D1 — O subcomando `brza note builder` — `bin/brza-note` (P2)

- **Origem:** R1.1
- **Contexto:** a flag `--builder` em `workstream` misturaria dois tipos no mesmo verbo. Um segundo corpo de worktree, memória e sync duplicaria o que `workstream()` já faz.

#### Como fica

`brza note builder <nome>` chama a mesma função que cria o worktree, liga a memória e faz o push, recebendo o prefixo `builder/`. `brza note workstream <nome>` continua passando `workstream/`. Os dois recusam se o outro prefixo já tem o nome, se `.worktrees/<nome>` existe, ou se o índice já usa esse nome curto. `plan-open`, `commit`, `sync` e `index --rebuild` reconhecem os dois prefixos por uma função só em `brza_runtime.py`, em vez de três constantes copiadas à mão sem teste.

### D2 — Nome único, worktree e `kind` — índice `.brza/index.jsonl` (P2)

- **Origem:** R1.2
- **Contexto:** o git aceita `workstream/bob` e `builder/bob` juntos. O disco não aceita dois worktrees em `.worktrees/bob`. A linha do índice hoje grava `workstream` com o nome curto e `worktree` com `.worktrees/<nome>`.

#### Como fica

A linha nova traz `kind` com valor `workstream` ou `builder`. O campo `workstream` continua o nome curto. `worktree` continua `.worktrees/<nome>`. Linha antiga sem `kind` vale `workstream`. O `brza note ls` mostra o `kind` quando o campo existe.

### D3 — Autor do agente só em `builder/` — `bin/brza-note` e `core/AGENTS.md` (P5, P6)

- **Origem:** R1.3
- **Contexto:** o `AGENTS.md` linhas 73–78 manda o autor `Anderson Pereira Brzezinski <brz.anderson.pereira@gmail.com>` em todo commit deste repositório. O `brza note commit` não confere o e-mail. O Bob precisa assinar `Bob The Builder <bob@brza.dev>` quando a branch é `builder/<nome>`.

#### Como fica

O `brza note commit`, numa branch `builder/`, lê o manifesto da D5 e usa esse autor. Outro autor é recusa, e nada é commitado. Numa branch `workstream/*`, o commit não consulta o manifesto e segue com o autor do `.claude/settings.json`, o do brz-anderson. O parágrafo "Quem commita é o brz-anderson" ganha uma frase: a exceção vale só em `builder/<nome>`, e o autor é o do manifesto daquele nome. `workstream/*` não muda.

### D4 — Bob e Cursor ficam na sequência — este plano (nenhum passo de código)

- **Origem:** R1.4
- **Contexto:** abrir `builder/` na norma é o que destrava o workstream pessoal do Bob e, depois, o `--agent cursor`.

#### Como fica

Nenhum passo daqui roda `brza note builder bob-the-builder` nem edita `packages/client/bin/brza-sessions`. A branch local `builder/bob-the-builder` pode existir no mesmo commit da `master`, sem nota e sem push. Ela não é a frente deste plano.

### D5 — O manifesto do Builder — `.brza/builders/<nome>.toml` (P5, P6)

- **Origem:** R1.5
- **Contexto:** o `.claude/settings.json` do workspace fixa `GIT_AUTHOR_NAME` e `GIT_AUTHOR_EMAIL` em brz-anderson. Numa branch `builder/`, o agente precisa assinar com o próprio autor, e um clone tem de achar essa identidade sem configuração manual.

#### Como fica

Cada Builder tem um arquivo versionado `.brza/builders/<nome>.toml` no brza-workspace. O schema desse arquivo fica na norma (o `core/`, que o `brza sync` leva à `master`). O arquivo em si não é config de worktree: `brza note builder` gera, no worktree, a config local de autor a partir do toml, e essa config sobrescreve o autor fixado no `.claude/settings.json` só para a branch `builder/<nome>`. O toml do Bob, com `Bob The Builder <bob@brza.dev>`, não nasce neste plano.

### D6 — O rótulo da medição — `core/.claude/hooks/measure.py` (P4)

- **Origem:** R1.6
- **Contexto:** o índice usa o nome curto mais `kind`. O resumo diário lê a string que o hook grava e não lista branches.

#### Como fica

Numa branch `builder/<nome>`, a linha de medição grava `workstream` como `builder/<nome>`. O índice não usa essa string: continua com o nome curto e o `kind`. O `summarize_measurements.py` não muda. `workstream/<nome>` continua gravando só `<nome>`.

## Passos

### P1 — Uma função para os dois prefixos

Executa D1 · executor: sessão no `brza-workflow`

Estimado: 2 h · Executado: — h

- [ ] `brza-workflow/bin/brza_runtime.py`: uma função que aceita `workstream/` e `builder/` e devolve o tipo e o nome curto. `workstream_of_plan` procura os dois prefixos. O `brza note` ainda recusa `builder/` até o P2.
- [ ] Teste novo da função: `builder/bob` é achado; `workstream/bob` junto de `builder/bob` é ambíguo.
- [ ] Desfazer: reverter o commit. Evidência esperada: o teste da função passa, e `brza note plan-open` numa branch `builder/` ainda sai 1.

### P2 — O subcomando `brza note builder`

Executa D1 e D2 · executor: sessão no `brza-workflow`

Estimado: 5 h · Executado: — h

- [ ] `bin/brza-note`: subcomando `builder <nome>` que reusa a função de worktree, memória e push já usada por `workstream`, com o prefixo `builder/`. `workstream <nome>` permanece. Recusa nome curto repetido no outro prefixo, worktree existente ou nome já usado no índice. Ao criar o worktree, gera a config local de autor a partir de `.brza/builders/<nome>.toml` e não grava essa config no git.
- [ ] `plan-open`, `commit`, `sync`, `index --rebuild` e o catálogo de links reconhecem os dois prefixos. A linha do índice ganha `kind`. `workstream` segue o nome curto e `worktree` segue `.worktrees/<nome>`.
- [ ] Teste em `tests/cli/test_brza_note.py` e `tests/cli/test_brza_note_index.py`: o subcomando cria `builder/<nome>` a partir da `master` e faz o push dessa branch; o mesmo nome em `workstream/` é recusado; `plan-open` e `commit --no-push` gravam `kind: builder`.
- [ ] Desfazer: reverter o commit. Evidência esperada: `brza note workstream demo` continua em `workstream/demo`, e `brza note builder demo` deixa de existir.

### P3 — O checador enxerga `builder/`

Executa D2 · executor: sessão no `brza-workflow`

Estimado: 2 h · Executado: — h

- [ ] `core/.claude/skills/notes-checker/scripts/check_notes.py` lista também `refs/heads/builder/` e `refs/remotes/origin/builder/`.
- [ ] Teste em `tests/notes-checker/run.py`: um link para uma nota que só está em `builder/bob` resolve.
- [ ] Desfazer: reverter o commit. Evidência esperada: o mesmo link volta a ser `unresolved-link`.

### P4 — Medição e trava do `/compact`

Executa D2 e D6 · executor: sessão no `brza-workflow`

Estimado: 2 h · Executado: — h

- [ ] `core/.claude/hooks/measure.py` e `packages/mcp/brza_mcp/telemetry.py` reconhecem `builder/`. A string gravada na medição é `builder/<nome>`. O índice não usa essa string. O `compact_guard.py` acompanha, porque usa `resolve_workstream`.
- [ ] Testes: `tests/hooks/test_measure_workstream.py`, `tests/hooks/test_compact_guard.py`, `tests/mcp/test_mcp_telemetry.py`. A branch `builder/bob` mede `builder/bob`; `workstream/studio` continua medindo `studio`.
- [ ] Desfazer: reverter o commit. Evidência esperada: branch `builder/bob` volta a medir como ausente, e o `/compact` manual deixa de olhar o worktree dela.

### P5 — O autor do agente no `brza note commit`

Executa D3 e D5 · executor: sessão no `brza-workflow`

Estimado: 3 h · Executado: — h

- [ ] O `brza note commit`, em branch `builder/<nome>`, lê `.brza/builders/<nome>.toml` e aplica esse autor. Autor diferente do manifesto recusa antes do `git commit`. Branch `workstream/*` não lê o manifesto e segue com o autor do `.claude/settings.json`.
- [ ] A config de autor do worktree é só gerada a partir do toml e sobrescreve, nessa branch, o `GIT_AUTHOR_*` fixado no `.claude/settings.json`. O arquivo gerado fica fora do git.
- [ ] Teste em `tests/cli/test_brza_note.py`, com um toml de fixture `Bob The Builder <bob@brza.dev>`: commit em `builder/bob` sai com esse autor; outro autor sai 1 e não cria commit; commit em `workstream/studio` segue com o autor do ambiente e não é recusado por estar fora do diretório.
- [ ] Desfazer: reverter o commit. Evidência esperada: o `brza note commit` volta a aceitar o autor que o `settings.json` mandar, nos dois prefixos.

### P6 — O texto da norma

Executa D1, D2, D3 e D5 · executor: sessão no `brza-workflow`

Estimado: 3 h · Executado: — h

- [ ] Atualizar `core/AGENTS.md` (o parágrafo das linhas 73–78 abre a exceção só em `builder/` e aponta o schema de `.brza/builders/<nome>.toml`), `core/plans/README.md`, `core/work/README.md`, `close-task` (o `sed` tira `workstream/` ou `builder/`), `migration-runner`, `notes-checker` e `templates/README.md`. O schema do manifesto mora nesse texto da norma.
- [ ] Atualizar o lado `new` da diferença em `tests/hooks/golden_differences.py` no mesmo commit.
- [ ] Teste: `tests/hooks/test_golden_render.py`.
- [ ] Desfazer: reverter o commit. Evidência esperada: o render com o manifesto do brza-workspace deixa de mencionar `builder/`.

### P7 — Trazer a norma ao workspace

Executa D1 · executor: sessão no `brza-workspace`, a pedido

Estimado: 1 h · Executado: — h

- [ ] Depois do merge do PR do `brza-workflow`, no checkout da `master`: `brza sync --dry-run`. Se o diff for só esta norma, `brza sync --no-push`, e o push da `master` no passo seguinte, o que o `AGENTS.md` linhas 67–78 autoriza. Em seguida `brza note sync` leva a `master` aos worktrees `workstream/*`.
- [ ] Este passo não roda `brza note builder`.
- [ ] Desfazer: se o push da `master` não ocorreu, descartar o commit local; se ocorreu, `git revert` desse commit. Evidência esperada: `brza sync --dry-run` seguinte não mostra diff desta norma, e `brza note plan-open` ainda não é usado para criar o Bob.

### P8 — A frase no README local

Executa D1 · executor: sessão no `brza-workspace`, a pedido

Estimado: 0.5 h · Executado: — h

- [ ] Uma frase no `README.md` deste workspace, editado na `master` pelo caminho das linhas 67–71 do `AGENTS.md`: `builder/<nome>` é o workstream pessoal de um Builder e nasce com `brza note builder <nome>`.
- [ ] Desfazer: reverter esse commit. Evidência esperada: a lista dos workstreams de agora continua igual, com a frase nova ao lado.

## Regressão

- **`brza note workstream <nome>` cria `workstream/<nome>`, faz o push dessa branch e liga a memória.** Conferência: o teste já existente `test_workstream_creates_the_branch_from_the_fresh_origin_master_and_the_worktree_and_pushes` em `tests/cli/test_brza_note.py`.
- **`plan-open` e `commit` numa branch `workstream/*` seguem iguais, com autor do `env`.** Conferência: um teste de `commit` em `workstream/studio` que não consulta a tabela de builders.
- **O `notes-checker` continua resolvendo link que só está em `workstream/*`.** Conferência: `tests/notes-checker/run.py`, o caso que já existe para `origin/workstream/*`.

## Worklogs

- 2026-11-14 — R1.1 a R1.6 fechadas; P1–P8 escritos e nenhum executado. A medição grava `builder/<nome>`. O link do worklog de 9 de novembro passou a apontar o PLN-017 no GitHub.
  [O PLN-024 do prefixo builder/ foi aberto](../../work/worklogs/2026-11-14-plano-do-prefixo-builder.md)

## Fechamento

- [ ] Todo passo `[x]` com evidência, ou `[-]` com motivo.
- [ ] Todo achado com destino que existe.
- [ ] Um resumo por commit ou PR do `brza-studio` da entrega, com o link do plano: os achados e o destino de cada um. Trabalho só em notas de `work/` e `plans/` não tem resumo.
- [ ] O durável saiu para a casa dona e está em `## Decisões` e `## Documentação`: a decisão em `work/decisions/`, a norma do `brza-studio`, o guia.
- [ ] As decisões que o plano respondeu estão `done`, citando a rodada.
- [ ] `status: done`, `phase: closed` e `completed` no frontmatter.
