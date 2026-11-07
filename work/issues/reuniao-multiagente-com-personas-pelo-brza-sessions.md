---
status: open
description: A reunião de seis personas em quatro runtimes pelo `brza sessions` funcionou, e deixou o que corrigir para virar fluxo: marcador de fim, medição fora do Claude e personas calibradas.
scope:
  - brza-workflow
  - workspace
opened: 2026-11-07
priority: medium
tags:
  - tooling
---

# A reunião multiagente com personas pelo `brza sessions`

Levantado na [Reunião Carvão em Brasa: a coordenação e a proposta de plano](../worklogs/2026-11-07-reuniao-carvao-em-brasa-coordenacao.md). A reunião de mini-rebranding testou, no `playground`, um fluxo novo: seis personas em seis
sessões de chat (dois Claude, dois Codex, um Grok, um Antigravity), coordenadas pelo `brza sessions` e
`brza sessions send`, com cinco rodadas e uma síntese da coordenação entre cada uma.

## O pedido

Decidir se o fluxo vira skill (por exemplo, `meeting-runner`) e corrigir o que a reunião mostrou:

- **O marcador de fim de rodada:** o briefing dizia "no fim do arquivo" e o pedido da rodada dizia "dentro da seção";
  três personas puseram o marcador nos dois lugares. O monitor por `grep` do marcador funcionou.
- **A latência por runtime:** Codex 1–2 min por rodada, Claude 2 min, Antigravity 1–2 min, Grok 7 min (agente
  `grok-build-plan` com raciocínio `xhigh`) — o Grok ficou uma rodada atrás e fez as rodadas 3 e 4 numa só vez.
- **A medição:** só as sessões Claude entram no `.measurements/measurements.jsonl`; o custo do Codex sai dos
  `token_count` do rollout em `~/.codex/sessions/`, e o do Grok e do Antigravity não sai.
- **A calibração das personas:** a persona empática (Antigravity) deu confiança média de 93 com a evidência mais fraca
  e o único número errado; a cética (Codex) deu seis votos contra e foi a mais bem avaliada pelos colegas.
- **Os dados movem mais que os argumentos:** a medição de daltonismo da coordenação causou três viradas na rodada 2.
- **O `--title` do `brza sessions`** é trocado pelo nome no Claude e no Codex.
- **O `brza shot` não roda** contra o `brza-studio` atual: "não achei BASE_CSS em
  `src/shared/native-chat/native-chat-visual-shell.ts`; o brza-studio mudou, e o brza-shot precisa acompanhar". A
  folha de contato do símbolo saiu do Chrome headless (`--headless=new --force-device-scale-factor=1|2 --screenshot`).
- **A evidência renderizada destravou o assunto mais fraco:** o símbolo foi de 64,5 a 79,7 de confiança com duas
  rodadas curtas sobre uma folha de contato — vale como passo padrão do fluxo quando a disputa é visual.
- **O `brza sessions` não repassa `--model` nem `--effort`** ao `brza agent launch`, que os aceita; a contraprova usou
  um lançador no scratch que importa a biblioteca do `brza sessions` e registra o nome no mesmo mapa. Falta a opção no
  próprio `brza sessions`, e um jeito de trocar o modelo de um chat aberto.
- **O chat do Antigravity recusa modelo explícito:** `gemini-4-argon[-high]`, `gpt-oss-120b`, `gemini-3.8-flash[-low]`
  voltaram "not available for the current authentication method", embora o `agy models` os liste.
- **A posição é da persona; a confiança, a extensão e a latência são do modelo.** A contraprova (as mesmas personas em
  outros modelos, contexto limpo) repetiu as posições; o Fogareiro caiu de 89 para 67 de confiança ao sair do Gemini
  3.8 Flash (High) para o Haiku 5.5 `low`; a Faísca no Grok Fast `low` foi nove vezes mais rápida sem perder ousadia.
  O fluxo deve escolher o modelo pelo papel, e medir a confiança com sessões que não escreveram o plano.
- **O revisor independente ficou 12 pontos abaixo da sala** (74 contra 85,8 na v3) e achou o que as seis personas não
  acharam (os mixes do chat, o estilo inline, os portões que não se mediam): vale como etapa fixa antes do aceite.

Fontes: os seis worklogs da reunião e a [Reunião Carvão em Brasa: a coordenação e a proposta de plano](../worklogs/2026-11-07-reuniao-carvao-em-brasa-coordenacao.md).
