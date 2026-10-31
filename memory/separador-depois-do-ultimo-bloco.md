---
name: separador-depois-do-ultimo-bloco
description: O --- vai também depois do último bloco <details> de arquivo, quando há prosa depois dele
metadata:
  type: feedback
---

Quando a resposta mostra arquivos em blocos `<details>` e segue com prosa depois do último, o `---` vai também abaixo do
último bloco, e não só entre os blocos. Anderson apontou a falta em 2026-10-31, no bloco da memória do `implementer`, no
fim da resposta do PLN-005 P3.

**Why:** sem o separador, o parágrafo que segue — o próximo passo, a pergunta — cola no bloco recolhido e some na
leitura. O `AGENTS.md` diz só "um separador `---` entre eles", e a leitura literal deixou o último sem.

**How to apply:** depois do último `</details>`, se vier texto, um `---` antes dele. Ver também
[[edicao-renderizada-com-o-removido-em-callout]].
