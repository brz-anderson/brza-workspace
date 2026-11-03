---
scope:
  - workspace
  - tools-kit
refs:
  - PLN-003
---

# O desempatador local do M11: o `tev1:4b` no lugar do Haiku

Anderson pediu, em 2026-11-02: "Avalie a possibilidade de utilizarmos o qwen2.5:7b como o orquestrador “barato” que
tínhamos sugerido ser um Haiku". A sugestão é o M11 do PLN-003, no workstream `tools-kit`: a tabela de política
(`brza.toml`) decide, e um Haiku por `claude -p --json-schema` só desempata, na fase 2b (R5.1 de lá,
`PLN-003-interview.md:236`; `PLN-003-design.md:196`). O PLN-003 ainda está no Desenho.

## O que se mediu

A mesma sonda em todos os modelos: 10 tarefas em texto livre, das quais o modelo tira a camada (alta, média ou rápida,
pela tabela do `AGENTS.md`), e 5 escolhas de conta por cota — uso semanal e de 5 h, com o teto de 90% e a margem de 5
pontos —, cada uma nas duas ordens. Os qwen rodaram pelo `/api/chat` do Ollama com o `format` do JSON Schema e
temperatura 0; o `tev1`, pelo `/v1/systemone`, o endpoint dos modelos de decisão; o Haiku, pelo `claude -p --model
haiku --json-schema`, sem ferramentas. Tudo no M5 Pro de 24 GB, com o Ollama 0.40.13.

| | `qwen2.5:7b` | `qwen2.5:14b` | `tev1:4b` | Haiku |
| :-- | :-- | :-- | :-- | :-- |
| Camada pelo texto | 10/10 | 10/10 | 10/10 (PT e EN) | 10/10 |
| Conta, 5 casos fixos × 2 ordens | 4/10 | 7/10 | 10/10 PT · 8/10 EN | 10/10 |
| Conta, 60 casos aleatórios contra a regra | — | — | 53/60 PT · 53/60 EN | — |
| A resposta muda com a ordem | 2 de 5 | 1 de 5 | 0 PT · 2 de 5 EN | 0 |
| Falha da chamada | 12 (`token repeat limit reached`) | 0 | 0 | 0 |
| Latência mediana, carregado | ~1,1 s | ~2,6 s | ~0,09 s (2,4 s frio) | ~7 s |
| Memória carregado | 6,6 GB | 15 GB, 11% livre, swap de 1,0 a 1,4 GB | 7,7 GB, 54% livre | 0 |
| Custo | 0 | 0 | 0 | ~US$ 0,0008 por chamada |

- **Classificar texto, todos acertam; a regra numérica, nenhum local acerta sempre.** Os erros do `tev1` nos 60 casos
  caem no teto de 90% e na margem de 5 pontos; em inglês, errou 6 dos 8 casos do teto. A cota fica na tabela.
- **A confiança do `tev1` separa, mas não basta sozinha:** em PT, mediana de 0,80 nos acertos e 0,37 nos erros, mas
  houve acerto com 0,02 e erro com 0,66. O limiar se calibra com empate real.
- **O `tev1` é determinístico:** a segunda rodada dos 20 casos fixos deu o mesmo resultado.
- **Os modelos de decisão do Ollama** (capacidade `decision`: `tev1`, `nimble-v3`, `pplx-decider`) devolvem a
  probabilidade de cada opção, sem gerar texto. O `nimble-v3` é CC BY-NC; a página do `tev1` não diz a licença e diz que
  idiomas fora do inglês não foram testados.
- **A Jev, da TypeSafe AI** (jevai.net é site não oficial; a documentação é `docs.typesafe.ai`), é o mesmo formato em
  nuvem, em acesso antecipado desde 2026-09-15, a US$ 0,042 ou 0,084 por milhão de tokens de entrada (as fontes
  divergem) e saída grátis; a própria TypeSafe a diz fraca em precisão numérica. Fica como opção para o pacote público
  sem Ollama.
- **Ressalvas:** as 10 tarefas são minhas e fáceis; as contas são sintéticas; não há empate real até a fase 2.

Os scripts (`tiebreak.py`, `haiku.py`, `decide.py`, `decide_rand.py`) e as saídas ficaram no scratch da sessão, fora
do git.

## As rodadas

- **Depois do 7B:** "Medir tbm o 14b" (texto livre, 2026-11-02).
- **Depois do 14B:** "Sugira outros modelos que rodam local e podem funcionar no nosso workflow" (texto livre).
- **Depois da lista:** marcou "tev1:4b (Recomendado)" e pediu "Pesquise sobre Jev AI - jevai.net".
- **Depois do `tev1`** (2026-11-03), respondidas nesta sessão do `workspace`:
  - o M11: **"tev1 + Haiku (Recomendado)"** — a cota fica na tabela; o `tev1` desempata o texto e manda ao Haiku abaixo
    do limiar de confiança; a Jev fica como opção de nuvem para o pacote público;
  - o disco: **"Remover os dois (Recomendado)"** — os `qwen2.5`.

O registro no M11 vai ao PLN-003 pela sessão do `tools-kit`, que é o dono do plano.

## Fora do workspace

- **O quê e onde:** `ollama pull tev1:4b`, 4,4 GB em `~/.ollama/models`. **Risco:** só disco. **Estado:** ativo.
  **Como desfazer:** `ollama rm tev1:4b`.
- **O quê e onde:** `ollama rm qwen2.5:7b qwen2.5:14b`, que tira os modelos registrados como ativos no worklog
  [O benchmark M5 Pro × M2 Pro e o Ollama local](2026-11-02-benchmark-m5-m2-e-ollama-local.md). **Risco:** os scripts
  da medição da revisão, fora do git, não rodam mais sem baixar de novo. **Estado:** feito, ~14 GB livres.
  **Como desfazer:** `ollama pull qwen2.5:7b` e `ollama pull qwen2.5:14b`.
