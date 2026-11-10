# Os consultores — por `Agent` ou em sessões

O consultor existe para tirar leitura pesada e rascunho do contexto da coordenação, e para trazer alternativas que a
coordenação sozinha não veria. Ele devolve; não grava o plano e não decide.

## O laço por `Agent` — o padrão

Leitura pesada e rascunho vão a um subagente por papel: `collector` para o Terreno e a coleta, `designer` para os itens
`D` e as alternativas, `reviewer` para a revisão. O laço é sempre o mesmo:

1. **Chame o subagente** com o pedido — a operação, o repositório alvo, o que as rodadas já decidiram, citado como foi
   respondido, e o que se espera de volta —, os caminhos do plano e **uma entrega por chamada**. O formato da devolução
   vai no primeiro pedido: correção mandada no meio da execução não é aplicada. Caminho de scratch com espaço vai por um
   link curto em `/private/tmp/` (o `CLAUDE.md` diz por quê).
2. **Ele devolve**, na ordem e só o que o pedido pediu: **levantamento** com cada fato e a fonte (`arquivo:linha`, aberta
   nesta execução); **pontos para rodada**, cada ponto sem lastro já como pergunta com opções, `Custo: … Se paga: …` em
   toda opção; **rascunho**, com cada escolha sem lastro marcada como ponto, nunca como texto final; **arquivos
   essenciais** (de 5 a 10); e **o que rodou e o que deu**.
3. **Faça a rodada** com os pontos, aqui, e grave-a pelo `round_log.py`.
4. **Retome o mesmo subagente** (`SendMessage`, com o contexto que ele já tem) com as respostas, enquanto sobrar ponto,
   até cinco rodadas por lacuna. Com zero pontos ele devolve "pronto para gravar", e quem grava é a coordenação.

**Consultores em paralelo, com foco**: bifurcação com 3 ou mais alternativas defensáveis vai a três consultores — mudança
mínima, arquitetura limpa, equilíbrio —, cada um devolvendo uma alternativa com custo, quando se paga e o que reabre, e o
ataque às outras duas.

## Em sessões — só na decisão cara

**O gatilho (PLN-021/R2.3)**: as duas condições valem — **3 ou mais alternativas defensáveis** e **escolha cara de
reverter**: contrato entre partes (API, protocolo, CLI que outro repositório chama), formato de dado gravado (manifesto,
frontmatter, esquema), norma. Também quando Anderson pede. No resto, `Agent`.

O porquê: o `Agent` roda no mesmo modelo da família da coordenação e custa ~US$ 2,8 por `designer`; a sessão em outro
runtime custa tempo de abertura e cota, e só se paga quando a diversidade de modelo pode mudar a recomendação numa
decisão que custaria refazer.

**Antes de abrir, narre o gatilho numa linha**: "D4: 3 alternativas, formato do manifesto (dado gravado) → consultores
em sessão (R2.3)". Sem essa linha, Anderson não sabe por que a rodada demora mais.

```bash
python3 -I .claude/skills/plan-runner/scripts/consult.py open PLN-NNN D<n> --brief .sessions/pln-nnn/D<n>/brief.md
python3 -I .claude/skills/plan-runner/scripts/consult.py wait PLN-NNN D<n>
python3 -I .claude/skills/plan-runner/scripts/consult.py table PLN-NNN D<n>
python3 -I .claude/skills/plan-runner/scripts/consult.py close PLN-NNN D<n>
```

- **O `brief.md`**, que a coordenação escreve: o Terreno (ou o caminho dele), os casos sobre os quais comparar, as
  rodadas citadas, o artefato que cada alternativa precisa escrever. O `open` acrescenta o foco de cada consultor, a
  forma do arquivo e o protocolo de fim, e começa o prompt com "Você é consultor do Desenho de …", que impede o
  consultor de acionar esta skill.
- **O roster padrão** (PLN-021/R4.3, recomendada, a confirmar): Claude Opus `high` na arquitetura limpa, Codex no maior
  esforço na mudança mínima, Grok no equilíbrio. `--roster <arquivo.json>` troca; runtime acima de 55% da cota
  (`brza quota --json`) não entra, e o `fallback` do roster o substitui.
- **Cada consultor grava só** `.sessions/pln-nnn/D<n>/<foco>.md`: a tese, o "Como fica" da alternativa, `Custo:` ·
  `Se paga:` · `Reabre:` sobre os casos dados, o ataque às outras duas, o que enfraquece a própria, e a última linha
  `<!-- fim-D<n>: <foco> -->`. Abre no worktree do workspace, e lê o resto só para consulta.
- **O `table`** junta os três arquivos numa tabela lado a lado (custo, se paga, reabre, risco × os focos), em Markdown
  para a mensagem e em `::orca-visual`.

## A rodada dos consultores

A mensagem traz, nesta ordem: a tabela lado a lado; **a argumentação integral de cada consultor** — tese, fatos com
fonte, ataque, o que enfraquece a própria, custo e se paga —; a reavaliação da coordenação, com a recomendação e o
argumento que sobreviveu ao ataque; e a pergunta em texto, no formato sem a ferramenta. Anderson recusou, em 2026-11-03,
a rodada que trazia só a síntese ("não vi os argumentos, mostre a argumentação completa no chat"); a reunião com
personas é a exceção, e a regra dela é da `meeting-runner`.

**Quem escolhe é Anderson.** Nenhum consultor, nem a coordenação, grava a alternativa como decidida antes da resposta.
