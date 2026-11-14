---
scope:
  - workspace
  - brza-workflow
tags:
  - tooling
refs:
  - PLN-021
  - PLN-025
---

# A execução do P2 do PLN-025 ficou no PR do gênero feedbacks

Anderson, em 2026-11-14, mandou que a prova de passo, achado e correção fique em `work/worklogs/`. Este arquivo é essa prova do P2 de [PLN-025: Cada execução de Builder deixa métrica, nota e persona calibrável](../../plans/PLN-025-esboco-dos-builders/PLN-025-plan.md). A abertura do plano continua em [O PLN-025 do esboço dos Builders foi aberto](2026-11-14-esboco-dos-builders.md). O corte é o assunto: lá é a abertura e a R1; aqui é a execução do gênero.

O passo segue desmarcado até o merge.

## Plano aceito em 2026-11-14

O P2 executa o D2: o gênero `work/feedbacks/`, uma nota por execução, sem `status`, com as cinco seções e `model`, `effort` e `result`. Norma e script no mesmo commit do `brza-workflow`, com um caso que falha se a seção some.

## Execução

Sessão `bc-6f7d9b8c-9869-5460-b824-3d55ba75f7d0`, `grok-4.7`, esforço `medium`. Abriu o [PR 1](https://github.com/brz-anderson/brza-workflow/pull/1), branch `cursor/pln-025-feedbacks-f7d0`, base `master` em `45e60134a503aa23523d12e53a5a416d5af1e210`. O commit `02fe2a51bd021137f56cc61991a80d2a1612e536` tem 5 arquivos. O `tests/notes-checker/run.py` saiu 0, com 11 casos novos em `check_feedback`.

O git desta gravação confirma o autor `Cursor Agent <cursoragent@cursor.com>`, os 5 arquivos e os 11 `expect` de feedback nesse commit.

Desvios de processo: o autor do commit é `Cursor Agent`, e o nome da branch saiu diferente do pedido. O teste de ouro em `AGENTS.md` estava vermelho antes do PR. O mesmo commit acrescenta ao catálogo de ouro as diferenças esperadas do gênero, em `tests/hooks/golden_differences.py`; isso é o delta do D2, separado das duas falhas anteriores de `AGENTS.md`.

## Revisão R1

Sessão `bc-e93e280f-cdde-5bb7-b3e7-dbf7a88b83db`, `grok-4.7`, esforço `xhigh`, somente leitura. Veredito: aprovar com correções. Quatro achados, todos válidos.

1. Importante. Em `02fe2a5`, `check_notes.py:649` varre o arquivo inteiro com `without_code(text)`, e o frontmatter entra na conta. A sonda mostrou um falso `feedback-section-order` e uma seção ausente que passava.
2. Menor. Faltavam testes para `result` e `model` ausentes. A mutação `if result is not None` passava com a suíte verde.
3. Menor. Faltava `feedbacks` em `templates/README.md`.
4. Menor e anterior. Em `02fe2a5`, `core/.claude/skills/notes-checker/SKILL.md:99` aponta para `${CLAUDE_SKILL_DIR}/tests/run.py`, e esse arquivo não existe na árvore. Na `master` `45e6013` a mesma frase está na linha 97.

Compatibilidade com o Studio, medida nessa revisão: o checador de `45e6013` e o de `02fe2a5` deram JSON idêntico em todas as notas reais. brand 65/0/0, logi-options 7/0/0, playground 194 arquivos com 2 erros e 2 avisos anteriores (o link do PLN-021 e um id 901 de fixture), sdd-process 6/0/0, studio 87 arquivos com 0 erros e 12 avisos, tools-kit 161/0/0 e workspace 73/0/0. O app `brza-studio` não lê o checador.

## Triagem

Os achados 1, 2 e 3 são para corrigir. O achado 4 e o ouro em `AGENTS.md` viram issue. O formulário foi entregue ao Anderson e a issue ainda não existe. O autor e a branch ficam neste registro como desvio de processo.

## Correção

Sessão `bc-08e5a03a-6e98-567e-bf78-a2e719541d45`, `grok-4.7`, esforço `medium`. Commit `2245460741d38a57a9677a3f5c27832114deafac`, autor `Cursor Agent <cursoragent@cursor.com>`. O PR passa a ter 8 arquivos. O commit troca a varredura para `body_of`, acrescenta 4 casos, e inclui `templates/README.md`, `templates/work/feedbacks/.gitkeep` e `tests/cli/test_brza_init.py`.

O git confirma: em `2245460`, `check_notes.py:649` lê `without_code(body_of(text))`. `check_feedback` fica com 15 `expect`, 4 a mais que `02fe2a5`. Os 15 casos de feedback passaram. A mutação de cada regra fez falhar estes casos: section-missing 3, section-order 1, model-invalid 2, effort-invalid 1 e result-invalid 2.

## Revisão R2

A mesma sessão de revisão. Veredito: aprovar, sem achados novos. As sondas foram refeitas, e o defeito volta quando a correção sai. A compatibilidade com o Studio continua idêntica nos 7 workstreams. O ouro tem 17 testes e falha nos 2 de `AGENTS.md`. `test_brza_init` tem 61 testes, com 4 falhas e 40 erros iguais na `master`, todos no mesmo parágrafo do `AGENTS.md`.

## Métricas do fluxo

Duas rodadas de revisão. Quatro achados, todos válidos. Três corrigidos. O importante, a varredura do frontmatter, o executor em `medium` não pegou. O erro do executor foi confiar na suíte verde sem sondar o caso de borda. O ajuste de rota que funcionou foi exigir a mutação no brief.

## Estado

O [PR 1](https://github.com/brz-anderson/brza-workflow/pull/1) está aberto e aguarda o merge do Anderson. O HEAD da branch é `2245460`. O P2 continua desmarcado no plano.

## Fora do workspace

- **O quê e onde:** no `brza-workflow`, o [PR 1](https://github.com/brz-anderson/brza-workflow/pull/1), branch `cursor/pln-025-feedbacks-f7d0`, commits `02fe2a5` e `2245460`, sobre `45e6013`. Oito arquivos: o checador, a norma em `core/work/README.md`, a skill, o catálogo de ouro, os testes do checador, `templates/README.md`, `templates/work/feedbacks/.gitkeep` e `tests/cli/test_brza_init.py`. **Risco:** o merge muda o checador que cada workstream copia; a comparação com `45e6013` deu o mesmo JSON nas notas reais dos 7 workstreams. **Estado:** o PR está aberto e fora da `master`. **Como desfazer:** fechar o PR sem merge. Depois de um merge, reverter `2245460` e `02fe2a5`.
