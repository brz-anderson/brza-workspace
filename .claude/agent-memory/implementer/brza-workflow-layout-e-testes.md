---
name: brza-workflow-layout-e-testes
description: Como as suítes rodam no repositório brza-workflow (PLN-006): comandos, layout dos testes, o que depende de P2/P3/P7, armadilhas de Python e de cópia
metadata:
  type: project
---

- Repositório `/Users/andepb/Projects/brza-workflow` (PLN-006, nasceu no P1 de `brza-workspace@d85c783`). Gate, da raiz dele, com
  `PYTHONDONTWRITEBYTECODE=1` (o repositório não tem `.gitignore` próprio; sem a variável sobra `__pycache__`):
  `python3 -m unittest discover -s tests/hooks`, `-s tests/cli` e `python3 tests/notes-checker/run.py`.
- Testes em `tests/{cli,hooks,notes-checker}/`; cada arquivo acha o código por `ROOT`/`BIN`/`CLIENT` ou `HOOKS` calculados do
  `__file__`. O CLI (`bin/`, `packages/client/bin/`) usa `str | None`: **exige Python >= 3.10** (no 3.9 do sistema a coleta
  dá 6 erros de import); os hooks e o `notes-checker` sobem no 3.9.
- Cópia da fonte: `git archive <sha> <caminhos> | tar -x -C $(mktemp -d)`. Não use `rm -rf dir/*` depois de `cd`: o guard do
  Claude barra o glob relativo; use `mktemp -d` e apague o caminho exato.
- `sed` do macOS não tem `\(a\|b\)`: edite com `python3` e `assert t.count(a) == 1`.
- Os scripts do `packages/client/bin` importam `brza_runtime` do `bin/` por `parents[3] / 'bin'` (ou `parents[2]` no
  `brza-doctor`, que usa `HERE`); o `brza-note` roda o `brza-sessions` do cliente por `HERE.parent / 'packages/client/bin'`.
- Sem skip por passo pendente: o `SettingsTest` do `test_fact_audit` saiu no P3 (lê `core/.claude/settings.hooks.json`) e o do installer no P7.
- **Testes do `brza-note` que precisam do workspace de mentira herdam de `NoteFixture`** (`tests/cli/test_brza_note.py`, sem
  `test_*`), e não de `NoteTest`: o unittest reexecutaria os testes herdados. O `test_brza_note_index.py` (P4) é o exemplo.
- **Índice da master (P4):** commit sem checkout por `plumb(...)` do próprio `brza-note` (o `runtime.git` não aceita `env` nem
  stdin; o `GIT_INDEX_FILE` temporário precisa de caminho absoluto). A corrida se testa trocando `GLOBALS['index_push']` por
  um fio que empurra um rival na primeira chamada; o teste de dois processos reais (`Popen` do `bin/brza-note` com
  `BRZA_WORKSPACE`) passou 6 de 6. O rename só chega ao índice se o caminho antigo for dado ao `commit`, e o `git add`
  recusava o pathspec sumido: o `commit` agora usa `git rm --cached --ignore-unmatch` para o que não existe no disco.
- O fixture tem `PLN-001-x` sem frontmatter no `studio`: todo teste de `--rebuild` o enxerga, conte com ele nos ids.
- **Worktree de trabalho do P2 em diante:** `/Users/andepb/Projects/brza-workflow/.worktrees/pN`, branch `feat/pln-006-pN`; o
  pedido manda trabalhar só nele. `PYTHONDONTWRITEBYTECODE=1` também em `python3 -c`/depuração solta: sem ele sobra
  `bin/__pycache__` e `core/.claude/hooks/__pycache__` (o `.gitignore` os ignora, mas apague pelo caminho exato).
- **`brza_root` (P2):** `core/.claude/hooks/brza_root.py`, só stdlib e 3.9; `bin/brza-where` e `bin/brza-register` o importam por
  `parent.parent/'core'/'.claude'/'hooks'` e também sobem no 3.9. O `brza_runtime` o importa do mesmo jeito e expõe
  `WORKSPACE`, `STUDIO` e `STUDIO_BRANCH` por `discover()` **no import**, pelo cwd, com o legado (`BRZA_WORKSPACE` sem manifesto,
  `~/Projects/brza-workspace`) como último recurso até o P8 pôr o manifesto lá. Teste do CLI que importa o runtime põe
  `os.environ['BRZA_REGISTRY'] = '/nonexistent/...'` antes do import; os de processo montam o env à mão.
- **O `brza_root` é um módulo só por processo:** teste que troca `brza_root.git` num teste de hook vaza para os seguintes
  (o `measure` o importa por `sys.modules`); use `mock.patch.object` com `addCleanup`. O `measure.resolve_workstream` engole
  exceção e devolve `(None, None)`: ao depurar, chame `_resolve_workstream` direto. O cache `_WORKSTREAMS` é por cwd: limpe-o
  entre duas leituras do mesmo cwd depois de mudar a branch.
- Testes do `brza_root` batem o parser contra o `tomllib` (pula no 3.9: 4 skips no 3.9 = 3 do `tomllib` + P3). Os testes
  de `tests/cli` não coletam no 3.9 (`str | None`); só os scripts `brza-where`/`brza-register` são rodados lá, por subprocesso.
- **P7 (install, doctor, claude-brza, bloco do shell):** tests/cli roda 264 testes, hooks 193 (1 skip P3), em 2026-10-31. O
  `brza-install` lê o checkout por `BRZA_WORKFLOW` (ou o pai do `bin/` do arquivo) **a cada chamada**: o teste põe a variável
  com `patch.dict(os.environ)` e `patch.object(runtime, 'LOCAL_BIN', tmp)`, sem tocar globais do `run_path`. Para provar link
  de verdade rode o `bin/brza-install` por subprocesso com `HOME` trocado (e sem `ORCA_USER_DATA_PATH`). O `claude-brza` e o
  `brza-doctor` testam por `run_path`; o doctor troca `GLOBALS` (`git_ident`, `git_config_email`, `which`, `APP`).
- Teste de função de shell: `zsh -f -c 'source bloco; ...'` com `ZDOTDIR`/`HOME` temporários e PATH com um `python3` que é
  `sys.executable` (o `/usr/bin/python3` 3.9 não roda o `brza-agents`, e ele falha calado). Use raiz com espaço no nome.
- `brza_root.find` pede que o cwd exista (o git roda nele): teste de "subpasta do código" precisa criar a pasta.
- **Norma em molde (P3):** `core/**/*.md` leva `{{tabela.chave}}`; o `brza_root.render` (+ `render_settings`, `merge_hooks`,
  `validate_manifest`, `dump_manifest`, `dump_lock`) vive no mesmo `brza_root.py`. **Teste de ouro** em
  `tests/hooks/test_golden_render.py`: cópia da master em `tests/hooks/fixtures/golden/master/` e a lista fechada de trocas de
  texto em `tests/hooks/golden_differences.py` (`DIFFERENCES`, `WHY`; o P8 reusa). Mudou um `.md` do núcleo: o ouro reprova até a
  lista acompanhar. Edição em massa dos `.md`: script Python com `count == 1` por troca literal e depois as trocas de valor por
  placeholder (a mais longa primeiro: nome+email, `brz-anderson/brza-studio`, `brz-anderson`, `brza-workspace`…), com o
  `\bmaster\b` à parte (a do código vira `{{code.branch}}`). As entradas da lista são trocas de substring; a inserção ancora
  numa linha vizinha.
- Varredura de `{{workspace.x}}` em `.py` exclui o `brza_root.py`, que documenta a sintaxe. `tests/hooks` no 3.9 dá 5 skips
  (tomllib: 3 do P2 e 2 do P3).
