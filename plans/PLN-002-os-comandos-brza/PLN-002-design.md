# PLN-002 — Desenho

O desenho dos sete comandos e da base comum. Cada item mostra a interface como vai para o disco: a ajuda do script, que
é a docstring dele, e as assinaturas do que muda no `brza_runtime.py`. O trecho é instrução, não fonte: fechado o
passo, o disco é a verdade, e a divergência vira um desvio `X`.

## O que este desenho assume

- **Issue:** os scripts se chamam `brza-<sub>`, moram em `scripts/brza/` do `brza-workspace` e rodam sozinhos; o
  `brza <sub>` digitado chega a eles pelo despacho do P0 (`brza-studio@9a81e65c852`).
- **Issue:** os nomes são `tree` e `test`, porque `worktree` e `check` colidem com o CLI do app.
- **Issue:** o `brza_runtime.py` só cresce; os nomes de hoje (`cli_command`, `user_data`, `runtime_file`, `brza`, `rpc`,
  `BrzaError`, `WORKSPACE`, `LOCAL_BIN`) ficam como estão.
- **R1.2, R2.4, R3.3:** nenhum comando toca o checkout principal do `brza-studio`; o que precisa de código parte de um
  worktree da `origin/master`, depois de um `git fetch origin`.
- **R3.4, R6.1:** o código comum — o envio ao chat, o checkout do `brza-studio` e o worktree — mora no runtime.
- **R4.4:** primeiro o P1, depois o P2; o P3 ao P6 em paralelo; o P7 quando a combinação com a 2d fechar; o P8 por último.
- **R5.3:** cada passo roda numa sessão `pln-002-pN` do `brza-workspace`, com commit direto na `master`.

## Terreno

Levantado em 2026-10-28 por um subagente Sonnet, só lendo; os fatos que as rodadas usaram estão no "Apresentado antes"
de cada uma, no [PLN-002 — Entrevista](PLN-002-interview.md).

### Os scripts

- **O runtime.** `scripts/brza/brza_runtime.py:15-19` tem as constantes, e não há a do checkout do `brza-studio`; o
  `claude-brza:35-39` a recalcula, com `BRZA_STUDIO`.
- **A duplicação.** `canonicalize` em `brza-run:109-116` e `brza-sessions:82-89`; `send_to_chat` em `brza-run:130-133`
  (com `send_mutation`, `:119-127`) e `brza-sessions:92-100`.
- **O `brza-install`.** Lista fixa (`:24-26`), flag por script (`:82-84`) e `link_command` que recusa link alheio
  (`:42-56`).
- **Os testes.** `python3 -m unittest discover -s scripts/brza/tests` → 21 testes OK em 1,4 s. Carregam cada script com
  `runpy.run_path` (`test_brza_scripts.py:15-19`); os patches de `rpc` estão em `test_brza_sessions.py:62-76` e
  `test_brza_scripts.py:110-113`.

### O `brza-studio`

- **O dev build.** Perfil e portas por worktree (`config/scripts/dev-instance-isolation.mjs:7-18,90-111,196-205`); o
  registro `out/dev-instance.json` com o `runnerPid` (`:137-155,285-298`), que não se apaga ao sair; o runner escala de
  SIGTERM para SIGKILL em 5 s (`config/scripts/run-electron-vite-dev.mjs:593-645`).
- **O seed.** `config/scripts/dev-profile-seed.mjs`: fonte padrão `brza-dev` ou o perfil do app (`:57-63`), falha com
  perfil já semeado (`:126-128`).
- **Os testes.** `config/scripts/run-vitest.mjs` roda sob o bun do `node_modules` do worktree (`:51-60`);
  `check:changed` (`package.json:25`) cai em `origin/main` sem `--base` (`config/scripts/check-changed.mjs:48,64`).
- **O build.** `build:mac` → `config/scripts/build-mac-local.mjs`: a versão leva o `HEAD` de onde roda (`:22-30`), alvo
  `dir` por padrão e `--dmg` opcional (`:83`); sai em `dist/mac-arm64/BrzA Studio.app`.
- **As sessões.** `session.tabs.listAll` (`src/main/runtime/rpc/methods/session-tabs.ts:44-51`), `agentSession.close`
  (`structured-agent-session.ts:147-170`), `session.tabs.close` (`session-tab-close-methods.ts:13-60`, que recusa sem
  `reason`).

## D1 — A base comum — `scripts/brza/brza_runtime.py`, `scripts/brza/brza-install` (P1)

- **Origem:** R3.4, R4.1, R6.1, R7.1; a autoligação e o PATH vêm da `brza-cli-subcomandos`, no P0.
- **Contexto:** o `sessions send`, o `tree`, o `test` e o `app install` precisam do mesmo envio e do mesmo worktree, e
  sete scripts novos não cabem em sete flags.

#### Como fica

O runtime ganha, sem mexer no que existe:

```python
STUDIO = Path(os.environ.get('BRZA_STUDIO') or Path.home() / 'Projects' / 'brza-studio')

def canonicalize(value) -> str: ...            # vindo do brza-run e do brza-sessions, sem mudança
def send_mutation(session_id, text, fence, now_ms, entropy) -> dict: ...
def send_to_chat(session_id: str, text: str): ...

def git(*args, cwd: Path = STUDIO) -> str:
    """Roda o git e devolve o stdout; erro vira BrzaError com o stderr."""

def worktree_add(path: Path, base: str = 'origin/master', branch: str | None = None, fetch: bool = True) -> Path:
    """`git fetch origin` (se fetch), e `git worktree add` em `path` de `base`; sem `branch`, sai detached."""

def install_offline(path: Path):
    """`pnpm install --offline --frozen-lockfile` em `path`; falha vira BrzaError que diz o comando online."""

def worktree_remove(path: Path):
    """`git worktree remove` sem --force; usado no worktree temporário, que nasce limpo."""
```

O `brza-run` e o `brza-sessions` passam a importar os três primeiros e mantêm os nomes no módulo, para os testes; os
testes passam a fazer o patch em `brza_runtime.rpc`.

O `brza-install` liga todo `brza-*` executável de `scripts/brza/`, inclusive a si mesmo. O `claude-brza` segue só pelo
`--chat-command`, porque mexe no override:

```text
brza install                  mostra o estado: cada link brza-* e o agentCmdOverrides.claude do app
brza install --all            liga em ~/.local/bin todo brza-* de scripts/brza/, inclusive o brza-install
brza install --chat-command   liga o claude-brza e o põe em agentCmdOverrides.claude
brza install --run | --sessions   atalhos de hoje, que ligam um só
--dry-run                     diz o que faria, sem fazer
```

O primeiro `--all` roda com o caminho inteiro, `scripts/brza/brza-install --all`, porque o link dele ainda não existe.

## D2 — O `brza tree` — `scripts/brza/brza-tree` (P2)

- **Origem:** R1.1 a R1.4, R5.1, R7.1.
- **Contexto:** 9 worktrees em 2 dias, o node_modules por symlink que derrubou o checkout principal e dois órfãos em
  disco.

#### Como fica

```text
brza tree <nome> [--type feat|fix|docs|chore] [--base <ref>] [--chat <sessão>]
    cria ~/Projects/brza-studio/.worktrees/<nome> na branch <tipo>/<nome> (tipo padrão feat), a partir de
    origin/master depois de git fetch origin, ou de --base; instala com pnpm install --offline --frozen-lockfile e
    imprime o caminho. --chat abre a sessão no worktree pelo brza sessions --checkout.
brza tree --rm <nome> [--force]
    remove o worktree e a branch quando o HEAD é ancestral da origin/master e o worktree está limpo. A branch sem
    commit próprio pede --force, porque "na origin/master" vale também para ela. Diretório em .worktrees/ sem registro
    no git worktree list é órfão: remove com --force, depois de listar o que há nele.
brza tree --list
    os worktrees de .worktrees/, cada um com a branch, os commits à frente da origin/master, se está limpo e os órfãos.
```

- **Saídas:** 0 feito; 1 recusado (sujo, não mergeado, órfão sem `--force`); 2 uso errado.
- **O install offline que falha** não apaga o worktree: imprime o caminho e o `pnpm install --frozen-lockfile` a rodar.

## D3 — O `brza dev` — `scripts/brza/brza-dev` (P3)

- **Origem:** R2.1 a R2.3, R7.1.
- **Contexto:** o dev build foi subido e encerrado à mão 4 ou mais vezes, e há 6 conferências pendentes no PLN-001.

#### Como fica

```text
brza dev [<worktree>] [--background] [--no-seed] [--reset]
    sobe o dev build do worktree (padrão: o diretório atual, que tem de ser um worktree do brza-studio). Semeia o perfil
    com pnpm dev:seed-profile só quando ele está vazio; --reset apaga o perfil do worktree antes, e --no-seed pula.
    Visível por padrão; --background põe ORCA_BACKGROUND_LAUNCH=1. Recusa se já há um build vivo no worktree.
brza dev --stop [<worktree>]
    lê o runnerPid de <worktree>/out/dev-instance.json, confere que o processo vive e é o runner, manda SIGTERM e espera
    até 10 s. Pid morto ou de outro processo: diz que não há build e sai 0.
brza dev --status [<worktree>]
    o pid, as portas e o userData do build, ou "parado".
```

- **Fora de escopo:** dois builds no mesmo worktree (R2.2).

## D4 — O `brza test` — `scripts/brza/brza-test` (P4)

- **Origem:** R2.4, R3.1, R7.3.
- **Contexto:** o baseline foi refeito à mão 3 vezes, e o `--base` foi esquecido.

#### Como fica

```text
brza test [<worktree>] [--no-baseline] [-- <caminhos de teste>]
    no worktree (padrão: o atual), roda o vitest pelo node config/scripts/run-vitest.mjs run --config
    config/vitest.config.ts, nos testes dos arquivos alterados contra origin/master (ou nos caminhos dados), e o
    pnpm check:changed --base=origin/master. Se algum teste falha, cria um worktree temporário da origin/master
    (worktree_add sem branch, install_offline), roda nele só os arquivos que falharam e remove no fim.
```

- **O relatório** separa três grupos: "passou", "falha nova" (passa na master) e "já falhava na master". Sai com 1 só
  com falha nova ou com o `check:changed` vermelho.
- **O teste alterado** é o arquivo `*.test.ts` alterado e o `*.test.ts` vizinho de cada fonte alterado. O que não tem
  vizinho entra no relatório como "sem teste".

## D5 — O `brza app install` — `scripts/brza/brza-app` (P5)

- **Origem:** R3.2, R3.3, R8.1, R8.2; a reinstalação e a troca dos textos vêm do P0.
- **Contexto:** a instalação foi feita à mão, e o despacho do P0 só chega ao app instalado por ela.

#### Como fica

```text
brza app install [--from <checkout>] [--dmg] [--yes] [--clean]
    constrói o app de um worktree temporário da origin/master (ou de --from), com pnpm build:mac [--dmg], apaga o
    /Applications/BrzA Studio.app antigo e copia dist/mac-arm64/BrzA Studio.app no lugar com ditto. Pergunta antes de
    substituir; com o app aberto, recusa (saída 2) sem --yes. --dmg copia o .dmg para ~/Downloads. --clean apaga o
    dist depois. O worktree temporário sai no fim; só o ditto que falha o deixa, com o ditto a repetir.
```

- **O `.dmg` vai para `~/Downloads`** (R8.1), porque o worktree temporário sai com ele.
- **Apaga e copia, e não `ditto` por cima** (R8.2): o `ditto` mescla, e o arquivo que saiu da versão nova quebraria a
  assinatura ad hoc.
- **O app aberto** é todo processo de `/Applications/BrzA Studio.app/Contents/`, menos o comando e os pais dele, porque
  o `brza app install` digitado no app chega ao script por um processo do app.

- **A conferência do P0**, depois da primeira instalação: `brza sessions --help` responde do chat e do terminal.
- **A troca dos textos:** `brza-install`/`brza-run` viram `brza install`/`brza run` na ajuda dos scripts e no
  `CLAUDE.md` (linha 33).

## D6 — O `brza note` — `scripts/brza/brza-note` (P6)

- **Origem:** R4.3, R7.2.
- **Contexto:** 10 commits de worklog e 3 issues em 2 dias, com o esqueleto e o commit feitos à mão.

#### Como fica

```text
brza note new worklog <assunto> [--scope workspace,brza-studio]
    cria work/worklogs/AAAA-MM-DD-<assunto>.md com o esqueleto abaixo e imprime o caminho; recusa se existe.
brza note new issue <assunto> [--scope …] [--priority low|medium|high]
    cria work/issues/<assunto>.md, com status: open e opened de hoje.
brza note commit <caminho>… -m <mensagem>
    roda o check_notes.py (sai se há erro), git add dos caminhos, commit, git pull --rebase e push na master;
    --no-push para no commit.
```

O esqueleto do worklog segue os de 2026-10-28 e o `work/README.md` (`:140-149`, `:297-303`):

```markdown
---
scope:
  - workspace
---

# <H1 a escrever>

O pedido de Anderson, em AAAA-MM-DD, na sessão `<$CLAUDE_SESSION_NAME, ou a escrever>`: "<o pedido>".

## O que se fez

## O que ficou

## Fora do workspace
```

- **O `## Fora do workspace`** sai vazio e é apagado quando não há o que registrar; os quatro campos estão no
  `work/README.md`.
- **A issue** leva o frontmatter, o H1 e a seção `## O pedido`.

## D7 — O `brza sessions list|send|close` — `scripts/brza/brza-sessions` (P7)

- **Origem:** R9.1, R9.2, R9.4 e R10.1, na combinação feita pela `pln-002-p7` (PLN-003/R6.1, que reabriu a R5.2).
- **Contexto:** achar, mandar e fechar sessão por nome se repetiu 8 ou mais vezes, e o CLI não fecha chat. O roteador
  do PLN-003 chama o `list`, o `send` e o `close` por nome, e lê o `--json`.

#### Como fica

```text
brza sessions [open] <nome> [--checkout <caminho>] [--prompt …]   o de hoje, sem mudança (R9.2)
brza sessions list [--json]                     os chats do app: nome, título, chat, worktree, estado
brza sessions send <nome> <texto> [--json]      agentSession.send, com queue-if-active
brza sessions close <nome> [--force] [--json]   agentSession.close e session.tabs.close com reason 'user'; sem --resume
```

- **Achar o chat pelo nome (R9.1):** as abas `agent-session` do `session.tabs.listAll`; para cada uma, o
  `agentSession.history` dá o `providerSession.id`, o id da sessão do Claude; o nome é o último `custom-title` do
  transcript `<config>/projects/*/<id>.jsonl`, nos mesmos `config_dirs()` do `running()`. Chat sem `/rename` fica sem
  nome e não é achado pelo `send` nem pelo `close`. Nome ausente ou repetido sai 1, e o repetido lista os chats.
- **O `send` não consulta trava (R10.1):** a trava de retomada foi desligada, e o `send` manda sempre. Quem decide
  acordar uma sessão grande parada é quem chama.
- **O `close` (R9.4):** recusa com saída 1 o chat `working` sem `--force`. Com ele, chama os dois RPCs; o
  `agentSession.close` sozinho deixa a aba no `listAll`. Nada de `--resume` nem de restart.

#### O `--json`, estável para o roteador

```text
list   {"sessions": [{"name": str|null, "title": str, "chat": "claude_…", "claude_session": str|null,
                      "worktree": str, "state": str|null}]}
send   {"sent": true, "name", "chat"}
close  {"closed": true, "name", "chat"}  ·  saída 1: {"closed": false, "name", "chat", "state"}
erro   saída 1: {"error": "<motivo>"}, no nome ausente, no repetido e no app que não responde
```

- **Descartada — o registro nome e id gravado pelo `open`.** O `providerSession.id` do `agentSession.history` e o
  `custom-title` do transcript dão o par sem arquivo novo, também para o chat aberto à mão (R9.1).
- **Descartada — achar pelo título da aba.** O título é o nome do app, do `agentSession.rename`, e não o do `/rename`.
- **Descartada — a trava no `send` (R9.3).** Entrou em `brza-workspace@9daa020` e saiu em `88d8a3a`, com a trava
  desligada (R10.1).

## D8 — O `brza doctor` — `scripts/brza/brza-doctor` (P8)

- **Origem:** R4.2, R7.1.
- **Contexto:** o `git var` foi rodado à mão 5 vezes, e a sessão aberta sem o wrapper sobe sem medição e sem aviso.

#### Como fica

```text
brza doctor [--json]
    ERRO  identidade: git var GIT_AUTHOR_IDENT não é o noreply do brz-anderson
    ERRO  medição: .claude/settings.json sem o measure.py, ou BRZA_WORKSPACE ausente no ambiente
    ERRO  links: algum brza-* de scripts/brza/ sem link certo em ~/.local/bin (o link_state do brza-install)
    ERRO  chat: agentCmdOverrides.claude não é o claude-brza (pelo rpc, quando o app responde)
    AVISO pnpm fora do PATH; perfil brza-dev sem estado; app instalado mais velho que a origin/master
```

- **Saídas:** 1 com algum ERRO, 0 sem. Cada linha diz o que conferiu e, no erro, o comando que conserta.
