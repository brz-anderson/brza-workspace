---
status: open
description: As quatro filhas leem a mesma brasa de um `brand.tokens.json`, com reserva ANSI 256 no BrzA CLI, para não derivarem na próxima recoloração.
scope:
  - brza-studio
  - brza-workflow
opened: 2026-11-07
priority: low
tags:
  - design
---

# A brasa nas quatro filhas, com tokens compartilhados e o CLI

Levantado na [Reunião Carvão em Brasa: a coordenação e a proposta de plano](../worklogs/2026-11-07-reuniao-carvao-em-brasa-coordenacao.md). **Tição e Fole chegaram à mesma ideia, cada um por um caminho, na rodada 3**: ninguém tinha
falado do BrzA CLI nem do Workspace, e sem eles "Carvão em Brasa é tema de um app, e não marca" (Fole).

## O pedido

- Um `brand.tokens.json` com os primitivos `--brz-*`, lido pelo app, pelo CLI e pelo workspace, e auditado pelo mesmo
  portão de contraste.
- No CLI (tabela do Tição): o "A" do `BrzA` em `#FF3D00`, ANSI 202 de reserva; erro `#FF7AA2`, ANSI 211; aviso
  `#FACC15`, ANSI 220; secundário `#A8A29E`, ANSI 248. Em 16 cores, a brasa fica sem cor, só negrito, para não virar o
  vermelho do erro. Com `NO_COLOR` ou sem TTY, nada de cor.
- O CLI não desenha a chama: a marca no terminal é o wordmark.

## O que a reunião levantou

Lenha deixou fora do mapa de implementação: pede escopo e custo próprios.

Fontes: [Reunião Carvão em Brasa: a participação de Tição, o Guardião](../worklogs/2026-11-07-reuniao-carvao-em-brasa-ticao.md), [Reunião Carvão em Brasa: a participação de Fole, a Estrategista de Marca](../worklogs/2026-11-07-reuniao-carvao-em-brasa-fole.md).
