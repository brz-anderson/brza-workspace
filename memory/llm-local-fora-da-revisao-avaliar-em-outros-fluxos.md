---
name: llm-local-fora-da-revisao-avaliar-em-outros-fluxos
description: O qwen2.5:14b local (Ollama) falhou na revisão do experimento da 12.2 do PLN-004; Anderson parou a medição e avaliará LLMs locais em outros fluxos depois
metadata:
  node_type: memory
  type: project
  originSessionId: 330bdc33-f82d-4dba-94d9-2b924664eb99
  modified: 2026-11-02T22:38:05.976Z
---

Em 2026-11-02, o `qwen2.5:14b` rodou as 3 revisões do experimento da 12.2 do PLN-004: recall 0 de 7, 1 achado
verdadeiro em 80 únicos, 47% de repetição, confiança 80 a 100 sem valor, 22,8 min de parede e 14,9 GB *wired* com swap
até 11,6 GB numa máquina de 24 GB. O desenho era sem ferramenta, com o diff em 4 trechos.

**Why:** Anderson quer economizar token com modelo local, e a medição disse que a revisão adversária não é a tarefa
para ele. Ele respondeu "Parar aqui" e disse que avaliará LLMs locais em outros fluxos no futuro.

**How to apply:** não proponha modelo local para revisão nem repita essa medição. Se Anderson trouxer um fluxo novo,
meça tarefa mecânica (extração, classificação, pré-filtro) e leve o consumo da máquina junto: memória livre e swap
pesam mais que CPU. O script, as saídas e as amostras estão em `/private/tmp/pln004/bench/` (`run-qwen.py`,
`out/qwen-*`), e o resumo está no worklog `2026-11-02-pln-004-a-revisao-contra-o-pln-006.md`.
