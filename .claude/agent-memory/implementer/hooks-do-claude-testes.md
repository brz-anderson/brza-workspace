---
name: hooks-do-claude-testes
description: Como testar e estender os hooks de .claude/hooks (measure.py, fact_audit.py stop e run): carga por importlib, MEASURE_DIR, Popen mockado, espião do claude, State com path
metadata:
  type: project
---

- Gate dos hooks: `cd <repo> && python3 -m unittest discover -s .claude/hooks/tests` (207 testes em 2026-10-31, ~15 s). Um arquivo só: `discover -s .claude/hooks/tests -p test_x.py` (o `unittest caminho.py` falha com "Empty module name").
- Script novo que importa do `measure.py`: carregue por `importlib.spec_from_file_location` do mesmo diretório e exponha o
  módulo (`fact_audit.measure`). O `MEASURE_DIR` é lido na importação: o teste seta a variável **antes** de carregar o
  script. Para não esperar o `settle`, o teste faz `module.measure.settle = lambda path, **_: None`.
- Estado próprio sob a mesma trava: `measure.State(os.path.join(measure.DIR, "<arquivo>.json"))` — não aninhar dois `State`.
- **A devolução de subagente mora no `SubagentHandback`**: `tool_use` de nome `SubagentHandback` com o texto em
  `input.message`, e não num bloco `text` (4 de 4 `designer`, 4 de 5 `collector` medidos). Parser de devolução lê esse
  campo e só cai no último `text` sem ele.
- Forma da linha do transcript: `{"type":"assistant","message":{"role":"assistant","content":[{"type":"text",...},
  {"type":"tool_use","name":"Write","input":{"file_path","content"}}]}}`; o Claude Code pode partir uma mensagem em várias
  linhas, uma por bloco.
- A tarefa manda editar o checkout da `master` (`/Users/andepb/Projects/brza-workspace`), mesmo com o cwd num worktree.
- **Teste que passa pelo `stop` do `fact_audit.py` solta o `run` de verdade, e o `run` chama o `claude` de verdade (custo).**
  A base do teste (`Base.setUp`) troca o `Popen` por mock e o `measure.workstream_of` por stub: `measure` e `fact_audit`
  dividem o módulo `subprocess`, então o mock do `Popen` também pegaria o `git` do `workstream_of`. Só `RunTest`
  (`mock_popen = False`) e o teste do processo solto usam o `Popen` real, sempre com `BRZA_FACT_AUDIT_CLAUDE` no espião.
- Espião do `claude`: script Python com shebang `sys.executable`, não shell — `sleep` num `sh` neto segura o pipe e o
  `communicate` pendura depois do timeout. O `run` mata o grupo (`start_new_session` + `killpg`).
- Subclasses de teste não herdam de uma classe com `test_*`: o unittest reexecuta tudo (por isso `Base` e `FactAuditTest`).
- O teste do processo solto espera o `fact_audit` aparecer no log antes de sair, senão o filho recria o tmp já apagado.
  Sobra um `ResourceWarning` do `Popen` largado de propósito.
- **Script de `scripts/` que usa o `measure.py`** (`fact_outcome.py`): carrega de `<BRZA_WORKSPACE ou HERE/..>/.claude/hooks/measure.py`
  pela mesma raiz do `summarize_measurements.py`; expõe `main(argv)` que devolve o código, e o teste chama `main` capturando
  `SystemExit` (o `parser.error` sai com 2) e stub em `module.measure.workstream_of`. Log que é diretório no lugar do arquivo
  simula erro de leitura. `measure.write` não segura trava: só anexa linha.
- **`summarize_measurements.py`** carrega no teste por `spec_from_file_location` (função `load()` do
  `test_summarize_measurements.py`); o teste monta o log em tmp e chama `main()` com `sys.argv` mockado. `--facts` lê o
  log sem o `--since` (`read_log(..., "")`) e filtra no `aggregate_facts`, porque o desfecho que chega depois da data vale.
  `parser.error` sai com `SystemExit(2)`: o teste captura `stderr` com `redirect_stderr`. O log real (`.measurements/`)
  ganha eventos `fact` a cada subagente `collector`/`designer`: não fixe número dele em teste.
- **Marca do `fact_audit.py`** (`MARK`/`REFERENCE`): valide a expressão contra o transcript real do subagente antes de fechar,
  chamando `marks_of(sources_of(lines))` por `spec_from_file_location` com `MEASURE_DIR` num tmp: o que a especificação cita
  é um recorte, e o real tem outras formas. O teto do `--max-budget-usd` sai de `budget_usd(len(facts))`; o teste do espião
  regrava o arquivo da rodada a cada `subTest`, porque o `run` o apaga.
- **O `run` do `fact_audit.py` lê o `--output-format stream-json --verbose`** (PLN-005/R11): o `result` é o *último* evento
  `type: result` (o real traz um `system` depois dele), e os `tool_use` de `Read`/`Grep`/`WebFetch` saem dos eventos
  `assistant`. O espião imprime o stream (`stream(result, *tools)` do `test_fact_audit.py`); stdout sem `result` é
  `invalid_json`. `claude` do shell é função: o binário é `~/.local/bin/claude`, e o macOS não tem `timeout`.
- **Teste de timeout que de fato barra o `killpg`:** espião com `grandchild=N` (neto que herda o pipe e dorme N s) e
  `assertLess(took, 8)`; o neto é morto no `finally` pelo pid gravado. Conferido em cópia (`cp -R .claude/hooks` num `mktemp
  -d`): `process.kill()` no lugar do `killpg` e sem `start_new_session` falham com ~25 s. Teste de timeout só com espião sem
  filho passa em qualquer mutação.
- **Raiz pelo git nos scripts de `scripts/`:** `workspace_root(here, env)` (copiada em `fact_outcome.py` e
  `summarize_measurements.py`) é testável com `env={}`; `.claude/hooks/tests/repo_fixture.py` monta repo temporário com
  worktree (`make`, `clean_env`). O `measure.workstream_of` só reconhece o `BRZA_WORKSPACE`/`~/Projects/brza-workspace`: num
  repo temporário o workstream é sempre `None`, então o teste de processo usa `--workstream all`.
- O worktree só recebe o script novo depois do `brza note sync`: para conferir à mão um script alterado na `master`, rode o
  caminho da `master` com o cwd no worktree.
