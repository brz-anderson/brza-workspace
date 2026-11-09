---
scope:
  - workspace
  - brza-workflow
tags:
  - tooling
  - chat
refs:
  - PLN-017
  - issue:custo-e-tokens-do-grok-nas-medicoes-da-reuniao
sessions:
  - 82c5337a-e28e-430d-8a75-66f9b304f01a
---

# PLN-017: a skill `meeting-runner` corrige os 19 desvios da P7 e passa a usar o `brza sessions` v2

Anderson autorizou em 2026-11-09 ("siga o plano"), depois de confirmar que a P7 do
[PLN-017: A reunião multiagente com personas roda como fluxo replicável: skill, `brza sessions` e painel no chat](../../plans/PLN-017-a-reuniao-multiagente-como-fluxo-replicavel/PLN-017-plan.md)
rodou com 19 desvios. Esta sessão foi a executora, no Dispatch `ctx_5877fe248b98` da coordenação "Retomar PLN-017",
registrada em [PLN-017: correções após P7 e rodada de voto informado](2026-11-09-pln-017-correcoes-apos-p7.md). O plano,
o D1 e a P8 ficam com a coordenação; esta tarefa não os edita.

## O pedido

Corrigir na skill, nesta ordem, X19 (o `worker_done` sem ids), X1 (a sessão do provedor e a medição depois do
fechamento automático) e X10 (o fato que chega tarde); depois os outros desvios da tabela de D1; trocar o transporte
dos scripts pelos verbos v2 do `brza sessions` (`brza-workflow@db6bd28`), preservando os comandos e o manifesto dos
callers; aplicar a R7 (encerramento) e a R2.1 (recibo `pending`); testes antes, teste integrado com o CLI real sem o
Studio, avaliação pela `skill-creator`, revisão independente e `brza note commit`. A `skill-creator`, do plugin
`skill-creator@claude-plugins-official`, foi carregada nesta sessão antes da primeira edição e conduziu o laço de
avaliação.

## As decisões que chegaram durante a tarefa

- **R8 (X10)**, resposta literal de Anderson em 2026-11-09, sessão `Retomar PLN-017`: "Executar rodada extra
  automaticamente. Custo: cerca de 3–5 min quando o gatilho ocorrer, com a coordenação prolongando a reunião sem
  perguntar. Se paga: quando eu estiver indisponível e o voto precisar considerar o fato novo."
- **R9 (quem participa da rodada extra)**, mesma data e sessão: "A coordenação escolhe e registra o motivo. Custo: um
  julgamento sobre participantes em cada gatilho, além da rodada. Se paga: quando o alcance do fato varia entre
  reuniões." O ponto foi levantado pelo revisor independente, porque o texto inicial fixava "só as personas afetadas"
  sem fonte.
- A duração da rodada extra é estimativa (~3–5 min, sujeita à persona mais lenta); o custo em US$ dela não foi medido na
  P7 (os US$ 0,42 são do Prumo na R2).

## O que mudou na skill

- **O transporte:** o `launch_persona.py` e o `wait_round.py` viraram tradutores do manifesto para `brza sessions
  open|send|wait|close`. Saíram o `worker-start` direto, a via híbrida, o `check --peek` e o "caixa vazia". A única
  chamada direta ao `brza orchestration` é a leitura `worker-show` do `--status`. O `--via` antigo sai 2 com a
  explicação (desvio de compatibilidade justificado: o v2 não tem mais `agent launch`, a híbrida caiu na sonda de P4a).
  Os comandos `launch_persona.py $R [personas] [--send|--release|--keep-open|--stop]`, `wait_round.py N --reuniao`,
  `tally.py`, `panel.py` e o manifesto seguem válidos.
- **Módulos novos:** `sessions_map.py` (o mapa v2 dobrado por nome, fonte única de `launch`, `wait` e `tally`),
  `common.py` (raiz, cabeçalho do `rodada-N.md`, resolução de personas, corte da `## Medida`) e `check_briefing.py`
  (X8).
- **O texto:** `SKILL.md` (199 → 257 linhas), `references/briefing.md`, `round-request.md` (tipo 5, "Fatos
  lidos", R8/R9), `narration.md`, `closing.md`, `persona.md`, `persona-worklog.md`, `synthesis.md` (`rodada_extra`) e
  `evals/evals.json` (casos 4, 5 e 6 novos; o 1 com a regra nova).

## Os 19 desvios da P7

| X | O desvio | Destino | Evidência |
| :-- | :-- | :-- | :-- |
| X1 | o recibo não trazia a sessão do provedor | corrigido: abertura por `brza sessions … --wait`, ids lidos só do mapa v2 (também depois do `close`), sem busca de transcript | `sessions_map.py`, `tally.session_ids`; `test_tally_v2` X1, `test_integration_v2` (medição depois do fechamento) |
| X2 | "Codex 0 M tokens" sem Codex | corrigido: o cartão só cita o Codex quando há Codex | `panel.py`; `test_panel_v2` |
| X3 | escalação "Worker stopped without reporting" a cada rodada | corrigido: ruído previsto contado numa linha; pergunta, `blocked` e `failed` destacados; eventos vistos persistidos por reunião | `wait_round.py`; `test_wait_round` (log real do v2), `EventosVistos` |
| X4 | medição do Claude chega no `Stop` | corrigido: "medição pendente" por 120 s e `--settle`; nunca zero | `tally.py`, `panel.py`; `test_tally_v2` X4 |
| X5 | "caixa vazia" com Run ligado | corrigido: a leitura do Run é a do v2 (`--all`, `--peek --wait`) | `test_o_script_nao_chama_mais_o_orchestration_check` |
| X6 | timeout de 2× a mediana antes da duração anunciada | corrigido: piso na duração do `rodada-N.md` + 2 min, contado do envio no mapa | `wait_round.calc_limite`; `test_nunca_encerra_antes_da_duracao_anunciada` |
| X7 | custo da sessão inteira sem rótulo | corrigido no rótulo, contrato `custo_rotulo` preservado | `tally.render_md`, `panel.py`; `test_tally_v2` X7 |
| X8 | número errado no briefing | corrigido: marca "conferido às HH:MM: `comando` → resultado" e `check_briefing.py` antes de abrir | `test_check_briefing` (o briefing da P7 sai 1 no `1.352`) |
| X9 | "Re: rodada" | corrigido: o pedido vai como turno do coordenador pelo `send` v2; o molde manda não responder por mensagem | `launch_persona.MOLDE`; `test_launch_persona` Molde |
| X10 | o fato decisivo chegou na rodada do voto | corrigido: voto só depois da síntese com os M#, linha "Fatos lidos" e aviso do `tally`; rodada extra automática pela R8, participantes pela R9 | `SKILL.md` Passo 3; `test_tally_v2` X10; casos 5 e 6 |
| X11 | horários errados no worklog da persona | corrigido no texto: `date` no briefing, no pedido, no prompt e no esqueleto do worklog | `references/`; `test_launch_persona` Molde |
| X12 | `decisoes[].quem` lido como "recomendam" | corrigido: "levantada por" e "recomendação:" | `panel.py`; `test_panel_v2` Decisoes |
| X13 | "virou: virou" | corrigido | `test_panel_v2` Virada |
| X14 | `∥` vira "ı" no painel | corrigido: `||` no HTML | `test_panel_v2` Paralelo; PNG |
| X15 | pausa de ~5 h | comportamento permitido, sem correção: o prazo só arma no `worker_done` | registrado no Passo 2 |
| X16 | três rodadas em vez de duas | comportamento permitido (escolha de Anderson), sem correção | — |
| X17 | molde improvisado da rodada extra, voto não lido | corrigido: tipo 5 no molde; o parser lê `#### O voto` e propostas `A`/`B`; voto por proposta | `test_tally_v2` X17 (worklogs reais da Trava e do Relance) |
| X18 | rodada para parte da sala não fecha no painel | corrigido: `--participantes` no `tally` e no `panel`, `--personas` no `wait_round`, nomes no `--send` | `test_tally_v2` X18, `test_panel_v2` X18 |
| X19 | `worker_done` sem `--task-id`/`--dispatch-id` | corrigido: nenhum comando próprio de `worker_done`; o do preâmbulo, com os ids; `--status` confere o aceite no `worker-show` | `launch_persona` Molde e Status; `test_integration_v2` Encerramento |

## Testes, avaliações e revisão

- **Suíte:** 149 → 292 testes OK
  (`cd .claude/skills/meeting-runner && python3 -I -m unittest discover -s scripts/tests -p 'test_*.py'`). Cada teste de
  defeito rodou antes contra a cópia da skill anterior e falhou; os logs vermelho e verde ficaram no scratch.
- **O teste integrado** carrega o `brza-sessions` real e troca só o app e o `brza` por fakes com os JSON reais da sonda
  de P4a e da P7: abertura com identidade no mapa e Run único, envio com `round_id`, status certo × velho × de outro
  remetente, `closing` × aceite × `stop_unknown`, medição depois do fechamento. Nenhum comando tocou o Studio.
- **Painel:** a R3 da P7 com o subconjunto, conferida por PNG a 736 px.
- **Avaliação pela `skill-creator`** (skill nova × a cópia anterior, Sonnet): iteração 3, casos 1, 4 e 5 — 97% × 73%;
  iteração 4, casos 5 e 6 depois da R9 — 100% × 84%. O caso 6 não discrimina (5/5 nos dois), e a linha de base dele usou
  um campo que só a skill nova tem: o repositório vaza para a linha de base. Os casos 2 e 3 (síntese e `tally`) não
  rodaram de novo; o `tally` está coberto pela suíte.
- **Revisão independente** (`reviewer`): 15 achados, nenhum bloqueante, confiança 72; depois das correções, 82, com
  três regressões do próprio delta (evento de quem está fora da rodada perdido, `failed` liberado dado como "liberada",
  número entre crases sem marca). As três foram corrigidas com teste que falha antes; a reverificação final foi desta
  sessão, com as reproduções do próprio revisor (`stale_events2.py`: a pergunta de quem estava fora sai na rodada que o
  inclui; `b2.md` acusa o `1.352` entre crases; `b.md` segue 0), sem nova passada do revisor sobre esse último delta.

## Pendências

- **O `worker_state` do v2** (`brza-workflow`, `packages/client/bin/brza-sessions:564`) lê `dispatch.status`
  (`completed`) antes de `worker.state` (`succeeded`): o `close` de worker encerrado manda outro pedido em vez de
  liberar, e o `wait` não conclui por `worker_done`. Os `events` do `wait` vêm sem `createdAt`. Vai a issue do
  `tools-kit`, aberta pela coordenação; a skill contorna no texto e pelo `--status`.
- **O Grok tem custo e tokens em disco**:
  [O custo e os tokens do Grok entram nas medições da reunião](../issues/custo-e-tokens-do-grok-nas-medicoes-da-reuniao.md).
  O contrato desta entrega segue "sem medição".
- **Reabrir uma persona pelo `fallback`** não tem caminho no script, e o v2 responde `running:` enquanto a aba do mesmo
  nome existe (problema anterior, agravado).
- **Nenhuma reunião rodou pelos verbos v2**: a próxima reunião é a primeira com eles e pode ser a primeira das duas sem
  desvio do critério de promoção. A P7 não conta.

## Fora do workspace

- **O quê e onde:** links em `/private/tmp/mr3-skill`, `/private/tmp/mr3-ws` e `/private/tmp/pln017-sonda-ref`, e a
  pasta `meeting-runner-workspace` no scratch desta sessão (cópia da skill anterior, especificação, logs vermelho e
  verde, avaliações, visores e a revisão). **Risco:** espaço em disco; apagar antes da conferência perde a evidência.
  **Estado:** ativo. **Como desfazer:** `rm` dos três links e da pasta do scratch depois de a coordenação fechar a P8.

## Correção posterior: a conferência independente de `d12ed91`

A conferência independente da sessão principal (Dispatch `ctx_9c4702bb2c23`) confirmou a dedupe dos eventos, o `failed`
liberado, o voto por proposta, o subconjunto e a R8/R9, e achou quatro pontos, voltados a esta tarefa no Dispatch
`ctx_4cffc4ff5523`.

- **Ressalva ao que está acima:** a frase "`b2.md` acusa o `1.352` entre crases" vale só para o número **sem unidade**
  dentro da crase. O `b2.md` usa `` `1.352` arquivos ``, com a unidade fora, e não cobria o A1: dentro das crases
  passavam `` `1.352 commits` ``, `` `163 arquivos` ``, `` `US$ 0,25` ``, `` `R$ 1.200` ``, `` `+19.165/−6.137` `` e
  `` `1352 de 2000` ``, que fora delas eram acusados. O texto acima fica como estava, por histórico.
- **A1, corrigido:** o `check_briefing.py` tira da crase só o que é comando, caminho, id, hash ou ref (`eh_codigo`) e
  passa o resto pela mesma regra de número de fora. Regressão `NumeroComUnidadeEntreCrases`: o mesmo fato tem o mesmo
  veredito dentro e fora das crases (nove formas, entre elas unidade longa, acento, moeda, razão e diff); comandos,
  caminhos, Dispatch, Run, tag, plano, `R6`, hash, `#39020` e `arquivo:linha` seguem ignorados; e a marca
  "conferido às HH:MM: `comando` → resultado" libera o item.
- **A2, só documentado:** o `--status` sem `--wait-settled` é consulta informativa e sai 0 quando leu todas as personas,
  com o `falhou` explícito na linha. O código de saída não mudou; o `SKILL.md` e o `closing.md` dizem que a decisão por
  rc é do `--wait-settled` (0, 1 ou 75).
- **A3, corrigido no texto:** o título da rodada extra no `SKILL.md` e no tipo 5 do `round-request.md` deixou de dizer
  "parte da sala" e passou a dizer "com os participantes que a coordenação escolhe", como a R9.
- **A4, corrigido:** o cartão do painel só cita o Codex quando há Codex entre os participantes (`CodexForaDaRodada`), e a
  tabela do chat só diz "Custo e latência dos Claude: total da sessão" com algum Claude na rodada
  (`NotaDosClaudeSoComClaudeNaRodada`); no painel, o cabeçalho "Custo (total da sessão)" segue a mesma regra
  (`CabecalhoSemClaude`, achado ao conferir o PNG). O `custo_rotulo` do estado e os números não mudaram.
- **Visto no PNG e fora do escopo:** sem `custos_coordenacao` no `sintese-N.json`, o cartão da coordenação mostra
  "US$ 0 … até —", embora o `synthesis.md` diga que o cartão some. É anterior a esta tarefa; fica como pendência.
- **Verificação:** as quatro regressões falharam no código de `d12ed91` e passam agora; a suíte foi de 292 a 300 testes
  OK. As sondas da conferência (`b.md` e `b2.md`, os mesmos fatos dentro e fora das crases) e as do revisor rodaram de
  novo: dentro e fora dão o mesmo veredito; o `b.md` do revisor segue 0, e o briefing da P7 segue 1, com o `1.352` na
  linha 22. A reverificação independente deste delta fica com a sessão principal.

## Medida

Corrido 1 h 1 min — agente 26 min, quem pediu 36 min, pausa 0 s · US$ 37,41 (turnos 15,80, subagentes 21,61) · CPU 84,19 s do `claude` e 608,74 s dos comandos, RSS até 534 MB · 18 turnos, 1 sessão · até 19:56 de 2026-11-09, pelo `brza note commit`
