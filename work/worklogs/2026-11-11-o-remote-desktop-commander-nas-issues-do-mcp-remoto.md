---
scope:
  - brza-workflow
tags:
  - infra
  - auth
refs:
  - issue:fila-de-saida-se-o-mac-dormindo-perder-correio
  - issue:proxy-remoto-de-autorizacao-no-brza-mcp
  - issue:sessao-cloud-executando-no-mac-pelo-worker
sessions:
  - 52a050a9-1a59-4d08-bab2-918957c76fe4
---

# O Remote Desktop Commander nas issues do MCP remoto

Anderson, em 2026-11-11, logo depois de registrar o `brza.dev`: "faça o mesmo com esse MCP:
https://github.com/desktop-commander/remote-desktop-commander".

## O que se fez

- **A leitura:** o README do repositório, pelo `WebFetch`. O Remote Desktop Commander é um servidor MCP hospedado em
  `https://mcp.desktopcommander.app/mcp`, com Streamable HTTP e OAuth 2.0 com PKCE. Ele repassa cada chamada a um
  agente no Mac, que se inicia com `npx @wonderwhy-er/desktop-commander@latest remote` e se pareia por device flow.
  Expõe arquivos, busca, edição e terminal (`Start Process`, `Kill System Process`). O README cita claude.ai, Claude
  Code, ChatGPT, Cursor, VS Code e Gemini CLI. Não cita o Codex nem a Claude Code Cloud. O status é "currently in
  beta", e o serviço é proprietário: o repositório só traz a documentação e os manifestos. A máquina "is reachable only
  while its device agent is running".
- **A varredura:** relay, MCP remoto, acesso remoto e celular nas notas dos workstreams. Ele afeta três issues da
  [Reunião MCP remoto: a coordenação e a proposta de arquitetura](2026-11-07-reuniao-mcp-remoto-coordenacao.md), todas no
  `playground`:
  - [A sessão Cloud executando no Mac pelo worker](../issues/sessao-cloud-executando-no-mac-pelo-worker.md): entra como
    terceiro candidato do modo G, com a pergunta de alcance pela Claude Code Cloud e o risco do serviço no meio;
  - [O proxy remoto de autorização no brza-mcp](../issues/proxy-remoto-de-autorizacao-no-brza-mcp.md): a seção nova
    diz por que ele não substitui o proxy. Com o terminal, a sessão remota roda o `brza` como chamador local e passa
    por cima do gate;
  - [A fila de saída, se o Mac dormindo perder correio](../issues/fila-de-saida-se-o-mac-dormindo-perder-correio.md):
    ele é um relay, mas não uma fila, e com o Mac suspenso a chamada falha.
- **Nada instalado:** o agente do Mac não rodou.

## O que ficou

A medida do alcance pela Claude Code Cloud ficou na issue do worker, em `## A pergunta`.

## Custo da tarefa

Corrido 2 min — agente 2 min, quem pediu 0 s, pausa 0 s · US$ 1,24 (turnos 1,24, subagentes 0,00) · CPU 4 s do `claude` e 4 s dos comandos, RSS até 384 MB · 1 turno, 1 sessão · até 22:49 de 2026-11-11, pelo `brza note commit`
