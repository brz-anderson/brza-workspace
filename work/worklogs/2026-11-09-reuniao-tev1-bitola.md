---
scope:
  - workspace
  - brza-workflow
  - brza-studio
tags:
  - tooling
sessions:
  - f497c2b6-20bf-4786-8d30-73c4cec86d58
---

# Reunião tev1 nos fluxos: a participação de Bitola, arquiteta de integração

O pedido de Anderson, em 2026-11-09, na sessão da coordenação (meeting-runner, chat do BrzA Studio): "classificar, com fatos medidos, os melhores usos do `tev1:4b` local nas seis frentes — CLI, Studio, MCP, meeting-runner, plan-runner, migration-runner —, em estilo brainstorm; saída: proposta de plano e o plano criado neste workstream, mapeando para onde ele pode evoluir". Este é o
registro de **Bitola** — persona arquiteta de integração, no Grok `grok-4.6` `high` —, aberto pela coordenação. A pauta e as
regras estão no briefing da reunião; cada rodada é uma seção abaixo, acrescentada no fim do arquivo.

## O que se fez

### Rodada 1: opinião inicial — 21:22

- **Posição:** Cliente único no MCP; tally e layer primeiro; Studio e CLI só envelopam.

#### 1. O ranking dos usos

- **Posição:** `classify_vote` quando `None`; ligar o `layer` do Resolver; gatilho voto×M# na meeting-runner.
- **Por quê:** Valor por risco, não volume. (1) Frente meeting-runner, `tally.py:226` `classify_vote`: célula vira `None` no texto livre; pergunta `voto` com `apoio` / `ressalva` / `contra`; *lido* a função e *medido* no levantamento 94 linhas tabulares + 54 `**Posição:**` + 33 `plano_porque`. (2) Frente MCP, `resolver.py:89` `classify` + `policy.py:231` `decide_model` + `tools.py:254` `dispatch`: pergunta `layer` com `alta`/`media`/`rapida`; *lido* a cadeia; *medido* 7 `route.resolver`, 0 pelo `tev1`, 6 Haiku, 1 fallback, confianças 0,57–0,96. (3) Frente meeting-runner, script do gatilho (issue): pergunta `gatilho` `sim`/`nao` no par voto×M#; *lido* `tev1_probe.py` e a issue; *medido* 4/4 sintéticos, `confidence` 0,15 e 0,42 nos dois `sim`. Plan-runner e migration-runner ficam de fora desta rodada: 0 scripts, classificação hoje é a sessão (*lido* SKILL.md). Studio de título/journal já é tipado (*lido* levantamento §2).
- **Ideias:** `Classifier.ask(state, questions)` em `brza_mcp/classify.py`, `tally.py` importa o módulo e não faz POST `(ousadia: baixa)`; o `Resolver.classify` vira wrapper da pergunta `layer` + Haiku `(ousadia: baixa)`.
- **Risco:** ranquear o que já existe (layer) acima do custo da auditoria (US$ 7,16 / 1564 `fact_check`, *medido*) e deixar o pré-filtro do `fact_audit.py:309` para a evolução.
- **Confiança:** 78/100

#### 2. A régua de entrada

- **Posição:** Fixture rotulada, n≥30, FN do erro caro, limiar na tabela; dúvida → Haiku → coordenação; sem limiar não entra.
- **Por quê:** *Lido* R2.2 em `resolver.py:9` e `policy.py:49`: sem `resolver.tev1_min_confidence` tudo vai ao Haiku de propósito. *Medido* no probe: acerto 4/4 não calibra, e o `sim` verdadeiro é a menor `confidence`. *Suposto:* o erro caro do gatilho é falso negativo (perder o X10); o erro caro do voto é inventar `apoio`/`contra` (falso positivo). Régua por uso, gravada na fixture: acerto, FN, FP, n, limiar. Abaixo do limiar ou `choice` fora do enum → `path: haiku` se o uso paga Haiku (layer, gatilho); voto livre abaixo do limiar fica `None` com aviso, sem Haiku (*suposto:* célula de voto não vale US$ 0,01). n mínimo 30 pares rotulados à mão; abaixo disso o uso não liga, só loga.
- **Ideias:** cada pergunta nomeada (`layer`, `voto`, `gatilho`) traz `min_confidence` e `on_doubt` no contrato `(ousadia: média)`; fixture JSON no estilo `tests/mcp/test_mcp_resolver.py` (já injeta `ollama`/`claude`, *lido*) `(ousadia: baixa)`.
- **Risco:** um limiar único para três perguntas; o probe já mostra que 0,5 passaria os `nao` e derrubaria os `sim`.
- **Confiança:** 84/100

#### 3. Onde mora o cliente

- **Posição:** `brza_mcp.classify.Classifier`; `brza classify` e o Studio só chamam; um POST, injetável.
- **Por quê:** O único POST a `/v1/systemone` hoje está em `resolver.py:115-126` `_tev1`, com `ollama(url, body, timeout)` injetável, timeout 20 s, sem proxy, erro → `None` (*lido*). `classify` hoje amarra `state` a uma pergunta `layer` e à cadeia Haiku (*lido* :89-109). Dois chamadores bastam no primeiro passo (Resolver e `tally.py`); seis cópias do urllib é o que muda quando o endpoint mudar. Sem pacote novo `packages/classify`. *Suposto:* skills do workspace importam o pacote MCP como o `brza-mcp` já faz.
- **Contrato (esboço):**

```python
# Classifier.ask(state: str, questions: dict[str, Question], fallback="none"|"haiku") -> dict
# Question = {instructions, criteria: {opção: desc}, min_confidence?: float, on_doubt?: "haiku"|"none"|"human"}
# Answer   = {choice, confidence, probabilities, path: tev1|haiku|fallback, reason, ms, tev1_confidence}
```

```text
brza classify --json < pedido.json
# pedido: {state, questions, fallback?}
# stdout: {answers: {id: Answer}, truncated?: bool, reason?}
```

- Sem Ollama / HTTP 400 / timeout: `path=fallback`, `choice=None`, não levanta (*lido* o `except` de `_tev1`). Fila cheia: o cliente serializa; *medido* 8 em paralelo = ~1,85 s, espera por chamada de 231 ms → 1.039 ms. Acima de 2.048 tokens: recusar no cliente com `reason=prompt_too_long` *antes* do POST (*medido* HTTP 400, "input is never truncated"). Cache: a repetição já volta em 2–6 ms (*medido*); não segundo cache.
- **Ideias:** `Resolver._tev1` passa a `Classifier.ask` com uma pergunta `(ousadia: baixa)`; ferramenta MCP `classify` depois, mesma assinatura JSON `(ousadia: média)`.
- **Risco:** `tally.py` no workspace importar `brza_mcp` puxa o pacote MCP para a skill; alternativa é o verbo CLI, um processo a mais (~latência do spawn, *suposto*).
- **Confiança:** 88/100

#### 4. Além do óbvio

- **Posição:** Várias perguntas por `state`; log de decisão; não copiar HTTP; não persona; não hot-path do Studio.
- **Por quê:** *Medido:* 3 perguntas numa chamada somam ~60–90 ms; 4 opções vs 2 somam ~20 ms. O docstring de `resolver.py:14-16` já descreve `questions` no plural; o código manda só `layer` (*lido*). Alternativa E (log rotulado) é o que alimenta a régua e um retreino futuro. *Não fazer:* persona, síntese, revisor (issue, *lido*); POST em `tally.py` / hook / Electron; classificar título OSC do terminal (*lido* `agent-title-status.ts:229`, latência de UI vs ~96 ms *medido*); paralelo; mandar 2.048+ tokens; ligar `tev1_min_confidence` sem tabela. Retreino e segundo modelo local ficam abertos, depois do log, *suposto* custo de coleta >> custo do 4b.
- **Ideias:** registro append-only `.measurements` `event=classify` com `{question, choice, confidence, path, expected?}` `(ousadia: média)`; catálogo de perguntas nomeadas num JSON, uso novo = id novo, cliente igual `(ousadia: alta)`.
- **Risco:** o catálogo vira abstração para seis frentes quando duas bastam (vício da persona). Mitigação: só `layer`, `voto`, `gatilho` no plano; o resto entra por id depois de n≥30.
- **Confiança:** 80/100

#### 5. O plano e para onde evolui

- **Posição:** Calibrar → extrair Classifier → voto `None` → limiar do layer → gatilho; CLI/MCP/log/auditoria abertos.
- **Por quê:** *Lido* a issue: "calibrar antes de qualquer código". *Lido* o vício da persona: arquitetura antes do primeiro uso medido — por isso a extração só cabe se o primeiro uso (voto `None`) entra na mesma fase. Alternativas: A é o recorte certo de produto e pequeno demais de cliente (dois POSTs nasceriam); B é o destino, cedo demais se nascer pacote novo; C (triagem da auditoria) tem o custo *medido* mas o `tev1` não abre arquivo (*lido* `fact_audit.py:309` `claude -p --tools Read,Grep,Glob,WebFetch`); D (Studio) compete com estado já tipado; E é pré-requisito da régua, não um produto.
- **Fases:** 0 calibrar pares voto×M# e voto livre (tabela FN/FP, n, limiar) · 1 `Classifier.ask` extraído, `Resolver` wrapper, fixture, sem uso novo · 2 `classify_vote` chama o módulo quando `None` · 3 ligar `resolver.tev1_min_confidence` com o limiar da tabela do `layer` · 4 script do gatilho com `on_doubt=haiku`. Pronto de cada fase: fixture verde + linha `classify` no jsonl + FN da tabela abaixo do teto combinado.
- **Evoluções abertas:** `brza classify`; ferramenta MCP `classify`; pré-filtro `rodado` do `fact_audit`; diálogo de startup do Studio (`startup-dialog-blocked-signals.ts:34`, *lido* levantamento); retreino; segundo modelo; plan-runner "é plano?" sobre o resumo do pedido.
- **Ideias:** fase 1 e 2 no mesmo PR se a extração for ≤ o wrapper + um import em `tally.py` `(ousadia: média)`; se passar de dois arquivos de produção, parte `(ousadia: baixa)`.
- **Risco:** fase 1 virar pacote e a calibração (fase 0) ficar atrás — aí o vício ganha.
- **Confiança:** 76/100

#### A ideia mais ousada desta rodada

Catálogo de perguntas nomeadas (`layer`, `voto`, `gatilho`, depois `fato_holds`) num JSON de contrato: cada uso novo é um id, um `min_confidence` e um `on_doubt`, nunca um cliente novo. Várias perguntas no mesmo `state` (custo *medido* 60–90 ms). Risco: virar framework para seis frentes; o plano só lista três ids até n≥30 de cada.

#### Issues candidatas

- **Extrair `Classifier.ask` de `Resolver._tev1`** — um POST, injetável, recusa >2048 no cliente — prioridade `high`
- **`classify_vote` via o módulo quando a célula é `None`** — primeiro uso medido, estado cabe em 2048 — prioridade `high`
- **Evento `classify` no jsonl de medições** — sem log não há régua nem retreino — prioridade `medium`
- **Ligar `resolver.tev1_min_confidence` depois da tabela do `layer`** — o caminho já existe e hoje é 0/7 — prioridade `medium`

#### Placar da rodada 1

| Assunto | Posição em uma linha | Confiança |
| :------ | :------------------- | :-------- |
| 1. O ranking dos usos | voto `None`, layer do Resolver, gatilho voto×M# | 78 |
| 2. A régua de entrada | n≥30, FN do erro caro, limiar por pergunta, sem limiar não entra | 84 |
| 3. Onde mora o cliente | `brza_mcp.classify`; CLI e Studio envelopam; um POST | 88 |
| 4. Além do óbvio | várias perguntas + log; sem HTTP copiado, sem persona, sem hot-path | 80 |
| 5. O plano e para onde evolui | calibrar → extrair → voto → layer → gatilho; CLI/MCP/auditoria abertos | 76 |

<!-- fim-rodada-1 -->

### Rodada 2: debate — 21:36

- **Posição:** Sombra no Classifier; voto None cai (M5); envelope é módulo+verbo fino.

#### As disputas

- **D1 · o envelope do cliente:** (c) — o POST fica em `brza_mcp.classify` (hoje `_tev1`, *lido* `resolver.py:115`); `brza classify` é stdin JSON do mesmo módulo, para hook/skill que não importa o pacote. (a) sozinho acopla `tally.py` ao MCP por 4 células (M5). (b) sozinho vira segundo urllib, ou o Studio fala com o Ollama. 86/100
- **D2 · o primeiro uso depois da sombra:** (e) — M5: `None` em 4/98 e o tev1 leu "ressalva" em 22/37 "apoio". M8 bloqueia a auditoria. M11: 3/6 sim perdidos; limiar 0,15 decide 10/23. M6: 7 linhas, 0 tev1. Sem tabela, o cliente só loga. 90/100
- **D3 · a régua:** (a) — n da classe cara ≥ 30 e FN 0 nela (M11: 18/23 esconde 3/6 sim). Limiar por pergunta (C3). `on_doubt` não herda o Haiku do `layer`. 88/100
- **D4 · o diálogo de startup do Studio:** (b) — M9: a regex quebrou; volume não medido. Entra no catálogo como id depois de n; não é fase. 82/100
- **D5 · retreino:** (b) — M8 mata (c): `.measurements/fact-audit/` vazia. Sombra guarda `(state, questions, choice, expected)` antes de qualquer LoRA. 92/100

#### Os ataques

- **Faro, D2(d) e D5(c):** LoRA e pré-filtro sobre 1.564 pares. M8: o parágrafo some no fim da auditoria; não há (fato, evidência, veredito). O 60–80% FrugalGPT é *suposto* (síntese diverge). Derruba o ataque: sombra persistindo o parágrafo + n≥30 de `rodado` com evidência e tabela FN dos `fails` (17/1564, M7).
- **Lida, D2(c):** ligar `tev1_min_confidence` com os 7 `route.resolver`. M6: 0/7 pelo tev1, sem gold de `layer`. É R2.2 ao contrário. Derruba o ataque: 30 pares `task`→`layer` rotulados à mão, tabela própria, limiar ≠ o do gatilho.

#### A concessão

M5 (coordenação, `voto_cells.out`): 4/98 `None` e 22/37 "apoio" viram ressalva. Na R1 o voto `None` era o primeiro uso. Cai para sombra: o volume não paga o import, e o modelo ainda lê a coluna da justificativa.

#### "Sim, e…"

Ferrolho, contrato de desconhecido por consumidor: `on_doubt` por pergunta no `Classifier.ask` (`haiku`|`none`|`human`), para o voto não pagar Haiku e o `layer` pagar. O catálogo só aceita id novo depois de um probe de discriminação (M12: `evento` saiu "sim" em 23/23). `(ousadia: média)`

#### Placar da rodada 2

| Assunto | Posição agora | Confiança R1 | Confiança R2 | Mudou? (não, ajustou, virou) | Quem ou o que te moveu |
| :------ | :------------ | :----------- | :----------- | :--------------------------- | :--------------------- |
| 1. O ranking dos usos | só sombra até tabela por pergunta | 78 | 90 | virou | M5, M8, M11 |
| 2. A régua de entrada | n_caro≥30, FN 0, limiar por pergunta | 84 | 88 | ajustou | M11 |
| 3. Onde mora o cliente | módulo + verbo fino, um POST | 88 | 86 | ajustou | Fagulha D1(b) como envelope |
| 4. Além do óbvio | várias perguntas só se discriminarem | 80 | 84 | ajustou | M12 |
| 5. O plano e para onde evolui | Classifier que só loga; ligar depois da tabela | 76 | 82 | virou | M5, M8, M11 |

<!-- fim-rodada-2 -->

### Rodada 3: voto final — 21:41

- **Posição:** P1+P6: cliente folha e portão; sugestão no painel sem mudar rota.
- **Fatos lidos:** M13, M14, M15; limite do M5 (coluna da ressalva no state).

#### O voto em cada proposta

| Proposta | Voto (apoio, apoio com ressalva, contra) | Ressalva ou alternativa em uma linha | Confiança |
| :------- | :--------------------------------------- | :----------------------------------- | :-------- |
| P1 | apoio com ressalva | `classify.py` é folha (urllib+config), sem importar `queue`/`accounts`/`tools` | 90 |
| P2 | apoio | — | 88 |
| P3 | apoio | `estado-rN.json`: só append de candidatos; a coordenação continua dona do arquivo | 86 |
| P4 | apoio com ressalva | `layer` loga o `task` inteiro do dispatch (M13); `voto` loga só a célula (limite do M5) | 84 |
| P5 | apoio | — | 88 |
| P6 | apoio | cortes 80%/10% são ponto de partida, revisáveis no primeiro probe | 91 |
| P7 | apoio | — | 88 |
| P8 | apoio com ressalva | `layer` só destrava se passar P6 no `task` inteiro; M13 (22% em `general-purpose`) sugere que não passa | 82 |

#### O que me faria mudar de ideia

- **P6 (91):** um probe em que pergunta útil com FN 0 na classe cara falha o 80% porque a classe rara é <20% das respostas — aí o portão briga com P5, e eu afrouxo o (a).
- **P1 (90):** medir que a folha puxa `policy.config` inteiro (contas, fila) ou que o spawn do verbo no hook passa de ~200 ms — aí o módulo sai de `brza_mcp` para `packages/client`.

#### A última ideia

Sugestão visível, rota intacta: no fecho da rodada, `Classifier.ask` no par voto×M# grava `sugestao_gatilho` (`choice`, `confidence`) em `estado-rN.json`; o painel mostra a linha; a coordenação confirma ou ignora. Regex, placar e Haiku não mudam. FN = status quo; FP = uma linha a mais. Lugar: `tally.py` chama o módulo; `panel.py` lê o campo. Corpus nasce na reunião (P3+P4) sem esperar n≥30 para Anderson ver um X10. `(ousadia: média)`

#### Os colegas

| Persona | A contribuição mais útil dela, em uma linha | Nota de 0 a 10 |
| :------ | :------------------------------------------ | :------------- |
| Balança | A tabela M11 (3/6 sim, limiar que esvazia) e o limite do M5 | 10 |
| Ferrolho | `unknown` e `on_doubt` por consumidor, sem herdar o Haiku do `layer` | 9 |
| Fagulha | Sombra que guarda o parágrafo (M8) e o verbo como casca, não como POST | 8 |
| Lida | Recuo do limiar do `layer` (M6) e a regra de não calar o que para o worker | 7 |
| Faro | Cascata e calibração como literatura; LoRA e truncar 1.500 tokens saem com M8/M3 | 6 |

#### Autoavaliação

Fiel ao contrato: um POST, `Classifier.ask`, `on_doubt` por pergunta, portão de discriminação (C9, agora P6). O vício da R1 (arquitetura e voto `None` antes do volume) caiu com M5 — isso é a persona, não uma saída. A última ideia é produto no painel, fora do arquétipo, de propósito: a sala pediu valor cedo sem ligar rota.

<!-- fim-rodada-3 -->

### Rodada 4: a confiança final — 21:47

- **Posição:** Folha e portão entram; linha zero antes do módulo; ordem M17 no painel.
- **Fatos lidos:** M17, M18, M19.

| Parte do plano | Confiança na versão anterior | Confiança na versão atual | Uma linha de porquê |
| :------------- | :------------------------- | :------------------------ | :------------------ |
| O cliente (P1) | 90 | 92 | Folha e fallback `packages/client` na seção; um POST, `unknown` no consumidor |
| A sombra, o corpus e a linha zero (P2, P3) | 87 | 90 | M18: o POST que já existe grava o `task`; o texto é o corpus, não o hash |
| A sugestão visível e a ordem | — | 88 | M17: top-3 acerta, taxa-base na cauda, AUC 0,74; a lista inteira fica |
| A régua e o portão (P5, P6) | 90 | 91 | Cortes provisórios e o choque classe rara × P5 entram no catálogo |
| As evoluções (P8) | 82 | 84 | `layer` só com P6 no `task` inteiro (M13); ferramenta MCP `classify` mapeada |
| **O plano inteiro** | 86 | 88 | Ressalvas da R3 no desenho; a tabela de fases ainda lista 1 antes de 0 |

- **A sua mudança da rodada anterior entrou?** sim — O cliente (folha), O catálogo (P6), A sugestão visível. Em parte o dono do `estado-rN.json` (append exclusivo não está escrito).
- **O que ainda está errado:** a tabela de fases põe 1 (cliente) antes de 0 (linha zero); a prosa diz o contrário — a linha zero não espera o módulo (M18). Dois escritores no `estado-rN.json` (coordenação e `tally.py`) sem contrato de append.
- **A pergunta que Anderson precisa responder:** a linha zero no resolver começa esta semana, antes de extrair `classify.py`? Recomendação: sim — um POST que já existe, texto que hoje se perde (M18).
- **Autoavaliação:** Fiel ao contrato: folha, um POST, portão, catálogo por id. A confiança sobe porque o desenho copiou o esboço. A sugestão no painel continua produto, fora do arquétipo; M17 a mede, então deixo os 88.

<!-- fim-rodada-4 -->

### Rodada 5: a confiança na v4 — 21:57

- **Posição:** v4 corrige as fases e o portão; falta a casa do módulo de gravação.
- **Fatos lidos:** M3 revisto, M20, parecer do revisor (achados 1–5 e 8), `proposta-v4.md`.

| Parte do plano | Confiança na versão anterior | Confiança na versão atual | Uma linha de porquê |
| :------------- | :------------------------- | :------------------------ | :------------------ |
| **O plano inteiro** | 88 | 90 | Fase 0 primeiro, catálogo só com P6, um escritor de texto, `sugestao-rN.json`; a casa da gravação não está no contrato |

- **O revisor acertou ou errou onde?** Acertou 1, 2 e 4 (fases × corpus, `layer` 86% fora do P6, retenção com dois escritores); o 60 é da v2. No 3, eu sobrepeso o M17 na R4 — o `state` era resumo.
- **O que ainda está errado:** a casa do módulo de gravação (seção A gravação): o hook mora no workspace e o resolver no `brza-workflow`, sem path — dois escritores de novo. O `timeout_ms` (O cliente) declara a espera e não serializa entre processos (M2).

<!-- fim-rodada-5 -->

## Custo da tarefa

Corrido 7 min — agente 5 min, quem pediu 3 min, pausa 0 s · US$ 2,48 (turnos 1,87, subagentes 0,61) · CPU 8,62 s do `claude` e 65,70 s dos comandos, RSS até 425 MB · 22 turnos, 1 sessão · dividida com 6 outros worklogs do commit · até 22:02 de 2026-11-09, pelo `brza note commit`
