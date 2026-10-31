---
name: feedback-custo-de-symlink-com-confianca
description: Errei o custo do symlink para arquivo que o runtime só roda depois de confiado (hooks.json do Codex); e não renumere itens D que as rodadas já citam
metadata:
  type: feedback
---

O `.codex/hooks.json` ligado por symlink saiu barato no meu rascunho, porque o `.claude/agent-memory` já ia assim. Não
rodou: o espião não gravou nada, e o `/hooks` de Anderson não deixou `hooks.state` (PLN-004, R8.1, 2026-10-31). Anderson
escolheu copiar o arquivo, aceitando que a cópia envelhece.

**Why:** arquivo que o runtime confia por caminho e hash não se comporta como arquivo comum; o que vale para a memória
e para as regras não vale para o hook. O `agy`, no mesmo teste, seguiu o link do hook sem pedir confiança.

**How to apply:** quando a alternativa recomendada liga por symlink um arquivo sujeito a confiança (hooks, configuração
de projeto), marque "a conferir" no custo e ponha a sonda antes da rodada. Outra coisa: ao enxugar um Desenho, não
renumere os itens `D` depois que uma rodada já os citou (a R7.4 cita o D14); funda o conteúdo e deixe o número. Ver
também [[feedback-medir-antes-de-desenhar]].
