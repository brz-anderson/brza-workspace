---
scope:
  - workspace
refs:
  - PLN-009
  - issue:o-dispatch-aceita-chamador-fora-do-studio
---

# O PLN-009: o MCP rodando e o C4 pelo chat do Studio

Anderson pediu para ver o MCP do
[PLN-009: O servidor MCP residente coordena o fluxo de trabalho nos dois clients](../../plans/PLN-009-o-mcp-orquestrador-do-fluxo/PLN-009-plan.md)
rodando. O teste usou o `brza-workflow@007383a`, da `feat/pln-009-mcp`.

## O servidor de pé

Com a fila vazia, o `brza mcp start` saiu 0 (pid 34093), e o `status` também. Pelo `curl`:
- o `/health` deu 200 com o token e 401 sem ele;
- o `initialize` respondeu como `brza-orchestrator 0.1.0`;
- o `tools/list` trouxe `dispatch`, `status` e `config`;
- o `tools/call status` devolveu a fila vazia e os tetos.

Na rodada, Anderson escolheu "Ligar numa sessão (Recomendado)". **O escopo local não serviu:**
- O `claude mcp add-json --scope local` gravou o servidor na chave da raiz da `master` no `~/.claude.json`. Ali ele
  valeria em todos os workstreams.
- Na chave do worktree, o CLI não o acha.
- A entrada foi desfeita, e a sessão de teste abriu no terminal com `--mcp-config`, num arquivo de `/private/tmp`.
- O token vinha por um `headersHelper` que lê `~/.brza/runtime/mcp.token`. O `claude-brza` instalado aponta a `master`
  do `brza-workflow`, que ainda não exporta a `BRZA_MCP_TOKEN`.
- Antes de abrir a sessão, uma sessão headless pelo Haiku chamou o `status` pelo MCP, e ele respondeu.

## O dispatch do terminal e o C4

**Do terminal, o `dispatch` falhou.** Foi o pedido 1, `collector`:
- O `caller` veio do argumento, `tools-kit-mcp-teste`, porque a sessão não tem `ORCA_AGENT_SESSION_ID` nem manda o
  `X-Brza-Session`.
- O gate abriu e foi aprovado.
- O `run-create` voltou `session_caller_unknown`, sem efeito no Studio.

Na rodada, Anderson escolheu "Disparar daqui (C4) (Recomendado)" e "Issue no tools-kit (Recomendado)" para o achado.

**O C4 passou pelo chat do Studio**, numa sessão com o `X-Brza-Session` e o `X-Brza-Client` dela:
- foi o pedido 2, um `consultant` sem gate;
- abriu run, task e worker no Studio;
- terminou em 17 s, com o `worker_done` "C4: 13 issues open";
- o `task-list` mostrou a task `completed`.

O Observado está no C4 do plano. O achado virou
[O dispatch aceita chamador fora do Studio](../issues/o-dispatch-aceita-chamador-fora-do-studio.md), no commit
`20d10b2`.

Na última rodada, Anderson escolheu:
- "Aprovado (Recomendado)" para o C4, gravado como veredito;
- "Parar agora (Recomendado)" para o serviço.

O `stop` saiu 0, o `status` 3 e o plist foi apagado.

**O que fica no PLN-009:**
- o C2 e o C3;
- a confirmação do merge;
- as issues das pendências.

## Candidato à norma

O `claude mcp add --scope local` rodado num worktree grava na chave da raiz da `master`, como o `claude plugin install`
que o `CLAUDE.md` já descreve, e na chave do worktree o CLI não acha o servidor. Vale para todos os workstreams:
sobe à norma por rodada, sem mexer nela daqui.

## Fora do workspace

- **O LaunchAgent `com.brza.orchestrator`:**
  - **O quê e onde:** carregado pelo `brza mcp start` (pid 34093), com o plist em `~/Library/LaunchAgents/`.
  - **Risco:** o plist subiria o serviço da `feat` no login.
  - **Estado:** descarregado pelo `brza mcp stop`, sem plist.
  - **Como desfazer:** nada a desfazer.
- **A fila do orquestrador, `~/.brza/orchestrator.db`:**
  - **O quê e onde:** ganhou o pedido 1 (`failed`), o pedido 2 (`done`) e os workers deles.
  - **Risco:** a próxima subida não despacha nenhum dos dois, porque já terminaram.
  - **Estado:** ficam.
  - **Como desfazer:** apagar o arquivo, com o serviço parado.
- **O Studio:**
  - **O quê e onde:** o run `run_482348be0728`, com a task `task_767283dce2dc` concluída e o worker do consultor.
  - **Risco:** nenhum, porque o worker só leu.
  - **Estado:** concluído.
  - **Como desfazer:** nada a desfazer.
- **O `~/.claude.json`:**
  - **O quê e onde:** a entrada `brza-orchestrator`, gravada pelo `claude mcp add-json --scope local`.
  - **Risco:** o servidor em todas as sessões do workspace.
  - **Estado:** removida pelo mesmo script que a moveu.
  - **Como desfazer:** nada a desfazer.
- **O `/private/tmp/brza-mcp-test.json`:**
  - **O quê e onde:** o `--mcp-config` da sessão de teste, sem segredo.
  - **Risco:** nenhum.
  - **Estado:** apagado.
  - **Como desfazer:** nada a desfazer.
