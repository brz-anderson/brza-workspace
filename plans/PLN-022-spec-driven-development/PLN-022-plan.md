---
status: open
phase: interview
origin: request
description: O SDD vira o processo de especificar antes de planejar e executar, com a spec no repositório dono.
ready: "não — a entrevista segue (rodada 3: critérios de aceite)"
scope:
  - workspace
opened: 2026-11-10
owner: Anderson
---

# PLN-022: O trabalho do workspace segue Spec Driven Development

- **Retomar:** as rodadas 1 e 2 fecharam; falta a rodada 3 (critérios de aceite da Cobertura e como o `specs:` convive com `Cobertura` e com as rodadas), antes de qualquer Desenho.

## Pedido

- **Origem:** pedido livre, na sessão `sdd-process` de 2026-11-10

> "Implementar o processo Spec Driven Development (SDD) neste workspace." Referência de Anderson: no outro projeto, o `fixfy_flutter` é o único que chegou a implementar o SDD, e a `SPEC.md` fica na raiz da feature ou do pacote, e não no plano.

### Cobertura

A preencher depois da rodada 3.

### Fora de escopo

- **A migração das specs que já existem em outros repositórios.** Entra quando um repositório pedir (R2.3).
- **A sincronização visual, a 4ª etapa do Fixfy.** Só vale para app com design system de tokens; entra quando o `brza-studio` adotar um (R2.3).
- **A autoria e a revisão por seção** (`Autoria`, `Revisor`, `Revisado`). Fica de fora pela R1.2.

## Entrevista

### Rodada 1 — onde mora o SDD e quanto dele entra (enviada e respondida 2026-11-10, sessão `sdd-process`)

**Apresentado antes:** não há plano nem nota sobre SDD no acervo. O levantamento do SDD do `fixfy_flutter` mostrou: a regra é `SPEC.md` na raiz da feature ou do pacote (`CONSTITUTION.md` §0), mas só existem 3 `spec.md` em `features/`, ainda fora da norma de autoria (ADR-015, MIG-015 pendente); nenhuma lib de `packages/` tem spec. O processo tem quatro etapas (especificação, contratos, implementação, sincronização visual), gate de PR e a skill `spec-writer` com a operação Conferir. O card é a fonte do requisito, e a spec o referencia sem transcrever. A recomendação inicial, `PLN-NNN-spec.md` na pasta do plano, caiu: a spec presa ao plano morre com ele.

1. **R1.1 — Onde a spec mora e o que ela especifica.**
   - A spec mora junto do que especifica, no repositório dono; o plano a cita pelo ID — custo: o processo se espalha por 2 ou 3 repositórios e o `notes-checker` precisa achar a spec fora de `plans/`; se paga: na primeira revisão depois que a coisa muda, porque a spec não morre com o plano.
   - Gênero próprio em `work/specs/` — custo: pasta nova e regra no checador; se paga: só se a mesma spec servir a mais de um repositório.
   - A spec dentro do plano — custo: o menor; se paga: agora, mas fecha com o plano.

   **Decidido — a spec mora junto do que especifica, no repositório dono**, e o plano a cita pelo ID. Resposta: "1.1.1".

2. **R1.2 — Quanto da maquinaria do Fixfy entra** (múltipla).
   - Só a ordem das etapas e o gate — custo: um parágrafo de norma e uma checagem no checador; se paga: no primeiro plano de código.
   - Autoria e revisão por seção — custo: alto, e o reset de `Revisado` depende de disciplina; se paga: nunca, com Anderson como único autor e revisor.
   - Uma skill `spec-writer` — custo: escrever e manter a skill; se paga: depois da primeira spec feita à mão.

   **Decidido — a ordem das etapas com o gate, e a skill `spec-writer`.** Fica de fora a autoria por seção. Resposta: "1.2 1 e 3".

3. **R1.3 — Origem do pedido.**
   - `origin: request` — custo: nenhum; se paga: agora.
   - Decisão ou issue existente.

   **Decidido — `origin: request`.** Resposta: "1.3.1".

### Rodada 2 — gate, primeira spec e fronteiras (enviada e respondida 2026-11-10, sessão `sdd-process`)

**Apresentado antes:** inferência da R1.1 — com a spec fora de `plans/`, o plano aponta para ela, e os critérios de aceite vivem na spec, sem cópia no plano.

1. **R2.1 — Quem barra o passo de código sem spec.**
   - O `notes-checker` barra o plano com passo de código sem spec citada, pelo frontmatter — custo: uma regra no checador, que lê outro repositório; se paga: no primeiro plano de código.
   - Só a norma, a `plan-runner` conferindo ao planejar — custo: o menor; se paga: agora, mas nada impede o esquecimento.

   **Decidido — o `notes-checker` barra, e o campo do frontmatter é `specs:`, uma lista**, porque um plano pode ter várias specs. Resposta: "1.2.1 mas deve ser `specs:` que espera uma lista, um plano pode ter várias specs" (lida como R2.1, opção 1).

2. **R2.2 — Onde a primeira spec nasce.**
   - Na própria skill `spec-writer` deste workstream, como piloto — custo: o primeiro uso da norma é sobre ela mesma; se paga: na própria entrega.
   - Numa feature real do `brza-studio` — custo: abre sessão e branch no app; se paga: quando houver feature de código.

   **Decidido — a skill `spec-writer`, como piloto.** Resposta: "restante recomendado".

3. **R2.3 — Fora de escopo agora** (múltipla): a migração das specs de outros repositórios; a sincronização visual (4ª etapa do Fixfy).

   **Decidido — os dois ficam de fora**, com a autoria por seção da R1.2. Resposta: "restante recomendado".

## Worklogs

- 2026-11-10 — R1 e R2 fechadas; plano aberto. Parou antes da R3.
  [Entrevista do SDD: a rodada 1 decide onde a spec mora](../../work/worklogs/2026-11-10-sdd-entrevista-rodada-1.md)
