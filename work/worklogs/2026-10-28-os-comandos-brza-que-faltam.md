---
scope:
  - workspace
  - brza-studio
---

# Os comandos brza que faltam, levantados nas notas e nos scripts

O pedido de Anderson, em 2026-10-28, na sessão `brza-comandos-lacunas`: "Levante as lacunas que poderíamos preencher ou
facilitar com scripts brza <command>: passos manuais que se repetem entre sessões e que um comando resolveria". Não
houve implementação.

## O que se fez

**O levantamento:** dois subagentes Sonnet, em paralelo e só lendo.
- **As notas:** os 8 worklogs, o PLN-001 e as 3 issues. Deram os passos manuais, com contagem e atrito.
- **Os scripts:** os de `scripts/brza/`, os da Fixfy (`~/Projects/fixfy/scripts/orca/` e o resto de `scripts/`) e os do
  `brza-studio`. Deram o catálogo e a equivalência Fixfy → brza.

Os agregados ficaram no scratch da sessão, fora do git. O resultado está em
[Os comandos brza que viram o PLN-002](../issues/os-comandos-brza-que-viram-o-pln-002.md).

**A coordenação:** o combinado com a `brza-workspace-80` foi pelo correio. O `orca orchestration send` não tem como
endereçar um chat, que não tem handle de terminal. A 80 respondeu:
- `scripts/brza/` não tem dono, e o contrato é o `brza_runtime.py`;
- o `brza-sessions` é da `brza-workspace-2d`;
- os scripts não dependem do despacho `brza X`;
- `brza worktree` colide com o CLI do app.

O `brza --help` conferido nesta sessão mostrou que o `check` também colide.

**O PATH:** o "pnpm fora do PATH" do PLN-001 (linhas 47-50) envelheceu. No chat de hoje, `which pnpm` dá
`/opt/homebrew/bin/pnpm`.

## O que Anderson respondeu

**Rodada 1:**
- **Comandos do `brza-studio`:** "Worktree + install (Recomendado), Dev build com seed (Recomendado), Testes + baseline
  (Recomendado)". O `ship` ficou fora.
- **Comandos de sessão e de workspace:** "doctor (Recomendado), sessions list/send/close (Recomendado), worklog new /
  note commit, app install".
- **Quem combina o `list/send/close` com a dona do `brza-sessions`:** "Reabrir a 2d e combinar". A recomendação era
  "Quem implementar assume".

**Rodada 2:**
- **Nome do comando de worktree:** "brza tree (Recomendado)".
- **Nome do comando de testes:** "brza test (Recomendado)".
- **Notas:** "brza note new|commit (Recomendado)".
- **Execução:** "PLN-002, um passo por comando (Recomendado)".

## O que ficou

O pendente está na issue
[Os comandos brza que viram o PLN-002](../issues/os-comandos-brza-que-viram-o-pln-002.md):
- escrever o PLN-002;
- reabrir a `brza-workspace-2d`;
- os pontos de desenho de cada comando, para as rodadas do plano.
