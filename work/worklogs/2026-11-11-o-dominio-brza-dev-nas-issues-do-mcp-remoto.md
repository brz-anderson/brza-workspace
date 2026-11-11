---
scope:
  - brza-workflow
tags:
  - infra
refs:
  - issue:correio-remoto-por-mcp-para-sessoes-fora-do-mac
  - issue:mcp-do-mac-no-codex-cloud
  - issue:proxy-remoto-de-autorizacao-no-brza-mcp
sessions:
  - 52a050a9-1a59-4d08-bab2-918957c76fe4
---

# O domínio brza.dev nas issues do MCP remoto

Anderson, em 2026-11-11: "agora temos domínio registrado! `brza.dev` atualize as notas dos workstreams que dependiam
disso".

## O que se fez

- **A varredura:** busquei domínio, DNS, túnel nomeado e Cloudflare nas notas, planos, wiki e memória de todos os
  workstreams. Só o `playground` dependia de domínio, na proposta da
  [Reunião MCP remoto: a coordenação e a proposta de arquitetura](2026-11-07-reuniao-mcp-remoto-coordenacao.md): a
  alternativa "proxy + túnel nomeado + Access" custava "um domínio na Cloudflare", e o D1 da rodada deixou "túnel e
  domínio só depois". As outras menções a domínio, como o `cloudId` do Jira no `studio` e a allowlist de rede dos
  runtimes, não dependiam de um domínio nosso.
- **A conferência:** `dig NS brza.dev` devolveu `piper.ns.cloudflare.com` e `sergi.ns.cloudflare.com`. O domínio está
  na Cloudflare, como o túnel nomeado pede. Ainda não há registro `A`.
- **As issues atualizadas**, com o domínio e o host como subdomínio ainda sem nome:
  - [O proxy remoto de autorização no brza-mcp](../issues/proxy-remoto-de-autorizacao-no-brza-mcp.md), na seção nova
    `## O domínio`. A ordem do D1 não muda: o proxy vem antes do túnel;
  - [O correio remoto por MCP para sessões fora do Mac](../issues/correio-remoto-por-mcp-para-sessoes-fora-do-mac.md),
    em `## O pedido`;
  - [O MCP do Mac no Codex Cloud](../issues/mcp-do-mac-no-codex-cloud.md), em `## O que se sabe`.
- **O que ficou como estava:** os worklogs da reunião, que são registro do dia.

## O que ficou

O nome do subdomínio do túnel ficou pendente na issue do proxy, em `## O domínio`. Ele se escolhe quando o túnel
entrar, depois do proxy.

## Custo da tarefa

Corrido 2 min — agente 2 min, quem pediu 0 s, pausa 0 s · US$ 1,03 (turnos 1,03, subagentes 0,00) · CPU 4 s do `claude` e 3 s dos comandos, RSS até 376 MB · 1 turno, 1 sessão · até 19:46 de 2026-11-11, pelo `brza note commit`
