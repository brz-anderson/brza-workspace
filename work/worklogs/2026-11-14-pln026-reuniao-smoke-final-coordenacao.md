---
scope:
  - workspace
tags:
  - tooling
---

# A reunião smoke final do PLN-026 não conta para a promoção

**SMOKE.** Esta reunião não conta para a promoção da meeting-runner. As duas posições ficam registradas. O modelo padrão não muda por causa dela.

CloudRuntime: `61e47ed6acb028b3feb4f2bf17db4f425266a93a` em `packages/client/bin/cloud_runtime.py`, ainda fora da master do brza-workflow.

Prova final do P8 do [PLN-026: brza sessions e meeting-runner funcionam na cloud](../../plans/PLN-026-sessoes-e-meeting-runner-na-cloud/PLN-026-plan.md), contra `61e47ed6acb028b3feb4f2bf17db4f425266a93a`, que inclui o PR #3 em `ed7d91ba8265cfd7e5cd6dd2a3fbf5572bcd69df`. Mesma pauta e as mesmas personas da smoke 2. Não conta para a promoção da meeting-runner.

## Pauta

Devemos manter `grok-4.7-low` como modelo padrão das personas de reunião smoke?

## Personas

| Persona | papel | modelo | modo |
| :------ | :---- | :----- | :--- |
| Arquiteto | propõe | grok-4.7-low | agent |
| Revisor | critica | grok-4.7-low | ask |

## Rodada 1

Duração da rodada: 110236 ms.

| Persona | turno | session_id | duração_ms | input | output | cache_read | cache_write | reasoning | custo |
| :------ | :---- | :--------- | ---------: | ----: | -----: | ---------: | ----------: | --------: | :---- |
| Arquiteto | open | `d75e6665-9209-4963-af6d-f7cdae28ee5f` | 2717 | 18503 | 75 | 0 | 0 | 73 | ausente |
| Arquiteto | send | `d75e6665-9209-4963-af6d-f7cdae28ee5f` | 5921 | 17521 | 269 | 1152 | 0 | 79 | ausente |
| Revisor | open | `bddb46b5-9e37-44f8-bcc4-afe20498b5cf` | 3357 | 18814 | 75 | 0 | 0 | 73 | ausente |
| Revisor | send | `bddb46b5-9e37-44f8-bcc4-afe20498b5cf` | 8863 | 19248 | 344 | 0 | 0 | 78 | ausente |

## Votos

| Persona | voto |
| :------ | :--- |
| Arquiteto | manter `grok-4.7-low` como padrão; override só local se o modelo for o limite |
| Revisor | manter o padrão, e recusar override local enquanto a falha não for separada de prompt e parser |

## Prova

SHA testado: `61e47ed6acb028b3feb4f2bf17db4f425266a93a`. Ele contém `ed7d91ba8265cfd7e5cd6dd2a3fbf5572bcd69df`.

```bash
git -C /agent/repos/brza-workflow rev-parse HEAD
```

rc 0. Saída: `61e47ed6acb028b3feb4f2bf17db4f425266a93a`.

```bash
env -u CURSOR_API_KEY BRZA_WORKFLOW_DIR=/agent/repos/brza-workflow python3 .claude/skills/meeting-runner/scripts/launch_persona.py /tmp/pln026-smoke-final/reuniao.json --transport cloud --round 1
```

rc 0. Relógio 2026-11-14 18:52:59–18:54:49 UTC. Duração da rodada 110236 ms. Custo `ausente` nos quatro turnos. O open e o send de cada persona usam o mesmo `session_id`: Arquiteto `d75e6665-9209-4963-af6d-f7cdae28ee5f`, Revisor `bddb46b5-9e37-44f8-bcc4-afe20498b5cf`. O Revisor foi com `--mode ask`.

`leak_count` 0 em 6 arquivos (ata, log, stdout, stderr, manifesto e o registro do watcher). `CURSOR_API_KEY` ausente no processo pai. `~/.config/cursor/auth.json` ausente antes e depois. Durante a rodada o watcher viu o home e o `auth.json` de cada persona, e não viu `.cursor/chats`. Depois do `close()`, `~/.local/share/brza/cloud-runtime/Arquiteto` e `Revisor` não existem, e `.cursor/chats` dentro deles também não.

<!-- fim-rodada-1 -->
