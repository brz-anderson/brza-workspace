---
name: hooks-do-claude-testes
description: Como testar e estender os hooks de .claude/hooks (measure.py, fact_audit.py stop e run): carga por importlib, MEASURE_DIR, Popen mockado, espião do claude, State com path
metadata:
  type: project
---

- Gate dos hooks: `cd <repo> && python3 -m unittest discover -s .claude/hooks/tests` (147 testes em 2026-10-31, com `test_fact_audit.py` e `test_fact_outcome.py`, ~11 s). Um arquivo só: `discover -s .claude/hooks/tests -p test_x.py` (o `unittest caminho.py` falha com "Empty module name").
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
