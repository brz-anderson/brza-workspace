# PLN-006 — Desenho

Do [PLN-006: O `brza init` monta a norma num workspace do zero](PLN-006-plan.md). Rascunhado pelo `designer` em
2026-10-31 e fechado pelas rodadas R1–R8 do plano. Cada fato e cada custo levam a marca `[id · tipo · confiança]` da
auditoria do PLN-005; a escolha que uma rodada fixou cita a rodada.

## Desenho

### O que este desenho assume

- **R1.1:** o PLN-006 mora no workstream `workspace`.
- **R1.2:** o workspace fica ao lado do repositório de código, como o par `brza-workspace` + `brza-studio`.
- **R1.3:** `brza init` é script determinístico.
- **R1.4:** o workspace acompanha o núcleo por sync.
- **R2.1 / R3.1:** o núcleo mora em `brz-anderson/brza-workflow`, público, sem nada pessoal; o `brza-workspace` é o
  primeiro cliente.
- **R2.2:** placeholders no núcleo, valores no `.brza/workspace.toml`; init e sync renderizam; seção inteiramente local
  vira arquivo local; no `settings.json`, o sync é dono de `hooks`, o init escreve `env` e `enabledPlugins`.
- **R2.3:** núcleo = norma, skills, agents, `brza-note`, `brza_runtime`, `brza-agents`, hooks `measure`,
  `compact_guard`, `fact_audit`; camada do cliente (`brza-sessions`, `claude-brza`, `install`, `doctor`, `run`) como
  pacote opcional; `app`, `dev`, `test`, `tree`, `shot` locais do `brza-studio`; o `resume_guard` sai.
- **R2.4:** a raiz sai do git common dir do cwd; o workspace se reconhece pelo `.brza/workspace.toml`; a
  `BRZA_WORKSPACE` é só override; `claude-brza` e `~/.zshrc` deixam de reconhecer por nome.
- **R3.2:** o CLI roda de um checkout do `brza-workflow` por máquina, ligado em `~/.local/bin` pelo `brza install`; o
  workspace não recebe `scripts/brza`; norma, skills, agents e hooks chegam ao workspace pelo sync.
- **R3.3:** branch padrão e remote no manifesto, `master`/`origin` quando ausentes.
- **R3.4:** `--author-name`/`--author-email`, padrão do `git config --global`; ssh e `gh` só documentados.
- **R4.1:** "Registro em ~/.config/brza": o repositório de código se liga ao workspace por
  `~/.config/brza/workspaces.toml`, arquivo de usuário que vai ao worklog.
- **R4.2:** "Camada local + sync": `app`, `dev`, `test`, `tree` e `shot` em `scripts/brza/` do `brza-workspace`, por
  `brza install --local`; `summarize_measurements` e `fact_outcome` ao workspace pelo sync, em `scripts/`;
  `brza-print` ao pacote do cliente.
- **R4.3 → R5:** o contador "Último PLN usado" sai; entra um índice JSONL na `master` do workspace. R5.1: "Planos,
  Issues, Decisões". R5.2: "Só acrescenta, merge=union": uma linha por evento, estado vigente na última de cada id.
  R5.3: "brza note, automático": `brza note plan-open` reserva o número (maior id + 1) com a linha "criado"; o
  `brza note commit` acrescenta "alterado" na `master` quando o frontmatter muda. R5.4: o coordenador fica numa issue.
- **R4.4:** "@AGENTS.md no CLAUDE.md".
- **R6.1:** `{{tabela.chave}}` por regex, parser TOML próprio. **R6.2:** o sync recusa o arquivo editado, mostra o
  diff e sai com 1; `--force <caminho>` sobrescreve. **R6.3:** segue a branch, com o sha no lock, por `brza sync`.
  **R6.4:** migração em estágios.
- **R7.1:** o registro guarda o par raiz + código, escrito pelo `brza init` e pelo `brza register`, que recusa código já
  ligado a outro workspace. **R7.2:** o índice é `.brza/index.jsonl`. **R7.3:** um campo `description` no frontmatter
  de plano, issue e decisão, obrigatório na nota nova. **R7.4:** a linha do índice chega à `master` por commit sem
  checkout, com 3 tentativas.
- **R8.1:** o id de issue e decisão é `issue:<slug>` ou `decision:<slug>`, com o slug da criação. **R8.2:** as menções
  à Fixfy saem do núcleo. **R8.3:** a medição datada fica no núcleo, como o porquê da regra. **R8.4:** a exceção ao
  índice vai numa decisão nova, sem `superseded_by`.

### Terreno

#### Os hooks e o CLI

- **Os hooks não importam nem chamam o `scripts/brza`.** `measure.py:28-35` importa só a stdlib; `measure.py:87` diz
  "Lógica copiada do scripts/brza/brza-note, sem importá-lo"; `compact_guard.py:27-28` importa o `measure` vizinho;
  `fact_audit.py:41-48` carrega o `measure.py` pelo diretório do próprio arquivo [F2 · lido · 95]. O único texto que
  aponta para o CLI é a mensagem de `compact_guard.py:88`, que manda rodar `brza note commit` [F3 · lido · 92].
- **A cópia duplica a lógica da raiz.** `measure.py:79-80`, `measure.py:88-91` e `measure.py:583-600` (com `"master"`
  literal em `:592`) repetem o `brza_runtime.py:21-23` e o `brza-note:145-169` [F4 · lido · 93].
- **Os hooks sobem no Python 3.9 do sistema; o CLI não.** A suíte `.claude/hooks/tests` roda no `/usr/bin/python3`
  3.9.6 com 176 OK, e os testes chamam o hook por `sys.executable` (4 lugares), isto é, também no 3.9
  [F29 · rodado · 95]. Os três hooks, chamados no 3.9 com um payload de sonda, saem com 0 [F30 · rodado · 90].
  `brza_runtime.py` e `brza-note` caem no 3.9 em `TypeError` no `X | None` [F5 · rodado · 95].
- **Mas nas sessões vivas o hook roda no 3.14.** O PATH das duas sessões de chat do app (pids 43331 e 67999, lançadas
  por `~/.local/bin/claude --settings …`) resolve `python3` para `/usr/local/bin/python3` 3.14.6; o da sessão
  `remote-control` (pid 81988), para `/opt/homebrew/bin/python3` 3.14.7 [F31 · rodado · 92]. O 3.9 entra só numa
  máquina cujo PATH não tenha Python do Homebrew ou do python.org.
- **A medição de fora do hook lê o hook pelo caminho do workspace.** `fact_outcome.py:29-35`,
  `summarize_measurements.py:34`, `close-task/SKILL.md:44` [F8 · lido · 93].
- **As linhas de hook do `settings.json`** chamam `${BRZA_PYTHON:-python3} "${BRZA_WORKSPACE:-$CLAUDE_PROJECT_DIR}/.claude/hooks/<hook>.py" … || true`
  (`settings.json:21-117`) [F9 · lido · 95]: hook que quebra não avisa.
- **Subir um Python custa ~27–29 ms** (10 `python3 -c 'import pathlib, subprocess, re'` em 0,27 s no 3.14 e 0,29 s no
  3.9) [F32 · rodado · 90].

#### O `AGENTS.md` no Claude Code

- Padrão `claude-md-or-agents-md`: com os dois arquivos, só o `CLAUDE.md` [F10 · doc · 95]. A opção que lê os dois está
  no `~/.claude/settings.json:233-238` desta máquina [F11 · rodado · 95], e a doc a ignora nos settings de projeto
  [F12 · doc · 95]. O `@AGENTS.md` vale em todo modo e não duplica [F13 · doc · 93]. `.claude/rules/*.md` sem `paths`
  carrega no arranque [F15 · doc · 93].

#### O código acha o workspace

- **Worktree fora do diretório do repositório devolve o `.git` do checkout principal**, em caminho físico: num
  `git worktree add ../wt`, o `git rev-parse --path-format=absolute --git-common-dir` dá `<principal>/.git`, com o link
  `/private/tmp/pln006` já resolvido para `~/Library/Application Support/brza-studio/chat-scratch/…`
  [F33 · rodado · 95]. O `claude-brza:13-14` diz que o app cria os worktrees em `~/orca/workspaces/…`
  [F42 · lido · 90]; hoje `~/orca/workspaces/brza-studio` está vazio, e o `brza-studio` só tem o checkout principal, de
  modo que o caso do app não foi visto ao vivo [F34 · rodado · 90].
- **`register` e `where` não são comandos embutidos do CLI do app**, e `brza <x>` despacha para `brza-<x>` do PATH
  [F17 · rodado · 90] [F41 · rodado · 88] (premissa: a lista de cabeças embutidas lida nesta execução está completa).

#### O índice da `master`

- **`merge=union` junta acréscimos simultâneos sem conflito, mas fora de ordem.** Sonda: `PLN-002` acrescentado numa
  branch e `issue:x` na `master`, depois mesclados, saem sem conflito, com `PLN-002` depois de `issue:x`
  [F35 · rodado · 95]. O `man gitattributes` diz que o `union` "tends to leave the added lines in the resulting file in
  random order" [F36 · doc · 95]. A "última linha de cada id" da R5.2 se lê, então, como a de maior `ts`.
- **Dá para acrescentar na `origin/master` sem tocar árvore nenhuma.** Sonda: de um worktree `workstream/a`, `git
  read-tree` num índice temporário, `hash-object`, `update-index --cacheinfo`, `write-tree`, `commit-tree -p
  origin/master` e `git push origin <sha>:refs/heads/master`; o checkout principal, sujo e na `master`, ficou intacto, e
  a `master` local ficou para trás da `origin/master` [F37 · rodado · 95].
- **A decisão vigente recusou exatamente este passo.** `work/decisions/as-notas-moram-em-workstreams-e-a-master-guarda-so-a-norma.md`,
  "Fundamento": "Recusados: … as decisões na `master`, porque pediriam um passo de subida a cada fechamento"
  [F38 · lido · 95]. A R5.3 aceita esse passo para o índice: é a exceção a registrar.
- **O trecho da norma que muda:** `AGENTS.md:33-34` ("Na `master`: só a norma — …") e `AGENTS.md:56-58` ("Nota se grava
  na branch do workstream, pelo `brza note commit`, que recusa a `master`…") [F39 · lido · 95].
- **Nenhuma nota tem campo de descrição.** A tabela de propriedades do `work/README.md:203-217` não tem `description`
  nem resumo [F40 · lido · 93]; plano abre com `- **Retomar:**` e issue com `## O pedido` (o plano e a issue lidos
  nesta execução) [F43 · lido · 88].
- **O contador hoje:** `plans/README.md:9`, e sete referências na `plan-runner` [F25 · rodado · 93].

#### O texto local na norma e os testes

- 136 menções ao par e à pessoa nos 15 Markdown do núcleo; `{{` só em `.py` [F23 · rodado · 92] [F24 · rodado · 93].
- Testes de hoje: `scripts/brza/tests` 259 OK em 75 s; `.claude/hooks/tests` 176 OK em 11 s; `notes-checker` 67 `ok`
  [F27 · rodado · 95].

### D1 — O repositório `brza-workflow` e o layout dele — `brz-anderson/brza-workflow` (P1)

- **Origem:** R2.1, R3.1, R3.2, R4.2, R5
- **Contexto:** o núcleo sai do `brza-workspace` para um repositório público, de onde roda o CLI e de onde o sync lê.

#### Como fica

```text
brza-workflow/
├── README.md                 instalar, brza init, brza register, brza sync, o pacote client
├── bin/                      o CLI; o brza install liga em ~/.local/bin; não vai ao workspace
│   ├── brza-init  brza-sync  brza-note  brza-agents  brza-install  brza-register  brza-where
│   └── brza_runtime.py       importa core/.claude/hooks/brza_root.py pelo caminho
├── core/                     o núcleo: espelho do workspace; o sync é dono destes caminhos
│   ├── AGENTS.md  CLAUDE.md  .gitignore  .gitattributes
│   ├── plans/README.md  work/README.md
│   ├── scripts/summarize_measurements.py  scripts/fact_outcome.py                  (R4.2)
│   └── .claude/
│       ├── settings.hooks.json    a chave `hooks` do settings.json, e só ela
│       ├── agents/{collector,designer,implementer,reviewer}.md
│       ├── skills/{plan-runner,close-task,notes-checker,agent-instructions-writer}/…
│       └── hooks/{measure,compact_guard,fact_audit,brza_root}.py
├── packages/client/          pacote opcional, com `packages = ["client"]` no manifesto
│   ├── bin/brza-sessions  brza-run  claude-brza  brza-doctor  brza-print           (R4.2)
│   └── core/.claude/rules/brza-client.md
├── templates/                o que o init escreve uma vez; o sync não toca
│   ├── README.md  .brza/workspace.toml  .brza/index.jsonl (vazio)
│   ├── .claude/settings.json  .claude/rules/workspace.md
│   └── wiki/guides/.gitkeep  work/{issues,worklogs,decisions,reviews,notes}/.gitkeep
└── tests/                    os testes do CLI, dos hooks e do notes-checker
```

- **O CLI acha o núcleo pelo próprio arquivo**; o sync lê `core/` por `git show <commit>:core/<caminho>`, e não da
  árvore de trabalho [C1 · inferido · 70].
- **Nasce por cópia, sem histórico**, com "a partir de `brza-workspace@<sha>`" na mensagem [C2 · inferido · 65].

### D2 — O manifesto e o lock — `.brza/workspace.toml`, `.brza/core.lock` (P3)

- **Origem:** R2.2, R2.4, R3.3, R3.4, R4.1, R6.1, R6.3
- **Contexto:** o manifesto guarda os valores dos placeholders e reconhece o workspace; o lock guarda o que o sync
  escreveu (R6.2) e o commit seguido (R6.3). Pela R4.1, o caminho do código no manifesto é o **padrão** que o init e o
  `brza register` propõem; o caminho que vale numa máquina é o do registro (D6).

#### Como fica

```toml
# .brza/workspace.toml — o manifesto do workspace. O init o escreve; depois é local: o sync nunca o toca.
schema = 1

[workspace]
name = "brza-workspace"            # {{workspace.name}}
title = "BrzA Studio"              # {{workspace.title}}
owner = "Anderson"                 # {{workspace.owner}}
branch = "master"                  # {{workspace.branch}}; ausente = master (R3.3)
remote = "origin"                  # {{workspace.remote}}; ausente = origin (R3.3)
born = "2026-10-26"                # o CUTOFF do check_notes; o init grava a data do dia

[author]                           # R3.4
name = "Anderson Pereira Brzezinski"
email = "240569289+brz-anderson@users.noreply.github.com"
login = "brz-anderson"

[code]
name = "brza-studio"               # {{code.name}}
path = "~/Projects/brza-studio"    # {{code.path}}; o padrão do registro (R4.1), não a verdade da máquina
github = "brz-anderson/brza-studio"
branch = "master"
remote = "origin"
plan_branch = "[a-z]+/pln-(\\d+)(-|$)"

[core]
ref = "master"                     # R6.3
packages = ["client"]

[checker]
worklogs_link_from = "2026-10-28"
```

```toml
# .brza/core.lock — gerado pelo brza sync; não edite
commit = "<sha do brza-workflow>"
ref = "master"
synced = "2026-11-03"

[files]
"AGENTS.md" = "sha256:…"
".claude/settings.json#hooks" = "sha256:…"
```

- **O parser do TOML é próprio** (R6.1), de um subconjunto — tabela, `[[tabela]]`, string, lista de string,
  comentário — em `brza_root.py`, conferido contra o `tomllib` nos testes. O mesmo parser lê o registro do D6.
  - **O argumento que fica:** o hook roda no `python3` que o PATH do lançador der, e o `|| true` cala a quebra [F9];
    numa máquina com só o 3.9 do sistema no PATH, um `import tomllib` derrubaria a medição e a trava de fechamento sem
    aviso. O hook sobe no 3.9 hoje [F29].
  - **O argumento que caiu:** "o hook roda no 3.9 aqui". Nas sessões vivas desta máquina ele roda no 3.14 [F31]. O
    parser se paga, portanto, só no workspace aberto numa máquina sem Python novo no PATH, e não nesta. O custo
    continua em ~1 h, dentro do P3 [C41 · inferido · 70]. A R6.1 não se reabre: o fato novo estreita o caso, não o
    elimina.
- **O `check_notes.py:41,51`** passa a ler `workspace.born` e `checker.worklogs_link_from` [C4 · inferido · 75].

### D3 — A fronteira, arquivo a arquivo (P1, P3)

- **Origem:** R2.2, R2.3, R3.2, R4.2, R4.4, R5

#### Como fica

| Arquivo de hoje | Dono depois | Modo no sync |
| :-- | :-- | :-- |
| `AGENTS.md`, `CLAUDE.md`, `plans/README.md`, `work/README.md` | núcleo | render |
| `.claude/agents/*.md`, `.claude/skills/**/*.md` | núcleo | render |
| `.claude/skills/notes-checker/scripts/*.py` | núcleo | cópia |
| `.claude/hooks/{measure,compact_guard,fact_audit}.py` + `brza_root.py` novo | núcleo | cópia |
| `.claude/hooks/tests/*`, `notes-checker/tests/run.py` | `brza-workflow/tests/`, com o código que testam | — |
| `.claude/hooks/resume_guard.py` e o teste | sai (R2.3) | apagado no primeiro sync |
| `.claude/settings.json` | init; o sync é dono só de `hooks` | merge da chave |
| `.gitignore` | núcleo | cópia |
| `.gitattributes` (novo, com `merge=union` do índice) | núcleo | cópia |
| `scripts/summarize_measurements.py`, `scripts/fact_outcome.py` | núcleo (R4.2) | cópia |
| `scripts/brza/{brza-note,brza_runtime.py,brza-agents,brza-install}` | `brza-workflow/bin/` | — |
| `scripts/brza/{brza-sessions,brza-run,claude-brza,brza-doctor,brza-print}` | `packages/client/bin/` (R2.3, R4.2) | — |
| `scripts/brza/{brza-app,brza-dev,brza-test,brza-tree,brza-shot}` e os testes | local do `brza-workspace` (R4.2) | — |
| `README.md` | init uma vez; local | — |
| `CLAUDE.md:34-45` (função do shell, chat do app) | `packages/client/core/.claude/rules/brza-client.md` (R4.4) | render |
| `CLAUDE.md:58-67` (identidade) | núcleo, com `{{author.*}}`; `personal` e `gh auth switch` ao `README.md` | render |
| `CLAUDE.md:69-80` (plugins) | núcleo, sem o `skill-creator`; a lista à `.claude/rules/workspace.md` | render |
| `AGENTS.md:37` (workstreams de agora) | `README.md` local | — |
| `AGENTS.md:60-65` ("Quem commita") | núcleo, com placeholders; a chave `personal` ao `README.md` | render |
| `plans/README.md:9` (o contador) | sai (R5.3); o número vem do índice (D11) | — |
| `.brza/index.jsonl` (novo) | local: nasce vazio no init; só o `brza note` acrescenta | — |
| As 7 menções à Fixfy | saem do núcleo (R8.2) | — |
| A medição datada (`AGENTS.md:92-93`, `CLAUDE.md:158+`) | fica no núcleo, como o porquê da regra (R8.3) | render |

### D4 — Os placeholders e o motor de render — `brza_root.render` (P3)

- **Origem:** R2.2, R6.1

#### Como fica

```python
PLACEHOLDER = re.compile(r'\{\{\s*([a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+)\s*\}\}')

def render(text: str, manifest: dict, path: str) -> str:
    """Troca cada {{tabela.chave}} pelo valor do manifesto, com os padrões da R3.3 já aplicados. Chave que falta é
    erro com o caminho e a linha; sem condicional, laço nem escape."""
```

| Placeholder | Substitui hoje | Amostra |
| :-- | :-- | :-- |
| `{{workspace.name}}` | `brza-workspace` | `AGENTS.md:1`, `collector.md:9`, `reviewer.md:9` |
| `{{workspace.title}}` | `BrzA Studio`, como o projeto | `AGENTS.md:3` |
| `{{workspace.owner}}` | `Anderson`, quem decide | `AGENTS.md:37`, `designer.md:13,36` |
| `{{workspace.branch}}`, `{{workspace.remote}}` | `` `master` ``, `origin/master` | 26 + 1 [F23] |
| `{{author.name}}`, `{{author.email}}`, `{{author.login}}` | nome, noreply, `brz-anderson` | `AGENTS.md:60-65`, `CLAUDE.md:58-67` |
| `{{code.name}}`, `{{code.path}}`, `{{code.github}}`, `{{code.branch}}` | `brza-studio` e afins | `AGENTS.md:3-5`, `plan-runner/SKILL.md:14,19-20` |

- Só renderiza `.md` e o `templates/.claude/settings.json`; o `.py` é cópia e lê o manifesto em execução [F24].
- **Teste de ouro:** `render(core, manifesto do brza-workspace)` igual à `master` de hoje, salvo a lista fechada do D12.

### D5 — O `AGENTS.md` carrega no Claude Code — `core/CLAUDE.md` (P3)

- **Origem:** R4.4

#### Como fica

```markdown
@AGENTS.md

# Adaptador do Claude Code

A norma do workspace está no `AGENTS.md`, importado na primeira linha deste arquivo: o Claude Code o carrega em
qualquer valor de **Project instructions**, e sem duplicar quando o valor é `claude-md-and-agents-md`. Este arquivo
traz só o adaptador: traduz o vocabulário da norma e acrescenta a mecânica própria do Claude. O que é só deste
workspace está em `.claude/rules/`, que o Claude Code também carrega no arranque.
```

### D6 — A raiz pelo cwd e o registro da máquina — `core/.claude/hooks/brza_root.py`, `~/.config/brza/workspaces.toml` (P2)

- **Origem:** R2.4, R3.3, R4.1
- **Contexto:** do workspace, o common dir basta; do repositório de código, que não tem manifesto, quem liga é o
  registro da máquina (R4.1).

#### Como fica

```toml
# ~/.config/brza/workspaces.toml — os workspaces desta máquina. Escrito pelo brza init e pelo brza register;
# arquivo de usuário: cada escrita vai ao worklog, em "## Fora do workspace".
[[workspace]]
root = "/Users/andepb/Projects/brza-workspace"   # o checkout principal, absoluto e físico
code = "/Users/andepb/Projects/brza-studio"      # o checkout principal do código, absoluto e físico
```

- **O par fica no registro** (R7.1): o `[code].path` do manifesto é versionado e vale para todas as
  máquinas; o registro guarda o caminho real desta.
- **Onde:** `$XDG_CONFIG_HOME/brza/workspaces.toml`, ou `~/.config/brza/workspaces.toml`; `BRZA_REGISTRY` só nos
  testes.
- **Quem escreve:** `brza init --code` (D8) e `brza register <raiz> [--code <caminho>]`, para a migração e para a
  segunda máquina; sem `--code`, o `[code].path` do manifesto. Recusa quando o mesmo código já está ligado a outro
  workspace (R7.1).

```python
MANIFEST = '.brza/workspace.toml'
REGISTRY = Path(os.environ.get('BRZA_REGISTRY')
                or Path(os.environ.get('XDG_CONFIG_HOME') or Path.home() / '.config') / 'brza' / 'workspaces.toml')

class Workspace(NamedTuple):           # compatível com o 3.9 [F29]
    root: Path
    manifest: dict
    role: Optional[str]                # 'notes' | 'code' | None
    top: Optional[Path]
    branch: Optional[str]

def find(cwd) -> Optional[Workspace]:
    """O workspace do cwd, nesta ordem:
    1. BRZA_WORKSPACE apontando para um diretório com o manifesto: o override (R2.4);
    2. o checkout principal do cwd — o pai do `git rev-parse --path-format=absolute --git-common-dir` — com o
       manifesto: papel 'notes';
    3. o registro: a entrada cujo `code`, em caminho físico e sem maiúsculas, é esse checkout principal, e cujo `root`
       tem o manifesto: papel 'code';
    4. nada disso: None."""
```

- **Os worktrees do app em `~/orca/workspaces/…`:** o common dir de um worktree é o `.git` do checkout principal,
  onde quer que o worktree esteja [F33]; o pai desse `.git` é o `~/Projects/brza-studio`, que casa com o `code` do
  registro. Nada se registra por worktree. A comparação usa caminho físico e sem maiúsculas, como o `claude-brza:45-48`
  faz hoje, porque o git devolve o caminho já resolvido [F33]. O caso do app não foi visto ao vivo [F34].
- **Custo por chamada:** o `git rev-parse` que já existe (~9 ms) [F18] e a leitura de um arquivo de poucas linhas;
  some a chamada de `git config` que a recomendação anterior pedia [C42 · inferido · 75].
- **`brza where`** (`bin/brza-where`) imprime `<raiz> notes|code` ou nada; é o que o `~/.zshrc` chama (D10), por ~30 ms
  de Python [F32].
- **Quem usa:** `brza_runtime`, `brza-note` (com `{remote}/{branch}` no lugar de `origin/master`), `brza-sessions`,
  `claude-brza`, `brza-tree` (que hoje acha a memória pelo `WORKSPACE`), `measure.py`, `compact_guard.py`.

### D7 — Os hooks leem a raiz e o código do manifesto — `core/.claude/hooks/` (P2)

- **Origem:** R2.3, R2.4, R4.1

#### Como fica

- **`measure.py`:** sai a cópia de `:88-91` e `:583-600`; entra `import brza_root`. A raiz da medição fica
  `MEASURE_DIR` → `BRZA_WORKSPACE` → o checkout principal do próprio script, pelo common dir. A sessão do código acha o
  workspace pelo registro (D6). O `"master"` de `:592` vira o `[workspace].branch`.
- **`compact_guard.py`:** as mensagens de `:5-10,84-88` usam `[workspace].name` e `[code].name`.
- **`fact_audit.py`:** sem mudança [F2].
- **Compatível com o 3.9**, como hoje [F29]: nenhum `X | None` em execução, nenhum `tomllib`.

### D8 — `brza init` — `bin/brza-init` (P5)

- **Origem:** R1.3, R1.2, R3.3, R3.4, R4.1, R5

#### Como fica

```text
brza init <dir> --name <nome> --code <caminho> [--title <projeto>] [--owner <quem decide>]
          [--author-name <nome>] [--author-email <e-mail>] [--author-login <login>]
          [--branch master] [--remote origin] [--code-branch master] [--package client]… [--dry-run]
```

1. **Recusa** `<dir>` não vazio, `--code` que não é repositório git, e `--code` já ligado a outro workspace no registro.
2. **Autor:** as flags; sem elas, `git config --global user.*`; sem os dois, recusa (R3.4).
3. `git init -b <branch>` em `<dir>`.
4. **Manifesto** (D2): `born` = hoje; `[code].path` = o `--code`, com `~` quando cabe; `core.ref` = a branch do checkout
   do `brza-workflow`.
5. **Templates:** `README.md`, `.claude/settings.json`, `.claude/rules/workspace.md`, `.brza/index.jsonl` vazio, o
   esqueleto `wiki/guides/` e `work/<gênero>/` com `.gitkeep`.
6. **Camada 1 do sync** (D9) no diretório novo: núcleo, chave `hooks`, `.gitattributes`, lock.
7. **Registro:** acrescenta `{root = <dir>, code = <--code>}` ao `~/.config/brza/workspaces.toml` (D6) e imprime
   `registro: <caminho>`, para o worklog.
8. **Confere:** `check_notes.py --root <dir>` verde e nenhum `brza-workspace`/`brza-studio` fora do que veio do
   manifesto.
9. **Commit** `chore: brza init (brza-workflow@<sha7>)`; sem push. A saída diz os próximos passos: `gh repo create`,
   `git remote add`, `git push -u`, `brza note workstream <nome>` e o bloco do shell. Sem remote, o `brza note`
   recusa o `plan-open` (D11).

### D9 — `brza sync`, as duas camadas — `bin/brza-sync`, `bin/brza-note` (P6)

- **Origem:** R1.4, R2.2, R3.2, R3.3, R6.2, R6.3

#### Como fica

```text
brza sync [--dry-run] [--ref <branch|sha>] [--force <caminho>]… [--no-push] [--core-only]
brza note sync [--no-push]
```

**Camada 1**, no checkout principal do workspace achado pelo cwd (D6):
1. Recusa fora da `[workspace].branch`, ou com mudança nos caminhos do núcleo.
2. `git pull --ff-only` do workspace, para trazer as linhas do índice que o `brza note` empurrou (D11);
   `git -C <brza-workflow> fetch -q origin`; o commit é `origin/<core.ref>`, ou o `--ref`.
3. Para cada arquivo de `core/` e dos pacotes: render ou cópia; contra o lock:
   - igual ao lock, ou ausente → escreve;
   - diferente do lock → não escreve, imprime o diff contra o novo e marca falha; `--force <caminho>` escreve (R6.2);
   - no lock e fora do núcleo novo → apaga, se não foi editado.
4. `.claude/settings.json`: troca só `hooks`.
5. Lock; `git add` dos caminhos tocados; commit `chore(norma): brza-workflow@<sha7>`; push, salvo `--no-push`. Sai com 1
   se algum arquivo foi recusado.

**Camada 2:** o `brza note sync`, que leva também o índice aos workstreams; o `.gitattributes` faz o `union` [F35].

- O sync **nunca toca** o manifesto, o índice, o `README.md` nem a `.claude/rules/workspace.md`.

### D10 — `brza install`, o lançador e o bloco do `~/.zshrc` (P7)

- **Origem:** R2.4, R3.2, R4.1, R4.2

#### Como fica

- **`brza install --all`** liga `bin/`; **`--client`**, `packages/client/bin/`; **`--local <dir>`**, os `brza-*` de
  um diretório local (hoje `~/Projects/brza-workspace/scripts/brza`, R4.2); **`--chat-command`** como hoje;
  **`--relink`** troca link que aponta para outro lugar.
- **Os scripts locais** acham o `brza_runtime` pelo `BRZA_WORKFLOW` ou pelo `realpath(shutil.which('brza-note'))`
  [C13 · inferido · 70].
- **`brza-doctor`:** o noreply sai do `[author].email`; e confere o registro: o workspace do cwd registrado, e nenhum
  código ligado a dois workspaces.
- **`claude-brza`:** `brza_root.find(cwd)`; com workspace, `BRZA_WORKSPACE=<raiz>`, `--settings` dela e, no papel
  `code`, o `--agents`.
- **O bloco do `~/.zshrc`** (e do `README.md` local):

```zsh
# brza: o workspace do cwd — pelo .brza/workspace.toml, ou, no código, pelo ~/.config/brza/workspaces.toml.
# O bloco "Funções do shell" do README do workspace. A BRZA_WORKSPACE exportada é override.
brza_claude() {
  local ws=$1 role=$2 json; shift 2
  local -a agents=()
  if [ "$role" = code ] && [[ " $* " != *" --agents"* ]]; then
    json=$(brza-agents --workspace "$ws" 2>/dev/null)
    [ -n "$json" ] && agents=(--agents "$json")
  fi
  BRZA_WORKSPACE="$ws" command claude --settings "$ws/.claude/settings.json" "${agents[@]}" "$@"
}

claude() { local w; w=$(brza-where 2>/dev/null); if [ -n "$w" ]; then brza_claude ${=w} "$@"; else fixfy_claude "$@"; fi; }
```

- **Saem** `BRZA_WORKSPACE=…`, `BRZA_STUDIO=…` e o `brza_where` de `~/.zshrc:51-65`; a troca vai ao worklog. O
  `brza-where` em Python custa ~30 ms por `claude` lançado [F32] e evita uma terceira cópia da regra da raiz em zsh
  [C43 · inferido · 75].

### D11 — O índice da `master` — `.brza/index.jsonl` (P4)

- **Origem:** R4.3, R5.1, R5.2, R5.3, R5.4
- **Contexto:** o contador sai. Um arquivo na `master` lista planos, issues e decisões de todos os workstreams, para
  quem coordena e para numerar o plano novo.

#### Como fica

**Caminho:** `.brza/index.jsonl`, junto do manifesto e do lock, fora das zonas do checador e das pastas de gênero
(R7.2). **É local**: nasce vazio no init, e o sync nunca o toca. O `.gitattributes`, que é do
núcleo, liga o driver:

```gitattributes
# O índice só cresce: dois acréscimos simultâneos se juntam sem conflito (o union do git, sem driver a configurar).
.brza/index.jsonl merge=union
```

**Uma linha por evento**, JSON numa linha, chaves em inglês:

```json
{"ts":"2026-10-31T14:02:11-03:00","event":"created","kind":"plan","id":"PLN-006","path":"plans/PLN-006-o-brza-init-monta-a-norma-do-zero/PLN-006-plan.md","title":"O `brza init` monta a norma num workspace do zero","description":"…","status":"open","phase":"design","workstream":"workspace","worktree":".worktrees/workspace","session":"brza-workspace-91","commit":"58d28ca"}
```

| Chave | De onde vem |
| :-- | :-- |
| `ts` | a hora do evento, ISO 8601 com fuso |
| `event` | `created` ou `changed` |
| `kind` | `plan`, `issue`, `decision`, pela pasta |
| `id` | `PLN-NNN` no plano; `issue:<slug>` e `decision:<slug>` com o slug da criação, que não muda (R8.1) |
| `path` | o caminho de hoje, que o rename muda |
| `title` | o H1 |
| `description` | o campo `description` do frontmatter, uma frase; nas notas anteriores à migração, o H1 (R7.3) |
| `status`, `phase` | o frontmatter; `phase` só no plano |
| `workstream`, `worktree` | a branch `workstream/<x>` do commit e `.worktrees/<x>` |
| `session`, `commit` | o `$CLAUDE_SESSION_NAME`, quando há, e o commit da nota no workstream |

- **O estado vigente de um id é a linha de maior `ts`**, e não a última do arquivo, porque o `union` deixa as linhas
  fora de ordem [F35] [F36]. Na mesma `ts`, vale a ordem do arquivo. É a leitura da R5.2 com esse fato, sem mudar a
  decisão.

**Quem grava** (R5.3):

```text
brza note plan-open <slug> --title <H1> --description <frase> [--workstream <nome>]
    git fetch; número = maior PLN do índice na origin/<branch> + 1; acrescenta a linha `created` com status open e
    phase interview; push na master; imprime PLN-NNN e o caminho plans/PLN-NNN-<slug>/PLN-NNN-plan.md. Push recusado
    por corrida: refaz do fetch, com o número de novo, até 3 vezes. Sem remote: recusa.
brza note commit <caminho>… -m <mensagem>
    como hoje, e depois do push no workstream: para cada plano, issue ou decisão do commit, compara o frontmatter
    (e o H1) com o do commit anterior. Nota nova → `created`; campo mudado → `changed`; rename → `changed` com o
    `path` novo; nada mudou → nenhuma linha. Todas as linhas do commit vão num commit só na master.
brza note index --rebuild
    lê planos, issues e decisões de todas as branches workstream/* (locais e da origin) e acrescenta `created` para o
    id que falta no índice; idempotente. Serve à migração e a reparar o índice depois de um push que falhou.
```

**Como o commit na `master` convive com o push no workstream** (R7.4): o `brza note` monta o commit da
`master` sem checkout — `fetch`, `read-tree` da `origin/<branch>` num índice temporário, `hash-object` do arquivo com as
linhas novas, `update-index`, `write-tree`, `commit-tree` e `push <sha>:refs/heads/<branch>` —, com 3 tentativas na
corrida. Assim não toca o checkout principal, que pode estar sujo ou na edição da norma, nem o worktree do workstream
[F37]. A `master` local fica atrás da `origin/master` até o próximo `git pull`; o `brza sync` puxa antes de escrever
(D9). Falhou depois de 3 tentativas: a nota já está no workstream, e a saída diz
`aviso: índice não gravado; rode brza note index --rebuild`, com saída 0 [C44 · inferido · 70].

- **Custo de tempo:** um `fetch` e um `push` a mais por `plan-open` e por commit que muda frontmatter, ~1–2 s com o
  GitHub [C45 · inferido · 55] (não medido; a sonda foi num remote local).
- **O `union` quase nunca roda nesse caminho**, porque cada acréscimo parte da `origin` recém-buscada; ele protege o
  merge da `master` nos workstreams e o `pull --rebase` de quem acrescentou à mão [C46 · inferido · 70].

**A exceção na norma.** O `AGENTS.md:33-34` passa a:

```markdown
- **Na `master`:** a norma — este arquivo, o `CLAUDE.md`, o `README.md`, o `plans/README.md`, o `work/README.md`, o
  `.claude/`, o `scripts/`, o `.gitignore` e o `.gitattributes` — e o índice `.brza/index.jsonl`, a única exceção:
  uma linha por plano, issue ou decisão criada ou alterada, em qualquer workstream, para que quem coordena veja
  todas as frentes num arquivo só. Só o `brza note` acrescenta, e ninguém edita.
```

E o `AGENTS.md:56`:

```markdown
**Nota se grava na branch do workstream, pelo `brza note commit`**, que recusa a `master` e dá o push no workstream;
quando o frontmatter de um plano, issue ou decisão muda, ele acrescenta a linha do índice na `master`, sem checkout.
O número do plano novo sai do `brza note plan-open`.
```

- **A decisão de 2026-10-30** [F38] recusou "um passo de subida a cada fechamento" para as decisões; o índice é esse
  passo, aceito na R5.3 só para a linha do índice. O registro vai como nota nova em `work/decisions/`, que cita a R5 e
  aponta a de 2026-10-30. Sem `superseded_by`, porque a regra de antes continua valendo para as notas (R8.4). A nota
  nasce como proposta e só vira decisão com a confirmação explícita de Anderson.
- **A `plan-runner`** troca as sete referências ao contador [F25] por "o número sai do `brza note plan-open`"; o
  `plans/README.md` perde a linha 9.

### D12 — A migração do `brza-workspace` para cliente (P8)

- **Origem:** R2.1, R6.4, R4.1, R5; Cobertura "o `brza-workspace` segue funcionando".

#### Como fica

1. **Na `master` do `brza-workspace`, sem mudar comportamento:** `.brza/workspace.toml`, `.claude/rules/workspace.md`,
   `.gitattributes` e `.brza/index.jsonl`, este povoado pelo `brza-workflow/bin/brza-note index --rebuild`, rodado
   pelo caminho (PLN-001 a PLN-006, as issues e as decisões). Os scripts de hoje ignoram os quatro arquivos.
2. **Registro:** `brza-workflow/bin/brza-register ~/Projects/brza-workspace --code ~/Projects/brza-studio`, que cria
   o `~/.config/brza/workspaces.toml`; vai ao worklog, em `## Fora do workspace`.
3. **Ensaio:** `brza-sync --dry-run --core-only`. Diferenças permitidas, e só elas:
   - `CLAUDE.md`: `@AGENTS.md` na primeira linha; saem `:34-45` (ao pacote) e o local (à `.claude/rules/workspace.md`);
   - `plans/README.md`: sai a linha do contador;
   - `plan-runner`: as sete referências ao contador;
   - `AGENTS.md`: sai a lista dos workstreams (`:37`) e a chave `personal`; entra a exceção do índice (D11);
   - `measure.py`, `compact_guard.py`: a raiz pelo `brza_root`; `brza_root.py` novo;
   - `resume_guard.py`, os testes de `.claude/hooks/tests` e do `notes-checker`: apagados;
   - `.claude/settings.json`: nenhuma.
4. **Índice em dia:** `brza-note index --rebuild` de novo, para pegar o plano aberto pelo contador entre os itens 1 e
   4 (idempotente).
5. **Troca dos links:** `brza-install --all --client --relink` e `--local ~/Projects/brza-workspace/scripts/brza`;
   `brza install --chat-command`. Volta: `ln -sfn` aos caminhos antigos.
6. **Sync real:** `brza sync --core-only`; um commit à parte tira de `scripts/brza/` o que foi ao `brza-workflow`.
7. **Camada 2:** `brza note sync`, que leva a `master` (e o índice) a `studio`, `tools-kit` e `workspace`.
8. **`~/.zshrc`:** o bloco do D10; worklog.
9. **Conferência:** `brza doctor` ok, com o registro; um turno num worktree do workspace e um no `brza-studio` gravam
   linha com `workstream`; `/compact` com nota suja barra; `brza note commit` de uma issue acrescenta `changed` na
   `origin/master`.

- **A sessão aberta não quebra:** até o item 5, nenhum script mudou [C8 · inferido · 75]; o `brza-note` novo acha a
  raiz pelo manifesto (item 1) e o código pelo registro (item 2); os hooks da sessão com a `BRZA_WORKSPACE` mudam no
  item 6, e os da sessão sem ela, no item 7 [C9 · inferido · 70].
