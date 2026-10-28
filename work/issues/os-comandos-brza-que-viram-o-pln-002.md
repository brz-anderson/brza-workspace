---
status: open
scope:
  - workspace
  - brza-studio
opened: 2026-10-28
priority: medium
tags:
  - tooling
---

# Os comandos `brza` que viram o PLN-002

Em 2026-10-28, a sessão `brza-comandos-lacunas` levantou os passos manuais que se repetem entre sessões e que um
`brza <sub>` resolveria. Anderson escolheu em duas rodadas os que entram. Eles serão executados num plano, o PLN-002, com
um passo por comando. O levantamento e as respostas estão em
[Os comandos brza que faltam, levantados nas notas e nos scripts](../worklogs/2026-10-28-os-comandos-brza-que-faltam.md).

**Pendente:**
- escrever o PLN-002 pela skill `plan-runner`;
- reabrir a `brza-workspace-2d`, dona do `brza-sessions` (`711ed55`), e combinar com ela a interface do
  `list/send/close`, como Anderson escolheu: "Reabrir a 2d e combinar".

## O que entra

O despacho `brza X` → `brza-X` vem da issue
[O CLI brza manda o subcomando desconhecido ao brza-<sub> do PATH, como o git](cli-brza-manda-subcomando-desconhecido-ao-brza-x-do-path.md).
Cada script se chama `brza-<sub>` e roda sozinho, sem esperar por ele. Script novo entra no `brza-install`, que cria os
links.

| Comando | O passo manual que substitui | Onde se repetiu |
| :------ | :--------------------------- | :-------------- |
| `brza tree <nome>` / `--rm` | `git worktree add` em `brza-studio/.worktrees/` e `pnpm install --offline`. O `--rm` só remove com a branch na `origin/master` | 9 worktrees em 2 dias. O node_modules por symlink derrubou o checkout principal (worklog do ▶ e do ⤢, linhas 48-52). Dois worktrees ficaram órfãos em disco, o `conferencia-p52-p53` e o `chat-markdown-largura-e-links` |
| `brza dev` / `--stop` | Subir o dev build do worktree com `pnpm dev:seed-profile`, achar o processo e encerrá-lo | 4+ vezes. Há 6 conferências pendentes no PLN-001 |
| `brza test` | `run-vitest` e `check:changed --base=origin/master`, e a prova de que a falha já estava na master | O baseline foi refeito à mão 3 vezes, e o `--base` foi esquecido |
| `brza doctor` | Conferir à mão `git var GIT_AUTHOR_IDENT`, hook de medição, override `claude-brza`, pnpm no PATH do chat e perfil `brza-dev` | `git var` 5 vezes. A sessão aberta sem o wrapper sobe sem medição e sem aviso |
| `brza sessions list\|send\|close` | Achar a sessão, mandar mensagem e fechar chat por nome. Hoje o script só abre | 8+ vezes. O worklog da chama registra que "o CLI não fecha chat" |
| `brza note new\|commit` | O esqueleto da nota, com `## Fora do workspace` no worklog, e o commit por caminho com `pull --rebase` e `check_notes` | 10 commits de worklog e 3 issues em 2 dias |
| `brza app install` | `build:mac --dmg`, `ditto` para `/Applications` e `rm -rf dist` | 1 vez, mais a reinstalação que o despacho exige |

**Ficaram fora:**
- **`ship`:** rebase, testes e push; Anderson não o marcou.
- **`fanout` e status da Run:** a recomendação foi tirar, porque o `orca orchestration` já cobre.
- **Scripts da Fixfy:** já têm gatilho em
  [Os scripts de orquestração da Fixfy que ficaram fora do port para o BrzA](scripts-da-fixfy-fora-do-port-para-o-brza.md).

## As restrições já conhecidas

- **Nomes:** o `brza worktree` e o `brza check` colidem com comandos do CLI do app. O despacho só desvia comando
  desconhecido, por isso os nomes são `tree` e `test`.
- **`brza_runtime.py`:** é o contrato (`cli_command`, `user_data`, `runtime_file`, `brza`, `rpc`, `BrzaError`,
  `WORKSPACE`, `LOCAL_BIN`). Ele cresce sem quebrar essa interface, e os testes de `scripts/brza/tests` seguem passando.
  O aviso é da `brza-workspace-80`.
- **`close`:** fecha um chat por nome. Não usa `--resume` nem "restart" (`AGENTS.md`, "Uma tarefa, uma sessão, um
  worklog").

## Pontos para as rodadas do PLN-002

- **`tree`:**
  - abre também o chat no worktree, pelo `brza-sessions --checkout`?
  - de que base sai a branch?
  - como evita o node_modules por symlink?
- **`dev`:**
  - o seed é o padrão?
  - quantos dev builds por worktree?
  - onde fica o pid para o `--stop`?
- **`test`:** a master do baseline vem de worktree temporário ou do checkout principal?
- **`app install`:** pede confirmação antes de sobrescrever o app em `/Applications`?
- **`brza_runtime.py`:** o `canonicalize` e a impressão digital, hoje duplicados em `brza-run` e `brza-sessions`, vão
  para lá? A proposta foi feita à `brza-workspace-80`, mas não foi levada a Anderson.
- **Ordem dos passos e paralelismo:** o `dev` e o `test` usam o worktree do `tree`, e o `doctor` confere o que os outros
  instalam.
