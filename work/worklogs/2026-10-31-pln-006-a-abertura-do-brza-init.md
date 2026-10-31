---
scope:
  - workspace
---

# PLN-006: a abertura do brza init

Anderson perguntou, na sessão `workspace`, se já havia mecanismo "para inicializar a norma inteira, com AGENTS CLAUDE
plans/ wiki/ work/ skills/ agents/ num repositório do zero". Não havia, e ele pediu o plano:
[PLN-006: O `brza init` monta a norma num workspace do zero](../../plans/PLN-006-o-brza-init-monta-a-norma-do-zero/PLN-006-plan.md).

## O que se levantou

- As peças de hoje — `brza note workstream`, `memory-setup`, `new`, `sync`, `brza install`, o `notes-checker` — só
  operam dentro do `brza-workspace` já montado.
- Os caminhos do par workspace/código estão fixos em `brza_runtime.py`, na função `claude` do `~/.zshrc` e no
  `claude-brza`.
- Umas 250 linhas, em ~40 arquivos da `master`, citam o que é local; a separação genérico/local custa ~4–6 h em
  qualquer caminho.

## O que se decidiu

A R1, toda na recomendada: o plano é o `PLN-006`, no `workspace`; o alvo é um workspace ao lado do código, como o par de
hoje; o mecanismo é um `brza init` determinístico; e a norma genérica acompanha a daqui por sync. O número subiu na
`master` em `0310bb4`.
