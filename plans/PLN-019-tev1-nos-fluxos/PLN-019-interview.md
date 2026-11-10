# PLN-019 — Entrevista

As rodadas 2 a 5 nasceram na reunião "tev1 nos fluxos" de 2026-11-09, das seis personas, do revisor independente e das
medições da coordenação; o Terreno e o Desenho estão no [plano](PLN-019-plan.md). Cada opção traz o custo e quando se
paga; a recomendada vem primeiro. Vão em texto, uma rodada por vez, com a proposta à vista; nenhuma está respondida.

## Rodada 2 — o cliente e os dados (preparada 2026-11-09, não enviada)

**R2.1. Onde mora o cliente do `tev1`?** (levantada por Bitola, Fagulha, Ferrolho; D1 da R2)

1. **Módulo folha `brza_mcp/classify.py` + verbo `brza classify` (Recomendado).** Custo: um módulo, um verbo e os
   testes, na fase 1 (~3 h, inferido). Se paga: na fase 2, quando o resolver, o `tally.py` e o hook chamam o mesmo POST.
   - Votos: 6/6 na R2 (D1c); R3: apoio de Fagulha e Faro, ressalva de Balança, Ferrolho, Bitola e Lida.
   - **A favor:** "(a) sozinho acopla o `tally.py` ao MCP por 4 células" — Bitola, R2.
   - **Contra:** "o log do POST que já existe não espera o módulo novo" — Balança, R3 (entra como fase 0).
2. **Só o módulo.** Custo: o `tally.py` e o hook importam o `brza_mcp`. Se paga: agora, se o import for barato.
3. **Só o verbo.** Custo: um processo por chamada no hook (~arranque, não medido). Se paga: nunca no volume da
   auditoria (510 fatos `rodado`).

**R2.2. Quanto tempo o texto fica em `.measurements/classify/`?** (Balança, Fagulha, Faro, Ferrolho, Lida; revisor,
achado 4) — os textos são do próprio workspace, na máquina de Anderson, fora do git; vale para os três escritores (o
parágrafo da auditoria, o `task` do resolver, o `state` do cliente).

1. **Até a pergunta passar ou falhar a régua, com teto de 180 dias, limpeza pelo módulo de gravação ao gravar
   (Recomendado).** Custo: ~8 KB por texto no teto de contexto (inferido), ~8 MB a cada mil; nenhum job. Se paga: na
   fase 3 — o `gatilho` precisa de ~10 reuniões e o `fato_rodado` de ~7 semanas para chegar a n = 30 (revisor).
   - A favor: "segurar o da pergunta até ela passar ou falhar a régua, não apagar em 30 dias" — Balança, R4.
   - Contra: "coleta mínima, acesso restrito e exclusão verificável antes da linha zero" — Ferrolho, R4.
2. **90 dias fixos.** Custo: o `gatilho` pode não chegar a n = 30 no prazo. Se paga: nas perguntas de volume.
3. **30 dias** (proposta da sala na R3). Custo: apaga o corpus do `gatilho` e do `fato_rodado` antes de n = 30. Se paga: nunca para calibrar.
4. **Só o hash.** Custo: o corpus não existe. Se paga: nunca — "hash sem texto não calibra" (Balança, R3).

**R2.3. Quem executa o código?** (inferência da coordenação, `README.md:12-14`: o `tools-kit` é dono do `brza`, dos
scripts e dos plugins; o `playground` testa fluxos antes de entrarem no ferramental. O cliente e o resolver estão no
`brza-workflow`; o `tally.py`, na meeting-runner deste workstream)

1. **O plano mora aqui; os passos do `brza-workflow` (cliente, verbo, resolver, hook) vão ao `tools-kit` por pedido
   no `Retomar` dele; os do `tally.py` e do painel ficam aqui (Recomendado).** Custo: dois workstreams no mesmo
   plano, com o pedido atravessando. Se paga: na fase 2, porque cada código fica com o dono dele pela norma.
2. **Tudo aqui, com worktree no `brza-workflow`.** Custo: o `playground` mexe no ferramental de outro workstream. Se
   paga: só se o `tools-kit` estiver parado.
3. **Tudo no `tools-kit`.** Custo: a meeting-runner, que consome primeiro e mora aqui, fica longe do código. Se paga:
   quando a skill subir ao core.

**R2.4. Sem Ollama, o que o cliente faz?** (C4, 4 personas)

1. **`unknown` explícito, sem retentativa; o consumidor decide pelo `on_doubt` (Recomendado).** Custo: cada consumidor
   escreve o seu caminho de dúvida. Se paga: agora — o caminho de hoje não muda quando o Ollama cai.
2. **Cai sempre no Haiku.** Custo: 3,7–7,0 s e ~US$ 0,01 por chamada (M6). Se paga: só no `layer`, que já faz isso.

**R2.5. O prazo de uma chamada ao `tev1`?** (revisor, achados 5 e E; Ferrolho e Lida, R3)

1. **2.500 ms na sombra, com `keep_alive` de 5 min; estourou, `timeout` e o consumidor segue pelo `on_doubt`
   (Recomendado).** Custo: até 2,5 s de espera no dispatch, e ~5 GB de memória ocupados por mais tempo. Se paga: na
   fase 2 — a chamada fria soma ~1,16 s de carga aos ~780 ms de 5.000 caracteres (revisor), ~1,9 s.
2. **1.500 ms, contando o `timeout` como dado.** Custo: a sombra perde quase toda chamada esporádica, que é fria. Se
   paga: só com uso contínuo.
3. **20 s, como hoje.** Custo: um Ollama travado segura o dispatch 20 s (M6). Se paga: nunca.

**R2.6. Onde mora o módulo de gravação?** (revisor v4, achado A; Bitola, R5) — o `fact_audit.py` é norma comum
(`.brza/core.lock:13`), editada no `core/` do `brza-workflow`; o resolver mora em `packages/mcp`.

1. **No `core/` do `brza-workflow`, ao lado do `measure.py`; o resolver o carrega pelo `BRZA_WORKSPACE` (Recomendado).**
   Custo: um `brza sync` e um teste em `tests/hooks`, ~+1 h (revisor). Se paga: na fase 0 — um formato serve aos três
   que gravam.
2. **Duas cópias, no hook e no `brza_mcp`.** Custo: os formatos se afastam com o tempo. Se paga: nunca.

## Rodada 3 — a régua (preparada 2026-11-09, não enviada)

**R3.1. Quando uma pergunta liga?** (Balança, Faro, Ferrolho; D3)

1. **Classe cara n ≥ 30, FN 0 nela fora da amostra do limiar, FP declarado (Recomendado).** Custo: meses de sombra no
   gatilho; semanas no `fato_rodado`. Se paga: quando a primeira pergunta passar — ou quando a tabela mostrar que o 4B
   não serve e o plano para.
   - Votos: 5/6 na R2 (D3a); Faro (b).
   - **A favor:** "meu ≤ 2% com n ≥ 50 esconderia um 'sim' perdido; M11 mostrou 50% de FN" — Fagulha, R2.
   - **Contra:** "exigir FN = 0 absoluto com 6 amostras induz overfitting" — Faro, R2.
2. **Conformal, α ≤ 5%, n ≥ 50.** Custo: a teoria certa, com n que não existe. Se paga: na fase 4, com volume.
3. **≥ 100 positivos e teste cego por reunião.** Custo: rotulagem dupla. Se paga: nunca no ritmo de hoje.

**R3.2. De onde vem o rótulo?** (Lida, Ferrolho)

1. **Do desfecho que já existe (veredito do Haiku, voto final, `fact_outcome`), à mão só na divergência, mais uma
   amostra das concordâncias (Recomendado).** Custo: o erro que o `tev1` e o Haiku compartilham escapa (Ferrolho). Se
   paga: agora — não cai na atenção de Anderson.
2. **Rotulagem dupla cega.** Custo: a segunda pessoa não existe (Lida, R2). Se paga: nunca.

**R3.3. O portão de entrada no catálogo (P6)?** (Bitola)

1. **Cortes de 80% e 10%, provisórios até o primeiro probe (Recomendado).** Custo: um probe de ≥ 20 pares por pergunta
   nova. Se paga: no primeiro M12 que ele evitar.
2. **Sem portão.** Custo: a pergunta que diz "sim" em tudo entra no log. Se paga: nunca.

## Rodada 4 — o que começa (preparada 2026-11-09, não enviada)

**R4.1. A cópia do parágrafo e o `task` do resolver: quando?** (revisor, achado 1; Lida e Bitola, R4)

1. **Fase 0, antes do cliente, logo depois da política de texto (R2.2) (Recomendado).** Custo: ~3 h no hook, no resolver,
   no módulo de gravação e no `brza sync` (inferido). Se paga: no primeiro dia — cada auditoria apaga um parágrafo (52 em 9,4 dias).
   - A favor: "a linha zero no resolver começa esta semana, antes de extrair `classify.py`" — Bitola, R4.
2. **Na fase 3, como na v2.** Custo: ~5 parágrafos perdidos por dia nas fases 1 e 2 (revisor). Se paga: só se o
   cliente mudar o formato do que se grava.

**R4.2. O catálogo segue o portão P6?** (revisor, achado 2)

1. **Sim: os quatro probes rodam na fase 2 e só as aprovadas entram; o `layer` está reprovado hoje (86% "alta")
   (Recomendado).** Custo: rotular à mão ≥ 20 pares por pergunta (a máquina leva menos de 1 min); o probe do `layer`
   espera a fase 3, por falta de `task` (revisor v4, achados C e D). Se paga: na fase 4 — a tabela não mistura pergunta
   enviesada.
2. **As quatro entram como provisórias.** Custo: o P6 vira letra morta. Se paga: nunca.

**R4.3. A ordem do gatilho no painel?** (Bitola, Fagulha, Ferrolho, Lida; revisor, achado 3)

1. **Primeiro o replay cego, com o `state` que o `tally` monta, nas reuniões rotuladas; só então o painel, com a lista
   inteira e "não calibrado, n_sim = N" (Recomendado).** Custo: ~1 h, uma vez (inferido). Se paga: na primeira reunião
   com a ordem, se o replay mostrar que a cauda não some.
   - A favor: "a ordem visível exige comparação antes do uso" — Ferrolho, R4.
   - Contra: "autoriza a sugestão ordenada no painel da próxima reunião, lista inteira e sem efeito? Recomendo que sim" — Fagulha, R4.
2. **No painel já, lista inteira e a marca.** Custo: ancoragem — 3 dos 6 "sim" vêm depois da 10ª posição (M17). Se
   paga: se a coordenação já lê a lista inteira.
3. **Adiar para a fase 4.** Custo: nada visível por meses. Se paga: quando a tabela passar a régua.

**R4.4. A prioridade do plano?**

1. **`medium` (Recomendado).** Custo: entra depois do que está `high`. Se paga: o valor é corpus, não urgência.
2. **`high`.** Custo: desloca o PLN-017/PLN-018. Se paga: só se a rodada extra da R8 virar dor.

**R4.5. O `fato_rodado` grava a saída do comando que o fato cita?** (revisor v4, achado B)

1. **Sim, só o `run` citado, sob a política da R2.2 (Recomendado).** Custo: a regra que casa fato com `run`, e saída de
   comando em disco. Se paga: na fase 4 do pré-filtro — sem ela, o `tev1` não tem contra o que julgar.
2. **Não, e o pré-filtro sai do plano.** Custo: perde o maior volume (M7), com teto de ~US$ 0,72/dia (M16). Se paga:
   já, em simplicidade.

## Rodada 5 — as evoluções (preparada 2026-11-09, não enviada)

**R5.1. O retreino `tev1-brza`?** (D5)

1. **Evolução aberta, só com o corpus da fase 3 (Recomendado).** Custo: nenhum agora. Se paga: se a fase 4 mostrar que
   o 4B base não passa a régua.
   - Votos: 5/6 (D5b); Lida (a).
2. **Fora do plano.** Custo: o plano termina em "o 4B não serve" sem alternativa. Se paga: agora — "manutenção mensal"
   (Lida, R2).

**R5.2. O diálogo de startup do Studio?** (D4)

1. **Contar os misses do regex primeiro (Recomendado).** Custo: um contador no Studio. Se paga: se a contagem der
   dezenas por dia (Lida, R3).
2. **No miss do regex, já** (Faro). Custo: a fila única no caminho de um worker travado. Se paga: sem volume, nunca.

**R5.3. Quando o plano se revê?**

1. **Quando uma pergunta chegar ao n da classe cara (Recomendado).** Custo: sem data. Se paga: a revisão tem dado.
2. **Em 30 dias.** Custo: a revisão pode chegar sem n. Se paga: se o corpus crescer depressa.
