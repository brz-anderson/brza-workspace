---
status: open
phase: interview
origin: issue
origin_ref: tev1-como-classificador-nos-scripts-da-meeting-runner
description: Classifica com fatos medidos os usos do tev1:4b nas seis frentes e o liga por um cliente único que grava o corpus em sombra e só decide quando cada pergunta passa a régua
ready: "não — aguarda as rodadas 2 a 5 da entrevista; a fase 0 espera a política de texto (R2.2)"
estimate_h: 14
executed_h: 0
remaining_h: 14
scope:
  - workspace
  - brza-workflow
opened: 2026-11-09
owner: Anderson
tags:
  - tooling
---

# PLN-019: O tev1 local entra nos fluxos por um cliente único, em sombra, até cada pergunta passar a régua

- **Retomar:** a reunião de 2026-11-09 entregou o Terreno, a classificação e o desenho; próximo passo, a Rodada 2 (o
  cliente e os dados) da [entrevista](PLN-019-interview.md), em texto.
- **Dividido:** [PLN-019 — Entrevista](PLN-019-interview.md)

## Pedido

- **Origem:** [O `tev1` local classifica nos scripts da meeting-runner, depois de calibrado com as três reuniões](../../work/issues/tev1-como-classificador-nos-scripts-da-meeting-runner.md);
  e o pedido de Anderson na sessão da meeting-runner de 2026-11-09, que abriu a reunião "tev1 nos fluxos".

> "discutir ações e opções, em diferentes frentes - CLI | Studio | MCP | meeting-runner | plan-runner |
> migration-runner - de como integrar o `tev1` rodando via `Ollama` aos nossos fluxos, busque classificar, com fatos
> medidos, os melhores usos para o modelo; […] até ter um plano sólido, já com Terreno medido, opções, esboços de
> desenho; já pronto para entrevista, procure já vir com o máximo de rodadas de perguntas prontas que puder"

Saída, no gate: "opção 1 + criar o plano, nesse workstream, mapeando para onde o plano pode evoluir".

### Cobertura

| Origem | Critério de aceite | Passo | Teste (nível) |
| :----- | :----------------- | :---- | :------------ |
| Pedido 1 | os usos nas seis frentes estão classificados, cada um com o fato medido que o decide | — | Terreno e D1 (conferência do revisor) |
| Pedido 2 | o texto que passa pelo `tev1` e pela auditoria deixa de se perder | P0 | um append por auditoria e por dispatch (unidade) |
| Pedido 3 | um cliente único, com falha explícita, serve às frentes | P1 | `too_long`, `no_ollama`, `timeout`, `bad_choice` (unidade) |
| Pedido 4 | nenhuma pergunta muda rota antes de passar o portão e a régua | P2, P4 | o probe P6 gravado; a tabela por limiar (unidade) |
| Pedido 5 | o plano mapeia para onde evolui | D6 | — |

### Fora de escopo

- **Implementar código na reunião.** Fora, pelo gate; o código começa na P0, a pedido.
- **Título do terminal do Studio, cota, conta, gate do dispatch; o `tev1` como persona, síntese ou revisor.** Fora, por
  6 de 6 na R3 (P7) — latência de ms, regra numérica, o modelo só escolhe opção.
- **O sugestor dos 494 fatos pendentes e a fila ordenada da auditoria.** Fora: 467 são `inferido`, sem saída gravada, e
  a auditoria não tem fila (M20; `fact_audit.py:244-251`).
- **A operação do migration-runner.** Fora até haver uso (0 acionamentos, M10).

## Restrições

- **Nada liga antes do portão e da régua.** O `min_confidence` nulo grava e não decide (R2: 6 de 6).
- **O cliente nunca trunca.** Acima do teto, recusa (`too_long`).

## Entrevista

### Rodada 1 — o gate da reunião (enviada 2026-11-09)

> **Apresentado antes:** a leitura da coordenação do pedido e da issue de origem.

Respondida em 2026-11-09.

1. **O objeto.** Opções: as seis frentes, o `tev1` como está (recomendada) — custo: nenhum; se paga: agora · incluir
   papéis gerativos — custo: ~1 rodada a mais; se paga: só se a medição mostrar uso gerativo · só a meeting-runner —
   custo: perde cinco frentes; se paga: se a reunião tivesse menos de 1 h. **Decidido — as seis frentes.**
2. **Fora do tema.** Opções: retreinar; trocar Ollama ou modelo; implementar hoje; a promoção da meeting-runner. **Decidido
   — só "implementar código hoje" fica fora**; retreino e outro modelo ficam dentro.
3. **A saída.** **Resposta:** "opção 1 + criar o plano, nesse workstream, mapeando para onde o plano pode evoluir".
4. **O `tev1` na sala.** **Decidido — as personas chamam só para medir acerto; a latência que entra é a da coordenação.**

As rodadas 2 a 5 estão preparadas, sem resposta, no [arquivo da entrevista](PLN-019-interview.md).

## Desenho

### O que este desenho assume

- **R1.1:** as seis frentes, com o `tev1:4b` como está.
- **R1.2:** retreino e outro modelo local estão dentro do tema, como evolução.
- **Reunião, R2 6/6:** nada liga antes da tabela por pergunta; o cliente é um módulo com verbo fino.

### Terreno

> Medido na reunião de 2026-11-09; os scripts e as saídas ficaram em `.sessions/reuniao-tev1/material/`, fora do git,
> e a proposta final está copiada no worklog da coordenação.

#### O modelo e o endpoint

- **M1 · latência.** ~96 ms (50 palavras) a ~745 ms (1.400), quente e sem concorrência; 3 perguntas custam ~65–90 ms a
  mais que 1; carga a frio 1,16 s. [medido]
- **M2 · fila única.** 8 chamadas levam ~1,85 s com 1, 4 ou 8 em paralelo. [medido]
- **M3 · teto.** Acima de 2.048 tokens, HTTP 400, sem truncar; com texto real, ~5.000 caracteres. [medido]
- **M4 · a `confidence`** é 1 − a entropia das probabilidades: mede a margem, não o acerto. [inferido]
- **M14 · ordem das opções.** Pesa no critério vago (`evento`: 0 → 7 de 17 "não" certos), não no `layer`. [medido]

#### As perguntas medidas

- **M11 · gatilho voto × fato novo.** 23 pares reais, rótulo à mão: 3 de 6 "sim", 15 de 17 "não"; os perdidos são de
  taxa-base, `confidence` 0,013–0,115. [medido, Balança]
- **M12 · `evento`** sai "sim" em 23 de 23. [medido]
- **M13 · `layer`.** 252 descrições reais: 39% sem o papel, 22% no `general-purpose`; "alta" em 86%. [medido]
- **M5 · voto de célula.** `None` em 4 de 98; "apoio" lido como "ressalva" em 22 de 37. [medido]
- **M17 · ordem do gatilho.** AUC 0,74; os 3 primeiros acertam; a taxa-base nas posições 11, 15 e 16. [medido]

#### Os fluxos

- **M6 · resolver do MCP.** 7 resoluções desde 2026-11-03, nunca pelo `tev1` (sem `resolver.tev1_min_confidence`);
  espera até 20 s (`~/Projects/brza-workflow/packages/mcp/brza_mcp/resolver.py:38`). [medido, lido]
- **M18 · o `task` se perde.** O resolver manda o `task` ao `tev1` e descarta o texto (`resolver.py:92`,
  `policy.py:251`). [lido]
- **M7, M16 · auditoria de fatos.** 1.564 `fact_check`, US$ 7,16 em 10 dias (~US$ 0,72/dia), 510 `rodado`. [medido]
- **M8 · a evidência se perde.** `.claude/hooks/fact_audit.py:428-430` apaga o parágrafo a cada auditoria. [lido]
- **M9 · Studio.** Falha e cota já tipadas; o regex do diálogo de startup quebrou com o Codex 0.157
  (`~/Projects/brza-studio/src/main/runtime/startup-dialog-blocked-signals.ts:4`). [lido]
- **M10, M15, M20.** plan-runner 44 usos, close-task 18, migration-runner 0; 49 turnos com `prompt_head`; 467 dos 494
  fatos pendentes são `inferido`. [medido]

### D1 — A classificação dos usos

- **Origem:** reunião, R1–R4; revisor.

| # | Uso | Frente | Hoje | O que o destrava |
| :- | :-- | :----- | :--- | :--------------- |
| 1 | Parar de perder o texto (parágrafo da auditoria, `task` do resolver) | hook, MCP | P0 | a política de texto (R2.2) |
| 2 | Gatilho como ordem visível, lista inteira | meeting-runner | P2b | o replay cego |
| 3 | Gatilho como decisão (rodada extra da R8) | meeting-runner | sombra | n_sim ≥ 30 e critério de taxa-base |
| 4 | `layer` do resolver | MCP | fora do catálogo | o probe P6 no `task` inteiro |
| 5 | Pré-filtro dos fatos `rodado` | hook | sombra no que cabe | o corpus da P0 |
| 6 | Reserva do voto `None` | meeting-runner | sombra barata | — |
| 7 | Diálogo de startup do Studio | Studio | evolução | contar os misses |
| 8 | "É plano?", "mudou o assunto?" | plan-runner, close-task | evolução | corpus |
| 9 | Operação do migration-runner | migration-runner | fora | uso real |

### D2 — A gravação, um escritor só — `.measurements/classify/` (P0)

- **Origem:** revisor, achados 1 e 4; R2–R4.

```text
.measurements/classify/
  fato_rodado.jsonl   # {fato, paragrafo, run_citado, veredito_haiku, kind, at} ← fact_audit.py, no finally, antes do os.remove
  layer.jsonl         # {task, tev1_choice, tev1_confidence, haiku_choice} ← resolver, no POST que já existe
  state/<sha>.txt     # o state de cada chamada do cliente (P1 em diante)
```

- Um módulo de gravação, usado pelo hook, pelo resolver e pelo cliente, aplica a retenção ao gravar, sem job. A casa
  recomendada é o `core/` do `brza-workflow`, ao lado do `measure.py`, porque o `fact_audit.py` é norma comum
  (`.brza/core.lock:13`); o resolver o carrega pelo `BRZA_WORKSPACE`.
- O `fato_rodado` guarda também o `run` que o fato cita: sem ele, o pré-filtro não tem contra o que julgar.
- Nada de texto no `measurements.jsonl`; lá só o evento `classify` com metadados.
- O veredito do Haiku é rótulo provisório.

#### Em aberto

A retenção (R2.2), a casa do módulo (R2.6) e o `run` citado (R4.5), no [arquivo da entrevista](PLN-019-interview.md).

### D3 — O cliente — `brza_mcp/classify.py` e `brza classify` (P1)

- **Origem:** R2 (D1c, 6/6); R3 (Bitola, Lida, Ferrolho); revisor, achado 5.

```python
# folha: só urllib e a leitura da configuração
Classifier.ask(state: str, questions: dict[str, str | Question], timeout_ms: int) -> dict[str, Answer]
# Answer = {choice: str | None, confidence, probabilities, path: "tev1" | "unknown",
#           reason: "ok" | "too_long" | "no_ollama" | "timeout" | "bad_choice", ms, model}
```

```bash
brza classify --json < pedido.json      # {"state": "...", "questions": {"gatilho": "gatilho"}, "timeout_ms": 2500}
```

- O limite real é o HTTP 400, que vira `too_long`; os ~5.000 caracteres são a pré-checagem medida, não garantia. O
  prazo recomendado é 2.500 ms com `keep_alive` de 5 min: a chamada fria dá ~1,9 s. Sem Ollama, `unknown`, sem
  retentativa. Sem daemon. A cadeia `unknown → Haiku` é do consumidor, pelo `on_doubt` da pergunta.
- Se a folha puxar a política inteira, ou o verbo no hook passar de ~200 ms, o módulo vai a `packages/client`.

#### Em aberto

O envelope (R2.1), quem executa (R2.3), o comportamento sem Ollama (R2.4) e o prazo (R2.5).

### D4 — O catálogo, o portão e a régua (P2, P4)

- **Origem:** R1 (Bitola); R2 (D3a, 5/6); R3; revisor, achado 2.

```json
{"gatilho": {"instructions": "…", "criteria": {"nao": "…", "sim": "…"}, "classe_cara": "sim",
             "min_confidence": null, "on_doubt": "coordenacao",
             "probe": {"n": 23, "fn_classe_cara": 3, "max_share": 0.78, "order_flip": null, "em": "2026-11-09"}}}
```

- **Portão (P6):** probe em ≥ 20 pares, com o texto real; nenhuma opção acima de 80% sem o rótulo justificar; menos de
  10% trocado ao inverter a ordem. Cortes provisórios. O custo é rotular à mão ≥ 20 pares por pergunta. Hoje nenhuma
  pergunta passou; o `layer` reprova (86% "alta"), e o probe dele no `task` inteiro espera a P3 (7 resoluções desde
  2026-11-03).
- **Régua (P5):** classe cara n ≥ 30, FN 0 fora da amostra (com a classe que já errou), FP declarado, amostra das
  concordâncias revisada; rótulo do desfecho que já existe, à mão só na divergência. Dissenso: Faro, conformal α ≤ 5%.

#### Em aberto

A régua (R3.1), o rótulo (R3.2), o portão (R3.3) e o catálogo segue o portão (R4.2).

### D5 — A ordem visível do gatilho — `sugestao-rN.json` (P2, P2b)

- **Origem:** R3 (Bitola, Ferrolho, Lida); R4 (Balança, Ferrolho, Bitola); revisor, achado 3.
- O `tally.py` grava os pares voto × M# com `choice` e `confidence` em `sugestao-rN.json`, arquivo próprio.
- O painel só os mostra depois do replay cego com o `state` do `tally`, que passa se os 3 "sim" de taxa-base caírem na
  metade de cima (≤ 12 de 23); sempre a lista inteira, com "não calibrado, n_sim = N". A ordem ancora quem lê.

#### Em aberto

A ordem no painel (R4.3).

### D6 — Para onde o plano evolui

- **O `layer` com o `task` inteiro**, se passar o portão; **o alarme do gatilho**; **o pré-filtro da auditoria**,
  medido em quantos fatos cabem.
- **O diálogo de startup do Studio**, depois de contar os misses.
- **O "é plano?" e o "mudou o assunto?"**, quando houver corpus.
- **O retreino `tev1-brza`** com o corpus da P0 (5 de 6; Lida contra).
- **Um segundo modelo local**, só onde o 4B falhar medido; **a ferramenta MCP `classify`**.

#### Em aberto

O retreino (R5.1), o Studio (R5.2) e quando o plano se revê (R5.3).

## Passos

### P0 — Parar de perder o texto

Executa D2 · executor: a definir em R2.3

Estimado: 3 h · Executado: — h

- [ ] **1. Teste que falha:** a auditoria e o dispatch sem linha na tabela deixam o texto em `.measurements/classify/`.
- [ ] **2. Implementar** o módulo de gravação no `core/`, a cópia do parágrafo e do `run` no `finally` do
      `fact_audit.py` e o append no resolver.
- [ ] **3. Rodar e ver passar;** `brza sync` no workspace.

### P1 — O cliente

Executa D3 · executor: a definir em R2.3

Estimado: 3 h · Executado: — h

- [ ] **1. Testes que falham:** `too_long`, `no_ollama`, `timeout`, `bad_choice`; o resolver sem mudar a rota.
- [ ] **2. Implementar** `Classifier.ask` e `brza classify`; o `_tev1` vira chamador.
- [ ] **3. Rodar e ver passar.**

### P2 — Os probes e a sombra

Executa D4, D5 · executor: a definir em R2.3

Estimado: 5 h · Executado: — h

- [ ] **1. O comando de probe**, a rotulagem à mão de ≥ 20 pares do `gatilho`, do `voto` e do `fato_rodado`, e os três
      probes, gravados no catálogo; o do `layer` espera a P3.
- [ ] **2. As aprovadas gravam o evento `classify`**; o `tally.py` grava `sugestao-rN.json` sem ir ao painel.

### P2b — A ordem no painel

Executa D5 · executor: a sessão deste workstream

Estimado: 1 h · Executado: — h

- [ ] **1. O replay cego** nas reuniões rotuladas, ordem original contra ordenada.
- [ ] **2. Se passar,** a coluna no painel, lista inteira, com a marca.

### P3 — O corpus

A espera até n ≥ 30 na classe cara de uma pergunta, e o probe do `layer` quando houver ≥ 20 `task`: `fails` do `rodado` ~7 semanas; "sim" do `gatilho` ~10 reuniões
(ritmo medido pelo revisor). Sem horas.

### P4 — A calibração

Executa D4 · executor: a sessão deste workstream

Estimado: 2 h · Executado: — h

- [ ] **1. A tabela** limiar × cobertura × FN × FP por pergunta, fora da amostra.
- [ ] **2. A rodada com Anderson** sobre a tabela: liga, espera ou para.

### P5 — O primeiro uso

A pedido, depois da P4: liga a pergunta que passou, com o `on_doubt` dela.

## Regressão

- **O resolver devolve a mesma camada de hoje** enquanto `resolver.tev1_min_confidence` for nulo. Como se confere: os
  testes do resolver no `brza-workflow` (`tests/mcp/test_mcp_resolver.py`).
- **A auditoria dá o mesmo veredito e o mesmo tempo** com a cópia. Como se confere: os testes do hook em `tests/hooks/`.
- **O `tally.py` e o painel não mudam** com a `sugestao-rN.json` gravada. Como se confere: os testes da meeting-runner.

## Worklogs

- 2026-11-09 — a reunião "tev1 nos fluxos": Terreno M1–M20, D1–D6 rascunhados, rodadas 2 a 5 preparadas. Parou na R2.
  [Reunião tev1 nos fluxos: a coordenação](../../work/worklogs/2026-11-09-reuniao-tev1-coordenacao.md)

## Pendências conhecidas

- [O `tev1` local classifica nos scripts da meeting-runner, depois de calibrado com as três reuniões](../../work/issues/tev1-como-classificador-nos-scripts-da-meeting-runner.md)
  — a origem; os três usos dela estão em D1 (2, 3 e 6).
