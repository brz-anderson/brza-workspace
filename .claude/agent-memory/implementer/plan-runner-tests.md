---
name: plan-runner-tests
description: como rodar a suíte do plan-runner e armadilhas dos testes de painel e executor
metadata:
  type: project
---

Suíte: `cd .claude/skills/plan-runner/scripts && python3 -I -m unittest discover -s tests` (205 testes em 2026-11-12).
Testes de executor/painel herdam `tests/_exec.py` (`Base`, relógio falso de 1 s por leitura). Plano de teste: `mini.step`/`plan`
com `_paths.plan_tmp`. Painel: `brza shot <html> <png> --width 736|375` e ler o PNG; o contêiner do painel é `.panel` (`container-type:inline-size`).
