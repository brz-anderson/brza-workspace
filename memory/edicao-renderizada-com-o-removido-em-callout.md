---
name: edicao-renderizada-com-o-removido-em-callout
description: "Arquivo editado aparece na resposta com o diff e, abaixo, o trecho renderizado, com o removido em callout CAUTION"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 330bdc33-f82d-4dba-94d9-2b924664eb99
  modified: 2026-10-31T05:02:59.004Z
---

No `<details>` do arquivo editado, abaixo do `diff`, vai o mesmo trecho em Markdown renderizado. Cada bloco de linhas
removidas fica no lugar em que estava, num callout `> [!CAUTION]` de título **Removido**.

**Why:** Anderson pediu em 2026-10-30, no PLN-004: "no arquivo editado, renderize também como `Markdown`, com as linhas
removidas como `>![<algum tip>]`". Na rodada de levar isso à norma, escolheu ficar só na memória do workstream: "faremos
mais medições ao longo dos trabalhos, como a possibilidade de poluir a conversa". O tipo `CAUTION` foi escolha da
sessão, e Anderson não o contestou.

**How to apply:** em toda resposta deste workstream que grava em `plans/`, `wiki/`, `work/` ou `memory/`, e também na
norma da `master` — `AGENTS.md`, `CLAUDE.md`, `README.md`. Em 2026-10-31, a edição do `AGENTS.md`, do `CLAUDE.md` e de
um worklog saiu só com o `diff`, porque a sessão leu o índice e não abriu esta memória; Anderson: "pq vc não está o
mostrando o diff como `Mardown` renderizado?". Observe o
peso: quando o renderizado repetir um trecho longo, como uma rodada inteira, anote o tamanho. A medição decide se a
regra sobe à norma do `AGENTS.md` ou se é enxugada.

**O `---` fecha todo bloco de arquivo, também o último.** Anderson, em 2026-10-31, sobre o bloco do `memory/MEMORY.md`,
o último da resposta: "essa linha deveria ter o --- abaixo também". A norma diz "um separador `---` entre eles"; aqui,
ele vai depois de cada `</details>`, inclusive quando há um arquivo só.
