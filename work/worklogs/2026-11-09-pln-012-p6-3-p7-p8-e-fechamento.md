---
scope:
  - brza-workflow
  - brza-workspace
refs:
  - PLN-012
  - PLN-018
  - REV-024
sessions:
  - c3083ec5-dc1c-448c-84d5-73e4a3c8a0b4
---

# PLN-012: o P6.3, o P7, o P8 e o fechamento da medida por tarefa

Anderson pediu em 2026-11-09, nesta sessão: "você é o dono e coordenador do plano `PLN-012`, coordene a execução do
plano até o fechamento, se algum passo travar por pedir decisão minha, pule-o, se houverem mais passos, pare apenas
quando não houver mais oq ser executado sem depender de decisão minha". Nenhum passo travou por decisão. O
[PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou](../../plans/PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-plan.md)
fechou.

## P6.3, a conferência

Fiz a conferência com a tarefa do P6.2:
- **Seção do worklog contra o `--by-task`:** dentro de 1,9%. O `--by-task` dá US$ 5,47 e a seção US$ 5,37; a
  diferença é o resto do turno depois do commit.
- **Seção contra o transcript:** dentro de 2,8%. As esperas das quatro rodadas, lidas à mão, somam 498 s, contra os
  512 s de `requester_s`.
- **P1.4:** coberto. Nos quatro turnos da sessão, `machine.from: env` e `cpu_children_s` ≥ 2.
- **Tarefa do P6.1:** passou de 5% no custo pelo mesmo resto de turno, num turno de 8 min. Ficou registrada.

## P7, o título e a suíte isolada

- **O que o `implementer` fez:** escreveu o P7 num worktree do `brza-workflow`.
  - O `brza note commit` grava `## Custo da tarefa` (R6.1) e reconhece também `## Medida`.
  - O `NoteFixture` limpa do ambiente `BRZA_WORKSPACE`, `CLAUDE_CODE_SESSION_ID` e as outras variáveis de sessão
    (X9).
- **Revisão:** três rodadas do `reviewer`, com os achados corrigidos aqui:
  - o teste do `--chat` do `brza-run` gravava `run` no log real;
  - o corte pegava o título dentro de bloco cercado;
  - as regras de abertura e fechamento da cerca;
  - o comprimento da cerca.
  O corte por cerca ficou na nova `without_cost_section`. O C2 foi descartado: é a volta deliberada ao corte de antes
  do P7 quando uma cerca não fecha.
- **Commits:** `brza-workflow@5642ae8`, mesclado em `7afed94`, e o `brza sync` em `brza-workspace@75c88b0`.
- **Suíte com o ambiente da sessão:** 591 testes e 4 falhas, todas de `test_brza_sessions`, que já existiam. Na
  `master` eram 22; as 18 de `note` vinham do mesmo vazamento de ambiente. O log real ficou com 0 linhas `task` e
  `run` de teste. As 3 linhas `run` de teste que restavam saíram, com backup em
  `.measurements/measurements.jsonl.bak-2026-11-09-run`.

## A revisão da entrega e o P8

O `reviewer` revisou a entrega inteira e o parecer é o
[REV-024: A revisão da entrega do PLN-012, a medida por tarefa](../reviews/REV-024-pln-012-entrega.md). Os achados:
- **A1:** o `close-task` não citava `## Medida`.
- **A2:** o pid do `task` era o do `brza-note`.
- **A3:** a CPU saía fora da regra de números do D3.
- **A4:** havia restos de texto no plano.
- **Três falsos.**

Os quatro foram corrigidos no P8 (`brza-workflow@829527c`), e a segunda rodada aprovou.

O checkout principal do `brza-workflow` tinha mudanças sem commit de outra sessão, a do PLN-018, no `task_context`
do `bin/brza-note`. Por isso o merge foi num worktree destacado, sobre a `origin/master`, com push direto
(`b2b497d`, X10). O `brza sync` foi em `brza-workspace@ba60bb6`.

**Aviso à sessão do PLN-018:**
- a `master` local daquele checkout está 2 commits atrás;
- o `brza note` roda dali, e por isso o pid e a CPU novos só valem depois que ela atualizar;
- as mudanças dela vão conflitar com o P8 na linha `'pid'` do evento `task`.

O plano dela também tinha edições sem commit, e por isso o aviso ficou aqui e no X10.

## Fechamento

O plano foi para `status: done`, `phase: closed` e `completed: 2026-11-09`, com `## Documentação` e `## Fechamento`.
- **Horas:** 17,75 h estimadas, com P7 e P8 somados no caminho, contra 6,9 h executadas.
- **O que ficou para depois:** as 12 issues de `## Pendências conhecidas`.

## Fora do workspace

- **`~/Projects/brza-workflow`:**
  - os worktrees e branches `pln-012-p7`, `pln-012-p8` e `merge-p8` foram criados e removidos;
  - push na `origin/master` de `7afed94` e `b2b497d`;
  - a `master` local não foi tocada, por causa das mudanças da outra sessão.
- **`~/Projects/brza-workspace/.measurements/measurements.jsonl`:** 3 linhas `run` de teste removidas, com backup ao
  lado.

## Memória

Os subagentes gravaram na memória deles:
- **`reviewer`:** `padroes-de-erro-em-scripts-de-medicao.md` e `achados-que-costumam-cair.md`, com o `MEMORY.md`
  desduplicado;
- **`implementer`:** `brza-workflow-p7-isolamento-env.md`.

Candidato à norma: os testes que chamam o `brza note` ou o `brza-run` precisam limpar o ambiente da sessão, senão
escrevem no log real. Hoje isso está na memória e no `NoteFixture`; ainda não está na norma do `brza-workflow`.

## Custo da tarefa

Corrido 1 h 12 min — agente 1 h 6 min, quem pediu 6 min, pausa 0 s · US$ 12,83 (turnos 5,79, subagentes 7,04) · CPU 59,07 s do `claude` e 2243,55 s dos comandos, RSS até 487 MB · 4 turnos, 1 sessão · até 21:17 de 2026-11-09, pelo `brza note commit`
