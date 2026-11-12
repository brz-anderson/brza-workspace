---
scope:
  - workspace
  - brza-studio
  - brza-workflow
tags:
  - planning
refs:
  - PLN-011
  - PLN-010
  - PLN-003
  - PLN-014
---

# Priorização: issues high × planos abertos × Context7

## O que foi feito

Pedido nesta sessão (cloud agent no `workstream/playground`): verificar as issues de maior prioridade, cruzar com os
planos abertos em todos os workstreams e buscar provas na documentação via Context7.

### Inventário (índice + frontmatter vivo)

| Recorte | Número |
| :------ | -----: |
| Issues abertas (todos os workstreams) | 143 |
| `priority: high` | 49 |
| `priority: medium` | 22 |
| `priority: low` | 42 |
| Sem `priority` | 30 |
| Planos abertos | 13 |

Régua do [`work/README.md`](../README.md): `blocks` e fato antes do rótulo `priority`.

### Cadeia que trava (fato > rótulo)

```text
PLN-011 (studio, high, phase: blocked)
  blocks: merge da fase 1 e passos seguintes aguardam C1 de Anderson
  ready: recompilar app de dev a partir da branch feat/pln-011-chat-cli e rodar C1
    │
    ▼
PLN-010 (tools-kit, high, phase: interview)
  depends_on: PLN-011
  ready: "não — falta o contrato do brza chat (R5 do PLN-011) no studio"
    │
    ▼
issue high tools-kit: brza-sessions-sobre-o-brza-chat
issue high studio: brza-chat-list-read-send-no-studio
issue high playground: ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins
```

Conferido na ponta remota do `brza-studio`: `feat/pln-011-chat-cli` em `0ca6ac7` (merge da v1.4.256). Os handlers
`src/cli/handlers/chat.ts` e os testes de cursor/fila/recibo estão na branch. O C1 continua manual no app de dev.

### PLN-014 trava o radar

O [PLN-014](../../plans/PLN-014-refinamento-do-radar-do-playground/PLN-014-plan.md) está `phase: interview` com
`blocks: A emenda das issues e qualquer porte esperam a entrevista deste plano.` Em 2026-11-04 eram quinze issues; em
2026-11-12 o playground sozinho tem **47** `high` abertas (radar de 6h). Nada se emenda e nada se porta antes da R1.

### Único high pronto sem bloqueio de pessoa

| Plano | Fase | Próximo |
| :---- | :--- | :------ |
| [PLN-003](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-plan.md) | `execution` | **P4** — plugin Claude com skills/hooks; há desvio aberto (distribuir via `brza-workflow` + MCP do PLN-009 em vez de `plugins/claude/` estático) |

O [PLN-009](../../plans/PLN-009-o-mcp-orquestrador-do-fluxo/PLN-009-plan.md) já está `done`; o MCP em
`brza-workflow/packages/mcp` autentica com `Authorization: Bearer` (`brza_mcp/server.py`, `cli.py`).

### Outros planos abertos (não high / não bloqueantes da cadeia)

| Plano | Workstream | Fase | Prioridade |
| :---- | :--------- | :--- | :--------- |
| PLN-001 | studio | execution | — |
| PLN-004 | workspace | interview | — |
| PLN-007 | brand | execution | — |
| PLN-015 | tools-kit | design | medium |
| PLN-016 | logi-options | interview | medium |
| PLN-019 | playground | interview | — |
| PLN-020 | playground | design | medium |
| PLN-021 | playground | execution | medium |
| PLN-022 | sdd-process | interview | — |

### Provas Context7 (documentação, não claim de produto)

1. **MCP Authorization (spec 2025-11-25)** — HTTP **SHOULD** seguir OAuth 2.1; clientes **MUST** implementar PKCE (`S256`
   quando capaz); servidores **MUST** expor Protected Resource Metadata (RFC9728). STDIO **SHOULD NOT** usar esse
   framework e lê credenciais do ambiente. Fonte:
   `https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization`.
   Cruza com
   [Autenticação MCP no chat…](../issues/autenticacao-mcp-no-chat-alerta-de-turnos-ativos-e-cache-de-orquestracao.md)
   (`high`) e com o `.mcp.json` do PLN-003/P4 (`Bearer ${BRZA_MCP_TOKEN}`).

2. **Electron `utilityProcess` / sandbox** — `NodeService` de `utilityProcess.fork` vem com
   `ServiceSandbox=kNoSandbox`; `nodeIntegration` desliga sandbox do renderer por padrão. Fonte: docs Electron
   (`tutorial/sandbox.md`, `api/utility-process.md`, mojom `node_service.mojom`). Cruza com o achado do studio
   *O worker de plugin sem sandbox alcança o token do runtime* (sem `priority` no frontmatter; risco condicional a
   instalar plugin com worker).

3. **Contraste / acessibilidade** — WAI-ARIA APG exige contraste WCAG 2.1 para texto e controles sobre imagem, e
   atenção a `forced-colors` / High Contrast. Cruza com
   [A auditoria automática de contraste…](../issues/auditoria-automatica-de-contraste-e-daltonismo-dos-tokens.md)
   (`high`, playground) — porte só depois da R1 do PLN-014.

### Ordem operacional gravada nesta passagem

1. **C1 do PLN-011** — runbook em [Runbook C1 do PLN-011](../notes/2026-11-12-runbook-c1-pln-011.md). Só Anderson no
   Mac destrava o `blocks`.
2. **Desenho do PLN-010** — insumos em [Insumos do Desenho do PLN-010](../notes/2026-11-12-insumos-desenho-pln-010.md);
   o Desenho na branch `tools-kit` espera o contrato confirmado pelo C1.
3. **PLN-003/P4** — briefing em [Briefing do PLN-003/P4](../notes/2026-11-12-briefing-pln-003-p4.md); sessão do
   `tools-kit`, depois de fechar o desvio de distribuição.
4. **R1 do PLN-014** — reapresentada no Retomar do plano e abaixo; nenhuma issue emendada.
5. **Segurança do worker** — proposta em
   [O default dos plugins e o alcance do worker sem sandbox](../decisions/o-default-dos-plugins-e-o-alcance-do-worker-sem-sandbox.md).

### R1 do PLN-014 (reapresentada)

Perguntas e opções iguais ao D1 do plano; recomendação inalterada (A1). Nada executado antes da resposta.

1. **Destino do PLN-014.** A1 (regra de despacho) · A2 (gate de setup) · A3 (dropar o plano).
2. **Issue de chats.** Fica `open` com ponteiro aos PLN-011/010 · Passa a `done` com handoff.
3. **Parêntese nos 7 arquivos com número fechado.** Entra nesta passagem · Fica para outra.

## O que não foi decidido / não rodou aqui

- C1 no app de dev (pede Mac + Anderson).
- Código do PLN-003/P4 (workstream `tools-kit`; desvio de distribuição em aberto).
- Resposta da R1 do PLN-014.
- Fechamento da decisão do worker de plugin.

## Fora do workspace

- Clone raso só-leitura em `/tmp/repos/brza-studio` e `/tmp/repos/brza-workflow` para conferir a branch
  `feat/pln-011-chat-cli` e o Bearer do MCP. Sem alteração nesses clones.
