---
scope:
  - brza-workspace
  - brza-workflow
refs:
  - PLN-012
  - REV-021
sessions:
  - c3083ec5-dc1c-448c-84d5-73e4a3c8a0b4
---

# PLN-012: o P6.2, a pasta solta na master e o brza run que perdia as aspas

A tarefa real que o P6.2 do
[PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou](../../plans/PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-plan.md)
mede, escolhida na rodada do P6.1: "A master atrasada (Recomendado)". Começou no turno "siga", depois do marco do
[PLN-012: o P6.1, o brza sync que instala a medida por tarefa](2026-11-09-pln-012-p6-1-brza-sync.md).

## A pasta solta

- O atraso do checkout da `master` do workspace já tinha sumido: o `brza sync` do P6.1 o atualizou.
- A pasta `~/Projects/brza-workspace/brza-workspace/` era um clone do próprio workspace, de 2026-11-04 00:03
  (`git reflog`: `clone: from https://github.com/brz-anderson/brza-workspace`), limpo, com os 45 arquivos rastreados
  presentes byte a byte como blobs no git do workspace, sem commit local nem stash. O `collector` não achou quem o fez:
  nem a medição nem os transcripts registram o comando.
- Rodada: "Apagar (Recomendado)". Apagada; o `git status` da `master` ficou limpo.

## O brza run

- O primeiro `brza run -- bash -c '…'` rodou partido: o `brza-run` juntava os argumentos com espaço e rodava a
  linha no `zsh -ic`, e o `bash -c` ficou só com o `cd`. Rodada: "Consertar aqui".
- O conserto mostrou que juntar "como no ssh" era o contrato documentado (`brza-run:15`) e testado. Rodada:
  "Trocar o contrato (Recomendado)". Um argumento só segue como linha de shell, e vários chegam inteiros.
- Revisão pelo `reviewer` interno, em três rodadas. O `agy` da memória do workstream ficou de fora porque a aprovação
  automática já o barrara hoje (REV-021). Os achados:
  - A1: o argumento que começa com `=` era expandido pelo zsh, ou abortava a linha e prendia a aba.
  - A2: o `--chat` do `main()` estava sem teste.
  - A3: o `inner` da aba estava sem teste.
  Os três foram corrigidos aqui, cada um com a mutação que o teste barra.
- `brza-workflow@b12fec4`, mesclado em `ffa29fe` e enviado, com 46 testes do `brza-run` OK. A chamada original,
  repetida, rodou inteira dentro do `bash -c`.

## A suíte de CLI e o log de medição

- A suíte `tests/cli` da `master` (`db6bd28`) já tinha 22 falhas, todas de `note` e `sessions`, nenhuma do
  `brza-run`. Sem as variáveis desta sessão no ambiente, foram 25 falhas e 1 erro. Não investiguei.
- Rodada dentro desta sessão, a suíte gravou no `.measurements/measurements.jsonl` real 56 eventos `task` com o
  `session_id` desta sessão e 28 da sessão `508e76c8`. Os testes do `brza note commit` herdam `BRZA_WORKSPACE` e
  `CLAUDE_CODE_SESSION_ID`. Os marcos falsos partiram esta tarefa, e o `--pending` mostrava só o último turno.
- Rodada: "Remover, com backup (Recomendado)" e "Corrigir no P7 (Recomendado)". O backup foi para
  `.measurements/measurements.jsonl.bak-2026-11-09`. Saíram 84 linhas `task`: 48 com `cwd` no temp do macOS e 36
  com `cwd` no `brza-workflow`, estas por fixture de worklog que nenhuma sessão commitou de lá. O critério do `cwd` no
  `brza-workflow` foi além da letra da opção, que falava só do temp, e está dito aqui. Depois disso, o `--pending`
  deu "2 turnos desde 19:06 (corrido 36 min, US$ 2,33 dos turnos e US$ 1,79 de 4 subagentes)".

## O título da seção

Anderson pediu no meio da tarefa: "precisamos de um nome que descreva melhor o intuito da seção `# Medida`". A
rodada R6 do PLN-012 respondeu "Custo da tarefa" e "P7 do PLN-012, depois desta tarefa (Recomendado)". O D3 foi
reescrito, e o P7 entrou no plano com o conserto do X9.

## Fora do workspace

- `~/Projects/brza-workspace/brza-workspace/`, o clone solto, apagado com `rm -rf`.
- `~/Projects/brza-workflow`: o worktree `.worktrees/fix-brza-run-argv` e a branch `fix/brza-run-argv` criados e
  removidos depois do merge. O `~/.local/bin/brza-run` aponta para o checkout da `master`, e o conserto passou a valer
  no merge.
- `~/Projects/brza-workspace/.measurements/measurements.jsonl`: 84 linhas `task` de teste removidas, com o backup ao
  lado.

## Memória

O `reviewer` gravou `padroes-de-erro-em-scripts-do-cliente.md` (novo) e editou `achados-que-costumam-cair.md` e o
`MEMORY.md` dele.

## Medida

Corrido 42 min — agente 33 min, quem pediu 9 min, pausa 0 s · US$ 5,37 (turnos 3,58, subagentes 1,79) · CPU 27,94 s do `claude` e 1089,43 s dos comandos, RSS até 459 MB · 3 turnos, 1 sessão · `brza run`: 3 comandos, CPU 0 s, pico 7 MB · até 19:48 de 2026-11-09, pelo `brza note commit`
