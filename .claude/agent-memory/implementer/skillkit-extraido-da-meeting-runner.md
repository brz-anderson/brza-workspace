---
name: skillkit-extraido-da-meeting-runner
description: o código comum das skills mora em .claude/scripts/skillkit (PLN-021 P1); como a meeting-runner importa dele, quais nomes os testes trocam e o que valida
metadata:
  type: project
---

**Valida (2026-11-09):** do worktree, `python3 -I -m unittest discover -s ".claude/scripts/tests"` (55 OK) e
`python3 -I -m unittest discover -s ".claude/skills/meeting-runner/scripts/tests"` (323 OK, sem mudar teste). Apague os `__pycache__`.

- Cada script da skill faz `sys.path.insert(0, AQUI); import _kit` antes de `from skillkit import …` (o `-I` não põe a pasta no
  `sys.path`). `SKILLKIT=/nope` faz o import falhar.
- A `meeting-runner` mantém os nomes que os testes trocam por atribuição como atributos do módulo (`wait_round.wait_brza`,
  `panel.gera_png`, `launch_persona.run_sessions`); `wait_round.BRZA` também fica (um teste lê). `wait_brza` do kit devolve
  `(rc, dict)`, não só dict (o teste da skill espera a tupla).
- `visual.gera_png` troca por `visual._run`/`visual._chrome`; o `brza shot` mede a altura sozinho (`altura` só vale ao Chrome).
  Painel real: `panel.py render tests/fixtures/estado-r3.json --out X.html --png X.png` -> 736 px de largura, altura medida.
- `salva_visual`: o 2º parâmetro é `prefixo` (o `reuniao.id` na meeting-runner); o `ErroPublicacao` é do kit e o `panel` o reexporta.
