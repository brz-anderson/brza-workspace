---
scope:
  - brza-studio
  - brza-workspace
tags:
  - norma
  - testes
sessions:
  - 9a8a3486-4242-4988-877a-d72abe0b9404
---

# A suíte completa do brza-studio passou a rodar só na CI do GitHub

O pedido de Anderson, em 2026-11-11: "oq é esse processo `bun.exe` que está comendo nossa RAM". Eram 15 processos
`bun.exe`, somando 3,5 GB, de um `pnpm test` com a suíte inteira. A sessão `studio-dd` (`5f596faf`) tinha disparado
esse teste 23 min antes, no worktree `brza-studio/.worktrees/sync-v1.4.256`, durante o sync da v1.4.256. O `bun.exe` é
o binário do pacote npm `bun`, o runtime em que o vitest do `brza-studio` roda.

## O que se fez

- **A suíte foi encerrada**, a pedido de Anderson ("encerre, avise a outra sessão e crie uma norma que suite a completa
  só se roda na CI no GitHub"). O `kill -INT` no `run-vitest.mjs` não levou os workers junto, e eles ficaram órfãos;
  saíram com `pkill -TERM` no padrão do `bun.exe` do vitest.
- **A `studio-dd` recebeu o aviso por correio:** não rodar a suíte de novo na máquina, só o alvo.
- **A CI do fork foi conferida antes da norma:**
  - o `pr.yml` só dispara em `pull_request`, e nenhuma execução dele aparece no fork, porque o push vai direto à
    `master`;
  - o `node-next-compat.yml` ("Scheduled x86 unit compatibility") roda a suíte unitária em `ubuntu-24.04` todo dia e
    aceita `workflow_dispatch`, em cerca de 15 min. As 4 últimas execuções falharam nos shards 1 e 11 de 12, o
    vermelho que veio do upstream;
  - o fork não traz as tags do upstream; só a `v1.4.251-alpha.1` está lá.
- **A norma ganhou a seção "A suíte completa do `brza-studio` só roda na CI do GitHub"** em `.claude/rules/workspace.md`,
  no commit `ad366f2` da `master`, e chegou aos workstreams pelo `brza note sync`.
- **As memórias foram ajustadas:**
  - a `suite-completa-uma-vez-no-merge` saiu, porque a regra subiu à norma. A `studio-dd` já a tinha reescrito para
    "só na CI", com a nota de que ela sairia quando a norma chegasse;
  - a `upstream-sync-procedure` passou a pedir a linha de base e a suíte depois dos consertos pela CI. O "Uma suíte de
    cada vez" saiu, e as lições da v1.4.256 que a `studio-dd` acrescentou ficaram;
  - a `oxfmt-oxlint-no-worktree` deixou de apontar a memória apagada.

## O que se decidiu

A rodada, com as respostas de Anderson:
- Gatilho da CI: "Disparo manual (Recomendado)" — `gh workflow run node-next-compat.yml --ref <branch>`, sem mudar
  arquivo do upstream.
- Onde mora: "`.claude/rules/workspace.md` (Recomendado)".
- As memórias: "Apagar e ajustar (Recomendado)".
- O texto da norma: aprovado como estava ("1").

A regra substitui a da memória de 2026-11-02, que mandava a sessão de coordenação rodar a suíte uma vez na máquina, no
merge.

## Fora do workspace

- **O quê e onde:** `kill -INT 57126` e `pkill -TERM` dos `bun.exe` do vitest no worktree `sync-v1.4.256` do
  `brza-studio`. **O risco:** o sync da `studio-dd` ficou sem o resultado da suíte; ela foi avisada.
  **Estado:** encerrado. **Como desfazer:** a suíte roda de novo na CI, pelo `node-next-compat.yml`.

## Custo da tarefa

Corrido 10 min — agente 5 min, quem pediu 5 min, pausa 0 s · US$ 1,46 (turnos 1,46, subagentes 0,00) · CPU 12 s do `claude` e 10 s dos comandos, RSS até 370 MB · 3 turnos, 1 sessão · até 20:24 de 2026-11-11, pelo `brza note commit`
