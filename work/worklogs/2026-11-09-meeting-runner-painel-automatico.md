---
scope:
  - workspace
tags:
  - tooling
refs:
  - PLN-017
sessions:
  - f497c2b6-20bf-4786-8d30-73c4cec86d58
---

# meeting-runner: o painel de cada rodada e a síntese saem do script, não da memória

Anderson pediu, depois da reunião "tev1 nos fluxos": "esses artboards deveriam estar sendo gerados ao final de toda
rodada, mas não está acontecendo, temos que corrigir a skill nesse sentido". A revisão foi pela `skill-creator`, como
toda skill deste workstream.

## O que faltou na reunião

Cada publicação do painel dependia de quatro passos manuais (`sintese-N.json`, `panel.py collect`, `panel.py render`,
o PNG), e o `wait_round.py` não chamava o painel. Saíram a abertura da R1 e da R2 e o fechamento da R1 à R4; faltaram as
aberturas da R3 à R5, todas as chegadas, o fechamento da R5 e o visual de síntese, que só saíram a pedido. A regra
estava escrita em `references/narration.md`.

Ao regenerar o painel da R5 apareceu outro defeito: o `brza note commit` gravou `## Custo da tarefa` (o custo da
coordenação) depois do marcador `<!-- fim-rodada-5 -->` nos seis worklogs de persona, e o `tally.py` passou a lê-las
como "atrasado".

## A rodada

Gravada no [PLN-017: A reunião multiagente com personas roda como fluxo replicável: skill, `brza sessions` e painel no chat](../../plans/PLN-017-a-reuniao-multiagente-como-fluxo-replicavel/PLN-017-plan.md),
como Rodada 10, as quatro respondidas na recomendada: "wait_round.py gera sozinho (Recomendado)"; "panel.py gera, passo
do encerramento (Recomendado)"; "Só na abertura e no fechamento (Recomendado)" para o PNG; "tally tolera + issue ao
tools-kit (Recomendado)".

## O que mudou

- **`wait_round.py`:** gera o painel em processo na abertura, a cada lote de chegadas e no fim, e imprime a linha
  `::orca-visual` abaixo da narração; PNG só na abertura e no fim, em `<pasta da reunião>/painel-rN.png`; `--publish-dir`
  (padrão `$ORCA_CHAT_SCRATCH_DIR`) e `--no-panel`; falha do painel vira `⚠ painel:` e não muda o rc; a janela vai em ISO
  com fuso; no fim, a linha `janela: --opened … --closed …` para o `publish` depois da síntese.
- **`panel.py`:** `publish N` (collect, render e PNG num comando) e `sintese` (o visual da reunião inteira, com o
  `sintese-final.json` opcional; o esquema está no docstring), os dois publicando no scratch do chat e com PNG por padrão.
- **`common.py`:** o `corta_medida` corta o bloco final `## Custo da tarefa` depois do último marcador, e só ele; o
  `tally.py` e o aviso do `wait_round.py` herdam a regra.
- **Texto:** o `SKILL.md` (os comandos, o Passo 3, o Passo 5, o fechamento, a narração), o `references/narration.md`
  (o ciclo de publicação) e o `references/closing.md` (o visual de síntese como passo 0 do encerramento).
- **Testes:** `tests/test_painel_automatico.py` (23 testes) e `tests/fixtures/tev1/`, das cinco rodadas da reunião;
  as chamadas antigas ao `wait_round.main` ganharam `--no-panel`.

## A avaliação

Pela `skill-creator`, revisar uma skill existente é snapshot, edição e comparação com a versão antiga. A mudança é de
script, com saída determinística, e a medida foram os testes: 300 OK no snapshot, 323 OK depois
(`PYTHONDONTWRITEBYTECODE=1 python3 -I -m unittest discover -s .claude/skills/meeting-runner/scripts/tests -p 'test_*.py'`).
A corrida com personas reais, com e sem a skill, ficou de fora: abre sessões de verdade e gasta cota. Prova de uso: o
`panel.py sintese` regerou, a partir dos dados gravados da reunião do `tev1`, o visual que a coordenação tinha feito à
mão, conferido por PNG a 736 px.

O revisor independente deu 80 à primeira versão: o `sintese` não publicava como a skill o descrevia, a janela perdia a
data, o `--once` gerava PNG, uma frase do `narration.md` contradizia o código e três mutações sobreviviam aos testes.
Todos corrigidos; o ponto que ele levou à rodada — o `publish` pedia a janela que o `wait_round` não imprimia — entrou
pela opção recomendada dele, a linha `janela:`, porque executa a R10.1 (o painel sai do script, não da memória).

## O que ficou

- [O brza note commit grava o custo da coordenação no worklog de cada persona](../../../tools-kit/work/issues/brza-note-commit-grava-o-custo-da-coordenacao-no-worklog-de-persona.md)
  — a issue ao `tools-kit` (`edeb58e`), porque o dado gravado continua errado.
- O painel no `--source marker` do `wait_round.py` não foi feito (modo legado sem Dispatch); quem o usar publica com
  `panel.py publish`.

## Custo da tarefa

Corrido 25 min — agente 10 min, quem pediu 15 min, pausa 0 s · US$ 11,28 (turnos 7,06, subagentes 4,22) · CPU 35,89 s do `claude` e 339,81 s dos comandos, RSS até 542 MB · 8 turnos, 1 sessão · até 22:32 de 2026-11-09, pelo `brza note commit`
