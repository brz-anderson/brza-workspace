---
status: open
description: O Enviar fica no carvão quando vazio e acende na brasa quando há texto ou anexo válido, e o foco de teclado vira um anel neutro separado da marca.
scope:
  - brza-studio
opened: 2026-11-07
priority: medium
tags:
  - design
---

# O Enviar acende por disponibilidade, e o foco é um anel neutro

Levantado na [Reunião Carvão em Brasa: a coordenação e a proposta de plano](../worklogs/2026-11-07-reuniao-carvao-em-brasa-coordenacao.md). É **a recomendação mais forte da reunião** (6/6, índice 88,0), e contraria o protótipo, que
punha o Enviar na 07 o tempo todo — o próprio protótipo admitia que "o foco muda menos".

## O pedido

- Vazio: Enviar no `#2C2D31` com a seta `#8E8C90`. Com texto ou anexo válido: `--action-brand` com a seta `#1A1B1E`.
  Reusar `imageBlock`, `hasDraft` e `sendButtonDisabled` de `native-chat-composer-send-state.ts:39-59`.
- Foco de teclado: anel sólido de 2 px com offset de 2 px — `#BCBCBC` no escuro, `#1A1B1E` no claro. O offset é
  obrigatório: o anel encostado na 07 dá 1,87:1.
- Parar: semântica própria, no rosa do erro, não na marca.

## O que a reunião levantou

- Tição: "um sinal que nunca muda deixa de informar". Fogareiro: a "lanterna permanente na visão periférica".
- Risco (Faísca, Cinza): o Enviar apagado parecer botão morto na primeira sessão. Derruba a proposta um teste com mais
  falhas de descoberta do Enviar, sobretudo com anexos, que a versão atual.

Fontes: [Reunião Carvão em Brasa: a participação de Lenha, a Engenheira Pragmática](../worklogs/2026-11-07-reuniao-carvao-em-brasa-lenha.md), [Reunião Carvão em Brasa: a participação de Cinza, o Cético Analítico](../worklogs/2026-11-07-reuniao-carvao-em-brasa-cinza.md), [Reunião Carvão em Brasa: a participação de Fogareiro, o Advogado do Usuário](../worklogs/2026-11-07-reuniao-carvao-em-brasa-fogareiro.md).
