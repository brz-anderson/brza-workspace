---
scope:
  - brza-workflow
  - brza-studio
tags:
  - chat
  - tooling
---

# Insumos do Desenho do PLN-010

Rascunho do dia para a sessão do `tools-kit` retomar o
[PLN-010](../../plans/PLN-010-brza-sessions-sobre-o-brza-chat/PLN-010-plan.md) assim que o C1 do PLN-011
fechar. Origem:
[Priorização: issues high × planos abertos × Context7](../worklogs/2026-11-12-priorizacao-issues-high-planos-e-context7.md).

## Gate

- `depends_on: PLN-011` — sem o contrato confirmado pelo C1, o Desenho não grava aceite.
- `ready` atual: falta o contrato do `brza chat` no studio.

## Contrato já rascunhado na Cobertura do PLN-011 (consumir, não reinventar)

| Superfície | Forma esperada pelo PLN-010 |
| :--------- | :-------------------------- |
| `list` | `--json` com `session`, `handle`, `worktree`, `title` |
| `read` | cursor `epoch:sequence`; página `after`; `nextCursor` / `hasNewer`; cursor inválido com reset explícito |
| `send` | recibo com fila (`held_by: question\|working\|null`), outcomes `accepted` / `queued` / `rejected` / `pending` / `unknown`; `--operation` idempotente |
| Origem | `ORCA_AGENT_SESSION_ID` / `orchestrationCompatibilityEvidence` |

## Pontos do Desenho (fase 1 high)

1. Aliases `brza sessions list/read/send` → `brza chat` do Studio, resolução por nome no mapa.
2. Códigos de saída alinhados à R2.1 do PLN-010 (0 / 1 / 75) vs. os do Studio (0 / 1 / 3) — mapear ou adotar.
3. Exceção transitória PLN-017/R3.1 (`rpc` para recibo / `--operation` / `read --last`) até o app alvo ter `brza chat`.
4. Se o `brza-run` mantém o exit code do comando e só anexa o recibo (ponto aberto no Retomar).

## Fora desta nota

Implementação e testes ficam na branch `workstream/tools-kit`. Este arquivo só empacota o que a auditoria fechou.
