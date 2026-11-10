---
status: open
phase: interview
origin: request
description: O SDD vira o processo de especificar antes de planejar e executar, com a spec no repositório dono.
ready: "não — a entrevista segue (rodada 2: critério de aceite e fora de escopo)"
scope:
  - workspace
opened: 2026-11-10
owner: Anderson
---

# PLN-022: O trabalho do workspace segue Spec Driven Development

- **Retomar:** a rodada 1 fechou; falta a rodada 2 (critérios de aceite, fora de escopo, convivência com `Cobertura`, rodadas e `notes-checker`), antes de qualquer Desenho.

## Pedido

- **Origem:** pedido livre, na sessão `sdd-process` de 2026-11-10

> "Implementar o processo Spec Driven Development (SDD) neste workspace." Referência de Anderson: no outro projeto, o `fixfy_flutter` é o único que chegou a implementar o SDD, e a `SPEC.md` fica na raiz da feature ou do pacote, e não no plano.

### Cobertura

A preencher depois da rodada 2.

### Fora de escopo

A preencher depois da rodada 2.

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

## Worklogs

- 2026-11-10 — R1 fechada; plano aberto. Parou antes da R2.
  [Entrevista do SDD: a rodada 1 decide onde a spec mora](../../work/worklogs/2026-11-10-sdd-entrevista-rodada-1.md)
