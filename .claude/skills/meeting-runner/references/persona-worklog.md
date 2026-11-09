# O esqueleto do worklog da persona

A coordenação cria o arquivo **antes** de abrir a sessão. Cada persona só acrescenta rodadas no fim.
Caminho: o molde `worklog` do manifesto (`work/worklogs/AAAA-MM-DD-<reuniao>-<slug>.md`).

```markdown
---
scope:
  - ‹repositório do tema›
tags:
  - ‹tag›
---

# Reunião ‹tema›: a participação de ‹Nome›, ‹o arquétipo›

O pedido de Anderson, em ‹AAAA-MM-DD›, na sessão da coordenação (`‹sessão›`): "‹resposta literal do gate›". Este é o
registro de **‹Nome›** — persona ‹o arquétipo›, no ‹runtime› ‹modelo› ‹esforço› —, aberto pela coordenação. A pauta e as
regras estão no briefing da reunião; cada rodada é uma seção abaixo, acrescentada no fim do arquivo.

## O que se fez
```

Sem `## O que ficou` e sem `## Fora do workspace`: nas seis personas da Carvão as duas seções ficaram vazias ("Nada.") e
só pediam a regra do marcador dentro ou fora delas. O frontmatter e o H1 seguem a norma de `work/worklogs/`; o
`notes-checker` confere o resto depois, quando a coordenação roda `brza note commit`.

O arquivo termina, em toda rodada, na linha `<!-- fim-rodada-N -->`. Se o esqueleto tivesse uma seção depois de
`## O que se fez`, a "última linha do arquivo" seria dela e o marcador cairia no meio: por isso a rodada é acrescentada
no **fim** e o esqueleto acaba em `## O que se fez`.
