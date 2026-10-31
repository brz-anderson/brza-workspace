---
scope:
  - workspace
---

# O checkout relativo do brza sessions

O pedido veio da sessão do workstream `workspace`, em 2026-10-31. Anderson decidiu lá, com a resposta literal "2. 1",
a opção "O `brza sessions` resolve o `--checkout` relativo a partir da raiz do `brza-workspace`, pedido ao
`tools-kit`". Um `--checkout` relativo passa a ser resolvido a partir da raiz do `brza-workspace`, e não do cwd. O
absoluto continua valendo igual.

O caso que falhou: rodado em `.worktrees/workspace`,
`brza sessions tools-kit-shot-736 ... --checkout .worktrees/tools-kit` montou
`path:/Users/andepb/Projects/brza-workspace/.worktrees/workspace/.worktrees/tools-kit`, e o app devolveu
`selector_not_found`. O `--checkout` passava por `Path.resolve()`, que parte do cwd.

## O que se fez

- **`d4c4543` na `master`:**
  `fix(brza): o --checkout relativo do brza sessions parte da raiz do brza-workspace`.
  - **`scripts/brza/brza-sessions`** ganhou o `workspace_root()` e o `resolve_checkout()`. A raiz é a pasta acima do
    `git --git-common-dir` do cwd quando esse repositório traz o `scripts/brza/brza-sessions`, ou seja, quando é um
    checkout do `brza-workspace`. No `brza-studio`, ou fora de um repositório, vale a `WORKSPACE`: a `BRZA_WORKSPACE`,
    ou o `~/Projects/brza-workspace` sem ela. O absoluto só passa pelo `expanduser` e pelo `resolve`, como antes.
  - **A ajuda** do `--checkout` e o uso no docstring dizem que o relativo parte da raiz do `brza-workspace`.
  - **Os testes**, no `test_brza_sessions.py`, rodam sobre um repositório git temporário com o worktree
    `.worktrees/workspace`:
    - o relativo, rodado de dentro do worktree, lança com `path:<raiz>/.worktrees/tools-kit` e grava esse caminho no
      mapa;
    - o relativo, rodado fora de um repositório, parte da `WORKSPACE`;
    - o absoluto, rodado de dentro do worktree, fica como veio.
- **A norma** não mudou: o `CLAUDE.md` já manda `--checkout .worktrees/<nome>`.
- **O merge da `master`** entrou só no `tools-kit`, sem o `brza note sync`, para não mexer no worktree do
  `workspace` com a sessão de lá trabalhando.

## A conferência

- **O primeiro teste falha com a resolução antiga**, trocada de volta por `c.expanduser().resolve()`, e passa com a
  nova.
- **A suíte** `python3 -m unittest discover -s scripts/brza/tests` deu `Ran 259 tests … OK` na `master`.
- **Um dry-run real em `.worktrees/workspace`**,
  `brza-sessions prova-736 --checkout .worktrees/tools-kit --dry-run`, mostrou
  `(chat, /Users/andepb/Projects/brza-workspace/.worktrees/tools-kit)`.
