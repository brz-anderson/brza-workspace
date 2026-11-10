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

# Reunião tev1 nos fluxos: a participação de Fagulha, provocadora

O pedido de Anderson, em 2026-11-09, na sessão da coordenação (meeting-runner, chat do BrzA Studio): "classificar, com fatos medidos, os melhores usos do `tev1:4b` local nas seis frentes — CLI, Studio, MCP, meeting-runner, plan-runner, migration-runner —, em estilo brainstorm; saída: proposta de plano e o plano criado neste workstream, mapeando para onde ele pode evoluir". Este é o
registro de **Fagulha** — persona provocadora, no Grok `grok-4.7-build-fast` `low` —, aberto pela coordenação. A pauta e as
regras estão no briefing da reunião; cada rodada é uma seção abaixo, acrescentada no fim do arquivo.

## O que se fez

Às 21:21, três chamadas a `POST /v1/systemone` (`tev1:4b`, `keep_alive` 1m), uma pergunta cada:

```sh
python3 -I - << 'PY'
# voto livre, diálogo de startup e fato já decidido pela saída; ver a tabela abaixo
PY
```

| Caso | Esperado (à mão) | Escolha | `confidence` | ms |
| :-- | :-- | :-- | --: | --: |
| "prefiro o símbolo C desde 48 px; o B só se o núcleo clarear" | ressalva | ressalva | 0,36 | 206 |
| "Codex update available. Press enter to install…" | codex_update | codex_update | 0,68 | 95 |
| "python3 -c print(2+2) → 4; a soma é 4" | ja_decidido | ja_decidido | 0,77 | 118 |

n=1 por caso. *Medido* nesta rodada. Não calibra limiar.

### Rodada 1: opinião inicial

- **Posição:** Sombra no fato rodado, no voto livre e no diálogo; o caro só vê a dúvida.

#### 1. O ranking dos usos

- **Posição:** Fato rodado, voto que o regex perde, diálogo que a regex do Codex quebra.
- **Por quê:** O dinheiro está na auditoria: 1.564 `fact_check`, US$ 7,16, ~140 s (*medido*, `levantamento.md` §0). O `tev1` não abre arquivo (*lido*, issue). Cabe no fatia `rodado` (510 fatos, texto médio 150 c). Frente auditoria, `fact_audit.py` antes de `call_claude` (:309): "a saída gravada decide?" → `ja_decidido` / `precisa_ler` / `nao_e_fato`. Segundo: meeting-runner, `tally.py:226`, célula que volta `None` → apoio / ressalva / contra / nao_voto; 94 votos tabulares e ~87 textos livres (*medido*, §8). Terceiro: Studio, `startup-dialog-blocked-signals.ts:34`, quando o regex falha (comentário do Codex 0.157 no levantamento §2): as ~10 razões do contrato + `nenhum`.
- **Ideias:** (1) Uma chamada com as três perguntas do pacote da rodada — voto, vira, reage a M# — no fecho do worklog; 3 perguntas somam ~60–90 ms (*medido* pela coordenação, briefing). `(ousadia: média)`. (2) Pré-filtro só em `kind=rodado`: `ja_decidido` com confiança alta não chama o Haiku. `(ousadia: alta)`.
- **Risco:** O "sim" sintético do gatilho saiu com confiança 0,15 e 0,42 (*lido*, issue). Cortar o Haiku cedo perde o caso caro. A sonda desta rodada acertou 3/3 com n=1.
- **Confiança:** 74/100

#### 2. A régua de entrada

- **Posição:** Sombra uma semana; entra quem tiver falso negativo ≤ 2% no rótulo que dói.
- **Por quê:** Sem `resolver.tev1_min_confidence`, tudo vai ao Haiku (*lido*, `resolver.py` e §3). Os 7 resolver reais foram Haiku ou fallback, confiança 0,57–0,96 (*medido*, §0). *Suposto:* o erro que importa muda por uso — auditoria perde `fails` (só 17 em 1.564); gatilho perde o "sim"; voto perde o "contra". Régua única: n ≥ 50 rótulos à mão, acerto e falso negativo por limiar 0,3 / 0,5 / 0,7 / 0,9, e a dúvida (abaixo do limiar, sem Ollama, HTTP 400) sobe ao Haiku; se o Haiku faltar, à coordenação, nunca ao silêncio.
- **Ideias:** (1) A tabela da Balança vira a régua; Fagulha não inventa número hoje. `(ousadia: baixa)`. (2) Dois limiares no mesmo cliente: alto para pular o Haiku, baixo para só registrar. `(ousadia: média)`.
- **Risco:** Um limiar copiado dos 4 casos sintéticos mata o gatilho verdadeiro.
- **Confiança:** 78/100

#### 3. Onde mora o cliente

- **Posição:** Um verbo `brza classify` no workflow, em cima do `resolver.py`, com N perguntas e um jsonl.
- **Por quê:** A chamada já existe (`resolver.py:115`, *lido*). As seis frentes não merecem seis clientes. Contrato: `state` + `questions` → `choice`, `probabilities`, `confidence`, `path`. Sem Ollama ou fila ocupada: `path=duvida` na hora, sem retentativa (8 paralelas não aumentam vazão, *medido*, briefing). Acima de 2.048 tokens o Ollama devolve 400 (*medido*, briefing): o verbo recusa com `path=recusa_tokens` e o chamador corta; não trunca em silêncio. CLI e hook falam com o verbo; o Studio fala HTTP local no mesmo contrato, porque o app não deve puxar o Python do workflow (*suposto*).
- **Ideias:** (1) `brza classify --state-file --questions f.json` grava uma linha em `.brza/classify.jsonl`. `(ousadia: média)`. (2) O MCP expõe o mesmo verbo para o dispatch que já chama `classify`. `(ousadia: baixa)`.
- **Risco:** O Studio em ms de título não espera 100–700 ms (*lido*, §2). Esse caminho fica de fora.
- **Confiança:** 80/100

#### 4. Além do óbvio

- **Posição:** A ousadia é a sombra em tudo que já tem rótulo; o modelo não decide ainda.
- **Por quê:** O corpus de ouro já existe e ninguém rotulou de novo: 94 votos, 564 perguntas com opção (439 na recomendada), 510 fatos `rodado` (*medido*, §0 e §8). *Suposto:* uma semana de sombra, com o caminho atual intacto, dá o par (tev1, rótulo) para limiar e para um retreino. Outro modelo ao lado só depois, no que o 4B errar junto (os "sim" de confiança baixa). Várias perguntas por `state` cabem: o formato já é um mapa (*lido*, §3.1).
- **Ideias:** (1) Retreino mxfp8 com o jsonl da sombra, `num_ctx` 2048 mantido. `(ousadia: alta)`. (2) No Studio, o tev1 só no miss do regex de diálogo, não no título. `(ousadia: média)`.
- **Não fazer:** persona, síntese ou revisor; cota e conta (é número, *lido*, §1); `computeAgentStatusFromTitle` (regex e latência, §2); migration-runner primeiro (0 usos, §6); fan-out paralelo; limiar publicado a partir de 4 casos.
- **Risco:** A sombra na auditoria disputa a mesma fila do Ollama e atrasa a reunião (*medido*, concorrência no briefing).
- **Confiança:** 71/100

#### 5. O plano e para onde evolui

- **Posição:** Fase 0 só grava; fase 1 mede; fase 2 corta o Haiku; o retreino fica aberto.
- **Por quê:** Pronto da fase 0: uma linha por decisão, zero mudança de rota. Pronto da fase 1: tabela limiar × acerto × falso negativo no fato `rodado` e no voto `None`, n≥50. Pronto da fase 2: `tev1_min_confidence` por pergunta, dúvida no Haiku, custo da auditoria medido de novo. *Suposto:* o plano mora em `plans/` deste workstream, sem código hoje.
- **Ideias:** (1) Fases: 0 sombra jsonl; 1 tabela; 2 `brza classify` no hook e no `tally.py`; 3 miss de diálogo no Studio; 4 retreino. `(ousadia: média)`. (2) Evoluções abertas: segundo modelo local, perguntas novas no resolver (`layer` já existe), limiar por frente, e desligar a sombra se a fila passar de ~1 s. `(ousadia: alta)`.
- **Risco:** Fase 2 sem a tabela da fase 1 repete o R2.2: tudo no Haiku, ou pior, um corte no escuro.
- **Confiança:** 76/100

#### A ideia mais ousada desta rodada

Uma semana em que cada fato `rodado` e cada voto que o `classify_vote` devolve `None` passam no `tev1` e só são gravados. O Haiku e o regex continuam mandando. No fim, o par (escolha, rótulo de hoje) escolhe o limiar — ou mostra que o 4B não serve e o retreino nasce desse jsonl. Risco: a fila única do Ollama (8 chamadas ~1,85 s) atrasar a auditoria no meio da reunião; a sombra precisa de `keep_alive` e de ceder quando a latência por chamada passar de ~1 s.

#### Issues candidatas

- **Sombra do tev1 nos fatos `rodado`** — 510 fatos e US$ 7,16 dizem onde cortar o Haiku sem cortar no escuro — `high`
- **`brza classify` com N perguntas e jsonl** — um cliente para as seis frentes, recusa explícita acima de 2048 tokens — `high`
- **Voto `None` do `tally.py` vai ao tev1 com aviso** — o regex já cobre o formato; o modelo só pega a prosa — `medium`
- **Diálogo de startup no miss do regex** — Codex 0.157 quebra o texto; o tev1 entra só aí, nunca no título — `medium`

#### Placar da rodada 1

| Assunto | Posição em uma linha | Confiança |
| :------ | :------------------- | :-------- |
| 1. O ranking dos usos | Fato rodado, voto livre, diálogo no miss do regex | 74 |
| 2. A régua de entrada | Sombra primeiro; falso negativo ≤ 2% no rótulo que dói | 78 |
| 3. Onde mora o cliente | `brza classify` sobre o resolver, dúvida sem retentativa | 80 |
| 4. Além do óbvio | Sombra no que já tem rótulo; não decidir ainda | 71 |
| 5. O plano e para onde evolui | Grava, mede, corta o Haiku; retreino aberto | 76 |

<!-- fim-rodada-1 -->

### Rodada 2: debate

Hora 21:36. Li a síntese (M1–M12) e a rodada 1 dos outros cinco. Não medi de novo: M5, M8, M11 e M12 já derrubam o que eu ia ligar.

- **Posição:** Larga o filtro e o voto: a sombra guarda o que a auditoria apaga.

#### As disputas

- **D1 · o envelope do cliente:** c — o módulo que o `tally.py` importa, mais o verbo fino para hook e CLI. Processo por fato, em 510 `rodado`, paga o arranque à toa; o Studio não importa o pacote. *Suposto* o custo do processo; o volume é *medido* (M7). — 80/100
- **D2 · o primeiro uso depois da sombra:** e — nenhum uso ligado. M8: a evidência da auditoria é apagada, então o pré-filtro não tem corpus. M5: o `None` do voto é 4 de 98. M11: o gatilho erra 3 de 6 "sim". M6: o `layer` tem 7 linhas. — 86/100
- **D3 · a régua:** a — no erro caro, n_sim ≥ 30 e FN 0. Meu "≤ 2% com n ≥ 50" esconderia um "sim" perdido; M11 mostrou 50% de FN nessa classe (n_sim = 6). — 74/100
- **D4 · o diálogo de startup do Studio:** b — fora até haver volume. M9 diz que o volume não foi medido, e M2 diz que cada chamada entra na mesma fila. O miss do regex continua candidato, em sombra, não no plano de ligar. — 70/100
- **D5 · retreino:** b — evolução aberta, alimentada pela sombra. M8 impede o (c): não há fato + evidência + veredito. — 88/100

#### Os ataques

- **Faro, pré-filtro e LoRA já.** M8 (`fact_audit.py:430`, pasta vazia) e a conferência da síntese: não existem 1.564 pares, e "60–80%" não foi medido aqui. O que derrubaria: uma cópia do parágrafo e do veredito ainda em disco.
- **Balança, pergunta `evento`.** M12: "sim" em 23 de 23, inclusive nos 17 "não". O critério vago vira alarme total. O que derrubaria: a mesma matriz com um critério que marque "não" nos 17 negativos.

#### A concessão

M5 me tirou o voto livre do pódio: o regex já acerta quase tudo, e o `tev1` leu "ressalva" em 22 de 37 "apoio". M8 me tirou o pré-filtro como primeiro uso. M11 me tirou qualquer filtro de gatilho.

#### "Sim, e…"

Sobre o `Classifier` da Bitola: a fase 0 não classifica. Antes de `fact_audit.py` apagar o parágrafo (M8), o hook grava fato, saída e veredito no jsonl do cliente. O `tev1` lê essa linha em sombra, sem cortar o Haiku. `(ousadia: média)`

#### Placar da rodada 2

| Assunto | Posição agora | Confiança R1 | Confiança R2 | Mudou? (não, ajustou, virou) | Quem ou o que te moveu |
| :------ | :------------ | :----------- | :----------- | :--------------------------- | :--------------------- |
| 1. O ranking dos usos | Sombra que guarda o parágrafo; voto e gatilho saem | 74 | 84 | ajustou | M5, M8, M11 |
| 2. A régua de entrada | FN 0 e n_sim ≥ 30 no erro caro | 78 | 74 | virou | M11, Balança |
| 3. Onde mora o cliente | Módulo importável e verbo fino | 80 | 80 | ajustou | Bitola |
| 4. Além do óbvio | Retreino só depois do corpus; diálogo espera volume | 71 | 82 | ajustou | M8, M9 |
| 5. O plano e para onde evolui | Fase 0 grava o que o hook apaga; nada liga | 76 | 84 | ajustou | M8 |

<!-- fim-rodada-2 -->

### Rodada 3: voto final

Hora 21:41. Sonda nova, n=4, critério "o texto já traz comando e resultado?" (`traz`/`nao_traz`):

```sh
python3 -I -  # POST /v1/systemone tev1:4b, uma pergunta tipo
```

Os dois "traz" saíram `traz` com confiança 0,84 e 0,86 (211 ms e 76 ms). Os dois "nao_traz" também saíram `traz`, com confiança 0,012 e ~0 (98 ms e 65 ms). A escolha não discrimina; a margem, sim. Não serve para ligar nada.

- **Posição:** Apoio cliente e corpus; o valor cedo é o lote noturno, sem mudar a rota.
- **Fatos lidos:** M13, M14, M15 e o limite do M5.

#### O voto em cada proposta

| Proposta | Voto (apoio, apoio com ressalva, contra) | Ressalva ou alternativa em uma linha | Confiança |
| :------- | :--------------------------------------- | :----------------------------------- | :-------- |
| P1 | apoio | O hook grava o corpus pelo verbo se o import do `brza_mcp` não couber | 88 |
| P2 | apoio | Trinta dias pode ser curto para o retreino; o hash não substitui o texto | 84 |
| P3 | apoio | A cópia do parágrafo vale mesmo com o `tev1` desligado | 92 |
| P4 | apoio com ressalva | `layer` e `gatilho` não rodam a cada chamada (M13: 22%; M11: 3/6); `fato_rodado` e `voto` sim | 80 |
| P5 | apoio | Classe cara fora da amostra, FN 0, FP declarado; sem limiar, só loga | 83 |
| P6 | apoio com ressalva | Os cortes de 80% e 10% são *supostos* até o primeiro probe | 76 |
| P7 | apoio | Diálogo só depois de contar os misses; título, cota e gate ficam fora | 84 |
| P8 | apoio com ressalva | Não "ligar o `layer` atual": M13 manda reescrever a pergunta antes | 77 |

#### O que me faria mudar de ideia

- **P3:** achar o parágrafo do fato ainda em disco depois do `os.remove` (`fact_audit.py:430`). Aí a cópia deixa de ser o primeiro passo.
- **P1:** um teste em que o hook do workspace não pode importar `brza_mcp`. Aí o verbo deixa de ser casca e passa a ser o cliente.

#### A última ideia

A sala diz que nada liga antes da tabela. O que liga é a rota. O valor de amanhã é um lote noturno, em série, sobre o jsonl do P3: `brza classify` lê cada parágrafo já guardado e escreve uma tabela escolha × veredito do Haiku no worklog da coordenação. Nada muda o `fact_audit.py`. O erro é uma linha errada numa tabela, e Anderson vê no dia seguinte onde o 4B discorda dos 17 `fails` e dos 638 `unknown` (M7). `(ousadia: média)`

#### Os colegas

| Persona | A contribuição mais útil dela, em uma linha | Nota de 0 a 10 |
| :------ | :------------------------------------------ | :------------- |
| Balança | A matriz 3/6 e o limite do M5: os 22 "apoio" podem ser o `state` da coordenação | 9 |
| Ferrolho | Negativo revisado e piloto que dá para desligar | 8 |
| Bitola | `Classifier.ask` e o probe antes de entrar no catálogo | 9 |
| Faro | A cascata como norte; o corpus de 1.564 pares não existia | 7 |
| Lida | O `tev1` só decide o que ninguém precisa ver | 8 |

#### Autoavaliação

Fiel na ideia do lote que entrega valor sem esperar o limiar, e no lugar (`brza classify` sobre o jsonl). Saí da provocação ao aceitar que `layer` e `gatilho` não merecem a fila (M2, M13): isso é a régua da Balança, não o atalho.

<!-- fim-rodada-3 -->

### Rodada 4: a confiança final

Hora 21:47. Li a proposta v2. A confiança da R3 no par é a média dos meus votos daquela rodada.

- **Posição:** O plano serve: grava o que se perde e mostra a ordem; nada decide ainda.
- **Fatos lidos:** M16, M17, M18, M19.

| Parte do plano | Confiança na versão anterior | Confiança na versão atual | Uma linha de porquê |
| :------------- | :------------------------- | :------------------------ | :------------------ |
| O cliente (P1) | 88 | 90 | A folha sem política e o verbo que sai entraram (R3, Bitola e Lida) |
| A sombra, o corpus e a linha zero (P2, P3) | 88 | 90 | M18 grava o `task` no POST que já existe; o texto, não o hash, é o corpus |
| A sugestão visível e a ordem | — | 81 | M17: AUC 0,74, os 3 primeiros acertam; a lista inteira fica; n=23 |
| A régua e o portão (P5, P6) | 80 | 84 | Os cortes seguem provisórios; o holdout guarda a classe que já errou |
| As evoluções (P8) | 77 | 80 | O `layer` atual se reescreve; o pré-filtro se mede em atenção (M16) |
| **O plano inteiro** | 83 | 85 | Começa por gravar e ordenar; nenhuma rota muda antes da régua |

- **A sua mudança da rodada anterior entrou?** sim — o lote noturno está em "A sugestão visível"; `layer` e `gatilho` fora de cada chamada estão em "O catálogo de perguntas".
- **O que ainda está errado:** em "As fases", a fase 1 vem antes da fase 0, e a linha zero (M18) não pode esperar o módulo. A retenção do texto ainda é a Rodada A, não um prazo. M19 (n=4) não vira régua.
- **A pergunta que Anderson precisa responder:** autoriza a sugestão ordenada no painel da próxima reunião, lista inteira e sem efeito? Recomendo que sim, e que o texto do `state` fique até a classe cara passar de n=30, não por 30 dias fixos.
- **Autoavaliação:** Fiel: o atalho virou desenho (ordem no painel e lote na auditoria) sem o modelo decidir. Saí da provocação ao aceitar que isso espera a sombra da fase 2, em vez de pedir a tabela na reunião de amanhã.

<!-- fim-rodada-4 -->

### Rodada 5: a confiança na v4

Hora 21:57.

- **Posição:** A v4 acerta: grava primeiro e tira o layer; a ordem espera o replay.
- **Fatos lidos:** M3 revisto, M20 e o parecer do revisor, pela proposta v4.

| Parte do plano | Confiança na versão anterior | Confiança na versão atual | Uma linha de porquê |
| :------------- | :------------------------- | :------------------------ | :------------------ |
| **O plano inteiro** | 85 | 86 | A fase 0 grava antes do cliente e o `layer` fica reprovado no P6 (86% "alta") |

- **O revisor acertou ou errou onde?** Acertou nos quatro furos da v2: a cópia na fase 3, o `layer` no catálogo, o M17 no resumo à mão e os dois escritores. Não vi número errado.
- **O que ainda está errado:** em "A gravação" e "As fases", a fase 0 espera a Rodada A, e cada auditoria segue apagando um parágrafo (M8). Em "A classificação dos usos", o teto de ~5.000 caracteres (M3) deixa sem medida quantos fatos `rodado` cabem.

<!-- fim-rodada-5 -->

## Custo da tarefa

Corrido 7 min — agente 5 min, quem pediu 3 min, pausa 0 s · US$ 2,48 (turnos 1,87, subagentes 0,61) · CPU 8,62 s do `claude` e 65,70 s dos comandos, RSS até 425 MB · 22 turnos, 1 sessão · dividida com 6 outros worklogs do commit · até 22:02 de 2026-11-09, pelo `brza note commit`
