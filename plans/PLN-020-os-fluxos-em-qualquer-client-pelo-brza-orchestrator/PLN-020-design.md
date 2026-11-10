# PLN-020 — Desenho

O Desenho do [PLN-020: Os fluxos do workspace rodam em qualquer client, pelas skills distribuídas e por verbos do brza-orchestrator](PLN-020-plan.md).
É rascunho de consultor: cada escolha sem lastro aponta a pergunta da R5 à R8, preparadas e não enviadas, na
Entrevista do plano. A alternativa marcada "recomendada" é a do consultor, não decisão.

## O que este desenho assume

- **R1.1:** o motor é a portabilidade entre clients, e a sonda vem antes de construir.
- **R2.2:** os verbos da reunião esperam duas reuniões sem desvio.
- **R3.1:** o `.agents/skills` é um symlink trazido pelo `core/`.
- **R3.2:** entram `close_task`, `start_task`, `index_query` e `decision_record`; o `check_notes` sai.
- **R3.3:** a identidade da norma vai ao `.git/config`.
- **R4.1:** os fluxos longos ficam nas skills distribuídas, sem verbo nem MCP prompt; o MCP cobre só o que o client
  não faz (D3–D6).
- **Restrição:** uma fonte só — o `brza note` é o motor, o verbo é o adaptador, e a skill chama o verbo, com o CLI de
  reserva.

## Terreno

### A sonda dos clients (2026-11-09)

A sonda rodou num clone isolado no scratch da sessão:
- repositório bare como `origin`, a `master` e os worktrees dos workstreams;
- `BRZA_WORKSPACE` e `MEASURE_DIR` apontando para o clone.

As saídas brutas ficaram no scratch, fora do git.

#### O catálogo de skills em cada client

- **M1 — Codex sem distribuição não vê as skills do workspace.** Codex CLI `0.166.0`, `codex exec -s read-only`: o
  catálogo trouxe as de usuário (`~/.codex/skills`), as de sistema e as de plugin, e "do repositório: nenhuma". [medido]
- **M2 — Codex vê as seis com um symlink.** `.agents/skills -> ../.claude/skills`, no worktree: as seis no catálogo,
  com a descrição. [medido]
- **M3 — Cursor lê o `.claude/skills` sem nada.** `cursor-agent 2026.10.22`, `--mode ask`: as seis, com e sem o
  `.agents/`. [medido]
- **M4 — Antigravity precisa do `.agents/skills` e corta por orçamento.** `agy --mode plan --sandbox`: sem o symlink,
  nenhuma; com ele, quatro. `meeting-runner` (896 caracteres de descrição) e `agent-instructions-writer` (636) saem
  "excluded due to context budget limits", na disputa com as skills de `~/.gemini/`. [medido]
- **M5 — O Gemini CLI não está instalado**; não medido.
- **M6 — O `brza-workflow` não distribui skill a outro client.** A busca por `.agents/skills` e `codex/skills` no
  repositório não achou nada. [lido]

#### O fluxo pelo Codex

- **M7 — O gatilho natural ativa a skill.** "confere as notas", sem o nome da skill:
  - o Codex leu o `SKILL.md` do `notes-checker`;
  - rodou a busca de `blocks` do `AGENTS.md` e o `check_notes.py --detail`;
  - relatou os achados sem editar.

  112.816 tokens de entrada, 93.184 em cache. [medido]
- **M8 — O Codex segue o `close-task` até o commit.** Pedido "crie a issue … depois fecha a tarefa":
  - leu o `work/README.md` e os dois `SKILL.md`;
  - conferiu o `CLAUDE_CODE_SESSION_ID` (ausente);
  - rodou o `fact_outcome.py --pending`, o checador e o `brza note commit`;
  - relatou fielmente o que barrou.

  497.963 tokens de entrada nos dois turnos, 460.544 em cache. [medido]
- **M9 — O sandbox padrão do Codex barra o commit.** No `workspace-write`, o `git add` falha em
  `.git/worktrees/playground/index.lock` com `Operation not permitted`, mesmo com o clone em `--add-dir`. Com a
  configuração de Anderson (`approval_policy = "on-request"`), cada `brza note commit` pede escalada. O modo sem
  sandbox foi barrado pelo classificador da sessão, e o commit foi rodado pela sessão com o comando e o ambiente do
  Codex. [medido]
- **M10 — A identidade do commit não é a da norma.** Sem `GIT_AUTHOR_*` no ambiente, o commit sai com o `user.email`
  do repositório, `240569289+brz-anderson@users.noreply.github.com`, e não com o `brz.anderson.pereira@gmail.com` que o
  `CLAUDE.md` fixa pelo `env`. [medido]
- **M11 — A tarefa do Codex não é medida.** O evento `task` sai com `session_id: null`, e o worklog fica sem a seção
  `## Custo da tarefa`. [medido]

### O código e a norma (os consultores, 2026-11-09)

Lidos e rodados por dois `designer`, só leitura, contra `brza-workflow@8eb989a`. Os caminhos de código são do
`~/Projects/brza-workflow`.

#### O `brza sync` e o symlink (D1)

- **T1 — O sync lê o núcleo pela árvore do commit e só prevê os modos `100644` e `100755`.** `bin/brza-sync:115`,
  `:119-129`. [lido]
- **T2 — O `apply` grava todo caminho com `write_bytes`.** `bin/brza-sync:326-331`. [lido]
- **T3 — Hoje, um symlink no `core/` chega ao workspace como arquivo `100644` com o texto do alvo.** Na sonda, o
  `.agents/skills` saiu com `is_symlink False` e o conteúdo `../.claude/skills`. [rodado]
- **T4 — Com o link já no disco, o sync seguinte quebra.** `SyncError … [Errno 21] Is a directory`; o
  `read_bytes` só trata `FileNotFoundError` (`bin/brza-sync:153-159`). O mesmo acontece com um diretório real no
  lugar. [rodado]
- **T5 — Com o link pendurado, o sync escreve através dele** e cai em `NotADirectoryError`. [rodado]
- **T6 — O lock guarda `sha256:<hex>` por caminho**, e o digest do texto do alvo cabe nele sem mudar o formato.
  `core/.claude/hooks/brza_root.py:648-651`, `:674-676`. [lido]
- **T7 — O `commit_and_push` decide o que existe por `Path.exists()`**, que segue o link. `bin/brza-sync:429-432`.
  [lido]
- **T8 — O symlink relativo resolve no worktree e mostra as skills da branch.** Num repositório de teste, o worktree
  `workstream/playground` listou a `meeting-runner`, que só a branch tem. A camada 2 é um `git merge`
  (`bin/brza-note:1576-1584`). [rodado]
- **T9 — O `core.symlinks` não está configurado em nenhum dos quatro repositórios**, e o padrão do git 2.54.0 é
  `true`. [rodado, doc]

#### A identidade (D2)

- **T10 — O `AGENTS.md`, o `CLAUDE.md` e o `work/README.md` moram no `core/`**, e o lock do workspace os segue
  (`.brza/core.lock:31-32`). A frase que a R3.3 tira está em `core/AGENTS.md:72-73`. O `README.md` do workspace
  (`:57`) e o molde `templates/README.md:48` também citam o `env`. [lido]
- **T11 — A fonte da identidade é o `[author]` do `.brza/workspace.toml`**
  (`/Users/andepb/Projects/brza-workspace/.brza/workspace.toml:12-15`). É de onde o `env` do `settings.json` nasce
  (`templates/.claude/settings.json:4-7`). [lido]
- **T12 — O `brza doctor` só confere, nunca grava.** Ele aponta o `brza install` como conserto
  (`packages/client/bin/brza-doctor:2`, `:153`, `:213`). A conferência de identidade dele mede o `git var`, que o `env`
  mascara dentro do Claude (`:56-100`). [lido]
- **T13 — O `.git/config` hoje:**
  - o do workspace tem o noreply, e o do `brza-studio` já tem o gmail;
  - os worktrees leem o `.git/config` do checkout principal;
  - o `extensions.worktreeConfig` está desligado.

  [rodado]
- **T14 — O código se acha pelo `brza_root.code_path`** (`brza_root.py:363-372`). O `runtime.STUDIO` cai em
  `~/Projects/brza-studio` mesmo sem `[code]` (`bin/brza_runtime.py:40-41`). [lido]
- **T15 — O `brza init` não grava o `.git/config`**: passa a identidade só pelo `env` do commit inicial
  (`bin/brza-init:324-329`). [lido]

#### O servidor e o motor (D3–D6)

- **T16 — O chamador é o header `X-Brza-Session` e, sem ele, o argumento `caller`.** O gate existe para gasto, e quem
  o aprova é o mesmo chamador. `packages/mcp/brza_mcp/tools.py:195-199`, `:343-354`. [lido]
- **T17 — O daemon está de novo carregado sem processo** (`launchctl list`, pid `-`). O `KeepAlive` só religa em saída
  com erro (`launchd.py:56`), e o plist só leva `HOME`, `PATH`, `BRZA_WORKSPACE`, `BRZA_HOME` e `BRZA_MCP_PORT`. [rodado,
  lido]
- **T18 — Nenhum client tem o servidor configurado nem manda o `X-Brza-Session`**: o `~/.codex/config.toml` não tem o
  `brza-orchestrator`. [rodado]
- **T19 — O `brza note commit` aceita qualquer caminho dentro da raiz-alvo**, e o id de sessão do `task` sai de
  `CLAUDE_CODE_SESSION_ID` ou `GROK_SESSION_ID`. Sem id, a `## Custo da tarefa` não se escreve
  (`bin/brza-note:722-728`, `:858-860`, `:1598-1625`). [lido]
- **T20 — No log real, 7 eventos `task` de chats `codex_…` de 2026-11-09 têm commit e `session_id` null**: o M11
  acontece fora da sonda. [rodado]
- **T21 — O PLN-018 fechou, mas a linha `turn` do Codex não se grava.** O `~/.codex/hooks.json` não chama o
  `runtime_turn.py`. No shell de ferramenta do Codex, `CODEX_THREAD_ID` é igual a `CODEX_SESSION_ID`, e o processo do
  hook não tem nenhuma das duas (`PLN-018-plan.md:166-169`). [rodado, lido]
- **T22 — A R1.1 do PLN-012 recusou o início e fim explícitos de tarefa como forma principal.** A tarefa começa no
  primeiro prompt depois do marco anterior (`PLN-012-plan.md:96-103`). [lido]
- **T23 — O motor e o servidor reduzem o índice por regras diferentes**: o maior `ts` (`brza-note:1039-1054`) e a
  última linha (`queue.py:301-314`). Hoje dão o mesmo nos 194 ids. O estado vigente tem 116 KB, e a forma enxuta dos
  abertos, 41 KB. O `brza note ls` leva 0,17 s, não tem `--json` e só lista issue e decisão. [rodado, lido]
- **T24 — Os transcripts guardam a fala de quem pediu**:
  - **no Claude,** a resposta do `AskUserQuestion` fica em `toolUseResult.answers`;
  - **no Codex,** o rollout tem o id no nome, e a fala é o `response_item` com `role: user`, sendo que o primeiro traz o
    `AGENTS.md` injetado.

  [rodado]
- **T25 — O push pelo daemon depende de a chave `personal`, que tem senha, estar no agente.** O launchd tem o
  `SSH_AUTH_SOCK`. Depois de um reboot, o push pode falhar até uma sessão usar a chave. [rodado, inferido]

## D1 — O `.agents/skills` chega a cada workspace como symlink — `core/.agents/skills`, `bin/brza-sync`

- **Origem:** R3.1.
- **Contexto:** o Codex e o Antigravity só leem `.agents/skills` (M1, M2, M4). O sync de hoje não leva symlink (T3) e
  quebra no sync seguinte (T4).

### Como fica

**O link no núcleo**, commitado no `brza-workflow` com modo `120000`: `core/.agents/skills -> ../.claude/skills`.
- No workspace, ele chega a `.agents/skills`.
- Nos worktrees, chega pelo merge da camada 2 e resolve para o `.claude/skills` da branch (T8).

**O `brza sync` trata o modo `120000`:**

```python
LINK = '120000'


def disk_bytes(root: Path, path: str) -> Optional[bytes]:
    """O que o workspace tem em `path`, na forma em que o git guarda: o alvo do link sem segui-lo, os bytes do arquivo,
    ou None."""
    target = root / path
    if target.is_symlink():
        return os.readlink(target).encode('utf-8')
    return read_bytes(target)


# plan_sync: o link não passa pelo render_file; diretório real no lugar do link é recusa (R5.1)
# apply: nunca escreve através de um link (T5)
if target.is_symlink():
    target.unlink()
if mode == LINK:
    os.symlink(data.decode('utf-8'), target)
else:
    target.write_bytes(data)

# commit_and_push: os.path.lexists no lugar de Path.exists (T7)
```

- **O lock** guarda o digest do texto do alvo (T6).
- **O `report`** escreve `escrito:   .agents/skills -> ../.claude/skills`.
- **A docstring do `brza-sync`** ganha a regra do link.

**A norma** (R5.2), no `core/AGENTS.md`:
- **A lista da `master`** (`:35-36`) ganha o `.agents/`.
- **A seção "O ferramental vive no escopo do projeto ou do workstream"** (`:84-88`) ganha:

> **As skills moram em `.claude/skills/`, e o `.agents/skills` é um link para lá**, que o núcleo traz: o Codex e o
> Antigravity leem só o `.agents/skills`, e o Cursor e o Claude Code, o `.claude/skills`. O link é relativo, e no
> worktree de um workstream mostra também as skills que só a branch tem. Skill nova vai ao `.claude/skills/`, nunca ao
> `.agents/`.

### O teste que falha antes

Em `tests/cli/test_brza_sync.py`, com um ajudante `flow_link(path, target)`:

| Teste | Por que falha hoje |
| :-- | :-- |
| `test_a_symlink_of_the_core_arrives_as_a_symlink_with_the_target_digest_in_the_lock` | chega como arquivo `100644` (T3) |
| `test_a_synced_symlink_is_in_sync_the_second_time` | `Is a directory` (T4) |
| `test_a_real_directory_in_place_of_the_link_is_refused_and_kept_even_with_force` | `SyncError` de leitura (T4) |
| `test_a_link_to_another_target_is_refused_and_force_replaces_it` | quebra na leitura (T4) |
| `test_the_sync_never_writes_through_a_dangling_link` | `NotADirectoryError` (T5) |
| `test_layer_two_brings_the_link_and_the_workstream_sees_its_own_skill` | o worktree recebe arquivo |

E em `tests/cli/test_brza_scripts.py`, `test_the_core_carries_the_agents_skills_link`.

### Fora deste item

- **O `brza-studio` não recebe o link**, porque a R3.1 fala de workspace. Reabre se o Codex trabalhar no código.
- **Máquina com `core.symlinks=false`** receberia o link como arquivo (T9). Nenhuma foi medida.

### Em aberto

R5.1 (o `.agents/skills` que não é o link) e R5.2 (onde vai a norma).

**Estimado pelo consultor:** 2 h. A R3.1 apresentou ~1 h, antes de se saber que o sync não leva symlink.

## D2 — A identidade da norma no `.git/config` — `bin/brza-install`, `packages/client/bin/brza-doctor`

- **Origem:** R3.3.
- **Contexto:** fora do Claude Code, o commit sai com o noreply (M10). O doctor mede o `git var`, que o `env` mascara,
  e não grava (T12).

### Como fica

**A fonte é o `[author]` do manifesto** (T11). O `env` do `settings.json` fica como está.

**Quem grava** (R5.3, recomendado): o `brza install --identity`. O nome da flag é escolha do consultor.

```python
IDENTITY = (('user.name', 'name'), ('user.email', 'email'))


def identity_repos(root: Path, manifest: dict) -> list[Path]:
    """O workspace e o código dele nesta máquina, pelo brza_root.code_path (T14). Os worktrees leem o .git/config do
    checkout principal e não entram na lista (T13)."""


def set_identity(dry_run: bool):
    """Grava o [author] do manifesto no .git/config do workspace e do código. Valor diferente: escreve e mostra
    `antigo -> novo` (R5.4)."""
```

**O doctor ganha a conferência `config`**, ao lado da `identidade`:
- lê o `git config user.name`/`user.email` do workspace e do código — o que um commit sem o `env` usa — e compara com
  o `[author]`;
- a divergência é `ERRO`, com o conserto `brza install --identity`;
- a docstring perde "num terminal aberto sem eles, as duas saem em erro".

**O `brza init`** chama o `set_identity` depois do commit inicial (R6.1, recomendado).

**A norma**, no `core/` (T10). O `core/AGENTS.md:71-74` passa a dizer:

> **A identidade está no `.git/config` dos dois**, que os worktrees compartilham: o `brza install --identity` a grava do
> `[author]` do `.brza/workspace.toml`, e o `brza doctor` confere. Assim o commit sai certo em qualquer client e no
> terminal; o runtime que também a põe no ambiente, como diz o adaptador dele, só a repete.

O `core/CLAUDE.md:48-55` vira "A identidade é a do `{{author.login}}`, também pelo `env`":

> No Claude Code, o `env` vence o ambiente que a sessão herde e o `.git/config`; fora dele, vale o `.git/config`. O
> `git var GIT_AUTHOR_IDENT` confere a sessão, e o `brza doctor`, os dois.

O `core/work/README.md:197-198` e o `templates/README.md:48` acompanham. O `README.md` do workspace (`:57`) é edição
local, na `master`.

### O teste que falha antes

- **Em `tests/cli/test_brza_install.py`:** `test_identity_writes_the_author_in_the_workspace_and_the_code`,
  `…_shows_the_old_value_and_overwrites_it`, `…_dry_run_writes_nothing`,
  `…_without_code_in_the_manifest_touches_only_the_workspace` e `…_from_a_worktree_writes_the_shared_config`.
- **Em `tests/cli/test_brza_doctor.py`:** `test_config_divergente_e_erro_que_manda_o_install_identity`,
  `test_config_certo_e_ok_mesmo_com_o_env_mascarando`, e o `config` na lista de `test_tudo_certo_sai_0…`.
- **Com a R6.1 na primeira opção:** `test_init_writes_the_author_in_the_git_config`.

### Em aberto

R5.3 (quem grava), R5.4 (o valor divergente) e R6.1 (o `brza init`).

**Estimado pelo consultor:** 2 h. A R3.3 apresentou ~1 h, antes de se saber que o doctor não grava.

## O padrão comum dos verbos (D3–D6)

- **O verbo chama o CLI em subprocesso**: `brza note <sub> … --json`, no cwd do chamador, com timeout de 120 s.
  - O motor ganha `--json` nos subcomandos que o verbo usa, e esse JSON é o contrato.
  - A reserva da skill é o mesmo comando, sem `--json`.
  - A raiz-alvo e a recusa do cwd estranho seguem o motor.
- **A sessão é declarada pelo client** num argumento, `session: {runtime, id}`, com o `id` lido no shell
  (`$CLAUDE_CODE_SESSION_ID`, `$CODEX_THREAD_ID`, `$GROK_SESSION_ID`).
  - O header não leva o id do Codex, e nenhum client manda header (T18).
  - Quem declarar um id falso só erra o carimbo da medição.
  - O `X-Brza-Session`, quando vier, vira o `chat_id`.
- **Nenhum dos quatro usa o gate do `dispatch`**: lá, quem aprova é o próprio chamador (T16). A proteção é invariante:
  - caminho só nas pastas de nota;
  - branch `workstream/*`;
  - o checador do motor;
  - a conferência da frase (D6).
- **A classificação para o proxy remoto** (R8.2): um atributo `remote` por ferramenta.

| Verbo | Escreve | `remote` (recomendado) |
| :-- | :-- | :-- |
| `index_query` | nada | `read`, com `refresh` forçado a `false` |
| `start_task` | só o marco, se existir | `read`: só o briefing |
| `close_task` | git e medição | `local` |
| `decision_record` | git e a decisão | `local` |

## D3 — `close_task` — `packages/mcp/brza_mcp/notes.py`, `bin/brza-note commit --session --runtime --json`

- **Origem:** R3.2, a crítica 8 da R1, M9 e M11.
- **Contexto:** no Codex, o sandbox barra o `.git` (M9), e o `task` sai sem sessão (M11, T20). O servidor commita fora
  do sandbox, o que é ganho e risco ao mesmo tempo.

### As alternativas — a entrada (R6.2)

#### A1 — Os caminhos dos arquivos que o client já escreveu (recomendada)

- **Custo:** nenhum além do adaptador. Diverge da redação do critério de aceite ("recebe o worklog estruturado").
- **Se paga:** agora. O servidor só commita o que o client já pôde escrever, então o client `read-only` não ganha
  escrita pelo servidor (M9).
- **Reabre:** um client sem disco, o remoto.

#### A2 — O texto Markdown inteiro no argumento

- **Custo:** ~1 h. Um client `read-only` passa a escrever nota pelo servidor.
- **Se paga:** só com client sem disco, fora de escopo.

#### A3 — Os campos estruturados (frontmatter e seções)

- **Custo:** ~3 a 4 h, uma segunda forma do worklog no motor, e um schema que muda a cada mudança da forma.
- **Se paga:** nunca, enquanto o checador não exigir seções. Ele barra frontmatter, link e nome, e não o corpo.

### Como fica (A1)

```json
{"type": "object", "required": ["cwd", "paths", "message", "session"], "properties": {
  "cwd": {"type": "string", "description": "o diretório absoluto da sessão"},
  "paths": {"type": "array", "items": {"type": "string"}, "minItems": 1,
            "description": "relativos ao cwd; ao menos um worklog de hoje em work/worklogs/"},
  "message": {"type": "string"},
  "session": {"type": "object", "required": ["runtime", "id"], "properties": {
    "runtime": {"enum": ["claude", "codex", "grok", "antigravity", "cursor"]}, "id": {"type": "string"}}},
  "until": {"type": "string", "description": "HH:MM ou ISO; só com runtime claude"}}}
```

A saída repassa o `--json` do motor:

```json
{"commit": "abc1234", "branch": "workstream/playground", "pushed": true,
 "index": [{"id": "PLN-020", "event": "changed"}],
 "task": {"session_id": "019a…", "runtime": "codex", "chat_id": "codex_…", "worklogs": ["…"], "measured": false},
 "warnings": ["aviso: sem priority: …"]}
```

O adaptador, na ordem:
1. **O `cwd`:** absoluto, existe, e o motor aceita.
2. **Os `paths`:**
   - cada um, resolvido, cai em `work/`, `plans/`, `wiki/`, `memory/` ou `.claude/agent-memory/`, as cinco pastas da
     trava do `/compact`;
   - pelo menos um é um worklog de hoje;
   - todos existem.
3. **O lock:** um por raiz-alvo.
4. **O motor:** `brza note commit <paths> -m <message> --session <id> --runtime <rt> [--until …] --json`.
5. **A saída:** 0 devolve o JSON; 1 devolve `isError` com a saída do motor.

**O motor ganha:**
- `--session` e `--runtime`, que vencem as variáveis de hoje, e o campo `runtime` no evento `task`;
- `--json`;
- a seção "Não medida — sessão sem turno medido" no worklog com `--session` e sem linha `turn` (R6.3).

**O push pelo daemon:** quando falha, o commit e o marco já estão gravados, e o verbo devolve o comando para repetir
o push (T25).

**A skill `close-task`, revista pela `skill-creator`:**
- usa o id de sessão do runtime;
- chama o `close_task` quando o servidor responde;
- senão, chama o `brza note commit … --session … --runtime …`.

### Em aberto

R6.2 (a entrada), R6.3 (a sessão fora do Claude), R6.4 (a identidade no motor) e R8.3 (o daemon e os clients).

**Estimado pelo consultor:** 7,5 h.

## D4 — `start_task` — `packages/mcp/brza_mcp/notes.py`, `bin/brza-note brief --json`

- **Origem:** R3.2 e a crítica 7 da R1.
- **Contexto:** o valor está no briefing, num client que não carrega a memória do workstream sozinho, e no marco de
  início na medição.

### As alternativas — o marco (R7.1)

#### A1 — O briefing agora, sem gravar; o marco espera a linha `turn` do Codex (recomendada)

- **Custo:** ~4 h. Diverge da redação do critério de aceite, que pede o marco.
- **Se paga:** agora, no Codex e no Antigravity, que não leem o `memory/` do workstream.
- **O argumento:** no Claude, o corte implícito e o `--until` já separam as tarefas (T22). No Codex, a linha `turn` não
  se grava (T21), então o marco cortaria zero turnos. A condição que a R3.2 deu para o marco ainda não se cumpriu.

#### A2 — O briefing e o marco, num evento `task_start`

- **Custo:** ~7 h, com +2,5 h no `summarize_measurements.py`, no motor e nos testes. Reabre a forma que a R1.1 do
  PLN-012 recusou (T22).
- **Se paga:** no Codex, depois do hook do PLN-004; no Claude, quase nunca.

### Como fica (A1)

```json
{"type": "object", "required": ["cwd"], "properties": {
  "cwd": {"type": "string"},
  "plan": {"type": "string", "pattern": "^PLN-\\d{3}$"},
  "step": {"type": "string"},
  "session": {"type": "object", "properties": {"runtime": {"type": "string"}, "id": {"type": "string"}}}}}
```

A saída do `brza note brief [--plan PLN-NNN] --json`, um subcomando novo:

```json
{"workstream": "playground", "branch": "workstream/playground",
 "blocks": [{"id": "PLN-011", "workstream": "studio", "status": "open", "title": "…", "path": "…"}],
 "plan": {"id": "PLN-020", "status": "open", "phase": "interview", "path": "…", "retomar": "…"},
 "memory": {"path": "memory/MEMORY.md", "index": "…"},
 "today_worklogs": ["…"], "dirty": ["…"]}
```

- **`blocks`:** do índice da `master`, com o `status` aberto. Hoje dá o mesmo que a varredura do `AGENTS.md` (T23).
- **`plan.retomar`:** a linha `Retomar` do plano.
- **`memory`:** só o `MEMORY.md`.
- **O tamanho:** ~2 a 4 KB.

**Com a A2,** o motor ganha também `brza note start`, que grava o evento `task_start`. O `task_segments` passa a
começar nele, e sem ele o corte de hoje segue igual.

**Quem aciona o verbo** é a R7.2.

### Em aberto

R7.1 (o marco) e R7.2 (quem aciona).

**Estimado pelo consultor:** 4 h com a A1, ou 7 a 9,5 h com a A2.

## D5 — `index_query` — `packages/mcp/brza_mcp/notes.py`, `bin/brza-note ls --json`

- **Origem:** R3.2, a sugestão da R1.
- **Contexto:** a coordenação fora do Claude Code quer os planos, as issues e as decisões de todos os workstreams sem
  varrer as branches.

### As alternativas — a fonte (R7.3)

#### A1 — O `brza note ls` ganha `--json`, os filtros e a página, e o verbo o chama (recomendada)

- **Custo:** ~4 h.
- **Se paga:** agora: uma redução só, e o `ls` do terminal ganha os mesmos filtros.

#### A2 — O verbo lê com o `git_index_reader` e o `reduce_index` do `queue.py`

- **Custo:** ~2,5 h e uma segunda redução, que pode divergir (T23).
- **Se paga:** nunca, pela restrição de uma fonte só.

### Como fica (A1)

```json
{"type": "object", "properties": {
  "kind": {"type": "array", "items": {"enum": ["plan", "issue", "review", "decision"]}},
  "status": {"type": "array", "items": {"enum": ["open", "in_progress", "in_review", "done", "dropped"]}},
  "workstream": {"type": "string"},
  "id": {"type": "string"},
  "blocks": {"type": "boolean"},
  "text": {"type": "string"},
  "fields": {"enum": ["slim", "full"], "default": "slim"},
  "limit": {"type": "integer", "minimum": 1, "maximum": 200, "default": 50},
  "offset": {"type": "integer", "minimum": 0, "default": 0},
  "refresh": {"type": "boolean", "default": false}}}
```

- **A saída:** `{"total", "offset", "limit", "next_offset", "source", "fetched", "items": [...]}`.
- **`slim`:** `id`, `kind`, `status`, `workstream`, `title`, `priority` e `path`, ~15 KB por página.
- **O `status` padrão:** os abertos.
- **Só leitura:** o verbo não toca disco nem medição.
- **O que fica de fora:** o `reduce_index` do `queue.py`, que é uma segunda redução, e alinhá-lo é pendência de outro
  item.

**Estimado pelo consultor:** 4 h.

## D6 — `decision_record` — `packages/mcp/brza_mcp/notes.py`, `bin/brza-note decision`

- **Origem:** R3.2, a sugestão da R1, com `confirmation_quote`.
- **Contexto:** a decisão nasce como proposta, e só a frase explícita de Anderson a fecha. Mensagem de subagente ou de
  outra sessão nunca é a confirmação (`AGENTS.md`, "Decisão é confirmação explícita").

### O que se consegue conferir

- **A frase no transcript da sessão declarada** (T24):
  - **no Claude,** nas mensagens de quem pediu e nas respostas do `AskUserQuestion`;
  - **no Codex,** nas mensagens `user` do rollout, sem a primeira.
- **A frase literal no arquivo da decisão**, e o checador barra o `done` sem `decided` e `decided_by`.
- **O que não se consegue:**
  - saber quem digitou;
  - conferir sem transcript — Grok, Antigravity e Cursor;
  - barrar o Claude com Bash livre, que pode alterar o próprio transcript.

### As alternativas — a conferência (R7.4)

#### A1 — O motor procura a frase no transcript, e sem achar recusa o `done` (recomendada)

- **Custo:** ~2,5 h. Do Antigravity, do Grok e do Cursor, a decisão só sai `open`.
- **Se paga:** na primeira decisão que um subagente ou outra sessão tentar gravar como `done`.

#### A2 — A frase como o client a declara, sem conferência

- **Custo:** nenhum.
- **Se paga:** nunca, contra o erro que a norma quer evitar.

#### A3 — O gate do `dispatch` para o `done`

- **Custo:** ~1,5 h.
- **Se paga:** nunca, porque quem aprova é a mesma sessão (T16).

### Como fica (A1)

`brza note decision <caminho> [--quote "<frase>"] --session <id> --runtime <rt> [-m …] [--json]`. O comando confere a
nota e segue o caminho do `commit`. O `brza note commit` de uma decisão continua sem conferência, como hoje.

```json
{"type": "object", "required": ["cwd", "path", "session"], "properties": {
  "cwd": {"type": "string"},
  "path": {"type": "string", "description": "work/decisions/<slug>.md, já escrito pelo client"},
  "confirmation_quote": {"type": "string", "description": "a frase literal de Anderson; obrigatória com status done"},
  "session": {"type": "object", "required": ["runtime", "id"], "properties": {
    "runtime": {"enum": ["claude", "codex", "grok", "antigravity", "cursor"]}, "id": {"type": "string"}}},
  "message": {"type": "string"},
  "worklog": {"type": "string"}}}
```

- **`status: open`:** sem frase.
- **`status: done`:**
  - a frase está literal no arquivo e no transcript da sessão, com o espaço normalizado;
  - sem achar, `isError`, com o pedido de gravar como `open`.
- **As palavras da norma** ("decidido", "fechado", "pode aplicar") não se exigem: são exemplos, e a resposta do
  `AskUserQuestion` vem como o rótulo da opção.
- **Onde mora a frase** é a R8.1.

**Estimado pelo consultor:** 6 h.

## A estimativa pelas recomendadas

| Item | Horas |
| :-- | --: |
| D1 | 2 |
| D2 | 2 |
| D3 | 7,5 |
| D4 (A1) | 4 |
| D5 | 4 |
| D6 | 6 |
| Total | 25,5 |

A ordem sugerida pelo consultor para os verbos é D5, D3, D6 e D4: o D5, só de leitura, prova o padrão do adaptador
antes da escrita. Os números vão às linhas `Estimado` quando os passos forem planejados.
