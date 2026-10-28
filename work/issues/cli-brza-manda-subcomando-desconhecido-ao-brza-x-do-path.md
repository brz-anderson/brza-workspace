---
status: done
scope:
  - brza-studio
opened: 2026-10-28
completed: 2026-10-28
priority: medium
tags:
  - tooling
---

# O CLI `brza` manda o subcomando desconhecido ao `brza-<sub>` do PATH, como o git

**Resolvida em 2026-10-28** pelo `9a81e65c852` do `brza-studio`, em
[O CLI brza despacha o subcomando desconhecido ao brza-X do PATH](../worklogs/2026-10-28-o-cli-brza-despacha-ao-brza-x-do-path.md).
Por resposta de Anderson, a reinstalação do app e a troca dos textos para `brza install` e `brza run` ficaram para o
`brza app install` do PLN-002.

## O pedido

Anderson pediu na sessão `brza-workspace-2d`, em 2026-10-28, que repassou o pedido pelo correio do Orca: "tudo sob a tag `brza` sem
kebab-case, `brza sessions`". A rodada desta sessão (`brza-workspace-80`), no mesmo dia, perguntou: "Como o
`brza sessions`, o `brza run` e o `brza install` chegam ao CLI `brza`?". A resposta foi "No CLI do app, como no git
(Recomendado)".

Das alternativas, ficaram de fora:
- **Um despachante `brza` em `~/.local/bin`:** perderia no chat, porque lá o PATH traz o
  `/Applications/BrzA Studio.app/Contents/Resources/bin` antes do `~/.local/bin`. No zsh de login, a ordem é a inversa.
- **Manter os nomes `brza-*`:** não atende ao pedido.

## O desenho escolhido

O `brza X …` que o CLI não conhece executa o `brza-X` do PATH, com os argumentos restantes, o stdin, o stdout e o
código de saída intactos, como o `git X` acha o `git-X`. Os scripts de `scripts/brza/` do `brza-workspace` mantêm o nome
dos arquivos: o `brza sessions` acha o `brza-sessions`, o `brza run` acha o `brza-run` e o `brza install` acha o
`brza-install`. O `claude-brza` fica de fora, porque é o `agentCmdOverrides.claude` e ninguém o digita.

Hoje, o comando desconhecido para em dois lugares do `brza-studio`:
- `src/cli/args.ts:256`, no `validateCommandAndFlags`, que lança `Unknown command` antes do despacho;
- `src/cli/dispatch.ts:40`, no `dispatch`.

O desvio entra antes da validação, só para o primeiro termo do caminho e só quando nenhum comando conhecido o começa.
Assim, o `brza terminal foo` segue como erro do CLI.

## O que conferir na sessão que fizer

- **Um teste de unidade:** subcomando externo achado e executado, não achado (o `Unknown command` de hoje) e comando
  conhecido sem desvio.
- **O build local e a reinstalação do app**, com `brza sessions --help` respondendo do chat e do terminal.
- **Um laço:** o `brza-X` que chama o `brza` não pode cair de volta no desvio.
- **Depois do build:** a ajuda do `brza-install` e do `brza-run` e o `CLAUDE.md` passam a citar `brza install` e
  `brza run`.
