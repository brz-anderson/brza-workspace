---
status: done
description: O código do servidor MCP residente mora em brza-workflow/packages/mcp/, ligado pelo brza install, e não no repositório público da CLI
scope:
  - workspace
  - brza-workflow
opened: 2026-11-03
decided: 2026-11-03
decided_by: Anderson
tags:
  - tooling
---

# O código do MCP mora no `brza-workflow`, em `packages/mcp/`

**O servidor MCP residente — o `brza-mcp` e o pacote `brza_mcp` — mora em `~/Projects/brza-workflow/packages/mcp/`,
roda desse checkout e é ligado pelo `brza install --mcp`. Ele não vai ao repositório público `brz-anderson/brza`, que
fica com a CLI e os plugins.** A PLN-003/R5.3 tinha posto "CLI, MCP, os dois plugins" no repositório público; para o
MCP, ela foi reaberta aqui.

Decidido por Anderson em 2026-11-03, na sessão do `tools-kit`: "brza-workflow (Recomendado)" (PLN-009/R1.1). Sobre o
texto, em 2026-11-06, na sessão do `tools-kit` que fechou o PLN-009: "pode gravar", com o texto inteiro na mensagem.

## Fundamento

- **Quando a R1.1 foi respondida, o `brz-anderson/brza` não existia:** o `gh repo view` respondeu "Could not resolve to
  a Repository" (PLN-009/R1). O `brza-workflow` já tinha `packages/client`, `bin/brza-*` e o `brza install`, desde
  2026-10-31 (PLN-006/P1).
- **A alternativa recusada foi publicar o `brz-anderson/brza` antes.** Custava ~4 h e um push público sem código, e
  pararia 22,5 h de MCP. O repositório local `~/Projects/brza` também ficou de fora: ~15 min a mais e uma segunda base
  de testes e de instalação.
- **O repositório público nasceu depois, só com a CLI:** criado em 2026-11-04 pelo PLN-003/P3
  (`brza-workspace@8d8042f`), com `brza/`, `Formula/`, `pyproject.toml` e `tests/`, sem o MCP.

## Onde vale

- `brza-workflow/README.md`, na linha do `packages/mcp/`, escrita no PLN-009/P1 (`1dfc9d9`) e mesclada em `23d812d`.
- PLN-003/R5.3, com "→ reaberta em PLN-009/R1.1", em `plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-interview.md`.
- Decidido em PLN-009/R1.1, no
  [PLN-009: O servidor MCP residente coordena o fluxo de trabalho nos dois clients](../../plans/PLN-009-o-mcp-orquestrador-do-fluxo/PLN-009-plan.md).
