---
name: pln021-skill-reuse-map
description: Onde moram os blocos reutilizáveis da meeting-runner, os verbos reais do brza sessions, a cobertura do check_notes e os tokens do Studio (levantamento do PLN-021, 2026-11-09)
metadata:
  type: reference
---

- `brza sessions`: sem verbo `open` (abrir = `brza sessions <nome> …`; `open`/`worker-show` viram NOME no help). `worker-show` é `brza orchestration worker-show --dispatch`. Verbos reais: list, send, wait, close, read --last, model, title, usage.
- meeting-runner/scripts: `sessions_map.py` é 100% genérico; corredores/`interpreta_abertura`/`*_argv` em `launch_persona.py:149-212`; medição em `tally.py:459-550`; `salva_visual` em `panel.py:519`. `gera_png` usa Chrome headless, não `brza shot`. Testes: `scripts/tests/`, `python3 -m unittest discover -s .` (323 OK, ~10 s).
- `check_notes.py` não confere soma de horas, IDs R/D/P/X, `[x]` com evidência (só `hours-not-a-number`, `finding-without-evidence`). plan-runner não tem scripts.
- Fonte velha: `PLN-017-design-painel.md:247` diz "brza shot quebrado"; PLN-017/P5 consertou e rodei: funciona.
- Tokens do Studio: `brza-studio/src/renderer/src/assets/main.css` (:root :194, .dark :330), mobile `mobile/src/theme/mobile-theme.ts`; sem tailwind.config (v4). `brza print` = simulador iOS/adb/janela Mac.
- `/private/tmp/<nome>` pode ser symlink para o scratch da sessão: gravar nele funciona.
