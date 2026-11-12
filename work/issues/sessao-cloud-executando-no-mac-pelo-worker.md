---
status: open
type: unknown
description: Medir o worker My Machines do Cursor e o ambiente self-hosted do Claude, em que o agente Cloud executa as ferramentas no Mac e usa o correio local sem túnel.
scope:
  - workspace
opened: 2026-11-07
priority: medium
tags:
  - tooling
  - infra
---

# A sessão Cloud executando no Mac pelo worker

Levantado na [Reunião MCP remoto: a coordenação e a proposta de arquitetura](../worklogs/2026-11-07-reuniao-mcp-remoto-coordenacao.md). É o modo 1 da proposta (G), que a coordenação achou no `--help` durante a reunião.

## A pergunta

- `cursor-agent worker` sem `--pool`: "a personal My Machines worker (no Enterprise plan needed)" que executa as
  ferramentas do Cloud Agent neste Mac, só por conexão de saída. O agente enxerga o `brza`, as sessões e os MCPs
  locais? O que o celular mostra quando o worker morre?
- `claude --environment <ccpool_…>`: o que é preciso para registrar o Mac como ambiente self-hosted?
- [Remote Desktop Commander](https://github.com/desktop-commander/remote-desktop-commander), um terceiro candidato, que
  entrou em 2026-11-11. É um servidor MCP hospedado (`https://mcp.desktopcommander.app/mcp`, Streamable HTTP, OAuth 2.0
  com PKCE) que repassa a chamada a um agente no Mac (`npx @wonderwhy-er/desktop-commander@latest remote`). Não pede
  túnel nem domínio. Expõe arquivos, busca e terminal (`Start Process`, `Kill System Process`). O README cita claude.ai,
  Claude Code, ChatGPT, Cursor, VS Code e Gemini CLI; não cita o Codex nem a Claude Code Cloud. Está em beta e o
  serviço é proprietário: o repositório só traz a documentação. Falta medir se a Claude Code Cloud com a rede padrão
  alcança o host dele, já que recusou o do nosso túnel (M7 da reunião).

## O risco

O agente Cloud ganha o poder de uma sessão local: quem controla a conta do Cursor ou do claude.ai controla o Mac.
No Remote Desktop Commander, o mesmo vale para a conta do serviço e para o próprio serviço, que fica no meio de toda
chamada. Com o terminal, a sessão remota roda o `brza` como chamador local e passa por cima do gate que o
[O proxy remoto de autorização no brza-mcp](proxy-remoto-de-autorizacao-no-brza-mcp.md) protege.
Registrar o worker muda estado fora do workspace e vai ao worklog do dia.
