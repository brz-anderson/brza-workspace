---
status: open
phase: interview
origin: request
ready: não — falta a rodada do MCP (R1.3, a medir), a medição do worker de plugin e a detecção do client
scope:
  - workspace
  - brza-studio
opened: 2026-10-29
owner: Anderson
tags:
  - tooling
---

# PLN-003: O workflow do workspace roda igual no BrzA Studio e no Orca, por plugins e pelo `brza`

- **Retomar:** a rodada 1 fechou o escopo. Falta medir as três formas do MCP (R1.3) e o que o worker de plugin do
  Orca alcança (fs, processo), e fazer a rodada da detecção do client e do despacho `brza X` no Orca.

## Pedido

- **Origem:** pedido livre, no chat do BrzA Studio de 2026-10-29. Relaciona-se com o
  [PLN-002](../PLN-002-os-comandos-brza/PLN-002-plan.md), sem depender do P7 dele (R1.4).

"vamos criar um plugin do Orca para o Workspace e um plugin do Claude + MCP para o Workflow e ajustar a CLI `brza` para
que o workflow funcione tanto no client `BrzA Studio` quanto no `Orca`" — Anderson, em 2026-10-29.

Os itens do pedido, numerados para a Cobertura:

1. o plugin do Orca para o Workspace;
2. o plugin do Claude com o MCP para o Workflow — o fluxo do workspace e o recurso Workflow do Claude Code (R1.1);
3. a CLI `brza` ajustada para o workflow funcionar no BrzA Studio e no Orca.

### Cobertura

> Rascunho: os critérios são propostas até a rodada que os confirma; o passo e o teste saem do Desenho.

| Origem     | Critério de aceite                                                                                      | Passo | Teste (nível) |
| :--------- | :------------------------------------------------------------------------------------------------------ | :---- | :------------ |
| `Pedido 1` | o mesmo `orca-plugin.json` instala nos dois apps e mostra o painel do workspace com planos e notas abertos | —     | —             |
| `Pedido 1` | os comandos do plugin mandam o `brza` certo ao terminal do worktree em foco                             | —     | —             |
| `Pedido 2` | o plugin do Claude traz as skills, os hooks e o MCP do workspace, e sobe nos chats dos dois apps          | —     | —             |
| `Pedido 2` | o plugin traz roteiros de Workflow do Claude Code para o fluxo do workspace                               | —     | —             |
| `Pedido 3` | `brza <sub>` acha o app que está rodando — BrzA Studio ou Orca — sem caminho fixo                        | —     | —             |

## Entrevista

### Rodada 1 — o escopo (enviada 2026-10-29)

**Apresentado antes:**
- **O sistema de plugins do Orca existe e é do upstream**, herdado pelo BrzA Studio: manifesto `orca-plugin.json`
  (`brza-studio/src/shared/plugins/plugin-manifest.ts`), com `panels`, `commands`, `events`; capacidades fechadas —
  `workspace:read`, `terminal:send`, `notifications:show`, `storage`, `secrets`, `events:subscribe`, `settings:own`
  (`plugin-capabilities.ts:7-15`). Nenhuma lê arquivo nem chama o CLI. Cada app lê o próprio `userData`.
- **A CLI `brza` fora do app só serve ao BrzA Studio**: caminhos fixos em `scripts/brza/brza_runtime.py:15-23`; dentro
  de um terminal de qualquer app, `cli_command()` e `user_data()` já seguem `ORCA_CLI_COMMAND` e `ORCA_USER_DATA_PATH`.
  O despacho `brza X` → `brza-X` só existe no fork (`brza-studio/src/cli/external-subcommand.ts`).
- **Não há MCP próprio** (`AGENTS.md`, `CLAUDE.md`); a issue `codex-como-subagente-no-chat-do-claude.md` propõe um.
- **O PLN-002 está bloqueado no P7** (`brza sessions`).

Respondida em 2026-10-29, no chat do BrzA Studio.

1. **O que é o "Workflow".** Opções:
   - o fluxo do workspace — planos, notas, worklogs, sessões, os `brza-*` (recomendada). Custo: ~0,5 h para delimitar.
     Se paga: no desenho do MCP;
   - o recurso Workflow do Claude Code, roteiros `agent()` no plugin. Custo: alto. Se paga: só para roteiros multi-agente
     pelo app;
   - os dois. Custo: dobra o escopo. Se paga: numa fase posterior.

   **Decidido — os dois.**

2. **O que o plugin do Orca faz.** Opções:
   - painel com planos, notas e worklogs abertos, mais comandos que mandam `brza` ao terminal; o mesmo manifesto nos
     dois apps (recomendada). Custo: ~6–10 h, mais ~1 h para medir o fs do worker antes. Se paga: na 1ª versão, nos dois
     apps;
   - só comandos e eventos. Custo: ~3 h. Se paga: agora, sem a visão do estado do workspace;
   - sem plugin do Orca. Custo: ~0. Se paga: se a interface do app não for o objetivo.

   **Decidido — painel e comandos.**

3. **O que o MCP expõe.** Opções:
   - as operações do fluxo, tipadas sobre o `brza_runtime`, em stdio, no plugin do Claude (recomendada). Custo: ~1–2 h
     por ferramenta. Se paga: quando a ferramenta com schema bater o Bash;
   - só o que a CLI não alcança — estado do app, `agentSession`, cartões no chat. Custo: ~4 h. Se paga: no 1º uso;
   - um MCP dentro do app. Custo: alto, muda o fork. Se paga: depois, e só no BrzA Studio.

   **Resposta:** "meça prós e contras dos 3 e registre no plano" — as três vão ao Desenho como alternativas medidas, e a
   escolha volta numa rodada.

4. **Onde o plano mora.** Opções:
   - `PLN-003`, sem depender do P7 do PLN-002 (recomendada). Custo: retrabalho se o P7 mudar o contrato. Se paga: agora;
   - `PLN-003` com a parte de sessões depois do P7. Custo: espera a 2d. Se paga: quando o P7 fechar;
   - estender o PLN-002. Custo: plano bloqueado fica maior. Se paga: nunca.

   **Decidido — `PLN-003`, sem depender do P7.**

## Worklogs

