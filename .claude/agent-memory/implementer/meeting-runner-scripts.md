---
name: meeting-runner-scripts
description: scripts da skill meeting-runner sobre o brza sessions v2 (PLN-017 P7) — formato do mapa, armadilhas do teste integrado e do relógio falso, comando que valida
metadata:
  type: project
---

**Valida:** `cd /private/tmp/mr3-skill && PYTHONDONTWRITEBYTECODE=1 python3 -I -m unittest discover -s scripts/tests -p 'test_*.py'`
(251 OK em 2026-11-09); apague os `__pycache__` depois. Teste vermelho contra o snapshot anterior:
`MR_SCRIPTS=/private/tmp/mr3-ws/skill-snapshot/scripts python3 -I -m unittest discover -s scripts/tests -p 'test_X.py'`
(os testes importam por `tests/_paths.py`, que honra `MR_SCRIPTS`; módulo novo importa com `try/except ImportError` para o
erro sair por teste e não por arquivo).

**Mapa v2** (`.sessions/sessions.jsonl`, só `sessions_map.fold_map` o lê): `open` traz `dispatch, run, sender, coordinator,
agent, model, effort, operation/round_id` e NÃO traz o id do provedor quando o app ainda não o deu; o `session` chega depois
(`--wait` do `open`, ou o `wait`). O `open` é o `last_send` da R1 (o `at` dele é o início da rodada 1). `close` só é gravado
quando o worker foi LIBERADO (`released`); `closing`/`stop_unknown` não gravam nada. No Claude `provider_session` == id do
transcript (o hook mede por ele).

**Armadilhas de teste**
- Fake de relógio: loop com `clock` fixo e `wait_fn` que volta na hora gira para sempre (travou a suíte). O fake tem de avançar
  o relógio por `timeout` quando nada chega e ~5 s quando chega `done` (o `--any` do v2 volta na hora).
- `def run(..., clock=time.time)` amarra o `time.time` na definição; para o teste poder trocar, `clock=None` e resolver dentro.
- Integração: `SourceFileLoader` do `brza-sessions` real + `setattr` no módulo (`brza, rpc, send_to_chat, provider_session,
  coordinator_identity, open_tabs, running, config_dirs, WORKSPACE, SESSION_MAP, time`); `time` trocado por um `FakeTime`
  (monotonic/sleep/time) e o MESMO objeto em `wait_round.time`. `BRZA_REGISTRY=/nonexistent` antes do import. O contrato do
  argparse: `by_name(argv)` com os `*_command` trocados por fakes; o `open` não tem verbo, entra por `main()` com `--dry-run`
  (o prompt-file precisa existir). `BrzaError(msg, body={"error": {"code": "stop_unknown"}})` dá o `error.code`.
- macOS: `sed -i` pede `''`; edite arquivo de teste por script Python, não por `sed -i`.

**Achados do v2 (só leitura, repassados à coordenação)**
- `worker_state` (brza-sessions:564) lê `dispatch.status` ANTES de `worker.state`; no `worker-show` real o primeiro é `completed`/
  `dispatched` e nunca casa com `('succeeded', ...)`: o `close` de worker já encerrado volta `closing`, e o `worker_done` do
  `wait` nunca vira `settled`. Os testes do v2 usam fakes com `dispatch.status='succeeded'`, por isso passam.
- O marcador `<!-- fim-rodada-N -->` só vale como última linha; o `brza note commit` acrescenta `## Medida` depois dele, e o
  `tally`/`wait_round` leem o worklog commitado como `falta`.

**Painel automático (2026-11-09, PLN-017)**
- Valida: `cd <worktree>/.claude/skills/meeting-runner && PYTHONDONTWRITEBYTECODE=1 python3 -I -m unittest discover -s scripts/tests -p 'test_*.py'`
  (317 OK). Teste novo do painel: `tests/test_painel_automatico.py`; fixtures reais em `tests/fixtures/tev1/`.
- O `wait_round.main` agora publica painel por padrão (chama o Chrome): todo teste que chama `main` sem querer o painel passa
  `--no-panel`, ou troca `panel.gera_png` por um fake; senão a suíte fica lenta e depende do Chrome.
- `corta_medida` (common.py) corta `## Medida` e `## Custo da tarefa`, só se o cabeçalho vier DEPOIS do último marcador e
  nada de nível 1-2 vier depois dele; parágrafo extra dentro do bloco do anexo é cortado junto (é parte do bloco).
- `panel.py` tem `publica_rodada` (collect+grava estado+render+PNG, em processo), `salva_visual` e `gera_png(…, altura)`; o
  `brza shot` confere o PNG (devolve 2x a largura pedida). PNG da síntese pede janela alta (4200), a do painel é 2000.
