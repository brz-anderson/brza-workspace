---
name: meeting-plan-review-patterns
description: Onde erram os planos que a coordenação monta a partir de rodadas de personas (reunião simulada), e quais hipóteses de revisão costumam cair
metadata:
  type: project
---

Nos planos sintetizados de rodadas de personas (a reunião Carvão em Brasa, 2026-11-07, no `playground`), o erro se
repete em cinco lugares:

- **A coluna de confiança contradiz a regra que o próprio plano declara** (índice ≥ 70 e evidência → alta). Refaça
  linha a linha; na v2, três de treze ainda violavam, e a regra nova ("a confiança vem da R5") apontava para notas
  que não existem por recomendação.
- **Atribuição pela posição de uma rodada antiga**, e não pelo voto final (quem "prefere" X já tinha votado Y).
- **Valor trocado entre o voto e o plano, com o mesmo placar** (votaram `#FF75A0`, o plano diz `#FF7AA2`); e o
  "conferido por duas fontes" vale para o valor antigo, que é o que o script audita.
- **Horas herdadas de quem estimou, com escopo novo enfiado na mesma fase.** Compare a fase do plano com o "ficou de
  fora" de quem estimou.
- **A "confiança se cada uma tivesse a mudança"** soma mudanças que o plano não deu, ou deu pela metade.

- **A cada rodada nova, a atribuição do voto escorrega de novo.** Na v3, a Faísca foi contada na variante oposta à
  que votou. Refaça o placar de toda decisão nova pelo texto literal do worklog.
- **A correção pega o caso apontado e deixa o irmão.** O placeholder foi corrigido, e o texto secundário, que usa a
  mesma variável, não foi. Ao conferir uma correção, procure quem compartilha a causa.

- **Taxa de base medida pelo autor, e não pelo repositório** (reunião CI no chat, 2026-11-09): `gh search prs
  --author=@me` deu 1 PR, e o `--owner` do mesmo dono mostrou mais 7 de uma conta de agente (`fixfy-claude`). O
  "zero eventos" e o gatilho de reabertura herdam o ponto cego. Refaça a taxa por `--owner`, por `gh auth status`
  (contas extras) e pelo `on:` dos workflows (push filtrado em `main` num fork cuja default é `master` dá zero runs).
- **Custo herdado de outra persona ou runtime:** a "rodada extra" com Grok e Antigravity foi orçada pelo custo do
  Claude da R1, e o `estado-rN.json` não tem o custo deles (`custo_usd: null`).
- **Linha citada da issue de origem desliza** (a proposta citou 46–50, o pedido está em 62–66); confira toda faixa.

Como achar rápido: extrair as tabelas de voto dos worklogs por regex e recalcular, e comparar cada HEX do plano com
as entradas fixas do script de auditoria.

**Why:** a coordenação reescreve entre rodadas, e o número antigo sobra numa célula.
**How to apply:** em toda revisão de síntese de reunião, faça essas cinco conferências antes de ler o mérito.

**Hipóteses que caíram (não gastar confiança alta nelas):**

- "Índice ou acordo mal calculado": a aritmética bateu nos 15 casos. Vale refazer porque é barato, mas espere que
  bata.
- "Referência de arquivo e linha errada" quando vem das personas que leram o código (Lenha, Tição): todas as que
  conferi existiam e diziam o que o plano afirmava. O erro estava no *recorte*: um intervalo de linhas que cobria
  duas regras CSS.

- "Fatos M marcados [medido] pela coordenação estão errados": na reunião CI no chat, M1–M8 conferiram todos; o erro
  estava no recorte (taxa por autor) e na citação (`:84` cobre só metade do M8).

**Quando o pedido manda não ler as confianças antes de dar o número**, elas podem estar no próprio alvo (a seção "A
confiança do plano") e no `estado-rN.json`: leia o alvo por faixa de linhas e não abra o estado inteiro; se viu,
declare.

**O arquivo alvo pode mudar no meio da revisão** (v1 → v2 em 5 min). Releia e confira o mtime antes de devolver.
Diga qual versão revisou e o que a nova já corrigiu.

Ver também [[brza-studio-contrast-review]].
