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

## A captura (P3)

O `implementer` fez o modo `stop` do `fact_audit.py`, com 24 testes. O teste num transcript real do `designer` mostrou
que a devolução não é texto: chega pelo `SubagentHandback`, e a especificação da sessão dizia o contrário (X1). O
`implementer` corrigiu, e a R5 fechou as três escolhas que ele fez sem a especificação fixar, todas na recomendada.

## A auditoria em segundo plano (P4)

A R6 decidiu que a citação errada de um fato verdadeiro sai `holds` com `cite: off`. O `implementer` fez o `run`, o
disparo no fim do `stop`, a marca no `turn` da sessão `-p` e a entrada no `settings.json`, com 22 testes; a R7 fechou
as três escolhas dele, e a sessão aplicou a da cerca. Desde o `3e123f0`, toda devolução do `designer` e do
`collector` com fato `rodado`, `lido` ou `doc` dispara a auditoria.

## O desfecho da sessão (P5)

O `implementer` fez o `scripts/fact_outcome.py`, com 28 testes: registrar o desfecho, `--pending` e `--list`. O
desfecho leva o `workstream` do fato, e não o do cwd (X2), porque chega em outra sessão. A R8 fechou duas escolhas dele,
ambas na recomendada.

## O resumo, a norma e a primeira auditoria real (P6, P7, P8, P10)

A R9 separou fato de custo no `--facts`, e o `implementer` fez o resumo com 25 testes; a sessão gravou a norma — o
`close-task`, o `CLAUDE.md` e o `README.md`. A prova do P8 veio sozinha: um `collector` do `studio` devolveu 25 fatos
marcados, e a auditoria conferiu 24 em 92 s, por US$ 0,157 — 21 `holds`, 3 `unknown`, 4 `cite: off`. A primeira
leitura é de humildade, não de excesso: a faixa 90+ do `lido` acertou 17 de 17, com distância de -7,2.

O mesmo `collector` escreveu 10 marcas fora da forma, e 7 fatos se perderam. A R10 decidiu o parser tolerante e a regra
mais clara nos papéis (P10), o teto da auditoria por fato, a dica dos pendentes com `--workstream all` e o erro de uso
do `--facts` com outro flag. Com a expressão nova, o transcript real dá F1–F28, sem malformada.

## Na master

- `2e8ea67` — "Último PLN usado" passa a 005 no `plans/README.md`.
- `68a925c` — a marca de confiança no `designer.md` e no `collector.md` (P2).
- `8d22660` — o `fact_audit.py stop` e os testes (P3).
- `3e123f0` — o `fact_audit.py run`, o `turn` marcado, o resumo e o `settings.json` (P4).
- `98a60d3` — o `fact_outcome.py` e os testes (P5).
- `72f684a` — o `--facts` do resumo (P6).
- `4c92097` — a auditoria no `CLAUDE.md`, no `README.md` e no `close-task` (P7).
- `b3e3efd` — a premissa fora da marca e o resumo que cita só o id, nos papéis (R10.1).
- `13a291a` — a marca tolerante e o teto por fato (P10).
