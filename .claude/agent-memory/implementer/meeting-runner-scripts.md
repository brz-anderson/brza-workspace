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
- **Faça cópia dos scripts antes de editar** (o arquivo é untracked, o git não guarda o antigo): sem cópia, a prova "o teste falha no código velho" vira mutação em `scratchpad/mut/` (copytree + replace do trecho + `unittest -k`), que funcionou para 16 achados.
- **Gabarito do `levantamento-processo.md` 3.1/3.2 bate com o código:** janelas que servem de teste real: MCP R3 `21:28:13`-`21:30:48` (Muralha 0,22/41 s, Plantão 0,03/24 s, Régua 155 s/661376, Atalho 35 s); Carvão R7 `20:35:00`-`20:35:30` (Cinza 24, Lenha 20, Tição 27, Fole 21 s); janela `19:59`-`20:36` dá Tição 3,61 e Fole 3,13.
- **Prosa de nota real tem número sem `/10`** ("Régua 9 —", "Plantão: 9."): o parser aceita `N/10` ou número solto seguido de pontuação/fim, nunca seguido de palavra ("3 vezes").
- **`tally.calc_sala`/`aplica_revisor`/`raiz_padrao`/`resolve_reuniao` são a fonte única**; o `panel.py` importa o `tally` no topo (não só no `collect`). Fixture do Codex tem TZ-dependência: testes de janela usam `TZ=America/Sao_Paulo` (Medicao.setUp).

- `shlex.quote` no dry-run do `launch_persona` quota `brza sessions` e placeholders como `<chat>`; os testes assertam a forma quotada.
- O dry-run da via `agent-launch` fica byte a byte igual ao antigo (testes antigos assertam `mapa: open model=… effort=…`); só as vias novas acrescentam `via=…`.
- Os testes antigos de `wait_round.run` dependem de `source="marker"` ser o padrão da FUNÇÃO (o padrão `mailbox` fica só no `main`).
- O formato do JSON de `brza orchestration worker-start|check` não foi sondado (P4a.0 do PLN-017): a leitura é tolerante e os testes usam formatos sintéticos.
- Gravar a memória no `.claude/agent-memory/` da RAIZ do worktree, nunca relativo ao cwd: uma passada gravou em `meeting-runner/scripts/.claude/` e foi preciso limpar.
