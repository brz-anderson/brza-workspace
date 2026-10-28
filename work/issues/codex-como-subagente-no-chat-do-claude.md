---
status: open
scope:
  - brza-studio
  - workspace
opened: 2026-10-28
tags:
  - chat
  - tooling
---

# O Codex chamado pela sessão Claude aparece como subagente no chat do BrzA Studio

Sugestão de melhoria de Anderson, em 2026-10-28, numa sessão da Fixfy que estudava como o chat nativo lê e escreve
arquivos: uma chamada ao Codex, feita pela sessão principal em Claude, aparecer no chat como se fosse um subagente.

## Como o chat monta um subagente hoje

O chat do Claude roda o `claude` instalado pelo `@anthropic-ai/claude-agent-sdk` 0.3.284, em stream-json, e o cartão de
subagente nasce **só** do stream desse processo. A sessão chama a ferramenta `Agent`, o stream traz os quadros `system`
`task_started`, `task_progress` e `task_notification`, e cada mensagem do filho chega com o `parent_tool_use_id` da
chamada (`src/main/claude/claude-subagent-task-frames.ts` e `src/main/claude/claude-subagent-linkage.ts`). O que roda
fora do processo `claude` não vira subagente. Os caminhos foram conferidos no `brza-studio` `9747ac2`.

## Os dois caminhos

**1. Um agente Claude que embrulha o Codex.** Funciona hoje, sem mexer no `brza-studio`. É um agente em
`.claude/agents/`, num modelo barato, que roda `codex exec --json -s read-only …` pelo Bash e devolve o resultado. A
sessão principal o chama pelo `Agent`, e o chat mostra o cartão de subagente com nome, estado, duração e resposta final.
Dentro do cartão aparece só a chamada de Bash, e não os passos do Codex. O custo é o de um Claude intermediário. Depende
do `delegate.py`, que está adiado em
[Os scripts de orquestração da Fixfy que ficaram fora do port para o BrzA](scripts-da-fixfy-fora-do-port-para-o-brza.md),
ou de chamar o `codex exec` direto.

**1b. Um colega de equipe que embrulha o Codex.** É o caminho 1 com as equipes de agentes do Claude Code
(`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`) no lugar do subagente. O `brza-studio` já as suporta no terminal: o
`src/main/runtime/claude-agent-teams-service.ts` liga a flag e põe um falso `tmux` no `PATH`, e cada colega abre como
painel dividido, ou no modo `in-process`. O colega é sempre um `claude`, porque é ele que troca mensagens com o líder, e
por isso o Codex continua precisando de um Claude que o embrulhe. A troca, contra o caminho 1:

- **ganha** a conversa: quem pediu fala direto com o colega no painel — com o Claude que embrulha, não com o Codex;
- **perde** o cartão: o colega aparece num painel do terminal, e não no chat, o contrário do que a sugestão pede. No
  chat, o `brza-studio` só trata o hook `TeammateIdle`, que estaciona colegas ociosos
  (`src/main/claude/claude-managed-hook-events.ts:28`);
- **custa mais**: cada colega é uma sessão inteira, com contexto próprio e vida longa.

Não mudam o caminho 2 nem a ressalva de permissão.

**2. Os passos do Codex dentro do cartão.** Precisa de feature no `brza-studio`. O app já traduz os itens do Codex em
linhas do chat, inclusive os subagentes do próprio Codex (`src/main/codex/codex-collab-agent-item-translation.ts`), e o
registro das linhas é genérico: cada uma diz qual agente a produziu e quem é o pai (`AgentJournalProducerLinkage`, em
`src/shared/agent-session-journal-types.ts:364`). Quando a sessão Claude disparar o Codex, o processo principal leria o
`--json` ou o rollout em `~/.codex/sessions/`, traduziria os itens com o tradutor que já existe e os gravaria como
filhos da chamada que disparou o Codex. Reconhecer a chamada fica mais firme com o agente do caminho 1, ou com uma
ferramenta de MCP própria, do que com `codex exec` dentro de um Bash qualquer. A mudança cai nos arquivos de chat mais
mexidos no upstream. É da família do correio recolhível, estimado em ~15 h na medição da Fixfy, e não foi medida.

**A forma do caminho 2 é um MCP do BrzA Studio.** Hoje o app não serve MCP nenhum: só lê e espelha a configuração de
MCP dos runtimes, e as sessões ACP abrem com `mcpServers: []` (`src/main/acp/acp-session-runtime.ts:143`). Mas o
processo principal já fala com o Codex pelo `app-server` (`src/main/codex/app-server/`). Com um servidor próprio, a
sessão Claude chamaria uma ferramenta como `brza.codex_run`, e o chat receberia no stream o `tool_use_id` dela. O app
rodaria o Codex pelo `app-server`, traduziria os itens com o tradutor que já existe e os gravaria como filhos daquele
id. Isso tira duas peças:

- **o reconhecimento por heurística** de um `codex exec` dentro de um Bash qualquer;
- **o Claude intermediário** do caminho 1, e o custo dele a cada chamada.

O mesmo servidor abre três usos:

- **a conversa com o Codex**, por uma segunda ferramenta, como `codex_reply(thread, mensagem)`, que continua a mesma
  thread do `app-server`. Quem pediu digitar dentro do cartão seria outra feature, maior;
- **o `agy`**, pela conexão ACP que o app já tem, com uma ferramenta genérica de delegar ao runtime no lugar do
  `delegate.py` adiado;
- **o correio entre contas**, que o `SendMessage` não cruza e hoje vai por arquivo, porque o app hospeda as sessões
  das duas contas; e a criação de worktree e de sessão como ferramenta tipada, no lugar da CLI `orca` pelo Bash.

Os contras:

- **só vale com o app aberto**: a sessão aberta no terminal comum fica sem a ferramenta, e o caminho 1 ou o
  `codex exec` direto continuam como alternativa;
- **esbarra na norma do ferramental**, que o quer só no escopo do projeto: o servidor injetado pelo app na hora de
  abrir a sessão seria uma segunda exceção, como os hooks do Orca, e pede decisão;
- **um servidor local que abre o Codex com escrita pede token**, no padrão que o app já usa nas equipes
  (`ORCA_AGENT_TEAMS_TOKEN`);
- **cada ferramenta ocupa contexto** em toda sessão, para sempre;
- **o custo não foi medido** para este desenho.

A conversa com o Codex só existe com o `codex_reply` do MCP, e a conversa com o Claude que o embrulha só no caminho 1b.
No caminho 1 e no 2 sem MCP, o cartão é só exibição.

**3. O chat só orquestra, e o subagente abre como sessão de terminal.** Ideia de Anderson, em 2026-10-28, que vira o
caminho 2 do avesso: em vez de trazer os passos do Codex para dentro do chat, o chat deixa de rodar subagente. Com o
MCP do BrzA Studio e a CLI `brza`, a sessão do chat, quando vai chamar um subagente, abre uma sessão de terminal no app
— Claude, Codex ou `agy` — e acompanha por ela. O chat fica como a visão de quem orquestra, e cada subagente vira uma
aba de terminal com a conversa inteira, onde quem pediu pode entrar e falar direto. É a troca do caminho 1b sem a flag
experimental das equipes e sem o Claude que embrulha o Codex: o runtime do subagente é qualquer um que o app abra no
terminal. Não foi medida, e a sessão que pegar a issue confere antes:

- **o que o chat mostra da sessão aberta**: um cartão que aponta para a aba, com estado e resposta final, ou nada, e
  como a resposta volta à sessão que orquestra — pela ferramenta do MCP, que espera o fim, ou por correio;
- **se o `Agent` nativo continua**: o chat passa a abrir sessão para todo subagente, ou só para o que não é Claude;
- **o custo**: cada subagente vira uma sessão inteira, com contexto próprio e vida longa, como o colega do caminho 1b.

## A ressalva de permissão

O `canUseTool` do chat aprova só o Bash que liga o Codex. O que o Codex faz depois roda sob a sandbox e a política de
aprovação dele, e o cartão de permissão não as vê. Para leitura e revisão, o `-s read-only` basta. Para escrita, a
proteção tem de estar na configuração do Codex.

Com o MCP, a chamada passa pelo `canUseTool` com os argumentos à vista, e a sandbox pedida — `read-only` ou
`workspace-write` — vira um argumento que o servidor impõe. O que o Codex faz dentro dela continua fora do cartão.

## O que falta decidir

A sugestão da sessão de origem é começar pelo caminho 1, que dá o cartão agora e mede se o uso pega, e só abrir o
caminho 2 se ver os passos do Codex no chat fizer falta, na forma de MCP. A sessão que pegar a issue mede antes
dois pontos, porque cada um pode mudar o desenho:

- **se o chat consegue dar um servidor de MCP ao `claude` que ele abre**, por `--mcp-config` ou por servidor no
  próprio processo, como o Agent SDK permite. Todo o MCP depende disso;
- **se o modo `in-process` das equipes, numa sessão de chat em stream-json, emite algum quadro** que o chat pudesse
  virar cartão. Se emitir, o colega do caminho 1b apareceria no chat, e a troca dele muda.

Depois, a entrevista:

- **o caminho:** o 1 sozinho, o 1b, o 1 como passo para o 2, direto o 2, ou o 3, com o chat só orquestrando;
- **a forma do caminho 2:** o MCP do BrzA Studio ou o reconhecimento do `codex exec` no Bash; com o MCP, quais
  ferramentas além do `codex_run` — o `codex_reply`, o `agy`, o correio entre contas — e a exceção na norma do
  ferramental;
- **o que o agente chama:** o `codex exec` direto ou o `delegate.py` portado, o que antecipa o gatilho dele;
- **a sandbox:** só `read-only`, ou também `workspace-write` num worktree, com a proteção na configuração do Codex.
