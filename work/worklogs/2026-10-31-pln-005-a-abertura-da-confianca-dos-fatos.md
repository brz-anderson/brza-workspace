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

O Desenho (D1–D6) e os Passos (P1–P9, 9 h) foram escritos e aceitos na R4 ("1"). A execução começa pelo P1, a pedido.

## A sonda do P1

O `claude -p` em Haiku 5.5 auditou três fatos de fixture em 9,6 s, por US$ 0,0056, e acertou os três vereditos: dois
`holds` e o `fails` plantado. Os hooks do projeto rodam na sessão `-p` e enxergam o `BRZA_FACT_AUDIT`, e o
`--max-budget-usd` corta com saída 1. O D2 ficou como estava. A sonda achou ainda uma citação errada do próprio plano,
`measure.py:22` no lugar da linha 23, que o Terreno corrigiu.

## A marca nos papéis (P2)

A régua ficou no `designer.md` e no `collector.md`, sem subir ao `AGENTS.md`, que carrega em toda sessão. A marca vai
logo depois do que afirma, porque o custo e o "se paga" de uma opção dividem a mesma linha.

## Na master

- `2e8ea67` — "Último PLN usado" passa a 005 no `plans/README.md`.
- `68a925c` — a marca de confiança no `designer.md` e no `collector.md` (P2).
