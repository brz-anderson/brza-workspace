---
name: llm-local-fora-da-revisao-avaliar-em-outros-fluxos
description: LLM local falhou na revisão (qwen2.5:14b, recall 0 de 7); no desempate do M11 do PLN-003, o modelo de decisão tev1:4b classifica texto, mas nenhum local aplica regra numérica
metadata:
  node_type: memory
  type: project
  originSessionId: 330bdc33-f82d-4dba-94d9-2b924664eb99
  modified: 2026-11-03T03:05:49.164Z
---

Em 2026-11-02, o `qwen2.5:14b` rodou as 3 revisões do experimento da 12.2 do PLN-004: recall 0 de 7, 1 achado
verdadeiro em 80 únicos, 47% de repetição, confiança 80 a 100 sem valor, 22,8 min de parede e 14,9 GB *wired* com swap
até 11,6 GB numa máquina de 24 GB. Anderson respondeu "Parar aqui".

Em 2026-11-03, no desempate do M11 do PLN-003, os locais acertaram a camada pelo texto (10/10), mas nenhum aplicou a
regra numérica de cota sempre: `qwen2.5:7b` 4/10 com loop de repetição, `qwen2.5:14b` 7/10 a 15 GB, `tev1:4b` 53/60
em casos aleatórios. O `tev1:4b` (modelo de decisão do Ollama, `/v1/systemone`) respondeu em ~0,09 s, a 7,7 GB, e
entendeu português. Anderson escolheu "tev1 + Haiku" e removeu os `qwen2.5`.

**Why:** Anderson quer economizar token e latência com modelo local; a medição diz onde ele serve: classificar e
escolher entre opções, não revisar nem fazer conta.

**How to apply:** não proponha local para revisão nem para regra numérica (vai à tabela/código). Para classificação,
roteamento e pré-filtro, comece pelos modelos de decisão (`tev1`), com limiar de confiança e volta ao Haiku, e meça a
memória livre e o swap junto. O resultado está no worklog `2026-11-03-o-desempatador-local-do-m11.md`.
