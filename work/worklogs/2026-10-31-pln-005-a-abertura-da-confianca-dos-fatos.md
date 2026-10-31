---
scope:
  - workspace
---

# PLN-005: a abertura da confiança dos fatos do desenho

Anderson pediu, na sessão `workspace`, "um mecanismo de medir tbm a confiança dos fatos coletados das sugestões de
desenho". A sessão levantou o que já existe e abriu
[PLN-005: A confiança dos fatos do desenho se mede contra o que se sustentou](../../plans/PLN-005-a-confianca-dos-fatos-do-desenho/PLN-005-plan.md).

## O que se levantou

- Só o `reviewer` dá confiança em número; o `designer` e o `collector` dão a fonte, e ninguém confere depois se o fato
  se sustentou.
- O evento `subagent` não guarda a devolução, mas o transcript do subagente está ao alcance do hook.
- Volume até hoje: 5 devoluções do `designer` (média de US$ 1,79) e 6 do `collector` (US$ 1,71).

## O que se decidiu

Três rodadas, gravadas na Entrevista do plano:
- **R1:** levam a marca os fatos do `designer`, os do `collector` e os custos das opções; a marca é número e tipo
  (`[F3 · lido · 90]`); um Haiku audita e a sessão registra o resto.
- **R2:** o hook dispara a auditoria em segundo plano; o desfecho vai por `scripts/fact_outcome.py`; o trabalho anda
  por PLN.
- **R3:** o disparo mora num `fact_audit.py` separado do `measure.py`; o parser lê a devolução e os arquivos gravados;
  o `close-task` lista os pendentes.

O Desenho (D1–D6) e os Passos (P1–P9, 9 h) foram escritos e esperam o aceite, na R4.

## Na master

- `2e8ea67` — "Último PLN usado" passa a 005 no `plans/README.md`.
