---
status: open
description: O PR #37710 e as issues #37701, #37707 e #37733 do upstream trazem abertura de agentes em Chat UI via CLI, paridade de superfície na orquestração e correções de limites de payload local.
scope:
  - brza-studio
  - brza-workflow
priority: high
opened: 2026-11-03
tags:
  - chat
  - tooling
---

# Abertura de agentes no Chat UI pela CLI e superfície chat na orquestração

Rastreado do PR aberto no upstream [`stablyai/orca#37710`](https://github.com/stablyai/orca/pull/37710) e das issues
[`stablyai/orca#37701`](https://github.com/stablyai/orca/issues/37701),
[`stablyai/orca#37707`](https://github.com/stablyai/orca/issues/37707) e
[`stablyai/orca#37733`](https://github.com/stablyai/orca/issues/37733).

## O problema

1. **Agentes criados via CLI forçados em PTY terminal (`#37710`):** ao rodar `brza terminal create --command ...` com
   scripts wrapper, variáveis de ambiente ou argumentos de permissão customizados, a aba abre sempre como terminal
   cru. O comando `agent launch --surface chat` não atende porque o runtime reconstrói o comando do agente e ignora
   o comando exato do chamador.
2. **Orquestração sem paridade de superfície (`#37701`):** `orchestration worker-start` não aceitava `--surface chat|terminal`,
   ficando em desacordo com `agent launch --surface` e impedindo que workers de tópicos fossem iniciados com a interface
   gráfica de chat por padrão.
3. **Falha na transição de TUI para Chat UI (`#37707`):** no Claude Code, alternar de TUI para Chat UI falhava com
   recusa de lançamento estruturado ("Orca couldn't confirm what happened").
4. **Erro espúrio de mismatch de ID em payloads grandes (`#37733`):** o transporte de socket Unix local limita payloads
   a 1 MiB; requisições maiores (como specs de orquestração detalhadas) falhavam com erro enganoso `mismatched response id`.

## O que o upstream propõe e implementa

- **No PR `#37710`:** adiciona `--command-agent <agent> --view-mode chat` ao `terminal create`, valida compatibilidade
  via capability `terminal.create-view-mode.v1` e preserva o comando original enquanto renderiza a aba no Chat UI.
- **Na issue `#37701`:** propõe `orchestration worker-start ... [--surface chat|terminal]` com eco no receipt (`surface`,
  `terminal` handle), garantindo paridade entre workers e agentes isolados.
- **Nas issues `#37707` e `#37733`:** estabiliza o handshake entre o modo TUI e Chat UI no Claude Code e aumenta/trata o
  teto de bytes nas requisições RPC de transporte local para specs volumosas.

## O que fazer

Portar o PR `#37710` para o `brza-studio` e adotar `--command-agent` / `--view-mode chat` nos disparos de sessão do
`brza-workflow`, permitindo que agentes com wrappers proprietários rodem diretamente na superfície de Native Chat.
