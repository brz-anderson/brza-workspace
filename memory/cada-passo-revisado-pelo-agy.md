---
name: cada-passo-revisado-pelo-agy
description: "Na execução de plano, cada passo só fica pronto depois de um reviewer rodado pelo agy, com os achados encaminhados pela opção recomendada"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 041f4028-2390-4bcf-b2c1-9511925a3772
  modified: 2026-11-03T06:12:17.007Z
---

Cada passo executado de um plano passa por um `reviewer` rodado pelo `agy` (Antigravity CLI), e só fica pronto (`[x]`)
depois dessa revisão, com cada achado encaminhado como a norma manda. O destino de cada achado é sempre o recomendado,
sem rodada de pergunta.

**Why:** Anderson pediu em 2026-11-03, ao retomar o PLN-009: "para cada passo executado, acione um `reviewer`
utilizando o `agy`, o passo só será considerado `pronto` ao final da revisão, com os achados encaminhados conforme
manda a norma, escolha o encaminhamento dos achados sempre pela opção `recomendada`". Uma revisão de outra família de
modelo não ancora na leitura do Claude que executou.

**How to apply:**
- O `agy` não tem o papel `reviewer`: o prompt leva o corpo de `.claude/agents/reviewer.md` e o pedido.
- Rode `agy -p "<prompt>" --model gemini-4-argon-high --mode plan --print-timeout 900s` no worktree do código. Em `--mode plan`, ele lê e roda comandos; o parecer volta pela saída, e a sessão o grava.
- **O destino preferido é `corrigido aqui`** (pedido seguinte, mesmo dia: "prefira sempre optar por `corrigir aqui`").
  Issue ou decisão só quando o conserto não cabe no passo; `falso` fica no parecer.
- **Laço de até 3 rodadas por passo:** os achados de código vão direto a um `implementer`; ao terminar, nova revisão
  pelo `agy`; repete até zerar os `corrigido aqui` ou completar 3 rodadas. O que sobra na 3ª vai a issue.
- O parecer vai a `work/reviews/pln-NNN-<assunto>.md` (ver [[pln-009-execucao]]).
