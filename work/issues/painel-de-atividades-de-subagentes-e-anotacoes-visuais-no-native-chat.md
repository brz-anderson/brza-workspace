---
status: open
description: Subagentes do Claude mantidos concluidos (#49959), desfecho de handoff de bots (#49960, #49937), cartoes de perguntas sem truncamento (#49948) e cores ultrathink (#49849).
scope:
  - brza-studio
  - brza-workflow
priority: high
opened: 2026-11-05
tags:
  - chat
  - tooling
references:
  - https://github.com/stablyai/orca/pull/42455
  - https://github.com/stablyai/orca/pull/48862
  - https://github.com/stablyai/orca/pull/48904
  - https://github.com/stablyai/orca/pull/48833
  - https://github.com/stablyai/orca/pull/48929
  - https://github.com/stablyai/orca/issues/49015
  - https://github.com/stablyai/orca/issues/49009
  - https://github.com/stablyai/orca/issues/49033
  - https://github.com/stablyai/orca/issues/48928
  - https://github.com/stablyai/orca/issues/48930
  - https://github.com/stablyai/orca/issues/49048
  - https://github.com/stablyai/orca/pull/48089
  - https://github.com/stablyai/orca/pull/48787
  - https://github.com/stablyai/orca/pull/48792
  - https://github.com/stablyai/orca/pull/48767
  - https://github.com/stablyai/orca/pull/48667
  - https://github.com/stablyai/orca/pull/48809
  - https://github.com/stablyai/orca/pull/48575
  - https://github.com/stablyai/orca/pull/48762
  - https://github.com/stablyai/orca/issues/48752
  - https://github.com/stablyai/orca/issues/48697
  - https://github.com/stablyai/orca/issues/48665
  - https://github.com/stablyai/orca/issues/48780
  - https://github.com/stablyai/orca/issues/48830
  - https://github.com/stablyai/orca/pull/48581
  - https://github.com/stablyai/orca/pull/48564
  - https://github.com/stablyai/orca/pull/48598
  - https://github.com/stablyai/orca/pull/48472
  - https://github.com/stablyai/orca/pull/48528
  - https://github.com/stablyai/orca/pull/48609
  - https://github.com/stablyai/orca/pull/48666
  - https://github.com/stablyai/orca/issues/48602
  - https://github.com/stablyai/orca/pull/48353
  - https://github.com/stablyai/orca/pull/48425
  - https://github.com/stablyai/orca/pull/48415
  - https://github.com/stablyai/orca/pull/48430
  - https://github.com/stablyai/orca/pull/48451
  - https://github.com/stablyai/orca/issues/48445
  - https://github.com/stablyai/orca/issues/48461
  - https://github.com/stablyai/orca/pull/48289
  - https://github.com/stablyai/orca/pull/49227
  - https://github.com/stablyai/orca/pull/49204
  - https://github.com/stablyai/orca/pull/49256
  - https://github.com/stablyai/orca/pull/49264
  - https://github.com/stablyai/orca/issues/49240
  - https://github.com/stablyai/orca/issues/48386
  - https://github.com/stablyai/orca/issues/49056
  - https://github.com/stablyai/orca/issues/37646
  - https://github.com/stablyai/orca/pull/49286
  - https://github.com/stablyai/orca/pull/49447
  - https://github.com/stablyai/orca/pull/35462
  - https://github.com/stablyai/orca/pull/49422
  - https://github.com/stablyai/orca/pull/49288
  - https://github.com/stablyai/orca/pull/49451
  - https://github.com/stablyai/orca/pull/49439
  - https://github.com/stablyai/orca/issues/49431
  - https://github.com/stablyai/orca/issues/49310
  - https://github.com/stablyai/orca/issues/49295
  - https://github.com/stablyai/orca/issues/49285
  - https://github.com/stablyai/orca/issues/43861
  - https://github.com/stablyai/orca/issues/30156
  - https://github.com/stablyai/orca/pull/49643
  - https://github.com/stablyai/orca/pull/49619
  - https://github.com/stablyai/orca/pull/49612
  - https://github.com/stablyai/orca/pull/49560
  - https://github.com/stablyai/orca/pull/49574
  - https://github.com/stablyai/orca/pull/49507
  - https://github.com/stablyai/orca/pull/49493
  - https://github.com/stablyai/orca/issues/49646
  - https://github.com/stablyai/orca/issues/49614
  - https://github.com/stablyai/orca/issues/49575
  - https://github.com/stablyai/orca/issues/49562
  - https://github.com/stablyai/orca/issues/49549
  - https://github.com/stablyai/orca/issues/49508
  - https://github.com/stablyai/orca/pull/49959
  - https://github.com/stablyai/orca/pull/49960
  - https://github.com/stablyai/orca/pull/49879
  - https://github.com/stablyai/orca/issues/49948
  - https://github.com/stablyai/orca/issues/49937
  - https://github.com/stablyai/orca/issues/49886
  - https://github.com/stablyai/orca/issues/49849
  - https://github.com/stablyai/orca/issues/49777
  - https://github.com/stablyai/orca/issues/49967
---

# Painel de atividades de subagentes e anotações visuais no Native Chat

Rastreado dos PRs no upstream [`stablyai/orca#48289`](https://github.com/stablyai/orca/pull/48289) (commit `c69dc71bca9`),
[`stablyai/orca#48223`](https://github.com/stablyai/orca/pull/48223),
[`stablyai/orca#48216`](https://github.com/stablyai/orca/pull/48216),
[`stablyai/orca#48271`](https://github.com/stablyai/orca/pull/48271),
[`stablyai/orca#48247`](https://github.com/stablyai/orca/pull/48247),
[`stablyai/orca#48237`](https://github.com/stablyai/orca/pull/48237),
[`stablyai/orca#48316`](https://github.com/stablyai/orca/pull/48316) (commit `f36d846d17b`),
[`stablyai/orca#48302`](https://github.com/stablyai/orca/pull/48302) (commit `06f5660cb08`),
[`stablyai/orca#48268`](https://github.com/stablyai/orca/issues/48268),
[`stablyai/orca#48269`](https://github.com/stablyai/orca/issues/48269),
[`stablyai/orca#48296`](https://github.com/stablyai/orca/issues/48296),
[`stablyai/orca#48124`](https://github.com/stablyai/orca/pull/48124) (commit `374693b1414`),
[`stablyai/orca#48129`](https://github.com/stablyai/orca/pull/48129) (commit `f7ddeb3f630`),
[`stablyai/orca#48126`](https://github.com/stablyai/orca/pull/48126) (resolve Issue [`#48123`](https://github.com/stablyai/orca/issues/48123)),
[`stablyai/orca#48074`](https://github.com/stablyai/orca/pull/48074),
[`stablyai/orca#48089`](https://github.com/stablyai/orca/pull/48089),
[`stablyai/orca#48078`](https://github.com/stablyai/orca/pull/48078) (resolve Issue [`#48077`](https://github.com/stablyai/orca/issues/48077)),
[`stablyai/orca#48076`](https://github.com/stablyai/orca/pull/48076),
[`stablyai/orca#48128`](https://github.com/stablyai/orca/pull/48128),
[`stablyai/orca#48038`](https://github.com/stablyai/orca/pull/48038) (commit `c6594b2c249`, resolve Issue [`#48025`](https://github.com/stablyai/orca/issues/48025)),
[`stablyai/orca#48154`](https://github.com/stablyai/orca/pull/48154),
[`stablyai/orca#48081`](https://github.com/stablyai/orca/pull/48081) (commit `bb95a42edc5`),
[`stablyai/orca#47999`](https://github.com/stablyai/orca/pull/47999) (commit `4e8e3501e6f`),
[`stablyai/orca#48064`](https://github.com/stablyai/orca/pull/48064) (commit `74d17605a62`),
[`stablyai/orca#48139`](https://github.com/stablyai/orca/pull/48139) (commit `5d1726ce567`),
[`stablyai/orca#47980`](https://github.com/stablyai/orca/pull/47980) (commit `60b0cbaea7e`),
[`stablyai/orca#47949`](https://github.com/stablyai/orca/pull/47949) (refs Issue [`#43461`](https://github.com/stablyai/orca/issues/43461)),
[`stablyai/orca#47975`](https://github.com/stablyai/orca/pull/47975),
[`stablyai/orca#47875`](https://github.com/stablyai/orca/pull/47875),
[`stablyai/orca#47872`](https://github.com/stablyai/orca/pull/47872),
[`stablyai/orca#47871`](https://github.com/stablyai/orca/pull/47871),
[`stablyai/orca#47878`](https://github.com/stablyai/orca/pull/47878) (commit `0edcb65de36`),
[`stablyai/orca#47929`](https://github.com/stablyai/orca/pull/47929) (commit `bd67f13662e`),
[`stablyai/orca#47959`](https://github.com/stablyai/orca/pull/47959) (commit `925bcc7ecb9`),
[`stablyai/orca#47859`](https://github.com/stablyai/orca/pull/47859) (commit `4b6677d11b4`),
[`stablyai/orca#47941`](https://github.com/stablyai/orca/pull/47941) (commit `9ccab10c6dd`),
[`stablyai/orca#47934`](https://github.com/stablyai/orca/pull/47934) (commit `a60bc9384c6`),
[`stablyai/orca#47939`](https://github.com/stablyai/orca/pull/47939) (commit `462a4eb8b1d`),
[`stablyai/orca#47904`](https://github.com/stablyai/orca/pull/47904) (commit `f48a4ef58f2`),
[`stablyai/orca#47869`](https://github.com/stablyai/orca/pull/47869) (commit `488a697ca7a`),
[`stablyai/orca#47815`](https://github.com/stablyai/orca/pull/47815) (commit `d4562c4474e`),
[`stablyai/orca#47978`](https://github.com/stablyai/orca/pull/47978) (commit `4139d3093ef`),
[`stablyai/orca#47961`](https://github.com/stablyai/orca/pull/47961) (commit `422ec833429`),
[`stablyai/orca#47963`](https://github.com/stablyai/orca/pull/47963) (commit `d16db92535c`),
além das issues [`stablyai/orca#47931`](https://github.com/stablyai/orca/issues/47931),
[`stablyai/orca#47854`](https://github.com/stablyai/orca/issues/47854) e
[`stablyai/orca#44486`](https://github.com/stablyai/orca/issues/44486),
[`stablyai/orca#47784`](https://github.com/stablyai/orca/pull/47784) (resolve Issue [`#47780`](https://github.com/stablyai/orca/issues/47780)),
[`stablyai/orca#47774`](https://github.com/stablyai/orca/pull/47774),
[`stablyai/orca#47724`](https://github.com/stablyai/orca/pull/47724) (resolve Issue [`#47715`](https://github.com/stablyai/orca/issues/47715)),
[`stablyai/orca#47667`](https://github.com/stablyai/orca/pull/47667),
[`stablyai/orca#47719`](https://github.com/stablyai/orca/pull/47719),
[`stablyai/orca#47457`](https://github.com/stablyai/orca/pull/47457) (refs Issue [`#41800`](https://github.com/stablyai/orca/issues/41800)),
[`stablyai/orca#43521`](https://github.com/stablyai/orca/pull/43521),
além das issues [`stablyai/orca#47807`](https://github.com/stablyai/orca/issues/47807) e [`stablyai/orca#47781`](https://github.com/stablyai/orca/issues/47781),
[`stablyai/orca#42129`](https://github.com/stablyai/orca/pull/42129),
[`stablyai/orca#47564`](https://github.com/stablyai/orca/pull/47564),
[`stablyai/orca#47432`](https://github.com/stablyai/orca/pull/47432),
[`stablyai/orca#47553`](https://github.com/stablyai/orca/pull/47553) (resolve Issue [`#47552`](https://github.com/stablyai/orca/issues/47552)),
[`stablyai/orca#47587`](https://github.com/stablyai/orca/pull/47587),
[`stablyai/orca#47485`](https://github.com/stablyai/orca/pull/47485),
[`stablyai/orca#45168`](https://github.com/stablyai/orca/pull/45168),
[`stablyai/orca#47559`](https://github.com/stablyai/orca/pull/47559),
[`stablyai/orca#47308`](https://github.com/stablyai/orca/pull/47308),
[`stablyai/orca#47309`](https://github.com/stablyai/orca/pull/47309),
[`stablyai/orca#47429`](https://github.com/stablyai/orca/pull/47429),
[`stablyai/orca#47359`](https://github.com/stablyai/orca/pull/47359) (resolve Issue [`#47358`](https://github.com/stablyai/orca/issues/47358)),
[`stablyai/orca#47346`](https://github.com/stablyai/orca/pull/47346),
[`stablyai/orca#47337`](https://github.com/stablyai/orca/pull/47337),
[`stablyai/orca#47464`](https://github.com/stablyai/orca/pull/47464),
[`stablyai/orca#47200`](https://github.com/stablyai/orca/pull/47200),
[`stablyai/orca#47220`](https://github.com/stablyai/orca/pull/47220),
[`stablyai/orca#47191`](https://github.com/stablyai/orca/pull/47191),
[`stablyai/orca#47016`](https://github.com/stablyai/orca/pull/47016) (resolve Issue [`#47021`](https://github.com/stablyai/orca/issues/47021)),
[`stablyai/orca#47080`](https://github.com/stablyai/orca/pull/47080) (refs Issue [`#47055`](https://github.com/stablyai/orca/issues/47055)),
[`stablyai/orca#47076`](https://github.com/stablyai/orca/pull/47076),
[`stablyai/orca#47084`](https://github.com/stablyai/orca/pull/47084),
[`stablyai/orca#46740`](https://github.com/stablyai/orca/pull/46740),
[`stablyai/orca#46901`](https://github.com/stablyai/orca/pull/46901),
[`stablyai/orca#46930`](https://github.com/stablyai/orca/pull/46930),
[`stablyai/orca#46974`](https://github.com/stablyai/orca/pull/46974) (resolve Issue [`#46953`](https://github.com/stablyai/orca/issues/46953)),
[`stablyai/orca#46739`](https://github.com/stablyai/orca/pull/46739),
[`stablyai/orca#45876`](https://github.com/stablyai/orca/pull/45876),
[`stablyai/orca#45881`](https://github.com/stablyai/orca/pull/45881),
[`stablyai/orca#46592`](https://github.com/stablyai/orca/pull/46592),
[`stablyai/orca#46570`](https://github.com/stablyai/orca/pull/46570),
[`stablyai/orca#46583`](https://github.com/stablyai/orca/pull/46583),
[`stablyai/orca#46608`](https://github.com/stablyai/orca/pull/46608),
[`stablyai/orca#45410`](https://github.com/stablyai/orca/pull/45410),
[`stablyai/orca#46165`](https://github.com/stablyai/orca/pull/46165),
[`stablyai/orca#46009`](https://github.com/stablyai/orca/pull/46009),
[`stablyai/orca#46127`](https://github.com/stablyai/orca/pull/46127),
[`stablyai/orca#46362`](https://github.com/stablyai/orca/pull/46362),
[`stablyai/orca#46281`](https://github.com/stablyai/orca/pull/46281),
[`stablyai/orca#46311`](https://github.com/stablyai/orca/pull/46311),
[`stablyai/orca#46316`](https://github.com/stablyai/orca/pull/46316),
[`stablyai/orca#46368`](https://github.com/stablyai/orca/pull/46368) (resolve Issue [`#46367`](https://github.com/stablyai/orca/issues/46367)),
[`stablyai/orca#46309`](https://github.com/stablyai/orca/pull/46309),
[`stablyai/orca#44461`](https://github.com/stablyai/orca/pull/44461) (resolve Issue [`#40998`](https://github.com/stablyai/orca/issues/40998)),
[`stablyai/orca#44808`](https://github.com/stablyai/orca/pull/44808),
[`stablyai/orca#43994`](https://github.com/stablyai/orca/pull/43994),
[`stablyai/orca#44413`](https://github.com/stablyai/orca/pull/44413),
[`stablyai/orca#44508`](https://github.com/stablyai/orca/pull/44508),
[`stablyai/orca#44203`](https://github.com/stablyai/orca/pull/44203),
[`stablyai/orca#42965`](https://github.com/stablyai/orca/pull/42965),
[`stablyai/orca#43908`](https://github.com/stablyai/orca/pull/43908) (resolve Issue [`#43988`](https://github.com/stablyai/orca/issues/43988)),
[`stablyai/orca#43954`](https://github.com/stablyai/orca/pull/43954),
[`stablyai/orca#43607`](https://github.com/stablyai/orca/pull/43607) (resolve Issue [`#43599`](https://github.com/stablyai/orca/issues/43599)),
[`stablyai/orca#43600`](https://github.com/stablyai/orca/pull/43600) (resolve Issue [`#43595`](https://github.com/stablyai/orca/issues/43595)),
[`stablyai/orca#43567`](https://github.com/stablyai/orca/pull/43567),
[`stablyai/orca#43562`](https://github.com/stablyai/orca/pull/43562),
[`stablyai/orca#43521`](https://github.com/stablyai/orca/pull/43521),
[`stablyai/orca#43516`](https://github.com/stablyai/orca/pull/43516),
[`stablyai/orca#43474`](https://github.com/stablyai/orca/pull/43474),
[`stablyai/orca#43456`](https://github.com/stablyai/orca/pull/43456),
[`stablyai/orca#43425`](https://github.com/stablyai/orca/pull/43425) (resolve Issue [`#43424`](https://github.com/stablyai/orca/issues/43424)),
além das issues [`stablyai/orca#44003`](https://github.com/stablyai/orca/issues/44003),
[`stablyai/orca#43983`](https://github.com/stablyai/orca/issues/43983),
[`stablyai/orca#43610`](https://github.com/stablyai/orca/issues/43610),
[`stablyai/orca#43597`](https://github.com/stablyai/orca/issues/43597),
[`stablyai/orca#43549`](https://github.com/stablyai/orca/issues/43549),
[`stablyai/orca#43462`](https://github.com/stablyai/orca/issues/43462) e
[`stablyai/orca#43461`](https://github.com/stablyai/orca/issues/43461),
[`stablyai/orca#43385`](https://github.com/stablyai/orca/pull/43385),
[`stablyai/orca#43380`](https://github.com/stablyai/orca/pull/43380),
além da issue [`stablyai/orca#43366`](https://github.com/stablyai/orca/issues/43366),
[`stablyai/orca#42455`](https://github.com/stablyai/orca/pull/42455),
[`stablyai/orca#42448`](https://github.com/stablyai/orca/pull/42448),
[`stablyai/orca#42305`](https://github.com/stablyai/orca/pull/42305) (resolve Issue [`#42099`](https://github.com/stablyai/orca/issues/42099)),
[`stablyai/orca#42307`](https://github.com/stablyai/orca/pull/42307),
[`stablyai/orca#42287`](https://github.com/stablyai/orca/pull/42287) (resolve Issue [`#42286`](https://github.com/stablyai/orca/issues/42286)),
[`stablyai/orca#42254`](https://github.com/stablyai/orca/pull/42254),
[`stablyai/orca#41955`](https://github.com/stablyai/orca/pull/41955),
[`stablyai/orca#41766`](https://github.com/stablyai/orca/pull/41766),
[`stablyai/orca#40935`](https://github.com/stablyai/orca/pull/40935),
[`stablyai/orca#39649`](https://github.com/stablyai/orca/pull/39649) (resolve Issue [`#39619`](https://github.com/stablyai/orca/issues/39619)),
[`stablyai/orca#39606`](https://github.com/stablyai/orca/pull/39606) (resolve Issue [`#37379`](https://github.com/stablyai/orca/issues/37379)),
[`stablyai/orca#39276`](https://github.com/stablyai/orca/pull/39276) (Issue [`#39275`](https://github.com/stablyai/orca/issues/39275)),
[`stablyai/orca#39082`](https://github.com/stablyai/orca/pull/39082) (Issue [`#39074`](https://github.com/stablyai/orca/issues/39074)),
[`stablyai/orca#39079`](https://github.com/stablyai/orca/pull/39079) (Issue [`#39073`](https://github.com/stablyai/orca/issues/39073)),
além das issues [`stablyai/orca#41008`](https://github.com/stablyai/orca/issues/41008) e
[`stablyai/orca#39619`](https://github.com/stablyai/orca/issues/39619),
[`stablyai/orca#38995`](https://github.com/stablyai/orca/pull/38995) (Issue [`#38994`](https://github.com/stablyai/orca/issues/38994)),
[`stablyai/orca#38963`](https://github.com/stablyai/orca/pull/38963),
[`stablyai/orca#38945`](https://github.com/stablyai/orca/pull/38945),
[`stablyai/orca#39013`](https://github.com/stablyai/orca/pull/39013) (Issue [`#39010`](https://github.com/stablyai/orca/issues/39010)),
[`stablyai/orca#38632`](https://github.com/stablyai/orca/pull/38632),
[`stablyai/orca#38633`](https://github.com/stablyai/orca/pull/38633),
[`stablyai/orca#38640`](https://github.com/stablyai/orca/pull/38640),
[`stablyai/orca#38470`](https://github.com/stablyai/orca/pull/38470),
[`stablyai/orca#38452`](https://github.com/stablyai/orca/pull/38452),
[`stablyai/orca#38594`](https://github.com/stablyai/orca/pull/38594) (Issue [`#38592`](https://github.com/stablyai/orca/issues/38592)),
[`stablyai/orca#38627`](https://github.com/stablyai/orca/pull/38627),
[`stablyai/orca#38649`](https://github.com/stablyai/orca/pull/38649) e
[`stablyai/orca#38625`](https://github.com/stablyai/orca/pull/38625) (Issue [`#38624`](https://github.com/stablyai/orca/issues/38624)).

## O problema

1. **Incapacidade de visualizar transcrições de chats estruturados no Agent Dashboard (`#39082`, `#39074`):**
   No painel Agent Dashboard, cartões de sessões de chat estruturado não possuíam PTY associado, exibindo apenas uma mensagem
   estática de que nenhuma pré-visualização estava disponível. O usuário precisava abrir o worktree e carregar a aba para
   ler o histórico ou acompanhar o progresso.
2. **Excesso de notificações intrusivas e falta de filtro por perguntas de agentes (`#39079`, `#39073`):**
   O canal de notificações do sistema tratava qualquer evento ("Agent Needs Input", conclusões de tarefas e campainhas de
   terminal) de forma idêntica. Desenvolvedores que desejavam ser avisados apenas quando o agente realmente precisava de
   uma resposta ou esclarecimento eram inundados por alertas repetitivos de aprovações rotineiras de ferramentas.
3. **Sessões flutuantes e de subagentes dispersas na barra lateral (`#38995`, `#38994`):**
   Subagentes e sessões ad-hoc abertas fora da hierarquia primária de worktrees misturavam-se de forma plana na lista de
   workspaces da barra lateral, sem indicação visual compacta do número de subagentes trabalhando em tempo real.
4. **Travamento do chat aguardando ferramentas ou comandos Bash longos do Claude (`#38963`):**
   Comandos demorados ou subagentes executados via Claude Bash bloqueavam a continuidade do chat até o término da invocação,
   sem opção para despachar o comando em segundo plano e permitir que o operador ou o agente seguissem a conversa.
5. **Travamentos e congelamentos em históricos massivos de sessões (`#38945`):**
   O indexador e motor de busca do Agent Session History executava transações SQLite síncronas pesadas na mesma thread do
   Node/servidor, travando a UI por minutos em históricos com mais de 20.000 transcrições.
6. **Processos órfãos fora de terminais invisíveis no monitor de recursos (`#39013`, `#39010`):**
   O popover Resource Usage monitorava apenas a árvore direta de processos de terminais ativos, omitindo servidores de
   desenvolvimento desanexados iniciados pelo agente.
7. **Invisibilidade e falta de inspeção de subagentes no Native Chat (`#38632`, `#38633`, `#38470`):**
   Falta de elenco estruturado (*roster*) dos subagentes em execução no chat desktop e mobile.
8. **Subagentes do OpenCode 2.x não renderizados no Chat UI (`#39276`, `#39275`):**
   Quando um agente OpenCode delegava tarefas a subagentes auxiliares (`subagent` no 2.x ou `task` no 1.x), as ações do filho
   apareciam como ferramentas genéricas na conversa principal, sem identificação do subagente, sem cartão dedicado de estado
   (running/done/stopped) e sem presença na faixa de agentes ativos acima do composer.
9. **Sessões irmãs do OpenCode em serviço compartilhado tratadas como subagentes (`#39619`):**
   Ao conectar múltiplos terminais ao mesmo serviço `opencode serve --service`, o hook do OpenCode considerava qualquer sessão ativa
   no fluxo de eventos como subagente da pane observada. Isso fazia com que abas ociosas exibissem o spinner `working` continuamente
   enquanto uma sessão irmã trabalhava.
10. **Poluição de títulos de abas do Claude Code com texto de aviso após `/clear` (`#39606`, resolve `#37379`):**
    Após rodar `/clear`, o título da aba no Orca assumia o texto bruto `<local-command-caveat>The command below was run directly in Claude Code...`
    em vez de preservar o título ao vivo (`✳ Claude Code`), permanecendo ilegível até o envio do próximo prompt real.
11. **Sobrescrita, duplicação e desaparecimento de imagens geradas no Native Chat (`#40935`):**
    Quando agentes geravam imagens (artboards, mockups ou diagramas), a entrega do artefato sobrescrevia o texto em prosa da
    resposta final quando chegava com atraso, aparecia duplicada caso a resposta já a incorporasse, ou desaparecia completamente
    ao navegar de volta pelo histórico de sessões anteriores.
12. **Invisibilidade do modelo e nível de esforço de subagentes no painel de agentes (`#41008`):**
    No painel de agentes da sessão do Claude ("1 agent — working", com nome, ferramenta ativa, tokens e tempo), não havia exibição
    do modelo e esforço de raciocínio de cada subagente. Quando agentes customizados ou chamadas dinâmicas utilizavam modelos
    discrepantes do pai (ex.: subagente executando em Opus no esforço high em sessão pai Sonnet), o operador ficava no escuro sobre
    os parâmetros de execução e custos correspondentes.
13. **Incompatibilidade para importar transcrições do Kimi Code e adotar conversas iniciadas via CLI (`#41955`):**
    Sessões e transcrições geradas pela CLI do Kimi Code permaneciam isoladas no filesystem, impossibilitando que desenvolvedores
    adotassem essas conversas dentro do Native Chat no desktop para continuar a interação com histórico estruturado,
    ferramental gráfico e inspeção de passos.
14. **Retenção de memória de subagentes após o fechamento da aba de chat (`#42254`):**
    Ao inspecionar um subagente dentro de uma conversa, o aplicativo guardava o registro de qual subagente estava aberto.
    Quando a aba de chat era fechada, esse registro continuava retido em memória até o reinício do aplicativo, acumulando
    vazamentos sutis em sessões de longa duração.
15. **Ausência da barra de subagentes ativos no mobile para chats baseados em terminal (`#42305`, resolve `#42099`):**
    No cliente mobile, chats orientados a terminal ou com subagentes delegados não exibiam a barra horizontal compacta de subagentes ativos, impedindo acompanhar workers em tempo real pelo smartphone.
16. **Perda ou reexecução espúria de perguntas interativas após reinicialização do app (`#42307`):**
    Perguntas pendentes de agentes interativos sofriam reinvocação ou disparavam novas requisições de modelo caso o app fosse reiniciado antes da resposta do usuário.
17. **Divergência na identificação de versão pontual do Claude no banner (`#42287`, resolve `#42286`):**
    O banner do chat truncava versões minoritárias pontuais do Claude (ex.: Opus 5.5 caindo incorretamente para Opus 5), gerando confusão sobre a real versão do modelo em execução.
18. **Substituição da tela inteira de chat ao inspecionar subagentes (`#42455`):**
    Clicar em um subagente na barra ou transcrição trocava toda a conversa principal pela visualização do subagente, ocultando o contexto da conversa pai, perdendo a posição de rolagem e bloqueando o rascunho ativo no composer.
19. **Invisibilidade de subagentes nas conversas do Pi Native Chat (`#42448`):**
    Enquanto Claude e Codex exibiam subagentes e ferramentas delegadas de forma visual, o agente Pi não renderizava a presença de subagentes no chat nativo.
20. **Falta de faixa de worker temporário no topo de chat workers (`#43521`):**
    Workers temporários disparados no chat não exibiam o banner no topo avisando sobre a natureza efêmera da tarefa, ao contrário do que já ocorria em abas de terminal.
21. **Ausência de identificador de plugin em mensagens e mails enviados (`#43425`, resolve `#43424`):**
    Mensagens geradas ou despachadas por plugins no chat nativo não exibiam nome nem ícone do plugin de origem, prejudicando a rastreabilidade das ações automatizadas.
22. **Incapacidade de referenciar outros chats e terminais via `@` no composer (`#43462`):**
    O compositor de mensagens não oferecia autocompletar com `@` para menções direcionadas a outras sessões de chat ou abas de terminal abertas no workspace.
23. **Citações "Add to chat" sem chips navegáveis de retorno (`#43461`):**
    Textos capturados do terminal ou editor para o chat ficavam colados como texto puro sem transformar-se em chips interativos capazes de saltar para a linha ou arquivo de origem ao clicar.
24. **Auto-retomada indevida de chats aguardando operador após reinício (`#43474`):**
    Ao reiniciar o aplicativo, conversas esperando confirmação ou entrada humana eram retomadas cegamente em vez de permanecerem listadas na fila de restart pendente.
25. **Consumo de memória sem limites em entregas e leituras atrasadas de chat (`#43456`):**
    Filas de eventos de chat e leituras de histórico acumulavam mensagens na memória sem limite quando o receptor ficava atrasado, elevando o heap do runtime.
26. **Montagem eager e pesada de abas de chat ocultas no arranque (`#43516`):**
    O componente de visualização de chat era montado imediatamente para todas as abas no carregamento, degradando a performance inicial de workspaces com muitos chats.
27. **Falta de seletores rápidos de presets de modelo, esforço de raciocínio e velocidade no Chat (`#43607`, resolve `#43599`):**
    Ajustar modelo, esforço de raciocínio e velocidade exigia abrir menus suspensos ou configurações em múltiplos níveis. Não havia presets rápidos de um clique posicionados diretamente abaixo do controle de velocidade.
28. **Inflexibilidade da tecla de envio de mensagens no Native Chat (`#43600`, resolve `#43595`):**
    O composer do chat disparava o envio fixamente ao pressionar Enter (exigindo Shift+Enter para quebra de linha), sem uma configuração que permitisse inverter o comportamento para operadores acostumados a usar Enter para parágrafos e Shift+Enter para envio.
29. **Omissão de painéis de agentes recém-iniciados no seletor "Send notes to" (`#43562`):**
    O menu "Send notes to" só listava painéis de agentes após o primeiro relatório de status formal ter sido emitido. Painéis recém-criados permaneciam invisíveis até que o agente executasse seu primeiro turno, impossibilitando o envio precoce de anotações.
30. **Dessincronização do destaque na visualização de Activity com a aba ativa (`#43567`):**
    O item de Activity na barra lateral esquerda não sincronizava seu realce de seleção visual ao alternar entre abas e workspaces de agentes, deixando o operador desorientado sobre qual agente estava selecionado no painel.
31. **Supressão ou aglutinação de resumos de raciocínio (thinking) entre chamadas de ferramentas (`#43610`):**
    Trechos intermediários de raciocínio emitidos pelo Claude entre chamadas sucessivas de ferramentas eram mesclados ou ocultados no Chat UI, dificultando acompanhar a linha lógica do modelo durante a execução sequencial de comandos.
32. **Exibição de tags brutas `<advisory>` de conselhos de modelo como texto de usuário (`#43549`):**
    Tags de aviso de harness/OMP como `<advisory>` eram despejadas diretamente na área de conversa como se fossem texto digitado pelo usuário, poluindo a visualização.
33. **Ocupação permanente de espaço de tela pela barra lateral esquerda (`#43597`):**
    A barra lateral esquerda não possuía modo auto-hide com revelação ao passar o cursor pela borda (edge-hover reveal), sacrificando espaço útil de tela em telas menores ou monitores secundários.
34. **Travamento em "Sending..." de novos chats sob concorrência de streaming múltiplo (`#43908`, resolve `#43988`):**
    Quando dezenas de chats eram retomados simultaneamente após um restart, o envio de mensagens em um novo chat ficava travado em "Sending..." por dezenas de segundos sem indicador de trabalho. O gravador único de journal no SQLite compartilhava uma única fila FIFO e o limite de backpressure do WAL travava todas as novas escritas.
35. **Vazamento de memória por retenção vitalícia de status de chats fechados (`#43954`):**
    O feed de status de chats no processo principal retinha o sumário de cada sessão já aberta ou encerrada durante todo o ciclo de vida do aplicativo, impedindo a desalocação de memória de conversas fechadas.
36. **Omissão de árvores de processos do Native Chat no Resource Manager (`#43983`):**
    O monitor de recursos contava apenas processos de terminais PTY locais e processos internos do Orca, ignorando as árvores de processos dos agentes em execução nas abas de chat nativo.
37. **Reaparecimento de registros falhados limpos da view de Activity após hidratação (`#44003`):**
    Linhas de atividades com falha previamente limpas pelo desenvolvedor voltavam a aparecer na interface após a hidratação de estado e geravam erros ao tentar abrir worktrees já removidos.
38. **Supressão do menu de contexto nativo de cópia ao selecionar texto do chat na web móvel (`#42965`):**
    No cliente web para dispositivos móveis (smartphones), ao selecionar trechos de texto em mensagens do chat, o menu de contexto nativo do navegador/sistema operacional (com a ação "Copiar" / "Copy") era suprimido ou desabilitado por manipuladores de eventos de seleção do chat, impedindo que o operador copiasse facilmente partes das respostas do assistente no telefone.
39. **Mensagens entre agentes e atualizações de workers ocupando turnos inteiros de conversa no chat (`#44413`):**
    Quando agentes trocavam mensagens de coordenação ou emitiam atualizações de tarefas no chat, cada aviso era exibido como uma mensagem de chat completa e inchada. Reinicializações de workers alteravam linhas antigas e geravam confusão sobre o estado gravado da tarefa.
40. **Tremulação e reflow visual da faixa de agentes no Native Chat durante atualizações de sessão (`#44508`):**
    A cada atualização de estado da sessão do agente, a barra horizontal de agentes (*agents strip*) sofria remontagem e saltos de renderização (layout shifts), gerando cintilação visual na área superior do composer.
41. **Esgotamento de memória ao exportar contexto de chat com saídas extensas de ferramentas (`#44203`):**
    Ao exportar o contexto da conversa ou transferir dados para o modelo, saídas extensas de ferramentas de terminal eram carregadas inteiramente em strings na memória heap, provocando travamentos e quedas por falta de memória (OOM).
42. **Consumo ilimitado de memória no processo principal com streaming de texto em múltiplos chats (`#43994`):**
    Quando múltiplos chats nativos ou assinantes (*subscribers*) lentos realizavam streaming simultâneo de respostas volumosas, o processo principal do Electron acumulava cópias não entregues de snapshots de texto ao vivo sem teto delimitado por subscriber. Em conexões lentas ou renderers ocupados, a retenção gerava picos de centenas de megabytes no heap do main process antes de desalocar a memória.
43. **Descompasso de título de chat ao renomear sessão Claude via comando `/rename` ou `/name` (`#44461`, resolve `#40998`):**
    Ao digitar `/rename <novo-nome>` ou `/name` em um chat Claude, o nome interno da conversa era alterado na CLI, mas a aba do Native Chat e a lista do Session History mantinham o nome autogerado pelo Studio (que tem precedência sobre o título do transcript). A interface não interceptava o evento `session_title_changed` emitido pela CLI, mantendo o título antigo visível.
44. **Desaparecimento de respostas de comandos locais `/recap` ao reabrir chats Claude (`#44808`):**
    Respostas geradas pelo comando `/recap` eram gravadas pelo Claude Code em registros do tipo `system/local_command` no transcript, enquanto no streaming ao vivo eram enviadas como frames sintéticos de assistente. Como a rotina de reidratação/catch-up e os decodificadores legados só liam linhas `user` e `assistant`, o conteúdo de resumos do `/recap` desaparecia da conversa ao reabrir a aba ou retomar o chat via "Resume in New Chat".
45. **Impossibilidade de citar pastas no menu de menções `@` do chat (`#46127`):**
    O menu popover de autocompletar com `@` suportava apenas arquivos e agentes, forçando o operador a digitar caminhos de pastas inteiros manualmente ao instruir agentes sobre diretórios do projeto.
46. **Citações "Add to chat" poluindo o composer como blocos Markdown brutos (`#46362`):**
    Ações de adicionar trechos selecionados de código ou notas ao chat colavam o texto cru no composer, ocupando espaço excessivo e sem indicador de origem navegável.
47. **Imagens anexadas a comentários de itens e perguntas não exibidas inline no chat (`#46281`):**
    Quando um usuário ou subagente anexava capturas de tela ou imagens de referência em respostas de perguntas de itens, a imagem não era renderizada inline na conversa, quebrando a inspeção visual.
48. **Mensagens vazias de assistente poluindo o histórico de conversa (`#46311`):**
    Em turnos com saídas parciais ou desvios de ferramentas que não geravam texto final, o frontend registrava e exibia mensagens de assistente totalmente em branco no desktop e mobile.
49. **Perda de instruções permanentes (`SOUL.md` / `MEMORY.md`) em chats gerenciados do Antigravity via ACP (`#46368`, resolve `#46367`):**
    A configuração de sessão sobrescrevia o campo `sessionMeta` do arranque com `setup._meta`, fazendo com que chats gerenciados do Antigravity descartassem silenciosamente as instruções permanentes e diretivas de alma e memória.
50. **Parada prematura de chats após atingir limite de uso por perfil desatualizado (`#45410`):**
    - Quando um agente atinge o limite de uso temporário (rate limit ou cota de provedor), a retomada automática dependia de `nativeChatAutoContinueAfterUsageLimit`, que vinha desabilitada por padrão, forçando o operador a intervir manualmente quando os limites expiravam. Além disso, redefinições simultâneas de cotas podiam disparar muitos agentes ao mesmo tempo sem escalonamento.
51. **Dificuldade de busca no menu de menção `@` de bots e perda de hierarquia de comandos (`#46165`):**
    - A lista de menções `@` de bots no Native Chat não filtrava por início de palavras nem considerava seleções recentes. Além disso, o disparo de `/` ou `$` após nomes espaçados de bots abria menus de forma inconsistente, e o cabeçalho 'Bots' desaparecia se houvesse apenas bots pausados na lista.
52. **Competição desordenada na reinicialização de chats interrompidos mid-turn versus tarefas concluídas (`#46009`):**
    - Ao reiniciar o aplicativo após crash ou reboot, chats com agentes interrompidos no meio de uma resposta competiam na mesma fila de inicialização com chats que já haviam concluído a resposta do agente e tinham apenas comandos em background pendentes, atrasando o retorno do agente ao operador.
53. **Incapacidade de excluir chats permanentemente e poluição do histórico de sessões (`#45876`):**
    - Usuários não tinham opção para deletar conversas desnecessárias no Native Chat e Session History; chats descartados permaneciam gravados no SQLite, poluíam buscas e podiam ser re-adotados acidentalmente.
54. **Poluição visual e colisão de controles nas linhas de chat e abas (`#45881`):**
    - Linhas de chat na lista da sidebar e na aba de chats exibiam múltiplos botões simultâneos; no hover, o botão `⋯` colidia com o timestamp e o status ao vivo ficava oculto em mensagens longas.
55. **Faixa de mensagens enfileiradas intrusiva e desconectada da linha de atividade (`#46592`):**
    - A faixa de mensagens enfileiradas (*queued-message strip*) exibia botões permanentes de ação que desviavam o foco da leitura e não se alinhavam com a linha de atividade do chat.
56. **Falta de menções `@` e comandos `/` na caixa de comentários de itens (`#46570`):**
    - A caixa de comentários em itens e issues não dispunha dos recursos de autocompletar do composer principal, impedindo citar agentes/arquivos via `@` ou invocar skills e comandos `/` diretamente.
57. **Falta de feedback visual no carregamento de itens de bots e identificadores opacos em Nova Aba (`#46583`, `#46608`):**
    - Ao abrir detalhes de itens de bots, a tela permanecia em branco antes da resposta do servidor em vez de exibir um esqueleto (*skeleton loader*); no seletor de Nova Aba, agentes apareciam com IDs internos opacos em vez dos nomes configurados no catálogo.
58. **Falha na renderização de imagens retornadas por ferramentas ACP sem caminho físico no disco (`#46901`):**
    - Ferramentas executadas por agentes ACP podem retornar imagens diretamente como payloads base64 sem caminho de arquivo gravado no workspace. O visualizador de anexos do Native Chat buscava carregar apenas arquivos a partir do caminho físico, resultando em imagens quebradas ou ausentes no card de saída da ferramenta.
59. **Quebra de transferência e lentidão em imagens de chat superiores a 3MB em clientes pareados (`#46930`):**
    - Quando clientes móveis ou instâncias pareadas tentavam visualizar imagens ou capturas com tamanho superior a 3MB anexadas no chat, o envio de payload monobloco causava estouro de buffer RPC ou timeouts de rede, inviabilizando a inspeção remota de imagens pesadas.
60. **Bloqueio de colagem via botão do meio do mouse (middle-click paste) em editores ProseMirror (`#46974`, resolve `#46953`):**
    - Em ambientes Linux e navegadores X11/Wayland, o clique com o botão do meio no composer baseado em ProseMirror (tanto no chat principal quanto em caixas de anotação) não disparava a colagem do buffer de seleção primária, quebrando o comportamento esperado da plataforma desktop.
61. **Omissão de pré-visualização de texto e chevron dinâmico confuso em linhas de mensagens de agentes (`#46739`):**
    - As linhas representativas de agentes no histórico de conversas exibiam apenas indicadores genéricos sem revelar a primeira linha de texto do turno e ocultavam o chevron de expansão, tornando difícil discernir o contexto rápido e saber se a linha era expansível.
62. **Inflação de diffs e substituição inteira de arquivo em edições de arquivos grandes via ACP (`#47016`, resolve `#47021`):**
    - Edições em arquivos grandes cuja soma do texto antigo e novo superava 256 KiB eram reportadas como substituição completa do arquivo, transformando uma edição de uma única linha em milhares de linhas removidas e readicionadas.
63. **Desaparecimento instantâneo de resultados de título ao concluir busca sem correspondência FTS (`#47080`, refs `#47055`):**
    - No Session History e no seletor `/resume`, enquanto o usuário digitava, sessões com títulos correspondentes apareciam na tela; se a busca full-text subsequente não encontrava correspondências no corpo das conversas, a lista era substituída por tela vazia, fazendo os resultados sumirem abruptamente.
64. **Truncamento prematuro em 8 linhas de perguntas abertas de agentes em itens (`#47076`):**
    - Quando um agente postava uma pergunta aberta em um item aguardando resposta humana, o comentário era cortado arbitrariamente em 8 linhas, ocultando o contexto da dúvida até que a pergunta fosse respondida ou substituída.
65. **Ocultação e ilegibilidade de item pills em linhas "Started" de mensagens com nomes longos (`#47084`):**
    - Em linhas de mensagens do tipo "Started" contendo remetente e chip de item vinculado, o nome do remetente possuía `flex-basis: auto` enquanto o chip do item tinha `flex-basis: 0`, fazendo com que o nome ocupasse todo o espaço horizontal e esmagasse o pill do item.
66. **Ausência de estado visual de repouso ("all-clear") na aba Items quando nada requer atenção (`#46740`):**
    - Quando todas as tarefas, perguntas e itens de um grupo de bots eram concluídos, a aba Items exibia uma lista vazia sem indicação visual de que a operação estava em dia (*all-clear*).
67. **Migração ordenada de mensagens enfileiradas e cancelamento com aviso de mensagens de conectores ao substituir chat (`#47200`):**
    - Quando um chat era substituído por uma nova conversa, mensagens enfileiradas aguardando a conclusão do turno ativo se perdiam ou ficavam órfãs, enquanto mensagens originadas de conectores ficavam retidas em limbo sem confirmação de cancelamento.
68. **Bloqueio total de correio de outros agentes por turnos com falhas transitórias (`#47220`):**
    - Mensagens enfileiradas de outros agentes eram suspensas indefinidamente quando o turno do agente principal falhava por qualquer motivo operacional, mesmo que a falha não fosse por esgotamento de cota de uso (*usage limit*).
69. **Impossibilidade de agentes anexarem itens, URLs e arquivos a itens abertos de outros agentes (`#47191`):**
    - Agentes ficavam impossibilitados de associar tarefas filhas, links de PRs, arquivos e comandos `worker-start --item` a itens de trabalho criados por outros agentes no mesmo workspace, limitando a colaboração entre bots na árvore de itens.
70. **Alargamento horizontal forçado do chat por sumários contínuos de tarefas em background (`#47359`, resolve `#47358`):**
    - Quando um comando em segundo plano (como `worker-start`) emitia uma linha de resultado ou JSON sem quebras, o token contínuo definia a largura mínima (`min-content`) do transcript, forçando barra de rolagem horizontal em todo o Native Chat.
71. **Ausência de estado formal `Waiting` para itens retidos por fatores externos (`#47308`, `#47309`, `#47429`):**
    - Itens aguardando conclusão externa (CI, deploy, revisão, resposta ou reset de cota de uso) permaneciam ambiguamente como `In progress`, sem sinalização clara do motivo da espera no hover card e janelas de desktop/mobile.
72. **Perda de modo Plan/Build e configurações de entrega ao migrar mensagens enfileiradas (`#47337`):**
    - Ao transferir a fila para uma conversa substituta, apenas o texto bruto era copiado; opções congeladas no enfileiramento (modo Plan/Build, modelo, esforço, personality, fast mode e modo steer) eram descartadas, revertendo envios planejados para o modo padrão.
73. **Perda de alinhamento e respostas precipitadas em itens com múltiplas perguntas (`#47464`, `#47461`, `#47385`, `#47372`):**
    - Respostas digitadas a uma única pergunta de um conjunto acordavam o agente imediatamente deixando as demais perguntas pendentes; além disso, respostas retidas não recuperavam o indicador `Replying to`, publicando como comentário comum fora de contexto.
74. **Falta de comando visual rápido para conversas laterais (`/btw` e `/side`) no composer (`#42129`):**
    - Ao digitar comandos de ramificação lateral como `/btw` ou `/side`, não havia feedback visual antes do envio, gerando incerteza se a mensagem iria para o chat corrente ou criaria uma conversa lateral independente.
75. **Classificação alarmista de perguntas abertas como estado bloqueado (`blocked`) em chats nativos (`#47564`):**
    - Enquanto nos terminais uma pergunta aberta lia pacificamente como `waiting`, o Native Chat mapeava a atenção da sessão diretamente para `blocked`, sinalizando bloqueio crítico da thread quando na verdade se tratava apenas de interação dialógica normal.
76. **Contagem incorreta de workers no composer e travamentos de rolagem na faixa de workers (`#47432`):**
    - A faixa de workers acima do composer contava workers já inativos ou finalizados; além disso, a faixa sofria de redimensionamento abrupto e tentava forçar encaixes na rolagem, quebrando a precisão de trackpads no macOS.
77. **Dessincronização do marcador lateral de turno (rail tick) entre linhas do chat (`#47553`, resolve `#47552`):**
    - Quando o scroll do chat parava exatamente na margem vazia entre duas linhas montadas, a rotina de detecção considerava a linha anterior obsoleta e mantinha aceso o marcador antigo.
78. **Fechamento indesejado do seletor de modelos ao interagir com a barra de rolagem (`#47587`):**
    - Clicar ou arrastar a barra de rolagem do popover de modelos fechava sumariamente o modal por tratar o clique como foco fora do componente.
79. **Descarte integral de rascunhos em itens quando o agente substitui a pergunta aberta (`#47485`):**
    - Se o usuário estivesse digitando uma resposta a uma pergunta em um item e o agente decidisse atualizar ou substituir a questão, todo o rascunho era apagado sem recuperação.
80. **Perda de mensagens anteriores paginadas ao receber novos snapshots da transcrição (`#45168`):**
    - Em chats longos, ao navegar para cima no histórico paginado (*paged-in rows*), qualquer atualização subsequente de frame reenviada pelo host descartava as linhas antigas, fazendo a visualização saltar para o presente.
81. **Disparo acidental de hover cards após navegação de retorno via teclado (`#47559`):**
    - Retornar na lista de itens via teclado posicionava o foco no elemento anterior, abrindo hover cards mesmo quando o cursor do mouse apontava para outra região.
82. **Envio acidental de rascunhos de outro chat ao clicar em Stop/Send em telas divididas (`#47784`, resolve `#47780`):**
    - Em layout de split chat (dois chats lado a lado), clicar em Stop ou Send no chat da direita mantinha o foco do teclado no editor de prompt do chat da esquerda (devido ao `preventDefault()` para evitar descarte de foco ao `<body>`), fazendo com que o `Cmd+Enter` subsequente enviasse o rascunho do chat esquerdo como steer indesejado.
83. **Falso estado "Status unavailable" e ícone incorreto para workers cujo chat foi interrompido (`#47774`):**
    - Na bandeja de workers do composer (worker tray / dock), workers cuja sessão foi encerrada (turnos cortados por saída/crash) caíam no fallback genérico `unavailable`, exibindo "Status unavailable" com contagem de minutos que parecia um worker rodando. Além disso, workers ativos usavam um loader cinza grande em vez do glifo compartilhado `AgentStateDot` (anel amarelo).
84. **Subagentes presos indefinidamente em "working" após o término de tarefas secundárias (`#47724`, resolve `#47715`):**
    - Quando um subagente concluía seu turno mas deixava processos em background, o término dessa tarefa invocava `wakeOwner()` incondicionalmente, re-marcando o proprietário como `running` sem expiração. Se o Claude Code não o retomasse, a linha ficava travada em "1 agent working" por dezenas de minutos sem filhos vivos.
85. **Dificuldade de referenciar chats e terminais ativos no composer (`#47667`):**
    - O menu de menções `@` suportava apenas arquivos e agentes do catálogo. Operadores que trabalham com múltiplos chats paralelos (ex.: backend, frontend e documentação) não podiam citar conversas nem terminais abertos para leitura ou envio direto sem consultar IDs de sessão manualmente.
86. **Ausência de estilização Markdown instantânea no composer (`#47719`):**
    - O editor do composer não formatava Markdown inline durante a digitação, forçando o operador a adivinhar a renderização de tabelas, blocos de código e ênfases antes do envio.
87. **Galeria de imagens restrita à mensagem atual e travamentos em decodificações pesadas (`#47457`, refs `#41800`):**
    - O visualizador de imagens do chat limitava a navegação de avançar/voltar exclusivamente aos anexos de uma única mensagem, e a decodificação síncrona monobloco de imagens base64 via `atob` prendia a thread do renderer em long tasks.
88. **Atrasos na abertura do seletor `/resume` e buscas de texto completo submetidas (`#47807`):**
    - Invocações do comando `/resume` retardavam a renderização inicial do picker e as buscas FTS devido a bloqueios de indexação no banco de histórico.
89. **Ocupação rígida da faixa de workers sobre o composer (`#47980`):**
    - A faixa de workers ativos ocupava altura fixa comprimindo o campo de digitação; o PR `#47980` faz o card de worker flutuar como uma pequena pílula (*floating pill*) acima da caixa de mensagem que se expande em card detalhado sob clique.
90. **Citações "Add to chat" renderizadas como chips interativos com salto à fonte (`#47949`, refs `#43461`):**
    - Textos e códigos anexados via "Add to chat" deixam de sujar o composer como blocos Markdown brutos e passam a ser exibidos como chips com arquivo e linha, saltando diretamente para o arquivo ao clicar.
91. **Invisibilidade de chats recém-abertos de Claude e Codex na sidebar antes do primeiro envio (`#47929`, commit `bd67f13662e`):**
    - Chats criados no workspace não apareciam na lista da barra lateral até que a primeira mensagem fosse transmitida; agora são registrados e exibidos imediatamente.
92. **Sobrecarga de leitura no journal para turnos mais novos (`#47878`, commit `0edcb65de36`):**
    - A leitura da janela de turnos mais recentes no journal SQLite lia todas as mensagens históricas da conversa; agora lê estritamente os envios que a janela comporta.
93. **Barra de progresso redundante no card de perguntas (`#47959`, commit `925bcc7ecb9`):**
    - O card de perguntas do chat descartou a barra de passos (step bar), adotando contadores compactos e setas de navegação direta.
94. **Perda indevida de estado Needs You ao iniciar workers com perguntas abertas (`#47941`, commit `9ccab10c6dd`):**
    - Iniciar um worker enquanto uma pergunta estava aberta no item limpava o estado de atenção; agora o item permanece rotulado como `Needs you`.
95. **Fricção no cancelamento de itens por diálogo de justificativa (`#47934`, commit `a60bc9384c6`):**
    - O cancelamento de itens de agentes passa a ser imediato com um clique, eliminando o diálogo de solicitação de motivo.
96. **Pre-carregamento de histórico e execução imediata em buscas submetidas de `/resume` (`#47815`, commit `d4562c4474e`):**
    - Pre-carrega o histórico de sessões e dispara a busca imediatamente ao submeter `/resume`, sem engasgos de interface.
97. **Re-projeção desnecessária de todas as linhas de chat durante streaming com ferramentas desacopladas (`#47931`):**
    - Quando o frame de streaming contém ferramentas desacopladas, a lista inteira de mensagens do Native Chat é re-projetada por frame, causando perda de fluidez.
98. **Ocultação de prosa durante blocos de pensamento intercalados (`#48353`, commit `6a87ef6dc1b`):**
    - Em modelos que emitem tags de pensamento (thinking) no meio da resposta, o stream dividia os blocos e ocultava o texto em prosa precedente até o encerramento do raciocínio.
99. **Sobrecarga visual no seletor de menções `@` exibindo dados redundantes (`#48425`, `#48223`, commits `004525c2f14`, `69a81ecc972`):**
    - As linhas do seletor `@` de agentes no mobile e desktop poluíam o espaço exibindo detalhes extensos e paths de execução em vez de focar no nome curto.
100. **Truncamento de prévia de ferramentas shell no chat (`#48430`):**
    - Clicar na prévia de comandos shell executados por ferramentas no Native Chat truncava o comando completo, impedindo a inspeção detalhada.
101. **Imagens locais em cache não recarregadas quando modificadas no disco (`#48451`):**
    - Quando um agente ou script atualizava uma imagem já exibida na conversa, o visualizador mantinha a versão antiga em cache sem re-ler o arquivo alterado.
102. **Perda de foco do composer no Linux via Alt-Tab (`#48461`):**
    - No Linux desktop, alternar janelas desarmava o foco do editor ProseMirror, exigindo clique manual para recuperar o cursor.
103. **Bandeja de workers ocupando espaço excessivo no composer em chats longos (`#48581`):**
    - A bandeja de workers ativos (worker tray) ocupava uma barra retangular fixa de largura completa, empurrando o composer para baixo; o upstream introduziu layout em chip/pílula compacta recolhível com contagem e estado inline.
104. **Aperto visual e quebra de alinhamento na queued row de mensagens pendentes (`#48564`, `#48598`):**
    - As linhas de mensagens enfileiradas (*queued row*) colidiam visualmente com o composer inferior por falta de margem e separação vertical, além de quebrar o layout quando múltiplas mensagens eram postadas rapidamente.
105. **Ausência de prompts sugeridos (*suggested prompts*) no Native Chat do Codex (`#48472`):**
    - Enquanto Claude apresentava chips de sugestão contextuais baseados no estado do repositório, o Codex Native Chat mantinha a tela inicial vazia sem guiar o desenvolvedor sobre ações possíveis.
106. **Falha na colagem direta de imagens da área de transferência (clipboard) no composer (`#48666`, refs `#48528`):**
    - Colar capturas de tela diretamente do clipboard (`Cmd+V` / `Ctrl+V`) gerava uploads inconsistentes ou falhava silenciosamente quando o MIME type vinha como `image/png` sem extensão física associada.
107. **Perda de foco do teclado ao fechar modal ou sheet de inspeção de subagente (`#48609`, resolve Issue `#48602`):**
    - Fechar a gaveta (*slide-up sheet*) de um subagente descartava o foco ativo para o `<body>`, forçando o operador a clicar novamente no editor de prompt do chat principal.

## O que o upstream implementa

- **Bandeja de workers compacta em chip recolhível no composer (`#48581`):**
  - Condensa os indicadores de workers em pílulas compactas alinhadas à direita da barra de ferramentas do composer, com contagem dinâmica e popover detalhado apenas ao clicar.
- **Espaçamento e alinhamento visual da queued row de mensagens (`#48564`, `#48598`):**
  - Ajusta margens superiores e inferiores, adiciona padding estruturado e assegura que mensagens enfileiradas não sobreponham os botões de ação e steer do composer.
- **Chips de prompts sugeridos contextuais para o Codex no Native Chat (`#48472`):**
  - Renderiza chips clicáveis com ações comuns de projeto (ex.: "Run tests", "Explain structure", "Find bugs") na abertura de novos chats Codex.
- **Tratamento robusto de colagem de imagens do clipboard (`#48666`, refs `#48528`):**
  - Intercepta eventos de `paste` com dados de imagem no ProseMirror, converte blobs anônimos em nomes de arquivos temporários válidos e anexa como artefatos prontos para envio.
- **Restauração determinística de foco ao fechar sheet de subagente (`#48609`, resolve Issue `#48602`):**
  - Retorna o foco do teclado diretamente ao campo de entrada do chat principal ao encerrar a inspeção de um subagente com <kbd>Esc</kbd> ou botão fechar.
- **Transferência automática de foco do teclado ao clicar em Stop/Send em split chat (`#47784`, resolve `#47780`):**
  - No `NativeChatComposerPrimaryButton`, detecta cliques esquerdos quando o elemento focado atual pertence ao editor de prompt de outro chat (`[data-native-chat-prompt-editor]`) e transfere o foco imediatamente para o composer do chat clicado, retendo o rascunho do outro split intacto e evitando envios cruzados acidentais com `Cmd+Enter`.
- **Bandeja de workers com status preciso, ações de recuperação e glifo `AgentStateDot` (`#47774`):**
  - Workers cujo processo ou sessão foi encerrado inesperadamente são exibidos como **Stopped unexpectedly** (ponto vermelho de falha) sob a seção "Needs attention", com ações diretas **Show** (abre o chat) e **Stop** (liquida o despacho pendente);
  - Unifica o ícone de workers em execução para o `AgentStateDot` (anel amarelo compartilhado) e expande a área de hover para cobrir a largura total da barra colapsada.
- **Lease de 60 segundos com expiração em `wakeOwner()` de subagentes (`#47724`, resolve `#47715`):**
  - Implementa lease temporal de 60 segundos no `ClaudeChildWork.end()` para reativar o proprietário; caso nenhum novo frame nomeie o subagente antes do prazo, a linha retorna automaticamente para o status gravado de conclusão (`done / succeeded`), eliminando badges perpétuos de trabalho.
- **Menções `@` para chats e terminais do host no composer (`#47667`):**
  - Ao digitar `@` no composer, consulta `agent.list` e `terminal.list` do host (com timeout seguro de 5s) e renderiza opções de chats e terminais como chips interativos que orientam o modelo a usar `orca agent read` e `orca orchestration send`.
- **Estilização Markdown ao vivo no composer enquanto o usuário digita (`#47719`):**
  - Aplica decorações de sintaxe Markdown dinamicamente na entrada de texto do composer ProseMirror sem aguardar o envio da mensagem.
- **Galeria unificada de imagens entre mensagens e decodificação assíncrona fatiada (`#47457`, refs `#41800`):**
  - Permite navegar por todas as imagens do viewport da conversa com setas de teclado e contador `N / M`;
  - Fatia a decodificação de payloads base64 com pausas no event loop, evitando long tasks, e descarta decodificações de imagens que já foram invalidadas do cache.
- **Faixa de worker temporário no topo de chat workers (`#43521`, commit `dbb1cf1bc41`):**
  - Exibe banner informativo no topo de workers abertos como chat e anuncia conclusão de trabalho por meio de uma região live estável (`aria-live`), evitando alertas duplicados em remontagens.
- **Pill de Side chat no composer para comandos `/btw` e `/side` (`#42129`):**
  - Digitar `/btw` ou `/side` seguido de espaço no início do composer exibe uma pílula cinza "Side chat", onde o envio abre o rascunho diretamente como conversa lateral sem poluir o chat principal;
  - Preserva a serialização do rascunho como texto puro e reconstrói o estado ao montar ou alterar disponibilidade.
- **Mapeamento de perguntas pendentes para o estado `waiting` em vez de `blocked` (`#47564`):**
  - Introduz a flag `attentionAsksOnlyQuestions` quando todas as interações pendentes de uma sessão estruturada forem perguntas; mapeia o estado visual de atenção para `waiting` (amarelo claro), reservando o estado alarmista `blocked` (vermelho) apenas para aprovações e permissões pendentes.
- **Contagem precisa de workers ativos e rolagem nativa da faixa no composer (`#47432`):**
  - Conta apenas workers genuinamente ativos no composer e permite rolagem nativa sem travar o trackpad ou forçar snap; a ação Clear remove workers finalizados imediatamente.
- **Iluminação contínua do tick da linha ativa no rail tick do Native Chat (`#47553`, resolve `#47552`):**
  - Mantém o marcador aceso para a linha correspondente mesmo quando a rolagem para exatamente no espaço vertical entre duas linhas montadas.
- **Prevenção de fechamento acidental do seletor de modelos ao clicar no scrollbar (`#47587`):**
  - Mantém o seletor aberto durante a rolagem e cliques na barra de scroll.
- **Restauração de respostas rascunhadas quando uma pergunta é substituída pelo agente (`#47485`):**
  - Devolve o texto digitado automaticamente para a caixa de comentários caso a pergunta original tenha sido reformulada antes do envio.
- **Preservação de histórico paginado ao receber snapshots mais recentes (`#45168`):**
  - Mantém mensagens antigas já paginadas (*paged-in*) quando o servidor envia novas janelas de transcrição, evitando saltos de scroll.
- **Abertura de hover cards estritamente sob foco do teclado (`#47559`):**
  - Corrige acionamento indevido de hover cards em listas após retornos com Back no teclado quando o cursor do mouse está fora da área.

- **Quebra automática de linha para sumários de tarefas em background no chat (`#47359`, resolve `#47358`):**
  - Aplica `overflow-wrap: anywhere` aos textos de sumários de resultados de tarefas em segundo plano, contendo o fluxo dentro da coluna e evitando barras de rolagem horizontais espúrias.
- **Estado `Waiting` e detalhamento de espera em itens de trabalho (`#47308`, `#47309`, `#47429`):**
  - Introduz o status formal `--status waiting --note "<o que aguarda>"`, exibindo o motivo no hover card no desktop, abaixo do título no mobile e atualizando a contagem da sidebar para "N needs you"; reverte para `In progress` automaticamente quando workers retomam.
- **Preservação integral de opções e modo Plan/Build na migração da fila de mensagens (`#47337`):**
  - Preserva modo de interação (Plan/Build), modelo, esforço de raciocínio, personality, fast mode, service tier e modo steer ao mover mensagens enfileiradas para chats substitutos.
- **Sincronização de respostas a perguntas e controle de contexto em comentários de itens (`#47464`, `#47461`, `#47385`, `#47372`):**
  - Aguarda o preenchimento de todas as respostas em conjuntos de perguntas antes de acordar o agente, vincula respostas digitadas deterministicamente à pergunta correspondente e mantém o comentário de pergunta aberto até reabertura do item.
- **Exibição sob demanda de ações de edição e exclusão na fila de mensagens (`#47346`):**
  - Revela botões Edit e Delete no hover do mouse, foco ou toque, mantendo o botão Steer permanentemente acessível em cada linha da fila de envio.
- **Migração ordenada de filas de envio e cancelamento limpo de conectores na substituição de chats (`#47200`):**
  - Ao substituir uma sessão de chat, transfere mensagens enfileiradas atrás do turno em execução diretamente para a nova conversa, mantendo autor, ordem e anexos; drena mensagens de conectores na sessão antiga emitindo aviso de parada.
- **Liberação de correio entre agentes em turnos falhos que não sejam por limite de uso (`#47220`):**
  - Executa o correio enfileirado de outros agentes no próximo turno se a falha anterior não tiver sido causada por limite de cota de uso, restringindo a pausa estrita apenas a cenários que aguardam redefinição de cota ou ação humana.
- **Anexação colaborativa de itens, PRs e arquivos entre agentes em itens abertos (`#47191`):**
  - Permite que um agente anexe URLs, PRs, arquivos e inicie workers vinculados a itens abertos por outro agente no workspace da máquina local, atribuindo os anexos ao autor chamador com rotulagem amigável ("Another agent").
- **Diffs compactos delimitados ao trecho modificado para arquivos grandes em ACP (`#47016`, resolve `#47021`):**
  - Mantém o caminho `createPatch` para textos até 256 KiB e, para textos maiores, descarta linhas compartilhadas nas extremidades gerando diff apenas sobre o trecho alterado (com tetos de 64 KiB e 256 edições), recalculando as posições originais das linhas.
- **Retenção de correspondências por título durante buscas full-text sem acertos (`#47080`, refs `#47055`):**
  - Mantém a exibição de sessões que casam por título enquanto a busca FTS está pendente ou quando não retorna acertos no texto, informando aviso suave sem zerar a lista nem perder foco e rolagem.
- **Exibição integral de comentários de perguntas abertas enquanto aguardam resposta (`#47076`):**
  - Mantém o texto completo da pergunta do agente sem truncamento em 8 linhas enquanto a pergunta estiver pendente de resposta humana, preservando espaçamento entre parágrafos.
- **Dimensionamento proporcional e prioritário de item pills em linhas Started (`#47084`):**
  - Ajusta a hierarquia flex para que a primeira linha de texto dê espaço primeiro, seguida do nome do remetente, garantindo que o chip do item e o nome preservem caracteres mínimos legíveis.
- **Linha de all-clear com avatar cinza de bot na aba Items (`#46740`):**
  - Exibe no topo da aba Items uma linha limpa de "tudo resolvido" com avatar monocromático de bot quando nenhum item demandar atenção humana imediata.
- **Store de anexos na sessão para pré-visualização de imagens ACP em memória (`#46901`):**
  - Armazena imagens geradas sem caminho em disco no attachment store da sessão ACP, expondo URIs temporárias seguras para renderização inline imediata no Native Chat UI.
- **Leitura em chunks particionados para imagens acima de 3MB em clientes pareados (`#46930`):**
  - Implementa transferência particionada via `readTextChunk` com ranges para streaming resiliente de imagens grandes entre servidor e clientes pareados sem estourar limites de mensagem.
- **Suporte a middle-click paste em editores ProseMirror no composer (`#46974`, resolve `#46953`):**
  - Conecta o manipulador nativo de `auxclick` e eventos de seleção primária ao ProseMirror, permitindo colar seleções do sistema operacional com o botão do meio do mouse.
- **Primeira linha informativa e chevron sempre visível em linhas de agentes (`#46739`):**
  - Exibe a primeira linha de texto do turno na linha do agente com truncamento elegante e mantém o chevron de expansão permanentemente visível para clareza de navegação.
- **Exclusão atômica de chats com tombstone permanente no SQLite (`#45876`):**
  - Introduz o método RPC `agentSession.delete.v1` e a opção Delete chat no menu de linha e Session History;
  - Interrompe a execução ativa com segurança, fecha abas abertas em todos os clientes pareados, exclui a linhagem de sessões `/clear` e grava tombstone permanente no SQLite para impedir re-adoção ou poluição de busca;
  - Suporta confirmação com opção de memorização "Don't ask again" configurável em Settings.
- **Linhas de chat serenas com chevron dinâmico e status na prévia (`#45881`):**
  - Posiciona o ícone da fonte à esquerda com transição suave para chevron de colapso no hover;
  - Desloca status ao vivo ("N running, N waiting") para a linha de prévia e substitui o timestamp pelo botão de menu `⋯` no hover, evitando conflitos visuais.
- **Faixa de mensagens enfileiradas limpa com ações no hover (`#46592`):**
  - Oculta botões permanentes da fila de envio, revelando ações somente no hover do mouse, foco por teclado ou toque em telas touch, alinhando a faixa à linha de atividade.
- **Menções `@` e comandos slash `/` na caixa de comentários de itens (`#46570`):**
  - Equipa a caixa de comentários de itens com os mesmos seletores de autocompletar do composer principal do chat, viabilizando menções diretas e envio de skills dedicadas.
- **Exibição de nomes canônicos do catálogo no seletor de Nova Aba (`#46583`):**
  - Resolve e exibe os nomes amigáveis dos agentes cadastrados no catálogo no picker de Nova Aba em vez de IDs internos.
- **Esqueleto (*skeleton loader*) no carregamento de itens de bots (`#46608`):**
  - Renderiza animação estruturada de esqueleto durante o carregamento assíncrono dos detalhes de itens de bots, eliminando telas vazias.
- **Continuação automática de chats após limite de uso como padrão (`#45410`):**
  - Habilita `nativeChatAutoContinueAfterUsageLimit` ativada por padrão com migração one-shot de perfis existentes no carregamento;
  - Limita a varredura pós-redefinição de cota a dois envios por rodada (mais antigos primeiro), prevenindo picos de concorrência ao reabrir múltiplos chats simultaneamente.
- **Busca por início de palavra e ordenação no autocompletar `@` de bots (`#46165`):**
  - Ranqueia menções de bots no composer do Native Chat priorizando início de palavras e escolhas recentes;
  - Preserva o prefixo `For:` antes do propósito destacado, mantém o cabeçalho de bots mesmo para bots pausados e abre menus contextuais `/` ou `$` após nomes compostos somente quando suportados pelo agente.
- **Priorização de chats interrompidos mid-turn na reinicialização (`#46009`):**
  - Ordena a retomada de chats após reinício priorizando conversas onde o agente estava no meio de um turno (`mid-reply`) para assumirem as vagas de inicialização primeiro;
  - Conversas finalizadas com apenas comandos de fundo pendentes recebem oferta de retomada sem consumir slots de agentes prioritários.
- **Suporte a pastas no menu de menções `@` do chat (`#46127`):**
  - Lista diretórios do repositório/workspace no menu suspenso de autocompletar ao digitar `@`, inserindo caminhos normalizados de pastas diretamente no composer.
- **Citações "Add to chat" renderizadas como chips compactos (`#46362`):**
  - Exibe seleções de código e texto capturadas via "Add to chat" como chips interativos com rótulo de arquivo e linha, despoluindo o composer e permitindo clique para abrir a origem.
- **Visualização inline de imagens em comentários de itens e perguntas (`#46281`):**
  - Renderiza capturas de tela e arquivos de imagem anexados a comentários de itens diretamente no feed de chat.
- **Ocultação de mensagens vazias de assistente no desktop e mobile (`#46311`):**
  - Suprime a renderização de bolhas e cartões de mensagens de assistente vazias em turnos sem saída de texto.
- **Linhas compactas de atividade com fusão de worker e link de item (`#46316`):**
  - Mantém linhas de atividade em layout de linha única e funde a indicação de inicialização de worker com o link direto para o item.
- **Preservação de instruções permanentes e `_meta` em sessões Antigravity (`#46368`, resolve `#46367`):**
  - Realiza o merge em camadas de `_meta` no servidor ACP, assegurando que `setup._meta` não destrua `launch.sessionMeta` e garantindo que `SOUL.md` e `MEMORY.md` permaneçam ativos durante a sessão.
- **Identificação visual de modelo autoselecionado no Antigravity (`#46309`):**
  - Exibe no cabeçalho e na barra de status o modelo exato escolhido automaticamente pelo Antigravity.
- **Sincronização imediata de `/rename` e `/name` do Claude com o título da aba do chat (`#44461`, resolve `#40998`):**
  - Monitora o envio de comandos `/rename` ou `/name` no Native Chat e captura o frame `session_title_changed` emitido pelo Claude durante a resposta para atualizar atômica e diretamente o nome de usuário da conversa (`setUserName`), refletindo o novo título na aba e no Session History.
- **Restauração de saídas de `/recap` na reabertura de chats Claude (`#44808`):**
  - Reconstitui o frame sintético de assistente a partir das linhas salvas `system/local_command` do transcript durante a reidratação, decodificando o comando como `command-output` e preservando a saída do `/recap` após reboots ou reaberturas de aba.
- **Teto de 8 MiB de live-text por subscriber e encerramento limpo de streams lentos (`#43994`):**
  - Implementa um limite rígido de 8 MiB para o texto ao vivo acumulado (em entrega + aguardando) em cada assinante (`subscriber-live-text-cap.ts`);
  - Quando um subscriber ultrapassa esse teto, seu stream é finalizado de forma autônoma sem afetar outros chats ou o orçamento global, permitindo que o cliente frontend restabeleça a conexão e continue a leitura suavemente a partir do seu cursor de histórico;
  - Desacopla leitores hospedados (*hosted readers*) para processos utilitários externos com retenção limitada e anotações diagnósticas de crash (`orca-retained-bytes`).
- **Linhas compactas de status para mensagens entre agentes com estado gravado do worker (`#44413`):**
  - Condensa avisos de início, tarefas e atualizações de workers em linhas compactas de status com o ícone do agente emissor, texto `"Update from <name>"`, botão de cópia e detalhes expansíveis sob demanda;
  - Vincula o badge ao estado real gravado do despacho (*dispatch state*), exibindo spinner durante execução e badge vermelho em falha, sem que restarts de workers corrompam linhas de histórico prévias.
- **Estabilização da faixa de agentes durante atualizações de sessão (`#44508`):**
  - Mantém a barra de agentes estática e imune a saltos visuais durante updates de sessão no Native Chat, eliminando reflows indesejados.
- **Streaming de grandes saídas de ferramentas na exportação de contexto (`#44203`):**
  - Transmite saídas volumosas de ferramentas diretamente em streaming durante a exportação do contexto da conversa, sem alocação do conteúdo integral na memória heap.
- **Renderização e ciclo de vida de subagentes OpenCode no Chat UI (`#39276`):**
  - Implementa o gancho de dialeto ACP `childSession` para capturar frames filhos marcados com `_meta["opencode/child-session"]`,
    vinculando o ID do agente filho à linha do tempo da conversa;
  - Cria um cartão dedicado com o nome da tarefa delegada, exibe o status ao vivo na faixa de agentes acima do composer e
    alinha as ferramentas e comandos do filho sob o seu próprio cartão.
- **Pré-visualização read-only de chats no Agent Dashboard (`#39082`):**
  - Carrega a transcrição da conversa sob demanda em modo somente leitura reutilizando o protocolo de histórico e os
    componentes de renderização de mensagens, sem inicializar provedores pesados nem interferir nas observações de PR links.
- **Notificações opt-in exclusivamente para perguntas de agentes (`#39079`):**
  - Adiciona o controle "Questions Only" nas preferências de notificação do desktop e push móvel;
  - Discrimina perguntas reais de pedidos comuns de permissão de ferramentas, notificando o operador apenas quando sua
    resposta for indispensável para o agente avançar.
- **Agrupamento de subagentes na sidebar e badges de atividade ao vivo (`#38995`):**
  - Categoriza sessões flutuantes e subagentes filhos em agrupamentos colapsáveis na barra lateral de workspaces com badges ao vivo.
- **Ação "Background" para ferramentas e subagentes Claude (`#38963`):**
  - Adiciona o botão "Background" ao lado da ferramenta em execução no chat e na barra expandida de tarefas, liberando a conversa.
- **Worker threads dedicadas para o SQLite de Session History (`#38945`):**
  - Isola a gravação do banco em uma thread dedicada e leituras/buscas FTS em conexões WAL em threads de leitura separadas com timeout de 10s.
- **Contabilização de processos fora de terminais no Resource Usage (`#39013`):**
  - Lê as tags de ambiente `ORCA_WORKTREE_ID` e `ORCA_PANE_KEY` para rastrear processos desanexados, computando como `outsideTerminals`.
- **Barra de atividade e visualizador de subagentes no Native Chat (`#38632`, `#38633`, `#38640`):**
  - Barra de atividade no desktop e folha expansível (*sheet*) no mobile listando todos os subagentes da conversa com estado vivo.
- **Supressão de textos de harness do Claude nos títulos de abas (`#39606`, resolve `#37379`):**
  - Impede que marcações de meta/harness (como `<local-command-caveat>`) sejam promovidas a título de sessão de fallback,
    preservando o título ao vivo (`✳ Claude Code`) após execuções de `/clear`.
- **Prevenção de falso status 'working' por OSC 7501 do OpenCode (`#39649`, resolve `#39619`):**
  - Filtra as sequências de escape OSC 7501 emitidas pelo OpenCode em instâncias compartilhadas (`opencode serve --service`),
    impedindo que o broadcast de status marque abas ociosas como em execução e garantindo que apenas a aba dona do comando
    exiba o status `working`.
- **Preservação de imagens geradas integradas à resposta final (`#40935`):**
  - Mantém imagens concluídas acopladas ao cartão da resposta final do assistente no desktop e cliente móvel, mesmo quando o
    artefato chega após o início do streaming de prosa;
  - Desduplica artefatos já referenciados no corpo Markdown e assegura que a projeção de histórico do SQLite retenha as
    imagens e seus controles intactos ao revisitar a sessão.
- **Exibição de modelo e nível de esforço de subagentes no painel (`#41008`):**
  - Propõe exibir badge compacto (ex.: `Opus · high`) ao lado da contagem de tokens na linha de cada subagente ativo no
    painel de agentes, extraindo a informação de `.claude/projects/.../subagents/agent-<id>.meta.json` e dos cabeçalhos de mensagens.
- **Exibição de modelo, ferramenta corrente e resultado de subagentes no chat (`#41766`):**
  - Expande as linhas de subagentes no Native Chat ("Kicked off N subagents") e Mobile: adiciona pill com modelo e nível de esforço (`Opus 5.5 · High`, `GPT-5.5 · XHigh`), linha secundária com a ferramenta ativa (ex.: `Read: src/auth/session.ts`) e, ao concluir, o texto do resultado final;
  - Adiciona hover card com role (`General purpose`, `Explore`), modelo, esforço, estado, tempo decorrido, tokens e prévia do texto;
  - Estende `NativeChatSubagentEntry` com campos opcionais `agentType`, `model`, `effort`, `operation` e `lastMessage` reconciliados do registro de child-work de Claude e Codex.
- **Importação de transcrições Kimi Code e adoção de conversas CLI (`#41955`):**
  - Implementa `kimi-transcript-import.ts` e parseador de eventos de conversas CLI do Kimi Code (`session_index.jsonl`), convertendo turnos, chamadas de ferramenta e raciocínio em mensagens nativas estruturadas;
  - Adiciona suporte no fluxo `structured-agent-cli-conversation-adoption.ts` para que sessões CLI ativas ou salvas do Kimi Code sejam importadas ou adotadas pelo Native Chat com reconciliação transparente de estado.
- **Descarte de referências de subagentes ao fechar abas de chat (`#42254`):**
  - Limpa imediatamente o mapa `activeSubagentByTab` ao fechar uma aba de chat, liberando referências em memória de subagentes abertos.
- **Barra de subagentes ativos no mobile para chats em terminal (`#42305`, resolve `#42099`):**
  - Renderiza a faixa de subagentes ativos também no cliente mobile para sessões baseadas em terminal, mantendo paridade com o chat estruturado.
- **Persistência estável de perguntas pendentes através de reinicializações (`#42307`):**
  - Restaura o estado de perguntas de escolha ou texto interativo sem disparar nova inferência ou acordar precocemente o agente antes da entrada do usuário.
- **Correspondência exata de versão do modelo Claude no banner (`#42287`, resolve `#42286`):**
  - Ajusta a regex de parse do modelo para reconhecer com precisão versões pontuais completas (exibindo `Claude Opus 5.5` em vez de simplificar para `Opus 5`).
- **Abertura de subagentes em painel deslizante (*slide-up sheet*) dentro do chat (`#42455`):**
  - Em vez de substituir toda a página de conversa, clicar em um subagente abre um painel modal deslizante ocupando 80% do painel de chat, com cantos arredondados e scrim suave sobre a conversa pai;
  - Mantém o chat principal, sua posição de rolagem e o rascunho do composer montados e intactos por baixo;
  - Exibe cabeçalho contextual com link de retorno hierárquico, seletor de subagentes aninhados, status, tokens, tempo e botão Stop;
  - Fecha facilmente com <kbd>Esc</kbd>, clique no scrim ou no botão fechar, retornando o foco diretamente para a linha de origem.
- **Suporte a subagentes no Pi Native Chat (`#42448`):**
  - Habilita a detecção e renderização visual de subagentes também em conversas estruturadas conduzidas pelo agente Pi.
- **Faixa de worker temporário no topo de chat workers (`#43521`):**
  - Renderiza uma faixa destacada no topo da interface de chat workers indicando que se trata de uma tarefa efêmera/temporária, equiparando à exibição em terminais.
- **Identificação de plugin em mensagens enviadas (`#43425`, resolve `#43424`):**
  - Exibe nome e ícone de plugins em badges dedicados nas mensagens e e-mails despachados por eles dentro do Native Chat.
- **Autocompletar com menções `@` para outros chats e terminais (`#43462`):**
  - Propõe suporte a menções digitadas com `@` no composer do chat para referenciar diretamente conversas e terminais ativos.
- **Chips navegáveis para citações "Add to chat" (`#43461`):**
  - Propõe exibir citações adicionadas ao chat como chips visuais com clique de navegação direta para a posição de origem no terminal ou arquivo.
- **Retenção de chats aguardando na restart list (`#43474`):**
  - Mantém chats que dependem de ação humana na lista de reinício pendente após reboot do app, em vez de retomá-los de modo automático.
- **Limitação de memória em filas de entrega e histórico de chat (`#43456`):**
  - Aplica teto máximo a filas de eventos de entrega e buffers de leitura histórica, prevenindo consumo descontrolado de RAM quando consumidores ficam lentos.
- **Montagem tardia (lazy) de abas de chat ocultas (`#43516`):**
  - Adia a montagem pesada do DOM e da árvore React da view de chat até o momento em que a aba correspondente é efetivamente exibida pelo usuário.
- **Indicação e acompanhamento de worktree quando o agente migra (`#43385`, Issue `#43366`):**
  - Quando um agente associado a um chat migra ou é transferido para outro worktree, o chat exibe uma faixa de contexto informando para qual worktree o agente se moveu e oferece atalho para seguir ou alternar para o novo espaço de trabalho.
- **Entrega direta de mensagens entre agentes no Native Chat (`#43380`):**
  - Restaura a entrega direta e síncrona de mensagens emitidas por outros agentes e subagentes diretamente para a sessão de chat ativa, eliminando intermediários bloqueantes.
- **Presets rápidos de modelo, esforço e velocidade no Chat (`#43607`, resolve `#43599`):**
  - Adiciona botões de atalho/chips de presets configuráveis posicionados diretamente abaixo do slider de velocidade do Native Chat, permitindo alternar combinações frequentes de modelo e esforço de raciocínio com um único clique.
- **Configuração de tecla de envio `nativeChatSendKey` (`#43600`, resolve `#43595`):**
  - Introduz a configuração `nativeChatSendKey` (`"enter"` ou `"shiftEnter"`), permitindo configurar Shift+Enter para enviar a mensagem e Enter para criar nova linha sem envio acidental.
- **Listagem de painéis de agentes antes do primeiro status report em anotações (`#43562`):**
  - No menu "Send notes to", faz fallback para o título do terminal de todos os painéis, permitindo direcionar anotações visuais para agentes logo após a criação da aba, mesmo antes do primeiro turno ou status report.
- **Sincronização do realce de Activity com o workspace e aba ativa (`#43567`):**
  - Sincroniza o highlight da view de Activity na barra lateral esquerda com o agente ou workspace atualmente em foco na área de abas.
- **Formatação de resumos de raciocínio Claude entre execuções de ferramentas (`#43610`):**
  - Propõe exibir os resumos de pensamento do Claude como linhas independentes e colapsáveis intercaladas entre as chamadas de ferramentas no Chat UI.
- **Parse e estilização de tags `<advisory>` (`#43549`):**
  - Trata tags de conselho `<advisory>` do harness OMP com componente visual dedicado em vez de exibi-las como mensagem crua de usuário.
- **Auto-hide com revelação por hover da barra lateral esquerda (`#43597`):**
  - Propõe opção para ocultar automaticamente a barra lateral e revelá-la suavemente ao passar o cursor pela margem esquerda da janela.
- **Desacoplamento de streaming e eliminação de contenção em "Sending..." (`#43908`, resolve `#43988`):**
  - Separa as filas de escrita do journal de chat para que novas mensagens e prompts não compitam diretamente na mesma fila FIFO de chats em streaming simultâneo;
  - Ajusta os checkpoints do WAL para evitar que picos de escrita congelem novos turnos de conversa.
- **Expurgo automático de linhas de status de chats encerrados (`#43954`):**
  - Limpa imediatamente as entradas de status de sessões fechadas do feed do processo principal, eliminando o acúmulo contínuo de memória durante a vida útil do host.
- **Contabilização de árvores de processos de Chat no Resource Manager (`#43983`):**
  - Rastreia e agrega o consumo de CPU e RAM das árvores de processos dos agentes em execução no Native Chat, integrando-as à exibição do Resource Manager.
- **Persistência de limpeza de atividades falhadas na view de Activity (`#44003`):**
  - Grava duravelmente o descarte de linhas de falha na view de Activity, evitando seu retorno espúrio após reidratação de estado.
- **Preservação do menu Copy nativo para texto de chat selecionado em navegadores móveis (`#42965`):**
  - Ajusta os manipuladores de toque e seleção CSS/DOM no cliente mobile web para reter o menu de contexto nativo do sistema operacional ao selecionar texto de conversa, garantindo acesso direto à ação "Copy".

## O que fazer

- Suportar exclusão de chat via RPC `agentSession.delete.v1` com tombstone permanente no SQLite (`#45876`).
- Implementar linhas de chat limpas com chevron colapsável no ícone da fonte e status na prévia (`#45881`).
- Suprimir botões permanentes na faixa de mensagens enfileiradas revelando ações sob hover ou foco (`#46592`).
- Adicionar autocompletar com menções `@` e comandos `/` na caixa de comentários de itens (`#46570`).
- Exibir nomes canônicos de catálogo de agentes no seletor de Nova Aba (`#46583`).
- Renderizar skeleton loader durante o carregamento de detalhes de itens de bots (`#46608`).
- Ativar continuação automática de chats após limites de uso por padrão com limite de dois envios concorrentes pós-reset (`#45410`).
- Adotar busca por início de palavras e seleções recentes no menu de menções `@` de bots (`#46165`).
- Priorizar a retomada de chats interrompidos mid-turn no reinício do sistema antes de tarefas finalizadas em background (`#46009`).
- Listar pastas e diretórios no popover de menções `@` do composer (`#46127`).
- Renderizar trechos de código de "Add to chat" como chips visuais clicáveis (`#46362`).
- Exibir imagens de comentários de itens inline no fluxo de conversa do chat (`#46281`).
- Ocultar mensagens vazias de assistente no desktop e mobile (`#46311`).
- Compactar linhas de atividade de chat em uma única linha com link do item (`#46316`).
- Preservar instruções permanentes do Antigravity mesclando metadados de sessão no ACP (`#46368`, resolve `#46367`).
- Exibir o modelo selecionado dinamicamente pelo Antigravity (`#46309`).
- Sincronizar comandos `/rename` e `/name` do Claude diretamente com o título da aba e do Session History (`#44461`, resolve `#40998`).
- Restaurar saídas do comando local `/recap` na reabertura de chats Claude e no Resume in New Chat (`#44808`).
- Limitar a 8 MiB o buffer de texto ao vivo de cada subscriber no processo principal com retomada por cursor (`#43994`).
- Exibir mensagens entre agentes como linhas compactas de status vinculadas ao estado do despacho (`#44413`).
- Estabilizar a faixa de agentes contra cintilações durante atualizações de sessão no Native Chat (`#44508`).
- Transmitir saídas volumosas de ferramentas em streaming na exportação de contexto do chat (`#44203`).
- Preservar o menu de contexto nativo de cópia para texto de chat selecionado no cliente móvel (`#42965`).
- Isolar filas de escrita de novos prompts do streaming de chats concorrentes para evitar travamentos em "Sending..." (`#43908`, resolve `#43988`).
- Desalocar registros de status de chats fechados do processo principal (`#43954`).
- Contabilizar processos de sessões do Native Chat no Resource Manager (`#43983`).
- Assegurar que linhas de atividade com falha descartadas permaneçam limpas após reidratação (`#44003`).
- Adicionar presets rápidos de modelo, esforço de raciocínio e velocidade no Native Chat (`#43607`, resolve `#43599`).
- Suportar a configuração `nativeChatSendKey` para permitir envio via Shift+Enter (`#43600`, resolve `#43595`).
- Listar painéis de agentes recém-iniciados no menu "Send notes to" via fallback de título de terminal (`#43562`).
- Sincronizar o destaque visual do item de Activity na barra lateral esquerda com a aba e workspace ativos (`#43567`).
- Exibir resumos de pensamento (thinking) do Claude intercalados entre ferramentas no chat nativo (`#43610`).
- Tratar e estilizar tags `<advisory>` do harness OMP com componente dedicado (`#43549`).
- Avaliar auto-hide da barra lateral com reveal por hover na borda (`#43597`).
- Exibir faixa de worker temporário no topo de chat workers (`#43521`).
- Identificar plugin de origem com nome e ícone em mensagens e mails do chat (`#43425`, resolve `#43424`).
- Adotar autocompletar com menções `@` para chats e terminais no composer (`#43462`).
- Renderizar citações "Add to chat" como chips clicáveis de navegação para a fonte (`#43461`).
- Reter conversas aguardando confirmação humana na restart list sem retomada cega (`#43474`).
- Limitar memória de buffers de entrega e leitura histórica no Native Chat (`#43456`).
- Implementar montagem tardia (lazy) da view de chat apenas quando a aba for exibida (`#43516`).
- Exibir faixa indicadora e navegação de worktree quando o agente de um chat migrar para outro workspace (`#43385`, Issue `#43366`).
- Assegurar a entrega direta de mensagens entre agentes e subagentes no Native Chat (`#43380`).
- Abrir subagentes em sheet deslizante sobre o chat nativo preservando o contexto pai (`#42455`).
- Renderizar subagentes no Pi Native Chat (`#42448`).
- Exibir barra de subagentes ativos no mobile para chats de terminal (`#42305`, resolve `#42099`).
- Preservar perguntas pendentes em reinicializações sem disparos espúrios de modelo (`#42307`).
- Exibir versão pontual exata do modelo Claude no banner (`#42287`, resolve `#42286`).
- Descartar referências e estado de subagentes abertos imediatamente ao fechar a respectiva aba de chat (`#42254`).
- Suportar importação de transcrições e adoção de conversas CLI do Kimi Code no Native Chat (`#41955`), permitindo transição contínua entre terminal e UI nativa.
- Exibir modelo, ferramenta ativa e resultado final de cada subagente nas linhas de subagentes do Native Chat e Mobile (`#41766`), com pills e hover card informativo.
- Integrar imagens geradas ao cartão da resposta final no chat nativo (`#40935`), evitando perdas e duplicações.
- Adotar badges de identificação de modelo e esforço de raciocínio de subagentes no painel de agentes (`#41008`).
- Adotar a supressão de textos de harness em títulos de abas do Claude (`#39606`).
- Isolar sessões irmãs do OpenCode no mesmo serviço (`#39649`, `#39619`), contendo sequências OSC 7501 e computando `working` apenas para a sessão ativa e seus filhos reais.
- Adotar a pré-visualização read-only de chats no Agent Dashboard (`#39082`) e o filtro de notificações de perguntas (`#39079`).
- Adotar o suporte nativo a subagentes OpenCode no Chat UI (`#39276`).
- Adotar o agrupamento visual de subagentes na sidebar (`#38995`) e a ação de backgrounding de ferramentas (`#38963`) no `brza-studio`.
- Portar o isolamento em threads de workers para o SQLite de histórico (`#38945`) e o rastreamento de processos órfãos (`#39013`).
- Integrar store de anexos da sessão para renderizar imagens de ferramentas ACP sem caminho físico (`#46901`).
- Suportar leitura particionada em faixas (chunked ranges) para anexos de imagens > 3MB em sessões pareadas (`#46930`).
- Tratar evento de paste com botão do meio do mouse no composer ProseMirror no Linux/desktop (`#46974`, resolve `#46953`).
- Exibir a primeira linha de conteúdo e chevron sempre visível nas linhas de agentes do chat (`#46739`).
- Gerar diffs delimitados apenas às linhas alteradas em arquivos grandes > 256 KiB via ACP (`#47016`, resolve `#47021`).
- Reter resultados por correspondência de título em buscas de sessões quando o FTS retornar vazio (`#47080`, refs `#47055`).
- Exibir perguntas abertas de agentes em comentários de itens sem truncamento antes da resposta (`#47076`).
- Garantir legibilidade mínima de item pills em linhas Started de mensagens do chat (`#47084`).
- Renderizar linha de all-clear com avatar monocromático de bot na aba Items quando não houver pendências (`#46740`).
- Migrar mensagens enfileiradas e encerrar com aviso itens de conectores ao trocar de chat ativo (`#47200`).
- Liberar o processamento de correio de outros agentes após falhas de turno não relacionadas a limite de uso (`#47220`).
- Suportar anotação e vinculação de itens e workers entre diferentes agentes na árvore de itens (`#47191`).
- Aplicar `overflow-wrap: anywhere` em sumários de tarefas em background para evitar alargamento da coluna de chat (`#47359`, resolve `#47358`).
- Adotar o status `Waiting` e respectivo detalhamento no hover card e telas de itens (`#47308`, `#47309`, `#47429`).
- Reter opções completas (modo Plan/Build, modelo, esforço e steer) ao migrar mensagens enfileiradas (`#47337`).
- Sincronizar envio de respostas compostas em itens aguardando resposta humana (`#47464`, `#47461`, `#47385`, `#47372`).
- Exibir botões Edit e Delete no hover/foco e reter Steer em todas as linhas da fila de envio (`#47346`).
- Renderizar pill visual de "Side chat" no composer ao digitar `/btw` ou `/side` com preservação de texto e atalhos (`#42129`).
- Mapear perguntas abertas para o status visual `waiting` em vez de `blocked` no chat nativo (`#47564`).
- Contabilizar apenas workers ativos e permitir rolagem nativa e fluida na faixa de workers do composer (`#47432`).
- Assegurar iluminação ininterrupta do marcador de turno (rail tick) entre linhas consecutivas do transcript (`#47553`, resolve `#47552`).
- Manter aberto o seletor de modelos durante interações com o scrollbar (`#47587`).
- Restaurar respostas rascunhadas na caixa de comentários quando o agente reformular uma pergunta em itens (`#47485`).
- Preservar histórico paginado de mensagens anteriores ao receber janelas de transcrição do host (`#45168`).
- Restringir abertura de hover cards estritamente à navegação focada por teclado (`#47559`).
- Transferir o foco do teclado para o split correspondente ao clicar em Stop ou Send no chat nativo (`#47784`, resolve `#47780`), evitando disparos acidentais com `Cmd+Enter`.
- Identificar workers com sessão interrompida como "Stopped unexpectedly" com ações Show/Stop e ícone `AgentStateDot` na bandeja de workers (`#47774`).
- Aplicar lease de expiração de 60s em `wakeOwner()` de subagentes para devolver o status a `done / succeeded` quando tarefas secundárias encerrarem (`#47724`, resolve `#47715`).
- Adicionar menções `@` para chats e terminais ativos no composer do chat (`#47667`).
- Renderizar estilização Markdown em tempo real durante a digitação no composer (`#47719`).
- Adotar a galeria unificada de imagens entre mensagens e a decodificação fatiada não-bloqueante no visualizador (`#47457`, refs `#41800`).
- Exibir a faixa de worker temporário com região `aria-live` estável no topo de chat workers (`#43521`, commit `dbb1cf1bc41`).
- Adotar o card flutuante de worker como pílula compacta sobre o composer com expansão sob clique (`#47980`).
- Renderizar seleções de "Add to chat" como chips interativos de navegação direta à fonte (`#47949`, refs `#43461`).
- Exibir novos chats Claude e Codex na barra lateral de workspaces imediatamente antes do primeiro envio (`#47929`, commit `bd67f13662e`).
- Otimizar leituras de turnos recentes do journal para ler apenas os envios que a janela comporta (`#47878`, commit `0edcb65de36`).
- Simplificar o card de perguntas removendo a barra de progresso em favor de contadores e setas (`#47959`, commit `925bcc7ecb9`).
- Reter o estado `Needs you` em itens quando workers iniciam com perguntas abertas (`#47941`, commit `9ccab10c6dd`).
- Cancelar itens de agente instantaneamente com um clique sem modal de justificativa (`#47934`, commit `a60bc9384c6`).
- Pre-carregar histórico de sessões para buscas instantâneas na submissão de `/resume` (`#47815`, commit `d4562c4474e`).
- Memoizar projeções de linhas de chat durante streaming com ferramentas desacopladas (`#47931`).
- Habilitar envio de prompt ou comando slash para abas de chat nativo via CLI e API de plugins (`#47854`).
- Integrar lista de mensagens pesquisável diretamente no rail do Native Chat (`#48124`, commit `374693b1414`).
- Corrigir scroll aninhado e contenção de rolagem em tool runs expandidos (`#48129`, commit `f7ddeb3f630`).
- Distinguir visualmente visualizações e artefatos gráficos da prosa de texto comum (`#48126`, resolve Issue `#48123`).
- Adotar paleta móvel de anotação de screenshots e captura de elementos no navegador (`#48074`).
- Interromper ferramentas ativas em background no momento do cancelamento do chat (`#48089`).
- Implementar steering concorrente de prompts no protocolo ACP para Antigravity (`#48078`, resolve Issue `#48077`).
- Suportar chats nativos e bots do Muse Code sobre ACP (`#48076`).
- Manter perguntas respondidas fechadas durante o replay de sessões Codex (`#48128`).
- Resumir arquivos alterados em patches multi-arquivo no Native Chat (`#48038`, commit `c6594b2c249`, resolve Issue `#48025`).
- Adotar pílula de salto direto para a questão aberta e cabeçalhos de itens condensados (`#48154`, `#48081`, commit `bb95a42edc5`).
- Exibir perguntas abertas unificadas sob botão Send único (`#47999`, commit `4e8e3501e6f`) e balão de pergunta para agentes bloqueados.
- Compactar comentários de itens até receberem foco explícito (`#48064`, commit `74d17605a62`).
- Reter o rótulo de perguntas substituídas com respostas retidas pendentes (`#48139`, commit `5d1726ce567`).
- Exibir workers de chat coordenador flutuando acima da caixa de mensagem no mobile (`#48289`, commit `c69dc71bca9`).
- Exibir apenas o nome nas linhas do seletor de menções `@` do chat nativo (`#48223`).
- Reter o tier herdado de velocidade Fast durante o steering de mensagens no Codex (`#48216`).
- Aninhar chats de workers sob a conversa de orquestração pai em clientes pareados e web (`#48271`, resolve Issue `#48268`).
- Permitir conversão direta de conversas do Claude Code existentes para Codex ou Pi (`#48247`).
- Suportar borda customizada de blocos inline de código no chat via temas da aplicação (`#48237`).
- Citar comentários da Activity de um item diretamente na caixa de comentários (`#48316`, commit `f36d846d17b`).
- Exibir o propósito do agente no menu de menção `@` em conversas mobile (`#48302`, commit `06f5660cb08`).
- Filtrar a visualização de Activity por tipo de agente (Claude, Codex, Pi) ao lado do status (`#48269`).
- Fornecer ação de Clear para falhas de workers assentados retidas no Home Chat dock (`#48296`).
- Manter a prosa de respostas visível e contínua quando intercalada por blocos de raciocínio/thinking (`#48353`, commit `6a87ef6dc1b`).
- Exibir apenas o nome canônico do agente nas linhas do seletor `@` no mobile (`#48425`, commit `004525c2f14`).
- Preservar o helper de snippets de menções utilizado pelo picker móvel (`#48415`, commit `c146a111bfc`).
- Exibir o comando shell completo ao clicar na prévia de ferramentas no Native Chat (`#48430`).
- Recarregar artefatos de imagem locais quando o arquivo em disco sofrer mutação (`#48451`).
- Oferecer opção para colapsar parâmetros de chamadas de ferramentas no balão de chat (`#48445`).
- Reter o foco do composer de mensagens após alternância de janelas via Alt-Tab no Linux (`#48461`).
- Adotar bandeja de workers compacta em chip recolhível no composer (`#48581`).
- Ajustar espaçamento e alinhamento visual da queued row de mensagens pendentes (`#48564`, `#48598`).
- Exibir chips de prompts sugeridos contextuais no Native Chat do Codex (`#48472`).
- Tratar colagem de imagens diretamente da área de transferência (clipboard) no composer (`#48666`, refs `#48528`).
- Restaurar foco no campo de entrada do chat principal ao fechar a sheet de inspeção de subagente (`#48609`, resolve Issue `#48602`).
- Interromper ferramentas de background ativas no momento em que o chat for finalizado (`#48089`).
- Exibir estado de execução do worker chip com ponto âmbar estático sem oscilação (`#48787`).
- Uniformizar margens e alinhamentos de todas as linhas acima da caixa de mensagem do composer (`#48792`).
- Importar registros de compactação superdimensionados do histórico do Codex sem truncamento (`#48767`).
- Substituir o nome completo da skill ao selecioná-la com o cursor posicionado internamente (`#48667`).
- Exibir o ícone do modo de acesso do composer (full access / ask approval) de forma neutra (`#48809`).
- Liberar leituras de transcrição enfileiradas ao fechar painéis de chat (`#48575`).
- Exibir tipo de trabalho (work type) de cada worker na bandeja de workers do chat (`#48762`, resolve Issue `#48752`).
- Apresentar workers despachados ativos mesmo antes do primeiro reporte de status no Agent Dashboard e pop-out (`#48697`).
- Renderizar imagens coladas inline no balão de envio de chat no local exato da colagem (`#48665`).
- Oferecer opção de "Fork from this response" em qualquer resposta concluída de chats OMP (`#48780`).
- Copiar anexos e imagens associadas ao copiar o texto de uma mensagem no Native Chat (`#48830`).
- Abrir inspeção de subagentes em uma slide-up sheet expansível dentro do próprio painel de chat (`#42455`).
- Manter respostas OMP visíveis após exibição de cards de recomendação/advisor (`#48862`).
- Anunciar capacidade de elicitação de formulários interativos (`ask_user_question`) para renderizar question cards no Devin (`#48904`).
- Reter o card de erro de abertura de chat até que o usuário clique explicitamente em Dismiss ou Retry (`#48833`).
- Exibir evento de compactação automática do Claude no histórico de chat (`#48929`).
- Suportar pausa de chat para que novas mensagens fiquem retidas até a retomada manual (`#49015`).
- Exibir contabilidade detalhada de tokens por sessão e por resposta na interface desktop (`#49009`).
- Adicionar atalho de teclado para rolar a transcrição de chat enquanto digita no composer (`#49033`).
- Suportar reações com emojis em mensagens de chat nativo e chats de grupo (`#48928`).
- Desbloquear envio de imagens para modelos OpenCode configurados com suporte a visão em `opencode.jsonc` (`#48930`).
- Implementar interface visual polida dedicada para o Muse (Meta) com paridade aos agentes Pi e Grok (`#49048`).
- Exibir subagentes bifurcados de comandos slash e atividade de ferramentas ao vivo no Native Chat do Claude (`#49227`, resolve Issue `#48386`).
- Reter respostas de formulários com arquivos anexados até que todas as perguntas pendentes sejam respondidas (`#49204`).
- Adicionar link direto entre o card de pergunta "Needs you" e a mensagem de chat exata que originou a pergunta (`#49240`).
- Exibir autoria e filtro por pessoa na aba Chats com altura uniforme por linha (`#49256`).
- Limitar cards de respostas mantidos em cache mobile para evitar acúmulo de itens fechados em outros clientes (`#49264`).
- Corrigir liquidação prematura de comandos slash no OpenCode 2 para garantir exibição contínua de perguntas interativas (`#49056`).
- Renderizar componentes de interface de extensões/mods do Claude Code no Native Chat (band, pane, status, toast) (`#37646`).
- Exibir progresso de fases de workflow e agentes do Claude diretamente no dock (`#49286`, resolve Issue `#49285`).
- Tornar URLs avulsas dentro de código inline clicáveis na interface do Native Chat (`#49447`, resolve Issue `#49431`).
- Eliminar congelamentos em respostas longas de chat durante o streaming (`#35462`) e cessar caminhadas repetidas de linhas (`#49422`).
- Habilitar preview de páginas HTML completas dentro de blocos de código e exportação para o Slack (`#49288`).
- Adicionar superfície de visualização de chat dedicada para o DeepSeek Harness no ACP (`#49451`).
- Adotar caixa de resposta de linha única com ações inline na visualização de itens (`#49439`).
- Suportar sugestões do próximo prompt com aceitação via Tab no chat nativo do Codex (`#49310`).
- Permitir colapsar blocos extensos de raciocínio/reasoning no OMP (`#49295`).
- Exibir subagentes em primeiro plano do Pi no chat nativo com abertura da transcrição filha (`#43861`).
- Suportar perguntas laterais `/btw` no chat nativo com paridade à CLI (`#30156`).
- Permitir execução direta de agentes ACP definidos pelo usuário no Native Chat (`#49643`).
- Oferecer botão 'Restart chat' proativo quando versão mais recente do Claude Code for instalada (`#49619`).
- Invocar skills do OpenCode como menções `@` a partir do seletor no chat nativo (`#49612`, resolve Issue `#49562`).
- Renderizar textos de itens utilizando o mesmo renderizador Markdown rico do chat com headers de código e links (`#49560`).
- Aguardar fechamento de blocos de código HTML antes de renderizar preview interativo (`#49574`).
- Enviar respostas de cards de oferta como respostas enfileiradas e nunca como steer digitado (`#49507`).
- Prevenir duplicação de mensagens do assistente sob gateways compatíveis com Anthropic com message id idêntico em streaming (`#49646`).
- Disponibilizar atalho configurável para alternar entre os modos Plan e Build no chat do Codex (`#49614`).
- Blindar a janela de chat contra congelamento em respostas runaway descontroladas do Codex (`#49575`).
- Incluir alterações efetuadas por subagentes OMP no card Changed files do Native Chat (`#49549`).
- Suportar perguntas laterais `/btw` e bifurcação de conversa para chats Antigravity ACP (`#49508`).
- Manter conclusões de subagentes do Claude devidamente liquidadas após o despertar do agente pai (`#49959`).
- Corrigir travamento visual de spinner em transferências (handoff) de bots respondidas em desktops pareados (`#49960`, resolve Issue `#49937`).
- Preservar assuntos de respostas legíveis nas notificações e cards de chat (`#49879`).
- Evitar truncamento de cards de perguntas em duas linhas para permitir leitura integral antes da resposta (`#49948`).
- Corrigir abertura do compositor ao selecionar `/goal` em chats Antigravity em vez de deixar texto simples (`#49886`).
- Colorir comandos e modos `ultrathink` / `ultraplan` / `ultracode` no compositor do chat com paridade ao Claude Code (`#49849`).
- Renderizar plugins do Claude Code que desenham respostas estendidas no chat (`cc-stretch stretchtext`, `#49777`).
- Exibir respostas do Pi como não lidas enquanto subagentes do mesmo turno ainda estiverem em execução (`#49967`).
