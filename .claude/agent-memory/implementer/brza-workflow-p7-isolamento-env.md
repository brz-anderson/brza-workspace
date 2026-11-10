---
name: brza-workflow-p7-isolamento-env
description: Isolamento do ambiente da sessão nos testes do brza note (X9 do PLN-012) e linha de base de falhas de tests/cli
metadata:
  type: project
---

- `NoteFixture.setUp` (tests/cli/test_brza_note.py) é o ponto único: `patch.dict(os.environ)` e `pop` de `SESSION_ENV` (BRZA_WORKSPACE, CLAUDE_CODE_SESSION_ID, ORCA_AGENT_SESSION_ID, MEASURE_DIR…). Só o `brza note commit` grava `task`; todo teste dele herda de `NoteFixture`. Prova do X9: contagem de `"event": "task"` no log real antes/depois de rodar `tests/cli` com o ambiente da sessão.
- Linha de base da `master` (ffa29fe), ambiente limpo: 26 falhas + 1 erro, todas em `test_brza_sessions`; com o ambiente da sessão o conjunto muda (outras 4), então compare sempre no ambiente limpo (`env -u BRZA_WORKSPACE -u CLAUDE_CODE_SESSION_ID -u ORCA_AGENT_SESSION_ID -u BRZA_STUDIO`). `tests/cli` leva ~220 s.
- Rodar um teste só: `cd tests/cli && python3 -m unittest test_brza_note.X` (o `-s tests/cli` não põe o módulo no path de outro cwd).
- As fixtures `tests/hooks/fixtures/golden/master/` são cópias manuais dos arquivos do core (com os `{{…}}` resolvidos); sem gerador, edite as duas.
