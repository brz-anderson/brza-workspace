---
scope:
  - workspace
refs:
  - PLN-011
  - PLN-014
  - PLN-022
sessions:
  - 5da0b8ae-2af2-4f10-b92c-9614895e55c1
---

# Entrevista do SDD: a rodada 1 decide onde a spec mora

Abertura do [PLN-022: O trabalho do workspace segue Spec Driven Development](../../plans/PLN-022-spec-driven-development/PLN-022-plan.md) e a rodada 1 da entrevista.

## O que se fez

- Leu a norma e os bloqueios em vigor (`PLN-014` e `PLN-011`, sem relação com SDD). Não havia nota sobre SDD.
- Levantou o SDD do `fixfy_flutter`: a regra é `SPEC.md` na raiz da feature ou do pacote, mas só há 3 `spec.md` em `features/`, ainda fora da norma de autoria. Nenhuma lib de `packages/` tem spec.
- Abriu o PLN-022 e gravou a rodada 1.

## O que se decidiu

- **R1.1:** a spec mora junto do que especifica, no repositório dono; o plano a cita pelo ID. A proposta inicial, `PLN-NNN-spec.md` na pasta do plano, caiu.
- **R1.2:** entram a ordem das etapas com o gate e a skill `spec-writer`; fica de fora a autoria por seção.
- **R1.3:** `origin: request`.

## Pendente

- Rodada 2: critérios de aceite, fora de escopo, convivência com `Cobertura`, rodadas e `notes-checker`. Está no `Retomar` do plano.

## Custo da tarefa

Corrido 10 min — agente 2 min, quem pediu 8 min, pausa 0 s · US$ 0,74 (turnos 0,74, subagentes 0,00) · CPU 8 s do `claude` e 10 s dos comandos, RSS até 446 MB · 3 turnos, 1 sessão · até 00:14 de 2026-11-10, pelo `brza note commit`
