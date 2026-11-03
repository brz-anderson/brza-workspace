---
scope:
  - brza-studio
  - workspace
refs:
  - PLN-007
---

# PLN-007: o BrzA Dark Theme, o tema grafite do chat

O pedido de Anderson, em 2026-11-03, na sessão do `brand`: "faça um artboard do chat com o fundo num tom mais próximo
de um grafite escuro", depois "e com o container do chat sempre no mesmo tom de quando em foco, oq muda é apenas a
borda", "implemente, como tema `BrzA Dark Theme`" e "aprovado, pode dar push".

Item novo do [PLN-007: A marca BrzA tem símbolo, logotipo e derivadas a partir da chama do app](../../plans/PLN-007-a-identidade-visual-da-marca-brza/PLN-007-plan.md),
fora da cobertura do P1 a P6.

## O que se fez

**Os artboards.** O canvas do chat sai de 5% do foreground sobre `#0a0a0a`, perto de `#161616` (`main.css:664-672`). O
artboard subiu o canvas para `#24272c`, com as fórmulas de mistura do app. A segunda versão pôs o composer sempre com o
gradiente do foco (`#373a41 → #25252b`, `main.css:495`), com a borda neutra sem foco e a da marca com foco. O botão de
enviar, que o artboard primeiro deixou laranja nos dois estados, passou a trocar do branco para o gradiente da marca com
o foco, como o app faz (`main.css:1198`).

**O tema.** O app tem dois lugares para tema: o catálogo do chat (`shared/native-chat-theme.ts`) e o tema de plugin, que
só aceita tokens públicos, entre os quais não está o preenchimento do composer. A rodada:

- "Onde mora": "Tema do chat (Recomendado)".
- "Composer": "Só no BrzA Dark Theme (Recomendado)".

Entrou no `brza-studio`, em `feat/brza-dark-theme`:

- `shared/terminal-themes/defaults.ts`: o tema `BrzA Dark Theme`, fundo `#24272c`, texto `#f0f0f0`, cursor `#f26228`.
  Tema de catálogo não mistura o foreground, e o canvas sai exatamente `#24272c`.
- `native-chat-theme-surface-style.ts` e `main.css`: só esse tema define `--chat-composer-resting-fill`, o gradiente do
  foco com o realce de 1 px no topo, e a regra `.brza-composer-focus` o pinta em repouso. A regra do foco ficou como
  estava.
- `native-chat-theme-surface-style.test.ts`, novo: o tema resolve com canvas `#24272c` e recebe o preenchimento; o
  padrão e o Dracula não.

Passaram os 3 testes novos e os de `src/shared`, `settings`, `native-chat` e `markdown-surface-theme`. Falharam 3 testes
de `wsl-host-deployment-store.test.ts`, que o diff não toca; a `master` não foi rodada para confirmar. O `tc:web` não
imprimiu erro, e os hooks do commit (`oxlint`, `oxfmt`, `ast-grep`) passaram.

Anderson abriu o app e o tema não apareceu na lista: era o app instalado em `/Applications`, build anterior ao commit.
O `pnpm dev` no worktree é o caminho.

## O que ficou

- **O tema não foi visto no app em execução.** Falta Anderson rodar `pnpm dev` no worktree e conferir, em Configurações,
  Chat, Tema escuro, "BrzA Dark Theme" em "Integrado", e o composer com o mesmo tom com e sem foco.
- O app instalado só o terá num build novo.
- O `terminalFollowsChatTheme` (ligado por padrão) faz o terminal pintar a mesma paleta; Anderson ainda não disse se quer
  isso.
- O worktree `.worktrees/brza-dark-theme` e a branch `feat/brza-dark-theme`, já contida na `master`, seguem abertos
  (`brza tree --rm brza-dark-theme`).

## Fora do workspace

No `brza-studio`, na `master`, em `50333c6ffd5` (push em `origin/master`):

- `50333c6ffd5` — `feat(brand): BrzA Dark Theme, a graphite chat theme (PLN-007)`.

O worktree `~/Projects/brza-studio/.worktrees/brza-dark-theme` foi criado pelo `brza tree`.
