---
status: open
description: O erro e o aviso saem do matiz da brasa — rosa frio `#FF7AA2` e limão `#FACC15` —, porque hoje colidem com a 07 em deuteranopia.
scope:
  - brza-studio
opened: 2026-11-07
priority: high
tags:
  - design
---

# O erro e o aviso saem do matiz da brasa

Levantado na [Reunião Carvão em Brasa: a coordenação e a proposta de plano](../worklogs/2026-11-07-reuniao-carvao-em-brasa-coordenacao.md): com a Brasa Incandescente `#FF3D00` como cor de ação, o erro de hoje `#ff6568` fica a 15° de
matiz dela e a **ΔE2000 10,3 em deuteranopia** (simulação de Machado 2009, severidade 1). O aviso `#eab308` cai a 12,1.
Abaixo de ~15 a triagem já marca risco de confusão.

## O pedido

Trocar os tokens de erro, de diff removido e de aviso no chat, nos dois temas, e manter ícone, texto e o sinal `−`/`+`
como pistas obrigatórias — nenhum estado depende só da cor.

| Sinal | Escuro | Claro | Medido |
| :---- | :----- | :---- | :----- |
| Erro, diff removido | `#FF7AA2` | `#6E3C5A` (a testar) | 7,02:1 no 01; 4,91 no pior hover; ΔE 22,6 da 07 em deuteranopia |
| Aviso | `#FACC15` | texto e ícone `#1A1B1E`, fundo `#FACC15` a 12% | 11,25:1 no 01; ΔE 17,3 da 07 em deuteranopia |

- **O diff removido também colide:** `#c74e39` contra a Brasa Viva dá 1,03:1 (Faísca).
- **No claro, o ocre não serve:** um aviso escuro legível no papel (`#7A5C00`) fica a ΔE 2,2 da brasa de texto 05 em
  deuteranopia; e o rosa claro `#B4235A` falha a triagem de tritanopia contra a 05 (ΔE 3,1). Daí o `#6E3C5A` da
  auditoria do Cinza.

## O que a reunião levantou

- Seis de seis votaram a favor (índice 77,6 no erro e 78,0 no aviso). Lenha defendia manter o `#ff6568` na rodada 1 e
  virou pelo dado de daltonismo; Fogareiro trocou o carmesim `#FF3366` (ΔE 11,4) pelo rosa.
- Tição: "manter um erro que parte dos usuários não separa do CTA não é conservar, é negligenciar."
- O risco: o rosa quebra o reflexo "vermelho = erro". Derruba a proposta um teste com pessoas com deficiência de cor em
  que o rosa seja lido como "não é erro" mais que o vermelho.

## Critério de pronto

- Os pares passam na auditoria automática ([A auditoria automática de contraste e daltonismo dos tokens](auditoria-automatica-de-contraste-e-daltonismo-dos-tokens.md)).
- O teste de tarefas não registra confusão entre erro e CTA.

Fontes: [Reunião Carvão em Brasa: a participação de Tição, o Guardião](../worklogs/2026-11-07-reuniao-carvao-em-brasa-ticao.md), [Reunião Carvão em Brasa: a participação de Cinza, o Cético Analítico](../worklogs/2026-11-07-reuniao-carvao-em-brasa-cinza.md), [Reunião Carvão em Brasa: a participação de Faísca, a Provocadora](../worklogs/2026-11-07-reuniao-carvao-em-brasa-faisca.md).
