---
description: O e-mail de autor dos commits troca o noreply do GitHub pelo brz.anderson.pereira@gmail.com no manifesto, no env e na norma de todos os workstreams.
scope:
  - workspace
  - brza-workflow
refs:
  - PLN-001
  - PLN-006
---

# O e-mail do autor passa ao Gmail

Em 2026-11-03, Anderson pediu a troca do e-mail de autor, nas palavras dele: `240569289+brz-anderson@users.noreply.github.com`
era o "e-mail cadastrado atualmente em todos os `workspace.toml`", e `brz.anderson.pereira@gmail.com` o "e-mail
correto, atualize em todas as referências".

## O que foi feito

- **Workspace, `master`, `0b24169`:** o `author.email` do `.brza/workspace.toml` e o `GIT_AUTHOR_EMAIL` e o
  `GIT_COMMITTER_EMAIL` do `env` do `.claude/settings.json`. Os dois são parte local, que o `brza sync` não toca.
- **Núcleo do `brza-workflow`, `c527e42`:** o `core/AGENTS.md` dizia "saem com o noreply do `{{author.login}}`" e o
  `core/CLAUDE.md`, "deve sair o noreply do `{{author.login}}`". Com um e-mail que não é noreply, a frase ficaria
  falsa, e as duas passaram a "o e-mail do". As fixtures de ouro (`tests/hooks/fixtures/golden/master/`) seguiram a
  frase e mantêm o noreply, que é o autor do teste.
- **`brza sync`, `1f56808`:** renderizou de novo o `AGENTS.md` e o `CLAUDE.md` com o e-mail novo e mesclou a `master`
  em `brand`, `playground`, `studio`, `tools-kit` e `workspace`. Os quatro arquivos de cada worktree ficaram sem
  noreply, conferidos por `grep`.

## O que ficou de fora

- **Notas que registram commits passados** seguem com o noreply, porque dizem com que e-mail aqueles commits saíram:
  `PLN-001-plan.md` (`studio`), `PLN-006-design.md` e dois worklogs de hoje (`workspace`) e um worklog do `tools-kit`.
- **Os testes do `brza-workflow` que usam o noreply de propósito**, como o `test_brza_doctor.py` e o
  `test_golden_render.py`, que proíbe `users.noreply.github.com` no molde.
- **A sessão que fez a troca** subiu com o `env` antigo; os commits dela passaram o e-mail novo à mão. Sessão nova já
  sai com ele, o que o `git var GIT_AUTHOR_IDENT` confere.

## O que rodou e o que deu

- `tests/hooks` do `brza-workflow`: 288 testes, OK. `tests/notes-checker/run.py`: ok.
- `tests/cli`: 20 falhas em `test_brza_note` e `test_brza_sessions`, de caminho e worktree. As mesmas 20 saem num
  worktree limpo da `master` do `brza-workflow` em `9f51cda`, antes da mudança: são anteriores a ela.

## Fora do workspace

- **O quê e onde:** commit `c527e42` na `master` do `brza-workflow`, com push, em `core/AGENTS.md`, `core/CLAUDE.md` e
  nas duas fixtures de ouro. **Risco:** todo workspace que rodar `brza sync` recebe a frase nova, que serve ao noreply
  e a qualquer e-mail. **Estado:** ativo. **Como desfazer:** `git revert c527e42` no `brza-workflow` e `brza sync`.
- **O quê e onde:** worktree temporário `/tmp/bw-base` do `brza-workflow`, para a rodada de comparação dos testes.
  **Risco:** nenhum. **Estado:** removido com `git worktree remove`. **Como desfazer:** nada a desfazer.
