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
- Rode `agy -p "<prompt>" --model <modelo> --add-dir <worktree das notas> --add-dir <scratch> --mode plan
  --print-timeout 1200s` no worktree do código. Sem o `--add-dir`, o sandbox do modo plan não lê fora do worktree, e
  no `-p` o pedido de permissão fica sem resposta. O parecer volta pela saída, e a sessão o grava.
- **A cota do `agy` acaba:** em 2026-11-03, o Gemini 4 Argon (high e medium) esgotou com reset em ~7 dias, e o Opus em
  ~5 h. Confira com um `agy -p "OK"` antes de um laço longo; `RESOURCE_EXHAUSTED` na saída é revisão que não rodou.
  Anderson escolheu (PLN-009/R3): seguir no `gemini-3.8-flash-high` e fazer uma rodada final pelo Opus antes do `[x]`.
- **O destino preferido é `corrigido aqui`** (pedido seguinte, mesmo dia: "prefira sempre optar por `corrigir aqui`").
  Issue ou decisão só quando o conserto não cabe no passo; `falso` fica no parecer.
- **Laço de até 3 rodadas por passo:** os achados de código vão direto a um `implementer`; ao terminar, nova revisão
  pelo `agy`; repete até zerar os `corrigido aqui` ou completar 3 rodadas. O que sobra na 3ª vai a issue.
- O parecer vai a `work/reviews/pln-NNN-<assunto>.md` (ver [[pln-009-execucao]]).
