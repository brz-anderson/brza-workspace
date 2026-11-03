---
name: comparar-pareceres
description: Como cruzar pareceres de dois revisores (Flash x Opus) com o código do commit, no PLN-009
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
