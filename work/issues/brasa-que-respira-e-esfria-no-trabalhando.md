---
status: open
description: O "trabalhando" troca a tremulação por um halo que respira só no painel focado e esfria em 600 ms ao terminar, sem nenhum indicador preso depois do fim.
scope:
  - brza-studio
opened: 2026-11-07
priority: medium
tags:
  - design
---

# A brasa que respira e esfria no "trabalhando"

Levantado na [Reunião Carvão em Brasa: a coordenação e a proposta de plano](../worklogs/2026-11-07-reuniao-carvao-em-brasa-coordenacao.md). A chama de 18 px tremula hoje no degradê âmbar; a sala quer que a brasa viva no estado, e
não na decoração.

## O pedido

- Só o halo da chama de 13 px do cabeçalho do painel focado respira: 2,4 s, só opacidade. Glifo e texto constantes.
  Reusar `data-native-chat-working` (`NativeChatStructuredSession.tsx:259-260`).
- Painéis não focados que trabalham: 06 parada (3,10:1 no pior fundo). A 05 parada dá 2,76:1 e reprova.
- Ao terminar, esfria em 600 ms até `#8E8C90`. Com `prefers-reduced-motion`, nada anima, nem o esfriar.
- Sem fagulha por ferramenta, sem modo noturno: Fole mediu que o `#E05A20` noturno fica a ΔE 8,7 da Claude, mais perto
  que a 07.
- **Teste de "brasa presa"** (Cinza): interromper, cancelar, desconectar e restaurar sessões com vários agentes;
  nenhum indicador segue "trabalhando" depois do término confirmado.

## O que a reunião levantou

Cinco de seis a favor, depois da correção da 05 para a 06, apontada pelo Cinza e pela Lenha. Fole defendeu uma fagulha
por ferramenta e cedeu; Fogareiro quer o modo noturno reavaliado no futuro.

Fontes: [Reunião Carvão em Brasa: a participação de Lenha, a Engenheira Pragmática](../worklogs/2026-11-07-reuniao-carvao-em-brasa-lenha.md), [Reunião Carvão em Brasa: a participação de Tição, o Guardião](../worklogs/2026-11-07-reuniao-carvao-em-brasa-ticao.md), [Reunião Carvão em Brasa: a participação de Cinza, o Cético Analítico](../worklogs/2026-11-07-reuniao-carvao-em-brasa-cinza.md).
