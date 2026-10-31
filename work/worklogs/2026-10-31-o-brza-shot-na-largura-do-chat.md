---
scope:
  - workspace
  - brza-studio
---

# O brza shot na largura do chat

O pedido veio da sessão do workstream `workspace`, no chat do BrzA Studio, em 2026-10-31. Anderson decidiu lá, na
rodada do teste dos artboards no chat: "A opção 1 em todas", com a 3.1 "736 px, a do chat, pedido ao `tools-kit`". O
`brza shot` passa a capturar em 736 px por padrão, a largura do chat: o `--chat-content-max-width: 46rem` do
`src/renderer/src/assets/main.css` do `brza-studio`, nas linhas 209 e 321.

O motivo, registrado no worklog `2026-10-31-artboards-na-rodada-de-desenho.md` do `workspace`, seção "O teste no
chat": o PNG de 1280 px escondeu um defeito do artboard. Uma grade `1fr 1fr` com título `nowrap` alargava a coluna, e a
736 px a segunda coluna saía cortada, como no chat, que esconde a barra de rolagem.

## O que se fez

- **`0dcc82d` na `master`:** `feat(brza): o brza shot captura em 736 px, a largura do chat`. O `scripts/brza/brza-shot`
  mudou o padrão do `--width` de 1280 para 736 no `add_argument`, no uso e na ajuda, que agora dizem que é a largura do
  chat.
- **Os testes:** nenhum dos 13 do `test_brza_shot.py` conferia o padrão; todos passaram de novo.
- **A norma:** fora dos passos 3 e 4 do Desenhar, que a sessão `workspace` reescreve com Anderson, nenhum arquivo da
  norma citava 1280. Não houve commit de norma.
- **O merge da `master`** entrou só no `tools-kit`, sem o `brza note sync`, para não mexer no worktree do `workspace`
  com a sessão de lá trabalhando.

## A conferência

- **Um `brza shot` sem `--width`, com `--scale 1`**, saiu com 736 px de largura (`sips -g pixelWidth`).
