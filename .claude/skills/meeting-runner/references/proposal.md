# A proposta, o revisor e a contraprova

Um arquivo por versão, `.sessions/<reuniao>/proposta-vN.md`. A coordenação monta a proposta das rodadas, da prova de
conceito e do revisor. **Nada nela está decidido**: as decisões são de Anderson.

## O molde

```markdown
# Proposta ‹tema› (v‹N›, não aprovada)

> Rascunho da coordenação, montado com as rodadas ‹1 a K› das ‹N› personas, a prova de conceito da coordenação e o
> revisor independente. **Nada aqui está decidido**; as decisões são de Anderson. Marcas de evidência: **[medido]**
> rodou hoje, com a saída; **[lido]** doc, `--help` ou código; **[inferido]** ninguém testou. Marcas de origem: **R3**
> veio da rodada 3; **revisor**, do revisor independente; **contraprova**, da contraprova.

## O requisito
‹o que a proposta entrega do pedido, e o que não — "parcial" se for parcial›

## O que se mediu

| # | Fato | Marca |
| :- | :--- | :---- |
| M1 | ‹fato, com a saída resumida› | [medido] |

## As alternativas

| Alternativa | Atende o requisito? | Custo | Risco | Se paga |
| :---------- | :------------------ | :---- | :---- | :------ |

## A confiança do plano

| Quem | Número | Base |
| :--- | -----: | :--- |
| **Revisor independente** | NN | **a confiança do plano** (R2.3) |
| Sala (média, mediana, n, faixa) | NN, NN, n/N, a–b | Antigravity fora da conta |
| Antigravity (à parte) | NN | confiança relatada, não somada |
| Diferença sala − revisor | ±NN | registrada em toda reunião, para medir |
| Contraprova (se houve) | NN | sessões novas, modelos baratos |

## Para Anderson decidir
‹cada decisão como pergunta com opções; o texto vai ao `references/closing.md`›
```

**Cada linha leva origem e evidência.** A proposta v2.1 da MCP separou "provado" de "inferido" e foi o que o revisor
mais atacou. Evidência `[medido]` exige a saída do comando na própria linha, não só "medido".

## O revisor independente

- Subagente `reviewer` (camada alta), **fora da sala**, em toda versão que vai a Anderson; não vê as confianças da sala.
- Peça a ele as cinco conferências da memória do papel (`.claude/agent-memory/reviewer/meeting-plan-review-patterns.md`):
  confiança × regra, atribuição pela rodada antiga, valor trocado, horas herdadas, "confiança se…" somada; e a correção
  que deixa o caso irmão.
- **O número dele é a confiança do plano.** Nas duas reuniões ele achou o que mudou o desenho (a mensagem remota como a da
  pessoa; os mixes do chat) e ficou 12 e 17 pontos abaixo da sala; na MCP v3.2 ficou 3 acima, em versões diferentes.
  Nenhum desconto fixo vira regra: registre a diferença a cada reunião e a medição decide depois de ~5.

## A contraprova (opcional, por gatilho)

**Gatilho:** a proposta vai a aprovação **e** (a decisão é cara de reverter **ou** sala e revisor divergem mais de 10
pontos). Fora disso, não rode: custou ~US$ 9,8 de Claude na Carvão (a coordenação que a conduziu pagou US$ 6,28 do total
em 13 min), não os US$ 3,5 que se pensava.

- **Formato:** R1 refeita às cegas mais a confiança na proposta, sessões novas, contexto limpo, outros modelos baratos:
  Haiku `low`, Sonnet `medium`, Grok Fast `low`, Codex Terra `medium`; **sem Fable**.
- **O pedido:** igual ao de R1, com "não leia os outros worklogs da reunião, nem a síntese, nem a proposta" até o pedido
  mandar. Worklogs `…-contraprova-<slug>.md`.
- **O que ela mede:** se a posição é da persona e a confiança é do modelo. Registre em quanto a confiança dos autores
  (sala) difere da dos novos modelos.
