---
name: plan-runner-executor-consult-panel
description: executor.py, consult.py e plan_panel.py do plan-runner (PLN-021 P3-P5) — armadilhas do brza wait, dos testes e da prova com o brza falso
metadata:
  type: project
---

**Valida:** `cd <worktree> && PYTHONDONTWRITEBYTECODE=1 python3 -I -m unittest discover -s ".claude/skills/plan-runner/scripts/tests"` (151 OK em 2026-11-10).
Prova: `. /private/tmp/pln021/p3-env.sh` (PATH com o brza falso, `BRZA_BIN`, sem `ORCA_CHAT_SCRATCH_DIR`) dentro da cópia do `make_repo.sh`.
No zsh, `$S` com espaço não divide: use `python3 -I $S/executor.py` com `S=` só o caminho.

- O `--marker` do `brza sessions wait` vale para TODAS as sessões (exige todos os marcadores): com 2 passos/consultores o script
  não o passa e confere o marcador do worklog sozinho. `wait --any` volta na hora com `ended_without_marker` num turno já
  terminado: o laço precisa de `sleep`, senão gira.
- Os testes trocam `executor.run_sessions/run_brza/wait_brza/run_shell/list_states` e `plan_panel.publica_seguro` por atribuição
  (`tests/_exec.py`, com `FakeClock` que avança a cada leitura). `round_log.main`/`plan_state.main --fix` agora publicam o painel:
  os helpers `cli` dos testes do P2 passam `--no-panel`. Nunca `del` função de módulo no teste: restaure.
- `.sessions/` do plano fica na raiz do worktree; o painel por padrão grava em `.sessions/pln-nnn/painel/` se não houver
  `ORCA_CHAT_SCRATCH_DIR`. Pergunta com só `**Resposta:**` não conta como "decidida" no painel.
