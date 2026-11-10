---
scope:
  - workspace
  - brza-workflow
  - brza-studio
tags:
  - tooling
refs:
  - PLN-018
  - PLN-019
  - issue:tev1-como-classificador-nos-scripts-da-meeting-runner
sessions:
  - f497c2b6-20bf-4786-8d30-73c4cec86d58
---

# Reunião tev1 nos fluxos: a coordenação

Anderson pediu, pela skill `meeting-runner`: "discutir ações e opções, em diferentes frentes - CLI | Studio | MCP |
meeting-runner | plan-runner | migration-runner - de como integrar o `tev1` rodando via `Ollama` aos nossos fluxos,
busque classificar, com fatos medidos, os melhores usos para o modelo", em estilo brainstorm, partindo da issue
[O `tev1` local classifica nos scripts da meeting-runner, depois de calibrado com as três reuniões](../issues/tev1-como-classificador-nos-scripts-da-meeting-runner.md),
até um plano pronto para entrevista ou 00h. Esta sessão foi a coordenação. O plano saiu:
[PLN-019: O tev1 local entra nos fluxos por um cliente único, em sombra, até cada pergunta passar a régua](../../plans/PLN-019-tev1-nos-fluxos/PLN-019-plan.md).

## O gate do tema

Rodada com opções, respondida por Anderson: objeto "Esse objeto (Recomendado)" — as seis frentes, o `tev1:4b` como está;
fora, só "Implementar código hoje (Recomendado)" (retreino e outro modelo ficam dentro); saída "opção 1 + criar o plano,
nesse workstream, mapeando para onde o plano pode evoluir"; o `tev1` na sala "Sim, só leitura; latência é da coord.
(Recomendado)".

## As personas

| Persona | Papel | Runtime | Modelo | Esforço | Fallback usado |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Balança | Cética medidora | Grok | grok-4.7 | xhigh | — |
| Ferrolho | Guardião da falha silenciosa | Codex | gpt-6.1-terra | medium | — |
| Bitola | Arquiteta de integração | Grok | grok-4.6 | high | — |
| Fagulha | Provocadora | Grok | grok-4.7-build-fast | low | — |
| Faro | Pesquisador | Antigravity | padrão | — | — |
| Lida | Voz do mantenedor com pouco tempo | Claude | claude-haiku-5-5 | low | — |

Cota na abertura (`brza quota --json`): Claude 58% da sessão, Codex 54%, Grok 10% da semana, Antigravity 4%. Pelo
pedido, o Grok levou os modelos caros, o Antigravity a pesquisa e o Codex um modelo médio antes do reset das 22h35.
Todas no Run `run_e11c2e02316f`.

## As rodadas

| Rodada | Aberta | Fechada | O que produziu |
| :-- | :-- | :-- | :-- |
| R1 opinião | 21:20:22 | 21:33:55 | a calibração do gatilho (Balança, M11), a pesquisa de cascata (Faro), 5 disputas |
| R2 debate | 21:35:42 | 21:39:08 | 5 viradas pelos fatos; 6/6 em "nada liga antes da tabela" e no módulo + verbo |
| R3 voto | 21:40:40 | 21:45:35 | 48 votos, 0 contra; a família "ordem visível, sem tirar nada da lista" |
| R4 confiança na v2 | 21:47:07 | 21:49:27 | sala 80,2; as fases fora de ordem; a retenção até a régua |
| R5 confiança na v4 | 21:57:13 | 21:58:54 | sala 82,8 contra revisor 78; a casa do módulo, o critério do replay |

Sem rodada extra da R8: o M16 e o M17 nasceram na rodada de voto, mas não contradizem premissa de voto (os votos no P3
se apoiavam no corpus, não na economia).

## A medição por persona (`tally.py`)

| Persona | Confiança R1 → R5 | Mudou na R2 | Nota dos colegas (R3) | Custo |
| :-- | :-- | :-- | --: | :-- |
| Balança | 76 → 79,4 → 81,9 → 76 → 82 | virou | 9,5 | sem medição (Grok) |
| Ferrolho | 80 → 85,4 → 89,6 → 82 → 88 | virou | 8,3 | 0,45 M tokens até a R4 (Codex) |
| Bitola | 78 → 86 → 87,1 → 88 → 90 | virou | 8,8 | sem medição (Grok) |
| Fagulha | 75,8 → 80,8 → 83 → 85 → 86 | virou | 8,5 | sem medição (Grok) |
| Faro | 88,8 → 89,4 → 92 → 93 → 96 | ajustou | 7,0 | sem medição (Antigravity) |
| Lida | 60,2 → 59,8 → 71,6 → 70 → 68 | virou | 7,8 | ~US$ 0,1 no total (painel) |

Sala (Antigravity fora): 74 → 78,3 → 82,6 → 80,2 → 82,8. Revisor: 60 na v2, 78 na v4. Diferença sala − revisor: +20,2 na
v2, +4,8 na v4 — abaixo do gatilho de 10, sem contraprova.

## O que Anderson decidiu

Só o gate. A proposta vai à entrevista do PLN-019, rodadas 2 a 5 (17 perguntas), em texto; nada está decidido.

## Os desvios do fluxo

- **A coordenação narrou uma hora de cabeça** ("21:40" para a chegada 4/6 da R2; o relógio dava 21:39): o X11 de novo,
  corrigido no chat.
- **A coordenação narrou um M13 errado** (73% de acerto do `layer`) antes de ver que o papel no texto vazava a resposta;
  corrigiu para 39% / 22% no turno seguinte.
- **A v2 contradizia as próprias regras** (a cópia na fase 3, o `layer` no catálogo contra o P6, o M17 sobre resumo);
  o revisor deu 60 e a v4 reescreveu. A ressalva de três personas sumiu sem registro na v2.
- **O Grok gravou memória de runtime** contra o briefing, de novo (abaixo).
- **O `rodada-1.md` citou a tarefa de Balança**, e Fagulha a citou na R1; não prova leitura do worklog dela.

## A proposta final (v5, copiada de `.sessions/reuniao-tev1/proposta-v5.md`)


> Rascunho da coordenação, montado com as rodadas 1 a 4 das seis personas (Balança, Ferrolho, Bitola, Fagulha, Faro,
> Lida), as medições da coordenação, o levantamento do `collector` e o revisor independente (60 na v2, 78 na v4).
> **Nada aqui está decidido**; as decisões são de Anderson. Marcas de evidência: **[medido]** rodou hoje, com a saída;
> **[lido]** código ou doc; **[inferido]** ninguém testou. Marcas de origem: **R1–R4**, a rodada; **coord.**, a
> coordenação; **revisor**, o revisor independente.

### O requisito

O pedido: "classificar, com fatos medidos, os melhores usos do `tev1`" nas seis frentes — CLI, Studio, MCP,
meeting-runner, plan-runner, migration-runner —, em brainstorm, e sair com um plano neste workstream, com Terreno medido,
opções, esboços de desenho, as evoluções e as perguntas da entrevista.

**Entrega:** a classificação medida dos usos, o desenho do cliente e da gravação, as fases com prazo estimado, as
evoluções e quatro rodadas de entrevista. **Não entrega:** nenhum uso ligado. Nenhuma pergunta tem hoje corpus e acerto
que a régua aceite (R2: 6 de 6); o plano começa por **parar de perder** o texto que já passa pelo `tev1` e pela auditoria
(revisor, achado 1).

### O que se mediu

| # | Fato | Marca |
| :- | :--- | :---- |
| M1 | Latência quente, sem concorrência, texto sintético curto: ~96 ms (50 palavras) a ~745 ms (1.400); 3 perguntas numa chamada custam ~65–90 ms a mais que 1 — `tev1_bench.out`; carga a frio 1,16 s, na primeira chamada do `tev1_probe.py` às 21:16 (saída no chat da coordenação, sem arquivo); 5.000 caracteres de texto real, quente: 772–780 ms (revisor) | [medido] coord. |
| M2 | Fila única: 8 chamadas levam ~1,85 s com 1, 4 ou 8 em paralelo; a espera por chamada vai de ~231 ms a ~1.039 ms | [medido] coord. |
| M3 | Acima de 2.048 tokens: HTTP 400 "input is never truncated". **Com texto real de worklog, o teto é ~5.000 caracteres** (6.000 → 2.153 tokens, 400); o sintético engana (1.800 repetições passam) — `teto.out`; o revisor achou o mesmo (6.000 → 2.169) | [medido] coord., revisor |
| M4 | A `confidence` é 1 − a entropia das probabilidades: mede a margem, não o acerto (p = 0,72 → 0,15) | [inferido] coord., da conta nas saídas |
| M5 | Voto de célula: o regex devolve `None` em 4 de 98 células reais; o `tev1` lê "ressalva" em 22 de 37 "apoio" — com a coluna da justificativa no texto, limite apontado por Balança — `voto_cells.out` | [medido] coord. |
| M6 | O resolver do MCP rodou 7 vezes desde 2026-11-03, 6 pelo Haiku e 1 fallback, 3,7–7,0 s (média 13,5 s com a queda de 61 s); nunca pelo `tev1` (sem `resolver.tev1_min_confidence`); espera até 20 s pelo Ollama (`resolver.py:38`) | [medido] levantamento, conferido; [lido] revisor |
| M7 | Auditoria de fatos: 1.564 `fact_check` em 52 auditorias, holds 909, unknown 638, fails 17; 510 fatos `rodado` | [medido] levantamento, conferido |
| M8 | A auditoria apaga o parágrafo de cada fato no fim (`fact_audit.py:428-430`); a pasta está vazia: não há (fato, evidência, veredito). **Cada auditoria apaga mais um**: 52 em 9,4 dias | [lido] coord.; [medido] Balança, revisor |
| M9 | O Studio já tipa falha e cota; o regex do diálogo de startup quebrou com o Codex 0.157 (`startup-dialog-blocked-signals.ts:4`); volume não medido | [lido] levantamento, conferido |
| M10 | Uso das skills: plan-runner 39 pela ferramenta mais 5 digitados, close-task 18, meeting-runner 1, migration-runner 0 | [medido] levantamento, revisor |
| M11 | Gatilho voto × fato novo, 23 pares de 2 reuniões, rótulo à mão, `state` **resumido à mão** por Balança: 3 de 6 "sim" e 15 de 17 "não"; os 3 perdidos são de taxa-base (0 PRs), `confidence` 0,013–0,115; limiar 0,15 → 0 FN, decide 10 de 23 — `material/balanca/` | [medido] Balança, conferido |
| M12 | A pergunta `evento` sai "sim" em 23 de 23 pares — `evento.out` | [medido] coord. |
| M13 | A pergunta `layer` do resolver, nas 252 descrições reais de subagente, contra o modelo que a sessão escolheu: 39% sem o papel no texto, 22% no `general-purpose` (13 de 60); "alta" em 216 de 252 (86%), contra 69 no rótulo. Limite: 3–5 palavras; o resolver recebe o `task` inteiro — `layer2.out` | [medido] coord. |
| M14 | Inverter a ordem das opções: o `layer` segue em "alta" (229 de 252); o `evento` com "não" primeiro acerta 7 de 17 "não" (era 0) — `ordem.out` | [medido] coord. |
| M15 | O corte de tarefa do `close-task` não tem corpus: 49 turnos com `prompt_head`, 29 marcos `task` | [medido] coord., revisor |
| M16 | A auditoria inteira custou US$ 7,16 em 10 dias corridos (~US$ 0,72/dia) e 2,0 h em segundo plano: o teto do pré-filtro em dinheiro é pequeno | [medido] coord. |
| M17 | O `tev1` como ordenador do gatilho, nos mesmos 23 `state` resumidos: os 6 "sim" nas posições 1, 2, 3, 11, 15 e 16 (AUC 0,74); ler os 10 primeiros pega 3 de 6 — `ranking.out`. Mesma amostra do M11, texto que não é o do pedido real | [medido] coord. |
| M18 | O resolver já manda o `task` inteiro ao `tev1` (`resolver.py:92`, `policy.py:251`) e descarta o texto | [lido] Balança, R3 |
| M19 | Sonda de Fagulha, n = 4: a escolha saiu igual nos 4, a confiança separou (0,84 e 0,86 contra 0,012 e ~0) | [medido] Fagulha, R3 — n mínimo |
| M20 | Dos 494 fatos pendentes de desfecho, 467 são `inferido`, que não vão à auditoria (`fact_audit.py:68`) | [medido] revisor, `fact_outcome.py --pending` |

### O voto da sala

R3: 48 votos, **nenhum contra** — 23 apoio, 25 apoio com ressalva (`tally.py 3`; as 48 células conferidas pelo revisor).
R4, a confiança no plano inteiro da v2: 80,2 (5/6), mediana 82, faixa 70–88; Faro (Antigravity) 93, à parte.

| Proposta | Balança | Ferrolho | Bitola | Fagulha | Faro | Lida |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| P1 cliente | ressalva | ressalva | ressalva | apoio | apoio | ressalva |
| P2 sombra e log | apoio | ressalva | apoio | apoio | apoio | ressalva |
| P3 corpus | apoio | ressalva | apoio | apoio | apoio | apoio |
| P4 quatro perguntas | ressalva | ressalva | ressalva | ressalva | ressalva | ressalva |
| P5 régua | ressalva | ressalva | apoio | apoio | ressalva | apoio |
| P6 portão | ressalva | ressalva | apoio | ressalva | apoio | ressalva |
| P7 fora | apoio | apoio | apoio | apoio | apoio | apoio |
| P8 evoluções | ressalva | ressalva | ressalva | ressalva | apoio | ressalva |

### A classificação dos usos, pelo que se mediu

| # | Uso | Frente | O fato que decide | Hoje | O que o destrava |
| :- | :-- | :----- | :---------------- | :--- | :--------------- |
| 1 | **Parar de perder o texto** — o parágrafo da auditoria e o `task` do resolver, gravados antes de qualquer cliente | hook, MCP | M8: cada auditoria apaga um; M18: o resolver joga o `task` fora | **fase 0** | a política de texto (Rodada A) |
| 2 | Gatilho voto × M# — como **ordem visível**, lista inteira | meeting-runner | M17: o topo acerta, a taxa-base fica na cauda; M11/M17 sobre `state` resumido | depois do replay cego (fase 2b) | o replay com o `state` que o `tally` monta |
| 3 | Gatilho voto × M# — como **decisão** (rodada extra da R8) | meeting-runner | M11: perde 3 de 6 "sim"; M12: a segunda pergunta não ajuda | sombra | n_sim ≥ 30 (~10 reuniões) e um critério que pegue a taxa-base |
| 4 | `layer` do resolver | MCP | M13: 86% "alta", 22% no caso real — **reprova o P6 hoje**; 7 resoluções desde 2026-11-03 | fora do catálogo; o probe vai à fase 3 | ≥ 20 `task` inteiros gravados pela fase 0 e rotulados |
| 5 | Pré-filtro dos fatos `rodado` | hook | M16: teto ~US$ 0,72/dia; M3: parágrafo + saída do comando passam de ~5.000 caracteres, e o cliente não trunca | sombra só no que cabe | o corpus da fase 0 **com o `run` citado** (R4.5) e a medida de quantos cabem |
| 6 | Reserva do voto `None` | meeting-runner | M5: 4 de 98 células | sombra barata, só a célula | — baixo valor; serve de régua |
| 7 | Diálogo de startup do Studio, no miss do regex | Studio | M9: quebra por versão, volume não medido | evolução | contar os misses |
| 8 | "É plano?" do plan-runner; "mudou o assunto?" do close-task | plan-runner, close-task | M15: sem corpus; M10: 44 e 18 usos | evolução | corpus de pedidos e turnos |
| 9 | Sugestor dos 494 fatos pendentes | hook | M20: 467 são `inferido`, sem saída gravada: o `tev1` julgaria só a frase | fora | — |
| 10 | Operação do migration-runner | migration-runner | M10: 0 usos | fora | uso real |
| — | Título do terminal, cota, conta, gate do dispatch; persona, síntese, revisor | Studio, MCP | latência de ms; regra numérica; o modelo só escolhe opção | fora (P7, 6/6) | — |

### O desenho

**A gravação, um escritor só (revisor, achados 1 e 4).** Tudo o que é texto vai a `.measurements/classify/`, fora do
git, por **um** módulo de gravação que todos usam — o hook, o resolver e, depois, o cliente —, com a retenção dele.
**A casa dele** (revisor v4, achado A; R5, Bitola): o `fact_audit.py` é norma comum (`.brza/core.lock:13`), editada no
`core/` do `brza-workflow` e trazida pelo `brza sync`; o resolver mora em `packages/mcp`. A recomendação é o módulo no
`core/`, ao lado do `measure.py`, e o resolver o carrega pelo `BRZA_WORKSPACE` (R2.6).
Nada de texto no `measurements.jsonl`, que é permanente e já tem cópias `.bak`; lá só o evento `classify` com metadados
(`question`, `choice`, `probabilities`, `confidence`, `path`, `reason`, `ms`, `state_sha`, `consumer`).

```text
.measurements/classify/
  fato_rodado.jsonl   # {fato, paragrafo, run_citado, veredito_haiku, kind, at} ← fact_audit.py, no finally, antes do os.remove
  layer.jsonl         # {task, tev1_choice, tev1_confidence, haiku_choice} ← resolver, no POST que já existe (M18)
  state/<sha>.txt     # o state de cada chamada do cliente (fase 1 em diante)
```

- **A retenção** é a da Rodada A, aplicada pelo módulo de gravação ao gravar, sem job (R3, Lida): a sala pede guardar o
  texto da pergunta até ela passar ou falhar na régua (R4: Balança, Fagulha, Faro). A política vem **antes** da fase 0
  (R4: Ferrolho, Lida). O veredito do Haiku é rótulo **provisório**, não a verdade (R4, Ferrolho).
- **A cópia não muda o veredito nem o tempo da auditoria** (R3, Lida): um append no `finally` (R3, Balança).
- **O `run` citado** (revisor v4, achado B): sem a saída do comando que o fato cita, o pré-filtro não tem contra o que
  julgar; gravá-la põe saída de comando em disco, sob a política da R2.2 (R4.5).

**O cliente (P1, R2 6/6, D1c).** O POST sai do `_tev1` (`resolver.py:115-126`) para um módulo; o resolver vira
chamador; o verbo é casca.

```python
# brza_mcp/classify.py — folha: só urllib e a leitura da configuração (R3, Bitola)
Classifier.ask(state: str, questions: dict[str, str | Question], timeout_ms: int) -> dict[str, Answer]
# Answer = {choice: str | None, confidence, probabilities, path: "tev1" | "unknown",
#           reason: "ok" | "too_long" | "no_ollama" | "timeout" | "bad_choice", ms, model}
```

```bash
brza classify --json < pedido.json      # {"state": "...", "questions": {"gatilho": "gatilho"}, "timeout_ms": 2500}
```

- **Prazo por chamada (revisor, achado 5; R3, Ferrolho e Lida):** `timeout_ms` obrigatório; estourou, `reason:
  timeout`. Sem daemon (R3, Lida), nada impede dois processos de chamarem juntos; a fila é do Ollama (M2), e o prazo é o
  que impede o chamador de esperar por ela. No resolver, o prazo cai dos 20 s de hoje (M6) para o que a R2.5 fixar: a chamada fria soma ~1,16 s de carga aos
  ~780 ms de 5.000 caracteres, ~1,9 s, e 1,5 s estouraria quase toda a sombra esporádica (revisor v4, achado E); a
  recomendação é 2.500 ms com `keep_alive` de 5 min.
- **Teto:** o limite real é o HTTP 400 do Ollama, que vira `too_long`; os ~5.000 caracteres são só a pré-checagem
  medida num texto real, não garantia (R5, Ferrolho) — nunca truncamento (M3; R3, Ferrolho). Sem Ollama: `unknown`, sem retentativa. A
  cadeia `unknown → Haiku` é do consumidor, pelo `on_doubt` da pergunta (C10).
- **Se a folha puxar a política inteira**, ou o verbo no hook passar de ~200 ms, o módulo vai a `packages/client` (R3,
  Bitola).

**O catálogo de perguntas (P4, P6; ideia de Bitola, R1).** Um JSON versionado; uso novo é id novo. **Só entra o que
passou o portão P6** (revisor, achado 2) — hoje, nenhuma:

| Pergunta | Probe P6 | Estado |
| :------- | :------- | :----- |
| `gatilho` | n = 23, maior opção 78% (18/23), ordem invertida não medida | falta o probe de ordem, no `state` real do `tally` |
| `layer` | n = 252, "alta" em 86% contra 27% no rótulo (M13) | **reprovado**; o probe no `task` inteiro vai à fase 3, quando houver ≥ 20 (revisor v4, achado C) |
| `voto` | sem probe (o M5 tinha a coluna da justificativa) | probe só com a célula |
| `fato_rodado` | sem probe | probe no corpus da fase 0, só no que cabe (M3) |

- **O portão (P6):** probe em ≥ 20 pares rotulados, com o texto real do pedido (R3, Balança); nenhuma opção acima de
  80% das respostas quando o rótulo não é assim, e menos de 10% de respostas trocadas ao inverter a ordem (M12–M14). Os
  cortes são provisórios até o primeiro probe (R3: Bitola, Fagulha, Ferrolho); com classe cara abaixo de 20%, o corte de
  80% briga com a régua e se revê (R3, Bitola). **O custo de um probe é rotular à mão ≥ 20 pares** — a máquina leva
  menos de 1 min (revisor v4, achado D; a ressalva de Lida na R3); no `gatilho`, os pares que o `tally` monta pedem
  rótulo novo.
- **A régua para ligar (P5):** a classe cara com n ≥ 30, FN 0 nela num conjunto fora da amostra do limiar — que guarda
  a classe que já errou, não um sorteio que a esvazie (R3, Balança) —, FP declarado; uma amostra das concordâncias
  também se revisa (R3, Ferrolho); o rótulo vem do desfecho que já existe — veredito do Haiku, voto final,
  `fact_outcome` —, à mão só na divergência (R3, Lida). O limiar mora num arquivo de medição; sem ele, o cliente só
  grava. **Dissenso registrado:** Faro quer o limiar por conformal risk control, α ≤ 5%, n ≥ 50 (R2, R3, R4) — opção da
  Rodada B.

**A ordem visível (R3: Bitola, Ferrolho, Lida; M17).** O `tally.py` grava os pares voto × M# com `choice` e
`confidence` num arquivo **próprio**, `sugestao-rN.json` — o `estado-rN.json` tem dois escritores e nenhum contrato
(R4, Bitola). O painel só os mostra depois do **replay cego** de Ferrolho (fase 2b): o `state` montado pelo `tally`, não o
resumo à mão (revisor, achado 3), nas reuniões já rotuladas, comparando a leitura na ordem original com a ordenada. **Passa** se os 3 "sim" de
taxa-base do M11 caírem na metade de cima da lista (posição ≤ 12 de 23) com o `state` real (R5, Balança); se não, a
ordem não vai ao painel. Se for ao painel: **sempre a lista inteira**, com a marca "não calibrado, n_sim = N" (R4, Balança). A ordem **ancora** quem
lê (R4, Ferrolho); o erro dela não custa "só a ordem". A ideia de Lida de ordenar a auditoria não tem onde entrar: o hook
manda todos os fatos de uma vez num só `claude -p` (`fact_audit.py:244-251`), e o `inferido` nem vai à auditoria (revisor).

### As fases

| Fase | Entrega | Pronto quando | Estimado |
| :--- | :------ | :------------ | :------- |
| 0. Parar de perder | o módulo de gravação no `core/` com a retenção; a cópia do parágrafo e do `run` citado no `finally` do `fact_audit.py`; o `task` e as duas escolhas no POST do resolver; o `brza sync` | a próxima auditoria e o próximo dispatch sem linha na tabela deixam o texto em `.measurements/classify/` | ~3 h [inferido] |
| 1. Cliente | `Classifier.ask` com `timeout_ms` + `brza classify`, o resolver como chamador, testes com o Ollama injetado | os testes do resolver passam sem mudar a rota; `too_long`, `no_ollama`, `timeout` e `bad_choice` têm teste | ~3 h [inferido] |
| 2. Probes e sombra | o comando de probe P6; a rotulagem à mão de ≥ 20 pares do `gatilho` (do `tally`), do `voto` e do `fato_rodado`; os três probes; só as aprovadas entram no catálogo e gravam o evento `classify`; `sugestao-rN.json` sem ir ao painel | cada uma das três com o probe gravado e o estado no catálogo | ~5 h [inferido] |
| 2b. A ordem no painel | o replay cego; se passar, a coluna no painel com a lista inteira e a marca | o replay mostra que a leitura ordenada não perde a cauda | ~1 h [inferido] |
| 3. Corpus | esperar o n da classe cara; o probe do `layer` quando houver ≥ 20 `task` | n ≥ 30 numa pergunta: `fails` do `rodado` ~7 semanas (6 em 9,4 dias); "sim" do `gatilho` ~10 reuniões; o `layer` no ritmo do resolver (7 desde 2026-11-03) | espera, sem horas [medido o ritmo, revisor] |
| 4. Calibração | a tabela limiar × cobertura × FN × FP por pergunta, fora da amostra | uma pergunta passa a régua — ou a tabela mostra que o 4B não serve | ~2 h [inferido] |
| 5. O primeiro uso | liga a pergunta que passou, com o `on_doubt` dela | entrevista com Anderson sobre a tabela | a medir |

### As evoluções (para onde o plano vai)

- **O `layer` com o `task` inteiro**, se passar o P6 — o M13 sugere que não passa (R3, Bitola); **o alarme do gatilho**;
  **o pré-filtro da auditoria**, medido em quantos fatos cabem e em atenção, não em dinheiro (M3, M16).
- **O diálogo de startup do Studio**, no miss do regex, depois de contar os misses (P7: 6/6 na R3; Faro, que pedia já na
  R2, passou a apoiar o "depois" na R3).
- **O "é plano?" e o "mudou o assunto?"**, quando houver corpus (M15).
- **O retreino `tev1-brza`** com o corpus da fase 0 (D5: 5 de 6 como evolução; Lida contra).
- **Um segundo modelo local** só onde o 4B falhar medido; **a ferramenta MCP `classify`** com a mesma assinatura.
- **Fora, com o porquê:** o sugestor dos 494 pendentes (M20) e a fila ordenada da auditoria (não há fila).

### A confiança do plano

| Quem | Número | Base |
| :--- | -----: | :--- |
| **Revisor independente** | **78** (v4; era 60 na v2) | **a confiança do plano** (R2.3) |
| Sala, R5 — o plano inteiro da v4 (média, mediana, n, faixa) | 82,8; 86; 5/6; 68–90 | `tally.py 5`, Antigravity fora |
| Antigravity (à parte) | 96 | relatado, não somado |
| Diferença sala − revisor | +4,8 na v4 (+20,2 na v2) | abaixo do gatilho de 10: sem contraprova; a decisão (gravar em sombra) é barata de reverter |
| Sala nas rodadas (R1 → R2 → R3 → R4 → R5) | 74 → 78,3 → 82,6 → 80,2 → 82,8 | `tally.py` |

A v5 aplica os achados A a F do revisor sobre a v4 e os três pontos da R5; nenhum deles mudou um voto.

### Para Anderson decidir

As quatro rodadas — R2 a R5, 17 perguntas — estão no arquivo de entrevista do PLN-019, revistas com o revisor e a R5.

## Os custos

- **Coordenação:** US$ 10,29 em 21 turnos até 22:01; **collector:** US$ 1,42; **revisor:** US$ 2,86 (duas revisões) —
  `measurements.jsonl`, `session_id` desta sessão: US$ 14,57.
- **Personas:** Lida ~US$ 0,1 (Claude); Ferrolho 0,45 M tokens até a R4 (Codex); Grok e Antigravity sem medição.
- **`tev1`:** local, sem custo; ~1.500 chamadas de medição da coordenação e de Balança.

## Fora do workspace

- **Memória de runtime do Grok** (`runtime_memory_check.py 21:20`): 42 arquivos em `~/.grok/memory-v2/` mudaram
  depois das 21:20, fora as observações de `_inbox`; os desta reunião: `reuniao-tev1-bitola.md`, `reuniao-tev1-fagulha.md`, `tev1-classifier.md`. A lista inclui
  arquivos de outras sessões Grok do workspace (o PLN-018), que o script não separa.
- **As seis personas** foram encerradas e aceitas pelo host às 22:01 (`succeeded/settled`, liberação automática ~22:03),
  no Run `run_e11c2e02316f`.
- **O Ollama** carregou o `tev1:4b` (até 7,9 GB) durante a reunião; nada foi exposto fora do 127.0.0.1.
- **Link** `/private/tmp/reuniao-tev1` → `.sessions/reuniao-tev1`, para os subagentes.

## Custo da tarefa

Corrido 7 min — agente 5 min, quem pediu 3 min, pausa 0 s · US$ 2,48 (turnos 1,87, subagentes 0,61) · CPU 8,62 s do `claude` e 65,70 s dos comandos, RSS até 425 MB · 22 turnos, 1 sessão · dividida com 6 outros worklogs do commit · até 22:02 de 2026-11-09, pelo `brza note commit`
