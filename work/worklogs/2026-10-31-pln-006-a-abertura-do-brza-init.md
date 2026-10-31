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

O `collector` levantou o Terreno: o que é genérico e o que é local em cada arquivo, o acoplamento em código e o sync de
hoje. A sessão conferiu cinco fatos por amostra, todos de pé. Um deles contradiz o `CLAUDE.md:3-4`: pela documentação,
com `AGENTS.md` e `CLAUDE.md` juntos o Claude Code carrega só o `CLAUDE.md`. Fica para o Desenho conferir.

A R2 e a R3, todas na recomendada, menos a R2.1, respondida "repo brza-workflow" e confirmada na R3.1:
- o núcleo mora em `brz-anderson/brza-workflow`, público, e o próprio `brza-workspace` o consome pelo sync;
- a parte local se separa por placeholders e um `.brza/workspace.toml`, com as seções inteiramente locais em arquivo
  próprio;
- o núcleo leva a norma, as skills, os agents, o `brza note` e os hooks parametrizados; o CLI roda do checkout do
  `brza-workflow`, e os scripts do `brza-studio` ficam locais;
- a raiz sai do cwd, pelo manifesto; a branch e o remote também vêm do manifesto, com `master` e `origin` por padrão; a
  identidade vem por flags, com o padrão do `git config`.
