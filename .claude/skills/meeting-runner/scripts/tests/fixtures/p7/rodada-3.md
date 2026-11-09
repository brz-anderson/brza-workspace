# Rodada 3 — o voto informado entre A e B (duração: ~5 min)

Anderson escolheu a rodada extra (alternativa C): a escolha entre A e B foi votada na R2 sem o fato que o Prumo mediu.
Leia antes, em `.sessions/reuniao-ci-no-chat/proposta-v2.md`, as linhas **M6, M6b, M7 e M9** da tabela "O que se mediu"
e a tabela "As alternativas" (A e B mudaram: a A ganhou o gatilho por dono e conta do revisor). Leia também a
`### Rodada 2` do worklog do Prumo. Dado medido pesa mais que argumento. Confira um número por comando, se quiser.

**Acrescente no fim** do seu worklog esta estrutura; a **última linha do arquivo** fica `<!-- fim-rodada-3 -->`:

```markdown
### Rodada 3: o voto informado entre A e B

- **Posição:** o seu voto, em até 100 caracteres.

#### O voto

| Proposta | Voto (apoio, apoio com ressalva, contra) | Ressalva ou alternativa em uma linha | Confiança |
| :------- | :--------------------------------------- | :----------------------------------- | :-------- |
| A | … | … | NN |
| B | … | … | NN |

- **O que o M6/M6b mudou em você:** até três linhas; "nada" vale, com o porquê.
- **O que te faria mudar de novo:** o fato ou o teste que derrubaria o seu voto.

| Parte do plano | Confiança na versão anterior | Confiança na versão atual | Uma linha de porquê |
| :------------- | :------------------------- | :------------------------ | :------------------ |
| **O plano inteiro** | NN | NN | … |

<!-- fim-rodada-3 -->
```

No máximo ~20 linhas. Não pergunte nada; decida e declare a suposição. Não faça commit.
Depois de gravar a seção e o marcador, rode `brza orchestration send --subject "fim-rodada-3" --body "persona:<slug>"`
(o sinal de fim); não envie `worker_done` agora.
