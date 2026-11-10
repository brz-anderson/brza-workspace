---
scope:
  - workspace
tags:
  - tooling
  - planning
refs:
  - PLN-021
sessions:
  - 31cf964e-5b71-41bf-b845-36e86d01f0d7
---

# A entrevista do PLN-021: o plan-runner com sessão coordenadora e a skill de artboards

## O que se fez

- **O pedido virou o [PLN-021: O plano roda por uma sessão coordenadora, com scripts de apoio e artboards de tela](../../plans/PLN-021-o-plano-coordenado-e-os-artboards/PLN-021-plan.md)**,
  aberto pelo `brza note plan-open`, com o pedido citado, a Cobertura em rascunho e as restrições.
- **O Terreno saiu de um `collector`**:
  - **Reaproveitável da `meeting-runner`:** o `sessions_map.py` inteiro; os verbos do `brza sessions`, a medição por
    janela e o `salva_visual`, que estão misturados ao manifesto de reunião.
  - **O que falta no `check_notes.py`:** ele não confere horas, IDs nem `[x]` com evidência.
  - **Artboards:** não há molde de tela nem moldura de aparelho; os tokens do `brza-studio` estão no `main.css` e no
    `mobile-theme.ts`.
  - **O agregado** ficou no scratch da sessão (`/private/tmp/pln021/terreno.md`), fora do git.
- **O `brza sync` lê só a master** (`brza-workflow/bin/brza-sync:8-13`). Editar o `plan-runner` na branch do
  playground não o trava; o risco é conflito no `brza note sync`.
- **O Desenho de D1 a D7 foi pedido a um `designer`**, com o rascunho no scratch.

## O que se decidiu

As rodadas estão inteiras no plano, com as opções e o custo de cada uma.

- **R1:** PLN novo no playground; a sessão coordenadora abre os executores dos passos, os consultores do Desenho em
  sessões e o painel de andamento; os artboards vão a uma skill própria.
- **R2.1, em texto livre:** "pasta script/ em .claude/; e não é pra mudar o nome da skill, continua sendo
  `plan-runner`". Reabriu a R1.2, que tinha escolhido uma skill nova `plan-coordinator`.
- **R2.2 a R2.4:** os quatro scripts (`plan_state.py`, `step_request.py`, `round_log.py`, `close_check.py`); consultores
  em sessão só em decisão cara; um pacote de tokens por projeto.
- **R3:** o `plan-runner` mantém o nome e muda só na branch `workstream/playground`; o código comum fica em
  `.claude/scripts/` nesta branch; a `meeting-runner` passa a importar de lá neste plano.

## Para a norma

- **A R3.1 é um desvio declarado:** uma skill do `core.lock` editada na branch de um workstream. Não está escrito na
  norma como o `brza note sync` trata o conflito de merge que isso pode gerar. Fica para a promoção, que é quando o
  desvio se desfaz.

## Custo da tarefa

Corrido 16 min — agente 6 min, quem pediu 9 min, pausa 0 s · US$ 2,86 (turnos 2,28, subagentes 0,58) · CPU 18 s do `claude` e 2 min dos comandos, RSS até 478 MB · 2 turnos, 1 sessão · até 23:36 de 2026-11-09, pelo `brza note commit`
