---
status: in_review
phase: review
origin: request
description: Grava a linha de turno do Grok e do Codex no log de medida, com o mesmo id no carimbo da tarefa, e sonda como medir o Antigravity.
ready: sim
estimate_h: 5
executed_h: 1.5
remaining_h: 0
scope:
  - brza-workflow
opened: 2026-11-09
owner: Anderson
priority: high
tags:
  - tooling
---

# PLN-018: O turno do Grok e do Codex entra no log, e a tarefa carimba o id dessa sessão

- **Retomar:** P1–P4 fechados em 2026-11-09, `brza-workflow@5098439`, ainda só na `master` local. Próximo: a revisão
  da entrega. O `.grok/hooks/runtime.json` e o hook do Codex ficam no PLN-004 e chamam esse script. Este plano não
  instala outro json.
- **Dividido:** [PLN-018 — Entrevista](PLN-018-interview.md)

## Pedido

- **Origem:** pedido livre de Anderson em 2026-11-09, na sessão `workspace`. A régua da entrega é a R1 e a R2, que
  cortaram o pedido. Lacunas já abertas:
  [O Grok fica sem medida por tarefa](../../work/issues/o-grok-fica-sem-medida-por-tarefa.md) e
  [Codex e Antigravity ficam sem medida por tarefa](../../work/issues/codex-e-antigravity-sem-medida-por-tarefa.md).
  O carimbo que este plano estende é o do
  [PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou](../PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-plan.md),
  P3 já no código (`brza-workflow/bin/brza-note:719` lê `CLAUDE_CODE_SESSION_ID`). A frente maior dos runtimes no
  fluxo continua no
  [PLN-004: Os runtimes Codex, `agy` e Grok trabalham no fluxo do workspace como o Claude](../PLN-004-os-runtimes-codex-agy-e-grok-no-fluxo/PLN-004-plan.md),
  parado antes da R21.

> "crie um plano para que todos os runtimes entrem na medição, prioridade alta"

O corte, nas respostas de 2026-11-09:

> "1. 2"
>
> "2. Grok e Codex + uma sonda verificando como medir também o Antigravity"
>
> "3. 1"
>
> "4. verifique o estado atual do planos PLN-004 e PLN-012 antes de decidir"

E, na volta da frase livre:

> "opção 1"

### Cobertura

| Origem | Critério de aceite | Passo | Teste (nível) |
| :----- | :----------------- | :---- | :------------ |
| `Pedido`, `R1.1` | Um turno de uso do Grok grava uma linha `turn`, com o runtime e com `estimated_cost_usd` igual aos `costUsdTicks` desse turno divididos por 1e10. Sem id de sessão no payload, a linha não é gravada | P1 | `tests/hooks/test_runtime_turn.py` (unidade) |
| `Pedido`, `R1.1` | Um turno do Codex grava uma linha `turn` com o runtime e o delta de `usage`. A soma de `thread_token_usage` e a de `turn_token_usage` não entram. Sem chave de preço, o custo fica nulo | P2 | `tests/hooks/test_runtime_turn.py` (unidade) |
| `Pedido`, `R1.1` | O `brza note commit` grava em `sessions:` e no evento `task` o mesmo id de sessão do runtime que a linha `turn` usa | P3 | `tests/cli/test_brza_note.py` (unidade) |
| `R2.1` | A sonda do Antigravity registra, para a CLI e para o chat ACP, se há token, model e custo. Este plano não ganha escritor do Antigravity | registrada no Terreno | conferência do Terreno |
| `R1.3` | Nenhum código de hook destes runtimes entra no `brza-workflow` antes da sonda de stdin mostrar se o caminho da sessão chega no Stop | P1 | a sonda fechou o portão em 2026-11-09; o escritor vem depois |

### Fora de escopo

- **Os outros ids do catálogo de launch do Studio.** A R1.2 ofereceu os 45; a R2.1 ficou em Grok, Codex e na sonda
  do Antigravity.
- **O escritor do Antigravity.** A sonda é deste plano e está no Terreno. A CLI tem token e não tem model nem custo
  na linha; o chat ACP não tem os três na transcrição. O escritor não entra aqui. A rodada que o traria de volta não
  foi feita. Continua em
  [Codex e Antigravity ficam sem medida por tarefa](../../work/issues/codex-e-antigravity-sem-medida-por-tarefa.md).
- **O backfill de sessões antigas.** A R4.1 do PLN-012 já o recusou. Este plano mede o que o hook vir a partir da entrega.
- **Mudar o launch do Studio** (`--trust`, ambiente no `grok agent stdio`). Era a opção 3 da R1.3. A sonda viu o
  caminho chegar sem `--trust`. Continua fora.
- **O que a R21.10 deixou no PLN-004.** O pacote `packages/runtimes`, o `brza delegate`, o `grok-brza`, a saída cedo
  dos hooks do núcleo quando há `GROK_HOOK_EVENT`, o arquivo `.grok/hooks/runtime.json` e o hook do Codex, o `agy`, a
  linha do filho fora da soma, o `guardian_review` e o `metadata.runtime` da memória. O `measure_runtimes.py` não
  grava esta linha: este plano é o único escritor dela. A reescrita do `D8` e do `D9` contra este Desenho é da sessão
  de lá. O painel da reunião continua na issue do `playground`.
- **Reabrir o PLN-012.** O P6.2 e o P6.3 seguem lá. Este plano estende o carimbo que o P3 já grava.
- **CPU e RSS destes runtimes.** `machine` continua null. O `proc_pid_rusage` do PLN-012 lê o executável `claude`.

## Restrições

- **O código é do `brza-workflow`.** Chega aos workspaces pelo `brza sync`. Editado no checkout do workspace, trava o
  sync seguinte. Nada do `playground` se edita por este plano.
- **O `measure()` do Claude não lê estes logs.** No `updates.jsonl` do Grok ele não grava; no `chat_history.jsonl`
  gravaria turno de token zero. Turno de token zero apaga o "não medida" do PLN-012. Sem id de sessão, não há linha.
- **O dólar do Grok é `costUsdTicks` dividido por 1e10.** A tabela de preço do Claude não precifica estes modelos: um
  model sem preço zera o custo do segmento. O objeto `session` do `usage.json` inclui histórico herdado e não se soma.
- **O delta do Codex é o `usage` do registro.** `thread_token_usage` e `turn_token_usage` não são delta. Não há chave
  de preço no rollout.
- **Um turno de uso, uma linha.** Na sessão `01a1a459` houve 3 Stops para 2 turnos de `usage.json`.
- **`events.jsonl` `turn_started.turn_number` e `usage.json` `turnNumber` são índices diferentes.** A hipótese
  `turnNumber = turn_started + 1` não segurou além de duas sessões. Não vira desenho.
- **O carimbo de hoje fica.** Sem `CLAUDE_CODE_SESSION_ID` e sem o id de runtime que este plano ainda vai acrescentar,
  o worklog commitado segue byte-igual ao de hoje. Conferência: `test_brza_note`.
- **O `brza sync` copia o script em `core/` e não copia o json de hook.** Esse json, e o hook do Codex, são do
  PLN-004. Este plano não instala outro json.

## Desenho

### O que este desenho assume

- **R1.1:** a primeira entrega grava o turno e o carimbo. Uma linha `turn` por turno de uso, com `runtime`. Sem id de
  sessão, não há linha. `machine` fica null. Sem backfill.
- **R1.2, R2.1:** Grok e Codex nesta entrega. O Antigravity fica na sonda, sem escritor.
- **R1.3:** o código do hook só começa depois da sonda. A sonda rodou. O launch do Studio não muda.
- **PLN-004, R21.10:** este plano é o único escritor da linha `turn` do Grok e do Codex. O arquivo que chama o
  escritor, o `agy`, o filho fora da soma, o `guardian_review` e o `metadata.runtime` da memória ficam lá. O `D8` e o
  `D9` se reescrevem contra este Desenho, na sessão de lá. A leitura do `usage.json` do Grok é uma função, chamada por
  este plano, pelo `D9` e pelo `brza sessions usage`.
- **O carimbo de hoje fica** quando não há `CLAUDE_CODE_SESSION_ID` nem `GROK_SESSION_ID`. Conferência:
  `tests/cli/test_brza_note.py:1138`.

### Terreno

Sonda de 2026-11-09, nesta sessão. Chaves e booleanos. Nenhum id, custo ou texto de transcrição entrou aqui. Os
diretórios e as sessões da sonda foram criados e removidos no fim.

#### O Stop do Grok

- **O caminho chega sem `--trust`.** Um `grok agent stdio`, com `--always-approve` e `--reasoning-effort low`, num git
  novo. `~/.grok/trusted_folders.toml` está vazio e o `config.toml` não tem `folder_trust`. O launch do Studio é esse
  comando, com `env: {}`, e não passa `--trust`
  (`brza-studio/src/main/acp/acp-launch-specs.ts:171-180`). Um prompt, `stopReason` `end_turn`, dois Stops.
- **Os dois Stops trazem o mesmo identificador.** `session_id` e `sessionId` preenchidos e iguais; `transcript_path` e
  `transcriptPath` preenchidos e iguais, basename `updates.jsonl`; `cwd` e `workspaceRoot` preenchidos e iguais. Há
  alias em camelCase e em snake_case. `hook_event_name` é `Stop`.
- **O hook de usuário carregou.** Um json novo em `~/.grok/hooks/` rodou ao lado de `orca-status.json`. O processo do
  hook tinha `GROK_SESSION_ID`, `CLAUDE_PROJECT_DIR` e `GROK_WORKSPACE_ROOT`, e não tinha `CLAUDE_CODE_SESSION_ID`.
- **O shell de ferramenta, que é o que o `brza note commit` vê, tem `GROK_SESSION_ID` e não tem
  `CLAUDE_CODE_SESSION_ID`.** Esse valor é o nome de um diretório de sessão da sonda. O `sessionId` do `usage.json` é o
  nome do diretório em 6 de 6. A igualdade do `session_id` do stdin com o ambiente, no mesmo Stop, não foi medida: um
  líder do Grok não recarregou o hook, e `--no-leader` não disparou o hook de usuário.
- **O custo está no turno.** `usage.json` tem `session`, `sessionId`, `turns` e `updatedAt`. O objeto `session` tem o
  `costUsdTicks` acumulado. Cada item de `turns` tem `turnNumber`, `endedAt` e o `costUsdTicks` daquele turno. Não se
  soma o objeto `session`.
- **O pai já inclui o filho.** Medido pelo PLN-004 em 2026-11-03, no Grok Build CLI 1.0.70
  (`/private/tmp/pln004/grok/levantamento.md`, F84): o `usage.json` do pai soma o turno do filho. Somar os dois conta
  em dobro. O `inputTokens` do turno inclui o que `cachedReadTokens` conta (F81).
- **Dois Stops, um fim de turno e um shutdown.** A sonda daqui viu dois Stops no mesmo `end_turn`; o segundo não traz
  `lastAssistantMessage`. O PLN-004 mediu os valores: `reason: end_turn` e, no segundo, `reason: shutdown`. O
  `SubagentStop` traz `subagentType`, `subagentId` e o `sessionId` e o `transcriptPath` do filho. O ambiente do hook
  traz `GROK_HOOK_EVENT` além do que a sonda daqui já viu.
- **Hook de projeto e hook de usuário não passam pela mesma trava.** A doc
  (`~/.grok/docs/user-guide/10-hooks.md:84-86`) pula em silêncio o hook de projeto enquanto a pasta não é confiada.
  O hook do próprio usuário em `~/.grok/hooks/` também espera confiança, com duas saídas: um `grok -p` trata a pasta
  como confiada para esse hook, e `GROK_FOLDER_TRUST=0` abre a trava. A sonda daqui, em `grok agent stdio` sem
  `--trust`, viu o json de `~/.grok/hooks/` rodar. Isso não diz que um `.grok/hooks/*.json` do projeto rodaria no chat.
- **O app não pré-confia o Grok.** O verbete `grok` em
  `brza-studio/src/shared/agent-launch/catalog/tui-agent-config.ts:284` não tem `preflightTrust`. Não há
  `GROK_FOLDER_TRUST` em `src/`. O `grok-brza` da R18.2, que poria essa variável, ainda não existe. O
  `~/.grok/hooks/orca-status.json` é o hook global do app: só age com `ORCA_PANE_KEY` e não mede.

#### O Stop do Codex

- **O Stop capturado é o de `codex exec`, não o do chat.** O chat do Studio sobe `app-server`
  (`brza-studio/src/main/codex/structured/launch/codex-structured-launch-resolution.ts:126`).
- **Um Stop traz o caminho.** Chaves: `cwd`, `hook_event_name`, `last_assistant_message`, `model`, `permission_mode`,
  `session_id`, `stop_hook_active`, `transcript_path`, `turn_id`. Sem camelCase. `session_id`, `transcript_path` e
  `cwd` preenchidos. O basename casa `rollout-*.jsonl`. A chave `model` existe; a sonda não registrou se o valor vinha
  vazio.
- **O processo do hook não tem `CODEX_SESSION_ID` nem `CODEX_THREAD_ID`.** Tinha `GROK_SESSION_ID` porque esta sessão,
  que é Grok, lançou o Codex. É herança, não comportamento do Codex.
- **O shell de ferramenta tem `CODEX_SESSION_ID` e `CODEX_THREAD_ID`, iguais entre si**, e diferentes do
  `GROK_SESSION_ID` herdado. Não há medida de igualdade com o `session_id` do stdin.
- **O comando só rodou dentro de `~/.codex/hooks.json`, com `--dangerously-bypass-hook-trust`.** Um
  `.codex/hooks.json` novo no projeto não rodou, nem com esse flag. O `config.toml` guarda `trusted_hash` em
  `[hooks.state."<arquivo>:stop:0:0"]`. Editar o arquivo muda o hash. A sonda devolveu o arquivo ao byte anterior.

#### O carimbo e a entrega

- **O carimbo lê só `CLAUDE_CODE_SESSION_ID`.** `brza-workflow/bin/brza-note:719`. Sem esse id,
  `prepare_worklog_measure` (`:834-836`) não mexe no worklog, e `write_task_event` (`:850-854`) ainda grava o evento
  com `session_id` null. `--until` recusa sem sessão Claude (`:727`). `session_name()` devolve None se o agente não é
  claude (`:254-255`). A norma diz o mesmo em `core/work/README.md:229`.
- **O `measure()` não serve a estes logs.** `turn()` (`core/.claude/hooks/measure.py:675-686`) volta sem gravar quando
  não há `transcript_path` ou quando `api_calls` é 0. A tabela `PRICES` (`:56-67`) é de modelos Claude. A linha `turn`
  (`:694-712`) não tem `runtime`.
- **O sync não entrega o hook destes runtimes.** `sources_of` (`bin/brza-sync:132-136`) copia `core/` e o `core/` de
  cada pacote, e tira `settings.hooks.json`. `merge_hooks` (`core/.claude/hooks/brza_root.py:740-751`) só troca a chave
  `hooks` do `.claude/settings.json`. `core.packages` é `[]` (`brza_root.py:531`). Não há `.grok/hooks` nem
  `.codex/hooks.json` no `brza-workflow`. O Stop do Claude continua em `core/.claude/settings.hooks.json:19-27`.

#### O Antigravity

- **CLI** (`~/.gemini/antigravity-cli`): 135 de 143 `transcript.jsonl` têm `input_tokens`, `output_tokens` e
  `cache_read_tokens`. A linha não tem `usage`, `model`, `cost`, `price` nem `usd`. O `model` de `settings.json` é
  configuração. O id é o nome do arquivo. `trajectory_id` não é esse nome (0 de 159).
- **Chat ACP** do Studio: 0 de 17 `transcript.jsonl` têm chave de token, model ou custo. `acp_token.json` tem
  `refresh_token` e `token_uri`: credencial, não uso. `trajectory_id` é o nome do arquivo em 24 de 24.
- **Fora dessas duas superfícies.** `~/.gemini/antigravity` repete o desenho da CLI, 8 de 8 com o trio de token, sem
  model e sem custo na linha. `~/.gemini/antigravity-ide` não tem transcrição. No blob do `.db` há JSON embutido em
  minoria; não é coluna e não é a fonte.
- **O hook que existe não mede.** `~/.gemini/config/hooks.json` aponta para o `antigravity-hook.sh` do Orca, não para o
  `measure.py`.

### D1 — A linha do Grok — `core/.claude/hooks/`

- **Origem:** R1.1, R1.3, PLN-004 R21.10
- **Contexto:** o Stop traz o id e o `updates.jsonl`, e o dólar está no `usage.json`, por turno. Dois Stops não são
  dois turnos. O arquivo que chama o escritor é do PLN-004.

#### Como fica

O tradutor é `runtime_turn.py` em `core/.claude/hooks/`, modo `grok` ou `codex`. Não é o `measure()` nem o
`measure_runtimes.py`. O `brza sync` o entrega porque copia `core/`. Quem o chama é o `.grok/hooks/runtime.json` da
R18.4 do PLN-004, e o hook do Codex de lá. Este plano não grava esse json, nem outro em `~/.grok/hooks/` ou em
`~/.codex/`.

A leitura do `usage.json` é uma função desse script. Este escritor, o `D9` do PLN-004 e o `brza sessions usage` da
issue do `playground` chamam a mesma função. A linha `turn` sai só deste script. O painel da reunião fica na issue.
Este plano não edita a skill nem o PLN-004.

No `Stop`, a função lê o `usage.json` cujo `sessionId` é o `session_id` do payload. Grava uma linha por
`turns[].turnNumber` que ainda não tenha linha. `Stop` com `reason: shutdown`, sem turno novo, não grava. Não soma o
objeto `session`. Não grava o `usage.json` do filho: o do pai já o inclui. A linha do filho fora da soma fica no
PLN-004. No `SubagentStop`, este script não grava linha `turn`.

A linha leva `event` `turn`, `runtime` `grok`, o `session_id` do payload e `estimated_cost_usd` igual ao
`costUsdTicks` daquele turno dividido por 1e10. O `input` da linha é `inputTokens` menos `cachedReadTokens`; o
`cache_read` é `cachedReadTokens`. `machine` é null. Sem `session_id`, não grava. Não há backfill. `current_turn` no
`brza-note` continua lendo só o transcript do Claude.

O teste que falha antes de o código existir: dois turnos no `usage.json` do pai, um `usage.json` de filho já contido
neles, e um segundo Stop `shutdown` gravam duas linhas, com o custo de cada turno do pai, sem o objeto `session` e sem
uma linha a mais do filho.

**Descartada — um json novo em `~/.grok/hooks/` instalado por este plano.** A sonda viu esse caminho rodar, e a R21.10
deu o arquivo de hook ao PLN-004. Dois json gravariam duas vezes.

### D2 — A linha do Codex — `core/.claude/hooks/`

- **Origem:** R1.1, R1.3, PLN-004 R21.10
- **Contexto:** o Stop de `codex exec` traz `session_id` e `transcript_path`. O delta que a restrição já fixou é o
  `usage` do registro. Não há chave de preço. O arquivo de hook é do PLN-004.

#### Como fica

O mesmo script lê o rollout em `transcript_path`, no modo `codex`. Uma linha por turno de uso, com o delta `usage`.
`thread_token_usage` e `turn_token_usage` não entram. Sem chave de preço, `estimated_cost_usd` é null. `runtime` é
`codex`. `machine` é null. Sem `session_id`, não grava. O `guardian_review` não entra nesta linha: fica no PLN-004.

O Stop do `app-server`, que é o launch do chat, não foi capturado. Se esse Stop não trouxer `transcript_path`, a linha
não sai. Isso não se preenche por hipótese.

**Descartada — um `.codex/hooks.json` novo no projeto, instalado por esta sonda.** O Stop não o executou, nem com
`--dangerously-bypass-hook-trust`. O flag só segue com hook já habilitado.

**Descartada — entregar com `--dangerously-bypass-hook-trust`.** É flag da sonda, não da entrega.

**Descartada — este plano edita o `~/.codex/hooks.json` do usuário, ou segue só com o Grok.** Eram as duas saídas em
aberto. A R21.10 deu o arquivo de hook ao PLN-004 e manteve as duas linhas neste plano. Editar o arquivo do usuário
mudaria o `trusted_hash`.

### D3 — O carimbo lê o id do runtime — `bin/brza-note`

- **Origem:** R1.1
- **Contexto:** hoje o `sessions:` e o `task.session_id` saem só de `CLAUDE_CODE_SESSION_ID`. No Grok essa variável
  não está no shell de ferramenta. `GROK_SESSION_ID` está, e é o `sessionId` do `usage.json`.

#### Como fica

`task_context` lê `CLAUDE_CODE_SESSION_ID` e, na ausência, `GROK_SESSION_ID`. `sessions:` e `task.session_id` recebem
esse valor. O teste de `test_brza_note.py:1138` continua verde quando nenhuma das duas está presente: o worklog
commitado fica byte-igual ao de hoje, e o evento sai com `session_id` null.

O teste do escritor afirma que o `session_id` da linha do Grok é o `GROK_SESSION_ID` do processo. A sonda não comparou
os dois no mesmo Stop. Se o teste falhar, o lado não se escolhe no código.

O carimbo do Codex não lê `CODEX_SESSION_ID`. O shell de ferramenta tem essa variável, igual a `CODEX_THREAD_ID` na
sonda, e o processo do hook não tem nenhuma das duas. Sem a igualdade com o `session_id` do Stop, o carimbo não a usa.
`--until` continua a exigir sessão Claude. `session_name()` continua None fora do Claude.

## Passos

### P1 — A linha do Grok

Executa D1 · executor: sessão que conduz

Estimado: 2 h · Executado: 0.5 h

- [x] **1. Teste que falha** — dois turnos no `usage.json` do pai, o do filho já contido neles, e um segundo Stop `shutdown`
- [x] **2. O script** `brza-workflow/core/.claude/hooks/runtime_turn.py`, modo `grok`
- [x] **3. Rodar** `python3 -m unittest tests.hooks.test_runtime_turn`
- [x] **4. Commit** no `brza-workflow`

**Evidência:** `brza-workflow@5098439` · `python3 -m unittest tests.hooks.test_runtime_turn` e os testes do carimbo e do `usage` → 21 passed

### P2 — A linha do Codex

Executa D2 · executor: sessão que conduz

Estimado: 1 h · Executado: 0.5 h

- [x] **1. O mesmo script, modo `codex`** — delta `usage`, custo null, `guardian_review` sem linha
- [x] **2. Rodar** o mesmo unittest
- [x] **3. Commit** no `brza-workflow`, junto do P1

**Evidência:** `brza-workflow@5098439` · o mesmo unittest → 21 passed

### P3 — O carimbo lê o id do Grok

Executa D3 · executor: sessão que conduz

Estimado: 1 h · Executado: 0.3 h

- [x] **1. `task_context`** lê `GROK_SESSION_ID` só na ausência de `CLAUDE_CODE_SESSION_ID`
- [x] **2. `--until`** continua a exigir sessão Claude
- [x] **3. Rodar** `tests/cli/test_brza_note.py`, com o teste de 1138 verde
- [x] **4. Commit** no `brza-workflow`, junto do P1

**Evidência:** `brza-workflow@5098439` · `TaskCommitTest.test_without_session_preserves_worklog_bytes_and_writes_null_session`, `test_grok_session_id_alone_is_stamped_on_the_worklog_and_the_task` e `test_until_with_only_grok_session_id_is_refused` → passed

### P4 — O `brza sessions usage` chama a leitura

Executa D1 · executor: sessão que conduz

Estimado: 1 h · Executado: 0.2 h

- [x] **1. O comando `usage` do Grok** chama `read_grok_usage`. Sem arquivo, continua `unmeasured`. O Antigravity não muda
- [x] **2. Rodar** `tests/cli/test_brza_sessions.py`
- [x] **3. Commit** no `brza-workflow`, junto do P1

**Evidência:** `brza-workflow@5098439` · `test_usage_grok_sums_turns_from_usage_json_and_not_the_session_object`, `test_usage_grok_and_antigravity_are_unmeasured` e `test_usage_codex_ignores_info_null_and_returns_last_totals` → passed

## Regressão

- **Sem `CLAUDE_CODE_SESSION_ID` e sem `GROK_SESSION_ID`, o worklog commitado fica byte-igual.** `TaskCommitTest.test_without_session_preserves_worklog_bytes_and_writes_null_session`.
- **O `usage` do Codex no `brza sessions` continua o último total do rollout.** `test_usage_codex_ignores_info_null_and_returns_last_totals`. Não é a linha `turn`.
- **O Antigravity no `brza sessions usage` continua `unmeasured`.** `test_usage_grok_and_antigravity_are_unmeasured`.
- **O Stop do Claude continua no `settings.hooks.json`.** Este plano não acrescenta json.

## Worklogs

- 2026-11-09 — R1 e R2 fechadas; PLN-018 reservado. Parou na sonda de stdin, antes do Desenho.
  [PLN-018: a abertura da medida do Grok e do Codex](../../work/worklogs/2026-11-09-pln-018-a-abertura-da-medida-do-grok-e-do-codex.md)
- 2026-11-09 — Sonda de stdin e do Antigravity; D1–D3 escritos. Parou no corte dos passos e na instalação do hook do
  Codex.
  [PLN-018: a sonda do stdin e o Desenho](../../work/worklogs/2026-11-09-pln-018-a-sonda-do-stdin.md)
- 2026-11-09 — Aviso do PLN-004 registrado. A R21.10 já estava decidida; o D1 e o D2 passam a entregar o escritor, e o
  arquivo de hook fica lá. O complemento do mesmo dia nomeou este plano como único escritor, os três leitores da
  função e a reescrita do D8 e do D9 contra este Desenho. O corte dos passos continua esperando.
  [PLN-018: o aviso do PLN-004](../../work/worklogs/2026-11-09-pln-018-o-aviso-do-pln-004.md)
- 2026-11-09 — R4: executar o escritor aqui. P1–P4 fechados em `brza-workflow@5098439`, na `master` local. A revisão
  da entrega é o próximo. Nenhum json de hook foi instalado.
  [PLN-018: o escritor da linha](../../work/worklogs/2026-11-09-pln-018-o-escritor-da-linha.md)

## Pendências conhecidas

- [O Grok fica sem medida por tarefa](../../work/issues/o-grok-fica-sem-medida-por-tarefa.md) — a medida é este plano;
  a issue segue aberta até a linha existir.
- [Codex e Antigravity ficam sem medida por tarefa](../../work/issues/codex-e-antigravity-sem-medida-por-tarefa.md) —
  o escritor do Antigravity continua nela; a sonda está no Terreno. A issue do `playground` sobre o custo do Grok na
  reunião e o `D9` do PLN-004 leem o mesmo `usage.json` pela função do D1. O painel dela não é deste plano.
