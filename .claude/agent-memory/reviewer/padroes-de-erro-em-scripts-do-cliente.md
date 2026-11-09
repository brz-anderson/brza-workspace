---
name: padroes-de-erro-em-scripts-do-cliente
description: Onde o defeito se esconde nos scripts do pacote client do brza-workflow (brza-run e afins) — shlex.quote que não protege do zsh, ramo do main sem teste, sonda que o próprio zsh do Bash expande
metadata:
  type: project
---

Padrões vistos na revisão do `fix/brza-run-argv` (2026-11-09, `command_of` com `shlex.join`):

- **`shlex.quote` é POSIX, não zsh.** Ele deixa sem aspas a palavra que começa com `=` (o `=` está no conjunto
  seguro), e o zsh, com `EQUALS` ligado por padrão, troca `=ls` por `/bin/ls` e aborta a linha com `=inexistente`
  ("not found"). Vale para tudo que monta linha com `shlex` e entrega a `$SHELL -ic` ou ao `--command` da aba, que o
  app digita no zsh interativo. Confiança 95, reproduzido rodando o script.
- **O ramo de despacho do `main()` fica sem teste.** Os testes chamam `run_in_tab`/`run_for_result`/`run_in_chat` direto
  pelo `runpy`; trocar o argumento num ramo do `main()` (o `--chat`) passa a suíte inteira. Cheque: mutar cada ramo
  numa cópia com `git init` (sem git, os testes de aba quebram no `rev-parse` e a base já falha).
- **A correção aplicada em dois lugares fica testada num só.** Na 2ª rodada, a `quote` entrou no `command_of` e no
  `inner` da aba; voltar o `inner` ao `shlex.quote` passou a suíte, porque a aba de mentira roda o `inner` em `/bin/sh`.
  Cheque: uma mutação por ponto de uso da função nova, não só pela função. Confiança 95, mutação.
- **A sonda com `=x` no Bash daqui é expandida antes:** o Bash tool roda em zsh; citar o `'=x'` na linha da sonda, senão
  o erro sai do meu shell e parece do script.

**Why:** o defeito real estava na diferença POSIX/zsh, que o teste com `/bin/sh -c` como aba de mentira não vê.
**How to apply:** em diff que cita argumento para shell, rodar a ida e volta com `/bin/zsh -ic` e casos `''`, `'a b'`,
`$HOME`, `*`, `'`, `!x` e `=ls`; mutar cada ramo do `main()`. Relacionado: [[achados-que-costumam-cair]],
[[padroes-de-erro-em-codigo-brza-mcp]].
