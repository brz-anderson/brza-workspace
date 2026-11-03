---
name: comparar-pareceres
description: Como cruzar pareceres de dois revisores (Flash x Opus) com o código do commit, e como sintetizar vários pareceres num REV, no PLN-009
metadata:
  type: feedback
---

Os worktrees de código ficam em `~/Projects/brza-workflow/.worktrees/pln-009-pN`, cada um já no commit revisado: dá para ler direto
e usar `git archive HEAD packages tests/mcp | tar -x -C /private/tmp/<pasta>` para mutar uma cópia sem tocar o repo.

**Why:** a verificação por mutante numa cópia (`python3` substituindo a linha, `unittest discover -s tests/mcp`) confirma em segundos um
achado "o teste passa sem X". A cópia parcial perde o `brza_root`, e 2 testes de `test_mcp_policy.LoadTest` erram na linha-base: compare com o
original antes de concluir.

**How to apply:** corte a parte "O que rodou" dos pareceres com `sed '/^## O que rodou/,$d'` para ler só os achados; ao conferir um
achado do Flash, cheque se a entrada (`dispatch`, `tools.py` `validate`) permite o estado que ele supõe; os dois `não sustenta` do Flash no P5
caíram assim. Não use `echo ====` seguido de `;` no zsh: o `=` inicial dá "not found" e o código de saída 1 mascara o resto.

**Sintetizar muitos pareceres num REV (500 KB em `/private/tmp/pln009/`):** não leia os arquivos inteiros. Um `grep -E -A1 '^### '` (título + linha
`> tipo · gravidade · confiança · → destino`) por parecer, gravado em arquivo e lido com `Read`, dá o índice; depois um script Python que extrai
só o primeiro trecho "Evidência" de cada achado escolhido (tirar links `(file://…)` e blocos de código). A saída direta no Bash passa de 30 KB e
vira `persisted-output`: grave em `/tmp` e leia por `Read`. Armadilhas: a rodada r2/r3 do Flash lista como `corrigido aqui` ou `falso (no
estado atual)` os achados da r1 só para confirmar o conserto (não são novos); o commit que corrige a r1/r2 dos passos P2 a P6 é `77b917f`, o
da r1 do P1 é `f8829f4`, o da rodada final é `b2c87a6`; o mesmo defeito aparece no Flash e no Opus com ids diferentes (una no REV).
