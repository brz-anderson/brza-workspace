---
name: meeting-runner-scripts
description: Armadilhas de teste e de dados dos scripts da skill meeting-runner (tally, wait_round, launch_persona, runtime_memory_check) no playground
metadata:
  type: project
---

Os scripts moram em `.claude/skills/meeting-runner/scripts/` (link curto `/private/tmp/mr-skill` na delegação). Comando que valida:
`cd /private/tmp/mr-skill && python3 -I -m unittest discover -s scripts/tests -p 'test_*.py'`; apague os `__pycache__` depois.

- **Os worklogs reais de 2026-11-07 não terminam no marcador:** os de Carvão têm `## O que ficou` depois dele, e os da MCP só têm marcador no fim da última rodada. A regra "última linha = `fim-rodada-M` com M >= N" dá `falta` em todos os de Carvão; o teste de aceite não depende do `estado`.
- **Prosa das notas da MCP varia por persona** (lista, linha única, `**Régua (10/10):**`): a regex por nome, `Nome[\W_]{0,8}?<nota>`, cobre todas; só existe nota na R3.
- **A média da sala 61,8 inclui o Cartógrafo (Antigravity):** a conta `sala.media` do manifesto tira ele (57,2); `media_todas` guarda a de seis.
- **Medição real confere com `estado-r3.json`** (Muralha 41 s/US$ 0,22; Régua 155 s e 661376 tokens): rode o `tally.py 3 --opened 21:28:13 --closed 21:30:48 --out - --json` na raiz do worktree. `measurements.jsonl` e `sessions.jsonl` estão na raiz comum do git, e o `repo_roots` os acha.
- **Teste que mexe em hora local** fixa `TZ=America/Sao_Paulo` com `time.tzset()`; os rollouts do Codex têm timestamp em `Z`.
- **`brza-sessions` importa `brza_runtime` no `exec_module`**: só carregue no caminho real, nunca no `--dry-run`.
