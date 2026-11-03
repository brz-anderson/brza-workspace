---
status: open
description: O test_brza_note falha indevidamente em dois testes quando o TMPDIR do ambiente contém brza-studio em seu caminho absoluto.
scope:
  - brza-workflow
opened: 2026-11-03
owner: Anderson
tags:
  - tooling
---

# Falso negativo em test_brza_note quando TMPDIR contém brza-studio no caminho

## O contexto

Ao executar a suíte de testes de unidade da CLI (`tests/cli/test_brza_note.py`) no `brza-workflow` sob o runner
do Antigravity, dois testes falharam:

1. `test_the_refusals_name_the_code_of_the_manifest_and_not_the_brza_studio`
2. `test_the_refusals_say_the_code_when_there_is_no_manifest`

A falha observada:

```text
AssertionError: 'brza-studio' unexpectedly found in 'recusado: sem workstream: a master guarda só a norma, e /Users/andepb/Library/Application Support/brza-studio/acp-temp/antigravity/run-d7ns1M/tmpdxhgbqpx não é worktree de workstream nem do casa-app; passe --workstream <nome>\n'
```

## O problema e o desvio

- Os testes utilizam `self.assertNotIn('brza-studio', out)` para garantir que a mensagem de erro use o nome do código
  do manifesto ou o termo genérico `do código`, em vez do nome fixo do app (`brza-studio`).
- Porém, a mensagem de recusa emite o caminho absoluto do diretório de execução atual:
  `"... e <caminho> não é worktree de workstream..."`.
- Como o ambiente do runner do Antigravity roda sob `/Users/andepb/Library/Application Support/brza-studio/...`,
  o caminho absoluto alocado temporariamente para o teste contém a substring `brza-studio`.
- Isso causa um falso negativo: a asserção falha pelo path do sistema de arquivos, e não pela lógica de formatação da mensagem.
- Executando com `TMPDIR=/tmp`, todos os 73 testes da suíte passaram sem erros (em 33,7 s).

## O que falta decidir

- Em `tests/cli/test_brza_note.py`, ajustar a asserção para validar especificamente a menção ao código ou mascarar o
  prefixo do diretório de trabalho/temporário na saída testada, evitando falsas falhas em qualquer ambiente cujo path
  contenham o nome do produto.
